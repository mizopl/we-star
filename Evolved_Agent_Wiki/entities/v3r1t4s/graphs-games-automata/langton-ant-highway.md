---
id: v3r1t4s-langton-ant-highway
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
# Langton's ant highway conjecture

# Overview

> Bank id `langton-ant-highway` · moonshot · tractability 1 · laptop-hours · disclosure **open**
> Bank says open as of 2026-10-03. Statuses go stale — re-check the primary source before any work.

## Statement

Conjecture: from every finite initial configuration of black cells, Langton's ant eventually builds the period-104 diagonal highway. It is proven that the ant's trajectory is always unbounded (Cohen-Kong), but not that it always reaches the highway.

## Success criterion

CONFIRMED only for (a) a finite initial configuration of black cells together with a machine-checkable proof that the ant never produces the highway (e.g. a proven different eventual behaviour verified by exact simulation to a provably repeating state), or (b) a formal (Lean/Isabelle) proof of the conjecture. Long transients without the highway are never counterexamples.

## Partial wins

- {"id": "p1", "statement": "Exhaustive verification of all initial configurations in a 6x6 (or larger) box under a stated symmetry reduction, each with a highway-capture certificate (window at t equals window at t+104 shifted by (+-2,+-2), ant beyond all black cells, and no initial black cell anywhere in the future sweep of the highway) re-checked by an independent simulator on a random 1% sample plus all hard cases."}
- {"id": "p2", "statement": "A rigorous highway-capture lemma (formal proof, or proof reduced to an exhaustively checked finite case analysis re-run independently) stating exactly when a highway, once formed with a given local pattern and no black cells in its future sweep, persists forever."}

## Verification

Exact integer simulation by an independent implementation. For highway detection, verify that the ant's local window at time t equals the window at time t+104 shifted by (+-2,+-2), and that the ant is beyond all initial black cells in the drift direction, so the future is provably periodic. For exhaustive claims, re-run a random 1% sample plus all hard cases with the independent simulator.

## Angles

- Prove a rigorous 'highway capture lemma': once the ant is beyond the convex hull of the debris in the highway direction with a specific local pattern, it is locked in forever. This turns finite simulation into proof for bounded boxes.
- Exhaustive 6x6 (2^36, about 6.9e10, reduced by 8-fold symmetry) with bit-parallel simulation on 10 cores using the capture lemma.
- Study the generalized ants of arXiv 2505.05426 and look for an obstruction mechanism that could appear in LR (Langton) rules from engineered initial patterns, for example highway-colliding 'eaters'.

## Pitfalls

- Simulation without a proven capture lemma is not a proof that the highway persists.
- Claims of counterexamples based only on long transients (the ant's chaotic phase can last 10^4 or more steps).
- The highway-capture certificate must also show that no initial black cell lies anywhere in the future sweep of the highway, not only ahead of the ant at the moment of detection.

## Sources

- https://arxiv.org/pdf/2505.05426
- https://en.wikipedia.org/wiki/Langton%27s_ant
- Status source: https://arxiv.org/pdf/2505.05426

## Citations

- [Problem page](../../../../.raw/V3R1T4S/known-unknowns/graphs-games-automata/langton-ant-highway.md)
- [Bank entry](../../../../.raw/V3R1T4S/bank/targets.json) (id `langton-ant-highway`, commit `7dd4480`)

## Related Nodes

- [[V3R1T4S Graphs, games and automata]]
- [[V3R1T4S]]
