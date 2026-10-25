---
id: v3r1t4s-psplib-j120-rcpsp-upper-bounds
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
# PSPLIB J120 (single-mode RCPSP): lower a best known heuristic makespan on an unproven instance

# Overview

> Bank id `psplib-j120-rcpsp-upper-bounds` · harvest · tractability 2 · laptop-hours · disclosure **open**
> Bank says open as of 2026-10-08. Statuses go stale — re-check the primary source before any work.

## Statement

PSPLIB (TU Munich) maintains best known heuristic upper bounds (HRS file) and proven lower bounds for the single-mode RCPSP sets. Live on 2026-10-08 the J120 merged JSON reports 600 instances, 89 proven optimal and 511 unproven; only 184 of the 600 carry a lower bound (95 unproven instances have LB < UB listed, 12 of them with UB - LB = 1), the other 416 have no LB at all. The HRS data carries per-instance author and date: 27 J120 bounds were lowered in 2024 by M. Vanhoucke and J. Coelho (18 on 2024-09-23), 17 in May-Aug 2026 by E. Goncharov (e.g. j12011_4 -> 194, j12016_9 -> 203, j12031_1 -> 196), and solution upload was re-enabled on 2026-05-06, so the table is live. Heuristic schedules are not published (only makespans), so ties cannot be copied. Find a precedence- and resource-feasible schedule with makespan strictly below the listed upper_bound for any instance with is_proven_optimal = false.

## Success criterion

A start-time vector (one integer start time per activity 1..n+2, dummies included) for one J120 instance whose entry in https://www.om-db.wi.tum.de/psplib/download_merged.php?set=j120&mode=sm has is_proven_optimal = false, such that a standalone checker written from the PSPLIB .sm format definition (PRECEDENCE RELATIONS successors, REQUESTS/DURATIONS durations and per-resource demands, RESOURCEAVAILABILITIES for the 4 renewable resources R1-R4) verifies every finish-to-start precedence (start_succ >= start_pred + dur_pred, zero lags), verifies for every integer period [t, t+1) over the whole horizon and for every resource that the summed demand of activities active in that period (start <= t < start + duration) does not exceed capacity, and reports the finish time of the sink (activity n+2) strictly less than the upper_bound for that (parameter, instance) in the merged JSON AND the Makespan in https://www.om-db.wi.tum.de/psplib/download_solution.php?set=j120&mode=sm&type=hrs, both re-fetched live immediately before claiming. The instance file must be the one from https://www.om-db.wi.tum.de/psplib/download_dataset.php?set=j120&mode=sm&format=zip (j120<param>_<inst>.sm; sha256 recorded). The checker must first (a) accept a serial-SGS schedule it generates itself and (b) reject a deliberately broken schedule (one precedence violated, one resource overload). The schedule, checker, instance sha256 and both fetched tables are saved together. Nothing is uploaded to PSPLIB; the write-up goes to the human.

## Partial wins

- {"id": "j60-j90-improve", "statement": "Same criterion on any J60 or J90 instance with is_proven_optimal = false in https://www.om-db.wi.tum.de/psplib/download_merged.php?set=j60&mode=sm or set=j90 (live: 98 and 105 unproven); counted as partial because these sets are smaller and more heavily searched."}
- {"id": "close-by-lower-bound", "statement": "Close an unproven J120 instance whose JSON entry has upper_bound - lower_bound = 1 (12 such instances live) by a reproducible CP-SAT / OR-Tools proof that makespan = upper_bound - 1 is infeasible, with saved model, parameters and seed, repeatable by the skeptic in under 1 hour on this Mac; counts only after the verifier re-runs it."}
- {"id": "tie-2024-2026-bounds", "statement": "Checker-validated schedules attaining the current upper_bound on at least 10 distinct J120 instances whose upper_bound_date is in 2024 or later (45 such instances live: 27 Vanhoucke-Coelho 2024, 1 Goncharov 2024, 17 Goncharov 2026); non-trivial because PSPLIB publishes only makespans for heuristic bounds, so these schedules cannot be downloaded."}

## Verification

Instance archive: https://www.om-db.wi.tum.de/psplib/download_dataset.php?set=j120&mode=sm&format=zip (600 .sm files). Bounds: download_merged.php?set=j120&mode=sm (JSON with keys instance_set, meta, summary, solutions[]) and the HRS/LB text files from download_solution.php?set=j120&mode=sm&type=hrs|lb. Python checker builds the resource-usage profile from the start times and compares against capacities period by period for all four resources, checks all precedences, and reports the sink finish time. Seconds. Re-fetch the JSON and HRS file with plain curl.

## Angles

- CP-SAT with interval variables and cumulative constraints, 10 workers, hours per instance, hinted by a good GA/SGS schedule; lazy-clause-generation CP produced most J120 UB improvements of the 2010s and 17 UBs still moved in 2026, so a long CP-SAT run on the never-improved-since-1998 instances is a real shot.
- Hybrid GA / iterated forward-backward improvement with activity-list representation and massive restarts (the Vanhoucke-Coelho 2024 method family); target instances whose UB is from 1997-1998 (231 of 600) with high network complexity and tight resources (parameter sets 6-10, 16-20, 26-30 etc., where RS is small).
- LNS over the critical path: fix all activities outside a time window, re-solve the window exactly with CP-SAT, slide the window.
- Use the 12 gap-1 instances for the closing partial win: CP-SAT with energetic reasoning and precedence-based symmetry breaking at makespan = UB-1.

## Pitfalls

- Makespan definition: finish time of the sink (dummy activity n+2) with dummies of zero duration; off-by-one from counting periods [t, t+1) incorrectly produces false 1-unit 'improvements'.
- Resource check must be per period over the whole horizon for all 4 renewable resources, not a per-activity or average check; precedence is finish-to-start with no lags in the single-mode .sm format.
- Only instances with is_proven_optimal = false count; 416 instances have no lower_bound key at all, so do not filter on LB < UB. Beating a proven-optimal UB is impossible and signals a checker bug.
- Use PSPLIB's own j120 .sm files (download_dataset.php), not regenerated ProGen instances with the same names from other sites; parameters differ.
- Re-fetch the merged JSON and HRS file immediately before claiming; uploads were re-enabled in May 2026 and 17 bounds landed in May-Aug 2026 without a news post. upper_bound_date formats differ ('Mon Sep 23 11:12:00 2024' vs '[2026-05-17 13:37:56]'); do not rely on date parsing.

## Sources

- https://www.om-db.wi.tum.de/psplib/getdata.php?mode=sm
- https://www.om-db.wi.tum.de/psplib/download_merged.php?set=j120&mode=sm
- https://www.om-db.wi.tum.de/psplib/download_merged.php?set=j60&mode=sm
- https://www.om-db.wi.tum.de/psplib/download_solution.php?set=j120&mode=sm&type=hrs
- https://www.om-db.wi.tum.de/psplib/download_solution.php?set=j120&mode=sm&type=lb
- https://www.om-db.wi.tum.de/psplib/download_dataset.php?set=j120&mode=sm&format=zip
- https://www.om-db.wi.tum.de/psplib/format.php
- https://www.om-db.wi.tum.de/psplib/latenews.php
- Status source: https://www.om-db.wi.tum.de/psplib/getdata.php?mode=sm

## Citations

- [Problem page](../../../../.raw/V3R1T4S/known-unknowns/optimization-benchmarks/psplib-j120-rcpsp-upper-bounds.md)
- [Bank entry](../../../../.raw/V3R1T4S/bank/targets.json) (id `psplib-j120-rcpsp-upper-bounds`, commit `7dd4480`)

## Related Nodes

- [[V3R1T4S Optimization benchmarks]]
- [[V3R1T4S]]
