---
id: v3r1t4s-saw-hypercubic-exact-enumeration
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
# Self-avoiding walks: an exact count c_n beyond the published record on the 4D/5D hypercubic, bcc, fcc or simple cubic lattice

# Overview

> Bank id `saw-hypercubic-exact-enumeration` · harvest · tractability 2.5 · laptop-days · disclosure **open**
> Bank says open as of 2026-10-15. Statuses go stale — re-check the primary source before any work.

## Statement

The number c_n of n-step self-avoiding walks is known exactly to n = 79 on the square lattice (Iwan Jensen), 36 on the simple cubic lattice (Raoul Schram, Gerard Barkema, Rob Bisseling 2011), 28 on bcc and 24 on fcc (Schram, Barkema, Bisseling, Nathan Clisby 2017), and 24 on the hypercubic lattices Z^d for every d >= 4 (Clisby, Richard Liang, Gordon Slade 2007, lace expansion; polygons to 26 in d = 4, 24 in d = 5, 6). The d >= 4 series have not been extended since 2007 (checked 2026-10-15), and the length-doubling program SAWdoubler (public, v2.0.1 2017, shipped with sc/bcc/fcc lattice files only) has not been reported on Z^4 or Z^5. Length doubling costs about O(2^N Z_N) for half-length N (Schram et al. 2011); the sc n = 36 record took 50,000 CPU-hours (N = 18, Z_18 = 2.24e12, 48 symmetries), while Z^4 n = 26 has N = 13, Z_13 = 8.75e10 and 384 symmetries, well under a thousandth of the work. The limit is memory for the subset counters, so this is a laptop-days, disk-assisted computation.

## Success criterion

Success means an exact integer c_n for one lattice in {Z^4, Z^5, Z^6, sc, bcc, fcc} with n strictly greater than the largest n in BOTH the lattice's OEIS b-file (re-fetched immediately before claiming) and the Clisby-Liang-Slade data page / Schram et al. papers, AND no arXiv/Google Scholar search finds a published value for that (lattice, n); AND the value is computed by two independent runs that agree exactly (different split points n = a + b of length doubling, or length doubling vs. a lace-expansion or transfer-style method), AND the same code reproduces every published c_m for m <= the previous record on that lattice.

## Partial wins

- {"id": "p1", "statement": "New exact terms for a related series on Z^4 or Z^5 beyond the published record: self-avoiding polygon counts p_n, or the sum of squared end-to-end distances, with the same two-run agreement rule."}
- {"id": "p2", "statement": "A clean, documented port of SAWdoubler (or an independent length-doubling implementation) to Z^d, d = 4..6, that reproduces all published c_n up to n = 24 for each d; reproduction only, but checkable and a prerequisite for the main win."}

## Verification

Skeptic (< 1 h): re-run the claimant's code to reproduce all published terms up to the old record on that lattice (minutes to an hour), check exact agreement of the two independent runs' outputs for the new term, and sanity-check the new term against ratio analysis (c_n / c_{n-2} consistent with the known growth constant mu, e.g. mu ~ 6.774 for Z^4) and parity/symmetry divisibility (c_n divisible by 2d). Full re-computation of the new term is laptop-hours and can be done after the panel.

## Angles

- Port SAWdoubler (written for sc, bcc, fcc) to Z^4: the length-doubling identity c_{2n} = sum over pairs of n-step walks with inclusion-exclusion over shared sites only needs the lattice neighbour structure and its symmetry group; exploit the 384-element hyperoctahedral group to store walks up to symmetry.
- Import from database engineering: the inclusion-exclusion step is a giant subset-join; external-memory sort-merge on a 1 TB disk replaces the cluster memory Schram et al. used.
- Import from coding theory: hash the site sets of half-walks into Bloom-filter-like signatures to prune non-intersecting pairs before exact checks.
- Do odd n by c_{2n+1} via an asymmetric split (n, n+1); computing n = 25 first is cheaper and already a record.
- Cross-check against the lace-expansion route: Clisby-Liang-Slade show that polygon counts plus lace graphs give c_n; a second method for the same term is exactly what the two-run rule needs.

## Pitfalls

- OEIS 'data' fields are truncated; the b-files and the Clisby-Liang-Slade data page hold the full records. Check both.
- Lattice naming: OEIS 'hexagonal' sometimes means triangular; A001666 is 'b.c.c. version 2'. Use the exact definitions of the record papers.
- Off-by-one and symmetry-factor errors give plausible-looking but wrong integers; reproduction of all lower terms plus a second independent run is mandatory.
- Integer overflow above 2^64 (c_25 in 5D is about 5.6e23); use 128-bit or arbitrary precision accumulators.
- A 2025 Utrecht bachelor thesis (Marloes de Groot, 'Enumerating self-avoiding walks by k-splitting', studenttheses.uu.nl handle 20.500.12932/48786) extends length doubling; its abstract reports no new counts, but read the full PDF before claiming novelty for any lattice.

## Sources

- https://personal.math.ubc.ca/~slade/lacecounts/
- https://personal.math.ubc.ca/~slade/se.pdf
- https://webspace.science.uu.nl/~bisse101/SAW/
- https://data.mendeley.com/datasets/xv59s4ckxg/1
- https://arxiv.org/abs/1104.2184
- https://arxiv.org/abs/1208.4758
- https://arxiv.org/abs/1703.09340
- https://oeis.org/A010575
- https://oeis.org/A010576
- https://oeis.org/A010577
- https://oeis.org/A001412
- https://oeis.org/A001666
- https://oeis.org/A001336
- https://oeis.org/A001411
- Status source: https://personal.math.ubc.ca/~slade/lacecounts/

## Citations

- [Problem page](../../../../.raw/V3R1T4S/known-unknowns/physics/saw-hypercubic-exact-enumeration.md)
- [Bank entry](../../../../.raw/V3R1T4S/bank/targets.json) (id `saw-hypercubic-exact-enumeration`, commit `7dd4480`)

## Related Nodes

- [[V3R1T4S Physics]]
- [[V3R1T4S]]
