---
id: v3r1t4s-revenge-gods-number-bounds
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
# Tighten God's number bounds for the 4x4x4 cube (OBTM)

# Overview

> Bank id `revenge-gods-number-bounds` · harvest · tractability 2 · laptop-hours · disclosure **open**
> Bank says open as of 2026-10-03. Statuses go stale — re-check the primary source before any work.

## Statement

Improve either bound on God's number for the 4x4x4 Rubik's Revenge in the outer block turn metric (OBTM). Upper bound 54 OBTM (ananasclassic, 2026-07-21, 18+16+20); confirmed counting lower bound 32 (2015 thread). No exact value is known.

## Success criterion

Lower bound: a rigorous counting proof that the number of distinct OBTM move sequences of length <= d, under a canonical form that only identifies sequences proven equal as permutations, is smaller than the exact number of distinct 4x4x4 positions (identical centers indistinguishable, ~7.4e45, recomputed exactly), giving G > d with d STRICTLY ABOVE the best published OBTM lower bound found in the speedsolving thread (latest page) and a fresh search at verification time. Upper bound: a multi-phase solve where each phase's worst case is an exact coset-BFS diameter the verifier reproduces, with the sum STRICTLY BELOW the best published OBTM upper bound at verification time (54 as of 2026-10-03). Both counts must be exact integers recomputed by independent code.

## Partial wins

- {"id": "p1", "statement": "An independent exact reproduction of ananasclassic's phase 1+2 bound of 18 OBTM (and of the 16 and 20 phase diameters) by symmetry-reduced coset BFS with code independent of the original, matching per-depth counts if published."}
- {"id": "p2", "statement": "A rigorous upper or lower bound in another stated metric (SSTM, BTM, STM or QTM) strictly better than the best value for that same metric found in the speedsolving thread and a fresh search at verification time, verified exactly as in the success criterion."}

## Verification

Lower bound: an independent transfer-matrix count of canonical sequences in Python with big integers. Check every quotienting relation used (same-axis commutation, any length-k identities) by applying both sides to a permutation representation of the cube. Recompute the exact position count. Upper bound: rerun the phase BFS (symmetry-reduced) and compare per-depth counts.

## Angles

- Sharpen counting lower bounds: beyond the same-axis commutation used in 2015, enumerate short relations of the 4x4x4 move group by computer (BFS to depth 6-8 in the permutation group, looking for collisions). Feed them into a canonical-sequence automaton (as Rokicki did for 3x3x3) and recount.
- Exploit the indistinguishable centers: positions are counted modulo center permutations, but sequences that differ only by center-permuting tails collide too. Quantify this rigorously.
- Upper bound: try alternative phase decompositions (a different first-phase subgroup or merged phases 2 and 3) and compute exact coset diameters with symmetry and bitset BFS on 10 cores.
- State the metric clearly and do the work in one metric (OBTM) to avoid apples-to-oranges claims.

## Pitfalls

- Metric confusion (OBTM, SSTM, BTM, STM, QTM). Records are per metric.
- Counting sequences as positions without proving the canonicalization only merges truly equal sequences.
- Treating the supercube (oriented centers) count as if it were the normal-cube count.
- An upper bound from heuristic 'never saw worse than' solving is not a bound.
- The 35 OBTM lower bound comes from a secondary source and was not found in the thread. Treat 32 as the confirmed baseline, but check the latest posts and metric before claiming an improvement to 33 or more.

## Sources

- https://www.speedsolving.com/threads/what-is-gods-number-on-a-4x4-rubiks-cube.35965/page-18
- https://arxiv.org/pdf/2112.08602
- https://www.speedsolving.com/threads/what-is-gods-number-on-a-4x4-rubiks-cube.35965/page-17
- Status source: https://www.speedsolving.com/threads/what-is-gods-number-on-a-4x4-rubiks-cube.35965/page-18

## Citations

- [Problem page](../../../../.raw/V3R1T4S/known-unknowns/graphs-games-automata/revenge-gods-number-bounds.md)
- [Bank entry](../../../../.raw/V3R1T4S/bank/targets.json) (id `revenge-gods-number-bounds`, commit `7dd4480`)

## Related Nodes

- [[V3R1T4S Graphs, games and automata]]
- [[V3R1T4S]]
