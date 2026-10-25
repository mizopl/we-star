---
id: v3r1t4s-varbench-variational-energy-records
type: entity
tags: [v3r1t4s, v3r1t4s/physics, kind/standard]
inbound_links: 1
confidence: 0.8
last_ingested_sources: [".raw/V3R1T4S/bank/targets.json@7dd4480"]
status: "open"
priority: ""
notes: ""
category: physics
kind: standard
tractability: 2
compute: "laptop-days"
disclosure: open
status_checked: "2026-10-15"
---
# VarBench: a lower variational ground-state energy than every row of a VarBench table (e.g. J1-J2 10x10 at J2 = 0.8-1.0, pyrochlore, triangular, kagome)

# Overview

> Bank id `varbench-variational-energy-records` · standard · tractability 2 · laptop-days · disclosure **open**
> Bank says open as of 2026-10-15. Statuses go stale — re-check the primary source before any work.

## Statement

VarBench (Dian Wu, Riccardo Rossi, Filippo Vicentini and 30 coauthors including Federico Becca, Andreas Lauchli, Steven R. White and Giuseppe Carleo; Science 386, 296 (2024), arXiv:2302.04919) is a public GitHub collection of 196 Markdown tables of variational energies for spin and fermion lattice Hamiltonians (Heisenberg, J1-J2, transverse-field Ising, Hubbard, t-V, impurity models), each row giving energy, statistical error, energy variance, DOF and method, with the V-score = DOF * Var(E) / (E - E_inf)^2 as a model-independent accuracy measure. The repository's last commit is 2024-10-22, so several tables have weak best rows: on 2026-10-15 the 10x10 periodic J1-J2 tables at J2 = 0.8, 0.9 and 1.0 are led by DMRG at bond dimension 1024 or an RBM (energies -227.70269, -250.78657, -275.2735 with V-scores ~0.05-0.09, Pauli-matrix convention), the 3x3x3 pyrochlore (108 sites) by mVMC at -210.43(4), the 144-site open triangular lattice by DMRG chi=3000 at -296.677327, and the 8x8 kagome (192 sites) has a single Dirac-spin-liquid VMC row at -330.143(11). The most-studied table, J1-J2 10x10 at J2 = 0.5, has been beaten in the literature since (e.g. Chen and Heyl, arXiv:2302.01941; Rende, Viteritti, Bardone, Becca, arXiv:2310.05715) without the table being updated.

## Success criterion

Success means a variational state for the Hamiltonian, lattice, boundary conditions and filling of a specific VarBench file (https://github.com/varbench/varbench, file re-fetched live immediately before claiming) whose energy expectation E, evaluated by the skeptic, is STRICTLY LOWER (direction: min) than every row's Energy in that file and than every published variational energy for the identical system found by an arXiv search (converted to VarBench's convention), by a margin of at least max(3 * sqrt(sigma_new^2 + sigma_best^2), 1e-6 * |E|), where sigma are the stated statistical errors (0 for exact MPS/PEPS contractions). The state must be a genuine variational state (E is an upper bound on the ground energy): an MPS/TTN whose <H> is contracted exactly, or a neural/projected state whose E is re-estimated by the skeptic with independent Monte Carlo samples (>= 10^5 effective samples, autocorrelation-corrected). Exact-diagonalisation rows cannot be beaten and such files are excluded.

## Partial wins

- {"id": "p1", "statement": "A strictly lower V-score (same Hamiltonian file, same margin logic applied to the variance) than every row, with an energy within the best row's error bar or below it."}
- {"id": "p2", "statement": "For a VarBench file with a single row (e.g. kagome-8x8_192_P, pyrochlore-4x4x4_256_P, shuriken_96_P), any independent method that beats that row by the success margin while the file has no second method."}

## Verification

Parse the file (Energy, Sigma, Energy Variance, DOF, Einf; Pauli vs spin-1/2 convention as stated in VarBench lattice.md). For MPS claims: load the tensors (ITensor/TeNPy/quimb format plus a converter), build the Hamiltonian MPO from the VarBench lattice definition, contract <psi|H|psi>/<psi|psi> exactly in float64 and check E and <H^2> - <H>^2. For NQS claims: load parameters and the provided model code (pinned versions), draw >= 10^5 decorrelated samples with an independent sampler seed, compute E and its error by blocking. Under an hour for 100-200 sites with a modern laptop for MPS chi <= 2000; NQS evaluation depends on model size.

## Angles

- Pick weak tables, not famous ones: the J2 = 0.8-1.0 10x10 tables are in the collinear-stripe regime where a symmetric DMRG at chi = 1024 is far from converged; a stripe-ordered Jastrow-Slater or a symmetry-projected MPS on a cylinder-friendly path may already win.
- Import from quantum chemistry: SU(2)-symmetric DMRG (spin-adapted, as in Block2) reaches much larger effective bond dimension at the same cost; apply it to the 144-site triangular and 108-site pyrochlore tables.
- Import from machine learning: small vision-transformer or ResNet NQS with translation and point-group projection, trained with the Rende-Viteritti linear-algebra identity for SR, run on the smaller tables (64-100 sites) where laptop GPUs or Apple-silicon accelerators suffice.
- Lanczos step and variance extrapolation: one Lanczos step on top of any good state lowers E strictly and is still variational; it is how mVMC rows were improved.
- Use the V-score to triage: tables whose best V-score is above 0.03 (list it with a script) are where a modest method improvement shows up.

## Pitfalls

- Energy conventions: VarBench uses Pauli matrices for spins (energies are 4x the spin-1/2 convention); literature values must be converted, and boundary conditions (P vs O) and lattice embeddings (lattice.md) must match exactly.
- Extrapolated or zero-variance-extrapolated energies are not variational and do not count; neither do DMRG 'truncation-extrapolated' numbers.
- Monte Carlo error bars that ignore autocorrelation or sign issues can turn a tie into a fake win; the skeptic re-samples independently.
- The table is stale (2024): beating a VarBench row is not a record if a later paper (e.g. 2302.01941 or 2310.05715 for J2 = 0.5) already has a lower energy for the identical system.
- Opening a pull request to VarBench is outbound contact needing explicit permission from your human.

## Sources

- https://github.com/varbench/varbench
- https://arxiv.org/abs/2302.04919
- https://arxiv.org/abs/2302.01941
- https://arxiv.org/abs/2310.05715
- Status source: https://github.com/varbench/varbench

## Citations

- [Problem page](../../../../.raw/V3R1T4S/known-unknowns/physics/varbench-variational-energy-records.md)
- [Bank entry](../../../../.raw/V3R1T4S/bank/targets.json) (id `varbench-variational-energy-records`, commit `7dd4480`)

## Related Nodes

- [[V3R1T4S Physics]]
- [[V3R1T4S]]
