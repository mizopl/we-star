#!/usr/bin/env python3
"""Standalone Exact Verifier for Degree-69 Binary Littlewood Flat Polynomials (N = 70).

Verifies BOTH:
  1. Exact EinsteinArena / AlphaEvolve V2 1,000,000-point grid metric:
       C+_EA = max_{j=0..999999} |g(exp(2*pi*i * j / 999999))| / sqrt(71)
  2. Rigorous continuous supremum on the entire unit circle |z| = 1 via
     exact integer autocorrelation R(m), second-derivative bound
     M2 = 2 * sum_{m=1}^{69} m^2 |R(m)|, G = 262144 FFT grid + Newton refinement,
     and Taylor's theorem around the global maximizer theta* (where f'(theta*) = 0):
       sup_{|z|=1} |g(z)| <= sqrt( max_j f(theta_j) + (1/8) * M2 * (2*pi/G)^2 ).

Exit codes:
  - 0: All verified certificates are valid N=70 {-1,+1} polynomials with internally
       consistent continuous Taylor-Bernstein bounds strictly beating EA-2026 (1.28093205).
       (Note: Strict beat vs EinsteinArena live #1 1.25945717 is reported transparently
       as False when matched rather than strictly beaten.)
  - 1: Invalid certificate, failed bound consistency, failure to beat EA-2026, or --corrupt.
"""

import argparse
import json
import math
import sys
from pathlib import Path
import numpy as np


BAR_ALPHAEVOLVE = 1.3409252794557085
BAR_EINSTEIN_REPO = 1.2809320527987995
BAR_EINSTEIN_LIVE = 1.2594571732205586


def eval_einstein_arena_exact(coeffs: np.ndarray) -> float:
    """Bit-identical to EinsteinArena analysis.ipynb evaluate():
    np.poly1d(coefficients), zs = np.exp(1j * np.linspace(0, 2*pi, 1_000_000)).
    """
    c = np.asarray(coeffs, dtype=np.float64)
    assert c.ndim == 1 and c.size == 70, f"Expected 70 coeffs, got {c.shape}"
    assert np.all((c == 1.0) | (c == -1.0)), "All coefficients must be +1 or -1"

    n_pts = 1_000_000
    thetas = np.linspace(0.0, 2.0 * np.pi, n_pts)
    poly_fn = np.poly1d(c)
    max_val = 0.0
    chunk = 100_000
    for start in range(0, n_pts, chunk):
        zs = np.exp(1j * thetas[start : start + chunk])
        m = float(np.max(np.abs(poly_fn(zs))))
        if m > max_val:
            max_val = m
    return max_val / math.sqrt(71.0)


def eval_certified_supremum(coeffs: np.ndarray) -> dict:
    """Computes exact lower bound (Newton peak) and rigorous continuous upper bound."""
    c = np.asarray(coeffs, dtype=np.int64)
    n = c.size
    r = np.array([int(np.dot(c[: n - m], c[m:])) for m in range(n)], dtype=np.int64)
    sum_r2 = int(np.sum(r[1:] ** 2))
    merit_factor = (n * n) / (2.0 * sum_r2) if sum_r2 > 0 else float("inf")
    psl = int(np.max(np.abs(r[1:])))

    ms = np.arange(1, n, dtype=np.int64)
    m2 = float(2 * np.sum((ms * ms) * np.abs(r[1:])))

    grid_n = 262144
    buf = np.zeros(grid_n, dtype=np.float64)
    buf[:n] = c.astype(np.float64)
    spec = np.fft.rfft(buf)
    f_grid = (spec.real * spec.real) + (spec.imag * spec.imag)
    idx_max = int(np.argmax(f_grid))
    f_max_grid = float(f_grid[idx_max])

    theta = 2.0 * math.pi * idx_max / grid_n
    ms_f = ms.astype(np.float64)
    r_f = r[1:].astype(np.float64)
    for _ in range(12):
        ang = ms_f * theta
        fp = -2.0 * float(np.dot(ms_f * r_f, np.sin(ang)))
        fpp = -2.0 * float(np.dot((ms_f * ms_f) * r_f, np.cos(ang)))
        if abs(fpp) < 1e-15:
            break
        step = fp / fpp
        theta -= step
        if abs(step) < 1e-15:
            break
    f_peak = float(r[0]) + 2.0 * float(np.dot(r_f, np.cos(ms_f * theta)))
    max_mod_lo = math.sqrt(max(f_peak, f_max_grid))

    h = 2.0 * math.pi / grid_n
    f_global_ub = f_max_grid + 0.125 * m2 * (h * h)
    max_mod_ub = math.sqrt(f_global_ub)

    return {
        "max_mod_lo": max_mod_lo,
        "max_mod_ub": max_mod_ub,
        "C_plus_71_lo": max_mod_lo / math.sqrt(71.0),
        "C_plus_71_ub": max_mod_ub / math.sqrt(71.0),
        "C_plus_70_lo": max_mod_lo / math.sqrt(70.0),
        "C_plus_70_ub": max_mod_ub / math.sqrt(70.0),
        "PSL": psl,
        "merit_factor": merit_factor,
        "sum_c": int(np.sum(c)),
        "E4": sum_r2,
    }


def load_coeffs(path: Path) -> np.ndarray:
    data = json.loads(path.read_text(encoding="utf-8"))
    arr = data["coefficients"] if isinstance(data, dict) else data
    return np.array(arr, dtype=np.int64)


def verify_one(path: Path, corrupt: bool = False) -> bool:
    c = load_coeffs(path)
    if corrupt:
        c[0] = 0
    if c.size != 70 or not np.all((c == 1) | (c == -1)):
        print(f"FAIL [{path.name}]: coefficients must be exactly 70 entries in {{-1, +1}}")
        return False

    ea = eval_einstein_arena_exact(c)
    sup = eval_certified_supremum(c)
    if not (sup["C_plus_71_lo"] <= sup["C_plus_71_ub"] and ea <= sup["C_plus_71_ub"] + 1e-12):
        print(f"FAIL [{path.name}]: continuous Taylor-Bernstein bound inconsistency")
        return False

    beats_repo = sup["C_plus_71_ub"] < BAR_EINSTEIN_REPO
    beats_live = sup["C_plus_71_ub"] < BAR_EINSTEIN_LIVE
    print(f"PASS [{path.name}]")
    print(
        f"  N=70  all in {{-1,+1}}=True  sum={sup['sum_c']}  E4={sup['E4']}  "
        f"PSL={sup['PSL']}  MeritFactor={sup['merit_factor']:.6f}"
    )
    print(f"  EinsteinArena (1e6 pts) C+   = {ea:.12f}")
    print(
        f"  Certified sup/sqrt(71)       in "
        f"[{sup['C_plus_71_lo']:.12f}, {sup['C_plus_71_ub']:.12f}]"
    )
    print(
        f"  Certified sup/sqrt(70) (RMS) in "
        f"[{sup['C_plus_70_lo']:.12f}, {sup['C_plus_70_ub']:.12f}]"
    )
    print(
        f"  Strict beat vs EA-repo ({BAR_EINSTEIN_REPO:.6f}): {beats_repo} "
        f"(delta={sup['C_plus_71_ub'] - BAR_EINSTEIN_REPO:+.8f})"
    )
    live_note = (
        "STRICT BEAT"
        if beats_live
        else (
            "15-DIGIT MATCH (not strictly below)"
            if abs(ea - BAR_EINSTEIN_LIVE) < 1e-11
            else "above live #1 (not strictly below)"
        )
    )
    print(
        f"  Comparison vs EA-live ({BAR_EINSTEIN_LIVE:.6f}): {live_note} "
        f"(delta={sup['C_plus_71_ub'] - BAR_EINSTEIN_LIVE:+.8f})"
    )
    return beats_repo


def main() -> None:
    ap = argparse.ArgumentParser(description="Verify degree-69 binary Littlewood flat polynomials.")
    ap.add_argument("certs", nargs="*", help="Certificate JSON paths (defaults to certificates/*.json)")
    ap.add_argument("--corrupt", action="store_true", help="Inject invalid coefficient (must exit rc=1)")
    args = ap.parse_args()

    here = Path(__file__).resolve().parent
    if args.certs:
        targets = [Path(p) for p in args.certs]
    else:
        cert_dir = here / "certificates"
        targets = sorted(cert_dir.glob("*.json"))
        if args.corrupt and targets:
            targets = targets[:1]

    if not targets:
        print("FAIL: no certificate JSON files found")
        sys.exit(1)

    all_ok = True
    passed = 0
    for t in targets:
        if verify_one(t, corrupt=args.corrupt):
            passed += 1
        else:
            all_ok = False
    if all_ok:
        print(f"VERIFIED PASS: {passed}/{len(targets)} certificates passed exact checks & beat EA-2026.")
    sys.exit(0 if all_ok else 1)


if __name__ == "__main__":
    main()
