---
id: v3r1t4s-saw-connective-constant-rigorous-bounds-2d
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
# Self-avoiding walks: a certified bound on the square-lattice connective constant beating Couronne's upper bound 2.662342426 (2022) or Jensen's lower bound 2.625622 (2004)

# Overview

> Bank id `saw-connective-constant-rigorous-bounds-2d` · standard · tractability 2 · laptop-days · disclosure **open**
> Bank says open as of 2026-10-15. Statuses go stale — re-check the primary source before any work.

## Statement

The square-lattice connective constant is estimated as mu = 2.63815853032790(3) (Jesper Jacobsen, Christian Scullard and Anthony Guttmann 2016; OEIS A387897, Wikipedia 'Connective constant'), but rigorous bounds are much looser. Upper: Olivier Couronne (arXiv 2211.16146, 2022) modified the finite-memory automaton of Andre Ponitz and Peter Tittmann (2000, 2.679193) and, with loops up to length 26 (one week, 32 GB), proved mu < 2.662342426. Lower: Iwan Jensen (arXiv cond-mat/0409381, J. Phys. A 2004) used Kesten's irreducible-bridge method to get mu > 2.625622. Jensen's Table 3 also lists rigorous brackets for the triangular (4.118935, 4.25152 by Sven Erick Alm), kagome (2.548497, 2.590301) and 4.8^2 (1.804596, 1.82926) lattices. Qidong He (J. Phys. A 58 (2025) 505003, arXiv 2508.01993) published open software (github.com/qidong-he/weighted_connective_constant) for Alm-type upper bounds on these lattices. Couronne's sequence of bounds (2.669575, 2.666665, 2.664196, 2.662342 for growing loop length) is still improving at the last step.

## Success criterion

Success means a rigorous bound on the square-lattice connective constant strictly better than the best published bound found by an arXiv/Google Scholar search re-run immediately before claiming (currently upper 2.662342426, lower 2.625622), by at least 1e-6, with a checkable certificate: for upper bounds, the automaton/transfer matrix definition plus a nonnegative test vector whose Collatz-Wielandt ratio is verified in exact or outward-rounded arithmetic; for lower bounds, the exact integer bridge counts used, with a program that recomputes the bound from them, and the counts reproducing Jensen's published values at all lengths he lists.

## Partial wins

- {"id": "p1", "statement": "A certified improvement, by at least 1e-6, of the best published rigorous bound for the triangular, kagome or 4.8^2 lattice (starting from Jensen 2004 Table 3; the claimant must show by search that no later bound beats theirs), same certificate rules."}
- {"id": "p2", "statement": "An independent reimplementation reproducing Couronne's 2.662342426 at loop length 26 (or his shorter-loop bounds) in less than his reported one week of computation; reproduction only, but it validates the code for the main attempt."}

## Verification

Skeptic: for an upper bound, rebuild the automaton from the stated loop list for a small loop length and match Couronne's or Ponitz-Tittmann's published value, then check the claimed certificate vector's ratios with exact arithmetic (minutes to hours depending on state count; the certificate can be checked by streaming). For a lower bound, recompute the bound from the supplied bridge counts and spot-check counts at small lengths by brute force.

## Angles

- Extend Couronne's automaton to loop length 28 with a compact state encoding and disk-backed sparse iteration; the bound sequence was still dropping about 1.9e-3 per two units of loop length.
- From formal languages: walks avoiding a finite set of short loops form a regular language; minimise the DFA (Hopcroft) and merge equivalent states before the eigenvalue step.
- From numerical linear algebra: certify with a Lanczos-improved test vector rather than plain power iteration; a better vector at the same automaton size gives a better certified ratio.
- Lower bound: Jensen's bridge counts can be extended with modern transfer-matrix code and modular arithmetic; Kesten's method converts every extra length directly into a bound.

## Pitfalls

- Estimates of mu (2.6381585303...) are not bounds; an 'upper bound' below 2.6381585 indicates a bug, not a record.
- Counting walks with finite memory overcounts only if the forbidden-loop set is applied consistently from both ends; an inconsistent automaton gives a too-small, invalid 'upper bound'.
- For hexagonal and 3.12^2 lattices the connective constant is known exactly (Duminil-Copin-Smirnov; A249776); bounds there are not open problems.
- Floating-point spectral radii are not certificates; outward rounding or exact arithmetic is required.

## Sources

- https://arxiv.org/abs/2211.16146
- https://arxiv.org/abs/cond-mat/0409381
- https://arxiv.org/abs/2508.01993
- https://github.com/qidong-he/weighted_connective_constant
- https://oeis.org/A387897
- https://en.wikipedia.org/wiki/Connective_constant
- Status source: https://arxiv.org/abs/2211.16146

## Citations

- [Problem page](../../../../.raw/V3R1T4S/known-unknowns/physics/saw-connective-constant-rigorous-bounds-2d.md)
- [Bank entry](../../../../.raw/V3R1T4S/bank/targets.json) (id `saw-connective-constant-rigorous-bounds-2d`, commit `7dd4480`)

## Related Nodes

- [[V3R1T4S Physics]]
- [[V3R1T4S]]
