---
id: v3r1t4s-cap-set-dim7-dim8
type: entity
tags: [v3r1t4s, v3r1t4s/record-tables, kind/moonshot]
inbound_links: 1
confidence: 0.8
last_ingested_sources: [".raw/V3R1T4S/bank/targets.json@7dd4480"]
status: "open"
priority: ""
notes: ""
category: record-tables
kind: moonshot
tractability: 1
compute: "laptop-hours"
disclosure: open
status_checked: "2026-10-03"
---
# Larger cap sets in F_3^7 (beat 236) or F_3^8 (beat 512)

# Overview

> Bank id `cap-set-dim7-dim8` · moonshot · tractability 1 · laptop-hours · disclosure **open**
> Bank says open as of 2026-10-03. Statuses go stale — re-check the primary source before any work.

## Statement

A cap set in F_3^n contains no three distinct points on a line (equivalently, no x,y,z distinct with x+y+z=0). Exact maxima are known through n=6 (112). For n=7, 236 <= r(7) <= 288: the lower bound is Calderbank-Fishburn and the upper bound is Thackeray (2022, no 289-cap). For n=8, the best known is 512 (FunSearch 2023, matched by X-evolve 2025).

## Success criterion

Success means a set S of distinct vectors in {0,1,2}^n (n = 7 or 8) such that for every pair of distinct x,y in S, the third point -(x+y) mod 3 is not in S, verified exhaustively, with |S| STRICTLY GREATER (direction: max) than the best known cap size for that n at verification time (OEIS A090245, Wikipedia 'Cap set', fresh arXiv search; context on 2026-10-03: 236 for n=7, 512 for n=8). For n=7, |S| must be <= 288 (Thackeray's bound); larger means a bug.

## Partial wins

- {"id": "p1", "statement": "A cap in F_3^9 or F_3^10, verified exhaustively, strictly larger than the best published cap for that dimension at verification time (Edel's tables, FunSearch, X-evolve, OEIS, fresh arXiv search)."}
- {"id": "p2", "statement": "An explicit admissible set (or other mechanically checkable ingredient) giving a cap-set capacity lower bound strictly above the live value at https://teorth.github.io/optimizationproblems/constants/4a.html, with the bound formula recomputed independently."}
- {"id": "p3", "statement": "An upper bound r(7) <= 287, delivered as a DRAT (or similarly checkable) proof that the skeptic verifies with drat-trim."}

## Verification

Encode the vectors as base-3 integers in a set. For all pairs, compute the third point and check membership: about |S|^2/2 = 130k checks, instant. Check distinctness, coordinate ranges, and the dimension.

## Angles

- Search caps that are unions of orbits under a prescribed subgroup of AGL(n,3) (e.g. Singer-like cyclic groups on F_{3^7}, or coordinate-permutation groups of order 7 or 14). Solve max independent orbit selection exactly with CP-SAT.
- Extend Edel's product/doubling-type constructions: pair a large cap in F_3^a with one in F_3^b under twisted gluing rules, and search the twists.
- Use an SAT/ILP with symmetry breaking in n=7 seeking 237, starting from the 236-cap and asking for any 'swap k out, k+1 in' move with k <= 6.
- Use priority-function evolution (FunSearch style) with a better scoring function, e.g. counting future-blocking lines, run for hours on 10 cores.

## Pitfalls

- Collinearity in F_3^n means x+y+z = 0 (mod 3) for distinct points, not affine collinearity over R.
- Projective vs affine caps are different problems with different tables.
- 236 has stood since the 1990s-2004 despite FunSearch and X-evolve, so expect failure.

## Sources

- https://arxiv.org/html/2508.07932
- https://arxiv.org/abs/2206.09804
- https://oeis.org/A090245
- Status source: https://arxiv.org/html/2508.07932

## Citations

- [Problem page](../../../../.raw/V3R1T4S/known-unknowns/record-tables/cap-set-dim7-dim8.md)
- [Bank entry](../../../../.raw/V3R1T4S/bank/targets.json) (id `cap-set-dim7-dim8`, commit `7dd4480`)

## Related Nodes

- [[V3R1T4S Record tables]]
- [[V3R1T4S]]
