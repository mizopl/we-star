---
id: v3r1t4s-ccd-c60-molecular-clusters
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
# (C60)_N molecular clusters (Pacheco-Prates-Ramalho N <= 105, Girifalco N < 81): lower a putative global minimum in the Doye-Wales tables

# Overview

> Bank id `ccd-c60-molecular-clusters` · harvest · tractability 2 · laptop-hours · disclosure **open**
> Bank says open as of 2026-10-15. Statuses go stale — re-check the primary source before any work.

## Statement

Jonathan Doye, David Wales, W. Branz and Florent Calvo (PRB 2001) located putative global minima of clusters of rigid-sphere C60 molecules interacting through the Pacheco and Prates-Ramalho potential up to N = 105 (icosahedral up to N = 15, then decahedral and close-packed); Doye and Wales (CPL 1996) did the same for the shorter-ranged Girifalco potential for N < 81. Both tables are on the Cambridge Cluster Database with point files. The short effective range makes landscapes strongly multi-funnel; Shao et al. (IEICE Trans. 2013) revisited only N <= 25. N = 26..105 for PPR has not been re-searched systematically (search 2026-10-13).

## Success criterion

Success means centre-of-mass coordinates of N molecules such that E* under the exact potential of that table (PPR = pair term plus Axilrod-Teller three-body term as in Doye et al. PRB 64, 235409; or Girifalco; calibrated by reproducing ten posted point-file energies to 1e-6 in the table's units) is STRICTLY LOWER (direction: min) than the live table energy for (potential, N) re-fetched immediately before claiming by at least 1e-4, AND than Shao et al. 2013 (PPR, N <= 25), Cheng-Cai-Shao 2005 (Girifalco, N <= 150, ChemPhysChem 6, 261) and any other published value for the same potential found by an arXiv/Google Scholar search; AND the structure is a certified local minimum: polish in float128 or mpmath (30 digits) to gradient norm < 1e-10 in reduced units, then the 3N x 3N Hessian in double precision has exactly 6 near-zero modes (|lambda| < 1e-6) and no negative eigenvalue; AND polishing the posted point file gives an energy at least 1e-4 higher.

## Partial wins

- {"id": "p1", "statement": "A certified improvement for PPR at N in 106..150, or for Girifalco at N in 81..150 against Cheng-Cai-Shao 2005, with a fetchable published comparator (DOI/arXiv plus table reference); a literature frontier, not a CCD record."}
- {"id": "p2", "statement": "Audit of both tables: posted point files that do not reproduce their posted energies or that polish lower by > 1e-4."}

## Verification

Checker (< 10 min): curl the live table; parse; evaluate PPR as pair + Axilrod-Teller triple sum (O(N^3), fine for N <= 150) or the Girifalco closed form, in float64 and mpmath; calibrate on posted files (PPR calibration must FAIL if the three-body term is omitted); polish; Hessian; polish the posted structure; margins.

## Angles

- Short-range potentials reward maximal nearest-neighbour contacts: enumerate decahedral (Marks, Ino) and close-packed (truncated octahedra, twinned) frameworks with the highest contact counts per N, as Doye-Wales did for short-range Morse, then relax.
- Seed from the CCD Morse rho = 14 (short-range) global minima at the same N, rescaled to the C60 nearest-neighbour distance; Doye's own work maps C60 onto short-range Morse behaviour.
- Import from colloid science: sticky-sphere maximal-contact clusters (Hoy, Holmes-Cerfon enumerations; Hoy's packings are hosted on the CCD) give exact contact-graph candidates for small N.
- Import from integer programming: maximise the number of unit-distance contacts on a lattice fragment exactly with a MIP, then relax off-lattice.

## Pitfalls

- Two different potentials with different units (eV vs well-depth units); compare only within one table.
- The Leary tetrahedron at N = 98, suggested by experiment, is NOT the PPR minimum per Doye et al.; reproducing experiment-motivated structures is not a record unless the energy beats the table.
- Precision: the PPR table lists eV values; margins below 1e-4 are noise.
- Under-converged posted coordinates; distinct-basin test mandatory.
- PPR without its three-body term, or with a sign or prefactor error in it, gives energies below the table. This exact coding error produced wrong 'global minima' in an earlier PPR study (see Doye et al. 2001).

## Sources

- https://www-wales.ch.cam.ac.uk/~wales/CCD/jon/structures/C60.html
- https://www-wales.ch.cam.ac.uk/~wales/CCD/jon/structures/C60/PPR/table.html
- https://www-wales.ch.cam.ac.uk/~wales/CCD/jon/structures/C60/PPR/all.tar.gz
- https://www-wales.ch.cam.ac.uk/~wales/CCD/jon/structures/C60/Girifalco/tables.html
- https://www-wales.ch.cam.ac.uk/~wales/CCD/jon/structures/C60/Girifalco/C60.tar
- https://arxiv.org/abs/cond-mat/0106637
- Status source: https://www-wales.ch.cam.ac.uk/~wales/CCD/jon/structures/C60.html

## Citations

- [Problem page](../../../../.raw/V3R1T4S/known-unknowns/packings-physics/ccd-c60-molecular-clusters.md)
- [Bank entry](../../../../.raw/V3R1T4S/bank/targets.json) (id `ccd-c60-molecular-clusters`, commit `7dd4480`)

## Related Nodes

- [[V3R1T4S Packings and physics]]
- [[V3R1T4S]]
