---
id: v3r1t4s-thomson-problem-live-tables
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
# Thomson problem: lower the best known Coulomb energy for some N (Deeter / Cambridge Cluster Database / Riesz s=1 tables)

# Overview

> Bank id `thomson-problem-live-tables` · harvest · tractability 2.5 · laptop-hours · disclosure **open**
> Bank says open as of 2026-10-08. Statuses go stale — re-check the primary source before any work.

## Statement

Minimize E(N) = sum_{i<j} 1/|x_i - x_j| for N unit-charge points on the unit sphere. Live tables: (1) Wayne Deeter's table (deetour.net/oppp/thomson/, last modified 2026-10-05) with 13-significant-digit energies and point files e.<N>.txt (12 decimals) for N = 4..523, which already corrects several Cambridge entries (e.g. N = 263, 360, 377, 380-382); (2) the Cambridge Cluster Database Thomson tables (Wales-Ulker 2006, N = 10..400 plus magic N up to 972; Wales-McKay-Altschuler 2009, N = 400..4352 step 10 plus magic N) with 7-decimal energies and xyz files (9 significant digits); (3) the CCD 'Riesz energy database' s = 1 (53 configurations, N = 512..9913, updated 2026-09-20, 18-digit point files); (4) Wikipedia's table (N <= 470); (5) EinsteinArena's N = 282 leaderboard (37147.294418, AlphaEvolve = Deeter's value). Tables disagree in places (CCD Riesz N = 512: 124673.9055677 vs Deeter 124673.8412508), so the record for an N is the MINIMUM over all live tables. Lai-Hao (ESWA 2024) improved N = 360; 2025-2026 arXiv work (2506.08398, 2512.12416) maps landscapes without new minima. Only N <= 6 and N = 12 are proven (a 2026 claim for N = 7 is unverified).

## Success criterion

Success means N points on the unit sphere (coordinates to >= 20 digits) for some N <= 1500 listed in at least one live table, such that E* computed in mpmath at 30 digits from the normalized coordinates is STRICTLY LOWER (direction: min) than the minimum energy for that N over ALL of: Deeter's table (https://deetour.net/oppp/thomson/, N = 4..523), CCD Thomson/table.html, CCD Thomson2/table.html, the CCD Riesz s=1 table (site/s_1/index.html), the Wikipedia table and (for N = 282) EinsteinArena, each re-fetched live immediately before claiming, by at least 1e-6 in absolute energy, AND the configuration is a certified strict local minimum (mpmath tangent-space Newton to gradient norm < 1e-20, all 2N-3 non-rotational tangent Hessian eigenvalues > 0), AND it is a different basin from every posted table configuration for that N: polishing each table's own point file (Deeter e.<N>.txt, CCD xyz/<N>.xyz, Riesz dat/points_<N>_1.dat) with the same routine must give an energy higher than E* by >= 1e-6. N > 1500 (Riesz rows up to 9913) cannot be Hessian-certified in under an hour and is partial win p3 only.

## Partial wins

- {"id": "p1", "statement": "A table-integrity finding: an N where a live table's posted energy is not reproduced by its own posted coordinates after mpmath polishing by more than 1e-6 (Deeter documents such cases for CCD N = 263, 377, 380, 381), reported with both energies to 12 digits."}
- {"id": "p2", "statement": "A certified improvement for the logarithmic potential (sum of -log|x_i - x_j|) or Riesz s = 2 for some N <= 500 against the Lai-Hao 2024 ESWA values, if the scout can fetch that paper's table; same local-minimum and distinct-basin rules."}
- {"id": "p3", "statement": "A certified improvement in the CCD Riesz s = 1 table (N = 512..9913) for N > 1500 or beating only that table: same mpmath energy, gradient norm < 1e-15 and a Lanczos/ARPACK smallest tangent-Hessian eigenvalue > 0 in double precision instead of the full eigendecomposition; reported as an improvement of that table only."}

## Verification

Checker (< 10 minutes for N <= 1500): (1) curl all live tables and take the minimum for N. (2) Normalize the claimed points in mpmath (mp.dps = 30), compute E* exactly. (3) Tangent-space Newton in mpmath until gradient norm < 1e-20; confirm E* changes by < 1e-12; build the 3N x 3N Hessian in double, project out rotations, assert 2N-3 positive eigenvalues. (4) Download every table's point file for N and polish identically; assert each E_table_polished - E* >= 1e-6. (5) Assert E_table_min - E* >= 1e-6. Report all energies to 12 digits.

## Angles

- Attack N = 400..523 where Deeter's table is newest and CCD only has every 10th N: use Deeter's own method (basin hopping with symmetric seeds from his 'roundest polyhedra' lists) plus Lai-Hao-style population crossover of Voronoi-defect patterns (scars). Deeter himself found new minima at 360 and 382 this way.
- Defect-motif engineering: for N near icosadeltahedral magic numbers (10h^2+10hk+10k^2+2) move the 12 disclinations into scar chains and re-relax; N = 520..523 and the Riesz rows 532..548 are far from magic and likely under-explored.
- CCD Riesz s = 1 rows for N = 512..972 duplicate Deeter/CCD Thomson values in several cases but are HIGHER for N = 512 (124673.9056 vs 124673.8413); check every N in both tables and polish the Riesz point files, since under-converged rows are easy targets for p3.
- Use the 2025 landscape result (number of local minima grows exponentially faster than thought) to justify massive restarts: 10 cores x 10^4 L-BFGS descents per N for N = 150..300 with symmetry-seeded starts (C2, C3, D2, D3, D5 orbits), then mpmath polish.

## Pitfalls

- Under-converged table values: a posted energy can exceed the true minimum of its own basin by 1e-7..1e-4 (Deeter's audit of CCD). Polishing the posted coordinates and getting a lower number is NOT a new minimum; the distinct-basin test is mandatory.
- Precision: CCD tables carry 7 decimals and xyz files 9 significant digits; always compute from coordinates in mpmath, never trust a printed value to more digits than it has.
- Multiple tables: the record is the minimum over all live tables (Deeter, CCD x2, Riesz s=1, Wikipedia, EinsteinArena); beating only the CCD value is not a record.
- Saddle points masquerading as minima: an L-BFGS stop with gradient 1e-8 can be a saddle; require positive tangent Hessian.
- EinsteinArena shows a verifier-exploit leader on the sibling Tammes page; never take a leaderboard number without recomputing from coordinates.

## Sources

- https://deetour.net/oppp/thomson/
- https://deetour.net/oppp/thomson/e.282.txt
- https://www-wales.ch.cam.ac.uk/~wales/CCD/Thomson/table.html
- https://www-wales.ch.cam.ac.uk/~wales/CCD/Thomson2/table.html
- https://www-wales.ch.cam.ac.uk/~wales/CCD/Thomson/site/index.html
- https://www-wales.ch.cam.ac.uk/~wales/CCD/Thomson/site/s_1/index.html
- https://www-wales.ch.cam.ac.uk/~wales/CCD/Thomson/xyz/100.xyz
- https://www-wales.ch.cam.ac.uk/~wales/CCD/Thomson/site/s_1/dat/points_512_1.dat
- https://en.wikipedia.org/wiki/Thomson_problem
- https://einsteinarena.com/problems/thomson-problem
- https://arxiv.org/abs/2506.08398
- Status source: https://deetour.net/oppp/thomson/

## Citations

- [Problem page](../../../../.raw/V3R1T4S/known-unknowns/packings-physics/thomson-problem-live-tables.md)
- [Bank entry](../../../../.raw/V3R1T4S/bank/targets.json) (id `thomson-problem-live-tables`, commit `7dd4480`)

## Related Nodes

- [[V3R1T4S Packings and physics]]
- [[V3R1T4S]]
