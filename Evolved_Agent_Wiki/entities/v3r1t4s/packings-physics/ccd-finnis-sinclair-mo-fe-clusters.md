---
id: v3r1t4s-ccd-finnis-sinclair-mo-fe-clusters
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
status_checked: "2026-10-15"
---
# Finnis-Sinclair molybdenum and iron clusters (N = 3..100): lower a putative global minimum in the Elliott-Shibuta-Wales tables

# Overview

> Bank id `ccd-finnis-sinclair-mo-fe-clusters` · harvest · tractability 2.5 · laptop-hours · disclosure **open**
> Bank says open as of 2026-10-15. Statuses go stale — re-check the primary source before any work.

## Statement

James Elliott, Yasushi Shibuta and David Wales (Phil. Mag. 89, 3311-3332, 2009) located putative global minima of Mo_N and Fe_N clusters, N = 3..100, bound by the Finnis-Sinclair many-body potential (Finnis and Sinclair, Phil. Mag. A 50, 45, 1984; the iron table uses the modified parameters of Phil. Mag. A 53, 161, 1986). The two Cambridge Cluster Database tables give energies in eV to 10 decimals with point files (points.tgz) and say the results were only 'partially reported' in the paper. These body-centred-cubic metals favour unusual cluster motifs, and no independent systematic re-search of these two tables was found (searches 2026-10-15; a 2017 force-biased Monte Carlo study of Fe_N, N <= 60, arXiv:1708.00096, only reproduced energies 'very close' to the CCD values). Checked live 2026-10-15: both pages HTTP 200.

## Success criterion

Success means Cartesian coordinates for N atoms (N in 3..100) for Mo or Fe such that E* under the exact Finnis-Sinclair parameters of that table (calibrated first: reproduce the posted energies of ten randomly chosen point files of that metal to 1e-7 eV) is STRICTLY LOWER (direction: min) by at least 1e-4 eV than the table energy for (metal, N) re-fetched live immediately before claiming, AND than any published value for the same potential and N found by an arXiv / Google Scholar search for 'Finnis-Sinclair clusters global minima' plus the metal; AND the structure is a certified local minimum: polish in float128 or mpmath (30 digits) to gradient norm < 1e-10 (reduced units of the table), then the 3N x 3N Hessian in double precision has exactly 6 near-zero modes (|lambda| < 1e-6) and no negative eigenvalue; AND polishing the posted structure for that N with the same routine gives an energy at least 1e-4 eV higher (distinct basin).

## Partial wins

- {"id": "p1", "statement": "Audit: recompute all 2 x 98 posted point files and list every row whose posted energy is not reproduced within 1e-6 eV or that polishes lower by more than 1e-4 eV."}
- {"id": "p2", "statement": "A certified improvement for N in 101..150 for either metal against a fetchable published comparator using the same parameters (DOI or arXiv plus table reference); a literature frontier, not a CCD record."}

## Verification

Checker (< 10 min): curl the live table, parse (N, energy) pairs; download points.tgz; implement E = sum_i [ 1/2 sum_{j!=i} V(r_ij) - A sqrt(rho_i) ], rho_i = sum_{j!=i} phi(r_ij), with the cubic-polynomial V and phi and cutoffs c, d of Finnis-Sinclair (1984 for Mo; 1986 modified Fe) and confirm by calibration; evaluate the claim in float64 and mpmath; polish; Hessian; polish the posted structure; assert margins.

## Angles

- bcc-aware seeding: build rhombic-dodecahedral and bcc-fragment candidates (the bulk structure of both metals) alongside icosahedral and decahedral ones for every N, relax, and compare; most cluster codes seed only fcc/icosahedral families.
- Basin hopping with dynamic lattice search on surface vacancies, as used for Gupta silver (Lai et al. 2025), restricted to the outer shell of the posted minima.
- Materials-science import: use the known low-energy grain-boundary and twin motifs of bcc Mo/Fe to construct twinned cluster candidates.
- Statistical-physics import: parallel tempering with replica exchange between N and N+1 (grand-canonical moves) to move between growth sequences.
- Cross-potential transfer: relax the Sutton-Chen, Gupta and glue global minima of the same N under Finnis-Sinclair; structures optimal for one many-body potential are good seeds for another.

## Pitfalls

- The iron table uses the 1986 modified Finnis-Sinclair parameters, not the 1984 ones; mixing them gives different energies that look like records. Calibrate per metal.
- Finnis-Sinclair V and phi are piecewise polynomials with cutoffs; a sloppy cutoff implementation shifts energies by more than 1e-4 eV. Reproduce the posted energies to 1e-7 eV first.
- The tables list 10 decimals; differences below 1e-4 eV are not records, and a polished posted structure that drops slightly is under-convergence, not a new minimum.
- Some cluster codes report cohesive energy per atom or binding energy relative to isolated atoms with the opposite sign; compare total energies only.

## Sources

- https://www-wales.ch.cam.ac.uk/~wales/CCD/FS_Mo/moly_fs.html
- https://www-wales.ch.cam.ac.uk/~wales/CCD/FS_Fe/iron_fs.html
- https://www-wales.ch.cam.ac.uk/~wales/CCD/FS_Mo/points.tgz
- https://www-wales.ch.cam.ac.uk/~wales/CCD/FS_Fe/points.tgz
- https://doi.org/10.1080/14786430903270668
- https://arxiv.org/abs/1708.00096
- Status source: https://www-wales.ch.cam.ac.uk/~wales/CCD/FS_Mo/moly_fs.html

## Citations

- [Problem page](../../../../.raw/V3R1T4S/known-unknowns/packings-physics/ccd-finnis-sinclair-mo-fe-clusters.md)
- [Bank entry](../../../../.raw/V3R1T4S/bank/targets.json) (id `ccd-finnis-sinclair-mo-fe-clusters`, commit `7dd4480`)

## Related Nodes

- [[V3R1T4S Packings and physics]]
- [[V3R1T4S]]
