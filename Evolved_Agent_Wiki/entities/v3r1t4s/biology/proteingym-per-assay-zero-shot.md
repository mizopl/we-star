---
id: v3r1t4s-proteingym-per-assay-zero-shot
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
tractability: 1.5
compute: "laptop-hours"
disclosure: open
status_checked: "2026-10-15"
---
# ProteinGym zero-shot substitutions: beat every listed model's Spearman on a single DMS assay

# Overview

> Bank id `proteingym-per-assay-zero-shot` · standard · tractability 1.5 · laptop-hours · disclosure **open**
> Bank says open as of 2026-10-15. Statuses go stale — re-check the primary source before any work.

## Statement

ProteinGym (OATML-Markslab) publishes, for 217 deep-mutational-scanning assays, the Spearman correlation of every benchmarked zero-shot fitness predictor (~100 models) in DMS_substitutions_Spearman_DMS_level.csv; the overall leaders (AIDO Protein-RAG 16B, VenusREM, ~0.518 average) are listed in the Summary CSV. Restricted to non-disease assays (stability, activity, binding, expression of non-pathogen proteins). Produce zero-shot scores (no use of the assay's own labels) that achieve a Spearman strictly higher than the maximum over all listed models for at least one assay.

## Success criterion

For one non-disease assay in the live DMS-level CSV at https://raw.githubusercontent.com/OATML-Markslab/ProteinGym/main/benchmarks/DMS_zero_shot/substitutions/Spearman/DMS_substitutions_Spearman_DMS_level.csv (re-fetched immediately before claiming), a saved score file (mutant, score) produced by a frozen, pre-registered method whose code never reads the assay's DMS_score column, such that ProteinGym's own Spearman routine yields a value strictly greater than the row maximum over all listed models; the method's hyperparameters must be fixed before scoring the target assay (pre-registration hash), and the same method must be run on all assays in the same function category with results reported.

## Partial wins

- {"id": "category-top10", "statement": "A frozen laptop-runnable method (<= 650M params) whose average Spearman over all Stability assays exceeds the 10th-ranked model's Stability column in the Summary CSV."}
- {"id": "low-msa-assay-win", "statement": "Beat the row max on a Low_MSA_depth assay with a method using no MSA."}

## Verification

Download the assay CSV from the ProteinGym data release, run the official Spearman computation on the submitted score file, compare to the live DMS-level row max; skeptic re-runs the frozen method on the assay from the pre-registered commit to reproduce the score file byte-for-byte (or within float tolerance). Under an hour per assay for small models.

## Angles

- Rank-average ensemble of precomputed ProteinGym model scores (released in the repo) plus ESM-2 650M masked-marginals, with ensemble weights fixed from OTHER assays only.
- Structure-aware thermodynamic proxy: ESM-IF / ProteinMPNN log-likelihoods on the AlphaFold DB structure for stability assays.
- Evolutionary model: EVmutation/Potts model trained on a fresh jackhmmer MSA with tuned reweighting, combined with site-conservation priors.
- Cross-domain import (recommender systems): low-rank matrix factorisation across assays x models to learn which model families transfer to which protein families, then pick per-assay without using its labels.
- Cross-domain import (econometrics/forecast combination): Bates-Granger optimal forecast combination with shrinkage, fit leave-one-assay-out.
- Cross-domain import (NLP calibration): temperature/position-specific calibration of PLM logits using unlabeled mutational spectra (entropy normalization per site).

## Pitfalls

- Label leakage: any tuning, ensembling weight or model selection that touches the target assay's DMS_score is supervised, not zero-shot. Freeze before scoring.
- Cherry-picking: beating the row max on one of 217 assays by chance is likely for a noisy small assay; require the frozen method be reported on the whole category and pre-registered.
- Several assay rows have very few mutants; Spearman bootstrap SE can exceed the margin. Require margin > bootstrap SE.
- Disease-relevant assays (human disease genes, viral proteins) belong to another lane; restrict to non-disease assays.
- The CSVs on main changed in Jan/Mar 2026; always compare to the live file, not a cached copy.

## Sources

- https://raw.githubusercontent.com/OATML-Markslab/ProteinGym/main/benchmarks/DMS_zero_shot/substitutions/Spearman/DMS_substitutions_Spearman_DMS_level.csv
- https://proteingym.org/benchmarks
- https://raw.githubusercontent.com/OATML-Markslab/ProteinGym/main/benchmarks/DMS_zero_shot/substitutions/Spearman/Summary_performance_DMS_substitutions_Spearman.csv
- Status source: https://raw.githubusercontent.com/OATML-Markslab/ProteinGym/main/benchmarks/DMS_zero_shot/substitutions/Spearman/DMS_substitutions_Spearman_DMS_level.csv

## Citations

- [Problem page](../../../../.raw/V3R1T4S/known-unknowns/biology/proteingym-per-assay-zero-shot.md)
- [Bank entry](../../../../.raw/V3R1T4S/bank/targets.json) (id `proteingym-per-assay-zero-shot`, commit `7dd4480`)

## Related Nodes

- [[V3R1T4S Biology]]
- [[V3R1T4S]]
