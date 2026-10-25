---
id: v3r1t4s-polaris-pkis2-kinase-small-leaderboards
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
# Polaris PKIS2/PKIS1 kinase benchmarks (EGFR, KIT, RET, LOK-SLK): beat shallow leaderboards on 74-144 test compounds

# Overview

> Bank id `polaris-pkis2-kinase-small-leaderboards` · harvest · tractability 3.5 · laptop-hours · disclosure **open**
> Bank says open as of 2026-10-15. Statuses go stale — re-check the primary source before any work.

## Statement

Polaris hosts 14 kinase-inhibition benchmarks built from the published PKIS1/PKIS2 chemogenomic sets: regression (percent-inhibition) and classification variants for EGFR wild-type, KIT wild-type, RET wild-type and the LOK/SLK pair, in both a v1 ('*-r-1' / '*-c-1') and a v2 ('*-reg-v2' / '*-cls-v2') formulation, with test sizes of 74-144 compounds. The leaderboards are extremely shallow: polaris/pkis2-kit-wt-reg-v2 has a SINGLE entry (CheMeleon, MAE 21.480, MSE 849.611, R2 0.296, Spearman 0.536), polaris/pkis2-kit-wt-cls-v2 has two (CheMeleon PR-AUC 0.646, MHNfs 0.376), polaris/pkis2-egfr-wt-reg-v2 has a handful (best MAE 16.009 by an 'aether-pharmaos' ensemble), polaris/pkis2-ret-wt-reg-v2 best MAE 18.252-18.309 from 1B/3B MolGPS models, polaris/pkis2-ret-wt-cls-v2 best PR-AUC 0.885, and polaris/pkis1-egfr-wt-mut-cls-v2 shows no leaderboard section at all. Data and explicit split indices download anonymously from the Polaris public API, so everything is scorable offline on a laptop. With 74-144 test compounds and percent-inhibition labels, careful classical QSAR plus variance reduction is directly competitive with the pretrained models that currently hold these rows.

## Success criterion

Pick one named Polaris PKIS benchmark whose live leaderboard has at least one entry. Success means a saved prediction file (one prediction per official test row in official order; probabilities for classification; manifest with slug, sha256 of the downloaded table.parquet and the exact test index array from the public API) such that (a) the test rows are exactly the indices in the 'split' field of https://polarishub.io/api/v1/benchmark/polaris/<slug> and the label column is that benchmark's targetCols entry, (b) the skeptic's own computation of the benchmark's mainMetric is strictly better in that metric's direction than EVERY value listed in the live leaderboard table, re-fetched immediately before claiming, (c) the margin is at least 5% relative for MSE/MAE or 0.020 absolute for PR-AUC/ROC-AUC/balanced-accuracy, AND a 10,000-resample bootstrap over the 74-144 test rows puts the attacker ahead in at least 95% of resamples, (d) fitting used only the official train indices, with any multi-task borrowing restricted to OTHER kinases' train indices (declared, and checked to contain no test row of the target benchmark), and (e) no external PKIS or ChEMBL kinase-profiling record for a test compound-kinase pair was used; the PKIS data are public, so this must be verified by InChIKey, not assumed. A first entry on an EMPTY leaderboard is NOT a record and does not count.

## Partial wins

- {"id": "p1", "statement": "The full strict win on polaris/pkis2-kit-wt-reg-v2, the single-entry regression leaderboard (live best MSE 849.611 / MAE 21.480), with the bootstrap rule satisfied."}
- {"id": "p2", "statement": "A multi-task result: one model trained jointly on the train indices of the EGFR, KIT and RET regression benchmarks that beats the live best on at least two of the three under the same margin rules, with the single-task version of the same model reported for ablation."}
- {"id": "p3", "statement": "A classification-ranking result: on polaris/pkis2-kit-wt-cls-v2 or pkis2-ret-wt-cls-v2, beat the live best PR-AUC by at least 0.020 with a model that also does not lose more than 0.010 ROC-AUC against the best listed ROC-AUC, i.e. a genuine ranking improvement rather than a metric trade."}

## Verification

Plain-curl the public API for the benchmark (targetCols, mainMetric, split indices) and for the related dataset (table.parquet URL on data.polarishub.io), hash-check the parquet, slice the official test rows, recompute the mainMetric with sklearn/scipy from the attacker's prediction file, run the bootstrap, verify the attacker's training indices are a subset of the official train indices and that declared auxiliary data contain no test InChIKey, then re-fetch the live leaderboard page and parse every listed value for that metric. Test sets of 74-144 rows and train sets of a few hundred make full re-training a matter of minutes on CPU.

## Angles

- Kinase-family multi-task learning: PKIS2 profiles the same compounds across hundreds of kinases, so the legitimate signal is cross-kinase correlation among the benchmarks' own train splits; a multi-task booster or reduced-rank regression over kinase columns (restricted to training rows) exploits this where single-task pretrained encoders cannot.
- Heavy-tailed percent-inhibition handling: labels are bounded percentages with a spike near 0; model logit/arcsine-transformed inhibition, or a two-stage hurdle model (active/inactive classifier times conditional magnitude regressor), then invert - directly attacks the MSE records (849 on KIT means the baseline is dominated by a few large errors).
- CROSS-DOMAIN (signal processing / matched filtering and whitening): whiten the fingerprint space by the training covariance and use Fisher-discriminant 'matched filters' per kinase as features; detection-theoretic whitening is well-suited to 100-compound problems where plain distances are noisy.
- CROSS-DOMAIN (coding theory / ECOC over kinase panels): represent each compound's activity across the panel of training kinases as a codeword, train a decoder for the target kinase bit, and use minimum-distance decoding; panel selectivity patterns are exactly an error-correcting code over targets.
- CROSS-DOMAIN (compression / NCD) and CROSS-DOMAIN (linguistics / fragment n-grams): parameter-free SMILES-compression kernels and BRICS-fragment n-gram naive Bayes as uncorrelated ensemble members for a 74-144-row test set, where diversity beats depth.
- CROSS-DOMAIN (statistical physics / replica averaging with a tuned noise temperature): bagging with deliberate label-noise injection and Boltzmann weighting by out-of-fold error, to manage the bias-variance trade-off on tiny data far better than a single tuned model.
- Conformal shrinkage toward the train mean for compounds whose nearest-neighbour distance exceeds a calibrated threshold - a guaranteed-in-expectation MSE/MAE win when the test fold contains novel chemotypes.

## Pitfalls

- Empty-leaderboard false win: several PKIS variants (and sibling Polaris benchmarks such as polaris/pkis1-egfr-wt-mut-cls-v2, which shows no leaderboard section) have no entries at all; submitting the first number there is NOT beating a record and must never be claimed as one.
- Public-source label leakage: PKIS1/PKIS2 percent-inhibition data are published and also present in ChEMBL, so any external kinase-profiling table or kinase-pretrained model can contain the test compounds' labels for the same kinase. Declared provenance plus InChIKey checks against the test fold are mandatory.
- Tiny single fold: with 74-144 test compounds, MAE/MSE standard errors are large (MSE on a heavy-tailed label is dominated by two or three compounds), so a 5%-relative margin plus a bootstrap is the minimum, and the count of models evaluated on the test fold must be disclosed.
- v1-vs-v2 confusion: the '*-r-1'/'*-c-1' (2023-12) and '*-reg-v2'/'*-cls-v2' (2024-07) benchmarks share a name but differ in split and sometimes label definition; quoting a v1 record against a v2 result (or vice versa) is an invalid comparison. Always cite the exact slug and its API-reported split.
- Metric trade: pkis2 classification tables list accuracy, f1, roc_auc, pr_auc, mcc and cohen_kappa; the benchmark's mainMetric is the only record, and an apparent win on one column with losses elsewhere must be reported as a scoped partial, not a record.
- Activity-cliff/duplicate structure overlap between train and test folds (PKIS contains close analogue series); report a 1-NN-on-ECFP baseline as a floor so that a 'win' is not just better memorisation.

## Sources

- https://polarishub.io/benchmarks/polaris/pkis2-kit-wt-reg-v2
- https://polarishub.io/benchmarks/polaris/pkis2-egfr-wt-reg-v2
- https://polarishub.io/benchmarks/polaris/pkis2-ret-wt-reg-v2
- https://polarishub.io/benchmarks/polaris/pkis2-kit-wt-cls-v2
- https://polarishub.io/benchmarks/polaris/pkis2-ret-wt-cls-v2
- https://polarishub.io/api/v1/benchmark?limit=100
- Status source: https://polarishub.io/benchmarks/polaris/pkis2-kit-wt-reg-v2

## Citations

- [Problem page](../../../../.raw/V3R1T4S/known-unknowns/drug-discovery/polaris-pkis2-kinase-small-leaderboards.md)
- [Bank entry](../../../../.raw/V3R1T4S/bank/targets.json) (id `polaris-pkis2-kinase-small-leaderboards`, commit `7dd4480`)

## Related Nodes

- [[V3R1T4S Drug discovery]]
- [[V3R1T4S]]
