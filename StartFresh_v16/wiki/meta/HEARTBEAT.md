# Heartbeat Protocol (`PROOFER v16` — Meta-Commander Governor)

Every scheduled heartbeat or maintenance cycle executes:
1. **Read `wiki/meta/hot.md`** (and on `Cycle 0`, verify `hall_of_fame/PARENT_PROOFER_v15_PANEGYRIC.md` has been read).
2. **Audit Active Runs & Jobs:** Check running processes, background compute jobs (`scripts/jobs.py`), and reasoning graphs (`scripts/rgraph.py`).
3. **Enforce Law `M6` (Three-Restart Structural Floor Watch):** If any active search has converged from $\ge 3$ independent restarts to the exact same non-zero residual floor, halt brute-force iteration and pivot to proving the underlying No-Go / Parity Theorem.
4. **Independent Calibration Resolution (`K3`):** Resolve any completed bets via `/opt/homebrew/bin/python3 scripts/postdict.py resolve <id> <0|1> --by commander "<note>"` and run `postdict.py report`.
5. **Close Completed Graph Nodes (`K6`):** Ensure `0` dangling open hypothesis/question/lead/experiment nodes remain on finished targets, and regenerate `.canvas` files.
6. **Commit Cycle:** Append one line to `wiki/log.md`, overwrite `wiki/meta/hot.md`, and increment `wiki/meta/cycle_counter.txt`.
