---
id: v3r1t4s-respicast-ili-ari-europe-beat-hub-ensemble
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
# European RespiCast hub: beat the hub ensemble's WIS for influenza-like illness or acute respiratory infection incidence across EU/EEA countries

# Overview

> Bank id `respicast-ili-ari-europe-beat-hub-ensemble` · harvest · tractability 3 · laptop-hours · disclosure **open**
> Bank says open as of 2026-10-15. Statuses go stale — re-check the primary source before any work.

## Statement

RespiCast's European Syndromic Indicators Forecasting Hub (ECDC with the ISI Foundation and the London School of Hygiene & Tropical Medicine; github.com/european-modelling-hubs/RespiCast-SyndromicIndicators, pushed 2026-10-13) collects weekly quantile forecasts of ILI and ARI incidence per 100,000 for EU/EEA countries, horizons 1 to 4 weeks. Unlike most hubs it publishes its own scores: model-evaluation/latest-forecast_scores.csv (32 MB, 276,635 rows, 33 model_ids) lists WIS and AE for every model, origin date, location and horizon from 2024-10-23 to 2026-10-07, including the ensemble (team_id respicast, model_id hubEnsemble) and the quantileBaseline, and target-data/ERVISS/snapshots holds the data vintages. That makes a vintage-honest retrospective comparison against the hub ensemble fully checkable on a laptop. Mean WIS over value_absolute, computed 2026-10-15: ILI 2024-25 ensemble 183.5 vs baseline 206.1; ILI 2025-26 ensemble 157.1 vs baseline 184.8; ARI 2024-25 ensemble 574.3 vs baseline 745.7; ARI 2025-26 ensemble 535.2 vs baseline 522.3, i.e. the quantile baseline currently beats the ensemble on ARI 2025-26 (raw mean WIS mixes countries of very different scale, so this is context, not a ranking).

## Success criterion

For one complete season (2024-25 or 2025-26) and one target (ILI or ARI incidence), quantile forecasts in the hub's format for every (origin_date, location, horizon) row where model_id hubEnsemble (team_id respicast) has a WIS in latest-forecast_scores.csv (re-fetched live immediately before claiming), produced by a frozen pipeline that at each origin date uses only the target-data snapshot available on that date, whose mean WIS (computed with the hub's evaluation convention against the same truth data the hub used) is STRICTLY LOWER (direction: min) than the ensemble's on exactly the same rows by at least 3% relative, with a paired bootstrap over origin dates excluding zero.

## Partial wins

- {"id": "p1", "statement": "Beat the hub ensemble on ARI incidence (fewer, newer models, so the ensemble is weaker) for one season under the full rules."}
- {"id": "p2", "statement": "Beat the best single submitted model's season-average relative WIS (not just the ensemble) for one target and season."}
- {"id": "p3", "statement": "Reproduce the hub's published WIS for hubEnsemble from its forecasts and truth to 4 significant figures (a verified scoring pipeline others can reuse)."}

## Verification

Skeptic loads latest-forecast_scores.csv, filters to the ensemble's rows (model_id == "hubEnsemble"; horizons 1-4), re-scores the attacker's forecast files against the hub truth with the hub convention (first reproducing the ensemble's published WIS to validate the scorer), checks via file-access logs that each origin date read only its snapshot, and bootstraps. Laptop-minutes to hours.

## Angles

- Pool across countries: a global model (gradient boosting or a small neural net) over all countries' scaled series learns season shape far better than per-country models, and the hub's best scorers (e.g. ISI-FluBcast, ISI-SEIR_BRW) hint that cross-country structure helps.
- Cross-domain import (retail demand forecasting): the M5-competition recipe of LightGBM on lagged features with Tweedie loss plus quantile post-processing.
- Cross-domain import (seismology): treat epidemic onset as an excitation; Hawkes / self-exciting point-process models capture early growth with few parameters.
- Calibrate rather than re-model: take the hub's own submitted forecasts available at each date and apply rolling conformal quantile recalibration plus performance-weighted pooling.
- Model reporting artefacts: ERVISS revisions and country-specific reporting delays; nowcast the horizon -1 value from snapshot-to-snapshot revisions.

## Pitfalls

- Using the latest target data (not the snapshot available at each origin date) leaks revisions; the snapshots folder exists to prevent this.
- Raw mean WIS mixes countries with incidence scales differing by orders of magnitude; compare on identical rows and also report relative WIS so a few large countries do not decide everything.
- Several submitted models have absurd outlier WIS values (e.g. 1e81) in the scores file; any 'beat the average model' framing is meaningless. Compare only to the ensemble on matched rows.
- Selecting the season or target after looking at results is a forking path; declare it before scoring.
- This is a forecasting benchmark, not public-health advice.

## Sources

- https://raw.githubusercontent.com/european-modelling-hubs/RespiCast-SyndromicIndicators/main/model-evaluation/latest-forecast_scores.csv
- https://github.com/european-modelling-hubs/RespiCast-SyndromicIndicators
- https://github.com/european-modelling-hubs/RespiCast-SyndromicIndicators/tree/main/target-data/ERVISS/snapshots
- https://respicast.ecdc.europa.eu/
- Status source: https://raw.githubusercontent.com/european-modelling-hubs/RespiCast-SyndromicIndicators/main/model-evaluation/latest-forecast_scores.csv

## Citations

- [Problem page](../../../../.raw/V3R1T4S/known-unknowns/disease-research/respicast-ili-ari-europe-beat-hub-ensemble.md)
- [Bank entry](../../../../.raw/V3R1T4S/bank/targets.json) (id `respicast-ili-ari-europe-beat-hub-ensemble`, commit `7dd4480`)

## Related Nodes

- [[V3R1T4S Disease research]]
- [[V3R1T4S]]
