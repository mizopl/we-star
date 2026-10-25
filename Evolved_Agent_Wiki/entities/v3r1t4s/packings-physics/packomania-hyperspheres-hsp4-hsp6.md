---
id: v3r1t4s-packomania-hyperspheres-hsp4-hsp6
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
tractability: 3.5
compute: "laptop-hours"
disclosure: open
status_checked: "2026-10-08"
---
# Packomania: equal 4D/5D/6D hyperspheres in a hypersphere (hsp4, hsp5, hsp6), beat a per-N record radius

# Overview

> Bank id `packomania-hyperspheres-hsp4-hsp6` · harvest · tractability 3.5 · laptop-hours · disclosure **open**
> Bank says open as of 2026-10-08. Statuses go stale — re-check the primary source before any work.

## Statement

Packomania Section 4 lists the best known radius r(N) of N equal d-dimensional balls packed in the unit d-ball for d = 4 (N = 2..300), d = 5 (N = 2..300) and d = 6 (N = 2..259), with 12-decimal txt/radius.txt files and per-N coordinates inside txt/hsp<d>_coords.tar.gz (files hsp<d>-<N>.txt: first line radius, then N rows of d coordinates, 12 decimals). Last updates: hsp4 06-Jul-2025, hsp5 01-Aug-2025, hsp6 31-Jul-2025. Author files show these tables were built almost single-handedly by Specht (hsp4: 247/299 rows Specht, 30 Sloane-Hardin-Smith, 11 Mackay; hsp5: 263/299 Specht; hsp6: 258/258 Specht). None of hsp4/5/6 appears in the pending-requests list (2026-10-08), and no competing group has touched them, so these are the least-contested per-N packing tables on Packomania.

## Success criterion

Success means N centers in R^d (d in {4,5,6}) for one N listed in the live https://packomania.com/hsp<d>/txt/radius.txt such that the FEASIBLE radius r* := min( min_{i<j} |c_i - c_j| / 2, 1 - max_i |c_i| ) (unit container ball centred at the origin), computed in mpmath at 50 digits directly from the submitted coordinates with no tolerance, is STRICTLY GREATER (direction: max) than that file's 12-decimal value for N re-fetched live immediately before claiming, by at least 1e-10 (the table carries 12 decimals; 1e-10 is 200x its rounding), AND the configuration is not isometric to the posted hsp<d>-<N>.txt configuration (sorted pairwise-distance multisets differ by more than 1e-8 somewhere), AND (d, N) does not appear in a History-of-updates entry on the live hsp<d>.html newer than the one the scout fetched. QUEUE RULE (Packomania, checked 2026-10-08): the N must NOT lie inside any range listed for this category on https://packomania.com/pending-requests.html re-fetched at verification time; a value that is already in Packomania's queue does not count as ours. The 26-Sep-2026 'Moki & Julio *many* 4666 candidates' bundle is category-unspecified and cannot be resolved; the verdict must state this caveat and the N must be re-checked against the live table once that bundle disappears from the pending list. No submission (email) is ever made; the claim is for the verified construction only.

## Partial wins

- {"id": "p1", "statement": "A certified improvement for a row attributed to 'unknown' or 'A. L. Mackay' in txt/author.txt (hsp4), i.e. a row seeded from classical constructions rather than optimized."}
- {"id": "p2", "statement": "An extension row: a certified packing for N = 301..310 (d = 4 or 5) or N = 260..270 (d = 6) that beats the obvious baseline of (best r(N-1) packing plus one ball at the largest cavity, re-jammed), reported with r* to 20 digits; not a record, but new data for an N the table does not list."}
- {"id": "p3", "statement": "A certified contact-graph audit: for every listed N, re-derive r from the coordinates in the tarball and report any N where the posted coordinates do not achieve the posted 12-decimal radius (data-integrity finding)."}

## Verification

Checker (< 2 minutes): curl the live hsp<d>/txt/radius.txt and parse row N; load the claimed centers; mpmath mp.dps=50; r* = min(half the minimum pairwise distance, 1 - maximum norm); assert r* - r_table >= 1e-10. Download txt/hsp<d>_coords.tar.gz (all three exist, checked 2026-10-08) and read hsp<d>-<N>.txt; recompute its r the same way (parser sanity: must reproduce the table to 1e-11) and compare sorted distance multisets to rule out an isometric copy. Re-fetch hsp<d>.html (History of updates) and pending-requests.html and apply the queue rule. Report r* to 20 digits.

## Angles

- Single-author tables are the softest: run a completely different optimizer than Specht's (event-driven LS compression in d dimensions from random starts, 10 cores x hundreds of restarts per N) over all N = 50..300; expect many small gains in 12-digit tables.
- Lattice shells: in 4D the D4 lattice (24-cell kissing) and in 6D the E6 lattice give dense shell structures; take shells around a center, cut to N, and relax; compare with txt/records.txt (density-record N) to find N where the table is NOT already a lattice shell.
- Kissing-configuration seeds: a central ball with a 24-ball (4D) or 40-ball (5D) or 72-ball (6D) shell plus a partial second shell is a natural template for N near 25, 41, 73 and N near the second-shell completions; the table's density-record lists hint at which are already found.
- Large-neighbourhood search on the posted coordinates: delete the 5 balls with the largest free volume (compute via random probing), re-insert at the deepest holes, re-jam; polish the active-contact KKT system with mpmath.

## Pitfalls

- 12-decimal table: compare against the exact posted value with a 1e-11 margin; an improvement of 3e-12 is indistinguishable from the table's own rounding.
- Container convention: unit container ball (radius 1, centered at origin); the 'ratio' column is 1/r, not the objective.
- A new packing isometric to the posted one (rotated/reflected) with the same r is not a record; the checker compares distance multisets.
- Email submission needs explicit permission from the human and Packomania asks for no submissions in October 2026; claim the verified configuration only.
- Tables are 12-decimal: polishing the posted coordinates to high precision can gain up to ~1e-12 from rounding alone; that is why the margin is 1e-10 and the non-isometry test is mandatory.

## Sources

- https://packomania.com/hsp4/hsp4.html
- https://packomania.com/hsp4/txt/radius.txt
- https://packomania.com/hsp5/txt/radius.txt
- https://packomania.com/hsp6/txt/radius.txt
- https://packomania.com/hsp4/txt/author.txt
- https://packomania.com/hsp5/txt/author.txt
- https://packomania.com/hsp6/txt/author.txt
- https://packomania.com/hsp4/txt/hsp4_coords.tar.gz
- https://packomania.com/hsp5/txt/hsp5_coords.tar.gz
- https://packomania.com/hsp6/txt/hsp6_coords.tar.gz
- https://packomania.com/pending-requests.html
- Status source: https://packomania.com/hsp4/hsp4.html

## Citations

- [Problem page](../../../../.raw/V3R1T4S/known-unknowns/packings-physics/packomania-hyperspheres-hsp4-hsp6.md)
- [Bank entry](../../../../.raw/V3R1T4S/bank/targets.json) (id `packomania-hyperspheres-hsp4-hsp6`, commit `7dd4480`)

## Related Nodes

- [[V3R1T4S Packings and physics]]
- [[V3R1T4S]]
