---
id: v3r1t4s-minimizer-density-record-tables
type: entity
tags: [v3r1t4s, v3r1t4s/biology, kind/harvest]
inbound_links: 1
confidence: 0.8
last_ingested_sources: [".raw/V3R1T4S/bank/targets.json@7dd4480"]
status: "CONFIRMED_SOLUTION"
priority: "P1"
notes: "Cycle 25–26 (run 2026-10-18-1743, PR elder-plinius/V3R1T4S#425): CLSS SOS-DP Fast Zeta Transform for exact DNA tie-seam gamechangers improved 17 precomputed (w,k) cells by >=0.5% rel; flagship (w=12, k=4) lowered from 0.1360458389 to 0.1336292920 (-1.7763% rel, 573933439/2^32 vs 584312429/2^32), 3-skeptic panel all pass, packaged in outbox/2026-10-18-mizopl-537faa12 (CHECK_RUN: PASS), submitted as draft PR #425 (commit 792cddd)."
category: biology
kind: harvest
tractability: 3
compute: "laptop-hours"
disclosure: open
status_checked: "2026-10-18"
---
# Minimizer schemes: beat the lowest published DNA density for a (w, k) pair in the public minimizer density tables

# Overview

> Bank id `minimizer-density-record-tables` · harvest · tractability 3 · laptop-hours · disclosure **open**
> Bank says open as of 2026-10-15. Statuses go stale — re-check the primary source before any work.

## Statement

Minimizers are the sampling scheme underneath almost every modern sequence aligner and assembler: for parameters w and k, each window of w+k-1 bases contributes its minimal k-mer under some order, and the density (expected fraction of positions chosen) decides how much memory and time downstream tools use. Two public repositories maintain comparable density tables: OrensteinLab/GreedyMini (Shay Golan, Ido Tziony, Matan Kraus, Yaron Orenstein, Arseny Shur; Bioinformatics 2025) publishes precomputed orders and the densities they achieve, and OrensteinLab/10-minimizers (Shur, Tziony, Orenstein; WABI 2026) publishes CSV tables of DNA densities for GreedyMini, decycling, double decycling, miniception, mod-minimizer and the new spacers across wide ranges of w and k, plus the .gm order files. For example in w_extension_k12.csv at k = 12, w = 10 the listed densities are GreedyMini 0.141413, double decycling 0.149105, miniception 0.164318 and mod-minimizer 0.181827. Lowering any cell is a purely computational, exactly checkable record, and the density of an explicit order can be computed or estimated to tight precision on a laptop.

## Success criterion

An explicit minimizer order for a stated (w, k) pair, given either as a complete rank file or as deterministic released code that emits one, whose DNA density, computed by the skeptic with the repositories' own density measurement code, is STRICTLY LOWER (direction: min) than the smallest value listed for that (w, k) pair across the tables in github.com/OrensteinLab/10-minimizers and the precomputed minimizers of github.com/OrensteinLab/GreedyMini (both re-fetched live immediately before claiming) by at least 0.5% relative, with the comparison made under the same density definition (expected density for the expected-density tables, particular density on the same sequence otherwise) and with the order's storage cost stated.

## Partial wins

- {"id": "p1", "statement": "Beat the best listed density for a (w, k) cell with a constant-space scheme (no explicit table of k-mer ranks), which the WABI 2026 authors identify as the practically important regime."}
- {"id": "p2", "statement": "Reproduce a published GreedyMini density for a mid-sized cell (w + k around 20) from scratch with your own search and release the order, confirming the table entry independently."}
- {"id": "p3", "statement": "An exact computation (not sampling) of the density of a published order for a cell where only estimated values are listed, with the method and its error bound published."}

## Verification

Skeptic loads the claimed order, verifies it is a total order on all k-mers (or a well-defined constant-space rank function), then computes density either exactly by enumerating windows for small w+k or by the repositories' measurement scripts on the same random or genomic sequence they use, and compares with the live table cell. Seconds to minutes per cell.

## Angles

- GreedyMini builds orders greedily on binary alphabets and extends to DNA by interleaving bits; attack the interleaving step directly, since the extension is a design choice rather than an optimum.
- Cross-domain import (coding theory): a minimizer order is a covering-style object on the de Bruijn graph, so lower bounds and constructions for covering codes and decycling sets transfer, and the decycling family already in the table came from that tradition.
- Cross-domain import (scheduling): choosing one position per sliding window is an interval-covering problem; local search over which window positions are forced can be guided by exchange arguments from scheduling heuristics.
- Use exact density computation inside the search loop for small w+k, so the optimiser sees the true objective rather than a sampled estimate, then extend the winning structure to larger parameters.
- Target the regimes where the published curves cross (the tables show different schemes winning at different w), because a scheme that is uniformly best across a crossing region is both a record and a practical result.

## Pitfalls

- Expected density (over random sequences) and particular density (on a specific genome) are different numbers; comparing one against the other is the easiest false win here.
- Binary-alphabet densities and DNA densities differ; the tables state which is which and a claim must match.
- A table-based order with a huge rank table can beat constant-space schemes trivially; the storage cost must be stated, and the constant-space comparison kept separate.
- Sampling-based density estimates have error bars of their own; a 0.1% improvement measured by sampling may not exist, hence the 0.5% relative margin or an exact computation.
- Papers report densities at specific (w, k) and sometimes for a fixed sequence such as a human chromosome; reproduce the published value for a known order before claiming to beat a neighbouring cell.

## Sources

- https://github.com/OrensteinLab/10-minimizers
- https://github.com/OrensteinLab/GreedyMini
- https://drops.dagstuhl.de/storage/00lipics/lipics-vol390-wabi2026/LIPIcs.WABI.2026.5/LIPIcs.WABI.2026.5.pdf
- https://www.ebi.ac.uk/europepmc/webservices/rest/PMC12261476/fullTextXML
- Status source: https://github.com/OrensteinLab/10-minimizers

## Citations

- [Problem page](../../../../.raw/V3R1T4S/known-unknowns/biology/minimizer-density-record-tables.md)
- [Bank entry](../../../../.raw/V3R1T4S/bank/targets.json) (id `minimizer-density-record-tables`, commit `7dd4480`)

## Related Nodes

- [[V3R1T4S Biology]]
- [[V3R1T4S]]
