---
id: v3r1t4s-site-percolation-2-uniform-lattices-thresholds
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
tractability: 4
compute: "laptop-hours"
disclosure: open
status_checked: "2026-10-15"
---
# Site percolation thresholds of the 20 two-uniform lattices: beat the 4-digit values of Neher, Mecke and Wagner (2008) listed on Wikipedia's percolation-threshold tables

# Overview

> Bank id `site-percolation-2-uniform-lattices-thresholds` · harvest · tractability 4 · laptop-hours · disclosure **open**
> Bank says open as of 2026-10-15. Statuses go stale — re-check the primary source before any work.

## Statement

The Wikipedia 'Percolation threshold' page (section '2-uniform lattices', checked 2026-10-15) lists site thresholds for the 20 two-uniform tilings, all from Richard Neher, Klaus Mecke and Herbert Wagner (J. Stat. Mech. 2008; arXiv 0708.3250 with supplementary table arXiv 0708.3251), obtained by Newman-Ziff simulations on L = 64..1024 with about 2e-4 precision: e.g. #41 (1/2)(3,4,3,12)+(1/2)(3,12^2) 0.7680(2), #42 0.7157(2), #36 0.6808(2), #15 0.6499(2), #34 0.6329(2), #16 0.6286(2). The bond thresholds on the same rows have 8 digits (several marked 'citation needed'). A 2021 study by Lebrecht, Centres and Ramirez-Pastor fitted site/bond ratios but did not remeasure. Site thresholds on Archimedean lattices are known to 6-15 digits (Suding-Ziff, Jacobsen's critical polynomials), so the two-uniform site column is an outlier that a laptop can improve by 2-4 digits with standard methods.

## Success criterion

Success means, for at least one of the 20 two-uniform lattices in the live Wikipedia table (re-fetched immediately before claiming), a site percolation threshold with stated one-sigma uncertainty at most 2e-6 (100 times smaller than the table's), such that (a) two independent methods agree within three combined sigma (for example Newman-Ziff wrapping-probability finite-size scaling on tori up to L >= 2048 unit cells, and the Jacobsen-Scullard critical-polynomial root sequence P_B(p) = 0 for growing bases), (b) the value is within 3 sigma of the table value or the discrepancy is explained, (c) the same code reproduces the published BOND threshold of that lattice to at least 6 digits and the site threshold of the (3,12^2) or kagome Archimedean lattice to at least 6 digits, and (d) a literature search finds no published site value for that lattice with uncertainty below 2e-6. Direction: smaller uncertainty.

## Partial wins

- {"id": "p1", "statement": "All 20 two-uniform site thresholds to uncertainty at most 2e-5 each, same two-method and reproduction rules, published as a table with code."}
- {"id": "p2", "statement": "An independent determination, to at least 7 digits, of a 'citation needed' bond threshold in the same Wikipedia table, either confirming it or showing a discrepancy larger than its stated error bar."}

## Verification

Skeptic (< 1 hour): rebuild the lattice from its vertex configuration and check coordination numbers and z-bar against the table; rerun the claimant's MC at two sizes with fresh seeds (minutes) and the critical-polynomial code for the smallest two bases (exact polynomials are deterministic); rerun the fit; check the reproduction tests.

## Angles

- Newman-Ziff union-find sweeps with wrapping probabilities on tori: at the threshold the wrapping probability tends to a universal value with small finite-size corrections, which gives 1e-6-1e-7 precision on a laptop for planar lattices.
- From algebraic combinatorics: Jacobsen-Scullard critical polynomials P_B(p) on n x n bases of the periodic tiling give root sequences that converge fast; even small bases often beat Monte Carlo by orders of magnitude.
- From computational geometry: generate each 2-uniform tiling programmatically from its vertex configuration (Grunbaum-Shephard numbering) and verify it by vertex-type counts before any percolation run.
- Use the site-to-bond mapping on the covering (line) lattice as a cross-check where a two-uniform lattice's covering lattice has a known bond threshold.

## Pitfalls

- Lattice identity: two-uniform numbering varies between sources; a precise value for the wrong tiling is a false win. Match the vertex-type fractions and z-bar in the Wikipedia row.
- Monte Carlo error bars that ignore finite-size corrections or seed correlations are too small; require the second method.
- Critical-polynomial roots are estimates that converge from one side for some lattices and oscillate for others; the error bar must come from the observed convergence, not the last difference.
- Some 'citation needed' bond values may come from unpublished critical-polynomial runs; a discrepancy with them is reportable but not by itself a record.

## Sources

- https://en.wikipedia.org/wiki/Percolation_threshold
- https://arxiv.org/abs/0708.3250
- https://arxiv.org/abs/0708.3251
- https://arxiv.org/abs/cond-mat/9811416
- https://arxiv.org/abs/cond-mat/0005264
- https://arxiv.org/abs/1507.03027
- Status source: https://en.wikipedia.org/wiki/Percolation_threshold

## Citations

- [Problem page](../../../../.raw/V3R1T4S/known-unknowns/physics/site-percolation-2-uniform-lattices-thresholds.md)
- [Bank entry](../../../../.raw/V3R1T4S/bank/targets.json) (id `site-percolation-2-uniform-lattices-thresholds`, commit `7dd4480`)

## Related Nodes

- [[V3R1T4S Physics]]
- [[V3R1T4S]]
