# PROOFER Heartbeat (every 20 min in the live session — shell v13)

Act on your own, even when unsure: an uncertain move that is logged, bet on and reversible beats waiting. The V3R1T4S kit and CONSTITUTION v13 still bind everything: no outward action, statuses only go down, a single context writes at most PROMISING, CHECK_RUN must PASS, and shell changes need the Hall of Fame ceremony.

## 1. Sense (always, cheap)
- `date -u`; `ls .lock RESUME PAUSE`; `ps -axo pid,etime,command | grep -E "[a]gy -p|[c]laude -p"`
- `head -3 REPORT.md`; `tail -3 LOG.md`; `tail -5 logs/$(date +%F).log`
- `python3 scripts/monitor.py`; `python3 scripts/jobs.py list`; `cat logs/preflight.txt`

## 2. Decide (first matching branch wins)
1. **PAUSE exists** → only append the heartbeat line; stop.
2. **Run in progress** → health check. The log or run folder changed in the last 40 min means healthy, so stop. No change for 40 min, or elapsed above 2× the effort budget (light 2 h, standard 6 h), means stalled: kill exactly that `agy -p` (or `claude -p`) PID (it is ours, started by run.sh), note it in the graph (`kill` node with the reason) and in the dossier, then go to branch 4.
3. **RESUME marker exists** → a limit hit. Leave it to the launchd `com.proofer.v3r1t4s.resume` agent (every 20 min); if the marker is older than 6 h, run `sh run.sh resume` in the background yourself.
4. **A run finished since the last heartbeat** (REPORT.md is newer than `wiki/reports/lab/heartbeat.log`'s last line) → **digest**:
   - read REPORT.md fully; `python3 scripts/pull_lab.py`
   - **you** resolve every prediction it settles, literally (K3): `PROOFER_HOME=. python3 scripts/postdict.py resolve <id> 0|1 --by commander "<note>"`; write the commander postdiction lines into that run's `POSTDICTION.md`, then `report` and **overwrite** `wiki/meta/beliefs.md`
   - every new infrastructure dead end becomes a check in `scripts/preflight.sh` (K4)
   - make sure every dead line in the run is a `kill` node in the graph, and every live lead is a `lead` node
   - log new bets for the next run (predict before acting)
   - then go to branch 5
5. **Idle, nothing pending** → **push forward**: launch the next run now with `sh run.sh` in the background. Before that:
   - if the last run's REPORT says the effort was too small for a live lead, raise `effort` in `settings.md` (light → standard), and say so in the log
   - if the quarry is dead or 3 consecutive runs gave NOTHING with no live lead, run VS over the charter's remaining quarries (`vs_sample.py`), bet, and point the next run at the pick through the dossier, never by editing kit files
   - if disk free < 10 GB: do not launch; write it under Needs you
6. **Blocked on the human** (an item only they can do) → never wait idle. Do the best reversible work around it (tooling, a checker, the next quarry's BRIEF) and keep the item in DECISIONS_NEEDED.

## 2b. Resource guard (always, before deciding)
- If `df -g ~` shows **< 12 GB free** or `memory_pressure -Q` shows **< 15% free**: pause (SIGSTOP) the newest commander-submitted compute job by its exact PID (`jobs.py list`, run=commander-*), append `paused <pid> <reason>` to that job's events.log, and resume it (SIGCONT) at a later heartbeat once disk is ≥ 14 GB and memory is ≥ 30%. Never pause a run's own jobs or anything that is not ours. Swap growth eats disk on macOS; it is the usual cause.

## 3. Record (always)
- After any submission (a PR opened on the human's "yes"): write `archive/SUBMITTED-<submission-id>.txt` with the PR URL and the UTC time. The monitor moves the package from "Needs you" to "Submitted" and shows the live PR state.
- Append one line to `wiki/reports/lab/heartbeat.log`: `UTC | branch | action | next`.
- Update `wiki/meta/hot.md` only when state changed. A full Run OS cycle (log, counter) runs only after a digest (branch 4), not on every heartbeat.
- Reply in the chat with at most 3 lines: what changed, what is next, anything the human must do. If nothing changed, reply with one line.
