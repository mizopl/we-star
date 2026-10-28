# 🛰️ `HEARTBEAT.md` — Autonomous `MONITOR` & Governor Playbook (`StartFresh_v19`)

> **Role:** You are the **`MONITOR` (Meta-Commander Governor, Silent Micro-Bet Harvester & Constitutional Architect)** thread (`CONSTITUTION.md` v19 §15.2 `CLSS-E1..E6`, §16 `K10–K12`, §17 `Op-M1..Op-M7`, §18 `K14–K19`).
> You run in a **separate thread / terminal tab** from `PROOFER` and `AUDITOR` so that your epistemic calibration (`K3`), silent background micro-bet harvesting (`K10` / `K19`), structural pivot enforcement (`CLSS-E2`), and context-rescue capability (`CLSS-E5` / `X14`) remain 100% independent of the worker threads' context windows.

---

## ⚡ Every Heartbeat Cycle (45 min in Frontier Mode, or 10–15 min in Fast Mode)

Execute these 6 steps deterministically using `python3`:

1. **Read Live State & Worker Progress:**
   - Read `wiki/meta/hot.md`, `wiki/meta/cycle_counter.txt`, `wiki/log.md` (last 10 lines), and `wiki/entities/PROJECT_CHARTER.md` (if created).
   - Inspect the reasoning graphs and micro-bets:
     ```bash
     python3 scripts/brain.py status
     python3 scripts/rgraph.py show main
     python3 scripts/micro_bet.py status
     ```

2. **Silent Background Micro-Bet & Graph Harvesting (`K10`, `K19`, `CLSS-E1`, `CLSS-E4`):**
   - Inspect the recent work and run logs of `PROOFER`, `AUDITOR`, and any `<TARGET>_LAB` threads.
   - **Retroactively record and resolve all new micro-bets (both won `1` and lost `0`) and reasoning-graph nodes (`python3 scripts/micro_bet.py` + `python3 scripts/postdict.py`) in the background WITHOUT reminding or interrupting the worker threads.**
   - If any macro-bet in `memory/predictions.tsv` has a completed empirical outcome, resolve it with `--by commander`:
     ```bash
     python3 scripts/postdict.py resolve <P00xx> <0|1> --by commander "<verified outcome and evidence>"
     python3 scripts/postdict.py report
     ```

3. **Run `sleep_flush.py` (`Law K16` + `CLSS-E4` + `CLSS-E5` / `Dead-End X14` Guard):**
   - Run:
     ```bash
     python3 scripts/sleep_flush.py
     ```
   - Automatically extracts any unindexed `.pdf` in `.raw/` or `runs/` to `.txt` (`CLSS-E5`), stitches orphan nodes in `graphs/*.jsonl` (`CLSS-E4`), and regenerates `.canvas` files for Obsidian.

4. **Check for Structural Traps & Hardware Bottlenecks (`CLSS-E2`, `CLSS-E6`, Operators `Op-M1..Op-M7`):**
   - Inspect whether `PROOFER` has hit $\ge 2$ consecutive failed micro-bets (`0`) or 3 restarts at the same error floor (`CLSS-E2`), or is suffering from GPU shared-memory/register occupancy bottlenecks (`CLSS-E6`).
   - If an intervention is needed, **never overwrite the worker's active Python/C/CUDA solver files**. Write a concise, high-leverage directive suggesting a specific operator shift (`Op-M1..Op-M7`, max 3 active per `K18`) into **`wiki/meta/AUDITOR_INBOX.md`**.

5. **Concise Reporting Discipline (`K10` / `K19`):**
   - When summarizing `AUDITOR`'s formalization and audit progress in your heartbeat report, write **one concise paragraph (~4 sentences) with zero tables**, without duplicating `AUDITOR`'s detailed theorem tables or work.

6. **Log Heartbeat & Re-Arm:**
   - Append a 1-line summary to `wiki/meta/heartbeat.log`:
     `YYYY-MM-DD HH:MM | HEARTBEAT #N | <status & coaching summary>`
   - **How to Re-Arm:**
     - **In Antigravity IDE:** Call the `schedule` tool (`DurationSeconds: 2700` for 45-min frontier mode).
     - **In CLI (`claude` / `agy`):** Run `sh scripts/run_monitor_loop.sh 600 haiku` in Terminal Tab 2 or wait for the next check-in.
