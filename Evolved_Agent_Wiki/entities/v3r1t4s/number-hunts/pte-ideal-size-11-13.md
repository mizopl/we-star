---
id: v3r1t4s-pte-ideal-size-11-13
type: entity
tags: [v3r1t4s, v3r1t4s/number-hunts, kind/harvest]
inbound_links: 1
confidence: 0.8
last_ingested_sources: [".raw/V3R1T4S/bank/targets.json@7dd4480"]
status: "open"
priority: ""
notes: ""
category: number-hunts
kind: harvest
tractability: 2
compute: "laptop-hours"
disclosure: open
status_checked: "2026-10-03"
---
# Ideal Prouhet-Tarry-Escott solution of size 11 or 13

# Overview

> Bank id `pte-ideal-size-11-13` · harvest · tractability 2 · laptop-hours · disclosure **open**
> Bank says open as of 2026-10-03. Statuses go stale — re-check the primary source before any work.

## Statement

Find two disjoint multisets A, B of n integers with sum a^k = sum b^k for k = 1..n-1 (an ideal PTE solution) for n = 11 or n = 13 (or any n ≥ 13). Ideal solutions over Z are known only for n ≤ 10 and n = 12. Status: Wikipedia lists n = 11 and n >= 13 as having no known ideal solution; the n = 12 example is Kuosa-Meyrignac-Chen Shuwen (1999). Coppersmith-Mossinghoff-Scheinerman-VanderKam (arXiv 2304.11254, 2023): no symmetric ideal solution for n = 11 with height <= 3500, n = 13 with height <= 2000, n = 15 with height <= 1100; they found n = 11 symmetric solutions over real quadratic fields. arXiv 2606.07735 (June 2026) treats only degree-3 symmetry questions.

## Success criterion

CONFIRMED for explicit integer multisets A, B with |A| = |B| = n where n = 11 or n >= 13 is listed as having no known ideal solution on https://en.wikipedia.org/wiki/Prouhet%E2%80%93Tarry%E2%80%93Escott_problem AT VERIFICATION TIME, A and B disjoint as multisets (so the effective size after cancellation is still n), and sum a^k = sum b^k exactly for every k = 1..n-1. Solutions over Gaussian, Eisenstein or real-quadratic integers, and non-ideal solutions (degree < n-1), do not count.

## Partial wins

- {"id": "p1", "statement": "Symmetric n = 11 frontier: an exhaustive search, independently reimplemented by the verifier, proving no symmetric ideal n = 11 solution with height up to a bound strictly greater than 3500 (CMSV 2023) or the largest published bound at verification time."}
- {"id": "p2", "statement": "Symmetric n = 13 frontier: as in p1 for n = 13, with height bound strictly greater than 2000 (CMSV 2023) or the largest published bound at verification time."}

## Verification

Python big integers: check sizes, check that the multisets are disjoint (Counter intersection empty), and compare power sums for k = 1..n-1. Equivalence to known solutions is irrelevant because none exist for these n. Under 1 second. For search-extension partial wins, the verifier reimplements the CMSV-style mod-p obstruction search, reruns it (or sampled height ranges plus the full obstruction tables), and compares the surviving-candidate lists.

## Angles

- Non-symmetric solutions: CMSV searched only symmetric (B = -A) solutions for odd n. Search non-symmetric n = 11 configurations with their local-solution and CRT-lifting method (required prime divisors of the constant C_n).
- Push the symmetric n = 11 search past height 3500 with their mod-p obstruction method plus more primes (29, 31, 37) and the 10 cores. Height 6000-8000 is a concrete frontier.
- Lattice approach: fix 9 of the 11 values and solve for the remaining two via the quadratic resolvent. CMSV found near-misses with irrational pairs; search nearby for rational ones with LLL.
- Build from n = 12 and n = 10 solutions using Frolov/Tarry transformations (A ∪ (B+d), B ∪ (A+d)), and look for cancellation that drops the size.

## Pitfalls

- Non-ideal solutions (degree k < n-1) are plentiful and do not count.
- Solutions with common elements in A and B have smaller effective size after cancellation.
- Solutions over quadratic fields (like CMSV's α, β examples) are not integer solutions.
- Floating-point power sums.

## Sources

- https://arxiv.org/pdf/2304.11254
- https://en.wikipedia.org/wiki/Prouhet%E2%80%93Tarry%E2%80%93Escott_problem
- http://www.cecm.sfu.ca/~lisonek/A13.html
- Status source: https://arxiv.org/pdf/2304.11254

## Citations

- [Problem page](../../../../.raw/V3R1T4S/known-unknowns/number-hunts/pte-ideal-size-11-13.md)
- [Bank entry](../../../../.raw/V3R1T4S/bank/targets.json) (id `pte-ideal-size-11-13`, commit `7dd4480`)

## Related Nodes

- [[V3R1T4S Number hunts]]
- [[V3R1T4S]]
