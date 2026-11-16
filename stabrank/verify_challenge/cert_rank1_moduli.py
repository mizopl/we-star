"""Certificate: chi >= 2 for |S>, |N>, |H3>, |H>, and |T> at m=1 and for |H>^2 and
|T>^2 (qubits), exactly.

A stabilizer state has one modulus on its support (the amplitudes are a
root of unity times 1/sqrt(|support|)), so a state whose nonzero
amplitudes take two different moduli is not a stabilizer state and its
rank is at least 2. |S> = (|1> - |2>)/sqrt2 has support of size 2, which is
not an affine subspace of F_3 (those have size 1 or 3), and the qubit
states |H>^2 and |T>^2 have amplitude moduli cos^2 and cos sin of an angle
whose cosine and sine differ; |N> = (1, 1, -2)/sqrt6, |H3> (moduli sqrt((3 + sqrt3)/6)
and sqrt((3 - sqrt3)/12)), |H> = (cos pi/8, sin pi/8), and |T> (cos beta, sin beta with
cos 2beta = 1/sqrt3) each have two moduli on their support. Every step is exact in sympy.

Printed claims: CERTIFIED chi(S^1) >= 2
                CERTIFIED chi(N^1) >= 2
                CERTIFIED chi(H3^1) >= 2
                CERTIFIED chi(qubit_H^1) >= 2
                CERTIFIED chi(qubit_T^1) >= 2
                CERTIFIED chi(qubit_H^2) >= 2
                CERTIFIED chi(qubit_T^2) >= 2
"""

import os
import sys

import sympy as sp

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from stabrank_verify import ORBIT_P, target_vector  # noqa: E402


def moduli_squared(v):
    return [sp.simplify(sp.expand(a * sp.conjugate(a))) for a in v if sp.simplify(a) != 0]


CELLS = (("S", 1), ("N", 1), ("H3", 1), ("qubit_H", 1), ("qubit_T", 1), ("qubit_H", 2), ("qubit_T", 2))


def main():
    ok = True
    for orbit, m in CELLS:
        v = target_vector(orbit, m)
        p = ORBIT_P[orbit]
        mods = moduli_squared(v)
        support = len(mods)
        distinct = sp.simplify(mods[0] - mods[-1]) != 0 or any(
            sp.simplify(a - b) != 0 for a in mods for b in mods)
        affine_sizes = {p ** k for k in range(m + 1)}
        reason = []
        if support not in affine_sizes:
            reason.append(f"support {support} is not the size {sorted(affine_sizes)} of an affine flat")
        if distinct:
            vals = sorted({sp.nsimplify(x) for x in mods}, key=lambda e: float(e))
            reason.append(f"moduli squared take {len(vals)} values {vals}")
        if not reason:
            print(f"{orbit} m={m}: could not exclude a stabilizer state", file=sys.stderr)
            ok = False
            continue
        print(f"{orbit} m={m}: not a stabilizer state, " + "; ".join(reason))
    if not ok:
        return 1
    for orbit, m in CELLS:
        print(f"CERTIFIED chi({orbit}^{m}) >= 2")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
