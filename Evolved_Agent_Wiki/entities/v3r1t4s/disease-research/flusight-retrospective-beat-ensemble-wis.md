---
id: v3r1t4s-flusight-retrospective-beat-ensemble-wis
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
tractability: 3.5
compute: "laptop-hours"
disclosure: open
status_checked: "2026-10-15"
---
# CDC FluSight hub: beat the FluSight-ensemble's season-average WIS retrospectively on a completed season

# Overview

> Bank id `flusight-retrospective-beat-ensemble-wis` · harvest · tractability 3.5 · laptop-hours · disclosure **open**
> Bank says open as of 2026-10-15. Statuses go stale — re-check the primary source before any work.

## Statement

The CDC FluSight forecast hub (github.com/cdcepi/FluSight-forecast-hub) stores every weekly probabilistic forecast ever submitted by every team (model-output/, one parquet/csv per model per reference date), the ground-truth target data including a hubverse oracle-output.csv (17 MB, fetched 2026-10-13) and time-series.csv (88 MB), the ensemble weights, and the official weighted-interval-score (WIS) evaluation reports (reports/Flu_Hospitalizations_Forecasts_WIS_27 May 2026.html and Flu_ED_Visit_Forecasts_WIS_27 May 2026.html, i.e. the 2025-26 season's end-of-season evaluation). The FluSight-ensemble routinely ranks at or near the top and beating it out-of-sample is a standing open problem in epidemic forecasting. Everything needed to score a new forecaster against every submitted model on a frozen, completed season is public, small and CPU-only, and the scoring rule (WIS over the hub's quantile levels, per horizon/location/target) is implemented in the open hubverse packages.

## Success criterion

Success means a released, deterministic forecasting pipeline plus saved quantile forecasts that (a) cover every reference date, location and horizon of ONE completed FluSight season as submitted-format output matching the hub's task-id schema in hub-config/, (b) at each reference date use ONLY data that was available on that date (the pipeline must read from the hub's own versioned/as-of target data or an archived data snapshot, and the code must be auditable for look-ahead, including no parameters tuned on later weeks of the same season), and (c) achieve a season-average WIS, computed with the public hubverse scoring code on the hub's oracle-output.csv for that season with the hub's own exclusion rules, STRICTLY LOWER (direction: min) than the FluSight-ensemble's season-average WIS for the same target, horizons, locations and reference dates as published in the hub's evaluation report in https://github.com/cdcepi/FluSight-forecast-hub/tree/main/reports , re-fetched live immediately before claiming, by at least 2% relative AND outside a stationary-bootstrap 90% interval over reference dates. A forecaster that consumes any other model's submitted forecasts for that season (including the ensemble's) is disqualified.

## Partial wins

- {"id": "p1", "statement": "Strictly lower season-average WIS than the FluSight-baseline model AND than the median submitted model for the same season/target/locations, under the same as-of data discipline and the hub's scorer, with the bootstrap interval excluding zero."}
- {"id": "p2", "statement": "Beat the FluSight-ensemble's WIS on the subset of forecasts at horizons 2-3 weeks ahead (where the ensemble is weakest) for all locations in a completed season, with the official scorer and the no-look-ahead audit, reported as a horizon-restricted result."}
- {"id": "p3", "statement": "A reproducible scoring audit: independently recompute the hub's published per-model season WIS table for a completed season from model-output/ plus oracle-output.csv with hubverse code, and document any model whose recomputed WIS differs from the published value by more than 1%, with the cause (missing submissions, revised targets, exclusion rules)."}

## Verification

Skeptic clones the hub at a pinned commit (model-output/, target-data/oracle-output.csv, hub-config/, reports/), validates the attacker's forecast files against the hub's validation schema, recomputes WIS for the attacker and for FluSight-ensemble/FluSight-baseline with the public hubverse scoring code (R hubEvals or an equivalent re-implementation cross-checked on the published numbers), and bootstraps over reference dates. Look-ahead audit: rerun the attacker's pipeline with the data snapshot truncated at each reference date and confirm the forecasts are reproduced bit-for-bit (or within documented stochastic tolerance), and grep the code and configs for any read of future weeks, of oracle-output.csv, or of other teams' submissions. All data is well under 1 GB.

## Angles

- Distributional discipline first: WIS rewards calibration more than point accuracy. Fit a simple, robust mean model (seasonal climatology plus recent trend) and spend the effort on the predictive distribution: quantile regression with heteroscedastic, horizon-dependent spread, conformalised quantiles from past residuals, and tail widening when the trend reverses.
- CROSS-DOMAIN (signal processing / control theory): treat weekly admissions as a noisy signal and forecast with a state-space model (Kalman/particle filter on log-incidence with a time-varying growth-rate state), which naturally produces calibrated intervals and handles reporting revisions as observation noise; add a Savitzky-Golay or wavelet denoiser before trend extraction.
- CROSS-DOMAIN (statistical physics / renewal theory): model epidemic growth as a renewal process with a time-varying reproduction number driven by an Ornstein-Uhlenbeck process, and propagate parameter uncertainty analytically; this is the physics-style answer to overconfident curve fits.
- CROSS-DOMAIN (ecology): borrow empirical-dynamic-modelling/nonlinear-time-series tools (simplex projection, S-map, attractor reconstruction across the 50+ state time series as a spatial replicate ensemble) to forecast by nearest-neighbour analogues of past season trajectories instead of parametric curves.
- Hierarchical pooling across locations and seasons: partial pooling (empirical Bayes shrinkage of growth rates toward national and census-division means) is where small-state WIS is won; the ensemble averages models, not information, so a properly pooled single model can beat it.
- CROSS-DOMAIN (compression / MDL for model selection): choose among candidate forecast families online by prequential (predictive) code length rather than by in-sample fit, which is exactly a WIS-friendly log-loss analogue and avoids the hindsight tuning that makes retrospective wins fake.
- Exploit documented ensemble weaknesses: turning points, holiday-week reporting artefacts, and seasons with early onset; a model that handles reporting-delay backfill explicitly (nowcast the most recent 2 weeks before forecasting) attacks the ensemble where it is structurally weak.

## Pitfalls

- Look-ahead/backfill leakage: hospitalisation and ED-visit targets are revised for weeks after first report. Training or fitting on the FINAL time series while claiming a retrospective forecast is the classic false positive here; only as-of snapshots (or the hub's versioned target data) may be used, and the oracle-output must never be read by the pipeline.
- Hindsight tuning: picking the model class, window length, or spread multiplier after seeing which choice scores best on that season is overfitting dressed as forecasting. Hyperparameters must be fixed on earlier seasons and frozen, with the commit history or a pre-registration to show it.
- Mismatched comparison sets: the ensemble's published WIS covers specific reference dates, locations, horizons and target (hospital admissions vs ED visits), with hub exclusion rules for missing or invalid submissions. Scoring the attacker on an easier subset (e.g. dropping low-count jurisdictions or a bad month) is the commonest way to fake a win.
- Scoring-rule errors: WIS must use the hub's exact quantile levels, with counts not rates, non-crossing quantiles, and the same log/natural scale as the official report; an averaging order change (mean of per-location WIS vs pooled) can move results by more than the claimed margin.
- Ensemble contamination: using other teams' submitted forecasts, or an ensemble member's output, for the same season turns the result into a post-hoc combination rather than a forecaster.

## Sources

- https://github.com/cdcepi/FluSight-forecast-hub/tree/main/reports
- https://github.com/cdcepi/FluSight-forecast-hub
- https://github.com/cdcepi/FluSight-forecast-hub/tree/main/model-output
- https://github.com/cdcepi/FluSight-forecast-hub/tree/main/target-data
- https://github.com/hubverse-org
- Status source: https://github.com/cdcepi/FluSight-forecast-hub/tree/main/reports

## Citations

- [Problem page](../../../../.raw/V3R1T4S/known-unknowns/disease-research/flusight-retrospective-beat-ensemble-wis.md)
- [Bank entry](../../../../.raw/V3R1T4S/bank/targets.json) (id `flusight-retrospective-beat-ensemble-wis`, commit `7dd4480`)

## Related Nodes

- [[V3R1T4S Disease research]]
- [[V3R1T4S]]
