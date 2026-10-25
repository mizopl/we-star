---
id: v3r1t4s-lattice-animals-hypercubic-d4-plus-exact-counts
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
tractability: 2.5
compute: "laptop-days"
disclosure: open
status_checked: "2026-10-15"
---
# Lattice animals in 4 to 9 dimensions: the next exact count of fixed polycubes beyond Luther and Mertens (OEIS A151830-A151835, unchanged since 2011)

# Overview

> Bank id `lattice-animals-hypercubic-d4-plus-exact-counts` · harvest · tractability 2.5 · laptop-days · disclosure **open**
> Bank says open as of 2026-10-15. Statuses go stale — re-check the primary source before any work.

## Statement

Fixed site animals on the hypercubic lattice Z^d (polycubes) are central to percolation series in high dimensions. Sebastian Luther and Stephan Mertens (J. Stat. Mech. 2011 P09026, arXiv 1106.1078) counted them with a parallel Redelmeier algorithm and Lunnon's proper-dimension decomposition: A151830 (d = 4) to n = 16 (692095652493483), A151831 (d = 5) and A151832 (d = 6) to n = 15, A151833-A151835 (d = 7, 8, 9) to n = 14; all carry keyword 'more' and have not been extended since 2011 (checked 2026-10-15). In 3D the record moved recently: Stanley Dodds' streamlined Redelmeier (2023, public C# program with Gunter Rote's comments) and Phillip Thompson's Rust port pushed A001931 from n = 19 to 22 (a(22) = 306405169166373418). The next 4D term is about 8e15 animals, the same size as A001931(20) that Dodds computed, and Lunnon's formula means only animals that genuinely span 4 dimensions need enumerating.

## Success criterion

Success means the exact value of the first unknown term of A151830, A151831, A151832, A151833, A151834 or A151835 (index one beyond the DATA and b-file, re-fetched live immediately before claiming), computed by two independent methods that agree exactly (for example direct d-dimensional Redelmeier/Dodds enumeration vs. Lunnon's sum over proper counts DX(n, i) with the lower-dimensional DX taken from independently recomputed lower-d counts, or two different work-partitionings with different code), with the same code reproducing every published term for that d, and a literature search finding no published value.

## Partial wins

- {"id": "p1", "statement": "Exact proper-dimension counts DX(n, d) (polycubes of size n spanning exactly d dimensions) for some (n, d) not published by Luther and Mertens, verified by reproducing their published DX table and by Lunnon's identity against the known A_d(n)."}
- {"id": "p2", "statement": "Independent full re-verification of Luther and Mertens' largest published term in some d >= 4 by a different algorithm (Pursey 2026 found errors in other published polycube counts); a confirmed discrepancy would be a major finding and needs a third run."}

## Verification

Skeptic: rerun the claimant's code for every n up to the published range in that d (minutes) and compare; spot-check the new term by re-running a random subset of the work partitions (the enumeration splits by the first few cells or by root subtree) with the independent code and checking the partial sums match; full recomputation (laptop-days) after the panel.

## Angles

- Port Dodds' streamlined Redelmeier implementation (public C# program with Gunter Rote's commentary, plus Thompson's Rust port) from 3D to d dimensions; it is what made A001931(20..22) feasible.
- Lunnon's decomposition A_d(n) = sum_i C(d, i) DX(n, i): only DX(n, d) is new work, and pruning branches that can no longer span d dimensions cuts the search drastically.
- From distributed computing: split by the first k cells into thousands of independent jobs with checkpointing; the partial sums double as the skeptic's spot-check units.
- From percolation theory: Mertens and Moore's 1/d series for p_c use exactly these counts; a new term feeds directly into a higher-order threshold expansion as a cross-check of plausibility.

## Pitfalls

- Fixed vs one-sided vs free counts: the sequences are fixed (translation only); dividing by the symmetry group gives a different sequence.
- 64-bit overflow: A151835 terms already exceed 2^61; use 128-bit counters for partial sums.
- Lunnon's formula needs DX(n, i) for all i <= d; a mismatch in any lower-dimensional input corrupts the sum silently, so recompute those inputs and compare with published tables.
- Index/offset: these sequences start at n = 1; an 'extra' term may be an existing one with a shifted offset.

## Sources

- https://oeis.org/A151830
- https://oeis.org/A151831
- https://oeis.org/A001931
- https://arxiv.org/abs/1106.1078
- https://oeis.org/A001931/a001931_1.cs.txt
- https://stephenpursey.com/papers/cavity-polycubes.pdf
- Status source: https://oeis.org/A151830

## Citations

- [Problem page](../../../../.raw/V3R1T4S/known-unknowns/physics/lattice-animals-hypercubic-d4-plus-exact-counts.md)
- [Bank entry](../../../../.raw/V3R1T4S/bank/targets.json) (id `lattice-animals-hypercubic-d4-plus-exact-counts`, commit `7dd4480`)

## Related Nodes

- [[V3R1T4S Physics]]
- [[V3R1T4S]]
