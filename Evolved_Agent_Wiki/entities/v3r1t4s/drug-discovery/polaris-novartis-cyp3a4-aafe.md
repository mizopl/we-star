---
id: v3r1t4s-polaris-novartis-cyp3a4-aafe
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
# Polaris novartis/adme-novartis-cyp3a4-reg: beat the listed absolute-average-fold-error on 368 test compounds

# Overview

> Bank id `polaris-novartis-cyp3a4-aafe` · harvest · tractability 3.5 · laptop-hours · disclosure **open**
> Bank says open as of 2026-10-15. Statuses go stale — re-check the primary source before any work.

## Statement

Polaris hosts a Novartis CYP3A4 in vitro metabolism benchmark (novartis/adme-novartis-cyp3a4-reg, created 2024-07-15, 368 test compounds) whose main metric is the pharmacokinetics-specific absolute average fold error (AAFE, lower is better). As of 2026-10-13 the leaderboard has only a handful of entries and they are strikingly weak in absolute terms: rank 1 'adme-novartis-cyp3a4-reg-GIRAFFE' AAFE 1.013 with MAE 0.190, MSE 0.062, R2 0.123, Spearman 0.344, Pearson 0.471; 'MolEncoder' AAFE 1.052 with a HIGHER Spearman (0.410) and Pearson (0.545) and R2 0.066; 'AceProp1' AAFE 1.053, Spearman 0.393. The companion classification benchmark novartis/adme-novartis-cyp3a4-cls lists NO results. R2 near 0.1 with Pearson near 0.5 means the listed models are badly mis-scaled rather than uninformative, i.e. the AAFE record is a calibration problem, not a representation-learning problem - exactly the kind of hill a laptop can take. The benchmark's split indices and the dataset parquet download anonymously from the Polaris public API, so scoring is offline and mechanical.

## Success criterion

Success means a saved prediction file (one prediction per official test row in official order; manifest with the slug, sha256 of the downloaded table.parquet and the exact test index array from https://polarishub.io/api/v1/benchmark/novartis/adme-novartis-cyp3a4-reg) such that (a) the test rows and the label column match the API's split and targetCols exactly, (b) the skeptic's own AAFE - computed with the same definition Polaris uses (10 ** mean(|log10(pred) - log10(true)|) on the endpoint's own scale, read from the Polaris metric implementation at verification time) - is strictly LOWER (direction: min) than EVERY absolute_average_fold_error listed in the live leaderboard table, re-fetched immediately before claiming, (c) the improvement is at least 1.5% relative AND a 10,000-resample bootstrap over the 368 test rows puts the attacker's AAFE below the listed best in at least 95% of resamples, (d) the attacker ALSO reports MAE, MSE, R2, Spearman and Pearson from the same prediction file and does not lose more than 0.02 Spearman against the best Spearman listed on that table (so the win is not a pure fold-error trick that destroys ranking), and (e) fitting used only the official train indices, with every pretrained component and external dataset declared and shown to contain no test-fold molecule by stereo-stripped InChIKey. The empty companion leaderboard novartis/adme-novartis-cyp3a4-cls is explicitly excluded: a first entry there is not a record.

## Partial wins

- {"id": "p1", "statement": "The full strict win on AAFE under the live-refetch, margin, bootstrap and no-ranking-loss rules."}
- {"id": "p2", "statement": "A calibration-only result: take a reproduced baseline's predictions (the attacker's own re-implementation of a descriptor/boosting model, reported with code), apply a monotone recalibration fit ONLY on out-of-fold train predictions, and show that AAFE drops below the live listed best while Spearman is unchanged to within 0.005 - isolating calibration as the mechanism."}
- {"id": "p3", "statement": "A ranking result: beat the best Spearman listed on the same live table (currently 0.410, MolEncoder) by at least 0.030 with the bootstrap rule satisfied, reported as a scoped metric-specific claim rather than as the benchmark record."}

## Verification

Plain curl of the public benchmark API (targetCols, mainMetric, split indices) and of the related dataset's table.parquet via /api/v1/dataset/novartis/...; sha256 check; slice the official test rows; recompute AAFE with the Polaris metric definition plus the five secondary metrics; bootstrap over test rows; confirm the attacker's training indices are a subset of the official train indices and that declared external sources contain no test InChIKey; re-fetch the live leaderboard HTML and parse every listed AAFE and Spearman. 368 test rows and a few thousand training rows make a full retrain minutes of CPU.

## Angles

- Attack the metric directly: AAFE is a geometric-mean absolute error in log space, so train on log10 of the endpoint with an L1 loss, and fit the optimal additive log-space offset (the median log residual) on out-of-fold train predictions; a pure median-offset correction typically removes several percent of AAFE from any mis-scaled model, which is what the 1.013-vs-R2-0.123 pattern implies is available.
- Variance-aware shrinkage in log space: predict a log-space mean and variance, then shrink toward the train-set log median proportionally to predicted variance; because AAFE penalises absolute log deviation, shrinking uncertain predictions is near-free improvement.
- Metabolism-specific features: CYP3A4 turnover depends on lipophilicity and on the presence of accessible soft spots, so add SMARTS counts for N-dealkylation/O-dealkylation/benzylic-oxidation motifs, logD7.4, aromatic-carbon fraction and fraction-sp3, on top of ECFP; cheap and mechanistically aligned.
- CROSS-DOMAIN (signal processing / homomorphic filtering): work entirely in the log domain, where multiplicative assay error becomes additive, apply robust (Huber/Theil-Sen) fitting and median filtering across ensemble members, and convert back only at the end - the textbook treatment for fold-error metrics.
- CROSS-DOMAIN (coding theory / ordinal ECOC): discretise log-clearance into ordered bins with a Hadamard codebook of binary tasks and decode by minimum distance, which stabilises predictions against the heavy assay noise of microsomal turnover data.
- CROSS-DOMAIN (compression / NCD similarity) and CROSS-DOMAIN (linguistics / fragment n-grams) as uncorrelated ensemble members: parameter-free SMILES-compression kernels and BRICS-fragment n-gram models, combined by inverse-variance fusion.
- CROSS-DOMAIN (ecology / abundance-weighted sampling): reweight training compounds by inverse scaffold abundance so that the model is not dominated by a few large analogue series, improving generalisation to the test fold's chemotypes.

## Pitfalls

- Metric definition drift: AAFE has several variants (geometric mean fold error, 10**mean|log10 ratio|, mean of max(p/t, t/p)). Computing a different variant than Polaris does can swing the number by a lot; the exact Polaris metric implementation must be read and used at verification time, and the attacker must report the formula used.
- Zero/negative predictions: AAFE is undefined for non-positive predictions, so clipping choices change the score. The clipping rule must be declared and applied identically to all compared prediction sets.
- Metric trade-off masquerading as a record: a log-space offset can lower AAFE while the model's ranking is unchanged or worse. The success criterion's no-Spearman-loss clause exists to prevent claiming a pure scaling trick, and any gain must be reported with all five secondary metrics.
- Single fold, 368 rows, heavy-tailed clearance labels: a few extreme compounds dominate, so without the bootstrap a 1-2% AAFE 'improvement' is noise. The number of models the attacker evaluated on the test fold must be disclosed.
- Leakage via public CYP3A4 data: Novartis released this set publicly and CYP3A4 turnover data for many of these compounds exist in ChEMBL and vendor collections; an undeclared pretrained ADMET model or an external CYP3A4 table can contain the test labels. Declare provenance and check InChIKeys against the test fold.
- Empty-companion confusion: novartis/adme-novartis-cyp3a4-cls has no entries; results there are not records, and classification scores must never be compared against this regression table.

## Sources

- https://polarishub.io/benchmarks/novartis/adme-novartis-cyp3a4-reg
- https://polarishub.io/benchmarks/novartis/adme-novartis-cyp3a4-cls
- https://polarishub.io/api/v1/benchmark?limit=100
- Status source: https://polarishub.io/benchmarks/novartis/adme-novartis-cyp3a4-reg

## Citations

- [Problem page](../../../../.raw/V3R1T4S/known-unknowns/drug-discovery/polaris-novartis-cyp3a4-aafe.md)
- [Bank entry](../../../../.raw/V3R1T4S/bank/targets.json) (id `polaris-novartis-cyp3a4-aafe`, commit `7dd4480`)

## Related Nodes

- [[V3R1T4S Drug discovery]]
- [[V3R1T4S]]
