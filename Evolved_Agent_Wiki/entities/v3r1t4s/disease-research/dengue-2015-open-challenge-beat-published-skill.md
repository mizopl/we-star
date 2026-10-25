---
id: v3r1t4s-dengue-2015-open-challenge-beat-published-skill
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
# Dengue Forecasting Project (San Juan and Iquitos): beat the published forecast skill on the frozen 2015 challenge targets

# Overview

> Bank id `dengue-2015-open-challenge-beat-published-skill` · harvest · tractability 3 · laptop-hours · disclosure **open**
> Bank says open as of 2026-10-15. Statuses go stale — re-check the primary source before any work.

## Statement

Dengue is the neglected-tropical-disease side of epidemic forecasting and has almost none of the infrastructure that influenza enjoys. The 2015 U.S. interagency Dengue Forecasting Project, analysed by Michael Johansson and colleagues in PNAS (open access, Europe PMC PMC6883829, 2019), remains the cleanest fully public benchmark: weekly case series, environmental and population data for San Juan (Puerto Rico) and Iquitos (Peru) are in github.com/cdcepi/dengue-forecasting-project-2015, the three targets (peak incidence, peak week, season total) and the probabilistic scoring rule (logarithmic score) are fixed and published, and the paper reports the skill achieved by every participating team and by a simple historical-average baseline, with the finding that many models failed to beat that baseline for several targets. Everything is kilobytes of CSV; the open question is whether modern methods beat the published skill under the challenge's own rules.

## Success criterion

Success means a released, deterministic pipeline plus saved probabilistic forecasts in the challenge's own format for ALL seasons, both cities and all three targets of the challenge, produced under the challenge's data rule - at each forecast week only data available then (the challenge's delivery schedule and the dated case series) and no data from the forecast season's future - whose mean logarithmic score, computed with the challenge's scoring definition by a scorer the skeptic reruns, is STRICTLY GREATER (direction: max, scores are log probabilities) than the best published mean score for that city and target, re-read live from https://www.ebi.ac.uk/europepmc/webservices/rest/PMC6883829/fullTextXML immediately before claiming, by a margin whose 95% bootstrap interval over forecast weeks excludes zero, AND strictly greater than the published historical-average baseline on the same rows. Results must be reported for all six city/target combinations; reporting only the combination that improved is not a result.

## Partial wins

- {"id": "p1", "statement": "Beat the published historical-average baseline on all three targets for BOTH cities under the challenge's data rule, with bootstrap intervals - something several original submissions did not achieve."}
- {"id": "p2", "statement": "Beat the best published score for peak week (the timing target, where the published skill is lowest) in one city, with the full predictive distributions released."}
- {"id": "p3", "statement": "A reproduction result: recompute the published per-team scores from the challenge's archived forecasts and the public truth series with a released scorer, documenting any discrepancy and its cause (score truncation rule, binning, missing weeks)."}

## Verification

Skeptic clones cdcepi/dengue-forecasting-project-2015, hashes the case and covariate series, reruns the attacker's pipeline week by week against a data loader truncated at each delivery date (file-access log checked), recomputes logarithmic scores with the challenge definition including its binning and truncation rules, bootstraps over forecast weeks, and re-reads the published skill table through Europe PMC. Kilobytes of data, minutes of CPU.

## Angles

- Treat the three targets as one joint distribution: simulate full season trajectories and derive peak height, peak week and season total from the same posterior, instead of fitting three separate predictors - coherence alone improves log scores.
- CROSS-DOMAIN (hydrology): seasonal streamflow forecasting faces the identical problem (predict a peak and its timing from a partially observed season) and its ensemble-streamflow-prediction trick - splice the observed season onto all historical remainders, then weight the analogues - is a strong, nearly parameter-free baseline.
- CROSS-DOMAIN (climate science): dengue transmission tracks temperature, rainfall and ENSO indices with lags; the challenge ships the environmental series, and lagged-covariate selection with proper out-of-sample discipline is underused.
- CROSS-DOMAIN (statistical physics / renewal processes): serotype-structured susceptibility makes successive seasons dependent; a renewal model with a susceptible-depletion state captures the alternation that pure time-series models miss.
- CROSS-DOMAIN (information theory): the score is a log score, so the task is density estimation, not point prediction - mixture densities, tail inflation and explicit mass on 'no epidemic' outcomes are where the score is won.
- Borrow across the two cities: San Juan has a much longer record than Iquitos, so hierarchical pooling of seasonal shape parameters regularises the short series.

## Pitfalls

- Hindsight data: the whole series is public today, so it is trivially easy to fit on the future of the season being forecast; only the challenge's as-of rule counts, with a file-access audit.
- Score definition: the challenge's logarithmic score uses specific bins and a truncation floor for zero-probability outcomes; changing the binning or the floor can swamp any real gain.
- Target cherry-picking: six city/target combinations invite selective reporting; all must be reported, and the baseline comparison must accompany every claim.
- Tiny samples: a handful of seasons means season-level luck dominates, so intervals over forecast weeks and, ideally, a leave-one-season-out replication are required before any claim.
- Old data: these are 1990s-2010s series from two cities; a skill gain is a methods result about this benchmark and carries no implication for current dengue control anywhere.

## Sources

- https://www.ebi.ac.uk/europepmc/webservices/rest/PMC6883829/fullTextXML
- https://github.com/cdcepi/dengue-forecasting-project-2015
- https://raw.githubusercontent.com/cdcepi/dengue-forecasting-project-2015/master/README.md
- https://predict.cdc.gov/
- Status source: https://github.com/cdcepi/dengue-forecasting-project-2015

## Citations

- [Problem page](../../../../.raw/V3R1T4S/known-unknowns/disease-research/dengue-2015-open-challenge-beat-published-skill.md)
- [Bank entry](../../../../.raw/V3R1T4S/bank/targets.json) (id `dengue-2015-open-challenge-beat-published-skill`, commit `7dd4480`)

## Related Nodes

- [[V3R1T4S Disease research]]
- [[V3R1T4S]]
