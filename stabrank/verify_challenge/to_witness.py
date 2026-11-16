"""Turn amplitude vectors into the witness format, exactly.

The verifier takes each term as (k, x0, W, Q, l) so that a non-stabilizer
vector cannot even be written down. Searches produce amplitude vectors. This
closes the gap: given a vector, recover the flat it is supported on and the
quadratic phase on that flat, or refuse because no such data exists, which is
the same thing as the vector not being a stabilizer state.

The recovery is deterministic. The coset representative x0 is the
lexicographically smallest support point, W is the reduced row echelon basis
of the differences, and the phase exponents are read off at y = e_i, y = 2 e_i
(odd p) and y = e_i + e_j, then checked at every point of the flat. A vector
whose phases are not a quadratic form on its support fails that check and is
reported, not approximated.

Coefficients come from fit_coeffs in exact arithmetic, so the output either
verifies on the nose or the script says no exact combination exists.

Usage:
    to_witness.py ORBIT M (solution.npz | vectors.json) [-o bounds/X.json]
                  [--author NAME] [--github HANDLE ...] [--method TEXT]

An .npz is one written by stabrank/examples/search_decomposition.py (keys
basis_func_0, basis_func_1, ...). A .json is a list of vectors, each a list of
complex numbers written as strings sympy can parse or as [re, im] pairs.
"""

from __future__ import annotations

import argparse
import datetime
import itertools
import json
import os
import sys

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from stabrank_verify import ORBIT_P, orbit_qudits, stabilizer_vector  # noqa: E402
from fit_coeffs import fit  # noqa: E402


class NotStabilizer(ValueError):
    """The vector is not a stabilizer state, with the reason."""


def _digits(idx, p, n):
    """Index -> point of F_p^n, most significant digit first (verifier order)."""
    out = []
    for _ in range(n):
        out.append(idx % p)
        idx //= p
    return out[::-1]


def _rref(rows, p):
    """Reduced row echelon form over F_p; returns (basis rows, pivot columns)."""
    M = [list(r) for r in rows]
    if not M:
        return [], []
    ncol = len(M[0])
    piv = []
    r = 0
    for c in range(ncol):
        s = next((i for i in range(r, len(M)) if M[i][c] % p), None)
        if s is None:
            continue
        M[r], M[s] = M[s], M[r]
        inv = pow(M[r][c], -1, p)
        M[r] = [(v * inv) % p for v in M[r]]
        for i in range(len(M)):
            if i != r and M[i][c] % p:
                f = M[i][c]
                M[i] = [(a - f * b) % p for a, b in zip(M[i], M[r])]
        piv.append(c)
        r += 1
        if r == len(M):
            break
    return M[:r], piv


def _root_exponent(z, order, tol):
    """z as an exact power of exp(2 pi i / order), or None."""
    if abs(abs(z) - 1) > tol:
        return None
    e = round(np.angle(z) / (2 * np.pi / order)) % order
    if abs(z - np.exp(2j * np.pi * e / order)) > tol:
        return None
    return int(e)


def term_from_vector(v, p, n, tol=1e-7):
    """(k, x0, W, Q, l) for the stabilizer state v, or raise NotStabilizer.

    The returned term rebuilds to v up to a scalar, which the coefficient fit
    absorbs. The phase group is the p-th roots for odd p and the fourth roots
    for qubits, matching the verifier.
    """
    v = np.asarray(v, dtype=complex).ravel()
    if v.shape[0] != p ** n:
        raise ValueError(f"vector has length {v.shape[0]}, expected {p ** n}")
    supp = np.flatnonzero(np.abs(v) > tol * np.abs(v).max())
    mags = np.abs(v[supp])
    if mags.max() - mags.min() > tol * mags.max():
        raise NotStabilizer("nonzero amplitudes do not all have the same modulus")
    pts = sorted(_digits(int(i), p, n) for i in supp)
    x0 = pts[0]
    diffs = [[(a - b) % p for a, b in zip(q, x0)] for q in pts[1:]]
    W, piv = _rref(diffs, p)
    k = len(W)
    if len(pts) != p ** k:
        raise NotStabilizer(f"support has {len(pts)} points, not a power of {p}")
    order = 4 if p == 2 else p
    pts_set = {tuple(q) for q in pts}

    def point(y):
        return tuple((x0[c] + sum(y[r] * W[r][c] for r in range(k))) % p
                     for c in range(n))

    def index(x):
        i = 0
        for c in x:
            i = i * p + c
        return i

    a0 = v[index(tuple(x0))]
    expo = {}
    for y in itertools.product(range(p), repeat=k):
        x = point(y)
        if x not in pts_set:
            raise NotStabilizer("support is not an affine flat")
        e = _root_exponent(v[index(x)] / a0, order, tol)
        if e is None:
            raise NotStabilizer("a relative phase is not a root of unity of the "
                                f"expected order {order}")
        expo[y] = e

    def unit(i, mult=1):
        y = [0] * k
        y[i] = mult % p
        return tuple(y)

    Q = [[0] * k for _ in range(k)]
    ell = [0] * k
    if p == 2:
        for i in range(k):
            ell[i] = expo[unit(i)] % 4
        for i in range(k):
            for j in range(i + 1, k):
                y = [0] * k
                y[i] = y[j] = 1
                d = (expo[tuple(y)] - ell[i] - ell[j]) % 4
                if d % 2:
                    raise NotStabilizer("phase is not a Z_4 quadratic form with even "
                                        "cross terms")
                Q[i][j] = d // 2
    else:
        inv2 = pow(2, -1, p)
        for i in range(k):
            e1, e2 = expo[unit(i)], expo[unit(i, 2)]
            Q[i][i] = ((e2 - 2 * e1) * inv2) % p
            ell[i] = (e1 - Q[i][i]) % p
        for i in range(k):
            for j in range(i + 1, k):
                y = [0] * k
                y[i] = y[j] = 1
                Q[i][j] = (expo[tuple(y)] - expo[unit(i)] - expo[unit(j)]) % p
    # Check the fitted form at every point; anything else is not stabilizer.
    for y, e in expo.items():
        q = sum(Q[i][j] * y[i] * y[j] for i in range(k) for j in range(i, k))
        lin = sum(ell[i] * y[i] for i in range(k))
        want = ((lin % 4) + 2 * (q % 2)) % 4 if p == 2 else (q + lin) % p
        if want != e:
            raise NotStabilizer("phases on the flat are not a quadratic form")
    return {"k": k, "x0": list(x0), "W": [list(r) for r in W], "Q": Q, "l": ell}


def load_vectors(path):
    """Amplitude vectors from an .npz (search driver output) or a JSON list."""
    if path.endswith(".npz"):
        d = np.load(path)
        keys = sorted((key for key in d.files if key.startswith("basis_func_")),
                      key=lambda s: int(s.split("_")[-1]))
        return [np.asarray(d[key], dtype=complex).ravel() for key in keys]
    import sympy as sp
    raw = json.load(open(path))
    out = []
    for vec in raw:
        row = []
        for z in vec:
            if isinstance(z, (list, tuple)):
                row.append(complex(z[0], z[1]))
            else:
                row.append(complex(sp.N(sp.sympify(z), 30)))
        out.append(np.array(row, dtype=complex))
    return out


def witness_from_vectors(orbit, m, vectors, tol=1e-7):
    """{"terms": [...], "coeffs": [...]} with exact coefficients, or raise.

    The vectors live on n = width * m qudits (orbit_qudits): m copies of the
    two-qubit CS state are a 4^m-vector."""
    p = ORBIT_P[orbit]
    n = orbit_qudits(orbit, m)
    terms = []
    for i, v in enumerate(vectors):
        try:
            terms.append(term_from_vector(v, p, n, tol))
        except NotStabilizer as exc:
            raise NotStabilizer(f"term {i}: {exc}") from None
    coeffs = fit(orbit, m, terms)
    if coeffs is None:
        raise ValueError("the terms are stabilizer states but no exact combination "
                         "of them reproduces the target")
    return {"terms": terms, "coeffs": [str(c) for c in coeffs]}


def main(argv):
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("orbit", choices=sorted(ORBIT_P))
    ap.add_argument("m", type=int)
    ap.add_argument("vectors", help=".npz from the search driver, or a JSON list")
    ap.add_argument("-o", "--out", help="write the submission here")
    ap.add_argument("--author", default="")
    ap.add_argument("--github", nargs="*", default=[])
    ap.add_argument("--method", default="")
    ap.add_argument("--reference", default="")
    ap.add_argument("--tol", type=float, default=1e-7)
    a = ap.parse_args(argv[1:])

    vecs = load_vectors(a.vectors)
    try:
        w = witness_from_vectors(a.orbit, a.m, vecs, a.tol)
    except (NotStabilizer, ValueError) as exc:
        print(f"rejected: {exc}")
        return 1
    sub = {
        "schema_version": "0.1", "orbit": a.orbit, "m": a.m, "direction": "upper",
        "rank": len(w["terms"]), "witness": w,
        "provenance": {"author": a.author, "reference": a.reference,
                       "method": a.method,
                       "date": datetime.date.today().isoformat(),
                       "github": a.github},
        "notes": "",
    }
    text = json.dumps(sub, indent=2) + "\n"
    if a.out:
        with open(a.out, "w") as f:
            f.write(text)
        print(f"written {a.out}: rank {sub['rank']}, coefficients exact")
    else:
        print(text, end="")
    p = ORBIT_P[a.orbit]
    # Sanity: every term rebuilds and the rank is what the terms say.
    for t in w["terms"]:
        stabilizer_vector(t, p, orbit_qudits(a.orbit, a.m))
    if not a.author:
        print("fill in provenance.author and notes before submitting", file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
