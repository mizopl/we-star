---
id: v3r1t4s-nucleotide-transformer-benchmark-mcc
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
# Nucleotide Transformer benchmark: beat the best published MCC on a genomic regulatory task

# Overview

> Bank id `nucleotide-transformer-benchmark-mcc` · standard · tractability 3 · laptop-hours · disclosure **open**
> Bank says open as of 2026-10-15. Statuses go stale — re-check the primary source before any work.

## Statement

The Nucleotide Transformer downstream benchmark (Hugo Dalla-Torre and co-authors, InstaDeep; Nature Methods 2024) fixes 18 genomic classification tasks (histone marks such as H3K9me3 and H3K4me2, promoter and enhancer types, splice sites) with published train/test splits and ten-fold results. The public leaderboard space hosts benchmark.csv with 273 rows of per-fold Matthews correlation coefficients, F1 and accuracy for every model and task, so the exact distribution behind each bar is visible rather than a single number. Splice-site tasks are saturated (best ten-fold mean MCC 0.966-0.971) but the chromatin tasks are not: computed from that file, the best ten-fold mean MCC is 0.4807 on H3K9me3 (NT-1000G 2.5B), 0.4991 on H3K4me1 (Enformer), 0.5169 on H3K27ac (Enformer), 0.5186 on H2AFZ and 0.5694 on enhancer types, across 15-16 models per task. The data load from the Hugging Face hub without registration, and sequences are short enough (a few hundred to a few thousand bases) for a small convolutional model or a cached-embedding probe to be trained on a laptop.

## Success criterion

Predictions for every sequence of a benchmark task's test split, from a model trained only on that task's training split (pretrained weights allowed if their corpus is declared and contains no test-split labels), whose mean MCC over the benchmark's ten folds, recomputed by the skeptic with the standard MCC definition on the released splits, is STRICTLY HIGHER (direction: max) than the best mean MCC for that task in the leaderboard's benchmark.csv (re-fetched live immediately before claiming) by at least 0.02 absolute, with the fold-wise values published and a paired comparison over folds favouring the new method.

## Partial wins

- {"id": "p1", "statement": "Beat the best listed mean MCC on H3K9me3 (0.4807 as of 2026-10-15) by at least 0.02 with a model under 100M parameters."}
- {"id": "p2", "statement": "Beat the best listed mean MCC on any three of the 18 tasks at once with a single frozen architecture and training recipe."}
- {"id": "p3", "statement": "A reproducible audit of fold-to-fold variance on the histone tasks, showing which published ranking differences are inside the noise, with the per-fold numbers from benchmark.csv."}

## Verification

Skeptic loads the task's released splits from the Hugging Face hub, checks the prediction file covers each test sequence per fold exactly once, computes MCC per fold, compares with the per-fold arrays in benchmark.csv, reruns the attacker's training from the released seed for at least one fold, and checks for overlap between training and test sequences. An hour or two.

## Angles

- Histone-mark tasks are about nucleosome positioning and sequence composition; engineered k-mer and periodicity features with a gradient-boosted tree are a serious baseline and run in minutes.
- Cross-domain import (audio): dinucleotide periodicity around 10 base pairs is a helical-phasing signal, so a filterbank or spectral front end may capture what a token-level transformer dilutes.
- Cross-domain import (clinical trials): with ten folds and small effects, use paired tests across folds rather than comparing means, and design the experiment to detect a stated effect size.
- Reverse-complement equivalence is a free symmetry; averaging over both strands at inference costs nothing and is not standard in all published entries.
- Probe cached embeddings from several released genomic models and ensemble them, which separates the value of pretraining from the value of fine-tuning compute.

## Pitfalls

- Genomic regions can be near-duplicated between train and test splits; verify the split as released rather than assuming it is clean, and report any overlap found.
- Reporting the best fold instead of the mean over folds is a common inflation; the criterion requires the ten-fold mean and the per-fold values.
- MCC, F1 and accuracy rank models differently on imbalanced histone tasks; compare against the same metric the leaderboard lists.
- Large pretrained genomic models saw most of the human genome, so they may have seen the test regions unlabelled; this is allowed but must be declared, and a claim of 'no leakage' needs the label check, not a corpus claim.
- A gain on a histone-mark classifier is a step in regulatory genomics, not evidence about any disease mechanism.

## Sources

- https://huggingface.co/spaces/InstaDeepAI/nucleotide_transformer_benchmark
- https://huggingface.co/spaces/InstaDeepAI/nucleotide_transformer_benchmark/blob/main/data/benchmark.csv
- https://www.ebi.ac.uk/europepmc/webservices/rest/PMC11810778/fullTextXML
- https://github.com/instadeepai/nucleotide-transformer
- Status source: https://huggingface.co/spaces/InstaDeepAI/nucleotide_transformer_benchmark/blob/main/data/benchmark.csv

## Citations

- [Problem page](../../../../.raw/V3R1T4S/known-unknowns/biology/nucleotide-transformer-benchmark-mcc.md)
- [Bank entry](../../../../.raw/V3R1T4S/bank/targets.json) (id `nucleotide-transformer-benchmark-mcc`, commit `7dd4480`)

## Related Nodes

- [[V3R1T4S Biology]]
- [[V3R1T4S]]
