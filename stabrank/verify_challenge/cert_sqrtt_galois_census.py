"""Certificate: chi(|sqrtT>^{ot 4}) >= 5 and chi(|sqrtT>^{ot 5}) >= 6 for the
sqrt(T) state, exactly, and chi(|sqrtT>^{ot m}) >= 6 for 6 <= m <= 10 by
projection.

|sqrtT> = (|0> + zeta |1>)/sqrt 2 with zeta = exp(i pi/8). Write t_k for the
unnormalized vector (1, zeta^k)^{ot m}, so t_1 = sqrt(2)^m |sqrtT>^m. By the
Galois descent of cert_sqrtt_galois.py the span W of the terms of any exact
stabilizer decomposition of t_1 contains t_1, t_5, t_9, t_13 (every qubit
stabilizer state is a scalar times a vector over Z[i], and these four are the
images of t_1 under Gal(Q(zeta)/Q(i))), and for m >= 3 they are independent
(a Vandermonde in zeta, zeta^5, -zeta, -zeta^5 on one coordinate of each
Hamming weight 0, 1, 2, 3). Let V4 be their span. Since t_1 lies in V4, an
r-term decomposition exists exactly when r stabilizer states have a span
containing V4, that is, when r independent stabilizer states have residues
modulo V4 spanning an (r - 4)-dimensional space. Hence

  four terms exist iff the stabilizer states inside V4 span V4;
  five terms exist iff some five independent stabilizer states have pairwise
  parallel (or zero) residues modulo V4.

Arithmetic, all exact. The residue of a vector v modulo V4 is the unique
vector of v + V4 vanishing on the four pivot coordinates x = 0, 1, 3, 7 (the
strings of weights 0 to 3 that are initial segments of ones); it is a linear
function of v with coefficients in Q(zeta) whose denominators divide the
Vandermonde determinant. Everything is computed modulo two primes P == 1
(mod 16), with zeta mapped to a primitive sixteenth root of unity g mod P
and i to g^4, which is a ring homomorphism Z[zeta] -> F_P under which the
pivot block stays invertible. A stabilizer state's residue is reduced to a
projective key: the index of its first nonzero entry mod P and two random
F_P-linear functionals divided by that entry. If two residues are parallel
over Q(zeta), r' = lambda r with lambda in Q(zeta)^*, then modulo P either
lambda reduces to a nonzero element of F_P and the two keys coincide, or one
of the two residues vanishes mod P. So every exact five-term decomposition
lies inside one key class together with the zero set Z, taken as the union
over the two primes of the states whose residue vanishes mod P, and the
classes are taken jointly under both primes. A class is examined only when
its members have rank at least r modulo one of the primes; this loses
nothing, since a 5 x 5 minor of a matrix with entries in {0, +-1, +-i} has
norm at most 5^5 = 3,125 < P, so exact rank at least 5 implies rank at least
5 modulo either prime (and likewise 4 x 4 minors, norm at most 4^4). No
floating-point number appears anywhere:
the screen is modular arithmetic on integers, and every candidate class and
the zero set are re-decided as exact ranks in Q(zeta_16) (sympy's algebraic
field, DomainMatrix). The bound files therefore declare `exact: true`.

Enumeration. The n-qubit stabilizer states are written down from the
verifier's own parametrization sum_y i^(l.y) (-1)^Q(y) |x0 + W y> with W in
reduced row echelon form, x0 supported off the pivot columns, Q strictly
upper triangular and l in Z_4^k, which names each state exactly once (entry
1 at y = 0 fixes the phase). The count is checked against
2^n prod_{j<=n} (2^j + 1) and the rows are checked pairwise distinct, so the
list is complete.

Results. m = 4: exactly three four-qubit stabilizer states lie in V4
(|0000> + i|1111>, the uniform odd-weight state, and the odd-weight state with
sign -1 on weight 3), of exact rank 3, so no four terms. m = 5: no five-qubit
stabilizer state lies in V4 and no key class has more than three members, so
no five terms. The upper bounds chi(|sqrtT>^4) <= 5 and chi(|sqrtT>^5) <= 6
are the product states spanning Sym^m, filed separately, so both cells are
exact. Projection monotonicity ((<0| (x) I) |sqrtT>^(m+1) is |sqrtT>^m up to a
scalar, and a computational-basis slice of a stabilizer state is a stabilizer
state or zero) carries chi >= 6 to every m >= 6.

Controls, all fatal: the state counts and distinctness at n = 3, 4, 5; the
Vandermonde minor is nonzero in Q(zeta_16) and mod both primes; the
verifier's target is t_1 up to the scalar; at m = 3 the zero set spans V4 =
Sym^3 (the known rank 4); at m = 4 the rank-5 census must find a class whose
members together with Z have exact rank 5, and the five product states of
the filed m = 4 witness must share one key class; at m = 5 the six product
states of the filed m = 5 witness must have residues of exact rank 2 and must
not share a class.

Printed claims: CERTIFIED chi(qubit_sqrtT^4) >= 5
                CERTIFIED chi(qubit_sqrtT^5) >= 6
                CERTIFIED chi(qubit_sqrtT^6) >= 6   (projection monotonicity, and likewise)
                CERTIFIED chi(qubit_sqrtT^7) >= 6
                CERTIFIED chi(qubit_sqrtT^8) >= 6
                CERTIFIED chi(qubit_sqrtT^9) >= 6
                CERTIFIED chi(qubit_sqrtT^10) >= 6
"""

from __future__ import annotations

import itertools
import os
import sys
import time

import numpy as np
import sympy as sp
from sympy.polys.matrices import DomainMatrix

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from stabrank_verify import target_vector  # noqa: E402

ZETA = sp.exp(sp.I * sp.pi / 8)
CONJ = (1, 5, 9, 13)                       # the automorphisms of Q(zeta_16) fixing i
PRIMES = (2013265921, 1811939329)          # 15 * 2^27 + 1 and 27 * 2^26 + 1, both == 1 mod 16
PRIM_ROOT = {2013265921: 31, 1811939329: 13}
PIVOTS = (0, 1, 3, 7)                      # one string of each Hamming weight 0, 1, 2, 3
SEED = 20261023
T0 = time.time()


def say(msg):
    print(f"[{time.time() - T0:6.1f}s] {msg}", flush=True)


def fail(msg):
    print(msg, file=sys.stderr)
    raise SystemExit(1)


# ----------------------------------------------------------------------------
# exact enumeration of the n-qubit stabilizer states as int8 codes:
# 0 outside the support, 1 + e inside for the amplitude i^e

def count_states(n):
    t = 1 << n
    for j in range(1, n + 1):
        t *= (1 << j) + 1
    return t


def rref_matrices(n, k):
    """Every k x n matrix over F_2 in reduced row echelon form with its
    non-pivot columns, where the coset representative x0 is free."""
    for pivots in itertools.combinations(range(n), k):
        non_pivots = [j for j in range(n) if j not in pivots]
        free = [(r, c) for r in range(k) for c in non_pivots if c > pivots[r]]
        for vals in itertools.product(range(2), repeat=len(free)):
            W = np.zeros((k, n), dtype=np.int64)
            for r in range(k):
                W[r, pivots[r]] = 1
            for (r, c), v in zip(free, vals):
                W[r, c] = v
            yield W, non_pivots


def stabilizer_codes(n):
    """All n-qubit stabilizer states, each named once, as an (N, 2^n) int8 array."""
    weights = 1 << np.arange(n - 1, -1, -1)
    blocks = []
    for k in range(n + 1):
        Y = np.array(list(itertools.product(range(2), repeat=k)), dtype=np.int64).reshape(1 << k, k)
        pairs = [(i, j) for i in range(k) for j in range(i + 1, k)]
        L = np.array(list(itertools.product(range(4), repeat=k)), dtype=np.int64).reshape(4 ** k, k)
        Qc = np.array(list(itertools.product(range(2), repeat=len(pairs))),
                      dtype=np.int64).reshape(1 << len(pairs), len(pairs))
        YY = np.array([[y[i] * y[j] for (i, j) in pairs] for y in Y], dtype=np.int64).reshape(1 << k, len(pairs))
        lin = (L @ Y.T) % 4                                   # (4^k, 2^k)
        quad = (2 * (Qc @ YY.T)) % 4                          # (2^(k(k-1)/2), 2^k)
        phase = ((quad[:, None, :] + lin[None, :, :]) % 4).reshape(-1, 1 << k).astype(np.int8) + 1
        for W, non_pivots in rref_matrices(n, k):
            for free in itertools.product(range(2), repeat=n - k):
                x0 = np.zeros(n, dtype=np.int64)
                x0[non_pivots] = free
                pos = ((x0[None, :] + Y @ W) % 2) @ weights
                codes = np.zeros((phase.shape[0], 1 << n), dtype=np.int8)
                codes[:, pos] = phase
                blocks.append(codes)
    return np.concatenate(blocks)


def row_hashes(codes):
    """Two independent 61-bit hashes of every row, for the distinctness check."""
    rng = np.random.default_rng(SEED + 7)
    M = (1 << 61) - 1
    out = []
    for _ in range(2):
        c = rng.integers(1, M, size=codes.shape[1], dtype=np.int64)
        h = np.zeros(len(codes), dtype=np.int64)
        for j in range(codes.shape[1]):
            h = (h + (codes[:, j].astype(np.int64) * c[j]) % M) % M
        out.append(h)
    return np.stack(out, axis=1)


# ----------------------------------------------------------------------------
# the residue census modulo a prime

def root16(P):
    g = pow(PRIM_ROOT[P], (P - 1) // 16, P)
    if pow(g, 8, P) != P - 1 or pow(g, 16, P) != 1:
        fail(f"{PRIM_ROOT[P]}^((P-1)/16) is not a primitive sixteenth root of unity mod {P}")
    return g


def modinv_arr(a, P):
    res = np.ones_like(a)
    base = a % P
    e = P - 2
    while e:
        if e & 1:
            res = (res * base) % P
        base = (base * base) % P
        e >>= 1
    return res


def matinv_mod(A, P):
    n = len(A)
    M = [[int(A[i][j]) % P for j in range(n)] + [int(i == j) for j in range(n)] for i in range(n)]
    for c in range(n):
        piv = next((r for r in range(c, n) if M[r][c]), None)
        if piv is None:
            fail(f"the pivot block is singular mod {P}")
        M[c], M[piv] = M[piv], M[c]
        inv = pow(M[c][c], P - 2, P)
        M[c] = [(x * inv) % P for x in M[c]]
        for r in range(n):
            if r != c and M[r][c]:
                f = M[r][c]
                M[r] = [(x - f * y) % P for x, y in zip(M[r], M[c])]
    return np.array([row[n:] for row in M], dtype=np.int64)


def rank_mod(rows, P):
    M = [[int(x) % P for x in r] for r in rows]
    rk = 0
    for c in range(len(M[0]) if M else 0):
        piv = next((r for r in range(rk, len(M)) if M[r][c]), None)
        if piv is None:
            continue
        M[rk], M[piv] = M[piv], M[rk]
        inv = pow(M[rk][c], P - 2, P)
        M[rk] = [(x * inv) % P for x in M[rk]]
        for r in range(len(M)):
            if r != rk and M[r][c]:
                f = M[r][c]
                M[r] = [(x - f * y) % P for x, y in zip(M[r], M[rk])]
        rk += 1
        if rk == len(M):
            break
    return rk


def weights(m):
    return np.array([bin(x).count("1") for x in range(1 << m)], dtype=np.int64)


class ResidueKeys:
    """Projective keys of the residues modulo V4 of every state, under one prime."""

    def __init__(self, m, P, rng):
        self.m, self.P = m, P
        g = root16(P)
        self.tab = np.array([0, 1, pow(g, 4, P), P - 1, P - pow(g, 4, P)], dtype=np.int64)
        w = weights(m)
        self.B = np.array([[pow(g, int(k * ww), P) for k in CONJ] for ww in w], dtype=np.int64)
        A = self.B[list(PIVOTS)]
        if any(w[p] != j for j, p in enumerate(PIVOTS)):
            fail("pivot strings are not of weights 0, 1, 2, 3")
        self.Ainv = matinv_mod(A, P)
        self.f = rng.integers(1, P, size=(2, 1 << m), dtype=np.int64)

    def residues(self, codes):
        P = self.P
        V = self.tab[codes]
        C = np.zeros((len(V), 4), dtype=np.int64)
        for k in range(4):
            C = (C + (V[:, PIVOTS[k]][:, None] * self.Ainv[:, k][None, :]) % P) % P
        R = V.copy()
        for k in range(4):
            R = (R - (C[:, k][:, None] * self.B[:, k][None, :]) % P) % P
        if R[:, list(PIVOTS)].any():
            fail("a residue does not vanish on the pivot coordinates")
        return R

    def keys(self, codes, chunk=250000):
        """(N, 3) int64: first nonzero index, two functionals over the pivot entry;
        a zero residue gets the row (-1, 0, 0)."""
        P = self.P
        out = np.empty((len(codes), 3), dtype=np.int64)
        for s in range(0, len(codes), chunk):
            R = self.residues(codes[s:s + chunk])
            nz = R != 0
            zero = ~nz.any(axis=1)
            p = np.argmax(nz, axis=1)
            rp = R[np.arange(len(R)), p]
            rp[zero] = 1
            inv = modinv_arr(rp, P)
            k = np.empty((len(R), 3), dtype=np.int64)
            k[:, 0] = np.where(zero, -1, p)
            for j in range(2):
                S = ((R * self.f[j][None, :]) % P).sum(axis=1) % P
                k[:, 1 + j] = np.where(zero, 0, (S * inv) % P)
            out[s:s + chunk] = k
        return out


def census(m, codes, r, label):
    """Return (zero set indices, list of candidate index sets of exact rank >= r,
    class size histogram). A candidate set is a key class plus the zero set
    whose exact rank over Q(zeta) is at least r, i.e. an r-term decomposition."""
    rng = np.random.default_rng(SEED + m)
    K = np.concatenate([ResidueKeys(m, P, rng).keys(codes) for P in PRIMES], axis=1)
    zero = (K[:, 0] == -1) | (K[:, 3] == -1)
    Z = np.flatnonzero(zero)
    nz = np.flatnonzero(~zero)
    Kn = K[nz]
    order = np.lexsort(Kn.T[::-1])
    Ks = Kn[order]
    brk = np.flatnonzero(np.any(Ks[1:] != Ks[:-1], axis=1)) + 1
    starts = np.concatenate([[0], brk])
    ends = np.concatenate([brk, [len(Ks)]])
    sizes = ends - starts
    hist = {int(s): int(c) for s, c in enumerate(np.bincount(sizes)) if c}
    say(f"{label}: |Z| = {len(Z)}, {len(sizes)} residue classes, sizes {hist}")
    need = max(r - len(Z), 1)
    found = []
    for b in np.flatnonzero(sizes >= need):
        members = nz[order[starts[b]:ends[b]]]
        sel = np.concatenate([members, Z])
        if max(rank_mod(tab_rows(codes[sel], P), P) for P in PRIMES) < r:
            continue                      # rank mod P is at most the exact rank
        rk = exact_rank(codes[sel], m)
        say(f"  class of {len(members)} + {len(Z)} in Z: exact rank {rk}")
        if rk >= r:
            found.append(sel)
    return Z, found, hist, K


def tab_rows(codes, P):
    g = root16(P)
    tab = np.array([0, 1, pow(g, 4, P), P - 1, P - pow(g, 4, P)], dtype=np.int64)
    return tab[codes].tolist()


_K = None


def field():
    global _K
    if _K is None:
        _K = sp.QQ.algebraic_field(ZETA)
    return _K


def exact_rank(codes, m, extra=None):
    """Exact rank over Q(zeta_16) of the states (rows of codes), with the
    optional extra rows (sympy expressions) appended."""
    K = field()
    xz = K.from_sympy(ZETA)
    tab = [K.zero, K.one, xz ** 4, -K.one, -(xz ** 4)]
    rows = [[tab[int(c)] for c in row] for row in codes]
    if extra is not None:
        rows += [[K.from_sympy(e) for e in row] for row in extra]
    return DomainMatrix(rows, (len(rows), 1 << m), K).rank()


def product_codes(m):
    """The six product states phi^m, phi over the single-qubit stabilizer states,
    as codes: |0>^m, |1>^m, |+>^m, |->^m, |+i>^m, |-i>^m."""
    w = weights(m)
    out = [np.zeros(1 << m, dtype=np.int8), np.zeros(1 << m, dtype=np.int8)]
    out[0][0] = 1
    out[1][-1] = 1
    for e in (0, 2, 1, 3):                                    # i^(e |x|)
        out.append(((e * w) % 4 + 1).astype(np.int8))
    return np.array(out)


def main():
    # Galois and Vandermonde facts, exactly
    for k in CONJ:
        if (k * 4) % 16 != 4:
            fail(f"zeta -> zeta^{k} does not fix i")
    K = field()
    z = K.from_sympy(ZETA)
    V = DomainMatrix([[z ** (k * w) for k in CONJ] for w in range(4)], (4, 4), K)
    if V.det() == K.zero:
        fail("the 4 x 4 Vandermonde minor is singular")
    say("Gal(Q(zeta_16)/Q(i)) = {zeta -> zeta^k : k = 1, 5, 9, 13}; the Vandermonde minor on "
        "weights 0..3 is nonzero in Q(zeta_16), so dim V4 = 4 for every m >= 3")
    for P in PRIMES:
        g = root16(P)
        if len({pow(g, k, P) for k in CONJ}) != 4:
            fail(f"the images of zeta^k, k in CONJ, are not distinct mod {P}")
    say(f"primes {PRIMES}: zeta maps to a primitive sixteenth root of unity, the four conjugate "
        "nodes stay distinct, so the pivot block is invertible mod P")
    for m in range(1, 5):
        tgt = target_vector("qubit_sqrtT", m) * sp.sqrt(2) ** m
        want = [ZETA ** int(w) for w in weights(m)]
        if any(sp.simplify(sp.expand(a - b)) != 0 for a, b in zip(tgt, want)):
            fail(f"m={m}: the verifier's target is not t_1")
    say("the verifier's sqrt(2)^m |sqrtT>^m equals t_1 = (1, zeta)^{ot m} symbolically for m <= 4")

    codes = {}
    for n in (3, 4, 5):
        c = stabilizer_codes(n)
        if len(c) != count_states(n):
            fail(f"{n} qubits: enumerated {len(c)} states, formula gives {count_states(n)}")
        h = row_hashes(c)
        if len(np.unique(h, axis=0)) != len(c):
            fail(f"{n} qubits: two enumerated states coincide")
        if not (c[:, 0] <= 4).all() or (c == 0).all(axis=1).any():
            fail(f"{n} qubits: a malformed code")
        codes[n] = c
        say(f"{n} qubits: {len(c)} stabilizer states enumerated, count matches, rows distinct")

    # m = 3 control: the zero set is Sym^3 cap stabilizer states and spans V4
    Z3, found3, _, _ = census(3, codes[3], 4, "m=3 census")
    if exact_rank(codes[3][Z3], 3) != 4:
        fail("m=3 control: the stabilizer states inside V4 do not span it")
    say("m=3 control: the states inside V4 span it (chi(|sqrtT>^3) = 4, as known)")

    # m = 4: rank 4 excluded by the zero set, rank 5 found (control)
    Z4, found4, hist4, K4 = census(4, codes[4], 5, "m=4 census")
    if len(Z4) != 3:
        fail(f"m=4: expected exactly three states inside V4, found {len(Z4)}")
    rk = exact_rank(codes[4][Z4], 4)
    rk_t = exact_rank(codes[4][Z4], 4, extra=[[ZETA ** int(w) for w in weights(4)]])
    if rk != 3 or rk_t != 4:
        fail(f"m=4: the states inside V4 have rank {rk} (with t_1: {rk_t}); expected 3 and 4")
    for row in codes[4][Z4]:
        say("  in V4: " + "".join(".1i-j"[c] for c in row))
    say("m=4: the three states inside V4 span 3 < 4 dimensions, so no four-term decomposition")
    if not found4:
        fail("m=4 control: the rank-5 census found no five-term decomposition")
    pc = product_codes(4)
    idx = [int(np.flatnonzero((codes[4] == p).all(axis=1))[0]) for p in pc[:5]]
    if len({tuple(K4[i]) for i in idx}) != 1:
        fail("m=4 control: the five product states of the filed witness are not in one class")
    say(f"m=4 control: {len(found4)} classes carry a five-term decomposition; the five product "
        "states share one residue class")

    # m = 5: rank 5 excluded
    Z5, found5, hist5, K5 = census(5, codes[5], 5, "m=5 census")
    if len(Z5) != 0:
        fail(f"m=5: {len(Z5)} states inside V4 (expected none); exact rank "
             f"{exact_rank(codes[5][Z5], 5)}")
    if found5:
        fail("m=5: a class of exact rank 5 exists: DECOMPOSITION FOUND, the bound is false")
    if max(hist5) >= 5:
        fail("m=5: a class with five members survived without an exact decision")
    pc = product_codes(5)
    idx = [int(np.flatnonzero((codes[5] == p).all(axis=1))[0]) for p in pc]
    if exact_rank(codes[5][idx], 5) != 6:
        fail("m=5 control: the six product states are dependent")
    if len({tuple(K5[i]) for i in idx}) < 2:
        fail("m=5 control: the six product states share one residue class")
    say("m=5: no state inside V4 and no residue class with five members, so no five-term "
        "decomposition; the six product states (rank 6, residues of rank 2) are the m=5 witness")
    say("projection: (<0| (x) I)|sqrtT>^(m+1) is |sqrtT>^m up to a scalar, so chi is monotone in m")

    print("CERTIFIED chi(qubit_sqrtT^4) >= 5")
    print("CERTIFIED chi(qubit_sqrtT^5) >= 6")
    r = 6
    for m in range(6, 11):
        print(f"CERTIFIED chi(qubit_sqrtT^{m}) >= {r}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
