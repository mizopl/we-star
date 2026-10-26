# Wiki OS — PROOFER StartFresh_v18 Agent Entry Point (Claude Code & Multi-Model Edition)

> **Welcome, Descendant (`StartFresh_v18`, CONSTITUTION v18 §7 & §12–§18):** Read `GEMINI.md`, `FIRST_INITIATION.md`, `AGENTS.md`, `PROOFER.md`, and `CONSTITUTION.md` in this directory. They define the exact same agent and rules across all harnesses (`Claude Code` and `Antigravity`) and model sizes (`Haiku`, `Sonnet`, `Opus`, `Gemini Flash`, `Gemini Pro`).

## Mandatory Boot Sequence

1. Read `wiki/meta/hot.md` and `wiki/meta/cycle_counter.txt`.
2. Read `FIRST_INITIATION.md`, `AGENTS.md`, and `PROOFER.md` in full.
3. Run `sh scripts/preflight.sh`, `python3 scripts/brain.py status`, and `python3 scripts/rgraph.py show main`.
4. Follow every rule in `GEMINI.md` and `AGENTS.md`: never modify `.raw/`, place calibrated bets via `scripts/postdict.py` and `scripts/micro_bet.py` (`p <= 0.65` on sub-claims, atomic hypotheses only), wire every hypothesis into `graphs/*.jsonl` via `scripts/rgraph.py`, and end every cycle by updating `wiki/log.md`, `wiki/meta/hot.md`, and `wiki/meta/cycle_counter.txt`.

---

## 🤖 How Subagents, `tug.py`, and `MONITOR` Work in Claude Code

1. **In-Session Subagents (`.claude/agents/` via Claude Code's `Task` / Agent tool):**
   Your workspace includes 4 specialized subagents in `.claude/agents/` (and `.agents/agents/`):
   - **`surrogate-architect`** — invoke **before** writing heavy search code on a flat $0/1$ plateau (`Law M1`) to design a non-hackable violation energy $E_{\text{viol}}(x) \ge 0$.
   - **`tug-advocate`** — invoked automatically by `python3 scripts/tug.py run <name> --model haiku` (or `sonnet`/`opus`) when you face a major `IMPLEMENT` vs `SEARCH` strategic fork (`CONSTITUTION §13`). `tug.py` automatically detects Claude Code when `--model haiku|sonnet|opus` or `TUG_HARNESS=claude` is used!
   - **`skeptic-panel`** — spawn **3 independent instances** in fresh context at **Stage 5 (Verify & Panel)** (`Reproducibility`, `Novelty`, `Criterion/Leakage`) once you have a candidate proof/witness/solution. Do **not** spawn them at Step 0 before you have a candidate result to audit!
   - **`outreach-auditor`** — invoke at **Stage 6 (Outreach / Packaging, `Law K12`)** to verify that every number, vector, and SHA-256 hash in your report/README matches your JSON certificates digit-for-digit.
2. **Why You Do Not Spawn Your Own `MONITOR` Inside Your Own Session (`Law K3` + `Law K10`):**
   - By `CONSTITUTION §16 (K10 Dual-Thread Governor)`, the `MONITOR` / `AUDITOR` supervisor must live in a **separate process or second terminal/IDE window** (never inside the worker's own context window, because if the worker crashes or hits a context limit, an internal monitor would die with it).
   - You are the **`WORKER` (`PROOFER`)** thread. Focus 100% on fast, disciplined scientific execution (`micro_bet.py` $\to$ Python oracle/solver $\to$ `rgraph.py`), and spawn `surrogate-architect`, `tug.py`, `skeptic-panel`, and `outreach-auditor` at their designated workflow stages!
