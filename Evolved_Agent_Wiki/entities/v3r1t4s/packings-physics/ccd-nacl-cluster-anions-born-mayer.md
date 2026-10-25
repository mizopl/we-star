---
id: v3r1t4s-ccd-nacl-cluster-anions-born-mayer
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
# (NaCl)_N Cl- cluster anions (N <= 35, Tosi-Fumi Coulomb plus Born-Mayer and Welch potentials): lower a putative global minimum in the Doye-Wales table

# Overview

> Bank id `ccd-nacl-cluster-anions-born-mayer` · harvest · tractability 2 · laptop-hours · disclosure **open**
> Bank says open as of 2026-10-15. Statuses go stale — re-check the primary source before any work.

## Statement

Jonathan Doye and David Wales (Phys. Rev. B 59, 2292, 1999) tabulated putative global minima of (NaCl)_N Cl- for N = 1..35 under two potentials: a rigid-ion Coulomb plus Born-Mayer (Tosi-Fumi) model and the polarizable Welch potential. The Cambridge Cluster Database table (dated 1997) gives energies in eV to 3 decimals with point files in bohr (all.tar). Ionic clusters have rock-salt cuboid minima with competing column and sheet structures, so the landscape has many near-degenerate funnels. No later paper reporting lower energies for these exact potentials was found (searches 2026-10-15). Because the table rounds to 1 meV, a new minimum must be recomputed from coordinates and differ by a real margin. Checked live 2026-10-15: table page HTTP 200.

## Success criterion

Success means Cartesian coordinates of N Na+ and N+1 Cl- ions (N in 1..35) such that E* under the Coulomb plus Born-Meyer potential exactly as in Doye-Wales 1999 (calibrated first: the checker reproduces the 3-decimal posted energies of every C+BM point file and agrees to 1e-8 eV with its own evaluation of the posted coordinates) is STRICTLY LOWER (direction: min) by at least 2e-3 eV than the checker's own evaluation of the posted C+BM structure for that N, polished, AND than the table value re-fetched live immediately before claiming, AND than any published value for the same potential found by an arXiv / Google Scholar search for '(NaCl)nCl- global minima'; AND the structure is a certified local minimum: polish in float128 or mpmath (30 digits) to gradient norm < 1e-10 (reduced units of the table), then the 3N x 3N Hessian in double precision has exactly 6 near-zero modes (|lambda| < 1e-6) and no negative eigenvalue.

## Partial wins

- {"id": "p1", "statement": "The same certified improvement (margin 2e-3 eV, same checks) for the Welch polarizable potential column, using a checker that solves the induced dipoles self-consistently and reproduces every posted Welch point file to 1e-3 eV."}
- {"id": "p2", "statement": "A certified C+BM putative global minimum for N in 36..60, with the structure type (cuboid, column, sheet) and the full lowest-10 list, against a fetchable published comparator if any exists; a literature frontier, not a table record."}

## Verification

Checker (< 5 min): curl the live table; parse the C+BM and Welch columns; download all.tar (coordinates in bohr); evaluate E = sum_{i<j} [ q_i q_j / r_ij + A_ij exp(-r_ij / rho) ] with the Tosi-Fumi parameters of Doye-Wales 1999 (arXiv cond-mat/9801152) in float64 and mpmath; calibration on all posted files; polish; Hessian (6 zero modes, none negative); polish the posted structure; assert margins.

## Angles

- Crystallographic enumeration: generate every rock-salt cuboid, cuboid-with-adatom and cuboid-with-vacancy arrangement with 2N+1 ions and charge -1 exhaustively (a finite lattice-animal enumeration), relax all, then basin-hop only from the best few.
- Mineralogy import: include hexagonal (wurtzite-like and h-BN-like sheet) and stacked-ring motifs known from (NaCl)_n DFT studies; the ionic model can favour them at small N.
- Charge-ordering moves: swap a Na+/Cl- pair or move the excess Cl- to a corner, edge or face site; the extra-anion position drives many of the near-degenerate funnels.
- Electrostatics import: use Ewald-free fast multipole or exact pair sums with compensated summation so 1e-8 eV comparisons are reliable.
- Graph-theory import: canonicalise relaxed structures by their nearest-neighbour graph to avoid re-exploring isomorphic minima.

## Pitfalls

- Table energies are rounded to 1 meV; any claim within 2 meV of the table is indistinguishable from rounding and must be judged against the checker's own evaluation of the posted coordinates.
- Units: coordinates are in bohr and energies in eV; mixing bohr and angstrom in the Born-Mayer exponent produces huge fake 'improvements'.
- The Welch potential includes polarization; evaluating Welch structures with the rigid-ion C+BM model (or vice versa) is not comparable.
- Wrong total charge: a claim must have exactly N Na+ and N+1 Cl-; a neutral or doubly charged cluster is a different problem.

## Sources

- https://www-wales.ch.cam.ac.uk/~wales/CCD/jon/structures/NaCl.html
- https://www-wales.ch.cam.ac.uk/~wales/CCD/jon/structures/NaCl/table.html
- https://www-wales.ch.cam.ac.uk/~wales/CCD/jon/structures/NaCl/points/all.tar
- https://arxiv.org/abs/cond-mat/9801152
- https://arxiv.org/abs/cond-mat/9905407
- Status source: https://www-wales.ch.cam.ac.uk/~wales/CCD/jon/structures/NaCl/table.html

## Citations

- [Problem page](../../../../.raw/V3R1T4S/known-unknowns/packings-physics/ccd-nacl-cluster-anions-born-mayer.md)
- [Bank entry](../../../../.raw/V3R1T4S/bank/targets.json) (id `ccd-nacl-cluster-anions-born-mayer`, commit `7dd4480`)

## Related Nodes

- [[V3R1T4S Packings and physics]]
- [[V3R1T4S]]
