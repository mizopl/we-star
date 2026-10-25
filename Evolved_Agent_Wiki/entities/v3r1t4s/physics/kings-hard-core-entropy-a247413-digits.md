---
id: v3r1t4s-kings-hard-core-entropy-a247413-digits
type: entity
tags: [v3r1t4s, v3r1t4s/physics, kind/harvest]
inbound_links: 1
confidence: 0.8
last_ingested_sources: [".raw/V3R1T4S/bank/targets.json@7dd4480"]
status: "open"
priority: ""
notes: ""
category: physics
kind: harvest
tractability: 3.5
compute: "laptop-hours"
disclosure: open
status_checked: "2026-10-15"
---
# Non-attacking kings (hard-core gas with diagonal exclusion) at unit activity: more correct digits of the entropy constant OEIS A247413

# Overview

> Bank id `kings-hard-core-entropy-a247413-digits` · harvest · tractability 3.5 · laptop-hours · disclosure **open**
> Bank says open as of 2026-10-15. Statuses go stale — re-check the primary source before any work.

## Statement

The lattice gas on the square lattice in which occupied sites may not be nearest or diagonal neighbours (equivalently independent sets of the king graph, non-attacking kings, or tilings by 1x1 and 2x2 squares, OEIS A063443) has, at activity 1, entropy constant 1.34264395112460129... OEIS A247413 (keyword 'more') lists 18 digits; digits a(14)-a(18) were computed by Kai Liang with tensor-network contraction (arXiv 2505.12776, v2 2025-06-23) and added on 2025-10-24, with stated bounds 1.34264395112460129 7851 <~ e^kappa < 1.34264395112460129 8092. Earlier values: Calkin-Wilf and Herbert Wilf (1995-98), Calkin-James-Purvis (2006), and Finch's quoted bracket 1.34254-1.34265. Unit activity is far below this model's columnar-ordering transition (critical activity about 97.5 in Monte Carlo studies), so the transfer matrix has a large gap and corner-transfer-matrix or boundary-MPS methods should converge exponentially. Eighteen digits is a modest bar for a laptop with arbitrary precision.

## Success criterion

Success means a decimal value of the A247413 constant with D decimals, D >= (number of terms in A247413 DATA, re-fetched live immediately before claiming) + 4, such that (a) two independent methods (for example CTM adapted to next-nearest-neighbour exclusion via 2x2 block spins, and exact strip transfer matrices with sequence extrapolation) agree on all D decimals, (b) both reproduce the 18 published digits, (c) the digits are stable over at least three increases of the truncation parameter, and (d) a literature/OEIS search finds no published value with D or more decimals. Direction: more digits.

## Partial wins

- {"id": "p1", "statement": "Rigorous two-sided bounds on the A247413 constant certifying at least 12 correct decimals, from Calkin-Wilf-type inequalities on cylinder and torus transfer matrices evaluated in exact arithmetic, with the Collatz-Wielandt certificate vectors published."}
- {"id": "p2", "statement": "The boundary (surface) free-energy coefficient of the king-graph model with free boundaries, which Kai Liang estimates in arXiv 2505.12776, to at least 4 more decimals than his published estimate, by two independent methods (note: the hard-core gas on the triangular lattice is the exactly solved hard-hexagon model and is not a target)."}

## Verification

Skeptic (< 1 hour): rerun both programs at the claimant's largest and second-largest truncations in arbitrary precision; confirm digit agreement and that the first 18 decimals equal A247413 fetched live; confirm the mapping (kings on (n-1)x(n-1) equals 1x1/2x2 tilings of n x n) by reproducing A063443 terms for n <= 12 with the same transfer code.

## Angles

- Block-spin CTM: group 2x2 cells into one super-site so the king constraint becomes a nearest-neighbour constraint between blocks, then run Baxter's CTM equations in arbitrary precision.
- From quantum information: the transfer matrix is a matrix-product operator with small bond dimension; VUMPS or a high-precision boundary-MPS power iteration gives an independent second method.
- From signal processing: strip free energies converge like exp(-L/xi); fit the exponential corrections (Prony-style) instead of plain Richardson, which shortens the widths needed.
- Use the tiling picture (A063443): a column-by-column 1x1/2x2 tiling transfer matrix has a different state space from the king-graph one, so agreement between the two is a strong internal check.

## Pitfalls

- Liang's last digits come from tensor-network bounds with an empirical component; reproduce the 18 digits but do not treat agreement in the tail beyond them as confirmation of anything.
- Floating-point eigen-solvers saturate at about 16 digits; claims beyond that need multiprecision throughout.
- Different boundary conditions (free, cylinder, torus) give different finite-size constants; only the bulk limit is the target, and finite-size 'constants' must not be reported as digits.
- OEIS A247413 is kappa = e^(entropy) per site; reporting ln(kappa) or the per-2x2-block value gives a different number.

## Sources

- https://oeis.org/A247413
- https://arxiv.org/abs/2505.12776
- https://oeis.org/A063443
- https://arxiv.org/abs/math/9810155
- https://arxiv.org/abs/2507.04007
- Status source: https://oeis.org/A247413

## Citations

- [Problem page](../../../../.raw/V3R1T4S/known-unknowns/physics/kings-hard-core-entropy-a247413-digits.md)
- [Bank entry](../../../../.raw/V3R1T4S/bank/targets.json) (id `kings-hard-core-entropy-a247413-digits`, commit `7dd4480`)

## Related Nodes

- [[V3R1T4S Physics]]
- [[V3R1T4S]]
