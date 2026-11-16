"""Exact certificate: chi(|cat_2>) >= 1, closing chi(|cat_2>) = 1.

|cat_2> = 2^{-1/2}(|T>^{ot 2} + (Z|T>)^{ot 2}) = (|00> + i|11>)/sqrt(2) has
exact squared Euclidean norm |||cat_2>||^2 = 1 > 0. Since the empty sum of zero
stabilizer states is the zero vector, every non-zero state has stabilizer rank
at least 1. Paired with bounds/cat-m2-upper-1.json (verified), this closes the
m = 2 cell of the magic-cat family at chi(|cat_2>) = 1.

Printed claim:
  CERTIFIED chi(cat_2) >= 1
"""

from __future__ import annotations

import os
import sys
import sympy as sp

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from stabrank_verify import target_vector  # noqa: E402


def main() -> int:
    v = target_vector("cat", 2)
    ref = sp.Matrix([1, 0, 0, sp.I])
    if len(v) != 4:
        print(f"unexpected cat_2 dimension: {len(v)}", file=sys.stderr)
        return 1
    for a in range(4):
        for b in range(a + 1, 4):
            minor = sp.simplify(sp.expand(v[a] * ref[b] - v[b] * ref[a]))
            if minor != 0:
                print(f"2x2 minor ({a},{b}) against |00> + i|11> did not vanish: {minor}", file=sys.stderr)
                return 1
    norm_sq = sp.simplify(sp.expand(sum(x * sp.conjugate(x) for x in v)))
    if norm_sq != 1:
        print(f"cat_2 norm squared != 1: {norm_sq}", file=sys.stderr)
        return 1
    print(f"exact symbolic check: |cat_2> proportional to |00> + i|11> and |||cat_2>||^2 = {norm_sq} > 0")
    print("CERTIFIED chi(cat_2) >= 1")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
