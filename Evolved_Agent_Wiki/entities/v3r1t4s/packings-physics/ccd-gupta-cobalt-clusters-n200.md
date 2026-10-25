---
id: v3r1t4s-ccd-gupta-cobalt-clusters-n200
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
# Gupta cobalt clusters (N = 2..200): lower a putative global minimum on the Cambridge Cluster Database cobalt table or its posted improvements

# Overview

> Bank id `ccd-gupta-cobalt-clusters-n200` · harvest · tractability 2.5 · laptop-hours · disclosure **open**
> Bank says open as of 2026-10-15. Statuses go stale — re-check the primary source before any work.

## Statement

The Cambridge Cluster Database (CCD) hosts a table of putative global minima for cobalt clusters Co_N, N = 2..200, bound by a many-body Gupta (second-moment tight-binding) potential, from Zhan Lixin, Jeff Z. Y. Chen, Wing-Ki Liu and S. K. Lai (J. Chem. Phys. 122, 244707, 2005), with energies in eV to about 10 significant digits and point files (points.tgz). Below the table the CCD links improved minima from Lai Xiangjing, Huang Wenqi and Ni Hanwen for ten sizes (84, 95, 101, 113, 121, 122, 196, 197, 198, 200; archive Co.zip), so the table rows for those N are no longer the record. Apart from that one patch, the 2..200 range rests on a single 2005 search; Gupta silver clusters in the same size range were improved at 47 sizes as recently as 2025 (Lai, Hao, Guo, Wen and Fu, Comput. Phys. Commun. 2025, iterated dynamic lattice search), which suggests the cobalt table is not converged at N > 100. Checked live 2026-10-15: table page HTTP 200, Co.zip HTTP 200.

## Success criterion

Success means Cartesian coordinates for N atoms (N in 2..200) such that E* under the exact Gupta parameter set of the CCD cobalt table (calibrated first: the checker must reproduce the posted energies of ten randomly chosen table point files to 1e-6 eV, and of all ten Co.zip files) is STRICTLY LOWER (direction: min) by at least 1e-4 eV than the minimum of (a) the table energy for that N on the live CCD cobalt page re-fetched immediately before claiming, (b) the energy recomputed from the Co.zip file for that N if one exists, and (c) any published value for the same potential and N found by an arXiv / Google Scholar / Crossref search for 'cobalt clusters Gupta global minimum'; AND the structure is a certified local minimum: polish in float128 or mpmath (30 digits) to gradient norm < 1e-10 (reduced units of the table), then the 3N x 3N Hessian in double precision has exactly 6 near-zero modes (|lambda| < 1e-6) and no negative eigenvalue; AND polishing every posted structure for that N with the same routine gives an energy at least 1e-4 eV higher (distinct basin).

## Partial wins

- {"id": "p1", "statement": "Audit: recompute all 199 table point files plus the ten Co.zip files with the calibrated potential and publish a merged table, listing every N where the posted energy is not reproduced within 1e-5 eV or a posted structure polishes lower by more than 1e-4 eV."}
- {"id": "p2", "statement": "A certified improvement (same rules) for N in 201..250 against a fetchable published comparator for the same parameter set (DOI or arXiv id plus table reference); reported as a literature frontier, not a CCD record."}

## Verification

Checker (< 10 min): curl the live cobalt table and parse (N, energy) pairs; download points.tgz and Co.zip; implement E = sum_i [ sum_{j!=i} A exp(-p (r_ij/r0 - 1)) - sqrt( sum_{j!=i} xi^2 exp(-2q (r_ij/r0 - 1)) ) ] with the parameter set that reproduces the posted files (start from Cleri-Rosato cobalt values and confirm by calibration); evaluate the claim in float64 and mpmath; L-BFGS then Newton polish; Hessian eigenvalues; polish posted structures for the same N; assert margins.

## Angles

- Port the 2025 iterated dynamic lattice search (monotonic basin hopping + surface-atom perturbation + lattice search over vacant surface sites) that improved 47 Gupta silver clusters; the cobalt landscape is similar (decahedral vs icosahedral competition), and the code ideas are described in the open author copy.
- Seed from neighbours: add or remove one surface atom from the best N-1 and N+1 structures (including the Co.zip improvements) and relax; the ten posted improvements cluster near shell closures, so look at N = 80..125 and 190..200 first.
- Crystallography import: build Marks decahedra, truncated octahedra and twinned hcp/fcc fragments (cobalt is hcp in bulk) in every size and filling pattern, relax, and keep the best; hcp-based candidates are rarely tried in Gupta cluster searches.
- Combinatorial optimisation import: treat surface-site occupation on a fixed core as a binary quadratic program (pair-energy surrogate fitted to Gupta energies) and solve it with tabu search or simulated bifurcation before a continuous polish.
- Machine-learning import: train a cheap graph or SOAP-kernel surrogate on thousands of relaxed Co_N minima and use it to rank millions of lattice-based candidates before Gupta relaxation.

## Pitfalls

- Several Gupta cobalt parameter sets exist (Cleri-Rosato 1993 and later refits); a lower energy under a different set is meaningless. Calibrate on the posted files before evaluating any claim.
- The table rows for N = 84, 95, 101, 113, 121, 122, 196, 197, 198, 200 are already beaten by Co.zip; beating the table there is not a record unless the Co.zip energy is beaten too. Note the page text lists '107' but the archive contains Co197; trust the files.
- Under-converged posted coordinates can polish to slightly lower energies; that is not a new minimum (distinct-basin test with margin 1e-4 eV is mandatory).
- Energies are in eV for the unscaled potential; rescaling r0 or using reduced units changes the numbers.

## Sources

- https://www-wales.ch.cam.ac.uk/~wales/CCD/CoCCD/cobalt.html
- https://www-wales.ch.cam.ac.uk/~wales/CCD/CoCCD/points.tgz
- https://www-wales.ch.cam.ac.uk/~wales/CCD/CoCCD/Co.zip
- https://doi.org/10.1063/1.1940028
- https://leria-info.univ-angers.fr/%7Ejinkao.hao/papers/LaietalCOMPHY2025.pdf
- https://www-wales.ch.cam.ac.uk/CCD.html
- Status source: https://www-wales.ch.cam.ac.uk/~wales/CCD/CoCCD/cobalt.html

## Citations

- [Problem page](../../../../.raw/V3R1T4S/known-unknowns/packings-physics/ccd-gupta-cobalt-clusters-n200.md)
- [Bank entry](../../../../.raw/V3R1T4S/bank/targets.json) (id `ccd-gupta-cobalt-clusters-n200`, commit `7dd4480`)

## Related Nodes

- [[V3R1T4S Packings and physics]]
- [[V3R1T4S]]
