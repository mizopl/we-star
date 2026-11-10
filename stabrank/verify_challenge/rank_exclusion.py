"""Exhaustive rank-2 and rank-3 exclusion by quotienting out the target.

A lower bound chi(psi) >= r + 1 says that no r stabilizer states span psi.
For r = 2 and r = 3 the whole dictionary of stabilizer states is small enough
to settle this by enumeration, if the enumeration is organised so that the
work is linear or quadratic in the dictionary rather than a binomial in it.

The organising fact is one quotient at a time. If psi lies in
span(s_1, ..., s_r) then the images of the s_j in C^d / span(psi) are linearly
dependent. For r = 2 that is two parallel directions, found by canonicalising
every direction and sorting once. For r = 3, fix the first state s_i as a pivot
and quotient by span(psi, s_i) as well: if psi is in span(s_i, s_j, s_k) then
the images of s_j and s_k in that second quotient are parallel, which is the
same sort, done once per pivot. The converse fails only when the three states
are themselves dependent, which is why every candidate is retested in the full
space. Every triple has a smallest index, so pivots only look at states with a
larger index and each triple is examined once.

Sorting finds parallel directions through a key that is constant on a
projective point: with u the unit direction, key = (KEY.u)/(CAN.u) for two fixed
generic functionals is unchanged by u -> lambda u. Parallel directions get equal
keys and land adjacent after sorting. The key is not injective on projective
points, though: it is constant on a whole hyperplane of directions, so an
unrelated direction can share a key exactly and sit between two parallel ones
in the sort order. Comparing only adjacent entries would then split the pair.
So the sorted keys are cut into runs wherever consecutive keys differ by more
than a relative 1e-8, and every pair inside a run is tested by its overlap.
Parallel directions have keys equal to rounding and always share a run; an
intruder can only enlarge a run, never separate its members. Runs are tiny
in practice, so the all-pairs test inside them costs nothing.

Before the sort, directions are pushed through a random linear map to a few
dimensions. A linear map preserves collinearity, so a genuine dependency is
still a dependency after projecting and the search cannot lose one; the map
can only propose extra candidates, and every candidate is then tested in the
full space by least squares. This is the same safeguard the T3 m=3 certificate
in this repository documents, and the projected dimension is kept well above
the value at which that certificate saw accidental near-parallel pairs.

Symmetry cuts the pivot loop by three orders of magnitude. The single-copy
Clifford stabilizer of the target (24 elements for the Strange state, 6 for
Norrell, 4 for H3, 3 for T3, 2 for the qubit H-type, 3 for the BK T-type),
the permutations of the copies, and one antiunitary symmetry generate a group
that fixes the target up to phase and permutes the dictionary; a decomposition
can be moved by any element of it onto one containing the representative of
any of its states, so only one pivot per orbit is needed, scanned against
every other state. Every generator is checked at runtime to fix the target
and to permute the dictionary. On three qutrits this leaves 12 (S), 74 (N)
or 116 (H3) pivots of 30240, and on four qubits 186 (H-type) or 62 (T-type)
of 36720.

Everything here is numerical and rests on a margin: the closest any two
non-parallel adjacent directions come to the parallel threshold is returned,
and a certificate should refuse to print its claim when that margin is thin.
The dictionaries themselves are exact up to rounding at 1e-16.
"""

from __future__ import annotations

import os
import sys
from concurrent.futures import ProcessPoolExecutor

import numpy as np

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

PARALLEL = 1e-6        # |<u, v>| above 1 - PARALLEL counts as parallel
MARGIN = 0.01          # an exclusion must clear the threshold by at least this
PROJ_DIM = 10          # random projection dimension for the per-pivot sort
RESID = 1e-9           # a candidate spans psi if its residual is below this


def _is_prime(p):
    return p >= 2 and all(p % q for q in range(2, int(p ** 0.5) + 1))


def _distinct_up_to_phase(raw, dim):
    """Collapse rows (or columns) of `raw` that agree up to a global phase,
    returning one column per state. The key is the vector divided by its
    first nonzero entry, rounded to six places, as in the qutrit path."""
    S = raw if raw.shape[1] == dim else raw.T
    seen = {}
    for row in S:
        pivot = row[np.flatnonzero(np.abs(row) > 1e-9)[0]]
        canon = np.round(row * (abs(pivot) / pivot), 6) + 0.0
        seen.setdefault(canon.real.tobytes() + canon.imag.tobytes(), row)
    return np.stack(list(seen.values()), axis=1)


def dictionary(p, n):
    """Every n-qudit stabilizer state for a prime p, one column each,
    distinct up to phase and unit norm.

    p = 2 closes the Clifford orbit of |0..0> (qubit_states), p = 3 uses the
    qutrit enumeration behind the T3 Galois bound, and an odd prime p >= 5
    lists the (flat, coset, phase-polynomial) triples of
    stabrank.stabilizer_extent and collapses the repeats up to a global
    phase. Every path is checked against p^n prod_{j<=n} (p^j + 1), which
    is 30 and 3900 for one and two ququints."""
    if p == 2:
        from qubit_states import all_states
        D = all_states(n)          # asserts the count itself
    elif p == 3:
        from stabrank.examples.t3_galois_lower_bound import distinct_states
        D = distinct_states(n)
    elif _is_prime(p):
        from stabrank.stabilizer_extent import enumerate_stabilizer_states
        D = _distinct_up_to_phase(enumerate_stabilizer_states(n, p), p ** n)
    else:
        raise ValueError("the local dimension p must be prime")
    want = p ** n
    for j in range(1, n + 1):
        want *= p ** j + 1
    if D.shape[1] != want:
        # Every exclusion is only as sound as the dictionary is complete.
        raise AssertionError(f"{D.shape[1]} states on {n} qudits of dimension {p}, "
                             f"expected {want}")
    return D / np.linalg.norm(D, axis=0)


def _orth(cols):
    """Orthonormal basis of the span of the given columns."""
    Q, _ = np.linalg.qr(np.column_stack(cols))
    return Q


def _parallel_groups(U, rng):
    """Groups of mutually parallel unit columns of U, and the closest approach
    to parallel among adjacent non-parallel pairs.

    Returns (groups, worst): groups is a list of index arrays each of size >= 2,
    worst is the largest adjacent overlap that was not counted as parallel.
    """
    n = U.shape[1]
    if n < 2:
        return [], 0.0
    for _attempt in range(8):
        can = rng.normal(size=U.shape[0]) + 1j * rng.normal(size=U.shape[0])
        key = rng.normal(size=U.shape[0]) + 1j * rng.normal(size=U.shape[0])
        c = can @ U
        # A direction the canonicalising functional nearly annihilates has no
        # usable key. Dropping it would silently remove it from every pair,
        # so redraw the functionals instead; a generic draw never hits this.
        if (np.abs(c) > 1e-9).all():
            break
    else:
        raise RuntimeError("could not draw a canonicalising functional that is "
                           "nonzero on every direction")
    kk = (key @ U) / c
    order = np.lexsort((kk.imag, kk.real))     # complex argsort is far slower
    ks = kk[order]
    # Cut the sorted keys into runs of (near-)equal key; parallel directions
    # share a run, and only pairs inside a run can be parallel.
    gap = np.abs(np.diff(ks)) > 1e-8 * (1 + np.abs(ks[:-1]))
    starts = np.concatenate(([0], np.flatnonzero(gap) + 1, [n]))
    # Adjacent overlaps across the whole order: the margin report says how
    # close any two neighbouring directions come to the parallel threshold.
    ov_adj = np.abs(np.sum(U[:, order[:-1]].conj() * U[:, order[1:]], axis=0))
    worst = float(ov_adj[ov_adj <= 1 - PARALLEL].max()) if (ov_adj <= 1 - PARALLEL).any() else 0.0
    groups = []
    for a, b in zip(starts[:-1], starts[1:]):
        if b - a < 2:
            continue
        members = order[a:b]
        V = U[:, members]
        G = np.abs(V.conj().T @ V)
        np.fill_diagonal(G, 0)
        par = G > 1 - PARALLEL
        off = G[~par & (G > 0)]
        if off.size:
            worst = max(worst, float(off.max()))
        # connected components of the parallel relation inside the run
        seen = np.zeros(b - a, bool)
        for s in range(b - a):
            if seen[s]:
                continue
            comp = [s]
            seen[s] = True
            stack = [s]
            while stack:
                v = stack.pop()
                for w in np.flatnonzero(par[v]):
                    if not seen[w]:
                        seen[w] = True
                        comp.append(w)
                        stack.append(w)
            if len(comp) >= 2:
                groups.append(members[comp])
    return groups, worst


def rank2_search(psi, D, seed=7):
    """Pairs (i, j) with psi in span(s_i, s_j), and the closest approach.

    Returns ("RANK1", 1.0) if some state is parallel to psi.
    """
    psi = psi / np.linalg.norm(psi)
    q = D - np.outer(psi, psi.conj() @ D)
    nq = np.linalg.norm(q, axis=0)
    if (nq <= 1e-9).any():
        return "RANK1", 1.0
    groups, worst = _parallel_groups(q / nq, np.random.default_rng(seed))
    pairs = [(int(g[a]), int(g[b])) for g in groups
             for a in range(len(g)) for b in range(a + 1, len(g))]
    return pairs, worst


class _Rank3Worker:
    """Per-process state for the pivot loop; built once per worker."""

    def __init__(self, psi, D, seed):
        self.psi = psi / np.linalg.norm(psi)
        self.D = D
        P = D - np.outer(self.psi, self.psi.conj() @ D)
        self.nP = np.linalg.norm(P, axis=0)
        self.P = P / np.where(self.nP > 0, self.nP, 1)
        rng = np.random.default_rng(seed)
        self.R = (rng.normal(size=(PROJ_DIM, D.shape[0]))
                  + 1j * rng.normal(size=(PROJ_DIM, D.shape[0])))
        self.RP = self.R @ self.P
        self.rng = np.random.default_rng(seed + 1)

    def pivots(self, plist, full):
        """Scan the given pivots. With `full`, every other state is a partner
        (used with symmetry representatives); otherwise only states of larger
        index are, since every triple is then met from its smallest member."""
        cands, worst, rank2 = [], 0.0, []
        N = self.P.shape[1]
        for i in plist:
            pi = self.P[:, i]
            if full:
                rest = np.concatenate((np.arange(0, i), np.arange(i + 1, N)))
            else:
                rest = np.arange(i + 1, N)
            ov = pi.conj() @ self.P[:, rest]
            q = self.RP[:, rest] - np.outer(self.R @ pi, ov)
            # full-space norm of the quotient direction, for the zero test
            nq_full = np.sqrt(np.maximum(1 - np.abs(ov) ** 2, 0))
            zero = nq_full < 1e-7
            if zero.any():
                rank2 += [(int(i), int(rest[j])) for j in np.flatnonzero(zero)]
            keep = ~zero
            nq = np.linalg.norm(q, axis=0)
            if (nq[keep] <= 1e-12).any():
                # A nonzero quotient direction that the random projection maps
                # to (nearly) zero: probability zero for a generic map, and if
                # it happens the search must not silently proceed without it.
                raise RuntimeError("random projection annihilated a direction; "
                                   "rerun with another seed")
            U = q[:, keep] / nq[keep]
            ids = rest[keep]
            groups, w = _parallel_groups(U, self.rng)
            worst = max(worst, w)
            for g in groups:
                g = ids[g]
                for a in range(len(g)):
                    for b in range(a + 1, len(g)):
                        cands.append((int(i), int(g[a]), int(g[b])))
        return cands, worst, rank2


_WORKER = None


def _init(psi, D, seed):
    global _WORKER
    _WORKER = _Rank3Worker(psi, D, seed)


def _run(job):
    return _WORKER.pivots(*job)


def rank3_search(psi, D, workers=None, seed=7, pivots=None):
    """Triples spanning psi, with diagnostics.

    With `pivots` given (indices of one representative per orbit of a
    symmetry group of psi acting on the dictionary), only those pivots are
    scanned, against every other state. Any decomposition can be moved by a
    symmetry onto one containing a representative, so nothing is lost; see
    `symmetry_orbit_reps`.

    Returns a dict with keys
      found:      list of (indices, coefficients) for triples that span psi
      rank2:      pairs found to span psi along the way (should be empty
                  when rank 2 has already been excluded)
      candidates: number of collinear-in-quotient triples tested
      min_resid:  smallest least-squares residual among candidates that
                  were not counted as decompositions
      worst:      closest approach to parallel among non-parallel directions
    Zero-norm quotient directions at the first stage (a state parallel to psi)
    are reported through rank2 as well, as ("RANK1", j).
    """
    N = D.shape[1]
    psi = psi / np.linalg.norm(psi)
    P = D - np.outer(psi, psi.conj() @ D)
    nP = np.linalg.norm(P, axis=0)
    out = {"found": [], "rank2": [], "candidates": 0, "min_resid": np.inf, "worst": 0.0}
    if (nP <= 1e-9).any():
        out["rank2"] = [("RANK1", int(j)) for j in np.flatnonzero(nP <= 1e-9)]
        return out
    workers = workers or max(1, min(8, (os.cpu_count() or 2) - 1))
    if pivots is None:
        # Balance work: pivot i costs N - i, so split by area rather than by count.
        cuts = [0]
        total = N * (N - 1) / 2
        for k in range(1, workers):
            target = total * k / workers
            i = int(N - np.sqrt(max(N * N - 2 * target, 0)))
            cuts.append(min(max(i, cuts[-1]), N))
        cuts.append(N)
        jobs = [(np.arange(cuts[k], cuts[k + 1]), False)
                for k in range(workers) if cuts[k] < cuts[k + 1]]
    else:
        plist = np.asarray(pivots, dtype=np.int64)
        workers = max(1, min(workers, len(plist)))
        jobs = [(chunk, True) for chunk in np.array_split(plist, workers) if len(chunk)]
    cands, rank2 = [], []
    if workers == 1:
        _init(psi, D, seed)
        for job in jobs:
            c, w, r2 = _run(job)
            cands += c; rank2 += r2; out["worst"] = max(out["worst"], w)
    else:
        with ProcessPoolExecutor(max_workers=workers, initializer=_init,
                                 initargs=(psi, D, seed)) as ex:
            for c, w, r2 in ex.map(_run, jobs):
                cands += c; rank2 += r2; out["worst"] = max(out["worst"], w)
    out["rank2"] = rank2
    out["candidates"] = len(cands)
    out["dependent"] = 0
    if rank2:
        return out
    # Candidates are tested in the full space, vectorised over batches by
    # Gram-Schmidt. Most candidates are three stabilizer states that are
    # linearly dependent among themselves (three states in one two-dimensional
    # stabilizer subspace), which look collinear in every quotient. Their span
    # is two-dimensional, and rank 2 has just been excluded above (rank2 is
    # empty), so they cannot contain psi and are counted rather than solved.
    # For the independent ones the residual of psi against the span is exact
    # up to rounding, and anything that passes is re-solved alone.
    cand = np.array(cands, dtype=np.int64).reshape(-1, 3)
    for lo in range(0, len(cand), 200000):
        idx = cand[lo:lo + 200000]
        s1, s2, s3 = (D[:, idx[:, k]].T for k in range(3))     # (batch, dim)
        u1 = s1
        v2 = s2 - np.sum(u1.conj() * s2, axis=1)[:, None] * u1
        n2 = np.linalg.norm(v2, axis=1)
        good = n2 > 1e-9
        u2 = v2 / np.where(good, n2, 1)[:, None]
        v3 = s3 - np.sum(u1.conj() * s3, axis=1)[:, None] * u1 \
                - np.sum(u2.conj() * s3, axis=1)[:, None] * u2
        n3 = np.linalg.norm(v3, axis=1)
        indep = good & (n3 > 1e-9)
        out["dependent"] += int((~indep).sum())
        u3 = v3 / np.where(indep, n3, 1)[:, None]
        r = psi[None, :] - sum(np.sum(u.conj() * psi[None, :], axis=1)[:, None] * u
                               for u in (u1, u2, u3))
        res = np.linalg.norm(r, axis=1)
        res = np.where(indep, res, np.inf)
        hit = res < RESID
        for cols in idx[hit]:
            A1 = D[:, cols]
            x, *_ = np.linalg.lstsq(A1, psi, rcond=None)
            r1 = float(np.linalg.norm(A1 @ x - psi))
            if r1 < RESID:
                out["found"].append(([int(c) for c in cols], x))
            else:
                out["min_resid"] = min(out["min_resid"], r1)
        rest = res[indep & ~hit]
        if rest.size:
            out["min_resid"] = min(out["min_resid"], float(rest.min()))
    return out


# ------------------------------------------------------------- symmetry ----

def _closure(gens, dim, want):
    """The group generated by `gens` (unitaries on C^dim) mod phase, by
    breadth-first closure, checked against the expected order `want`."""
    def key(U):
        v = U.ravel()
        v = v / v[np.flatnonzero(np.abs(v) > 1e-9)[0]]
        return (np.round(v, 6) + 0.0).tobytes()

    I = np.eye(dim, dtype=complex)
    seen = {key(I): I}
    frontier = [I]
    while frontier:
        nxt = []
        for U in frontier:
            for g in gens:
                V = g @ U
                k = key(V)
                if k not in seen:
                    seen[k] = V
                    nxt.append(V)
        frontier = nxt
    if len(seen) != want:
        raise AssertionError(f"Clifford closure found {len(seen)} elements, expected {want}")
    return list(seen.values())


def clifford_group(p):
    """The single-qudit Clifford group mod phase, as unitaries, by closure.

    For an odd prime the generators are the Fourier transform, the phase
    gate diag(w^{j(j-1)/2}) and the shift X, and the group has
    p^3 (p^2 - 1) elements mod phase: 216 for qutrits, 3000 for ququints.
    For qubits H and S generate the 24 elements."""
    if p == 2:
        H = np.array([[1, 1], [1, -1]]) / np.sqrt(2)
        S = np.diag([1, 1j])
        gens = [H, S]
    elif _is_prime(p):
        w = np.exp(2j * np.pi / p)
        F = np.array([[w ** (j * k) for k in range(p)] for j in range(p)]) / np.sqrt(p)
        S = np.diag([w ** ((j * (j - 1) // 2) % p) for j in range(p)])
        X = np.roll(np.eye(p), 1, axis=0)
        gens = [F, S, X]
    else:
        raise ValueError("p must be prime")
    return _closure(gens, p, 24 if p == 2 else p ** 3 * (p * p - 1))


def qubit_clifford_order(n):
    """|C_n / U(1)| = 2^(n^2 + 2n) prod_{j<=n} (4^j - 1): 24, 11520, 92897280."""
    t = 2 ** (n * n + 2 * n)
    for j in range(1, n + 1):
        t *= 4 ** j - 1
    return t


def local_clifford_group(orbit):
    """The Clifford group of one copy of the orbit state, mod phase.

    For a single-qudit orbit this is `clifford_group(p)`. For a qubit orbit
    of width w (CS, w = 2) it is the w-qubit Clifford group, closed from
    H_i, S_i and CNOT_ij and checked against 2^(w^2 + 2w) prod (4^j - 1),
    which is 11,520 for two qubits; three qubits (92,897,280) is not
    closable this way, so a width-3 orbit would need generators of the
    target's stabilizer instead."""
    from stabrank_verify import ORBIT_P, ORBIT_WIDTH
    p, w = ORBIT_P[orbit], ORBIT_WIDTH.get(orbit, 1)
    if w == 1:
        return clifford_group(p)
    if p != 2:
        raise ValueError("multi-qudit orbits are implemented for qubits only")
    if w > 2:
        raise ValueError("the three-qubit Clifford group is too large to close; "
                         "a width-3 orbit needs an explicit stabilizer generating set")
    from qubit_states import _clifford_generators
    return _closure(_clifford_generators(w), 2 ** w, qubit_clifford_order(w))


def _copy_permutation(perm, p, m, width=1):
    """The unitary permuting the m copies by `perm`, as a p^n x p^n matrix
    with n = width * m: each copy is a block of `width` qudits and the
    blocks move whole."""
    n = width * m
    dim = p ** n
    M = np.zeros((dim, dim))
    for src in range(dim):
        x = [(src // p ** (n - 1 - k)) % p for k in range(n)]
        y = [x[perm[k // width] * width + k % width] for k in range(n)]
        dst = sum(y[k] * p ** (n - 1 - k) for k in range(n))
        M[dst, src] = 1
    return M


def symmetry_orbit_reps(orbit, m, D, antiunitary=True):
    """One representative per orbit of the dictionary under a symmetry group
    of |M>^m, with the group's order and the orbit count.

    With antiunitary=False the group is the unitary part only. The slice-and-
    lift test needs that: a unitary symmetry of |M>^m acts on |M>^(m+1) as
    I (x) U and preserves slices, while the antiunitary one mixes them.

    The group is generated by the single-copy Clifford stabilizer of |M>
    acting on the first copy, the permutations of the copies, and one
    antiunitary symmetry (a Clifford composed with complex conjugation) when
    the state has one. For a width-w orbit (CS, w = 2) a copy is a block of
    w qubits: the local group is the w-qubit Clifford group (24 elements fix
    |CS> up to phase), the copy permutations move blocks whole, and the
    dictionary is the one on w m qubits. Every generator is checked here to
    fix |M>^m up to a phase and to permute the dictionary, so a wrong
    generator raises rather than silently shrinking the search.

    Why one pivot per orbit suffices: a symmetry g carries a decomposition
    psi = sum c_j s_j to psi = sum c'_j (g s_j) (with c' = c or its
    conjugate), and g s_j is again a stabilizer state. If some decomposition
    contains a state s, pick g with g s = the representative of s's orbit;
    the image decomposition contains the representative and is found when
    that representative is the pivot with every other state as a partner.
    """
    import math
    from stabrank_verify import orbit_state, ORBIT_P, ORBIT_WIDTH
    p = ORBIT_P[orbit]
    width = ORBIT_WIDTH.get(orbit, 1)
    N = D.shape[1]
    psi1 = np.array([complex(x) for x in orbit_state(orbit)]).ravel()
    psi1 /= np.linalg.norm(psi1)
    psi = psi1
    for _ in range(m - 1):
        psi = np.kron(psi, psi1)
    if D.shape[0] != len(psi):
        raise ValueError(f"dictionary on {D.shape[0]} amplitudes does not match "
                         f"{m} copies of {orbit} on {width * m} qudits ({len(psi)})")
    G = local_clifford_group(orbit)
    uni = [U for U in G if abs(abs(np.vdot(psi1, U @ psi1)) - 1) < 1e-9]
    anti = [U for U in G if abs(abs(np.vdot(psi1, U @ psi1.conj())) - 1) < 1e-9]
    if not antiunitary:
        anti = []

    def key(v):
        v = v / v[np.flatnonzero(np.abs(v) > 1e-9)[0]]
        return (np.round(v, 6) + 0.0).tobytes()

    index = {key(D[:, i]): i for i in range(N)}
    if len(index) != N:
        raise AssertionError("dictionary states are not distinct up to phase")
    I = np.eye(p ** width, dtype=complex)
    gens = []
    for U in uni:
        g = U
        for _ in range(m - 1):
            g = np.kron(g, I)
        gens.append((g, False))
    if m >= 2:
        gens.append((_copy_permutation((1, 0) + tuple(range(2, m)), p, m, width), False))
        gens.append((_copy_permutation(tuple(range(1, m)) + (0,), p, m, width), False))
    if anti:
        g = anti[0]
        for _ in range(m - 1):
            g = np.kron(g, anti[0])
        gens.append((g, True))
    perms = []
    for g, is_anti in gens:
        target = g @ (psi.conj() if is_anti else psi)
        if abs(abs(np.vdot(psi, target)) - 1) > 1e-9:
            raise AssertionError("a proposed symmetry does not fix the target up to phase")
        img = g @ (D.conj() if is_anti else D)
        try:
            pm = np.array([index[key(img[:, i])] for i in range(N)])
        except KeyError:
            raise AssertionError("a proposed symmetry does not map the dictionary to itself")
        if len(np.unique(pm)) != N:
            raise AssertionError("a proposed symmetry is not a permutation of the dictionary")
        perms.append(pm)
    parent = np.arange(N)

    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    for pm in perms:
        for a in range(N):
            ra, rb = find(a), find(int(pm[a]))
            if ra != rb:
                parent[ra] = rb
    roots = np.array([find(a) for a in range(N)])
    reps = np.unique(roots)
    order = (2 if anti else 1) * len(uni) ** m * math.factorial(m)
    return reps, {"order": order, "orbits": len(reps), "local": len(uni),
                  "antiunitary": bool(anti), "roots": roots, "perms": perms}


def psi_for(orbit, m):
    from stabrank_verify import target_vector
    return np.array([complex(x) for x in target_vector(orbit, m)]).ravel()


def certify_rank3(orbit, m, D, label=None, workers=None, symmetry=True):
    """Run the rank-3 exclusion for one cell and print a report.

    Returns True when no rank <= 3 decomposition exists and the margin is
    adequate, False otherwise. The caller decides what claim to print.
    """
    label = label or f"{orbit} m={m}"
    psi = psi_for(orbit, m)
    pivots = None
    if symmetry:
        pivots, info = symmetry_orbit_reps(orbit, m, D)
        print(f"{label}: symmetry group of order {info['order']} "
              f"({info['local']} local Cliffords per copy, copy permutations"
              f"{', one antiunitary' if info['antiunitary'] else ''}) splits the "
              f"{D.shape[1]} states into {info['orbits']} orbits; one pivot each")
    r = rank3_search(psi, D, workers=workers, pivots=pivots)
    if r["rank2"]:
        print(f"{label}: rank <= 2 decomposition FOUND via {r['rank2'][:3]}")
        return False
    if r["found"]:
        cols, x = r["found"][0]
        print(f"{label}: rank-3 decomposition FOUND, states {cols}, "
              f"coefficients {np.round(x, 6)}")
        return False
    slack = (1 - PARALLEL) - r["worst"]
    indep = r["candidates"] - r["dependent"]
    resid = (f" (smallest residual {r['min_resid']:.4f})"
             if np.isfinite(r["min_resid"]) else "")
    print(f"{label}: {r['candidates']} collinear candidates, of which "
          f"{r['dependent']} are three states of one two-dimensional span and "
          f"{indep} are independent triples; none spans the target{resid}. "
          f"Closest approach to parallel {r['worst']:.6f}, clearing the "
          f"threshold by {slack:.4f}.")
    if slack < MARGIN:
        print(f"{label}: margin too thin to stand behind", file=sys.stderr)
        return False
    return True


def control_rank3(orbit, m, D, label=None, symmetry=True):
    """A cell with a known rank-3 decomposition; the search must find it."""
    label = label or f"{orbit} m={m}"
    pivots = symmetry_orbit_reps(orbit, m, D)[0] if symmetry else None
    r = rank3_search(psi_for(orbit, m), D, pivots=pivots)
    if not r["found"]:
        print(f"positive control FAILED: no rank-3 decomposition found for "
              f"{label}, where one is known; the search is broken", file=sys.stderr)
        return False
    print(f"positive control: {label} found {len(r['found'])} rank-3 "
          f"decomposition(s), as expected")
    return True


def run_certificate(cells, controls, workers=None, also=()):
    """Drive a certificate script: controls first, then each cell, and print
    one CERTIFIED line per cell that survives.

    cells:    (orbit, m) pairs whose rank-3 exclusion is the claim, printed as
              CERTIFIED chi(orbit^m) >= 4
    controls: (orbit, m) pairs with a known rank-3 decomposition; the search
              must find each or the script exits non-zero without claiming.
    also:     extra (orbit, m, rank) claims that follow from the cells by the
              projection lemma (see cert_*_from_*.py), printed only when every
              cell passed.

    Returns a process exit code.
    """
    dicts = {}

    def dict_for(orbit, m):
        from stabrank_verify import ORBIT_P, orbit_qudits
        key = (ORBIT_P[orbit], orbit_qudits(orbit, m))
        if key not in dicts:
            dicts[key] = dictionary(*key)
            unit = {2: "qubit", 3: "qutrit", 5: "ququint"}.get(key[0], f"qudit(p={key[0]})")
            print(f"{key[1]} {unit}s: {dicts[key].shape[1]} stabilizer states")
        return dicts[key]

    for orbit, m in controls:
        if not control_rank3(orbit, m, dict_for(orbit, m)):
            return 1
    print()
    ok = True
    for orbit, m in cells:
        if not certify_rank3(orbit, m, dict_for(orbit, m), workers=workers):
            ok = False
            continue
        print(f"CERTIFIED chi({orbit}^{m}) >= 4")
    if ok:
        for orbit, m, rank in also:
            print(f"CERTIFIED chi({orbit}^{m}) >= {rank}")
    return 0 if ok else 1
