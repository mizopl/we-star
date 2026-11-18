"""Exact Z[i] certificate: chi(|CS>^{ot 4}) >= 5 via 4-qubit Clifford postselection.

Mathematical summary (zero floating-point operations, ~8 s warm / ~24 s cold with Numba JIT on 1 core):
1. Even-qubit (<0|_2 (I (x) H))^{ot 4} Clifford postselection:
   For |CS> = (|00> + |01> + |10> + i|11>) / 2, applying I (x) H and slicing
   the second qubit onto <0| gives (<0|_2 (I (x) H)) |CS> = (2 sqrt(2))^{-1} |Psi_1>
   with |Psi_1> = 2|0> + (1 + i)|1> in Z[i]^2 (verified symbolically against
   stabrank_verify.target_vector("CS", m) for m = 1, 4). Because local Clifford
   unitaries preserve stabilizer rank and <0| projections cannot increase it
   (Lean: IsStabP.slice / stabRankP_sliceP_le),
       chi(|CS>^{ot 4}) >= chi(|Psi_4>),   |Psi_m> = (2|0> + (1 + i)|1>)^{ot m}.
2. Exact tightness witness for |Psi_4> (chi(|Psi_4>) <= 5):
   Verified in exact Z[i]^16 arithmetic:
       |Psi_4> = (5+5i)(|0>+|1>)^{ot 4} + (5-5i)(|0>+i|1>)^{ot 4}
               + (3-i)(|0>-|1>)^{ot 4} + (3+i)(|0>-i|1>)^{ot 4} - 20|1111>.
3. Hadamard-certified exact modular rank & Pauli slice-and-lift (chi(|Psi_4>) >= 5):
   From cert_cs_m3_m4_exact.py, chi(|Psi_3>) = 4 on D_3 (1,080 three-qubit
   stabilizer states in Z[i]^8). Any rank-4 decomposition of |Psi_4> =
   |0> (x) 2|Psi_3> + |1> (x) (1+i)|Psi_3> slices at x_0 = 0 to a minimal rank-4
   decomposition sum_{r=1}^4 c_r u_r = 2|Psi_3> on D_3 and at x_0 = 1 to phased
   3-qubit Pauli translates sum_{r=1}^4 c_r mu_r P_r u_r = (1+i)|Psi_3> with
   mu_r in {1, i, -1, -i} and P_r among the 8 Pauli classes of u_r.
   At split prime P = 1,000,000,009 == 1 (mod 4), every 4 x 4 minor M of U in
   {0, +-1, +-i}^{8 x 4} has |det M| <= 2^4 = 16 (norm <= 256 < P), and after
   clearing Delta = det(U_piv) in Cramer's rule, |d_r| <= 2^3 * ||2|Psi_3>_piv||_2
   < 8 * 29.4 < 236, so each coordinate of sum_r d_r mu_r P_r u_r - (1+i) Delta |Psi_3>
   in Z[i] has modulus < 4*236 + sqrt(2)*16*8 < 1,126 and algebraic norm
   < 1,268,000 << P (the 2,000,000 check in `main()` is a conservative sanity
   ceiling not otherwise used by the code). Exhaustive S_3-reduced enumeration
   of all minimal rank-4 decompositions of |Psi_3> on D_3 (2,297 orbit-filtered
   quadruples across 270 S_3 pivot orbits — a count depending on the `E3`
   dictionary ordering and the `orb_s3[j] >= i` representative filter — after
   re-verifying 0 rank <= 3 decompositions) followed by exact 32^2 x 32^2
   meet-in-the-middle Pauli matching mod P finds 0 lifts (with positive controls
   on both |Psi_3> rank-4 recovery and a synthetic 4-term Pauli-lifted state).

Printed claim:
  CERTIFIED chi(CS^4) >= 5
"""

from __future__ import annotations

import itertools
import os
import sys
import time

for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS", "NUMEXPR_NUM_THREADS"):
    os.environ.setdefault(_v, "1")

import numpy as np
from numba import njit, int64, uint64
import sympy as sp

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import cert_cs_m3_m4_exact as cs_base  # noqa: E402
from stabrank_verify import target_vector  # noqa: E402

P = 1_000_000_009  # Prime == 1 (mod 4); exceeds Cramer/Hadamard norm bound < 2,000,000


def verify_symbolic_cs4_postselection_and_rank5_witness() -> None:
    """Symbolically verify (<0|_2 (I (x) H))^{ot m} |CS>^{ot m} = (2 sqrt(2))^{-m} |Psi_m>
    for m = 1 and m = 4 against stabrank_verify.target_vector, plus the explicit
    5-term Z[i]^16 decomposition of |Psi_4>."""
    inv_r2 = 1 / sp.sqrt(2)
    IH = sp.Matrix([
        [inv_r2, inv_r2, 0, 0],
        [inv_r2, -inv_r2, 0, 0],
        [0, 0, inv_r2, inv_r2],
        [0, 0, inv_r2, -inv_r2],
    ])
    cs1 = target_vector("CS", 1)
    rot1 = IH * cs1
    proj1 = sp.Matrix([sp.simplify(rot1[0]), sp.simplify(rot1[2])])
    psi1 = sp.Matrix([2, 1 + sp.I])
    if sp.simplify(proj1[0] * psi1[1] - proj1[1] * psi1[0]) != 0:
        raise AssertionError("2x2 minor mismatch for (<0|_2 (I (x) H))|CS>")
    for j in range(2):
        if sp.simplify(proj1[j] - psi1[j] / (2 * sp.sqrt(2))) != 0:
            raise AssertionError("Exact scale mismatch for (<0|_2 (I (x) H))|CS>")

    # Verify m = 4 postselection directly on target_vector("CS", 4) (256 amplitudes -> 16 amplitudes)
    cs4 = target_vector("CS", 4)
    # Applying (<0|_2 (I (x) H)) to each 2-qubit block (x_{2q}, x_{2q+1}) sums over x_{2q+1} in {0,1} with factor 2^{-1/2}
    psi4_ref = sp.Matrix(sp.kronecker_product(
        sp.kronecker_product(psi1, psi1),
        sp.kronecker_product(psi1, psi1),
    ))
    scale4 = sp.Integer(1) / sp.Integer(64)  # (2 sqrt(2))^{-4} = 1 / 64
    for mask4 in range(16):
        acc = sp.Integer(0)
        for even_bits in range(16):
            idx8 = 0
            for q in range(4):
                b_odd = (mask4 >> (3 - q)) & 1
                b_even = (even_bits >> (3 - q)) & 1
                idx8 = (idx8 << 2) | (b_odd << 1) | b_even
            acc += cs4[idx8]
        acc = sp.simplify(acc / sp.Integer(4))  # (2^{-1/2})^4 = 1/4 from H^{ot 4}
        if sp.simplify(acc - scale4 * psi4_ref[mask4]) != 0:
            raise AssertionError(f"Symbolic CS^4 postselection mismatch at mask {mask4}")

    # Verify explicit 5-term Z[i]^16 decomposition of |Psi_4>
    coeffs5 = [5 + 5 * sp.I, 5 - 5 * sp.I, 3 - sp.I, 3 + sp.I]
    recon = sp.zeros(16, 1)
    for k in range(4):
        uk = sp.Matrix([1, sp.I ** k])
        uk4 = sp.Matrix(sp.kronecker_product(
            sp.kronecker_product(uk, uk),
            sp.kronecker_product(uk, uk),
        ))
        recon += coeffs5[k] * uk4
    e_1111 = sp.zeros(16, 1)
    e_1111[15] = 1
    recon -= 20 * e_1111
    for j in range(16):
        if sp.simplify(recon[j] - psi4_ref[j]) != 0:
            raise AssertionError(f"Explicit rank-5 witness for |Psi_4> failed at index {j}")


@njit(cache=True)
def _mod_inv(a: int64, p: int64) -> int64:
    t, newt = int64(0), int64(1)
    r, newr = p, a % p
    while newr != 0:
        q = r // newr
        t, newt = newt, t - q * newt
        r, newr = newr, r - q * newr
    if t < 0:
        t += p
    return t


@njit(cache=True)
def _solve_and_test_lift(
    tup: np.ndarray,
    D3p: np.ndarray,
    pauli_D3p: np.ndarray,
    t0_vec: np.ndarray,
    t1_vec: np.ndarray,
    im_p: int64,
    p: int64,
) -> int64:
    """Solve D3p[tup]^T * c = t0_vec mod p; return -1 if non-minimal/not in span,
    else return number of 32^4 Pauli-phase solutions to sum c_r mu_r P_r u_r = t1_vec."""
    A = np.empty((8, 5), dtype=np.int64)
    for r in range(8):
        for c in range(4):
            A[r, c] = D3p[tup[c], r]
        A[r, 4] = t0_vec[r] % p
    row = 0
    for col in range(4):
        piv = -1
        for i in range(row, 8):
            if A[i, col] != 0:
                piv = i
                break
        if piv < 0:
            return int64(-1)
        if piv != row:
            for c in range(5):
                tmp = A[row, c]
                A[row, c] = A[piv, c]
                A[piv, c] = tmp
        inv = _mod_inv(A[row, col], p)
        for c in range(col, 5):
            A[row, c] = (A[row, c] * inv) % p
        for i in range(8):
            if i != row and A[i, col] != 0:
                fac = A[i, col]
                for c in range(col, 5):
                    v = (A[i, c] - fac * A[row, c]) % p
                    if v < 0:
                        v += p
                    A[i, c] = v
        row += 1
    for i in range(4, 8):
        if A[i, 4] != 0:
            return int64(-1)
    coeffs = np.empty(4, dtype=np.int64)
    for c in range(4):
        if A[c, 4] == 0:
            return int64(-1)
        coeffs[c] = A[c, 4]

    ph4 = np.array([int64(1), im_p, p - int64(1), p - im_p], dtype=np.int64)
    opts = np.empty((4, 32, 8), dtype=np.int64)
    for r in range(4):
        cr = coeffs[r]
        for pi_idx in range(8):
            for m_idx in range(4):
                sc = (cr * ph4[m_idx]) % p
                for d in range(8):
                    opts[r, pi_idx * 4 + m_idx, d] = (sc * pauli_D3p[tup[r], pi_idx, d]) % p

    TSIZE = 4096
    TMASK = 4095
    tkey = np.zeros(TSIZE, dtype=np.uint64)
    tused = np.zeros(TSIZE, dtype=np.int8)
    l_vecs = np.empty((1024, 8), dtype=np.int64)
    tidx = np.full(TSIZE, -1, dtype=np.int64)
    tnext = np.full(1024, -1, dtype=np.int64)

    for a in range(32):
        for b in range(32):
            idx = a * 32 + b
            h = uint64(0x51ED270B27C6D0F5)
            for d in range(8):
                v = opts[0, a, d] + opts[1, b, d]
                if v >= p:
                    v -= p
                l_vecs[idx, d] = v
                h = (h ^ uint64(v)) * uint64(0x9E3779B97F4A7C15)
            h ^= (h >> uint64(32))
            slot = int64(h & uint64(TMASK))
            while tused[slot] != 0 and tkey[slot] != h:
                slot = (slot + 1) & TMASK
            if tused[slot] == 0:
                tused[slot] = 1
                tkey[slot] = h
            tnext[idx] = tidx[slot]
            tidx[slot] = idx

    hits = int64(0)
    for a in range(32):
        for b in range(32):
            h = uint64(0x51ED270B27C6D0F5)
            need = np.empty(8, dtype=np.int64)
            for d in range(8):
                v = (t1_vec[d] - opts[2, a, d] - opts[3, b, d]) % p
                if v < 0:
                    v += p
                need[d] = v
                h = (h ^ uint64(v)) * uint64(0x9E3779B97F4A7C15)
            h ^= (h >> uint64(32))
            slot = int64(h & uint64(TMASK))
            while tused[slot] != 0:
                if tkey[slot] == h:
                    cur = tidx[slot]
                    while cur != -1:
                        eq = True
                        for d in range(8):
                            if l_vecs[cur, d] != need[d]:
                                eq = False
                                break
                        if eq:
                            hits += 1
                        cur = tnext[cur]
                    break
                slot = (slot + 1) & TMASK
    return hits


@njit(cache=True)
def _enum_and_lift_all_p(
    Q1p: np.ndarray,
    reps: np.ndarray,
    orb_s3: np.ndarray,
    D3p: np.ndarray,
    pauli_D3p: np.ndarray,
    t0_vec: np.ndarray,
    t1_vec: np.ndarray,
    im_p: int64,
    p: int64,
) -> tuple[int64, int64, int64]:
    """Exact full-dimension mod-P 2-pivot enumeration over S_3 pivot representatives.
    Because P = 1,000,000,009 > 256 (Hadamard minor norm bound on D_3), Q1p has
    zero projection loss and zero modular rank drops."""
    N = Q1p.shape[0]
    TSIZE = 1 << 13
    TMASK = TSIZE - 1
    tkey = np.zeros(TSIZE, dtype=np.uint64)
    tval = np.full(TSIZE, -1, dtype=np.int64)
    tnext = np.full(N, -1, dtype=np.int64)
    tstamp = np.zeros(TSIZE, dtype=np.int64)
    stamp = int64(0)
    n_r3 = int64(0)
    n_r4 = int64(0)
    n_lifts = int64(0)
    tup = np.empty(4, dtype=np.int64)

    for idx_r in range(len(reps)):
        i = reps[idx_r]
        ui = Q1p[i]
        c0 = -1
        for d in range(7):
            if ui[d] != 0:
                c0 = d
                break
        if c0 < 0:
            return int64(1), int64(0), int64(0)
        ia = _mod_inv(ui[c0], p)
        Q2 = np.empty((N, 6), dtype=np.int64)
        for k in range(N):
            s = (Q1p[k, c0] * ia) % p
            col = 0
            for d in range(7):
                if d == c0:
                    continue
                v = (Q1p[k, d] - s * ui[d]) % p
                if v < 0:
                    v += p
                Q2[k, col] = v
                col += 1
        for j in range(N):
            if j == i or orb_s3[j] < i:
                continue
            vj = Q2[j]
            c1 = -1
            for d in range(6):
                if vj[d] != 0:
                    c1 = d
                    break
            if c1 < 0:
                n_r3 += 1
                continue
            ib = _mod_inv(vj[c1], p)
            stamp += 1
            for k in range(j + 1, N):
                if k == i or orb_s3[k] < i:
                    continue
                s = (Q2[k, c1] * ib) % p
                w = np.empty(5, dtype=np.int64)
                col = 0
                lead = -1
                for d in range(6):
                    if d == c1:
                        continue
                    val = (Q2[k, d] - s * vj[d]) % p
                    if val < 0:
                        val += p
                    w[col] = val
                    if lead < 0 and val != 0:
                        lead = col
                    col += 1
                if lead < 0:
                    # Either {s_i, s_j, s_k} is linearly dependent or spans Psi_3
                    # Test whether Psi_3 lies in span(s_i, s_j, s_k) by checking if
                    # D3p[{i,j,k}] has rank 2 (dependent) vs rank 3 (rank-3 decomposition!)
                    # Quick rank check on 3x8 matrix D3p[{i, j, k}]:
                    M3 = np.empty((3, 8), dtype=np.int64)
                    for d in range(8):
                        M3[0, d] = D3p[i, d]
                        M3[1, d] = D3p[j, d]
                        M3[2, d] = D3p[k, d]
                    rk3 = 0
                    for col3 in range(8):
                        if rk3 == 3:
                            break
                        pv = -1
                        for r3 in range(rk3, 3):
                            if M3[r3, col3] != 0:
                                pv = r3
                                break
                        if pv < 0:
                            continue
                        if pv != rk3:
                            for d in range(8):
                                tmp = M3[rk3, d]; M3[rk3, d] = M3[pv, d]; M3[pv, d] = tmp
                        inv3 = _mod_inv(M3[rk3, col3], p)
                        for d in range(col3, 8):
                            M3[rk3, d] = (M3[rk3, d] * inv3) % p
                        for r3 in range(rk3 + 1, 3):
                            if M3[r3, col3] != 0:
                                f3 = M3[r3, col3]
                                for d in range(col3, 8):
                                    vv = (M3[r3, d] - f3 * M3[rk3, d]) % p
                                    if vv < 0:
                                        vv += p
                                    M3[r3, d] = vv
                        rk3 += 1
                    if rk3 == 3:
                        n_r3 += 1
                    continue
                iw = _mod_inv(w[lead], p)
                h = uint64(lead + 1)
                for d in range(5):
                    h = (h * uint64(1000000033)) ^ uint64((w[d] * iw) % p)
                h = (h ^ (h >> uint64(32))) * uint64(0x9E3779B97F4A7C15)
                h ^= (h >> uint64(32))
                slot = int64(h & uint64(TMASK))
                while True:
                    if tstamp[slot] != stamp:
                        tstamp[slot] = stamp
                        tkey[slot] = h
                        tval[slot] = k
                        tnext[k] = -1
                        break
                    if tkey[slot] == h:
                        cur = tval[slot]
                        while cur != -1:
                            # Confirm exact proportionality of w(cur) and w(k) in all 5 coords
                            tup[0] = i
                            tup[1] = j
                            tup[2] = cur
                            tup[3] = k
                            res = _solve_and_test_lift(tup, D3p, pauli_D3p, t0_vec, t1_vec, im_p, p)
                            if res >= 0:
                                n_r4 += 1
                                n_lifts += res
                            cur = tnext[cur]
                        tnext[k] = tval[slot]
                        tval[slot] = k
                        break
                    slot = (slot + 1) & TMASK
    return n_r3, n_r4, n_lifts


def main() -> int:
    t0 = time.time()
    if not sp.isprime(P) or (P - 1) % 4 != 0:
        raise AssertionError(f"P = {P} is not a prime congruent to 1 mod 4")
    if P <= 2_000_000:
        raise AssertionError(f"P = {P} does not exceed Cramer/Hadamard norm bound 2,000,000")

    verify_symbolic_cs4_postselection_and_rank5_witness()

    im_p = 0
    for g in range(2, 200):
        cand = pow(g, (P - 1) // 4, P)
        if (cand * cand) % P == P - 1:
            im_p = cand
            break
    if im_p == 0:
        raise AssertionError("Failed to find square root of -1 mod P")

    E3 = cs_base.stabilizer_exponents(3)
    D3p = np.array([0, 1, im_p, P - 1, P - im_p], dtype=np.int64)[E3 + 1]

    # Build exact 8-element Pauli class table on D_3 over F_P
    digs3 = np.array(list(itertools.product((0, 1), repeat=3)), dtype=np.int64)
    w3b = np.array([4, 2, 1], dtype=np.int64)
    pauli_D3p = np.empty((1080, 8, 8), dtype=np.int64)
    for s in range(1080):
        u = D3p[s]
        seen = {}
        out = []
        for a in range(8):
            abits = digs3[a]
            dst = (digs3 ^ abits[None, :]) @ w3b
            for c in range(8):
                cbits = digs3[c]
                ph = (digs3 @ cbits) % 2
                qu = np.zeros(8, dtype=np.int64)
                qu[dst] = np.where(ph == 0, u, (P - u) % P)
                nz = np.flatnonzero(qu)
                f = int(nz[0])
                canon = (qu * pow(int(qu[f]), P - 2, P)) % P
                key = canon.tobytes()
                if key not in seen:
                    seen[key] = True
                    out.append(canon)
        if len(out) != 8:
            raise AssertionError(f"Expected 8 Pauli classes for state {s}, got {len(out)}")
        pauli_D3p[s] = np.stack(out)

    # Exact S_3 copy-permutation symmetry on D_3 (unitary, preserves slices along qubit 0)
    row_map = {E3[i].tobytes(): i for i in range(1080)}
    perms_s3 = []
    for p_perm in itertools.permutations(range(3)):
        dst = digs3[:, p_perm] @ w3b
        M = E3[:, dst].copy()
        f = np.argmax(M >= 0, axis=1)
        ref = M[np.arange(1080), f][:, None]
        M = np.where(M >= 0, (M - ref) % 4, -1).astype(np.int8)
        perms_s3.append([row_map[M[i].tobytes()] for i in range(1080)])
    perms_s3_arr = np.array(perms_s3, dtype=np.int64)
    orb_s3 = np.min(perms_s3_arr, axis=0)
    reps_s3 = np.unique(orb_s3)

    p1p = np.array([2, (1 + im_p) % P], dtype=np.int64)
    p3p = np.kron(np.kron(p1p, p1p), p1p) % P
    p3pn = (p3p * pow(int(p3p[0]), P - 2, P)) % P
    Q1p = (D3p[:, 1:] - np.outer(D3p[:, 0], p3pn[1:])) % P

    t0_vec = (2 * p3p) % P
    t1_vec = ((1 + im_p) * p3p) % P

    # Positive control: symmetric 4-tuple {(|0> + i^k |1>)^3}_{k=0..3} lifts when slice 1 is
    # sum_k c_k (|0> + i^k |1>)^3 = t0_vec (since (|0>+|1>) (x) u_k has identical slices!)
    sym4_indices = []
    for k_ph in range(4):
        u1 = np.array([0, k_ph], dtype=np.int8)
        e_vec = np.array([(u1[b0] + u1[b1] + u1[b2]) % 4 for b0, b1, b2 in digs3], dtype=np.int8)
        sym4_indices.append(row_map[e_vec.tobytes()])
    sym4_tup = np.array(sorted(sym4_indices), dtype=np.int64)
    ctrl_hits = int(_solve_and_test_lift(sym4_tup, D3p, pauli_D3p, t0_vec, t0_vec, int64(im_p), int64(P)))
    if ctrl_hits <= 0:
        raise AssertionError("Positive control failed: symmetric rank-4 tuple did not lift on |+> (x) |Psi_3>")

    n_r3, n_r4, n_lifts = _enum_and_lift_all_p(
        Q1p, reps_s3, orb_s3, D3p, pauli_D3p, t0_vec, t1_vec, int64(im_p), int64(P)
    )
    if n_r3 != 0:
        raise AssertionError(f"Unexpected rank <= 3 decomposition of |Psi_3>: {n_r3}")
    if n_r4 <= 0:
        raise AssertionError("Failed to recover the rank-4 decompositions of |Psi_3>")
    if n_lifts != 0:
        print(f"SLICE-1 LIFT FOUND FOR |Psi_4|: {n_lifts}", file=sys.stderr)
        return 1

    print(
        f"exact Z[i] / F_P check (P={P}): {len(reps_s3)} S_3 pivot orbits on D_3, "
        f"{int(n_r4)} minimal rank-4 tuples tested, 0 Pauli lifts to |Psi_4>, "
        f"chi(|Psi_4>) = 5 [{time.time() - t0:.2f}s]"
    )
    print("CERTIFIED chi(CS^4) >= 5")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
