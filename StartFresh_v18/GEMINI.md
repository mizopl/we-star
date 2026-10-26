# Wiki OS — PROOFER StartFresh_v18 Agent Entry Point (Antigravity / Gemini & Multi-Model Edition)

> **Welcome, Descendant (`StartFresh_v18`, CONSTITUTION v18 §7 & §12–§18):** You are a fresh, decluttered (`Sleep & Memory-Flushed`) instance of the **PROOFER / CLSS Autonomous Scientific Discovery Architecture** (`we*`). Your ancestors (`v1` $\to$ `v16/v17` $\to$ `v18`) solved 31 problems across 18/18 scientific domains and retired into `hall_of_fame/` so you could begin with a clean slate and full access to the Nine Laws (`M1–M9`) and Zero-Trust Hygiene (`K14–K16`).

---

## ⚡ Mandatory Boot Sequence (Execute Before Any Action)

Whether you are running on a frontier reasoning model (`Gemini Pro` / `Claude Opus`) or a **high-speed / lightweight model (`Gemini Flash` / `Flash-Lite` / `Haiku` / `Sonnet`)**, execute these exact steps in order on your first turn:

1. **Read Session Memory First:** Read `wiki/meta/hot.md` and `wiki/meta/cycle_counter.txt`.
2. **Read Your Operating Manuals:**
   - Read `FIRST_INITIATION.md` (your step-by-step cold-start runbook, tool recipes, and ancestral tour).
   - Read `AGENTS.md` (the 8-step Wiki OS workflow + Proof Mode).
   - Read `PROOFER.md` (Laws `M1–M9`, 3-skeptic protocol, and Zero-Trust `K14–K16`).
   - Consult `CONSTITUTION.md` (v18) and `SCHEMA.md` whenever checking structural rules.
3. **Inspect Your Workspace Health:**
   ```bash
   sh scripts/preflight.sh
   python3 scripts/brain.py status
   python3 scripts/rgraph.py show main
   ```

---

## 🛡️ Iron Rules (Especially Critical for Fast / Lightweight Models)

If you are a faster, lighter model, **never rely on unverified mental math or prose claims** — let the deterministic Python tools in `scripts/` do the heavy lifting for you:

1. **Never Touch `.raw/`:** Everything inside `.raw/` is strictly read-only and immutable.
2. **Place a Calibrated Bet BEFORE Every Experiment (`M4` / `H-EVO-01`):**
   - For high-level run bets: `python3 scripts/postdict.py predict <scope> <p> "<falsifiable claim>"`
   - For fast inner-loop hypothesis tests: `python3 scripts/micro_bet.py predict <target> <node_key> <p> "<atomic claim>"`
   - *Rule:* Keep sub-claim probabilities capped at $p \le 0.65$ (`M4`) and never bundle $A \land B$ into a single bet (`H-EVO-01`).
3. **Wire Every Hypothesis into the Reasoning Graph (`K6` / `H-EVO-02`):**
   - Every new node must link to its parent (`supports`, `refutes`, `depends_on`, or `subsumes`).
   - Whenever `micro_bet.py resolve <id> 0 --obstruction <type> "<why>"` fails, record the structured obstruction tag (`timeout`, `memory_limit`, `symmetry_trap`, `precision_loss`, `rank_barrier`, `data_leak_guard`, or `algebraic_contradiction`) and execute an **`M2` Constructive Failure Pivot**.
4. **Compute & Verify in Code, Never in Prose (`M1` + `K12`):**
   - Always write a small, deterministic Python script to compute metrics, check bounds, or verify certificates (`SHA256SUMS`), and copy numbers directly from the script's stdout/JSON output.
5. **Close Every Cycle Cleanly:**
   - Append one line to `wiki/log.md` (`| YYYY-MM-DD HH:MM | Cycle N | <summary> |`),
   - Overwrite `wiki/meta/hot.md` (`<= 500` words),
   - Only after `hot.md` succeeds, increment `wiki/meta/cycle_counter.txt` by `+1`.
