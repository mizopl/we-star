---
id: v3r1t4s-friedman-packing-records
type: entity
tags: [v3r1t4s, v3r1t4s/record-tables, kind/harvest]
inbound_links: 1
confidence: 0.8
last_ingested_sources: [".raw/V3R1T4S/bank/targets.json@7dd4480"]
status: "open"
priority: ""
notes: ""
category: record-tables
kind: harvest
tractability: 2
compute: "laptop-hours"
disclosure: open
status_checked: "2026-10-03"
---
# Erich Friedman Packing Center: beat a listed packing

# Overview

> Bank id `friedman-packing-records` · harvest · tractability 2 · laptop-hours · disclosure **open**
> Bank says open as of 2026-10-03. Statuses go stale — re-check the primary source before any work.

## Statement

Friedman's Packing Center lists best known packings of n congruent shapes (circles, squares, triangles, pentagons, hexagons, octagons and others) into containers of various shapes. Mostly the goal is the smallest container for n unit shapes, or the largest shapes for a unit container. Several pages were updated in Sep-Oct 2026, including AI-team records (Numaro, Jul 2026, unequal-circle total-radius records) and new proofs (Vu-Le, Sep 2026). Submissions are by email, with sizes to 5 decimals; extensions of existing categories are accepted up to n=50. Many categories show updates dated 30 Sep - 3 Oct 2026, so multiple agents sweep the pages daily. Submission is by email, which is an outbound message on the human's behalf and requires explicit permission from the human.

## Success criterion

Success means explicit placements (centers plus rotation angles) for n shapes that meet all of the following. (1) Pairwise interiors are disjoint and every shape lies inside the container, certified rigorously by interval arithmetic or exact rational/algebraic computation. (2) The objective is STRICTLY BETTER, in the page's own direction (smaller container, or larger shape/total radius), than the value on the specific live Friedman page re-fetched immediately before verification, by at least 1e-5 at Friedman's 5-decimal precision. (3) The category and n are listed on the page, or n <= 50 for an extension of an existing category. The claim is for the verified construction; emailing Friedman needs explicit permission from the human.

## Partial wins

- {"id": "p1", "statement": "A Packomania record: a circles-in-square or circles-in-circle packing, rigorously certified, whose objective strictly beats the live Packomania value for that n at its listed precision."}
- {"id": "p2", "statement": "An EinsteinArena sum-of-radii record: a circle packing for one of the EinsteinArena AlphaEvolve-style sum-of-radii problems, with containment and non-overlap certified in interval or exact arithmetic, whose exactly computed score strictly beats the live arena leaderboard best."}

## Verification

Use an independent checker. Represent polygons by exact vertices after applying the rotation with rational approximations to cos/sin, or bound them with interval arithmetic. Test pairwise overlap with the separating axis theorem in interval arithmetic, requiring positive separation or exact touching certified. Check containment of every vertex (and for circles, the center distance to each container edge >= r). Compute the objective and compare with the page value.

## Angles

- Avoid circles-in-squares and circles-in-circles (Packomania-saturated). Target odd shape/container pairs (pentagons in triangles, octagons in squares, triangles in pentagons) where the record is an old hand construction.
- Use penalty-method optimization with a contracting container (minimize container scale plus a squared overlap penalty from SAT-based penetration depth), with L-BFGS and random restarts across 10 cores.
- Use a 'jamming plus rattler removal' pipeline: compress a random packing (Lubachevsky-Stillinger event-driven for circles, a rigid-body MD analogue for polygons), then optimize the rotation angles.
- Transfer lattice cuts. Cut good periodic packings of the shape with the container and locally repair boundary pieces.

## Pitfalls

- Comparing in the wrong direction. Some pages minimize container side, others maximize total radius or perimeter.
- Numerical 'touching' that is actually a tiny overlap. Require rigorous certification.
- Circle packing pages are heavily optimized already. The AlphaEvolve sum-of-radii benchmarks are separate EinsteinArena problems.
- Pages are being updated daily (Sep 30 - Oct 3 2026), so re-fetch the specific page immediately before claiming.
- Submitting to Friedman is an email on the human's behalf and needs explicit permission. Claim the verified construction, not the submission.

## Sources

- https://erich-friedman.github.io/packing/
- https://erich-friedman.github.io/packing/submit.html
- Status source: https://erich-friedman.github.io/packing/

## Citations

- [Problem page](../../../../.raw/V3R1T4S/known-unknowns/record-tables/friedman-packing-records.md)
- [Bank entry](../../../../.raw/V3R1T4S/bank/targets.json) (id `friedman-packing-records`, commit `7dd4480`)

## Related Nodes

- [[V3R1T4S Record tables]]
- [[V3R1T4S]]
