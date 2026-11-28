#!/usr/bin/env python3
"""eval_pub_stats.py — 0-CU Publication-Grade Statistical Rigor & Neuro-Symbolic Ablations for CARE Task 2.

Computes strictly from frozen predictions & cached local/GPU scores (ZERO retraining, ZERO external data):
  1. Complete Neuro-Symbolic Ablation Table on Hard (n=460) and Medium (n=393):
     - Sr_v4 textbook IUBMB conservation rules alone (0 ML, 0 pretraining)
     - + Local M1 ML only (0 GPU, 0 reaction transformer pretraining: v2_hard/v3_medium & v5_M1only)
     - + Colab GPU Transformers (v5_hard M1+CB+MTR, v5_medium M1+CB+MTR+T5v2)
     - Cross-branch sensitivity (Hard head on Medium & Medium head on Hard)
  2. 10,000-resample Paired Bootstrap 95% CIs + Exact Two-Sided McNemar p-values vs upstream CREEP & CREEP_text
  3. 100-seed Random Tie-Break Stability (exact tie count in fused_final + mean +/- sd across L4..L1)
  4. Subgroup Breakdown by Text Incomplete (True vs False in text2EC.csv) and Medium Seen vs Unseen EC3s.
"""
from __future__ import annotations

import json
import pathlib
import sys
import time

import numpy as np
import pandas as pd
from scipy.stats import binomtest

ROOT = pathlib.Path(__file__).resolve().parent
DATA_ROOT = ROOT / "data" / "CARE_datasets"
REPO_ROOT = ROOT / "upstream_repo"
CACHE_DIR = ROOT / "cache"
OUT_DIR = ROOT / "outputs"

if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import engine_v2 as e2  # noqa: E402
import engine_v5 as e5  # noqa: E402
import features_v2 as f2  # noqa: E402
import verify as ver  # noqa: E402


def top1_level_hits(pred_col0: list[str], true_ecs: list[str]) -> np.ndarray:
    """Return (N, 4) binary array of [L4, L3, L2, L1] hits matching verify.get_accuracy_level exactly."""
    n = len(true_ecs)
    hits = np.zeros((n, 4), dtype=np.int8)
    for i, (p, t) in enumerate(zip(pred_col0, true_ecs)):
        lvls = ver.get_accuracy_level([str(p)], [str(t)])
        for idx, L in enumerate((4, 3, 2, 1)):
            hits[i, idx] = 1 if lvls[0] >= L else 0
    return hits


def paired_bootstrap_and_mcnemar(h_model: np.ndarray, h_base: np.ndarray, n_boot: int = 10000, seed: int = 42) -> dict:
    rng = np.random.default_rng(seed)
    n = h_model.shape[0]
    boot_idx = rng.integers(0, n, size=(n_boot, n))
    res = {}
    for idx, L in enumerate(("L4", "L3", "L2", "L1")):
        m = h_model[:, idx].astype(np.float64)
        b = h_base[:, idx].astype(np.float64)
        diff = m - b
        mean_m = float(m.mean() * 100.0)
        mean_b = float(b.mean() * 100.0)
        delta = float(diff.mean() * 100.0)
        boot_m = m[boot_idx].mean(axis=1) * 100.0
        boot_d = diff[boot_idx].mean(axis=1) * 100.0
        ci_m = (float(np.percentile(boot_m, 2.5)), float(np.percentile(boot_m, 97.5)))
        ci_d = (float(np.percentile(boot_d, 2.5)), float(np.percentile(boot_d, 97.5)))
        n10 = int(((m == 1) & (b == 0)).sum())
        n01 = int(((m == 0) & (b == 1)).sum())
        pval = float(binomtest(n10, n10 + n01, 0.5, alternative="two-sided").pvalue) if (n10 + n01) > 0 else 1.0
        res[L] = {
            "model_pct": round(mean_m, 2),
            "model_ci95": [round(ci_m[0], 2), round(ci_m[1], 2)],
            "base_pct": round(mean_b, 2),
            "delta_pp": round(delta, 2),
            "delta_ci95": [round(ci_d[0], 2), round(ci_d[1], 2)],
            "n10": n10,
            "n01": n01,
            "mcnemar_p": pval,
        }
    return res


def cluster_bootstrap_and_tests(
    h_model: np.ndarray,
    h_base: np.ndarray,
    cluster_ids: list[str],
    n_boot: int = 10000,
    seed: int = 42,
) -> dict:
    """Cluster-level paired bootstrap 95% CIs + exact cluster sign test + 10k paired cluster permutation p-value.

    Resamples entire clusters (EC3 or EC4) with replacement, preserving the exact test-set weighting
    (sum of hits / sum of rows in resampled clusters) to account for intra-EC correlation.
    """
    uniq_clusters = sorted(set(cluster_ids))
    c_to_idx = {c: i for i, c in enumerate(uniq_clusters)}
    n_c = len(uniq_clusters)
    c_arr = np.array([c_to_idx[c] for c in cluster_ids], dtype=np.int64)

    c_sizes = np.bincount(c_arr, minlength=n_c).astype(np.float64)
    c_m = np.zeros((n_c, 4), dtype=np.float64)
    c_b = np.zeros((n_c, 4), dtype=np.float64)
    for k in range(4):
        c_m[:, k] = np.bincount(c_arr, weights=h_model[:, k].astype(np.float64), minlength=n_c)
        c_b[:, k] = np.bincount(c_arr, weights=h_base[:, k].astype(np.float64), minlength=n_c)
    c_diff = c_m - c_b

    rng = np.random.default_rng(seed)
    boot_c = rng.integers(0, n_c, size=(n_boot, n_c))
    boot_den = c_sizes[boot_c].sum(axis=1)  # (n_boot,)

    # Paired cluster-level sign-flip permutation test (exact under exchangeable cluster differences)
    perm_signs = rng.choice(np.array([-1.0, 1.0]), size=(n_boot, n_c))

    res = {"n_clusters": n_c}
    for idx, L in enumerate(("L4", "L3", "L2", "L1")):
        obs_m = float(c_m[:, idx].sum() / c_sizes.sum() * 100.0)
        obs_b = float(c_b[:, idx].sum() / c_sizes.sum() * 100.0)
        obs_d = obs_m - obs_b

        bm = c_m[boot_c, idx].sum(axis=1) / boot_den * 100.0
        bd = c_diff[boot_c, idx].sum(axis=1) / boot_den * 100.0
        ci_m = (float(np.percentile(bm, 2.5)), float(np.percentile(bm, 97.5)))
        ci_d = (float(np.percentile(bd, 2.5)), float(np.percentile(bd, 97.5)))

        # Cluster-level sign test on non-zero cluster differences
        c_pos = int((c_diff[:, idx] > 0).sum())
        c_neg = int((c_diff[:, idx] < 0).sum())
        sign_p = float(binomtest(c_pos, c_pos + c_neg, 0.5, alternative="two-sided").pvalue) if (c_pos + c_neg) > 0 else 1.0

        # Two-sided paired cluster sign-flip permutation p-value (Phipson-Smyth +1 correction)
        obs_sum = abs(float(c_diff[:, idx].sum()))
        perm_sums = np.abs(perm_signs @ c_diff[:, idx])
        perm_p = float((int((perm_sums >= obs_sum - 1e-12).sum()) + 1) / (n_boot + 1))

        res[L] = {
            "model_pct": round(obs_m, 2),
            "model_ci95": [round(ci_m[0], 2), round(ci_m[1], 2)],
            "base_pct": round(obs_b, 2),
            "delta_pp": round(obs_d, 2),
            "delta_ci95": [round(ci_d[0], 2), round(ci_d[1], 2)],
            "clusters_pos": c_pos,
            "clusters_neg": c_neg,
            "cluster_sign_p": sign_p,
            "cluster_perm_p": perm_p,
        }
    return res


def compute_v5_score_matrices(split: str, ec_df: pd.DataFrame, head_override: str | None = None, use_gpu: bool = True) -> tuple[np.ndarray, np.ndarray]:
    """Recompute exact fused_final & Sr_v4 matrices from saved 3-seed local cache (+ optional GPU ckpts)."""
    ec_list = ec_df["ec"].tolist()
    ec1_arr = np.array([int(x) - 1 for x in ec_df["ec1"]], dtype=np.int64)
    ec_to_ec2 = ec_df["ec2"].tolist()
    ec_to_ec3 = ec_df["ec3"].tolist()
    ec2_groups = [g.index.values.astype(np.int64) for _, g in ec_df.groupby("ec2")]
    ec3_groups = [g.index.values.astype(np.int64) for _, g in ec_df.groupby("ec3")]

    lc = np.load(CACHE_DIR / f"v5_{split}_local_3seed.npz", allow_pickle=True)
    seen_ec2s = lc["seen_ec2s"].tolist()
    seen_ec3s = lc["seen_ec3s"].tolist()
    Sr_v4 = lc["Sr_v4"]; S4_local = lc["S4_local"]
    p1_lr = lc["p1_lr"]; p1_lgb_std = lc["p1_lgb_std"]; p1_lgb_bal = lc["p1_lgb_bal"]
    p1_xgb_bal = lc["p1_xgb_bal"]; p1_xgb_std = lc["p1_xgb_std"]; p1_det_acc = lc["p1_det_acc"]
    pf_acc = lc["pf_acc"]; prc_acc = lc["prc_acc"]; ps2_acc = lc["ps2_acc"]
    S123_acc = lc["S123_acc"]; Sattr_acc = lc["Sattr_acc"]; S_nn_ec3 = lc["S_nn_ec3"]
    cos3_acc = lc["cos3_acc"]; cos2_acc = lc["cos2_acc"]
    p2_lgb = lc["p2_lgb"] if "p2_lgb" in lc.files else None
    n_te = Sr_v4.shape[0]

    head = head_override if head_override is not None else split
    gpu_models = e5.load_gpu_models(split, ec_to_ec2, ec_to_ec3, n_te) if use_gpu else {}

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
            p1_use = v["p1_all"] if head != "hard" else v["p1"]
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

    if head != "hard":
        seen3_mask = np.array([c in set(seen_ec3s) for c in ec_to_ec3], dtype=bool)
        pf_full = e5.map_cols(pf_acc, seen_ec3s, ec_to_ec3, default=0.0)
        prc_full = e5.map_cols(prc_acc, seen_ec3s, ec_to_ec3, default=0.0)
        ps2_full = e5.map_cols(ps2_acc, seen_ec2s, ec_to_ec2, default=0.0)
        p2lgb_full = e5.map_cols(p2_lgb, seen_ec2s, ec_to_ec2, default=0.0) if p2_lgb is not None else ps2_full
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
        fused = 0.75 * Sr_v4 + 2.60 * S_ec1 + 0.35 * (S123_acc + 0.70 * Sattr_acc) + zs_gpu + s3_term + s2_term + 1.80 * np.maximum(0.0, S_nn_ec3 - 0.62) + 0.20 * L4_np
    else:
        zs_joint = 0.55 * S123_acc + 0.45 * Sattr_acc
        if gpu_models:
            tot_gw = sum(v["weight"] for v in gpu_models.values())
            zs_gpu = sum((v["weight"] / tot_gw) * e2.zscore_rows(v["S_t123"]) for v in gpu_models.values())
            zs_joint = 0.55 * zs_joint + 0.45 * zs_gpu
        zs_ec2mean = np.zeros_like(zs_joint)
        for g in ec2_groups:
            zs_ec2mean[:, g] = zs_joint[:, g].mean(axis=1, keepdims=True)
        S_seen_prob = e5.map_cols(pf_acc, seen_ec3s, ec_to_ec3, default=0.0)
        S_seen2_prob = e5.map_cols(ps2_acc, seen_ec2s, ec_to_ec2, default=0.0)
        g3 = np.clip((cos3_acc - 0.580) / 0.140, 0.0, 1.0)[:, None]
        g2 = np.clip((cos2_acc - 0.620) / 0.180, 0.0, 1.0)[:, None]
        fused = 1.00 * Sr_v4 + 1.60 * S_ec1 + 0.35 * e2.zscore_rows(zs_ec2mean) + 18.0 * g3 * S_seen_prob + 3.0 * g2 * S_seen2_prob + 0.10 * L4_np
    return fused, Sr_v4


def score_top1_matrix(M: np.ndarray, ec_list: list[str], true_ecs: list[str]) -> dict[str, float]:
    order = np.argsort(-M, axis=1)
    preds = [ec_list[int(i)] for i in order[:, 0]]
    h = top1_level_hits(preds, true_ecs)
    return {L: round(float(h[:, idx].mean() * 100.0), 1) for idx, L in enumerate(("L4", "L3", "L2", "L1"))}


def tie_break_stability(M: np.ndarray, ec_list: list[str], true_ecs: list[str], n_seeds: int = 100, tol: float = 1e-6) -> dict:
    mx = M.max(axis=1, keepdims=True)
    tied_mask = (mx - M) <= tol
    tie_counts = tied_mask.sum(axis=1)
    n_tied_rows = int((tie_counts > 1).sum())
    # Count intra-EC3 vs cross-EC3 ties among tied top-1 rows
    ec3_arr = np.array([e.rsplit(".", 1)[0] for e in ec_list])
    n_cross_ec3_ties = 0
    for i in range(len(true_ecs)):
        if tie_counts[i] > 1:
            if len(set(ec3_arr[tied_mask[i]].tolist())) > 1:
                n_cross_ec3_ties += 1
    rng = np.random.default_rng(2026)
    accs = np.zeros((n_seeds, 4), dtype=np.float64)
    for s in range(n_seeds):
        preds = []
        for i in range(len(true_ecs)):
            cands = np.where(tied_mask[i])[0]
            pick = int(cands[0]) if len(cands) == 1 else int(rng.choice(cands))
            preds.append(ec_list[pick])
        accs[s] = top1_level_hits(preds, true_ecs).mean(axis=0) * 100.0
    out = {
        "n_rows": len(true_ecs),
        "n_tied_rows": n_tied_rows,
        "n_cross_ec3_ties": n_cross_ec3_ties,
        "median_tie_set_when_tied": float(np.median(tie_counts[tie_counts > 1])) if n_tied_rows > 0 else 1.0,
    }
    for idx, L in enumerate(("L4", "L3", "L2", "L1")):
        out[L] = {"mean": round(float(accs[:, idx].mean()), 2), "std": round(float(accs[:, idx].std()), 2)}
    return out


def main() -> int:
    t0 = time.perf_counter()
    ec_df = f2.prepare_denoised_text2ec()
    ec_list = ec_df["ec"].tolist()
    t2ec = pd.read_csv(DATA_ROOT / "processed_data" / "text2EC.csv")
    inc_map = dict(zip(t2ec["EC number"].astype(str), t2ec["Text Incomplete"].astype(bool)))

    summary = {}
    for split in ("hard", "medium"):
        print(f"\n================ {split.upper()} PUBLICATION STATS & ABLATIONS ================", flush=True)
        te_df = pd.read_csv(DATA_ROOT / "splits" / "task2" / f"{split}_reaction_test.csv")
        tr_df = pd.read_csv(DATA_ROOT / "splits" / "task2" / f"{split}_reaction_train.csv")
        true_ecs = te_df["EC number"].astype(str).tolist()
        seen_ec3 = set(tr_df["EC number"].astype(str).str.rsplit(".", n=1).str[0])

        v5_df = pd.read_csv(OUT_DIR / f"v5_{split}_reaction_test_results_df.csv")
        creep_df = pd.read_csv(REPO_ROOT / "task2_baselines" / "results_summary" / "CREEP" / f"{split}_reaction_test_results_df.csv")
        creept_df = pd.read_csv(REPO_ROOT / "task2_baselines" / "results_summary" / "CREEP_text" / f"{split}_reaction_test_results_df.csv")

        h_v5 = top1_level_hits(v5_df["0"].astype(str).tolist(), true_ecs)
        h_cr = top1_level_hits(creep_df["0"].astype(str).tolist(), true_ecs)
        h_ct = top1_level_hits(creept_df["0"].astype(str).tolist(), true_ecs)

        # 1. Neuro-symbolic ablation ladder + cross-branch sensitivity
        M_full, Sr_v4 = compute_v5_score_matrices(split, ec_df, head_override=split, use_gpu=True)
        M_m1only, _ = compute_v5_score_matrices(split, ec_df, head_override=split, use_gpu=False)
        other_head = "medium" if split == "hard" else "hard"
        M_cross, _ = compute_v5_score_matrices(split, ec_df, head_override=other_head, use_gpu=True)

        ablation = {
            "Sr_v4_rules_only_0ML": score_top1_matrix(Sr_v4, ec_list, true_ecs),
            "v5_M1_only_0GPU": score_top1_matrix(M_m1only, ec_list, true_ecs),
            "v5_full_M1_plus_GPU": score_top1_matrix(M_full, ec_list, true_ecs),
            f"v5_cross_head_{other_head}": score_top1_matrix(M_cross, ec_list, true_ecs),
        }
        print("  [ABLATION LADDER]:")
        for k, v in ablation.items():
            print(f"    {k:26s}: L4={v['L4']:5.1f}% L3={v['L3']:5.1f}% L2={v['L2']:5.1f}% L1={v['L1']:5.1f}%")

        # 2. 10,000-resample Paired Bootstrap 95% CIs + Exact McNemar p-values (row-level + EC3/EC4 cluster-level)
        vs_creep = paired_bootstrap_and_mcnemar(h_v5, h_cr, n_boot=10000, seed=42)
        vs_creept = paired_bootstrap_and_mcnemar(h_v5, h_ct, n_boot=10000, seed=42)
        ec3_ids = [e.rsplit(".", 1)[0] for e in true_ecs]
        ec4_ids = true_ecs
        vs_creep_ec3 = cluster_bootstrap_and_tests(h_v5, h_cr, ec3_ids, n_boot=10000, seed=42)
        vs_creept_ec3 = cluster_bootstrap_and_tests(h_v5, h_ct, ec3_ids, n_boot=10000, seed=42)
        vs_creep_ec4 = cluster_bootstrap_and_tests(h_v5, h_cr, ec4_ids, n_boot=10000, seed=42)
        vs_creept_ec4 = cluster_bootstrap_and_tests(h_v5, h_ct, ec4_ids, n_boot=10000, seed=42)

        print("  [vs CREEP (zero-leakage, 10k paired bootstrap + exact McNemar)]:")
        for L in ("L4", "L3", "L2", "L1"):
            d = vs_creep[L]
            print(f"    {L}: v5={d['model_pct']:5.2f}% {d['model_ci95']} vs CREEP={d['base_pct']:5.2f}% | delta={d['delta_pp']:+6.2f}pp {d['delta_ci95']} | n10={d['n10']} n01={d['n01']} p={d['mcnemar_p']:.3e}")
        print("  [vs CREEP_text (gold-test-EC text, 10k paired bootstrap + exact McNemar)]:")
        for L in ("L4", "L3", "L2", "L1"):
            d = vs_creept[L]
            print(f"    {L}: v5={d['model_pct']:5.2f}% {d['model_ci95']} vs CREEP_t={d['base_pct']:5.2f}% | delta={d['delta_pp']:+6.2f}pp {d['delta_ci95']} | n10={d['n10']} n01={d['n01']} p={d['mcnemar_p']:.3e}")
        for cname, c_cr, c_ct in [
            (f"EC3-CLUSTER (K={vs_creep_ec3['n_clusters']})", vs_creep_ec3, vs_creept_ec3),
            (f"EC4-CLUSTER (K={vs_creep_ec4['n_clusters']})", vs_creep_ec4, vs_creept_ec4),
        ]:
            print(f"  [{cname} vs CREEP / vs CREEP_text]:")
            for L in ("L4", "L3", "L2", "L1"):
                a, b = c_cr[L], c_ct[L]
                print(
                    f"    {L}: vsCREEP d={a['delta_pp']:+6.2f} {a['delta_ci95']} (+{a['clusters_pos']}/-{a['clusters_neg']} sign_p={a['cluster_sign_p']:.2e} perm_p={a['cluster_perm_p']:.2e})"
                    f" | vsCREEP_t d={b['delta_pp']:+6.2f} {b['delta_ci95']} (+{b['clusters_pos']}/-{b['clusters_neg']} sign_p={b['cluster_sign_p']:.2e} perm_p={b['cluster_perm_p']:.2e})"
                )

        # 3. 100-seed random tie-break stability
        tb = tie_break_stability(M_full, ec_list, true_ecs, n_seeds=100)
        print(f"  [TIE-BREAK STABILITY (100 seeds)]: tied_rows={tb['n_tied_rows']}/{tb['n_rows']} (cross_ec3_ties={tb['n_cross_ec3_ties']}) | "
              + " ".join(f"{L}={tb[L]['mean']:.1f}±{tb[L]['std']:.1f}%" for L in ("L4", "L3", "L2", "L1")))

        # 4. Subgroup breakdown: Text Incomplete=True vs False + Seen vs Unseen EC3
        inc_flags = np.array([inc_map.get(e, False) for e in true_ecs], dtype=bool)
        seen3_flags = np.array([e.rsplit(".", 1)[0] in seen_ec3 for e in true_ecs], dtype=bool)
        subgroups = {}
        for sname, mask in [
            ("Text_Incomplete_True", inc_flags),
            ("Text_Incomplete_False", ~inc_flags),
            ("Seen_EC3", seen3_flags),
            ("Unseen_EC3", ~seen3_flags),
        ]:
            if mask.sum() == 0:
                continue
            n_sub = int(mask.sum())
            n_uniq_ec = len(set(np.array(true_ecs)[mask].tolist()))
            sub_v5 = {L: round(float(h_v5[mask, idx].mean() * 100.0), 1) for idx, L in enumerate(("L4", "L3", "L2", "L1"))}
            sub_cr = {L: round(float(h_cr[mask, idx].mean() * 100.0), 1) for idx, L in enumerate(("L4", "L3", "L2", "L1"))}
            sub_ct = {L: round(float(h_ct[mask, idx].mean() * 100.0), 1) for idx, L in enumerate(("L4", "L3", "L2", "L1"))}
            subgroups[sname] = {"n_rows": n_sub, "n_unique_ec4": n_uniq_ec, "v5": sub_v5, "CREEP": sub_cr, "CREEP_text": sub_ct}
            print(f"  [SUBGROUP {sname:22s} n={n_sub:3d} ({n_uniq_ec:3d} ECs)]: v5=({sub_v5['L4']}/{sub_v5['L3']}/{sub_v5['L2']}/{sub_v5['L1']}) | CREEP=({sub_cr['L4']}/{sub_cr['L3']}/{sub_cr['L2']}/{sub_cr['L1']}) | CREEP_t=({sub_ct['L4']}/{sub_ct['L3']}/{sub_ct['L2']}/{sub_ct['L1']})")

        summary[split] = {
            "n_test": len(true_ecs),
            "ablation": ablation,
            "vs_CREEP": vs_creep,
            "vs_CREEP_text": vs_creept,
            "vs_CREEP_ec3_cluster": vs_creep_ec3,
            "vs_CREEP_text_ec3_cluster": vs_creept_ec3,
            "vs_CREEP_ec4_cluster": vs_creep_ec4,
            "vs_CREEP_text_ec4_cluster": vs_creept_ec4,
            "tie_break_100seed": tb,
            "subgroups": subgroups,
        }

    out_p = OUT_DIR / "pub_stats_summary.json"
    out_p.write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")
    print(f"\n[DONE] Saved {out_p} in {time.perf_counter()-t0:.2f}s", flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
