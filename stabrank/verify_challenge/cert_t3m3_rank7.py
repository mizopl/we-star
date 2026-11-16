"""Certificate: chi(|T3>^{ot 3}) >= 7, by eliminating every rank-6 configuration exactly.

The argument has three parts, and every rejection is in exact arithmetic.

1. Descent to Q(w3).  |T3>^{ot 3} has entries w9^{f(x)} with f(x) = x1 + x2 + x3
   taken as an integer in 0..6.  Writing f = r + 3q, the vector is
   psi_0 + w9 psi_1 + w9^2 psi_2 (up to the normalisation 27^{-1/2}) with psi_r
   supported on the coset {f = r mod 3} and entries w3^q.  A stabilizer state is
   a vector over Z[w3], so a span of stabilizer states is defined over Q(w3) and
   contains |T3>^{ot 3} iff it contains all three psi_r (this is the Galois
   argument of cert_t3_galois.py, made explicit; V_3 = span{psi_0, psi_1, psi_2}
   and dim V_3 = 3 because the supports are disjoint).  The whole problem is now
   over Q(w3): find six stabilizer states whose span contains V_3.

2. Geometry mod ell.  Six states spanning a space that contains V_3 have images
   in Q(w3)^27 / V_3 spanning at most 3 dimensions.  Everything is reduced mod
   ell = 65521 (a prime that is 1 mod 3, so w3 has an image); reduction can only
   lower a rank, so every genuine configuration is still one mod ell, and a
   random linear projection to F_ell^6 preserves linear dependence, so the scan
   finds a superset of the true configurations and cannot lose one.  A first
   pivot i runs over orbit representatives of the symmetry group of V_3 (the
   1458 monomial Cliffords that map V_3 to itself, and their compositions with
   complex conjugation, which also fixes the dictionary and V_3; 2916 elements,
   45 orbits on the 30240 states).  The second pivot j is the least index among
   the other five, taken minimal in its orbit under the stabilizer of i; the
   remaining four have images that vanish or are mutually parallel modulo
   span(q_i, q_j), which is found by hashing canonical coordinates.

3. Exact decision.  All members of such a class lie in one 6-dimensional space
   containing V_3, so V_3 lies in the span of some six of them iff it lies in the
   span of the whole class set.  That is decided by comparing the rank of the
   class set with the rank of the class set together with psi_0, psi_1, psi_2,
   both computed mod ell2 = 2^31 - 1.  Because every entry is 0 or a root of
   unity, a k x k minor has modulus at most k^{k/2} (Hadamard), which is below
   sqrt(ell2) for k <= 9; an element of Z[w3] of norm below ell2 that maps to 0
   in F_ell2 is 0, so a rank value <= 8 computed mod ell2 is the rank over
   Q(w3).  No candidate needed anything else.

A rank-r decomposition with r < 6 padded by any 6 - r further states is a
rank-6 configuration in the above sense, so the scan covers every rank <= 6.
As a positive control the same code is run at m = 2, where exactly three states
lie in V_2 and span it (the known chi(|T3>^{ot 2}) = 3), and the two-pivot scan
for five-state configurations must report class sets whose span contains V_2.

Printed claim: CERTIFIED chi(T3^3) >= 7
"""
from __future__ import annotations

import itertools
import os
import sys
import time
from concurrent.futures import ProcessPoolExecutor

for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS", "NUMEXPR_NUM_THREADS"):
    os.environ.setdefault(_v, "1")

import numpy as np
from numba import njit, int64, uint64

ELL = 65521                    # prime, 1 mod 6
ELL2 = 2 ** 31 - 1             # prime, 1 mod 6; ranks <= 8 mod ELL2 are exact (Hadamard)
NOSUPP = 6
T0 = time.time()


def log(msg):
    print(f"[{time.time() - T0:6.1f}s] {msg}", flush=True)


def _root(order, ell):
    for g in range(2, ell):
        z = pow(g, (ell - 1) // order, ell)
        if all(pow(z, order // q, ell) != 1 for q in (2, 3) if order % q == 0):
            return z
    raise RuntimeError


Z6 = _root(6, ELL)
Z6_2 = _root(6, ELL2)
for _z, _l in ((Z6, ELL), (Z6_2, ELL2)):
    _w3 = pow(_z, 2, _l)
    assert (_w3 * _w3 + _w3 + 1) % _l == 0 and pow(_z, 3, _l) == _l - 1
INV = np.zeros(ELL, dtype=np.int64)
INV[1:] = [pow(x, ELL - 2, ELL) for x in range(1, ELL)]


# ------------------------------------------------------------ dictionary ----

def enumerate_terms(m, p=3):
    """Every m-qutrit stabilizer state once: RREF flat W, coset x0 on non-pivots,
    phase polynomial Q (upper triangular) and l, as in stabrank_verify."""
    for k in range(m + 1):
        for pivots in itertools.combinations(range(m), k):
            nonp = [c for c in range(m) if c not in pivots]
            free_pos = [(r, c) for r in range(k) for c in nonp if c > pivots[r]]
            for free in itertools.product(range(p), repeat=len(free_pos)):
                W = [[0] * m for _ in range(k)]
                for r in range(k):
                    W[r][pivots[r]] = 1
                for (r, c), v in zip(free_pos, free):
                    W[r][c] = v
                for x0f in itertools.product(range(p), repeat=m - k):
                    x0 = [0] * m
                    for c, v in zip(nonp, x0f):
                        x0[c] = v
                    ut = [(i, j) for i in range(k) for j in range(i, k)]
                    for qv in itertools.product(range(p), repeat=len(ut)):
                        Q = [[0] * k for _ in range(k)]
                        for (i, j), v in zip(ut, qv):
                            Q[i][j] = v
                        for lv in itertools.product(range(p), repeat=k):
                            yield k, x0, W, Q, list(lv)


def term_exponents(k, x0, W, Q, l, m, p=3):
    out = np.full(p ** m, NOSUPP, dtype=np.int8)
    for y in itertools.product(range(p), repeat=k):
        x = [(x0[c] + sum(y[r] * W[r][c] for r in range(k))) % p for c in range(m)]
        pos = 0
        for c in range(m):
            pos = pos * p + x[c]
        assert out[pos] == NOSUPP
        e = sum(Q[i][j] * y[i] * y[j] for i in range(k) for j in range(i, k))
        e += sum(l[i] * y[i] for i in range(k))
        out[pos] = (2 * (e % p)) % 6
    return out


def build_dictionary(m):
    E = np.stack([term_exponents(*t, m) for t in enumerate_terms(m)])
    expected = 3 ** m
    for j in range(1, m + 1):
        expected *= 3 ** j + 1
    assert E.shape[0] == expected, (E.shape[0], expected)
    return E


def canon_rows(E):
    E = E.copy()
    supp = E != NOSUPP
    first = np.argmax(supp, axis=1)
    shift = E[np.arange(E.shape[0]), first]
    E[supp] = ((E - shift[:, None])[supp]) % 6
    return E


def row_keys(E):
    return [r.tobytes() for r in canon_rows(E)]


def to_mod(E, z6, ell):
    tab = np.array([pow(z6, e, ell) for e in range(6)] + [0], dtype=np.int64)
    return tab[E.astype(np.int64)]


def t3_targets(m):
    dim = 3 ** m
    T = np.full((3, dim), NOSUPP, dtype=np.int8)
    for pos in range(dim):
        x, t = [], pos
        for _ in range(m):
            x.append(t % 3)
            t //= 3
        f = sum(x)
        T[f % 3, pos] = (2 * (f // 3)) % 6
    return T


# ---------------------------------------------------- linear algebra mod ell ---

def rank_mod(M, ell):
    A = M.copy() % ell
    rows, cols = A.shape
    r = 0
    for c in range(cols):
        nz = np.flatnonzero(A[r:, c])
        if len(nz) == 0:
            continue
        pr = r + nz[0]
        if pr != r:
            A[[r, pr]] = A[[pr, r]]
        A[r] = (A[r] * pow(int(A[r, c]), ell - 2, ell)) % ell
        f = A[:, c].copy()
        f[r] = 0
        A = (A - np.outer(f, A[r])) % ell
        r += 1
        if r == rows:
            break
    return r


def quotient_projection(Vl, Tl, D, seed):
    """Images of the rows of Vl in F_ell^dim / span(Tl), randomly projected to F_ell^D."""
    R_, dim = Tl.shape
    piv = []
    for r in range(R_):
        c = next(c for c in range(dim) if Tl[r, c] != 0
                 and all(Tl[s, c] == 0 for s in range(R_) if s != r))
        piv.append(c)
    Vq = Vl.copy() % ELL
    for r in range(R_):
        c = (Vq[:, piv[r]] * INV[Tl[r, piv[r]]]) % ELL
        Vq = (Vq - np.outer(c, Tl[r])) % ELL
    assert np.all(Vq[:, piv] == 0)
    keep = [c for c in range(dim) if c not in piv]
    Vq = Vq[:, keep]
    rng = np.random.default_rng(seed)
    Rm = rng.integers(0, ELL, size=(D, Vq.shape[1]), dtype=np.int64)
    return (Vq @ Rm.T) % ELL


# ------------------------------------------------------------- symmetry ----

def _affine_index_map(A, b, m, p=3):
    dim = p ** m
    perm = np.empty(dim, dtype=np.int64)
    for pos in range(dim):
        x, t = [], pos
        for _ in range(m):
            x.append(t % p)
            t //= p
        x = x[::-1]
        xp = [(sum(A[i][j] * x[j] for j in range(m)) + b[i]) % p for i in range(m)]
        q = 0
        for c in range(m):
            q = q * p + xp[c]
        perm[pos] = q
    return perm


def _rank_mod_p(M, p):
    A = M.copy() % p
    rows, cols = A.shape
    r = 0
    for c in range(cols):
        pr = next((i for i in range(r, rows) if A[i, c] % p), None)
        if pr is None:
            continue
        A[[r, pr]] = A[[pr, r]]
        A[r] = (A[r] * pow(int(A[r, c]), -1, p)) % p
        for i in range(rows):
            if i != r and A[i, c]:
                A[i] = (A[i] - A[i, c] * A[r]) % p
        r += 1
    return r


def _monomial_matrix(m, p=3):
    mons = [tuple([0] * m)]
    for i in range(m):
        e = [0] * m
        e[i] = 1
        mons.append(tuple(e))
    for i in range(m):
        for j in range(i, m):
            e = [0] * m
            e[i] += 1
            e[j] += 1
            mons.append(tuple(e))
    dim = p ** m
    X = np.zeros((dim, len(mons)), dtype=np.int64)
    for pos in range(dim):
        x, t = [], pos
        for _ in range(m):
            x.append(t % p)
            t //= p
        x = x[::-1]
        for a, e in enumerate(mons):
            v = 1
            for xi, ei in zip(x, e):
                v *= xi ** ei
            X[pos, a] = v % p
    return X


def _solve_mod_p(A, rhs, p):
    A = A.copy() % p
    rhs = rhs.copy() % p
    rows, cols = A.shape
    piv_cols = []
    r = 0
    for c in range(cols):
        pr = next((i for i in range(r, rows) if A[i, c]), None)
        if pr is None:
            continue
        A[[r, pr]] = A[[pr, r]]
        rhs[[r, pr]] = rhs[[pr, r]]
        inv = pow(int(A[r, c]), -1, p)
        A[r] = (A[r] * inv) % p
        rhs[r] = (rhs[r] * inv) % p
        for i in range(rows):
            if i != r and A[i, c]:
                f = A[i, c]
                A[i] = (A[i] - f * A[r]) % p
                rhs[i] = (rhs[i] - f * rhs[r]) % p
        piv_cols.append(c)
        r += 1
        if r == rows:
            break
    if any(rhs[r:] % p):
        return None
    part = np.zeros(cols, dtype=np.int64)
    for i, c in enumerate(piv_cols):
        part[c] = rhs[i]
    null = []
    for fc in [c for c in range(cols) if c not in piv_cols]:
        z = np.zeros(cols, dtype=np.int64)
        z[fc] = 1
        for i, c in enumerate(piv_cols):
            z[c] = (-A[i, fc]) % p
        null.append(z)
    return part, null


def monomial_symmetries(T, m, p=3):
    """All maps v -> w6^{Q(x')} v(A^{-1}(x' - b)) (and the same after complex
    conjugation) that permute the target rows up to scalars.  Q is found by
    solving a linear system over F_3, so the list is complete for this class."""
    R_, dim = T.shape
    supp = T != NOSUPP
    X = _monomial_matrix(m, p)
    nmon = X.shape[1]
    coset_of = np.full(dim, -1)
    for r in range(R_):
        coset_of[supp[r]] = r
    rows = [v for v in itertools.product(range(p), repeat=m) if any(v)]
    elements = []
    for mat in itertools.product(rows, repeat=m):
        A = np.array(mat, dtype=np.int64)
        if _rank_mod_p(A, p) < m:
            continue
        for b in itertools.product(range(p), repeat=m):
            perm = _affine_index_map(A, b, m, p)
            pi, ok = [], True
            for r in range(R_):
                img = perm[supp[r]]
                rp = coset_of[img[0]]
                if rp < 0 or not np.array_equal(np.sort(img), np.flatnonzero(supp[rp])):
                    ok = False
                    break
                pi.append(rp)
            if not ok or len(set(pi)) != R_:
                continue
            for s in (1, -1):
                rhs6 = np.zeros(dim, dtype=np.int64)
                which = np.full(dim, -1)
                for r in range(R_):
                    xs = np.flatnonzero(supp[r])
                    rhs6[perm[xs]] = (T[pi[r], perm[xs]].astype(int) - s * T[r, xs].astype(int)) % 6
                    which[perm[xs]] = pi[r]
                par, bad = {}, False
                for r in range(R_):
                    ps = set((rhs6[which == r] % 2).tolist())
                    if len(ps) != 1:
                        bad = True
                        break
                    par[r] = ps.pop()
                if bad:
                    continue
                rhs3 = np.zeros(dim, dtype=np.int64)
                for r in range(R_):
                    sel = which == r
                    rhs3[sel] = ((rhs6[sel] - par[r]) // 2) % 3
                idx = np.flatnonzero(which >= 0)
                Amat = np.zeros((len(idx), nmon + R_), dtype=np.int64)
                Amat[:, :nmon] = X[idx]
                for a, pos in enumerate(idx):
                    Amat[a, nmon + which[pos]] = 1
                sol = _solve_mod_p(Amat, rhs3[idx], p)
                if sol is None:
                    continue
                part, null = sol
                seen = set()
                for coeffs in itertools.product(range(p), repeat=len(null)):
                    z = part.copy()
                    for cf, nv in zip(coeffs, null):
                        z = (z + cf * nv) % p
                    qc = tuple(z[1:nmon].tolist())
                    if qc in seen:
                        continue
                    seen.add(qc)
                    Qexp = (2 * (X[:, 1:nmon] @ np.array(qc, dtype=np.int64))) % 6
                    elements.append((perm, s, Qexp.astype(np.int64)))
    return elements


def apply_element(E, elem):
    perm, s, Qexp = elem
    out = np.full_like(E, NOSUPP)
    supp = E != NOSUPP
    vals = (s * E.astype(np.int64) + Qexp[perm][None, :]) % 6
    out[:, perm] = np.where(supp, vals, NOSUPP)
    return out.astype(np.int8)


def target_image_ok(T, elem):
    """The element maps each target row to a scalar multiple of a target row."""
    img = apply_element(T, elem)
    keys = set(row_keys(T))
    return all(k in keys for k in row_keys(img))


# ---------------------------------------------------------------- kernels ---

TSIZE = 1 << 17
TMASK = TSIZE - 1
MULT = np.array([0x9E3779B97F4A7C15, 0xC2B2AE3D27D4EB4F, 0x165667B19E3779F9,
                 0x27D4EB2F165667C5, 0x94D049BB133111EB, 0xBF58476D1CE4E5B9,
                 0x2545F4914F6CDD1D, 0xD6E8FEB86659FD93], dtype=np.uint64)


@njit(cache=True)
def _hash(v, n):
    h = uint64(0x51ED270B27C6D0F5)
    for d in range(n):
        h ^= (uint64(v[d]) + uint64(0x9E37)) * MULT[d]
        h = (h ^ (h >> uint64(29))) * uint64(0xBF58476D1CE4E5B9)
    return h ^ (h >> uint64(32))


@njit(cache=True)
def _reduce_one(PD, inv, i, ell):
    N, D = PD.shape
    qi = PD[i]
    a = -1
    for d in range(D):
        if qi[d] != 0:
            a = d
            break
    ia = inv[qi[a]]
    Q1 = np.empty((N, D - 1), dtype=np.int64)
    for k in range(N):
        c = (PD[k, a] * ia) % ell
        col = 0
        for d in range(D):
            if d == a:
                continue
            Q1[k, col] = (PD[k, d] - c * qi[d]) % ell
            col += 1
    return Q1


@njit(cache=True)
def _group_keys(Q, inv, ell, kstart, exclude, isfree, keys, tkey, tcnt, tstamp, stamp, slot_of):
    N, Dq = Q.shape
    nzero = 0
    v = np.empty(Dq, dtype=np.int64)
    for k in range(kstart, N):
        if k == exclude or isfree[k] != 0:
            slot_of[k] = -1
            continue
        lead = -1
        for d in range(Dq):
            if Q[k, d] != 0:
                lead = d
                break
        if lead < 0:
            nzero += 1
            slot_of[k] = -2
            keys[k] = 0
            continue
        s = inv[Q[k, lead]]
        for d in range(Dq):
            v[d] = (Q[k, d] * s) % ell
        h = _hash(v, Dq)
        if h == 0:
            h = uint64(1)
        keys[k] = h
        slot = int64(h & uint64(TMASK))
        while True:
            if tstamp[slot] != stamp:
                tstamp[slot] = stamp
                tkey[slot] = h
                tcnt[slot] = 1
                break
            if tkey[slot] == h:
                tcnt[slot] += 1
                break
            slot = (slot + 1) & TMASK
        slot_of[k] = slot
    return nzero


@njit(cache=True)
def kernel2(PD, inv, i, jok, isfree, nfree, need, ell, max_out):
    """Two-pivot scan for first pivot i and second pivots j with jok[j] != 0, k > j.

    States with isfree[k] != 0 lie inside the target space (zero image); they are
    never pivots and are counted as free members of every class (nfree of them).
    States whose image is parallel to q_i (zero after reducing mod q_i) lie in
    span(V, s_i) and are likewise free for this pivot; they are returned in
    `par` so the caller can add them to every class of this pivot (there are
    none at m = 3, which the caller asserts).
    Returns candidate classes (j, nzero, nclass), their members (class id, k), par."""
    N, D = PD.shape
    out_cand = np.empty((max_out, 3), dtype=np.int64)
    out_memb = np.empty((max_out * 64, 2), dtype=np.int64)
    nc = 0
    nm = 0
    keys = np.zeros(N, dtype=np.uint64)
    tkey = np.zeros(TSIZE, dtype=np.uint64)
    tcnt = np.zeros(TSIZE, dtype=np.int64)
    tstamp = np.zeros(TSIZE, dtype=np.int64)
    slot_of = np.zeros(N, dtype=np.int64)
    stamp = 0
    Q1 = _reduce_one(PD, inv, i, ell)
    D1 = D - 1
    skip = isfree.copy()
    npar = 0
    for k in range(N):
        if k != i and isfree[k] == 0:
            z = True
            for d in range(D1):
                if Q1[k, d] != 0:
                    z = False
                    break
            if z:
                skip[k] = 1
                npar += 1
    par = np.empty(npar, dtype=np.int64)
    t = 0
    for k in range(N):
        if skip[k] != 0 and isfree[k] == 0 and k != i:
            par[t] = k
            t += 1
    nfree_all = nfree + npar
    Q2 = np.empty((N, D1 - 1), dtype=np.int64)
    for j in range(N):
        if j == i or jok[j] == 0 or skip[j] != 0:
            continue
        qj = Q1[j]
        b = -1
        for d in range(D1):
            if qj[d] != 0:
                b = d
                break
        ib = inv[qj[b]]
        for k in range(j + 1, N):
            c = (Q1[k, b] * ib) % ell
            col = 0
            for d in range(D1):
                if d == b:
                    continue
                Q2[k, col] = (Q1[k, d] - c * qj[d]) % ell
                col += 1
        stamp += 1
        nzero = _group_keys(Q2, inv, ell, j + 1, i, skip, keys, tkey, tcnt, tstamp, stamp, slot_of)
        nzero += nfree_all
        if nzero >= need and nc < max_out:
            out_cand[nc, 0] = j
            out_cand[nc, 1] = nzero
            out_cand[nc, 2] = 0
            for k in range(j + 1, N):
                if slot_of[k] == -2 and nm < out_memb.shape[0]:
                    out_memb[nm, 0] = nc
                    out_memb[nm, 1] = k
                    nm += 1
            nc += 1
        for k in range(j + 1, N):
            s = slot_of[k]
            if s < 0:
                continue
            if tcnt[s] > 0 and tcnt[s] + nzero >= need:
                if nc < max_out:
                    out_cand[nc, 0] = j
                    out_cand[nc, 1] = nzero
                    out_cand[nc, 2] = tcnt[s]
                    h = keys[k]
                    for kk in range(j + 1, N):
                        if slot_of[kk] == -2 or (slot_of[kk] >= 0 and keys[kk] == h):
                            if nm < out_memb.shape[0]:
                                out_memb[nm, 0] = nc
                                out_memb[nm, 1] = kk
                                nm += 1
                    nc += 1
                tcnt[s] = -1
    return out_cand[:nc], out_memb[:nm], par


# --------------------------------------------------------------- workers ---

_G = {}


def _init(PD, E2, T2, isfree):
    _G["PD"], _G["E2"], _G["T2"], _G["isfree"] = PD, E2, T2, isfree
    _G["free"] = [int(k) for k in np.flatnonzero(isfree)]


def _scan(args):
    i, jok, need = args
    isfree = _G["isfree"]
    c, mb, par = kernel2(_G["PD"], INV, int(i), jok, isfree, len(_G["free"]), need, ELL, 400000)
    assert c.shape[0] < 400000 and mb.shape[0] < 400000 * 64, "output buffer overflow"
    par = [int(k) for k in par]
    memb = {}
    for cid, k in mb:
        memb.setdefault(int(cid), []).append(int(k))
    classes = [(int(i), int(c[cid, 0]), int(c[cid, 1]), int(c[cid, 2]), memb.get(cid, []) + par)
               for cid in range(c.shape[0])]
    return classes, len(par)


def _decide(classes):
    """For each class set decide, exactly, whether span(T) is inside its span."""
    E2, T2 = _G["E2"], _G["T2"]
    found = []
    undecided = 0
    hist = {}
    for i, j, nz, ng, members in classes:
        cls = [i, j] + members + _G["free"]
        hist[(nz, ng)] = hist.get((nz, ng), 0) + 1
        S = E2[cls]
        rS = rank_mod(S, ELL2)
        rST = rank_mod(np.vstack([S, T2]), ELL2)
        if rS > 8 or rST > 8:
            undecided += 1          # Hadamard exactness does not cover this size
            continue
        if rST == rS:
            found.append((cls, rS))
    return found, undecided, hist


def decide_all(classes, ex, chunk=4000):
    found, undecided, hist = [], 0, {}
    chunks = [classes[a:a + chunk] for a in range(0, len(classes), chunk)]
    for f, u, h in ex.map(_decide, chunks):
        found.extend(f)
        undecided += u
        for k, v in h.items():
            hist[k] = hist.get(k, 0) + v
    return found, undecided, hist


# --------------------------------------------------------------- pipeline ---

def run(m, rank, ex, PD, E2, T2, reps, jok_of, N, allow_parallel):
    need = rank - 2
    classes, npar = [], 0
    for c, p in ex.map(_scan, [(i, jok_of[i], need) for i in reps]):
        classes.extend(c)
        npar += p
    assert allow_parallel or npar == 0, "two states parallel off V_3 mod ell (none exist over C)"
    log(f"m={m} rank={rank}: {len(classes)} candidate classes from {len(reps)} first pivots")
    found, undecided, hist = decide_all(classes, ex)
    assert undecided == 0, f"{undecided} classes too large for the exactness bound"
    return classes, found, hist


def symmetry(E, T, m, isfree):
    N = E.shape[0]
    elems = monomial_symmetries(T, m)
    assert all(target_image_ok(T, e) for e in elems)
    index = {k: i for i, k in enumerate(row_keys(E))}
    gmin = np.arange(N)
    stab = {}
    for e in elems:
        P = np.fromiter((index[k] for k in row_keys(apply_element(E, e))), dtype=np.int64, count=N)
        assert len(np.unique(P)) == N, "an element does not permute the dictionary"
        gmin = np.minimum(gmin, P)
        fixed = np.flatnonzero(P == np.arange(N))
        for i in fixed:
            stab.setdefault(int(i), []).append(P)
    reps = np.array([r for r in np.unique(gmin) if not isfree[r]])
    jok_of = {}
    for i in reps:
        imin = np.arange(N)
        for P in stab[int(i)]:
            imin = np.minimum(imin, P)
        jok_of[int(i)] = ((imin == np.arange(N)) & (isfree == 0)).astype(np.int8)
    return len(elems), reps, jok_of


def main():
    nw = max(1, min(8, (os.cpu_count() or 2) - 1))

    # -------------------------------------------- positive control at m = 2 ---
    m = 2
    E = build_dictionary(m)
    N = E.shape[0]
    T = t3_targets(m)
    Vl, Tl = to_mod(E, Z6, ELL), to_mod(T, Z6, ELL)
    PD = quotient_projection(Vl, Tl, 6, 2024)
    isfree = np.all(PD == 0, axis=1).astype(np.int8)
    inside = np.flatnonzero(isfree)
    assert len(inside) == 3, inside
    E2, T2 = to_mod(E, Z6_2, ELL2), to_mod(T, Z6_2, ELL2)
    r3 = rank_mod(E2[inside], ELL2)
    r3t = rank_mod(np.vstack([E2[inside], T2]), ELL2)
    assert r3 == 3 and r3t == 3, (r3, r3t)
    log(f"m=2 control: exactly 3 of {N} states lie in V_2 and span it, so chi(T3^2) = 3")
    nel, reps, jok_of = symmetry(E, T, m, isfree)
    with ProcessPoolExecutor(max_workers=nw, initializer=_init, initargs=(PD, E2, T2, isfree)) as ex:
        classes, found, hist = run(m, 5, ex, PD, E2, T2, reps, jok_of, N, True)
    # every class set carries the three states inside V_2 plus two pivots, so its
    # rank is at least 5; a genuine five-state span containing V_2 has rank exactly 5
    assert found, "m=2 control failed: no class set contains V_2"
    best = min(r for _, r in found)
    assert best == 5, f"m=2 control failed: minimal class-set rank {best}, expected 5"
    log(f"m=2 control: symmetry order {nel}, {len(reps)} orbits; {len(found)} of {len(classes)} "
        f"classes contain V_2 (minimal class-set rank 5), as expected")

    # ------------------------------------------------------ the theorem, m = 3 ---
    m = 3
    E = build_dictionary(m)
    N = E.shape[0]
    T = t3_targets(m)
    Vl, Tl = to_mod(E, Z6, ELL), to_mod(T, Z6, ELL)
    PD = quotient_projection(Vl, Tl, 6, 2024)
    isfree = np.all(PD == 0, axis=1).astype(np.int8)
    assert not isfree.any(), "a stabilizer state lies in V_3 mod ell"
    E2, T2 = to_mod(E, Z6_2, ELL2), to_mod(T, Z6_2, ELL2)
    log(f"m=3: dictionary of {N} states, V_3 of dimension 3, no state inside V_3")
    nel, reps, jok_of = symmetry(E, T, m, isfree)
    nj = sum(int(jok_of[int(i)].sum()) for i in reps)
    log(f"m=3: symmetry group of order {nel}, {len(reps)} orbits, {nj} (i, j) pivot pairs")
    with ProcessPoolExecutor(max_workers=nw, initializer=_init, initargs=(PD, E2, T2, isfree)) as ex:
        classes, found, hist = run(m, 6, ex, PD, E2, T2, reps, jok_of, N, False)
    log(f"m=3: class histogram by (zero members, parallel members): {dict(sorted(hist.items()))}")
    if found:
        best = min(found, key=lambda f: f[1])
        print(f"RANK-{best[1]} DECOMPOSITION EXISTS -> chi(T3^3) <= {best[1]}")
        print("  class set:", best[0])
        return 1
    print(f"no set of six stabilizer states spans V_3 (all {len(classes)} candidate classes "
          f"rejected exactly) => chi(T3^3) >= 7")
    print("CERTIFIED chi(T3^3) >= 7")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
