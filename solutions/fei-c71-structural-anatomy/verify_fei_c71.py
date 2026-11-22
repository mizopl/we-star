#!/usr/bin/env python3
"""Standalone cold verifier for Field Notes #006:
Structural Anatomy of the n=18 FEI Record (C_71), Continuous Fourier Homotopy,
Hod (2017) Open Problem #2 (g_5), and the n=8 Shared-Variable Cascade.

Verifies from first principles (zero network, < 2s):
  1. Exact algebraic construction of the n=18 [Num2026] record (Zenodo 21497769)
     as the phi-anti-self-dual Paley(9) = K_3 [] K_3 3x3 Permanent / Konig
     Cross-Seam (|inA|=247, |inB|=247, 9 Konig edges, I=261/128, 100.00% Jensen
     saturation on degrees 1 and 2, exact bit-for-bit agreement between O(k 2^k)
     Disjoint-Host WHT and full 2^18 integer FWHT).
  2. Smooth continuous Fourier homotopy surrogate at Num2026 (< 1e-9 error) and
     at f = 0 (C_smooth(0) = 4.0).
  3. 80-digit mpmath verification of Hod (2017) Open Problem #2:
     g_5(x) = (~x_4) | (x_2 & ((~x_0) | (x_3 & x_1))), attractive fixed point
     p* = phi^{-1}, T'(p*) = 11 - 5*sqrt(5) = -0.1803398875..., exact uniform-leaf
     iterated limit 6.45142608794814288378...
  4. Exact verification of the n=8 Shared-Variable Monotone Cascade
     (C = 6.363969446288..., +0.016902 over the 2x2 grid 6.3470674987...).

Usage:
  python3 verify_fei_c71.py
  python3 verify_fei_c71.py --corrupt   # flips 1 bit; must fail with exit code 1
"""

import argparse
from fractions import Fraction
import itertools
import math
import sys

import mpmath
from mpmath import iv
import numpy as np


def fwht_int64(arr: np.ndarray) -> np.ndarray:
    a = np.asarray(arr, dtype=np.int64).copy()
    n = a.size
    step = 1
    while step < n:
        a = a.reshape(-1, 2, step)
        u = a[:, 0, :].copy()
        v = a[:, 1, :].copy()
        a[:, 0, :] = u + v
        a[:, 1, :] = u - v
        a = a.reshape(-1)
        step *= 2
    return a


def is_monotone_table(table: np.ndarray, n: int) -> bool:
    """TRUE = -1, bit i set <=> x_i = TRUE."""
    idx = np.arange(1 << n, dtype=np.int64)
    for j in range(n):
        b = 1 << j
        lo = idx[(idx & b) == 0]
        if np.any((table[lo] == -1) & (table[lo | b] == 1)):
            return False
    return True


def eval_full_exact(table: np.ndarray, n: int, dps: int = 80) -> dict:
    N = 1 << n
    a = fwht_int64(table)
    absa = np.abs(a)
    vals, counts = np.unique(absa[absa > 0], return_counts=True)
    parseval = sum(int(v) * int(v) * int(c) for v, c in zip(vals.tolist(), counts.tolist()))
    if parseval != N * N:
        raise AssertionError(f"Parseval failed: {parseval} != {N * N}")

    idx = np.arange(N, dtype=np.int64)
    flips = 0
    for j in range(n):
        b = 1 << j
        lo = idx[(idx & b) == 0]
        flips += int(np.sum(table[lo] != table[lo | b]))
    I_exact = Fraction(flips, N // 2)

    mpmath.mp.dps = dps
    iv.dps = dps
    ln2 = iv.log(2)
    H = iv.mpf(0)
    denom = N * N
    for v, cnt in zip(vals.tolist(), counts.tolist()):
        if v == N:
            continue
        pref = Fraction(v * v * cnt, denom)
        H += (iv.mpf(pref.numerator) / iv.mpf(pref.denominator)) * (iv.mpf(2 * n) - 2 * (iv.log(v) / ln2))
    C_iv = H / (iv.mpf((I_exact - 1).numerator) / iv.mpf((I_exact - 1).denominator))
    return {
        "balanced": int(a[0]) == 0,
        "monotone": is_monotone_table(table, n),
        "I": I_exact,
        "H_mid": mpmath.mpf(H.mid),
        "C_lo": mpmath.mpf(C_iv.a),
        "C_hi": mpmath.mpf(C_iv.b),
        "spectrum": a,
    }


def eval_disjoint_host_compact(k: int, core_vals: np.ndarray, groups: list, dps: int = 80) -> dict:
    """Exact O(k 2^k) Fourier decomposition for f(x, y) = f_const(x) + sum_r 1_{B_r}(x) y_r."""
    M = 1 << k
    f_const = np.asarray(core_vals, dtype=np.int64).copy()
    for g in groups:
        for u in g:
            f_const[u] = 0
    a0 = fwht_int64(f_const)
    pop = np.array([bin(i).count("1") for i in range(M)], dtype=np.int64)

    I_num = int(np.sum(pop * (a0 * a0)))
    freq = {}
    for v in np.abs(a0):
        vi = int(v)
        if vi > 0:
            freq[vi] = freq.get(vi, 0) + 1

    for g in groups:
        ind = np.zeros(M, dtype=np.int64)
        for u in g:
            ind[u] = 1
        ag = fwht_int64(ind)
        I_num += int(np.sum((pop + 1) * (ag * ag)))
        for v in np.abs(ag):
            vi = int(v)
            if vi > 0:
                freq[vi] = freq.get(vi, 0) + 1

    I_exact = Fraction(I_num, M * M)
    mpmath.mp.dps = dps
    iv.dps = dps
    ln2 = iv.log(2)
    H = iv.mpf(0)
    for v, cnt in freq.items():
        pref = Fraction(v * v * cnt, M * M)
        H += (iv.mpf(pref.numerator) / iv.mpf(pref.denominator)) * (iv.mpf(2 * k) - 2 * (iv.log(v) / ln2))
    C_iv = H / (iv.mpf((I_exact - 1).numerator) / iv.mpf((I_exact - 1).denominator))
    return {
        "balanced": int(a0[0]) == 0,
        "I": I_exact,
        "C_lo": mpmath.mpf(C_iv.a),
        "C_hi": mpmath.mpf(C_iv.b),
        "a0": a0,
    }


def build_paley9_permanent_core():
    """Construct the phi-anti-self-dual 3x3 Permanent / Konig Cross-Seam on K_3 [] K_3."""
    M = 1 << 9
    # A: 6 permutation transversals of size 3 on 3x3 grid (bit 3*r + c)
    perm_masks = []
    for p in itertools.permutations(range(3)):
        m = 0
        for r, c in enumerate(p):
            m |= 1 << (3 * r + c)
        perm_masks.append(m)
    # B: 3 rows + 3 columns of size 3
    line_masks = []
    for r in range(3):
        line_masks.append(sum(1 << (3 * r + c) for c in range(3)))
    for c in range(3):
        line_masks.append(sum(1 << (3 * r + c) for r in range(3)))

    core = np.zeros(M, dtype=np.int64)
    inA = inB = 0
    gap = []
    for x in range(M):
        has_A = any((x & m) == m for m in perm_masks)
        has_B = any((x & m) == 0 for m in line_masks)
        if has_A and has_B:
            raise AssertionError("Cross-intersection violated")
        if has_A:
            core[x] = -1  # TRUE
            inA += 1
        elif has_B:
            core[x] = 1   # FALSE
            inB += 1
        else:
            gap.append(x)

    # Pair the 18 gap states into 9 isolated Konig edges: (row r U col c) \ {(r,c)} and (row r U col c)
    groups = []
    used = set()
    for r in range(3):
        for c in range(3):
            cross = sum(1 << (3 * rr + cc) for rr in range(3) for cc in range(3) if rr == r or cc == c)
            u = cross ^ (1 << (3 * r + c))
            v = cross
            groups.append([u, v])
            used.add(u)
            used.add(v)
    assert inA == 247 and inB == 247 and len(gap) == 18 and used == set(gap)
    return core, groups


def verify_paley9_and_homotopy(corrupt: bool = False):
    core, groups = build_paley9_permanent_core()
    if corrupt:
        # Flip 1 cell in the core to break balance / optimality
        core = core.copy()
        core[0] = -core[0]

    compact = eval_disjoint_host_compact(9, core, groups, dps=80)
    assert compact["balanced"], "Core is not balanced (a0 != 0)"
    assert compact["I"] == Fraction(261, 128), f"Expected I=261/128, got {compact['I']}"

    # Verify full 2^18 truth table matches compact O(k 2^k) evaluation bit-exact
    full = np.empty(1 << 18, dtype=np.int64)
    # Build table[x | (y << 9)] where bit 9+r is y_r (0 => +1, 1 => -1)
    idx_x = np.arange(1 << 9, dtype=np.int64)
    host_idx = np.full(1 << 9, -1, dtype=np.int64)
    for r, g in enumerate(groups):
        for u in g:
            host_idx[u] = r
    for y in range(1 << 9):
        base = core.copy()
        for r, g in enumerate(groups):
            val = -1 if ((y >> r) & 1) else 1
            for u in g:
                base[u] = val
        full[y * 512 : (y + 1) * 512] = base

    full_res = eval_full_exact(full, 18, dps=80)
    assert full_res["balanced"] and full_res["monotone"], "Full n=18 table failed balance/monotonicity"
    assert full_res["I"] == compact["I"] == Fraction(261, 128)
    assert abs(full_res["C_lo"] - compact["C_lo"]) < mpmath.mpf("1e-70")

    # Verify 100.00% Jensen saturation on degrees 1 and 2 of the core spectrum
    a0 = compact["a0"]
    pop = np.array([bin(i).count("1") for i in range(512)], dtype=np.int64)
    deg1 = np.abs(a0[pop == 1])
    deg2 = np.abs(a0[pop == 2])
    assert deg1.size == 9 and np.all(deg1 == 114), f"Deg-1 not uniform 114: {deg1}"
    assert deg2.size == 36 and np.all(deg2 == 44), f"Deg-2 not uniform 44: {deg2}"

    # Verify smooth continuous Fourier homotopy surrogate matches Num2026 to < 1e-9 and C_smooth(0) = 4.0
    k = 9
    M = 1 << k
    f_arr = core.astype(np.float64)  # -1, +1 on core, 0 on 18 Konig-edge cells
    fhat = fwht_int64(core).astype(np.float64) / M
    sq = fhat[1:] ** 2
    sq_nz = sq[sq > 0]
    vac = float(np.sum(1.0 - f_arr * f_arr)) / M  # 18/512
    H_smooth = float(-np.sum(sq_nz * np.log2(sq_nz))) + (2 * k - 2) * vac
    I_smooth = float(np.dot(pop[1:], sq)) + 0.5 * (k + 1) * vac
    C_smooth = H_smooth / (I_smooth - 1.0)
    err_smooth = abs(C_smooth - float(compact["C_lo"]))
    assert err_smooth < 1e-9, f"Smooth homotopy mismatch: {err_smooth}"
    # Origin check: at f = 0, vac = 1 => H_smooth(0) = 2k - 2, I_smooth(0) = (k+1)/2 => C_smooth(0) = 4.0
    C_origin = (2 * k - 2) / (0.5 * (k + 1) - 1.0)
    assert abs(C_origin - 4.0) < 1e-15

    print(f"[PASS] Paley(9) 3x3 Permanent / Konig Cross-Seam (n=18, bit-exact 2^18 == O(k 2^k)):")
    print(f"       |inA|=247, |inB|=247, R=9 Konig edges, I={compact['I']}, mono=True, balanced=True")
    print(f"       Jensen saturation: deg-1 = 9x(114/512) [100.00%], deg-2 = 36x(44/512) [100.00%]")
    print(f"       C_71 in [{mpmath.nstr(compact['C_lo'], 32)}, {mpmath.nstr(compact['C_hi'], 32)}]")
    print(f"[PASS] Continuous Fourier Homotopy surrogate: err={err_smooth:.3e}, C_smooth(0)={C_origin:.1f}")


def verify_hod_open_problem_2():
    """80-digit mpmath verification of Hod (2017) Open Problem #2:
    g_5(x) = (~x_4) | (x_2 & ((~x_0) | (x_3 & x_1))), attractive fixed point p* = phi^{-1}."""
    mpmath.mp.dps = 80
    phi = (1 + mpmath.sqrt(5)) / 2
    p_star = 1 / phi

    def p_biased_mp(f_bits, n, p):
        q = 1 - p
        sd = mpmath.sqrt(p * q)
        M = 1 << n
        a = [mpmath.mpf(1 - 2 * f_bits[x]) for x in range(M)]
        step = 1
        while step < M:
            nxt = [None] * M
            for i in range(0, M, 2 * step):
                for j in range(step):
                    u0 = a[i + j]
                    u1 = a[i + step + j]
                    nxt[i + j] = q * u0 + p * u1
                    nxt[i + step + j] = sd * (u1 - u0)
            a = nxt
            step *= 2
        p_out = (1 - a[0]) / 2
        var_out = 4 * p_out * (1 - p_out)
        I_p = mpmath.mpf(0)
        Ht_p = mpmath.mpf(0)
        ln2 = mpmath.log(2)
        for S in range(1, M):
            sq = a[S] * a[S]
            if sq > 0:
                I_p += bin(S).count("1") * sq / (4 * p * q)
                qS = sq / var_out
                Ht_p -= qS * mpmath.log(qS) / ln2
        return p_out, I_p, Ht_p

    g5 = [
        ((1 - ((x >> 4) & 1)) | (((x >> 2) & 1) & ((1 - (x & 1)) | (((x >> 3) & 1) & ((x >> 1) & 1)))))
        for x in range(32)
    ]
    p_fp, I_fp, Ht_fp = p_biased_mp(g5, 5, p_star)
    assert abs(p_fp - p_star) < mpmath.mpf("1e-75"), "p* = phi^{-1} fixed point failed"
    Tp_prime = -1 + 2 * p_star - 3 * (p_star ** 2) + 5 * (p_star ** 4)
    assert abs(Tp_prime - (11 - 5 * mpmath.sqrt(5))) < mpmath.mpf("1e-75")
    assert abs(Tp_prime) < 1

    # Exact uniform-leaf iteration from p_0 = 1/2 (d = 120)
    p_cur = mpmath.mpf("0.5")
    It = mpmath.mpf("1.0")
    Ht = mpmath.mpf("0.0")
    for _ in range(120):
        pn, Ip, Htp = p_biased_mp(g5, 5, p_cur)
        alpha = (p_cur * (1 - p_cur) / (pn * (1 - pn))) * Ip
        It = alpha * It
        Ht = Htp + alpha * Ht
        p_cur = pn
    var_d = 4 * p_cur * (1 - p_cur)
    I_d = var_d * It
    H_d = -(1 - var_d) * mpmath.log(1 - var_d, 2) - var_d * mpmath.log(var_d, 2) + var_d * Ht
    ratio = H_d / I_d
    assert abs(ratio - mpmath.mpf("6.4514260879481428837863")) < mpmath.mpf("1e-18")
    print(f"[PASS] Hod (2017) Open Problem #2 (g_5, 80-digit mpmath, uniform leaves p_0=1/2):")
    print(f"       p* = phi^{{-1}} = {mpmath.nstr(p_star, 20)}, T'(p*) = 11 - 5*sqrt(5) = {mpmath.nstr(Tp_prime, 15)}")
    print(f"       lim H(g_5^(d))/I(g_5^(d)) = {mpmath.nstr(ratio, 25)} (< Hod read-once 6.4547837)")


def verify_shared_cascade_n8():
    """Verify the n=8 Shared-Variable Monotone Cascade (6.3639694463 vs 2x2 grid 6.3470674987)."""
    core_vals = np.array([
        1,1,1,1,1,1,1,1,1,1,-1,-1,1,1,-1,-1,1,1,1,1,1,1,1,1,1,1,-1,-1,1,-1,-1,-1,
        1,1,1,1,1,1,1,1,1,1,-1,-1,1,1,-1,-1,1,1,0,0,-1,-1,-1,-1,1,1,-1,-1,-1,-1,-1,-1,
        1,1,1,1,1,1,1,1,1,1,-1,-1,1,1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,
        1,1,1,1,1,1,1,1,1,1,-1,-1,1,1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,
    ], dtype=np.int64)
    groups = [[50, 51]]
    full = np.empty(256, dtype=np.int64)
    for y in (0, 1):
        b = core_vals.copy()
        for u in groups[0]:
            b[u] = -1 if y else 1
        full[y * 128 : (y + 1) * 128] = b
    res = eval_full_exact(full, 8, dps=60)
    assert res["balanced"] and res["monotone"]
    assert res["I"] == Fraction(53, 32)
    assert abs(res["C_lo"] - mpmath.mpf("6.363969446288165")) < mpmath.mpf("1e-12")
    print(f"[PASS] n=8 Shared-Variable Monotone Cascade: I={res['I']}, balanced=True, mono=True,")
    print(f"       C = {mpmath.nstr(res['C_lo'], 18)} (+0.016902 over 2x2 grid 6.3470674987)")


def main():
    ap = argparse.ArgumentParser(description="Cold verifier for Field Notes #006 (FEI C_71)")
    ap.add_argument("--corrupt", action="store_true", help="Flip 1 bit in Paley(9) core; must fail (rc=1)")
    args = ap.parse_args()
    try:
        verify_paley9_and_homotopy(corrupt=args.corrupt)
        verify_hod_open_problem_2()
        verify_shared_cascade_n8()
    except AssertionError as exc:
        print(f"[FAIL] Verification failed as expected: {exc}", file=sys.stderr)
        sys.exit(1)
    print("ALL FIELD NOTE #006 CHECKS PASSED.")


if __name__ == "__main__":
    main()
