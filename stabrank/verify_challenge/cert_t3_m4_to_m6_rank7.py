"""Exact certificate: chi(|T3>^{ot m}) >= 7 for m = 4, 5, 6 by projection monotonicity.

On `main`, `bounds/T3-m3-lower-7.json` (`verify_challenge/cert_t3m3_rank7.py`,
`exact: true`) proves chi(|T3>^{ot 3}) >= 7 in exact modular arithmetic over
Z[omega_3]. By computational-basis projection monotonicity, since
<0|T3> = 3^{-1/2} != 0 and (<0| (x) I)|T3>^{ot (k+1)} = 3^{-1/2} |T3>^{ot k},
applying (<0|^{ot (m - 3)} (x) I^{ot 3}) maps any r-term stabilizer
decomposition of |T3>^{ot m} to an at-most-r-term stabilizer decomposition of
|T3>^{ot 3} (Lean: stabRankP_powVecP_mono in LeanProofs/Stabilizer/SliceP.lean).

This script verifies the projective identity of |T3> and its two-copy slice
symbolically against `stabrank_verify.orbit_state` and `target_vector`, runs
`cert_t3m3_rank7.main()` from scratch, and certifies m = 4, 5, 6.

Printed claims:
  CERTIFIED chi(T3^3) >= 7
  CERTIFIED chi(T3^4) >= 7
  CERTIFIED chi(T3^5) >= 7
  CERTIFIED chi(T3^6) >= 7
"""

from __future__ import annotations

import os
import sys
import sympy as sp

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from stabrank_verify import orbit_state, target_vector  # noqa: E402
import cert_t3m3_rank7  # noqa: E402


def verify_symbolic_t3() -> None:
    w9 = sp.exp(2 * sp.pi * sp.I / 9)
    ref1 = sp.Matrix([1, w9, w9 ** 2])
    t3 = orbit_state("T3")
    for a in range(3):
        for b in range(a + 1, 3):
            if sp.simplify(sp.expand(t3[a] * ref1[b] - t3[b] * ref1[a])) != 0:
                raise AssertionError(f"2x2 minor ({a},{b}) mismatch against orbit_state('T3')")
    amp0 = sp.simplify(t3[0])
    if amp0 == 0:
        raise AssertionError("symbolic <0|T3> == 0")
    t3_2 = target_vector("T3", 2)
    sliced = sp.Matrix([t3_2[0], t3_2[1], t3_2[2]])
    for j in range(3):
        if sp.simplify(sliced[j] - amp0 * t3[j]) != 0:
            raise AssertionError(f"slice (<0| (x) I)|T3>^2 mismatch at index {j}")


def main() -> int:
    verify_symbolic_t3()
    code = cert_t3m3_rank7.main()
    if code != 0:
        return code
    print("symbolic projection check passed: <0|T3> = 3^(-1/2) != 0, lifting chi >= 7 to m = 4, 5, 6")
    for m in (4, 5, 6):
        print(f"CERTIFIED chi(T3^{m}) >= 7")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
