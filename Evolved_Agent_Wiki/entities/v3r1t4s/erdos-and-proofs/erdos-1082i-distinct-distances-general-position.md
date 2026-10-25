---
id: v3r1t4s-erdos-1082i-distinct-distances-general-position
type: entity
tags: [v3r1t4s, v3r1t4s/erdos-and-proofs, kind/harvest]
inbound_links: 1
confidence: 0.8
last_ingested_sources: [".raw/V3R1T4S/bank/targets.json@7dd4480"]
status: "open"
priority: ""
notes: ""
category: erdos-and-proofs
kind: harvest
tractability: 2
compute: "laptop-hours"
disclosure: open
status_checked: "2026-10-03"
---
# Erdos #1082(i): n points, no three collinear, with fewer than floor(n/2) distinct distances

# Overview

> Bank id `erdos-1082i-distinct-distances-general-position` · harvest · tractability 2 · laptop-hours · disclosure **open**
> Bank says open as of 2026-10-03. Statuses go stale — re-check the primary source before any work.

## Statement

Does every set of n points in the plane with no three collinear determine at least floor(n/2) distinct distances? Part (ii) (a single point seeing floor(n/2) distances) has been disproved: Harborth's 8-point example, and 42-point examples by eigensolver and Xichuan. Part (i) remains open. The forum (sallerk, 2026-08-31) proves it for all n <= 15 using bounds on g(k). Altman 1963: points in convex position always give >= floor(n/2) distances, so any counterexample must be non-convex. The smallest possible counterexample is 16 points with 7 distances; g(7) (max points with 7 distances) is unknown.

## Success criterion

An explicit set of n >= 16 pairwise-distinct points with exact coordinates (integers, rationals, or elements of an explicitly specified number field such as Q(sqrt3), Q(cos(2pi/m))), no three collinear, determining strictly fewer than floor(n/2) distinct distances under exact arithmetic. n must exceed the verified range listed on the forum at verification time (n <= 15 as of 2026-10-03). Distances are compared via canonical exact representations, not printed expressions.

## Partial wins

- {"id": "p1", "statement": "A rigorous, independently reproducible proof (computer-assisted allowed, with both implementations rerun by the verifier) that every set of 16 points in the plane with no three collinear determines at least 8 distinct distances, extending the forum's n <= 15."}
- {"id": "p2", "statement": "The same rigorous verification for all n up to 20."}

## Verification

Compute all C(n,2) squared distances exactly (sympy in the specified field, canonicalised by minimal polynomial or a basis representation) and count distinct values. Check all C(n,3) orientation determinants are exactly nonzero. Independent cross-check: 100-digit mpmath evaluation; the distance clusters must match the exact count, with the gap between clusters far larger than precision.

## Angles

- Two or three concentric regular m-gons, possibly plus the centre (the family that killed part ii). Treat the radius ratio rho and rotation phi as unknowns and solve the polynomial equations that merge distance classes, using resultants or Groebner bases in sympy. Each merge is an algebraic condition, so look for rho that merges many at once.
- Subsets of the Eisenstein or Gaussian lattice in general position: take lattice points on a few norm circles (x^2+xy+y^2 = N with many representations) plus interior points chosen so all differences have norms in a tiny set.
- Start from Erdos-Fishburn / Wei maximal k-distance sets (g(k) for small k) and study which collinear triples block them. Delete or move points to break collinearity while preserving distance classes.
- Exact search: an integer program over candidate points from a finite ring, with constraints 'no three collinear' and 'distance set within a chosen set D', solved by CP-SAT.

## Pitfalls

- Convex-position constructions cannot work (Altman 1963).
- Float tolerance merging distinct distances.
- Mixing up part (ii) (per-point distances, already disproved) with part (i) (total distances).
- n <= 15 is already proved.
- Ensure pairwise-distinct points; a duplicated point trivially lowers the distance count.
- Squared distances in a number field must be compared via canonical basis coordinates (or exact zero tests of differences), not by printing sympy expressions.

## Sources

- https://www.erdosproblems.com/1082
- https://www.erdosproblems.com/forum/thread/1082
- https://www.erdosproblems.com/982
- https://github.com/google-deepmind/formal-conjectures/blob/main/FormalConjectures/ErdosProblems/1082.lean
- Status source: https://www.erdosproblems.com/1082

## Citations

- [Problem page](../../../../.raw/V3R1T4S/known-unknowns/erdos-and-proofs/erdos-1082i-distinct-distances-general-position.md)
- [Bank entry](../../../../.raw/V3R1T4S/bank/targets.json) (id `erdos-1082i-distinct-distances-general-position`, commit `7dd4480`)

## Related Nodes

- [[V3R1T4S Erdős problems and proofs]]
- [[V3R1T4S]]
