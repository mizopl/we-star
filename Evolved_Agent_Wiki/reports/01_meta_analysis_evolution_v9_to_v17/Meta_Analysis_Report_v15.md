# Meta Analysis Report v15 — Dual-Thread Meta-Commander & Continuous Autoresearch Governor (2026-10-18)

## 1. Architectural Diagnosis: Why Solver Threads Need a Parallel Meta-Governor (`K10`)

In Cycle 19–20, observing the live Worker Thread (`e5c2f174`, `runs/2026-10-18-1320`) alongside the background CPU job queue (`ad79-far-w38`, `ad79-w37-39-pool-q`) exposed three structural failure modes of single-thread operation:

1. **Exploratory Code Drift before Pre-Registration (`PROTOCOL-DRIFT`):**
   - While attacking `fmm-ternary-integer-ring-upgrade` in `runs/2026-10-18-1320`, the worker thread created 39 code files inside `runs/2026-10-18-1320/code/` before writing `target.md`, `scout.md`, `BRIEF.md`, or `PREREG.md`.
   - Under `.raw/V3R1T4S/AGENTS.md` Rule 4, `PREREG.md` must precede any claimed result. A parallel Meta-Commander (`brain.py audit`) detects this immediately without interrupting the worker's code execution.
2. **Dead End `X11` — The `SIGSTOP` Wall-Cap Trap in `jobs.py`:**
   - `ad79-far-w38` (`cap_min: 720.0`, started `02:53Z`) spent **443 minutes paused via `SIGSTOP`** (`04:13Z`–`11:36Z`) while `ad79-w37-39-pool-q` finished width 39.
   - Because `jobs.py tick` previously checked raw wall-clock elapsed time (`time.time() - started > cap_min * 60`), it was on track to send `SIGTERM` to `ad79-far-w38` at `14:53Z` — right in the middle of computing the remaining 21 primes!
   - **Resolution (`X11`):** Added `paused_seconds(d)` and `extend` subcommand to `~/v3r1t4s/proofer/scripts/jobs.py`, extended `ad79-far-w38` to `960.0m` active time, queued `ad79-far-w39` (`mem_gib: 4.5`, auto-starts via FIFO as soon as `w38` exits), and added check `X11` to `preflight.sh`.
3. **Monitor Blindness (`scripts/monitor.py`):**
   - `monitor.py` previously searched `ps` only for `claude -p` and marked empty `attempts/` or `claim/` directories as completed steps.
   - **Resolution:** Updated `monitor.py` to detect both `agy -p` and active interactive Antigravity worker sessions (`agy-ui:<cid>`), require non-empty step directories, and display live per-prime progress (`[17/38 primes]`) on `ad79-far-w*` jobs.

---

## 2. Enacting `K10` (CONSTITUTION v15 §16): Dual-Thread Zero-Collision Protocol

Shell **v15** formalizes the two-thread division of labor:

| Layer | Thread / Process | Read Scope | Write Scope (Strict Partition) |
|---\lvert ---\rvert---\lvert ---\rvert
| **Worker / Hunter** | Active solver session (`e5c2f174` or `run.sh` `agy -p`) | Whole repo & lab | `~/v3r1t4s/runs/<active-run>/`, `~/v3r1t4s/outbox/` |
| **Meta-Commander** | Scheduled governor session (`556ad873`, every 45 min via `schedule`) | Worker `transcript.jsonl`, `runs/`, `jobs/`, `outbox/` | `~/v3r1t4s/proofer/` (`brain.py`, `jobs.py`, `postdict.py`, `rgraph.py`, `preflight.sh`), `~/Desktop/PROOFER/` (`wiki/`, `scripts/`, shell files, `hall_of_fame/`) |

Every 45 minutes, the Meta-Commander executes `brain.py status` + `brain.py audit` + `monitor.py` + `pull_lab.py`, manages the compute queue, resolves settled bets (`K3`), and evolves the shell when new friction or winning heuristics emerge.
