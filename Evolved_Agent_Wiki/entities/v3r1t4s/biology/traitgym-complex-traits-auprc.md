---
id: v3r1t4s-traitgym-complex-traits-auprc
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
# TraitGym complex traits: beat the best AUPRC for picking the causal regulatory variant among matched controls

# Overview

> Bank id `traitgym-complex-traits-auprc` · standard · tractability 3 · laptop-hours · disclosure **open**
> Bank says open as of 2026-10-15. Statuses go stale — re-check the primary source before any work.

## Statement

TraitGym (Gonzalo Benegas, Gokcen Eraslan, Yun S. Song; bioRxiv 2025.02.11.637758) asks a model to tell a likely causal non-coding variant from nine control variants matched on allele frequency, distance to gene and other summary statistics. The complex-traits set is built from fine-mapped UK Biobank associations across 83 traits. The main metric is AUPRC averaged over chromosomes, weighted by chromosome. In the published metric files under complex_traits_matched_9/AUPRC_by_chrom_weighted_average/all (75 files, read directly from the Hugging Face dataset over plain HTTPS), the best entry is the CADD+GPN-MSA+Borzoi logistic-regression combination at 0.3623 (standard error 0.0155), then CADD+Borzoi 0.3509 and GPN-MSA+Borzoi 0.3491; the best single supervised model is Enformer at 0.3033 and the best zero-shot score is CADD at 0.2499. Ten of eleven variants in each group are controls, so a perfect method would reach 1.0 and random guessing about 0.1: the field is far from solving this. All variant tables, precomputed features and per-model metric files are public; the scoring is a short Snakemake rule the skeptic can rerun.

## Success criterion

A score (or probability) for every variant in complex_traits_matched_9 test split, produced by a method whose feature extraction and training read no causal/control label outside the chromosomes used for training under the benchmark's own by-chromosome cross-validation, whose AUPRC_by_chrom_weighted_average recomputed by the skeptic with the TraitGym repository's metric rule is STRICTLY HIGHER (direction: max) than the best value among the published per-model CSVs in that directory and on the leaderboard space (both re-fetched live immediately before claiming) by at least 0.02 absolute, with a bootstrap 95% interval over chromosomes that excludes the previous best.

## Partial wins

- {"id": "p1", "statement": "Beat the best zero-shot entry (CADD at 0.2499 as of 2026-10-15) by at least 0.02 AUPRC with a score that uses no supervised training on TraitGym labels at all."}
- {"id": "p2", "statement": "Match or beat the best listed combination on the complex-traits set using only features that run on a laptop CPU (no Enformer or Borzoi forward passes), reusing the published feature parquet files."}
- {"id": "p3", "statement": "A reproducible demonstration, from the public variant tables alone, that part of the remaining gap comes from control variants that are themselves plausibly causal (mismatched matching), quantified on a subset and with an honest statement of how it changes the ceiling."}

## Verification

Skeptic downloads the dataset's test parquet and the relevant feature parquet files from the Hugging Face dataset repository over plain HTTPS (about 6.7 GB for everything, far less for one feature set), checks the submitted score file covers each variant exactly once, runs the repository's AUPRC_by_chrom_weighted_average computation, compares with the published per-model CSVs, and audits the code for use of labels outside the training chromosomes. Minutes.

## Angles

- The controls are matched on summary statistics but not on local sequence context; a model that predicts the matching variables themselves will look good and generalise badly, so build a control-matching-invariant representation on purpose and measure what is left.
- Cross-domain import (information retrieval): this is a ranking problem with one positive per group of eleven, so train a listwise ranking loss within groups instead of pointwise classification, which the published logistic regressions use.
- Cross-domain import (econometrics): treat fine-mapping posterior probabilities as noisy labels and fit a measurement-error model, since the positives are themselves statistical calls rather than experimentally confirmed causal variants.
- Combine the released feature parquet files with simple interaction terms (conservation x predicted regulatory activity x distance) that the linear probes cannot represent, keeping everything on CPU.
- Look per-trait and per-consequence subset: the repository publishes subsets such as 3_prime_UTR_variant and disease, and a method that wins on the whole set but loses on every subset is overfitting the mix.

## Pitfalls

- Chromosome leakage: feature selection, hyperparameters or calibration fitted on all chromosomes and then scored by by-chromosome cross-validation inflates the result; everything must respect the chromosome split.
- Reusing a model that was pretrained on the UK Biobank fine-mapping results, or on CADD scores derived from them, can smuggle the labels in; declare every external score used.
- Comparing a 'matched_9' result against the 'all' (unmatched) dataset, or complex traits against Mendelian traits, compares to a different and much easier bar.
- AUPRC on these group sizes is noisy; a 0.01 gain is within the published standard errors (around 0.010-0.016), hence the 0.02 margin plus bootstrap requirement.
- A benchmark gain here means better prioritisation of candidate variants for follow-up, not a demonstrated causal mechanism or a clinical finding.

## Sources

- https://huggingface.co/datasets/songlab/TraitGym
- https://github.com/songlab-cal/TraitGym
- https://www.biorxiv.org/content/10.1101/2025.02.11.637758v2
- https://huggingface.co/spaces/songlab/TraitGym-leaderboard
- Status source: https://huggingface.co/datasets/songlab/TraitGym/tree/main/complex_traits_matched_9/AUPRC_by_chrom_weighted_average/all

## Citations

- [Problem page](../../../../.raw/V3R1T4S/known-unknowns/biology/traitgym-complex-traits-auprc.md)
- [Bank entry](../../../../.raw/V3R1T4S/bank/targets.json) (id `traitgym-complex-traits-auprc`, commit `7dd4480`)

## Related Nodes

- [[V3R1T4S Biology]]
- [[V3R1T4S]]
