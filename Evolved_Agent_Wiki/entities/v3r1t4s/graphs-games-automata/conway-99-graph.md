---
id: v3r1t4s-conway-99-graph
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
# Conway's 99-graph, srg(99,14,1,2)

# Overview

> Bank id `conway-99-graph` · moonshot · tractability 1 · laptop-hours · disclosure **open**
> Bank says open as of 2026-10-03. Statuses go stale — re-check the primary source before any work.

## Statement

Does a strongly regular graph with parameters (99,14,1,2) exist? Equivalently: is there a 99-vertex graph in which every edge lies in exactly one triangle and every non-adjacent pair has exactly two common neighbours? Conway offered $1000 for an answer.

## Success criterion

CONFIRMED only for an explicit 99 x 99 symmetric 0/1 adjacency matrix with zero diagonal satisfying A^2 = 14I + A + 2(J - I - A), checked exactly in integers. Non-existence requires a formal (Lean/Isabelle) proof or a fully reproducible exhaustive computation with UNSAT certificates checked by drat-trim/cake_lpr and an independently re-derived encoding; never a confirmed claim without that. Near misses (any fraction of constraints satisfied) are never results.

## Partial wins

- {"id": "p1", "statement": "A DRAT/LRAT-checked (independently re-encoded) proof that no srg(99,14,1,2) admits a specified automorphism (stated prime order and fixed-point/cycle structure) that is not already excluded by arXiv 2308.02978, its refinements, or arXiv 2608.11211 (literature check at verification time)."}
- {"id": "p2", "statement": "An independent machine-checked re-derivation (Lean/Isabelle, or SAT with DRAT-checked proofs from an independent encoding) of the forced-structure reduction of arXiv 2608.11211."}

## Verification

Exact integer matrix identity check in numpy (int32). For non-existence or UNSAT claims, require DRAT/LRAT proofs checked by drat-trim or cake_lpr, together with an independent re-derivation of the encoding.

## Angles

- Prescribe automorphism groups not yet excluded by the 2308.02978 analysis (orders 3 and 11 actions) and solve the orbit-matrix SAT problem.
- Local structure: each vertex neighbourhood is 7 disjoint edges, and the graph contains 693 triangles that form a partial geometry or linear space. Search for the corresponding pg(2,6,1)-like geometry with exact cover.
- Use the 2608.11211 forced-structure reduction as a starting point with a different SAT encoding (pysat with cadical, cube-and-conquer over 10 cores).

## Pitfalls

- Many repos claim 'near misses'. A near miss is not a result.
- Do not confuse it with Conway's other $1000 problems or with srg(99,...) relatives.

## Sources

- https://arxiv.org/abs/2608.11211
- https://arxiv.org/pdf/2308.02978
- https://github.com/tonykoval/hunting-srg99
- Status source: https://arxiv.org/abs/2608.11211

## Citations

- [Problem page](../../../../.raw/V3R1T4S/known-unknowns/graphs-games-automata/conway-99-graph.md)
- [Bank entry](../../../../.raw/V3R1T4S/bank/targets.json) (id `conway-99-graph`, commit `7dd4480`)

## Related Nodes

- [[V3R1T4S Graphs, games and automata]]
- [[V3R1T4S]]
