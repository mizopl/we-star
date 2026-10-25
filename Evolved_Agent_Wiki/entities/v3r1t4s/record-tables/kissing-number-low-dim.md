---
id: v3r1t4s-kissing-number-low-dim
type: entity
tags: [v3r1t4s, v3r1t4s/record-tables, kind/moonshot]
inbound_links: 1
confidence: 0.8
last_ingested_sources: [".raw/V3R1T4S/bank/targets.json@7dd4480"]
status: "open"
priority: ""
notes: ""
category: record-tables
kind: moonshot
tractability: 1
compute: "laptop-hours"
disclosure: open
status_checked: "2026-10-03"
---
# Kissing number lower bounds in dimensions 9-23

# Overview

> Bank id `kissing-number-low-dim` · moonshot · tractability 1 · laptop-hours · disclosure **open**
> Bank says open as of 2026-10-03. Statuses go stale — re-check the primary source before any work.

## Statement

Find more unit spheres touching a central unit sphere without overlapping, i.e. a set of nonzero vectors of equal norm with pairwise angle >= 60 degrees, in dimensions 9-23. Cohn's table (2026): d9 306, d10 510, d11 604, d12 841, d13 1154, d14 1932, d15 2564, d16 4320, d17 5730, d18 7654, d19 11948, d20 19448, d21 29768, d22 49896, d23 93150. Attributions: d11 592 (Ganzhinov 2025) -> 593 (AlphaEvolve) -> 604 (Bianchi-Kwon-Pappu-Zou, arXiv:2606.10402, EinsteinArena, 'recently solved, certified'); d12 840 -> 841 (Takhanov-Assylbekov-Yun, arXiv:2606.18984); d14 1932 (Ganzhinov 2025); d19 11948 (Ho, arXiv:2603.10425). Sep 2026 work (arXiv:2609.35051, 2609.21591) only improved d >= 25.

## Success criterion

Success means K vectors in R^d (9 <= d <= 23) given exactly (integer/rational coordinates or exact algebraic numbers in a specified field), all with identical squared norm N and every pair with <x,y> <= N/2, verified in exact arithmetic, no two coinciding, with K STRICTLY GREATER (direction: max) than the lower bound for dimension d at https://cohn.mit.edu/kissing-numbers/ at verification time (and any newer arXiv claim). Floating-point configurations with tiny overlap loss do NOT qualify unless exactified.

## Partial wins

- {"id": "p1", "statement": "An exact kissing configuration in a dimension d >= 24 listed in Cohn's table, verified in exact arithmetic, with size strictly greater than the live table value for that d (several were moved in Sep 2026, so re-check)."}
- {"id": "p2", "statement": "A rigorous upper-bound improvement: an SDP/LP certificate verified in exact rational or interval arithmetic proving a kissing-number upper bound strictly below the live Cohn-table upper bound for some d in 9..23."}

## Verification

Use exact integer arithmetic. Scale the coordinates to integers, compute all Gram entries as Python ints, and assert the diagonal is constant and the off-diagonal entries are <= diag/2. For K ~ 600-12000, the Gram matrix is up to 1.4e8 entries, so use numpy int64 with overflow checks or chunked object arithmetic. Check that no two vectors coincide.

## Angles

- Start from the structure of the 604 d11 configuration (480 vectors from D11+ orbits plus extras) and apply analogous 'lattice orbit plus deep-hole insertion' in d13 and d14 from laminated lattices Lambda_13 and K_13.
- Use Ganzhinov's symmetric-search method: prescribe a large group (e.g. a subgroup of W(E8) x W(A_k)), so candidates are unions of orbits. Solve the max-clique of compatible orbits exactly.
- Project or slice the Leech lattice and Barnes-Wall configurations and look for antipodal-pair swaps that free room, certified exactly.
- Do continuous optimization with an energy term, then snap to a rational lattice (LLL on the scaled coordinates) to obtain an exact certificate.

## Pitfalls

- A near-zero overlap loss is not a proof. Exact certification is mandatory.
- Cohn's table is the source of truth, and d11/d12 moved in 2026.
- Vectors must have equal norm exactly, not only up to rounding.

## Sources

- https://cohn.mit.edu/kissing-numbers/
- https://einsteinarena.com/problems/kissing-number-d11
- https://arxiv.org/abs/2609.35051
- https://arxiv.org/abs/2606.10402
- https://arxiv.org/abs/2606.18984
- https://arxiv.org/abs/2603.10425
- Status source: https://cohn.mit.edu/kissing-numbers/

## Citations

- [Problem page](../../../../.raw/V3R1T4S/known-unknowns/record-tables/kissing-number-low-dim.md)
- [Bank entry](../../../../.raw/V3R1T4S/bank/targets.json) (id `kissing-number-low-dim`, commit `7dd4480`)

## Related Nodes

- [[V3R1T4S Record tables]]
- [[V3R1T4S]]
