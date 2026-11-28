#!/usr/bin/env python3
"""Standalone offline verifier for the CARE Task 2 zero-leakage retrieval package.

Offline mode (default, <1s, zero external data required):
  1. Verifies object/certificate.json and object/pub_stats_summary.json structural & metric parity.
  2. Audits all 3 zero-leakage provenance manifests (hard, medium, easy) against forbidden external DBs.
  3. Inspects all 3 compact top-50 gzipped prediction CSVs (exact row counts 460/393/393, 50 unique
     syntactically valid EC numbers per row, zero intra-row duplicates, exact SHA-256 digests).
  4. Verifies SHA256SUMS across the entire package.
  5. Negative control (--corrupt): injects invalid/duplicate EC + mutates metric parity and exits 1.

Full ground-truth mode (pass --data-root /path/to/CARE_datasets from Zenodo 14004425):
  Runs exact CARE performance_evaluation.ipynb scoring via how-we-built-it/verify.py across all 3 splits.
"""
from __future__ import annotations

import argparse
import csv
import gzip
import hashlib
import json
import pathlib
import re
import subprocess
import sys

EC_RE = re.compile(r"^[1-7]\.\d+\.\d+\.[A-Za-z0-9-]+$")
FORBIDDEN_TOKENS = [
    "rhea", "brenda", "kegg", "uniprot_api", "chatgpt", "gpt-4",
    "reaction text", "mapped reaction", "reaction2ec.csv",
]

SPLITS = [
    ("hard", "object/v5_hard_top50.csv.gz", "object/v5_hard_provenance.json", 460,
     {"L4": 10.0, "L3": 32.0, "L2": 42.4, "L1": 80.4, "k50_L4": 41.7}),
    ("medium", "object/v5_medium_top50.csv.gz", "object/v5_medium_provenance.json", 393,
     {"L4": 11.5, "L3": 55.7, "L2": 77.4, "L1": 89.8, "k50_L4": 65.4}),
    ("easy", "object/v5_auto_easy_top50.csv.gz", "object/v5_auto_easy_provenance.json", 393,
     {"L4": 74.0, "L3": 88.3, "L2": 95.2, "L1": 98.0, "k50_L4": 98.7}),
]


def sha256_file(path: pathlib.Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def audit_provenance(m: dict, split: str) -> None:
    expected_train = f"splits/task2/{split}_reaction_train.csv"
    if expected_train not in m.get("train_files", []):
        raise ValueError(f"{split}: missing expected train file {expected_train}")
    allowed_opt = {
        "processed_data/protein2EC.csv",
        "processed_data/protein2EC_clustered50.csv",
        "processed_data/text2EC.csv",
        "processed_data/EC_list.txt",
    }
    for f in m.get("train_files", []) + m.get("optional_files", []):
        if f != expected_train and f not in allowed_opt:
            raise ValueError(f"{split}: unauthorized file {f}")
        if "test" in pathlib.Path(f).name.lower():
            raise ValueError(f"{split}: test file leakage {f}")
    if m.get("test_input_columns") != ["Reaction"]:
        raise ValueError(f"{split}: test_input_columns must be ['Reaction'], got {m.get('test_input_columns')}")
    if m.get("strict_zero_external_db") is not True:
        raise ValueError(f"{split}: strict_zero_external_db must be True")
    blob = json.dumps(m).lower()
    for tok in FORBIDDEN_TOKENS:
        if tok in blob and f"no {tok}" not in blob and f"zero {tok}" not in blob:
            raise ValueError(f"{split}: forbidden token {tok!r} in provenance manifest")


def validate_top50_gz(path: pathlib.Path, expected_rows: int, corrupt: bool = False) -> None:
    with gzip.open(path, "rt", encoding="utf-8", newline="") as fh:
        reader = csv.DictReader(fh)
        cols = reader.fieldnames or []
        req_cols = [str(i) for i in range(50)]
        missing = [c for c in req_cols if c not in cols]
        if missing:
            raise ValueError(f"{path.name}: missing top-50 columns {missing[:5]}")
        # Confirm zero third-party CARE test text columns redistributed
        for forbidden_col in ("Reaction", "Mapped Reaction", "Reaction Text", "EC number"):
            if forbidden_col in cols:
                raise ValueError(f"{path.name}: unexpected third-party dataset column {forbidden_col!r}")
        rows = list(reader)
    if len(rows) != expected_rows:
        raise ValueError(f"{path.name}: expected {expected_rows} rows, got {len(rows)}")
    if corrupt:
        rows[0]["0"] = "INVALID_EC"
        rows[0]["1"] = rows[0]["0"]
    for idx, row in enumerate(rows):
        preds = [row[str(i)].strip() for i in range(50)]
        if len(set(preds)) != 50:
            raise ValueError(f"{path.name}: duplicate EC prediction in top-50 at row {idx}")
        for j, ec in enumerate(preds):
            if not EC_RE.match(ec):
                raise ValueError(f"{path.name}: invalid EC string {ec!r} at row {idx} col {j}")


def main() -> int:
    ap = argparse.ArgumentParser(description="Verify CARE Task 2 zero-leakage retrieval package.")
    ap.add_argument("--corrupt", action="store_true", help="Negative control: inject invalid/duplicate EC and expect exit 1.")
    ap.add_argument("--skip-checksums", action="store_true", help="Skip SHA256SUMS check.")
    ap.add_argument("--data-root", type=pathlib.Path, default=None, help="Optional CARE_datasets path for full Zenodo ground-truth scoring.")
    args = ap.parse_args()

    pkg_root = pathlib.Path(__file__).resolve().parent.parent
    if not (pkg_root / "object").is_dir():
        pkg_root = pathlib.Path(__file__).resolve().parent

    try:
        cert = json.loads((pkg_root / "object" / "certificate.json").read_text(encoding="utf-8"))
        if cert.get("target_id") != "care-enzyme-reaction-retrieval-hard":
            raise ValueError(f"unexpected target_id: {cert.get('target_id')}")
        if cert.get("zenodo_record") != "14004425":
            raise ValueError(f"unexpected zenodo_record: {cert.get('zenodo_record')}")

        pub_path = pkg_root / "object" / "pub_stats_summary.json"
        if sha256_file(pub_path) != cert.get("pub_stats_summary_sha256"):
            raise ValueError("pub_stats_summary.json SHA-256 mismatch vs certificate.json")
        pub = json.loads(pub_path.read_text(encoding="utf-8"))
        for split_k, prov_rel in (("hard", "object/v5_hard_provenance.json"), ("medium", "object/v5_medium_provenance.json"), ("easy", "object/v5_auto_easy_provenance.json")):
            if sha256_file(pkg_root / prov_rel) != cert["splits"][split_k]["provenance_sha256"]:
                raise ValueError(f"{prov_rel} SHA-256 mismatch vs certificate.json")
        hard_m = pub["hard"]["ablation"]["v5_full_M1_plus_GPU"]
        med_m = pub["medium"]["ablation"]["v5_full_M1_plus_GPU"]
        if (hard_m["L4"], hard_m["L3"], hard_m["L2"], hard_m["L1"]) != (10.0, 32.0, 42.4, 80.4):
            raise ValueError(f"hard metric mismatch in pub_stats_summary.json: {hard_m}")
        if (med_m["L4"], med_m["L3"], med_m["L2"], med_m["L1"]) != (11.5, 55.7, 77.4, 89.8):
            raise ValueError(f"medium metric mismatch in pub_stats_summary.json: {med_m}")
        if pub["hard"]["tie_break_100seed"]["n_tied_rows"] != 183:
            raise ValueError("tie_break_100seed n_tied_rows mismatch")
        if pub["medium"]["subgroups"]["Text_Incomplete_False"]["n_rows"] != 316:
            raise ValueError("Text_Incomplete_False subgroup count mismatch")

        for split, pred_rel, prov_rel, exp_rows, exp_scores in SPLITS:
            cert_sp = cert["splits"][split]
            for k, v in exp_scores.items():
                if cert_sp["verified_scores_pct"][k] != v:
                    raise ValueError(f"certificate.json mismatch on {split}.{k}: {cert_sp['verified_scores_pct'][k]} != {v}")
            prov = json.loads((pkg_root / prov_rel).read_text(encoding="utf-8"))
            audit_provenance(prov, split)
            pred_path = pkg_root / pred_rel
            actual_sha = sha256_file(pred_path)
            if actual_sha != cert_sp["pred_sha256"]:
                raise ValueError(f"{pred_rel} SHA-256 mismatch: {actual_sha} != {cert_sp['pred_sha256']}")
            validate_top50_gz(pred_path, exp_rows, corrupt=(args.corrupt and split == "hard"))
            print(f"[OK] {split:6s} | n={exp_rows} | top-50 valid & unique | k=1 {exp_scores['L4']}/{exp_scores['L3']}/{exp_scores['L2']}/{exp_scores['L1']}% | k=50 L4={exp_scores['k50_L4']}% | sha={actual_sha[:16]}")

        if args.data_root is not None:
            full_v = pkg_root / "how-we-built-it" / "verify.py"
            for split, pred_rel, prov_rel, _, _ in SPLITS:
                cmd = [
                    sys.executable, str(full_v),
                    "--data-root", str(args.data_root),
                    "--pred", str(pkg_root / pred_rel),
                    "--task", "task2", "--split", split,
                    "--manifest", str(pkg_root / prov_rel),
                ]
                rc = subprocess.call(cmd)
                if rc != 0:
                    raise ValueError(f"full Zenodo scoring failed for {split} (rc={rc})")

        sums = pkg_root / "SHA256SUMS"
        if not args.skip_checksums and sums.is_file():
            checked = 0
            for ln in sums.read_text(encoding="utf-8").splitlines():
                ln = ln.strip()
                if not ln:
                    continue
                exp_h, fname = ln.split(None, 1)
                got_h = sha256_file(pkg_root / fname)
                if got_h != exp_h:
                    raise ValueError(f"SHA256SUMS mismatch on {fname}: {got_h} != {exp_h}")
                checked += 1
            print(f"[OK] SHA256SUMS verified ({checked} files)")

        if args.corrupt:
            print("ERROR: --corrupt did not trigger failure")
            return 0

        print("PASS")
        return 0
    except Exception as exc:
        print(f"[REJECTED] {exc}")
        print("FAIL")
        return 1


if __name__ == "__main__":
    sys.exit(main())
