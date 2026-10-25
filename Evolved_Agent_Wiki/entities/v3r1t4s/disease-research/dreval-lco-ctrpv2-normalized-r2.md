---
id: v3r1t4s-dreval-lco-ctrpv2-normalized-r2
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
# DrEval leave-cell-line-out: beat the public best normalized R^2 / Pearson for cancer drug-response prediction on CTRPv2

# Overview

> Bank id `dreval-lco-ctrpv2-normalized-r2` · harvest · tractability 3 · laptop-hours · disclosure **open**
> Bank says open as of 2026-10-15. Statuses go stale — re-check the primary source before any work.

## Statement

DrEval (drevalpy, Bernett et al., Nature Communications 2026, article 4238) is a standardised benchmark for drug-response prediction in cancer cell lines. Its headline finding is that complex deep models barely beat a naive predictor of mean drug and cell-line effects, and that NO published model surpasses a tuned Random Forest in the leave-cell-line-out (LCO) setting. The full public benchmark report is served as static HTML at https://dilis-lab.github.io/drevalpy-report/ (run id all_runs; the documented main run is CTRPv2 lnIC50 with 10-fold CV and cross-study evaluation on CTRPv1/CCLE/GDSC1/GDSC2, test modes LPO/LCO/LTO/LDO). The per-model metric table is machine-readable: heatmaps/heatmap_algorithms_LCO_normalized.html embeds a Plotly figure whose z values are base64 float64 arrays. As of 2026-10-13 the LCO ranking by normalized R^2 is RandomForest 0.1852, MultiOmicsRandomForest 0.1633, ProteomicsRandomForest 0.1612, DIPK 0.1084, SimpleNeuralNetwork 0.0706, GradientBoosting 0.0545, MultiOmicsNeuralNetwork 0.0003, naive baselines ~ -0.002 and below; by normalized Pearson, RandomForest 0.4347 leads. 'Normalized' means after subtracting the NaiveMeanEffectsPredictor, i.e. the metric measures only the differential-sensitivity signal, which is where every method is still weak (the paper notes all models stay below 0.20 normalized R^2 in LCO). Beating a tuned Random Forest on this normalized metric with CPU-only methods is a genuine, narrow, currently-open frontier, and drevalpy runs end-to-end on a laptop (the pipeline, splits, baselines and metrics all ship in the package, v1.6.0 archived on Zenodo, repo pushed 2026-10-13).

## Success criterion

Success means a new model, implemented as a drevalpy model class, run through drevalpy's own pipeline on the same dataset and test mode as the public report (CTRPv2, test_mode=LCO, the same number of CV splits as the report's run, lnIC50 response, the package's own split generation with the report's seed/configuration), whose mean normalized R^2 across the CV splits, computed by drevalpy's own evaluation code, is STRICTLY HIGHER (direction: max) than the maximum normalized R^2 over ALL models in https://dilis-lab.github.io/drevalpy-report/heatmaps/heatmap_algorithms_LCO_normalized.html, re-fetched and re-decoded live immediately before claiming, by at least 0.02 absolute AND by at least 2x the across-split standard error of the attacker's own result, while not being worse than the live best normalized Pearson by more than 0.01. The claim must ship: pinned drevalpy version and commit, the model class source, the exact CLI/API invocation, the per-split predictions and ground-truth CSVs that drevalpy writes, the drevalpy-generated report directory, and a re-run of the published RandomForest baseline in the SAME environment and splits (so the comparison is same-splits, not report-vs-local). If the attacker's own RandomForest re-run differs from the published 0.1852 by more than 0.02, the comparison must be made against the attacker's own re-run AND against the published value, and both must be beaten. Hyperparameters may be selected only with the inner validation partitions drevalpy provides; no test fold may be touched before the final evaluation. In addition, before claiming, the agent must re-fetch the maintained DrEval Challenge Leaderboard (https://drevalpy.readthedocs.io/en/latest/leaderboard.html and the rendered leaderboard image in the drevalpy repository, which as of 2026-10-15 lists 25 models on CTRPv2 LCO with best normalized Pearson 0.376 (EnsembleMF) and best RMSE 1.274 (DrugGNN)) and must show that its normalized Pearson is not lower than the live leaderboard maximum. A result that beats only the frozen 2025 report heatmap, while trailing a model already on the live leaderboard, is NOT a win and must be reported as a reproduction-scale result.

## Partial wins

- {"id": "p1", "statement": "Same criterion in the LTO (leave-tissue-out) setting against https://dilis-lab.github.io/drevalpy-report/heatmaps/heatmap_algorithms_LTO_normalized.html (live best normalized R^2 as of 2026-10-13: 0.0728, RandomForest), by >= 0.02 absolute, with the same same-splits re-run requirement."}
- {"id": "p2", "statement": "Strictly beat the live best normalized Pearson (0.4347 as of 2026-10-13) and normalized Spearman (0.4283) in LCO by >= 0.01 each while not losing more than 0.01 of normalized R^2 relative to the live best. Rank-correlation gains without R^2 gains are a separate, independently checkable result."}
- {"id": "p3", "statement": "A negative result of record: a same-environment, same-splits re-run of the published RandomForest, MultiOmicsRandomForest and DIPK in LCO showing a reproducibility gap of > 0.02 normalized R^2 against the published report values, with full logs. This is a reproducibility finding about the public benchmark, not a win, and must be reported as such."}

## Verification

Skeptic installs the pinned drevalpy in a clean venv, runs the attacker's model class plus the RandomForest baseline on CTRPv2 LCO with the attacker's exact invocation (drevalpy writes per-split predictions, ground truth and metrics as CSVs; laptop-hours to about a day on 10 cores), then recomputes normalized R^2 directly from the CSVs with their own script (normalization against the NaiveMeanEffectsPredictor predictions, which the pipeline always produces), and confirms the drevalpy-reported value matches. Record side: curl the table_url, extract the Plotly JSON, base64-decode the z array, and read the live maximum. Leakage audit: confirm the test folds' cell lines never appear in training for that split, that no omics preprocessing (feature selection, scaling, PCA, gene filtering) was fitted on all cell lines jointly, and that no hyperparameter was chosen using test-fold predictions.

## Angles

- Conventional: the normalized metric isolates differential sensitivity, so model the RESIDUAL after the mean-effects fit directly (per-drug residual regression on cell-line omics), instead of predicting lnIC50 and hoping the normalisation is kind. Per-drug residual models with heavy regularisation are the natural shape for LCO.
- Conventional: better feature selection for unseen cell lines - pathway-level aggregation, variance-stabilised expression, and per-drug target-pathway priors; the published Random Forest uses generic landmark-gene features and is unlikely to be feature-optimal.
- Cross-domain import (statistical physics / random matrix theory): denoise the cell-line expression matrix by Marchenko-Pastur eigenvalue shrinkage before regression, keeping only components outside the bulk spectrum. LCO fails mainly because of covariate shift in noisy high-dimensional omics, which is exactly what spectral shrinkage addresses, and it costs seconds on a laptop.
- Cross-domain import (coding theory / error-correcting output codes): decompose the per-drug prediction task into an ensemble of binary 'sensitive vs resistant' codewords over drug clusters and decode the cell line's response profile with a minimum-distance decoder; this turns a hard regression into many easy classifications and recovers rank signal (Pearson/Spearman normalized) that the regression loss throws away.
- Cross-domain import (ecology / community similarity): treat cell lines as 'sites' and drugs as 'species' and import beta-diversity / ordination machinery (Procrustes alignment of drug-response ordinations between training and held-out cell lines) to transfer response geometry rather than point predictions.
- Variance reduction and honest tuning: because the bar is 0.02 normalized R^2, ensembling across splits, bagged feature subsets and careful inner-validation-only tuning may matter as much as the model class; measure the across-split standard error first and refuse to chase gains below it.

## Pitfalls

- Same-splits comparison is mandatory. drevalpy regenerates CV splits; comparing a local run against the published report numbers without re-running the Random Forest baseline in the same environment and splits is the single most likely false positive here, because split variance in LCO is large relative to the 0.02 bar.
- Normalisation confusion: 'normalized R^2' is relative to the NaiveMeanEffectsPredictor, and unnormalized R^2 can look spectacular (LPO overall Pearson ~0.91 for DIPK) while carrying zero differential-sensitivity signal. Quoting an unnormalized number as a record is the classic crank move in this field.
- Cell-line identity leakage through omics preprocessing: fitting scalers, PCA, gene filters, batch correction or drug/cell-line embeddings on the full dataset before splitting lets held-out cell lines inform training. LCO specifically forbids this, and it is invisible in the output metrics.
- Response-measure substitution: the public run predicts lnIC50. Switching to AUC or pEC50, or to GDSC instead of CTRPv2, changes the achievable numbers entirely and is not a comparable record.
- Cross-study confusion: the report also contains cross-study tables (CTRPv2 -> GDSC2 etc.) with different and lower values; comparing an in-study result against a cross-study table (or vice versa) invalidates the claim.
- Duplicate drug-cell-line pairs and replicate rows in CTRPv2 straddling folds; drevalpy handles this for its own splits, but any custom data joining by the attacker can reintroduce it.
- Two different public scoreboards exist for CTRPv2 LCO: the 2025 report heatmaps (frozen, last modified 2025-10-17, 11-15 models, the package's own 10-fold run) and the maintained DrEval Challenge Leaderboard (precomputed splits from Zenodo splits.zip, LN_IC50_curvecurator, 25 models as of 2026-10-15). They are not comparable to each other, and beating the older one is not a record.

## Sources

- https://dilis-lab.github.io/drevalpy-report/heatmaps/heatmap_algorithms_LCO_normalized.html
- https://drevalpy.readthedocs.io/en/latest/leaderboard.html
- https://raw.githubusercontent.com/daisybio/drevalpy/main/docs/_static/img/leaderboard_light.png
- https://github.com/daisybio/drevalpy
- https://www.ebi.ac.uk/europepmc/webservices/rest/PMC13168506/fullTextXML
- https://zenodo.org/records/23159774
- Status source: https://dilis-lab.github.io/drevalpy-report/heatmaps/heatmap_algorithms_LCO_normalized.html

## Citations

- [Problem page](../../../../.raw/V3R1T4S/known-unknowns/disease-research/dreval-lco-ctrpv2-normalized-r2.md)
- [Bank entry](../../../../.raw/V3R1T4S/bank/targets.json) (id `dreval-lco-ctrpv2-normalized-r2`, commit `7dd4480`)

## Related Nodes

- [[V3R1T4S Disease research]]
- [[V3R1T4S]]
