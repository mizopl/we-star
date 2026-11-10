"""Exact Z[i] certificate for the two-qubit controlled-S magic state at m = 2, 3, 4.

Printed claims (when all checks pass):
    CERTIFIED chi(CS^2) >= 3
    CERTIFIED chi(CS^3) >= 4
    CERTIFIED chi(CS^4) >= 4

Mathematical summary (100% exact Gaussian-integer arithmetic, ~2.5 s on 1 core):
1. Even-qubit (I (x) H)^m Clifford postselection lemma:
   For one copy of |CS> = (|00> + |01> + |10> + i|11>) / 2, applying the local
   Clifford unitary I (x) H and projecting the second qubit onto <0| gives:
       (<0|_2 (I (x) H)) |CS> = (2 |0> + (1 + i) |1>) / (2 sqrt(2)) = (2 sqrt(2))^{-1} |Psi_1>.
   Because I (x) H is a Clifford unitary (preserving stabilizer rank) and
   computational-basis projection <0| maps every stabilizer state to a stabilizer
   state or zero (Lean: stabRank_projection in LeanProofs/Stabilizer/SliceP.lean),
   for every m >= 1:
       chi(|CS>^{ot m}) >= chi(|Psi_m>),   where |Psi_m> = (2 |0> + (1 + i) |1>)^{ot m} in Z[i]^{2^m}.
   This identity is checked symbolically against stabrank_verify.target_vector("CS", m)
   for m = 1, 2, 3 before any bound is decided.

2. Exact Z[i] rank-2 exclusion at m = 2 (chi(CS^2) >= chi(Psi_2) = 3):
   On 2 qubits (D_2 = 60 stabilizer states in Z[i]^4), exhaustive fraction-free
   Gaussian-integer linear solves over all C(60, 2) = 1,770 pairs find 0 rank-2
   decompositions of |Psi_2>, while exhaustive check over all C(60, 3) = 34,220
   triples finds all 483 exact rank-3 decompositions of |Psi_2> (positive control).

3. Two-handle exact Z[i] rank-3 exclusion at m = 3 (chi(CS^3) >= chi(Psi_3) = 4):
   - Handle A (1-qubit Pauli slice-and-lift Psi_2 -> Psi_3 on D_2):
     Slicing |Psi_3> along qubit 1 gives slice 0 equal to 2 |Psi_2> and slice 1
     equal to (1 + i) |Psi_2>. Because chi(Psi_2) = 3, any rank-3 decomposition
     of |Psi_3> restricts on slice 0 to one of the 483 exact rank-3 decompositions
     of |Psi_2> and on slice 1 to phased 2-qubit Pauli translates mu_j P_j a_j
     satisfying 2 sum_{j=1}^3 d_j (mu_j P_j a_j) = (1 + i) D |Psi_2>. Checking
     all 16^3 = 4,096 phased Pauli triples across all 483 decompositions in exact
     Z[i] arithmetic finds 0 lifts.
   - Handle B (unconditional exhaustive 1-pivot quotient on D_3 = 1,080 states):
     Independently of slice-and-lift and with zero symmetry assumptions, sweeping
     all 1,080 states s_1 in D_3 as pivots and grouping the double quotient
     q_2(s) in Z[i]^7 modulo span_{Q(i)}(Psi_3, s_1) into exact primitive Z[i]-rays
     finds 0 rank-3 decompositions of |Psi_3>, whereas the 4 symmetric product
     states {(|0> + i^k |1>)^{ot 3}}_{k=0}^3 in D_3 give an explicit exact rank-4
     decomposition of |Psi_3> (positive control: chi(Psi_3) = 4).

4. Projection monotonicity to m = 4 (chi(CS^4) >= 4):
   Since (<00|_{7,8} (x) I_6) |CS>^{ot 4} = (1/2) |CS>^{ot 3} (and equivalently
   (<0|_4 (x) I_3) |Psi_4> = 2 |Psi_3>), projection monotonicity gives
   chi(|CS>^{ot 4}) >= chi(|CS>^{ot 3}) >= 4.
"""

from __future__ import annotations

import itertools
import math
import os
import sys
import time

os.environ.setdefault("OMP_NUM_THREADS", "1")

import numpy as np  # noqa: E402
import sympy as sp  # noqa: E402

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from stabrank_verify import target_vector  # noqa: E402


def fail(msg: str) -> None:
    print(f"FAILED: {msg}", file=sys.stderr, flush=True)
    raise SystemExit(1)


def rref_subspaces(n: int, k: int):
    for piv in itertools.combinations(range(n), k):
        free = [(r, c) for r in range(k) for c in range(n) if c not in piv and c > piv[r]]
        for vals in itertools.product((0, 1), repeat=len(free)):
            W = np.zeros((k, n), np.int64)
            for r in range(k):
                W[r, piv[r]] = 1
            for (r, c), a in zip(free, vals):
                W[r, c] = a
            yield piv, W


def grid(vals, k: int) -> np.ndarray:
    rows = list(itertools.product(vals, repeat=k))
    return np.array(rows, np.int64).reshape(len(rows), k)


def stabilizer_exponents(n: int) -> np.ndarray:
    dim = 1 << n
    rows = []
    for k in range(n + 1):
        ys = grid((0, 1), k)
        pairs = [(i, j) for i in range(k) for j in range(i + 1, k)]
        quad = np.array([[y[i] * y[j] for (i, j) in pairs] for y in ys], np.int64).reshape(len(ys), len(pairs))
        Qs = grid((0, 1), len(pairs))
        Ls = grid(range(4), k)
        ph = (2 * (Qs @ quad.T))[:, None, :] + (Ls @ ys.T)[None, :, :]
        ph = (ph % 4).reshape(-1, len(ys))
        weights = 1 << (n - 1 - np.arange(n))
        for piv, W in rref_subspaces(n, k):
            nonpiv = [c for c in range(n) if c not in piv]
            for x0f in itertools.product((0, 1), repeat=n - k):
                x0 = np.zeros(n, np.int64)
                x0[nonpiv] = x0f
                pts = ((x0[None, :] + ys @ W) % 2) @ weights
                E = np.full((ph.shape[0], dim), -1, np.int8)
                E[:, pts] = ph
                rows.append(E)
    E = np.concatenate(rows)
    expect = 1 << n
    for j in range(1, n + 1):
        expect *= (1 << j) + 1
    if E.shape[0] != expect:
        fail(f"{E.shape[0]} stabilizer states on {n} qubits, expected {expect}")
    first = np.argmax(E >= 0, axis=1)
    base = E[np.arange(E.shape[0]), first].astype(np.int16)
    return np.where(E >= 0, (E.astype(np.int16) - base[:, None]) % 4, -1).astype(np.int8)


def dictionary_zi(n: int) -> tuple[np.ndarray, np.ndarray]:
    E = stabilizer_exponents(n)
    lut_r = np.array([1, 0, -1, 0, 0], dtype=np.int64)
    lut_i = np.array([0, 1, 0, -1, 0], dtype=np.int64)
    idx = np.where(E >= 0, E, 4)
    return lut_r[idx], lut_i[idx]


def psi_target_zi(m: int) -> tuple[np.ndarray, np.ndarray]:
    """Exact Gaussian-integer arrays (Tr, Ti) for |Psi_m> = (2|0> + (1+i)|1>)^{ot m}."""
    dim = 1 << m
    Tr = np.zeros(dim, dtype=np.int64)
    Ti = np.zeros(dim, dtype=np.int64)
    for x in range(dim):
        w = bin(x).count("1")
        scale = 1 << (m - w)
        pr, pi = 1, 0
        for _ in range(w):
            pr, pi = pr - pi, pr + pi
        Tr[x] = scale * pr
        Ti[x] = scale * pi
    return Tr, Ti


def check_symbolic_cs_postselection() -> None:
    """Verify symbolically against stabrank_verify.target_vector("CS", m) for m = 1, 2, 3
    that applying (<0|_2 (I (x) H))^{ot m} to |CS>^{ot m} equals (2 sqrt(2))^{-m} |Psi_m>,
    and that (<00|_{7,8} (x) I_6) |CS>^{ot 4} = (1/2) |CS>^{ot 3}."""
    for m in (1, 2, 3):
        cs_m = target_vector("CS", m)
        Tr, Ti = psi_target_zi(m)
        scale = (2 * sp.sqrt(2)) ** m
        # Applying <0|_2 (I (x) H) to the second qubit of each copy sums over the even-qubit bits
        # and divides by sqrt(2)^m, so scale * postselected(x) = 2^m * sum_{y in F_2^m} cs_m(x_1, y_1, ..., x_m, y_m)
        for x in range(1 << m):
            acc = sp.Integer(0)
            for y in range(1 << m):
                idx = 0
                for bit in range(m):
                    xb = (x >> (m - 1 - bit)) & 1
                    yb = (y >> (m - 1 - bit)) & 1
                    idx = (idx << 2) | (xb << 1) | yb
                acc += cs_m[idx]
            want = int(Tr[x]) + sp.I * int(Ti[x])
            if sp.simplify((2 ** m) * acc - want) != 0:
                fail(f"symbolic postselection mismatch for CS at m={m}, x={x}")
    # Also check <00|_{7,8} |CS>^4 = (1/2) |CS>^3
    cs3 = target_vector("CS", 3)
    cs4 = target_vector("CS", 4)
    for idx3 in range(64):
        if sp.simplify(2 * cs4[idx3 << 2] - cs3[idx3]) != 0:
            fail(f"symbolic <00| projection mismatch for CS^4 at idx={idx3}")


def canonical_ray_groups(Qr: np.ndarray, Qi: np.ndarray) -> tuple[list[int], list[list[int]]]:
    mag2 = Qr * Qr + Qi * Qi
    zero_mask = np.all(mag2 == 0, axis=1)
    zero_ids = np.flatnonzero(zero_mask).tolist()
    nz_ids = np.flatnonzero(~zero_mask)
    if len(nz_ids) == 0:
        return zero_ids, []
    Qr_nz, Qi_nz, mag2_nz = Qr[nz_ids], Qi[nz_ids], mag2[nz_ids]
    first_col = np.argmax(mag2_nz > 0, axis=1)
    row_idx = np.arange(len(nz_ids))
    cr = Qr_nz[row_idx, first_col][:, None]
    ci = Qi_nz[row_idx, first_col][:, None]
    Nr = cr * Qr_nz + ci * Qi_nz
    Ni = cr * Qi_nz - ci * Qr_nz
    g = np.gcd(np.gcd.reduce(np.abs(Nr), axis=1), np.gcd.reduce(np.abs(Ni), axis=1))[:, None]
    Nr //= g
    Ni //= g
    packed = np.ascontiguousarray(np.hstack([Nr, Ni]))
    void_dt = np.dtype((np.void, packed.shape[1] * packed.dtype.itemsize))
    keys = packed.view(void_dt).ravel()
    order = np.argsort(keys, kind="mergesort")
    sorted_keys = keys[order]
    diff = np.concatenate(([True], sorted_keys[1:] != sorted_keys[:-1], [True]))
    starts = np.flatnonzero(diff)
    groups = []
    for a, b in zip(starts[:-1], starts[1:]):
        if b - a >= 2:
            groups.append(nz_ids[order[a:b]].tolist())
    return zero_ids, groups


P1 = 2013265921
RI1 = pow(31, (P1 - 1) // 4, P1)


def exact_zi_solve(
    Sr_cols: np.ndarray, Si_cols: np.ndarray, Tr: np.ndarray, Ti: np.ndarray
) -> tuple[int, np.ndarray, np.ndarray] | None:
    """Exact fraction-free Gaussian-integer solver for S * c = T over Q(i).
    Returns (D, nr, ni) with D > 0 and S * (nr + i*ni) == D * (Tr + i*Ti), or None."""
    dim, r = Sr_cols.shape
    S_mod = (Sr_cols + RI1 * Si_cols) % P1
    t_mod = (Tr + RI1 * Ti) % P1
    M = np.column_stack([S_mod, t_mod]).tolist()
    rank = 0
    for c in range(r):
        piv = None
        for row in range(rank, dim):
            if M[row][c]:
                piv = row
                break
        if piv is None:
            return None
        M[rank], M[piv] = M[piv], M[rank]
        inv = pow(M[rank][c], P1 - 2, P1)
        M[rank] = [(x * inv) % P1 for x in M[rank]]
        for row in range(dim):
            if row != rank and M[row][c]:
                f = M[row][c]
                M[row] = [(x - f * y) % P1 for x, y in zip(M[row], M[rank])]
        rank += 1
    for row in range(r, dim):
        if M[row][r]:
            return None

    M_zi = [
        [(int(Sr_cols[row, c]), int(Si_cols[row, c])) for c in range(r)] + [(int(Tr[row]), int(Ti[row]))]
        for row in range(dim)
    ]
    for c in range(r):
        piv = None
        for row in range(c, dim):
            re, im = M_zi[row][c]
            if re != 0 or im != 0:
                piv = row
                break
        if piv is None:
            return None
        if piv != c:
            M_zi[c], M_zi[piv] = M_zi[piv], M_zi[c]
        pre, pim = M_zi[c][c]
        dpiv = pre * pre + pim * pim
        M_zi[c] = [(pre * xre + pim * xim, pre * xim - pim * xre) for (xre, xim) in M_zi[c]]
        for row in range(dim):
            if row != c:
                fre, fim = M_zi[row][c]
                if fre != 0 or fim != 0:
                    new_row = []
                    for (xre, xim), (yre, yim) in zip(M_zi[row], M_zi[c]):
                        nre = dpiv * xre - (fre * yre - fim * yim)
                        nim = dpiv * xim - (fre * yim + fim * yre)
                        new_row.append((nre, nim))
                    g_row = 0
                    for nre, nim in new_row:
                        g_row = math.gcd(g_row, math.gcd(abs(nre), abs(nim)))
                    if g_row > 1:
                        new_row = [(nre // g_row, nim // g_row) for nre, nim in new_row]
                    M_zi[row] = new_row

    for row in range(r, dim):
        if M_zi[row][r] != (0, 0):
            return None

    denoms = [M_zi[c][c][0] for c in range(r)]
    if any(M_zi[c][c][1] != 0 or denoms[c] <= 0 for c in range(r)):
        fail("pivot denominator not positive real")
    L = 1
    for d in denoms:
        L = math.lcm(L, d)
    nr = np.array([M_zi[c][r][0] * (L // denoms[c]) for c in range(r)], dtype=np.int64)
    ni = np.array([M_zi[c][r][1] * (L // denoms[c]) for c in range(r)], dtype=np.int64)
    g_all = math.gcd(L, int(np.gcd.reduce(np.abs(nr))), int(np.gcd.reduce(np.abs(ni))))
    D = L // g_all
    nr //= g_all
    ni //= g_all
    lhs_r = Sr_cols @ nr - Si_cols @ ni
    lhs_i = Sr_cols @ ni + Si_cols @ nr
    if not (np.array_equal(lhs_r, D * Tr) and np.array_equal(lhs_i, D * Ti)):
        fail("exact_zi_solve verification failed")
    return D, nr, ni


def pauli_options_zi(Sr: np.ndarray, Si: np.ndarray, m: int) -> tuple[np.ndarray, np.ndarray]:
    """All 4 * 2^m phased Pauli translates mu * P_k u for each state u in D_m."""
    N = len(Sr)
    dim = 1 << m
    K = 4 * dim
    Opts_r = np.zeros((N, K, dim), dtype=np.int64)
    Opts_i = np.zeros((N, K, dim), dtype=np.int64)
    x = np.arange(dim, dtype=np.int64)
    signs = np.ones((dim, dim), dtype=np.int64)
    for bit in range(m):
        mask = 1 << bit
        signs[(x[:, None] & mask != 0) & (x[None, :] & mask != 0)] *= -1
    for u_idx in range(N):
        ur, ui = Sr[u_idx], Si[u_idx]
        seen = set()
        cls_r, cls_i = [], []
        for a in range(dim):
            perm = x ^ a
            ua_r, ua_i = ur[perm], ui[perm]
            for c in range(dim):
                sg = signs[c]
                vr, vi = sg * ua_r, sg * ua_i
                nz = int(np.argmax((vr != 0) | (vi != 0)))
                cr, ci = int(vr[nz]), int(vi[nz])
                nr = cr * vr + ci * vi
                ni = cr * vi - ci * vr
                key = (nr.tobytes(), ni.tobytes())
                if key not in seen:
                    seen.add(key)
                    cls_r.append(vr)
                    cls_i.append(vi)
        if len(cls_r) != dim:
            fail(f"expected {dim} Pauli classes, got {len(cls_r)}")
        for k in range(dim):
            vr, vi = cls_r[k], cls_i[k]
            Opts_r[u_idx, 4 * k : 4 * k + 4] = [vr, -vi, -vr, vi]
            Opts_i[u_idx, 4 * k : 4 * k + 4] = [vi, vr, -vi, -vr]
    return Opts_r, Opts_i


def main() -> int:
    t0 = time.time()
    check_symbolic_cs_postselection()
    print(f"symbolic (I (x) H)^m postselection and <00| projection identities verified [{time.time() - t0:.2f}s]")

    # 1. Exact rank-2 exclusion and rank-3 enumeration of Psi_2 on D_2 (60 states)
    Sr2, Si2 = dictionary_zi(2)
    Tr2, Ti2 = psi_target_zi(2)
    if np.any( np.all((4 * Sr2 == Sr2[:, 0:1] * Tr2[None, :]) & (4 * Si2 == Si2[:, 0:1] * Ti2[None, :]), axis=1) ):
        fail("Psi_2 is a single stabilizer state")
    r2_decs = 0
    for a, b in itertools.combinations(range(60), 2):
        sol = exact_zi_solve(Sr2[[a, b]].T, Si2[[a, b]].T, Tr2, Ti2)
        if sol is not None:
            _, nr, ni = sol
            if all(nr[j] != 0 or ni[j] != 0 for j in range(2)):
                r2_decs += 1
    if r2_decs != 0:
        fail(f"expected 0 rank-2 decompositions of Psi_2, got {r2_decs}")
    print("CERTIFIED chi(CS^2) >= 3")

    # 2. Handle A: enumerate all 483 exact rank-3 decompositions of Psi_2 and test 1-qubit Pauli lift to Psi_3
    Opts_r2, Opts_i2 = pauli_options_zi(Sr2, Si2, 2)
    S1r2 = Tr2 - Ti2
    S1i2 = Tr2 + Ti2
    r3_psi2 = 0
    lifts_2_to_3 = 0
    for a, b, c in itertools.combinations(range(60), 3):
        sol = exact_zi_solve(Sr2[[a, b, c]].T, Si2[[a, b, c]].T, Tr2, Ti2)
        if sol is not None:
            D, nr, ni = sol
            if all(nr[j] != 0 or ni[j] != 0 for j in range(3)):
                r3_psi2 += 1
                T0r = 2 * (nr[0] * Opts_r2[a] - ni[0] * Opts_i2[a])
                T0i = 2 * (nr[0] * Opts_i2[a] + ni[0] * Opts_r2[a])
                T1r = 2 * (nr[1] * Opts_r2[b] - ni[1] * Opts_i2[b])
                T1i = 2 * (nr[1] * Opts_i2[b] + ni[1] * Opts_r2[b])
                T2r = 2 * (nr[2] * Opts_r2[c] - ni[2] * Opts_i2[c])
                T2i = 2 * (nr[2] * Opts_i2[c] + ni[2] * Opts_r2[c])
                S01r = (T0r[:, None, :] + T1r[None, :, :]).reshape(-1, 4)
                S01i = (T0i[:, None, :] + T1i[None, :, :]).reshape(-1, 4)
                rem_r = D * S1r2[None, :] - S01r
                rem_i = D * S1i2[None, :] - S01i
                for k2 in range(16):
                    m = np.all((rem_r == T2r[k2]) & (rem_i == T2i[k2]), axis=1)
                    lifts_2_to_3 += int(np.sum(m))
    if r3_psi2 != 483 or lifts_2_to_3 != 0:
        fail(f"expected 483 rank-3 decompositions of Psi_2 with 0 lifts, got ({r3_psi2}, {lifts_2_to_3})")
    print(f"Handle A (D_2 slice-and-lift): {r3_psi2} exact rank-3 decompositions of Psi_2, 0 lift to Psi_3 [{time.time() - t0:.2f}s]")

    # 3. Handle B: unconditional exhaustive 1-pivot quotient sweep over all 1,080 states of D_3
    Sr3, Si3 = dictionary_zi(3)
    Tr3, Ti3 = psi_target_zi(3)
    N3 = len(Sr3)
    Q1r = int(Tr3[0]) * Sr3 - Sr3[:, 0:1] * Tr3[None, :]
    Q1i = int(Tr3[0]) * Si3 - Si3[:, 0:1] * Ti3[None, :]
    z3, rg3 = canonical_ray_groups(Q1r[:, 1:], Q1i[:, 1:])
    if len(z3) != 0 or len(rg3) != 0:
        fail(f"expected 0 kernel and 0 rank-2 ray groups for Psi_3, got ({len(z3)}, {len(rg3)})")

    Q1r_sub, Q1i_sub = Q1r[:, 1:], Q1i[:, 1:]
    fc = np.argmax((Q1r_sub * Q1r_sub + Q1i_sub * Q1i_sub) > 0, axis=1)
    r3_psi3 = 0
    for s1 in range(N3 - 2):
        k = int(fc[s1])
        q1r, q1i = int(Q1r_sub[s1, k]), int(Q1i_sub[s1, k])
        sub = np.arange(s1 + 1, N3)
        qsr, qsi = Q1r_sub[sub, k : k + 1], Q1i_sub[sub, k : k + 1]
        Q2r = (q1r * Q1r_sub[sub] - q1i * Q1i_sub[sub]) - (qsr * Q1r_sub[s1 : s1 + 1] - qsi * Q1i_sub[s1 : s1 + 1])
        Q2i = (q1r * Q1i_sub[sub] + q1i * Q1r_sub[sub]) - (qsr * Q1i_sub[s1 : s1 + 1] + qsi * Q1r_sub[s1 : s1 + 1])
        _, rg2 = canonical_ray_groups(Q2r, Q2i)
        for grp in rg2:
            for a, b in itertools.combinations(grp, 2):
                s2, s3 = int(sub[a]), int(sub[b])
                sol = exact_zi_solve(Sr3[[s1, s2, s3]].T, Si3[[s1, s2, s3]].T, Tr3, Ti3)
                if sol is not None:
                    _, nr, ni = sol
                    if all(nr[j] != 0 or ni[j] != 0 for j in range(3)):
                        r3_psi3 += 1
    if r3_psi3 != 0:
        fail(f"expected 0 rank-3 decompositions of Psi_3 on D_3, got {r3_psi3}")

    # Positive control on D_3: verify that the 4 symmetric product stabilizer states
    # {(|0> + i^k |1>)^{ot 3} : k = 0, 1, 2, 3} in D_3 form an exact rank-4 decomposition of Psi_3
    sym4_ids = []
    for k in range(4):
        v1 = np.array([1, 1j ** k], dtype=np.complex128)
        v3 = np.kron(np.kron(v1, v1), v1)
        vr = np.rint(v3.real).astype(np.int64)
        vi = np.rint(v3.imag).astype(np.int64)
        matches = np.flatnonzero(np.all((Sr3 == vr[None, :]) & (Si3 == vi[None, :]), axis=1))
        if len(matches) != 1:
            fail(f"symmetric product state k={k} not uniquely found in D_3")
        sym4_ids.append(int(matches[0]))
    sol4 = exact_zi_solve(Sr3[sym4_ids].T, Si3[sym4_ids].T, Tr3, Ti3)
    if sol4 is None or any(sol4[1][j] == 0 and sol4[2][j] == 0 for j in range(4)):
        fail("positive control failed: 4 symmetric product states did not decompose Psi_3")

    print(
        f"Handle B (unconditional 1,080-pivot sweep on D_3): 0 rank-3 decompositions of Psi_3, "
        f"positive control rank-4 decomposition verified [{time.time() - t0:.2f}s]"
    )
    print("CERTIFIED chi(CS^3) >= 4")
    print("CERTIFIED chi(CS^4) >= 4")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
