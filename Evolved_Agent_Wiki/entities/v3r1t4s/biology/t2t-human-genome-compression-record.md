---
id: v3r1t4s-t2t-human-genome-compression-record
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
tractability: 2.5
compute: "laptop-days"
disclosure: open
status_checked: "2026-10-15"
---
# T2T human genome compression: beat the best bits-per-base entry in the public human-genome compression table

# Overview

> Bank id `t2t-human-genome-compression-record` · standard · tractability 2.5 · laptop-days · disclosure **open**
> Bank says open as of 2026-10-15. Statuses go stale — re-check the primary source before any work.

## Statement

The cobilab human-genome compression table (github.com/cobilab/HumanGenome, maintained by Diogo Pratas and colleagues) is a ranked record table for lossless reference-free compression of the T2T CHM13 v2.0 human genome: 3,117,292,120 DNA symbols, baseline 2 bits per symbol. The current top entry is JARVIS3 at 538,155,679 bytes (1.381 bits per base), followed by a reproducible JARVIS3 run at 539,129,963 bytes (1.384, 641 minutes, 13.7 GB RAM), several JARVIS2 entries near 1.395, GeCo3 near 1.425, and general-purpose compressors far behind (nncp 1.514, paq8l 1.571, zstd/lzma around 1.66). Every entry links a replication script, the sequence is a public S3 object, and the JARVIS3 paper (Maria J. P. Sousa, Armando J. Pinho, Diogo Pratas, Bioinformatics 2024) describes this as the best result to date on this benchmark. Verification is a byte count plus an exact round-trip decompression, which is as mechanical as a record check gets.

## Success criterion

A compressor (source code released, deterministic, no network access at run time, no reference genome or external sequence database embedded beyond what the entry declares) that losslessly compresses the chm13v2.0 DNA symbol stream, as defined by the table's own scripts, to STRICTLY FEWER bytes (direction: min) than the top entry in the table at https://github.com/cobilab/HumanGenome (re-fetched live immediately before claiming), with the decompressed output byte-identical to the input, the model size included in the reported total, and the full command line and hardware stated. A margin of at least 0.1% of the compressed size is required to exclude bookkeeping differences.

## Partial wins

- {"id": "p1", "statement": "Reproduce the top JARVIS3 entry's byte count from its replication script on commodity hardware and publish the timing and memory, confirming the record is reproducible (the top row's time and memory are listed as unknown)."}
- {"id": "p2", "statement": "Beat the best entry on the companion Cassava genome table (github.com/cobilab/CassavaGenome, top entry JARVIS2 at 69,078,516 bytes / 0.7249 bits per base) under the same round-trip rule."}
- {"id": "p3", "statement": "Beat the best general-purpose compressor entry (nncp at 1.514 bits per base) with a method that uses under 2 GB of RAM and finishes in under two hours, which would make strong DNA compression practical on a laptop."}

## Verification

Skeptic downloads chm13v2.0.fa.gz from the public human-pangenomics S3 bucket, prepares the symbol stream exactly as the table's scripts do, runs the claimed compressor and then its decompressor in a clean environment with no network, checks byte-identity with the original and the total output size (including any model or parameter files), and compares with the live table. Hours of compute, fully mechanical.

## Angles

- The leaders are mixtures of finite-context models with neural mixing; the remaining redundancy is mostly long-range repeats, so add an explicit repeat-aware match model with a large hash and let the mixer arbitrate.
- Cross-domain import (text compression contests): techniques from the Hutter-prize lineage, such as two-pass parameter tuning and context-mixing with SSE stages, have not been fully ported to four-symbol alphabets.
- Cross-domain import (database systems): tune for the memory hierarchy, since the practical limit here is RAM and cache misses rather than model quality; a smaller model that fits in cache can afford more passes.
- Exploit biology the general compressors ignore: satellite arrays and segmental duplications, newly complete in T2T, are highly structured, and a model keyed on tandem-repeat period could pay for itself.
- Measure where the bits actually go per chromosome arm and attack only the worst region, rather than tuning the global average.

## Pitfalls

- Shipping a model trained on the same genome, or on a reference that contains it, and not counting that model's size, is the classic false win; the total must include everything needed to decompress.
- Decompression must be exact and must be demonstrated, not asserted; a compressor that loses line breaks, case, or ambiguity codes is not comparable to the table entries.
- The table's entries use a specific symbol stream (DNA symbols only, as the scripts prepare it); comparing a FASTA-file size against a symbol-stream size is apples to oranges.
- Runtime matters for reproducibility but not for the ranking, so a 100x slower entry still counts; say so honestly instead of implying practicality.
- The top row currently lists unknown time and memory; the claim must compare against its byte count as published, and the skeptic should note if the row changes.

## Sources

- https://github.com/cobilab/HumanGenome
- https://raw.githubusercontent.com/cobilab/HumanGenome/main/README.md
- https://www.ebi.ac.uk/europepmc/webservices/rest/PMC11645547/fullTextXML
- https://github.com/cobilab/jarvis3
- https://s3-us-west-2.amazonaws.com/human-pangenomics/T2T/CHM13/assemblies/analysis_set/chm13v2.0.fa.gz
- Status source: https://github.com/cobilab/HumanGenome

## Citations

- [Problem page](../../../../.raw/V3R1T4S/known-unknowns/biology/t2t-human-genome-compression-record.md)
- [Bank entry](../../../../.raw/V3R1T4S/bank/targets.json) (id `t2t-human-genome-compression-record`, commit `7dd4480`)

## Related Nodes

- [[V3R1T4S Biology]]
- [[V3R1T4S]]
