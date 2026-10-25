---
id: v3r1t4s-covid19-hub-europe-archive-beat-eurocovidhub-ensemble
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
# European COVID-19 Forecast Hub archive: beat EuroCOVIDhub-ensemble's WIS on the hub's own published scores

# Overview

> Bank id `covid19-hub-europe-archive-beat-eurocovidhub-ensemble` · harvest · tractability 3 · laptop-hours · disclosure **open**
> Bank says open as of 2026-10-15. Statuses go stale — re-check the primary source before any work.

## Statement

The European COVID-19 Forecast Hub ran from 2021 to autumn 2024 and is now archived at github.com/european-modelling-hubs/covid19-forecast-hub-europe_archive, with every submitted forecast in data-processed, the truth data, and - crucially - its own evaluation/scores.csv, a 2.8 MB file holding WIS, its sharpness/under- and overprediction decomposition, absolute error, bias and interval coverage for every model, forecast date, horizon and country (31,256 rows covering 2023-10-30 to 2024-09-16 as fetched 2026-10-15), including EuroCOVIDhub-ensemble and EuroCOVIDhub-baseline. Nikos Bosse, Katharine Sherratt and colleagues' evaluation of this hub (PMC10238088, 2023) found the ensemble hard to beat, which is exactly the standing question. Everything needed for a frozen, vintage-honest retrospective is public and small, and because the hub is closed the comparison can never drift under the claimant's feet.

## Success criterion

Success means saved quantile forecasts, in the hub's submission format, covering every (model-free) forecast_date, location, target_variable and horizon for which EuroCOVIDhub-ensemble has a row in https://raw.githubusercontent.com/european-modelling-hubs/covid19-forecast-hub-europe_archive/main/evaluation/scores.csv (re-fetched live immediately before claiming) for one declared target_variable and one declared continuous period of at least six months, produced by a deterministic pipeline that at each forecast date uses only data available then (the hub's dated truth snapshots; no final revised series, no other team's submissions, no parameter tuned on later weeks), whose mean WIS, recomputed by the skeptic with the public scoringutils/hubverse implementation on the identical rows, is STRICTLY LOWER (direction: min) than the ensemble's by at least 3% relative, with a stationary bootstrap over forecast dates at 90% excluding zero. The scorer must first reproduce the ensemble's published WIS from the raw forecasts and truth to within 1%.

## Partial wins

- {"id": "p1", "statement": "Strictly lower mean WIS than EuroCOVIDhub-baseline AND than the median submitted model over the declared period and target, under the as-of discipline, with the bootstrap interval excluding zero."}
- {"id": "p2", "statement": "Beat the ensemble on the subset of smaller countries (bottom half by mean reported count), where ensembles are typically weakest, across all forecast dates of the declared period."}
- {"id": "p3", "statement": "An independent scoring reproduction: recompute the published per-model WIS decomposition in scores.csv from data-processed and the truth data, documenting every model whose recomputed value differs by more than 1% and why."}

## Verification

Skeptic clones the archive at a pinned commit, validates the attacker's forecast files against the hub format, recomputes WIS for the attacker, the ensemble and the baseline with public scoring code (first reproducing published values as a scorer check), bootstraps over forecast dates, and audits for look-ahead by rerunning the attacker's pipeline against truncated truth snapshots and by grepping the code for reads of future weeks, of scores.csv or of data-processed. The repository is a few hundred megabytes; the check is CPU-minutes.

## Angles

- Use the score decomposition as a map: scores.csv separates sharpness from under- and overprediction per model and country, so the attacker can see exactly where the ensemble pays - usually overprediction after peaks - and design for that.
- CROSS-DOMAIN (renewal theory / statistical physics): a renewal-process model with an Ornstein-Uhlenbeck reproduction number propagates uncertainty analytically and avoids the overconfident curve fits that WIS punishes.
- CROSS-DOMAIN (signal processing): complex demodulation or a Kalman filter on log-incidence estimates phase and amplitude separately, and epidemic turning points are phase problems.
- CROSS-DOMAIN (econometrics): forecast combination with time-varying weights estimated by exponentially weighted performance (the standard model-averaging literature) applied only to past scores at each date, with shrinkage to equal weights.
- CROSS-DOMAIN (MDL / prequential model selection): choose among candidate forecast families online by predictive code length rather than hindsight fit - the discipline that keeps retrospective wins honest.
- Hierarchical pooling across countries and waves, which is where small-country WIS is won; the ensemble averages models, not information.

## Pitfalls

- Final-data leakage: training or fitting on the revised series while calling the exercise retrospective is the classic false positive; only dated snapshots may be read and the audit must show it.
- Hindsight tuning: selecting the model family, window or spread multiplier after seeing the period's scores is overfitting dressed as forecasting; parameters must be frozen on an earlier period with commit evidence.
- Row mismatch: the ensemble did not submit every week for every country; the comparison must be on exactly its rows, with the hub's exclusion rules.
- Scoring conventions: WIS depends on the quantile set, counts versus rates and the averaging order; reproducing the published ensemble values first is the only way to know the scorer matches.
- Ensemble contamination: consuming other teams' submissions for the same period turns the result into a post-hoc combination, not a forecaster.
- A retrospective WIS gain on a closed hub is a methods result; it is not evidence about any future epidemic.

## Sources

- https://raw.githubusercontent.com/european-modelling-hubs/covid19-forecast-hub-europe_archive/main/evaluation/scores.csv
- https://github.com/european-modelling-hubs/covid19-forecast-hub-europe_archive
- https://www.ebi.ac.uk/europepmc/webservices/rest/PMC10238088/fullTextXML
- https://github.com/epiforecasts/scoringutils
- Status source: https://raw.githubusercontent.com/european-modelling-hubs/covid19-forecast-hub-europe_archive/main/evaluation/scores.csv

## Citations

- [Problem page](../../../../.raw/V3R1T4S/known-unknowns/disease-research/covid19-hub-europe-archive-beat-eurocovidhub-ensemble.md)
- [Bank entry](../../../../.raw/V3R1T4S/bank/targets.json) (id `covid19-hub-europe-archive-beat-eurocovidhub-ensemble`, commit `7dd4480`)

## Related Nodes

- [[V3R1T4S Disease research]]
- [[V3R1T4S]]
