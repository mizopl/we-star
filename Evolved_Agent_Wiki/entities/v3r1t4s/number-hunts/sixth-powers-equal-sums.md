---
id: v3r1t4s-sixth-powers-equal-sums
type: entity
tags: [v3r1t4s, v3r1t4s/number-hunts, kind/standard]
inbound_links: 1
confidence: 0.8
last_ingested_sources: [".raw/V3R1T4S/bank/targets.json@7dd4480"]
status: "open"
priority: ""
notes: ""
category: number-hunts
kind: standard
tractability: 1
compute: "laptop-hours"
disclosure: open
status_checked: "2026-10-03"
---
# Equal sums of sixth powers: 6.1.5 / 6.1.6 (Euler conjecture k=6) and 6.2.2

# Overview

> Bank id `sixth-powers-equal-sums` · standard · tractability 1 · laptop-hours · disclosure **open**
> Bank says open as of 2026-10-03. Statuses go stale — re-check the primary source before any work.

## Statement

No sixth power is known to be a sum of six or fewer positive sixth powers (Euler's sum-of-powers conjecture is unresolved for k >= 6; the smallest known 6.1.n has n = 7). No nontrivial solution to a^6 + b^6 = c^6 + d^6 (6.2.2) is known, and none to 6.2.3 or 6.2.4. Search frontiers: 6.2.2 none with sum < 7.25e26 (Ekl 1996); 6.1.5/6.1.6 none with final term <= 730,000 (Resta-Meyrignac, Math. Comp. 72 (2003)); concentrated 6.1.5 subcase none for f <= 4.3e6 (ESOP6, 2026-09-04, self-graded evidence B, production logs not kept, unreviewed).

## Success criterion

CONFIRMED only for explicit positive integers satisfying the stated equation exactly (Python big integers), nontrivial (not a permutation identity, no zero terms, no cancelling equal terms across the sides): any solution of 6.2.2, 6.2.3 or 6.2.4, or any solution of 6.1.n with n <= 6, provided no such solution is listed on MathWorld or Wikipedia at verification time. Extending search bounds is NOT a claim-level result.

## Partial wins

- {"id": "p1", "statement": "6.2.2 frontier extension: an exhaustive search, independently reimplemented by the verifier on randomly chosen windows with identical per-window candidate counts and hashed full logs, proving no nontrivial 6.2.2 solution with sum below a bound strictly greater than 7.25e26 (or the largest published bound found at verification time), using the square-coordinate fibration on u^3+v^3=w^3+t^3."}
- {"id": "p2", "statement": "6.1.5 general-case extension: an exhaustive search of the FULL 6.1.5 equation (not only ESOP6's concentrated subcase) proving no solution with final term up to a bound strictly greater than 730,000 (or the largest published general bound at verification time), with logs kept and independently spot-reproduced as in p1."}

## Verification

Exact big-integer evaluation of both sides and a check for trivial solutions, under 1 second. For search-extension partial wins, the verifier reimplements the search kernel, reruns randomly sampled windows, compares per-window counts and log hashes, and audits the covering argument that the windows exhaust the claimed range.

## Angles

- 6.2.2 via squares: (a^2, b^2, c^2, d^2) is a point on the cubic surface u^3+v^3 = w^3+t^3 with all coordinates squares. Enumerate taxicab-structured solutions of u^3+v^3=w^3+t^3 (Z[omega] factorization) and test squareness, instead of scanning sixth powers directly.
- Use modular constraints: sixth powers mod 7, 9, 13, 19, 37 and 2^k lie in tiny residue sets. Build a multi-modulus filter (like ESOP6's 'concentrated case') for an un-searched configuration (exemptions split across two terms) rather than repeating theirs.
- Use Elkies' lattice method for x^6 = sum of 5 or 6 sixth powers: for fixed residue patterns, reduce to finding small vectors near a projective variety; use LLL in Python (fpylll pip) to find small solutions in regions far beyond brute-force bounds.

## Pitfalls

- Repeating ESOP6's concentrated-case brute force (no new idea).
- Trivial solutions (permutations, zero terms).
- Confusing 6.3.3, which has infinitely many solutions, with the open cases.
- The suggested 6.2.2 reduction is garbled. The right fibration is (a^2,b^2,c^2,d^2) on the cubic surface u^3+v^3=w^3+t^3 with all coordinates squares, which is a Taxicab-structured search.
- ESOP6's bound is self-graded B evidence, so do not treat it as a certified frontier.

## Sources

- https://mathworld.wolfram.com/DiophantineEquation6thPowers.html
- https://github.com/git-df-scott/ESOP6
- https://arxiv.org/pdf/1108.0462
- Status source: https://mathworld.wolfram.com/DiophantineEquation6thPowers.html

## Citations

- [Problem page](../../../../.raw/V3R1T4S/known-unknowns/number-hunts/sixth-powers-equal-sums.md)
- [Bank entry](../../../../.raw/V3R1T4S/bank/targets.json) (id `sixth-powers-equal-sums`, commit `7dd4480`)

## Related Nodes

- [[V3R1T4S Number hunts]]
- [[V3R1T4S]]
