---
id: v3r1t4s-flusight-ed-visits-beat-ensemble-wis
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
# CDC FluSight emergency-department visits: beat the FluSight-ensemble's season WIS on the newer ED-visit target

# Overview

> Bank id `flusight-ed-visits-beat-ensemble-wis` · harvest · tractability 3.5 · laptop-hours · disclosure **open**
> Bank says open as of 2026-10-15. Statuses go stale — re-check the primary source before any work.

## Statement

The CDC FluSight hub added a second prediction target - the weekly proportion of emergency-department visits attributed to influenza, from the National Syndromic Surveillance Program - alongside its long-running hospital-admissions target, and publishes a separate end-of-season evaluation for it (reports/'Flu_ED_Visit_Forecasts_WIS_27 May 2026.html' in github.com/cdcepi/FluSight-forecast-hub, directory fetched 2026-10-15; model-output holds every team's submissions through 2026-10-17, and target-data holds oracle-output.csv, 17 MB, plus the 89 MB time-series.csv with as-of values). The ED-visit target is young: fewer teams have tuned models for a bounded proportion with its own reporting artefacts, the series is revised, and the ensemble's lead over the baseline is correspondingly less entrenched than on admissions. The scoring rule is the open hubverse weighted interval score, so a stranger can rescore everything on a laptop.

## Success criterion

Success means saved quantile forecasts, in the hub's submission format for the ED-visit target, covering every reference date, location and horizon of ONE completed season for which FluSight-ensemble submitted, produced by a released deterministic pipeline that at each reference date uses only data available then (the hub's as-of target data or an archived snapshot; no final revised series, no oracle-output, no other team's submissions, no parameter tuned on later weeks of that season), whose season-average WIS, computed with public hubverse scoring code against the hub's oracle-output for that season under the hub's exclusion rules, is STRICTLY LOWER (direction: min) than the FluSight-ensemble's for the same target, season, locations, horizons and reference dates as published in the hub's ED-visit evaluation report in https://github.com/cdcepi/FluSight-forecast-hub/tree/main/reports , re-fetched live immediately before claiming, by at least 3% relative AND outside a stationary-bootstrap 90% interval over reference dates. The scorer must first reproduce the ensemble's published value for that season to within 1%.

## Partial wins

- {"id": "p1", "statement": "Strictly lower season-average WIS than the FluSight-baseline AND than the median submitted model on the ED-visit target for one completed season, under the as-of discipline and the hub's scorer."}
- {"id": "p2", "statement": "Beat the ensemble at horizons 2-3 weeks ahead on the ED-visit target across all locations of one completed season, reported as a horizon-restricted result."}
- {"id": "p3", "statement": "A transfer result: show that a single model fitted jointly on the admissions and ED-visit targets beats the same model fitted on ED visits alone, by a margin with an interval, quantifying how much the older target's history is worth."}

## Verification

Skeptic clones the hub at a pinned commit, validates the attacker's files against hub-config task-ids for the ED-visit target, recomputes WIS for the attacker, the ensemble and the baseline with public hubverse code (first reproducing the published report value), bootstraps over reference dates, and audits look-ahead by rerunning the pipeline on truncated snapshots and by grepping for reads of oracle-output, of future weeks or of model-output. Under a gigabyte, CPU-only.

## Angles

- Respect the support: the target is a bounded proportion, so logit-scale modelling with heteroscedastic, horizon-dependent spread and back-transformed quantiles avoids the crossing and tail problems that cost WIS on count-style models.
- CROSS-DOMAIN (signal processing / control): a state-space model on logit-proportion with a time-varying growth state and revisions treated as observation noise produces calibrated intervals without hand-tuned spread.
- CROSS-DOMAIN (econometrics of mixed-frequency data): ED visits lead admissions, so a leading-indicator regression (MIDAS-style) exploits the two targets' different timing instead of modelling each in isolation.
- CROSS-DOMAIN (ecology / nonlinear dynamics): analogue forecasting across jurisdictions as replicate trajectories handles season-shape variation that parametric curves miss, especially at turning points.
- Backfill first: the most recent weeks of NSSP proportions are revised, so an explicit revision model for the last two weeks is probably the largest single WIS gain.
- Hierarchical pooling across jurisdictions and the two targets, with shrinkage of growth-rate volatility toward a national mean - the ensemble averages models, not information.

## Pitfalls

- Look-ahead through revisions: the ED-visit series is revised after first report; fitting on the final series while claiming a retrospective forecast is the classic false positive here.
- Target confusion: the hub scores two targets with different units and different reports; comparing against the hospital-admissions ensemble value, or mixing the targets' rows, invalidates the claim.
- Mismatched task sets: the ensemble's published score covers specific locations, horizons and dates with exclusion rules; dropping low-volume jurisdictions is the commonest fake win.
- Hindsight tuning: choosing the transform, window or spread multiplier after seeing the season's scores must be excluded by freezing parameters on earlier seasons with commit evidence.
- Ensemble contamination: consuming other teams' submissions for the scored season makes the result a combination, not a forecast.
- A WIS improvement is a forecasting-method result and is not public-health guidance.

## Sources

- https://github.com/cdcepi/FluSight-forecast-hub/tree/main/reports
- https://github.com/cdcepi/FluSight-forecast-hub
- https://github.com/cdcepi/FluSight-forecast-hub/tree/main/target-data
- https://github.com/hubverse-org
- Status source: https://github.com/cdcepi/FluSight-forecast-hub/tree/main/reports

## Citations

- [Problem page](../../../../.raw/V3R1T4S/known-unknowns/disease-research/flusight-ed-visits-beat-ensemble-wis.md)
- [Bank entry](../../../../.raw/V3R1T4S/bank/targets.json) (id `flusight-ed-visits-beat-ensemble-wis`, commit `7dd4480`)

## Related Nodes

- [[V3R1T4S Disease research]]
- [[V3R1T4S]]
