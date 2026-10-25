---
id: v3r1t4s-ccd-sutton-chen-clusters
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
tractability: 1.5
compute: "laptop-hours"
disclosure: open
status_checked: "2026-10-15"
---
# Sutton-Chen metal clusters (12-6, 9-6, 10-8; N <= 80): lower a putative global minimum in the Doye-Wales tables

# Overview

> Bank id `ccd-sutton-chen-clusters` · harvest · tractability 1.5 · laptop-hours · disclosure **open**
> Bank says open as of 2026-10-15. Statuses go stale — re-check the primary source before any work.

## Statement

Jonathan Doye and David Wales (New J. Chem. 1998) located putative global minima of clusters bound by the many-body Sutton-Chen potential E = eps sum_i [ 1/2 sum_{j!=i} (a/r_ij)^n - c sqrt(rho_i) ], rho_i = sum_{j!=i} (a/r_ij)^m, for the (n,m) = 12-6 (Ag, Rh), 9-6 (Ni, Cu) and 10-8 (Au, Pt) parameterizations, all N <= 80, posted on the Cambridge Cluster Database with point files (reduced units eps = a = 1, energies to 4 decimals). Their own basin-hopping runs found only 95% / 94% / 85% of the final minima unseeded, the landscapes are multi-funnel (decahedral vs icosahedral vs close-packed competition), and the CCD invites improvements. The 10-8 table had the lowest unseeded hit rate. Two cells are already beaten in the literature and the CCD tables have not been updated (checked 2026-10-15): Lopez-Castro, Ortiz-Chi and Merino (GrowPAL, J. Chem. Theory Comput. 20, 4939, 2024) report new lowest minima for 12-6 N = 68 and 10-8 N = 58, and Shao, Liu and Cai (J. Chem. Theory Comput. 1, 762, 2005) a new Ag68 minimum; remaining cells N <= 80 have been re-searched by GrowPAL without improvement, so expected headroom is small.

## Success criterion

Success means coordinates for N atoms (N <= 80) for one of the three Sutton-Chen variants such that E* computed with the exact (n, m, c) of Doye-Wales 1998 (calibrated by reproducing ten posted point-file energies to 1e-4) is STRICTLY LOWER (direction: min) by at least 1e-3 than the minimum of the table energy for that (variant, N) re-fetched live immediately before claiming and every published value for that cell, at least GrowPAL 2024 (Table 3 and SI) and Shao-Liu-Cai 2005, plus any value found by an arXiv/Google Scholar search for 'Sutton-Chen clusters global minima'; for 12-6 N = 68 and 10-8 N = 58 beating the CCD table alone is explicitly NOT a win; AND the structure is a certified local minimum: polish in float128 or mpmath (30 digits) to gradient norm < 1e-10 in reduced units, then the 3N x 3N Hessian in double precision has exactly 6 near-zero modes (|lambda| < 1e-6) and no negative eigenvalue, AND polishing the posted point file gives an energy at least 1e-3 higher (distinct basin).

## Partial wins

- {"id": "p1", "statement": "A certified improvement for N in 81..150 for one variant against a fetchable published value (DOI/arXiv plus table reference) for the same parameters."}
- {"id": "p2", "statement": "Audit: re-polish all 3 x 78 posted point files and report any whose posted energy is not reproduced within 1e-4 or whose polished energy drops by > 1e-3."}

## Verification

Checker (< 10 min): curl the table page for the variant, parse N and energy; load claim; compute SC energy in float64 and mpmath; polish (analytic gradient), Hessian check; download points/all.tar, polish the posted structure; assert margins. Potential constants (n, m, c) are taken from Doye-Wales 1998 Table 1 (arXiv cond-mat/9711038) and must reproduce posted energies before any claim is evaluated.

## Angles

- Start where the 1998 unseeded search was weakest (10-8, N = 40..80): seed from the 12-6 and 9-6 structures at the same N and from the Morse/LJ global minima (CCD), since all three families share decahedral/fcc/icosahedral competitors.
- Lattice-based construction (dynamic lattice searching, as used by Shao and Huang for LJ 310..1000): enumerate Marks decahedra, truncated octahedra and anti-Mackay icosahedra, fill/remove surface sites greedily, then relax.
- Import from crystallography: generate twinned and stacking-fault close-packed fragments (hcp/fcc mixtures, labelled 'c' in the tables) as seeds; these are under-sampled by random-start basin hopping.
- Import from machine learning: train a cheap surrogate on local-environment descriptors (coordination, common-neighbour analysis) over all posted minima, then use it to rank surface-site additions before expensive relaxations.

## Pitfalls

- Parameter drift: c differs between variants and between sources (bulk-fitted vs reduced); a claim computed with the wrong c is meaningless. Calibrate on posted files first.
- Energies are in reduced units (eps = a = 1); rescaling by element constants before comparing produces fake differences.
- The table carries 4 decimals; differences below 1e-3 are not records.
- Polishing a posted structure to a slightly lower number is under-convergence, not a new minimum (distinct-basin test).
- The live CCD SC tables lag the literature at 12-6 N = 68 and 10-8 N = 58 (GrowPAL 2024). Reproducing those structures is not novel. GrowPAL's SI coordinates are behind an ACS 403, so the energy in its Table 3 (Europe PMC full text) is the comparator.

## Sources

- https://www-wales.ch.cam.ac.uk/~wales/CCD/jon/structures/SC.html
- https://www-wales.ch.cam.ac.uk/~wales/CCD/jon/structures/SC/12-6/table.12-6.html
- https://www-wales.ch.cam.ac.uk/~wales/CCD/jon/structures/SC/9-6/table.9-6.html
- https://www-wales.ch.cam.ac.uk/~wales/CCD/jon/structures/SC/10-8/table.10-8.html
- https://www-wales.ch.cam.ac.uk/~wales/CCD/jon/structures/SC/12-6/points/all.tar
- https://www-wales.ch.cam.ac.uk/~wales/CCD/jon/structures/SC/potential.html
- https://arxiv.org/abs/cond-mat/9711038
- https://www.ebi.ac.uk/europepmc/webservices/rest/PMC11171261/fullTextXML
- https://doi.org/10.1021/acs.jctc.4c00365
- https://doi.org/10.1021/ct049865j
- Status source: https://www-wales.ch.cam.ac.uk/~wales/CCD/jon/structures/SC.html

## Citations

- [Problem page](../../../../.raw/V3R1T4S/known-unknowns/packings-physics/ccd-sutton-chen-clusters.md)
- [Bank entry](../../../../.raw/V3R1T4S/bank/targets.json) (id `ccd-sutton-chen-clusters`, commit `7dd4480`)

## Related Nodes

- [[V3R1T4S Packings and physics]]
- [[V3R1T4S]]
