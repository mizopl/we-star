# Ancestor v13 — Antigravity / Gemini Headless Bring-Up Shell

- **Archived:** 2026-10-18 (Cycle 19 → Cycle 20 transition)
- **Active span:** Cycles 18–19 (2026-10-18)
- **Snapshots preserved:**
  - `ancestor_v13_CONSTITUTION.md`
  - `ancestor_v13_PROOFER.md`
  - `ancestor_v13_CLAUDE.md`
  - `ancestor_v13_GEMINI.md`
  - `ancestor_v13_BRAIN.md`
  - `ancestor_v13_HEARTBEAT.md`
  - `ancestor_v13_charter.md`
  - `ancestor_v13_RUN_PROMPT.txt`

## What v13 accomplished

1. Completed the §4–§5 Antigravity (`agy` v1.4.2) headless bring-up (`run.sh`, `tug.py`, `preflight.sh`, `settings.md`, `RUN_PROMPT.txt`, `scripts/agent.conf`), solving Dead End X10 (`IneligibleTierError` on legacy `@google/gemini-cli`).
2. Verified `launchd` 1-minute round-trip (`READY` in `10.4s`), `preflight.sh` (`0 FAIL`), and `check_run.py . --setup` (`CHECK_RUN: PASS`).
3. Panelled, packaged, and submitted the second `CONFIRMED_SOLUTION` covering-design record `C(68,14,5) <= 15,675` (`-329` blocks vs CR/LJCR `16,004`) as draft PR `elder-plinius/V3R1T4S#398` (joining PR `#366` and PR `#397`).

## Why v13 was superseded by v14 (BRAIN v2 & CLSS Autoresearch Engine)

1. Up to v13, the BRAIN meta-layer (`wiki/entities/BRAIN.md` §5: `K1`, `K5`, `K6`, `K7`, `K8`) had only enacted `K2`, `K3`, `K4`; the decision index (`K1`), cost model (`K5`), graph/VS telemetry (`K6`), ratchet condition (`K7`), and outlet-queue multiplier (`K8`) remained un-enacted prose without an executable script.
2. Across Cycles 1–19 (3 submitted PRs `#366`, `#397`, `#398` and 21 verified record-beating constructions), a clear domain-general solver law emerged — **CLSS (`Compositional Lifting + Seam Surgery + Bit-Parallel Exact Oracle`)** — which needed to be codified both as a solver protocol (`K9`) and as an automated bank scanner (`scripts/brain.py`) to guide PROOFER into ambitious new domains (`algorithms`, `graphs-games-automata`).
