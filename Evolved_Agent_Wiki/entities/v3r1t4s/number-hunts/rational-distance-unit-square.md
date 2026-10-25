---
id: v3r1t4s-rational-distance-unit-square
type: entity
tags: [v3r1t4s, v3r1t4s/number-hunts, kind/standard]
inbound_links: 1
confidence: 0.8
last_ingested_sources: [".raw/V3R1T4S/bank/targets.json@7dd4480"]
status: "open"
priority: ""
notes: ""
category: number-hunts
kind: standard
tractability: 1
compute: "laptop-hours"
disclosure: open
status_checked: "2026-10-03"
---
# Rational distance problem for the unit square (four-distance problem)

# Overview

> Bank id `rational-distance-unit-square` · standard · tractability 1 · laptop-hours · disclosure **open**
> Bank says open as of 2026-10-03. Statuses go stale — re-check the primary source before any work.

## Statement

Is there a point (x, y) in the plane with rational distances to all four vertices of the unit square? Points on a diagonal, midline or edge are proven impossible (Yang Ji, arXiv 2105.05250), along with some prime-related cases. An unreviewed 2026 GitHub project (Mulatram-UwU, AI agent with human GPG-signing) claims an exhaustive search ruling out common denominators Q <= 5e10 (headline 2e10), with Lean checks of the reduction and search logic, and states it is not a solution.

## Success criterion

CONFIRMED only for explicit rationals x, y (exact fractions) such that x^2+y^2, (x-1)^2+y^2, x^2+(y-1)^2 and (x-1)^2+(y-1)^2 are all squares of rationals: each value in lowest terms has a perfect-square numerator and denominator, checked with fractions.Fraction and math.isqrt. Three-distance points never count.

## Partial wins

- {"id": "p1", "statement": "New impossible family: a complete proof that no point on an explicit infinite rational curve (e.g. a line through the center with a fixed non-axis, non-diagonal slope t, or a whole one-parameter family of such lines) has rational distances to all four vertices, beyond the diagonal/midline/edge cases of arXiv 2105.05250, with all genus/rank/Chabauty computations rerunnable by the verifier and the written argument checked line by line (Lean preferred)."}
- {"id": "p2", "statement": "New local obstruction: an extension of the congruence condition of arXiv 1904.12097 to additional primes, with a complete proof and a brute-force check over residues that the verifier reruns, ruling out a stated positive proportion of height-bounded candidates not excluded by the published condition."}

## Verification

Python fractions.Fraction exact computation and isqrt square tests on reduced numerator/denominator. For partial wins, line-by-line proof check plus rerun of all computer-algebra steps.

## Angles

- Three-distance solutions form a known parametrized surface (infinitely many points rational to three vertices). Parametrize it via a K3/elliptic fibration and search for fibers where the fourth distance condition gives an elliptic curve of positive rank, which is far more efficient than denominator scanning.
- Use symmetry: impose the point on a rational line through the center with slope t (not the diagonals/midlines already excluded). Each t gives a curve. Compute genus and use Chabauty on low-genus cases to prove impossibility families.
- Use local-global obstructions: extend the 2019 congruence condition (arXiv 1904.12097) to more primes to rule out larger fractions of height-bounded candidates.

## Pitfalls

- Only three of four distances rational: infinitely many such points are known.
- Floating-point near-misses.
- Trusting the unreviewed 5e10 bound as established fact.

## Sources

- https://arxiv.org/pdf/1904.12097
- https://arxiv.org/abs/2105.05250
- https://github.com/Mulatram-UwU/rational-distance-problem
- Status source: https://arxiv.org/pdf/1904.12097

## Citations

- [Problem page](../../../../.raw/V3R1T4S/known-unknowns/number-hunts/rational-distance-unit-square.md)
- [Bank entry](../../../../.raw/V3R1T4S/bank/targets.json) (id `rational-distance-unit-square`, commit `7dd4480`)

## Related Nodes

- [[V3R1T4S Number hunts]]
- [[V3R1T4S]]
