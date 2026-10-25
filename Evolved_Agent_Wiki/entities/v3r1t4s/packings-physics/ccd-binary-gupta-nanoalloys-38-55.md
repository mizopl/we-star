---
id: v3r1t4s-ccd-binary-gupta-nanoalloys-38-55
type: entity
tags: [v3r1t4s, v3r1t4s/packings-physics, kind/harvest]
inbound_links: 1
confidence: 0.8
last_ingested_sources: [".raw/V3R1T4S/bank/targets.json@7dd4480"]
status: "CONFIRMED_SOLUTION"
priority: ""
notes: ""
category: packings-physics
kind: harvest
tractability: 2
compute: "laptop-hours"
disclosure: open
status_checked: "2026-10-15"
---
# Binary Gupta nanoalloys (Ag-Au, Cu-Ag, Cu-Au 55-atom; Cu-Au 38-atom; Li-Na and Na-K 55-atom): lower the best homotop energy for some composition

# Overview

> Bank id `ccd-binary-gupta-nanoalloys-38-55` · harvest · tractability 2 · laptop-hours · disclosure **open**
> Bank says open as of 2026-10-15. Statuses go stale — re-check the primary source before any work.

## Statement

The Cambridge Cluster Database hosts composition-resolved putative global minima for binary Gupta clusters: Ag_nAu_{55-n}, Cu_nAg_{55-n}, Cu_nAu_{55-n} and Cu_nAu_{38-n} for every n from Lai Xiangjing, Huang Wenqi and Xu Ruchu (J. Chem. Phys. 135, 164109, 2011; rar archives with the energy in each file header), and Li_nNa_{55-n} and Na_nK_{55-n} from Andres Aguado (J. Chem. Phys. 133, 094302, 2010; tar archives). Each composition is a separate cell (about 300 cells), and the problem combines geometry with the homotop (atom-labelling) problem. Later algorithms benchmarked on some of these systems include Xia Wu and Wen Cheng's BDLS-ILS (J. Chem. Phys. 141, 124110, 2014), Rondina and Da Silva's revised basin hopping (J. Chem. Inf. Model. 53, 2282, 2013) and Du et al. (R. Soc. Open Sci. 2019, Ag-Au and Cu-Au at 1:1, 1:3, 3:1 up to 108 atoms); a claim must beat all of them where they overlap. Checked live 2026-10-15: CCD index page and all six archives HTTP 200.

## Success criterion

Success means coordinates and species labels for one system and composition listed in a CCD archive (for example Cu_12Au_26) such that E* under the exact Gupta parameter set used for that archive (calibrated first: the checker reproduces the header energies of every file in that archive to 1e-6 eV from coordinates) is STRICTLY LOWER (direction: min) by at least 1e-4 eV than the checker's evaluation of the archive structure for that composition (archives re-downloaded immediately before claiming) AND than any published value for the same system, parameters and composition found by an arXiv / Google Scholar search (at least the four papers named in the statement); AND the structure is a certified local minimum: polish in float128 or mpmath (30 digits) to gradient norm < 1e-10 (reduced units of the table), then the 3N x 3N Hessian in double precision has exactly 6 near-zero modes (|lambda| < 1e-6) and no negative eigenvalue; AND polishing the archive structure gives an energy at least 1e-4 eV higher.

## Partial wins

- {"id": "p1", "statement": "Audit: a merged machine-readable table of all compositions in the six archives, recomputed from coordinates, listing every file whose header energy is not reproduced within 1e-5 eV or that polishes lower by more than 1e-4 eV, and every cell where a later paper (with fetchable values) already beats the archive."}
- {"id": "p2", "statement": "A batch of at least five certified homotop improvements (same rules) in one system, found by exchange-only moves on the posted geometries (no change of the geometric motif), reported with the improvement sizes."}

## Verification

Checker (< 10 min): download the archive (bsdtar reads .rar), parse every file, recompute energies with the Gupta form E = sum_i [ sum_{j!=i} A_ab exp(-p_ab (r_ij/r0_ab - 1)) - sqrt( sum_{j!=i} xi_ab^2 exp(-2 q_ab (r_ij/r0_ab - 1)) ) ] with the parameters from the source paper; calibration; evaluate the claim in float64 and mpmath; polish; Hessian; composition check; margins.

## Angles

- Homotop optimisation as quadratic unconstrained binary optimisation: on a fixed relaxed geometry, fit pairwise site-exchange energies and solve the labelling with tabu search or simulated annealing; then relax and iterate (an import from combinatorial optimisation).
- Composition walking: take the best structure at n and swap one atom to get n+1, relax, and sweep both directions across the whole composition range; neighbouring cells share motifs.
- Segregation physics: build core-shell and Janus seeds guided by surface-energy and atomic-size mismatch (Cu core / Au shell, Na core / K shell) before global search.
- Alloy-theory import: use a cluster-expansion surrogate (as in bulk alloy thermodynamics) trained on Gupta energies to screen labellings quickly.
- Cross-check the 38-atom Cu-Au cells, the most benchmarked, last; the 55-atom Li-Na and Na-K archives have seen the least follow-up.

## Pitfalls

- Parameter sets: the Ag-Au, Cu-Ag and Cu-Au archives use one published parameter table and the alkali archives another; header energies inside files are not evidence. Recompute every comparator from coordinates.
- Composition mix-ups: the record is per composition; a lower energy at a different n, or with A and B labels swapped, is not an improvement.
- Later papers (Wu-Cheng 2014, Rondina-Da Silva 2013, Du et al. 2019) may already beat an archive cell; beating the CCD file alone is not novel.
- Differences below 1e-4 eV are numerical; the distinct-basin test is mandatory.

## Sources

- https://www-wales.ch.cam.ac.uk/CCD.html
- https://www-wales.ch.cam.ac.uk/~wales/CCD/AgAu_55.rar
- https://www-wales.ch.cam.ac.uk/~wales/CCD/CuAg_55.rar
- https://www-wales.ch.cam.ac.uk/~wales/CCD/CuAu_55.rar
- https://www-wales.ch.cam.ac.uk/~wales/CCD/CuAu_38.rar
- https://www-wales.ch.cam.ac.uk/~wales/CCD/LiNa_Gupta.tar
- https://www-wales.ch.cam.ac.uk/~wales/CCD/NaK_Gupta.tar
- https://doi.org/10.1063/1.3656766
- https://doi.org/10.1063/1.4896152
- https://doi.org/10.1021/ci400224z
- https://doi.org/10.1098/rsos.190342
- Status source: https://www-wales.ch.cam.ac.uk/CCD.html

## Citations

- [Problem page](../../../../.raw/V3R1T4S/known-unknowns/packings-physics/ccd-binary-gupta-nanoalloys-38-55.md)
- [Bank entry](../../../../.raw/V3R1T4S/bank/targets.json) (id `ccd-binary-gupta-nanoalloys-38-55`, commit `7dd4480`)

## Related Nodes

- [[V3R1T4S Packings and physics]]
- [[V3R1T4S]]
