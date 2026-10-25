---
id: v3r1t4s-heilbronn-records
type: entity
tags: [v3r1t4s, v3r1t4s/record-tables, kind/harvest]
inbound_links: 1
confidence: 0.8
last_ingested_sources: [".raw/V3R1T4S/bank/targets.json@7dd4480"]
status: "open"
priority: ""
notes: ""
category: record-tables
kind: harvest
tractability: 2
compute: "laptop-hours"
disclosure: open
status_checked: "2026-10-03"
---
# Heilbronn triangle problem: new best configurations (square, triangle, convex region)

# Overview

> Bank id `heilbronn-records` · harvest · tractability 2 · laptop-hours · disclosure **open**
> Bank says open as of 2026-10-03. Statuses go stale — re-check the primary source before any work.

## Statement

Place n points in a container (unit square, unit-area triangle, or an optimal convex region) to maximize the minimum area of a triangle formed by three of the points. Optimality is proven only for small n (square up to n=9; triangle up to n=8 per arXiv:2607.15021). Best known configurations for n up to 36 are tracked on Tej Stead's leaderboard. Optimality proofs: triangle n <= 8 (arXiv:2607.15021), square n <= 9 (arXiv:2603.11107). Rob Gardiner (renidrag) set square n = 21, 23, 25, 35 and triangle n = 20 records through Oct 2026; Lackovic (codrAlex) set convex n = 31 and 33 in late Sep 2026. Records change daily.

## Success criterion

Success means exact rational (or exactly specified algebraic) coordinates for n points (3 <= n <= 36) that meet all of the following. (1) Every point lies in the closed container, checked exactly. (2) The minimum over all C(n,3) triangles of |area|, computed in exact rational arithmetic and normalized as the leaderboard specifies (convex category: area of the convex hull of the points), is STRICTLY GREATER (direction: max) than the value shown for that (container, n) at https://math.tejstead.com/heilbronn re-fetched immediately before verification. (3) An independent local checker, written from the leaderboard's published normalization rules (not the site's own verifier; nothing is submitted), reproduces the value. Submitting to the leaderboard is the human's decision after review.

## Partial wins

- {"id": "p1", "statement": "An EinsteinArena Heilbronn record: a configuration for the EinsteinArena Heilbronn n=11 problem whose score, computed exactly under the arena's own scoring rules, strictly exceeds the live arena leaderboard best."}
- {"id": "p2", "statement": "A new optimality certificate: a re-runnable rigorous computer-assisted proof (interval branch-and-bound with logged subdivision that the skeptic re-executes) that the best known configuration is optimal for the unit square at n = 10 or the triangle at n = 9, beyond arXiv:2603.11107 / 2607.15021."}

## Verification

Independent script with fractions.Fraction. Check containment (for the triangle container, use the leaderboard's exact vertices). Compute all triangle areas as |det|/2 exactly and take the min. Apply the normalization: divide by the container area or the convex-hull area, with the hull computed exactly. Compare against the live leaderboard figure. Require a strict improvement, and report the relative improvement.

## Angles

- Use an active-set NLP. Maximize t subject to area_ijk >= t for the currently smallest ~50 triangles (with signs fixed by orientation), solved with SLSQP or IPOPT (pip cyipopt), re-identifying the active set iteratively. Then rationalize coordinates to high-precision fractions and re-verify exactly.
- Run symmetry-constrained searches (C2, C3, D2 or mirror symmetry) to cut dimension. Many records are symmetric, so enumerate symmetry types systematically for the less-attacked n (26-36).
- Exploit cross-container transfer. Map a strong triangle configuration into the convex category, then let the convex region adapt.
- Do a final 'equalization' polish: solve the KKT system for the active triangles with Newton's method in mpmath at 50 digits, then verify exactly.

## Pitfalls

- The records are moving daily, so re-fetch the leaderboard immediately before claiming.
- Floating-point min-area can mislead at the 1e-12 level. Certify with exact rationals.
- Area normalization differs between categories (unit square vs unit-area triangle vs convex hull).
- Gains of under 1e-9 relative may be treated as ties, so confirm with the leaderboard verifier.
- EinsteinArena also runs a Heilbronn n=11 problem with its own scoring, which is not the leaderboard.

## Sources

- https://math.tejstead.com/heilbronn
- https://github.com/renidrag/heilbronn-solutions
- https://github.com/codrAlex/heilbronn-search
- https://arxiv.org/abs/2607.15021
- https://arxiv.org/abs/2603.11107
- Status source: https://math.tejstead.com/heilbronn

## Citations

- [Problem page](../../../../.raw/V3R1T4S/known-unknowns/record-tables/heilbronn-records.md)
- [Bank entry](../../../../.raw/V3R1T4S/bank/targets.json) (id `heilbronn-records`, commit `7dd4480`)

## Related Nodes

- [[V3R1T4S Record tables]]
- [[V3R1T4S]]
