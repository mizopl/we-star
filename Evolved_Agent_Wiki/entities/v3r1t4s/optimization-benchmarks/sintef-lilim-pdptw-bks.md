---
id: v3r1t4s-sintef-lilim-pdptw-bks
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
tractability: 2.5
compute: "laptop-hours"
disclosure: open
status_checked: "2026-10-08"
---
# SINTEF Li & Lim PDPTW benchmark: hierarchically beat a best-known solution on a 600/800/1000-task instance

# Overview

> Bank id `sintef-lilim-pdptw-bks` · harvest · tractability 2.5 · laptop-hours · disclosure **open**
> Bank says open as of 2026-10-08. Statuses go stale — re-check the primary source before any work.

## Statement

SINTEF's Transportation Optimization Portal maintains the best known solutions for the Li & Lim pickup-and-delivery-with-time-windows benchmark with a hierarchical objective: minimize vehicles, then total distance (double precision, reported to 2 decimals); detailed solution files checked by SINTEF's own checker are linked for every entry. Live on 2026-10-08 the 600/800/1000-task tables (58 real instances per size at 1000: lrc2_10_8 and lrc2_10_9 were never defined by Li & Lim and have no instance file) are dominated by entries from 2019-2021 (SCR, HW, SB) and Jan 2024 (NVIDIA), i.e. far fewer contributors than VRPTW, and none of the entries carries an optimality mark except a few 2003 '*' rows. Find a feasible solution that is hierarchically better (fewer vehicles, or equal vehicles and strictly smaller distance) than the listed BKS for any 600, 800 or 1000-task instance.

## Success criterion

A solution file in SINTEF's posted format ('Route k : id id ...' lines, task ids as in the instance file, depot = 0) for one Li & Lim instance with 600, 800 or 1000 tasks, such that a standalone checker written from the instance format (first line 'vehicles capacity speed'; then one line per node: id x y demand ready due service pickup-partner delivery-partner, with the depot as node 0) that (a) verifies every task served exactly once, (b) verifies each pickup and its delivery are in the same route with the pickup first, (c) verifies the running load never exceeds capacity and never goes negative along each route, (d) verifies time windows with double-precision Euclidean travel times, arrival = max(departure_prev + d, ready) <= due at every task and return to the depot by its due time, service time added after arrival, and (e) computes total distance in double precision, reports either strictly fewer vehicles (routes) than the table entry, or the same number of vehicles and a distance that is strictly smaller than the listed value by at least 0.01 after rounding to 2 decimals, where the table entry is the one on https://www.sintef.no/projectweb/top/pdptw/li-lim-benchmark/<600|800|1000>-customers/ re-fetched live immediately before claiming. The checker must first reproduce the posted BKS solution file's vehicle count and distance for that instance (e.g. lc1_10_2 file -> 94 / 44548.51, verified by the vetter 2026-10-08). The solution file, checker, instance file (sha256 from the SINTEF zip) and page snapshot are saved together. Nothing is submitted to SINTEF; the write-up goes to the human.

## Partial wins

- {"id": "pdptw-400-improve", "statement": "Hierarchical improvement, by the identical checker and re-fetch rule, on any 400-task instance at https://www.sintef.no/projectweb/top/pdptw/li-lim-benchmark/400-customers/ (instances from pdp_400.zip); counted as partial because the smaller instances have been searched more exhaustively."}
- {"id": "pdptw-200-improve", "statement": "Hierarchical improvement, by the identical checker and re-fetch rule, on any 200-task instance at https://www.sintef.no/projectweb/top/pdptw/li-lim-benchmark/200-customers/ that is not marked optimal ('*') in its row (instances from pdp_200.zip)."}
- {"id": "equal-vehicles-tie-new-structure", "statement": "A checker-validated solution for a 1000-task instance with the BKS vehicle count and a distance within 0.01 of the listed value whose undirected edge set differs from the posted BKS solution file in at least 10% of edges (edge-set comparison by the same checker); an alternative optimum-candidate, independently checkable from the two files."}

## Verification

Instances: https://www.sintef.no/contentassets/1338af68996841d3922bc8e87adc430c/pdptw1000.zip (58 files, LC1_10_1.txt ...), pdptw800.zip, pdp_600.zip, pdp_400.zip, pdp_200.zip, all linked from https://www.sintef.no/projectweb/top/pdptw/li-lim-benchmark/ (pdp_1000.zip is the same 58 instances). Posted BKS solution files are linked from each table row (e.g. https://www.sintef.no/contentassets/4787adf42512493986a16420bb6d1ca9/lc1_10_2.94_44548.51.txt). The skeptic runs the Python checker on the posted file (must reproduce vehicles and distance to 2 decimals and report zero violations), then on the claimed file. Minutes. Re-fetch the size page with plain curl and parse the instance's <tr>.

## Angles

- Adaptive large neighbourhood search with pair-aware removal/insertion (Ropke-Pisinger style) plus route-minimisation (ejection chains / squeeze), seeded from the posted BKS and run for hours with many seeds on 10 cores; most 2019-2021 entries came from exactly such methods with more wall time.
- Equal-vehicle distance polishing: fix the route set, optimise 2-3 neighbouring routes exactly with a CP-SAT model with precedence and time windows; any strict improvement is a strict global improvement.
- Target instances whose entry is oldest (2019 SB / 2019 SCR rows) or with high vehicle counts relative to a capacity-based lower bound (sum of demands / capacity), where vehicle reduction may be possible.
- Reuse VRPTW machinery: a PDPTW solution with pickup-before-delivery is a VRPTW solution with extra precedence constraints, so HGS-style crossover with repair is applicable.

## Pitfalls

- Hierarchical objective: a shorter-distance solution using one more vehicle is worse, not better; and a solution with fewer vehicles must still be feasible.
- Precedence and pairing: pickup and delivery must be in the same route with pickup first; load must be checked along the route (it rises and falls), not as a route total.
- Rounding: the table shows 2 decimals; a difference below 0.01 is not a win; reproduce the posted BKS file's value first.
- Instance size: Li & Lim '1000-task' instances have slightly more than the nominal number of tasks (e.g. LC1_10_2 has 1046); use the file's actual task list and the depot's time window / capacity from the file.
- lrc2_10_8 and lrc2_10_9 do not exist (no instance file; SINTEF says Li & Lim never supplied them). A 'first solution' for them is impossible and must never be counted.
- Dates in the table are free-form ('19-Dec-21', '19-Des-21', '2001'); do not parse dates to decide openness, use only the vehicles/distance cells.

## Sources

- https://www.sintef.no/projectweb/top/pdptw/li-lim-benchmark/
- https://www.sintef.no/projectweb/top/pdptw/li-lim-benchmark/1000-customers/
- https://www.sintef.no/projectweb/top/pdptw/li-lim-benchmark/800-customers/
- https://www.sintef.no/projectweb/top/pdptw/li-lim-benchmark/600-customers/
- https://www.sintef.no/projectweb/top/pdptw/li-lim-benchmark/400-customers/
- https://www.sintef.no/projectweb/top/pdptw/li-lim-benchmark/200-customers/
- https://www.sintef.no/contentassets/1338af68996841d3922bc8e87adc430c/pdptw1000.zip
- https://www.sintef.no/contentassets/1338af68996841d3922bc8e87adc430c/pdptw800.zip
- https://www.sintef.no/contentassets/1338af68996841d3922bc8e87adc430c/pdp_600.zip
- https://www.sintef.no/contentassets/1338af68996841d3922bc8e87adc430c/pdp_400.zip
- https://www.sintef.no/contentassets/4787adf42512493986a16420bb6d1ca9/lc1_10_2.94_44548.51.txt
- Status source: https://www.sintef.no/projectweb/top/pdptw/li-lim-benchmark/

## Citations

- [Problem page](../../../../.raw/V3R1T4S/known-unknowns/optimization-benchmarks/sintef-lilim-pdptw-bks.md)
- [Bank entry](../../../../.raw/V3R1T4S/bank/targets.json) (id `sintef-lilim-pdptw-bks`, commit `7dd4480`)

## Related Nodes

- [[V3R1T4S Optimization benchmarks]]
- [[V3R1T4S]]
