---
id: v3r1t4s-openproblems-predict-modality-cite-rmse
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
compute: "laptop-hours"
disclosure: open
status_checked: "2026-10-15"
---
# Open Problems predict modality: beat the best listed RMSE for predicting protein abundance from RNA (and RNA from ATAC) on NeurIPS 2021/2022 data

# Overview

> Bank id `openproblems-predict-modality-cite-rmse` · standard · tractability 2.5 · laptop-hours · disclosure **open**
> Bank says open as of 2026-10-15. Statuses go stale — re-check the primary source before any work.

## Statement

The Open Problems 'predict modality' task (authors incl. Alejandro Granados, Alex Tong, Bastian Rieck, Daniel Burkhardt, Louise Deconinck, Robrecht Cannoodt, Vladimir Shitov) asks methods to predict one single-cell modality from another on held-out donors/sites of the NeurIPS 2021 (BMMC CITE-seq and multiome) and NeurIPS 2022 (PBMC) datasets. The task is actively re-run (latest public run run_2026-10-10_07-15-14) and the top of the board is tight: on openproblems_neurips2021/bmmc_cite/normal (RNA to protein) the best RMSE is 0.6561 (senkin & tmp), then 0.6576 (SS-OPM), 0.6634 (Guanlab-dengkw); on bmmc_multiome/swap the best RMSE is 0.5143 (Guanlab-dengkw); on neurips2022 pbmc_multiome/swap the best RMSE is 0.3552 (SS-OPM), with a clear gap to second place. Several entries are NeurIPS 2021/2022 competition winners, so a strict improvement is a genuine advance on a well-studied problem.

## Success criterion

On a dataset/direction of the latest predict-modality run (live page and newest score file on the openproblems-data S3 bucket, re-fetched live immediately before claiming), a frozen method trained only on train_mod1/train_mod2 and given test_mod1 produces predictions whose RMSE, recomputed by the skeptic with the official metric component of github.com/openproblems-bio/task_predict_modality against test_mod2, is STRICTLY LOWER (direction: min) than every non-control method listed for that dataset by at least 0.5% relative, and whose mean Pearson per cell is not lower than the best listed value minus 0.005.

## Partial wins

- {"id": "p1", "statement": "Beat the listed best RMSE on neurips2022 pbmc_multiome/swap (where one method leads by a wide margin) or bmmc_cite/normal by >= 0.5% relative under the full criterion."}
- {"id": "p2", "statement": "A leakage-free ensemble of the publicly released top methods (SS-OPM, senkin & tmp, Guanlab-dengkw) with weights chosen on a donor-held-out split of the TRAINING data, beating every individual listed method on one dataset."}

## Verification

Skeptic downloads the train/test h5ad files for the dataset from the public S3 bucket, runs the attacker's frozen code with test_mod2 absent, scores with the official metric component, and compares with the newest score file and the live page. Training data are 0.4-0.7 GB per dataset; laptop-hours.

## Angles

- Ensemble the strongest public solutions with weights fitted on a donor-held-out split of the training data; competition winners are often individually close but make different errors.
- Cross-domain import (machine translation): treat RNA-to-protein as translation and use kNN-retrieval-augmented prediction (kNN-MT): blend a parametric model with the averaged targets of nearest training cells in a learned embedding.
- Cross-domain import (geophysics / data assimilation): use an optimal-interpolation (Kalman-style) correction where the prior is a population-level prediction and the observation is each cell's RNA neighbourhood.
- Donor/batch shift is the main difficulty: fit domain-adversarial or simple moment-matching (CORAL) alignment of test_mod1 to the training distribution before prediction; it needs no test labels.
- For ATAC-to-RNA, use gene-activity scores (peaks within gene bodies and promoters) as a prior feature set and learn only residuals, which is cheap and robust.

## Pitfalls

- test_mod2 is the label and is downloadable from the same bucket; the skeptic runs the method without it present.
- Tuning hyperparameters by looking at test RMSE (even through the leaderboard numbers) is overfitting; tune only on held-out donors from the training data.
- Normalisation variants (log_cp10k, sqrt_cp10k, l1_sqrt) produce different RMSE scales; compare only against the same dataset/normalisation the leaderboard uses.
- The leaderboard is being re-run often (several runs in Sep-Oct 2026), so the record can move under you; re-fetch before claiming.

## Sources

- https://openproblems.bio/benchmarks/predict_modality/
- https://github.com/openproblems-bio/task_predict_modality
- https://openproblems-data.s3.amazonaws.com/?list-type=2&prefix=resources/task_predict_modality/
- Status source: https://openproblems.bio/benchmarks/predict_modality/

## Citations

- [Problem page](../../../../.raw/V3R1T4S/known-unknowns/biology/openproblems-predict-modality-cite-rmse.md)
- [Bank entry](../../../../.raw/V3R1T4S/bank/targets.json) (id `openproblems-predict-modality-cite-rmse`, commit `7dd4480`)

## Related Nodes

- [[V3R1T4S Biology]]
- [[V3R1T4S]]
