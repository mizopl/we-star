"""Exact Z[omega_3, sqrt(3)] certificate: chi(|H3>^{ot m}) >= 5 for m = 4, 5, 6.

Upgrades H3 m = 4 from `reproduced` (1,183 s floating-point 2-pivot search in
`cert_h3_m4_lift.py`) to `verified` (`exact: true`) in ~4 seconds on 1 core,
and lifts chi >= 5 to m = 5, 6 by exact projection monotonicity.

Key mathematical & algorithmic guarantees (zero floating-point operations):
1. 2D tau-Galois target plane cuts m = 3 rank-4 search from 2 pivots to 1 pivot:
   Unnormalised |H3> proportional to h = (1 + sqrt(3), 1, 1)^T lies in
   Z[sqrt(3)]^3, whereas every qutrit stabilizer state lies in Z[omega_3]^{3^m}.
   Since [Q(omega_3, sqrt(3)) : Q(omega_3)] = 2 with Galois automorphism
   tau(sqrt(3)) = -sqrt(3), tau(omega_3) = omega_3, any Q(omega_3)-span of
   stabilizer states containing h^{ot 3} must contain the 2D Q(omega_3)-plane
   V_3(H3) = span(v_0, v_1). Modulo V_3(H3), a 4-state decomposition spans at
   most 4 - 2 = 2 dimensions, so fixing a single pivot reduces the quotient to
   dimension <= 1 (exact ray hashing across 116 symmetry pivot orbits).
2. Hadamard algebraic norm certificate at split prime P = 1,000,000,021:
   In Q(omega_3) (degree 2 over Q), every 6 x 6 minor formed by 4 stabilizer
   row segments in {0, 1, omega_3, omega_3^2}^6 (squared Euclidean norm <= 6)
   and the 6-column segments of (v_0, v_1) (full squared norms 48 and 72)
   satisfies
       N_{Q(omega_3)/Q}(det M) = |det M|^2 <= 6^4 * 48 * 72 = 4,478,976 < P.
   Every surviving 4-tuple is also confirmed over Z via the exact 2k x 2d
   regular representation in SymPy.
3. Exact Z[omega_3, sqrt(3)] meet-in-the-middle Pauli slice lift at m = 4:
   Up to the order-384 symmetry group of |H3>^{ot 3} (with explicit complex
   conjugate closure so all unitary orbits are covered without assuming
   antiunitary slice invariance), |H3>^{ot 3} has a unique rank-4 decomposition
   orbit. Solving the exact slice-0 equation (1 + sqrt(3)) h^{ot 3} = sum c_r u_r
   in SymPy over Q(omega_3, sqrt(3)) determines c_1..c_4 uniquely, and exact
   integer meet-in-the-middle over all 81^2 x 81^2 Pauli-and-phase slice-1
   assignments proves 0 solutions exist (with positive control on |S>^2).

Printed claims:
  CERTIFIED chi(H3^4) >= 5
  CERTIFIED chi(H3^5) >= 5
  CERTIFIED chi(H3^6) >= 5
"""

from __future__ import annotations

import itertools
import os
import sys
import time

for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS", "NUMEXPR_NUM_THREADS"):
    os.environ.setdefault(_v, "1")

import numpy as np
import sympy as sp

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from qutrit_codes import all_codes  # noqa: E402
from rank_exclusion_codes import CodeIndex  # noqa: E402
from stabrank_verify import orbit_state, target_vector  # noqa: E402

P = 1_000_000_021
LUT_A = np.array([0, 1, 0, -1], dtype=np.int64)
LUT_B = np.array([0, 0, 1, -1], dtype=np.int64)


def codes_to_zw3(codes: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    return LUT_A[codes + 1], LUT_B[codes + 1]


def zw3_rank(M_A: np.ndarray, M_B: np.ndarray) -> int:
    top = np.hstack([M_A, M_B])
    bot = np.hstack([-M_B, M_A - M_B])
    r2 = int(sp.Matrix(np.vstack([top, bot]).tolist()).rank())
    if r2 % 2 != 0:
        raise AssertionError(f"Odd Q-rank {r2} for Q(omega_3)-matrix")
    return r2 // 2


def rank_mod_p(M: np.ndarray, mod: int = P) -> int:
    A = (M % mod).astype(np.int64, copy=True)
    m, n = A.shape
    r = 0
    for c in range(n):
        if r == m:
            break
        piv = -1
        for i in range(r, m):
            if A[i, c] != 0:
                piv = i
                break
        if piv < 0:
            continue
        if piv != r:
            A[[r, piv]] = A[[piv, r]]
        inv = pow(int(A[r, c]), mod - 2, mod)
        A[r] = (A[r] * inv) % mod
        for i in range(r + 1, m):
            if A[i, c] != 0:
                A[i] = (A[i] - A[i, c] * A[r]) % mod
        r += 1
    return r


def exact_pauli_classes_zw3(uA: np.ndarray, uB: np.ndarray, m: int) -> list[tuple[np.ndarray, np.ndarray]]:
    """Return the exact 3^m distinct projective Pauli images Q u = X^a Z^c u in
    Z[omega_3]^{3^m} (canonicalised by first non-zero entry)."""
    dim = 3 ** m
    digs = np.array(list(itertools.product(range(3), repeat=m)), dtype=np.int64)
    powers = 3 ** np.arange(m - 1, -1, -1, dtype=np.int64)
    seen = {}
    out = []
    for a in itertools.product(range(3), repeat=m):
        dst = ((digs + np.array(a, dtype=np.int64)) % 3) @ powers
        for c in itertools.product(range(3), repeat=m):
            ph = (digs @ np.array(c, dtype=np.int64)) % 3
            za = np.where(ph == 0, uA, np.where(ph == 1, -uB, uB - uA))
            zb = np.where(ph == 0, uB, np.where(ph == 1, uA - uB, -uA))
            qa = np.zeros(dim, dtype=np.int64)
            qb = np.zeros(dim, dtype=np.int64)
            qa[dst] = za
            qb[dst] = zb
            nz = np.flatnonzero((qa != 0) | (qb != 0))
            f = int(nz[0])
            a0, b0 = int(qa[f]), int(qb[f])
            ca = qa * (a0 - b0) + qb * b0
            cb = qb * a0 - qa * b0
            g = int(np.gcd.reduce(np.concatenate([ca, cb])))
            key = (ca // g).tobytes() + (cb // g).tobytes()
            if key not in seen:
                seen[key] = True
                out.append((qa, qb))
    if len(out) != 3 ** m:
        raise AssertionError(f"Expected {3**m} Pauli images on {m} qutrits, got {len(out)}")
    return out


def mul_zw3_s3(
    c_vals: tuple[int, int, int, int], uA: np.ndarray, uB: np.ndarray, w3_pow: int
) -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    """Multiply scalar c = c0 + c1*w3 + c2*s3 + c3*w3*s3 by w3^{w3_pow} * (uA + uB*w3)
    in the Z-basis {1, w3, s3, w3*s3}."""
    if w3_pow == 0:
        xA, xB = uA, uB
    elif w3_pow == 1:
        xA, xB = -uB, uA - uB
    else:
        xA, xB = uB - uA, -uA
    c0, c1, c2, c3 = c_vals
    r0 = c0 * xA - c1 * xB
    r1 = c0 * xB + c1 * xA - c1 * xB
    r2 = c2 * xA - c3 * xB
    r3 = c2 * xB + c3 * xA - c3 * xB
    return r0, r1, r2, r3


def verify_symbolic_h3_and_controls() -> None:
    """Symbolic 2x2-minor projective checks against stabrank_verify.orbit_state
    and target_vector, plus exact Z[omega_3] positive control on |S>^2."""
    s3 = sp.sqrt(3)
    h_exact = orbit_state("H3")
    h_ref = sp.Matrix([1 + s3, 1, 1])
    for a in range(3):
        for b in range(a + 1, 3):
            minor = sp.simplify(sp.expand(h_exact[a] * h_ref[b] - h_exact[b] * h_ref[a]))
            if minor != 0:
                raise AssertionError(f"2x2 minor ({a},{b}) mismatch against orbit_state('H3'): {minor}")
    if sp.simplify(h_exact[0]) == 0:
        raise AssertionError("Symbolic <0|H3> == 0")

    h2_exact = target_vector("H3", 2)
    h2_ref = sp.Matrix(sp.kronecker_product(h_ref, h_ref))
    for j in range(1, 9):
        minor = sp.simplify(sp.expand(h2_exact[0] * h2_ref[j] - h2_exact[j] * h2_ref[0]))
        if minor != 0:
            raise AssertionError(f"2x2 minor (0,{j}) mismatch against target_vector('H3', 2)")
    # Verify computational slice (<0| (x) I)|H3>^2 = <0|H3> * |H3>
    for j in range(3):
        if sp.simplify(h2_exact[j] - h_exact[0] * h_exact[j]) != 0:
            raise AssertionError(f"Slice (<0| (x) I)|H3>^2 mismatch at {j}")

    # Positive control: |S>^2 = (0, 0, 0, 0, 1, -1, 0, -1, 1) has rank-2 decompositions in D_2
    codes2, _ = all_codes(2)
    A2, B2 = codes_to_zw3(codes2)
    s2 = np.array([0, 0, 0, 0, 1, -1, 0, -1, 1], dtype=np.int64)
    QA = A2 - A2[:, 4:5] * s2[None, :]
    QB = B2 - B2[:, 4:5] * s2[None, :]
    keep = [j for j in range(9) if j != 4]
    QA, QB = QA[:, keep], QB[:, keep]
    nz = (QA != 0) | (QB != 0)
    f = np.argmax(nz, axis=1)
    a0 = QA[np.arange(len(QA)), f][:, None]
    b0 = QB[np.arange(len(QB)), f][:, None]
    ca = QA * (a0 - b0) + QB * b0
    cb = QB * a0 - QA * b0
    g = np.gcd(np.gcd.reduce(ca, axis=1), np.gcd.reduce(cb, axis=1))[:, None]
    g = np.where(g == 0, 1, g)
    _, cnt = np.unique(np.hstack([ca // g, cb // g]), axis=0, return_counts=True)
    if int(np.sum(cnt >= 2)) == 0:
        raise AssertionError("Positive control failed: rank-2 decomposition of |S>^2 not found")


def test_h3_m4_lift_exact(tup: tuple[int, int, int, int], A3: np.ndarray, B3: np.ndarray) -> int:
    """Exact integer meet-in-the-middle test of whether the 3-qutrit rank-4 basis
    `tup` lifts to |H3>^4 on slices x_0 = 0, 1, 2."""
    digs3 = np.array([[(i // 9) % 3, (i // 3) % 3, i % 3] for i in range(27)], dtype=np.int64)
    kz3 = np.sum(digs3 == 0, axis=1)
    h_int = np.array([1, 1, 4, 10], dtype=np.int64)[kz3]
    h_s3 = np.array([0, 1, 2, 6], dtype=np.int64)[kz3]

    t0_int = h_int + 3 * h_s3
    t0_s3 = h_int + h_s3

    U_A = A3[list(tup)]
    U_B = B3[list(tup)]
    M_top = np.hstack([U_A.T, -U_B.T])
    M_bot = np.hstack([U_B.T, (U_A - U_B).T])
    M_sys = sp.Matrix(np.vstack([M_top, M_bot]).tolist())
    rhs_int = sp.Matrix(list(t0_int) + [0] * 27)
    rhs_s3 = sp.Matrix(list(t0_s3) + [0] * 27)

    sol_ab, params1 = M_sys.gauss_jordan_solve(rhs_int)
    sol_gd, params2 = M_sys.gauss_jordan_solve(rhs_s3)
    if len(params1) != 0 or len(params2) != 0:
        raise AssertionError("Rank-4 basis is not linearly independent in exact solve")

    rat_list = list(sol_ab) + list(sol_gd)
    den_lcm = 1
    for q in rat_list:
        den_lcm = int(sp.ilcm(den_lcm, sp.denom(q)))
    ab_int = [int(q * den_lcm) for q in sol_ab]
    gd_int = [int(q * den_lcm) for q in sol_gd]

    coeffs = []
    for r in range(4):
        c_tup = (ab_int[r], ab_int[r + 4], gd_int[r], gd_int[r + 4])
        if c_tup == (0, 0, 0, 0):
            raise AssertionError("Zero coefficient in minimal rank-4 decomposition")
        coeffs.append(c_tup)

    acc0 = [np.zeros(27, dtype=np.int64) for _ in range(4)]
    for r in range(4):
        v0, v1, v2, v3 = mul_zw3_s3(coeffs[r], U_A[r], U_B[r], 0)
        acc0[0] += v0; acc0[1] += v1; acc0[2] += v2; acc0[3] += v3
    if not (np.array_equal(acc0[0], den_lcm * t0_int) and np.all(acc0[1] == 0)
            and np.array_equal(acc0[2], den_lcm * t0_s3) and np.all(acc0[3] == 0)):
        raise AssertionError("Exact slice-0 reconstruction check failed")

    tgt1 = (
        den_lcm * h_int,
        np.zeros(27, dtype=np.int64),
        den_lcm * h_s3,
        np.zeros(27, dtype=np.int64),
    )

    opts = []
    for r in range(4):
        paulis = exact_pauli_classes_zw3(U_A[r], U_B[r], 3)
        r_vecs = []
        for qa, qb in paulis:
            for e_ph in (0, 1, 2):
                v0, v1, v2, v3 = mul_zw3_s3(coeffs[r], qa, qb, e_ph)
                r_vecs.append(np.concatenate([v0, v1, v2, v3]))
        opts.append(np.stack(r_vecs))

    target_flat = np.concatenate(tgt1)
    L_sums = (opts[0][:, None, :] + opts[1][None, :, :]).reshape(-1, 108)
    R_need = (target_flat[None, None, :] - opts[2][:, None, :] - opts[3][None, :, :]).reshape(-1, 108)

    left_map: dict[bytes, list[int]] = {}
    for idx_l in range(len(L_sums)):
        b = L_sums[idx_l].tobytes()
        if b in left_map:
            left_map[b].append(idx_l)
        else:
            left_map[b] = [idx_l]

    # Positive control on the meet-in-the-middle lift table itself:
    # for (|0>+|1>+|2>) (x) |H3>^3, slice 1 equals slice 0 = den_lcm*(t0_int + t0_s3*s3),
    # which must admit >= 1 exact Pauli-and-phase match (the identity assignment).
    target_flat_0 = np.concatenate([
        den_lcm * t0_int, np.zeros(27, dtype=np.int64),
        den_lcm * t0_s3, np.zeros(27, dtype=np.int64),
    ])
    R_ctrl = (target_flat_0[None, None, :] - opts[2][:, None, :] - opts[3][None, :, :]).reshape(-1, 108)
    if sum(len(left_map[R_ctrl[idx_r].tobytes()]) for idx_r in range(len(R_ctrl)) if R_ctrl[idx_r].tobytes() in left_map) < 1:
        raise AssertionError("Positive control failed: (|0>+|1>+|2>) (x) |H3>^3 did not lift in left_map")

    slice1_matches = 0
    for idx_r in range(len(R_need)):
        b = R_need[idx_r].tobytes()
        if b in left_map:
            slice1_matches += len(left_map[b])
    return slice1_matches


def main() -> int:
    t0 = time.time()
    if not sp.isprime(P) or (P - 1) % 3 != 0:
        raise AssertionError(f"P = {P} is not a prime congruent to 1 mod 3")
    hadamard_sq = (6 ** 4) * 48 * 72  # 4,478,976
    if P <= hadamard_sq:
        raise AssertionError(f"P = {P} does not exceed Hadamard norm bound {hadamard_sq}")

    verify_symbolic_h3_and_controls()

    codes3, ks3 = all_codes(3)
    A3, B3 = codes_to_zw3(codes3)
    g = int(sp.primitive_root(P))
    w3 = pow(g, (P - 1) // 3, P)
    w3_lut = np.array([0, 1, w3, (w3 * w3) % P], dtype=np.int64)
    D3_mod = w3_lut[codes3 + 1]

    digs3 = np.array([[(i // 9) % 3, (i // 3) % 3, i % 3] for i in range(27)], dtype=np.int64)
    kz3 = np.sum(digs3 == 0, axis=1)
    v0_int = np.array([1, 0, 2, 4], dtype=np.int64)[kz3]
    v1_int = np.array([0, 1, 2, 6], dtype=np.int64)[kz3]
    if int(v0_int @ v0_int) != 48 or int(v1_int @ v1_int) != 72:
        raise AssertionError("Unexpected squared norms for V_3(H3) basis")

    v0 = v0_int % P
    v1 = v1_int % P
    V3_mod = np.vstack([v0, v1])
    keep = [j for j in range(27) if j not in (8, 26)]
    Q0 = (D3_mod[:, keep] - np.outer(D3_mod[:, 26], v0[keep]) - np.outer(D3_mod[:, 8], v1[keep])) % P

    nz0 = Q0 != 0
    if not np.all(np.any(nz0, axis=1)):
        raise AssertionError("Rank <= 2 state found in V_3(H3)")
    f0 = np.argmax(nz0, axis=1)
    lead0 = Q0[np.arange(len(Q0)), f0]
    pref0 = lead0.copy()
    for k in range(1, len(lead0)):
        pref0[k] = (pref0[k - 1] * int(lead0[k])) % P
    inv_all0 = pow(int(pref0[-1]), P - 2, P)
    invs0 = np.empty(len(lead0), dtype=np.int64)
    for k in range(len(lead0) - 1, 0, -1):
        invs0[k] = (inv_all0 * pref0[k - 1]) % P
        inv_all0 = (inv_all0 * int(lead0[k])) % P
    invs0[0] = inv_all0
    Q0_norm = (Q0 * invs0[:, None]) % P
    _, cnt0 = np.unique(Q0_norm, axis=0, return_counts=True)
    if int(cnt0.max()) != 1:
        raise AssertionError("Rank-3 decomposition candidate found modulo V_3(H3)")
    print("m=3 rank-3 excluded in 0 pivots modulo 2D Galois plane V_3(H3)")

    # Zero-float projective Clifford symmetry orbits of V_3(H3) on D_3 over F_P
    # <F_3> = {I, F_3, F_3^2, F_3^3} fixes span(h) (order 4 on each copy), plus S_3 and conjugation
    F3_scaled = (
        (1 - w3)
        * np.array([[pow(w3, (j * k) % 3, P) for k in range(3)] for j in range(3)], dtype=np.int64)
    ) % P
    code_index = CodeIndex(codes3)

    def local_f3_perm(G3: np.ndarray) -> np.ndarray:
        blocks = D3_mod.reshape(len(D3_mod), 3, 9)
        img_flat = (np.einsum("ab,nbj->naj", G3, blocks) % P).reshape(len(D3_mod), 27)
        nz = img_flat != 0
        f = np.argmax(nz, axis=1)
        lead = img_flat[np.arange(len(img_flat)), f]
        pref = lead.copy()
        for k in range(1, len(lead)):
            pref[k] = (pref[k - 1] * int(lead[k])) % P
        inv_acc = pow(int(pref[-1]), P - 2, P)
        invs = np.empty(len(lead), dtype=np.int64)
        for k in range(len(lead) - 1, 0, -1):
            invs[k] = (inv_acc * pref[k - 1]) % P
            inv_acc = (inv_acc * int(lead[k])) % P
        invs[0] = inv_acc
        canon_img = (img_flat * invs[:, None]) % P
        out_codes = np.full_like(codes3, -1)
        out_codes[canon_img == 1] = 0
        out_codes[canon_img == w3] = 1
        out_codes[canon_img == (w3 * w3) % P] = 2
        if not np.all((canon_img == 0) | (out_codes >= 0)):
            raise AssertionError("F_3 image entry outside {0, 1, w3, w3^2} mod P")
        return code_index.lookup(out_codes)

    def axis_perm(perm_axes: tuple[int, int, int]) -> np.ndarray:
        src = digs3[:, perm_axes] @ np.array([9, 3, 1], dtype=np.int64)
        prow = codes3[:, src].copy()
        f = np.argmax(prow >= 0, axis=1)
        ref = prow[np.arange(len(prow)), f][:, None]
        prow = np.where(prow >= 0, (prow - ref) % 3, -1).astype(np.int8)
        return code_index.lookup(prow)

    crow_all = np.where(codes3 >= 0, (-codes3) % 3, -1).astype(np.int8)
    fc_all = np.argmax(crow_all >= 0, axis=1)
    crow_all = np.where(crow_all >= 0, (crow_all - crow_all[np.arange(len(crow_all)), fc_all][:, None]) % 3, -1).astype(np.int8)
    perms_h3 = [
        local_f3_perm(F3_scaled),
        axis_perm((1, 0, 2)),
        axis_perm((1, 2, 0)),
        code_index.lookup(crow_all),
    ]
    inv_perms_h3 = [np.argsort(pm) for pm in perms_h3]
    labels_h3 = np.arange(len(codes3), dtype=np.int64)
    while True:
        new_lbl = labels_h3.copy()
        for pm, ip in zip(perms_h3, inv_perms_h3):
            new_lbl = np.minimum(new_lbl, new_lbl[pm])
            new_lbl = np.minimum(new_lbl, new_lbl[ip])
        if np.array_equal(new_lbl, labels_h3):
            break
        labels_h3 = new_lbl
    reps_h3 = np.unique(labels_h3)
    if len(reps_h3) != 116:
        raise AssertionError(f"Expected 116 symmetry orbits for H3 m=3, got {len(reps_h3)}")
    rng = np.random.default_rng(20261111)
    hw = rng.integers(1, P - 1, size=24, dtype=np.int64)

    true_r4: set[tuple[int, int, int, int]] = set()
    for piv in reps_h3:
        u = Q0[piv]
        c0 = int(np.flatnonzero(u)[0])
        un = (u * pow(int(u[c0]), P - 2, P)) % P
        cols = [j for j in range(25) if j != c0]
        W = (Q0[:, cols] - np.outer(Q0[:, c0], un[cols])) % P
        nz = W != 0
        active = np.flatnonzero(np.any(nz, axis=1))
        Wa = W[active]
        fa = np.argmax(nz[active], axis=1)
        lead = Wa[np.arange(len(active)), fa]
        pref = lead.copy()
        for k in range(1, len(lead)):
            pref[k] = (pref[k - 1] * int(lead[k])) % P
        inv_all = pow(int(pref[-1]), P - 2, P)
        invs = np.empty(len(lead), dtype=np.int64)
        for k in range(len(lead) - 1, 0, -1):
            invs[k] = (inv_all * pref[k - 1]) % P
            inv_all = (inv_all * int(lead[k])) % P
        invs[0] = inv_all
        h = (((Wa * invs[:, None]) % P) @ hw) % P
        order = np.argsort(h, kind="mergesort")
        hs = h[order]
        _, st_arr, cnt_arr = np.unique(hs, return_index=True, return_counts=True)
        for st, cnt in zip(st_arr[cnt_arr >= 3], cnt_arr[cnt_arr >= 3]):
            grp = active[order[st:st + cnt]]
            S_idx = [int(piv)] + [int(x) for x in grp]
            rkS = rank_mod_p(D3_mod[S_idx])
            if rkS >= 4 and rank_mod_p(np.vstack([D3_mod[S_idx], V3_mod])) == rkS:
                for sub3 in itertools.combinations([int(x) for x in grp], 3):
                    tup = tuple(sorted((int(piv), *sub3)))
                    if (rank_mod_p(D3_mod[list(tup)]) == 4
                            and rank_mod_p(np.vstack([D3_mod[list(tup)], V3_mod])) == 4):
                        V3_A = np.vstack([v0_int, v1_int])
                        V3_B = np.zeros_like(V3_A)
                        if (zw3_rank(A3[list(tup)], B3[list(tup)]) == 4
                                and zw3_rank(np.vstack([A3[list(tup)], V3_A]),
                                             np.vstack([B3[list(tup)], V3_B])) == 4):
                            true_r4.add(tup)

    if len(true_r4) == 0:
        raise AssertionError("Failed to find the known rank-4 decomposition of |H3>^3")

    code_map = {codes3[i].tobytes(): i for i in range(len(codes3))}
    unitary_reps: set[tuple[int, int, int, int]] = set(true_r4)
    for tup in list(true_r4):
        conj_tup = []
        for idx in tup:
            row = codes3[idx]
            crow = np.where(row >= 0, (-row) % 3, -1).astype(np.int8)
            nz_f = int(np.flatnonzero(crow >= 0)[0])
            ref = crow[nz_f]
            crow = np.where(crow >= 0, (crow - ref) % 3, -1).astype(np.int8)
            conj_tup.append(code_map[crow.tobytes()])
        unitary_reps.add(tuple(sorted(conj_tup)))

    for tup in sorted(unitary_reps):
        s1_hits = test_h3_m4_lift_exact(tup, A3, B3)
        if s1_hits != 0:
            print(f"SLICE-1 LIFT CANDIDATE FOUND for {tup}: {s1_hits}", file=sys.stderr)
            return 1

    print(f"exact H3 m=3->4 lift check: {len(true_r4)} antiunitary ({len(unitary_reps)} unitary) "
          f"rank-4 orbit(s) of |H3>^3, 0 exact Z[omega_3, sqrt(3)] slice-1 solutions "
          f"[{time.time() - t0:.2f}s]")
    for m in (4, 5, 6):
        print(f"CERTIFIED chi(H3^{m}) >= 5")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
