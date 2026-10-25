---
id: v3r1t4s-codetables-binary-linear
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
# Binary (or small-q) linear codes beating codetables.de lower bounds

# Overview

> Bank id `codetables-binary-linear` · harvest · tractability 3 · laptop-hours · disclosure **open**
> Bank says open as of 2026-10-03. Statuses go stale — re-check the primary source before any work.

## Statement

For given [n,k] over GF(q), codetables.de (Grassl) records the best known lower and upper bounds on the maximum minimum distance d. A linear code with d larger than the tabulated lower bound is a new record. Binary tables cover n <= 256.

## Success criterion

Success means a k x n generator matrix over GF(q) with these properties. (1) Rank is exactly k over GF(q), computed independently. (2) The exact minimum distance d is computed by full enumeration of all q^k - 1 nonzero codewords when feasible (2^k <= ~2^32), or, for large k (or large k with small n-k, via the dual and MacWilliams identities), by two independent exact minimum-distance implementations that agree; never by sampling. (3) d is STRICTLY GREATER (direction: max) than the lower bound in the live http://www.codetables.de/ cell for (q,n,k) at verification time, and at most the upper bound. (4) The code is not one of the 7 LinCodeEvolve codes (arXiv:2609.37056) or a code derived from them, and no newer arXiv claim already reaches that d.

## Partial wins

- {"id": "p1", "statement": "A quantum-code record: an explicit stabilizer code \[\[n,k,d\]\] (symplectic self-orthogonality checked exactly, minimum distance computed exactly) whose d is strictly greater than the lower bound in the live codetables.de quantum-code table for that (n,k)."}
- {"id": "p2", "statement": "An improved upper bound: a re-checkable certificate (exact rational LP dual certificate, or an exhaustive non-existence classification with code the skeptic re-runs) proving that no [n,k,d] code over GF(q) exists for d equal to the live codetables.de upper bound, thereby lowering it."}

## Verification

Use an independent script. Compute rank by Gaussian elimination over GF(2) with numpy uint8 or bitset ints. For k <= 32, compute weights with a Gray-code walk over all codewords using XOR of packed rows (2^k * n/64 ops; k=22 takes seconds). For larger k, use two independent minimum-distance implementations (e.g. a custom Brouwer-Zimmermann plus pip 'galois' or 'ldpc' style tools) and require agreement. Look up the live table cell at codetables.de/BKLC/... for (n,k) and confirm the strict improvement. Then check arXiv for newer claims.

## Angles

- Search quasi-cyclic and quasi-twisted codes of index 2-6. Each code is defined by a few circulant first rows, so the search space is small and the codes have a good chance of structure. Use the circulant to prune minimum-distance computation (only one codeword per cyclic orbit needs checking).
- Run Construction X/XX on any new QC code, plus puncturing, shortening and extending, to propagate one win to several neighboring table cells.
- Look at ternary/quaternary tables (q=3,4,5) in moderate n, which have historically received less AI attention than binary.
- Use an evolutionary search over generator programs, not matrices (LinCodeEvolve style). Mutate small Python code that emits QC first rows, with the exact minimum-distance checker as the fitness.
- Use Gray-code minimum-distance evaluation with early abort. Stop as soon as a codeword of weight below the target is found, which makes rejection cheap.

## Pitfalls

- Floating-point or int8 overflow in the GF(2) arithmetic. Use bit operations.
- A d computed only on a random sample of codewords proves nothing.
- Rank deficiency: the code is then really [n,k'] with k' < k.
- Comparing against a stale snapshot. The LinCodeEvolve results may already be incorporated, so re-check the live cell.
- When k is large but n-k is small, use the dual and MacWilliams identities, or require two independent minimum-distance implementations. Never sample.

## Sources

- http://www.codetables.de/
- https://arxiv.org/abs/2609.37056
- Status source: http://www.codetables.de/

## Citations

- [Problem page](../../../../.raw/V3R1T4S/known-unknowns/record-tables/codetables-binary-linear.md)
- [Bank entry](../../../../.raw/V3R1T4S/bank/targets.json) (id `codetables-binary-linear`, commit `7dd4480`)

## Related Nodes

- [[V3R1T4S Record tables]]
- [[V3R1T4S]]
