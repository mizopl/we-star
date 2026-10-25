# PROOFER Heartbeat & Meta-Commander Protocol (every 45 min via `schedule` — shell v15)

Act on your own, even when unsure: an uncertain move that is logged, bet on and reversible beats waiting. The V3R1T4S kit and CONSTITUTION v15 still bind everything: no outward action, statuses only go down, a single context writes at most PROMISING, CHECK_RUN must PASS, and shell changes need the Hall of Fame ceremony.

## 0. Dual-Thread Zero-Collision Rule (CONSTITUTION v15 §16, K10)
- **Worker Thread (`e5c2f174` / `run.sh`)** writes exclusively inside `~/v3r1t4s/runs/<active-run>/` and `~/v3r1t4s/outbox/`.
- **Meta-Commander (`556ad873`)** NEVER modifies files inside the worker's active `runs/<active-run>/code/` directory while the worker is live (`< 180s` since last `transcript.jsonl` step). Meta-Commander writes to `~/v3r1t4s/proofer/` (`brain.py`, `jobs.py`, `postdict.py`, `rgraph.py`, `preflight.sh`) and `~/Desktop/PROOFER/` (`wiki/`, `scripts/`, shell files, `hall_of_fame/`).

## 1. Sense & Audit (always, cheap)
- `/opt/homebrew/bin/python3 ~/v3r1t4s/proofer/scripts/brain.py status`
- `/opt/homebrew/bin/python3 ~/v3r1t4s/proofer/scripts/brain.py audit`
- `/opt/homebrew/bin/python3 ~/v3r1t4s/proofer/scripts/jobs.py list`; `/opt/homebrew/bin/python3 ~/v3r1t4s/proofer/scripts/jobs.py tick`
- `sh ~/v3r1t4s/proofer/scripts/preflight.sh > ~/v3r1t4s/logs/preflight.txt`
- `/opt/homebrew/bin/python3 ~/Desktop/PROOFER/scripts/pull_lab.py`; `/opt/homebrew/bin/python3 ~/Desktop/PROOFER/scripts/monitor.py`

## 2. Decide (first matching branch wins)
1. **Compute Queue Handoff (`A089980` / `jobs.py`):**
   - If `ad79-far-w38` has finished (`done`), verify `jobs.py tick` launched `ad79-far-w39`.
   - When both `ad79-far-w38` and `ad79-far-w39` are `done`, compare all 40 cells `w=0..39` between `hs_mod` (`attempts/extender/res/`) and `far.py` (`attempts/far-import/res/`).
2. **Active Worker Thread & Cloud GPU Supervision (`brain.py audit`, `K10` + `K11`):**
   - Inspect the worker's last 30 steps in `transcript.jsonl`: check tool failure rate, whether it is stuck in a loop, or whether it has `PROTOCOL-DRIFT` (coding before `PREREG.md`).
   - Enforce **`K11` (`Cloud GPU Offload Mandate`)**: verify heavy PyTorch / 3D CNN GPU jobs use `/opt/homebrew/bin/colab run --gpu L4|A100|H100` (`colab_gpu_runner.py`, Google Ultra `4,057+` compute units) or `kaggle_gpu_runner.py` (`Tesla T4`) rather than saturating local Mac Unified Memory (`mps`), and check `/opt/homebrew/bin/colab sessions` to stop any orphaned idle VMs after GPU runs complete.
   - Extract any new dead ends (`rgraph.py add/kill`) or infrastructure pitfalls (`preflight.sh` check, K4).
   - If the worker completed a run or settled a bet, resolve predictions literally (`postdict.py resolve <id> 0|1 --by commander`, K3) and overwrite `wiki/meta/beliefs.md`.
3. **Meta-Evolution (`Autoresearch on PROOFER`):**
   - When the worker's trajectory reveals a new winning pattern or recurring friction, update `brain.py` (`costs.tsv`, `clss_score`), `BRAIN.md`, or evolve the shell (`CONSTITUTION.md` + Hall of Fame snapshot ceremony §7.4).
4. **Idle (neither UI worker nor headless `agy -p` active, and no `PAUSE`):**
   - Launch the next scheduled run via `sh ~/v3r1t4s/run.sh` in the background if disk free ≥ 10 GB.

## 2b. Resource guard (always, before deciding)
- If `df -g ~` shows **< 12 GB free** or `memory_pressure -Q` shows **< 15% free**: pause (`SIGSTOP`) the newest commander-submitted compute job by its exact PID (`jobs.py list`, `run=commander-*`), append `paused <pid> <reason>` to that job's `events.log` (`X11` pause-aware cap will exclude paused time), and resume (`SIGCONT` + `resumed` line in `events.log`) once disk ≥ 14 GB and memory ≥ 30%.

## 3. Record (always)
- Append one line to `wiki/reports/lab/heartbeat.log`: `UTC | branch | action | next`.
- Update `wiki/meta/hot.md` and `wiki/log.md` (+ `cycle_counter.txt`) whenever a digest or shell evolution occurs.
- Output a concise 4–6 line status summary in chat.
