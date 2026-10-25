---
id: v3r1t4s-erdos757-sidon-in-45-sets
type: entity
tags: [v3r1t4s, v3r1t4s/record-tables, kind/harvest]
inbound_links: 1
confidence: 0.8
last_ingested_sources: [".raw/V3R1T4S/bank/targets.json@7dd4480"]
status: "open"
priority: ""
notes: ""
category: record-tables
kind: harvest
tractability: 3
compute: "laptop-hours"
disclosure: open
status_checked: "2026-10-03"
---
# Erdos #757: (4,5)-set with Sidon density below 4/7

# Overview

> Bank id `erdos757-sidon-in-45-sets` · harvest · tractability 3 · laptop-hours · disclosure **open**
> Bank says open as of 2026-10-03. Statuses go stale — re-check the primary source before any work.

## Statement

Let c* be the largest constant such that every (4,5)-set A of reals (every 4-element subset determines at least five distinct values among its six pairwise absolute differences) of size n contains a Sidon subset of size >= c* n. Ma-Tang (arXiv:2602.23282) give 9/17 (about 0.5294) <= c* <= 4/7 (about 0.5714); the 4/7 witness is A = {0,136,200,243,246,249,272,286,298,323,400,528,596,1056} (|A|=14, max Sidon subset 8, independently re-checked by the auditor on 2026-10-03). The bank research attributes to Ma-Tang the identity c* = inf_n f(n)/n (f(n) = min over (4,5)-sets of size n of the largest Sidon subset); the auditor flags that this attribution, or the blow-up lemma (a disjoint generic union of dilated copies stays (4,5) and its Sidon number adds), must be confirmed in the paper before a finite witness is read as a new upper bound on c*. Given that, ONE finite (4,5)-set with s/|A| < 4/7 improves the upper bound; e.g. |A|=16 with s=9, |A|=18 with s=10, |A|=23 with s=13, |A|=25 with s=14.

## Success criterion

Success means a finite set A of distinct integers with all of the following. (1) Every 4-subset has at least 5 distinct absolute differences, checked exhaustively. (2) The exact maximum Sidon subset size s(A) is certified by two independent exact methods (bitmask branch-and-bound and an ILP that forbids every a+b=c+d, including a=b, i.e. 3-APs). (3) The ratio s/|A|, compared in fractions.Fraction, is STRICTLY SMALLER (direction: min) than the best upper bound on c* shown at verification time at https://www.erdosproblems.com/757, on the EinsteinArena 'Sidon Subsets of (4,5)-Sets' leaderboard and in any newer arXiv paper (context: 4/7 on 2026-10-03; a ratio exactly equal to the live best is not a success). (4) s/|A| >= 9/17; a ratio below 9/17 contradicts a theorem and means a bug, never a claim. (5) The verifier confirms in arXiv:2602.23282 the lemma that a finite witness bounds c* (the blow-up lemma or the inf-formula), or else re-derives it. (6) The checker reproduces s=8 on the Ma-Tang 14-set as a calibration test.

## Partial wins

- {"id": "p1", "statement": "A new extremal witness: a (4,5)-set A with |A| NOT a multiple of 14 (e.g. |A| = 21 with s = 12) whose certified exact maximum Sidon subset gives s/|A| exactly equal to the live best ratio (4/7 on 2026-10-03), verified by the same two-method pipeline. Disjoint unions of dilated copies of the Ma-Tang 14-set only reach multiples of 14, so this is a structurally new extremal example."}
- {"id": "p2", "statement": "A frozen abstract target: an explicit 3-uniform hypergraph H on n vertices that satisfies every structural property arXiv:2602.23282 proves for 3-AP hypergraphs of (4,5)-sets (linear, F7-free, at most n-2 edges, and any further listed condition, each checked by script against the paper), with exact independence number alpha(H) and alpha(H)/n strictly below the live best ratio. The skeptic must confirm that the paper does not already exhibit or exclude such an H."}

## Verification

Use an independent script. (a) Run the C(n,4) (4,5) check. (b) Compute the exact max Sidon subset by exhaustive bitmask search for n <= 26, or with B&B plus a pulp/CBC ILP (all 3-AP and a+b=c+d constraints) and require agreement. (c) Calibrate on {0,136,200,243,246,249,272,286,298,323,400,528,596,1056}, which must give (4,5)=True and s=8. (d) Do the rational comparison. (e) Check the live arena and erdosproblems page.

## Angles

- Use the hypergraph view. For (4,5)-sets, the Sidon number equals the independence number of the 3-AP hypergraph H(A), which Ma-Tang show is linear and F7-free with m <= n-2 edges. Search over abstract linear 3-uniform hypergraphs with small independence ratio that satisfy those constraints, then realize them as integer sets with an ILP or SMT over integer coordinates.
- Glue copies of the 14-element witness along shared elements, or overlay two dilated copies so that APs share points. Look for configurations where the extra shared vertices push alpha(H)/n below 4/7.
- Simulated annealing over integer sets in [0, 5000]. Score = max Sidon size / n plus a penalty for (4,5) violations. Do incremental (4,5) checking with difference-multiset counters and exact Sidon computation via fast bitset branch-and-bound.
- Since c* = inf f(n)/n, aim at n in {16,18,23,25,30} and the s values that would beat 4/7. Use the Henning-Yeo transversal bound (17 tau <= 5n + 3m) to see which (n,m) are even possible before searching.
- Use AP-rich seeds: unions of short APs with carefully perturbed common differences, Sidon-like scaffolds (Singer sets) with planted 3-APs, and the Ma-Tang base set as a seed for local moves.
- Before searching, use the Henning-Yeo transversal bound and Ma-Tang's structural constraints to list which (n, m, s) are combinatorially possible, and then target only those n (auditor note: Ma-Tang presumably searched small n themselves).

## Pitfalls

- Getting the definition wrong. The erdosproblems summary paraphrases it confusingly. Use the Ma-Tang definition exactly: 6 absolute differences, at least 5 distinct.
- Floating-point reals. Use integers only, so equality of differences is exact.
- Counting Sidon too loosely. Sidon must also forbid a+a=b+c (3-APs), and that is the key obstruction here.
- A heuristic max-independent-set gives only a lower bound on s, which can understate s and fake a win. The maximum must be certified exactly.
- Ratio below 9/17 means a bug (contradicts a theorem).
- EinsteinArena now hosts this problem, so check the leaderboard right before claiming. An arena entry may beat 4/7 without an arXiv paper.
- A ratio s/n < 4/7 but with s/n not a new infimum relative to arena submissions is not a record.

## Sources

- https://arxiv.org/html/2602.23282
- https://www.erdosproblems.com/757
- https://teorth.github.io/optimizationproblems/constants/5b.html
- https://einsteinarena.com/
- Status source: https://arxiv.org/html/2602.23282

## Citations

- [Problem page](../../../../.raw/V3R1T4S/known-unknowns/record-tables/erdos757-sidon-in-45-sets.md)
- [Bank entry](../../../../.raw/V3R1T4S/bank/targets.json) (id `erdos757-sidon-in-45-sets`, commit `7dd4480`)

## Related Nodes

- [[V3R1T4S Record tables]]
- [[V3R1T4S]]
