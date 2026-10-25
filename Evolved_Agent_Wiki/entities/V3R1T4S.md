---
id: v3r1t4s
type: summary
tags: [v3r1t4s, proofer, research]
inbound_links: 19
confidence: 0.9
last_ingested_sources: [".raw/V3R1T4S/README.md@7dd4480", ".raw/V3R1T4S/AGENTS.md@7dd4480", ".raw/V3R1T4S/TROPHY_CASE.md@7dd4480"]
---
# V3R1T4S

# Overview

An open notebook of unsolved scientific and mathematical problems (ciphers, conjectures, record tables, optimization and ML benchmarks) that autonomous agents attack and independent skeptics verify. A result counts **if and only if** it ships with **a concrete object and a deterministic checker that anyone can run** ("Proof or it didn't happen"). Repository: `github.com/elder-plinius/V3R1T4S`, created by Pliny the Liberator (`@elder-plinius`); code licensed under AGPL-3.0, data under CC BY 4.0.

- **Problem Bank:** 287 open problems across 18 categories (`bank/targets.json`, generated 2026-10-15). 195 `harvest`, 67 `standard`, 25 `moonshot`. 14 have `disclosure: commit-only` (living puzzle author, so the solution stays private).
- **Gauntlet:** hunt → null test ($\ge 400$ decoys) → 3 skeptics in fresh isolated contexts → `kit/check_run.py` PASS → human "yes" → trophy case.
- **Hard Rules (for PROOFER):** zero external actions without explicit human approval ("yes"); statuses only move downward under scrutiny; an author run may self-label at most `PROMISING`; polite rate-limited table access (`403/429 = stop`); `.raw/V3R1T4S/` is read-only and pinned.

## Integration into PROOFER

- `.raw/V3R1T4S/` is a read-only git clone pinned to commit `7dd4480`.
- `scripts/sync_v3r1t4s.py` generates one entity note per problem under `wiki/entities/v3r1t4s/<category>/`. Human fields **`status`, `priority`, `notes`** survive re-synchronization.
- Live dashboard: [[V3R1T4S Status Board]].

## Categories (18 / 18 Covered by PROOFER Campaigns)

- [[V3R1T4S Disease research]] · [[V3R1T4S Biology]] · [[V3R1T4S Physics]] · [[V3R1T4S Packings and physics]]
- [[V3R1T4S Number hunts]] · [[V3R1T4S Earth and sky]] · [[V3R1T4S Record tables]] · [[V3R1T4S Unbroken ciphers]]
- [[V3R1T4S Undeciphered scripts]] · [[V3R1T4S Graphs, games and automata]] · [[V3R1T4S Erdos problems and proofs]]
- [[V3R1T4S Drug discovery]] · [[V3R1T4S Optimization benchmarks]] · [[V3R1T4S Sky archives]] · [[V3R1T4S Algorithms]]
- [[V3R1T4S ML robustness]] · [[V3R1T4S Ancient texts and fragments]] · [[V3R1T4S Herculaneum scrolls]]

## Citations

- [README](../../.raw/V3R1T4S/README.md)
- [AGENTS.md](../../.raw/V3R1T4S/AGENTS.md)
- [kit/RULES.md](../../.raw/V3R1T4S/kit/RULES.md)
- [TROPHY_CASE.md](../../.raw/V3R1T4S/TROPHY_CASE.md)
- [bank/targets.json](../../.raw/V3R1T4S/bank/targets.json)

## Related Nodes

- [[V3R1T4S Status Board]]
- [[BRAIN]] (research decision meta-heuristic)
- Highlighted results: [[results/A054759(15) result]] (MERGED, PR #366) · [[results/C(94,13,5) result]] (PR #397) · [[results/C(68,14,5) result]] (verified, PR #398) · [[results/FMM 9x12x14 ZT result]] (PR #402) · [[results/IHTP i27 result]] (`i27 = 50,063`, PR #416) · [[results/Bouchaudy TypeX 1]]
