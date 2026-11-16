"""Solve for the exact coefficients of a proposed decomposition.

Submitters supply the stabilizer terms; this recovers the coefficients in exact
arithmetic, or reports that no exact combination of those terms reproduces the
target. Running it before submitting turns a "close" decomposition into either
a submission or a clear no, without burning a verification slot.

The terms are linearly independent in every case that matters (a dependent set
would mean the true rank is lower), so the exact normal equations
(A^H A)^{-1} A^H b give the unique candidate, and it is then checked against the
target on the nose rather than by residual size.
"""

from __future__ import annotations

import json
import os
import sys

import numpy as np
import sympy as sp

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from stabrank_verify import ORBIT_P, is_zero, orbit_qudits, stabilizer_vector, target_vector


def fit(orbit, m, terms):
    """Exact coefficients, or None if no exact combination reproduces the target.

    The terms are parametrized over the n = width * m qudits the m copies
    occupy (orbit_qudits), which is m itself for every single-qudit orbit."""
    p = ORBIT_P[orbit]
    cols = [stabilizer_vector(t, p, orbit_qudits(orbit, m)) for t in terms]
    A = sp.Matrix.hstack(*cols)
    b = target_vector(orbit, m)

    if A.rank() < A.cols:
        raise ValueError("the supplied terms are linearly dependent, so the true "
                         "rank is below the number of terms; drop the redundant ones")
    if orbit in CYCLOTOMIC:
        return _fit_cyclotomic(orbit_qudits(orbit, m), terms, cols, b, *CYCLOTOMIC[orbit])
    G = sp.simplify(A.H * A)
    x = sp.simplify(G.inv() * (A.H * b))
    if any(not is_zero(v)[0] for v in (A * x - b)):
        return None
    return [sp.nsimplify(sp.radsimp(sp.simplify(v))) for v in x]


# Orbits whose target lives in a cyclotomic field strictly larger than the
# stabilizer states' field, solved inside that field: (p, order of the phases
# of a stabilizer state times sqrt(p^k), order of the target's phases).
# T3: stabilizer entries in {0, 1, w3, w3^2}, target in powers of w9.
# sqrt(T): stabilizer entries in {0, 1, i, -1, -i}, target in powers of
# zeta_16 = exp(i pi/8).
CYCLOTOMIC = {"T3": (3, 3, 9), "qubit_sqrtT": (2, 4, 16)}


def _fit_cyclotomic(n, terms, cols, b, p, stab_order, target_order):
    """Exact coefficients for an orbit of CYCLOTOMIC, solved inside Q(zeta)
    with zeta = exp(2 pi i / target_order), for n qudits of dimension p.

    The generic route through sympy's simplify produces coefficients for these
    orbits that are pages long (nested (-1)**(k/18) radicals for T3), or
    mis-simplifies them altogether (nsimplify on the sqrt(T) four-copy
    coefficients), and verifying a submission carrying them takes the verifier
    the better part of an hour. Every quantity here lives in one number field:
    a stabilizer term times sqrt(p^k) has entries that are 0 or a power of
    zeta^(target_order/stab_order), and the target times sqrt(p)^n has entries
    that are powers of zeta. Solving there gives each coefficient as a short
    polynomial in zeta with rational coefficients, times the power of sqrt(p)
    that restores the normalizations, and the check that the solution
    reproduces the target is exact field arithmetic rather than
    simplification.
    """
    from sympy.polys.matrices import DomainMatrix

    zeta = sp.exp(2 * sp.pi * sp.I / target_order)
    K = sp.QQ.algebraic_field(zeta)
    xz = K.from_sympy(zeta)
    step = target_order // stab_order
    dim = p ** n
    root = sp.sqrt(p)

    def as_power(z, order):
        """z (a numeric complex root of unity) as an exponent of w_order, or None."""
        if abs(z) < 1e-9:
            return None
        e = int(round(np.angle(z) / (2 * np.pi / order))) % order
        assert abs(z - np.exp(2j * np.pi * e / order)) < 1e-9
        return e

    rows = []
    for i in range(dim):
        row = []
        for j, col in enumerate(cols):
            z = complex(sp.N(col[i] * root ** int(terms[j]["k"]), 30))
            e = as_power(z, stab_order)
            row.append(K.zero if e is None else xz ** (step * e))
        rows.append(row)
    rhs = []
    for i in range(dim):
        e = as_power(complex(sp.N(b[i] * root ** n, 30)), target_order)
        rhs.append([K.zero if e is None else xz ** e])
    Am = DomainMatrix(rows, (dim, len(cols)), K)
    bm = DomainMatrix(rhs, (dim, 1), K)
    # pick independent rows through the rref of the transpose, then solve square
    _, piv = Am.transpose().rref()
    sq = DomainMatrix([rows[i] for i in piv], (len(piv), len(cols)), K)
    if len(piv) != len(cols):
        raise ValueError("the supplied terms are linearly dependent")
    x = sq.lu_solve(DomainMatrix([rhs[i] for i in piv], (len(piv), 1), K))
    if (Am * x - bm).to_Matrix() != sp.zeros(dim, 1):
        return None
    out = []
    for j in range(len(cols)):
        c = K.to_sympy(x[j, 0].element)
        c = sp.expand(c * root ** (int(terms[j]["k"]) - n))
        out.append(c)
    return out


def main(argv):
    if len(argv) < 2:
        print("usage: fit_coeffs.py <submission.json> [--write]")
        return 2
    path = argv[1]
    sub = json.load(open(path))
    try:
        c = fit(sub["orbit"], int(sub["m"]), sub["witness"]["terms"])
    except ValueError as exc:
        print(f"rejected: {exc}")
        return 1
    if c is None:
        print("no exact combination of these terms reproduces the target")
        return 1
    strs = [str(v) for v in c]
    print("exact coefficients:")
    for s in strs:
        print(f"  {s}")
    if "--write" in argv:
        sub["witness"]["coeffs"] = strs
        with open(path, "w") as f:
            json.dump(sub, f, indent=2)
            f.write("\n")
        print(f"written into {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
