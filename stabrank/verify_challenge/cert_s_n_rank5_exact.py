"""Exact Z[omega_3] / Hadamard-prime certificate: chi(|S>^{ot m}) >= 5 (m = 5..8)
and chi(|N>^{ot m}) >= 5 (m = 4..6).

Upgrades all five remaining `reproduced` lower bounds on `S` and `N`
(`S-m{5,6,7,8}-lower-5.json` and `N-m4-lower-5.json`) to `verified` (`exact: true`,
zero floating-point operations anywhere in enumeration, symmetry, or slice-and-lift),
and adds `N-m5-lower-5.json` and `N-m6-lower-5.json` by projection monotonicity.

Mathematical guarantees (100% integer / Z[omega_3] / F_P arithmetic):
1. Symbolic projective & slice verification:
   Checks all 2 x 2 projective minors of unnormalised |S> = (0, 1, -1) and
   |N> = (1, 1, -2) (and their two-copy tensor squares) against
   `stabrank_verify.orbit_state` and `target_vector`, together with the slice
   identities (<1| (x) I)|S>^2 = 2^{-1/2}|S> and (<0| (x) I)|N>^2 = 6^{-1/2}|N>.
2. Zero-float projective Clifford symmetry group over F_P (P = 1,000,000,021):
   Since |(1 - omega_3)|^2 = (1 - omega_3)(1 - omega_3^2) = 3, the scaled Fourier
   gate (1 - omega_3) F_3 = ((1 - omega_3) omega_3^{j k})_{j,k=0}^2 is unitary up
   to scalar 3 and has entries in Z[omega_3]. Closing {X, diag(1, 1, omega_3),
   (1 - omega_3) F_3} projectively over F_P yields all 216 elements of C_1(3)/U(1),
   isolating the exact 24 local unitaries fixing |S> and 6 local unitaries fixing
   |N>, and acting on `all_codes(3)` (30,240 states) in exact Z[omega_3] arithmetic.
3. Exact 1-pivot rank-3 exclusion & 2-pivot rank-4 census on D_3:
   - At P = 1,000,000,021 == 1 (mod 3), Hadamard's bound on any k x k minor
     (k <= 5) with stabilizer rows in {0, 1, omega_3, omega_3^2} and target row
     |S>^3 (squared norm 8) or |N>^3 (squared norm 216) gives
         N_{Q(omega_3)/Q}(det M) <= 5^4 * 216 = 135,000 << P,
     so F_P-rank equals Q(omega_3)-rank on every <= 5-subset; surviving 4-tuples
     are additionally confirmed in SymPy over Z.
   - 1-pivot canonical ray bucketing (deterministic int64 matmul filter followed
     by exact `rank_mod_p` verification) proves chi(|S>^3) >= 4 and
     chi(|N>^3) >= 4 (with positive controls finding the rank-2 pairs of |S>^2
     and all 48 rank-3 triples of |N>^2), so every rank-4 decomposition at m = 3
     is minimal.
   - 2-pivot candidate harvest runs mod ell = 65521 == 1 (mod 3) in F_ell^6
     with Schreier stabilizer partner reduction; independence of candidate
     3-subsets and 4-subsets is checked on the full unprojected 27-column
     dictionary D_3 mod ell = 65521 (exact by Hadamard: 3 x 3 and 4 x 4
     stabilizer minors satisfy |det|^2 <= 3^3 = 27 and 4^4 = 256 < 65521, so
     zero valid rank-4 decompositions can be dropped by projection), with
     explicit verification that zero non-collinear quotient vectors vanish
     under the F_ell^6 projection, followed by complex-conjugate closure so all
     unitary orbits are covered without assuming antiunitary slice invariance.
4. Exact Z[omega_3] integer meet-in-the-middle Pauli slice-and-lift:
   - Positive control: the rank-2 decomposition {|1>, |2>} of |S> lifts to |S>^2.
   - Norrell (m = 3 -> 4): solving slice k = 1 (sum c_r u_r = |N>^3) in SymPy
     over Q(omega_3) and testing all 81^2 x 81^2 Pauli-and-phase assignments on
     slice k = 2 (-2 |N>^3) and slice k = 0 (+|N>^3) finds 0 lifts, proving
     chi(|N>^{ot m}) >= 5 for m = 4, 5, 6.
   - Strange (m = 3 -> 4 -> 5): lifting all unitary-closed rank-4 reps of |S>^3
     to |S>^4 recovers 69 exact rank-4 decompositions of |S>^4 in Z[omega_3]^81
     (a count depending on the `all_codes(3)` dictionary ordering and the
     `unitary_reps` representative set; internal positive control, verified
     entrywise against |S>^4), and testing all 243^2 x 243^2 four-qutrit
     Pauli-and-phase assignments on slice k = 2 (-|S>^4) and homogeneous slice
     k = 0 (0) finds 0 lifts to |S>^5, proving chi(|S>^{ot m}) >= 5 for m = 5, 6, 7, 8.

Printed claims:
  CERTIFIED chi(N^4) >= 5
  CERTIFIED chi(N^5) >= 5
  CERTIFIED chi(N^6) >= 5
  CERTIFIED chi(S^5) >= 5
  CERTIFIED chi(S^6) >= 5
  CERTIFIED chi(S^7) >= 5
  CERTIFIED chi(S^8) >= 5
"""

from __future__ import annotations

from concurrent.futures import ProcessPoolExecutor
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
from qutrit_codes import all_codes  # noqa: E402
from rank_exclusion_codes import CodeIndex  # noqa: E402
from slice_lift import stabilizer_orbit_labels  # noqa: E402
from stabrank_verify import orbit_state, target_vector  # noqa: E402

ELL = 65521          # Prime == 1 (mod 3); 65521^4 > 1.8e19
P = 1_000_000_021    # Prime == 1 (mod 3); exceeds Hadamard bound 135,000

LUT_A = np.array([0, 1, 0, -1], dtype=np.int64)
LUT_B = np.array([0, 0, 1, -1], dtype=np.int64)

_G_SCAN = None


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


def verify_symbolic_s_and_n() -> None:
    """Symbolic 2x2-minor projective checks and slice identities for S and N."""
    for name, ref_list, slice_idx, expected_amp in [
        ("S", [0, 1, -1], 1, 1 / sp.sqrt(2)),
        ("N", [1, 1, -2], 0, 1 / sp.sqrt(6)),
    ]:
        v1 = orbit_state(name)
        ref1 = sp.Matrix(ref_list)
        for a in range(3):
            for b in range(a + 1, 3):
                if sp.simplify(sp.expand(v1[a] * ref1[b] - v1[b] * ref1[a])) != 0:
                    raise AssertionError(f"2x2 minor ({a},{b}) mismatch against orbit_state({name!r})")
        if sp.simplify(v1[slice_idx] - expected_amp) != 0:
            raise AssertionError(f"Unexpected <{slice_idx}|{name}> amplitude: {v1[slice_idx]}")
        v2 = target_vector(name, 2)
        ref2 = sp.Matrix(sp.kronecker_product(ref1, ref1))
        nz_piv = next(j for j in range(9) if ref2[j] != 0)
        for j in range(9):
            if sp.simplify(sp.expand(v2[nz_piv] * ref2[j] - v2[j] * ref2[nz_piv])) != 0:
                raise AssertionError(f"2x2 minor ({nz_piv},{j}) mismatch against target_vector({name!r}, 2)")
        for j in range(3):
            if sp.simplify(v2[3 * slice_idx + j] - expected_amp * v1[j]) != 0:
                raise AssertionError(f"Slice (<{slice_idx}| (x) I)|{name}>^2 mismatch at {j}")


def exact_clifford_symmetries_d3(
    codes3: np.ndarray, D3p: np.ndarray, w3_p: int
) -> dict[str, tuple[np.ndarray, np.ndarray, list[np.ndarray], int]]:
    """Build exact 1-qutrit projective Clifford group C_1(3) (216 matrices over F_P)
    and exact permutations on all_codes(3) for S and N with zero floating-point ops."""
    X3 = np.array([[0, 0, 1], [1, 0, 0], [0, 1, 0]], dtype=np.int64)
    S3 = np.diag([1, 1, w3_p]) % P
    F3_scaled = (
        (1 - w3_p)
        * np.array([[pow(w3_p, (j * k) % 3, P) for k in range(3)] for j in range(3)], dtype=np.int64)
    ) % P

    def canon_mat(M: np.ndarray) -> np.ndarray:
        flat = (M % P).ravel()
        f = int(np.flatnonzero(flat)[0])
        return (M * pow(int(flat[f]), P - 2, P)) % P

    id3 = canon_mat(np.eye(3, dtype=np.int64))
    seen = {id3.tobytes(): id3}
    queue = [id3]
    while queue:
        U = queue.pop()
        for G in (X3, S3, F3_scaled):
            V = canon_mat((G @ U) % P)
            b = V.tobytes()
            if b not in seen:
                seen[b] = V
                queue.append(V)
    if len(seen) != 216:
        raise AssertionError(f"Expected 216 projective 1-qutrit Cliffords, got {len(seen)}")

    # Map F_P powers {0, 1, w3_p, w3_p^2} back to int8 codes {-1, 0, 1, 2}
    fp_to_code = {0: -1, 1: 0, int(w3_p): 1, int((w3_p * w3_p) % P): 2}
    code_index = CodeIndex(codes3)

    def mat_to_perm(G27: np.ndarray | None, conj: bool = False, perm_axes: tuple[int, int, int] | None = None) -> np.ndarray:
        if conj:
            crow = np.where(codes3 >= 0, (-codes3) % 3, -1).astype(np.int8)
            f = np.argmax(crow >= 0, axis=1)
            ref = crow[np.arange(len(crow)), f][:, None]
            crow = np.where(crow >= 0, (crow - ref) % 3, -1).astype(np.int8)
            return code_index.lookup(crow)
        if perm_axes is not None:
            digs = np.array([[(i // 9) % 3, (i // 3) % 3, i % 3] for i in range(27)], dtype=np.int64)
            src = digs[:, perm_axes] @ np.array([9, 3, 1], dtype=np.int64)
            # |x_0, x_1, x_2> -> |x_{p0}, x_{p1}, x_{p2}>: at dst index, value is old[inv_perm]
            prow = codes3[:, src].copy()
            f = np.argmax(prow >= 0, axis=1)
            ref = prow[np.arange(len(prow)), f][:, None]
            prow = np.where(prow >= 0, (prow - ref) % 3, -1).astype(np.int8)
            return code_index.lookup(prow)
        # Apply G27 = U (x) I_9 on first qutrit in exact F_P arithmetic!
        # D3p has shape (30240, 27) = (30240, 3, 9)
        blocks = D3p.reshape(len(D3p), 3, 9)
        img = np.einsum("ab,nbj->naj", G27, blocks) % P
        img_flat = img.reshape(len(D3p), 27)
        nz = img_flat != 0
        f = np.argmax(nz, axis=1)
        lead = img_flat[np.arange(len(img_flat)), f]
        # Batch modular inversion via prefix products
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
        out_codes[canon_img == w3_p] = 1
        out_codes[canon_img == (w3_p * w3_p) % P] = 2
        # Verify no unexpected F_P values appeared (i.e. every image is a valid stabilizer state!)
        valid_entries = (canon_img == 0) | (out_codes >= 0)
        if not np.all(valid_entries):
            raise AssertionError("Clifford image entry outside {0, 1, w3, w3^2} mod P")
        return code_index.lookup(out_codes)

    p_swap01 = mat_to_perm(None, perm_axes=(1, 0, 2))
    p_cyc = mat_to_perm(None, perm_axes=(1, 2, 0))
    p_conj = mat_to_perm(None, conj=True)

    result = {}
    for name, v_int, expected_local in [("S", [0, 1, -1], 24), ("N", [1, 1, -2], 6)]:
        v = np.array(v_int, dtype=np.int64) % P
        nz_v = int(np.flatnonzero(v)[0])
        vc = (v * pow(int(v[nz_v]), P - 2, P)) % P
        local_mats = []
        for U in seen.values():
            uv = (U @ v) % P
            nz = np.flatnonzero(uv)
            if len(nz) > 0:
                uvc = (uv * pow(int(uv[nz[0]]), P - 2, P)) % P
                if np.array_equal(uvc, vc):
                    local_mats.append(U)
        if len(local_mats) != expected_local:
            raise AssertionError(f"Expected {expected_local} local symmetries for {name}, got {len(local_mats)}")
        perms = [mat_to_perm(U) for U in local_mats] + [p_swap01, p_cyc, p_conj]
        inv_p = [np.argsort(pm) for pm in perms]
        labels = np.arange(len(codes3), dtype=np.int64)
        while True:
            new = labels.copy()
            for pm, ip in zip(perms, inv_p):
                new = np.minimum(new, new[pm])
                new = np.minimum(new, new[ip])
            if np.array_equal(new, labels):
                break
            labels = new
        reps, orb_sizes = np.unique(labels, return_counts=True)
        g_order = 2 * (len(local_mats) ** 3) * 6
        result[name] = (labels, reps, orb_sizes, perms, g_order)
    return result


def verify_m2_and_m3_rank3_exclusions(
    codes3: np.ndarray, D3p: np.ndarray, sym_info: dict, w3_p: int
) -> None:
    """Exact F_P positive controls at m = 2 (S rank 2, N rank 3) and 1-pivot
    rank-3 exclusions at m = 3 for S and N."""
    codes2, _ = all_codes(2)
    D2p = np.array([0, 1, w3_p, (w3_p * w3_p) % P], dtype=np.int64)[codes2 + 1]

    def canon_rows_p(W: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
        nz = W != 0
        act = np.flatnonzero(np.any(nz, axis=1))
        if len(act) == 0:
            return act, np.empty((0, W.shape[1]), dtype=np.int64)
        Wa = W[act]
        fa = np.argmax(nz[act], axis=1)
        lead = Wa[np.arange(len(act)), fa]
        pref = lead.copy()
        for k in range(1, len(lead)):
            pref[k] = (pref[k - 1] * int(lead[k])) % P
        inv_acc = pow(int(pref[-1]), P - 2, P)
        invs = np.empty(len(lead), dtype=np.int64)
        for k in range(len(lead) - 1, 0, -1):
            invs[k] = (inv_acc * pref[k - 1]) % P
            inv_acc = (inv_acc * int(lead[k])) % P
        invs[0] = inv_acc
        return act, (Wa * invs[:, None]) % P

    # Control 1: |S>^2 has rank-2 decompositions in D_2
    s1 = np.array([0, 1, -1], dtype=np.int64)
    s2 = np.kron(s1, s1) % P
    keep_s2 = [j for j in range(9) if j != 4]
    QS2 = (D2p[:, keep_s2] - np.outer(D2p[:, 4], s2[keep_s2])) % P
    _, WS2 = canon_rows_p(QS2)
    _, cnt_s2 = np.unique(WS2, axis=0, return_counts=True)
    if int(np.sum(cnt_s2 >= 2)) == 0:
        raise AssertionError("Control failed: rank-2 decomposition of |S>^2 not found")

    # Control 2: |N>^2 has exactly 48 rank-3 decompositions in D_2
    n1 = np.array([1, 1, -2], dtype=np.int64)
    n2 = np.kron(n1, n1) % P
    QN2 = (D2p[:, 1:] - np.outer(D2p[:, 0], n2[1:])) % P
    r3_n2 = set()
    for piv in range(len(D2p)):
        u = QN2[piv]
        c0 = int(np.flatnonzero(u)[0])
        un = (u * pow(int(u[c0]), P - 2, P)) % P
        cols = [c for c in range(8) if c != c0]
        W = (QN2[:, cols] - np.outer(QN2[:, c0], un[cols])) % P
        act, Wn = canon_rows_p(W)
        _, u_st, u_cnt = np.unique(Wn, axis=0, return_index=True, return_counts=True)
        for ui in u_st[u_cnt >= 2]:
            mem = [int(x) for x in act[np.all(Wn == Wn[ui], axis=1)]]
            for a, b in itertools.combinations(mem, 2):
                tup = tuple(sorted((piv, a, b)))
                if rank_mod_p(D2p[list(tup)]) == 3 and rank_mod_p(np.vstack([D2p[list(tup)], n2])) == 3:
                    r3_n2.add(tup)
    if len(r3_n2) != 48:
        raise AssertionError(f"Control failed: expected 48 rank-3 decompositions of |N>^2, got {len(r3_n2)}")

    # 1-pivot exact rank-3 exclusions on D_3 for S and N
    rng = np.random.default_rng(20261116)
    hw25 = rng.integers(1, P - 1, size=25, dtype=np.int64)
    for name, v_int in [("S", [0, 1, -1]), ("N", [1, 1, -2])]:
        v = np.array(v_int, dtype=np.int64)
        v3 = np.kron(np.kron(v, v), v) % P
        nz0 = int(np.flatnonzero(v3)[0])
        v3n = (v3 * pow(int(v3[nz0]), P - 2, P)) % P
        keep = [j for j in range(27) if j != nz0]
        Q1 = (D3p[:, keep] - np.outer(D3p[:, nz0], v3n[keep])) % P
        if not np.all(np.any(Q1 != 0, axis=1)):
            raise AssertionError(f"Rank-1 state found for {name}^3")
        _, reps, _, _, _ = sym_info[name]
        for piv in reps:
            u = Q1[int(piv)]
            c0 = int(np.flatnonzero(u)[0])
            un = (u * pow(int(u[c0]), P - 2, P)) % P
            cols = [c for c in range(26) if c != c0]
            W = (Q1[:, cols] - np.outer(Q1[:, c0], un[cols])) % P
            act, Wn = canon_rows_p(W)
            if len(act) < len(Q1) - 1:
                raise AssertionError(f"Rank-2 decomposition found for {name}^3")
            # Deterministic int64 matmul filter (wraps in int64), followed by exact rank_mod_p check
            h = (Wn @ hw25) % P
            order = np.argsort(h, kind="mergesort")
            hs = h[order]
            if not np.any(hs[1:] == hs[:-1]):
                continue
            _, st_arr, cnt_arr = np.unique(hs, return_index=True, return_counts=True)
            for st, cnt in zip(st_arr[cnt_arr >= 2], cnt_arr[cnt_arr >= 2]):
                grp = [int(piv)] + [int(x) for x in act[order[st:st + cnt]]]
                if rank_mod_p(np.vstack([D3p[grp], v3])) == rank_mod_p(D3p[grp]):
                    raise AssertionError(f"Rank-3 decomposition found for {name}^3: {grp}")


@njit(cache=True)
def _rank_rows_27(D3e: np.ndarray, r0: int64, r1: int64, r2: int64, r3: int64, nrows: int64, inv: np.ndarray, ell: int64) -> int64:
    """Exact 27-column rank over F_ell (ell = 65521) of 3 or 4 rows of D3e.
    By Hadamard's inequality, 3x3 and 4x4 minors of {0, 1, w3, w3^2} have
    |det|^2 <= 27 and 256 < 65521, so F_ell-rank equals exact Q(omega_3)-rank."""
    A = np.empty((4, 27), dtype=np.int64)
    for c in range(27):
        A[0, c] = D3e[r0, c]
        A[1, c] = D3e[r1, c]
        A[2, c] = D3e[r2, c]
        if nrows == 4:
            A[3, c] = D3e[r3, c]
    rk = int64(0)
    for c in range(27):
        if rk == nrows:
            break
        piv = -1
        for i in range(rk, nrows):
            if A[i, c] != 0:
                piv = i
                break
        if piv < 0:
            continue
        if piv != rk:
            for col in range(c, 27):
                tmp = A[rk, col]
                A[rk, col] = A[piv, col]
                A[piv, col] = tmp
        ia = inv[A[rk, c]]
        for col in range(c, 27):
            A[rk, col] = (A[rk, col] * ia) % ell
        for i in range(rk + 1, nrows):
            if A[i, c] != 0:
                fac = A[i, c]
                for col in range(c, 27):
                    v = (A[i, col] - fac * A[rk, col]) % ell
                    if v < 0:
                        v += ell
                    A[i, col] = v
        rk += 1
    return rk


@njit(cache=True)
def _scan_pivot_ell6(
    RQ1: np.ndarray,
    D3e: np.ndarray,
    inv: np.ndarray,
    i: int64,
    jok: np.ndarray,
    orb_rep: np.ndarray,
    ell: int64,
) -> tuple[np.ndarray, int64]:
    """Exact 6-column mod-65521 2-pivot rank-4 candidate scanner for pivot i,
    using unprojected 27-column D3e rank checks (exact by Hadamard: 256 < 65521)
    so linear projection is never used to assert independence."""
    N = RQ1.shape[0]
    TSIZE = 1 << 16
    TMASK = TSIZE - 1
    tkey = np.zeros(TSIZE, dtype=np.uint64)
    tval = np.full(TSIZE, -1, dtype=np.int64)
    tnext = np.full(N, -1, dtype=np.int64)
    tstamp = np.zeros(TSIZE, dtype=np.int64)
    stamp = int64(0)
    out = np.empty((200000, 4), dtype=np.int64)
    nout = int64(0)
    acc_zeros = int64(0)

    ui = RQ1[i]
    c0 = -1
    for d in range(6):
        if ui[d] != 0:
            c0 = d
            break
    if c0 < 0:
        return out[:0], int64(1)
    ia = inv[ui[c0]]
    Q2 = np.empty((N, 5), dtype=np.int64)
    for k in range(N):
        s = (RQ1[k, c0] * ia) % ell
        col = 0
        for d in range(6):
            if d == c0:
                continue
            v = (RQ1[k, d] - s * ui[d]) % ell
            if v < 0:
                v += ell
            Q2[k, col] = v
            col += 1

    for j in range(N):
        if j == i or jok[j] == 0:
            continue
        vj = Q2[j]
        c1 = -1
        for d in range(5):
            if vj[d] != 0:
                c1 = d
                break
        if c1 < 0:
            acc_zeros += 1
            continue
        ib = inv[vj[c1]]

        stamp += 1
        for k in range(j + 1, N):
            if k == i or orb_rep[k] < i:
                continue
            s = (Q2[k, c1] * ib) % ell
            w0 = int64(0); w1 = int64(0); w2 = int64(0); w3 = int64(0)
            col = 0
            for d in range(5):
                if d == c1:
                    continue
                val = (Q2[k, d] - s * vj[d]) % ell
                if val < 0:
                    val += ell
                if col == 0:
                    w0 = val
                elif col == 1:
                    w1 = val
                elif col == 2:
                    w2 = val
                else:
                    w3 = val
                col += 1
            if w0 != 0:
                iw = inv[w0]
                h = (
                    uint64(1)
                    + uint64((w1 * iw) % ell) * uint64(65537)
                    + uint64((w2 * iw) % ell) * uint64(0x9E3779B97F4A7C15)
                    + uint64((w3 * iw) % ell) * uint64(0xBF58476D1CE4E5B9)
                )
            elif w1 != 0:
                iw = inv[w1]
                h = (
                    uint64(2)
                    + uint64((w2 * iw) % ell) * uint64(0x9E3779B97F4A7C15)
                    + uint64((w3 * iw) % ell) * uint64(0xBF58476D1CE4E5B9)
                )
            elif w2 != 0:
                iw = inv[w2]
                h = uint64(3) + uint64((w3 * iw) % ell) * uint64(0xBF58476D1CE4E5B9)
            elif w3 != 0:
                h = uint64(4)
            else:
                # w == 0 in F_ell^4: check exact 27-col rank of {s_i, s_j, s_k} in D3e (|det|^2 <= 27 < 65521)
                if _rank_rows_27(D3e, i, j, int64(k), int64(0), int64(3), inv, ell) == 3:
                    acc_zeros += 1
                continue

            slot = int64((h ^ (h >> uint64(32))) & uint64(TMASK))
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
                        # Exact 27-column independence check (|det|^2 <= 256 < 65521: zero projection loss!)
                        if _rank_rows_27(D3e, i, j, cur, int64(k), int64(4), inv, ell) == 4:
                            if nout < out.shape[0]:
                                out[nout, 0] = i
                                out[nout, 1] = j
                                out[nout, 2] = cur
                                out[nout, 3] = k
                                nout += 1
                        cur = tnext[cur]
                    tnext[k] = tval[slot]
                    tval[slot] = k
                    break
                slot = (slot + 1) & TMASK
    return out[:nout], acc_zeros


def _init_scan_worker(RQ1, D3e, INV, labels, D3p, v3p):
    global _G_SCAN
    _G_SCAN = (RQ1, D3e, INV, labels, D3p, v3p)


def _run_scan_job(job):
    r, jok = job
    RQ1, D3e, INV, labels, D3p, v3p = _G_SCAN
    cands, acc_z = _scan_pivot_ell6(RQ1, D3e, INV, int64(r), jok, labels, int64(ELL))
    if int(acc_z) != 0 or len(cands) >= 200000:
        raise RuntimeError(f"Projection degeneracy or buffer overflow at pivot {r}: acc_z={acc_z}, cands={len(cands)}")
    hits = []
    for row in cands:
        tup = tuple(sorted(int(x) for x in row))
        if rank_mod_p(D3p[list(tup)]) == 4 and rank_mod_p(np.vstack([D3p[list(tup)], v3p])) == 4:
            hits.append(tup)
    return int(np.sum(jok)), len(cands), hits


def exact_pauli_pairs_zw3(
    uA: np.ndarray, uB: np.ndarray, m: int
) -> list[tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]]:
    """Vectorised exact Z[omega_3] builder returning all 3^m distinct Pauli-class
    pairs (Q u, Q^{-1} u) on m qutrits without renormalising (so Q and Q^{-1} keep
    consistent relative phase!)."""
    dim = 3 ** m
    digs = np.array(list(itertools.product(range(3), repeat=m)), dtype=np.int64)
    powers = 3 ** np.arange(m - 1, -1, -1, dtype=np.int64)
    Cs = digs  # (dim, m)
    PH = (digs @ Cs.T) % 3  # (dim, dim), entry (x, c_idx) = c.x mod 3

    # Precompute w3^{+ph} * u and w3^{-ph} * u for all x, c_idx: shape (dim, dim)
    uA_col = uA[:, None]
    uB_col = uB[:, None]
    posA = np.where(PH == 0, uA_col, np.where(PH == 1, -uB_col, uB_col - uA_col))
    posB = np.where(PH == 0, uB_col, np.where(PH == 1, uA_col - uB_col, -uA_col))
    negA = np.where(PH == 0, uA_col, np.where(PH == 2, -uB_col, uB_col - uA_col))
    negB = np.where(PH == 0, uB_col, np.where(PH == 2, uA_col - uB_col, -uA_col))

    seen = {}
    out = []
    for a_idx in range(dim):
        abits = digs[a_idx]
        y = ((digs + abits[None, :]) % 3) @ powers  # x + a
        quA = np.empty((dim, dim), dtype=np.int64)
        quB = np.empty((dim, dim), dtype=np.int64)
        quA[y, :] = posA
        quB[y, :] = posB
        # (Q^{-1} u)[x] = w3^{-c.x} u[x + a]
        u_shiftA = uA[y][:, None]
        u_shiftB = uB[y][:, None]
        qiA = np.where(PH == 0, u_shiftA, np.where(PH == 2, -u_shiftB, u_shiftB - u_shiftA))
        qiB = np.where(PH == 0, u_shiftB, np.where(PH == 2, u_shiftA - u_shiftB, -u_shiftA))

        # Canonicalise columns of qu modulo {1, w3, w3^2} to pick 1 representative per Pauli class
        nz = (quA != 0) | (quB != 0)
        first = np.argmax(nz, axis=0)
        a0 = quA[first, np.arange(dim)]
        b0 = quB[first, np.arange(dim)]
        # Since every non-zero entry of u is in {1, w3, w3^2}: (1,0)->*1, (0,1)->*w3^2, (-1,-1)->*w3
        ca = np.where((a0 == 1) & (b0 == 0), quA, np.where((a0 == 0) & (b0 == 1), quB - quA, -quB))
        cb = np.where((a0 == 1) & (b0 == 0), quB, np.where((a0 == 0) & (b0 == 1), -quA, quA - quB))
        for c_idx in range(dim):
            key = ca[:, c_idx].tobytes() + cb[:, c_idx].tobytes()
            if key not in seen:
                seen[key] = True
                out.append((
                    quA[:, c_idx].copy(),
                    quB[:, c_idx].copy(),
                    qiA[:, c_idx].copy(),
                    qiB[:, c_idx].copy(),
                ))
    if len(out) != dim:
        raise AssertionError(f"Expected {dim} Pauli classes on {m} qutrits, got {len(out)}")
    return out


def mul_zw3_vec(cA: int, cB: int, uA: np.ndarray, uB: np.ndarray, w3_pow: int) -> tuple[np.ndarray, np.ndarray]:
    """Compute (cA + cB*w3) * w3^{w3_pow} * (uA + uB*w3) in Z[omega_3]."""
    if w3_pow == 0:
        xA, xB = uA, uB
    elif w3_pow == 1:
        xA, xB = -uB, uA - uB
    else:
        xA, xB = uB - uA, -uA
    return cA * xA - cB * xB, cA * xB + cB * xA - cB * xB


def solve_zw3_coeffs(U_A: np.ndarray, U_B: np.ndarray, tgt_A: np.ndarray, tgt_B: np.ndarray) -> tuple[int, list[tuple[int, int]]]:
    """Solve sum_r c_r u_r = tgt in exact Q(omega_3) via SymPy; return (D, [(cA_r, cB_r)])
    in Z[omega_3] such that sum_r c_r u_r == D * tgt."""
    dim = U_A.shape[1]
    M_top = np.hstack([U_A.T, -U_B.T])
    M_bot = np.hstack([U_B.T, (U_A - U_B).T])
    M_sys = sp.Matrix(np.vstack([M_top, M_bot]).tolist())
    rhs = sp.Matrix(list(tgt_A) + list(tgt_B))
    sol, params = M_sys.gauss_jordan_solve(rhs)
    if len(params) != 0:
        raise AssertionError("Basis is not linearly independent in exact Q(omega_3) solve")
    den_lcm = 1
    for q in sol:
        den_lcm = int(sp.ilcm(den_lcm, sp.denom(q)))
    r_cnt = U_A.shape[0]
    ints = [int(q * den_lcm) for q in sol]
    coeffs = []
    for r in range(r_cnt):
        pair = (ints[r], ints[r + r_cnt])
        if pair == (0, 0):
            raise AssertionError("Zero coefficient in minimal decomposition")
        coeffs.append(pair)
    # Verify reconstruction entrywise in Z[omega_3]
    recA = np.zeros(dim, dtype=np.int64)
    recB = np.zeros(dim, dtype=np.int64)
    for r in range(r_cnt):
        xA, xB = mul_zw3_vec(coeffs[r][0], coeffs[r][1], U_A[r], U_B[r], 0)
        recA += xA
        recB += xB
    if not (np.array_equal(recA, den_lcm * tgt_A) and np.array_equal(recB, den_lcm * tgt_B)):
        raise AssertionError("Exact Z[omega_3] slice-1 reconstruction check failed")
    return den_lcm, coeffs


def exact_lifts_zw3(
    U_A: np.ndarray,
    U_B: np.ndarray,
    den_lcm: int,
    coeffs: list[tuple[int, int]],
    alpha_0: int,
    alpha_1: int,
    alpha_2: int,
    tgt_A: np.ndarray,
    tgt_B: np.ndarray,
    m: int,
    hw: np.ndarray,
) -> list[tuple[np.ndarray, np.ndarray]]:
    """Exact integer meet-in-the-middle Pauli slice-and-lift from m to m + 1 qutrits,
    centered on slice k = 1 (where alpha_1 == 1 and sum_r c_r u_r == den_lcm * tgt).
    Slice k = 2 requires sum_r c_r mu_r (Q_r u_r) == (alpha_2 * den_lcm) * tgt;
    Slice k = 0 requires sum_r c_r nu_r (Q_r^{-1} u_r) == (alpha_0 * den_lcm) * tgt."""
    if alpha_1 != 1:
        raise ValueError("alpha_1 must be normalised to 1")
    r_cnt = U_A.shape[0]
    dim = 3 ** m
    imgs = [exact_pauli_pairs_zw3(U_A[r], U_B[r], m) for r in range(r_cnt)]

    opts2 = []
    for r in range(r_cnt):
        cA, cB = coeffs[r]
        rows = []
        for quA, quB, _, _ in imgs[r]:
            for mu_pow in (0, 1, 2):
                vA, vB = mul_zw3_vec(cA, cB, quA, quB, mu_pow)
                rows.append(np.concatenate([vA, vB]))
        opts2.append(np.stack(rows))  # (3^(m+1), 2*dim)

    rhs2 = np.concatenate([alpha_2 * den_lcm * tgt_A, alpha_2 * den_lcm * tgt_B])
    rhs0 = np.concatenate([alpha_0 * den_lcm * tgt_A, alpha_0 * den_lcm * tgt_B])

    half = r_cnt // 2
    L = opts2[0]
    for arr in opts2[1:half]:
        L = (L[:, None, :] + arr[None, :, :]).reshape(-1, 2 * dim)
    R = opts2[half]
    for arr in opts2[half + 1:]:
        R = (R[:, None, :] + arr[None, :, :]).reshape(-1, 2 * dim)
    R_need = rhs2[None, :] - R

    # Deterministic int64 matmul filter (wraps in int64; equal vectors map identically),
    # followed by exact full 2*dim int64 np.array_equal verification below.
    hL = ((L % P) @ hw) % P
    hR = ((R_need % P) @ hw) % P
    ordL = np.argsort(hL, kind="mergesort")
    hLs = hL[ordL]
    lo = np.searchsorted(hLs, hR, side="left")
    hi = np.searchsorted(hLs, hR, side="right")
    cand_r = np.flatnonzero(hi > lo)

    n_opt = 3 ** (m + 1)
    nu_combos = list(itertools.product((0, 1, 2), repeat=r_cnt))
    lifted = []

    for r_idx in cand_r:
        need_vec = R_need[r_idx]
        for pos in range(int(lo[r_idx]), int(hi[r_idx])):
            l_idx = int(ordL[pos])
            if not np.array_equal(L[l_idx], need_vec):
                continue
            # Decode mixed-radix indices
            idxs = []
            tmp = l_idx
            for _ in range(half):
                idxs.append(tmp % n_opt)
                tmp //= n_opt
            idxs = idxs[::-1]
            rtmp = int(r_idx)
            r_idxs = []
            for _ in range(r_cnt - half):
                r_idxs.append(rtmp % n_opt)
                rtmp //= n_opt
            idxs.extend(r_idxs[::-1])

            cls = [c // 3 for c in idxs]
            mus = [c % 3 for c in idxs]

            # Test all 3^r_cnt cube-root choices nu_r on slice k = 0
            qinv_phased = []
            for r in range(r_cnt):
                cA, cB = coeffs[r]
                _, _, qiA, qiB = imgs[r][cls[r]]
                qinv_phased.append([
                    np.concatenate(mul_zw3_vec(cA, cB, qiA, qiB, nu_p))
                    for nu_p in (0, 1, 2)
                ])
            for nus in nu_combos:
                acc0 = qinv_phased[0][nus[0]].copy()
                for r in range(1, r_cnt):
                    acc0 += qinv_phased[r][nus[r]]
                if np.array_equal(acc0, rhs0):
                    # Assemble exact (m+1)-qutrit stabilizer vectors: (nu Q^{-1} u, u, mu Q u)
                    next_A, next_B = [], []
                    for r in range(r_cnt):
                        quA, quB, qiA, qiB = imgs[r][cls[r]]
                        s0A, s0B = mul_zw3_vec(1, 0, qiA, qiB, nus[r])
                        s2A, s2B = mul_zw3_vec(1, 0, quA, quB, mus[r])
                        next_A.append(np.concatenate([s0A, U_A[r], s2A]))
                        next_B.append(np.concatenate([s0B, U_B[r], s2B]))
                    lifted.append((np.stack(next_A), np.stack(next_B)))
    return lifted


def main() -> int:
    t0 = time.time()
    for pr in (ELL, P):
        if not sp.isprime(pr) or (pr - 1) % 3 != 0:
            raise AssertionError(f"Prime check failed for {pr}")
    if P <= 135_000:
        raise AssertionError(f"P = {P} does not exceed Hadamard norm bound 135,000")

    verify_symbolic_s_and_n()

    w3_e = next(pow(g, (ELL - 1) // 3, ELL) for g in range(2, 100) if pow(g, (ELL - 1) // 3, ELL) != 1)
    w3_p = next(pow(g, (P - 1) // 3, P) for g in range(2, 100) if pow(g, (P - 1) // 3, P) != 1)
    INV = np.zeros(ELL, dtype=np.int64)
    INV[1:] = [pow(x, ELL - 2, ELL) for x in range(1, ELL)]

    codes1, _ = all_codes(1)
    A1, B1 = codes_to_zw3(codes1)
    # Positive lift control: |S> = |1> - |2> (rank 2 on 1 qutrit) lifts to |S>^2
    i1 = int(np.flatnonzero((A1[:, 0] == 0) & (A1[:, 1] == 1) & (A1[:, 2] == 0) & np.all(B1 == 0, axis=1))[0])
    i2 = int(np.flatnonzero((A1[:, 0] == 0) & (A1[:, 1] == 0) & (A1[:, 2] == 1) & np.all(B1 == 0, axis=1))[0])
    U1_A, U1_B = A1[[i1, i2]], B1[[i1, i2]]
    s1_A = np.array([0, 1, -1], dtype=np.int64)
    s1_B = np.zeros(3, dtype=np.int64)
    den1, coeffs1 = solve_zw3_coeffs(U1_A, U1_B, s1_A, s1_B)
    rng = np.random.default_rng(20261116)
    lifts_s1 = exact_lifts_zw3(
        U1_A, U1_B, den1, coeffs1, 0, 1, -1, s1_A, s1_B, 1,
        rng.integers(1, P - 1, size=6, dtype=np.int64),
    )
    if len(lifts_s1) == 0:
        raise AssertionError("Positive lift control failed: |S> did not lift to |S>^2")

    codes3, _ = all_codes(3)
    A3, B3 = codes_to_zw3(codes3)
    D3e = np.array([0, 1, w3_e, (w3_e * w3_e) % ELL], dtype=np.int64)[codes3 + 1]
    D3p = np.array([0, 1, w3_p, (w3_p * w3_p) % P], dtype=np.int64)[codes3 + 1]

    sym_info = exact_clifford_symmetries_d3(codes3, D3p, w3_p)
    verify_m2_and_m3_rank3_exclusions(codes3, D3p, sym_info, w3_p)
    print(f"controls and m=3 rank-3 exclusions passed [{time.time() - t0:.2f}s]")

    R26 = rng.integers(1, ELL - 1, size=(26, 6), dtype=np.int64)
    code_map3 = {codes3[i].tobytes(): i for i in range(len(codes3))}
    workers = max(1, min(4, os.cpu_count() or 1))

    hw54 = rng.integers(1, P - 1, size=54, dtype=np.int64)
    hw162 = rng.integers(1, P - 1, size=162, dtype=np.int64)

    for name, v_int in [("N", [1, 1, -2]), ("S", [0, 1, -1])]:
        ts = time.time()
        v = np.array(v_int, dtype=np.int64)
        v3_z = np.kron(np.kron(v, v), v)
        v3e = v3_z % ELL
        nz0 = int(np.flatnonzero(v3e)[0])
        v3en = (v3e * INV[v3e[nz0]]) % ELL
        keep = [c for c in range(27) if c != nz0]
        RQ1 = (((D3e[:, keep] - np.outer(D3e[:, nz0], v3en[keep])) % ELL) @ R26) % ELL
        v3p = v3_z % P

        labels, reps, orb_sizes, perms, g_order = sym_info[name]
        jobs = []
        for r, osize in zip(reps, orb_sizes):
            s_lbl, _ = stabilizer_orbit_labels(perms, int(r), stabilizer_order=g_order // int(osize))
            cand = np.flatnonzero((labels >= r) & (np.arange(len(codes3)) != r))
            _, first = np.unique(s_lbl[cand], return_index=True)
            jok = np.zeros(len(codes3), dtype=np.int8)
            jok[cand[first]] = 1
            jobs.append((int(r), jok))

        r4_orbs: set[tuple[int, int, int, int]] = set()
        tot_partners = 0
        with ProcessPoolExecutor(
            max_workers=workers, initializer=_init_scan_worker, initargs=(RQ1, D3e, INV, labels, D3p, v3p)
        ) as ex:
            for npairs, _, hits in ex.map(_run_scan_job, jobs):
                tot_partners += npairs
                for tup in hits:
                    # Confirm over Z in SymPy as well!
                    v3_B = np.zeros(27, dtype=np.int64)
                    if (zw3_rank(A3[list(tup)], B3[list(tup)]) == 4
                            and zw3_rank(np.vstack([A3[list(tup)], v3_z]),
                                         np.vstack([B3[list(tup)], v3_B])) == 4):
                        r4_orbs.add(tup)

        if len(r4_orbs) == 0:
            raise AssertionError(f"Failed to find known rank-4 decomposition of |{name}>^3")

        # Close under complex conjugation so every unitary orbit is tested without antiunitary assumptions
        unitary_reps = set(r4_orbs)
        for tup in list(r4_orbs):
            conj_tup = []
            for idx in tup:
                row = codes3[idx]
                crow = np.where(row >= 0, (-row) % 3, -1).astype(np.int8)
                f = int(np.flatnonzero(crow >= 0)[0])
                crow = np.where(crow >= 0, (crow - crow[f]) % 3, -1).astype(np.int8)
                conj_tup.append(code_map3[crow.tobytes()])
            unitary_reps.add(tuple(sorted(conj_tup)))

        v3_B = np.zeros(27, dtype=np.int64)
        lifts_m4 = []
        for tup in sorted(unitary_reps):
            U_A, U_B = A3[list(tup)], B3[list(tup)]
            den, coeffs = solve_zw3_coeffs(U_A, U_B, v3_z, v3_B)
            found4 = exact_lifts_zw3(
                U_A, U_B, den, coeffs, v_int[0], v_int[1], v_int[2], v3_z, v3_B, 3, hw54
            )
            for wA, wB in found4:
                lifts_m4.append((wA, wB, den, coeffs))

        if name == "N":
            if len(lifts_m4) != 0:
                print(f"RANK-4 LIFT FOUND FOR |N>^4: {len(lifts_m4)}", file=sys.stderr)
                return 1
            print(
                f"exact N m=3->4 check: {len(reps)} pivot orbits ({tot_partners} pairs), "
                f"{len(unitary_reps)} rank-4 rep(s) of |N>^3, 0 lifts to |N>^4 [{time.time() - ts:.2f}s]"
            )
        else:
            if len(lifts_m4) == 0:
                raise AssertionError("Internal positive control failed: no rank-4 lift of |S>^3 to |S>^4 found")
            v4_z = np.kron(v, v3_z)
            v4_B = np.zeros(81, dtype=np.int64)
            lifts_m5 = 0
            for wA, wB, den, coeffs in lifts_m4:
                # Verify assembled m=4 decomposition reproduces den * |S>^4 in Z[omega_3]^81
                rec4A = np.zeros(81, dtype=np.int64)
                rec4B = np.zeros(81, dtype=np.int64)
                for r in range(4):
                    xA, xB = mul_zw3_vec(coeffs[r][0], coeffs[r][1], wA[r], wB[r], 0)
                    rec4A += xA
                    rec4B += xB
                if not (np.array_equal(rec4A, den * v4_z) and np.all(rec4B == 0)):
                    raise AssertionError("Assembled |S>^4 lift failed exact Z[omega_3]^81 identity")
                found5 = exact_lifts_zw3(
                    wA, wB, den, coeffs, 0, 1, -1, v4_z, v4_B, 4, hw162
                )
                lifts_m5 += len(found5)
            if lifts_m5 != 0:
                print(f"RANK-4 LIFT FOUND FOR |S>^5: {lifts_m5}", file=sys.stderr)
                return 1
            print(
                f"exact S m=3->4->5 check: {len(reps)} pivot orbits ({tot_partners} pairs), "
                f"{len(unitary_reps)} m=3 rep(s) -> {len(lifts_m4)} exact |S>^4 lifts -> "
                f"0 lifts to |S>^5 [{time.time() - ts:.2f}s]"
            )

    for m in (4, 5, 6):
        print(f"CERTIFIED chi(N^{m}) >= 5")
    for m in (5, 6, 7, 8):
        print(f"CERTIFIED chi(S^{m}) >= 5")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
