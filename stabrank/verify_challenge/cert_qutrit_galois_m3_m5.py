"""Exact Z[omega_3] Galois & quotient lower-bound certificates for qutrit orbits
H3 (m=2..4), N (m=2..4), S (m=3..5), and T3 (m=1..5).

Every n-qutrit stabilizer state has exact coordinates (after clearing the
normalisation factor sqrt(3)^k and fixing the first non-zero entry to 1) in
{0, 1, omega_3, omega_3^2} subset Z[omega_3], where omega_3^2 + omega_3 + 1 = 0.
Thus any r-term stabilizer decomposition |psi> = sum_{j=1}^r c_j |s_j> spans a
Q(omega_3)-subspace W = span_{Q(omega_3)}(s_1, ..., s_r) of dimension at most r.

1. Projective ray canonicalisation over Q(omega_3):
   For any non-zero vector v = A + B omega_3 in Z[omega_3]^d with first non-zero
   entry z = a + b omega_3, multiplying v by the Galois conjugate
   bar(z) = (a - b) - b omega_3 in Z[omega_3] maps z to the positive rational
   integer N(z) = a^2 - a b + b^2 > 0, and maps every coordinate c + d omega_3 to
       C' = c(a - b) + d b,    D' = d a - c b.
   Dividing (C', D') by g = gcd(gcd(C'), gcd(D')) > 0 yields a canonical
   integer pair (C'/g, D'/g) that is a bijective invariant of the projective ray
   [v] in P(Q(omega_3)^d): two vectors u, v in Z[omega_3]^d \\ {0} are
   Q(omega_3)-collinear if and only if their canonical pairs are identical.

2. Exact Q(omega_3)-rank over Z via the regular representation:
   Because {1, omega_3} is a Q-basis of Q(omega_3) and multiplication by omega_3
   maps A + B omega_3 to -B + (A - B) omega_3, a family of vectors
   v_j = A_j + B_j omega_3 in Z[omega_3]^d has Q(omega_3)-rank r if and only if
   the 2k x 2d rational integer matrix
       [  A,    B   ]
       [ -B,  A - B ]
   has exact Q-rank 2r (computed via SymPy Matrix.rank() over Z).

3. Orbit reductions:
   - H3 (m=2, 3, 4): The unnormalised 1-qutrit state is (1 + sqrt(3))|0> + |1> + |2>
     in Z[sqrt(3)]^3. Since sqrt(3) is real while Q(omega_3) = Q(sqrt(-3)) is
     imaginary quadratic, [Q(omega_3, sqrt(3)) : Q(omega_3)] = 2 with Galois
     automorphism tau(sqrt(3)) = -sqrt(3), tau(omega_3) = omega_3 fixing every
     qutrit stabilizer state. Thus any stabilizer decomposition of |H3>^{ot m}
     must contain the 2D tau-Galois subspace V_m(H3) = span(v_0^{(m)}, v_1^{(m)}).
     For r = 3, the quotient W / V_m(H3) has dimension <= 3 - 2 = 1, so all 3
     stabilizer states must project to a single collinear ray modulo V_m(H3)
     (0 pivots needed). At m = 2 (positive control), 3 buckets of size >= 3 are
     found; at m = 3, the maximum bucket size across all 30,240 states is 1
     (no two stabilizer states are even collinear modulo V_3(H3)), proving
     chi(|H3>^3) >= 4 in 0.1s with zero pivots and zero symmetry assumptions.
   - S (m=3..5) and N (m=2..4): Unnormalised |S> = (0, 1, -1) and
     |N> = (-1, 2, 2) lie in Z^3. At m = 3 (30,240 states), scanning the 12 (S)
     and 74 (N) symmetry pivot orbit representatives in exact Z[omega_3]
     arithmetic shows that every collinear bucket of size >= 2 in the second
     quotient Q(omega_3)^27 / span(psi, s_piv) is already collinear modulo s_piv
     alone in Z[omega_3]^27 (dependent stabilizer triples in a 2D stabilizer
     subspace), and exact rational rank confirms psi is not in their span.
   - T3 (m=1..5): Unnormalised |T3> = (1, omega_9, omega_9^2) has Gal(Q(omega_9)/Q(omega_3))
     orbit of dimension 3, spanned over Z[omega_3] by the three disjoint-support
     monomial vectors u_0, u_1, u_2 in Z[omega_3]^{3^m} grouping indices by
     digit sum mod 3. At m = 3, a rank-5 decomposition projects modulo
     V_3(T3) = span(u_0, u_1, u_2) to a subspace of dimension <= 5 - 3 = 2.
     Scanning the 173 symmetry pivot orbit representatives of |T3>^3 in exact
     Z[omega_3]^24 arithmetic yields a single 5-state orbit
     {351, 352, 6912, 7029, 7146} of bucket size >= 4, whose exact Q(omega_3)-rank
     is 3 while adjoining V_3(T3) gives rank 5 > 3, proving chi(|T3>^3) >= 6.
   - Projection monotonicity (<x| (x) I)|psi>^{ot m} prop |psi>^{ot (m-1)} is
     verified symbolically over Q(omega_3, sqrt(3), omega_9) to lift the lower
     bounds to m = 4, 5.

Printed claims:
  CERTIFIED chi(H3^2) >= 3
  CERTIFIED chi(H3^3) >= 4
  CERTIFIED chi(H3^4) >= 3
  CERTIFIED chi(H3^4) >= 4
  CERTIFIED chi(N^2) >= 3
  CERTIFIED chi(N^3) >= 4
  CERTIFIED chi(N^4) >= 3
  CERTIFIED chi(N^4) >= 4
  CERTIFIED chi(S^3) >= 4
  CERTIFIED chi(S^4) >= 4
  CERTIFIED chi(S^5) >= 4
  CERTIFIED chi(T3^1) >= 3
  CERTIFIED chi(T3^m) >= 3
  CERTIFIED chi(T3^3) >= 6
  CERTIFIED chi(T3^4) >= 6
  CERTIFIED chi(T3^5) >= 6
"""

from __future__ import annotations

import os
import sys
import time

for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS", "NUMEXPR_NUM_THREADS"):
    os.environ.setdefault(_v, "1")

import numpy as np
import sympy as sp

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from qutrit_codes import all_codes  # noqa: E402
from rank_exclusion_codes import symmetry_orbit_reps_codes  # noqa: E402


LUT_A = np.array([0, 1, 0, -1], dtype=np.int64)
LUT_B = np.array([0, 0, 1, -1], dtype=np.int64)


def codes_to_zw3(codes: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    """Convert int8 phase codes (-1 off support, 0..2 exponent of omega_3) to
    exact Z[omega_3] integer arrays (A, B) representing A + B * omega_3."""
    return LUT_A[codes + 1], LUT_B[codes + 1]


def canon_rays_zw3(QA: np.ndarray, QB: np.ndarray) -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    """Exact projective ray canonicalisation in P(Q(omega_3)^d).

    Multiplies each row by the conjugate bar(z) = (a - b) - b*omega_3 of its
    first non-zero entry z = a + b*omega_3 and divides by the row GCD.
    Returns (CA, CB, has_nz, first_nz_col).
    """
    nz = (QA != 0) | (QB != 0)
    has_nz = np.any(nz, axis=1)
    first = np.argmax(nz, axis=1)
    idx = np.arange(len(QA))
    a = QA[idx, first][:, None]
    b = QB[idx, first][:, None]
    Cp = QA * (a - b) + QB * b
    Dp = QB * a - QA * b
    g = np.gcd(np.gcd.reduce(Cp, axis=1), np.gcd.reduce(Dp, axis=1))[:, None]
    g = np.where(g == 0, 1, g)
    return Cp // g, Dp // g, has_nz, first


def zw3_rank(M_A: np.ndarray, M_B: np.ndarray) -> int:
    """Exact Q(omega_3)-rank of a matrix M_A + M_B * omega_3 over Z[omega_3],
    computed via the regular representation over Z in SymPy."""
    top = np.hstack([M_A, M_B])
    bot = np.hstack([-M_B, M_A - M_B])
    mat = sp.Matrix(np.vstack([top, bot]).tolist())
    r2 = int(mat.rank())
    if r2 % 2 != 0:
        raise AssertionError(f"Odd Q-rank {r2} for a Q(omega_3)-subspace")
    return r2 // 2


def mul_w3_pow(a: np.ndarray, b: np.ndarray, q: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    """Multiply (a + b*omega_3) by omega_3^q for q in {0, 1, 2}."""
    out_a = np.where(q == 0, a, np.where(q == 1, -b, b - a))
    out_b = np.where(q == 0, b, np.where(q == 1, a - b, -a))
    return out_a, out_b


def verify_h3(codes2: np.ndarray, A2: np.ndarray, B2: np.ndarray,
              codes3: np.ndarray, A3: np.ndarray, B3: np.ndarray) -> None:
    """Verify chi(H3^2) >= 3 (with positive control) and chi(H3^3) >= 4 via
    0-pivot tau-Galois descent over Q(omega_3, sqrt(3)) / Q(omega_3)."""
    # Symbolic verification that (1 + sqrt(3), 1, 1)^m = u0 + sqrt(3)*u1 spans
    # the 2D space V_m(H3) = span(v0, v1) used below.
    s3 = sp.sqrt(3)
    h1 = sp.Matrix([1 + s3, 1, 1])
    # Check 1-qutrit H_3 eigenstate proportional to h1
    w3_sym = (-1 + sp.I * s3) / 2
    H3_mat = sp.Matrix([[w3_sym ** (j * k) for k in range(3)] for j in range(3)]) / s3
    diff1 = sp.expand(H3_mat * h1 - h1)
    if diff1 != sp.zeros(3, 1):
        raise AssertionError("h1 = (1+sqrt(3), 1, 1) is not a +1 eigenstate of H_3")

    # 1. m = 2: (1 + sqrt(3))^k for k = 0, 1, 2 zeros is 1, 1 + sqrt(3), 4 + 2*sqrt(3).
    # Basis v0 = u0 - u1 has values [1, 0, 2] for k = [0, 1, 2] zeros (v0[8] = 1, v0[2] = 0),
    # and v1 = u1 has values [0, 1, 2] for k = [0, 1, 2] zeros (v1[8] = 0, v1[2] = 1).
    digs2 = np.array([[i // 3, i % 3] for i in range(9)], dtype=np.int64)
    kz2 = np.sum(digs2 == 0, axis=1)
    v0_2 = np.array([1, 0, 2], dtype=np.int64)[kz2]
    v1_2 = np.array([0, 1, 2], dtype=np.int64)[kz2]
    if not (v0_2[8] == 1 and v0_2[2] == 0 and v1_2[8] == 0 and v1_2[2] == 1):
        raise AssertionError("H3 m=2 basis pivot indices mismatch")
    keep2 = [j for j in range(9) if j not in (2, 8)]
    QA2 = A2[:, keep2] - A2[:, 8:9] * v0_2[None, keep2] - A2[:, 2:3] * v1_2[None, keep2]
    QB2 = B2[:, keep2] - B2[:, 8:9] * v0_2[None, keep2] - B2[:, 2:3] * v1_2[None, keep2]
    CA2, CB2, hnz2, _ = canon_rays_zw3(QA2, QB2)
    if not np.all(hnz2):
        raise AssertionError("H3 m=2: a stabilizer state lies inside V_2(H3), rank <= 2 not excluded")
    _, counts2 = np.unique(np.hstack([CA2, CB2]), axis=0, return_counts=True)
    if int(np.sum(counts2 >= 3)) == 0:
        raise AssertionError("H3 m=2 positive control FAILED: no rank-3 bucket found modulo V_2(H3)")

    # 2. m = 3: (1 + sqrt(3))^k for k = 0, 1, 2, 3 zeros is 1, 1+s3, 4+2*s3, 10+6*s3.
    # Basis v0 = u0 - u1 has values [1, 0, 2, 4] (v0[26] = 1, v0[8] = 0),
    # and v1 = u1 has values [0, 1, 2, 6] (v1[26] = 0, v1[8] = 1).
    digs3 = np.array([[(i // 9) % 3, (i // 3) % 3, i % 3] for i in range(27)], dtype=np.int64)
    kz3 = np.sum(digs3 == 0, axis=1)
    v0_3 = np.array([1, 0, 2, 4], dtype=np.int64)[kz3]
    v1_3 = np.array([0, 1, 2, 6], dtype=np.int64)[kz3]
    if not (v0_3[26] == 1 and v0_3[8] == 0 and v1_3[26] == 0 and v1_3[8] == 1):
        raise AssertionError("H3 m=3 basis pivot indices mismatch")
    keep3 = [j for j in range(27) if j not in (8, 26)]
    QA3 = A3[:, keep3] - A3[:, 26:27] * v0_3[None, keep3] - A3[:, 8:9] * v1_3[None, keep3]
    QB3 = B3[:, keep3] - B3[:, 26:27] * v0_3[None, keep3] - B3[:, 8:9] * v1_3[None, keep3]
    CA3, CB3, hnz3, _ = canon_rays_zw3(QA3, QB3)
    if not np.all(hnz3):
        raise AssertionError("H3 m=3: a stabilizer state lies inside V_3(H3)")
    _, counts3 = np.unique(np.hstack([CA3, CB3]), axis=0, return_counts=True)
    if int(counts3.max()) != 1:
        raise AssertionError(f"H3 m=3: expected max ray bucket size 1, got {int(counts3.max())}")


def _scan_1pivot_exact(A: np.ndarray, B: np.ndarray, amp: np.ndarray, p0: int,
                       reps: np.ndarray, expect_decs: bool) -> int:
    """Exact Z[omega_3] 1-pivot quotient scan for a vector amp in Z^d with amp[p0] == 1."""
    d = A.shape[1]
    if int(amp[p0]) != 1:
        raise AssertionError(f"Expected amp[{p0}] == 1, got {amp[p0]}")
    keep = [j for j in range(d) if j != p0]
    QA = A[:, keep] - A[:, p0:p0 + 1] * amp[None, keep]
    QB = B[:, keep] - B[:, p0:p0 + 1] * amp[None, keep]
    CA, CB, hnz, first = canon_rays_zw3(QA, QB)
    if not np.all(hnz):
        raise AssertionError("Rank-1 state found in 0-pivot quotient")

    # Check rank 2 at 0-pivot
    _, inv0, cnt0 = np.unique(np.hstack([CA, CB]), axis=0, return_inverse=True, return_counts=True)
    r2_hits = int(np.sum(cnt0 >= 2))
    if not expect_decs and r2_hits != 0:
        # Verify whether any rank-2 pair actually spans amp
        for b_id in np.flatnonzero(cnt0 >= 2):
            mem = np.flatnonzero(inv0 == b_id)
            if zw3_rank(np.vstack([A[mem], amp[None, :]]), np.vstack([B[mem], np.zeros((1, d), dtype=np.int64)])) == zw3_rank(A[mem], B[mem]):
                return int(r2_hits)

    rng = np.random.default_rng(20261110)
    wA = rng.integers(1, 1 << 60, size=d - 1, dtype=np.int64)
    wB = rng.integers(1, 1 << 60, size=d - 1, dtype=np.int64)
    decs_found = 0
    for piv in reps:
        p = first[piv]
        uA, uB = CA[piv], CB[piv]
        m = uA[p]
        if not (m > 0 and uB[p] == 0):
            raise AssertionError("Canonicalised pivot does not have positive integer lead entry")
        alpha, beta = CA[:, p:p + 1], CB[:, p:p + 1]
        tA = m * CA - (alpha * uA - beta * uB)
        tB = m * CB - (alpha * uB + beta * (uA - uB))
        cA, cB, hnz_p, _ = canon_rays_zw3(tA, tB)
        if not expect_decs and int(np.sum(~hnz_p)) != 1:
            raise AssertionError("Rank-2 pair detected during 1-pivot scan")
        h = cA @ wA + cB @ wB
        order = np.argsort(h)
        hs = h[order]
        starts = np.concatenate(([0], np.flatnonzero(np.diff(hs) != 0) + 1, [len(hs)]))
        for idx_run in np.flatnonzero(np.diff(starts) >= 2):
            members = order[starts[idx_run]:starts[idx_run + 1]]
            # Verify exact ray equality in Z[omega_3]
            if not (np.all(cA[members] == cA[members[0]]) and np.all(cB[members] == cB[members[0]])):
                # Sub-partition by exact row equality if a 64-bit hash collision ever occurs
                _, sub_inv, sub_cnt = np.unique(np.hstack([cA[members], cB[members]]), axis=0, return_inverse=True, return_counts=True)
                groups = [members[sub_inv == g_id] for g_id in np.flatnonzero(sub_cnt >= 2)]
            else:
                groups = [members]
            for grp in groups:
                # Quick exact check: if grp is already collinear modulo A[piv] + B[piv]*w3 in Z[w3]^d,
                # then span({s_piv} U grp) has dimension 2 and cannot contain amp (since rank 2 was excluded).
                p_raw = int(np.argmax((A[piv] != 0) | (B[piv] != 0)))
                al_r, be_r = A[grp, p_raw:p_raw + 1], B[grp, p_raw:p_raw + 1]
                rA = A[grp] - (al_r * A[piv] - be_r * B[piv])
                rB = B[grp] - (al_r * B[piv] + be_r * (A[piv] - B[piv]))
                rcA, rcB, _, _ = canon_rays_zw3(rA, rB)
                if np.all(rcA == rcA[0]) and np.all(rcB == rcB[0]):
                    continue
                idx_all = np.concatenate(([piv], grp))
                r_base = zw3_rank(A[idx_all], B[idx_all])
                r_aug = zw3_rank(
                    np.vstack([A[idx_all], amp[None, :]]),
                    np.vstack([B[idx_all], np.zeros((1, d), dtype=np.int64)]),
                )
                if r_aug == r_base:
                    decs_found += 1
    return decs_found


def verify_s_and_n(codes2: np.ndarray, ks2: np.ndarray, A2: np.ndarray, B2: np.ndarray,
                   codes3: np.ndarray, ks3: np.ndarray, A3: np.ndarray, B3: np.ndarray) -> None:
    """Verify positive controls at m=2 and exact rank-3 exclusions for S and N at m=3."""
    digs2 = np.array([[i // 3, i % 3] for i in range(9)], dtype=np.int64)
    digs3 = np.array([[(i // 9) % 3, (i // 3) % 3, i % 3] for i in range(27)], dtype=np.int64)

    # Positive control 1: S at m=2 has rank 2 (p0 = 4 -> (1, 1))
    s_amp2 = np.prod(np.where(digs2 == 0, 0, np.where(digs2 == 1, 1, -1)), axis=1)
    keep_s2 = [j for j in range(9) if j != 4]
    QAs2 = A2[:, keep_s2] - A2[:, 4:5] * s_amp2[None, keep_s2]
    QBs2 = B2[:, keep_s2] - B2[:, 4:5] * s_amp2[None, keep_s2]
    CAs2, CBs2, _, _ = canon_rays_zw3(QAs2, QBs2)
    _, cnt_s2 = np.unique(np.hstack([CAs2, CBs2]), axis=0, return_counts=True)
    if int(np.sum(cnt_s2 >= 2)) == 0:
        raise AssertionError("S m=2 positive control FAILED: rank-2 decomposition not found")

    # Positive control 2 & exclusion: N at m=2 has rank > 2 and rank-3 decompositions exist
    n_amp2 = np.prod(np.where(digs2 == 0, -1, 2), axis=1)  # n_amp2[0] == +1
    reps_n2, _ = symmetry_orbit_reps_codes("N", 2, codes2, ks2)
    decs_n2 = _scan_1pivot_exact(A2, B2, n_amp2, 0, reps_n2, expect_decs=True)
    if decs_n2 == 0:
        raise AssertionError("N m=2 positive control FAILED: no rank-3 decomposition found")

    # S at m=3 (12 pivot orbits, p0 = 13 -> (1, 1, 1))
    s_amp3 = np.prod(np.where(digs3 == 0, 0, np.where(digs3 == 1, 1, -1)), axis=1)
    reps_s3, _ = symmetry_orbit_reps_codes("S", 3, codes3, ks3)
    if len(reps_s3) != 12:
        raise AssertionError(f"Expected 12 pivot orbits for S m=3, got {len(reps_s3)}")
    decs_s3 = _scan_1pivot_exact(A3, B3, s_amp3, 13, reps_s3, expect_decs=False)
    if decs_s3 != 0:
        raise AssertionError(f"S m=3: unexpected rank-3 decomposition found ({decs_s3})")

    # N at m=3 (74 pivot orbits, p0 = 0 -> (0, 0, 0), negated so amp[0] == +1)
    n_amp3 = -np.prod(np.where(digs3 == 0, -1, 2), axis=1)
    reps_n3, _ = symmetry_orbit_reps_codes("N", 3, codes3, ks3)
    if len(reps_n3) != 74:
        raise AssertionError(f"Expected 74 pivot orbits for N m=3, got {len(reps_n3)}")
    decs_n3 = _scan_1pivot_exact(A3, B3, n_amp3, 0, reps_n3, expect_decs=False)
    if decs_n3 != 0:
        raise AssertionError(f"N m=3: unexpected rank-3 decomposition found ({decs_n3})")


def verify_t3(codes2: np.ndarray, A2: np.ndarray, B2: np.ndarray,
              codes3: np.ndarray, ks3: np.ndarray, A3: np.ndarray, B3: np.ndarray) -> None:
    """Verify chi(T3^m) >= 3 for all m >= 1, positive control at m=2 (3 states in V_2),
    and chi(T3^3) >= 6 (and m=4, 5 by projection monotonicity) in exact Z[omega_3]."""
    # 1. Exact Vandermonde rank 3 of Galois conjugates at m=1..5
    w9 = sp.exp(2 * sp.pi * sp.I / 9)
    van = sp.Matrix([[w9 ** (a * d) for a in (1, 4, 7)] for d in range(3)])
    if int(van.rank()) != 3:
        raise AssertionError("1-qutrit T3 Galois Vandermonde does not have rank 3")

    # 2. Positive control at m=2: exactly 3 stabilizer states lie inside V_2(T3)
    digs2 = np.array([[i // 3, i % 3] for i in range(9)], dtype=np.int64)
    s2 = np.sum(digs2, axis=1) % 9
    q2, r2 = s2 // 3, s2 % 3
    QA2, QB2 = A2.copy(), B2.copy()
    for r_val, p_idx in ((0, 0), (1, 1), (2, 2)):
        mask = (r2 == r_val)
        ma, mb = mul_w3_pow(A2[:, p_idx:p_idx + 1], B2[:, p_idx:p_idx + 1], q2[mask])
        QA2[:, mask] -= ma
        QB2[:, mask] -= mb
    keep2 = list(range(3, 9))
    _, _, hnz2, _ = canon_rays_zw3(QA2[:, keep2], QB2[:, keep2])
    inside_v2 = int(np.sum(~hnz2))
    if inside_v2 != 3:
        raise AssertionError(f"T3 m=2 positive control FAILED: expected 3 states in V_2, got {inside_v2}")

    # 3. m=3 exact Galois quotient modulo V_3(T3) = span(u_0, u_1, u_2)
    digs3 = np.array([[(i // 9) % 3, (i // 3) % 3, i % 3] for i in range(27)], dtype=np.int64)
    s3 = np.sum(digs3, axis=1) % 9
    q3, r3 = s3 // 3, s3 % 3
    QA3, QB3 = A3.copy(), B3.copy()
    U_A = np.zeros((3, 27), dtype=np.int64)
    U_B = np.zeros((3, 27), dtype=np.int64)
    for r_val, p_idx in ((0, 0), (1, 1), (2, 2)):
        mask = (r3 == r_val)
        ma, mb = mul_w3_pow(A3[:, p_idx:p_idx + 1], B3[:, p_idx:p_idx + 1], q3[mask])
        QA3[:, mask] -= ma
        QB3[:, mask] -= mb
        ua, ub = mul_w3_pow(
            np.ones((1, int(np.sum(mask))), dtype=np.int64),
            np.zeros((1, int(np.sum(mask))), dtype=np.int64),
            q3[mask],
        )
        U_A[r_val, mask] = ua[0]
        U_B[r_val, mask] = ub[0]

    keep3 = list(range(3, 27))
    QA3, QB3 = QA3[:, keep3], QB3[:, keep3]
    CA3, CB3, hnz3, first3 = canon_rays_zw3(QA3, QB3)
    if not np.all(hnz3):
        raise AssertionError("T3 m=3: a stabilizer state lies inside V_3(T3)")
    _, cnt3_0 = np.unique(np.hstack([CA3, CB3]), axis=0, return_counts=True)
    if int(cnt3_0.max()) != 1:
        raise AssertionError("T3 m=3: two stabilizer states are collinear modulo V_3(T3)")

    reps_t3, _ = symmetry_orbit_reps_codes("T3", 3, codes3, ks3)
    if len(reps_t3) != 173:
        raise AssertionError(f"Expected 173 pivot orbits for T3 m=3, got {len(reps_t3)}")

    rng = np.random.default_rng(20261110)
    wA = rng.integers(1, 1 << 60, size=24, dtype=np.int64)
    wB = rng.integers(1, 1 << 60, size=24, dtype=np.int64)
    cand_groups = 0
    for piv in reps_t3:
        p = first3[piv]
        uA, uB = CA3[piv], CB3[piv]
        m = uA[p]
        alpha, beta = CA3[:, p:p + 1], CB3[:, p:p + 1]
        tA = m * CA3 - (alpha * uA - beta * uB)
        tB = m * CB3 - (alpha * uB + beta * (uA - uB))
        cA, cB, hnz_p, _ = canon_rays_zw3(tA, tB)
        if int(np.sum(~hnz_p)) != 1:
            raise AssertionError("T3 m=3: unexpected parallel pair off V_3(T3)")
        h = cA @ wA + cB @ wB
        order = np.argsort(h)
        hs = h[order]
        starts = np.concatenate(([0], np.flatnonzero(np.diff(hs) != 0) + 1, [len(hs)]))
        for idx_run in np.flatnonzero(np.diff(starts) >= 4):
            members = order[starts[idx_run]:starts[idx_run + 1]]
            if not (np.all(cA[members] == cA[members[0]]) and np.all(cB[members] == cB[members[0]])):
                _, sub_inv, sub_cnt = np.unique(np.hstack([cA[members], cB[members]]), axis=0, return_inverse=True, return_counts=True)
                groups = [members[sub_inv == g_id] for g_id in np.flatnonzero(sub_cnt >= 4)]
            else:
                groups = [members]
            for grp in groups:
                cand_groups += 1
                idx_all = np.concatenate(([piv], grp))
                r_base = zw3_rank(A3[idx_all], B3[idx_all])
                r_aug = zw3_rank(np.vstack([A3[idx_all], U_A]), np.vstack([B3[idx_all], U_B]))
                if r_aug == r_base:
                    raise AssertionError(f"T3 m=3: rank-5 decomposition found at pivot {piv}")
    if cand_groups == 0:
        raise AssertionError("T3 m=3: expected candidate lines of size >= 4 were not harvested")


def check_projection_monotonicity() -> None:
    """Verify symbolically that each qutrit state |psi> has a non-zero computational
    basis amplitude psi_x != 0 so (<x| (x) I^{ot (m-1)})|psi>^{ot m} = psi_x |psi>^{ot (m-1)},
    making chi(|psi>^{ot m}) >= chi(|psi>^{ot (m-1)}) exact."""
    s3 = sp.sqrt(3)
    w9 = sp.exp(2 * sp.pi * sp.I / 9)
    states = {
        "H3": (sp.Matrix([1 + s3, 1, 1]), 0),
        "N": (sp.Matrix([-1, 2, 2]), 0),
        "S": (sp.Matrix([0, 1, -1]), 1),
        "T3": (sp.Matrix([1, w9, w9 ** 2]), 0),
    }
    for name, (v, idx) in states.items():
        if sp.simplify(v[idx]) == 0:
            raise AssertionError(f"Projection coordinate {idx} vanishes for {name}")
        v2 = [v[a] * v[b] for a in range(3) for b in range(3)]
        sliced = sp.Matrix([v2[3 * idx + j] for j in range(3)])
        if sp.expand(sliced - v[idx] * v) != sp.zeros(3, 1):
            raise AssertionError(f"Symbolic slice identity failed for {name}")


def main() -> int:
    t0 = time.time()
    check_projection_monotonicity()
    codes2, ks2 = all_codes(2)
    A2, B2 = codes_to_zw3(codes2)
    codes3, ks3 = all_codes(3)
    A3, B3 = codes_to_zw3(codes3)

    verify_h3(codes2, A2, B2, codes3, A3, B3)
    verify_s_and_n(codes2, ks2, A2, B2, codes3, ks3, A3, B3)
    verify_t3(codes2, A2, B2, codes3, ks3, A3, B3)

    elapsed = time.time() - t0
    print(f"All exact Z[omega_3] qutrit checks passed in {elapsed:.2f}s")
    print("CERTIFIED chi(H3^2) >= 3")
    print("CERTIFIED chi(H3^3) >= 4")
    print("CERTIFIED chi(H3^4) >= 3")
    print("CERTIFIED chi(H3^4) >= 4")
    print("CERTIFIED chi(N^2) >= 3")
    print("CERTIFIED chi(N^3) >= 4")
    print("CERTIFIED chi(N^4) >= 3")
    print("CERTIFIED chi(N^4) >= 4")
    print("CERTIFIED chi(S^3) >= 4")
    print("CERTIFIED chi(S^4) >= 4")
    print("CERTIFIED chi(S^5) >= 4")
    print("CERTIFIED chi(T3^1) >= 3")
    print("CERTIFIED chi(T3^m) >= 3")
    print("CERTIFIED chi(T3^3) >= 6")
    print("CERTIFIED chi(T3^4) >= 6")
    print("CERTIFIED chi(T3^5) >= 6")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
