"""Exact certificate: chi(|qubit_H>^{ot m}) >= 5 and chi(|qubit_T>^{ot m}) >= 5 for m = 7..10.

Extends `verify_challenge/cert_qubit_galois_m5_m6_rank4.py` (which proves
chi(|qubit_H>^{ot 5}) >= 5 and chi(|qubit_T>^{ot 5}) >= 5 in exact Z[i] /
Z[i, sqrt(3)] arithmetic and lifts to m = 6) to m = 7, 8, 9, 10 by
computational-basis projection monotonicity (<0|^{ot (m - 5)} (x) I^{ot 5}),
giving a fast self-contained verified-tier floor (~7 s on 1 core) alongside the
attested rank-6 bounds on the board.

Printed claims:
  CERTIFIED chi(qubit_H^5) >= 5
  CERTIFIED chi(qubit_H^6) >= 5
  CERTIFIED chi(qubit_T^5) >= 5
  CERTIFIED chi(qubit_T^6) >= 5
  CERTIFIED chi(qubit_H^7) >= 5
  CERTIFIED chi(qubit_H^8) >= 5
  CERTIFIED chi(qubit_H^9) >= 5
  CERTIFIED chi(qubit_H^10) >= 5
  CERTIFIED chi(qubit_T^7) >= 5
  CERTIFIED chi(qubit_T^8) >= 5
  CERTIFIED chi(qubit_T^9) >= 5
  CERTIFIED chi(qubit_T^10) >= 5
"""

from __future__ import annotations

import os
import sys
import sympy as sp

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from stabrank_verify import orbit_state, target_vector  # noqa: E402
import cert_qubit_galois_m5_m6_rank4  # noqa: E402


def verify_symbolic_qubit_projections() -> None:
    # 1. Purely symbolic 2x2-minor projective checks against orbit_state
    qh = orbit_state("qubit_H")
    ref_h = sp.Matrix([1 + sp.sqrt(2), 1])
    if sp.simplify(sp.expand(qh[0] * ref_h[1] - qh[1] * ref_h[0])) != 0:
        raise AssertionError("2x2 minor mismatch for orbit_state('qubit_H')")

    qt = orbit_state("qubit_T")
    c0_sq = sp.trigsimp(qt[0] ** 2)
    s0 = sp.simplify(qt[1] / sp.exp(sp.I * sp.pi / 4))
    s0_sq = sp.trigsimp(s0 ** 2)
    if not (bool(qt[0] > 0) and bool(s0 > 0)):
        raise AssertionError("Sign check failed for orbit_state('qubit_T') trig entries")
    # Verify (qt[0] / s0)^2 == ((1 + sqrt(3)) / sqrt(2))^2 = 2 + sqrt(3) and phase == (1 + I)/sqrt(2)
    if sp.simplify(c0_sq - s0_sq * (2 + sp.sqrt(3))) != 0:
        raise AssertionError("Modulus ratio mismatch for orbit_state('qubit_T')")
    if sp.simplify(sp.expand_complex(sp.exp(sp.I * sp.pi / 4) * sp.sqrt(2) - (1 + sp.I))) != 0:
        raise AssertionError("Phase mismatch for orbit_state('qubit_T')")

    # 2. Purely symbolic non-zero <0| amplitude and two-copy computational slice check
    for name in ("qubit_H", "qubit_T"):
        v1 = orbit_state(name)
        amp0 = sp.simplify(v1[0])
        if amp0 == 0 or not bool(amp0 > 0):
            raise AssertionError(f"symbolic <0|{name}> <= 0")
        v2 = target_vector(name, 2)
        for j in range(2):
            if sp.simplify(sp.trigsimp(v2[j] - amp0 * v1[j])) != 0:
                raise AssertionError(f"slice (<0| (x) I)|{name}>^2 mismatch at {j}")


def main() -> int:
    verify_symbolic_qubit_projections()
    rc = cert_qubit_galois_m5_m6_rank4.main()
    if rc is not None and rc != 0:
        return int(rc)
    print("symbolic projection checks passed for qubit_H and qubit_T; lifting chi >= 5 to m = 7..10")
    for m in (7, 8, 9, 10):
        print(f"CERTIFIED chi(qubit_H^{m}) >= 5")
    for m in (7, 8, 9, 10):
        print(f"CERTIFIED chi(qubit_T^{m}) >= 5")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
