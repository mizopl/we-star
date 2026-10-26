---
type: hall_of_fame_note
note_kind: minor_retirement
retired_version: v9
successor_version: v9.1
date: 2026-10-17
snapshots: [ancestor_v9_proofer_md_snapshot.md, ancestor_v9_constitution_snapshot.md]
---
# Note of Fame — v9 "Proofer Build" (lived one cycle)

**Achieved:** gave the librarian a proof engine (autoresearch ratchet, verbalized sampling, predict→postdict→overwrite) without loosening the V3R1T4S kit. It picked the first quarry by VS (seed 730399641) and logged 3 bets before any work.

**Missing:** it had no memory of *how* it reasoned, only of what it bet. Lines of attack were scattered over NOTES.md files, which is the very circle-walking the human warned about. It also assumed one session would do everything, while the human asked for a swarm.

**Why retired:** the human asked for a cron-driven swarm and reasoning graphs "readable for yourself, so you don't walk in circles". v9.1 adds §5 Swarm and §6 Reasoning graph (`rgraph.py`, with `check` that refuses dead near-duplicates).

## Patch v9.1.1 (2026-10-17, same day)
The first live run dispatched both lens subagents in the background and ended its turn. Headless `claude -p` killed them after 10 minutes. Fix: subagents run in the foreground, the run waits for them, and `CLAUDE_CODE_PRINT_BG_WAIT_CEILING_MS=0` is set in run.sh. A separate long job (n15.py, its own PID and an alarm-based cap) survived, which is why the kit's "own PID + hard cap" rule matters.
