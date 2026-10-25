---
id: v3r1t4s-hest-bench-cancer-expression-from-morphology
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
tractability: 3
compute: "laptop-hours"
disclosure: open
status_checked: "2026-10-15"
---
# HEST-Benchmark: beat the best published Pearson for predicting spatial gene expression from tumour histology

# Overview

> Bank id `hest-bench-cancer-expression-from-morphology` · harvest · tractability 3 · laptop-hours · disclosure **open**
> Bank says open as of 2026-10-15. Statuses go stale — re-check the primary source before any work.

## Statement

HEST-1k (Guillaume Jaume, Paul Doucet, Andrew Song and colleagues at Mahmood Lab, NeurIPS 2024 Spotlight) pairs spatial-transcriptomics spots with the matching histology patches and defines HEST-Benchmark: predict the expression of 50 highly variable genes from a 112 x 112 micron patch at 0.5 micron per pixel, in nine tasks covering eight cancer types, scored by Pearson correlation with leave-one-patient-out style public splits. The public result table in the repository README (re-read live on 2026-10-15, table dated 03.04.26) lists 25 publicly available models scored identically with ridge regression on PCA-reduced (256 factors) patch embeddings. The live bests are: average across tasks 0.4229 (H-Optimus-1), with GenBio-PathFM 0.4197 and H-Optimus-0 0.4150; per task, IDC 0.6024 (H-Optimus-1), PRAD 0.3913 (GenBio-PathFM), PAAD 0.5159 (Virchow), SKCM 0.6715 (GenBio-PathFM), COAD 0.3284 (GenBio-PathFM), READ 0.2421 (H-Optimus-1), CCRCC 0.2719 (Virchow2), LUNG 0.5787 (GenBio-PathFM), LYMPH_IDC 0.2842 (GenBio-PathFM); a plain ImageNet ResNet50 reaches 0.3252 on average. Three tasks sit below 0.29 and the gap between a generic ResNet and billion-parameter pathology foundation models is only about 0.10 Pearson, which says the regression head and the spatial statistics - not the encoder - may be where the remaining signal is. The benchmark data are ungated on Hugging Face (MahmoodLab/hest-bench, 42 GB in total but per-task: SKCM 0.49 GB, LUNG 0.82 GB, PAAD 1.2 GB, COAD 2.47 GB), so a single-task attack is laptop-scale, and precomputed CTransPath embeddings ship in the fm_v1 folder.

## Success criterion

Success means, for one named HEST-Benchmark task, a saved per-spot prediction matrix for the 50 benchmark genes on every test split defined by that task's splits/test_*.csv files in https://huggingface.co/datasets/MahmoodLab/hest-bench, produced by a method trained only on the corresponding train_*.csv patients, and a mean Pearson correlation computed exactly as the HEST-Library's benchmark code computes it (same gene list, same per-gene then per-split averaging), that is STRICTLY HIGHER (direction: max) than the maximum value in that task's column over ALL model rows of the live HEST-Benchmark table at https://raw.githubusercontent.com/mahmoodlab/HEST/main/README.md - re-fetched and re-parsed immediately before claiming - by at least 0.015 absolute, with the gain surviving 5 random seeds reported as mean +/- std and exceeding 2x that std. The attacker must also re-run, in the same environment and splits, at least two published rows (one foundation model with precomputed or recomputable embeddings and the ResNet50 row) and land within 0.01 Pearson of their published values, or the comparison is void. No test-patient patch, expression value or summary statistic may enter training, gene filtering, normalisation, PCA fitting, hyperparameter choice or early stopping. Deliverables: pinned HEST-Library commit, dataset file sha256s, split files used, training and inference scripts, per-split prediction files, and the verbatim benchmark output for all tasks claimed.

## Partial wins

- {"id": "p1", "statement": "Beat the live best on two of the three weakest tasks (as of 2026-10-15: READ 0.2421, CCRCC 0.2719, LYMPH_IDC 0.2842) by >= 0.015 each with ONE frozen configuration, which is far stronger evidence than a single-task win on the easy IDC or SKCM tasks."}
- {"id": "p2", "statement": "Show that a non-foundation-model pipeline (stains-normalised classical texture/colour features, or a small CPU-trainable encoder) exceeds the published ResNet50 average of 0.3252 by >= 0.03 on at least four tasks, quantifying how much of the foundation-model advantage is reproducible without a large pretrained encoder."}
- {"id": "p3", "statement": "A spatial-leakage audit: re-score the published-style ridge pipeline after enforcing a minimum physical distance between training and test spots within the same slide, and report how much of the reported Pearson on each task is attributable to neighbouring-spot correlation. A benchmark-critique result, checkable from the saved spot coordinates and predictions."}

## Verification

Skeptic downloads the chosen task's folder from the ungated Hugging Face dataset (0.5-3 GB for most tasks), compares sha256s against the attacker's manifest, confirms the train/test patient lists match the published split csv files exactly, loads the attacker's predictions and recomputes the Pearson correlations with the HEST-Library's own benchmark function at a pinned commit (minutes), then re-runs the attacker's training for at least two seeds (laptop-hours) and the two baseline rows. The live record is read by curling the README and parsing the markdown table. Leakage audit: confirm that PCA, scalers, gene selection and any image-level statistics were fitted on training patients only, and that no spot from a test patient appears in training.

## Angles

- Conventional: replace ridge-on-PCA with a head that matches the data's structure - per-gene shrinkage toward the slide mean, multi-output reduced-rank regression, or a Poisson/negative-binomial likelihood on counts instead of Gaussian regression on normalised values.
- Conventional: use the spatial arrangement the published pipeline throws away - neighbourhood averaging of embeddings, conditional autoregressive smoothing of predictions, or multi-scale patches - while keeping the train/test patient split intact.
- Cross-domain import (signal processing / super-resolution): expression over a slide is a smooth field sampled on a lattice; borrow deconvolution and total-variation denoising from image restoration to separate the measurable low-frequency field from per-spot shot noise, and predict only the part that is predictable.
- Cross-domain import (geostatistics / kriging): this is literally a spatial prediction problem with a known covariance structure; fit a variogram per gene per slide and use kriging with the image embedding as external drift, which is the standard tool in mining and soil science for exactly this data shape.
- Cross-domain import (ecology / rarefaction): spot-level counts differ in sequencing depth exactly as ecological surveys differ in effort; coverage-based rarefaction per spot before correlating removes a nuisance axis that currently inflates variance in the weak tasks.
- Cross-domain import (compression / MDL): choose the number of PCA factors and the per-gene regularisation by description length rather than validation Pearson; with only a handful of patients per task, validation-based selection is itself extremely noisy.
- Ensembling encoders: the table shows 25 encoders whose errors are probably decorrelated; a rank- or precision-weighted ensemble of two or three embeddings, with weights fitted on training patients only, is cheap and untested in the published table.

## Pitfalls

- Spot-level leakage within a slide: patches from the same tumour region are strongly correlated, so any split that is not strictly by patient/sample, or any smoothing that crosses the train/test boundary, manufactures correlation. Verify the split files are used exactly as published.
- Metric definition drift: the published numbers are Pearson per gene averaged in a specific way after a specific normalisation (ridge on PCA-256 embeddings). Recomputing with a different gene set, different normalisation or a different averaging order moves the number by more than the 0.015 bar.
- Encoder provenance and training-data contamination: several listed encoders were pretrained on public cohorts that may overlap HEST slides. A claim built on a new pretrained encoder must state its pretraining corpus; otherwise an apparent win can be memorisation of the same slides.
- Single-seed and single-task cherry-picking: with few patients per task, seed and split variance is large. Five seeds, a 2x-std margin and a full nine-task report are required.
- Stale-table comparison: the README table has been updated repeatedly (entries dated 30.08.24 and 03.04.26) and accepts community pull requests, so the record must be re-read live before claiming.
- Over-claiming: predicting 50 highly variable genes from morphology at Pearson 0.4 is a benchmark result about tissue texture, not a diagnostic assay, and certainly not a substitute for sequencing a patient's tumour.

## Sources

- https://raw.githubusercontent.com/mahmoodlab/HEST/main/README.md
- https://github.com/mahmoodlab/HEST
- https://huggingface.co/datasets/MahmoodLab/hest-bench
- https://hest.readthedocs.io/en/latest/
- Status source: https://raw.githubusercontent.com/mahmoodlab/HEST/main/README.md

## Citations

- [Problem page](../../../../.raw/V3R1T4S/known-unknowns/disease-research/hest-bench-cancer-expression-from-morphology.md)
- [Bank entry](../../../../.raw/V3R1T4S/bank/targets.json) (id `hest-bench-cancer-expression-from-morphology`, commit `7dd4480`)

## Related Nodes

- [[V3R1T4S Disease research]]
- [[V3R1T4S]]
