---
id: v3r1t4s-packomania-cci-equal-circles-in-circle
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
# Packomania: equal circles in a circle (cci), beat a per-N record radius

# Overview

> Bank id `packomania-cci-equal-circles-in-circle` · harvest · tractability 2.5 · laptop-hours · disclosure **open**
> Bank says open as of 2026-10-08. Statuses go stale — re-check the primary source before any work.

## Statement

Packomania's 'circles in a circle' table (cci) lists the best known radius r(N) of N equal circles packed in the unit circle for every N = 1..2600 plus selected larger N up to 5000 (2735 rows). Only N <= 13 and N = 19 are proven; everything else is a putative record. Last table update 25-Dec-2024 (Basurto/Gurin/Odriozola/Specht); earlier waves by Lai-Hao et al. (2023-2024) and Zhou-He-Zheng-Li (2023). The cci category does NOT appear in Packomania's pending-requests list of 2026-10-08, so the live table is the actual frontier for this container. Per-N values are machine-readable (txt/radius.txt, 30 decimals) and per-N coordinates are at cci/txt/cci<N>.txt (30 decimals).

## Success criterion

Success means a file of N centers (x_i, y_i) for one N listed in https://packomania.com/cci/txt/radius.txt such that the FEASIBLE radius r* := min( min_{i<j} |c_i - c_j| / 2, 1 - max_i |c_i| ), computed in mpmath at 50 digits directly from the submitted coordinates (no tolerance), is STRICTLY GREATER (direction: max) than the 30-decimal radius for that N re-fetched live immediately before claiming, by at least 1e-11, AND the configuration is not isometric to the posted cci<N>.txt one (sorted distance multisets differ), AND N does not appear in a History-of-updates line on the live cci.html newer than the one the scout fetched. QUEUE RULE (Packomania, checked 2026-10-08): the N must NOT lie inside any range listed for this category on https://packomania.com/pending-requests.html re-fetched at verification time; a value that is already in Packomania's queue does not count as ours. The 26-Sep-2026 'Moki & Julio *many* 4666 candidates' bundle is category-unspecified and cannot be resolved; the verdict must state this caveat and the N must be re-checked against the live table once that bundle disappears from the pending list. Packomania coordinate files are CENTERED (container centre at the origin: circle/sphere radius 1, square side 1 in [-1/2,1/2]^2, cube edge 1 in [-1/2,1/2]^3). No submission (email) is ever made; the claim is for the verified construction only.

## Partial wins

- {"id": "p1", "statement": "A configuration for some N in 1..2600 whose feasible radius r* equals the live table value to within 1e-11 but is certified non-isometric to the posted cci<N>.txt (different sorted distance multiset AND different contact graph, mpmath at 50 digits): a second optimum; not a record."}
- {"id": "p2", "statement": "A certified improvement for one of the gap values N > 2600 that the table lists (e.g. N = 4495, 5000), where the record is a lattice-like seed by Specht rather than an optimized packing."}
- {"id": "p3", "statement": "A certified improvement in the sibling regular-hexagon table chx (N <= 1261, 12-decimal https://packomania.com/chx/txt/radius.txt, so margin 1e-10) using the same mpmath feasible-radius rule, for an N not covered by any chx entry on the live pending-requests page (on 2026-10-08 chx N = 55 and 89 are queued)."}

## Verification

Independent checker (< 2 minutes): (1) curl the live https://packomania.com/cci/txt/radius.txt and parse row N. (2) Load the claimed centers; mpmath mp.dps=50; r* = min(min pair distance / 2, 1 - max |c_i|). (3) Assert r* - r_table >= 1e-11. (4) Download cci/txt/cci<N>.txt, recompute its r (must reproduce the table to 1e-20; parser sanity) and compare sorted distance multisets. (5) Re-fetch cci<N>.html, the cci.html History of updates and pending-requests.html; apply the queue rule. (6) Compare the contact graph against txt/contacts.txt.

## Angles

- Target N in 1000..2600: 2121 of 2735 rows are Specht's own (txt/author.txt), and the 2023-2024 Lai-Hao / Zhou-He / Basurto waves stopped near N = 1000, so the large-N rows have had far less competition. Use the N=1000..2600 coordinates as seeds and run perturb-and-repack (remove k circles, re-insert at largest holes, then re-jam).
- Hexagonal-core templates: take the chx (hexagon) hex-number packings, cut a circular window and relax the boundary layer; Cantrell's bound rows ('now meet Cantrell's bound') show where the frontier is already tight, so skip those N.
- Monotonic basin-hopping on a smooth penalty (sum of squared overlaps + squared protrusion) with L-BFGS, then an exact jamming step: solve the KKT system of the active contact set with mpmath to polish r to 30+ digits before comparing.
- Rattler exploitation: rows with many 'loose' circles (txt/loose.txt) have slack; move rattlers to open up a boundary contact and re-inflate.

## Pitfalls

- Direction and normalization: cci fixes the container radius at 1 and maximizes r; some literature reports the container radius for unit circles (ratio = 1/r). Compare r to r, never ratio to r.
- Double-precision 'records' of +1e-13 are noise. The 1e-11 margin on the mpmath feasible radius is mandatory; a configuration with tiny overlaps that 'rounds' to a record is a false positive.
- Stale-table trap: Packomania has a queue of over 5,000 pending candidates (2026-10-08). cci is not in the queue today, but re-check pending-requests.html and the per-N page immediately before claiming.
- Known-literature trap: an improvement may already be published (Lai-Hao 2024, Basurto 2024) but not yet uploaded; search arXiv for the N before claiming.
- Submitting to Packomania is by email (an outbound message on the human's behalf) and is asked not to happen in October 2026; claim the verified construction, not a submission.

## Sources

- https://packomania.com/cci/cci.html
- https://packomania.com/cci/txt/radius.txt
- https://packomania.com/cci/txt/author.txt
- https://packomania.com/cci/txt/cci100.txt
- https://packomania.com/cci/txt/cci_coords.tar.gz
- https://packomania.com/pending-requests.html
- https://packomania.com/hints.html
- Status source: https://packomania.com/cci/cci.html

## Citations

- [Problem page](../../../../.raw/V3R1T4S/known-unknowns/packings-physics/packomania-cci-equal-circles-in-circle.md)
- [Bank entry](../../../../.raw/V3R1T4S/bank/targets.json) (id `packomania-cci-equal-circles-in-circle`, commit `7dd4480`)

## Related Nodes

- [[V3R1T4S Packings and physics]]
- [[V3R1T4S]]
