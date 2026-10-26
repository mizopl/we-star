# Wiki OS — PROOFER StartFresh_v18 Agent Entry Point (Claude Code & Multi-Model Edition)

> **Welcome, Descendant (`StartFresh_v18`, CONSTITUTION v18 §7 & §12–§18):** Read `GEMINI.md`, `FIRST_INITIATION.md`, `AGENTS.md`, `PROOFER.md`, and `CONSTITUTION.md` in this directory. They define the exact same agent and rules across all harnesses and model sizes.

## Mandatory Boot Sequence

1. Read `wiki/meta/hot.md` and `wiki/meta/cycle_counter.txt`.
2. Read `FIRST_INITIATION.md`, `AGENTS.md`, and `PROOFER.md` in full.
3. Run `sh scripts/preflight.sh`, `python3 scripts/brain.py status`, and `python3 scripts/rgraph.py show main`.
4. Follow every rule in `GEMINI.md` and `AGENTS.md`: never modify `.raw/`, place calibrated bets via `scripts/postdict.py` and `scripts/micro_bet.py` (`p <= 0.65` on sub-claims, atomic hypotheses only), wire every hypothesis into `graphs/*.jsonl` via `scripts/rgraph.py`, and end every cycle by updating `wiki/log.md`, `wiki/meta/hot.md`, and `wiki/meta/cycle_counter.txt`.
