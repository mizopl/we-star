---
id: v3r1t4s-burnt-pancake-even-n-exact-flips
type: entity
tags: [v3r1t4s, v3r1t4s/biology, kind/standard]
inbound_links: 1
confidence: 0.8
last_ingested_sources: [".raw/V3R1T4S/bank/targets.json@7dd4480"]
status: "open"
priority: ""
notes: ""
category: biology
kind: standard
tractability: 3
compute: "laptop-hours"
disclosure: open
status_checked: "2026-10-15"
---
# Burnt pancake sorting: settle T(n) for an even n by finding a flipping sequence that attains the lower bound

# Overview

> Bank id `burnt-pancake-even-n-exact-flips` · standard · tractability 3 · laptop-hours · disclosure **open**
> Bank says open as of 2026-10-15. Statuses go stale — re-check the primary source before any work.

## Statement

Sorting burnt pancakes (prefix reversals with orientation) is the textbook model for genome rearrangement by reversals, and T(n), the number of flips needed to sort the all-burnt-side-up sorted stack I_n = [-1,-2,...,-n], is tabulated in OEIS A078942 with the related diameter in A078941. Gerold Jager and Nacim Oijid (arXiv:2601.09447) closed the odd case by proving the upper bound floor((3n+3)/2) for n = 1 mod 4, matching Josef Cibulka's 2011 lower bound, so for odd n the value is exact. For even n only two values remain possible, 3n/2 + 1 or 3n/2 + 2, and which one holds is open. By explicit search the same authors found sequences attaining the lower bound for n = 24 (37 flips) and n = 26 (40 flips), disproving the values Bruno Bouzy's 2016 technical report listed for those two n, and they note these are the only even n above 2 where the lower bound is known to be attained. Deciding another even n, in either direction, is a checkable new record.

## Success criterion

For some even n not already decided in the live OEIS entry A078942 and its references (re-fetched live immediately before claiming), either (a) an explicit flipping sequence that sorts I_n in exactly 3n/2 + 1 flips, verified by a checker that applies each prefix reversal with sign flipping and confirms the final stack is [1,2,...,n] with all burnt sides down, or (b) an exhaustive-search certificate, independently re-runnable within a stated time budget, that no sequence of 3n/2 + 1 flips sorts I_n, hence T(n) = 3n/2 + 2. Either way the value must be strictly new: not already listed for that n in A078942 or in arXiv:2601.09447, and the novelty check must find no later publication giving it.

## Partial wins

- {"id": "p1", "statement": "Re-verify the published n = 24 (37 flips) and n = 26 (40 flips) sequences with an independent checker and publish the checker, since these two values contradict an earlier published table and deserve independent confirmation."}
- {"id": "p2", "statement": "A search that decides T(n) for one further even n by exhaustion, even if the answer is the upper value 3n/2 + 2, with a reproducible certificate and the search's state count."}
- {"id": "p3", "statement": "An improved admissible heuristic for the burnt-pancake graph, demonstrated by solving a published hard stack strictly faster than the reported times in Bouzy's table, with code released."}

## Verification

A twenty-line checker applies the claimed flips to [-1,...,-n] and compares with the identity stack; that side is seconds. For a non-existence certificate the skeptic re-runs the released search with the published heuristic and seed, or checks an independently generated proof artefact (for example a pruned-search log with reproducible node counts), and confirms the heuristic used is admissible.

## Angles

- The published even-n solutions were found by a search that explores few states; reproduce that search and extend it with a better admissible heuristic combining breakpoints, anti-adjacencies and wrong adjacencies as Bouzy's weighted heuristic does.
- Cross-domain import (SAT and constraint solving): encode 'sortable in exactly k flips' as a propositional formula with symmetry breaking and hand it to a modern solver, which turns the existence question into a certificate either way.
- Cross-domain import (group theory): the stacks form a Cayley graph; use coset enumeration or a subgroup decomposition to prune whole branches instead of searching permutations one by one.
- Build constructive sequences from the odd-n proof scheme and test exactly where it fails for even n, as the authors state their construction cannot be applied there; a repaired construction for one residue class would settle a family at once.
- Meet in the middle: bidirectional search from I_n and from the identity, with a perfect hash of stacks, is memory-bound but well suited to a laptop with tens of gigabytes.

## Pitfalls

- Confusing T(n), the flips to sort the special stack I_n, with g(n), the diameter of the whole burnt-pancake graph; the OEIS has separate sequences (A078942 and A078941) and they differ at n = 15.
- Published tables disagree: the 2016 technical report's values for n = 24 and n = 26 were later shown to be wrong, so a claim must name the source it beats and check the live OEIS entry.
- An inadmissible heuristic makes a non-existence claim worthless; admissibility must be proved, not assumed, before a lower-bound certificate counts.
- Off-by-one conventions in flip definitions (whether a flip of size 1 counts, whether the spatula goes below or above) change the answer; state the convention and reproduce a known value first.
- This is a combinatorial model of genome rearrangement, not a statement about real genomes; a new value says nothing directly about any organism.

## Sources

- https://oeis.org/A078942
- https://oeis.org/A078941
- https://arxiv.org/abs/2601.09447
- https://helios2.mi.parisdescartes.fr/~bouzy/publications/Bouzy-BurntPancake-CdL-TR-3.pdf
- Status source: https://oeis.org/A078942

## Citations

- [Problem page](../../../../.raw/V3R1T4S/known-unknowns/biology/burnt-pancake-even-n-exact-flips.md)
- [Bank entry](../../../../.raw/V3R1T4S/bank/targets.json) (id `burnt-pancake-even-n-exact-flips`, commit `7dd4480`)

## Related Nodes

- [[V3R1T4S Biology]]
- [[V3R1T4S]]
