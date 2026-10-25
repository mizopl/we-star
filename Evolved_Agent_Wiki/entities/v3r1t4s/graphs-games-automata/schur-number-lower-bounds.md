---
id: v3r1t4s-schur-number-lower-bounds
type: entity
tags: [v3r1t4s, v3r1t4s/graphs-games-automata, kind/harvest]
inbound_links: 1
confidence: 0.8
last_ingested_sources: [".raw/V3R1T4S/bank/targets.json@7dd4480"]
status: "open"
priority: ""
notes: ""
category: graphs-games-automata
kind: harvest
tractability: 2
compute: "laptop-hours"
disclosure: open
status_checked: "2026-10-03"
---
# Raise the lower bound on Schur numbers S(6) / S(7) or weak Schur WS(6)

# Overview

> Bank id `schur-number-lower-bounds` · harvest · tractability 2 · laptop-hours · disclosure **open**
> Bank says open as of 2026-10-03. Statuses go stale — re-check the primary source before any work.

## Statement

S(k) is the largest N such that {1..N} can be partitioned into k sum-free sets (no x+y=z within a part, x=y allowed); WS(k) is the weak variant (x != y). Exact values are known only for k <= 5 (S(5)=160, Heule 2017). Find an explicit partition beating the best known lower bound for S(6), S(7), WS(6) or WS(7).

## Success criterion

(1) An explicit assignment color: {1..N} -> {1..k}, k in {6, 7}. (2) No monochromatic solution of x+y=z, with x=y allowed for Schur and x != y required for weak Schur, checked exhaustively in O(N^2) by two independent implementations. (3) N STRICTLY GREATER (direction: max) than the best known lower bound in the largest-N convention at verification time, taken from the live tables https://oeis.org/A045652 (Schur) or https://oeis.org/A118771 (weak Schur, converting its smallest-failing convention by subtracting 1), arXiv:2607.15034 and a fresh arXiv search (2026-10-03 context: S(6) 536, S(7) 1696, WS(6) 582, WS(7) 1740). (4) Bounds obtained only by plugging into recurrences are not records.

## Partial wins

- {"id": "p1", "statement": "An explicit, directly verified k-coloring for some k >= 8 (Schur or weak Schur) whose N strictly exceeds the best value at verification time in arXiv 2607.15034, OEIS A045652/A118771 and a fresh search (recurrence-only bounds excluded)."}
- {"id": "p2", "statement": "A DRAT/LRAT-checked UNSAT proof (independent encoding) that no sum-free 6-partition of {1..537} exists within a precisely stated template or symmetry class (e.g. the Fredricksen-Sweet symmetric structure or a Rowley-style S-template) not previously ruled out in the literature."}

## Verification

Independent Python check: for each color class C (as a set), assert that no x,y in C have x+y in C (for weak Schur, require x<y). This is O(N^2), under 3M operations for N=1700. Check the version convention explicitly: A045652 (S(5)=160) versus A030126 (S(5)=161).

## Angles

- Template and symmetry search in the style of Rowley's S-templates and 2607.15034's shifted S-templates. Search for template colorings that extend a good S(4) or S(5) coloring, using SAT for the special label cells.
- Symmetric sum-free partitions (Fredricksen-Sweet: color(x) = color(N+1-x) structure). Encode them as SAT with symmetry, which roughly halves the variables, and use cube-and-conquer over 10 cores for N=537 with 6 colors.
- Incremental SAT growth: take the best known 536-coloring, extend N by 1, and repair with local search (WalkSAT or probSAT) over a sliding window of recolorable elements.
- For weak Schur, start from the Ahmed et al. 2023 constructions and use SAT on the tail.
- Use symmetric colourings: impose c(x) relations with c(N+1-x) (or the Abbott-Hanson/template structure used in 2607.15034) to shrink the SAT instance, then solve with CaDiCaL/kissat.
- Extend Fredricksen-Sweet's 536 colouring: run SAT with assumptions fixing most of the colouring and freeing a window near the end, then search for 537.
- Use cube-and-conquer on 10 cores with symmetry breaking (colour order fixed by first occurrence).
- Use template- or modular-based constructions (colouring determined by x mod m with exceptions) and exhaustive search over small templates.

## Pitfalls

- Off-by-one between conventions: largest partitionable N versus smallest failing N (S(5)=160 vs 161).
- Schur requires x=y to be forbidden as well (2x in the same part as x); weak Schur does not. Do not mix the two.
- Bounds obtained from recurrences, such as S(k+2) >= 10S(k)+2, are not new direct colorings for k=6 or 7.
- Forgetting the x=y case (x+x=z), which weak Schur numbers omit. Do not confuse S(6) with WS(6).
- S(6) >= 536 has resisted 26 years of SAT attempts, so expect failure and report partial results honestly.
- An off-by-one in N: a colouring of {1..536} only matches the record.

## Sources

- https://oeis.org/A045652
- https://oeis.org/A118771
- https://doi.org/10.37236/1510
- https://arxiv.org/abs/2607.15034
- https://arxiv.org/abs/1711.08076
- Status source: https://oeis.org/A045652

## Citations

- [Problem page](../../../../.raw/V3R1T4S/known-unknowns/graphs-games-automata/schur-number-lower-bounds.md)
- [Bank entry](../../../../.raw/V3R1T4S/bank/targets.json) (id `schur-number-lower-bounds`, commit `7dd4480`)

## Related Nodes

- [[V3R1T4S Graphs, games and automata]]
- [[V3R1T4S]]
