---
id: v3r1t4s-superpermutations-n7-n8
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
# Shorter superpermutations for n=7 (below 5905) or n=8 (below 46204)

# Overview

> Bank id `superpermutations-n7-n8` · harvest · tractability 2 · laptop-hours · disclosure **open**
> Bank says open as of 2026-10-03. Statuses go stale — re-check the primary source before any work.

## Statement

Find a string over {1..n} containing all n! permutations as contiguous substrings that is shorter than the best known. For n=7 the record is 5905 (Teodorescu, 17 Aug 2026) with lower bound 5884. For n=8 it is 46204 (Uku Raudvere, 26 Jul 2026). For n=9 it is 408965 and for n=10 it is 4037046 (Echols, Jul 2026, GPT-5.6-Sol), and Raudvere also posted n=11..13.

## Success criterion

Success means a string over the alphabet {1..n} (n in 7..10) in which all n! permutations occur as length-n substrings, verified exhaustively, whose length is STRICTLY SMALLER (direction: min) than the best length at verification time on https://en.wikipedia.org/wiki/Superpermutation and the superpermutators group (context on 2026-10-03: 5905 for n=7, 46204 for n=8, 408965 for n=9, 4037046 for n=10). For n=7 the length must also be >= 5884; anything shorter means a bug.

## Partial wins

- {"id": "p1", "statement": "A superpermutation for n in 11..13, verified exhaustively, strictly shorter than Raudvere's live record for that n (context: 43,948,807 / 522,910,088 / 6,749,568,009)."}
- {"id": "p2", "statement": "A lower bound for n=7 strictly above 5884, delivered as a re-runnable computer-assisted proof (exact ILP or exhaustive search with certificate) that the skeptic re-executes, after confirming no stronger lower bound is published."}

## Verification

Slide a window of length n and add each window that is a permutation (n distinct symbols) to a set. Assert the set size is n!, the alphabet is exactly {1..n}, and the length is below the record. For n=10 the string is ~4M characters, which is trivial to check.

## Angles

- For n=8, apply the Egan/Houston kernel method with the newer 2026 tricks Raudvere used. Search palindromic kernels of higher weight and use the 2-cycle graph cover with a cheaper ATSP solve (LKH via pip 'lkh' or elkai) on the 7!-node 'cycle graph'.
- Treat it as ATSP on the permutation graph with edge weights 1..n and use an exact or near-exact solver on reduced quotient graphs (by symmetry). For n=7, solve on the 5040-node graph with elkai/LKH and many restarts, exploiting symmetry to restrict the search.
- Lift a better n=7 solution through the Williams/Egan-style constructions to n=8 and beyond, which gives cascading improvements.
- Look for a structural insight in Teodorescu's 5905: identify which 'weight-3 or weight-4 edges' it saves and generalize.

## Pitfalls

- Counting a window with repeated symbols as a permutation.
- Alphabet/length off-by-one.
- The n=7 record changed in Aug 2026 and n=8 in Jul 2026. Always re-check the superpermutators group.
- Raudvere's n=11-13 lengths (43,948,807; 522,910,088; 6,749,568,009) are also live baselines if one lifts constructions upward.

## Sources

- https://groups.google.com/g/superpermutators
- https://github.com/superpermutators/superperm
- https://www.gregegan.net/SCIENCE/Superpermutations/Superpermutations.html
- Status source: https://groups.google.com/g/superpermutators

## Citations

- [Problem page](../../../../.raw/V3R1T4S/known-unknowns/record-tables/superpermutations-n7-n8.md)
- [Bank entry](../../../../.raw/V3R1T4S/bank/targets.json) (id `superpermutations-n7-n8`, commit `7dd4480`)

## Related Nodes

- [[V3R1T4S Record tables]]
- [[V3R1T4S]]
