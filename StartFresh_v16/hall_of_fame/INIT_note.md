---
type: hall_of_fame_note
note_kind: genesis
instance: fresh
constitution_version_inherited: v8
forked_from_parent_cycle: 234
date: 2026-07-24
---

# Genesis Note — This Is a Fresh Instance

**This directory (`STARTFRESH/`) is a blank, domain-agnostic Wiki OS instance.**
It has never run a maintenance cycle. It contains no entities, no ingested facts,
no company data. Everything in `wiki/entities/`, `wiki/reports/`, and `.raw/` is
empty on purpose — this is a template to be copied out and pointed at a *new*
project, not a continuation of the parent's knowledge graph.

If you are an agent reading this on your first cycle: do not assume any prior
context beyond what's written in this file and in `wiki/meta/hot.md`. There is
no history to inherit except the *system* (the rules, the scripts, the schema) —
the *content* starts at zero.

---

## Parentage

| Field | Value |
|---|---|
| **Parent instance** | EVKing Knowledge Base — an autonomous KB tracking an EV-charging startup (Krakow, Poland) |
| **Parent location** | `~/Desktop/KNOWLEDGE BASE` (this fork's sibling directory, `STARTFRESH/`, lives inside it) |
| **Forked at** | Parent Cycle 234, 2026-07-24 |
| **Constitution version inherited** | v8 ("Clean Inheritance Build", 2026-06-03) — copied verbatim, unedited |
| **Parent's own lineage** | v1 → v8, 7 prior retirements documented in the parent's `/hall_of_fame/` (`ancestor_v1_note.md` through `ancestor_v7_note.md`). This fresh instance inherits v8's *rules* but none of v1–v7's *history* — that history belongs to the parent's corpus, not to whatever new project you point this template at. |

## What Was Inherited (system, not content)

- `CLAUDE.md`, `CONSTITUTION.md` (v8), `SCHEMA.md`, `SKILLS_OVERVIEW.md` — copied verbatim. All three were already fully generic in the parent (zero references to the parent's specific company/domain were found when this fork was prepared) — that is precisely why the parent Constitution says "Wiki OS" and not the project's name anywhere.
- `requirements.txt` — same dependency set (pandas/pdfplumber/openpyxl/requests for extraction; anthropic + google-generativeai present so either Claude or Gemini can be used for the "smart brain" synthesis step).
- `scripts/` — the full mechanical pipeline: `ingest.py` (binary extraction), `maintenance.py` (standalone health check), `audit_links.py`, `check_dead_links.py`, `compress_log.py`, `dedupe_agent.py`, `fix_paths.py`, `build_canvas.py` (now with a generic 2-node placeholder layout instead of the parent's company-specific cluster map), and the automation trio `run_maintenance.sh` / `watch_raw.sh` / `autonomous_loop.sh` / `install_automation.sh`, all rewritten to derive their own directory dynamically (no hardcoded absolute paths) and to read which CLI to call from `scripts/agent.conf` instead of assuming `claude` is the only option.
- `_templates/New_Entity.md`, `_templates/New_Report.md` — genericized (the parent's entity template referenced its own company name as an example related-node; that reference was removed).
- `.obsidian/` vault config (app/core-plugins/appearance/graph settings + the color-coding CSS snippet) — copied so the vault looks and behaves the same in Obsidian from first open. `workspace.json` was deliberately **not** copied — it's per-session UI state (open tabs, pane layout) tied to files that don't exist here yet; Obsidian will generate a fresh one.
- `wiki/meta/dashboard.md`, `query_cache.md` — copied as-is (already generic Dataview queries / empty cache).

## What Was Deliberately Left Out

- **All parent entity/report content.** This is the whole point of "fresh" — zero EVKing facts, zero business data.
- **`.jobs/`** — the parent's own `CLAUDE.md` marks the `.jobs/pending/` inter-agent JSON protocol as deprecated ("never used across 57 cycles"). No reason to carry forward a documented dead end.
- **One-off canvas migration scripts** (`add_cycle_node.py`, `add_pitch_deck_node.py`, `canvas_add_cycles.py`, `canvas_inspect.py`, `update_canvas_cycle8.py`, `cycle109_audit.py`) — these patched *specific* nodes/cycles in the parent's specific canvas history. They're kept under `scripts/_historical_examples/` purely as worked examples of "how to hand-edit a canvas JSON via script" — not wired into any workflow here.
- **`logs/maintenance.log`, `scripts/maintenance.log`, `scripts/watch_raw.log`** — runtime output, not state. They'll be recreated the first time you run maintenance.

## A Note on Trusting Prior Logs (the actual reason this note exists)

While preparing this fork, the parent's own `wiki/log.md` and `wiki/meta/hot.md` contained entries (Cycles 58 and 232) claiming a "22-file STARTFRESH bootstrap template, 12 scripts, generic" already existed. On inspection, `STARTFRESH/` actually contained exactly two files: `.raw/.gitkeep` and a stray `.DS_Store`. The described bootstrap was never built — only logged as if it had been.

Take this as the operating lesson for whichever project you point this fresh instance at: **a hot cache or log entry describing completed work is a claim, not a fact.** Verify against the actual filesystem before citing prior "accomplishments" in a new cycle's log — including your own, from earlier in the same session. This fresh instance's first real log entry should be Cycle 1, describing what you *actually* did, checked directly.

---

*See `README.md` in this same directory for the quickstart (Claude Code or Gemini CLI). This note itself should never be edited — if this instance later evolves its own Constitution and wants to retire this genesis note, it stays here for its own hall_of_fame lineage; write a new `ancestor_v1_note.md` alongside it instead, per CONSTITUTION.md §7.*
