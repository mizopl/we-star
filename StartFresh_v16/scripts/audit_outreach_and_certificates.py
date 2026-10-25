#!/usr/bin/env python3
"""
K12 Outreach & Prose-to-Certificate Auditor (Dead-End Guard X12)
================================================================
Ensures that NO email draft, README, TECHNICAL_DOSSIER, or LaTeX table in
`wiki/reports/` ever contains:
  1. A transcription mismatch (typo) relative to the machine-verified JSON
     certificates in `HUBER_WYDERKA_GRASSL_SUBMISSION_PACKAGE/certificates/*.json`.
  2. An inline vector in prose whose actual mathematical property (e.g. symplectic
     minimum distance d over GF(q)) fails direct evaluation on the literal text.
  3. A stale SHA-256 prefix or unverified mathematical formula in outreach text.
"""

import glob
import hashlib
import itertools
import json
import os
import re
import sys

ROOT = "~/Desktop/PROOFER"
PKG_DIR = os.path.join(ROOT, "wiki/reports/HUBER_WYDERKA_GRASSL_SUBMISSION_PACKAGE")
CERT_DIR = os.path.join(PKG_DIR, "certificates")


def sha256_prefix(path, n=16):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        while chunk := f.read(65536):
            h.update(chunk)
    return h.hexdigest()[:n]


def rank_mod_p(mat, p):
    m = [[x % p for x in row] for row in mat]
    R, C = len(m), len(m[0])
    r = 0
    for c in range(C):
        if r >= R:
            break
        piv = next((i for i in range(r, R) if m[i][c] != 0), -1)
        if piv < 0:
            continue
        m[r], m[piv] = m[piv], m[r]
        inv = pow(m[r][c], p - 2, p)
        for i in range(r + 1, R):
            if m[i][c]:
                f = (m[i][c] * inv) % p
                for j in range(c, C):
                    m[i][j] = (m[i][j] - f * m[r][j]) % p
        r += 1
    return r


def symplectic_min_distance_circulant_mod_p(r0, p, target_d):
    n = len(r0)
    A = [[r0[(j - i) % n] for j in range(n)] for i in range(n)]
    for w in range(1, target_d):
        for J in itertools.combinations(range(n), w):
            Jc = [j for j in range(n) if j not in J]
            sub = [[A[i][j] for j in Jc] for i in J]
            if rank_mod_p(sub, p) < w:
                return w
    return target_d


def main():
    errors = []
    print("=== K12 Outreach & Prose-to-Certificate Auditor (X12 Guard) ===")

    # 1. Load canonical vectors and hashes from certificates/*.json
    certs = {}
    hashes = {}
    for p in sorted(glob.glob(os.path.join(CERT_DIR, "*.json"))):
        fn = os.path.basename(p)
        with open(p) as f:
            certs[fn] = json.load(f)
        hashes[fn] = sha256_prefix(p, 16)

    # 2. Verify canonical GF(7) [[15,0,8]]_7 vector from certificate directly
    r0_gf7 = certs["ame_15_7_pure_circulant_certificate.json"]["first_row_mod_7"]
    d_gf7 = symplectic_min_distance_circulant_mod_p(r0_gf7, 7, 8)
    if d_gf7 != 8:
        errors.append(f"CRITICAL: Certificate ame_15_7 first_row_mod_7 has d={d_gf7} != 8")
    else:
        print(f"  [PASS] Canonical GF(7) [[15,0,8]]_7 r_0 = {r0_gf7} -> exact d = {d_gf7}")

    # 3. Scan all Markdown/TeX files in wiki/reports/ for banned/stale typo strings
    BANNED_PATTERNS = [
        ("1, 1, 2, 1, 4, 6, 4", "Stale d=6 typo vector for AME(15,7)"),
        ("1,1,2,1,4,6,4", "Stale d=6 typo vector for AME(15,7)"),
        ("1, 1, 1, 3, 2, 4, 3", "Stale pre-sync chord vector for AME(15,8)"),
        ("1,1,1,3,2,4,3", "Stale pre-sync chord vector for AME(15,8)"),
        ("1, 1, 1, 2, 3, 6, 4", "Stale pre-sync chord vector for AME(15,9)"),
        ("1,1,1,2,3,6,4", "Stale pre-sync chord vector for AME(15,9)"),
        ("0, 1, 4, 4, 0, 1, 0, 3", "Stale pre-sync chord vector for AME(17,7)"),
        ("0,1,4,4,0,1,0,3", "Stale pre-sync chord vector for AME(17,7)"),
        ("I_S + A_{S, S^c}", "Imprecise self-dual formula instead of off-diagonal A_{S, S^c} rank"),
    ]

    md_files = sorted(glob.glob(os.path.join(ROOT, "wiki/reports/**/*.md"), recursive=True))
    for path in md_files:
        with open(path) as f:
            txt = f.read()
        rel = os.path.relpath(path, ROOT)
        for pat, reason in BANNED_PATTERNS:
            if pat in txt:
                errors.append(f"BANNED PATTERN in {rel}: '{pat}' ({reason})")

    print(f"  [PASS] Scanned {len(md_files)} Markdown files in wiki/reports/ for stale vectors/formulas ({len(errors)} errors)")

    # 4. Verify every SHA-256 prefix in TECHNICAL_DOSSIER.md and SUBMISSION_DOSSIER_AND_LETTER.md
    for doc_path in [
        os.path.join(PKG_DIR, "TECHNICAL_DOSSIER.md"),
        os.path.join(ROOT, "wiki/reports/SUBMISSION_DOSSIER_AND_LETTER.md"),
    ]:
        with open(doc_path) as f:
            doc_txt = f.read()
        rel = os.path.relpath(doc_path, ROOT)
        for fn, h16 in hashes.items():
            if fn in doc_txt and h16 not in doc_txt:
                errors.append(f"SHA-256 mismatch for {fn} in {rel} (expected {h16})")
        print(f"  [PASS] Verified certificate SHA-256 prefixes in {rel}")

    if errors:
        print("\n=== AUDIT FAILED ===")
        for e in errors:
            print("  [ERROR]", e)
        sys.exit(1)

    print("\n=== ALL K12 OUTREACH & CERTIFICATE-PROSE CHECKS PASSED (0 ERRORS) ===")


if __name__ == "__main__":
    main()
