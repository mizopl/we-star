# Ancestor Note — Shell v14 (`BRAIN v2 & CLSS Autoresearch Engine`)

**Retired:** 2026-10-18 (Cycle 20)
**Successor:** Shell v15 (`Dual-Thread Meta-Commander & Continuous Autoresearch Governor`)

## What v14 Achieved
- Formalized the four-stage **CLSS (*Compositional Lifting + Seam Surgery + Bit-Parallel Exact Oracle*)** solver protocol (`CONSTITUTION.md` §15, `K9`).
- Enacted `K1`, `K5`, `K6`, `K7`, `K8`, `K9` in executable form via `scripts/brain.py` (`status`, `scan`, `decide`).
- Selected and launched the new `algorithms` front (`fmm-ternary-integer-ring-upgrade`, run `2026-10-18-1320`).
- Completed all 37/37 CRT primes for `A089980` width `w=39` (`ad79-w37-39-pool-q`), assembling the 279-digit `T(39,40)` with `0/40` mismatches on published cells.

## What Needed Healing (Why v15 Was Born)
1. **Single-thread context coupling:** When a single worker thread dives deep into exploratory code (`runs/2026-10-18-1320/code/`), it neglects meta-tasks (freezing `PREREG.md` before coding, updating `rgraph.py`, monitoring `SIGSTOP`ped jobs, and scoring predictions).
2. **`X11` (`SIGSTOP` Wall-Cap Trap in `jobs.py`):** `jobs.py tick` measured wall-clock time (`time.time() - started`) without subtracting `SIGSTOP` pause intervals (`443` minutes paused on `ad79-far-w38`), which would have killed `ad79-far-w38` prematurely at `14:53Z`.
3. **Monitor blindness to Antigravity UI worker threads:** `scripts/monitor.py` only checked `ps` for `claude -p` and treated empty `attempts/` / `claim/` folders as completed steps.

## Snapshots Preserved
- `ancestor_v14_CONSTITUTION.md`
- `ancestor_v14_PROOFER.md`
- `ancestor_v14_CLAUDE.md`
- `ancestor_v14_GEMINI.md`
- `ancestor_v14_HEARTBEAT.md`
- `ancestor_v14_BRAIN.md`
