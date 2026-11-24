#!/usr/bin/env python3
"""Standalone Verifier for 50/50 Exact Binary Littlewood Minima (N = 10..59, deg 9..58).

Standard library + NumPy only; zero strippable asserts.
Verification scope (honest boundary):
  - Default mode (~0.12s): verifies SHA256SUMS, all 50/50 binary witnesses, exact E4,
    continuous Taylor-Bernstein M_n & C+ brackets (gap < 5e-6), independent refutation of
    recorded coarse_hits, Mod-4 E4 / Golay-skew laws, and presence of N=53..59 dual-grid
    attestation metadata. It does NOT replay GPU Stage-2 lower bounds for N=27..59.
  - --full-numpy: independently replays full Stage-1 + Stage-2 lower bounds (plus --corrupt)
    in pure NumPy for N=10..26 (17 dimensions).
  - --c11-dims 53,54,55,56,57,58,59: compiles verify_stage1_c.c and independently replays
    all 22/22 Stage-1 SHA-256 survivor sets across both primary (G=256) and alternate (G=128) grids.
  - Stage-2 exhaustive lower bounds for N=27..59 remain GPU-attested by engine5_v51_cuda_mitm.cu.

Run under:
  env -i PATH=/opt/homebrew/bin:/usr/bin:/bin python3 verify.py
  env -i PATH=/opt/homebrew/bin:/usr/bin:/bin python3 verify.py --corrupt   # MUST exit 1
"""
from __future__ import annotations

import argparse
import hashlib
import json
import math
import os
import subprocess
import sys
import tempfile
import time
from pathlib import Path

if sys.version_info < (3, 10):
    sys.stderr.write(f"ERROR: Python >= 3.10 required, got {sys.version.split()[0]}\n")
    sys.exit(2)

import numpy as np

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))
from verify_dual_lb import eval_certified_supremum_general, verify_d2_cooley_tukey_v3_cert


def _require(cond: bool, msg: str) -> None:
    if not cond:
        raise ValueError(msg)


def _sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def verify_sha256sums(sums_path: Path) -> int:
    _require(sums_path.exists(), f"Missing {sums_path.name}")
    checked = 0
    seen: set[str] = set()
    for lineno, raw in enumerate(sums_path.read_text(encoding="utf-8").splitlines(), 1):
        line = raw.strip()
        if not line:
            continue
        parts = line.split()
        _require(len(parts) == 2, f"{sums_path.name}:{lineno} malformed line: {raw!r}")
        expected_hex, rel = parts
        _require(
            len(expected_hex) == 64 and all(ch in "0123456789abcdef" for ch in expected_hex),
            f"{sums_path.name}:{lineno} invalid sha256 hex: {expected_hex!r}",
        )
        target = (ROOT / rel).resolve()
        _require(ROOT in target.parents or target == ROOT, f"Path escape: {rel}")
        _require(target.exists(), f"Missing pinned file: {rel}")
        actual = _sha256_file(target)
        _require(actual == expected_hex, f"SHA-256 mismatch on {rel}: expected {expected_hex}, got {actual}")
        seen.add(rel)
        checked += 1
    for N in range(10, 60):
        rel = f"certs/cert_d2_exact_N{N}.json"
        _require(rel in seen, f"Unpinned certificate in {sums_path.name}: {rel}")
    return checked


def verify_all_50_certs(corrupt: bool = False) -> dict:
    certs_dir = ROOT / "certs"
    table_path = ROOT / "TABLE_N10_N59.json"
    _require(table_path.exists(), "Missing TABLE_N10_N59.json")
    table = json.loads(table_path.read_text(encoding="utf-8"))
    rows_by_n = {int(r["N"]): r for r in table.get("rows", [])}
    _require(len(rows_by_n) == 50, f"Expected 50 rows in TABLE_N10_N59.json, got {len(rows_by_n)}")

    skew_odd_count = 0
    odd_count = 0
    mod4_violations = 0
    max_gap_mn = 0.0

    for N in range(10, 60):
        p = certs_dir / f"cert_d2_exact_N{N}.json"
        _require(p.exists(), f"Missing certificate: {p.name}")
        c = json.loads(p.read_text(encoding="utf-8"))
        _require(int(c["N"]) == N, f"N mismatch in {p.name}")

        w = np.array(c["witness_c"], dtype=np.int64)
        if corrupt and N == 57:
            # Flip 1 bit on N=57 to confirm the verifier strictly rejects corrupted witnesses
            w[0] = -w[0]

        _require(w.size == N and bool(np.all((w == 1) | (w == -1))), f"N={N}: non-binary witness")
        info = eval_certified_supremum_general(w, G=131072)
        _require(info["E4"] == int(c["witness_E4"]), f"N={N}: E4 mismatch ({info['E4']} != {c['witness_E4']})")

        M_lb = float(c["certified_LB_M"])
        _require(info["f_lo"] > M_lb, f"N={N}: certified LB {M_lb} >= witness f_lo {info['f_lo']}")

        lb_mn = math.sqrt(M_lb / float(N))
        lb_cp = math.sqrt(M_lb / float(N + 1))
        gap_mn = info["M_n_ub"] - lb_mn
        gap_cp = info["C_plus_ub"] - lb_cp
        max_gap_mn = max(max_gap_mn, gap_mn)
        _require(gap_mn < 5e-6 and gap_cp < 5e-6, f"N={N}: bracket width too large (M_n={gap_mn:.2e})")

        tol = 1e-12 if c.get("hardened_v4_2") else 1e-8
        _require(
            info["C_plus_lo"] - tol <= float(c["witness_C_plus_lo"])
            <= float(c["witness_C_plus_ub"]) <= info["C_plus_ub"] + tol,
            f"N={N}: C+ bracket mismatch",
        )

        # Independently refute every recorded coarse_hit
        M_e, M_o = (N + 1) // 2, N // 2
        for gec, goc in c.get("coarse_hits", []):
            ch = np.empty(N, dtype=np.int64)
            ch[0] = 1
            ch[1] = 1
            for m in range(1, M_e):
                ch[2 * m] = 1 if ((int(gec) >> (m - 1)) & 1) else -1
            for m in range(1, M_o):
                ch[2 * m + 1] = 1 if ((int(goc) >> (m - 1)) & 1) else -1
            ch_info = eval_certified_supremum_general(ch, G=131072)
            _require(ch_info["f_lo"] > M_lb, f"N={N}: coarse_hit ({gec},{goc}) violates M_lb")

        # Dual-grid cross-check attestation metadata on frontier N=53..59 (GPU-attested; C11 replays Stage-1 with --c11-dims)
        if N >= 53:
            cc = c.get("cross_check_alt_G")
            _require(bool(cc and cc.get("verified_zero_below_M_target") is True), f"N={N}: missing dual-grid attestation metadata")

        # Verify exact cyclic mod-4 E4 lower bound on N == 2 (mod 4)
        if N % 4 == 2:
            if info["E4"] < (3 * N - 4) // 2:
                mod4_violations += 1

        # Verify Golay skew-symmetry statistics on odd N
        if N % 2 == 1:
            odd_count += 1
            m = N // 2
            is_skew = all(int(w[m + j]) == ((-1) ** j) * int(w[m - j]) for j in range(1, m + 1))
            if is_skew:
                skew_odd_count += 1
                # Verify all-even-lag mod-4 theorem r_{2k} == N (mod 4)
                for k in range(1, m + 1):
                    lag = 2 * k
                    r_lag = int(np.dot(w[: N - lag], w[lag:]))
                    if (r_lag - N) % 4 != 0:
                        mod4_violations += 1

        # Spot exact algebraic theorem at N=57: |P_56(i)|^2 == 89
        if N == 57:
            re_i = int(np.sum(w[0::2] * np.array([1 if j % 2 == 0 else -1 for j in range(29)])))
            im_i = int(np.sum(w[1::2] * np.array([1 if j % 2 == 0 else -1 for j in range(28)])))
            _require(re_i * re_i + im_i * im_i == 89, f"N=57: |P(i)|^2 != 89 (got {re_i*re_i + im_i*im_i})")

        # Cross-check table row witness & E4 parity
        row = rows_by_n[N]
        wit_str = "".join("+" if x > 0 else "-" for x in w)
        _require(row["witness_str"] == wit_str, f"N={N}: TABLE_N10_N59.json witness mismatch")
        _require(int(row["E4"]) == info["E4"], f"N={N}: TABLE_N10_N59.json E4 mismatch")

    _require(mod4_violations == 0, f"Mod-4 E4/skew violations: {mod4_violations}")
    return {
        "certs_verified": 50,
        "max_gap_mn": max_gap_mn,
        "odd_total": odd_count,
        "odd_golay_skew": skew_odd_count,
        "mod4_violations": mod4_violations,
    }


def run_full_numpy_replay() -> int:
    count = 0
    for N in range(10, 27):
        p = ROOT / "certs" / f"cert_d2_exact_N{N}.json"
        cert = json.loads(p.read_text(encoding="utf-8"))
        _require(bool(verify_d2_cooley_tukey_v3_cert(cert, corrupt=False)), f"Pure-NumPy replay failed on N={N}")
        _require(not bool(verify_d2_cooley_tukey_v3_cert(cert, corrupt=True)), f"Pure-NumPy --corrupt did not reject N={N}")
        count += 1
    return count


def run_c11_stage1_checks(dims: list[int]) -> int:
    c_src = ROOT / "verify_stage1_c.c"
    _require(c_src.exists(), "Missing verify_stage1_c.c")
    compiler = "/Library/Developer/CommandLineTools/usr/bin/clang"
    extra_flags: list[str] = []
    if os.path.exists(compiler):
        sdk = "/Library/Developer/CommandLineTools/SDKs/MacOSX.sdk"
        if os.path.isdir(sdk):
            extra_flags = ["-isysroot", sdk]
    else:
        compiler = "cc"
    with tempfile.TemporaryDirectory() as td:
        bin_path = Path(td) / "verify_stage1_c"
        r = subprocess.run(
            [compiler, "-O3", "-std=c11", *extra_flags, str(c_src), "-lm", "-o", str(bin_path)],
            capture_output=True, text=True,
        )
        _require(r.returncode == 0, f"C11 build failed: {r.stderr}")
        checks = 0
        for N in dims:
            c = json.loads((ROOT / "certs" / f"cert_d2_exact_N{N}.json").read_text(encoding="utf-8"))
            Me, Mo = (N + 1) // 2, N // 2
            M_lb = f"{float(c['certified_LB_M']):.17g}"
            eps = f"{float(c['eps_safe']):.17g}"
            G = str(int(c["G"]))
            out_e = subprocess.check_output(
                [str(bin_path), str(Me), str(Mo), M_lb, G, eps, "0" if N % 2 == 0 else "1"], text=True
            ).strip()
            ese = c["n_survivors"] if N % 2 == 0 else c["n_survivors_e_canon"]
            esha = c["survivor_codes_sha256"] if N % 2 == 0 else c["survivor_e_sha256"]
            _require(f"S={ese} sha256={esha}" in out_e, f"N={N} G={G} E mismatch: {out_e}")
            checks += 1
            if N % 2 == 1:
                out_o = subprocess.check_output(
                    [str(bin_path), str(Mo), str(Me), M_lb, G, eps, "0"], text=True
                ).strip()
                eso, esho = c["n_survivors_o"], c["survivor_o_sha256"]
                _require(f"S={eso} sha256={esho}" in out_o, f"N={N} G={G} O mismatch: {out_o}")
                checks += 1
            cc = c.get("cross_check_alt_G")
            if cc and "G_alt" in cc:
                Ga = str(int(cc["G_alt"]))
                out_ae = subprocess.check_output(
                    [str(bin_path), str(Me), str(Mo), M_lb, Ga, eps, "0" if N % 2 == 0 else "1"], text=True
                ).strip()
                _require(
                    f"S={cc['Se_alt']} sha256={cc['e_sha_alt']}" in out_ae,
                    f"N={N} G_alt={Ga} E mismatch: {out_ae}",
                )
                checks += 1
                if N % 2 == 1:
                    out_ao = subprocess.check_output(
                        [str(bin_path), str(Mo), str(Me), M_lb, Ga, eps, "0"], text=True
                    ).strip()
                    _require(
                        f"S={cc['So_alt']} sha256={cc['o_sha_alt']}" in out_ao,
                        f"N={N} G_alt={Ga} O mismatch: {out_ao}",
                    )
                    checks += 1
        return checks


def main() -> int:
    ap = argparse.ArgumentParser(description="Verifier for 50/50 exact Littlewood minima (N=10..59).")
    ap.add_argument("--corrupt", action="store_true", help="Inject 1-bit witness corruption (must fail rc=1).")
    ap.add_argument("--full-numpy", action="store_true", help="Replay full Stage-1+Stage-2 lower bounds in NumPy on N=10..26.")
    ap.add_argument("--c11-dims", default="", help="Comma-separated frontier dims (e.g. 53,54,55,56,57,58,59 for all 22 C11 checks).")
    args = ap.parse_args()

    t0 = time.time()
    n_pinned = verify_sha256sums(ROOT / "SHA256SUMS")
    stats = verify_all_50_certs(corrupt=args.corrupt)
    n_np = run_full_numpy_replay() if args.full_numpy else 0
    c11_dims = [int(x) for x in args.c11_dims.split(",") if x.strip()]
    n_c11 = run_c11_stage1_checks(c11_dims) if c11_dims else 0

    print(
        f"PASS: 50/50 witness brackets, SHA256SUMS ({n_pinned} files), coarse_hits, and Mod-4 laws checked "
        f"(max_gap_M={stats['max_gap_mn']:.2e}, odd_golay_skew={stats['odd_golay_skew']}/{stats['odd_total']}, "
        f"mod4_viols={stats['mod4_violations']}); "
        f"lower bounds replayed in NumPy for N=10..26: {n_np}/17 (--full-numpy); "
        f"Stage-1 C11 SHA-256 checks (G=256+128): {n_c11}/22 (--c11-dims); "
        f"N=27..59 Stage-2 lower bounds are GPU-attested (elapsed={time.time() - t0:.2f}s)"
    )
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except Exception as exc:
        sys.stderr.write(f"FAIL: {exc}\n")
        sys.exit(1)
