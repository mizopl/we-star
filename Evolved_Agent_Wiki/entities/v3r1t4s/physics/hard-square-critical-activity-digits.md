---
id: v3r1t4s-hard-square-critical-activity-digits
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
tractability: 2.5
compute: "laptop-days"
disclosure: open
status_checked: "2026-10-15"
---
# Hard-square lattice gas: more digits of the critical activity z_c = 3.7962551739... (Guo-Blote 2002) or of the negative-activity singularity -0.1193388818... (Todo 1999)

# Overview

> Bank id `hard-square-critical-activity-digits` · standard · tractability 2.5 · laptop-days · disclosure **open**
> Bank says open as of 2026-10-15. Statuses go stale — re-check the primary source before any work.

## Statement

The nearest-neighbour-exclusion lattice gas on the square lattice (hard squares) has an Ising-class order-disorder transition at activity z_c+ and a Lee-Yang-class singularity on the negative axis z_c-, neither known in closed form (contrast hard hexagons, solved by Baxter). Best published values: z_c+ = 3.79625517391234(4) by Wenan Guo and Henk Blote (Phys. Rev. E 66 (2002) 046140, transfer-matrix finite-size scaling), and z_c- = -0.11933888188(1) by Synge Todo (Int. J. Mod. Phys. C 10 (1999) 517; arXiv cond-mat/9703176). Xinliang Lyu's tensor-network RG study (arXiv 2603.25492, v2 2026-07-23) still uses both as reference values and itself reaches about 7e-7 relative accuracy. Those transfer-matrix studies used strip widths that were limited by 1997-2002 memory; the state count grows like the golden ratio to the width, so widths around 30-36 are now within laptop reach, and high-precision eigenvalue solvers plus modern extrapolation should add digits.

## Success criterion

Success means an estimate of z_c+ with stated uncertainty at most 4e-16 (ten times smaller than Guo-Blote's 4e-15), or of z_c- with stated uncertainty at most 1e-12, such that (a) it agrees with the published value within the combined uncertainties, (b) two independent finite-size estimators (for example phenomenological renormalisation of correlation lengths at widths L, L+2 and the free-energy/conformal-anomaly or Binder-type crossing method, or a corner-transfer-matrix scaling analysis) agree within their uncertainties, (c) the raw strip data (leading eigenvalues to at least 30 digits for each width and activity) are published so a skeptic can redo the extrapolation, and (d) a literature search re-run immediately before claiming finds no published value with smaller uncertainty. Direction: smaller uncertainty, consistent value.

## Partial wins

- {"id": "p1", "statement": "Exact-to-30-digits transfer-matrix eigenvalue data for the hard-square model at widths strictly beyond the largest width used by Guo and Blote (or Todo), released as files with the generating code; checkable by recomputing any single width, useful whether or not the extrapolation beats the record."}
- {"id": "p2", "statement": "A reproduction of z_c+ = 3.79625517391234(4) to at least 13 significant digits with an independently written code and estimator, documenting the widths and corrections-to-scaling form needed."}

## Verification

Skeptic (< 1 hour): recompute the leading two eigenvalues for two of the claimed widths at two activities in multiprecision and match the released data; rerun the claimant's extrapolation script on the released data; check the estimator families agree; compare with the published values.

## Angles

- Use sparse, symmetry-reduced transfer matrices (translation and reflection momentum sectors; the ordered phase breaks sublattice symmetry, so use the odd sector for the correlation length) at widths up to the mid-30s.
- From conformal field theory: the critical point is Ising-class with known correction exponents (Guo and Blote confirmed Ising corrections); fit with the exactly known irrelevant-operator exponents instead of free parameters.
- From quantum chemistry and DMRG: a corner-transfer-matrix or boundary-MPS calculation at fixed bond dimension gives a second, width-free estimator via finite-entanglement scaling.
- For z_c-, the Lee-Yang edge exponent is exactly known (sigma = -1/6 in 2D); building it into the fit, as for the hard-hexagon case solved exactly, tightens the extrapolation.

## Pitfalls

- Under-estimated error bars are the classic false win: an extrapolation that ignores a correction term gives a tight but wrong value. Require two estimator families and report fits with one fewer correction term.
- Activity vs chemical potential vs fugacity conventions; and the 2x2 hard-square model (kings, critical activity near 97.5) is a different model with the same name in some papers.
- Double-precision eigenvalues limit the extrapolation to about 12-13 digits of z_c; multiprecision eigen-solvers are mandatory beyond that.
- The Guo-Blote paper is not on arXiv; quote its value from the paper or from Lyu's reference list, not from secondary rounding.

## Sources

- https://arxiv.org/abs/2603.25492
- https://arxiv.org/abs/cond-mat/9703176
- https://doi.org/10.1103/PhysRevE.66.046140
- https://arxiv.org/abs/cond-mat/9811264
- Status source: https://arxiv.org/abs/2603.25492

## Citations

- [Problem page](../../../../.raw/V3R1T4S/known-unknowns/physics/hard-square-critical-activity-digits.md)
- [Bank entry](../../../../.raw/V3R1T4S/bank/targets.json) (id `hard-square-critical-activity-digits`, commit `7dd4480`)

## Related Nodes

- [[V3R1T4S Physics]]
- [[V3R1T4S]]
