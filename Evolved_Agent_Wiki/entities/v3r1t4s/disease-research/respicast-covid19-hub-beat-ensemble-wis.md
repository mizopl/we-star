---
id: v3r1t4s-respicast-covid19-hub-beat-ensemble-wis
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
# RespiCast COVID-19 hub: beat the hub ensemble's season WIS for COVID-19 hospital admissions in EU/EEA countries

# Overview

> Bank id `respicast-covid19-hub-beat-ensemble-wis` · harvest · tractability 3 · laptop-hours · disclosure **open**
> Bank says open as of 2026-10-15. Statuses go stale — re-check the primary source before any work.

## Statement

The European COVID-19 Forecasting Hub, run by ECDC with the ISI Foundation and the London School of Hygiene & Tropical Medicine as part of RespiCast (github.com/european-modelling-hubs/respicast-COVID19), collects weekly quantile forecasts of COVID-19 hospital admissions for EU/EEA countries and - unusually - publishes its own scores: model-evaluation/latest-forecast_scores.csv (5.9 MB, fetched 2026-10-15) carries WIS, relative WIS and rank for every model, origin date, country and horizon from 2024-10-23 onwards, including the hubEnsemble and the quantileBaseline, while target-data holds the ERVISS data with dated snapshots. This is the COVID-19 sibling of the hub's syndromic-indicator track and a separate forecasting problem (admissions counts, different country set, different model pool). Beating a hub ensemble out of sample is a standing open question in epidemic forecasting, and everything needed is a few megabytes of CSV.

## Success criterion

For one complete season (2024-25 or 2025-26) and the hospital-admissions target, quantile forecasts in the hub's format for every (origin_date, location, horizon) row for which hubEnsemble has a WIS in https://raw.githubusercontent.com/european-modelling-hubs/respicast-COVID19/main/model-evaluation/latest-forecast_scores.csv (re-fetched live immediately before claiming), produced by a frozen pipeline that at each origin date reads only the target-data snapshot available on that date and no other team's forecasts, whose mean WIS - computed with the hub's own convention, validated by first reproducing hubEnsemble's published WIS on those rows to four significant figures - is STRICTLY LOWER (direction: min) than the ensemble's on exactly those rows by at least 3% relative, with a paired bootstrap over origin dates whose interval excludes zero. The season and target must be declared before scoring.

## Partial wins

- {"id": "p1", "statement": "Beat the hub ensemble under the full rules at horizons 1-2 only (the near-term, backfill-dominated horizons) for one complete season, reported as a horizon-restricted result."}
- {"id": "p2", "statement": "Beat the best single submitted model's season-average relative WIS (not only the ensemble) for one season, on matched rows."}
- {"id": "p3", "statement": "Reproduce the hub's published WIS for hubEnsemble and quantileBaseline from the raw forecasts and the truth data to four significant figures, released as a reusable scoring script, documenting the exclusion rules needed to reconcile them."}

## Verification

Skeptic loads latest-forecast_scores.csv, filters to hubEnsemble rows for the declared season and target, re-scores the attacker's forecast files against the hub's truth with the hub convention (validating the scorer by reproducing the ensemble's published values first), checks via file-access logs that each origin date read only the snapshot available then, confirms no row of another team's model-output was read, and bootstraps over origin dates. Laptop-minutes.

## Angles

- Nowcast the reporting delay first: ERVISS admissions are revised for weeks, and the near horizons dominate average WIS, so a negative-binomial delay model fitted to snapshot-to-snapshot revisions is probably the single largest gain available.
- Pool across countries: a single global model over scaled national series, with partial pooling of growth rates toward a European mean, beats per-country fits when several countries report only a handful of admissions a week.
- CROSS-DOMAIN (energy demand forecasting): quantile regression averaging and rolling conformal recalibration of quantiles, the standard recipe of electricity-load competitions, targets WIS directly because WIS rewards calibration over point accuracy.
- CROSS-DOMAIN (control theory): a state-space model on log-admissions with a time-varying growth-rate state (Kalman or particle filter) treats revisions as observation noise and emits calibrated intervals by construction.
- CROSS-DOMAIN (ecology / nonlinear time series): simplex projection and S-map analogue forecasting across the 25+ country series as replicate trajectories, instead of parametric curves, handles turning points where ensembles are weakest.
- Reconciliation: forecast countries jointly and reconcile to an EU aggregate (MinT), which stabilises small countries whose WIS is otherwise dominated by noise.

## Pitfalls

- Vintage leakage: using the current target data rather than the snapshot available at each origin date silently imports revisions; the snapshots folder exists precisely to prevent this and the audit must show it.
- Row mismatch: the ensemble's scores cover specific origin dates, countries and horizons; dropping hard countries or weeks is the commonest way to fake a win, so the comparison must be on exactly the ensemble's rows.
- Scale mixing: national admission counts differ by orders of magnitude, so a raw mean WIS is dominated by the largest countries; relative WIS must be reported alongside and the row set must be identical.
- Season or target selection after seeing results is a forking path; declare both before scoring.
- Outlier scores: submitted models occasionally carry absurd WIS values in these files, so any 'beats the average model' framing is meaningless - the ensemble on matched rows is the only legitimate bar.
- This is a forecasting-method benchmark, not public-health advice.

## Sources

- https://raw.githubusercontent.com/european-modelling-hubs/respicast-COVID19/main/model-evaluation/latest-forecast_scores.csv
- https://github.com/european-modelling-hubs/respicast-COVID19
- https://github.com/european-modelling-hubs/respicast-COVID19/tree/main/target-data
- https://respicast.ecdc.europa.eu/
- Status source: https://raw.githubusercontent.com/european-modelling-hubs/respicast-COVID19/main/model-evaluation/latest-forecast_scores.csv

## Citations

- [Problem page](../../../../.raw/V3R1T4S/known-unknowns/disease-research/respicast-covid19-hub-beat-ensemble-wis.md)
- [Bank entry](../../../../.raw/V3R1T4S/bank/targets.json) (id `respicast-covid19-hub-beat-ensemble-wis`, commit `7dd4480`)

## Related Nodes

- [[V3R1T4S Disease research]]
- [[V3R1T4S]]
