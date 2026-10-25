---
id: v3r1t4s-erdos-506-circles-small-n
type: entity
tags: [v3r1t4s, v3r1t4s/erdos-and-proofs, kind/harvest]
inbound_links: 1
confidence: 0.8
last_ingested_sources: [".raw/V3R1T4S/bank/targets.json@7dd4480"]
status: "open"
priority: ""
notes: ""
category: erdos-and-proofs
kind: harvest
tractability: 2
compute: "laptop-hours"
disclosure: open
status_checked: "2026-10-03"
---
# Erdos #506: minimum number of circles determined by n points, beating or closing the n <= 393 gap

# Overview

> Bank id `erdos-506-circles-small-n` · harvest · tractability 2 · laptop-hours · disclosure **open**
> Bank says open as of 2026-10-03. Statuses go stale — re-check the primary source before any work.

## Statement

Find the minimum number m(n) of circles through >= 3 of n points, where the points are not all on a line or circle. For n > 393, m(n) = F(n) = C(n-1,2) + 1 - floor((n-1)/2) (Elliott 1967, corrected by Purdy-Smith; Balintova-Balint 1994). For n <= 393 it is open. Forum (mzn, 2026-08-18): m(5)=5, m(6)=8, m(7)=11, m(8)=17, with exact-arithmetic configurations (versus F = 5, 9, 13, 19), and m(9) <= 25 = F(9), with no way found to beat it. Forum (Peysakhov, 2026-06-11): 18 circles at n=8.

## Success criterion

Confirmed: (A) exact coordinates for n >= 9 points, not all collinear and not all concyclic (exact nondegeneracy as in 506.lean), determining strictly fewer than F(n) = C(n-1,2) + 1 - floor((n-1)/2) circles (F(9)=25, F(10)=33, F(11)=41, F(12)=51) AND strictly fewer (direction: min) than the best value posted on the forum thread for that n AT VERIFICATION TIME. Or (B) a complete proof that m(n) = F(n) for every 9 <= n <= 393.

## Partial wins

- {"id": "p1", "statement": "A rigorous lower-bound proof establishing m(n) exactly for some n in {6, 7, 8} (matching the forum configuration), provided no matching lower-bound proof was already posted on the forum."}
- {"id": "p2", "statement": "A complete proof that m(9) = 25."}
- {"id": "p3", "statement": "A complete proof that the formula m(n) = F(n) holds for all n > N0 with an explicit N0 < 393 (lowering the Elliott/Balintova-Balint threshold), with every constant recomputed exactly."}

## Verification

(A) For every non-collinear triple, compute the exact circumcircle (centre and r^2 as rationals or exact field elements), deduplicate and count. Independent re-implementation: union-find on triples using the exact 4-point concyclicity determinant. Confirm the configuration is neither all collinear nor all concyclic, then compare with F(n). (B) Line-by-line refereeing of the constants in the Elliott-type argument; recompute every numeric inequality exactly.

## Angles

- Lift to the sphere by inverse stereographic projection. Circles correspond to planes not through the pole and lines to planes through the pole. So minimise (#planes containing >= 3 points) - (#those through the pole). Search orbit configurations of finite rotation groups (prisms, antiprisms, cuboctahedron, Johnson solids, two parallel regular polygons plus poles) and choose the pole on as many plane sections as possible. Use rational points on S^2 for exact arithmetic.
- Extend mzn's n=8 cube and Peysakhov's two-squares configurations by adding points lying on many existing circles, or by moving to 3-fold or 4-fold symmetric families with many concyclic 4-sets and collinear triples. Collinear triples are 'free' because they determine no circle.
- For (B): revisit Elliott's argument with modern tools. Lin-Makhul-Mojarrad-Schicho-Swanepoel-de Zeeuw ('On sets defining few ordinary circles') handles sufficiently large n. Make their constants explicit, and use inversion to turn Melchior/Csima-Sawyer-type ordinary-line inequalities into circle bounds.

## Pitfalls

- Counting lines as circles.
- Floating-point concyclicity.
- n <= 9 data is already on the forum.
- The F(n) formula is proved only for n > 393, so beating it at n <= 8 is already known.
- Nondegeneracy convention: the Lean statement uses 'not all collinear and not all concyclic'; do not switch to 'no three collinear' silently.
- The forum's small-n 'exact' values may be upper bounds only; check whether a matching lower-bound proof was posted before citing them as m(n).
- Degenerate configurations (all concyclic, or all but one collinear) are excluded by the Lean statement; check the exact nondegeneracy in 506.lean.

## Sources

- https://www.erdosproblems.com/506
- https://www.erdosproblems.com/forum/thread/506
- https://github.com/google-deepmind/formal-conjectures/blob/main/FormalConjectures/ErdosProblems/506.lean
- Status source: https://www.erdosproblems.com/506

## Citations

- [Problem page](../../../../.raw/V3R1T4S/known-unknowns/erdos-and-proofs/erdos-506-circles-small-n.md)
- [Bank entry](../../../../.raw/V3R1T4S/bank/targets.json) (id `erdos-506-circles-small-n`, commit `7dd4480`)

## Related Nodes

- [[V3R1T4S Erdős problems and proofs]]
- [[V3R1T4S]]
