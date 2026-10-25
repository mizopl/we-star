---
id: v3r1t4s-erdos-835-large-steiner-systems
type: entity
tags: [v3r1t4s, v3r1t4s/erdos-and-proofs, kind/harvest]
inbound_links: 1
confidence: 0.8
last_ingested_sources: [".raw/V3R1T4S/bank/targets.json@7dd4480"]
status: "open"
priority: ""
notes: ""
category: erdos-and-proofs
kind: harvest
tractability: 2
compute: "pure thought + laptop-minutes (literature, design-theory proofs, small exhaustive checks)"
disclosure: open
status_checked: "2026-10-03"
---
# Erdos #835: (k+1)-colouring of J(2k,k), equivalently large sets of Steiner systems S(k-1,k,2k)

# Overview

> Bank id `erdos-835-large-steiner-systems` · harvest · tractability 2 · pure thought + laptop-minutes (literature, design-theory proofs, small exhaustive checks) · disclosure **open**
> Bank says open as of 2026-10-03. Statuses go stale — re-check the primary source before any work.

## Statement

Does some k > 2 admit a colouring of the k-subsets of [2k] with k+1 colours such that every (k+1)-set sees all k+1 colours, i.e. chi(J(2k,k)) = k+1? A (k+1)-set has exactly k+1 k-subsets, so each colour class meets every (k+1)-set exactly once; taking complements, each colour class is a Steiner system S(k-1,k,2k), so the property is equivalent to a large set LS(k-1,k,2k) (athvedt, forum 2026-05-21). OPEN. Settled negatively for k=3..8 (computation), for all k with k+1 composite (Ma-Tang), and for k=10 and k=12 (athvedt, forum 2026-05-21, via the nonexistence of S(4,5,15) [Mendelsohn-Hung] and S(4,5,17) [Ostergard-Pottonen]). The smallest open case is k=16 (veljjanoski, forum 2026-09-21; partial Kramer-Mesner searches). Then k=18, 22, 28, ... KentaKitamura (2026-05-30): every k-set must share its colour with its complement. The answer is widely expected to be NO.

## Success criterion

FULL: a complete proof that chi(J(2k,k)) != k+1 for every k>=16 with k+1 prime, or an explicit colouring for some k. Partial win: a fully verified settlement of k=16 (the smallest open case per the forum), with every cited nonexistence theorem quoted with its exact hypotheses. Re-deriving k=10 or k=12 is NOT a result. At verification time, re-read the forum thread to confirm the claimed case is still listed as open.

## Partial wins

- {"id": "p1", "statement": "A fully verified settlement of k = 16 (no LS(15,16,32), equivalently no (k+1)-colouring of J(32,16) as required), with every cited nonexistence theorem opened and quoted with exact hypotheses and any computation rerun independently, provided k = 16 is still listed as open on the forum at verification time."}
- {"id": "p2", "statement": "A fully verified settlement of a single other open case (k = 18, 22, 28, ...; k+1 prime), with the same citation and rerun standards, provided it is not already settled on the forum."}
- {"id": "p3", "statement": "A rigorous, refereed obstruction (e.g. spectral/Delsarte-type or block-intersection integrality) that rules out an explicitly described infinite subfamily of the open k."}

## Verification

YES case: brute force over all (k+1)-subsets for distinct colours. NO case: (1) re-derive the colour class to S(k-1,k,2k) reduction and the derived-design chain; (2) for k=16 the chain reaches S(4,5,21), S(5,6,22), etc. Confirm from the literature which of these are known not to exist and which are admissible but open; chains ending in admissible-but-open or existing designs (e.g. S(4,5,23) for k=18) do not kill the case; (3) any computer search (Kramer-Mesner under group G) proves nothing in general unless combined with a proof that every solution has such a symmetry; (4) independent rerun of the code.

## Angles

- k = 16: follow the derived-design chain from S(15,16,32) down through S(5,6,22) and S(4,5,21); confirm from the literature which of these are known not to exist and which are admissible but open. Also derive the large-set chain (blocks through a point across all systems form a large set of S(k-2,k-1,2k-1)), which is a stronger hypothesis than a single system.
- Attack the large-set condition rather than single Steiner systems. The colour classes are perfect 'clique-hitting' codes in the Johnson scheme J(2k,k). Apply Delsarte's theory (design-orthogonal-to-clique / Roos-type identities, Lloyd-type theorems for perfect codes in Johnson graphs, eigenvalue integrality) for a uniform obstruction killing all k at once.
- Derived large sets: the blocks through a fixed point, across all k+1 systems, form a large set of S(k-2,k-1,2k-1). Iterate to small parameters where exhaustive nonexistence is checkable (LS of S(3,4,v) or S(4,5,v) for small v) and look for a pattern.
- Use intersection-number constraints: in S(t,t+1,2t+2) with v = 2(t+1) the Tits bound holds with equality. Exploit the equality case (block complements, self-complementarity of the whole large set) to derive integrality conditions via block-intersection polynomials (Cameron/Mendelsohn style).
- Use KentaKitamura's lemma (every k-set shares its colour with its complement) to halve the variables in any SAT/Kramer-Mesner encoding and to derive further parity/integrality constraints.
- Extend veljjanoski's Kramer-Mesner searches for S(15,16,32) to further automorphism groups, but treat results as heuristic unless paired with a proof that any large set must have that symmetry.

## Pitfalls

- Cameron's 2014 blog asserts that S(9,10,20) does not exist without giving a citation.
- Keevash-type existence results apply only to large v and are irrelevant here.
- Notation varies: S(2k,k,k-1) versus S(k-1,k,2k).
- A large set needs k+1 pairwise disjoint systems covering ALL k-subsets; disjointness alone is weaker.
- k=10 is already settled on the forum; do not claim it.
- k=12 is ALREADY settled on the forum (athvedt, 2026-05-21, via S(4,5,17) nonexistence); do not claim it.
- Kramer-Mesner searches restricted to specific automorphism groups do not prove nonexistence.
- AlphaProof's J(18,9) result concerns k=9 (composite k+1), not k=18.

## Sources

- https://www.erdosproblems.com/835
- https://www.erdosproblems.com/forum/thread/835
- https://github.com/QuanyuTang/erdos-problem-835
- https://github.com/google-deepmind/formal-conjectures/blob/main/FormalConjectures/ErdosProblems/835.lean
- https://raw.githubusercontent.com/QuanyuTang/erdos-problem-835/main/On_Problem_835.pdf
- Status source: https://www.erdosproblems.com/835

## Citations

- [Problem page](../../../../.raw/V3R1T4S/known-unknowns/erdos-and-proofs/erdos-835-large-steiner-systems.md)
- [Bank entry](../../../../.raw/V3R1T4S/bank/targets.json) (id `erdos-835-large-steiner-systems`, commit `7dd4480`)

## Related Nodes

- [[V3R1T4S Erdős problems and proofs]]
- [[V3R1T4S]]
