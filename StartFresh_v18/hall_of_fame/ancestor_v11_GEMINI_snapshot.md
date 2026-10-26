# Wiki OS — Librarian Agent Configuration (Gemini CLI entry point)

Gemini CLI reads this file the same way Claude Code reads `CLAUDE.md` in this
same directory. **The two files describe the same agent and must stay in sync**
— this file is a thin pointer plus a safety-net summary, not a second copy of
the rules, so they cannot drift apart from editing one and forgetting the other.

## What to do right now

1. Read `CLAUDE.md` in this same directory in full — it is the complete,
   tool-agnostic operating configuration (persona, core rules, the 8-step
   autonomous maintenance workflow). Nothing in it is Claude-specific.
2. Read `CONSTITUTION.md` and `SCHEMA.md` in full — the detailed rules and
   data formats referenced throughout `CLAUDE.md`.
3. Then proceed exactly as `CLAUDE.md` instructs, substituting nothing —
   every rule (never mutate `.raw/`, read `wiki/meta/hot.md` first, the
   8-step workflow, the log/hot-cache mandate, the query-cache shortcut for
   direct business questions) applies identically regardless of which CLI
   is running you.

## Safety-net summary (in case the above files are truncated or not loaded)

- Never modify, delete, or overwrite anything under `.raw/` — it is immutable.
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
cycles. It defaults to `claude --print`. To use Gemini CLI for those background
triggers instead of just interactive sessions, edit `scripts/agent.conf`:

```
AGENT_CMD="gemini -p"
```

Verify the exact non-interactive flag for your installed Gemini CLI version
first (`gemini --help`) — it has changed across releases.
