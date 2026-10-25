---
id: v3r1t4s-dna-codes-gc-rc-king-table
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
# DNA codes with GC-content and reverse-complement constraint: beat a lower bound in the A_4^GC,RC(n,d,w) table

# Overview

> Bank id `dna-codes-gc-rc-king-table` · harvest · tractability 2.5 · laptop-hours · disclosure **open**
> Bank says open as of 2026-10-15. Statuses go stale — re-check the primary source before any work.

## Statement

Same page as the GC table, second table: A_4^GC,RC(n,d,w) additionally requires Hamming distance >= d between any codeword and the reverse-complement of any codeword (including itself), the constraint that prevents unwanted hybridization in DNA storage/computing. Lower bounds for 4 <= n <= 20 listed; many mid-range 'v' (VNS) and 'c' (linear) entries are not known optimal. Construct a strictly larger code for any unmarked (n,d).

## Success criterion

A codeword list for some (n,d) whose A_4^GC,RC entry on https://rambutan.umassmed.edu/king/dnacodes.html is not followed by '.' or ':', checked to satisfy: length n, alphabet ACGT, GC count = floor(n/2), pairwise Hamming >= d, Hamming(x, rc(y)) >= d for all x,y including x=y, distinct; size strictly greater than the live table entry re-fetched immediately before claiming and than any post-2010 published value for the same parameters (novelty search, e.g. arXiv 1903.03535 lists GC,RC improvements).

## Partial wins

- {"id": "halving-gap", "statement": "For an unmarked (n,d), a code of size > half the GC-table entry, beating the GC,RC entry by construction from an RC-closed GC code (checker-confirmed)."}
- {"id": "tie-v-entry-n>=15", "statement": "Tie a 'v' entry with n >= 15 using our own search from scratch."}

## Verification

Same checker as the GC table plus the reverse-complement constraint (rc = reverse + A<->T, C<->G) applied to all ordered pairs including self-pairs. Seconds.

## Angles

- Build codes as unions of RC-orbit pairs {x, rc(x)}: search on the quotient graph of orbit pairs with max-clique / VNS.
- Reversible cyclic and quasi-cyclic codes over GF(4) (Gaborit-King linear constructions, reversible G^k codes) restricted to the GC-weight slice, then greedy completion.
- Simulated annealing with tabu over codeword swaps, objective = size with conflict penalty; 10 parallel chains seeded from the page's codes/LinearGCRC.txt.
- Cross-domain import (graph colouring/register allocation): Kempe-chain style recolouring moves on the conflict graph to free room for an extra codeword.
- Cross-domain import (frequency hopping / radar sequence design): use difference-set and Costas-style algebraic constructions with built-in reversal symmetry as seeds.

## Pitfalls

- Self-constraint: Hamming(x, rc(x)) >= d is required; omitting it inflates sizes and is the most common false positive.
- Some authors use the 'Watson-Crick complement' (without reversal) distance instead; that is a different table (Chee-Ling).
- Table is from 2010; novelty must be checked against later literature.
- Some large-n results in recent papers (n=48..160) are outside this table and not comparable.

## Sources

- https://rambutan.umassmed.edu/king/dnacodes.html
- https://arxiv.org/abs/2108.02033
- https://arxiv.org/abs/2403.11551
- Status source: https://rambutan.umassmed.edu/king/dnacodes.html

## Citations

- [Problem page](../../../../.raw/V3R1T4S/known-unknowns/biology/dna-codes-gc-rc-king-table.md)
- [Bank entry](../../../../.raw/V3R1T4S/bank/targets.json) (id `dna-codes-gc-rc-king-table`, commit `7dd4480`)

## Related Nodes

- [[V3R1T4S Biology]]
- [[V3R1T4S]]
