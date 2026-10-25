---
id: v3r1t4s-dreval-cross-study-ctrpv2-to-gdsc2
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
# DrEval cross-study generalisation: beat the public best CTRPv2-to-GDSC2 (and CCLE/GDSC1/CTRPv1) transfer numbers

# Overview

> Bank id `dreval-cross-study-ctrpv2-to-gdsc2` · harvest · tractability 3 · laptop-hours · disclosure **open**
> Bank says open as of 2026-10-15. Statuses go stale — re-check the primary source before any work.

## Statement

The hardest honest test in cancer drug-response prediction is transfer between independent screens. The public DrEval report includes cross-study tables: models trained on CTRPv2 under the LCO protocol are evaluated on four external datasets (GDSC1, GDSC2, CCLE, CTRPv1), and the tables are fully machine-readable Plotly tables (header: Model, MSE, RMSE, MAE, R^2, Pearson, Spearman, Kendall, and the normalized variants). As of 2026-10-13 the CTRPv2 -> GDSC2 LCO table reads (best first by MSE): GradientBoosting MSE 5.092 +/- 0.374 (normalized Pearson 0.209), RandomForest 5.095 +/- 0.139 (0.123), MultiOmicsRandomForest 5.172 (0.125), NaiveDrugMeanPredictor / NaiveMeanEffectsPredictor 5.447 +/- 0.029 (0.000), DIPK 6.407 (normalized Pearson 0.301 - the best normalized Pearson despite a worse MSE), SuperFELTR 7.919, SimpleNeuralNetwork 8.638, ElasticNet 11.775, SRMF 10880. Every model's normalized R^2 is NEGATIVE (best -0.115), i.e. no model in the public cross-study tables as of the claim date beats the naive mean-effects model on external data in squared-error terms (the newer models on the maintained DrEval Challenge Leaderboard, https://drevalpy.readthedocs.io/en/latest/leaderboard.html, have no published cross-study results in the 2025 report). That is a crisp, public, currently-open frontier with a numeric table, and it is laptop-scale: training happens on CTRPv2 and scoring on an external study is a forward pass.

## Success criterion

Success means a drevalpy model class trained ONLY on CTRPv2 under the report's LCO protocol (package-generated splits, lnIC50, same number of CV splits) and evaluated by drevalpy's own cross-study machinery on one of the four external datasets, achieving EITHER (a) a mean MSE strictly LOWER than the minimum MSE over all models in that dataset's live cross-study table, re-fetched and re-parsed live immediately before claiming, by at least 0.10 absolute AND at least 2x the attacker's across-split std, with normalized Pearson not below the live best by more than 0.02; OR (b) a mean normalized R^2 strictly HIGHER than the live maximum in that table by at least 0.03 absolute and at least 2x the attacker's std. In both cases the attacker must include a same-environment, same-splits re-run of GradientBoosting, RandomForest and the NaiveMeanEffectsPredictor and must beat the re-run values as well as the published ones. The external dataset must be used only for evaluation: no external labels, no external response statistics, no external-fitted preprocessing, and no selection of the attacker's model or hyperparameters using any external-dataset metric (choose on CTRPv2 inner validation only, and declare the chosen configuration before the external evaluation is run - the agent must log a pre-registration file with sha256 before scoring). Before claiming, the agent must also re-fetch the maintained DrEval Challenge Leaderboard (https://drevalpy.readthedocs.io/en/latest/leaderboard.html) and the drevalpy repository, and check whether any newer model there has published cross-study results for the same external dataset; if so, those values are part of the bar. A result that beats only the frozen 2025 report tables while trailing a newer published cross-study value is NOT a win.

## Partial wins

- {"id": "p1", "statement": "Any model that achieves a POSITIVE mean normalized R^2 on any one of the four external datasets under the above protocol (i.e. beats the NaiveMeanEffectsPredictor in squared error on an independent screen, which no model in the public tables does; best is -0.115 on GDSC2 as of 2026-10-13), by at least 0.02 and 2x std, with the pre-registration and same-splits re-runs."}
- {"id": "p2", "statement": "Strictly beat the live best normalized Pearson on two of the four external transfers (e.g. GDSC2 best 0.301 as of 2026-10-13) by >= 0.02 each under the same protocol."}
- {"id": "p3", "statement": "A measured decomposition of the transfer gap: quantify, with the same splits, how much of the cross-study error is attributable to (i) drug-concentration-range differences, (ii) cell-line overlap, (iii) response-measure calibration, by re-scoring the SAME predictions after each correction, and show which single correction closes the most gap. Mechanically checkable from the written prediction CSVs, not implied by the published tables."}

## Verification

Skeptic installs pinned drevalpy, runs the attacker's model and the baselines with the attacker's exact invocation including --cross_study_datasets (laptop-hours to about a day), then recomputes MSE and the normalized metrics directly from drevalpy's written per-split prediction/ground-truth CSVs with their own script, including the normalisation against the NaiveMeanEffectsPredictor. Record side: curl the cross-study table HTML, extract the Plotly table JSON and read the header/cells arrays (plain strings, no decoding needed). Pre-registration check: verify the sha256-stamped configuration file predates the external evaluation logs. Leakage audit: grep for any read of the external dataset during training or model selection, confirm cell lines and drugs shared between CTRPv2 and the external set are handled exactly as drevalpy's cross-study code does, and confirm no response-scale calibration was fitted on external labels.

## Angles

- Conventional: calibration-free targets. Train on within-study ranks or on per-drug standardised responses so the model never has to transfer an absolute lnIC50 scale, then map back with only training-study statistics; most of the cross-study MSE is scale and concentration-range mismatch.
- Conventional: robust feature spaces - pathway-level or rank-transformed expression features that are invariant to platform differences between CCLE-derived and Sanger-derived omics.
- Cross-domain import (signal processing / channel equalisation): treat the external screen as the same signal passed through a different measurement channel and fit a blind equaliser (quantile-matching / histogram equalisation estimated from UNLABELLED external features only) to the prediction distribution; blind, label-free equalisation is legitimate transductive calibration and is exactly the tool for a scale-mismatch channel.
- Cross-domain import (statistical physics of generalisation / domain-shift geometry): measure the covariate shift between studies with a spectral distance between omics covariance matrices, then reweight training samples by an importance ratio estimated in the leading eigen-directions (kernel mean matching); this is the principled version of 'train on the cell lines that look like the target screen'.
- Cross-domain import (ecology / rank-abundance statistics): compare per-drug response distributions across screens as rank-abundance curves and transfer only the ordinal structure, scoring with Spearman-oriented losses; ecology has well-developed tools for comparing community compositions measured with different effort.
- Ensembles across model families with disagreement-based abstention, measuring whether the best achievable cross-study metric comes from a single family or from averaging; cheap and directly testable with saved predictions.

## Pitfalls

- Any use of external labels - even for choosing which checkpoint, feature set or calibration to use - converts this into a fitted-on-test number. Pre-registration with a sha256-stamped config is mandatory precisely because this leak is so tempting and so invisible.
- Cell-line and drug overlap between CTRPv2 and the external screens: the same cell line measured in both studies is not an independent test point in the usual sense, and silently dropping or keeping overlaps changes the number. The claim must state the overlap handling and match drevalpy's own convention.
- Response-measure mismatch: GDSC lnIC50 and CTRP lnIC50 are computed from different concentration ranges and curve-fitting conventions; a naive comparison of raw MSE across studies is meaningless and an apparent win can be pure rescaling. Report both raw and per-drug-standardised metrics.
- Normalized vs unnormalized metric confusion. Every public cross-study normalized R^2 is negative; quoting a positive raw R^2 (e.g. 0.223 for GradientBoosting on GDSC2) as beating the naive baseline is wrong - the naive baseline has raw R^2 0.167 and identical MSE structure.
- Same-splits and same-environment re-runs are required; the attacker's pipeline version may differ from the report's, and cross-study stds are large (GradientBoosting MSE +/- 0.374).
- Over-interpretation: better cross-study transfer on public cell-line screens is a benchmark result, not evidence about clinical response.
- The 2025 report pages are a frozen snapshot (last modified 2025-10-17) while the maintained DrEval Challenge Leaderboard now lists 25 models, several of which are absent from the report's cross-study tables; 'no model beats the naive baseline out of study' holds only for the public cross-study tables as of the claim date. The paper itself must be read via Europe PMC, since nature.com redirects (303) a plain GET to a login host.

## Sources

- https://dilis-lab.github.io/drevalpy-report/html_tables/table_cross_study_GDSC2_LCO.html
- https://github.com/daisybio/drevalpy
- https://dilis-lab.github.io/drevalpy-report/
- https://drevalpy.readthedocs.io/en/latest/
- https://www.ebi.ac.uk/europepmc/webservices/rest/PMC13168506/fullTextXML
- https://drevalpy.readthedocs.io/en/latest/leaderboard.html
- Status source: https://dilis-lab.github.io/drevalpy-report/html_tables/table_cross_study_GDSC2_LCO.html

## Citations

- [Problem page](../../../../.raw/V3R1T4S/known-unknowns/disease-research/dreval-cross-study-ctrpv2-to-gdsc2.md)
- [Bank entry](../../../../.raw/V3R1T4S/bank/targets.json) (id `dreval-cross-study-ctrpv2-to-gdsc2`, commit `7dd4480`)

## Related Nodes

- [[V3R1T4S Disease research]]
- [[V3R1T4S]]
