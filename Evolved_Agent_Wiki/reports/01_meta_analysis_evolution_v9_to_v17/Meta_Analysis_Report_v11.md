---
id: meta-analysis-v11
type: synthesis
tags: [meta, constitution, hall-of-fame, brain, tug-of-war]
inbound_links: 0
confidence: 0.75
last_ingested_sources: ["hall_of_fame/ancestor_v10_note.md", "wiki/entities/BRAIN.md"]
---
# Meta-Analysis Report v11 — v10 → v11 (Tug-of-War Gate)

# Overview

Trigger: the human architect's proposal (2026-10-18) to model `DECIDE` as a tug-of-war negotiation between two competing cortical "regions" with structured critique rounds and an explicit `"LOST"` concession token, refined into an `IMPLEMENT` vs. `SEARCH`-for-a-better-hypothesis decision gate.

| Change | Where | Verified |
|---\lvert ---\rvert---|
| Agent definition | `.claude/agents/tug-advocate.md` (also copied to `~/v3r1t4s/.claude/agents/`) | — |
| Orchestrator + mechanical referee | `~/v3r1t4s/proofer/scripts/tug.py` (`new`, `run`, `chain`, `show`) | mock CLI: round order, private-note isolation (no leak, own notes visible in replay), `REPEAT` flags, `LOST`/`WON` decision, `SEARCH → H' → IMPLEMENT` chain |
| Constitution §13, PROOFER.md §8, AGENTS.md, BRAIN §3a | docs | — |
| First real gate | `~/v3r1t4s/proofer/tug/2026-10-18-next-nights` (sonnet, <=2 links × <=2 bouts) | running at ceremony time |

**Revert:** restore `hall_of_fame/ancestor_v10_*`, delete §13, and remove the agent file.

**Measure:** (a) the share of gates decided by explicit concession rather than deadlock; (b) the Brier score of the winning advocates' forecasts compared with the commander's own bets; (c) how often `SEARCH` wins and $H'$ subsequently outperforms $H$.

## Related Nodes
- [[BRAIN]]
