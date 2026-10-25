---
id: v3r1t4s-packomania-csq-equal-circles-in-square
type: entity
tags: [v3r1t4s, v3r1t4s/packings-physics, kind/harvest]
inbound_links: 1
confidence: 0.8
last_ingested_sources: [".raw/V3R1T4S/bank/targets.json@7dd4480"]
status: "open"
priority: ""
notes: ""
category: packings-physics
kind: harvest
tractability: 2.5
compute: "laptop-hours"
disclosure: open
status_checked: "2026-10-08"
---
# Packomania: equal circles in a square (csq), beat a per-N record radius

# Overview

> Bank id `packomania-csq-equal-circles-in-square` · harvest · tractability 2.5 · laptop-hours · disclosure **open**
> Bank says open as of 2026-10-08. Statuses go stale — re-check the primary source before any work.

## Statement

Packomania's 'circles in a square' table (csq) lists the best known radius r(N) of N equal circles in the unit square for N = 1..1000 and selected N up to 10000 (3150 rows, 12-decimal radius.txt, per-N coordinates at csq/txt/csq<N>.txt). Proven optimal only for N <= 30 and a few special N (36 etc.). Last update 10-Sep-2026 (two candidates N = 3000 and 9996 by ZeroThesis); the big 2022 wave by Lai-Hao-Xiao-Glover improved ~250 values of N in 106..400. IMPORTANT: the pending-requests page (2026-10-08) lists 557 csq candidates in 401..1000 and 250 in 1015..9996 (Zeeshan Tariq, Sept 2026) that are not yet processed, so the live table for N > 400 is probably about to move.

## Success criterion

Success means N centers for one N listed in https://packomania.com/csq/txt/radius.txt such that the FEASIBLE radius r* := min( min_{i<j} |c_i - c_j| / 2, 1/2 - max_i max(|x_i|,|y_i|) ) for the centered unit square [-1/2,1/2]^2, computed in mpmath at 50 digits with no tolerance, is STRICTLY GREATER (direction: max) than the live 12-decimal txt/radius.txt value for that N re-fetched immediately before claiming, by at least 1e-10, AND the configuration is not isometric to the posted csq<N>.txt one (sorted distance multisets differ), AND N is outside every csq range on the live pending-requests page (on 2026-10-08: 401..1000 and 1015..9996 are queued, so only N <= 400 and N = 1001..1014 can be claimed until the queue is processed; queued N is partial win p1). QUEUE RULE (Packomania, checked 2026-10-08): the N must NOT lie inside any range listed for this category on https://packomania.com/pending-requests.html re-fetched at verification time; a value that is already in Packomania's queue does not count as ours. The 26-Sep-2026 'Moki & Julio *many* 4666 candidates' bundle is category-unspecified and cannot be resolved; the verdict must state this caveat and the N must be re-checked against the live table once that bundle disappears from the pending list. Packomania coordinate files are CENTERED (container centre at the origin: circle/sphere radius 1, square side 1 in [-1/2,1/2]^2, cube edge 1 in [-1/2,1/2]^3). No submission (email) is ever made; the claim is for the verified construction only.

## Partial wins

- {"id": "p1", "statement": "A certified improvement (same mpmath rule, margin 1e-10) for an N inside a csq pending-queue range: real but not novelty-safe; record the value and re-check against the live table when Packomania processes the queue."}
- {"id": "p2", "statement": "A certified improvement to a sibling 2D equal-circle Packomania table that exists live (csc semicircle, crt triangle, ccq circles-in-circle-quarter) for an N OUTSIDE every pending-queue range for that category (on 2026-10-08 csc 41..250, crt 54..299, ccq 57..600 are queued), same mpmath rule against that table's live txt/radius.txt with margin 1e-10 for 12-decimal files and 1e-11 for 30-decimal files."}
- {"id": "p3", "statement": "A second distinct optimal configuration for a proven-optimal N (N <= 30), i.e. equal r* to 1e-11 but non-isometric to the posted coordinates, verified by contact-graph non-isomorphism."}

## Verification

Checker (< 2 minutes): curl https://packomania.com/csq/txt/radius.txt live (tab-separated N, r), parse row N; load claimed centers; mpmath mp.dps=50; r* = min(half the minimum pairwise distance, 1/2 - max_i max(|x_i|,|y_i|)); assert r* - r_table >= 1e-10. Download csq/txt/csq<N>.txt, recompute its r (parser sanity) and compare sorted distance multisets. Re-fetch csq<N>.html, the csq.html History of updates and pending-requests.html; apply the queue rule. Report r* to 20 digits.

## Angles

- Work in 106..400 where the 2022 Lai-Hao wave set most rows: their algorithm was a single method; try a different family (event-driven Lubachevsky-Stillinger compression from random starts, then KKT polishing) and look for N where the table's contact count is low relative to 2N+1.
- Exploit density dips: txt/records.txt lists the density-record N (e.g. 188, 194, ...); the N just after a density-record often sits in a bad basin (e.g. a record packing minus circles, with freed rattlers). Attack N = record+1..record+3 with rattler-driven re-packing.
- Shifted-lattice families: for N near k^2 or k(k+1) try square/hexagonal hybrids with one or two skew rows, then optimize the skew angle continuously.
- Use the per-N coordinate files as seeds and run large-neighbourhood search: remove 5-10% of circles, re-insert at the largest empty circles (Voronoi vertices), re-jam, accept if r improves.

## Pitfalls

- Queue-stale table: 807 csq candidates are pending (N > 400). A 'record' for N in those ranges may already be in Specht's inbox; the criterion forces N <= 400 or an explicit queue check.
- 12-decimal table: an apparent improvement in the 12th decimal can be the table's own rounding (Packomania truncates to 12 decimals on csq); require the 1e-11 margin against the exact posted value and prefer re-deriving the table radius from the posted coordinates (csq<N>.txt) in mpmath.
- Coordinate convention: Packomania files are centered at the origin with side length 1 (coordinates in [-0.5, 0.5]); do not test containment against [0, 1] without shifting.
- Submission is by email and asked to pause in October 2026; do not count a submission as a claim.

## Sources

- https://packomania.com/csq/csq.html
- https://packomania.com/csq/txt/radius.txt
- https://packomania.com/csq/txt/records.txt
- https://packomania.com/csq/txt/author.txt
- https://packomania.com/csq/txt/csq100.txt
- https://packomania.com/csq/txt/csq_coords.tar.gz
- https://packomania.com/pending-requests.html
- https://arxiv.org/abs/2609.05093
- Status source: https://packomania.com/csq/csq.html

## Citations

- [Problem page](../../../../.raw/V3R1T4S/known-unknowns/packings-physics/packomania-csq-equal-circles-in-square.md)
- [Bank entry](../../../../.raw/V3R1T4S/bank/targets.json) (id `packomania-csq-equal-circles-in-square`, commit `7dd4480`)

## Related Nodes

- [[V3R1T4S Packings and physics]]
- [[V3R1T4S]]
