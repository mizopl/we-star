---
id: v3r1t4s-dna-codes-gc-king-table
type: entity
tags: [v3r1t4s, v3r1t4s/biology, kind/harvest]
inbound_links: 1
confidence: 0.8
last_ingested_sources: [".raw/V3R1T4S/bank/targets.json@7dd4480"]
status: "open"
priority: ""
notes: ""
category: biology
kind: harvest
tractability: 2.5
compute: "laptop-hours"
disclosure: open
status_checked: "2026-10-15"
---
# DNA codes with constant GC-content: beat a lower bound in the Gaborit-King A_4^GC(n,d,w) table

# Overview

> Bank id `dna-codes-gc-king-table` · harvest · tractability 2.5 · laptop-hours · disclosure **open**
> Bank says open as of 2026-10-15. Statuses go stale — re-check the primary source before any work.

## Statement

Oliver King's table (rambutan.umassmed.edu/king/dnacodes.html, last updated June 23, 2010) lists best-known lower bounds for A_4^GC(n,d,w): the maximum size of a quaternary (A,C,G,T) code of length n, minimum Hamming distance d, with every codeword containing exactly w = floor(n/2) G/C letters, for 4 <= n <= 20, 3 <= d <= 20. Entries marked '.' or ':' are proven optimal. Construct an explicit code strictly larger than the table entry for an unmarked (n,d). These codes are used for DNA data storage address/primer design and microarray probes.

## Success criterion

A plain-text list of codewords for some (n,d) whose table entry on https://rambutan.umassmed.edu/king/dnacodes.html is NOT followed by '.' or ':' such that a checker confirms all words have length n over {A,C,G,T}, exactly the table's GC-content w (w = floor(n/2), confirm from King 2003), pairwise Hamming distance >= d, are distinct, and the count is strictly greater than the table entry re-fetched live immediately before claiming, AND strictly greater than any value for the same (n,d,w) found by a novelty search of post-2010 literature (e.g. Limbachiya-Gupta-Rao altruistic-algorithm papers, Montemanni-Smith, arXiv 1903.03535, 2108.02033).

## Partial wins

- {"id": "tie-unmarked-mid", "statement": "Reproduce (tie) an unmarked 'v' (variable-neighbourhood-search) entry with n >= 14 from scratch with our own search, checker-confirmed."}
- {"id": "new-optimality-proof", "statement": "Prove an unmarked entry optimal via exact max-clique with symmetry breaking, producing a checkable certificate (e.g. clique-solver log + upper-bound LP)."}

## Verification

Python checker: read codewords, assert alphabet, length, GC count, uniqueness, all-pairs Hamming distance >= d (n<=20 and sizes <= ~10^5 is seconds with numpy bit tricks), compare size to live table cell. Run on a code file from the page's codes/ directory first.

## Angles

- Max-clique search on the GC-constrained Hamming graph with automorphism (coordinate permutation x base-swap A<->T, C<->G) orbit reduction, then clique solvers (e.g. MoMC / cliquer) on quotient graphs.
- Variable-neighbourhood search / tabu with conflict-driven replacement, starting from the table's own linear codes in codes/LinearGC.txt.
- Linear and additive codes over GF(4)/Z4 with GC-weight selection: search quasi-cyclic generator matrices and take the largest constant-GC coset slice.
- Cross-domain import (constant-weight binary codes): map A/T vs G/C to a weight constraint and lift known record constant-weight codes from Brouwer's tables (our bank already confirmed wins there) via product/concatenation constructions.
- Cross-domain import (SAT/SMT scheduling): encode 'size >= table+1' as a SAT instance with symmetry-breaking predicates and run kissat/cadical for small n (n<=12).
- Cross-domain import (sphere packing/lattice codes): Construction A from quaternary lattices and spherical-code style greedy-with-repulsion annealing.

## Pitfalls

- The table is stale (2010); later papers (Limbachiya et al. 2016-2018, Montemanni-Smith, Smith-Aboluion-Montemanni-Perkins) may already exceed some cells - a 'win' versus the page alone is not novel.
- GC-content w: the table fixes w = floor(n/2); a code with mixed or different GC weights is not admissible.
- Do not confuse with the GC,RC table directly below it on the same page (different, stricter constraint).
- Entries ending in '.' or ':' are proven optimal; exceeding one indicates a checker bug.

## Sources

- https://rambutan.umassmed.edu/king/dnacodes.html
- https://www.combinatorics.org/ojs/index.php/eljc/article/view/v10i1r33
- https://arxiv.org/abs/2403.11551
- https://arxiv.org/abs/2108.02033
- Status source: https://rambutan.umassmed.edu/king/dnacodes.html

## Citations

- [Problem page](../../../../.raw/V3R1T4S/known-unknowns/biology/dna-codes-gc-king-table.md)
- [Bank entry](../../../../.raw/V3R1T4S/bank/targets.json) (id `dna-codes-gc-king-table`, commit `7dd4480`)

## Related Nodes

- [[V3R1T4S Biology]]
- [[V3R1T4S]]
