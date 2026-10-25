---
id: v3r1t4s-rsv-hub-retrospective-beat-ensemble-wis
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
# RSV forecast hub: beat the hub ensemble's season-average WIS retrospectively on a completed RSV season

# Overview

> Bank id `rsv-hub-retrospective-beat-ensemble-wis` · harvest · tractability 3 · laptop-hours · disclosure **open**
> Bank says open as of 2026-10-15. Statuses go stale — re-check the primary source before any work.

## Statement

RSV forecasting is the thin, under-studied sibling of influenza and COVID forecasting: far fewer teams, far fewer published methods, and strong age-structured seasonality. Two public hubverse hubs cover it. (a) github.com/HopkinsIDD/rsv-forecast-hub is now an archive: from the 2025-26 season the hub was handed to CDC's Center for Forecasting and Outbreak Analytics; its model-output/hub-ensemble has 47 files ending 2025-04-06 (2023-24 files marked -RETRO), it scores RSV-NET-derived hospitalisation counts by state AND age group, and target-data/archive holds 153 dated *_rsvnet_hospitalization.csv vintages (2023-10-16 to 2026-05-29). (b) github.com/CDCgov/rsv-forecast-hub runs the live season with 18 model directories and RSVHub-ensemble (33 files, 2025-09-27 to 2026-10-17 as of 2026-10-15); its targets are wk inc rsv hosp (NHSN confirmed admissions) and wk inc rsv prop ed visits (NSSP) with NO age groups, and its hubverse target-data ships time-series.parquet with as_of plus oracle-output.parquet. Neither hub ships a scores file, so the ensemble's own model-output is the comparator and must be re-scored. Because the submitted model pool is small, the gap between the hub ensemble and a carefully calibrated single model is plausibly larger here than for flu, while the data is tiny and entirely CPU-friendly.

## Success criterion

Success means, on ONE of two separately declared routes, saved quantile forecasts in that hub's submission format produced by a released deterministic pipeline that at each reference date reads only data available on that date (as-of vintages; no final revised series, no other team's forecasts, no parameter tuned on later weeks of the same season), whose season-average WIS, computed with the public hubverse scoring code (same locations, horizons, reference dates and, where applicable, age groups; hub exclusion rules applied), is STRICTLY LOWER (direction: min) than the hub ensemble's season-average WIS recomputed identically from that hub's own ensemble model-output, re-fetched live immediately before claiming, by at least 3% relative AND outside a stationary-bootstrap 90% interval over reference dates. Route (a), archive: a completed season (2023-24 or 2024-25) of github.com/HopkinsIDD/rsv-forecast-hub, covering every reference date, location, age group and horizon of the hub-ensemble (https://github.com/HopkinsIDD/rsv-forecast-hub/tree/main/model-output/hub-ensemble), with as-of data taken from that hub's target-data/archive vintages. Route (b), live hub: the 2025-26 season of github.com/CDCgov/rsv-forecast-hub for wk inc rsv hosp or wk inc rsv prop ed visits, against RSVHub-ensemble (https://github.com/CDCgov/rsv-forecast-hub/tree/main/model-output/RSVHub-ensemble), with as-of data taken from that hub's time-series.parquet as_of column or from data.cdc.gov releases available at each reference date. Neither hub currently publishes its own scores file; if one appears for the claimed season, its ensemble value becomes the bar instead of the recomputed one.

## Partial wins

- {"id": "p1", "statement": "Strictly lower season-average WIS than every individual submitted model (not necessarily the ensemble) for a completed season, under the as-of data discipline and the public scorer, with a bootstrap interval excluding zero."}
- {"id": "p2", "statement": "Route (a) only: beat the ensemble's WIS restricted to the pediatric (0-4 years) age groups of the HopkinsIDD archive hub, where RSV dynamics are sharpest and the submitted pool is thinnest, across all locations and reference dates of a completed season (the CDCgov hub has no age groups)."}
- {"id": "p3", "statement": "An independent recomputation of per-model season WIS for a completed RSV season from the hub's raw model-output and target data, released as a reproducible script, documenting any discrepancy with the hub's own published scores (if any) and the exclusion rules needed to reconcile them."}

## Verification

Same mechanics as the FluSight target: pin the hub commit, validate the attacker's files against hub-config task-ids, recompute WIS with public hubverse code for the attacker, each submitted model and the ensemble, bootstrap over reference dates, and audit for look-ahead by rerunning the pipeline against truncated data snapshots and by code review (no reads of future weeks, of the final target series, or of model-output/). Data volume is tens of megabytes; the whole check is minutes on CPU.

## Angles

- Age-structured mechanistic core with statistical calibration: a compact age-stratified SIRS/renewal model with waning immunity, fitted per jurisdiction by particle filtering, then conformalised residual quantiles; RSV's strong immunity-driven biennial-ish pattern rewards mechanism more than flu does.
- CROSS-DOMAIN (signal processing): seasonal harmonic regression with time-varying amplitude/phase estimated by a Kalman filter or complex demodulation; RSV onset timing runs by weeks between seasons and jurisdictions, so phase estimation (not level fitting) is the real forecasting problem.
- CROSS-DOMAIN (ecology / metapopulation): treat jurisdictions as patches with coupled epidemic waves, estimate a spatial coupling kernel from past seasons (gravity model fitted to onset-time lags), and forecast a late-onset state from its already-peaking neighbours.
- CROSS-DOMAIN (combinatorial search over model space): run a small genetic-programming / model-lottery search over forecast formulas and spread rules, with prequential (out-of-sample, earlier-seasons-only) selection to avoid hindsight bias; selection by prequential code length (MDL) keeps it honest.
- Nowcast the backfill first: RSV surveillance reporting is late and incomplete; a reporting-delay model (negative-binomial delay distribution per jurisdiction, estimated from revision history in the hub's target-data history) that corrects the last 2-3 weeks before extrapolating is probably the single biggest WIS gain available.
- Borrow strength from influenza and COVID hubs: fit shared hierarchical priors on growth-rate volatility across respiratory pathogens, then specialise per pathogen, exploiting the much richer flu record to regularise the thin RSV one.

## Pitfalls

- Revision leakage: RSV hospitalisation targets are revised substantially; fitting on final data and calling it a retrospective forecast is the standard false positive. Only as-of snapshots may be used, and the audit must show it.
- Thin-pool illusion: with few submitted models and few seasons, one season's WIS is noisy. A 1-2% margin is meaningless; require a bootstrap interval over reference dates and, if possible, replication on a second completed season.
- Target/scale mismatch: age-group and location sets changed across seasons in this hub, as did the target definition and the hub-config task-ids. Comparing a forecaster scored on one task set to an ensemble scored on another is invalid.
- Hindsight model selection: choosing the mechanistic structure, waning rate or spread multiplier after inspecting the season is overfitting; parameters must be frozen from earlier seasons with commit evidence.
- Ensemble recomputation error: if the hub's ensemble is weighted or trained, recomputing it naively (equal-weight median) can create a strawman that is easy to beat; the ensemble's own submitted output in model-output/ is the only legitimate comparator.
- The CDCgov hub removed auxiliary-data/nssp-raw-data/latest.parquet on 2026-10-12, so a pipeline that relied on the hub's own Wednesday NSSP release must switch to data.cdc.gov releases - and must still only read the vintage available at each reference date.
- Mixing the two hubs: the HopkinsIDD archive scores RSV-NET counts by age group, the CDCgov hub scores NHSN admissions and NSSP ED-visit proportions without age groups. A forecast scored on one hub's targets cannot be compared with the other hub's ensemble.

## Sources

- https://github.com/CDCgov/rsv-forecast-hub/tree/main/model-output/RSVHub-ensemble
- https://github.com/CDCgov/rsv-forecast-hub
- https://github.com/HopkinsIDD/rsv-forecast-hub/tree/main/model-output/hub-ensemble
- https://github.com/HopkinsIDD/rsv-forecast-hub
- https://github.com/HopkinsIDD/rsv-forecast-hub/tree/main/target-data
- https://github.com/hubverse-org
- Status source: https://github.com/CDCgov/rsv-forecast-hub/tree/main/model-output/RSVHub-ensemble

## Citations

- [Problem page](../../../../.raw/V3R1T4S/known-unknowns/disease-research/rsv-hub-retrospective-beat-ensemble-wis.md)
- [Bank entry](../../../../.raw/V3R1T4S/bank/targets.json) (id `rsv-hub-retrospective-beat-ensemble-wis`, commit `7dd4480`)

## Related Nodes

- [[V3R1T4S Disease research]]
- [[V3R1T4S]]
