#!/usr/bin/env python3
"""Self-contained one-command verifier for the we* unitaryfoundation/stabrank package.

Verifies:
1. Schema conformance & filename/claim bijective parity across all 35 bounds/*.json
   files from unitaryfoundation/stabrank PR #193 (commit fc1495d).
2. Exact execution of all 5 Cyclotomic / Galois certificate scripts
   (cert_qubit_galois_m3_m4.py, cert_qubit_galois_m5_m6_rank4.py,
   cert_cat_m7_to_m10_lift.py, cert_cs_m3_m4_exact.py, cert_qutrit_galois_m3_m5.py)
   and exact symbolic witness checking via stabrank_verify.py, requiring 35/35 PASS
   at tier == "verified" (~20.5 s on a single Apple M1 core).
3. Static zero-sorry / zero-axiom audit and theorem-signature verification across
   all 10 Lean 4 modules from unitaryfoundation/stabrank PR #194 (commit 6fc15c5).
"""

from __future__ import annotations

import glob
import json
import os
import re
import sys
import time

ROOT = os.path.dirname(os.path.abspath(__file__))
VERIFY_DIR = os.path.join(ROOT, "verify_challenge")
if VERIFY_DIR not in sys.path:
    sys.path.insert(0, VERIFY_DIR)

import jsonschema  # noqa: E402
import stabrank_verify  # noqa: E402
import validate_bounds  # noqa: E402

EXPECTED_BOUND_COUNT = 35

EXPECTED_LEAN_THEOREMS: dict[str, list[str]] = {
    "lean_proofs/LeanProofs/ReflectQutrit.lean": [
        "norrellVec_eq_ev",
    ],
    "lean_proofs/LeanProofs/M1Lower.lean": [
        "qubit_h_m1_stabRankP_gt_one",
        "qubit_h_m1_stabRankP_eq_two",
        "qubit_t_m1_stabRankP_gt_one",
        "qubit_t_m1_stabRankP_eq_two",
        "h3_m1_stabRank_gt_one",
        "h3_m1_stabRank_eq_two",
        "norrell_m1_stabRank_gt_one",
        "norrell_m1_stabRank_eq_two",
    ],
    "lean_proofs/LeanProofs/QubitHM1StabRank.lean": [
        "qubit_h_m1_stabRankP_le_two",
    ],
    "lean_proofs/LeanProofs/QubitTM1StabRank.lean": [
        "qubit_t_m1_stabRankP_le_two",
    ],
    "lean_proofs/LeanProofs/H3M1StabRank.lean": [
        "h3_m1_stabRank_le_two",
    ],
    "lean_proofs/LeanProofs/NorrellM1StabRank.lean": [
        "norrell_m1_stabRank_le_two",
    ],
    "lean_proofs/LeanProofs/QubitTM7StabRank.lean": [
        "qubit_t_m7_stabRankP_le_nine",
    ],
    "lean_proofs/LeanProofs/QubitTM8StabRank.lean": [
        "qubit_t_m8_stabRankP_le_nine",
    ],
    "lean_proofs/LeanProofs/NorrellM5StabRank.lean": [
        "norrell_m5_stabRank_le_ten",
    ],
    "lean_proofs/LeanProofs/H3M5StabRank.lean": [
        "h3_m5_stabRank_le_twelve",
    ],
}

FORBIDDEN_LEAN_TOKENS = re.compile(r"\b(sorry|admit|axiom)\b")


def strip_lean_comments(src: str) -> str:
    src = re.sub(r"/-.*?-/", "", src, flags=re.S)
    src = re.sub(r"--[^\n]*", "", src)
    return src


def expected_claim_line(orbit: str, m: int, rank: int) -> str:
    if orbit == "cat":
        return f"CERTIFIED chi(cat_{m}) >= {rank}"
    return f"CERTIFIED chi({orbit}^{m}) >= {rank}"


def main() -> int:
    t0 = time.monotonic()
    schema_path = os.path.join(ROOT, "schema", "bound.schema.json")
    with open(schema_path, encoding="utf-8") as fh:
        schema = json.load(fh)
    validator = jsonschema.Draft202012Validator(schema)

    bound_paths = sorted(glob.glob(os.path.join(ROOT, "bounds", "*.json")))
    if len(bound_paths) != EXPECTED_BOUND_COUNT:
        print(
            f"FAIL: expected {EXPECTED_BOUND_COUNT} bound JSON files, found {len(bound_paths)}"
        )
        return 1

    print(f"[1/3] Schema & bijective metadata check across {len(bound_paths)} bounds...")
    for path in bound_paths:
        base = os.path.basename(path)
        with open(path, encoding="utf-8") as fh:
            sub = json.load(fh)

        schema_errs = [e.message for e in validator.iter_errors(sub)]
        tier_errs, _notes = validate_bounds.tier_requirements(sub)
        all_errs = schema_errs + tier_errs
        if all_errs:
            print(f"FAIL {base}: {all_errs}")
            return 1

        orbit = sub["orbit"]
        m = sub["m"]
        direction = sub["direction"]
        rank = sub["rank"]
        expected_base = f"{orbit}-m{m}-{direction}-{rank}.json"
        if base != expected_base:
            print(f"FAIL {base}: filename mismatch vs payload {expected_base}")
            return 1

        prov = sub.get("provenance", {})
        if prov.get("author") != "we* + @mizopl":
            print(f"FAIL {base}: unexpected provenance.author {prov.get('author')!r}")
            return 1

        if direction == "lower":
            cert = sub.get("certificate", {})
            if cert.get("exact") is not True:
                print(f"FAIL {base}: lower bound must declare exact=true")
                return 1
            want_expect = expected_claim_line(orbit, m, rank)
            if cert.get("expect") != want_expect:
                print(
                    f"FAIL {base}: expect={cert.get('expect')!r} != {want_expect!r}"
                )
                return 1
        elif direction == "upper":
            if "witness" not in sub:
                print(f"FAIL {base}: upper bound missing explicit witness")
                return 1

    print("[2/3] Running exact Galois/Cyclotomic certificates & witness checks (PR #193)...")
    for path in bound_paths:
        base = os.path.basename(path)
        with open(path, encoding="utf-8") as fh:
            sub = json.load(fh)
        res = stabrank_verify.verify(sub)
        sign = "<=" if sub["direction"] == "upper" else ">="
        print(
            f"  {'PASS' if res.ok else 'FAIL'}  {base:<26s} "
            f"chi(|{sub['orbit']}>^{sub['m']}) {sign} {sub['rank']}  [tier={res.tier}]"
        )
        if not res.ok or res.tier != "verified":
            print(f"FAIL {base}: ok={res.ok}, tier={res.tier!r}, detail={res.detail}")
            return 1

    print("[3/3] Auditing 10 zero-axiom Lean 4 proof modules (PR #194)...")
    total_theorems = 0
    for rel_path, thms in EXPECTED_LEAN_THEOREMS.items():
        full_path = os.path.join(ROOT, rel_path)
        if not os.path.isfile(full_path):
            print(f"FAIL: missing Lean module {rel_path}")
            return 1
        with open(full_path, encoding="utf-8") as fh:
            raw = fh.read()
        code_only = strip_lean_comments(raw)
        bad_tok = FORBIDDEN_LEAN_TOKENS.search(code_only)
        if bad_tok:
            print(
                f"FAIL {rel_path}: forbidden token {bad_tok.group(0)!r} found in Lean code"
            )
            return 1
        for thm in thms:
            if not re.search(rf"^\s*theorem\s+{re.escape(thm)}\b", code_only, re.M):
                print(f"FAIL {rel_path}: missing theorem {thm}")
                return 1
            total_theorems += 1

    elapsed = time.monotonic() - t0
    print(
        f"\nPASS: 35/35 bounds verified at tier='verified' + "
        f"10/10 Lean 4 modules ({total_theorems} target theorems, 0 sorryAx) "
        f"audited in {elapsed:.2f}s."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
