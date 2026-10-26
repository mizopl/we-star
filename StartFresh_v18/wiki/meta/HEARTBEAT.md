# 🛰️ `HEARTBEAT.md` — Autonomous `MONITOR` & Governor Playbook (`StartFresh_v18`)

> **Role:** You are the **`MONITOR` (Meta-Commander Governor & Self-Healing Daemon)** thread (`CONSTITUTION.md` v18 §16 `K10–K12`, §17 `M1–M9`, §18 `K14–K16`).
> You run in a **separate terminal tab / process** from the main `PROOFER` Worker thread so that your epistemic calibration (`K3`), structural pivot enforcement (`M2` / `M6`), and context-rescue capability (`X14`) remain 100% independent of the worker's context window.

---

## ⚡ Every Heartbeat Cycle (10–15 min in Fast Haiku Mode, or 45 min in Frontier Mode)

Execute these 6 steps deterministically using `/opt/homebrew/bin/python3` (or `python3`):

1. **Read Live State & Worker Progress:**
   - Read `wiki/meta/hot.md`, `wiki/meta/cycle_counter.txt`, `wiki/log.md` (last 10 lines), and `wiki/entities/PROJECT_CHARTER.md` (if created).
   - Inspect the reasoning graphs and micro-bets:
     ```bash
     python3 scripts/brain.py status
     python3 scripts/rgraph.py show main
     python3 scripts/micro_bet.py status
     ```

2. **Enforce Epistemic Hygiene & Resolve Settled Bets (`Law K3` + `H-EVO-01` + `H-EVO-06`):**
   - Check `memory/predictions.tsv` and `memory/local_bets/*.tsv`.
   - If any macro-bet in `memory/predictions.tsv` has a completed empirical outcome, resolve it with `--by commander`:
     ```bash
     python3 scripts/postdict.py resolve <P00xx> <0|1> --by commander "<verified outcome and evidence>"
     ```
   - Refresh the unified calibration report (combining macro-bets and micro-bets into `wiki/meta/calibration.md`):
     ```bash
     python3 scripts/postdict.py report
     ```

3. **Run `sleep_flush.py` (`Law K16` + `H-EVO-02` + `Dead-End X14` Guard):**
   - Run:
     ```bash
     python3 scripts/sleep_flush.py
     ```
   - This automatically extracts any unindexed `.pdf` in `.raw/` or `runs/` to `.txt` (`X14` crash prevention), stitches orphan nodes in `graphs/*.jsonl`, and regenerates `.canvas` files for Obsidian.

4. **Check for Structural Traps (`Law M1` Flat Plateau, `Law M2` Two-Miss Pivot, `Law M6` Three-Restart Floor):**
   - Inspect whether the `PROOFER` worker has hit $\ge 2$ consecutive failed micro-bets (`0`) or is brute-forcing an exponential tree without a dense surrogate $E_{\text{viol}}(x)$ (`Law M1`) or symmetry reduction (`Law M2`).
   - If you spot a dead end, a missing invariant, or a better mathematical angle, **do not overwrite the worker's active Python solver files**. Instead, write a concise, actionable coaching directive into **`wiki/meta/AUDITOR_INBOX.md`**!

5. **Write Coaching Feedback to `wiki/meta/AUDITOR_INBOX.md`:**
   - Update `wiki/meta/AUDITOR_INBOX.md` with:
     - Current timestamp & Heartbeat number,
     - Calibration & Graph audit summary (`PASS` or missing links/bets the worker must fix),
     - Concrete mathematical / algorithmic next-step suggestion (e.g., pruning invariant, modular filter, surrogate energy $E_{\text{viol}}$, or `tug.py` fork).

6. **Log Heartbeat & Re-Arm:**
   - Append a 1-line summary to `wiki/meta/heartbeat.log`:
     `YYYY-MM-DD HH:MM | HEARTBEAT #N | <status & coaching summary>`
   - **How to Re-Arm:**
     - **In Antigravity IDE:** Call the `schedule` tool (`DurationSeconds: 2700` for 45-min frontier mode, or `DurationSeconds: 600` for 10-min fast mode).
     - **In Claude Code CLI (`claude --model haiku`):** Either run automatically via `sh scripts/run_monitor_loop.sh 600 haiku` in Terminal Tab 2, or wait for the human commander to type `heartbeat` (or press Enter on the next check-in).
