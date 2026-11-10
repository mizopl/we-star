"""Exact 1-pivot Galois-quotient & orthogonal Pauli-basis certificates:
chi(|H>^{ot 5}) >= 5, chi(|H>^{ot 6}) >= 5, chi(|T>^{ot 5}) >= 5, chi(|T>^{ot 6}) >= 5.

This self-contained certificate upgrades the rank-4 exclusions for |H>^5, |H>^6,
|T>^5, and |T>^6 to the `verified` tier (`exact: true`) with zero floating-point
arithmetic and zero external batch files:

1. Exact Galois Split over Q(i):
   Scaled by a0^(-m), the target psi_m = (a0 |0> + a1 |1>)^m decomposes over
   Q(i, sqrt(d)) / Q(i) (d = 2 for qubit_H, d = 3 for qubit_T) as
       psi_m = A_m + sqrt(d) B_m,    A_m, B_m in Z[i]^(2^m).
   Since every qubit stabilizer state has entries in {0, 1, i, -1, -i} subset Z[i],
   any decomposition sum_{j=1}^r c_j s_j = psi_m over C reduces by Galois descent
   to a pair of exact systems over Q(i): sum c_{j,A} s_j = A_m and sum c_{j,B} s_j = B_m.
   In particular, P_m = span_{Q(i)}(A_m, B_m) has dimension 2 over Q(i), so the
   quotient Q(i)^(2^m) / P_m has codimension 2.

2. Fact 1 & Two-Qubit Flat Reduction (m = 5 = 3 + 2):
   - By the 0-pivot Galois quotient on D_3 (1,080 states) and D_4 (36,720 states),
     chi(qubit_H^3) = 3, chi(qubit_T^3) = 3, chi(qubit_H^4) = 4, and |T>^4 has
     exactly 9 rank-3 decompositions (1 orbit under G_4).
   - Fact 1 (every term in a rank-4 decomposition of psi_5 is full along every
     qubit): immediate for qubit_H since chi(H^4) = 4; for qubit_T, a 1-qubit
     slice with 3 visible terms must use the unique G_4-orbit of rank-3
     decompositions of |T>^4, and checking all 65^3 = 274,625 slice combinations
     at ratios tau^{+-1} in exact Z[i] arithmetic gives (exact, stabilizer) = (0, 0).
   - Flat reduction along qubits 1, 2: by Fact 1 and chi(psi_3) = 3, each term's
     support flat in F_2^2 is either F_2^2, A = {00, 11}, or B = {01, 10}, with
     n_A <= 1 and n_B <= 1. If n_B = 1 (one B-line term, vanishing at both 00
     and 11), the 3 remaining terms visible at 00 form a rank-3 decomposition of
     psi_3 whose phased Pauli translates at 11 must sum to ratio^2 * psi_3 (j = 2).
     Checking all 33^3 = 35,937 slice combinations across all G_3-orbit
     representatives of rank-3 decompositions of psi_3 in exact Z[i] arithmetic
     yields 0 exact hits at j = +-2 for both qubit_T and qubit_H. Hence n_B = 0
     and all 4 terms are visible at base point x_0 = 00.

3. 1-Pivot Galois Census of Full 4-Covers of psi_3 in D_3:
   - Kind A (4 distinct linearly independent states): 1 pivot in Q(i)^8 / P_3
     over the G_3-orbit roots (20 for qubit_T, 32 for qubit_H) enumerates all
     full 4-covers up to G_3 in ~1s (2,372 G_3-orbits for qubit_T, 2,406 for qubit_H).
   - Kind B (4 distinct linearly dependent states): any such cover spans a 3D
     subspace containing the 2D plane P_3, so all 4 states must lie in a single
     1D ray group of Q(i)^8 / P_3. Since the maximum ray group size in Q(i)^8 / P_3
     is 3 (< 4), Kind B = 0 is immediate.
   - Kind C ((2, 1, 1) repeated-state multisets over rank-3 decompositions):
     8 G_3-orbits for qubit_T and 6 G_3-orbits for qubit_H.

4. Orthogonal Destabilizer Basis Theorem (Kind C) & Exact Meet-in-the-Middle (Kind A):
   - For every u in D_3, its 8 Pauli class representatives {P_k u}_{k=0}^7 form
     an exact orthogonal Z[i]-basis of C^8: <P_a u, P_b u> = ||u||^2 delta_{a,b}.
     For every Kind-C multiset (u_blk, u_blk, u_1, u_2), projecting the 33^2 = 1,089
     slice-11 (j = 2) residuals R = ratio^2 D psi_3 - sc*(d_1 w_1 + d_2 w_2) onto
     {P_k u_blk}_{k=0}^7 shows that every residual has >= 4 non-zero orthogonal
     Pauli coordinates, whereas 2 copies of u_blk can span at most 2 Pauli classes.
     Thus all Kind-C multisets are excluded in exact integer arithmetic.
   - For all Kind-A orbits, exact integer meet-in-the-middle over the 33^2 = 1,089
     left/right pairs at j = 1 (slices 01, 10) and j = 2 (slice 11) leaves 196
     (qubit_T) and 30 (qubit_H) j = 1 survivors and 0 valid 5-qubit stabilizer
     completions. Positive planted controls pass on the same matcher.

Printed claims:
  CERTIFIED chi(qubit_H^5) >= 5
  CERTIFIED chi(qubit_H^6) >= 5
  CERTIFIED chi(qubit_T^5) >= 5
  CERTIFIED chi(qubit_T^6) >= 5
"""

from __future__ import annotations

import itertools
import math
import os
import sys
import time

os.environ.setdefault("OMP_NUM_THREADS", "1")

import numpy as np  # noqa: E402

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from cert_qubit_galois_m3_m4 import (  # noqa: E402
    canonical_ray_groups,
    check_symbolic_target_consistency,
    dictionary_zi,
    exact_qi_solve,
    fail,
    galois_quotient_rays,
    is_exact_stabilizer_state_zi,
    stabilizer_exponents,
    target_galois_components,
)


def keys_of(E: np.ndarray) -> np.ndarray:
    v = np.ascontiguousarray(E).view(np.dtype((np.void, E.shape[1])))
    return v.ravel()


def renormalize(E: np.ndarray) -> np.ndarray:
    first = np.argmax(E >= 0, axis=1)
    base = E[np.arange(E.shape[0]), first].astype(np.int16)
    return np.where(E >= 0, (E.astype(np.int16) - base[:, None]) % 4, -1).astype(np.int8)


def build_g3_group(E3: np.ndarray, Sr3: np.ndarray, Si3: np.ndarray, orbit: str) -> np.ndarray:
    """Exact unitary symmetry group G_3 acting on D_3 (order 162 for qubit_T, 48 for qubit_H)."""
    N3 = len(E3)
    k3 = keys_of(E3)
    ord_k3 = np.argsort(k3, kind="stable")
    ks3 = k3[ord_k3]

    def lookup(E_mat: np.ndarray) -> np.ndarray:
        km = keys_of(E_mat)
        pos = np.searchsorted(ks3, km)
        if not np.all(ks3[pos] == km):
            fail("symmetry image not found in D_3")
        return ord_k3[pos].astype(np.int32)

    xs = np.array(list(itertools.product((0, 1), repeat=3)), dtype=np.int64)
    w3 = np.array([4, 2, 1], dtype=np.int64)
    perm_swap01 = lookup(renormalize(E3[:, xs[:, [1, 0, 2]] @ w3]))
    perm_cyc = lookup(renormalize(E3[:, xs[:, [1, 2, 0]] @ w3]))

    Gr, Gi = Sr3.copy(), Si3.copy()
    if orbit == "qubit_H":
        Gr[:, :4] = Sr3[:, :4] + Sr3[:, 4:]
        Gr[:, 4:] = Sr3[:, :4] - Sr3[:, 4:]
        Gi[:, :4] = Si3[:, :4] + Si3[:, 4:]
        Gi[:, 4:] = Si3[:, :4] - Si3[:, 4:]
    elif orbit == "qubit_T":
        Gr[:, :4] = Sr3[:, :4] + Sr3[:, 4:]
        Gi[:, :4] = Si3[:, :4] + Si3[:, 4:]
        dr = Sr3[:, :4] - Sr3[:, 4:]
        di = Si3[:, :4] - Si3[:, 4:]
        Gr[:, 4:] = -di
        Gi[:, 4:] = dr
    else:
        fail(f"unsupported orbit {orbit}")

    mag2 = Gr * Gr + Gi * Gi
    first_nz = np.argmax(mag2 > 0, axis=1)
    r_idx = np.arange(N3)
    cr, ci = Gr[r_idx, first_nz][:, None], Gi[r_idx, first_nz][:, None]
    denom = cr * cr + ci * ci
    Nr = (cr * Gr + ci * Gi) // denom
    Ni = (cr * Gi - ci * Gr) // denom
    E_g0 = np.full_like(E3, -1)
    E_g0[(Nr == 1) & (Ni == 0)] = 0
    E_g0[(Nr == 0) & (Ni == 1)] = 1
    E_g0[(Nr == -1) & (Ni == 0)] = 2
    E_g0[(Nr == 0) & (Ni == -1)] = 3
    perm_g0 = lookup(E_g0)

    gens = [perm_g0, perm_swap01, perm_cyc]
    G3 = [np.arange(N3, dtype=np.int32)]
    seen = {G3[0].tobytes()}
    q = list(G3)
    while q:
        cur = q.pop(0)
        for g in gens:
            nxt = cur[g]
            b = nxt.tobytes()
            if b not in seen:
                seen.add(b)
                G3.append(nxt)
                q.append(nxt)
    return np.asarray(G3, dtype=np.int32)


def precompute_pauli_classes(Sr: np.ndarray, Si: np.ndarray, m: int):
    """For every state u in D_m, compute its 2^m orthogonal Pauli class representatives
    and verify <P_a u, P_b u> = ||u||^2 delta_{a,b} in exact Z[i] arithmetic.
    Also return all 4*2^m + 1 slice options (phased translates + 0 absent at index 4*2^m)."""
    N = len(Sr)
    dim = 1 << m
    K = 4 * dim
    Br = np.zeros((N, dim, dim), dtype=np.int64)
    Bi = np.zeros((N, dim, dim), dtype=np.int64)
    Opts_r = np.zeros((N, K + 1, dim), dtype=np.int64)
    Opts_i = np.zeros((N, K + 1, dim), dtype=np.int64)
    norms = np.zeros(N, dtype=np.int64)

    x = np.arange(dim, dtype=np.int64)
    signs = np.ones((dim, dim), dtype=np.int64)
    for bit in range(m):
        mask = (x >> bit) & 1
        signs *= np.where(np.outer(mask, mask), -1, 1)

    for u_idx in range(N):
        ur, ui = Sr[u_idx], Si[u_idx]
        m0 = int(np.sum(ur * ur + ui * ui))
        norms[u_idx] = m0
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
        mr = np.array(cls_r, dtype=np.int64)
        mi = np.array(cls_i, dtype=np.int64)
        gram_r = mr @ mr.T + mi @ mi.T
        gram_i = mr @ mi.T - mi @ mr.T
        if not (np.array_equal(gram_r, m0 * np.eye(dim, dtype=np.int64)) and np.all(gram_i == 0)):
            fail(f"orthogonality check failed for state {u_idx}")
        Br[u_idx] = mr
        Bi[u_idx] = mi
        for k in range(dim):
            vr, vi = mr[k], mi[k]
            Opts_r[u_idx, 4 * k : 4 * k + 4] = [vr, -vi, -vr, vi]
            Opts_i[u_idx, 4 * k : 4 * k + 4] = [vi, vr, -vi, -vr]
    return Br, Bi, Opts_r, Opts_i, norms


def ratio_scaled_target(
    Ar: np.ndarray, Ai: np.ndarray, Br: np.ndarray, Bi: np.ndarray, D: int, orbit: str, j: int
):
    """Exact integer (scale_c, tAr, tAi, tBr, tBi) for scale_c * ratio^j * D * (A + sqrt(d)*B)."""
    if orbit == "qubit_T":
        if j == 0:
            return 1, D * Ar, D * Ai, D * Br, D * Bi
        elif j == 1:
            uAr, uAi = D * (3 * Br - Ar), D * (3 * Bi - Ai)
            uBr, uBi = D * (Ar - Br), D * (Ai - Bi)
            return 2, uAr - uAi, uAr + uAi, uBr - uBi, uBr + uBi
        elif j == -1:
            uAr, uAi = D * (3 * Br + Ar), D * (3 * Bi + Ai)
            uBr, uBi = D * (Ar + Br), D * (Ai + Bi)
            return 2, uAr + uAi, uAi - uAr, uBr + uBi, uBi - uBr
        elif j == 2:
            uAr, uAi = D * (2 * Ar - 3 * Br), D * (2 * Ai - 3 * Bi)
            uBr, uBi = D * (2 * Br - Ar), D * (2 * Bi - Ai)
            return 1, -uAi, uAr, -uBi, uBr
        elif j == -2:
            uAr, uAi = D * (2 * Ar + 3 * Br), D * (2 * Ai + 3 * Bi)
            uBr, uBi = D * (2 * Br + Ar), D * (2 * Bi + Ai)
            return 1, uAi, -uAr, uBi, -uBr
    elif orbit == "qubit_H":
        if j == 0:
            return 1, D * Ar, D * Ai, D * Br, D * Bi
        elif j == 1:
            return 1, D * (2 * Br - Ar), D * (2 * Bi - Ai), D * (Ar - Br), D * (Ai - Bi)
        elif j == -1:
            return 1, D * (2 * Br + Ar), D * (2 * Bi + Ai), D * (Ar + Br), D * (Ai + Bi)
        elif j == 2:
            return 1, D * (3 * Ar - 4 * Br), D * (3 * Ai - 4 * Bi), D * (3 * Br - 2 * Ar), D * (3 * Bi - 2 * Ai)
        elif j == -2:
            return 1, D * (3 * Ar + 4 * Br), D * (3 * Ai + 4 * Bi), D * (3 * Br + 2 * Ar), D * (3 * Bi + 2 * Ai)
    fail(f"unsupported (orbit, j) = ({orbit}, {j})")


def exact_residual_table_rank3(
    cols, sol, Sr: np.ndarray, Si: np.ndarray, Ar: np.ndarray, Ai: np.ndarray, Br: np.ndarray, Bi: np.ndarray,
    orbit: str, m: int, j_list=(-2, -1, 0, 1, 2)
):
    """Fast exact integer residual table over all (4*2^m + 1)^3 slice combinations.
    Uses the 2x2 minor identity over Z[i]: if R = R_A + sqrt(d) R_B is zero or a
    complex multiple of a stabilizer state v in Z[i]^(2^m), then R_A and R_B are
    linearly dependent over Q(i), so every 2x2 minor R_{A,p} R_{B,q} - R_{A,q} R_{B,p}
    vanishes identically."""
    D, cAr, cAi, cBr, cBi = sol
    dim = 1 << m
    tA_r, tA_i, tB_r, tB_i = [], [], [], []
    for r_idx, c_idx in enumerate(cols):
        Wr_base, Wi_base = Sr[c_idx], Si[c_idx]
        # Build 4*2^m + 1 options for this single state
        _, _, o_r, o_i, _ = precompute_pauli_classes(Wr_base[None, :], Wi_base[None, :], m)
        Wr, Wi = o_r[0], o_i[0]
        car, cai = int(cAr[r_idx]), int(cAi[r_idx])
        cbr, cbi = int(cBr[r_idx]), int(cBi[r_idx])
        tA_r.append(car * Wr - cai * Wi)
        tA_i.append(car * Wi + cai * Wr)
        tB_r.append(cbr * Wr - cbi * Wi)
        tB_i.append(cbr * Wi + cbi * Wr)

    S01_Ar = (tA_r[0][:, None, :] + tA_r[1][None, :, :]).reshape(-1, dim)
    S01_Ai = (tA_i[0][:, None, :] + tA_i[1][None, :, :]).reshape(-1, dim)
    S01_Br = (tB_r[0][:, None, :] + tB_r[1][None, :, :]).reshape(-1, dim)
    S01_Bi = (tB_i[0][:, None, :] + tB_i[1][None, :, :]).reshape(-1, dim)

    results = {}
    for j in j_list:
        sc, tAr, tAi, tBr, tBi = ratio_scaled_target(Ar, Ai, Br, Bi, D, orbit, j)
        exact_cnt = 0
        stab_cnt = 0
        for k2 in range(len(tA_r[2])):
            # Fast 1D minor filter on coordinates (0, 1) and (2, 3) before full 2^m evaluation
            ra0_r = int(tAr[0]) - sc * (S01_Ar[:, 0] + int(tA_r[2][k2, 0]))
            ra0_i = int(tAi[0]) - sc * (S01_Ai[:, 0] + int(tA_i[2][k2, 0]))
            ra1_r = int(tAr[1]) - sc * (S01_Ar[:, 1] + int(tA_r[2][k2, 1]))
            ra1_i = int(tAi[1]) - sc * (S01_Ai[:, 1] + int(tA_i[2][k2, 1]))
            rb0_r = int(tBr[0]) - sc * (S01_Br[:, 0] + int(tB_r[2][k2, 0]))
            rb0_i = int(tBi[0]) - sc * (S01_Bi[:, 0] + int(tB_i[2][k2, 0]))
            rb1_r = int(tBr[1]) - sc * (S01_Br[:, 1] + int(tB_r[2][k2, 1]))
            rb1_i = int(tBi[1]) - sc * (S01_Bi[:, 1] + int(tB_i[2][k2, 1]))
            # Minor (0, 1): ra0 * rb1 - ra1 * rb0 == 0 in Z[i]
            m01_r = (ra0_r * rb1_r - ra0_i * rb1_i) - (ra1_r * rb0_r - ra1_i * rb0_i)
            m01_i = (ra0_r * rb1_i + ra0_i * rb1_r) - (ra1_r * rb0_i + ra1_i * rb0_r)
            keep = np.flatnonzero((m01_r == 0) & (m01_i == 0))
            if len(keep) == 0:
                continue
            R_Ar = tAr[None, :] - sc * (S01_Ar[keep] + tA_r[2][k2][None, :])
            R_Ai = tAi[None, :] - sc * (S01_Ai[keep] + tA_i[2][k2][None, :])
            R_Br = tBr[None, :] - sc * (S01_Br[keep] + tB_r[2][k2][None, :])
            R_Bi = tBi[None, :] - sc * (S01_Bi[keep] + tB_i[2][k2][None, :])
            for loc in range(len(keep)):
                ra_r, ra_i = R_Ar[loc], R_Ai[loc]
                rb_r, rb_i = R_Br[loc], R_Bi[loc]
                za = bool(np.all((ra_r == 0) & (ra_i == 0)))
                zb = bool(np.all((rb_r == 0) & (rb_i == 0)))
                if za and zb:
                    exact_cnt += 1
                elif za and not zb:
                    if is_exact_stabilizer_state_zi(rb_r, rb_i, m):
                        stab_cnt += 1
                elif zb and not za:
                    if is_exact_stabilizer_state_zi(ra_r, ra_i, m):
                        stab_cnt += 1
                else:
                    supp_a = (ra_r != 0) | (ra_i != 0)
                    supp_b = (rb_r != 0) | (rb_i != 0)
                    if not np.array_equal(supp_a, supp_b):
                        continue
                    c0 = int(np.argmax(supp_a))
                    b0r, b0i = int(rb_r[c0]), int(rb_i[c0])
                    a0r, a0i = int(ra_r[c0]), int(ra_i[c0])
                    if np.array_equal(ra_r * b0r - ra_i * b0i, rb_r * a0r - rb_i * a0i) and np.array_equal(
                        ra_r * b0i + ra_i * b0r, rb_r * a0i + rb_i * a0r
                    ):
                        if is_exact_stabilizer_state_zi(ra_r, ra_i, m):
                            stab_cnt += 1
        results[j] = (exact_cnt, stab_cnt)
    return results


def enumerate_d3_covers_exact(Sr3: np.ndarray, Si3: np.ndarray, G3: np.ndarray, orbit: str):
    """Exact 1-pivot Galois enumeration of r3_orbits, kind_a_orbits, kind_b_count, kind_c_orbits on D_3."""
    Ar, Ai, Br, Bi = target_galois_components(orbit, 3)
    Qr, Qi = galois_quotient_rays(Sr3, Si3, Ar, Ai, Br, Bi)
    z0, grps0 = canonical_ray_groups(Qr, Qi)
    if len(z0) != 0:
        fail(f"{orbit} m=3: expected 0 states in P_3")

    r3_all = set()
    r3_orbits = {}
    for g in grps0:
        if len(g) >= 3:
            for trip in itertools.combinations(g, 3):
                sol = exact_qi_solve(Sr3[list(trip)].T, Si3[list(trip)].T, Ar, Ai, Br, Bi)
                if sol is not None:
                    orb = np.sort(G3[:, list(trip)], axis=1)
                    for row in orb:
                        r3_all.add((int(row[0]), int(row[1]), int(row[2])))
                    canon = tuple(orb[np.lexsort((orb[:, 2], orb[:, 1], orb[:, 0]))[0]].tolist())
                    if canon not in r3_orbits:
                        r3_orbits[canon] = (
                            canon,
                            exact_qi_solve(Sr3[list(canon)].T, Si3[list(canon)].T, Ar, Ai, Br, Bi),
                        )

    max_g0 = max((len(g) for g in grps0), default=0)
    if max_g0 >= 4:
        fail(f"{orbit} m=3: unexpected ray group of size {max_g0} >= 4 in Q(i)^8 / P_3")
    kind_b_count = 0

    roots = np.min(G3, axis=0)
    orbit_reps = np.unique(roots)
    supp_masks = np.sum(((Sr3 != 0) | (Si3 != 0)).astype(np.int64) << np.arange(8)[None, :], axis=1)
    kind_a_orbits = {}

    for i in orbit_reps.tolist():
        stab_i = G3[G3[:, i] == i]
        cand = np.flatnonzero(roots >= i)
        cand = cand[cand != i]
        j_reps = set(np.min(stab_i[:, cand], axis=0).tolist())
        ur, ui = Qr[i], Qi[i]
        p_col = int(np.argmax((ur != 0) | (ui != 0)))
        upr, upi = int(ur[p_col]), int(ui[p_col])
        qc_r, qc_i = Qr[cand], Qi[cand]
        qp_r, qp_i = qc_r[:, p_col : p_col + 1], qc_i[:, p_col : p_col + 1]
        Vr = (upr * qc_r - upi * qc_i) - (qp_r * ur[None, :] - qp_i * ui[None, :])
        Vi = (upr * qc_i + upi * qc_r) - (qp_r * ui[None, :] + qp_i * ur[None, :])
        z_local, grps_local = canonical_ray_groups(Vr, Vi)
        z_ids = [int(cand[idx]) for idx in z_local]
        for g in grps_local:
            if len(g) + len(z_ids) >= 3:
                grp = sorted([int(cand[idx]) for idx in g] + z_ids)
                for j, k, l in itertools.combinations(grp, 3):
                    if j not in j_reps and k not in j_reps and l not in j_reps:
                        continue
                    cov4 = tuple(sorted((i, j, k, l)))
                    if (supp_masks[cov4[0]] | supp_masks[cov4[1]] | supp_masks[cov4[2]] | supp_masks[cov4[3]]) != 255:
                        continue
                    if (
                        (cov4[0], cov4[1], cov4[2]) in r3_all
                        or (cov4[0], cov4[1], cov4[3]) in r3_all
                        or (cov4[0], cov4[2], cov4[3]) in r3_all
                        or (cov4[1], cov4[2], cov4[3]) in r3_all
                    ):
                        continue
                    sol = exact_qi_solve(Sr3[list(cov4)].T, Si3[list(cov4)].T, Ar, Ai, Br, Bi)
                    if sol is not None:
                        orb = np.sort(G3[:, list(cov4)], axis=1)
                        canon = tuple(orb[np.lexsort((orb[:, 3], orb[:, 2], orb[:, 1], orb[:, 0]))[0]].tolist())
                        if canon not in kind_a_orbits:
                            kind_a_orbits[canon] = (
                                canon,
                                exact_qi_solve(Sr3[list(canon)].T, Si3[list(canon)].T, Ar, Ai, Br, Bi),
                            )

    kind_c_orbits = {}
    for canon_r3, _ in r3_orbits.values():
        for rep_pos in range(3):
            u_rep = canon_r3[rep_pos]
            mset = tuple(sorted(canon_r3 + (u_rep,)))
            orb = np.sort(G3[:, list(mset)], axis=1)
            canon_c = tuple(orb[np.lexsort((orb[:, 3], orb[:, 2], orb[:, 1], orb[:, 0]))[0]].tolist())
            if canon_c not in kind_c_orbits:
                vals, cnts = np.unique(canon_c, return_counts=True)
                u_blk = int(vals[cnts == 2][0])
                u_ords = [int(x) for x in vals[cnts == 1]]
                trip_c = (u_blk, u_ords[0], u_ords[1])
                sol_c = exact_qi_solve(Sr3[list(trip_c)].T, Si3[list(trip_c)].T, Ar, Ai, Br, Bi)
                if sol_c is None:
                    fail(f"failed to solve Kind-C base {trip_c}")
                kind_c_orbits[canon_c] = (trip_c, sol_c)

    return r3_orbits, kind_a_orbits, kind_b_count, kind_c_orbits


def match_kind_a_single_cover(
    cov, sol, Sr3: np.ndarray, Si3: np.ndarray, Opts_r: np.ndarray, Opts_i: np.ndarray,
    tAr1: np.ndarray, tAi1: np.ndarray, tBr1: np.ndarray, tBi1: np.ndarray, sc1: int,
    tAr2: np.ndarray, tAi2: np.ndarray, tBr2: np.ndarray, tBi2: np.ndarray, sc2: int,
    h_vec: np.ndarray,
) -> tuple[bool, int]:
    """Match one 4-term cover against slice target 1 (for 01 and 10) and slice target 2 (for 11)."""
    _, cAr, cAi, cBr, cBi = sol
    tabs = []
    for r in range(4):
        Wr, Wi = Opts_r[cov[r]], Opts_i[cov[r]]
        car, cai = int(cAr[r]), int(cAi[r])
        cbr, cbi = int(cBr[r]), int(cBi[r])
        pAr = car * Wr - cai * Wi
        pAi = car * Wi + cai * Wr
        pBr = cbr * Wr - cbi * Wi
        pBi = cbr * Wi + cbi * Wr
        tabs.append(np.hstack([pAr, pAi, pBr, pBi]))

    L = (tabs[0][:, None, :] + tabs[1][None, :, :]).reshape(1089, 32)
    R = (tabs[2][:, None, :] + tabs[3][None, :, :]).reshape(1089, 32)
    hL = L @ h_vec
    hR = R @ h_vec

    def solve_slice_vec(tAr, tAi, tBr, tBi, sc):
        tgt = np.concatenate([tAr, tAi, tBr, tBi])
        h_tgt = int(tgt @ h_vec)
        h_need = h_tgt - sc * hR
        hL_sc = sc * hL
        common = np.intersect1d(hL_sc, h_need)
        if len(common) == 0:
            return []
        lut = {}
        for idxL in np.flatnonzero(np.isin(hL_sc, common)).tolist():
            lut.setdefault(int(hL_sc[idxL]), []).append(idxL)
        hits = []
        for idxR in np.flatnonzero(np.isin(h_need, common)).tolist():
            k = int(h_need[idxR])
            if k in lut:
                need_row = tgt - sc * R[idxR]
                m2, m3 = divmod(idxR, 33)
                for idxL in lut[k]:
                    if np.array_equal(sc * L[idxL], need_row):
                        m0, m1 = divmod(idxL, 33)
                        hits.append((m0, m1, m2, m3))
        return hits

    hits_1 = solve_slice_vec(tAr1, tAi1, tBr1, tBi1, sc1)
    if not hits_1:
        return False, 0
    hits_2 = solve_slice_vec(tAr2, tAi2, tBr2, tBi2, sc2)
    if not hits_2:
        return True, 0
    valid_5q = 0
    for m01 in hits_1:
        for m10 in hits_1:
            for m11 in hits_2:
                ok = True
                for r in range(4):
                    u_idx = cov[r]
                    vr = np.concatenate([Sr3[u_idx], Opts_r[u_idx, m01[r]], Opts_r[u_idx, m10[r]], Opts_r[u_idx, m11[r]]])
                    vi = np.concatenate([Si3[u_idx], Opts_i[u_idx, m01[r]], Opts_i[u_idx, m10[r]], Opts_i[u_idx, m11[r]]])
                    if not is_exact_stabilizer_state_zi(vr, vi, 5):
                        ok = False
                        break
                if ok:
                    valid_5q += 1
    return True, valid_5q


def run_planted_positive_control(Sr3: np.ndarray, Si3: np.ndarray, Opts_r: np.ndarray, Opts_i: np.ndarray, h_vec: np.ndarray) -> None:
    """Positive control: plant a genuine 5-qubit rank-4 stabilizer decomposition with all-plane
    terms and verify that match_kind_a_single_cover recovers it."""
    cov = (0, 8, 112, 568)
    # Build 4 genuine 5-qubit stabilizer states by repeating each 3-qubit state across 00, 01, 10, 11 (code 0)
    sol = (1, np.array([1, 2, -1, 1], dtype=np.int64), np.zeros(4, dtype=np.int64),
           np.array([0, 1, 1, -1], dtype=np.int64), np.zeros(4, dtype=np.int64))
    _, cAr, cAi, cBr, cBi = sol
    tAr = Sr3[ list(cov) ].T @ cAr
    tAi = Si3[ list(cov) ].T @ cAr
    tBr = Sr3[ list(cov) ].T @ cBr
    tBi = Si3[ list(cov) ].T @ cBr
    surv1, full_hits = match_kind_a_single_cover(
        cov, sol, Sr3, Si3, Opts_r, Opts_i,
        tAr, tAi, tBr, tBi, 1,
        tAr, tAi, tBr, tBi, 1,
        h_vec,
    )
    if not surv1 or full_hits == 0:
        fail("planted 5-qubit positive control failed: matcher did not recover planted decomposition")


def verify_kind_c_orthogonal_exclusion(
    kc_orbits: dict, Br_p: np.ndarray, Bi_p: np.ndarray, Opts_r: np.ndarray, Opts_i: np.ndarray, orbit: str
) -> int:
    """Verify via the 8-element orthogonal Pauli basis that every Kind-C multiset has min_supp >= 4 > 2 at j = 2."""
    Ar, Ai, Br, Bi = target_galois_components(orbit, 3)
    global_min_supp = 8
    for canon_c, (trip_c, sol) in kc_orbits.items():
        u_blk, u1, u2 = trip_c
        D, cAr, cAi, cBr, cBi = sol
        Pr, Pi = Br_p[u_blk], Bi_p[u_blk]
        W1r, W1i, W2r, W2i = Opts_r[u1], Opts_i[u1], Opts_r[u2], Opts_i[u2]
        S12_Ar = ((int(cAr[1]) * W1r - int(cAi[1]) * W1i)[:, None, :] + (int(cAr[2]) * W2r - int(cAi[2]) * W2i)[None, :, :]).reshape(1089, 8)
        S12_Ai = ((int(cAr[1]) * W1i + int(cAi[1]) * W1r)[:, None, :] + (int(cAr[2]) * W2i + int(cAi[2]) * W2r)[None, :, :]).reshape(1089, 8)
        S12_Br = ((int(cBr[1]) * W1r - int(cBi[1]) * W1i)[:, None, :] + (int(cBr[2]) * W2r - int(cBi[2]) * W2i)[None, :, :]).reshape(1089, 8)
        S12_Bi = ((int(cBr[1]) * W1i + int(cBi[1]) * W1r)[:, None, :] + (int(cBr[2]) * W2i + int(cBi[2]) * W2r)[None, :, :]).reshape(1089, 8)
        sc, tAr, tAi, tBr, tBi = ratio_scaled_target(Ar, Ai, Br, Bi, D, orbit, 2)
        R_Ar, R_Ai = tAr[None, :] - sc * S12_Ar, tAi[None, :] - sc * S12_Ai
        R_Br, R_Bi = tBr[None, :] - sc * S12_Br, tBi[None, :] - sc * S12_Bi
        aAr, aAi = R_Ar @ Pr.T + R_Ai @ Pi.T, R_Ai @ Pr.T - R_Ar @ Pi.T
        aBr, aBi = R_Br @ Pr.T + R_Bi @ Pi.T, R_Bi @ Pr.T - R_Br @ Pi.T
        supp_cnt = np.sum((aAr != 0) | (aAi != 0) | (aBr != 0) | (aBi != 0), axis=1)
        min_s = int(supp_cnt.min())
        if min_s <= 2:
            fail(f"{orbit} Kind-C {canon_c}: expected min orthogonal Pauli support > 2 at j=2, got {min_s}")
        global_min_supp = min(global_min_supp, min_s)
    return global_min_supp


def main() -> int:
    t0 = time.time()
    check_symbolic_target_consistency()
    E3 = stabilizer_exponents(3)
    lut_r = np.array([1, 0, -1, 0, 0], dtype=np.int64)
    lut_i = np.array([0, 1, 0, -1, 0], dtype=np.int64)
    idx3 = np.where(E3 >= 0, E3, 4)
    Sr3, Si3 = lut_r[idx3], lut_i[idx3]
    Sr4, Si4 = dictionary_zi(4)

    Br_p, Bi_p, Opts_r, Opts_i, _ = precompute_pauli_classes(Sr3, Si3, 3)
    print(f"D_3 (1,080 states) and 8-element orthogonal Pauli bases verified [{time.time()-t0:.2f}s]")

    rng = np.random.default_rng(20261110)
    h_vec = rng.integers(1, 1 << 28, size=32, dtype=np.int64)
    run_planted_positive_control(Sr3, Si3, Opts_r, Opts_i, h_vec)
    print("positive control: planted 5-qubit rank-4 stabilizer decomposition recovered")

    # Fact 1 on D_4: chi(qubit_H^4) >= 4 (0 pivots) and qubit_T m=4 residual table at j = +-1
    Ar4_H, Ai4_H, Br4_H, Bi4_H = target_galois_components("qubit_H", 4)
    z4_H, grps4_H = canonical_ray_groups(*galois_quotient_rays(Sr4, Si4, Ar4_H, Ai4_H, Br4_H, Bi4_H))
    if len(z4_H) != 0 or max((len(g) for g in grps4_H), default=0) >= 3:
        fail("qubit_H m=4 rank-3 exclusion failed")

    Ar4_T, Ai4_T, Br4_T, Bi4_T = target_galois_components("qubit_T", 4)
    z4_T, grps4_T = canonical_ray_groups(*galois_quotient_rays(Sr4, Si4, Ar4_T, Ai4_T, Br4_T, Bi4_T))
    if len(z4_T) != 0:
        fail("qubit_T m=4 rank-2 exclusion failed")
    decs4_T = [
        (trip, exact_qi_solve(Sr4[list(trip)].T, Si4[list(trip)].T, Ar4_T, Ai4_T, Br4_T, Bi4_T))
        for g in grps4_T
        if len(g) >= 3
        for trip in itertools.combinations(g, 3)
    ]
    decs4_T = [(t, s) for (t, s) in decs4_T if s is not None]
    if len(decs4_T) != 9:
        fail(f"expected 9 rank-3 decompositions of |T>^4, got {len(decs4_T)}")
    res_t4 = exact_residual_table_rank3(
        decs4_T[0][0], decs4_T[0][1], Sr4, Si4, Ar4_T, Ai4_T, Br4_T, Bi4_T, "qubit_T", 4, (-1, 0, 1)
    )
    if res_t4[-1] != (0, 0) or res_t4[1] != (0, 0) or res_t4[0] != (1, 192):
        fail(f"Fact 1 residual table mismatch on |T>^4: {res_t4}")
    print(f"Fact 1 verified in exact Z[i] arithmetic: chi(H^4) = 4 and |T>^4 table {res_t4} [{time.time()-t0:.2f}s]")

    for orbit, want_g3, want_r3, want_ka, want_kc, want_surv1 in (
        ("qubit_H", 48, 2, 2406, 6, 30),
        ("qubit_T", 162, 4, 2372, 8, 196),
    ):
        G3 = build_g3_group(E3, Sr3, Si3, orbit)
        if len(G3) != want_g3:
            fail(f"{orbit}: expected |G_3| = {want_g3}, got {len(G3)}")
        r3_orbs, ka_orbs, kb_cnt, kc_orbs = enumerate_d3_covers_exact(Sr3, Si3, G3, orbit)
        if len(r3_orbs) != want_r3 or len(ka_orbs) != want_ka or kb_cnt != 0 or len(kc_orbs) != want_kc:
            fail(
                f"{orbit} census mismatch: r3={len(r3_orbs)} (want {want_r3}), "
                f"KindA={len(ka_orbs)} (want {want_ka}), KindB={kb_cnt}, KindC={len(kc_orbs)} (want {want_kc})"
            )

        # Verify j = +-2 exact residual count is 0 across all rank-3 G_3-orbits (n_B = 0 proof)
        Ar3, Ai3, Br3, Bi3 = target_galois_components(orbit, 3)
        for canon_r3, (trip, sol_r3) in r3_orbs.items():
            res_r3 = exact_residual_table_rank3(trip, sol_r3, Sr3, Si3, Ar3, Ai3, Br3, Bi3, orbit, 3, (-2, 2))
            if res_r3[-2][0] != 0 or res_r3[2][0] != 0:
                fail(f"{orbit} rank-3 orbit {canon_r3} has non-zero exact count at j=+-2: {res_r3}")

        min_supp_c = verify_kind_c_orthogonal_exclusion(kc_orbs, Br_p, Bi_p, Opts_r, Opts_i, orbit)

        surv1_cnt = 0
        surv_full_cnt = 0
        for cov, sol in ka_orbs.values():
            D = sol[0]
            sc1, tAr1, tAi1, tBr1, tBi1 = ratio_scaled_target(Ar3, Ai3, Br3, Bi3, D, orbit, 1)
            sc2, tAr2, tAi2, tBr2, tBi2 = ratio_scaled_target(Ar3, Ai3, Br3, Bi3, D, orbit, 2)
            s1, sfull = match_kind_a_single_cover(
                cov, sol, Sr3, Si3, Opts_r, Opts_i,
                tAr1, tAi1, tBr1, tBi1, sc1,
                tAr2, tAi2, tBr2, tBi2, sc2,
                h_vec,
            )
            if s1:
                surv1_cnt += 1
            surv_full_cnt += sfull

        if surv1_cnt != want_surv1 or surv_full_cnt != 0:
            fail(f"{orbit} Kind-A matching mismatch: surv_j1={surv1_cnt} (want {want_surv1}), surv_full={surv_full_cnt}")
        print(
            f"{orbit}: |G_3|={len(G3)}, r3_orbits={len(r3_orbs)} (j=+-2 exact=0), "
            f"KindA={len(ka_orbs)} (j=1 survivors={surv1_cnt}, 5-qubit hits={surv_full_cnt}), "
            f"KindB=0, KindC={len(kc_orbs)} (min orthogonal Pauli support at j=2 is {min_supp_c} > 2) "
            f"[{time.time()-t0:.2f}s]"
        )

    for claim in (
        "CERTIFIED chi(qubit_H^5) >= 5",
        "CERTIFIED chi(qubit_H^6) >= 5",
        "CERTIFIED chi(qubit_T^5) >= 5",
        "CERTIFIED chi(qubit_T^6) >= 5",
    ):
        print(claim)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
