---
id: v3r1t4s-ccd-glue-potential-al-pb-clusters
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
tractability: 2
compute: "laptop-hours"
disclosure: open
status_checked: "2026-10-15"
---
# Glue-potential aluminium (N <= 190) and lead (N <= 160) clusters: lower a putative global minimum in Doye's polytetrahedral tables

# Overview

> Bank id `ccd-glue-potential-al-pb-clusters` · harvest · tractability 2 · laptop-hours · disclosure **open**
> Bank says open as of 2026-10-15. Statuses go stale — re-check the primary source before any work.

## Statement

Jonathan Doye located putative global minima for clusters bound by the Ercolessi-Adams aluminium glue potential for N = 3..189 (J. Chem. Phys. 119, 1136, 2003; nearly all minima polytetrahedral, with ordered disclination networks like Frank-Kasper phases) and, with Shaun Hendy, for the Lim-Ong-Ercolessi lead glue potential for N = 3..160 (Eur. Phys. J. D 22, 99, 2003). Both tables are on the Cambridge Cluster Database with 6-decimal energies in eV and point files (all.tar), and invite improvements. Polytetrahedral landscapes are rough and multi-funnel, each table comes from one basin-hopping campaign, and no later systematic re-search of either table was found (searches 2026-10-15). Both glue potentials are tabulated spline functions: Ercolessi's original pages (fisica.uniud.it) do not respond (2026-10-15) but are archived in the Wayback Machine (2017 snapshots, HTTP 200), and OpenKIM carries several spline implementations of the Ercolessi-Adams Al potential. Checked live 2026-10-15: both table pages HTTP 200.

## Success criterion

Success means Cartesian coordinates for N atoms such that E* under the exact glue potential of that table (Al: Ercolessi-Adams 1994; Pb: Lim-Ong-Ercolessi 1992; calibrated first: the checker reproduces the posted energies of ten randomly chosen point files of that table to 1e-6 eV) is STRICTLY LOWER (direction: min) by at least 1e-4 eV than the table energy for (metal, N) re-fetched live immediately before claiming, AND than any published value for the same potential and N found by an arXiv / Google Scholar search for 'glue potential clusters' plus the metal; AND the structure is a certified local minimum: polish in float128 or mpmath (30 digits) to gradient norm < 1e-10 (reduced units of the table), then the 3N x 3N Hessian in double precision has exactly 6 near-zero modes (|lambda| < 1e-6) and no negative eigenvalue; AND polishing the posted structure for that N gives an energy at least 1e-4 eV higher (distinct basin).

## Partial wins

- {"id": "p1", "statement": "A reproducible open implementation of both glue potentials (from the archived Fortran sources) that reproduces every posted energy of both tables to 1e-6 eV, plus a list of any row that is not reproduced or that polishes lower by more than 1e-4 eV."}
- {"id": "p2", "statement": "A certified improvement for Al glue clusters at N in 190..250 against a fetchable published comparator for the same potential (DOI/arXiv plus table reference); a literature frontier, not a CCD record."}

## Verification

Checker (< 15 min): curl the live table; parse (N, energy); download all.tar; load the glue potential from the archived Ercolessi Fortran routines (Al cross-checked against OpenKIM EAM_ErcolessiAdams_1994_Al); E = sum_{i<j} phi(r_ij) + sum_i U(sum_{j!=i} rho(r_ij)); evaluate the claim in float64 and mpmath with the same splines; polish; Hessian; polish the posted structure; assert margins.

## Angles

- Frank-Kasper import from metallurgy: build cluster candidates by carving spheres out of the Z, H, sigma, C15 and C14 Frank-Kasper phases (the bulk analogues Doye identified) at many centres and orientations, then relax.
- Disclination-network enumeration from soft-matter defect theory: enumerate polytetrahedral clusters by their disclination graph topology (as in Nelson's curved-space picture) and relax one representative per topology.
- Seeded basin hopping from N-1 and N+1 minima of the same table and from the Dzugutov and modified-Dzugutov tables, which share polytetrahedral motifs.
- Lead tables: Doye showed the lead glue and lead Gupta potentials give very different structures; relax the Gupta lead minima (CCD Pb Gupta table) under the glue potential as seeds.
- Population annealing with resampling (statistical-physics import) to keep many funnels alive at once.

## Pitfalls

- Spline implementation drift: OpenKIM lists several spline variants (cubic natural, quintic clamped, quintic Hermite) of the same Al potential, with slightly different energies. Only the implementation that reproduces the posted CCD energies counts.
- The lead glue potential (Lim-Ong-Ercolessi) is not the Gupta lead potential of the separate CCD Gupta table; never compare across them.
- Margins below 1e-4 eV are noise for 6-decimal tables; under-converged posted structures polish slightly lower (distinct-basin test mandatory).
- Glue potentials have finite cutoffs; an L-BFGS run can end on a cutoff kink with a nonzero gradient. The Hessian and gradient checks are required.

## Sources

- https://www-wales.ch.cam.ac.uk/~wales/CCD/jon/structures/Al.html
- https://www-wales.ch.cam.ac.uk/~wales/CCD/jon/structures/Al/table.html
- https://www-wales.ch.cam.ac.uk/~wales/CCD/jon/structures/Al/points/all.tar
- https://www-wales.ch.cam.ac.uk/~wales/CCD/jon/structures/lead.html
- https://www-wales.ch.cam.ac.uk/~wales/CCD/jon/structures/lead/table.html
- https://www-wales.ch.cam.ac.uk/~wales/CCD/jon/structures/lead/points/all.tar
- https://arxiv.org/abs/cond-mat/0301374
- https://arxiv.org/abs/cond-mat/0207432
- http://web.archive.org/web/20170607140842/http://www.fisica.uniud.it:80/~ercolessi/potentials/Al/
- http://web.archive.org/web/20170523125240/http://www.fisica.uniud.it:80/~ercolessi/potentials/Pb/
- https://openkim.org/id/MO_324507536345_001
- Status source: https://www-wales.ch.cam.ac.uk/~wales/CCD/jon/structures/Al/table.html

## Citations

- [Problem page](../../../../.raw/V3R1T4S/known-unknowns/packings-physics/ccd-glue-potential-al-pb-clusters.md)
- [Bank entry](../../../../.raw/V3R1T4S/bank/targets.json) (id `ccd-glue-potential-al-pb-clusters`, commit `7dd4480`)

## Related Nodes

- [[V3R1T4S Packings and physics]]
- [[V3R1T4S]]
