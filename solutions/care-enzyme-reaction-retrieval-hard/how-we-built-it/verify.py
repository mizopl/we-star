#!/usr/bin/env python3
"""Standalone Verifier & Leakage Auditor for CARE Benchmark (Tasks 1 & 2).

Implements exact official `performance_evaluation.ipynb` metric rules:
  - get_accuracy_level(predicted_ECs, true_ECs)
  - get_average_accuracy(accuracy_level_list, level)
  - Level 4 (X.X.X.X), Level 3 (X.X.X.-), Level 2 (X.X.-.-), Level 1 (X.-.-.-)
  - Task 2 k in {1, 3, 5, 10, 20, 30, 40, 50}
  - Supports BOTH full CARE results_summary CSVs AND compact row-indexed top-50 `.csv.gz` archives
    (columns: `row_idx,0,1,...,49`, joined read-only against `--data-root` official test splits).
  - Strictly read-only by default (writes nothing unless `--ckpt` is explicitly supplied).
  - `--corrupt`: negative control applying a seeded random row permutation + invalid EC + duplicate top-50
    checks (exits rc=1 when corruption is caught & accuracy collapses, rc=0 if verifier fails to catch it).
"""
from __future__ import annotations

import argparse
import json
import pathlib
import sys
import time
import warnings

import numpy as np
import pandas as pd

warnings.filterwarnings("ignore")

ROOT = pathlib.Path(__file__).resolve().parent
DEFAULT_DATA_ROOT = (
    ROOT / "data" / "CARE_datasets"
    if (ROOT / "data" / "CARE_datasets").exists()
    else ROOT.parent / "data" / "CARE_datasets"
)
DEFAULT_REPO_ROOT = (
    ROOT / "upstream_repo"
    if (ROOT / "upstream_repo").exists()
    else ROOT.parent / "upstream_repo"
)

OFFICIAL_TASK2_TABLE4 = {
    ("easy", "random"): (0.0, 1.0, 4.6, 22.9),
    ("easy", "Similarity"): (59.3, 77.1, 85.2, 90.6),
    ("easy", "CLIPZyme"): (12.2, 39.9, 61.8, 79.9),
    ("easy", "CREEP"): (39.4, 66.4, 79.9, 92.9),
    ("easy", "CREEP_text"): (60.3, 89.3, 93.9, 96.7),
    ("medium", "random"): (0.0, 0.5, 4.1, 17.0),
    ("medium", "Similarity"): (0.0, 40.2, 55.7, 73.3),
    ("medium", "CLIPZyme"): (2.0, 26.0, 46.6, 69.0),
    ("medium", "CREEP"): (4.1, 44.3, 63.1, 86.5),
    ("medium", "CREEP_text"): (7.4, 59.5, 75.6, 92.1),
    ("hard", "random"): (0.0, 0.9, 1.5, 18.3),
    ("hard", "Similarity"): (0.0, 0.0, 13.5, 42.0),
    ("hard", "CLIPZyme"): (1.1, 4.1, 13.5, 46.7),
    ("hard", "CREEP"): (1.3, 4.8, 18.7, 57.6),
    ("hard", "CREEP_text"): (1.3, 9.8, 22.2, 57.2),
}

OFFICIAL_TASK1_TABLE2 = {
    ("30", "random", 1): (0.0, 1.2, 3.2, 19.4),
    ("30", "BLAST", 1): (51.4, 60.0, 62.5, 65.7),
    ("30", "Foldseek", 1): (54.9, 68.3, 72.9, 80.6),
    ("30", "CLEAN", 1): (55.1, 68.8, 74.8, 84.5),
    ("30-50", "random", 1): (0.0, 0.7, 3.6, 22.5),
    ("30-50", "BLAST", 1): (81.1, 87.9, 90.7, 92.3),
    ("30-50", "Foldseek", 1): (79.8, 87.1, 90.5, 95.0),
    ("30-50", "CLEAN", 1): (80.2, 88.0, 91.6, 95.5),
    ("price", "random", 1): (0.0, 0.7, 4.7, 22.3),
    ("price", "BLAST", 1): (35.1, 70.9, 78.4, 78.4),
    ("price", "Foldseek", 1): (41.2, 82.4, 93.2, 96.6),
    ("price", "CLEAN", 1): (31.8, 74.3, 81.8, 85.8),
    ("promiscuous", "BLAST", 1): (93.7, 94.8, 95.2, 95.9),
    ("promiscuous", "Foldseek", 1): (88.0, 90.9, 92.4, 94.4),
    ("promiscuous", "CLEAN", 20): (69.4, 77.9, 81.5, 87.0),
}

FORBIDDEN_EXTERNAL_TOKENS = (
    "rhea",
    "brenda",
    "kegg",
    "uniprot_api",
    "chatgpt",
    "openai",
    "gpt-4",
    "gpt-3.5",
    "mapped reaction",
    "reaction text",
)


def get_average_accuracy(accuracy_level_list: list[int], level: int) -> float:
    return float(np.mean([1 if x >= level else 0 for x in accuracy_level_list]))


def expand_list(predicted_ecs: list[str], on: str = "; ") -> list[str]:
    expanded = []
    for entry in predicted_ecs:
        if isinstance(entry, list):
            return entry
        expanded.extend(str(entry).split(on))
    return expanded


def get_accuracy_level(predicted_ecs: list[str] | str, true_ecs: list[str] | str) -> list[int]:
    if isinstance(predicted_ecs, str):
        predicted_ecs = [predicted_ecs]
    if isinstance(true_ecs, str):
        true_ecs = [true_ecs]

    maxes = []
    for true_ec in true_ecs:
        true_split = str(true_ec).strip().split(".")
        counters = []
        for pred_ec in predicted_ecs:
            pred_str = str(pred_ec).strip()
            if pred_str.count(".") != 3:
                pred_str = "0.0.0.0"
            pred_split = pred_str.split(".")
            counter = 0
            for pred_part, true_part in zip(pred_split, true_split):
                if pred_part == true_part:
                    counter += 1
                else:
                    break
            counters.append(counter)
        maxes.append(int(np.max(counters)))
    return maxes


def load_official_test_df(data_root: pathlib.Path, task: str, split: str) -> pd.DataFrame:
    if task == "task2":
        p = data_root / "splits" / "task2" / f"{split}_reaction_test.csv"
    else:
        name_map = {
            "30": "30_protein_test.csv",
            "30-50": "30-50_protein_test.csv",
            "price": "price_protein_test.csv",
            "promiscuous": "promiscuous_protein_test.csv",
        }
        p = data_root / "splits" / "task1" / name_map[split]
    return pd.read_csv(p)


def load_prediction_df(pred_path: pathlib.Path, data_root: pathlib.Path, task: str, split: str) -> pd.DataFrame:
    """Load either a full CARE results CSV or a compact row-indexed top-50 `.csv.gz` archive."""
    df = pd.read_csv(pred_path)
    if "EC number" not in df.columns and "row_idx" in df.columns:
        ref = load_official_test_df(data_root, task, split).reset_index(drop=True)
        expected_idx = np.arange(len(ref))
        if len(df) != len(ref) or not np.array_equal(df["row_idx"].to_numpy(), expected_idx):
            raise ValueError(f"Compact archive row_idx mismatch vs official {split} split (len={len(df)} vs {len(ref)})")
        rank_cols = [c for c in df.columns if c != "row_idx"]
        key_col = "Reaction" if task == "task2" else "Entry"
        df = pd.concat([ref[[key_col, "EC number"]], df[rank_cols].reset_index(drop=True)], axis=1)
    return df


def evaluate_results_df(
    df: pd.DataFrame,
    task: str = "task2",
    split: str = "hard",
    baseline_mode: str = "ranked",
    ks: list[int] | None = None,
) -> dict[int, tuple[float, float, float, float]]:
    if "0" not in df.columns:
        raise ValueError("Missing column '0' in results DataFrame.")
    num_col_idx = list(df.columns).index("0")
    work = df.copy()
    work.iloc[:, num_col_idx:] = work.iloc[:, num_col_idx:].fillna("0.0.0.0")

    if ks is None:
        if baseline_mode in ("Pika", "ChatGPT", "ChatGPT_text") or (
            task == "task1" and baseline_mode in ("BLAST", "Foldseek")
        ):
            ks = [1]
        elif task == "task1" and baseline_mode in ("CLEAN", "random"):
            ks = [1, 20] if split == "promiscuous" else [1]
        elif task == "task1":
            ks = [1]
        else:
            max_avail = len(work.columns) - num_col_idx
            ks = [k for k in (1, 3, 5, 10, 20, 30, 40, 50) if k <= max_avail] or [1]

    out = {}
    ec_lists = work["EC number"].astype(str).apply(lambda s: [e.strip() for e in s.split(";")])
    for k in ks:
        raw_preds = work.iloc[:, num_col_idx : num_col_idx + k].values.tolist()
        if baseline_mode in ("BLAST", "Foldseek"):
            preds = [expand_list(r, on="; ") for r in raw_preds]
        elif baseline_mode in ("Pika", "ChatGPT", "ChatGPT_text"):
            preds = [expand_list(r, on=",") for r in raw_preds]
        elif task == "task1" and split == "promiscuous" and baseline_mode in ("CLEAN", "random", "ranked"):
            preds = [r[: len(true_list)] for r, true_list in zip(raw_preds, ec_lists)]
        else:
            preds = raw_preds

        levels = [get_accuracy_level(p, t) for p, t in zip(preds, ec_lists)]
        accs = []
        for lvl in (4, 3, 2, 1):
            mean_acc = float(np.mean([get_average_accuracy(row_lvls, lvl) for row_lvls in levels]))
            accs.append(round(mean_acc * 100.0, 1))
        out[k] = (accs[0], accs[1], accs[2], accs[3])
    return out


def validate_submission_integrity(df: pd.DataFrame, data_root: pathlib.Path, task: str, split: str) -> list[str]:
    errs = []
    ref = load_official_test_df(data_root, task, split)
    if len(df) != len(ref):
        errs.append(f"Row count mismatch: got {len(df)}, expected {len(ref)}")
        return errs

    key_col = "Reaction" if task == "task2" else "Entry"
    if key_col not in df.columns:
        errs.append(f"Missing key column '{key_col}'")
    elif not (df[key_col].astype(str).values == ref[key_col].astype(str).values).all():
        errs.append(f"Key column '{key_col}' order/values differ from official {split} test split")

    if "EC number" not in df.columns:
        errs.append("Missing 'EC number' ground truth column")
    elif not (df["EC number"].astype(str).values == ref["EC number"].astype(str).values).all():
        errs.append("'EC number' column differs from official test split")

    if "0" not in df.columns:
        errs.append("Missing top-1 prediction column '0'")
        return errs

    ec_vocab = set(np.loadtxt(data_root / "processed_data" / "EC_list.txt", dtype=str))
    num_idx = list(df.columns).index("0")
    rank_cols = list(df.columns[num_idx:])
    expected_names = [str(i) for i in range(len(rank_cols))]
    if rank_cols != expected_names:
        errs.append(f"Ranking columns must be contiguous strings '0'..'{len(rank_cols)-1}', got {rank_cols[:5]}...")
        return errs

    k_check = min(50, len(rank_cols))
    top_vals = df.iloc[:, num_idx : num_idx + k_check].astype(str).apply(lambda col: col.str.strip()).values
    invalid_cells = []
    dup_rows = 0
    for r_idx in range(top_vals.shape[0]):
        row = top_vals[r_idx]
        if len(set(row.tolist())) != k_check:
            dup_rows += 1
        for c_idx, val in enumerate(row):
            if val.count(".") != 3 or val not in ec_vocab:
                if len(invalid_cells) < 5:
                    invalid_cells.append((r_idx, c_idx, val))
    if invalid_cells:
        errs.append(f"Found invalid/out-of-vocabulary ECs in top-{k_check} columns, sample(row,col,val)={invalid_cells[:3]}")
    if dup_rows > 0:
        errs.append(f"Found {dup_rows} rows with duplicate EC predictions within top-{k_check} columns")
    return errs


def reproduce_baselines(repo_root: pathlib.Path) -> int:
    t0 = time.perf_counter()
    drifts = []
    for (split, bl), expected in OFFICIAL_TASK2_TABLE4.items():
        p = repo_root / "task2_baselines" / "results_summary" / bl / f"{split}_reaction_test_results_df.csv"
        df = pd.read_csv(p)
        res = evaluate_results_df(df, task="task2", split=split, baseline_mode=bl, ks=[1])[1]
        if res != expected:
            drifts.append(f"Task2 {split}/{bl}: got {res}, expected {expected}")

    for (split, bl, k), expected in OFFICIAL_TASK1_TABLE2.items():
        p = repo_root / "task1_baselines" / "results_summary" / bl / f"{split}_protein_test_results_df.csv"
        df = pd.read_csv(p)
        res = evaluate_results_df(df, task="task1", split=split, baseline_mode=bl, ks=[k])[k]
        if res != expected:
            drifts.append(f"Task1 {split}/{bl} k={k}: got {res}, expected {expected}")

    dt = time.perf_counter() - t0
    if drifts:
        for d in drifts:
            print(f"[DRIFT] {d}", file=sys.stderr)
        return 1
    print(f"[PASS] Reproduced all {len(OFFICIAL_TASK2_TABLE4)} Task 2 + {len(OFFICIAL_TASK1_TABLE2)} Task 1 official baselines with 0.000% drift in {dt:.2f}s.")
    return 0


def audit_provenance(manifest_path: pathlib.Path, task: str, split: str) -> list[str]:
    errs = []
    if not manifest_path.exists():
        return [f"Missing provenance manifest: {manifest_path}"]
    m = json.loads(manifest_path.read_text(encoding="utf-8"))
    expected_train = (
        f"splits/task2/{split}_reaction_train.csv"
        if task == "task2"
        else "splits/task1/protein_train.csv"
    )
    train_files = m.get("train_files", [])
    if expected_train not in train_files:
        errs.append(f"Designated train file '{expected_train}' not recorded in train_files={train_files}")

    allowed_optional = (
        {"processed_data/protein2EC.csv", "processed_data/protein2EC_clustered50.csv", "processed_data/text2EC.csv", "processed_data/EC_list.txt"}
        if task == "task2"
        else {"processed_data/reaction2EC.csv", "processed_data/text2EC.csv", "processed_data/EC_list.txt", "splits/task1/protein_train50.csv"}
    )
    for f in train_files + m.get("optional_files", []):
        if f != expected_train and f not in allowed_optional:
            errs.append(f"Unauthorized training/optional file: {f}")
        if "test" in pathlib.Path(f).name.lower():
            errs.append(f"LEAKAGE: test file referenced in training/optional files: {f}")

    if m.get("test_input_columns") != (["Reaction"] if task == "task2" else ["Sequence"]):
        errs.append(f"Strict test input violation: got {m.get('test_input_columns')} (must only read Reaction SMILES / Sequence at test time)")

    blob = json.dumps(m).lower()
    for tok in FORBIDDEN_EXTERNAL_TOKENS:
        if tok in blob and f"no {tok}" not in blob and f"zero {tok}" not in blob:
            errs.append(f"Forbidden external resource/column token detected in manifest: {tok}")

    if m.get("strict_zero_external_db") is not True:
        errs.append("strict_zero_external_db must be True")
    return errs


def main() -> int:
    ap = argparse.ArgumentParser(description="CARE Benchmark Verifier & Leakage Auditor (Read-Only by Default)")
    ap.add_argument("--data-root", type=pathlib.Path, default=DEFAULT_DATA_ROOT, help="Path to CARE_datasets directory")
    ap.add_argument("--repo-root", type=pathlib.Path, default=DEFAULT_REPO_ROOT, help="Path to upstream CARE repo (for --reproduce-baselines)")
    ap.add_argument("--reproduce-baselines", action="store_true", help="Verify 0.000%% drift against official repo results_summary")
    ap.add_argument("--pred", type=pathlib.Path, default=None, help="Prediction CSV or compact top-50 .csv.gz archive")
    ap.add_argument("--task", default="task2", choices=["task1", "task2"])
    ap.add_argument("--split", default="hard")
    ap.add_argument("--corrupt", action="store_true", help="Negative control: seeded permutation + invalid/dup EC checks (must exit rc=1)")
    ap.add_argument("--manifest", type=pathlib.Path, default=None, help="Optional provenance manifest JSON to audit")
    ap.add_argument("--ckpt", type=pathlib.Path, default=None, help="Optional output JSON metrics file (read-only if omitted)")
    args = ap.parse_args()

    if args.reproduce_baselines:
        rc = reproduce_baselines(args.repo_root)
        if args.pred is None or rc != 0:
            return rc

    if args.pred is None:
        ap.print_help()
        return 1

    t0 = time.perf_counter()
    df = load_prediction_df(args.pred, args.data_root, args.task, args.split)

    if args.corrupt:
        corrupted = df.copy()
        num_idx = list(df.columns).index("0")
        rng = np.random.default_rng(12345)
        perm = rng.permutation(len(df))
        if np.array_equal(perm, np.arange(len(df))) and len(df) > 1:
            perm = np.roll(perm, 1)
        corrupted.iloc[:, num_idx:] = df.iloc[perm, num_idx:].values
        corrupted2 = df.copy()
        corrupted2.loc[0, "0"] = "INVALID_EC"
        errs2 = validate_submission_integrity(corrupted2, args.data_root, args.task, args.split)
        corrupted3 = df.copy()
        if "1" in corrupted3.columns:
            corrupted3.loc[0, "1"] = corrupted3.loc[0, "0"]
        errs3 = validate_submission_integrity(corrupted3, args.data_root, args.task, args.split)
        res_orig = evaluate_results_df(df, task=args.task, split=args.split, ks=[1])[1]
        res_perm = evaluate_results_df(corrupted, task=args.task, split=args.split, ks=[1])[1]
        collapsed = res_perm[3] < res_orig[3] - 10.0 and res_perm != res_orig
        print(f"[CORRUPT_CONTROL] orig_k1={res_orig} permuted_k1={res_perm} invalid_ec_errs={errs2} dup_errs={errs3}")
        if errs2 and (errs3 or "1" not in df.columns) and collapsed:
            print("[CORRUPT_PASS_FAIL_EXPECTED] Verifier caught corrupted submission and score collapsed across all levels (exiting rc=1 as required).")
            return 1
        print("[CORRUPT_SELF_TEST_FAILED] Corruption did not collapse score or trigger integrity errors!", file=sys.stderr)
        return 0

    errs = validate_submission_integrity(df, args.data_root, args.task, args.split)
    if args.manifest is not None:
        errs.extend(audit_provenance(args.manifest, args.task, args.split))

    if errs:
        for e in errs:
            print(f"[FAIL] {e}", file=sys.stderr)
        return 1

    metrics = evaluate_results_df(df, task=args.task, split=args.split)
    dt = time.perf_counter() - t0
    k1 = metrics[1]
    print(f"[PASS] task={args.task} split={args.split} n={len(df)} elapsed={dt:.3f}s | k=1 L4={k1[0]:.1f}% L3={k1[1]:.1f}% L2={k1[2]:.1f}% L1={k1[3]:.1f}%")
    for k, vals in sorted(metrics.items()):
        if k != 1:
            print(f"       k={k:2d} L4={vals[0]:.1f}% L3={vals[1]:.1f}% L2={vals[2]:.1f}% L1={vals[3]:.1f}%")

    if args.ckpt is not None:
        payload = {
            "task": args.task,
            "split": args.split,
            "n_test": len(df),
            "elapsed_sec": round(dt, 4),
            "metrics_pct": {str(k): {"L4": v[0], "L3": v[1], "L2": v[2], "L1": v[3]} for k, v in metrics.items()},
        }
        args.ckpt.parent.mkdir(parents=True, exist_ok=True)
        args.ckpt.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
