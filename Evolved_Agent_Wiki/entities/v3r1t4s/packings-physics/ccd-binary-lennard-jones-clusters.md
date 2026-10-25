---
id: v3r1t4s-ccd-binary-lennard-jones-clusters
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
# Binary Lennard-Jones clusters: lower a putative global minimum in the Doye-Meyer table (N <= 100, size ratios 1.05-1.30) or its published improvements

# Overview

> Bank id `ccd-binary-lennard-jones-clusters` · harvest · tractability 2.5 · laptop-hours · disclosure **open**
> Bank says open as of 2026-10-15. Statuses go stale — re-check the primary source before any work.

## Statement

Jonathan Doye and Lars Meyer (PRL 2005, 'Mapping the magic numbers in binary Lennard-Jones clusters') tabulated putative global minima of two-species LJ clusters A_{N-n}B_n with eps_AA = eps_AB = eps_BB and sigma_AB = (sigma_AA + sigma_BB)/2, for every N up to 100 and size ratios sigma_BB/sigma_AA in {1.05, 1.1, 1.15, 1.2, 1.25, 1.3} (the composition n is free: the record for (N, ratio) is the lowest energy over all n). The live Cambridge Cluster Database (CCD) table lists energy and point group per cell with point files. It is known to lag the literature: improved structures from Sicher, Mohr and Goedecker (JCP 2011), Istvan Kolossvary (PRE 2010) and Huang Wenqi and Ye Tao (JCIM 2011, two zip archives) are hosted separately on the CCD index page and NOT folded into the table (for example ratio 1.15, N = 73: table -404.046888, Huang-Ye file -404.0955878), and Takeuchi (Comput. Theor. Chem. 2015) reported further new minima (N = 59 and 68 at 1.15, N = 70 at 1.2). Six hundred cells, one 2005 search plus scattered patches: the cells N = 60..100 are the realistic frontier.

## Success criterion

Success means an xyz file with N atoms labelled A/B (any composition) for a size ratio in {1.05,...,1.3} and N <= 100, whose energy E* = sum_{i<j} 4 eps (sigma_ij^12/r^12 - sigma_ij^6/r^6) (sigma_AA = 1, sigma_BB = ratio, sigma_AB = (1+ratio)/2, eps = 1, no cutoff) is STRICTLY LOWER (direction: min) by at least 1e-4 than the minimum of: the energy for that (N, ratio) on the CCD BLJ table re-fetched live immediately before claiming, the energies in every improvement archive linked from https://www-wales.ch.cam.ac.uk/CCD.html (re-downloaded and re-evaluated by the checker, not read from headers), and any value for that cell in Cassioli et al. (population basin hopping, 95 new minima), Marques-Pereira 2010 (Chem. Phys. Lett. 485, 211), Kolossvary-Bowers 2010, Sicher-Mohr-Goedecker 2011, Ye-Xu-Huang 2011, Rondina-Da Silva 2013 (J. Chem. Inf. Model. 53, 2282), Wu-Cheng 2014 (J. Chem. Phys. 141, 124110), Takeuchi (Comput. Theor. Chem. 1050, 68), or any later paper found by an arXiv/Google Scholar search for 'binary Lennard-Jones clusters global minima'; AND the structure is a certified local minimum: polish in float128 or mpmath (30 digits) to gradient norm < 1e-10 in reduced units, then the 3N x 3N Hessian in double precision has exactly 6 near-zero modes (|lambda| < 1e-6) and no negative eigenvalue; AND polishing every posted structure for that cell with the same routine gives an energy at least 1e-4 higher (distinct basin).

## Partial wins

- {"id": "p1", "statement": "A certified improvement for some (N, ratio) with N in 101..150 over the best value in a fetchable published table (DOI or arXiv plus table reference); reported as a literature frontier, not a CCD record."}
- {"id": "p2", "statement": "Audit: a machine-readable merged table of all 600 cells (min over the CCD table and all hosted archives, each re-evaluated from coordinates), listing every cell where the live table is beaten by a hosted file by > 1e-4 and any posted point file that does not reproduce its own posted energy within 1e-5."}
- {"id": "p3", "statement": "A certified improvement at a size ratio in 1.4..2.0 for N <= 50 over Takeuchi's published value for the same (N, ratio) (his supplementary data), or a first certified putative global minimum for ratio 1.4..2.0 at N in 51..100 reported as a literature frontier."}

## Verification

Checker (< 10 min): curl the live table, parse the cell; download all.tar plus the four improvement archives and re-evaluate every candidate for the cell with the same energy function; evaluate the claim in float64 and mpmath (30 digits), L-BFGS then Newton polish, Hessian eigenvalues (6 zero modes, none negative); confirm composition and ratio; assert margin >= 1e-4 over the minimum. Calibration first: the checker must reproduce the posted energy of 10 random table point files to 1e-6.

## Angles

- Build the merged record table first (p2): it immediately shows which cells were improved by Huang-Ye/Kolossvary/Goedecker and therefore which neighbouring cells (N +- 1, adjacent ratio) were never revisited; those neighbours are the cheapest targets.
- Two-level search: for fixed geometry, the A/B labelling is a quadratic binary problem; alternate continuous relaxation with exhaustive or simulated-annealing swaps of labels (the 'exchange move' of Sicher-Mohr-Goedecker) and seed from polytetrahedral and core-shell templates of the neighbouring N.
- Import from alloy materials science: core-shell 'chemical ordering' heuristics (small atoms in the core, large on the surface, as in Ag-Cu nanoalloys) give strong starting labellings; then relax.
- Import from protein-design / graph coloring: treat the label assignment on a fixed contact graph as a max-weight cut-like problem and solve it exactly with a small MIP or QUBO solver for each geometry visited by basin hopping.
- Use structural motifs of the 1.3 ratio (Frank-Kasper / Z16 polytetrahedral cores) as seeds at 1.25, and vice versa; Doye-Meyer's own phase diagram shows motif boundaries where both families are close in energy.

## Pitfalls

- The live CCD table is NOT the record: several cells are beaten by archives hosted elsewhere on the same site and by Takeuchi 2015. Beating only the table is not a win; re-evaluate every hosted file.
- Wrong mixing rule or units: sigma_AB must be the arithmetic mean and all eps equal to 1; a Lorentz-Berthelot variant with different eps or a cutoff/shift changes every energy.
- Composition: the record for (N, ratio) is minimized over composition; an improvement at a fixed n that is still above the cell minimum is not a record.
- Under-converged posted coordinates polish to slightly lower energies; the distinct-basin test (>= 1e-4) is mandatory.
- Header energies inside archive files are not evidence; always recompute from coordinates.
- softmattertheory.lu's 180,000-cluster BLJ database (Mravlak et al. 2016) uses eps_BB, eps_AB != 1. It is a different potential, not a comparator.

## Sources

- https://www-wales.ch.cam.ac.uk/~wales/CCD/jon/structures/BLJ/table.html
- https://www-wales.ch.cam.ac.uk/~wales/CCD/jon/structures/BLJ/all.tar
- https://www-wales.ch.cam.ac.uk/CCD.html
- https://www-wales.ch.cam.ac.uk/~wales/CCD/NEW_BINARY_LJ_MINIMA/
- https://www-wales.ch.cam.ac.uk/~wales/CCD/Wenqi_Tao_BLJ.zip
- https://www-wales.ch.cam.ac.uk/~wales/CCD/Wenqi_Tao_BLJ2.zip
- https://www-wales.ch.cam.ac.uk/~wales/CCD/Istvan_Kolossvary_new_BLJ_minima.tgz
- https://arxiv.org/abs/cond-mat/0504726
- https://eprints.lib.hokudai.ac.jp/repo/huscap/all/57327/CTC_1050_68-.pdf
- Status source: https://www-wales.ch.cam.ac.uk/~wales/CCD/jon/structures/BLJ/table.html

## Citations

- [Problem page](../../../../.raw/V3R1T4S/known-unknowns/packings-physics/ccd-binary-lennard-jones-clusters.md)
- [Bank entry](../../../../.raw/V3R1T4S/bank/targets.json) (id `ccd-binary-lennard-jones-clusters`, commit `7dd4480`)

## Related Nodes

- [[V3R1T4S Packings and physics]]
- [[V3R1T4S]]
