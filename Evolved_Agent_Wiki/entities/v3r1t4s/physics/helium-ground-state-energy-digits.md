---
id: v3r1t4s-helium-ground-state-energy-digits
type: entity
tags: [v3r1t4s, v3r1t4s/physics, kind/moonshot]
inbound_links: 1
confidence: 0.8
last_ingested_sources: [".raw/V3R1T4S/bank/targets.json@7dd4480"]
status: "open"
priority: ""
notes: ""
category: physics
kind: moonshot
tractability: 1
compute: "laptop-days"
disclosure: open
status_checked: "2026-10-15"
---
# MOONSHOT - Helium atom nonrelativistic ground-state energy: more correct digits than Schwartz's 2006 record

# Overview

> Bank id `helium-ground-state-energy-digits` · moonshot · tractability 1 · laptop-days · disclosure **open**
> Bank says open as of 2026-10-15. Statuses go stale — re-check the primary source before any work.

## Statement

The nonrelativistic, infinite-nuclear-mass ground-state energy of helium is the benchmark three-body Coulomb eigenvalue. Charles Schwartz (arXiv:math-ph/0605018, 2006) used a Hylleraas-type basis with negative powers and a logarithmic term, up to order 50 (24,099 terms), obtaining E = -2.90372 43770 34119 59831 11592 45194 40444 66969 25309... hartree (about 46 significant digits, the last ones by extrapolation). Later work (Hiroyuki Nakashima and Hiroshi Nakatsuji 2007, about 40 digits; Alexei Frolov's exponential expansions 2018, 27-35 digits; Hylleraas-B-spline work 2019) has not surpassed it, and a 2024 Canadian Journal of Physics paper on H- basis sets still calls Schwartz's the most accurate three-body calculation. A rigorous variational upper bound with more converged digits is a checkable object: the Rayleigh quotient of an explicit trial function. Checked live 2026-10-15: arXiv abstract HTTP 200.

## Success criterion

Success means an explicit trial wavefunction (basis definition and coefficients, published as a file) whose Rayleigh quotient E_var, computed by the checker in exact or interval arithmetic, is STRICTLY LOWER (direction: min) than Schwartz's best variational (not extrapolated) eigenvalue as printed in arXiv:math-ph/0605018 re-fetched immediately before claiming, AND whose value agrees with Schwartz's extrapolated E* on every digit Schwartz reports as converged; the number of new digits claimed is the length of the prefix on which E_var and an extrapolation over at least three basis sizes agree beyond Schwartz's 46th significant digit.

## Partial wins

- {"id": "p1", "statement": "An independent open-source reproduction of at least 40 significant digits of the helium ground-state energy from an explicit trial function whose Rayleigh quotient the checker evaluates (no new digits; a published reproducible certificate, which Schwartz's paper does not provide)."}
- {"id": "p2", "statement": "A variational energy for the H- ground state (same nuclear-mass and nonrelativistic conventions) lower than the best value in the 2024 Canadian Journal of Physics triple-basis paper and in any later paper found by a literature search."}

## Verification

Checker (minutes to a few hours depending on basis size): read the basis (Hylleraas powers, exponents, log terms) and coefficients; assemble the overlap and Hamiltonian matrices in python-flint arb ball arithmetic at precision >= (claimed digits + 20) using closed-form integrals; compute the Rayleigh quotient c^T H c / c^T S c with a rigorous error ball; confirm it lies strictly below Schwartz's printed variational value; compare digits with Schwartz's printed sequence.

## Angles

- Numerical-analysis import: replace dense generalized eigen-solves with inverse iteration in multiprecision using a low-precision factorisation as preconditioner (mixed-precision iterative refinement), so 24,000+ term bases fit in laptop memory.
- Basis design from singularity analysis: include Fock-expansion logarithmic terms (r^2 ln r near the triple-coalescence point) systematically; the slowest convergence comes from that singularity.
- Triple and multi-exponent Hylleraas bases (Drake's doubled basis idea) with exponents optimised in low precision and frozen before the high-precision run.
- Rigorous-numerics import: certify the Rayleigh quotient and add a Temple or Kato lower bound to bracket the eigenvalue, which also certifies the claimed digits.
- Compressed-sensing / sparse-basis import: prune basis functions with negligible coefficients after a low-precision solve to cut the high-precision cost.

## Pitfalls

- Conventions: infinite nuclear mass and no relativistic or QED terms; finite-mass energies (about -2.90330) or 'total energies' including corrections are different numbers.
- Schwartz's last digits are extrapolated; beating the extrapolated E* is impossible for a variational bound unless his extrapolation is wrong. The bar is his printed variational eigenvalue, and new digits need convergence evidence.
- Floating-point linear algebra at 100+ digits silently loses precision in near-singular overlap matrices; only ball/interval arithmetic results count.
- This is a moonshot: Schwartz needed a 24,099-term basis in high-precision arithmetic; budget laptop-days and stop early if a 40-digit reproduction (p1) is not reached quickly.

## Sources

- https://arxiv.org/abs/math-ph/0605018
- https://arxiv.org/abs/1810.11288
- https://arxiv.org/abs/physics/9912052
- https://doi.org/10.1139/cjp-2023-0277
- Status source: https://arxiv.org/abs/math-ph/0605018

## Citations

- [Problem page](../../../../.raw/V3R1T4S/known-unknowns/physics/helium-ground-state-energy-digits.md)
- [Bank entry](../../../../.raw/V3R1T4S/bank/targets.json) (id `helium-ground-state-energy-digits`, commit `7dd4480`)

## Related Nodes

- [[V3R1T4S Physics]]
- [[V3R1T4S]]
