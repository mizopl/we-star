---
id: v3r1t4s-jsp-optimizizer-open-upper-bounds
type: entity
tags: [v3r1t4s, v3r1t4s/optimization-benchmarks, kind/harvest]
inbound_links: 1
confidence: 0.8
last_ingested_sources: [".raw/V3R1T4S/bank/targets.json@7dd4480"]
status: "open"
priority: ""
notes: ""
category: optimization-benchmarks
kind: harvest
tractability: 2
compute: "laptop-hours"
disclosure: open
status_checked: "2026-10-08"
---
# Job-shop scheduling: lower the makespan upper bound on an open Taillard / Demirkol / SWV / YN / ABZ instance (Optimizizer tables)

# Overview

> Bank id `jsp-optimizizer-open-upper-bounds` · harvest · tractability 2 · laptop-hours · disclosure **open**
> Bank says open as of 2026-10-08. Statuses go stale — re-check the primary source before any work.

## Statement

Oleg Shylo's Optimizizer pages maintain the live best known lower and upper bounds, with the UB solution sequence, for the classical JSP benchmarks. Live on 2026-10-08: 20 Taillard instances (Ta18, Ta22, Ta23, Ta25-27, Ta29, Ta30, Ta32, Ta33, Ta40-44, Ta46-50), 49 Demirkol DMU instances and 10 Extra instances (Abz08, Swv06-Swv10, Yn01-Yn04) have LB < UB. UBs and LBs moved in 2024-2026 (UBs by HTSFP2024, HUSTLLG2026, OptalCP2026, EVALDIVERSIFY; LBs by RL2024, YMRL2025/2026), so the tables are a live frontier. Find a feasible schedule with makespan strictly below the listed UB for any instance with LB < UB.

## Success criterion

A schedule for one instance listed with LB < UB on https://optimizizer.com/TA.php, https://optimizizer.com/DMU.php or https://optimizizer.com/Extra.php, given as per-machine job sequences in Optimizizer's own 'sol' format (one line per machine in instance machine order 0..m-1, each line the n job ids 0..n-1 in processing order), such that a standalone checker written from the OR-Library/JSPLIB instance format (first line 'n m', then one line per job of (machine, time) pairs, 0-based machines) builds the semi-active schedule from the job routings plus the machine sequences (longest path in the disjunctive graph; must be acyclic), independently computes the makespan, and reports a value strictly less than the UB shown in that table, re-fetched live immediately before claiming. The checker must first reproduce the listed UB from the table's own 'sol' sequence for that instance (e.g. https://optimizizer.com/solution.php?name=ta41&UB=2006&problemclass=ta -> 2006 from the JSPLIB ta41 file; verified by the vetter 2026-10-08). The schedule file, checker, instance file (with sha256) and table snapshot are saved together. Nothing is submitted to Optimizizer; the write-up goes to the human.

## Partial wins

- {"id": "close-small-gap-instance", "statement": "Close an instance with gap <= 3 (live: Ta33 1790/1791, Ta18 1393/1396) by a reproducible proof that no schedule with makespan <= UB-1 exists (CP-SAT / OptalCP run with logged seed, model file and a wall time a skeptic can repeat in under 1 hour on this 10-core Mac); counts only after the verifier re-runs it successfully."}
- {"id": "dmu-cscmax-improve", "statement": "Strict UB improvement on any open Dmu41-Dmu80 (cscmax) instance on https://optimizizer.com/DMU.php; these have the largest LB-UB gaps (e.g. Dmu41_cscmax_20_15_10 3130/3248, Dmu46_cscmax_20_20_6 3740/4035) so they are the most likely to be slack; same checker and re-fetch rule."}
- {"id": "extra-set-improve", "statement": "Strict UB improvement on Swv06-Swv10, Yn01-Yn04 or Abz08 on https://optimizizer.com/Extra.php, checked by the same standalone checker and re-fetch rule."}

## Verification

Instance data: Taillard ta01-ta80, swv, yn, abz in OR-Library/JSPLIB format from https://raw.githubusercontent.com/tamy0612/JSPLIB/master/instances/<name> (lines starting with '#' are comments); Demirkol instances from https://raw.githubusercontent.com/thomasWeise/jsspInstancesAndResults/master/data-raw/instance-data/demirkol/<rcmax|cscmax>_J_M_k.txt, where Optimizizer's DmuNN_<rcmax|cscmax>_J_M_k maps to <rcmax|cscmax>_J_M_k.txt (same 'n m' + (machine,time)-pair format). The skeptic runs the Python checker on (1) the Optimizizer 'sol' sequence (solution.php?name=<name>&UB=<ub>&problemclass=<ta|dmu|extra>) to confirm it yields the table UB, then (2) the claimed schedule. Seconds of compute. Re-fetch the table page with plain curl and parse the instance's <tr> (LB and UB are the leading integers of cells 3 and 4).

## Angles

- Tabu search with N7/N6 neighborhoods and path relinking (Nowicki-Smutnicki i-TSAB, Zhang et al. TS/SA) seeded from the posted UB sequence, run for hours with many restarts on 10 cores; most historical UB improvements came from exactly this with more wall time.
- Large-neighborhood search with CP-SAT: fix all but a window of ~30-40% of operations (time-window or machine-subset neighborhoods) and solve the subproblem to optimality repeatedly (LNS/CP hybrids produced the 2024-2026 improvements).
- Target the instances with the largest relative gap (Ta50 1837/1923, Ta41 1912/2006, Dmu cscmax instances with 3-7% gaps, Swv07 1523/1595): the UB is far from the LB so there may be real slack.
- Run OR-Tools CP-SAT with the full model, 10 workers, hint = posted UB schedule, for several hours on 30x20 and 50x20 instances; OptalCP2026 lowered several DMU UBs with a CP solver, so CP-SAT may lower one directly.
- Exploit a new 2026 LB (YMRL2026) landing within a few units of the UB: run a targeted satisfiability search for makespan = UB-1 with strong symmetry breaking.

## Pitfalls

- Instance format confusion: Taillard's original files list the times matrix and machines matrix separately (machines 1-based) whereas the OR-Library/JSPLIB format interleaves (machine, time) pairs 0-based. The checker must reproduce the posted UB from the posted sequence before any claim.
- Optimizizer 'sol' pages are machine sequences (m lines of n job ids), not start times; the checker must build the schedule from scratch and detect cycles. Checking only job-order feasibility or reading makespan from the attacker's own simulator is not enough.
- Several instances were improved in 2026 (HUSTLLG2026 on Ta26, Ta32, Ta44, Ta46 and many DMU; OptalCP2026 on DMU); re-fetch the specific table page immediately before claiming, and compare against UB not LB.
- Claiming a closed instance (LB = UB after a CP run) is only a partial win if the skeptic can repeat the run; a solver log alone is not a certificate.
- Do not use the GitHub REST API (api.github.com) for instance listings; it rate-limits unauthenticated calls (403 seen 2026-10-08). Use the raw.githubusercontent.com file URLs.

## Sources

- https://optimizizer.com/TA.php
- https://optimizizer.com/DMU.php
- https://optimizizer.com/Extra.php
- https://optimizizer.com/solution.php?name=ta41&UB=2006&problemclass=ta
- https://raw.githubusercontent.com/tamy0612/JSPLIB/master/instances/ta41
- https://raw.githubusercontent.com/tamy0612/JSPLIB/master/instances/swv06
- https://raw.githubusercontent.com/thomasWeise/jsspInstancesAndResults/master/data-raw/instance-data/demirkol/rcmax_30_20_10.txt
- https://raw.githubusercontent.com/thomasWeise/jsspInstancesAndResults/master/data-raw/instances/instances_with_bks.txt
- Status source: https://optimizizer.com/TA.php

## Citations

- [Problem page](../../../../.raw/V3R1T4S/known-unknowns/optimization-benchmarks/jsp-optimizizer-open-upper-bounds.md)
- [Bank entry](../../../../.raw/V3R1T4S/bank/targets.json) (id `jsp-optimizizer-open-upper-bounds`, commit `7dd4480`)

## Related Nodes

- [[V3R1T4S Optimization benchmarks]]
- [[V3R1T4S]]
