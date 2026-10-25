---
id: v3r1t4s-polaris-adme-fang-biogen-endpoints
type: entity
tags: [v3r1t4s, v3r1t4s/drug-discovery, kind/harvest]
inbound_links: 1
confidence: 0.8
last_ingested_sources: [".raw/V3R1T4S/bank/targets.json@7dd4480"]
status: "open"
priority: ""
notes: ""
category: drug-discovery
kind: harvest
tractability: 3
compute: "laptop-hours"
disclosure: open
status_checked: "2026-10-15"
---
# Polaris ADME-Fang (Biogen 3,521-compound DMPK set): beat the top listed score on an endpoint's public fold

# Overview

> Bank id `polaris-adme-fang-biogen-endpoints` · harvest · tractability 3 · laptop-hours · disclosure **open**
> Bank says open as of 2026-10-15. Statuses go stale — re-check the primary source before any work.

## Statement

Polaris hosts the Fang et al. 2023 Biogen DMPK dataset (3,521 compounds, six in vitro ADME endpoints, data public at github.com/molecularinformatics/Computational-ADME) as two generations of benchmarks: polaris/adme-fang-{solu,perm,rppb,hppb,rclint,hclint}-1 (Dec 2023, main metric pearsonr) and biogen/adme-fang-{...}-reg-v1 plus multi-task variants (Jul 2024). Several leaderboards are populated by large pretrained models - polaris/adme-fang-perm-1 best MAE 0.238 / Pearson 0.879 (1B_MPNN_MolGPS), polaris/adme-fang-solu-1 best MAE 0.312 / Pearson 0.770, polaris/adme-fang-rppb-1 Pearson 0.908 on only 24 test compounds, polaris/adme-fang-hppb-1 Pearson 0.888 on 34, biogen/adme-fang-perm-reg-v1 topped by a community 'vidraft-perm-structure-only-ensemble' at MAE 0.316 - while biogen/adme-fang-rclint-reg-v1 and biogen/adme-fang-hclint-reg-v1 are EMPTY. Split indices and table.parquet are served anonymously by the public API (verified 200 for the adme-fang-1 parquet and for the perm-1 benchmark's explicit test index array), so scoring is fully offline. The open question per endpoint: can a CPU-only descriptor model beat the listed best on the official fold?

## Success criterion

Pick one named ADME-Fang benchmark whose live leaderboard has at least one entry (empty leaderboards are excluded: a first submission is not a record). Success means a saved prediction file (one prediction per official test row in official order; manifest with the full slug, the sha256 of the downloaded table.parquet and the exact test index array from https://polarishub.io/api/v1/benchmark/<owner>/<slug>) such that (a) the test rows and label column match the API's split and targetCols exactly, (b) the skeptic's own computation of the benchmark's mainMetric is strictly better in that metric's direction than EVERY value listed in the live leaderboard table, re-fetched immediately before claiming, (c) for benchmarks with at least 300 test rows the margin is at least 0.010 absolute (correlation metrics) or 3% relative (error metrics) with a 10,000-resample bootstrap confirming superiority in at least 95% of resamples; for the tiny folds (rppb-1 with 24 and hppb-1 with 34 test compounds) the margin must be at least 0.030 absolute Pearson AND the bootstrap must confirm superiority in at least 97.5% of resamples, (d) fitting used only the official train indices of that benchmark, and (e) the attacker declares every pretrained component and every external dataset and demonstrates zero stereo-stripped-InChIKey overlap between them and the test fold - noting that the full Biogen ADME_public_set_3521.csv is public, so an external copy of the endpoint values for test compounds is the most obvious leak.

## Partial wins

- {"id": "p1", "statement": "The full strict win on one of the larger folds (polaris/adme-fang-perm-1 or -solu-1, 400-483 test rows; or biogen/adme-fang-perm-reg-v1 / -solu-reg-v1), where the bootstrap has enough rows to be meaningful."}
- {"id": "p2", "statement": "A structure-only result: beating the best listed entry that uses large-scale pretraining or phenomics side-information (the '1B_MPNN_*' / '3B_e50_MPNN_*' / '*-Phenomics' rows) on one endpoint with a model that uses only RDKit descriptors/fingerprints and classical learners, under the same margin and bootstrap rules, even if a community ensemble row remains ahead - reported as a scoped claim."}
- {"id": "p3", "statement": "A multi-endpoint consistency result: one multi-task model trained on the official train folds of the six Fang endpoints that beats the live best on at least two populated endpoint leaderboards simultaneously, with its single-task ablation reported."}

## Verification

Plain curl of https://polarishub.io/api/v1/benchmark/<owner>/<slug> (public) for targetCols, mainMetric and split indices; curl of the dataset's table.parquet URL from /api/v1/dataset/...; sha256 check; slice official test rows; recompute the mainMetric with scipy/sklearn from the attacker's prediction file; bootstrap; verify the attacker's train indices are a subset of the official train indices and that declared external data (including ADME_public_set_3521.csv) contain no test-fold InChIKey for that endpoint; re-fetch the live leaderboard page and parse all listed values. 3,521 compounds total, so a full retrain is minutes of CPU.

## Angles

- Endpoint-appropriate transforms and mechanistic features: MDR1-MDCK efflux ratio and protein binding are driven by ionisation, lipophilicity and molecular size; model log-transformed endpoints with pKa-derived charge class, logD7.4, TPSA, aromatic-ring count and H-bond descriptors, and fit separate submodels per charge class (acids/bases/neutrals) - a classic DMPK decomposition that monolithic models blur.
- Multi-task across the six Fang endpoints (train folds only): clearance, permeability, solubility and protein binding are strongly correlated through lipophilicity, so a multi-output booster or reduced-rank model borrows strength exactly where the per-endpoint folds are small.
- CROSS-DOMAIN (signal processing / Kalman-style shrinkage): treat each prediction as a noisy measurement with an estimated variance and fuse several models by inverse-variance weighting; optimal linear fusion beats equal-weight averaging on correlation metrics and is free.
- CROSS-DOMAIN (compression-based similarity): NCD-kernel SVR over canonical SMILES as an uncorrelated ensemble member - especially useful on the 24-34-compound rppb/hppb folds where any high-variance learner is dangerous.
- CROSS-DOMAIN (ecology / environmental niche models): treat physicochemical space as an environment and fit monotone GAM 'niche' responses with ecological-style smoothers plus interaction terms, which extrapolate more gracefully than trees on a different-chemotype test fold.
- CROSS-DOMAIN (coding theory / ordinal thresholds): for Pearson-scored endpoints, build the prediction from an ensemble of threshold classifiers (ordinal ECOC) and map decoded ranks back to values by the train-fold quantile function, giving noise-robust, monotone predictions.
- Rank-then-calibrate: since pearsonr is scored, fit the ranking first (pairwise loss) and then a monotone calibration from ranks to values on the train fold; separating ordering from scale is a reliable few-point Pearson gain.

## Pitfalls

- Public-CSV label leakage: the entire Biogen dataset (ADME_public_set_3521.csv) is on GitHub, so joining it to the Polaris test rows recovers the labels exactly. Any use of the public CSV for anything other than the official train indices must be treated as leakage, and claims must prove the test endpoint values were never read.
- Tiny folds: rppb-1 has 24 and hppb-1 has 34 test compounds; Pearson on 24 points has a 95% CI roughly +-0.15, so 'records' there are nearly meaningless. The stricter margin and bootstrap thresholds for these folds exist to prevent exactly that false positive, and a win there should be reported as fragile.
- Empty-leaderboard false win: biogen/adme-fang-rclint-reg-v1 and -hclint-reg-v1 currently list no results; a first entry is not a record.
- v1-vs-reg-v1 confusion: polaris/adme-fang-*-1 (Dec 2023) and biogen/adme-fang-*-reg-v1 (Jul 2024) use different splits and sometimes different label columns despite near-identical names; comparing across them is invalid. Always cite the full owner/slug and the API-reported split and targetCols.
- Metric column confusion: these leaderboards display MAE, MSE, r2, spearmanr, pearsonr and explained_var simultaneously, and the rows are NOT sorted by the mainMetric (on adme-fang-hppb-1 the row with the best MAE is listed second). Only the API's mainMetric is the record; improvements on other columns are scoped partials.
- Pretraining contamination: the phenomics/MolGPS entries and any public ADMET-pretrained encoder may include Fang compounds; an attacker reusing such an encoder must declare it, and the skeptic should treat an undeclared pretrained featuriser as disqualifying.

## Sources

- https://polarishub.io/benchmarks/polaris/adme-fang-perm-1
- https://polarishub.io/benchmarks/polaris/adme-fang-solu-1
- https://polarishub.io/benchmarks/polaris/adme-fang-rppb-1
- https://polarishub.io/benchmarks/polaris/adme-fang-hppb-1
- https://polarishub.io/benchmarks/biogen/adme-fang-perm-reg-v1
- https://polarishub.io/benchmarks/biogen/adme-fang-solu-reg-v1
- https://github.com/molecularinformatics/Computational-ADME
- https://polarishub.io/api/v1/dataset/polaris/adme-fang-1
- Status source: https://polarishub.io/benchmarks/polaris/adme-fang-perm-1

## Citations

- [Problem page](../../../../.raw/V3R1T4S/known-unknowns/drug-discovery/polaris-adme-fang-biogen-endpoints.md)
- [Bank entry](../../../../.raw/V3R1T4S/bank/targets.json) (id `polaris-adme-fang-biogen-endpoints`, commit `7dd4480`)

## Related Nodes

- [[V3R1T4S Drug discovery]]
- [[V3R1T4S]]
