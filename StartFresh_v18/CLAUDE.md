# Wiki OS — PROOFER StartFresh_v18 Agent Entry Point (Claude Code & Multi-Model Edition)

> **Welcome, Descendant (`StartFresh_v18`, CONSTITUTION v18 §7 & §12–§18):** Read `GEMINI.md`, `FIRST_INITIATION.md`, `AGENTS.md`, `PROOFER.md`, and `CONSTITUTION.md` in this directory. They define the exact same agent and rules across all harnesses (`Claude Code` and `Antigravity`) and model sizes (`Haiku`, `Sonnet`, `Opus`, `Gemini Flash`, `Gemini Pro`).

## Mandatory Boot Sequence

1. Read `wiki/meta/hot.md`, `wiki/meta/AUDITOR_INBOX.md` (coaching & steering notes from `MONITOR` / `AUDITOR`), and `wiki/meta/cycle_counter.txt`.
2. Read `FIRST_INITIATION.md`, `AGENTS.md`, and `PROOFER.md` in full.
3. Run `sh scripts/preflight.sh`, `python3 scripts/brain.py status`, and `python3 scripts/rgraph.py show main`.
4. Follow every rule in `GEMINI.md` and `AGENTS.md`: never modify `.raw/`, check `wiki/meta/AUDITOR_INBOX.md` at the start of every cycle, place calibrated bets via `scripts/postdict.py` and `scripts/micro_bet.py` (`p <= 0.65` on sub-claims, atomic hypotheses only), wire every hypothesis into `graphs/*.jsonl` via `scripts/rgraph.py`, and end every cycle by updating `wiki/log.md`, `wiki/meta/hot.md`, and `wiki/meta/cycle_counter.txt`.

---

## 🤖 How Subagents, `tug.py`, `MONITOR`, and `AUDITOR` Work in Claude Code

1. **In-Session Subagents (`.claude/agents/` via Claude Code's `Task` / Agent tool):**
   Your workspace includes 4 specialized subagents in `.claude/agents/` (and `.agents/agents/`):
   - **`surrogate-architect`** — invoke **before** writing heavy search code on a flat $0/1$ plateau (`Law M1`) to design a non-hackable violation energy $E_{\text{viol}}(x) \ge 0$.
   - **`tug-advocate`** — invoked automatically by `python3 scripts/tug.py run <name> --model haiku` (or `sonnet`/`opus`) when you face a major `IMPLEMENT` vs `SEARCH` strategic fork (`CONSTITUTION §13`). `tug.py` automatically detects Claude Code when `--model haiku|sonnet|opus` or `TUG_HARNESS=claude` is used!
   - **`skeptic-panel`** — spawn **3 independent instances** in fresh context at **Stage 5 (Verify & Panel)** (`Reproducibility`, `Novelty`, `Criterion/Leakage`) once you have a candidate proof/witness/solution. Do **not** spawn them at Step 0 before you have a candidate result to audit!
   - **`outreach-auditor`** — invoke at **Stage 6 (Outreach / Packaging, `Law K12`)** to verify that every number, vector, and SHA-256 hash in your report/README matches your JSON certificates digit-for-digit.
2. **Why `MONITOR` and `AUDITOR` Run in Separate Terminal Tabs (`Law K3` + `Law K10`):**
   - By `CONSTITUTION §16 (K10 Dual-Thread Governor)`, the `MONITOR` and `AUDITOR` supervisors live in **separate terminal tabs** inside the same project folder (never inside the worker's own context window):
     - **Tab 1 (`PROOFER` Worker):** Runs `claude --model haiku` (or `sonnet`/`opus`), executes experiments, logs `micro_bet.py` + `rgraph.py`, and reads `wiki/meta/AUDITOR_INBOX.md` at the start of every cycle.
     - **Tab 2 (`MONITOR` Governor):** Runs either `sh scripts/run_monitor_loop.sh 600 haiku` (automatic 10-minute Haiku heartbeat!) or interactive `claude --model haiku` with the `MONITOR` prompt from `FIRST_INITIATION.md` §III-A.
     - **Tab 3 (`AUDITOR` Interactive Coach):** Runs interactive `claude --model haiku` with the `AUDITOR` prompt from `FIRST_INITIATION.md` §III-B, writing mathematical hints and `Law M2` pivots into `wiki/meta/AUDITOR_INBOX.md`.
