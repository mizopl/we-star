# Dossier: square-grid-lattice-gas-exact-counts-oeis

## Best verified so far
- **CONFIRMED_PARTIAL (p1), run 2026-10-17-1252:** A054759(15) = 4310182149988584261406143524214457416387448
  (Eulerian orientations of the 15×15 torus / square ice). Two agreeing runs (RUN_A forward+closed-form 11 primes
  <2^20; RUN_B reversed-encoding+explicit-walk 12 disjoint primes <2^19), reproduces all 14 published terms, CRT
  bounded above a·2^64. Three-skeptic panel all pass (two recomputed all 23 residues from scratch); honesty gate
  CONFIRMED_PARTIAL; package outbox/2026-10-17-anonymous-8ee58c17-fd616054 passes CHECK_RUN. Growth clause NOT met
  (not part of p1). **Ready for the human: say "submit 2026-10-17-anonymous-8ee58c17-fd616054".**
- A054759 sector transfer-matrix code reproduces all 14 published terms (runs/.../smaller-first/code/sixvertex.py).

## Live leads
- **p2 = A089980 antidiagonal 79 — PROGRESS run 2026-10-17-2208 (current state; supersedes the L1754 lines below).**
  w=0..34: two decompositions agree exactly (hs_mod primes in (2^30,2^31) vs far.py primes < 2^30, 18/18 for w=17..34,
  runs/2026-10-17-2208/attempts/cross-check/code/compare_out.txt; independence audit and own fresh-prime spot check
  w=17..22 12/12). w=35,36: hs_mod ACCEPTED (0 published mismatches, check prime ok;
  runs/2026-10-17-2208/attempts/extender-harvest/antidiag79_w35plus.tsv). Still missing: far.py w=35,36 (QUEUED as
  jobs ad79-far-w35 / ad79-far-w36, results -> runs/2026-10-17-1913/attempts/far-import/antidiag79_far.tsv);
  hs_mod w=37..39 (job ad79-w37-39-pool-q, 2 jobs in parallel, cap 1800 min, submitted 22:13Z by the commander
  after it superseded ad79-w37-39-pool for timeouts under contention; res/ in run 1913's extender folder; 18 w=37
  files incl. partials at 22:20Z); far.py w=37..39 (not started; ~0.46/0.76/1.2 ks per prime
  and ~2.6/4.2/6.8 GB per process HEURISTIC from phi^w scaling — w=39 may not fit this host's RAM). Next run:
  (1) `jobs.py list`, harvest far w=35/36 and compare with the extender values; (2) harvest/assemble w=37 (assemble.py
  35 39); (3) queue far.py w=37 when memory allows; (4) when all 40 cells agree: claim/ + panel.
  Novelty wording (settled-check 2208): cells w<=7 of antidiagonal 79 are implied by published OEIS row sequences
  (A000045, A001333, A051736, A051737, A089936-A089938) and agree with ours; the claim is "first full antidiagonal 79".
- **p2 = A089980 antidiagonal 79 — PROGRESS run 2026-10-17-1754.** 35 of 40 distinct cells done: exact T(w,79-w)
  for w=0..34 in runs/2026-10-17-1754/attempts/extender/antidiag79.tsv. Each width reproduced ALL its published
  cells (0 mismatches; 2142 checks total) with a held-out CRT check prime; peak RSS 463 MiB at w=34 (~44 min total).
  Widths 0..16 are two-decomposition-agreed (modular frontier+CRT vs an independent exact-bigint full-column transfer,
  attempts/small-data/; 17/17). Widths 17..34 are single-decomposition NUMERICAL (+ fresh-prime self-break on w=30/32/34).
  Status re-confirmed OPEN (b-file still d=78, "Liang Kai antidiagonals 0..78"). NOT a claim (row incomplete + single
  decomposition for w>=17). Next, in order: (1) widths 35,36 (now known safe, ~0.6-0.9 GiB) then 37,38,39 one prime
  per process when `sysctl vm.swapusage` shows headroom; (2) a SECOND modular decomposition (reversed/boustrophedon or
  column-sweep, disjoint primes) for w=17..39 to meet the two-run rule on every cell; (3) three-skeptic panel; then a
  whole-row CONFIRMED_PARTIAL candidate. Graph: L1754.
- **[superseded] p2 run 1708 counter build.** Fast counter
  runs/2026-10-17-1708/attempts/small-data/code/hs_mod.py (two-piece Fibonacci frontier, numpy, uint64 mod p<2^31)
  reproduces 1714 published cells (widths 0-20,22,24,26,28,30; 0 mismatches); w=38/39 length-2 spot checks match.
  Measured w=39 L=40: 315 s/prime, 3.05 GiB (NUMERICAL); whole antidiagonal ~8.6 core-h at 32-37 primes (HEURISTIC).
  Not published anywhere (settled-check 1708). Next steps, in order: (1) DONE in run 1708 (per-prime exact(), --first-prime-index; old code hs_mod_v1.py) and
  implement --first-prime-index; (2) DONE for w=32 (47 cells, 0 mismatches, one prime per process, 135 MiB); next validate w=34 alone (~935 s);
  (3) residues for w<=39 one prime per process, <=3 in parallel only if swap is free; each w=39 run gives T(39,39)
  as a free check; (4) a second decomposition with disjoint primes (column sweep or reversed bit encoding) for the
  two-run rule; (5) panel. "New row" for antidiagonal-read A089980 = antidiagonal 79 (all 80 cells); state the
  reading in the claim and let CRITERION judge it.
- **A210662 row 28 (alt p2):** contains A028420(28) itself (monomer-dimer 28x28, 2^28 broken-profile states) — as
  hard as the main target. Lower priority.
- **main target A006506(40)**: T(40,40) with hs_mod.py ~542 s/prime, 4.93 GiB, ~5-5.7 core-h (HEURISTIC). Still
  capped at PROMISING by the growth clause (see dead angles) unless the human rules on it.
- **A027683(33)** (p1 bis, torus hard squares): feasibility unchecked.

## Dead angles / lessons
- The main criterion's "a(N)^(1/N^2) within 1e-3 of the entropy constant" is UNREACHABLE at reachable finite n:
  published a(14) gap 0.0085, a(15) gap 0.0074 vs Lieb W=(4/3)^(3/2)=1.539601. Treat it as an asymptotic note.
  A main-sequence integer win will still fail this clause literally — flag it, never round.
- Background subagents in headless mode die ~10 min after the turn ends: run lens/panel subagents in the
  FOREGROUND and wait (fixed in run.sh / RUN_PROMPT; PROOFER v9.1.1). NOTE run 1754: a long numpy compute also
  exceeds the 10-min foreground Bash cap, so the primary compute ran as a commander-launched DETACHED background
  process (nice + per-width SIGALRM cap + per-width checkpoint), monitored with a `while kill -0 PID` waiter; it
  survives turn boundaries. The lens SWARM was adapted: settled-check + the independent exact-bigint cross-check ran
  as fresh-context foreground subagents; the heavy frontier compute ran directly under the commander for tight memory control.
- hs_mod frontier memory scales ~phi^w, NOT the 3 GiB flat fear: measured peak 119 MiB (w=30), 189 (w=32), 297
  (w=33), 463 MiB (w=34). So widths up to ~36 are safe even with saturated swap; only w>=37 is genuinely heavy.
- GF/linear-recurrence extrapolation to get a new cell is DEAD for hard widths: for fixed w the row is C-finite with
  recurrence order ~phi^w, needing ~2*phi^w published cells; only 79-w exist. Viable only for tiny w (DP already instant).

## Working tools
- arXiv 2505.12776's "m+n<=79" is KING graphs, not grids; Liang 2507.04007 covers A089980 m+n<=78 and borrowed N(39,39).
- Several CRT primes in one process at width>=32: no speedup, memory multiplies, thrashes swap. One prime per process.
- The host's swap was ~13 GB used by other processes during run 1708: check `sysctl vm.swapusage` before big widths.
- rgraph keys collide with other sessions writing the same graph; use run-suffixed keys (e.g. R1708A).
- No `timeout`/`gtimeout` on this Mac: use Python signal.alarm caps.
- `python3 -I` breaks local imports (sixvertex); run own first-party code without -I.
- float64 BLAS modular matmul is EXACT here: entries<p<2^20, contracted dim<=C(15,7)=6435, sum<2^53. Verified.
- Standalone stdlib checker (pure-python sector TM + brute force + CRT) runs ~70 s; see the package.

## Beliefs (per PROOFER §3.4)
Run 1754: P0012/P0013/P0014 all hit (brier 0.023/0.062/0.003). Updated beliefs: (a) the 0-mismatch b-file gate is
near-certain for widths adjacent to already-reproduced ones — price ~0.92, not 0.85. (b) Frontier memory is phi^w,
so widths up to ~36 are safe even under swap pressure; only w>=37 is heavy — this run under-reached only because
the laptop's swap was held by other processes, not because the math was hard. (c) Exact-integer extension with an
in-pass deterministic gate + a second independent decomposition stays the highest-odds, panel-friendly shape (no
null test). The remaining p2 risk is purely logistical: finishing w=35..39 and a second decomposition for w>=17 on a
night with free RAM, then the panel reading "new row" = antidiagonal 79.

Run 1708: P0008 (0.15) hit — the frontier DP is core-hours per prime, not nights. Underconfident on vectorised exact DP cost. P0009 (0.30) missed — nothing is published past the frontier. p2 antidiagonal 79 is now the best-odds next object (feasible, unpublished); the remaining risk is the two-run independence and the panel reading "row" as antidiagonal.

Exact-integer extensions with a deterministic checker are the highest-odds shape here and are panel-friendly
(no null test; skeptics recompute from scratch). I was underconfident (P0006 p=0.2 hit, P0007 p=0.6 hit). The
main sequences are gated by the unreachable growth clause — lower the odds of a CONFIRMED_SOLUTION there. p2
rectangular rows need to be run as a primary lens, not a side check (P0005 missed for that reason).

## Commander note 2026-10-17T19:53Z: run 2026-10-17-1913 hit a session limit at 19:47Z (reset 22:00Z, RESUME_AFTER set)
Detached jobs kept running after the session died. **Resume them; do not restart them:**
- extender pool: PID 17509 `code/pool.py res 35 39 5 7.0 <deadline 23:15 local>` in runs/2026-10-17-1913/attempts/extender/ (widths 35–39, 5 procs, results under res/, log pool.log). It stops itself at its deadline.
- far-import: PID 19905 `far.py drive 33 34 2 2026-10-17T21:05:00Z` in runs/2026-10-17-1913/attempts/far-import/ (second decomposition, w=33–34 so far, antidiag79_far.tsv). It stops itself at 21:05Z.
- The run folder has no lens report.md files yet. The resumed run must write them, run self-break and the panel if the whole row w=0..39 has two agreeing decompositions, then the gate and check_run.
- Commander 20:33Z: pool.py `cap_sec(w)=max(600, 27*1.62**(w-34)*4)` gives 600 s for w=37, but w=36 jobs took 327–362 s, so w=37 needs ~550–650 s and w≥37 jobs time out (3 FAIL by 22:31 local). Widths 35–36 finished (res/ has 78 files). On resume, rerun the failed (w,j) with a per-job cap of ≥2× the measured time of the previous width (w37 ≥1200 s, w38 ≥2000 s, w39 ≥3200 s). It is just a runtime parameter of the frozen counter, so it does not affect PREREG.
- **Commander 21:13Z: THE ONLY POOL now running/queued is `code/pool_commander.py res 37 39 4 7.0`** (the frozen pool.py with cap_sec 1283/2078/3367 s for w=37/38/39). It is started by waiter PID 25617 once pool PID 17509 exits (~21:25Z) and logs to runs/2026-10-17-1913/attempts/extender/pool_commander.log. **Do NOT start another pool on res/**: monitor it, and work on the second decomposition (far-import) and the reports instead. HEURISTIC estimate for ~105 remaining jobs: ~12–15 h (overnight). Kill only its PID (written in the log as child pids).
- Commander 22:14Z: the w37–39 pool now runs **as queue job `ad79-w37-39-pool-q`** (2 parallel jobs, cap factor 4.0). The old adopted pool was superseded: with 4 parallel jobs, w=37 jobs hit 1283 s under swap contention. far-w35 and far-w36 failed at first because of a relative cwd (jobs.py bug, fixed) and were requeued; they are running now. Check them with `jobs.py list`.

## Commander 2026-10-18: p2 is PARKED in the job queue
Jobs ad79-far-w35, ad79-far-w36 and ad79-w37-39-pool-q run under the launchd ticker. A run only needs to **harvest** them (jobs.py list; out.log or res/) when they finish. Per K2 it must not wait on them, and they do not block runs from taking the next charter quarry (covering-designs-record, charter v2).
- Commander 00:53Z: far w35 and w36 jobs finished. Their FINAL T values **equal** the hs_mod values (antidiag79_w35plus.tsv in run 2208): w35 has 275 digits and w36 has 277. So **w=0..36 now agree under two decompositions (37/40)**. hs w37 is complete (37/37 residues in res/; it still needs assembling). Submitted job ad79-far-w37 (cap 480 min, 2.8 GiB). Remaining: far w37, then w38 and w39 for both methods.
- Commander 02:53Z: far w37 FINAL equals the hs_mod w37 assembled by the frozen assemble.py (runs/2026-10-17-1913/attempts/extender/commander/assemble_w37_38.tsv, 278 digits). hs w38 is ACCEPTED (0/41 mismatches, 279 digits). **38/40 cells now agree under two decompositions (w=0..37).** Queued ad79-far-w38 (mem 3.0 is set low on purpose, since the ticker's 20% free-memory guard is the real protection; expect ~3.6 GB RSS). The pool has started w39.
