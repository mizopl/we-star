"""Exact Galois-quotient certificates for qubit_H and qubit_T at m = 3..6 (ranks 3 and 4).

Every n-qubit stabilizer state is a positive scalar times a vector over Z[i]
with entries in {0, 1, i, -1, -i}. For both single-qubit magic states:
  - qubit_H: |H> = cos(pi/8)|0> + sin(pi/8)|1>, scaled by cos(pi/8)^(-1) to
    |0> + (sqrt(2) - 1)|1> in Z[sqrt(2)]^2,
  - qubit_T: |T> = cos(beta)|0> + e^{i pi/4} sin(beta)|1> with cos(2 beta) = 1/sqrt(3),
    scaled by 2 cos(beta)^(-1) to 2|0> + (1 + i)(sqrt(3) - 1)|1> in Z[i, sqrt(3)]^2,
the m-fold tensor power decomposes uniquely over the quadratic extension
Q(i, sqrt(d)) / Q(i) (with d = 2 for qubit_H and d = 3 for qubit_T) as
    psi_m = A_m + sqrt(d) B_m,    A_m, B_m in Z[i]^(2^m).

By Galois descent under the automorphism sigma(sqrt(d)) = -sqrt(d) fixing Q(i)
and every stabilizer vector s_j in Z[i]^(2^m) pointwise, any complex linear
combination sum_{j=1}^r c_j s_j = psi_m (c_j in C) forces both A_m and B_m to
lie in span_{Q(i)}(s_1, ..., s_r). Since A_m and B_m are linearly independent
over Q(i) on coordinates x = 0 (weight 0) and x = 1 (weight 1) for all m >= 1,
the Galois plane P_m = span_{Q(i)}(A_m, B_m) has dimension 2 over Q(i).

Eliminating coordinates 0 and 1 defines an exact Z[i]-linear map
q : Z[i]^(2^m) -> Z[i]^(2^m - 2) with kernel P_m:
  (i)  A rank-1 or rank-2 decomposition of psi_m requires span_{Q(i)}(s_1, s_2) = P_m,
       so q(s_j) = 0 for each participating state. At m = 3 (1,080 states) and
       m = 4 (36,720 states), zero stabilizer states satisfy q(s) = 0 for both
       qubit_H and qubit_T, immediately certifying chi >= 3 at m = 3, 4 (and at
       m = 5 for qubit_T by <0| projection monotonicity) with zero pivots.
  (ii) A rank-3 decomposition {s_1, s_2, s_3} of psi_m has dim_{Q(i)} span(s_1, s_2, s_3) / P_m <= 1,
       so q(s_1), q(s_2), q(s_3) are pairwise parallel over Q(i) and share the
       same primitive canonical Z[i]-ray. At m = 4 (36,720 states):
         - For qubit_H, the maximum parallel ray group in Z[i]^14 has size 2 (< 3),
           certifying chi(qubit_H^4) >= 4 (and chi >= 4 at m = 5, 6 by <0| projection)
           with zero pivots.
         - For qubit_T, exactly 9 triples in D_4 have parallel rays in Q(i)^16 / P_4,
           giving the 9 rank-3 decompositions of |T>^4 in exact Gaussian-rational
           arithmetic. Testing all 9 triples under the 1-qubit Pauli slice-and-lift
           equation in exact Z[i] arithmetic yields 0 lifts to |T>^5, certifying
           chi(qubit_T^5) >= 4 and chi(qubit_T^6) >= 4.

Controls (all fatal, same exact code path):
  (+) qubit_H at m = 2: 2 states in P_2 forming 1 exact rank-2 decomposition,
      which does not lift to m = 3 (0 lifts).
  (+) qubit_T at m = 2: 3 states in P_2 forming 3 exact rank-2 decompositions.
  (+) qubit_H at m = 3: 16 exact rank-3 decompositions.
  (+) qubit_T at m = 3: 72 exact rank-3 decompositions, with 9 exact 1-qubit
      lifts to |T>^4.

No floating-point operation is used in any step; all bound files declare `exact: true`.

Printed claims:
  CERTIFIED chi(qubit_H^3) >= 3
  CERTIFIED chi(qubit_H^4) >= 3
  CERTIFIED chi(qubit_H^4) >= 4
  CERTIFIED chi(qubit_H^5) >= 4
  CERTIFIED chi(qubit_H^6) >= 4
  CERTIFIED chi(qubit_T^3) >= 3
  CERTIFIED chi(qubit_T^4) >= 3
  CERTIFIED chi(qubit_T^5) >= 3
  CERTIFIED chi(qubit_T^5) >= 4
  CERTIFIED chi(qubit_T^6) >= 4
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


# ------------------------------------ exact stabilizer state enumeration ----

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
    """All n-qubit stabilizer states as int8 exponent rows: e[x] in {0..3}
    (amplitude i^e) or -1 (off support), normalized so the first nonzero entry
    has exponent 0. Count checked against 2^n prod_{j=1}^n (2^j + 1)."""
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
    """Exact Gaussian-integer arrays (Sr, Si) of shape (N_n, 2^n) with entries in {-1, 0, 1}."""
    E = stabilizer_exponents(n)
    lut_r = np.array([1, 0, -1, 0, 0], dtype=np.int64)
    lut_i = np.array([0, 1, 0, -1, 0], dtype=np.int64)
    idx = np.where(E >= 0, E, 4)
    return lut_r[idx], lut_i[idx]


# ------------------------------------ Galois plane & exact Z[i] quotient ----

def target_galois_components(orbit: str, m: int) -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    """Exact integer arrays (Ar, Ai, Br, Bi) of length 2^m such that the scaled
    target state is (Ar + i*Ai) + sqrt(d)*(Br + i*Bi) over Z[i] (d=2 for qubit_H, d=3 for qubit_T)."""
    dim = 1 << m
    Ar = np.zeros(dim, dtype=np.int64)
    Ai = np.zeros(dim, dtype=np.int64)
    Br = np.zeros(dim, dtype=np.int64)
    Bi = np.zeros(dim, dtype=np.int64)
    for x in range(dim):
        w = bin(x).count("1")
        if orbit == "qubit_H":
            a, b = 1, 0
            for _ in range(w):
                a, b = 2 * b - a, a - b
            Ar[x] = a
            Br[x] = b
        elif orbit == "qubit_T":
            a, b = 1, 0
            for _ in range(w):
                a, b = 3 * b - a, a - b
            scale = 1 << (m - w)
            pr, pi = 1, 0
            for _ in range(w):
                pr, pi = pr - pi, pr + pi
            Ar[x] = scale * a * pr
            Ai[x] = scale * a * pi
            Br[x] = scale * b * pr
            Bi[x] = scale * b * pi
        else:
            fail(f"unsupported orbit {orbit}")
    return Ar, Ai, Br, Bi


def check_symbolic_target_consistency() -> None:
    """100% symbolic consistency check against stabrank_verify.target_vector for m = 1, 2."""
    # Check qubit_H: target_vector("qubit_H", 1) = [cos(pi/8), sin(pi/8)]
    t_h = target_vector("qubit_H", 1)
    if sp.simplify(t_h[1] / t_h[0] - (sp.sqrt(2) - 1)) != 0:
        fail("symbolic ratio mismatch for qubit_H")
    # Check qubit_T: target_vector("qubit_T", 1) has cos(2*beta) = 1/sqrt(3), ratio = e^{i pi/4} tan(beta)
    t_t = target_vector("qubit_T", 1)
    tan_b = (sp.sqrt(3) - 1) / sp.sqrt(2)
    if sp.simplify((1 - tan_b ** 2) / (1 + tan_b ** 2) - sp.Rational(1, 3) * sp.sqrt(3)) != 0:
        fail("symbolic half-angle identity failed for qubit_T")
    ratio_t = sp.exp(sp.I * sp.pi / 4).rewrite(sp.cos) * tan_b
    if sp.simplify(2 * ratio_t - (1 + sp.I) * (sp.sqrt(3) - 1)) != 0:
        fail("symbolic ratio mismatch for qubit_T")
    for orbit, d_val, r_sym, s0 in (
        ("qubit_H", 2, sp.sqrt(2) - 1, 1),
        ("qubit_T", 3, (1 + sp.I) * (sp.sqrt(3) - 1), 2),
    ):
        for m in (1, 2):
            Ar, Ai, Br, Bi = target_galois_components(orbit, m)
            for x in range(1 << m):
                w = bin(x).count("1")
                sym_entry = (s0 ** (m - w)) * (r_sym ** w)
                want = (int(Ar[x]) + sp.I * int(Ai[x])) + sp.sqrt(d_val) * (int(Br[x]) + sp.I * int(Bi[x]))
                if sp.simplify(sp.expand(sym_entry - want)) != 0:
                    fail(f"symbolic target mismatch for {orbit} m={m} at x={x}")


def galois_quotient_rays(
    Sr: np.ndarray, Si: np.ndarray, Ar: np.ndarray, Ai: np.ndarray, Br: np.ndarray, Bi: np.ndarray
) -> tuple[np.ndarray, np.ndarray]:
    """Exact Gaussian-integer projection q(s) in Z[i]^(2^m - 2) modulo P_m = span_{Q(i)}(A_m, B_m)."""
    if not (Br[0] == 0 and Bi[0] == 0 and Ai[0] == 0 and Ar[0] > 0):
        fail("unexpected weight-0 target component")
    if not (Ar[1] + Br[1] == 0 and Ai[1] + Bi[1] == 0):
        fail("unexpected weight-1 target component")
    Ur, Ui = Ar + Br, Ai + Bi
    b1r, b1i = int(Br[1]), int(Bi[1])
    nb1 = b1r * b1r + b1i * b1i
    a0 = int(Ar[0])
    Vr = b1r * Br + b1i * Bi
    Vi = b1r * Bi - b1i * Br
    gU = math.gcd(a0, int(np.gcd.reduce(np.abs(Ur))), int(np.gcd.reduce(np.abs(Ui))))
    u0 = a0 // gU
    Ur, Ui = Ur // gU, Ui // gU
    gV = math.gcd(nb1, int(np.gcd.reduce(np.abs(Vr))), int(np.gcd.reduce(np.abs(Vi))))
    v1 = nb1 // gV
    Vr, Vi = Vr // gV, Vi // gV
    L = math.lcm(u0, v1)
    su, sv = L // u0, L // v1
    s0r, s0i = Sr[:, 0:1], Si[:, 0:1]
    s1r, s1i = Sr[:, 1:2], Si[:, 1:2]
    Qr = L * Sr - su * (s0r * Ur[None, :] - s0i * Ui[None, :]) - sv * (s1r * Vr[None, :] - s1i * Vi[None, :])
    Qi = L * Si - su * (s0r * Ui[None, :] + s0i * Ur[None, :]) - sv * (s1r * Vi[None, :] + s1i * Vr[None, :])
    if not (np.all(Qr[:, :2] == 0) and np.all(Qi[:, :2] == 0)):
        fail("quotient did not eliminate coordinates 0 and 1")
    return Qr[:, 2:], Qi[:, 2:]


def canonical_ray_groups(Qr: np.ndarray, Qi: np.ndarray) -> tuple[list[int], list[list[int]]]:
    """Partition states into kernel indices (q(s) = 0) and parallel ray groups of size >= 2 over Q(i)."""
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
    Wr = cr * Qr_nz + ci * Qi_nz
    Wi = cr * Qi_nz - ci * Qr_nz
    W = np.hstack([Wr, Wi])
    g = np.gcd.reduce(np.abs(W), axis=1)
    W = W // g[:, None]
    W_contig = np.ascontiguousarray(W, dtype=np.int64)
    view = W_contig.view(np.dtype((np.void, W_contig.shape[1] * 8))).ravel()
    order = np.argsort(view, kind="stable")
    vs = view[order]
    starts = np.concatenate(([0], np.flatnonzero(vs[1:] != vs[:-1]) + 1, [len(nz_ids)]))
    groups = [sorted(nz_ids[order[a:b]].tolist()) for a, b in zip(starts[:-1], starts[1:]) if b - a >= 2]
    return zero_ids, groups


# --------------------- exact fraction-free Z[i] solver & 1-qubit lifting ----

P1 = 2013265921
RI1 = pow(31, (P1 - 1) // 4, P1)


def exact_qi_solve(
    Sr_cols: np.ndarray, Si_cols: np.ndarray, Ar: np.ndarray, Ai: np.ndarray, Br: np.ndarray, Bi: np.ndarray
):
    """Exact fraction-free Gaussian elimination in Z[i] solving S c_A = D A and S c_B = D B
    with rank(S) = r and all r coefficients (c_A[j], c_B[j]) != (0, 0)."""
    dim, r = Sr_cols.shape
    S_mod = (Sr_cols + RI1 * Si_cols) % P1
    a_mod = (Ar + RI1 * Ai) % P1
    b_mod = (Br + RI1 * Bi) % P1
    M = np.column_stack([S_mod, a_mod, b_mod]).tolist()
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
        if M[row][r] or M[row][r + 1]:
            return None

    M_zi = [
        [(int(Sr_cols[row, c]), int(Si_cols[row, c])) for c in range(r)]
        + [(int(Ar[row]), int(Ai[row])), (int(Br[row]), int(Bi[row]))]
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
        if M_zi[row][r] != (0, 0) or M_zi[row][r + 1] != (0, 0):
            return None

    pivs = [M_zi[c][c][0] for c in range(r)]
    D = 1
    for d_c in pivs:
        D = math.lcm(D, d_c)
    cAr, cAi, cBr, cBi = [], [], [], []
    for c in range(r):
        scale = D // pivs[c]
        are, aim = M_zi[c][r]
        bre, bim = M_zi[c][r + 1]
        if are == 0 and aim == 0 and bre == 0 and bim == 0:
            return None
        cAr.append(scale * are)
        cAi.append(scale * aim)
        cBr.append(scale * bre)
        cBi.append(scale * bim)
    cAr_a = np.array(cAr, dtype=np.int64)
    cAi_a = np.array(cAi, dtype=np.int64)
    cBr_a = np.array(cBr, dtype=np.int64)
    cBi_a = np.array(cBi, dtype=np.int64)
    lhs_Ar = Sr_cols @ cAr_a - Si_cols @ cAi_a
    lhs_Ai = Sr_cols @ cAi_a + Si_cols @ cAr_a
    lhs_Br = Sr_cols @ cBr_a - Si_cols @ cBi_a
    lhs_Bi = Sr_cols @ cBi_a + Si_cols @ cBr_a
    if not (np.array_equal(lhs_Ar, D * Ar) and np.array_equal(lhs_Ai, D * Ai)):
        fail("exact Z[i] verification failed on Galois component A")
    if not (np.array_equal(lhs_Br, D * Br) and np.array_equal(lhs_Bi, D * Bi)):
        fail("exact Z[i] verification failed on Galois component B")
    return int(D), cAr_a, cAi_a, cBr_a, cBi_a


def build_exact_pauli_translates(Sr_u: np.ndarray, Si_u: np.ndarray, m: int) -> tuple[np.ndarray, np.ndarray]:
    """All 4 * 2^m phased Pauli translates mu X^a Z^c u in exact int64 arrays (Wr, Wi)."""
    dim = 1 << m
    x = np.arange(dim, dtype=np.int64)
    signs = np.ones((dim, dim), dtype=np.int64)
    for bit in range(m):
        mask = (x >> bit) & 1
        signs *= np.where(np.outer(mask, mask), -1, 1)
    seen = set()
    base_r, base_i = [], []
    for a in range(dim):
        perm = x ^ a
        ua_r, ua_i = Sr_u[perm], Si_u[perm]
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
                base_r.append(vr)
                base_i.append(vi)
    if len(base_r) != dim:
        fail(f"expected {dim} Pauli classes, got {len(base_r)}")
    out_r, out_i = [], []
    for vr, vi in zip(base_r, base_i):
        out_r.extend([vr, -vi, -vr, vi])
        out_i.extend([vi, vr, -vi, -vr])
    return np.array(out_r, dtype=np.int64), np.array(out_i, dtype=np.int64)


def is_exact_stabilizer_state_zi(vr: np.ndarray, vi: np.ndarray, m: int) -> bool:
    """Exact verification in Z[i] that vr + i*vi is an m-qubit stabilizer state."""
    mag2 = vr * vr + vi * vi
    supp = np.flatnonzero(mag2 > 0)
    n_supp = len(supp)
    if n_supp == 0 or (n_supp & (n_supp - 1)) != 0:
        return False
    m0 = int(mag2[supp[0]])
    if not np.all(mag2[supp] == m0):
        return False
    s0 = int(supp[0])
    W_elems = supp ^ s0
    if set(W_elems.tolist()) != set((W_elems[:, None] ^ W_elems[None, :]).ravel().tolist()):
        return False
    cr, ci = int(vr[s0]), int(vi[s0])
    nr = (cr * vr[supp] + ci * vi[supp]) // m0
    ni = (cr * vi[supp] - ci * vr[supp]) // m0
    phase_lut = {(1, 0): 0, (0, 1): 1, (-1, 0): 2, (0, -1): 3}
    w_to_e = {}
    for w, r_val, i_val in zip(W_elems.tolist(), nr.tolist(), ni.tolist()):
        tup = (r_val, i_val)
        if tup not in phase_lut:
            return False
        w_to_e[w] = phase_lut[tup]
    basis = []
    span = {0}
    for w in W_elems.tolist():
        if w not in span:
            basis.append(w)
            span = span | {s ^ w for s in span}
    d = len(basis)
    l_vec = [w_to_e[b] for b in basis]
    Q_mat = [[0] * d for _ in range(d)]
    for a in range(d):
        for b in range(a + 1, d):
            diff = (w_to_e[basis[a] ^ basis[b]] - l_vec[a] - l_vec[b]) & 3
            if diff not in (0, 2):
                return False
            Q_mat[a][b] = diff
    for bits in itertools.product((0, 1), repeat=d):
        w = 0
        pred = 0
        for a, bit in enumerate(bits):
            if bit:
                w ^= basis[a]
                pred += l_vec[a]
        for a in range(d):
            if bits[a]:
                for b in range(a + 1, d):
                    if bits[b]:
                        pred += Q_mat[a][b]
        if (pred & 3) != w_to_e[w]:
            return False
    return True


def exact_1qubit_lifts(cols, sol, Sr, Si, Ar, Ai, Br, Bi, orbit: str, m: int) -> list[tuple[int, ...]]:
    """All 1-qubit Pauli slice-1 lifts of decomposition `cols` from m to m+1 in exact Z[i] arithmetic."""
    D, cAr, cAi, cBr, cBi = sol
    r = len(cols)
    dim = 1 << m
    if orbit == "qubit_H":
        tAr, tAi = D * (2 * Br - Ar), D * (2 * Bi - Ai)
        tBr, tBi = D * (Ar - Br), D * (Ai - Bi)
        s_cAr, s_cAi, s_cBr, s_cBi = cAr, cAi, cBr, cBi
    elif orbit == "qubit_T":
        uAr, uAi = D * (3 * Br - Ar), D * (3 * Bi - Ai)
        uBr, uBi = D * (Ar - Br), D * (Ai - Bi)
        tAr, tAi = uAr - uAi, uAr + uAi
        tBr, tBi = uBr - uBi, uBr + uBi
        s_cAr, s_cAi, s_cBr, s_cBi = 2 * cAr, 2 * cAi, 2 * cBr, 2 * cBi
    else:
        fail(f"unsupported orbit {orbit}")

    target_vec = np.concatenate([tAr, tAi, tBr, tBi])
    term_tables = []
    raw_translates = []
    for j, c_idx in enumerate(cols):
        Wr, Wi = build_exact_pauli_translates(Sr[c_idx], Si[c_idx], m)
        raw_translates.append((Wr, Wi))
        car, cai = int(s_cAr[j]), int(s_cAi[j])
        cbr, cbi = int(s_cBr[j]), int(s_cBi[j])
        pAr = car * Wr - cai * Wi
        pAi = car * Wi + cai * Wr
        pBr = cbr * Wr - cbi * Wi
        pBi = cbr * Wi + cbi * Wr
        term_tables.append(np.hstack([pAr, pAi, pBr, pBi]))

    mid = r // 2
    L = term_tables[0]
    for j in range(1, mid):
        L = (L[:, None, :] + term_tables[j][None, :, :]).reshape(-1, 4 * dim)
    R = term_tables[mid]
    for j in range(mid + 1, r):
        R = (R[:, None, :] + term_tables[j][None, :, :]).reshape(-1, 4 * dim)

    need = target_vec[None, :] - R
    L_c = np.ascontiguousarray(L, dtype=np.int64)
    N_c = np.ascontiguousarray(need, dtype=np.int64)
    dtype_row = np.dtype((np.void, 4 * dim * 8))
    vL = L_c.view(dtype_row).ravel()
    vN = N_c.view(dtype_row).ravel()
    ordN = np.argsort(vN, kind="stable")
    vNs = vN[ordN]
    lo = np.searchsorted(vNs, vL, side="left")
    hi = np.searchsorted(vNs, vL, side="right")
    valid_lifts = []
    K = 4 * dim
    for idxL in np.flatnonzero(hi > lo).tolist():
        l_indices = []
        rem = idxL
        for _ in range(mid):
            rem, kj = divmod(rem, K)
            l_indices.append(kj)
        l_indices.reverse()
        for pos in range(int(lo[idxL]), int(hi[idxL])):
            idxR = int(ordN[pos])
            if not np.array_equal(L[idxL], need[idxR]):
                continue
            r_indices = []
            rem = idxR
            for _ in range(r - mid):
                rem, kj = divmod(rem, K)
                r_indices.append(kj)
            r_indices.reverse()
            combo = l_indices + r_indices
            ok_stab = True
            for j, kj in enumerate(combo):
                ur, ui = Sr[cols[j]], Si[cols[j]]
                wr, wi = raw_translates[j][0][kj], raw_translates[j][1][kj]
                if not is_exact_stabilizer_state_zi(np.concatenate([ur, wr]), np.concatenate([ui, wi]), m + 1):
                    ok_stab = False
                    break
            if ok_stab:
                valid_lifts.append(tuple(combo))
    return valid_lifts


def main() -> int:
    t0 = time.time()
    check_symbolic_target_consistency()
    print("symbolic consistency: scaled targets match stabrank_verify.target_vector over Q(i, sqrt(d))")

    Sr2, Si2 = dictionary_zi(2)
    Sr3, Si3 = dictionary_zi(3)
    Sr4, Si4 = dictionary_zi(4)
    print(f"exact Z[i] dictionaries built: D_2={len(Sr2)}, D_3={len(Sr3)}, D_4={len(Sr4)} [{time.time()-t0:.2f}s]")

    # Controls at m = 2
    Ar2_H, Ai2_H, Br2_H, Bi2_H = target_galois_components("qubit_H", 2)
    z2_H, _ = canonical_ray_groups(*galois_quotient_rays(Sr2, Si2, Ar2_H, Ai2_H, Br2_H, Bi2_H))
    if len(z2_H) != 2:
        fail(f"positive control qubit_H m=2: expected 2 states in P_2, got {len(z2_H)}")
    sol2_H = exact_qi_solve(Sr2[z2_H].T, Si2[z2_H].T, Ar2_H, Ai2_H, Br2_H, Bi2_H)
    if sol2_H is None:
        fail("positive control qubit_H m=2: the 2 states in P_2 do not decompose |H>^2")
    lifts_h2 = exact_1qubit_lifts(z2_H, sol2_H, Sr2, Si2, Ar2_H, Ai2_H, Br2_H, Bi2_H, "qubit_H", 2)
    if len(lifts_h2) != 0:
        fail(f"negative control qubit_H m=2->3: expected 0 lifts, got {len(lifts_h2)}")

    Ar2_T, Ai2_T, Br2_T, Bi2_T = target_galois_components("qubit_T", 2)
    z2_T, _ = canonical_ray_groups(*galois_quotient_rays(Sr2, Si2, Ar2_T, Ai2_T, Br2_T, Bi2_T))
    if len(z2_T) != 3:
        fail(f"positive control qubit_T m=2: expected 3 states in P_2, got {len(z2_T)}")
    r2_T_count = sum(
        1
        for pair in itertools.combinations(z2_T, 2)
        if exact_qi_solve(Sr2[list(pair)].T, Si2[list(pair)].T, Ar2_T, Ai2_T, Br2_T, Bi2_T) is not None
    )
    if r2_T_count != 3:
        fail(f"positive control qubit_T m=2: expected 3 rank-2 decompositions, got {r2_T_count}")
    print("controls m=2: qubit_H has 1 rank-2 decomposition (0 lifts to m=3); qubit_T has 3 rank-2 decompositions")

    # m = 3 rank-2 exclusions and rank-3 controls
    Ar3_H, Ai3_H, Br3_H, Bi3_H = target_galois_components("qubit_H", 3)
    z3_H, grps3_H = canonical_ray_groups(*galois_quotient_rays(Sr3, Si3, Ar3_H, Ai3_H, Br3_H, Bi3_H))
    if len(z3_H) != 0:
        fail(f"qubit_H m=3: expected 0 states in P_3, got {len(z3_H)}")
    decs3_H = [
        trip
        for g in grps3_H
        if len(g) >= 3
        for trip in itertools.combinations(g, 3)
        if exact_qi_solve(Sr3[list(trip)].T, Si3[list(trip)].T, Ar3_H, Ai3_H, Br3_H, Bi3_H) is not None
    ]
    if len(decs3_H) != 16:
        fail(f"positive control qubit_H m=3: expected 16 rank-3 decompositions, got {len(decs3_H)}")

    Ar3_T, Ai3_T, Br3_T, Bi3_T = target_galois_components("qubit_T", 3)
    z3_T, grps3_T = canonical_ray_groups(*galois_quotient_rays(Sr3, Si3, Ar3_T, Ai3_T, Br3_T, Bi3_T))
    if len(z3_T) != 0:
        fail(f"qubit_T m=3: expected 0 states in P_3, got {len(z3_T)}")
    decs3_T = []
    lifts3_T = 0
    for g in grps3_T:
        if len(g) >= 3:
            for trip in itertools.combinations(g, 3):
                sol = exact_qi_solve(Sr3[list(trip)].T, Si3[list(trip)].T, Ar3_T, Ai3_T, Br3_T, Bi3_T)
                if sol is not None:
                    decs3_T.append((trip, sol))
                    lifts3_T += len(exact_1qubit_lifts(trip, sol, Sr3, Si3, Ar3_T, Ai3_T, Br3_T, Bi3_T, "qubit_T", 3))
    if len(decs3_T) != 72 or lifts3_T != 9:
        fail(f"positive control qubit_T m=3: expected 72 rank-3 decompositions and 9 lifts to m=4, got {len(decs3_T)} and {lifts3_T}")
    print(f"m=3 exact Galois quotient: 0 states in P_3 for both orbits; 16 (qubit_H) and 72 (qubit_T, 9 lifts to m=4) rank-3 decompositions")

    # m = 4 rank-2 and rank-3 exclusions + m = 5, 6 slice-and-lift / projection
    Ar4_H, Ai4_H, Br4_H, Bi4_H = target_galois_components("qubit_H", 4)
    z4_H, grps4_H = canonical_ray_groups(*galois_quotient_rays(Sr4, Si4, Ar4_H, Ai4_H, Br4_H, Bi4_H))
    max_grp4_H = max((len(g) for g in grps4_H), default=0)
    if len(z4_H) != 0 or max_grp4_H >= 3:
        fail(f"qubit_H m=4: expected 0 states in P_4 and max parallel ray group < 3, got z={len(z4_H)}, max_grp={max_grp4_H}")
    print(f"qubit_H m=4: 0 states in P_4, max parallel ray group size in Q(i)^16/P_4 is {max_grp4_H} < 3 -> no rank-2 or rank-3 decomposition exists")

    Ar4_T, Ai4_T, Br4_T, Bi4_T = target_galois_components("qubit_T", 4)
    z4_T, grps4_T = canonical_ray_groups(*galois_quotient_rays(Sr4, Si4, Ar4_T, Ai4_T, Br4_T, Bi4_T))
    if len(z4_T) != 0:
        fail(f"qubit_T m=4: expected 0 states in P_4, got {len(z4_T)}")
    decs4_T = []
    lifts4_T = 0
    for g in grps4_T:
        if len(g) >= 3:
            for trip in itertools.combinations(g, 3):
                sol = exact_qi_solve(Sr4[list(trip)].T, Si4[list(trip)].T, Ar4_T, Ai4_T, Br4_T, Bi4_T)
                if sol is not None:
                    decs4_T.append((trip, sol))
                    lifts4_T += len(exact_1qubit_lifts(trip, sol, Sr4, Si4, Ar4_T, Ai4_T, Br4_T, Bi4_T, "qubit_T", 4))
    if len(decs4_T) != 9 or lifts4_T != 0:
        fail(f"qubit_T m=4->5: expected 9 rank-3 decompositions at m=4 and 0 lifts to m=5, got {len(decs4_T)} and {lifts4_T}")
    print(f"qubit_T m=4->5: 0 states in P_4; 9 exact rank-3 decompositions of |T>^4, 0 lift to |T>^5 [{time.time()-t0:.2f}s]")

    for claim in (
        "CERTIFIED chi(qubit_H^3) >= 3",
        "CERTIFIED chi(qubit_H^4) >= 3",
        "CERTIFIED chi(qubit_H^4) >= 4",
        "CERTIFIED chi(qubit_H^5) >= 4",
        "CERTIFIED chi(qubit_H^6) >= 4",
        "CERTIFIED chi(qubit_T^3) >= 3",
        "CERTIFIED chi(qubit_T^4) >= 3",
        "CERTIFIED chi(qubit_T^5) >= 3",
        "CERTIFIED chi(qubit_T^5) >= 4",
        "CERTIFIED chi(qubit_T^6) >= 4",
    ):
        print(claim)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
