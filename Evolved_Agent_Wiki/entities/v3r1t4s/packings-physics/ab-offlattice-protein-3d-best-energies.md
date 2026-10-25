---
id: v3r1t4s-ab-offlattice-protein-3d-best-energies
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
# 3D AB off-lattice protein model: beat the best published energy for a standard Fibonacci or PDB-derived benchmark sequence

# Overview

> Bank id `ab-offlattice-protein-3d-best-energies` · harvest · tractability 2 · laptop-hours · disclosure **open**
> Bank says open as of 2026-10-15. Statuses go stale — re-check the primary source before any work.

## Statement

The 3D AB off-lattice model (Stillinger-Head-Gordon AB model extended to 3D) represents a chain of L unit-length bonds with residues A (hydrophobic) or B (hydrophilic) and energy E = 1/4 sum_{i=1}^{L-2} (1 - cos theta_i) + 4 sum_{i<j-1} (r_ij^-12 - C(s_i,s_j) r_ij^-6), C(A,A) = 1, C(A,B) = C(B,B) = 1/2. A benchmark set of Fibonacci sequences (F13, F21, F34, F55, F89) and 18 PDB-derived sequences (1BXP ... 2EWH, 13 to 98 residues) is standard. Borko Boskovic and Janez Brest (Swarm Evol. Comput. 2020, arXiv:1903.01456, Table 10) report the best energies to date (e.g. F89: 86.4318 in their sign convention, 1PCH: 166.7194, 2EWH: 257.0741), improving their own 2018 values by up to 11.6 units for the longest chains after 4-day grid runs. The large recent jumps on the longest sequences show these are far from converged. Istvan Kolossvary's 2012 putative minima (hosted on the CCD) use a different variant of the model and are not comparable.

## Success criterion

Success means bond and torsion angles (or Cartesian coordinates with all bond lengths 1 within 1e-9) for one of the 23 benchmark sequences, exactly as listed in arXiv:1903.01456 Table 2, such that E* computed with the formula in the statement (float64, confirmed in mpmath) satisfies -E* > B + 1e-3, where B is the LARGEST value reported for that sequence in Table 10 of arXiv:1903.01456 (re-fetched immediately before claiming; the table reports -E as positive numbers) and in any later or independent paper for the identical model found by an arXiv / Google Scholar search for '3D AB off-lattice' plus the sequence label (including Kim, Chaos Solitons Fractals 90, 111, 2016 for F89, after confirming that paper uses the same energy function); direction: min in E (max in the tabulated -E); AND the conformation is a local minimum in angle space (gradient norm < 1e-8).

## Partial wins

- {"id": "p1", "statement": "A certified improvement for F89, 1PCH or 2EWH (the three longest sequences) by at least 0.5 energy units over the best published value; this is the realistic harvest cell."}
- {"id": "p2", "statement": "An independent reproduction: recompute the energies of the published best conformations if the authors released them (the paper points to a public demo at spse.feri.um.si, unreachable on 2026-10-13 and 2026-10-15) and report any discrepancy."}

## Verification

Checker (< 1 min): rebuild coordinates from angles (or check bond lengths), assert the exact sequence string, compute E with the stated C(s_i,s_j), confirm in mpmath; numeric gradient; compare with Table 10 and the literature list.

## Angles

- Two-phase idea of Boskovic-Brest, scaled differently: first maximise hydrophobic-core compactness (a packing problem for the A residues), then relax the full energy; replace DE with basin hopping on 10 cores for the 3 longest chains.
- Import from structural biology: thread the sequence onto real protein backbone fragments (helix/sheet angle libraries) to seed conformations, then relax off-lattice.
- Import from sphere packing: the A-A LJ term rewards an icosahedral/polytetrahedral hydrophobic core; build cores from LJ cluster global minima (CCD) with the right number of A residues and route the chain through them with a TSP-like path search.
- Hidden-force Monte Carlo (Kolossvary-Bowers) or parallel tempering in angle space with replica exchange across temperatures as a direct competitor to DE.

## Pitfalls

- Model variants: 2D vs 3D, with or without a torsion term (Irback's AB model has a different backbone term), sign conventions (papers report -E). Only the exact formula above and the exact Table 2 sequences count.
- Bond-length violations: optimisers in Cartesian space that let bonds drift away from 1 get artificially low energies; bond lengths must be exactly 1.
- The excluded sum is over |i - j| >= 2; including nearest neighbours or excluding next-nearest changes energies.
- Kolossvary's CCD file uses a different potential; do not compare against it.
- Sign convention: Boskovic-Brest tables list -E (positive numbers). A claim whose E* is merely below the positive table value is meaningless; compare -E* with the table. Kim 2016 (CSA, F89) is paywalled and may use a different 3D AB variant. Confirm the energy function before treating its value as the bar or ignoring it.

## Sources

- https://arxiv.org/abs/1903.01456
- https://arxiv.org/abs/1710.07031
- https://www-wales.ch.cam.ac.uk/~wales/CCD/Protein_AB_models_by_Istvan_Kolossvary.txt
- https://arxiv.org/abs/1205.4705
- Status source: https://arxiv.org/abs/1903.01456

## Citations

- [Problem page](../../../../.raw/V3R1T4S/known-unknowns/packings-physics/ab-offlattice-protein-3d-best-energies.md)
- [Bank entry](../../../../.raw/V3R1T4S/bank/targets.json) (id `ab-offlattice-protein-3d-best-energies`, commit `7dd4480`)

## Related Nodes

- [[V3R1T4S Packings and physics]]
- [[V3R1T4S]]
