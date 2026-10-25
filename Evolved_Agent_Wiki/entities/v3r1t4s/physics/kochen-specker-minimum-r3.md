---
id: v3r1t4s-kochen-specker-minimum-r3
type: entity
tags: [v3r1t4s, v3r1t4s/physics, kind/moonshot]
inbound_links: 1
confidence: 0.8
last_ingested_sources: [".raw/V3R1T4S/bank/targets.json@7dd4480"]
status: "open"
priority: ""
notes: ""
category: physics
kind: moonshot
tractability: 1
compute: "laptop-days"
disclosure: open
status_checked: "2026-10-15"
---
# MOONSHOT - Smallest Kochen-Specker vector system in R^3: find one with at most 30 vectors (known range 24..31)

# Overview

> Bank id `kochen-specker-minimum-r3` · moonshot · tractability 1 · laptop-days · disclosure **open**
> Bank says open as of 2026-10-15. Statuses go stale — re-check the primary source before any work.

## Statement

A Kochen-Specker (KS) vector system in R^3 is a finite set of directions with no 0/1 colouring that gives exactly one 1 in every orthogonal triple and never two 1s on an orthogonal pair; its existence proves quantum contextuality. The smallest known has 31 vectors (Conway and Kochen). Lower bounds rose from 18 (Arends, Ouaknine, Wampler 2011) and 22 (Uijlen, Westerbaan 2014) to 24 (Zhengyu Li, Curtis Bright, Vijay Ganesh, arXiv:2306.13319, with SAT + computer algebra and DRAT certificates; independently Kirchweger, Peitl and Szeider), and in July 2026 Siddique and Mian (arXiv:2607.26413) machine-checked the geometric half of that proof. Trandafir and Cabello (arXiv:2501.11640) showed no 30-vector KS set arises from the 13-ray Yu-Oh set by completing bases and adding rays orthogonal to two previous ones, and conjectured 31 is minimal; Li, Bright, Trandafir and Cabello (arXiv:2604.19947, Apr 2026) proved Schutte's 33-ray set is the smallest KS set containing the complete 25-ray Yu-Oh extension. Separately, Cabello (arXiv:2508.07335) set the record for fewest orthogonal bases in dimension 3 at 14. The problem is open between 24 and 31.

## Success criterion

Success means a set of N <= 30 pairwise non-parallel nonzero vectors in R^3 with exact coordinates (integers, or elements of an explicit real number field) such that (a) its orthogonality graph, computed exactly, admits no {0,1}-colouring with exactly one 1 on every orthogonal triple and at most one 1 on every orthogonal pair, certified by a SAT solver run whose UNSAT result is checked by a DRAT proof checker (drat-trim or cake_lpr), and (b) N is STRICTLY LESS (direction: min) than 31, the smallest published KS system in R^3 found by an arXiv search re-run immediately before claiming (status source arXiv:2306.13319 and later papers). A complex C^3 set does not count for the main criterion.

## Partial wins

- {"id": "p1", "statement": "A KS set in R^3 or C^3 using at most 13 complete orthogonal bases (fewer than Cabello's 14, arXiv:2508.07335), certified the same way."}
- {"id": "p2", "statement": "A KS set in C^3 with at most 30 rays (exact coordinates in a cyclotomic field), certified the same way and checked against the literature on complex KS sets."}
- {"id": "p3", "statement": "An independently re-checkable improvement of the lower bound from 24 to 25 (complete enumeration with DRAT certificates for the combinatorial part and exact certificates for non-embeddability), which is laptop-weeks at best and must reuse no unverified Z3 steps."}

## Verification

Load vectors, verify exactly (sympy or flint) that they are pairwise non-parallel; build the orthogonality graph by exact dot products; list all triangles (orthogonal bases) and edges; encode the 010-colouring as CNF; run CaDiCaL/kissat with DRAT output and check the proof with drat-trim. Under a minute for N <= 40. Literature check: arXiv search for 'Kochen-Specker' minimum 3 dimensions.

## Angles

- Graph-first search: enumerate small squarefree, triangle-dense graphs that are non-010-colourable (SAT), then test embeddability in R^3 or C^3 with Groebner bases; Li-Bright-Ganesh showed the embeddability filter is the bottleneck, so better exact embeddability tests (rational parametrisation of orthogonal frames) help.
- Import from finite geometry: build candidate sets from root systems and lattice vectors with small integer coordinates (as Conway-Kochen and Peres sets do), and search subsets with simulated annealing on the number of colourings (#SAT as the objective).
- Import from quantum games: KS sets correspond to perfect quantum strategies in bipartite nonlocal games (Trandafir-Cabello); search for small perfect strategies for qutrit-qutrit games instead and extract the KS set.
- Complex coordinates: allow cube or eighth roots of unity; C^3 has more orthogonal triples per vector count, which could help partial win p2.

## Pitfalls

- Parallel vectors and sign duplicates: v and -v (or complex multiples) are the same ray; count rays, not vectors.
- Floating-point orthogonality creates spurious edges; orthogonality must be exact.
- The colouring rule must forbid two 1s on every orthogonal PAIR, not just triples; dropping the pair rule makes small 'KS sets' appear.
- A real KS set inside a complex search, or a state-independent contextuality set that is not KS (e.g. Yu-Oh's 13 rays), does not satisfy the criterion.
- Unverified UNSAT claims (solver output without a checked DRAT proof) are not certificates.

## Sources

- https://arxiv.org/abs/2306.13319
- https://arxiv.org/abs/2607.26413
- https://arxiv.org/abs/2501.11640
- https://arxiv.org/abs/2604.19947
- https://arxiv.org/abs/2508.07335
- Status source: https://arxiv.org/abs/2306.13319

## Citations

- [Problem page](../../../../.raw/V3R1T4S/known-unknowns/physics/kochen-specker-minimum-r3.md)
- [Bank entry](../../../../.raw/V3R1T4S/bank/targets.json) (id `kochen-specker-minimum-r3`, commit `7dd4480`)

## Related Nodes

- [[V3R1T4S Physics]]
- [[V3R1T4S]]
