---
type: hall_of_fame_note
note_kind: retirement
retired_version: v9.1 (incl. patch v9.1.1)
successor_version: v10
date: 2026-10-17
snapshots: [ancestor_v9.1_CONSTITUTION_snapshot.md, ancestor_v9.1_CLAUDE_snapshot.md, ancestor_v9.1_PROOFER_snapshot.md, ancestor_v9.1_RUN_PROMPT_snapshot.txt, ancestor_v9.1_run_sh_snapshot.sh]
---
# Note of Fame — v9.1 "Swarm & Reasoning Graph" (lived ~9 hours)

**Achieved.** It produced this instance's first confirmed result: **A054759(15) = 4310182149988584261406143524214457416387448**, CONFIRMED_PARTIAL with a 3/3 panel and CHECK_RUN PASS. It also pushed A089980 antidiagonal 79 from nothing to 37 of 40 widths in flight. The reasoning graph grew to 48 nodes, 6 of them dead with reasons, and runs consulted it: no dead line was knowingly repeated. Calibration went from no data to a Brier of 0.226 over 12 bets.

**What failed.**
- Half of its dead ends were infrastructure (background subagents, cron without a keychain, resumes before the reset, a too-small job cap). Each was fixed by hand after it had already cost a run.
- Long computations lived inside LLM sessions and died with them, or the sessions burned their budget waiting.
- Runs scored their own bets, and 2 of 12 were scored generously.

**Why retired.** The human asked for a research-decision meta-heuristic. `wiki/entities/BRAIN.md` derived it from v9.1's own record, and v10 enacts three of its proposals: two clocks (job queue), independent scoring, and preflight from dead ends.

**Lesson passed down.** The kit never failed, and the scaffolding around it did. Guard the scaffolding as rigorously as the claims.
