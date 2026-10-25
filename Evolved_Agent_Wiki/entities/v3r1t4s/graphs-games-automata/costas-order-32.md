---
id: v3r1t4s-costas-order-32
type: entity
tags: [v3r1t4s, v3r1t4s/graphs-games-automata, kind/moonshot]
inbound_links: 1
confidence: 0.8
last_ingested_sources: [".raw/V3R1T4S/bank/targets.json@7dd4480"]
status: "open"
priority: ""
notes: ""
category: graphs-games-automata
kind: moonshot
tractability: 1
compute: "laptop-hours"
disclosure: open
status_checked: "2026-10-03"
---
# First Costas array of order 32 or 33

# Overview

> Bank id `costas-order-32` · moonshot · tractability 1 · laptop-hours · disclosure **open**
> Bank says open as of 2026-10-03. Statuses go stale — re-check the primary source before any work.

## Statement

A Costas array of order n is an n x n permutation matrix in which all n(n-1)/2 displacement vectors between pairs of dots are distinct. Costas arrays are conjectured to exist for all n, but no array of order 32 or 33 is known. Orders 32 and 33 are the smallest open cases.

## Success criterion

CONFIRMED only for a permutation pi of {0..n-1} with n = 32 or 33 such that all n(n-1)/2 displacement vectors (j-i, pi(j)-pi(i)), i<j, are distinct, checked exhaustively by two independent methods (vector set size and difference-triangle rows), and no Costas array of that order is listed at verification time on the live primary page https://en.wikipedia.org/wiki/Costas_array (direction: none; existence target), in Beard's database of known arrays, or in a fresh arXiv/literature search. 'Almost Costas' arrays are never results.

## Partial wins

- {"id": "p1", "statement": "A complete enumeration of main-diagonal-symmetric Costas arrays at order 43 (one past the 37-42 census of arXiv 2608.28690), reproduced by an independent solver, with the list of arrays found (or the certified empty list) and each array checked exactly."}
- {"id": "p2", "statement": "A complete enumeration, at order 32 or 33, of a symmetry class other than main-diagonal symmetry (stated precisely) with an independently reproduced search or DRAT-checked UNSAT proof, where no published census covers that class at that order."}
- {"id": "p3", "statement": "An exhaustive, independently reproduced proof that no order-32 Costas array arises from a precisely stated perturbation family of algebraic arrays (e.g. Welch or Golomb/Lempel arrays of orders 30-34 with at most r rows/columns changed or corner dots added/removed, r stated)."}

## Verification

Python: build the set of the n(n-1)/2 vectors (j-i, π[j]-π[i]) and assert its size is n(n-1)/2. Also check the equivalent difference-triangle condition (distinct entries in each row of the difference triangle) as an independent second check.

## Angles

- Modify algebraic constructions: take Welch (p=31, 37) and Golomb/Lempel (q=31, 32 as 2^5, 37) arrays of nearby orders, remove or add corner dots, and search for 'repairs' with SAT over small row/column perturbations.
- Symmetric search: require main-diagonal or other symmetry (the 2608.28690 census shows symmetric families are fully enumerable to order 42). Try other symmetry types at order 32 with a SAT plus symmetry-breaking encoding (pysat).
- Exploit the order-32 field: GF(32) Golomb constructions give order 30. Search for two-dot extensions under every primitive-element pair systematically.
- Annealing on permutations with an exact incremental collision count, plus restarts seeded from near-Costas arrays. Known to plateau at a few collisions, but it is cheap to run in the background.
- Avoid main-diagonal symmetry (ruled out by 2608.28690). Explore other dihedral-type symmetric classes or near-algebraic arrays, e.g. Welch W_1(37) arrays with 4-5 corner dots removed plus repair by local search.
- Do backtracking with difference-triangle constraints and bitset pruning (Drakakis/Rickard methods), run on 10 cores over randomized row orders. It is unlikely to finish but can sample deep partial arrays.
- Use SAT with pysat: one-hot permutation encoding plus at-most-one constraints per displacement vector. Use cube-and-conquer seeded by fixing the first 3-4 columns.
- Partial win: 'near-Costas' arrays of order 32 with the fewest repeated vectors, compared against published deficiency studies (Jedwab-Wodlinger).

## Pitfalls

- 'Almost Costas' arrays with 1-2 repeated vectors are not results.
- Off-by-one errors in order (an order-31 Welch array is already known).
- Exhaustive enumeration of order 32 was estimated at about a year on tens of thousands of CPUs, so do not try it.
- Mistaking a Golomb-ruler-like partial array or a non-permutation for a Costas array.
- Main-diagonal symmetric searches at these orders are proven fruitless.
- Experts estimate exhaustive enumeration of order 32 needs massive compute, so the realistic outcome is a partial or negative result.

## Sources

- https://en.wikipedia.org/wiki/Costas_array
- https://arxiv.org/pdf/1102.5727
- https://arxiv.org/abs/2608.28690
- Status source: https://en.wikipedia.org/wiki/Costas_array

## Citations

- [Problem page](../../../../.raw/V3R1T4S/known-unknowns/graphs-games-automata/costas-order-32.md)
- [Bank entry](../../../../.raw/V3R1T4S/bank/targets.json) (id `costas-order-32`, commit `7dd4480`)

## Related Nodes

- [[V3R1T4S Graphs, games and automata]]
- [[V3R1T4S]]
