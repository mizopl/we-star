# Wiki OS — PROOFER Agent Configuration (Gemini / Antigravity entry point, shell v14)

> **Status (2026-10-18, CONSTITUTION v14 §12–§15):** Handed over from Claude Code to Antigravity / Gemini (`agy` v1.4.2) and upgraded with the **BRAIN v2 & CLSS Autoresearch Engine** (`scripts/brain.py`). All headless scripts (`run.sh`, `settings.md`, `preflight.sh`, `tug.py`, `brain.py`, `RUN_PROMPT.txt`, `scripts/agent.conf`) are wired for `~/.local/bin/agy -p`. Read `HANDOFF_ANTIGRAVITY.md` for historical context and dead ends X1–X10.

Antigravity (`agy`) reads this file the same way Claude Code reads `CLAUDE.md` in this
same directory. **The two files describe the same agent and must stay in sync**
— this file is a thin pointer plus a safety-net summary, not a second copy of
the rules, so they cannot drift apart from editing one and forgetting the other.

## What to do right now

0. Read `HANDOFF_ANTIGRAVITY.md` (current state, priorities, harness mapping, dead ends).
1. Read `CLAUDE.md` in this same directory in full: the complete operating configuration (persona, core rules, the 8-step
   maintenance workflow, Proof Mode). Its rules are tool-agnostic.
2. Read `CONSTITUTION.md` (v14) and `SCHEMA.md` in full — the detailed rules and
   data formats referenced throughout `CLAUDE.md`.
3. Then proceed exactly as `CLAUDE.md` instructs, substituting nothing —
   every rule (never mutate `.raw/`, read `wiki/meta/hot.md` first, the
   8-step workflow, the log/hot-cache mandate, the query-cache shortcut for
   direct business questions) applies identically regardless of which CLI
   is running you.

## Safety-net summary (in case the above files are truncated or not loaded)

- Never modify, delete, or overwrite anything under `.raw/` — it is immutable.
- Always use `python3` (`/usr/bin/python3` is broken on this Mac, X9).
- Before any action, read `wiki/meta/hot.md` (session memory).
- End every maintenance cycle by appending one line to `wiki/log.md`
  (format: `| YYYY-MM-DD HH:MM | Cycle N | <summary> |`), then overwrite
  `wiki/meta/hot.md`, then — only after that write succeeds — increment
  `wiki/meta/cycle_counter.txt` by 1.
- If the human's message is a direct factual/business question rather than
  an instruction to run maintenance, skip the full workflow: check
  `wiki/meta/query_cache.md` first, otherwise read `wiki/meta/index.md` and
  the 1–3 most relevant entity files, answer directly, then cache the answer.

## Automation scripts

`scripts/agent.conf` controls which CLI `run_maintenance.sh` / `watch_raw.sh` /
`autonomous_loop.sh` / `install_automation.sh` invoke for scheduled/background
cycles. Under v13 it is set to Antigravity CLI (`~/.local/bin/agy -p`):

```
AGENT_CMD="~/.local/bin/agy -p"
```
