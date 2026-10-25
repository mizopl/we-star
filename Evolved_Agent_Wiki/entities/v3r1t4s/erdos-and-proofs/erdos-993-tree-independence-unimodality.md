---
id: v3r1t4s-erdos-993-tree-independence-unimodality
type: entity
tags: [v3r1t4s, v3r1t4s/erdos-and-proofs, kind/standard]
inbound_links: 1
confidence: 0.8
last_ingested_sources: [".raw/V3R1T4S/bank/targets.json@7dd4480"]
status: "open"
priority: ""
notes: ""
category: erdos-and-proofs
kind: standard
tractability: 1
compute: "laptop-hours"
disclosure: open
status_checked: "2026-10-03"
---
# Erdos #993: a tree (or forest) with non-unimodal independent-set sequence

# Overview

> Bank id `erdos-993-tree-independence-unimodality` · standard · tractability 1 · laptop-hours · disclosure **open**
> Bank says open as of 2026-10-03. Statuses go stale — re-check the primary source before any work.

## Statement

For every tree or forest T, is the sequence i_k(T) (number of independent sets of size k) unimodal? This is the Alavi-Malde-Schwenk-Erdos conjecture. It is false for general graphs. Log-concavity fails for trees from n = 26 (Kadrawi-Levit 2023). The n = 32 check covered all 109,972,410,221 trees (forum 2026-08-09) and the 3-branch-vertex lemma has a Lean formalisation (BrettRey2, 2026-08-21).

## Success criterion

An explicit tree or forest (edge list) whose exactly computed sequence (i_0, i_1, ...) has indices a < b < c with i_a > i_b < i_c. Plateaus do not count.

## Partial wins

- {"id": "p1", "statement": "An exhaustive, reproducible verification that every tree on 33 vertices has a unimodal independent-set sequence, with the enumerated tree count matching the known number of unlabeled trees on 33 vertices (OEIS A000055) and the code rerun by the verifier."}
- {"id": "p2", "statement": "A rigorous (refereed or Lean-checked) proof that any counterexample tree must have at least 4 vertices of degree >= 3, strengthening the known 3."}

## Verification

Confirm the graph is a forest (acyclic; for a tree, connected with n-1 edges). Compute the independence polynomial exactly with Python big integers by the rooted-tree DP I(T) = I(T-v) + x*I(T-N[v]), done twice: two different roots, or DP versus brute force for n <= 40. Then scan for a strict valley.

## Angles

- Mixture design: I(T) = I(T-v) + x*I(T-N[v]). Engineer the two summands to be log-concave with well-separated modes and comparable mass, e.g. attach many pendant stars K_{1,m} (factors (1+x)^m shift modes) on one side versus long paths on the other. Optimise the parameters analytically.
- Amplify the known 'multiple breaks of log-concavity' trees (arXiv 2511.00334, 2502.10654) by gluing or iterating them; search for a dip.
- Evolutionary / RL search over trees with 50-300 vertices. Fitness: min over b of i_b / min(i_{b-1}, i_{b+1}) approaching 1 from above. Use mutations preserving >= 3 branch vertices.
- Forest route: by Hoggar, a forest counterexample needs a non-LC component. Build disjoint unions of non-LC trees whose convolution creates a valley.

## Pitfalls

- Plateaus are allowed in unimodality.
- Float overflow; use exact integers.
- Confirm the object is a tree or forest (a cycle gives an invalid graph).
- Already exhaustively checked to n = 32.

## Sources

- https://www.erdosproblems.com/993
- https://www.erdosproblems.com/forum/thread/993
- https://zenodo.org/records/19100781
- https://arxiv.org/abs/2603.03025
- https://arxiv.org/abs/2604.18824
- Status source: https://www.erdosproblems.com/993

## Citations

- [Problem page](../../../../.raw/V3R1T4S/known-unknowns/erdos-and-proofs/erdos-993-tree-independence-unimodality.md)
- [Bank entry](../../../../.raw/V3R1T4S/bank/targets.json) (id `erdos-993-tree-independence-unimodality`, commit `7dd4480`)

## Related Nodes

- [[V3R1T4S Erdős problems and proofs]]
- [[V3R1T4S]]
