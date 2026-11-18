"""Exact Z[omega_5] / Hadamard-prime certificate: chi(|T5>^{ot m}) >= 5 for m = 2..5.

Upgrades T5 m = 2, 3, 4 from `reproduced` (floating-point margin 1e-6 in
`cert_t5_m2_rank4.py`) to `verified` (`exact: true`), settling chi(|T5>^{ot 2}) = 5
at verified/lean in both directions, and adds the missing m = 5 cell by
projection monotonicity.

Mathematical guarantees (zero floating-point arithmetic):
1. Exact ququint dictionary D(5, n): Every n-ququint stabilizer state has
   support on an affine flat x_0 + rowspace(G) subset F_5^n (G in RREF of rank
   0 <= k <= n) and amplitudes omega_5^{Q(u) + l.u} in Z[omega_5], yielding
   exactly 30 states for n = 1 and 3,900 states for n = 2.
2. Hadamard algebraic norm bound over Z[omega_5]: For any k x k matrix M
   (k <= 5) with entries in {0, 1, omega_5, omega_5^2, omega_5^3, omega_5^4},
   Hadamard's inequality in each of the 4 embeddings sigma_c: Q(omega_5) -> C
   gives |sigma_c(det M)| <= k^{k/2}, hence
       |N_{Q(omega_5)/Q}(det M)| <= (k^{k/2})^4 = k^{2k} <= 5^{10} = 9,765,625.
   At the split prime P = 1,000,000,021 = 1 (mod 5) (P > 102 * 5^{10}), the
   ring homomorphism Z[omega_5] -> F_P sending omega_5 -> g^{(P-1)/5} mod P
   cannot annihilate any non-zero minor of size <= 5, so F_P-rank equals the
   exact Q(omega_5)-rank on every <= 5-subset of D(5, 2) union {|T5>^{ot 2}}.
3. Order-200 Galois-Clifford symmetry reduction: Because c -> c^3 mod 5 is a
   bijection on F_5^*, every Galois automorphism sigma_{c^3}: omega_5 -> omega_5^{c^3}
   paired with coordinate scaling x -> c x mod 5, local Clifford shifts
   U_a |x> = omega_5^{(x+a)^3 - x^3} |x+a>, and copy swap preserves both D(5, 2)
   and span_{Q(omega_5)}(|T5>^{ot 2}), forming an exact permutation group G_200
   of order 200 (verified explicitly on both D(5, 2) and |T5>^{ot 2}) with 38
   pivot orbits and 40,124 stabilizer-reduced (pivot, partner) pairs. Canonical
   quotient rays are bucketed via a deterministic int64 matmul filter (wrapping
   in int64 while preserving row equality) and then verified by exact row
   matching (`np.unique(..., axis=0)`) and exact `rank_mod_p` checks.
4. Positive controls (fatal if violated):
   - Exact 1-ququint search finds the 10 rank-3 decompositions of |T5> (2 orbits of 5).
   - Exact 2-ququint rank-4 search from pivot |00> recovers the product
     rank-4 decomposition {|00>, |0+>, |+0>, |++>} of (5|+> - |0>)^{ot 2}.
5. Projection monotonicity: (<0| (x) I)|T5>^{ot (m+1)} = 5^{-1/2} |T5>^{ot m},
   verified symbolically in SymPy alongside 2x2 minors against orbit_state("T5")
   and target_vector("T5", 2), lifts chi >= 5 to m = 3, 4, 5.

Printed claims:
  CERTIFIED chi(T5^2) >= 5
  CERTIFIED chi(T5^3) >= 5
  CERTIFIED chi(T5^4) >= 5
  CERTIFIED chi(T5^5) >= 5
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
import sympy as sp

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from stabrank_verify import orbit_state, target_vector  # noqa: E402

P = 1_000_000_021

_G_Q1 = None
_G_ORB = None
_G_PERMS = None
_G_HW = None


def ququint_codes(n: int) -> np.ndarray:
    """Exact phase-exponent codes (-1 off support, 0..4 power of omega_5) for all
    stabilizer states on n ququints, using only integer arithmetic over F_5."""
    dim = 5 ** n
    powers = 5 ** np.arange(n - 1, -1, -1, dtype=np.int64)
    states = []
    for k in range(n + 1):
        u_grid = (
            np.array(list(itertools.product(range(5), repeat=k)), dtype=np.int64)
            if k > 0 else np.zeros((1, 0), dtype=np.int64)
        )
        q_pairs = [(a, b) for a in range(k) for b in range(a, k)]
        monoms = [((u_grid[:, a] * u_grid[:, b]) % 5) for a, b in q_pairs] + [u_grid[:, a] for a in range(k)]
        all_m = np.column_stack(monoms) if monoms else np.zeros((len(u_grid), 0), dtype=np.int64)
        c_grid = (
            np.array(list(itertools.product(range(5), repeat=all_m.shape[1])), dtype=np.int64)
            if all_m.shape[1] > 0 else np.zeros((1, 0), dtype=np.int64)
        )
        phases_all = ((c_grid @ all_m.T) % 5).astype(np.int8)
        for pivs in itertools.combinations(range(n), k):
            free_cols = [c for c in range(n) if c not in pivs]
            pos_list = [(r, c) for r in range(k) for c in free_cols if c > pivs[r]]
            for vals in itertools.product(range(5), repeat=len(pos_list)):
                G = np.zeros((k, n), dtype=np.int64)
                for r, pcol in enumerate(pivs):
                    G[r, pcol] = 1
                for (r, c), v in zip(pos_list, vals):
                    G[r, c] = v
                base_pts = (u_grid @ G) % 5 if k > 0 else np.zeros((1, n), dtype=np.int64)
                for shift_vals in itertools.product(range(5), repeat=len(free_cols)):
                    x0 = np.zeros(n, dtype=np.int64)
                    for c, sv in zip(free_cols, shift_vals):
                        x0[c] = sv
                    flat_idx = ((base_pts + x0[None, :]) % 5) @ powers
                    block = np.full((len(phases_all), dim), -1, dtype=np.int8)
                    block[:, flat_idx] = phases_all
                    states.append(block)
    return np.vstack(states)


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


def canon_mod_rows(W: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
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
    inv_all = pow(int(pref[-1]), P - 2, P)
    invs = np.empty(len(lead), dtype=np.int64)
    for k in range(len(lead) - 1, 0, -1):
        invs[k] = (inv_all * pref[k - 1]) % P
        inv_all = (inv_all * int(lead[k])) % P
    invs[0] = inv_all
    return act, (Wa * invs[:, None]) % P


def _init_worker(Q1: np.ndarray, orb_rep: np.ndarray, perms200: np.ndarray, hw22: np.ndarray) -> None:
    global _G_Q1, _G_ORB, _G_PERMS, _G_HW
    _G_Q1, _G_ORB, _G_PERMS, _G_HW = Q1, orb_rep, perms200, hw22


def _scan_pivot_r4(piv: int) -> tuple[int, list[tuple[int, ...]]]:
    Q1, orb_rep, perms200, hw22 = _G_Q1, _G_ORB, _G_PERMS, _G_HW
    u = Q1[piv]
    c0 = int(np.flatnonzero(u)[0])
    un = (u * pow(int(u[c0]), P - 2, P)) % P
    cols1 = [c for c in range(24) if c != c0]
    Q2_full = (Q1[:, cols1] - np.outer(Q1[:, c0], un[cols1])) % P

    stab = perms200[perms200[:, piv] == piv]
    valid_mask = (orb_rep >= piv) & (np.arange(len(Q1)) != piv)
    valid_s = np.flatnonzero(valid_mask)
    stab_min_all = np.min(stab, axis=0)
    js = [int(x) for x in valid_s if int(stab_min_all[x]) == int(x)]

    cand_hits = []
    for j in js:
        vj = Q2_full[j]
        nz_j = np.flatnonzero(vj)
        if len(nz_j) == 0:
            continue
        cj = int(nz_j[0])
        vjn = (vj * pow(int(vj[cj]), P - 2, P)) % P
        cols2 = [c for c in range(23) if c != cj]

        pool = valid_s[(stab_min_all[valid_s] >= j) & (valid_s != j)]
        if len(pool) < 2:
            continue
        Qp = Q2_full[pool]
        W3 = (Qp[:, cols2] - np.outer(Qp[:, cj], vjn[cols2])) % P
        act_loc, Wn = canon_mod_rows(W3)
        if len(act_loc) < len(pool):
            zeros = pool[np.all(W3 == 0, axis=1)]
            for z in zeros:
                cand_hits.append((int(piv), int(j), int(z)))
        if len(act_loc) < 2:
            continue
        # Deterministic int64 matmul filter (wraps in int64), followed by exact subW row equality
        h = (Wn @ hw22) % P
        order = np.argsort(h, kind="mergesort")
        hs = h[order]
        if not np.any(hs[1:] == hs[:-1]):
            continue
        _, st_arr, cnt_arr = np.unique(hs, return_index=True, return_counts=True)
        for st, cnt in zip(st_arr[cnt_arr >= 2], cnt_arr[cnt_arr >= 2]):
            sub_idx = act_loc[order[st:st + cnt]]
            subW = Wn[order[st:st + cnt]]
            _, u_st, u_cnt = np.unique(subW, axis=0, return_index=True, return_counts=True)
            for ui, uc in zip(u_st[u_cnt >= 2], u_cnt[u_cnt >= 2]):
                members = pool[sub_idx[np.all(subW == subW[ui], axis=1)]]
                cand_hits.append((int(piv), int(j), *[int(x) for x in members]))
    return len(js), cand_hits


def verify_symbolic_t5() -> None:
    """Symbolic 2x2-minor projective checks against stabrank_verify.orbit_state
    and target_vector, plus slice projection identity."""
    w5 = sp.exp(2 * sp.pi * sp.I / 5)
    ref1 = sp.Matrix([w5 ** ((x ** 3) % 5) for x in range(5)])
    t5_sym = orbit_state("T5")
    for a in range(5):
        for b in range(a + 1, 5):
            if sp.simplify(sp.expand_complex(t5_sym[a] * ref1[b] - t5_sym[b] * ref1[a])) != 0:
                raise AssertionError(f"2x2 minor ({a},{b}) mismatch against orbit_state('T5')")
    if sp.simplify(t5_sym[0] - 1 / sp.sqrt(5)) != 0:
        raise AssertionError("Symbolic <0|T5> != 1/sqrt(5)")

    t5_2 = target_vector("T5", 2)
    ref2 = sp.Matrix(sp.kronecker_product(ref1, ref1))
    for j in range(1, 25):
        if sp.simplify(sp.expand_complex(t5_2[0] * ref2[j] - t5_2[j] * ref2[0])) != 0:
            raise AssertionError(f"2x2 minor (0,{j}) mismatch against target_vector('T5', 2)")
    for j in range(5):
        if sp.simplify(sp.expand_complex(t5_2[j] - t5_sym[0] * t5_sym[j])) != 0:
            raise AssertionError(f"Slice (<0| (x) I)|T5>^2 mismatch at {j}")


def verify_controls(c1: np.ndarray, c2: np.ndarray, w5_lut: np.ndarray) -> None:
    """Positive controls on 1 ququint (|T5> rank 3) and 2 ququints (|N5>^2 rank 4)."""
    D1 = w5_lut[c1 + 1]
    e1 = np.array([(x ** 3) % 5 for x in range(5)], dtype=np.int64)
    psi1 = np.array([w5_lut[int(e) + 1] for e in e1], dtype=np.int64)
    Q1 = (D1[:, 1:] - np.outer(D1[:, 0], psi1[1:])) % P
    r3_t5 = set()
    for piv in range(len(D1)):
        u = Q1[piv]
        c0 = int(np.flatnonzero(u)[0])
        un = (u * pow(int(u[c0]), P - 2, P)) % P
        cols = [c for c in range(4) if c != c0]
        W = (Q1[:, cols] - np.outer(Q1[:, c0], un[cols])) % P
        act, Wn = canon_mod_rows(W)
        _, u_st, u_cnt = np.unique(Wn, axis=0, return_index=True, return_counts=True)
        for ui in u_st[u_cnt >= 2]:
            mem = act[np.all(Wn == Wn[ui], axis=1)]
            for a, b in itertools.combinations([int(x) for x in mem], 2):
                tup = tuple(sorted((piv, a, b)))
                if rank_mod_p(D1[list(tup)]) == 3 and rank_mod_p(np.vstack([D1[list(tup)], psi1])) == 3:
                    r3_t5.add(tup)
    if len(r3_t5) != 10:
        raise AssertionError(f"Control 1 FAILED: expected 10 rank-3 decompositions of |T5> (2 orbits of 5), got {len(r3_t5)}")

    D2 = w5_lut[c2 + 1]
    row_map = {c2[i].tobytes(): i for i in range(len(c2))}
    z_code = np.array([0, -1, -1, -1, -1], dtype=np.int8)
    p_code = np.array([0, 0, 0, 0, 0], dtype=np.int8)

    def kron_code(a: np.ndarray, b: np.ndarray) -> int:
        out = np.full(25, -1, dtype=np.int8)
        for i in range(5):
            for j in range(5):
                if a[i] >= 0 and b[j] >= 0:
                    out[i * 5 + j] = (int(a[i]) + int(b[j])) % 5
        return row_map[out.tobytes()]

    piv00 = kron_code(z_code, z_code)
    want = tuple(sorted(kron_code(a, b) for a in (z_code, p_code) for b in (z_code, p_code)))
    n5_1 = np.array([-4, 1, 1, 1, 1], dtype=np.int64) % P
    n5_2 = np.kron(n5_1, n5_1) % P
    inv0 = pow(int(n5_2[0]), P - 2, P)
    n5_norm = (n5_2 * inv0) % P
    QN1 = (D2[:, 1:] - np.outer(D2[:, 0], n5_norm[1:])) % P
    u = QN1[piv00]
    c0 = int(np.flatnonzero(u)[0])
    un = (u * pow(int(u[c0]), P - 2, P)) % P
    cols1 = [c for c in range(24) if c != c0]
    QN2 = (QN1[:, cols1] - np.outer(QN1[:, c0], un[cols1])) % P
    found_want = False
    j_target = want[1] if want[0] == piv00 else want[0]
    vj = QN2[j_target]
    cj = int(np.flatnonzero(vj)[0])
    vjn = (vj * pow(int(vj[cj]), P - 2, P)) % P
    cols2 = [c for c in range(23) if c != cj]
    WN3 = (QN2[:, cols2] - np.outer(QN2[:, cj], vjn[cols2])) % P
    act, Wn = canon_mod_rows(WN3)
    _, u_st, u_cnt = np.unique(Wn, axis=0, return_index=True, return_counts=True)
    for ui in u_st[u_cnt >= 2]:
        mem = [int(x) for x in act[np.all(Wn == Wn[ui], axis=1)]]
        for a, b in itertools.combinations(mem, 2):
            if tuple(sorted((piv00, j_target, a, b))) == want:
                if rank_mod_p(D2[list(want)]) == 4 and rank_mod_p(np.vstack([D2[list(want)], n5_norm])) == 4:
                    found_want = True
    if not found_want:
        raise AssertionError("Control 2 FAILED: product rank-4 decomposition of |N5>^2 not recovered")


def main() -> int:
    t0 = time.time()
    if not sp.isprime(P) or (P - 1) % 5 != 0:
        raise AssertionError(f"P = {P} is not a prime congruent to 1 mod 5")
    hadamard_bound = 5 ** 10
    if P <= hadamard_bound:
        raise AssertionError(f"P = {P} does not exceed Hadamard norm bound {hadamard_bound}")
    g = int(sp.primitive_root(P))
    w5 = pow(g, (P - 1) // 5, P)
    if sum(pow(w5, k, P) for k in range(5)) % P != 0 or w5 == 1:
        raise AssertionError("Invalid primitive 5th root of unity mod P")

    verify_symbolic_t5()

    c1 = ququint_codes(1)
    c2 = ququint_codes(2)
    if c1.shape != (30, 5) or c2.shape != (3900, 25):
        raise AssertionError(f"Unexpected ququint dictionary shapes: {c1.shape}, {c2.shape}")

    w5_lut = np.array([0] + [pow(w5, k, P) for k in range(5)], dtype=np.int64)
    verify_controls(c1, c2, w5_lut)
    print("controls passed: 10 exact rank-3 decompositions of |T5> (2 orbits) and product rank-4 of |N5>^2 recovered")

    row_bytes = {c2[i].tobytes(): i for i in range(len(c2))}
    if len(row_bytes) != 3900:
        raise AssertionError("Duplicate states in ququint_codes(2)")
    digs2 = np.array(list(itertools.product(range(5), repeat=2)), dtype=np.int64)
    e1 = np.array([(x ** 3) % 5 for x in range(5)], dtype=np.int64)
    target_exp2 = np.array([(e1[i // 5] + e1[i % 5]) % 5 for i in range(25)], dtype=np.int64)
    perms200 = []
    for c in (1, 2, 3, 4):
        k_gal = (c ** 3) % 5
        for swap in (False, True):
            for a1 in range(5):
                for a2 in range(5):
                    src = digs2[:, ::-1] if swap else digs2
                    y0 = (src[:, 0] + a1) % 5
                    y1 = (src[:, 1] + a2) % 5
                    ph_u = ((e1[y0] - e1[src[:, 0]]) + (e1[y1] - e1[src[:, 1]])) % 5
                    dst_idx = ((c * y0) % 5) * 5 + ((c * y1) % 5)
                    # Verify this symmetry maps target_exp2 to target_exp2 + const (mod 5)
                    t_mapped = np.empty(25, dtype=np.int64)
                    t_mapped[dst_idx] = (k_gal * (target_exp2 + ph_u)) % 5
                    diffs = (t_mapped - target_exp2) % 5
                    if len(set(diffs.tolist())) != 1:
                        raise AssertionError("Symmetry element failed to preserve |T5>^2 projectively")
                    mapped = np.full_like(c2, -1)
                    mapped[:, dst_idx] = np.where(c2 >= 0, (k_gal * (c2 + ph_u[None, :])) % 5, -1)
                    nz_f = np.argmax(mapped >= 0, axis=1)
                    ref = mapped[np.arange(len(c2)), nz_f][:, None]
                    mapped = np.where(mapped >= 0, (mapped - ref) % 5, -1).astype(np.int8)
                    perms200.append([row_bytes[mapped[i].tobytes()] for i in range(len(c2))])
    perms200 = np.array(perms200, dtype=np.int32)
    perm_set = {perms200[i].tobytes() for i in range(len(perms200))}
    if len(perm_set) != 200:
        raise AssertionError("Galois-Clifford symmetry group does not have order 200")
    # Explicit group-closure check across generators (c=2 scaling, swap, x0+1, x1+1) on all 200 elements:
    for gen_idx in (1, 5, 25, 50):
        gen_p = perms200[gen_idx]
        if not all(gen_p[perms200[i]].tobytes() in perm_set for i in range(len(perms200))):
            raise AssertionError("perms200 is not closed under composition")

    orb_rep = np.min(perms200, axis=0)
    reps = sorted(int(x) for x in set(orb_rep))
    D2 = w5_lut[c2 + 1]
    psi2 = np.array([w5_lut[int(target_exp2[i]) + 1] for i in range(25)], dtype=np.int64)

    Q1 = (D2[:, 1:] - np.outer(D2[:, 0], psi2[1:])) % P
    if not np.all(np.any(Q1 != 0, axis=1)):
        raise AssertionError("Rank-1 state found for |T5>^2")

    for piv in reps:
        u = Q1[piv]
        c0 = int(np.flatnonzero(u)[0])
        un = (u * pow(int(u[c0]), P - 2, P)) % P
        cols = [c for c in range(24) if c != c0]
        W2 = (Q1[:, cols] - np.outer(Q1[:, c0], un[cols])) % P
        act, Wn = canon_mod_rows(W2)
        if len(act) < len(Q1) - 1:
            raise AssertionError("Rank-2 decomposition found for |T5>^2")
        _, u_st, u_cnt = np.unique(Wn, axis=0, return_index=True, return_counts=True)
        for ui in u_st[u_cnt >= 2]:
            grp = [piv] + [int(x) for x in act[np.all(Wn == Wn[ui], axis=1)]]
            if rank_mod_p(np.vstack([D2[grp], psi2])) == rank_mod_p(D2[grp]):
                raise AssertionError(f"Rank-3 decomposition found for |T5>^2: {grp}")

    rng = np.random.default_rng(20261111)
    hw22 = rng.integers(1, P - 1, size=22, dtype=np.int64)
    workers = max(1, min(4, os.cpu_count() or 1))
    total_pairs = 0
    true_r4 = []
    with ProcessPoolExecutor(max_workers=workers, initializer=_init_worker,
                             initargs=(Q1, orb_rep, perms200, hw22)) as ex:
        for npairs, cands in ex.map(_scan_pivot_r4, reps):
            total_pairs += npairs
            for grp in cands:
                rk_s = rank_mod_p(D2[list(grp)])
                rk_sp = rank_mod_p(np.vstack([D2[list(grp)], psi2]))
                if rk_sp == rk_s:
                    true_r4.append(grp)

    if true_r4:
        print(f"RANK-4 DECOMPOSITION FOUND: {true_r4[0]}", file=sys.stderr)
        return 1

    print(f"exact F_P check (P={P} > 5^10={hadamard_bound}): {len(reps)} Galois-Clifford orbits, "
          f"{total_pairs} (pivot, partner) pairs, 0 rank <= 4 decompositions [{time.time() - t0:.2f}s]")
    for m in (2, 3, 4, 5):
        print(f"CERTIFIED chi(T5^{m}) >= 5")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
