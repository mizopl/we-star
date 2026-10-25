---
id: v3r1t4s-square-grid-lattice-gas-exact-counts-oeis
type: entity
tags: [v3r1t4s, v3r1t4s/physics, kind/harvest]
inbound_links: 1
confidence: 0.8
last_ingested_sources: [".raw/V3R1T4S/bank/targets.json@7dd4480"]
status: "CONFIRMED_PARTIAL"
priority: "1"
notes: "p1 WON: A054759(15) CONFIRMED_PARTIAL 2026-10-17 — see [[A054759(15) result]]. Next: L2 rectangular rows, L3 A027683(33)."
category: physics
kind: harvest
tractability: 3.5
compute: "laptop-hours"
disclosure: open
status_checked: "2026-10-15"
---
# Exact partition functions of lattice gases on n x n boards: the next term of OEIS A028420 (monomer-dimer), A006506 (hard squares), A063443 (kings/1x1-2x2 tilings), A054759 (square ice on the torus) or A027683 (hard squares on the torus)

# Overview

> Bank id `square-grid-lattice-gas-exact-counts-oeis` · harvest · tractability 3.5 · laptop-hours · disclosure **open**
> Bank says open as of 2026-10-15. Statuses go stale — re-check the primary source before any work.

## Statement

Exact unit-activity partition functions of classic lattice models on n x n boards are tabulated in OEIS and extended by a few people: A028420 (monomer-dimer coverings = all matchings of the n x n grid) b-file to n = 27 (Liang Kai; n <= 21 Jennifer Henry); A006506 (hard squares = independent sets of the n x n grid) b-file to n = 39 (Jin-Guo Liu; earlier terms Robert Gerbicz, Paolo Butera and Marco Pernici, Casey Mills Davis); A063443 (tilings by 1x1 and 2x2 squares = non-attacking kings) to n = 40 (Andrew Woods, Vaclav Kotesovec, Johan Nilsson); A054759 (Eulerian orientations of the n x n torus = square ice, six-vertex model at the ice point) to n = 14 (Brendan McKay, 2024-04-18); A027683 (independent sets of the n x n torus) to n = 32 (Rintaro Matsuo). All checked live 2026-10-15. Column-by-column transfer matrices with modular arithmetic (several 62-bit primes and Chinese remaindering) make the next term of A028420 (2^28 frontier states, about 226-digit answer) and A006506 (Fibonacci-many frontier states, F(42) = 2.7e8 at width 40) and A063443 (comparable) laptop-hours to laptop-days computations; A054759 is much easier and is listed as a partial win.

## Success criterion

Success means the exact integer value of the first unknown term a(N) of A028420, A006506 or A063443, where N is one more than the largest index in the sequence's DATA and b-file re-fetched live immediately before claiming, computed by two independent runs that agree exactly (different primes/CRT moduli sets AND a different decomposition, e.g. row vs column sweep or a different state encoding, or one exact big-integer run), with the same code reproducing every published term for n <= N-1 exactly, and the result consistent with the known growth constant (a(N)^(1/N^2) within 1e-3 of the corresponding entropy constant).

## Partial wins

- {"id": "p1", "statement": "The next unknown term(s) of A054759 (square ice on the n x n torus) or A027683 (hard squares on the n x n torus), same two-run and reproduction rules; A054759 is expected to be easy (row transfer matrix with 2^n states plus one tracked boundary edge) and is a partial only."}
- {"id": "p2", "statement": "A new row of an associated rectangular table (A210662 monomer-dimer m x n, A089980 hard squares m x n) extending the largest published m by one for all n up to the published range, same rules."}

## Verification

Skeptic (< 1 hour): rerun the claimant's program modulo one fresh 62-bit prime not used in the claim and check the residue of a(N); rerun for all n <= 20 and compare with the b-file; check digit count against the entropy-constant growth estimate. Full recomputation (hours) can follow the panel.

## Angles

- Broken-profile dynamic programming with one 32/64-bit counter per frontier state, run once per prime modulus (about 13 primes for a 226-digit A028420 term), parallel over primes across cores; memory is about 8 bytes x 2^28 per array for A028420(28).
- From signal processing / FFT practice: exploit the left-right reflection symmetry of the frontier to halve states, as Liang and Liu did with tensor-network contractions.
- From tensor networks (Jin-Guo Liu's GenericTensorNetworks approach): an exact contraction with an optimised order and big-integer or modular tensors is a genuinely independent second method.
- From number theory: random-prime residue checks (Freivalds-style) let a skeptic validate a 300-digit claim in minutes without redoing all primes.

## Pitfalls

- Offsets differ (A028420 starts at n = 0, A054759 at n = 1); a 'new' term at the wrong index is an existing one.
- Torus conventions for tiny n (multi-edges and loops at n = 1, 2) change the small terms; reproduce the published small terms before trusting the code.
- CRT with too few primes silently returns the value modulo the product; check the bound on a(N) (from the entropy constant) is below the modulus product with a wide margin.
- These sequences also fall under the bank's generic OEIS 'more' target; claims belong here only under this entry's two-run and reproduction rules. Some terms may sit in a pending OEIS edit; check the sequence's history page.

## Sources

- https://oeis.org/A028420
- https://oeis.org/A006506
- https://oeis.org/A063443
- https://oeis.org/A054759
- https://oeis.org/A027683
- https://arxiv.org/abs/2505.12776
- https://arxiv.org/abs/2507.04007
- Status source: https://oeis.org/A028420

## Citations

- [Problem page](../../../../.raw/V3R1T4S/known-unknowns/physics/square-grid-lattice-gas-exact-counts-oeis.md)
- [Bank entry](../../../../.raw/V3R1T4S/bank/targets.json) (id `square-grid-lattice-gas-exact-counts-oeis`, commit `7dd4480`)

## Related Nodes

- [[V3R1T4S Physics]]
- [[V3R1T4S]]
