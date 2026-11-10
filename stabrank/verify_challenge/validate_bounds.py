"""Validate submissions against schema/bound.schema.json.

The schema is linked from every page of the site, so it has to be the real
contract rather than documentation that drifted: additionalProperties is false
throughout, which means a field the schema does not know about is an error, not
a silent pass.  It is checked in CI for exactly that reason.

Schema conformance is necessary and nowhere near sufficient.  It says a
submission is well formed, not that the bound holds; stabrank_verify.py decides
that.  Run this first anyway, since a malformed file wastes a verification run.
"""

from __future__ import annotations

import glob
import json
import os
import sys

import jsonschema

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SCHEMA = os.path.join(ROOT, "schema", "bound.schema.json")

# The schema's `maximum` of 10 copies is a verification budget for single
# qubits, 2^10 amplitudes. A ququint bound has 5^m amplitudes, so the same
# budget stops at m = 5 (3125; m = 6 would be 15625), and a CS bound has
# 4^m (two qubits per copy), so it stops at m = 4 (256; m = 8 would be
# 65,536). The schema cannot say so because its cap is global.
M_CAP = {"T5": (5, "5^m amplitudes"), "CS": (4, "two qubits per copy, 4^m amplitudes")}

# Family tracks are indexed by the qubit count, and the smallest members are
# stabilizer states or empty: |cat_1> = |0>, so the cat track starts at m = 2.
M_MIN = {"cat": 2}


def tier_requirements(sub):
    """Cross-field rules the schema cannot express, as (errors, notes).

    A note is not a defect. A submission with no witness and no certificate is
    a perfectly good citation of a published bound; it just cannot hold a
    record, and saying so once here is cheaper than a surprise on the board.
    """
    errors, notes = [], []
    d = sub.get("direction")
    cap, why = M_CAP.get(sub.get("orbit"), (None, None))
    if cap is not None and isinstance(sub.get("m"), int) and sub["m"] > cap:
        errors.append(f"m = {sub['m']} exceeds the verification budget for "
                      f"{sub['orbit']}, which is m <= {cap} ({sub['orbit']} has "
                      f"{why}; the schema's cap of 10 is for single qubits)")
    low = M_MIN.get(sub.get("orbit"))
    if low is not None and isinstance(sub.get("m"), int) and sub["m"] < low:
        errors.append(f"m = {sub['m']} is below the first cell of the "
                      f"{sub['orbit']} family, which is m = {low}")
    if d == "upper" and "certificate" in sub:
        errors.append("an upper bound is settled by a decomposition, not a "
                      "certificate script; drop 'certificate'")
    if d == "lower" and "witness" in sub:
        errors.append("a lower bound cannot carry a witness; drop 'witness'")
    w = sub.get("witness")
    if w and len(w.get("terms", [])) != len(w.get("coeffs", [])):
        errors.append(f"{len(w.get('terms', []))} terms against "
                      f"{len(w.get('coeffs', []))} coefficients")
    if w and len(w.get("terms", [])) != sub.get("rank"):
        errors.append(f"rank is {sub.get('rank')} but the witness has "
                      f"{len(w.get('terms', []))} terms")
    for c in (w or {}).get("coeffs", []):
        if any(ch in c for ch in ".eE") and "sqrt" not in c and "exp" not in c:
            errors.append(f"coefficient {c!r} looks like a float; "
                          "coefficients must be exact")

    comp = sub.get("provenance", {}).get("compute")
    if comp is not None and not comp:
        errors.append("provenance.compute is present but empty; either report "
                      "what the search cost or drop the field")
    if comp and sub.get("provenance", {}).get("method") == "literature":
        notes.append("compute is reported for a literature value; the ledger "
                     "attributes it to this submission, not to the cited work")
    if d == "upper" and not w and "lean" not in sub:
        notes.append("no decomposition and no Lean proof, so this records as "
                     "cited and cannot hold a record")
    budget = (sub.get("certificate") or {}).get("budget_s")
    if budget is not None and budget > 900 and not comp:
        errors.append("a certificate budget above the default 900 s must come with "
                      "provenance.compute, so the ledger records what the bound cost")
    if budget is not None and budget <= 900:
        notes.append("budget_s at or below the default 900 s has no effect; drop it")
    cert = sub.get("certificate") or {}
    if cert.get("attested"):
        # An attested bound rests on an enumeration the certificate does not
        # re-run. Its cost belongs in the ledger, and it cannot at the same
        # time claim that the pipeline confirmed the whole argument.
        if not comp:
            errors.append("certificate.attested requires provenance.compute, so the "
                          "ledger records what the offline enumeration cost")
        if cert.get("exact"):
            errors.append("certificate.attested and exact: true are mutually exclusive; "
                          "the enumeration is not re-run under the budget, so the "
                          "bound earns attested, not verified")
        notes.append("attested: the certificate must re-run the declared number of "
                     "batches from scratch and only hash the rest; say in notes what "
                     "completeness rests on")
    if d == "lower" and "certificate" not in sub and "lean" not in sub:
        notes.append("no certificate and no Lean proof, so this records as "
                     "cited and cannot hold a record")
    return errors, notes


def main(argv):
    schema = json.load(open(SCHEMA))
    paths = argv[1:] or sorted(glob.glob(os.path.join(ROOT, "bounds", "*.json")))
    bad = 0
    for path in paths:
        name = os.path.basename(path)
        try:
            sub = json.load(open(path))
        except json.JSONDecodeError as exc:
            print(f"FAIL  {name}  not valid JSON: {exc}")
            bad += 1
            continue
        problems = [f"{'.'.join(str(x) for x in e.path) or '<root>'}: {e.message}"
                    for e in jsonschema.Draft202012Validator(schema).iter_errors(sub)]
        errors, notes = tier_requirements(sub)
        problems += errors
        if problems:
            bad += 1
            print(f"FAIL  {name}")
            for p in problems:
                print(f"      {p}")
        else:
            print(f"OK    {name}")
        for n in notes:
            print(f"      note: {n}")
    print(f"\n{len(paths) - bad} of {len(paths)} valid")
    return 1 if bad else 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
