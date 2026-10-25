---
id: v3r1t4s-lehmer-totient
type: entity
tags: [v3r1t4s, v3r1t4s/number-hunts, kind/moonshot]
inbound_links: 1
confidence: 0.8
last_ingested_sources: [".raw/V3R1T4S/bank/targets.json@7dd4480"]
status: "open"
priority: ""
notes: ""
category: number-hunts
kind: moonshot
tractability: 1
compute: "pure thought"
disclosure: open
status_checked: "2026-10-03"
---
# Lehmer's totient problem: composite n with phi(n) | n - 1

# Overview

> Bank id `lehmer-totient` · moonshot · tractability 1 · pure thought · disclosure **open**
> Bank says open as of 2026-10-03. Statuses go stale — re-check the primary source before any work.

## Statement

Is there a composite n with phi(n) dividing n - 1? Any such n is odd and squarefree. Known computational bounds: omega(N) >= 15 and N > 10^26 (Renze, computational notebook, cited in Yamada arXiv 2303.16853); Pinch claims N > 10^30. If 3 | N: omega(N) >= 4*10^7 and N > 10^(3.6*10^8) (Burcsi-Czirbusz-Farkas 2011). A 2025 preprints.org paper claiming elimination of 14-prime composites and a 'GRH-density resolution' is unreviewed and treated as unverified.

## Success criterion

Full resolution CONFIRMED only with a Lean-formalized proof (no sorry, clean axiom audit), or an explicit composite n with phi(n) | n-1 verified via a complete prime factorization (every factor proven prime). Computational bound improvements are partial wins, judged against the best bounds stated at https://arxiv.org/pdf/2303.16853 and https://en.wikipedia.org/wiki/Lehmer%27s_totient_problem AT VERIFICATION TIME; reproducing omega >= 15 is a regression test, not a result. Unreviewed preprints claiming resolution never count.

## Partial wins

- {"id": "p1", "statement": "omega(N) >= 16: a rigorous, exhaustive computer proof, independently reimplemented by the verifier with identical branch-closure reasons on every branch, using exact rational arithmetic for every product p/(p-1) bound."}
- {"id": "p2", "statement": "Certified N > 10^30: a rigorous, exhaustive, independently reimplemented computer proof that any Lehmer number exceeds 10^30 (certifying Pinch's uncertified claim), or a strictly larger bound, with a published branch log."}

## Verification

The verifier first reproduces Cohen-Hagis omega >= 14 and Renze's omega >= 15 as regressions. It then independently reimplements the branch-and-bound over increasing prime tuples using the Lehmer constraints (N odd and squarefree, p_i does not divide p_j - 1, and the condition on prod p/(p-1) with exact rationals) and diffs the branch-closure logs. For a counterexample: factor n, compute phi(n) exactly, and check divisibility.

## Angles

- Branch-and-bound over increasing prime tuples in the style of Cohen-Hagis/Renze (N odd, squarefree, p_i not dividing p_j - 1, exact-rational bounds on prod p/(p-1)), parallelized on the 10 cores, aiming at a reproducible full branch log for omega = 15 -> 16.
- Combine with Carmichael structure: any Lehmer number is a Carmichael number with extra constraints. Use Pinch's Carmichael tables to test structural conjectures quickly (sanity, not proof).
- Use p-adic overflow constraints (as in the 2025 preprint) but derive them rigorously and check every claimed lemma symbolically.

## Pitfalls

- Unreviewed preprints claiming resolution.
- Floating-point products of p/(p-1) in branch bounds; use exact rationals.
- Confusing Lehmer's totient problem with Lehmer's Mahler-measure problem.
- ω ≥ 15 / N > 10^26 is already known (Renze), and Pinch claims N > 10^30.
- arXiv 2003.13055 (Agama) is not a usable branch-and-bound method. Do not build on it.

## Sources

- https://en.wikipedia.org/wiki/Lehmer%27s_totient_problem
- https://math.dartmouth.edu/~carlp/Carmichael_giuga.pdf
- https://arxiv.org/pdf/2303.16853
- Status source: https://en.wikipedia.org/wiki/Lehmer%27s_totient_problem

## Citations

- [Problem page](../../../../.raw/V3R1T4S/known-unknowns/number-hunts/lehmer-totient.md)
- [Bank entry](../../../../.raw/V3R1T4S/bank/targets.json) (id `lehmer-totient`, commit `7dd4480`)

## Related Nodes

- [[V3R1T4S Number hunts]]
- [[V3R1T4S]]
