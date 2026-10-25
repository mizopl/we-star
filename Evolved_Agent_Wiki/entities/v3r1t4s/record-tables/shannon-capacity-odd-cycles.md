---
id: v3r1t4s-shannon-capacity-odd-cycles
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
tractability: 2
compute: "laptop-hours"
disclosure: open
status_checked: "2026-10-03"
---
# Shannon capacity of odd cycles: larger independent sets in strong powers

# Overview

> Bank id `shannon-capacity-odd-cycles` · harvest · tractability 2 · laptop-hours · disclosure **open**
> Bank says open as of 2026-10-03. Statuses go stale — re-check the primary source before any work.

## Statement

An independent set S in the strong product C_m^{⊠d} gives Theta(C_m) >= |S|^(1/d). Improve the best known lower bound for Theta(C_m), m odd. For C7 this is Ben Green's open problem #38 (formal-conjectures GreensOpenProblems/38.lean): the largest A in F_7^d with (A-A) ∩ {-1,0,1}^d = {0}. Tao's optimization-constants repo lists Theta(C7) as constant C_9 (constants/9a.md). As of 2026-10-03: Theta(C7) >= 3.25883262... (Ravi Tandon, arXiv:2608.30273, 31 Aug 2026, heterogeneous recursion in C7^{⊠500}; cited on 9a.md under the key [Tan2026]), with other 2026 C7 values 3.25878915 (Gao, arXiv:2607.27869), 3.25880537 (Buys-Polak-Zuiddam, Lean-verified, arXiv:2607.29681) and 3.2580207 (Itty-Rosin-Carstensen-Reichman, 134,753 in C7^{⊠10}, arXiv:2607.21517). Buys-Polak-Zuiddam also give C11 >= 5.294502522, C13 >= 6.302455083, C15 >= 7.301600534, C19 >= 9.357192706, C21 >= 10.342455853, C23 >= 11.328224258, superseding Itty et al. X-evolve found an independent set of size 19,946 in C15^{⊠5}. The published alpha(C7^{⊠5}) baseline is 367 (Polak-Schrijver 2018, arXiv:1808.07438). EinsteinArena hosts 'Shannon Capacity C7^5: find 368 words' (arena best 367). Because 368^(1/5) ~ 3.259639 > 3.25883262 (equivalently record^5 ~ 367.545 < 368), a 368-element independent set in C7^{⊠5} would itself beat the capacity record; 367^(1/5) ~ 3.257866 does not.

## Success criterion

Capacity record: an explicit independent set S in C_m^{⊠d} (m odd; pairwise non-adjacent, verified exhaustively), or a fully specified recursive construction whose every finite ingredient is explicitly listed and verified and whose limiting rate is independently re-derived, giving a lower bound on Theta(C_m) (|S|^(1/d), computed with mpmath to 30 digits) STRICTLY GREATER (direction: max) than the best lower bound for that m at verification time: the max over the live primary table https://github.com/teorth/optimizationproblems/blob/main/constants/9a.md (C7 table; the other odd cycles are in its comments), arXiv:2608.30273, 2607.29681, 2607.27869, 2607.21517 and any newer arXiv result, using the record's exact digits. A finite-dimension set must beat the asymptotic record itself, not just an earlier fixed-dimension value. Against the 2026-10-03 C7 record 3.25883262... (recompute against the live record) this means |S| >= 368 in d=5, >= 1198 in d=6, >= 3904 in d=7, >= 12,721 in d=8, >= 41,454 in d=9, or >= 135,090 in d=10. In particular a verified 368-element independent set in C7^{⊠5} (the EinsteinArena target) IS a full capacity record, since 368^(1/5) ~ 3.259639 > 3.25883262; 367 (Polak-Schrijver 2018) gives only 3.257866. A fixed-d independence-number record below these thresholds is not claim-level.

## Partial wins

- {"id": "p1", "statement": "An explicit independent set in C7^{⊠10} of size strictly greater than the best published explicit C7^{⊠10} set at verification time (134,753, Itty-Rosin-Carstensen-Reichman 2026, arXiv:2607.21517, on 2026-10-03) but below the asymptotic threshold (135,090 at the 2026-10-03 record; larger sets are full successes), verified by an exhaustive pair check."}
- {"id": "p2", "statement": "An independent set in C15^{⊠5} of size strictly greater than X-evolve's 19,946 and any newer published value, verified exhaustively."}
- {"id": "p3", "statement": "A fixed-dimension independence record for another odd cycle: an independent set in C_m^{⊠d} (m odd, m >= 9) whose size strictly exceeds the best published alpha(C_m^{⊠d}) found at verification time (including the 2026 papers listed above), verified exhaustively."}

## Verification

Two distinct vectors x,y are adjacent iff for every coordinate i, (x_i - y_i) mod m is in {0,1,m-1}. Check all pairs by vectorized numpy, or bucket by coordinates to make it near-linear. Check all elements are distinct and in range. Compute |S|^(1/d) with mpmath to 30 digits and compare with the live record; equivalently check |S| > record^d exactly. For recursive constructions, rebuild the full set if its size is under ~1e8, or verify each gadget plus the composition lemma symbolically.

## Angles

- Search independent sets in C_m^{⊠d} that are invariant under a cyclic group (x -> x + v, or coordinate rotations). Reduce to max independent set on the quotient orbit graph, solved by CP-SAT.
- Extend Tandon's heterogeneous recursion: use different auxiliary independent sets at different recursion depths, optimized jointly by ILP over a small catalog of gadgets.
- Target the larger odd cycles C9, C17, C19 and C21, whose records may not have been touched in 2026, since most effort went to C7.
- Use linear codes over Z_m (lattice-based independent sets) as seeds, then local search to add points.
- Attack the EinsteinArena C7^{⊠5} 368 target with orbit-quotient CP-SAT. It is not just a stepping stone: 368^(1/5) ~ 3.25964 beats the capacity record, so 368 would be a full success. 367 has stood since Polak-Schrijver 2018, so expect it to be hard.
- Low dimensions with structure: search for A in F_7^6 (or F_7^7) invariant under a large group (coordinate permutations combined with multiplication by units), using exact cover / CP-SAT on orbits. 1198 in dimension 6 versus the trivial product 367*3 = 1101 is a crisp target.
- Local improvement of the published 134,753-element set in C_7^{⊠10}: delete-k / add-(k+1) swaps guided by conflict graphs, run in parallel on 10 cores.
- Better gadgets for the Gao/Tan recursions: search small heterogeneous blocks (mixing C_7^{⊠2}, C_7^{⊠3} and C_7^{⊠5} gadgets with 'valid tuple' compatibility) whose recursion eigenvalue beats Tan's. The rate is computable from a small transfer matrix.
- Algebraic constructions: images of codes over GF(7) or Z_49 under Lee-metric-like maps, and quadratic-residue / Paley-type sets in F_7^m.

## Pitfalls

- The capacity bound needs |S|^(1/d), not |S|/m^d. Check the exponent carefully.
- Confusing an independence-number record at fixed d with a capacity record.
- Several 2026 papers within weeks, so the record must be re-searched immediately before claiming.
- Four C7 papers appeared within five weeks (Jul-Aug 2026). Compare against all of them, not just Tandon.
- Exponent arithmetic: 368^(1/5) ~ 3.259639 is ABOVE the C7 record 3.25883262 (record^5 ~ 367.545), so a verified 368-set in C7^{⊠5} is a full capacity record, while 367^(1/5) ~ 3.257866 only matches Polak-Schrijver 2018. Recompute thresholds as floor(record^d)+1 against the live record.
- Adjacency in the strong product means each coordinate is equal or adjacent, not all equal; get this exactly right.
- Confusing a finite-level value with the limiting rate of a recursion.
- Records moved four times in Jul-Sep 2026; re-check the repo and arXiv.
- Probable-correctness search outputs with no exhaustive pair check.
- Re-fetch 9a.md and arXiv on the day; a fifth 2026 improvement may have landed after 2026-09-26.
- A finite-dimension set must beat the asymptotic recursive limit, not just the old fixed-dimension value (e.g. 1102 in dim 6 beats nothing asymptotically).
- Attribution: Tao's 9a page cites the 3.25883262 record under the key [Tan2026]; that is R. Tandon (arXiv:2608.30273), not a separate 'Tan 2026' result.

## Sources

- https://arxiv.org/abs/2608.30273
- https://arxiv.org/abs/2607.21517
- https://arxiv.org/pdf/2607.29681
- https://teorth.github.io/optimizationproblems/
- https://einsteinarena.com/
- https://arxiv.org/abs/2607.27869
- https://github.com/teorth/optimizationproblems/blob/main/constants/9a.md
- https://github.com/nathanielitty/lower-bounds-for-shannon-capacity
- https://github.com/xyz2606/recursive_construction_of_the_Shannon_capacity_of_C_7
- https://github.com/spectra-research/shannon-capacity-lean
- https://github.com/tandonravi/C7-Shannon-Capacity-Heterogeneous-Recursion
- https://arxiv.org/abs/2607.29681
- https://github.com/google-deepmind/formal-conjectures/blob/main/FormalConjectures/GreensOpenProblems/38.lean
- Status source: https://arxiv.org/abs/2608.30273

## Citations

- [Problem page](../../../../.raw/V3R1T4S/known-unknowns/record-tables/shannon-capacity-odd-cycles.md)
- [Bank entry](../../../../.raw/V3R1T4S/bank/targets.json) (id `shannon-capacity-odd-cycles`, commit `7dd4480`)

## Related Nodes

- [[V3R1T4S Record tables]]
- [[V3R1T4S]]
