---
id: v3r1t4s-polaris-tdcommons-mirror-admet-leaderboards
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
tractability: 3.5
compute: "laptop-hours"
disclosure: open
status_checked: "2026-10-15"
---
# Polaris tdcommons/* ADMET mirrors: beat the top listed score on a single-fold public split (offline-scorable)

# Overview

> Bank id `polaris-tdcommons-mirror-admet-leaderboards` · harvest · tractability 3.5 · laptop-hours · disclosure **open**
> Bank says open as of 2026-10-15. Statuses go stale — re-check the primary source before any work.

## Statement

Polaris mirrors 16 TDC ADMET datasets as its own single-task benchmarks (tdcommons/caco2-wang, herg, dili, half-life-obach, vdss-lombardo, clearance-hepatocyte-az, clearance-microsome-az, ld50-zhu, cyp2c9-substrate-carbonmangels, cyp2d6-substrate-carbonmangels, cyp3a4-substrate-carbonmangels, bbb-martins, ames, ppbr-az, lipophilicity-astrazeneca, bioavailability-ma, pgp-broccatelli, solubility-aqsoldb, hia-hou). Unlike TDC these are ONE fixed fold with explicit train/test index lists served by the public API (e.g. caco2-wang 728/182, herg 132 test, dili 96 test, half-life-obach 135 test, cyp2c9-substrate 135 test), and both the table.parquet and the split indices download anonymously over plain HTTPS (verified: https://data.polarishub.io/dataset/polaris/adme-fang-1/table.parquet returned 200 and /api/v1/benchmark/<slug> returns the explicit test index array), so a laptop can score locally with no account and no submission. Leaderboards are active but shallow and dominated by big pretrained models: tdcommons/herg best ROC-AUC 0.915, tdcommons/dili 0.950, tdcommons/caco2-wang MAE 0.270, tdcommons/half-life-obach Spearman 0.625, tdcommons/vdss-lombardo Spearman 0.726, tdcommons/clearance-hepatocyte-az Spearman 0.538, tdcommons/ld50-zhu MAE 0.526, tdcommons/cyp2c9-substrate-carbonmangels PR-AUC 0.478. Single-fold scoring on 96-1,478 test molecules means a careful classical model has a real shot, and the frontier is per-benchmark.

## Success criterion

Pick one named Polaris tdcommons benchmark. Success means a saved prediction file (one prediction per official test row in the official order, probabilities in [0,1] for classification, manifest with the benchmark slug, the sha256 of the downloaded table.parquet, and the exact test index array) such that (a) the test rows are exactly the indices in the 'split' field of https://polarishub.io/api/v1/benchmark/tdcommons/<slug> and the label column is that benchmark's targetCols entry, (b) the skeptic's own computation of the benchmark's mainMetric (sklearn: mean_absolute_error, roc_auc_score, average_precision for pr_auc, scipy.stats.spearmanr) is strictly better in the metric's own direction than EVERY value listed in the live leaderboard table at https://polarishub.io/benchmarks/tdcommons/<slug>, re-fetched immediately before claiming, (c) the margin is at least 3% relative for error metrics, or at least 0.010 absolute for ROC-AUC / PR-AUC / Spearman, AND a 10,000-resample bootstrap over test rows puts the attacker's value ahead of the listed best in at least 95% of resamples, (d) the model was fit only on the official train indices (internal validation carved from them), and (e) the attacker declares every pretrained component with its training-data provenance and shows that no test molecule (stereo-stripped InChIKey) appears in any declared training source - which, since these are standard public ADMET sets, must be checked rather than assumed. Reporting a different metric from the benchmark's mainMetric, or a different split, does not count.

## Partial wins

- {"id": "p1", "statement": "The full strict win on one of the tiny-test benchmarks (tdcommons/dili 96, tdcommons/herg 132, tdcommons/cyp2c9-substrate-carbonmangels 135, tdcommons/half-life-obach 135) with the bootstrap rule satisfied."}
- {"id": "p2", "statement": "A no-pretraining result: a model using only RDKit-computable features and classical learners (no pretrained neural encoder, no external labelled data) whose score beats every listed entry that is a large pretrained model (the '1B_MPNN_*', '3B_e50_MPNN_*', 'MolEncoder', 'CheMeleon', 'TabPFNv2-*' rows) on one benchmark, under the same margin and bootstrap rules, even if some other row remains ahead - reported explicitly as a scoped claim."}
- {"id": "p3", "statement": "A cross-benchmark sweep: one fixed recipe (no per-benchmark tuning on test) that beats the live leaderboard best on at least three tdcommons/* Polaris benchmarks at once, each verified against its own live table."}

## Verification

Skeptic calls https://polarishub.io/api/v1/benchmark/tdcommons/<slug> with plain curl (public, no auth), reads targetCols, mainMetric and the split index arrays, downloads the related dataset's table.parquet from the data.polarishub.io URL given by /api/v1/dataset/tdcommons/<slug>, checks its sha256 against the manifest, slices the official test rows, loads the attacker's prediction vector, recomputes the mainMetric with sklearn/scipy, runs the bootstrap, checks train/test InChIKey disjointness and that the attacker's training indices are a subset of the official train indices, then re-fetches the live leaderboard HTML and parses every listed value. Everything fits in minutes on CPU.

## Angles

- Single-fold means variance reduction wins: average many models and many featurisations (ECFP/FCFP/Avalon/MACCS/RDKit-2D), each tuned by grouped CV on the train indices only, then combine by out-of-fold-weighted stacking. The listed leaders are single large pretrained models with no ensembling across feature families.
- Tabular-foundation-model-style priors on CPU: the leaderboards already contain TabPFNv2 rows, and their numbers are beatable on several benchmarks; running TabPFN-class models over multiple descriptor subsets and aggregating (bagging over feature subspaces) is CPU-feasible at these data sizes and is the most direct route.
- CROSS-DOMAIN (compression-based similarity): normalised compression distance over canonical SMILES as an SVR/k-NN kernel, used as an ensemble member that errs differently from fingerprint models - parameter-free, no training, seconds of CPU.
- CROSS-DOMAIN (signal processing / matched filters): build 'matched filter' templates per activity class from the train set in fingerprint space (class-mean fingerprint, whitened by the within-class covariance - i.e. a Fisher/LDA direction in bit space) and use the filter response as a feature; a classical detection-theory view of substructure alerts.
- CROSS-DOMAIN (ecology / rarefaction and abundance weighting): weight training molecules by the inverse 'abundance' of their scaffold in the train set (rarefaction-style) so rare scaffolds are not drowned out, since the test fold is a different scaffold community.
- CROSS-DOMAIN (coding theory / ordinal ECOC) for the Spearman and PR-AUC benchmarks: threshold-ensemble decoding to produce a robust ranking rather than a point estimate.
- Metric-specific post-processing: for MAE benchmarks, median-calibrate; for PR-AUC, rank-optimise the positive class with a pairwise loss; for Spearman, aggregate ensemble members in rank space (Borda) instead of value space.

## Pitfalls

- Pretraining contamination is the central trap: these are the standard public TDC/ADMET sets, so '1B_MPNN', 'MolEncoder', 'CheMeleon' and any ADMET-pretrained encoder may have trained on the very molecules in this single test fold, and so may an attacker's chosen pretrained featuriser. Provenance must be declared and InChIKey overlap with the test fold checked; an undeclared pretrained featuriser is grounds to reject the claim outright.
- Wrong split: the Polaris fold is NOT the TDC scaffold split (different sizes and indices) and is a single fold, not 5 seeds. Mixing the two protocols - e.g. quoting a TDC 5-seed mean against a Polaris table - is an invalid comparison in both directions.
- Single-fold luck: 96-1,478 test rows with one fold means no seed averaging is available; the bootstrap and the absolute/relative margin rules are the only defence, and the number of distinct models the attacker evaluated on the test fold must be reported (any selection on the test fold invalidates the claim).
- Metric mismatch: each benchmark has one mainMetric from the API (mean_absolute_error, roc_auc, pr_auc, spearmanr). The leaderboard page may show several columns; beating a non-main metric is not a record, and pr_auc must be computed as average precision exactly as Polaris does.
- Label-column confusion in the parquet: several of these datasets carry multiple columns (raw and transformed endpoint values); scoring against a column other than targetCols silently changes the scale.
- Novelty trap: the Polaris tables move (new rows appeared through 2025-2026, e.g. 'vidraft-*', 'agentomics-ml-*', 'nextflow-frontier-*' entries), so the table MUST be re-fetched minutes before any claim, and the NOVELTY skeptic must also check for papers reporting the same Polaris fold.

## Sources

- https://polarishub.io/benchmarks/tdcommons/herg
- https://polarishub.io/benchmarks/tdcommons/dili
- https://polarishub.io/benchmarks/tdcommons/caco2-wang
- https://polarishub.io/benchmarks/tdcommons/half-life-obach
- https://polarishub.io/benchmarks/tdcommons/vdss-lombardo
- https://polarishub.io/benchmarks/tdcommons/clearance-hepatocyte-az
- https://polarishub.io/benchmarks/tdcommons/ld50-zhu
- https://polarishub.io/benchmarks/tdcommons/cyp2c9-substrate-carbonmangels
- https://polarishub.io/api/v1/benchmark?limit=100
- Status source: https://polarishub.io/benchmarks/tdcommons/herg

## Citations

- [Problem page](../../../../.raw/V3R1T4S/known-unknowns/drug-discovery/polaris-tdcommons-mirror-admet-leaderboards.md)
- [Bank entry](../../../../.raw/V3R1T4S/bank/targets.json) (id `polaris-tdcommons-mirror-admet-leaderboards`, commit `7dd4480`)

## Related Nodes

- [[V3R1T4S Drug discovery]]
- [[V3R1T4S]]
