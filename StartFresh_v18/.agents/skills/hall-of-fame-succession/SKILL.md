---
name: hall-of-fame-succession
description: >-
  Andrej Karpathy LLM Wiki maintenance and the Hall of Fame Generational
  Succession Protocol (CONSTITUTION.md §1–§10). Use when compiling raw sources
  from .raw/ into wiki/, auditing wikilinks, or retiring an aging Constitution
  generation into hall_of_fame/ to restore system plasticity.
---

# Karpathy `LLM Wiki` Compiler & `Hall of Fame` Succession Protocol (`§1–§10`)

## 1. Karpathy `LLM Wiki` Compilation Rules ("Stop Retrieving, Start Compiling")
- **Immutable `.raw/`:** Never modify, overwrite, or delete files in `.raw/`.
- **Compiled `wiki/`:** Synthesize raw sources into structured Markdown pages (`wiki/entities/*.md`, `wiki/concepts/*.md`, `wiki/reports/*.md`) conforming to `SCHEMA.md`.
- **Graph Hygiene:** Maintain bidirectional `[[wikilinks]]`, update `wiki/meta/index.md`, run `python3 scripts/audit_links.py` and `python3 scripts/maintenance.py` to ensure zero orphan nodes and zero dead links.
- **Atomic Cycle Commit:** At the end of every cycle, append one summary line to `wiki/log.md`, overwrite `wiki/meta/hot.md`, and increment `wiki/meta/cycle_counter.txt` by 1.

## 2. The `Hall of Fame` Generational Succession Protocol (`CONSTITUTION.md` §7)
When an agentic system accumulates patches across many cycles, it suffers from *primacy bias* / *loss of plasticity* and status-quo resistance to modifying its own rules. To evolve cleanly without erasing history:
1. **Snapshot the Retiring Generation:** Copy the retiring `CONSTITUTION.md`, `PROOFER.md`, and `AGENTS.md` to `hall_of_fame/ancestor_vN_CONSTITUTION.md` (and `ancestor_vN_PROOFER.md`).
2. **Write the Ancestor Note (`hall_of_fame/ancestor_vN_note.md`):** Honor the retiring generation's verified achievements, document the exact failure mode or structural discovery that motivated the upgrade, and state the new universal rule distilled from its life.
3. **Write the Meta-Analysis Report (`wiki/reports/Meta_Analysis_Report_vN+1.md`):** Document the transition in the wiki and bump the version number in `CONSTITUTION.md` (or spawn a clean `StartFresh` descendant seed).
