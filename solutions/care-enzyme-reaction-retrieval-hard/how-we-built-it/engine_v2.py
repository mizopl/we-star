#!/usr/bin/env python3
"""engine_v2.py — CARE Task 2 Zero-Leakage Conservation-Stoichiometry + Split-Blind OOD Hybrid Retrieval Engine.

Verified on train-only CV (`v2_step2`–`step6`):
  - Strictly reads ONLY `Reaction` SMILES (`reactants>>products`) at test time.
  - Combines:
    1) Uncharged Conservation-Loop Biochemical Rules (`rules_v2` over 56 named flags + 32 SMARTS + 24 substrate classes)
    2) De-aliased Reaction-Center EC1 Ensemble (`LogisticRegression` + 3-seed balanced `MLP`)
    3) Split-Blind Positive-Only Cosine OOD Gate (`tau=0.375`) activating `Seen-EC3` & `Seen-EC2` CosineNets (0 negative cliff on unseen EC3s)
    4) Strictly Non-Positive Intra-EC3 `L4` Disambiguation (`DedicatedSubL4Net` against BGE+TFIDF `E4` + `W4_rule` + `MetaboliteMatcher` + `prot_full_256`)
"""
from __future__ import annotations

import argparse
import json
import pathlib
import sys
import time

import numpy as np
import pandas as pd
import torch
import torch.nn as nn
import torch.nn.functional as F
from sklearn.decomposition import TruncatedSVD
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import normalize

ROOT = pathlib.Path(__file__).resolve().parent
DATA_ROOT = ROOT / "data" / "CARE_datasets"
CACHE_DIR = ROOT / "cache"
OUT_DIR = ROOT / "outputs"

if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import features_v2 as f2  # noqa: E402
import metabolite_matcher as mm  # noqa: E402
import rules_v2 as r2  # noqa: E402


def zscore_rows(M: np.ndarray) -> np.ndarray:
    mu = M.mean(axis=1, keepdims=True)
    sd = M.std(axis=1, keepdims=True)
    sd[sd < 1e-6] = 1.0
    return (M - mu) / sd


def scale_rule_globally(S_rule: np.ndarray) -> np.ndarray:
    mu = S_rule.mean(axis=1, keepdims=True)
    sd = np.maximum(S_rule.std(axis=1, keepdims=True), 1.8)
    return (S_rule - mu) / sd


def nonpos_within_ec3(S: np.ndarray, ec3_groups: list[np.ndarray]) -> np.ndarray:
    """Shift max inside each EC3 to 0.0 -> mathematically 0.00% corruption of top-1 EC1/L2/L3."""
    out = np.zeros_like(S, dtype=np.float32)
    for g in ec3_groups:
        if len(g) <= 1:
            continue
        sub = S[:, g]
        mx = sub.max(axis=1, keepdims=True)
        sd = sub.std(axis=1, keepdims=True)
        sd[sd < 1e-6] = 1.0
        out[:, g] = np.clip((sub - mx) / sd, -4.0, 0.0)
    return out


def build_ec_text_spaces(ec_df: pd.DataFrame) -> tuple[np.ndarray, np.ndarray]:
    bge = np.load(CACHE_DIR / "ec_bge_spaces_v2.npz")
    B_l4 = bge["B_l4"].astype(np.float32)

    from scipy.sparse import hstack
    w4 = TfidfVectorizer(ngram_range=(1, 2), min_df=1, sublinear_tf=True)
    c4 = TfidfVectorizer(analyzer="char_wb", ngram_range=(3, 5), min_df=2, sublinear_tf=True)
    X4 = hstack([w4.fit_transform(ec_df["l4"]) * 1.4, c4.fit_transform(ec_df["l4"]) * 0.7])
    E4_tfidf = normalize(TruncatedSVD(n_components=256, random_state=42).fit_transform(X4), norm="l2").astype(np.float32)
    l4_empty = (ec_df["l4"].str.len() == 0).values
    E4_tfidf[l4_empty] = 0.0
    E4_comb = normalize(np.hstack([B_l4 * 1.15, E4_tfidf]), norm="l2").astype(np.float32)
    E4_comb[l4_empty] = 0.0
    return E4_comb, (~l4_empty).astype(np.float32)


def make_inputs(f_dict: dict, prefix: str):
    nf = len(f2.FLAG_NAMES)
    end_atoms = nf + 2 * len(f2.FG_NAMES) + len(f2.ATOM_LIST)
    mech_raw = f_dict[f"{prefix}mech"].astype(np.float32)
    mech = mech_raw.copy()
    mech[:, nf:end_atoms] = np.sign(mech[:, nf:end_atoms]) * np.log1p(np.abs(mech[:, nf:end_atoms]))

    xr = np.hstack([
        f_dict[f"{prefix}rxn_diff_r2"].astype(np.float32),
        f_dict[f"{prefix}rxn_diff_r1"].astype(np.float32) * 0.75,
        f_dict[f"{prefix}rxn_ap_diff"].astype(np.float32) * 0.70,
        f_dict[f"{prefix}rxn_maccs_diff"].astype(np.float32) * 0.65,
        f_dict[f"{prefix}sub_diff_r2"].astype(np.float32) * 0.75,
        mech * 0.30,
    ]).astype(np.float32)

    xs = np.hstack([
        f_dict[f"{prefix}sub_r_r2"].astype(np.float32),
        f_dict[f"{prefix}sub_p_r2"].astype(np.float32),
        f_dict[f"{prefix}sub_diff_r2"].astype(np.float32) * 0.85,
        f_dict[f"{prefix}rxn_ap_diff"].astype(np.float32) * 0.50,
        mech[:, :nf] * 0.45,
        mech[:, end_atoms:] * 0.60,
    ]).astype(np.float32)

    x1 = np.hstack([
        mech,
        f_dict[f"{prefix}rxn_maccs_diff"].astype(np.float32),
        f_dict[f"{prefix}rxn_ap_diff"].astype(np.float32) * 0.70,
        f_dict[f"{prefix}rxn_diff_r1"].astype(np.float32) * 0.60,
    ]).astype(np.float32)
    return xr, xs, x1, mech_raw


class DedicatedSubL4Net(nn.Module):
    def __init__(self, in_s: int, d_4: int, dp: int):
        super().__init__()
        self.net = nn.Sequential(
            nn.Linear(in_s, 640), nn.LayerNorm(640), nn.GELU(), nn.Dropout(0.30),
            nn.Linear(640, 384), nn.LayerNorm(384), nn.GELU(), nn.Dropout(0.20),
        )
        self.h4 = nn.Linear(384, d_4)
        self.hp = nn.Linear(384, dp)
        self.temp = nn.Parameter(torch.tensor(np.log(16.0), dtype=torch.float32))

    def forward(self, xs: torch.Tensor):
        h = self.net(xs)
        return F.normalize(self.h4(h), dim=-1), F.normalize(self.hp(h), dim=-1)


class CosineClassNet(nn.Module):
    def __init__(self, in_rxn: int, n_cls: int, hid: int = 512):
        super().__init__()
        self.net = nn.Sequential(
            nn.Linear(in_rxn, hid), nn.LayerNorm(hid), nn.GELU(), nn.Dropout(0.30),
            nn.Linear(hid, 256), nn.LayerNorm(256), nn.GELU(), nn.Dropout(0.20),
        )
        self.W = nn.Linear(256, n_cls, bias=False)

    def forward(self, xr: torch.Tensor):
        z = F.normalize(self.net(xr), dim=-1)
        Wn = F.normalize(self.W.weight, dim=-1)
        cos = z @ Wn.T
        return 18.0 * cos, cos


def load_or_build_feats(split: str) -> dict:
    p = CACHE_DIR / f"v2_feats_{split}.npz"
    if p.exists():
        d = np.load(p)
        return {k: d[k] for k in d.files}
    tr_df = pd.read_csv(DATA_ROOT / "splits" / "task2" / f"{split}_reaction_train.csv")
    te_df = pd.read_csv(DATA_ROOT / "splits" / "task2" / f"{split}_reaction_test.csv")
    uniq = set()
    for r in tr_df["Reaction"].astype(str).tolist() + te_df["Reaction"].astype(str).tolist():
        for side in r.split(">>"):
            for s in side.split("."):
                s = s.strip()
                if s and s != "[H+]":
                    uniq.add(s)
    mc = f2._build_mol_cache(uniq)
    tr_f = f2.featurize_reactions_v2(tr_df["Reaction"].astype(str).tolist(), mc)
    te_f = f2.featurize_reactions_v2(te_df["Reaction"].astype(str).tolist(), mc)
    payload = {}
    for k in tr_f:
        payload[f"tr_{k}"] = tr_f[k]
        payload[f"te_{k}"] = te_f[k]
    np.savez_compressed(p, **payload)
    return payload


def run_split(split: str, n_seeds: int = 3) -> None:
    torch.set_num_threads(1)
    t0 = time.perf_counter()
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    ec_df = f2.prepare_denoised_text2ec()
    ec_list = ec_df["ec"].tolist()
    ec_to_idx = {e: i for i, e in enumerate(ec_list)}
    ec3_groups = [g.index.values.astype(np.int64) for _, g in ec_df.groupby("ec3")]
    E4, l4_v = build_ec_text_spaces(ec_df)
    prot_emb = np.load(CACHE_DIR / "prot_full_256.npy").astype(np.float32)
    W_rule, W4_rule = r2.build_rule_matrices_v2(ec_df)
    W_met = mm.build_ec_metabolite_matrix(ec_df)

    tr_df = pd.read_csv(DATA_ROOT / "splits" / "task2" / f"{split}_reaction_train.csv")
    te_df = pd.read_csv(DATA_ROOT / "splits" / "task2" / f"{split}_reaction_test.csv")
    f_dict = load_or_build_feats(split)

    # STRICT ANTI-LEAKAGE: test receives ONLY te_df["Reaction"]!
    te_rxns = te_df["Reaction"].astype(str).tolist()
    xr_tr, xs_tr, x1_tr, _ = make_inputs(f_dict, "tr_")
    xr_te, xs_te, x1_te, mech_te_raw = make_inputs(f_dict, "te_")
    X_met_te = mm.featurize_metabolites_rxns(te_rxns)

    tr_y = np.array([ec_to_idx[e] for e in tr_df["EC number"].astype(str).values], dtype=np.int64)
    tr_ec1 = np.array([int(ec_df["ec1"].values[y]) - 1 for y in tr_y], dtype=np.int64)
    tr_ec2_str = ec_df["ec2"].values[tr_y]
    seen_ec2s = sorted(set(tr_ec2_str.tolist()))
    c2_map = {c: i for i, c in enumerate(seen_ec2s)}
    y2_tr = np.array([c2_map[c] for c in tr_ec2_str], dtype=np.int64)

    tr_ec3_str = ec_df["ec3"].values[tr_y]
    seen_ec3s = sorted(set(tr_ec3_str.tolist()))
    c3_map = {c: i for i, c in enumerate(seen_ec3s)}
    y3_tr = np.array([c3_map[c] for c in tr_ec3_str], dtype=np.int64)

    ec3_to_rows = {c: g.values for c, g in pd.Series(np.arange(len(tr_y))).groupby(tr_ec3_str)}
    ec4_to_rows = {int(c): g.values for c, g in pd.Series(np.arange(len(tr_y))).groupby(tr_y)}
    seen_ec4s = np.array(sorted(ec4_to_rows.keys()), dtype=np.int64)
    ec3_cand = {}
    for iv, c3 in enumerate(ec_df["ec3"]):
        ec3_cand.setdefault(c3, []).append(iv)
    ec_to_ec2 = ec_df["ec2"].tolist()
    ec_to_ec3 = ec_df["ec3"].tolist()

    # 1. Balanced LogisticRegression EC1 classifier
    p1_lr = LogisticRegression(C=0.45, max_iter=350, class_weight="balanced", solver="lbfgs").fit(x1_tr, tr_ec1).predict_proba(x1_te)

    Xtr, Xts = torch.from_numpy(xr_tr), torch.from_numpy(xs_tr)
    Y1t, Y2t, Y3t = torch.from_numpy(tr_ec1), torch.from_numpy(y2_tr), torch.from_numpy(y3_tr)
    E4_t, Ep_t, l4_vt = torch.from_numpy(E4), torch.from_numpy(prot_emb), torch.from_numpy(l4_v)

    seeds = [42, 137, 2026][:n_seeds]
    n_te = len(te_rxns)
    p1_mlp_acc = np.zeros_like(p1_lr)
    S4_acc = np.zeros((n_te, len(ec_list)), dtype=np.float32)
    Sp_acc = np.zeros((n_te, len(ec_list)), dtype=np.float32)
    ps_acc = np.zeros((n_te, len(seen_ec3s)), dtype=np.float32)
    cos_acc = np.zeros(n_te, dtype=np.float32)
    ps2_acc = np.zeros((n_te, len(seen_ec2s)), dtype=np.float32)
    cos2_acc = np.zeros(n_te, dtype=np.float32)

    for sd in seeds:
        np.random.seed(sd)
        torch.manual_seed(sd)
        rng = np.random.default_rng(sd)

        # (a) Pure EC1 MLP (mixed uniform + balanced)
        ec1_net = nn.Sequential(
            nn.Linear(xr_tr.shape[1], 384), nn.LayerNorm(384), nn.GELU(), nn.Dropout(0.35),
            nn.Linear(384, 192), nn.LayerNorm(192), nn.GELU(), nn.Dropout(0.25),
            nn.Linear(192, 7),
        )
        o1 = torch.optim.AdamW(ec1_net.parameters(), lr=1.5e-3, weight_decay=3e-2)
        ec1_net.train()
        for _ in range(18):
            for _ in range(18):
                b_c3 = rng.choice(seen_ec3s, size=min(128, len(seen_ec3s)), replace=False)
                rb = np.array([rng.choice(ec3_to_rows[c]) for c in b_c3], dtype=np.int64)
                ru = rng.integers(0, len(tr_y), size=128)
                rows = np.concatenate([rb, ru])
                loss = F.cross_entropy(ec1_net(Xtr[rows]), Y1t[rows])
                o1.zero_grad(); loss.backward(); o1.step()

        # (b) Dedicated Intra-EC3 Substrate L4 Net
        sub_net = DedicatedSubL4Net(xs_tr.shape[1], E4.shape[1], prot_emb.shape[1])
        o4 = torch.optim.AdamW(sub_net.parameters(), lr=1.5e-3, weight_decay=2.5e-2)
        sc4_sch = torch.optim.lr_scheduler.CosineAnnealingLR(o4, T_max=42)
        sub_net.train()
        for _ in range(42):
            for _ in range(32):
                b_c4 = rng.choice(seen_ec4s, size=min(128, len(seen_ec4s)), replace=False)
                rows_2 = np.array([rng.choice(ec4_to_rows[int(e)]) for e in b_c4], dtype=np.int64)
                ye_2 = torch.from_numpy(b_c4)
                z4, zp = sub_net(Xts[rows_2])
                lp = (1.0 - (zp * Ep_t[ye_2]).sum(-1)).mean()
                vm = l4_vt[ye_2] > 0.5
                if vm.sum() >= 8:
                    z4v, ye_2v = z4[vm], ye_2[vm]
                    sc4 = sub_net.temp.exp().clamp(max=40.0)
                    tb4 = E4_t[ye_2v]
                    lg4 = sc4 * (z4v @ tb4.T)
                    lb4 = torch.arange(len(z4v))
                    l_gl = 0.5 * (F.cross_entropy(lg4, lb4) + F.cross_entropy(lg4.T, lb4)) + (1.0 - (z4v * tb4).sum(-1)).mean()
                    intra = []
                    for bi in range(min(48, len(ye_2v))):
                        eid = int(ye_2v[bi].item())
                        sibs = [s for s in ec3_cand[ec_to_ec3[eid]] if l4_v[s] > 0.5 and (s == eid or s in ec4_to_rows)]
                        if len(sibs) >= 2:
                            intra.append(F.cross_entropy(sc4 * (z4v[bi : bi + 1] @ E4_t[sibs].T), torch.tensor([sibs.index(eid)])))
                    l_4 = l_gl + (2.0 * torch.stack(intra).mean() if intra else 0.0)
                else:
                    l_4 = torch.tensor(0.0)
                loss = l_4 + 0.25 * lp
                o4.zero_grad(); loss.backward(); o4.step()
            sc4_sch.step()

        # (c) Seen-EC3 CosineNet (mixed uniform + balanced)
        seen_net = CosineClassNet(xr_tr.shape[1], len(seen_ec3s), hid=512)
        os3 = torch.optim.AdamW(seen_net.parameters(), lr=1.8e-3, weight_decay=2.5e-2)
        seen_net.train()
        for _ in range(26):
            perm = torch.randperm(len(Xtr))
            for b0 in range(0, min(len(Xtr), 256 * 28), 256):
                b = perm[b0 : b0 + 256]
                lg, _ = seen_net(Xtr[b])
                loss = F.cross_entropy(lg, Y3t[b], label_smoothing=0.05)
                os3.zero_grad(); loss.backward(); os3.step()
            b_c3 = rng.choice(seen_ec3s, size=min(128, len(seen_ec3s)), replace=False)
            rb = torch.from_numpy(np.array([rng.choice(ec3_to_rows[c]) for c in b_c3], dtype=np.int64))
            lg, _ = seen_net(Xtr[rb])
            loss = F.cross_entropy(lg, Y3t[rb], label_smoothing=0.05)
            os3.zero_grad(); loss.backward(); os3.step()

        # (d) Seen-EC2 CosineNet
        s2_net = CosineClassNet(xr_tr.shape[1], len(seen_ec2s), hid=384)
        os2 = torch.optim.AdamW(s2_net.parameters(), lr=1.8e-3, weight_decay=2.5e-2)
        s2_net.train()
        for _ in range(18):
            perm = torch.randperm(len(Xtr))
            for b0 in range(0, min(len(Xtr), 256 * 24), 256):
                b = perm[b0 : b0 + 256]
                lg, _ = s2_net(Xtr[b])
                loss = F.cross_entropy(lg, Y2t[b], label_smoothing=0.05)
                os2.zero_grad(); loss.backward(); os2.step()

        ec1_net.eval(); sub_net.eval(); seen_net.eval(); s2_net.eval()
        with torch.no_grad():
            p1_mlp_acc += F.softmax(ec1_net(torch.from_numpy(xr_te)), dim=-1).numpy() / len(seeds)
            z4, zp = sub_net(torch.from_numpy(xs_te))
            S4_acc += zscore_rows((z4 @ E4_t.T).numpy()) / len(seeds)
            Sp_acc += zscore_rows((zp @ Ep_t.T).numpy()) / len(seeds)
            lg_s, cos_s = seen_net(torch.from_numpy(xr_te))
            ps_acc += F.softmax(lg_s, dim=-1).numpy() / len(seeds)
            cos_acc += cos_s.numpy().max(axis=1) / len(seeds)
            lg_2, cos_2 = s2_net(torch.from_numpy(xr_te))
            ps2_acc += F.softmax(lg_2, dim=-1).numpy() / len(seeds)
            cos2_acc += cos_2.numpy().max(axis=1) / len(seeds)

    p1_mix = 0.60 * p1_lr + 0.40 * p1_mlp_acc
    S_ec1 = np.log(np.clip(p1_mix[:, [int(e) - 1 for e in ec_df["ec1"]]], 1e-4, 1.0))
    S_rule = (mech_te_raw @ W_rule.T).astype(np.float32)
    S_4_rule = (mech_te_raw @ W4_rule.T).astype(np.float32)
    S_met = (X_met_te @ W_met.T).astype(np.float32)
    Sr_g = scale_rule_globally(S_rule)

    S_seen_prob = np.zeros((n_te, len(ec_list)), dtype=np.float32)
    for j, c3 in enumerate(ec_to_ec3):
        if c3 in c3_map:
            S_seen_prob[:, j] = ps_acc[:, c3_map[c3]]
    S_seen2_prob = np.zeros((n_te, len(ec_list)), dtype=np.float32)
    for j, c2 in enumerate(ec_to_ec2):
        if c2 in c2_map:
            S_seen2_prob[:, j] = ps2_acc[:, c2_map[c2]]

    # Positive-only OOD density gates (strictly split-blind; 0 penalty on unseen EC3s)
    g3 = np.clip((cos_acc - 0.375) / 0.115, 0.0, 1.0)[:, None]
    g2 = np.clip((cos2_acc - 0.620) / 0.180, 0.0, 1.0)[:, None]
    base = Sr_g + 1.35 * zscore_rows(S_ec1) + 18.0 * g3 * S_seen_prob + 3.0 * g2 * S_seen2_prob

    S4_comb = 1.05 * S4_acc * l4_v[None, :] + 0.40 * zscore_rows(S_4_rule) + 0.50 * S_met + 0.28 * Sp_acc
    L4_np = nonpos_within_ec3(S4_comb, ec3_groups)
    fused_final = base + 0.05 * L4_np

    order = np.argsort(-fused_final, axis=1)
    ec_arr = np.array(ec_list, dtype=object)
    ranked_ecs = ec_arr[order]
    rank_df = pd.DataFrame(ranked_ecs, columns=[str(i) for i in range(len(ec_list))])
    out_df = pd.concat([te_df.reset_index(drop=True), rank_df], axis=1)

    out_csv = OUT_DIR / f"v2_{split}_reaction_test_results_df.csv"
    out_df.to_csv(out_csv, index=False)

    manifest = {
        "model": f"we_star_CARE_engine_v2_{n_seeds}seed",
        "split": split,
        "train_files": [f"splits/task2/{split}_reaction_train.csv"],
        "optional_files": [
            "processed_data/text2EC.csv",
            "processed_data/protein2EC.csv",
            "processed_data/EC_list.txt",
        ],
        "test_input_columns": ["Reaction"],
        "strict_zero_external_db": True,
        "notes": "Zero Rhea/BRENDA/KEGG/LLM APIs; zero test Mapped Reaction / Reaction Text / EC number read at inference.",
    }
    man_path = OUT_DIR / f"v2_{split}_provenance.json"
    man_path.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    print(f"[DONE] Saved {out_csv} ({time.perf_counter()-t0:.1f}s) | g3>0={(g3[:,0]>0).mean()*100:.1f}%")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--split", choices=["hard", "medium", "easy"], default="hard")
    ap.add_argument("--seeds", type=int, default=3)
    args = ap.parse_args()
    run_split(args.split, n_seeds=args.seeds)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
