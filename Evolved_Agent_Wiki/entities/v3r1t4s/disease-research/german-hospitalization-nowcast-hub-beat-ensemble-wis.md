---
id: v3r1t4s-german-hospitalization-nowcast-hub-beat-ensemble-wis
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
# German COVID-19 hospitalization nowcast hub: beat the hub ensemble's WIS on the published real-time nowcasts

# Overview

> Bank id `german-hospitalization-nowcast-hub-beat-ensemble-wis` · harvest · tractability 3 · laptop-hours · disclosure **open**
> Bank says open as of 2026-10-15. Statuses go stale — re-check the primary source before any work.

## Statement

Nowcasting - estimating today's value of a statistic that will only be complete in weeks - is the neglected half of epidemic forecasting, and Germany's seven-day COVID-19 hospitalization incidence was a textbook case because reports arrive with long, age- and state-dependent delays. The Hospitalization Nowcast Hub run by the Karlsruhe Institute of Technology chair of econometrics and statistics with the Heidelberg Institute for Theoretical Studies (github.com/KITmetricslab/hospitalization-nowcast-hub) archives, in a standard format, every submitted real-time nowcast (data-processed), retrospective nowcasts (data-processed_retrospective), and the Robert Koch Institute truth data with its full reporting triangle (data-truth). Daniel Wolffram, Johannes Bracher and colleagues published the collaborative evaluation in 2023 (PMC10446237), scoring models and the ensemble by weighted interval score across states and age groups. The data is tens of megabytes and the whole exercise is CPU-only.

## Success criterion

Success means saved quantile nowcasts, in the hub's submission format, for every (forecast_date, location, age_group, delay horizon) row for which the hub ensemble has a nowcast over one declared continuous evaluation period of at least eight weeks within the hub's operating window, produced by a deterministic pipeline that at each date reads ONLY the reporting triangle as it stood on that date (the hub's dated truth files), whose mean weighted interval score against the hub's final truth, recomputed by the skeptic with public scoring code on exactly those rows, is STRICTLY LOWER (direction: min) than the ensemble's by at least 5% relative, with a stationary bootstrap over dates at 90% excluding zero. The scorer must first reproduce the ensemble's published scores from https://github.com/KITmetricslab/hospitalization-nowcast-hub and the evaluation of https://www.ebi.ac.uk/europepmc/webservices/rest/PMC10446237/fullTextXML (re-read live immediately before claiming) to within 1%. Submitted nowcasts of other teams may not be consumed.

## Partial wins

- {"id": "p1", "statement": "Beat the ensemble by >= 5% relative WIS restricted to the youngest and oldest age strata, where delays are longest and the submitted pool thinnest, over the declared period."}
- {"id": "p2", "statement": "Beat every individual submitted model (not necessarily the ensemble) over the declared period under the as-of discipline, with the bootstrap interval excluding zero."}
- {"id": "p3", "statement": "A reproduction of the hub's published evaluation: recompute per-model WIS for the published period from data-processed and the truth data with a released script, documenting every discrepancy and the exclusion rules needed to reconcile it."}

## Verification

Skeptic clones the hub at a pinned commit, reconstructs the reporting triangle as of each nowcast date from the dated truth files, validates the attacker's files against the hub format, recomputes WIS for the attacker and the ensemble on identical rows with public code (validated by reproducing the published numbers), bootstraps over dates, and audits for look-ahead by rerunning the pipeline on truncated triangles and by code review. Tens of megabytes, minutes of CPU.

## Angles

- Model the delay distribution properly: a hierarchical negative-binomial delay model with day-of-week effects, state and age-group random effects and a slowly varying reporting-probability curve is the textbook nowcast and still beats most submissions when fitted carefully.
- CROSS-DOMAIN (survival analysis): the reporting triangle is right-truncated survival data, so inverse-probability-of-censoring weighting and discrete-time hazard models transfer directly and give calibrated intervals.
- CROSS-DOMAIN (queueing theory): treat reports as arrivals through a server with time-varying capacity (weekends, holidays, backlog clearance) rather than as a static delay distribution - backlog dynamics are exactly what breaks naive nowcasts.
- CROSS-DOMAIN (signal processing / deconvolution): nowcasting is deconvolution of a known-ish delay kernel from a truncated signal; regularised Richardson-Lucy or total-variation deconvolution with uncertainty by bootstrap is an unexploited angle.
- Borrow strength across strata: states and age groups share delay structure; partial pooling plus post-stratification stabilises the thin strata where the ensemble is weakest.
- Calibration last: conformalise the predictive quantiles on past nowcast errors, since WIS rewards honest spread far more than a better point estimate.

## Pitfalls

- Triangle leakage: using the completed truth for past dates instead of the triangle as it stood is the defining false positive of nowcasting work; the audit must rerun the pipeline on truncated triangles.
- Revision definition: the RKI series was itself revised and redefined during the period; the claim must state which truth version it scores against and use the same one for both predictors.
- Row mismatch across strata: the ensemble does not cover every state/age/date cell; scoring on an easier subset is the commonest way to fake a win.
- Short evaluation windows: the hub's window is limited, so a few weeks of luck can look like skill; the stationary bootstrap over dates and a minimum window length are required.
- Consuming other teams' nowcasts turns the result into a post-hoc combination rather than a nowcaster.
- A WIS improvement on an archived German series is a methods result, not public-health guidance.

## Sources

- https://github.com/KITmetricslab/hospitalization-nowcast-hub
- https://www.ebi.ac.uk/europepmc/webservices/rest/PMC10446237/fullTextXML
- https://raw.githubusercontent.com/KITmetricslab/hospitalization-nowcast-hub/main/README.md
- https://github.com/epiforecasts/scoringutils
- Status source: https://github.com/KITmetricslab/hospitalization-nowcast-hub

## Citations

- [Problem page](../../../../.raw/V3R1T4S/known-unknowns/disease-research/german-hospitalization-nowcast-hub-beat-ensemble-wis.md)
- [Bank entry](../../../../.raw/V3R1T4S/bank/targets.json) (id `german-hospitalization-nowcast-hub-beat-ensemble-wis`, commit `7dd4480`)

## Related Nodes

- [[V3R1T4S Disease research]]
- [[V3R1T4S]]
