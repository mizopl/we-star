---
id: v3r1t4s-fmm-catalogue-small-format-rank
type: entity
tags: [v3r1t4s, v3r1t4s/algorithms, kind/harvest]
inbound_links: 1
confidence: 0.8
last_ingested_sources: [".raw/V3R1T4S/bank/targets.json@7dd4480"]
status: "open"
priority: ""
notes: ""
category: algorithms
kind: harvest
tractability: 3
compute: "laptop-hours"
disclosure: open
status_checked: "2026-10-08"
---
# Fast matrix multiplication: beat a best-known rank in the Lille FMM catalogue for a small format

# Overview

> Bank id `fmm-catalogue-small-format-rank` · harvest · tractability 3 · laptop-hours · disclosure **open**
> Bank says open as of 2026-10-08. Statuses go stale — re-check the primary source before any work.

## Statement

For a matrix-multiplication format <n,m,p> with max(n,m,p) <= 16, OTHER THAN <3,3,3> and <4,4,4> (those two are the separate moonshot target fmm-4x4x4-rank47-3x3x3-rank22), find a bilinear (non-commutative) scheme with strictly fewer multiplications (tensor rank) than the best known value over ANY ring. Live scoreboards: Sedoglavic's Lille catalogue (fmm.univ-lille.fr; JSON digest fmm_sota.json, 5456 formats with 2<=n<=m<=p<=32, regenerated 2026-10-01), Perminov's status table (README 'Research Findings & Status', 680 formats up to 16x16x16, ZT/Z/Q columns) and MerlijnW70's fmm-schemes. Ranks checked live 2026-10-08: <2,2,2>:7, <2,2,3>:11, <2,3,3>:15, <2,4,5>:32, <3,4,5>:47, <3,3,6>:40, <3,4,7>:63, <5,5,5>:93, <6,6,6>:153, <2,4,6>:39, <2,3,10>:50. The frontier moved a lot in 2025-2026 (AlphaEvolve May 2025; flip graphs with symmetry arXiv:2502.04514; Perminov's open-source flip-graph framework arXiv:2603.02398 and meta flip graph arXiv:2606.02480, which improved 207 formats up to 16x16x16; Perminov CHANGELOG rank improvements as late as 28 Sep 2026, e.g. <4,4,8>:95, <7,7,15>:507, <15,16,16>:2223; MerlijnW70 ternary batches merged 29 Sep and 2 Oct 2026). Most formats with max dim <= 6 are heavily mined; mid-size rectangular formats (max dim 7-16) are where new ranks keep appearing. Perminov's table marks many ZT/Z cells '(?)' (meaning undocumented in the README; the table says previous ranks are 'given in brackets'), so do not read '(?)' as 'open'.

## Success criterion

Success means an explicit bilinear scheme (U, V, W coefficient matrices or an equivalent list of rank-one terms) for a format <n,m,p> with max(n,m,p) <= 16 and sorted(n,m,p) not in {(3,3,3),(4,4,4)}, whose number of rank-one terms r is STRICTLY LESS (direction: min) than ALL of: the rank listed for the sorted format in https://raw.githubusercontent.com/sedoglavic/fmm_digest/master/fmm_sota.json, the rank on https://fmm.univ-lille.fr/<n>x<m>x<p>.html, the minimum over the ZT/Z/Q columns for that format in https://raw.githubusercontent.com/dronperminov/FastMatrixMultiplication/master/README.md, and the lowest rank for that format in https://github.com/MerlijnW70/fmm-schemes (every one re-fetched live immediately before claiming; the scheme beats the minimum over all four). The scheme must be verified in exact arithmetic (integers/fractions, or mod p for GF(p)) over the ring it claims; a scheme valid only over GF(2) counts here ONLY if r is also strictly below the GF(2) rank (F2 column) for that format in https://raw.githubusercontent.com/solven-eu/matmulcatalog/master/generated/COVERAGE.md (otherwise see partial win p2). A scheme obtained by composing, padding or block-splitting known schemes does not count if the resulting rank equals a value already listed (the Lille table has a 'construction' column listing such derivations). Ternary/integer re-derivations of a rank already attained over Q are NOT this target (see fmm-ternary-integer-ring-upgrade); fewer additions at an existing rank is NOT this target (see fmm-additive-complexity-records).

## Partial wins

- {"id": "p1", "statement": "A new rank for a format with 17 <= max(n,m,p) <= 32 (outside Perminov's 16x16x16 table but inside the Lille catalogue): an exactly verified scheme whose rank is strictly below the live fmm_sota.json entry and the live Lille per-format page for that format, and not a plain composition already listed in the Lille 'construction' column."}
- {"id": "p2", "statement": "A GF(2)-only improvement: an exactly verified (mod 2) scheme whose rank is strictly below the F2 column for its format in the live matmulcatalog COVERAGE.md AND below every GF(2)-valid scheme for that format in Perminov's live repository and MerlijnW70's repository, for a format where the characteristic-0 best rank is already <= the new GF(2) rank (so it is not a new rank overall)."}

## Verification

Parse the candidate scheme (JSON U, V, W integer/rational matrices, or a Maple-style product list as in the Lille *_raw.mpl files). With exact fractions/sympy, form the r products m_k = (sum_ij U_k,ij A_ij)*(sum_jl V_k,jl B_jl) and check that for every (i,l) sum_k W_k,il m_k equals the symbolic entry (A*B)_il with exact coefficients over the claimed ring (reduce mod p for GF(p)); equivalently check the Brent equations. Count r after dropping zero terms. Re-fetch fmm_sota.json, the Lille per-format page, Perminov's README (all three ZT/Z/Q columns) and MerlijnW70's repo, and compare against the sorted format (rank is invariant under axis permutation/transposition). For p2 also re-fetch COVERAGE.md and the GF(2) schemes. Whole check runs in minutes on a 10-core Mac even for 16x16x16.

## Angles

- Flip-graph random walks (Kauers-Moosbauer) with 'plus' transitions and reductions, seeded from the current best scheme of a '(?)'-marked format and its neighbours (e.g. start from <2,4,6>:39 or <2,3,10>:50 and from one-larger formats, then restrict).
- Meta flip graph (Perminov): run flips on a larger format and project/peel to smaller formats; alternate ternary {-1,0,1} and GF(2)/GF(3) coefficient domains, then lift via Hensel/rational reconstruction to Z or Q.
- Symmetry-restricted search: impose a cyclic Z3 or S3 symmetry (or the stabilizer listed on the Lille page) to shrink the flip-graph state space and search for rank r-1 schemes with that symmetry, as in Flip Graphs with Symmetry (arXiv:2502.04514).
- Alternating least squares / Levenberg-Marquardt CP decomposition with sparsity and rounding to ternary, then exact verification, for rectangular formats with max dim 7-10 where the gap between rank and naive product is largest.
- SAT/SMT encoding over GF(2) for rank r-1 of small formats (<2,2,k>, <2,3,k>) with symmetry breaking, then lift to Z; the GF(2) lower-bound literature (arXiv:2609.06725) tells you where this is futile.

## Pitfalls

- Numerical 'decompositions' with floating-point residual 1e-8 are not schemes: only an exactly verified identity counts. Border-rank (approximate) decompositions are a different quantity and do not beat a rank entry.
- Permutations and transposes: <n,m,p> rank is invariant under axis permutations and transposition; compare against the catalogue entry for the sorted format. Also check Perminov's and MerlijnW70's tables: the Lille digest lags them by days.
- Schemes valid only in characteristic 2 (e.g. AlphaTensor's 4x4x4:47) do not beat a characteristic-0 entry; state the ring and verify exactly in it. A scheme using 1/2 is not valid over Z or GF(2).
- Trivial composition of known schemes (Kronecker products, padding, block splits) reproduces catalogue entries; the catalogue already lists those constructions, so an 'improvement' that equals a composition is a bookkeeping error.
- Counting bugs: r must be the number of rank-one terms after removing zero terms and merging duplicates; a term with a zero W-row still counts.
- Scope split: <3,3,3> and <4,4,4> belong to the moonshot entry; ring upgrades (ternary/integer at an existing rank) belong to fmm-ternary-integer-ring-upgrade; addition counts belong to fmm-additive-complexity-records. Do not double-claim.
- The Lille digest lags Perminov/MerlijnW70 by days and the catalogue front page says underlying data are being reconstructed; the bar is the minimum over all live tables, never the Lille number alone.

## Sources

- https://fmm.univ-lille.fr/
- https://raw.githubusercontent.com/sedoglavic/fmm_digest/master/fmm_sota.json
- https://github.com/sedoglavic/fmm_digest
- https://raw.githubusercontent.com/dronperminov/FastMatrixMultiplication/master/README.md
- https://raw.githubusercontent.com/dronperminov/FastMatrixMultiplication/master/CHANGELOG.md
- https://github.com/dronperminov/ternary_flip_graph
- https://github.com/MerlijnW70/fmm-schemes
- https://github.com/jakobmoosbauer/flips
- https://raw.githubusercontent.com/solven-eu/matmulcatalog/master/generated/COVERAGE.md
- https://arxiv.org/abs/2606.02480
- https://arxiv.org/abs/2603.02398
- https://arxiv.org/abs/2502.04514
- Status source: https://fmm.univ-lille.fr/

## Citations

- [Problem page](../../../../.raw/V3R1T4S/known-unknowns/algorithms/fmm-catalogue-small-format-rank.md)
- [Bank entry](../../../../.raw/V3R1T4S/bank/targets.json) (id `fmm-catalogue-small-format-rank`, commit `7dd4480`)

## Related Nodes

- [[V3R1T4S Algorithms]]
- [[V3R1T4S]]
