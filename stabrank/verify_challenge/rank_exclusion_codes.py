"""Rank-2 and rank-3 exclusion over a dictionary held as phase codes.

The method is that of rank_exclusion.py (quotient out the target, then a
pivot; parallel images mean a candidate; symmetry gives one pivot per orbit)
rearranged so that the complex dictionary is never held. On four qutrits the
7,439,040 states are 4.8 GB as complex64; as phase codes they are 600 MB, and
every quantity the search needs is an inner product with a stabilizer state,
which is computed from the codes in chunks:

  G_j   = <psi | s_j>                              (one pass)
  R s_j for a small random matrix R                (one pass, kept: r x N)
  <s_i | s_j> for the current pivot i              (one pass per pivot)

With q_j = s_j - G_j psi the quotient direction, <q_i | q_j> = <s_i | s_j> -
conj(G_i) G_j and |q_j|^2 = 1 - |G_j|^2, so the per-pivot geometry follows
from the pivot's inner-product pass and the stored projections. Candidates
are re-tested in the full space by expanding just the states involved.

Symmetry orbits are computed exactly: each generator is applied to the
expanded states in chunks, the images are re-encoded, located in the
dictionary by a hash and then verified code-for-code, so a hash collision
raises instead of merging two orbits. Orbits are found by label propagation.

Soundness is inherited from rank_exclusion.py; see there for the argument.
The dictionary count is asserted by the enumerator.
"""

from __future__ import annotations

import math
import os
import sys
from concurrent.futures import ProcessPoolExecutor
import multiprocessing

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from qutrit_codes import all_codes, expand, inner, project, encode  # noqa: E402
from rank_exclusion import (PARALLEL, MARGIN, PROJ_DIM, RESID, _parallel_groups,  # noqa: E402
                            clifford_group, _copy_permutation)

CHUNK = 200_000


def _hash_codes(codes):
    """Two independent 64-bit hashes per row, computed in chunks."""
    rng = np.random.default_rng(12345)
    w1 = rng.integers(1, 2 ** 63 - 1, size=codes.shape[1], dtype=np.int64).astype(np.uint64)
    w2 = rng.integers(1, 2 ** 63 - 1, size=codes.shape[1], dtype=np.int64).astype(np.uint64)
    h1 = np.empty(codes.shape[0], dtype=np.uint64)
    h2 = np.empty(codes.shape[0], dtype=np.uint64)
    for lo in range(0, codes.shape[0], CHUNK):
        c = (codes[lo:lo + CHUNK].astype(np.int16) + 1).astype(np.uint64)
        h1[lo:lo + CHUNK] = c @ w1
        h2[lo:lo + CHUNK] = c @ w2
    return h1, h2


class CodeIndex:
    """Exact lookup of states by code, hash-accelerated, verified."""

    def __init__(self, codes):
        self.codes = codes
        h1, h2 = _hash_codes(codes)
        self.order = np.lexsort((h2, h1))
        self.h1 = h1[self.order]
        self.h2 = h2[self.order]

    def lookup(self, img_codes):
        """Indices of the given codes in the dictionary; raises if any is absent."""
        q1, q2 = _hash_codes(img_codes)
        pos = np.searchsorted(self.h1, q1)
        pos = np.minimum(pos, len(self.h1) - 1)
        # walk forward over equal h1 to match h2 (collisions in h1 are rare)
        idx = self.order[pos]
        ok = (self.h1[pos] == q1) & (self.h2[pos] == q2)
        bad = np.flatnonzero(~ok)
        for b in bad:
            p = pos[b]
            found = False
            while p < len(self.h1) and self.h1[p] == q1[b]:
                if self.h2[p] == q2[b]:
                    idx[b] = self.order[p]
                    found = True
                    break
                p += 1
            if not found:
                raise AssertionError("an image state is not in the dictionary")
        if not np.array_equal(self.codes[idx], img_codes):
            raise AssertionError("hash matched a different state; lookup is not exact")
        return idx


def symmetry_orbit_reps_codes(orbit, m, codes, ks):
    """Representatives of the dictionary orbits under the symmetry group of |M>^m."""
    from stabrank_verify import orbit_state, ORBIT_P
    p = ORBIT_P[orbit]
    N, dim = codes.shape
    psi1 = np.array([complex(x) for x in orbit_state(orbit)]).ravel()
    psi1 /= np.linalg.norm(psi1)
    psi = psi1
    for _ in range(m - 1):
        psi = np.kron(psi, psi1)
    G = clifford_group(p)
    uni = [U for U in G if abs(abs(np.vdot(psi1, U @ psi1)) - 1) < 1e-9]
    anti = [U for U in G if abs(abs(np.vdot(psi1, U @ psi1.conj())) - 1) < 1e-9]
    I = np.eye(p, dtype=complex)
    gens = []
    for U in uni:
        g = U
        for _ in range(m - 1):
            g = np.kron(g, I)
        gens.append((g, False))
    if m >= 2:
        gens.append((_copy_permutation((1, 0) + tuple(range(2, m)), p, m), False))
        gens.append((_copy_permutation(tuple(range(1, m)) + (0,), p, m), False))
    if anti:
        g = anti[0]
        for _ in range(m - 1):
            g = np.kron(g, anti[0])
        gens.append((g, True))
    index = CodeIndex(codes)
    labels = np.arange(N, dtype=np.int64)
    perms = []
    for g, is_anti in gens:
        target = g @ (psi.conj() if is_anti else psi)
        if abs(abs(np.vdot(psi, target)) - 1) > 1e-9:
            raise AssertionError("a proposed symmetry does not fix the target up to phase")
        pm = np.empty(N, dtype=np.int64)
        for lo in range(0, N, CHUNK):
            amp = expand(codes[lo:lo + CHUNK], ks[lo:lo + CHUNK], p)
            img = g @ (amp.conj() if is_anti else amp)
            pm[lo:lo + CHUNK] = index.lookup(encode(img, p))
        if len(np.unique(pm)) != N:
            raise AssertionError("a proposed symmetry is not a permutation of the dictionary")
        perms.append(pm)
    # label propagation to orbit minima
    inv = [np.argsort(pm) for pm in perms]
    while True:
        new = labels.copy()
        for pm, ip in zip(perms, inv):
            new = np.minimum(new, new[pm])
            new = np.minimum(new, new[ip])
        if np.array_equal(new, labels):
            break
        labels = new
    reps = np.unique(labels)
    order = (2 if anti else 1) * len(uni) ** m * math.factorial(m)
    return reps, {"order": order, "orbits": len(reps), "local": len(uni),
                  "antiunitary": bool(anti)}


class _Geometry:
    """Everything about the quotient by psi that does not depend on the pivot."""

    def __init__(self, psi, codes, ks, seed=7):
        self.codes, self.ks = codes, ks
        self.p = 3
        self.psi = (psi / np.linalg.norm(psi)).astype(np.complex128)
        self.G = inner(self.psi, codes, ks)                        # <psi|s_j>
        self.nq = np.sqrt(np.maximum(1 - np.abs(self.G) ** 2, 0))
        rng = np.random.default_rng(seed)
        dim = codes.shape[1]
        self.R = rng.normal(size=(PROJ_DIM, dim)) + 1j * rng.normal(size=(PROJ_DIM, dim))
        RS = project(self.R, codes, ks)                            # R s_j
        Rpsi = self.R @ self.psi
        # R p_j with p_j = q_j / |q_j|; states parallel to psi are flagged separately
        safe = np.where(self.nq > 1e-9, self.nq, 1)
        self.RP = (RS - np.outer(Rpsi, self.G)) / safe[None, :]
        self.rng = np.random.default_rng(seed + 1)

    def state(self, idx):
        return expand(self.codes[idx], self.ks[idx], self.p)

    def pivot_overlaps(self, i):
        """<p_i | p_j> for all j."""
        si = self.state(np.array([i]))[:, 0]
        S = inner(si, self.codes, self.ks)                         # <s_i | s_j>
        num = S - np.conj(self.G[i]) * self.G
        return num / (self.nq[i] * np.where(self.nq > 1e-9, self.nq, 1))


_GEO = None


def _init_geo(geo):
    global _GEO
    _GEO = geo


def _scan(job):
    plist, = job
    geo = _GEO
    N = geo.codes.shape[0]
    cands, worst, rank2 = [], 0.0, []
    for i in plist:
        ov = geo.pivot_overlaps(i)
        rest = np.concatenate((np.arange(0, i), np.arange(i + 1, N)))
        ov = ov[rest]
        q = geo.RP[:, rest] - np.outer(geo.RP[:, i], ov)
        nq_full = np.sqrt(np.maximum(1 - np.abs(ov) ** 2, 0))
        zero = nq_full < 1e-7
        if zero.any():
            rank2 += [(int(i), int(rest[j])) for j in np.flatnonzero(zero)]
        keep = ~zero
        nq = np.linalg.norm(q, axis=0)
        if (nq[keep] <= 1e-12).any():
            raise RuntimeError("random projection annihilated a direction; rerun with another seed")
        U = q[:, keep] / nq[keep]
        ids = rest[keep]
        groups, w = _parallel_groups(U, geo.rng)
        worst = max(worst, w)
        for g in groups:
            g = ids[g]
            for a in range(len(g)):
                for b in range(a + 1, len(g)):
                    cands.append((int(i), int(g[a]), int(g[b])))
    return cands, worst, rank2


def rank2_search_codes(geo):
    """Pairs spanning psi, and the closest approach among sorted neighbours."""
    if (geo.nq <= 1e-9).any():
        return "RANK1", 1.0
    U = geo.RP / np.linalg.norm(geo.RP, axis=0)
    groups, worst = _parallel_groups(U, np.random.default_rng(7))
    pairs = []
    for g in groups:
        # confirm in the full space: the two quotient directions must be parallel
        S = geo.state(g)
        Q = S - np.outer(geo.psi, geo.G[g])
        Q /= np.linalg.norm(Q, axis=0)
        Gm = np.abs(Q.conj().T @ Q)
        for a in range(len(g)):
            for b in range(a + 1, len(g)):
                if Gm[a, b] > 1 - PARALLEL:
                    pairs.append((int(g[a]), int(g[b])))
    return pairs, worst


def rank3_search_codes(geo, pivots, workers=None):
    """Triples spanning psi, scanning the given pivots against every state."""
    out = {"found": [], "rank2": [], "candidates": 0, "dependent": 0,
           "min_resid": np.inf, "worst": 0.0}
    if (geo.nq <= 1e-9).any():
        out["rank2"] = [("RANK1", int(j)) for j in np.flatnonzero(geo.nq <= 1e-9)]
        return out
    plist = np.asarray(pivots, dtype=np.int64)
    workers = max(1, min(workers or max(1, (os.cpu_count() or 2) - 1), len(plist)))
    jobs = [(chunk,) for chunk in np.array_split(plist, workers) if len(chunk)]
    cands, rank2 = [], []
    if workers == 1:
        _init_geo(geo)
        for job in jobs:
            c, w, r2 = _scan(job)
            cands += c; rank2 += r2; out["worst"] = max(out["worst"], w)
    else:
        ctx = multiprocessing.get_context("fork")
        _init_geo(geo)
        with ProcessPoolExecutor(max_workers=workers, mp_context=ctx) as ex:
            for c, w, r2 in ex.map(_scan, jobs):
                cands += c; rank2 += r2; out["worst"] = max(out["worst"], w)
    out["rank2"] = rank2
    out["candidates"] = len(cands)
    if rank2:
        return out
    cand = np.array(cands, dtype=np.int64).reshape(-1, 3)
    psi = geo.psi
    for lo in range(0, len(cand), 100_000):
        idx = cand[lo:lo + 100_000]
        s1 = geo.state(idx[:, 0]).T
        s2 = geo.state(idx[:, 1]).T
        s3 = geo.state(idx[:, 2]).T
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
        res = np.where(indep, np.linalg.norm(r, axis=1), np.inf)
        hit = res < RESID
        for cols in idx[hit]:
            A1 = geo.state(cols)
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


def psi_for(orbit, m):
    from stabrank_verify import target_vector
    return np.array([complex(x) for x in target_vector(orbit, m)]).ravel()


def certify_m4(orbit, workers=None):
    """Rank-2 then rank-3 exclusion for a qutrit orbit at m=4, with a code-path
    positive control at m=2. Prints a report; returns the highest excluded rank
    (2 or 3), or 0 on failure."""
    import time
    t0 = time.time()
    # positive control: the code path must find the known rank-3 decompositions at m=2
    c2, k2 = all_codes(2)
    geo2 = _Geometry(psi_for("N", 2), c2, k2)
    reps2, _ = symmetry_orbit_reps_codes("N", 2, c2, k2)
    r2 = rank3_search_codes(geo2, reps2, workers=1)
    if not r2["found"]:
        print("positive control FAILED: the code path did not find the rank-3 decomposition "
              "of the Norrell state at m=2", file=sys.stderr)
        return 0
    print(f"positive control: Norrell m=2 found {len(r2['found'])} rank-3 decomposition(s) "
          f"through the code path", flush=True)
    codes, ks = all_codes(4)
    print(f"4 qutrits: {codes.shape[0]} states enumerated ({time.time() - t0:.0f}s)", flush=True)
    geo = _Geometry(psi_for(orbit, 4), codes, ks)
    pairs, worst = rank2_search_codes(geo)
    if pairs == "RANK1" or pairs:
        print(f"{orbit} m=4: rank <= 2 decomposition FOUND {pairs if pairs != 'RANK1' else ''}")
        return 0
    slack2 = (1 - PARALLEL) - worst
    print(f"{orbit} m=4: no pair spans it; closest approach {worst:.6f}, clearing by "
          f"{slack2:.4f} ({time.time() - t0:.0f}s)", flush=True)
    if slack2 < MARGIN:
        print("rank-2 margin too thin to stand behind", file=sys.stderr)
        return 0
    print(f"CERTIFIED chi({orbit}^4) >= 3", flush=True)
    reps, info = symmetry_orbit_reps_codes(orbit, 4, codes, ks)
    print(f"{orbit} m=4: symmetry group of order {info['order']} splits {codes.shape[0]} states "
          f"into {info['orbits']} orbits ({time.time() - t0:.0f}s)", flush=True)
    r = rank3_search_codes(geo, reps, workers=workers)
    if r["rank2"] or r["found"]:
        print(f"{orbit} m=4: rank-3 decomposition FOUND {r['found'][:1] or r['rank2'][:3]}")
        return 2
    slack = (1 - PARALLEL) - r["worst"]
    indep = r["candidates"] - r["dependent"]
    resid = f" (smallest residual {r['min_resid']:.4f})" if np.isfinite(r["min_resid"]) else ""
    print(f"{orbit} m=4: {r['candidates']} collinear candidates, {r['dependent']} dependent, "
          f"{indep} independent; none spans the target{resid}. Closest approach "
          f"{r['worst']:.6f}, clearing by {slack:.4f} ({time.time() - t0:.0f}s)", flush=True)
    if slack < MARGIN:
        print("rank-3 margin too thin to stand behind", file=sys.stderr)
        return 2
    print(f"CERTIFIED chi({orbit}^4) >= 4", flush=True)
    return 3
