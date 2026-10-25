---
id: v3r1t4s-degree-diameter-table
type: entity
tags: [v3r1t4s, v3r1t4s/graphs-games-automata, kind/harvest]
inbound_links: 1
confidence: 0.8
last_ingested_sources: [".raw/V3R1T4S/bank/targets.json@7dd4480"]
status: "CONFIRMED_SOLUTION"
priority: ""
notes: ""
category: graphs-games-automata
kind: harvest
tractability: 3.5
compute: "laptop-hours"
disclosure: open
status_checked: "2026-10-03"
---
# New largest known (Delta,D) graph in the degree-diameter table

# Overview

> Bank id `degree-diameter-table` · harvest · tractability 3.5 · laptop-hours · disclosure **open**
> Bank says open as of 2026-10-03. Statuses go stale — re-check the primary source before any work.

## Statement

For maximum degree Δ and diameter D, find a graph with more vertices than the current entry in the Comellas degree-diameter table. The table covers degree up to 20 and diameter up to 10.

## Success criterion

(1) Explicit adjacency list of a simple undirected graph G on N vertices. (2) Maximum degree <= Delta. (3) G connected with diameter <= D, checked by all-pairs BFS, or by one BFS plus a machine-checked vertex-transitivity proof (explicit Cayley group and generators regenerating exactly the submitted edge set). (4) N STRICTLY GREATER than the (Delta,D) entry of the live Comellas general-graph table at https://web.mat.upc.edu/francesc.comellas/delta-d/table_degree_diameter.html, re-fetched immediately before claiming (the table changes daily). (5) N <= Moore bound; boldface (proven-optimal) entries cannot be beaten, so beating one signals a bug.

## Partial wins

- {"id": "p1", "statement": "A graph satisfying (1)-(3) with N strictly greater than the (Delta,D) entry in a table snapshot whose fetch time and SHA-256 were recorded BEFORE the search started, but which was overtaken by another group's update logged on the live table after that snapshot (independent collision); the skeptic checks the graph, the snapshot hash and the update-log date."}
- {"id": "p2", "statement": "A graph strictly beating the live entry of a separately maintained special-class degree-diameter table (bipartite, Cayley or circulant), verified with the same exact degree/diameter checker plus the class property (bipartition, or Cayley group and generators reproducing the edge set), compared against that table's live page."}

## Verification

Load the graph with scipy.sparse. Assert it is symmetric with no loops and no multi-edges, and check the degree array. Run BFS from every vertex: multi-source frontier bitsets in numpy work up to about 2e5 vertices. For Cayley graphs, regenerate the edge set from the stated group and generators, check it equals the submitted list, and then run one BFS. Compare N with the live HTML table. Also confirm N is at most the Moore bound.

## Angles

- Voltage-graph lifts: choose a small base graph (Petersen, Hoffman-Singleton, or the record graphs for (Δ, D-1)) and anneal voltage assignments over Z_n, Z_n x Z_m, or metacyclic groups, scoring by the number of vertex pairs at distance greater than D in the lift. Base graph plus group gives a fast BFS on the quotient.
- Cayley graphs of semidirect products Z_m ⋊_r Z_n with generator sets chosen by SA. Many of the 2026 entries are Cayley graphs, marked with an asterisk in the table.
- Polarity-quotient and Kronecker-product constructions (arXiv 2608.27253): apply them systematically to every table entry to propagate the recent improvements to neighbouring (Δ,D).
- Gomez-style compound graphs: replace vertices of a large diameter-(D-2) graph with copies of a small graph and rewire. Use the fresh 2026 records as seeds.
- Target the entries updated least recently. Large-D, small-Δ entries got fewer 2026 updates than (Δ,3), (Δ,4), (Δ,5).
- Seed voltage-lift and Kronecker/polarity searches with the partial-flag graphs H_{k,q} of arXiv 2608.03965, after checking whether they already appear in the table.

## Pitfalls

- The table is updated almost daily. A claim must beat the value shown at verification time, not the value at search start.
- Diameter computed on the quotient or base graph instead of the actual lift.
- Multi-edges or loops in voltage lifts silently reduce the true degree count.
- Degree-diameter problems for special classes (bipartite, Cayley-only, circulant) have separate tables. Only the general-graph table counts here.
- Boldface entries such as (3,2), (3,3), (3,4) and (4,2) are proven optimal. Beating one means there is a bug.
- More than 15 independent groups updated the table in August to October 2026. Timestamp claims and re-fetch the table just before claiming.
- arXiv 2608.03965 (partial-flag graphs H_{k,q}, asymptotically attaining the Moore bound) is a new seed family. Its graphs may already be in the table.

## Sources

- https://web.mat.upc.edu/francesc.comellas/delta-d/table_degree_diameter.html
- https://en.wikipedia.org/wiki/Table_of_the_largest_known_graphs_of_a_given_diameter_and_maximal_degree
- https://arxiv.org/pdf/2608.27253
- https://arxiv.org/abs/2608.03965
- Status source: https://web.mat.upc.edu/francesc.comellas/delta-d/table_degree_diameter.html

## Citations

- [Problem page](../../../../.raw/V3R1T4S/known-unknowns/graphs-games-automata/degree-diameter-table.md)
- [Bank entry](../../../../.raw/V3R1T4S/bank/targets.json) (id `degree-diameter-table`, commit `7dd4480`)

## Related Nodes

- [[V3R1T4S Graphs, games and automata]]
- [[V3R1T4S]]
