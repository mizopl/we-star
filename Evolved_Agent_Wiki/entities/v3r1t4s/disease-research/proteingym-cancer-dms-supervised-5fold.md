---
id: v3r1t4s-proteingym-cancer-dms-supervised-5fold
type: entity
tags: [v3r1t4s, v3r1t4s/disease-research, kind/harvest]
inbound_links: 1
confidence: 0.8
last_ingested_sources: [".raw/V3R1T4S/bank/targets.json@7dd4480"]
status: "open"
priority: ""
notes: ""
category: disease-research
kind: harvest
tractability: 4
compute: "laptop-hours"
disclosure: open
status_checked: "2026-10-15"
---
# ProteinGym supervised benchmark: beat the public best 5-fold Spearman on a cancer-gene DMS assay

# Overview

> Bank id `proteingym-cancer-dms-supervised-5fold` · harvest · tractability 4 · laptop-hours · disclosure **open**
> Bank says open as of 2026-10-15. Statuses go stale — re-check the primary source before any work.

## Statement

ProteinGym also publishes a SUPERVISED benchmark with frozen cross-validation schemes (random, modulo and contiguous 5-fold), per-assay Spearman for 11 methods, in plain CSVs in the repo (benchmarks/DMS_supervised/substitutions/Spearman/DMS_substitutions_Spearman_DMS_level_fold_random_5.csv and the modulo/contiguous variants). Because the folds are fixed and published, a claimed improvement is exactly reproducible. The cancer-gene rows in the random-5 scheme as of 2026-10-13: BRCA1_HUMAN_Findlay_2018 best 0.683 (Kermut; ProteinNPT 0.559, Tranception Embeddings 0.573); MSH2_HUMAN_Jia_2020 best 0.665 (Kermut; ProteinNPT 0.526, One-Hot 0.513); P53_HUMAN_Kotler_2018 best 0.791 (Kermut; MSA Transformer Embeddings 0.742, ProteinNPT 0.736); PTEN_HUMAN_Mighell_2018 best 0.647 (Kermut; ProteinNPT 0.632); RASK_HUMAN_Weng_2022_abundance best 0.787 (Tranception Embeddings; ProteinNPT 0.786, Kermut 0.769). Only ELEVEN methods are listed, the leader is a Gaussian-process model over embeddings, and the whole task is regression on a few thousand rows with precomputed embeddings - squarely laptop-scale, and the kind of narrow numeric frontier where a better kernel, better embedding mixture or better uncertainty treatment plausibly wins within laptop-hours.

## Success criterion

Success means, for one cancer-gene DMS assay and one of the three published fold schemes, out-of-fold predictions for every mutant in ProteinGym's reference file for that assay, produced by training the method five times on the four complementary folds defined by ProteinGym's own published fold assignment column (sha256 logged) and predicting the held-out fold each time, such that the Spearman between the concatenated out-of-fold predictions and the measured DMS scores, recomputed by the skeptic in ProteinGym's convention, is STRICTLY HIGHER (direction: max) than the maximum over all method columns for that assay in the live CSV for the SAME fold scheme (re-fetched immediately before claiming) by at least 0.015 absolute. All hyperparameters, kernels, embedding choices, feature transforms and early-stopping rules must be fixed before the target assay is scored and pre-registered with a sha256-stamped file; they may be tuned only on assays with different UniProt IDs, or by nested cross-validation INSIDE each training fold (never using the held-out fold). Deliverables: the per-fold prediction files, the fold assignment used, the pre-registration file, the method code, and all five trained-model configs.

## Partial wins

- {"id": "p1", "statement": "Beat the live per-assay best by >= 0.015 on the SAME cancer-gene assay in two of the three fold schemes (random-5, modulo-5, contiguous-5) with one frozen configuration. The contiguous scheme is the hardest extrapolation setting and a win there is substantially stronger."}
- {"id": "p2", "statement": "Beat the live best on MSH2_HUMAN_Jia_2020 (0.665 random-5 as of 2026-10-13, 16,749 mutants) by >= 0.02 Spearman with the full pre-registered protocol."}
- {"id": "p3", "statement": "A same-protocol reproduction of the published leader (Kermut) on one cancer-gene assay, landing within 0.01 Spearman of the published value, with full logs. Independently checkable, non-trivial, and a prerequisite for believing any improvement claim; report it as a reproduction, not a record."}

## Verification

Skeptic downloads the assay's reference file and ProteinGym's published fold assignments, checks sha256s, verifies the attacker's out-of-fold predictions cover every mutant exactly once and that each prediction came from a model trained without that mutant's fold (by re-running the five trainings from the attacker's code and configs; laptop-hours with precomputed embeddings), recomputes the concatenated Spearman in ProteinGym's convention, and re-fetches the live CSV for the same fold scheme to read the per-assay maximum. Leakage audit: confirm the pre-registration predates scoring, that embeddings were not fitted on the assay's labels, that no target-encoding or label-derived feature (per-position mean score, label-based clustering) crossed fold boundaries, and that nested tuning never touched the held-out fold.

## Angles

- Conventional: better kernels over existing embeddings - the leader is a GP, so composite kernels (Matern over embeddings x Hamming over mutated positions x one-hot amino-acid kernel), automatic relevance determination, and proper marginal-likelihood optimisation inside each training fold are the obvious next step.
- Conventional: stack zero-shot scores as a prior mean for the supervised GP (the zero-shot columns are public and label-free), which is the cheapest reliable way to lift supervised Spearman on small assays.
- Cross-domain import (coding theory): represent each variant as a codeword over positions and amino acids and use a Hamming-weighted kernel plus syndrome-style features (which positions changed, to which chemical class), i.e. treat the DMS set as a punctured code and exploit its algebraic structure instead of relying on dense embeddings.
- Cross-domain import (statistical physics / epistasis): add a Potts-model statistical energy and explicit pairwise-epistasis features from DCA on the protein family as GP input dimensions; supervised models on single proteins rarely include couplings, and the contiguous-fold scheme punishes models that cannot extrapolate across the sequence.
- Cross-domain import (compression / MDL): select kernel complexity and feature subsets by description length rather than inner-fold Spearman, which is the right regulariser when the training folds are small (265-1,800 mutants for some assays) and inner-fold selection is itself noisy.
- Cross-domain import (signal processing): treat the position-by-amino-acid score matrix as a 2-D signal and denoise it with a separable wavelet or total-variation prior before fitting, exploiting the strong smoothness of DMS landscapes along the position axis.
- Uncertainty-aware prediction: because Spearman rewards correct ordering, convert the GP posterior into a rank-optimal point prediction (e.g. the posterior median or an expected-rank transform) rather than the posterior mean.

## Pitfalls

- Fold-boundary leakage is the dominant trap and is subtle: any per-position label statistic, label-based clustering, target encoding, or embedding fine-tuned on the full assay crosses the fold boundary while looking like honest feature engineering. The skeptic must re-run the five trainings rather than trust the out-of-fold file.
- Fold-scheme confusion: random-5, modulo-5 and contiguous-5 have different records in different CSVs; comparing a random-5 result against a contiguous-5 record (or against the zero-shot CSV, which is a different benchmark entirely) is an easy and fatal error.
- Protein-level tuning leakage: PTEN, P53, RASK and VKOR1 each appear in several assays; tuning on one and scoring another shares the same protein's labels. Exclusion must be by UniProt ID.
- Cross-benchmark confusion: ProteinGym also publishes clinical_supervised and clinical_zero_shot benchmarks with their own tables; a number from one benchmark never beats a record in another.
- Small-assay noise: BRCA2_HUMAN_Erwood_2022_HEK293T has 265 mutants, so 5-fold Spearman swings by far more than 0.015 across seeds. Prefer the large assays, and report seed variability for anything under ~2,000 mutants.
- Over-claiming clinical relevance: a supervised model fitted on a laboratory mutational scan is not a clinical variant classifier, and the write-up must say so explicitly.

## Sources

- https://raw.githubusercontent.com/OATML-Markslab/ProteinGym/main/benchmarks/DMS_supervised/substitutions/Spearman/DMS_substitutions_Spearman_DMS_level_fold_random_5.csv
- https://proteingym.org/benchmarks
- https://github.com/OATML-Markslab/ProteinGym
- Status source: https://raw.githubusercontent.com/OATML-Markslab/ProteinGym/main/benchmarks/DMS_supervised/substitutions/Spearman/DMS_substitutions_Spearman_DMS_level_fold_random_5.csv

## Citations

- [Problem page](../../../../.raw/V3R1T4S/known-unknowns/disease-research/proteingym-cancer-dms-supervised-5fold.md)
- [Bank entry](../../../../.raw/V3R1T4S/bank/targets.json) (id `proteingym-cancer-dms-supervised-5fold`, commit `7dd4480`)

## Related Nodes

- [[V3R1T4S Disease research]]
- [[V3R1T4S]]
