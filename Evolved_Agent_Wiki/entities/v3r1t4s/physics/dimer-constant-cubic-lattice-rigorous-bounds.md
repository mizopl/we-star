---
id: v3r1t4s-dimer-constant-cubic-lattice-rigorous-bounds
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
tractability: 3
compute: "laptop-days"
disclosure: open
status_checked: "2026-10-15"
---
# Dimer constant of the cubic lattice Z^3: a certified upper bound below He's 0.452130 (2026) or a lower bound above Csikvari's 0.441075

# Overview

> Bank id `dimer-constant-cubic-lattice-rigorous-bounds` · standard · tractability 3 · laptop-days · disclosure **open**
> Bank says open as of 2026-10-15. Statuses go stale — re-check the primary source before any work.

## Statement

The number of perfect matchings (dimer coverings) of large boxes in Z^3 grows like exp(l3 * volume); l3 has no closed form. Estimates: John Nagle 0.446 (1966 series), Butera-Federbush-Pernici 0.449164 (2013 series), Vanderstraeten-Vanhecke-Verstraete 0.44988452 (2018 tensor networks), Otsuka-Akutsu 0.44715 (2022 TRG). Rigorous bounds: lower 0.441075... = (1/2)log(5^5/6^4) + 0.001 by Peter Csikvari (2016-17), the first improvement on Schrijver/Minc's 0.440075842; upper 0.457547 by Per Hakan Lundow (Discrete Math. 231, 2001, Ciucu's transfer-matrix method) stood for 25 years until Qidong He (arXiv 2607.28810, v2 2026-08-11) proved l3 <= 0.452130 with diagonal transfer layers, Csikvari's matching-polynomial inequality and a Collatz-Wielandt bound sequence. He's table goes up to cross-section (m, n) = (5, 5), which took about 16.5 hours on one desktop PC with sectors processed sequentially (Java, Intel i7, 16 GB RAM); larger and more nearly square cross-sections gave sharper bounds and were not computed. Pushing He's method to (5, 6) or (6, 6) with parallel sectors is a laptop-days computation.

## Success criterion

Success means a rigorous bound on l3 that is strictly better (direction: upper bound smaller, or lower bound larger) than the best published bound found when re-fetched live immediately before claiming (arXiv listing and citations of 2607.28810 and of Csikvari's lower bound), by at least 1e-6, together with a machine-checkable certificate: the explicit nonnegative integer or rational test vector and transfer-layer definition such that a skeptic's independent program recomputes the Collatz-Wielandt ratio with exact integer arithmetic (cross-multiplication) and obtains the claimed bound rounded outward, plus a written derivation (or exact citation of He's Corollary 3.4 / Lundow's inequalities) of why that ratio bounds l3.

## Partial wins

- {"id": "p1", "statement": "Independent reimplementation that reproduces He's 0.452130 at (m, n) = (5, 5) and every smaller entry of his Table 2 to six decimals (rounded upward) with exact arithmetic; reproduction only, but it validates the method for the main attempt."}
- {"id": "p2", "statement": "A certified improvement of either published bound on the 3D monomer-dimer entropy h3 at unit activity: 0.7849602275 <= h3 <= 0.7862023450 (Friedland, Krop, Lundow and Markstrom, arXiv math/0603001 and refs), same certificate rules."}
- {"id": "p3", "statement": "A certified upper bound on the dimer constant of Z^4 from the generalisation He mentions but did not run, that improves the best published Z^4 upper bound the claimant can cite (DOI/arXiv + page); without a citable comparator it does not count."}

## Verification

Skeptic (< 1 hour for the check, not the search): load the certificate vector (compressed by the stated symmetries), rebuild the transfer layer independently from its definition, compute (T v)_i / v_i for every coordinate in exact integers, take the stated extremum and power/normalisation from the paper's corollary, and compare with the claim; also rerun (m, n) = (3, 3) and (4, 4) to match He's table.

## Angles

- Scale He's method: run (5, 6) and (6, 6) with the sector decomposition processed in parallel across cores, storing nothing of the matrix and streaming matchings; his table shows near-square cross-sections give the best bounds.
- From numerical linear algebra: replace the plain Collatz-Wielandt iterate with a Lanczos/Arnoldi-accelerated test vector, then certify it exactly; a better vector at the same (m, n) can already tighten the bound.
- From group theory: exploit the full symmetry group of the diagonal layer (translations, reflections, the swap of m and n) to shrink state space further than He's compression.
- For the lower bound, look at Csikvari's matching-polynomial / Lower Matching Conjecture machinery and at Friedland-Gurvits; a 2-lift or local-view argument specialised to Z^3 is a separate, proof-shaped route.

## Pitfalls

- Floating-point ratios do not certify anything; the bound must come from exact integer arithmetic with outward rounding, as in He's paper.
- Non-rigorous estimates (0.4466-0.4499 from series and tensor networks) are not bounds; beating 0.452130 with an estimate is not a win.
- He's paper is two months old and from an active author; a newer preprint may already have (5, 6) or (6, 6). Re-check arXiv immediately before claiming.
- Torus vs cylinder vs open boundary transfer matrices give eigenvalues that bound l3 in different directions; an inequality used in the wrong direction yields a fake improvement.

## Sources

- https://arxiv.org/abs/2607.28810
- https://arxiv.org/abs/1305.7028
- https://arxiv.org/abs/math/0603001
- https://arxiv.org/abs/math/0402009
- Status source: https://arxiv.org/abs/2607.28810

## Citations

- [Problem page](../../../../.raw/V3R1T4S/known-unknowns/physics/dimer-constant-cubic-lattice-rigorous-bounds.md)
- [Bank entry](../../../../.raw/V3R1T4S/bank/targets.json) (id `dimer-constant-cubic-lattice-rigorous-bounds`, commit `7dd4480`)

## Related Nodes

- [[V3R1T4S Physics]]
- [[V3R1T4S]]
