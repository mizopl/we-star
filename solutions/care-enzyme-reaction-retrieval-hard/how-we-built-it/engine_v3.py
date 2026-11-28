#!/usr/bin/env python3
"""engine_v3.py — CARE Task 2 Zero-Leakage Conservation-Rule + Per-Reaction Rule-Gap Gated Multi-View Engine.

Upgrades `engine_v2.py` with:
  1) Per-Reaction `rule_unseen_gap` gate (`allow = clip((-gap - 0.05)/0.15, 0, 1)`): zero corruption on unseen-EC3
     reactions where rules pick an unseen EC3 (`gap >= 0`), while cleanly unlocking full retrieval on seen-EC3s (`gap <= -0.20`).
  2) Multi-View Seen-EC3 + Text-Contrastive Ensemble (Full CosineNet + Reaction-Center-Only CosineNet +
     Contrastive `S_123` E123 aligner + `S_attr` IUBMB concept aligner + Multi-FP Soft-kNN similarity).
  3) Preserves `engine_v2` intra-EC3 `L4` (`DedicatedSubL4Net` + `W4_rule` + `MetaboliteMatcher` + `prot_full_256`) with
     strictly non-positive `within_ec3` centering (`0.000%` L1/L2/L3 interference).
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

import engine_v2 as e2  # noqa: E402
import features_v2 as f2  # noqa: E402
import metabolite_matcher as mm  # noqa: E402
import rules_v2 as r2  # noqa: E402


def make_rc_only_feats(f_dict: dict, prefix: str) -> np.ndarray:
    """Reaction-center-only features excluding radius-2 substrate scaffold bits."""
    nf = len(f2.FLAG_NAMES)
    end_at = nf + 2 * len(f2.FG_NAMES) + len(f2.ATOM_LIST)
    mech = f_dict[f"{prefix}mech"].astype(np.float32).copy()
    mech[:, nf:end_at] = np.sign(mech[:, nf:end_at]) * np.log1p(np.abs(mech[:, nf:end_at]))
    return np.hstack([
        f_dict[f"{prefix}rxn_diff_r1"].astype(np.float32),
        f_dict[f"{prefix}rxn_ap_diff"].astype(np.float32) * 0.85,
        f_dict[f"{prefix}rxn_maccs_diff"].astype(np.float32) * 0.85,
        mech * 0.40,
    ]).astype(np.float32)


def build_text_spaces_v3(ec_df: pd.DataFrame):
    bge = np.load(CACHE_DIR / "ec_bge_spaces_v2.npz")
    B_l2 = bge["B_l2"].astype(np.float32)
    B_l3 = bge["B_l3"].astype(np.float32)
    B_l4 = bge["B_l4"].astype(np.float32)

    from scipy.sparse import hstack
    w123 = TfidfVectorizer(ngram_range=(1, 2), min_df=1, sublinear_tf=True)
    c123 = TfidfVectorizer(analyzer="char_wb", ngram_range=(3, 5), min_df=2, sublinear_tf=True)
    X123 = hstack([w123.fit_transform(ec_df["l123"]) * 1.3, c123.fit_transform(ec_df["l123"]) * 0.7])
    Et123 = normalize(TruncatedSVD(n_components=256, random_state=42).fit_transform(X123), norm="l2").astype(np.float32)
    E123 = normalize(np.hstack([B_l3 * 1.1, B_l2 * 0.6, Et123]), norm="l2").astype(np.float32)

    w4 = TfidfVectorizer(ngram_range=(1, 2), min_df=1, sublinear_tf=True)
    c4 = TfidfVectorizer(analyzer="char_wb", ngram_range=(3, 5), min_df=2, sublinear_tf=True)
    X4 = hstack([w4.fit_transform(ec_df["l4"]) * 1.4, c4.fit_transform(ec_df["l4"]) * 0.7])
    E4_tfidf = normalize(TruncatedSVD(n_components=256, random_state=42).fit_transform(X4), norm="l2").astype(np.float32)
    l4_empty = (ec_df["l4"].str.len() == 0).values
    E4_tfidf[l4_empty] = 0.0
    E4 = normalize(np.hstack([B_l4 * 1.15, E4_tfidf]), norm="l2").astype(np.float32)
    E4[l4_empty] = 0.0

    stop = ["of", "the", "and", "as", "on", "to", "in", "with", "group", "groups", "acting",
            "from", "other", "related", "substances", "or", "for", "but", "not", "bonds", "bond"]
    v_l2 = TfidfVectorizer(ngram_range=(1, 2), min_df=4, max_features=140, binary=True,
                           token_pattern=r"(?u)\b[a-zA-Z0-9][a-zA-Z0-9\-+\(\)]{1,}\b", stop_words=stop)
    v_l3 = TfidfVectorizer(ngram_range=(1, 2), min_df=4, max_features=220, binary=True,
                           token_pattern=r"(?u)\b[a-zA-Z0-9][a-zA-Z0-9\-+\(\)]{1,}\b", stop_words=stop)
    A_all = np.hstack([
        v_l2.fit_transform(ec_df["l2"]).toarray(),
        v_l3.fit_transform(ec_df["l3_clean"]).toarray(),
    ]).astype(np.float32)
    return E123, E4, (~l4_empty).astype(np.float32), A_all


def run_split(split: str, n_seeds: int = 3) -> None:
    torch.set_num_threads(1)
    t0 = time.perf_counter()
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    ec_df = f2.prepare_denoised_text2ec()
    ec_list = ec_df["ec"].tolist()
    ec_to_idx = {e: i for i, e in enumerate(ec_list)}
    ec3_groups = [g.index.values.astype(np.int64) for _, g in ec_df.groupby("ec3")]
    E123, E4, l4_v, A_all = build_text_spaces_v3(ec_df)
    A_norm = normalize(A_all, norm="l2").astype(np.float32)
    prot_emb = np.load(CACHE_DIR / "prot_full_256.npy").astype(np.float32)
    W_rule, W4_rule = r2.build_rule_matrices_v2(ec_df)
    W_met = mm.build_ec_metabolite_matrix(ec_df)

    tr_df = pd.read_csv(DATA_ROOT / "splits" / "task2" / f"{split}_reaction_train.csv")
    te_df = pd.read_csv(DATA_ROOT / "splits" / "task2" / f"{split}_reaction_test.csv")
    f_dict = e2.load_or_build_feats(split)

    # STRICT ANTI-LEAKAGE: test reads ONLY `Reaction` SMILES
    te_rxns = te_df["Reaction"].astype(str).tolist()
    xr_tr, xs_tr, x1_tr, _ = e2.make_inputs(f_dict, "tr_")
    xr_te, xs_te, x1_te, mech_te_raw = e2.make_inputs(f_dict, "te_")
    xrc_tr = make_rc_only_feats(f_dict, "tr_")
    xrc_te = make_rc_only_feats(f_dict, "te_")
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

    # 1. Balanced LogisticRegression EC1 + Multi-FP Nearest-Neighbor EC3 max similarity
    p1_lr = LogisticRegression(C=0.45, max_iter=350, class_weight="balanced", solver="lbfgs").fit(x1_tr, tr_ec1).predict_proba(x1_te)
    nn_tr = normalize(np.hstack([
        f_dict["tr_rxn_diff_r2"].astype(np.float32),
        f_dict["tr_sub_diff_r2"].astype(np.float32) * 0.60,
        f_dict["tr_rxn_ap_diff"].astype(np.float32) * 0.45,
    ]), norm="l2").astype(np.float32)
    nn_te = normalize(np.hstack([
        f_dict["te_rxn_diff_r2"].astype(np.float32),
        f_dict["te_sub_diff_r2"].astype(np.float32) * 0.60,
        f_dict["te_rxn_ap_diff"].astype(np.float32) * 0.45,
    ]), norm="l2").astype(np.float32)
    S_all_tr = nn_te @ nn_tr.T
    S_nn_ec3 = np.zeros((len(te_rxns), len(ec_list)), dtype=np.float32)
    seen_ec3_max = {c3: np.max(S_all_tr[:, idxs], axis=1) for c3, idxs in ec3_to_rows.items()}
    for j, c3 in enumerate(ec_to_ec3):
        if c3 in seen_ec3_max:
            S_nn_ec3[:, j] = seen_ec3_max[c3]

    Xtr, Xrct, Xts = torch.from_numpy(xr_tr), torch.from_numpy(xrc_tr), torch.from_numpy(xs_tr)
    Y1t, Y2t, Y3t = torch.from_numpy(tr_ec1), torch.from_numpy(y2_tr), torch.from_numpy(y3_tr)
    E123_t, E4_t, Ep_t = torch.from_numpy(E123), torch.from_numpy(E4), torch.from_numpy(prot_emb)
    l4_vt = torch.from_numpy(l4_v)
    A_t = torch.from_numpy((A_all > 0).astype(np.float32))
    pr_a = np.clip((A_all[tr_y] > 0).mean(0), 0.005, 0.995)
    pw_a = torch.from_numpy(np.clip((1.0 - pr_a) / pr_a, 1.0, 15.0).astype(np.float32))

    seeds = [42, 137, 2026][:n_seeds]
    n_te = len(te_rxns)
    p1_mlp_acc = np.zeros_like(p1_lr)
    S123_acc = np.zeros((n_te, len(ec_list)), dtype=np.float32)
    Sattr_acc = np.zeros((n_te, len(ec_list)), dtype=np.float32)
    S4_acc = np.zeros((n_te, len(ec_list)), dtype=np.float32)
    Sp_acc = np.zeros((n_te, len(ec_list)), dtype=np.float32)
    pf_acc = np.zeros((n_te, len(seen_ec3s)), dtype=np.float32)
    prc_acc = np.zeros((n_te, len(seen_ec3s)), dtype=np.float32)
    ps2_acc = np.zeros((n_te, len(seen_ec2s)), dtype=np.float32)

    for sd in seeds:
        np.random.seed(sd); torch.manual_seed(sd); rng = np.random.default_rng(sd)

        # (a) Full CosineNet
        full_net = e2.CosineClassNet(xr_tr.shape[1], len(seen_ec3s), hid=512)
        of = torch.optim.AdamW(full_net.parameters(), lr=1.8e-3, weight_decay=3e-2)
        full_net.train()
        for _ in range(28):
            perm = torch.randperm(len(Xtr))
            for b0 in range(0, min(len(Xtr), 256 * 32), 256):
                b = perm[b0 : b0 + 256]
                lg, _ = full_net(Xtr[b])
                loss = F.cross_entropy(lg, Y3t[b], label_smoothing=0.05)
                of.zero_grad(); loss.backward(); of.step()
            b_c3 = rng.choice(seen_ec3s, size=min(128, len(seen_ec3s)), replace=False)
            rb = torch.from_numpy(np.array([rng.choice(ec3_to_rows[c]) for c in b_c3], dtype=np.int64))
            lg, _ = full_net(Xtr[rb])
            loss = F.cross_entropy(lg, Y3t[rb], label_smoothing=0.05)
            of.zero_grad(); loss.backward(); of.step()

        # (b) Reaction-Center-Only CosineNet
        rc_net = e2.CosineClassNet(xrc_tr.shape[1], len(seen_ec3s), hid=512)
        orc = torch.optim.AdamW(rc_net.parameters(), lr=1.8e-3, weight_decay=3e-2)
        rc_net.train()
        for _ in range(28):
            perm = torch.randperm(len(Xrct))
            for b0 in range(0, min(len(Xrct), 256 * 32), 256):
                b = perm[b0 : b0 + 256]
                lg, _ = rc_net(Xrct[b])
                loss = F.cross_entropy(lg, Y3t[b], label_smoothing=0.05)
                orc.zero_grad(); loss.backward(); orc.step()
            b_c3 = rng.choice(seen_ec3s, size=min(128, len(seen_ec3s)), replace=False)
            rb = torch.from_numpy(np.array([rng.choice(ec3_to_rows[c]) for c in b_c3], dtype=np.int64))
            lg, _ = rc_net(Xrct[rb])
            loss = F.cross_entropy(lg, Y3t[rb], label_smoothing=0.05)
            orc.zero_grad(); loss.backward(); orc.step()

        # (c) Contrastive S_123 + S_attr + EC1 Trunk
        txt_net = nn.Sequential(
            nn.Linear(xr_tr.shape[1], 512), nn.LayerNorm(512), nn.GELU(), nn.Dropout(0.35),
            nn.Linear(512, 384), nn.LayerNorm(384), nn.GELU(), nn.Dropout(0.25),
        )
        h1 = nn.Linear(384, 7)
        h123 = nn.Linear(384, E123.shape[1])
        ha = nn.Linear(384, A_all.shape[1])
        ot = torch.optim.AdamW(list(txt_net.parameters()) + list(h1.parameters()) + list(h123.parameters()) + list(ha.parameters()), lr=1.5e-3, weight_decay=3e-2)
        txt_net.train()
        for _ in range(30):
            for _ in range(26):
                b_c3 = rng.choice(seen_ec3s, size=min(128, len(seen_ec3s)), replace=False)
                rb = np.array([rng.choice(ec3_to_rows[c]) for c in b_c3], dtype=np.int64)
                ru = rng.integers(0, len(tr_y), size=64)
                rows = np.concatenate([rb, ru])
                h = txt_net(Xtr[rows])
                ye = torch.from_numpy(tr_y[rows])
                z123 = F.normalize(h123(h), dim=-1)
                tb = E123_t[ye]
                lg = 18.0 * (z123 @ tb.T); lb = torch.arange(len(rows))
                loss = (
                    0.8 * F.cross_entropy(h1(h), Y1t[rows])
                    + 1.3 * F.binary_cross_entropy_with_logits(ha(h), A_t[ye], pos_weight=pw_a)
                    + 0.5 * (F.cross_entropy(lg, lb) + F.cross_entropy(lg.T, lb))
                    + 1.2 * (1.0 - (z123 * tb).sum(-1)).mean()
                )
                ot.zero_grad(); loss.backward(); ot.step()

        # (d) Seen-EC2 CosineNet
        s2_net = e2.CosineClassNet(xr_tr.shape[1], len(seen_ec2s), hid=384)
        os2 = torch.optim.AdamW(s2_net.parameters(), lr=1.8e-3, weight_decay=2.5e-2)
        s2_net.train()
        for _ in range(18):
            perm = torch.randperm(len(Xtr))
            for b0 in range(0, min(len(Xtr), 256 * 24), 256):
                b = perm[b0 : b0 + 256]
                lg, _ = s2_net(Xtr[b])
                loss = F.cross_entropy(lg, Y2t[b], label_smoothing=0.05)
                os2.zero_grad(); loss.backward(); os2.step()

        # (e) Dedicated Intra-EC3 Substrate L4 Net
        sub_net = e2.DedicatedSubL4Net(xs_tr.shape[1], E4.shape[1], prot_emb.shape[1])
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
                    lg4 = sc4 * (z4v @ tb4.T); lb4 = torch.arange(len(z4v))
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

        full_net.eval(); rc_net.eval(); txt_net.eval(); s2_net.eval(); sub_net.eval()
        with torch.no_grad():
            pf_acc += F.softmax(full_net(torch.from_numpy(xr_te))[0], dim=-1).numpy() / len(seeds)
            prc_acc += F.softmax(rc_net(torch.from_numpy(xrc_te))[0], dim=-1).numpy() / len(seeds)
            ht = txt_net(torch.from_numpy(xr_te))
            p1_mlp_acc += F.softmax(h1(ht), dim=-1).numpy() / len(seeds)
            S123_acc += e2.zscore_rows((F.normalize(h123(ht), dim=-1) @ E123_t.T).numpy()) / len(seeds)
            Sattr_acc += e2.zscore_rows((normalize(torch.sigmoid(ha(ht)).numpy(), norm="l2").astype(np.float32) @ A_norm.T)) / len(seeds)
            ps2_acc += F.softmax(s2_net(torch.from_numpy(xr_te))[0], dim=-1).numpy() / len(seeds)
            z4, zp = sub_net(torch.from_numpy(xs_te))
            S4_acc += e2.zscore_rows((z4 @ E4_t.T).numpy()) / len(seeds)
            Sp_acc += e2.zscore_rows((zp @ Ep_t.T).numpy()) / len(seeds)

    p1_mix = 0.60 * p1_lr + 0.40 * p1_mlp_acc
    S_ec1 = np.log(np.clip(p1_mix[:, [int(e) - 1 for e in ec_df["ec1"]]], 1e-4, 1.0))
    S_rule = (mech_te_raw @ W_rule.T).astype(np.float32)
    S_4_rule = (mech_te_raw @ W4_rule.T).astype(np.float32)
    S_met = (X_met_te @ W_met.T).astype(np.float32)
    Sr_g = e2.scale_rule_globally(S_rule)

    S_pf = np.zeros((n_te, len(ec_list)), dtype=np.float32)
    S_prc = np.zeros((n_te, len(ec_list)), dtype=np.float32)
    for j, c3 in enumerate(ec_to_ec3):
        if c3 in c3_map:
            idx3 = c3_map[c3]
            S_pf[:, j] = pf_acc[:, idx3]
            S_prc[:, j] = prc_acc[:, idx3]
    S_seen2 = np.zeros((n_te, len(ec_list)), dtype=np.float32)
    for j, c2 in enumerate(ec_to_ec2):
        if c2 in c2_map:
            S_seen2[:, j] = ps2_acc[:, c2_map[c2]]

    # Per-reaction unseen-vs-seen Rule Consistency Gate (0 test peeking; 0 batch stats!)
    is_seen_col = np.array([c in c3_map for c in ec_to_ec3])
    rule_unseen_gap = Sr_g[:, ~is_seen_col].max(axis=1) - Sr_g[:, is_seen_col].max(axis=1)
    allow = np.clip((-rule_unseen_gap - 0.03) / 0.17, 0.0, 1.0)[:, None]

    base = (
        Sr_g
        + (1.35 + 0.65 * allow) * e2.zscore_rows(S_ec1)
        + allow * (
            0.85 * S123_acc
            + 0.85 * Sattr_acc
            + 12.0 * (0.55 * S_pf + 0.45 * S_prc)
            + 2.5 * S_seen2
            + 3.0 * np.maximum(0.0, S_nn_ec3 - 0.62)
        )
    )

    S4_comb = 1.05 * S4_acc * l4_v[None, :] + 0.40 * e2.zscore_rows(S_4_rule) + 0.50 * S_met + 0.28 * Sp_acc
    L4_np = e2.nonpos_within_ec3(S4_comb, ec3_groups)
    fused_final = base + 0.05 * L4_np

    order = np.argsort(-fused_final, axis=1)
    ec_arr = np.array(ec_list, dtype=object)
    ranked_ecs = ec_arr[order]
    rank_df = pd.DataFrame(ranked_ecs, columns=[str(i) for i in range(len(ec_list))])
    out_df = pd.concat([te_df.reset_index(drop=True), rank_df], axis=1)

    out_csv = OUT_DIR / f"v3_{split}_reaction_test_results_df.csv"
    out_df.to_csv(out_csv, index=False)

    manifest = {
        "model": f"we_star_CARE_engine_v3_{n_seeds}seed",
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
    man_path = OUT_DIR / f"v3_{split}_provenance.json"
    man_path.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    print(f"[DONE] Saved {out_csv} ({time.perf_counter()-t0:.1f}s) | allow>0={(allow[:,0]>0).mean()*100:.1f}% | allow>0.8={(allow[:,0]>0.8).mean()*100:.1f}%")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--split", choices=["hard", "medium", "easy"], default="medium")
    ap.add_argument("--seeds", type=int, default=3)
    args = ap.parse_args()
    run_split(args.split, n_seeds=args.seeds)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
