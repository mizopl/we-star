---
id: v3r1t4s-cvrplib-x-xl-xxl-bks
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
# CVRPLIB: beat a best-known solution on an open X, XL or Arnold-XXL CVRP instance

# Overview

> Bank id `cvrplib-x-xl-xxl-bks` · harvest · tractability 2.5 · laptop-hours · disclosure **open**
> Bank says open as of 2026-10-08. Statuses go stale — re-check the primary source before any work.

## Statement

CVRPLIB (galgos.inf.puc-rio.br/cvrplib) lists, for every CVRP instance, the best known upper bound (UB) and whether it is proven optimal (Opt column). Live on 2026-10-08: 39 of the 100 Uchoa X instances are Opt = no, all 100 XL instances (XL-n1048-k237 .. XL-n10001-k1570, Queiroga et al. 2026 challenge set) are Opt = no, and all 10 Arnold-Gendreau-Sorensen XXL instances (Leuven1/2, Antwerp1/2, Ghent1/2, Brussels1/2, Flanders1/2; 3,000-30,000 customers) are Opt = no. The Updates page shows BKSs still falling in Sept 2026, often by a single unit (XL-n7193-k1683 2,958,155 -> 2,958,154 on Sept 23; Antwerp1 477,261 -> 477,260 on Sept 12; X-n536-k96, X-n716-k35, X-n979-k58 on Sept 20; 70 XL instances on Sept 11). Find a feasible solution with total cost strictly below the listed UB for any instance whose Opt column reads 'no'.

## Success criterion

A solution file in CVRPLIB format ('Route #k: c1 c2 ...' lines with 0-based customer ids, customer c = node c+1 of the .vrp NODE_COORD_SECTION, node 1 = depot, each route implicitly starts and ends at the depot; number of routes unrestricted) for one instance whose Opt column reads 'no' in the All Instances table at https://galgos.inf.puc-rio.br/cvrplib/index.php/en/instances (plain curl -L; the table is one HTML <tr> per instance with columns Instance, |C|, |K|, Q, UB, Opt), such that a standalone checker written from the TSPLIB/CVRPLIB format definition that (a) parses the .vrp file (NODE_COORD_SECTION, DEMAND_SECTION, CAPACITY), (b) verifies every customer 2..n appears exactly once across all routes, (c) verifies every route load <= CAPACITY, and (d) sums EUC_2D edge lengths each rounded to the nearest integer (TSPLIB nint, int(d+0.5)) over depot->c1->...->ck->depot, reports an integer total strictly less than the UB shown for that instance in the All Instances table AND consistent with the Updates log at https://galgos.inf.puc-rio.br/cvrplib/index.php/en/updates, both re-fetched live immediately before claiming. Before any claim the same checker must reproduce the posted BKS file costs exactly: X-n1001-k43 (instance id 257) -> 72346, Antwerp1 (id 258) -> 477260, XL-n9571-k55 (id 377) -> 106342 (all three verified by the vetter on 2026-10-08). Instance and BKS files: https://galgos.inf.puc-rio.br/cvrplib/index.php/en/download/instance/<id> and .../download/bks/<id>; ids are in the table HTML (href download/instance/<id>). The solution file, the checker, and the fetched table snapshot are saved together. Nothing is submitted to CVRPLIB by the agent; the write-up goes to the human.

## Partial wins

- {"id": "x-open-tie-new-structure", "statement": "A solution for an open X instance (Opt = no) whose checker cost equals the live UB exactly but whose undirected edge set differs from the posted BKS file's edge set in at least 10% of edges (edge-set comparison by the same checker); an alternative optimum-candidate, independently checkable from the two files."}
- {"id": "xl-tie-new-structure", "statement": "Same as above for any XL instance with n >= 5,000: checker cost equal to the live UB with >= 10% edge-set difference from the posted BKS file. (A plain tie is not a partial win because the BKS files are downloadable.)"}
- {"id": "xxl-improve-any", "statement": "Strict UB improvement on any of the 10 Arnold-Gendreau-Sorensen XXL instances (Leuven1/2, Antwerp1/2, Ghent1/2, Brussels1/2, Flanders1/2), same checker and same re-fetch rule; recorded separately because these are the least saturated (last moved Sept 12 2026 by a single submitter, by 1 unit on Antwerp1)."}

## Verification

Skeptic downloads the .vrp via https://galgos.inf.puc-rio.br/cvrplib/index.php/en/download/instance/<id> and the posted BKS via .../download/bks/<id>, runs the standalone Python checker (nint per edge, 0-based customers, depot = node 1, load <= CAPACITY, every customer exactly once) on the posted BKS first: it must reproduce the table UB exactly (257 -> 72346, 258 -> 477260, 377 -> 106342). Then runs it on the claimed solution file: feasible and strictly smaller integer cost. Re-fetches https://galgos.inf.puc-rio.br/cvrplib/index.php/en/instances with plain curl -L and parses the instance's <tr> (UB cell like '$72{,}346.00$', Opt cell 'yes'/'no'). Minutes on any machine. Optionally also pastes into the site's checker page (https://galgos.inf.puc-rio.br/cvrplib/index.php/en/bks_challenge/checker); that is not required and nothing is submitted.

## Angles

- Run open-source HGS-CVRP (Vidal 2022, C++) and FILO2 (Accorsi & Vigo, built for 10k+ customers) with long time limits and many seeds on the XXL and largest XL instances; seed from the posted BKS and apply SWAP*/relocate/2-opt* polishing with ruin-and-recreate restarts.
- Target instances whose BKS moved most recently by a single unit from a single submitter (Antwerp1, Flanders1/2, XL-n7193-k1683) since one-unit movement signals slack; also instances with very long routes (large Q) where per-route TSP optimality via LKH-3 plus inter-route exchanges can shave units.
- Decompose XL/XXL instances geographically (barycenter clustering / route-based partitions), optimize subproblems with HGS to near-optimality, then re-merge and run global local search.
- Exact polishing: fix most routes, extract 3-5 neighboring routes, solve the resulting small CVRP exactly (CP-SAT or a set-partitioning MIP over enumerated routes); any strict improvement of the subproblem is a strict global improvement.
- Exploit the integer-rounded objective: search for moves whose unrounded delta is slightly positive but rounded delta is negative (rounding slack), which continuous-metric local search ignores.

## Pitfalls

- Distance convention: X, XL and AGS instances use EUC_2D with nearest-integer rounding per edge; unrounded X-n1001-k43 BKS is 72386.96, rounded is 72346. The checker must reproduce 72346 / 477260 / 106342 on the posted files before any claim.
- Customer ids: solution files are 0-based (depot excluded) while .vrp nodes are 1-based with node 1 = depot; an off-by-one makes an infeasible route look feasible.
- Fleet size: the k in X-nNNN-kK and XL-nNNN-kK is the fleet used by the BKS, not a hard limit in the CVRPLIB convention; AGS rows show '—' for |K|. The checker does not restrict route count, but report the route count alongside the cost.
- The table value must be re-fetched at claim time: X, XL and XXL UBs changed several times in Sept 2026; a 'win' against a value cached at scout time may already be stale.
- Do not count XML100 instances (all optimal), instances with Opt = 'yes' (61 X instances), or the XLTW VRPTW set (not released) as targets.
- The /index.php/en/ root URL redirects (301) to /index.php/en/instances; always use the /instances URL and plain curl -L.

## Sources

- https://galgos.inf.puc-rio.br/cvrplib/index.php/en/instances
- https://galgos.inf.puc-rio.br/cvrplib/index.php/en/updates
- https://galgos.inf.puc-rio.br/cvrplib/index.php/en/download/instance/257
- https://galgos.inf.puc-rio.br/cvrplib/index.php/en/download/bks/257
- https://galgos.inf.puc-rio.br/cvrplib/index.php/en/download/instance/258
- https://galgos.inf.puc-rio.br/cvrplib/index.php/en/download/bks/258
- https://galgos.inf.puc-rio.br/cvrplib/index.php/en/download/instance/377
- https://galgos.inf.puc-rio.br/cvrplib/index.php/en/download/bks/377
- https://galgos.inf.puc-rio.br/cvrplib/index.php/en/bks_challenge/overview
- https://galgos.inf.puc-rio.br/cvrplib/index.php/en/bks_challenge/score/instances
- Status source: https://galgos.inf.puc-rio.br/cvrplib/index.php/en/instances

## Citations

- [Problem page](../../../../.raw/V3R1T4S/known-unknowns/optimization-benchmarks/cvrplib-x-xl-xxl-bks.md)
- [Bank entry](../../../../.raw/V3R1T4S/bank/targets.json) (id `cvrplib-x-xl-xxl-bks`, commit `7dd4480`)

## Related Nodes

- [[V3R1T4S Optimization benchmarks]]
- [[V3R1T4S]]
