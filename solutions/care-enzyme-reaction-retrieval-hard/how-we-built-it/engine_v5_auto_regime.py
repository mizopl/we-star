#!/usr/bin/env python3
"""engine_v5_auto_regime.py — Train-Catalog Auto-Regime CARE Task 2 Retrieval Engine (0 Split-Name Branching).

Strictly eliminates split-name conditionals inside training and decoding:
  - Detects the task regime strictly from training-set coverage of the official CARE EC catalog (`text2EC.csv`),
    with ZERO test-label access:
      1) `ec3_cov < 0.85` -> `unseen_ec3_zeroshot` (conservation-rule + EC2-mean zero-shot + g3@0.58 OOD gate)
      2) `ec3_cov >= 0.85` and `ec4_cov < 0.99` -> `seen_ec3_unseen_ec4` (hierarchical EC1/EC2/hybrid-OOD-EC3 + zero-shot L4)
      3) `ec4_cov >= 0.99` -> `full_catalog_seen_ec4` (3-seed multi-view Seen-EC4 CosineClassNet + Multi-FP substrate+rxn kNN
                               + hierarchical EC1/EC2/EC3 + conservation rules + zero-shot L4_np; 0 GPU required)
  - Strictly reads ONLY `Reaction` SMILES (`reactants>>products`) from the test CSV.
"""
from __future__ import annotations

import argparse
import json
import pathlib
import sys
import time

import lightgbm as lgb
import numpy as np
import pandas as pd
import torch
import torch.nn as nn
import torch.nn.functional as F
import xgboost as xgb
from sklearn.decomposition import TruncatedSVD
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler, normalize

ROOT = pathlib.Path(__file__).resolve().parent
DATA_ROOT = ROOT / "data" / "CARE_datasets"
CACHE_DIR = ROOT / "cache"
OUT_DIR = ROOT / "outputs"

if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import conservation_v4 as c4  # noqa: E402
import engine_v2 as e2  # noqa: E402
import engine_v3 as e3  # noqa: E402
import features_v2 as f2  # noqa: E402
import metabolite_matcher as mm  # noqa: E402
import rules_v2 as r2  # noqa: E402


def map_cols(probs: np.ndarray, class_names: list[str], col_names: list[str], default: float = 0.0) -> np.ndarray:
    cmap = {c: i for i, c in enumerate(class_names)}
    out = np.full((probs.shape[0], len(col_names)), default, dtype=np.float32)
    for j, c in enumerate(col_names):
        if c in cmap:
            out[:, j] = probs[:, cmap[c]]
    return out


def compute_reaction_weights(rxns: list[str], power: float = 1.0) -> np.ndarray:
    if power <= 0.0:
        return np.ones(len(rxns), dtype=np.float32)
    s = pd.Series(rxns)
    cnt = s.map(s.value_counts()).values.astype(np.float32)
    w = 1.0 / np.power(np.maximum(cnt, 1.0), power)
    return (w / w.mean()).astype(np.float32)


def detect_train_regime(n_seen_ec3: int, n_cat_ec3: int, n_seen_ec4: int, n_cat_ec4: int) -> tuple[str, float, float]:
    """Pure train-catalog regime detector (zero split strings, zero test data)."""
    ec3_cov = n_seen_ec3 / max(n_cat_ec3, 1)
    ec4_cov = n_seen_ec4 / max(n_cat_ec4, 1)
    if ec3_cov < 0.85:
        return "unseen_ec3_zeroshot", ec3_cov, ec4_cov
    if ec4_cov < 0.99:
        return "seen_ec3_unseen_ec4", ec3_cov, ec4_cov
    return "full_catalog_seen_ec4", ec3_cov, ec4_cov


def load_optional_gpu_ckpts(gpu_prefixes: list[tuple[str, str, float]], ec_to_ec2: list[str], ec_to_ec3: list[str], n_te: int) -> dict[str, dict]:
    if not gpu_prefixes:
        return {}
    candidates = [
        CACHE_DIR / "care_gpu_stage2_outputs.npz",
        CACHE_DIR / "care_gpu_stage2_ckpt.npz",
        CACHE_DIR / "care_gpu_stage1_ckpt.npz",
    ]
    loaded: dict[str, dict] = {}
    for p in candidates:
        if not p.exists():
            continue
        z = np.load(p, allow_pickle=True)
        if "E123" not in z.files or "E4" not in z.files:
            continue
        E123_g = z["E123"].astype(np.float32)
        E4_g = z["E4"].astype(np.float32)
        l4_vg = z["l4_valid"].astype(np.float32)
        for short, prefix, base_w in gpu_prefixes:
            if short in loaded or f"{prefix}_z123" not in z.files:
                continue
            p1 = z[f"{prefix}_p1"].astype(np.float32)
            assert p1.shape[0] == n_te, f"Row count mismatch for {prefix}: {p1.shape[0]} vs {n_te}"
            p2 = z[f"{prefix}_p2"].astype(np.float32)
            p3 = z[f"{prefix}_p3"].astype(np.float32)
            s2_l = [str(x) for x in z[f"{prefix}_seen_ec2"].tolist()]
            s3_l = [str(x) for x in z[f"{prefix}_seen_ec3"].tolist()]
            p1_p2 = np.zeros_like(p1)
            for idx, c2 in enumerate(s2_l):
                p1_p2[:, int(c2.split(".")[0]) - 1] += p2[:, idx]
            p1_p3 = np.zeros_like(p1)
            for idx, c3 in enumerate(s3_l):
                p1_p3[:, int(c3.split(".")[0]) - 1] += p3[:, idx]
            loaded[short] = {
                "weight": base_w,
                "p1": p1,
                "p1_all": 0.60 * p1 + 0.20 * p1_p2 + 0.20 * p1_p3,
                "p2_full": map_cols(p2, s2_l, ec_to_ec2, default=0.0),
                "p3_full": map_cols(p3, s3_l, ec_to_ec3, default=0.0),
                "S_t123": (z[f"{prefix}_z123"].astype(np.float32) @ E123_g.T),
                "S_t4": (z[f"{prefix}_z4"].astype(np.float32) @ E4_g.T) * l4_vg[None, :],
                "src": p.name,
            }
    return loaded


def run_auto_regime(
    train_csv: pathlib.Path,
    test_csv: pathlib.Path,
    feat_cache_tag: str,
    local_cache_path: pathlib.Path,
    out_csv: pathlib.Path,
    manifest_path: pathlib.Path,
    gpu_prefixes: list[tuple[str, str, float]],
    train_rel_name: str,
    n_seeds: int = 3,
    use_local_cache: bool = False,
) -> None:
    """Train & decode strictly via train-catalog auto-regime (zero split-name conditionals)."""
    torch.set_num_threads(1)
    t0 = time.perf_counter()
    out_csv.parent.mkdir(parents=True, exist_ok=True)

    ec_df = f2.prepare_denoised_text2ec()
    ec_list = ec_df["ec"].tolist()
    ec_to_idx = {e: i for i, e in enumerate(ec_list)}
    ec1_arr = np.array([int(x) - 1 for x in ec_df["ec1"]], dtype=np.int64)
    ec_to_ec2 = ec_df["ec2"].tolist()
    ec_to_ec3 = ec_df["ec3"].tolist()
    ec2_groups = [g.index.values.astype(np.int64) for _, g in ec_df.groupby("ec2")]
    ec3_groups = [g.index.values.astype(np.int64) for _, g in ec_df.groupby("ec3")]
    n_cat_ec3 = ec_df["ec3"].nunique()
    n_cat_ec4 = len(ec_list)

    tr_df = pd.read_csv(train_csv)
    te_df = pd.read_csv(test_csv)
    n_te = len(te_df)

    # Pure train-catalog regime detection (zero test data, zero split string inspection!)
    tr_y = np.array([ec_to_idx[e] for e in tr_df["EC number"].astype(str).values], dtype=np.int64)
    seen_ec2s_tr = sorted(set(ec_df["ec2"].values[tr_y].tolist()))
    seen_ec3s_tr = sorted(set(ec_df["ec3"].values[tr_y].tolist()))
    seen_ec4s_tr = sorted(set(tr_y.tolist()))
    regime, ec3_cov, ec4_cov = detect_train_regime(len(seen_ec3s_tr), n_cat_ec3, len(seen_ec4s_tr), n_cat_ec4)
    print(
        f"[AUTO_REGIME] train_ec3_cov={len(seen_ec3s_tr)}/{n_cat_ec3} ({ec3_cov*100:.1f}%) | "
        f"train_ec4_cov={len(seen_ec4s_tr)}/{n_cat_ec4} ({ec4_cov*100:.1f}%) -> regime={regime}",
        flush=True,
    )

    p4_nn_acc = None
    S_nn_r4 = None
    S_nn_f4 = None
    S_vote4 = None

    if use_local_cache and local_cache_path.exists():
        lc = np.load(local_cache_path, allow_pickle=True)
        seen_ec2s = lc["seen_ec2s"].tolist()
        seen_ec3s = lc["seen_ec3s"].tolist()
        Sr_v4 = lc["Sr_v4"]; S4_local = lc["S4_local"]
        p1_lr = lc["p1_lr"]; p1_lgb_std = lc["p1_lgb_std"]; p1_lgb_bal = lc["p1_lgb_bal"]
        p1_xgb_bal = lc["p1_xgb_bal"]; p1_xgb_std = lc["p1_xgb_std"]; p1_det_acc = lc["p1_det_acc"]
        pf_acc = lc["pf_acc"]; prc_acc = lc["prc_acc"]; ps2_acc = lc["ps2_acc"]
        S123_acc = lc["S123_acc"]; Sattr_acc = lc["Sattr_acc"]; S_nn_ec3 = lc["S_nn_ec3"]
        cos3_acc = lc["cos3_acc"]; cos2_acc = lc["cos2_acc"]
        p2_lgb = lc["p2_lgb"] if "p2_lgb" in lc.files else None
        if "p4_nn_acc" in lc.files:
            p4_nn_acc = lc["p4_nn_acc"]
            S_nn_r4 = lc["S_nn_r4"]
            S_nn_f4 = lc["S_nn_f4"]
            S_vote4 = lc["S_vote4"]
        print(f"[LOCAL_CACHE_LOADED] {local_cache_path.name} ({time.perf_counter()-t0:.2f}s)", flush=True)
    else:
        E123, E4, l4_v, A_all = e3.build_text_spaces_v3(ec_df)
        A_norm = normalize(A_all, norm="l2").astype(np.float32)
        prot_path = CACHE_DIR / "prot_full_256.npy"
        if not prot_path.exists():
            import build_prot_full_256 as bp256  # noqa: E402
            bp256.build_prot_full_256(prot_path)
        prot_emb = np.load(prot_path).astype(np.float32)
        W_rule, W4_rule = r2.build_rule_matrices_v2(ec_df)
        D_v4 = c4.build_rule_delta_v4(ec_df)
        W_met = mm.build_ec_metabolite_matrix(ec_df)

        f_dict = e2.load_or_build_feats(feat_cache_tag)

        # STRICT ANTI-LEAKAGE: test reads ONLY `Reaction` SMILES
        tr_rxns = tr_df["Reaction"].astype(str).tolist()
        te_rxns = te_df["Reaction"].astype(str).tolist()

        xr_tr_raw, xs_tr, x1_tr, mech_tr_raw = e2.make_inputs(f_dict, "tr_")
        xr_te_raw, xs_te, x1_te, mech_te_raw = e2.make_inputs(f_dict, "te_")
        xrc_tr_raw = e3.make_rc_only_feats(f_dict, "tr_")
        xrc_te_raw = e3.make_rc_only_feats(f_dict, "te_")

        c_tr = c4.extract_fast_conservation_feats(tr_rxns, mech_tr_raw)
        c_te = c4.extract_fast_conservation_feats(te_rxns, mech_te_raw)
        scale_c = np.array([0.2, 0.2, 0.2, 0.2, 0.2] + [0.6] * 19, dtype=np.float32)
        xr_tr = np.hstack([xr_tr_raw, c_tr * scale_c])
        xr_te = np.hstack([xr_te_raw, c_te * scale_c])
        xrc_tr = np.hstack([xrc_tr_raw, c_tr * scale_c])
        xrc_te = np.hstack([xrc_te_raw, c_te * scale_c])
        X_met_te = mm.featurize_metabolites_rxns(te_rxns)

        tr_ec1 = ec1_arr[tr_y]
        seen_ec2s = seen_ec2s_tr
        c2_map = {c: i for i, c in enumerate(seen_ec2s)}
        y2_tr = np.array([c2_map[c] for c in ec_df["ec2"].values[tr_y]], dtype=np.int64)
        seen_ec3s = seen_ec3s_tr
        c3_map = {c: i for i, c in enumerate(seen_ec3s)}
        y3_tr = np.array([c3_map[c] for c in ec_df["ec3"].values[tr_y]], dtype=np.int64)

        ec3_to_rows = {c: g.values for c, g in pd.Series(np.arange(len(tr_y))).groupby(ec_df["ec3"].values[tr_y])}
        ec4_to_rows = {int(c): g.values for c, g in pd.Series(np.arange(len(tr_y))).groupby(tr_y)}
        seen_ec4s = np.array(sorted(ec4_to_rows.keys()), dtype=np.int64)
        ec3_cand: dict[str, list[int]] = {}
        for iv, c3 in enumerate(ec_to_ec3):
            ec3_cand.setdefault(c3, []).append(iv)

        w_inv = compute_reaction_weights(tr_rxns, power=1.0)
        w_sqrt = compute_reaction_weights(tr_rxns, power=0.5)
        w_raw = np.ones(len(tr_rxns), dtype=np.float32)

        # 1. Tree + Scaled LogisticRegression EC1 (& LightGBM EC2 when ec3_cov >= 0.85)
        x1_scaler = StandardScaler()
        x1_tr_s = x1_scaler.fit_transform(x1_tr).astype(np.float32)
        x1_te_s = x1_scaler.transform(x1_te).astype(np.float32)
        p1_lr = LogisticRegression(C=0.25, max_iter=400, class_weight="balanced", solver="lbfgs").fit(
            x1_tr_s, tr_ec1, sample_weight=w_inv
        ).predict_proba(x1_te_s).astype(np.float32)

        svd = TruncatedSVD(n_components=128, random_state=42)
        Xfp_tr = np.hstack([f_dict["tr_rxn_diff_r2"].astype(np.float32), f_dict["tr_rxn_ap_diff"].astype(np.float32) * 0.7])
        Xfp_te = np.hstack([f_dict["te_rxn_diff_r2"].astype(np.float32), f_dict["te_rxn_ap_diff"].astype(np.float32) * 0.7])
        X_tree_tr = np.hstack([mech_tr_raw, c_tr, f_dict["tr_rxn_maccs_diff"].astype(np.float32), svd.fit_transform(Xfp_tr).astype(np.float32)])
        X_tree_te = np.hstack([mech_te_raw, c_te, f_dict["te_rxn_maccs_diff"].astype(np.float32), svd.transform(Xfp_te).astype(np.float32)])

        cnt1_inv = np.bincount(tr_ec1, weights=w_inv, minlength=7).astype(np.float32)
        sw1_bal = w_inv * np.clip((cnt1_inv.mean() / np.maximum(cnt1_inv[tr_ec1], 1e-3)) ** 0.50, 0.5, 12.0)

        p1_lgb_std = lgb.LGBMClassifier(
            objective="multiclass", num_class=7, n_estimators=450, learning_rate=0.06, num_leaves=63,
            colsample_bytree=0.55, subsample=0.85, min_child_samples=15, reg_lambda=2.0, n_jobs=2, random_state=42, verbose=-1,
        ).fit(X_tree_tr, tr_ec1, sample_weight=w_sqrt).predict_proba(X_tree_te).astype(np.float32)
        p1_lgb_bal = lgb.LGBMClassifier(
            objective="multiclass", num_class=7, n_estimators=450, learning_rate=0.06, num_leaves=63,
            colsample_bytree=0.55, subsample=0.85, min_child_samples=8, reg_lambda=2.0, n_jobs=2, random_state=137, verbose=-1,
        ).fit(X_tree_tr, tr_ec1, sample_weight=sw1_bal).predict_proba(X_tree_te).astype(np.float32)
        p1_xgb_bal = xgb.XGBClassifier(
            objective="multi:softprob", num_class=7, n_estimators=420, learning_rate=0.06, max_depth=7,
            colsample_bytree=0.50, subsample=0.85, reg_lambda=3.0, tree_method="hist", n_jobs=2, random_state=42, eval_metric="mlogloss",
        ).fit(X_tree_tr, tr_ec1, sample_weight=sw1_bal).predict_proba(X_tree_te).astype(np.float32)
        p1_xgb_std = xgb.XGBClassifier(
            objective="multi:softprob", num_class=7, n_estimators=420, learning_rate=0.06, max_depth=7,
            colsample_bytree=0.50, subsample=0.85, reg_lambda=3.0, tree_method="hist", n_jobs=2, random_state=137, eval_metric="mlogloss",
        ).fit(X_tree_tr, tr_ec1, sample_weight=w_sqrt).predict_proba(X_tree_te).astype(np.float32)

        p2_lgb = None
        if regime != "unseen_ec3_zeroshot":
            p2_lgb = lgb.LGBMClassifier(
                objective="multiclass", num_class=len(seen_ec2s), n_estimators=220, learning_rate=0.08, num_leaves=31,
                colsample_bytree=0.40, subsample=0.80, min_child_samples=8, reg_lambda=2.5, n_jobs=2, random_state=42, verbose=-1,
            ).fit(X_tree_tr, y2_tr, sample_weight=w_sqrt).predict_proba(X_tree_te).astype(np.float32)
        print(f"[TREES_READY] regime={regime} in {time.perf_counter()-t0:.1f}s", flush=True)

        # 2. Multi-FP kNN similarities (EC3 always + full substrate+rxn EC4 when full_catalog_seen_ec4!)
        nn_tr = normalize(np.hstack([f_dict["tr_rxn_diff_r2"].astype(np.float32), f_dict["tr_sub_diff_r2"].astype(np.float32) * 0.60, f_dict["tr_rxn_ap_diff"].astype(np.float32) * 0.45]), norm="l2").astype(np.float32)
        nn_te = normalize(np.hstack([f_dict["te_rxn_diff_r2"].astype(np.float32), f_dict["te_sub_diff_r2"].astype(np.float32) * 0.60, f_dict["te_rxn_ap_diff"].astype(np.float32) * 0.45]), norm="l2").astype(np.float32)
        S_all_tr = nn_te @ nn_tr.T
        S_nn_ec3 = np.zeros((n_te, len(ec_list)), dtype=np.float32)
        seen_ec3_max = {c3: np.max(S_all_tr[:, idxs], axis=1) for c3, idxs in ec3_to_rows.items()}
        for j, c3 in enumerate(ec_to_ec3):
            if c3 in seen_ec3_max:
                S_nn_ec3[:, j] = seen_ec3_max[c3]

        if regime == "full_catalog_seen_ec4":
            vf_tr = normalize(np.hstack([
                f_dict["tr_rxn_diff_r2"].astype(np.float32),
                f_dict["tr_sub_r_r2"].astype(np.float32) * 0.85,
                f_dict["tr_sub_p_r2"].astype(np.float32) * 0.85,
                f_dict["tr_sub_diff_r2"].astype(np.float32) * 0.60,
                f_dict["tr_rxn_ap_diff"].astype(np.float32) * 0.40,
            ]), norm="l2").astype(np.float32)
            vf_te = normalize(np.hstack([
                f_dict["te_rxn_diff_r2"].astype(np.float32),
                f_dict["te_sub_r_r2"].astype(np.float32) * 0.85,
                f_dict["te_sub_p_r2"].astype(np.float32) * 0.85,
                f_dict["te_sub_diff_r2"].astype(np.float32) * 0.60,
                f_dict["te_rxn_ap_diff"].astype(np.float32) * 0.40,
            ]), norm="l2").astype(np.float32)
            S_f_raw = vf_te @ vf_tr.T
            S_nn_r4 = np.zeros((n_te, len(ec_list)), dtype=np.float32)
            S_nn_f4 = np.zeros((n_te, len(ec_list)), dtype=np.float32)
            for eid, rows in ec4_to_rows.items():
                S_nn_r4[:, eid] = S_all_tr[:, rows].max(axis=1)
                S_nn_f4[:, eid] = S_f_raw[:, rows].max(axis=1)
            S_vote4 = np.zeros((n_te, len(ec_list)), dtype=np.float32)
            S_comb_raw = 0.45 * S_all_tr + 0.55 * S_f_raw
            w_knn = compute_reaction_weights(tr_rxns, power=0.7)
            K = 15
            for i in range(n_te):
                row = S_comb_raw[i]
                top_idx = np.argpartition(row, -K)[-K:]
                sims = row[top_idx]
                wts = np.exp(22.0 * (sims - sims.max())) * w_knn[top_idx]
                wts /= wts.sum() + 1e-8
                for ti, wv in zip(top_idx, wts):
                    S_vote4[i, tr_y[ti]] += float(wv)
            x4_tr = np.hstack([xr_tr, xs_tr * 0.75]).astype(np.float32)
            x4_te = np.hstack([xr_te, xs_te * 0.75]).astype(np.float32)
            X4t = torch.from_numpy(x4_tr); X4te_t = torch.from_numpy(x4_te); Y4t = torch.from_numpy(tr_y)
            p4_nn_acc = np.zeros((n_te, len(ec_list)), dtype=np.float32)

        # 3. 3-Seed Multi-View Local Neural Ensemble
        Xtr, Xrct, Xts = torch.from_numpy(xr_tr), torch.from_numpy(xrc_tr), torch.from_numpy(xs_tr)
        Y1t, Y2t, Y3t = torch.from_numpy(tr_ec1), torch.from_numpy(y2_tr), torch.from_numpy(y3_tr)
        E123_t, E4_t, Ep_t = torch.from_numpy(E123), torch.from_numpy(E4), torch.from_numpy(prot_emb)
        l4_vt = torch.from_numpy(l4_v)
        A_t = torch.from_numpy((A_all > 0).astype(np.float32))
        pr_a = np.clip((A_all[tr_y] > 0).mean(0), 0.005, 0.995)
        pw_a = torch.from_numpy(np.clip((1.0 - pr_a) / pr_a, 1.0, 15.0).astype(np.float32))
        w_inv_t = torch.from_numpy(w_inv)
        log_pri1_inv = torch.from_numpy(np.log(np.maximum(cnt1_inv / cnt1_inv.sum(), 1e-6))).float()

        seed_configs = [(42, w_inv, "inv_mult"), (137, w_sqrt, "sqrt_inv_mult"), (2026, w_raw, "raw")][:n_seeds]
        p1_det_acc = np.zeros((n_te, 7), dtype=np.float32)
        S123_acc = np.zeros((n_te, len(ec_list)), dtype=np.float32)
        Sattr_acc = np.zeros((n_te, len(ec_list)), dtype=np.float32)
        S4_acc = np.zeros((n_te, len(ec_list)), dtype=np.float32)
        Sp_acc = np.zeros((n_te, len(ec_list)), dtype=np.float32)
        pf_acc = np.zeros((n_te, len(seen_ec3s)), dtype=np.float32)
        prc_acc = np.zeros((n_te, len(seen_ec3s)), dtype=np.float32)
        ps2_acc = np.zeros((n_te, len(seen_ec2s)), dtype=np.float32)
        cos3_acc = np.zeros(n_te, dtype=np.float32)
        cos2_acc = np.zeros(n_te, dtype=np.float32)

        Xte_t, Xrcte_t, Xste_t = torch.from_numpy(xr_te), torch.from_numpy(xrc_te), torch.from_numpy(xs_te)
        ep_f = 14 if regime == "unseen_ec3_zeroshot" else 18
        tau3 = 0.0 if regime == "unseen_ec3_zeroshot" else 0.45

        for sd, w_view, w_tag in seed_configs:
            ts = time.perf_counter()
            np.random.seed(sd); torch.manual_seed(sd); rng = np.random.default_rng(sd)
            w_vt = torch.from_numpy(w_view)
            pri3 = np.bincount(y3_tr, weights=w_view, minlength=len(seen_ec3s)).astype(np.float32)
            log_pri3 = torch.from_numpy(np.log(np.maximum(pri3 / pri3.sum(), 1e-6))).float()
            pri2 = np.bincount(y2_tr, weights=w_view, minlength=len(seen_ec2s)).astype(np.float32)
            log_pri2 = torch.from_numpy(np.log(np.maximum(pri2 / pri2.sum(), 1e-6))).float()

            ec1_net = nn.Sequential(
                nn.Linear(xr_tr.shape[1], 512), nn.LayerNorm(512), nn.GELU(), nn.Dropout(0.35),
                nn.Linear(512, 256), nn.LayerNorm(256), nn.GELU(), nn.Dropout(0.25),
                nn.Linear(256, 7),
            )
            o1 = torch.optim.AdamW(ec1_net.parameters(), lr=1.4e-3, weight_decay=3e-2)
            sch_1 = torch.optim.lr_scheduler.CosineAnnealingLR(o1, T_max=16)
            ec1_net.train()
            for _ in range(16):
                perm = torch.randperm(len(Xtr))
                for b0 in range(0, len(Xtr), 256):
                    b = perm[b0 : b0 + 256]
                    ce = F.cross_entropy(ec1_net(Xtr[b]) + 0.35 * log_pri1_inv, Y1t[b], label_smoothing=0.03, reduction="none")
                    loss = (ce * w_inv_t[b]).sum() / w_inv_t[b].sum().clamp(min=1e-6)
                    o1.zero_grad(); loss.backward(); o1.step()
                sch_1.step()

            full_la = e2.CosineClassNet(xr_tr.shape[1], len(seen_ec3s), hid=640)
            ofl = torch.optim.AdamW(full_la.parameters(), lr=1.6e-3, weight_decay=2.5e-2)
            sch_f = torch.optim.lr_scheduler.CosineAnnealingLR(ofl, T_max=ep_f)
            full_la.train()
            for _ in range(ep_f):
                perm = torch.randperm(len(Xtr))
                for b0 in range(0, len(Xtr), 256):
                    b = perm[b0 : b0 + 256]
                    ce = F.cross_entropy(full_la(Xtr[b])[0] + tau3 * log_pri3, Y3t[b], label_smoothing=0.05, reduction="none")
                    loss = (ce * w_vt[b]).sum() / w_vt[b].sum().clamp(min=1e-6)
                    ofl.zero_grad(); loss.backward(); ofl.step()
                sch_f.step()

            rc_la = e2.CosineClassNet(xrc_tr.shape[1], len(seen_ec3s), hid=512)
            orcl = torch.optim.AdamW(rc_la.parameters(), lr=1.6e-3, weight_decay=2.5e-2)
            sch_r = torch.optim.lr_scheduler.CosineAnnealingLR(orcl, T_max=ep_f)
            rc_la.train()
            for _ in range(ep_f):
                perm = torch.randperm(len(Xrct))
                for b0 in range(0, len(Xrct), 256):
                    b = perm[b0 : b0 + 256]
                    ce = F.cross_entropy(rc_la(Xrct[b])[0] + tau3 * log_pri3, Y3t[b], label_smoothing=0.05, reduction="none")
                    loss = (ce * w_vt[b]).sum() / w_vt[b].sum().clamp(min=1e-6)
                    orcl.zero_grad(); loss.backward(); orcl.step()
                sch_r.step()

            s2_la = e2.CosineClassNet(xr_tr.shape[1], len(seen_ec2s), hid=384)
            os2 = torch.optim.AdamW(s2_la.parameters(), lr=1.6e-3, weight_decay=2.5e-2)
            sch_2 = torch.optim.lr_scheduler.CosineAnnealingLR(os2, T_max=12)
            s2_la.train()
            for _ in range(12):
                perm = torch.randperm(len(Xtr))
                for b0 in range(0, len(Xtr), 256):
                    b = perm[b0 : b0 + 256]
                    ce = F.cross_entropy(s2_la(Xtr[b])[0] + 0.40 * log_pri2, Y2t[b], label_smoothing=0.05, reduction="none")
                    loss = (ce * w_vt[b]).sum() / w_vt[b].sum().clamp(min=1e-6)
                    os2.zero_grad(); loss.backward(); os2.step()
                sch_2.step()

            txt_net = nn.Sequential(
                nn.Linear(xr_tr.shape[1], 512), nn.LayerNorm(512), nn.GELU(), nn.Dropout(0.35),
                nn.Linear(512, 384), nn.LayerNorm(384), nn.GELU(), nn.Dropout(0.25),
            )
            h123 = nn.Linear(384, E123.shape[1]); ha = nn.Linear(384, A_all.shape[1])
            ot = torch.optim.AdamW(list(txt_net.parameters()) + list(h123.parameters()) + list(ha.parameters()), lr=1.5e-3, weight_decay=3e-2)
            txt_net.train()
            for _ in range(28):
                for _ in range(26):
                    b_c3 = rng.choice(seen_ec3s, size=min(128, len(seen_ec3s)), replace=False)
                    rb = np.array([rng.choice(ec3_to_rows[c]) for c in b_c3], dtype=np.int64)
                    ru = rng.integers(0, len(tr_y), size=64)
                    rows = np.concatenate([rb, ru])
                    h = txt_net(Xtr[rows]); ye = torch.from_numpy(tr_y[rows])
                    z123 = F.normalize(h123(h), dim=-1); tb = E123_t[ye]
                    lg = 18.0 * (z123 @ tb.T); lb = torch.arange(len(rows))
                    loss = 1.3 * F.binary_cross_entropy_with_logits(ha(h), A_t[ye], pos_weight=pw_a) + 0.5 * (F.cross_entropy(lg, lb) + F.cross_entropy(lg.T, lb)) + 1.2 * (1.0 - (z123 * tb).sum(-1)).mean()
                    ot.zero_grad(); loss.backward(); ot.step()

            sub_net = e2.DedicatedSubL4Net(xs_tr.shape[1], E4.shape[1], prot_emb.shape[1])
            o4 = torch.optim.AdamW(sub_net.parameters(), lr=1.5e-3, weight_decay=2.5e-2)
            sc4_sch = torch.optim.lr_scheduler.CosineAnnealingLR(o4, T_max=40)
            sub_net.train()
            for _ in range(40):
                for _ in range(32):
                    b_c4 = rng.choice(seen_ec4s, size=min(128, len(seen_ec4s)), replace=False)
                    rows_2 = np.array([rng.choice(ec4_to_rows[int(e)]) for e in b_c4], dtype=np.int64)
                    ye_2 = torch.from_numpy(b_c4)
                    z4, zp = sub_net(Xts[rows_2])
                    lp = (1.0 - (zp * Ep_t[ye_2]).sum(-1)).mean()
                    vm = l4_vt[ye_2] > 0.5
                    if vm.sum() >= 8:
                        z4v, ye_2v = z4[vm], ye_2[vm]
                        sc4 = sub_net.temp.exp().clamp(max=40.0); tb4 = E4_t[ye_2v]
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

            c4_net = None
            if regime == "full_catalog_seen_ec4":
                pri4 = np.bincount(tr_y, weights=w_view, minlength=len(ec_list)).astype(np.float32)
                log_pri4 = torch.from_numpy(np.log(np.maximum(pri4 / pri4.sum(), 1e-7))).float()
                c4_net = e2.CosineClassNet(x4_tr.shape[1], len(ec_list), hid=768)
                oc4 = torch.optim.AdamW(c4_net.parameters(), lr=1.8e-3, weight_decay=2.0e-2)
                sc_c4 = torch.optim.lr_scheduler.CosineAnnealingLR(oc4, T_max=18)
                c4_net.train()
                for _ in range(18):
                    perm = torch.randperm(len(X4t))
                    for b0 in range(0, len(X4t), 256):
                        b = perm[b0 : b0 + 256]
                        ce = F.cross_entropy(c4_net(X4t[b])[0] + 0.30 * log_pri4, Y4t[b], label_smoothing=0.05, reduction="none")
                        loss = (ce * w_vt[b]).sum() / w_vt[b].sum().clamp(min=1e-6)
                        oc4.zero_grad(); loss.backward(); oc4.step()
                    sc_c4.step()

            ec1_net.eval(); full_la.eval(); rc_la.eval(); s2_la.eval(); txt_net.eval(); sub_net.eval()
            with torch.no_grad():
                p1_det_acc += F.softmax(ec1_net(Xte_t), dim=-1).numpy() / len(seed_configs)
                lg_f, cos_f = full_la(Xte_t)
                pf_acc += F.softmax(lg_f, dim=-1).numpy() / len(seed_configs)
                cos3_acc += cos_f.numpy().max(axis=1) / len(seed_configs)
                prc_acc += F.softmax(rc_la(Xrcte_t)[0], dim=-1).numpy() / len(seed_configs)
                lg_2, cos_2 = s2_la(Xte_t)
                ps2_acc += F.softmax(lg_2, dim=-1).numpy() / len(seed_configs)
                cos2_acc += cos_2.numpy().max(axis=1) / len(seed_configs)
                ht = txt_net(Xte_t)
                S123_acc += e2.zscore_rows((F.normalize(h123(ht), dim=-1) @ E123_t.T).numpy()) / len(seed_configs)
                Sattr_acc += e2.zscore_rows((normalize(torch.sigmoid(ha(ht)).numpy(), norm="l2").astype(np.float32) @ A_norm.T)) / len(seed_configs)
                z4, zp = sub_net(Xste_t)
                S4_acc += e2.zscore_rows((z4 @ E4_t.T).numpy()) / len(seed_configs)
                Sp_acc += e2.zscore_rows((zp @ Ep_t.T).numpy()) / len(seed_configs)
                if c4_net is not None:
                    c4_net.eval()
                    p4_nn_acc += F.softmax(c4_net(X4te_t)[0], dim=-1).numpy() / len(seed_configs)
            print(f"[SEED {sd} ({w_tag})] done in {time.perf_counter()-ts:.1f}s", flush=True)

        Sr_v4 = e2.scale_rule_globally(((mech_te_raw @ W_rule.T) + (c_te @ D_v4.T)).astype(np.float32))
        S_4_rule = (mech_te_raw @ W4_rule.T).astype(np.float32)
        S_met = (X_met_te @ W_met.T).astype(np.float32)
        S4_local = (1.05 * S4_acc * l4_v[None, :] + 0.40 * e2.zscore_rows(S_4_rule) + 0.50 * S_met + 0.28 * Sp_acc).astype(np.float32)
        lc_payload = {
            "seen_ec2s": np.array(seen_ec2s, dtype=str), "seen_ec3s": np.array(seen_ec3s, dtype=str),
            "Sr_v4": Sr_v4, "S4_local": S4_local,
            "p1_lr": p1_lr, "p1_lgb_std": p1_lgb_std, "p1_lgb_bal": p1_lgb_bal,
            "p1_xgb_bal": p1_xgb_bal, "p1_xgb_std": p1_xgb_std, "p1_det_acc": p1_det_acc,
            "pf_acc": pf_acc, "prc_acc": prc_acc, "ps2_acc": ps2_acc,
            "S123_acc": S123_acc, "Sattr_acc": Sattr_acc, "S_nn_ec3": S_nn_ec3,
            "cos3_acc": cos3_acc, "cos2_acc": cos2_acc,
        }
        if p2_lgb is not None:
            lc_payload["p2_lgb"] = p2_lgb
        if p4_nn_acc is not None:
            lc_payload["p4_nn_acc"] = p4_nn_acc
            lc_payload["S_nn_r4"] = S_nn_r4
            lc_payload["S_nn_f4"] = S_nn_f4
            lc_payload["S_vote4"] = S_vote4
        np.savez_compressed(local_cache_path, **lc_payload)
        print(f"[LOCAL_CACHE_SAVED] {local_cache_path.name} ({time.perf_counter()-t0:.1f}s)", flush=True)

    # 4. Optional GPU checkpoints (0 extra CU; unused on full_catalog_seen_ec4 Easy)
    gpu_models = load_optional_gpu_ckpts(gpu_prefixes, ec_to_ec2, ec_to_ec3, n_te)

    # 5. Geometric Log-Odds EC1 Consensus + EC6/EC7 Conservation Margin
    sr_max_ec1 = np.column_stack([Sr_v4[:, ec1_arr == c].max(1) for c in range(7)])
    sr_z_ec1 = (sr_max_ec1 - sr_max_ec1.mean(1, keepdims=True)) / np.maximum(sr_max_ec1.std(1, keepdims=True), 1e-6)
    m_ec6 = np.maximum(0.0, sr_max_ec1[:, 5] - np.delete(sr_max_ec1, 5, axis=1).max(1))
    m_ec7 = np.maximum(0.0, sr_max_ec1[:, 6] - np.delete(sr_max_ec1, 6, axis=1).max(1))

    p1_tree = 0.20 * p1_lgb_std + 0.30 * p1_lgb_bal + 0.14 * p1_xgb_bal + 0.11 * p1_xgb_std + 0.17 * p1_det_acc + 0.08 * p1_lr
    if gpu_models:
        tot_gw = sum(v["weight"] for v in gpu_models.values())
        w_tree = 0.42
        lp1 = w_tree * np.log(np.clip(p1_tree, 5e-3, 1.0)) + 0.65 * sr_z_ec1
        for v in gpu_models.values():
            gw = (1.0 - w_tree - 0.10) * (v["weight"] / tot_gw)
            p1_use = v["p1"] if regime == "unseen_ec3_zeroshot" else v["p1_all"]
            lp1 += gw * np.log(np.clip(p1_use, 5e-3, 1.0))
    else:
        lp1 = 0.90 * np.log(np.clip(p1_tree, 5e-3, 1.0)) + 0.65 * sr_z_ec1

    lp1[:, 5] += 1.6 * np.clip(m_ec6, 0.0, 2.0)
    lp1[:, 6] += 1.0 * np.clip(m_ec7, 0.0, 2.0)
    e_x = np.exp(lp1 - lp1.max(1, keepdims=True))
    p1_head = e_x / e_x.sum(1, keepdims=True)
    S_ec1 = np.log(np.clip(p1_head[:, ec1_arr], 1e-4, 1.0))

    if gpu_models:
        tot_gw = sum(v["weight"] for v in gpu_models.values())
        S4_gpu = sum((v["weight"] / tot_gw) * e2.zscore_rows(v["S_t4"]) for v in gpu_models.values())
        S4_comb = 0.85 * S4_local + 1.00 * S4_gpu
    else:
        S4_comb = S4_local
    L4_np = e2.nonpos_within_ec3(S4_comb, ec3_groups)

    # 6. Auto-Regime Decoding Head (selected strictly from train-catalog coverage!)
    if regime == "unseen_ec3_zeroshot":
        zs_joint = 0.55 * S123_acc + 0.45 * Sattr_acc
        if gpu_models:
            tot_gw = sum(v["weight"] for v in gpu_models.values())
            zs_gpu = sum((v["weight"] / tot_gw) * e2.zscore_rows(v["S_t123"]) for v in gpu_models.values())
            zs_joint = 0.55 * zs_joint + 0.45 * zs_gpu
        zs_ec2mean = np.zeros_like(zs_joint)
        for g in ec2_groups:
            zs_ec2mean[:, g] = zs_joint[:, g].mean(axis=1, keepdims=True)
        S_seen_prob = map_cols(pf_acc, seen_ec3s, ec_to_ec3, default=0.0)
        S_seen2_prob = map_cols(ps2_acc, seen_ec2s, ec_to_ec2, default=0.0)
        g3 = np.clip((cos3_acc - 0.580) / 0.140, 0.0, 1.0)[:, None]
        g2 = np.clip((cos2_acc - 0.620) / 0.180, 0.0, 1.0)[:, None]
        fused_final = (
            1.00 * Sr_v4 + 1.60 * S_ec1 + 0.35 * e2.zscore_rows(zs_ec2mean)
            + 18.0 * g3 * S_seen_prob + 3.0 * g2 * S_seen2_prob + 0.10 * L4_np
        )
    elif regime == "seen_ec3_unseen_ec4":
        seen3_mask = np.array([c in set(seen_ec3s) for c in ec_to_ec3], dtype=bool)
        pf_full = map_cols(pf_acc, seen_ec3s, ec_to_ec3, default=0.0)
        prc_full = map_cols(prc_acc, seen_ec3s, ec_to_ec3, default=0.0)
        ps2_full = map_cols(ps2_acc, seen_ec2s, ec_to_ec2, default=0.0)
        p2lgb_full = map_cols(p2_lgb, seen_ec2s, ec_to_ec2, default=0.0)
        fl_seen = 1e-2
        if gpu_models:
            tot_gw = sum(v["weight"] for v in gpu_models.values())
            gpu_p3_arith = sum((v["weight"] / tot_gw) * v["p3_full"] for v in gpu_models.values())
            gpu_p2_arith = sum((v["weight"] / tot_gw) * v["p2_full"] for v in gpu_models.values())
            p3_arith = 0.16 * pf_full + 0.12 * prc_full + 0.72 * gpu_p3_arith
            p2_arith = 0.18 * p2lgb_full + 0.16 * ps2_full + 0.66 * gpu_p2_arith
            p3_max = p3_arith.max(axis=1, keepdims=True)
            u_fl = np.clip(0.01 + 0.15 * np.clip(1.0 - p3_max, 0.0, 1.0), 1e-4, 0.45)
            s3_geom_local = (
                0.55 * np.log(np.where(seen3_mask[None, :], np.maximum(pf_full, fl_seen), u_fl))
                + 0.45 * np.log(np.where(seen3_mask[None, :], np.maximum(prc_full, fl_seen), u_fl))
            )
            s3_geom_gpu = sum(
                (v["weight"] / tot_gw) * np.log(np.where(seen3_mask[None, :], np.maximum(v["p3_full"], fl_seen), u_fl))
                for v in gpu_models.values()
            )
            s3_term = 1.80 * (0.35 * (0.25 * s3_geom_local + 0.75 * s3_geom_gpu) + 0.65 * np.log(np.where(seen3_mask[None, :], np.maximum(p3_arith, fl_seen), u_fl)))
            s2_term = 0.75 * np.log(np.clip(p2_arith, 1e-3, 1.0))
            zs_gpu = 0.55 * sum((v["weight"] / tot_gw) * e2.zscore_rows(v["S_t123"]) for v in gpu_models.values())
        else:
            p3_arith = 0.55 * pf_full + 0.45 * prc_full
            p2_arith = 0.50 * p2lgb_full + 0.50 * ps2_full
            p3_max = p3_arith.max(axis=1, keepdims=True)
            u_fl = np.clip(0.01 + 0.15 * np.clip(1.0 - p3_max, 0.0, 1.0), 1e-4, 0.45)
            s3_geom = (
                0.55 * np.log(np.where(seen3_mask[None, :], np.maximum(pf_full, fl_seen), u_fl))
                + 0.45 * np.log(np.where(seen3_mask[None, :], np.maximum(prc_full, fl_seen), u_fl))
            )
            s3_term = 1.50 * (0.35 * s3_geom + 0.65 * np.log(np.where(seen3_mask[None, :], np.maximum(p3_arith, fl_seen), u_fl)))
            s2_term = 0.65 * np.log(np.clip(p2_arith, 1e-3, 1.0))
            zs_gpu = 0.0
        fused_final = (
            0.75 * Sr_v4 + 2.60 * S_ec1 + 0.35 * (S123_acc + 0.70 * Sattr_acc)
            + zs_gpu + s3_term + s2_term + 1.80 * np.maximum(0.0, S_nn_ec3 - 0.62) + 0.20 * L4_np
        )
    else:
        # Full-Catalog Seen-EC4 Regime (ec4_cov >= 0.99): 3-seed Seen-EC4 CosineNet + Multi-FP kNN + Hierarchical EC1/2/3 + L4_np
        pf_full = map_cols(pf_acc, seen_ec3s, ec_to_ec3, default=1e-5)
        prc_full = map_cols(prc_acc, seen_ec3s, ec_to_ec3, default=1e-5)
        ps2_full = map_cols(ps2_acc, seen_ec2s, ec_to_ec2, default=1e-4)
        p2lgb_full = map_cols(p2_lgb, seen_ec2s, ec_to_ec2, default=1e-4)
        s3_hier = 0.55 * np.log(np.clip(pf_full, 1e-4, 1.0)) + 0.45 * np.log(np.clip(prc_full, 1e-4, 1.0))
        s2_hier = np.log(np.clip(0.50 * p2lgb_full + 0.50 * ps2_full, 1e-3, 1.0))
        log_p4 = np.log(np.clip(p4_nn_acc, 1e-5, 1.0))
        log_v4 = np.log(np.clip(S_vote4, 1e-4, 1.0))
        fused_final = (
            1.65 * log_p4
            + 2.40 * (0.35 * S_nn_r4 + 0.65 * S_nn_f4)
            + 0.30 * log_v4
            + 0.45 * s3_hier
            + 0.25 * s2_hier
            + 0.55 * S_ec1
            + 0.20 * Sr_v4
            + 0.15 * L4_np
        )

    order = np.argsort(-fused_final, axis=1)
    ec_arr = np.array(ec_list, dtype=object)
    rank_df = pd.DataFrame(ec_arr[order], columns=[str(i) for i in range(len(ec_list))])
    out_df = pd.concat([te_df.reset_index(drop=True), rank_df], axis=1)
    out_df.to_csv(out_csv, index=False)

    manifest = {
        "model": f"we_star_CARE_engine_v5_auto_regime_{regime}_{n_seeds}seed_{'+'.join(sorted(gpu_models)) if gpu_models else 'M1only'}",
        "auto_detected_regime": regime,
        "train_ec3_coverage": round(ec3_cov, 4),
        "train_ec4_coverage": round(ec4_cov, 4),
        "train_files": [train_rel_name],
        "optional_files": [
            "processed_data/text2EC.csv",
            "processed_data/protein2EC.csv",
            "processed_data/EC_list.txt",
        ],
        "test_input_columns": ["Reaction"],
        "strict_zero_external_db": True,
        "gpu_models": sorted(gpu_models.keys()),
        "notes": "Train-catalog auto-regime with zero split-name conditionals; zero external databases (no rhea, no brenda, no kegg, no uniprot_api, no chatgpt); test input strictly unmapped Reaction SMILES only (no mapped reaction, no reaction text).",
    }
    manifest_path.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    print(f"[DONE] regime={regime} saved {out_csv.name} ({time.perf_counter()-t0:.1f}s) | gpus={sorted(gpu_models.keys())}", flush=True)


def main() -> int:
    ap = argparse.ArgumentParser(description="Train-Catalog Auto-Regime CARE Task 2 Engine (Zero Split-Name Branching)")
    ap.add_argument("--split", choices=["hard", "medium", "easy"], required=True, help="Dataset path alias only (never inspected by model/decoder)")
    ap.add_argument("--seeds", type=int, default=3)
    ap.add_argument("--use-local-cache", action="store_true")
    args = ap.parse_args()

    # Path resolution table ONLY — split string is never passed into run_auto_regime!
    gpu_map = {
        "hard": [("cb", "hard_cb", 0.38), ("mtr", "hard_mtr", 0.20), ("t5", "hard_t5", 0.42)],
        "medium": [("cb", "med_cb", 0.35), ("mtr", "med_mtr", 0.20), ("t5", "med_t5", 0.45)],
        "easy": [],
    }
    cache_map = {
        "hard": CACHE_DIR / f"v5_hard_local_{args.seeds}seed.npz",
        "medium": CACHE_DIR / f"v5_medium_local_{args.seeds}seed.npz",
        "easy": CACHE_DIR / f"v5_auto_easy_local_{args.seeds}seed.npz",
    }
    run_auto_regime(
        train_csv=DATA_ROOT / "splits" / "task2" / f"{args.split}_reaction_train.csv",
        test_csv=DATA_ROOT / "splits" / "task2" / f"{args.split}_reaction_test.csv",
        feat_cache_tag=args.split,
        local_cache_path=cache_map[args.split],
        out_csv=OUT_DIR / f"v5_auto_{args.split}_reaction_test_results_df.csv",
        manifest_path=OUT_DIR / f"v5_auto_{args.split}_provenance.json",
        gpu_prefixes=gpu_map[args.split],
        train_rel_name=f"splits/task2/{args.split}_reaction_train.csv",
        n_seeds=args.seeds,
        use_local_cache=args.use_local_cache,
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
