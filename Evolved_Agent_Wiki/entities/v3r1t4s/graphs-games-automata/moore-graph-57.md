---
id: v3r1t4s-moore-graph-57
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
compute: "pure thought"
disclosure: open
status_checked: "2026-10-03"
---
# The missing Moore graph (degree 57, diameter 2)

# Overview

> Bank id `moore-graph-57` · moonshot · tractability 1 · pure thought · disclosure **open**
> Bank says open as of 2026-10-03. Statuses go stale — re-check the primary source before any work.

## Statement

Does a 57-regular graph on 3250 vertices with diameter 2 and girth 5 exist? This is srg(3250,57,0,1), the last open case of the Hoffman-Singleton theorem.

## Success criterion

CONFIRMED only for an explicit adjacency list on 3250 vertices that is 57-regular with A^2 + A - 56I = J, checked exactly in integers. A non-existence argument is NOT a confirmed claim unless fully formalized in Lean or Isabelle and checked. Partial wins are logged, not claimed.

## Partial wins

- {"id": "p1", "statement": "A computer-verified exclusion (reproducible code, exact arithmetic; formal proof preferred) of automorphisms of a specific odd prime order p, or of a specific automorphism-group order, that is not already excluded in the literature (arXiv 2606.29183 and its references, checked fresh); if it relies on 2606.29183 (unrefereed), the dependency must be stated."}
- {"id": "p2", "statement": "An independent machine-checked (Lean/Isabelle) or fully reproducible exact-computation verification of the arXiv 2606.29183 theorem that a Moore graph of degree 57 has no involutory automorphisms."}

## Verification

Load the adjacency matrix as a 3250 x 3250 int8 array. Check symmetry, zero diagonal and all row sums equal to 57. Compute A@A + A in int32 and compare with 56I + J exactly. For partial results, independently re-run the eigenvalue and character-table or fixed-point arguments, for example with GAP or sympy, in exact arithmetic.

## Angles

- Build on the 'no involutions' result: push the fixed-subgraph analysis to elements of order 3, 5, 7 and 11, using eigenvalue multiplicity (1729/1520) and trace constraints. A computer-checked exclusion of a prime order is a partial win.
- Search for constructions with large odd-order groups acting semiregularly (orbit matrices or quotient matrices over Z_{2·5^3·13} subgroups), using CP-SAT on orbit matrices.
- Mine 'potential subgraphs' work (MDPI Symmetry 16(12):1563) for forbidden configurations, and encode them as SAT on small neighbourhood structures.

## Pitfalls

- Long history of incorrect non-existence claims. Treat any 'proof' with extreme suspicion.
- Floating-point eigenvalue checks are not proofs.
- 2606.29183 is a recent single-author preprint and has not been refereed. Partial results that build on it inherit that risk, so state the dependency explicitly.

## Sources

- https://arxiv.org/html/2606.29183
- https://www.mdpi.com/2073-8994/16/12/1563
- https://arxiv.org/pdf/2210.09577
- Status source: https://arxiv.org/html/2606.29183

## Citations

- [Problem page](../../../../.raw/V3R1T4S/known-unknowns/graphs-games-automata/moore-graph-57.md)
- [Bank entry](../../../../.raw/V3R1T4S/bank/targets.json) (id `moore-graph-57`, commit `7dd4480`)

## Related Nodes

- [[V3R1T4S Graphs, games and automata]]
- [[V3R1T4S]]
