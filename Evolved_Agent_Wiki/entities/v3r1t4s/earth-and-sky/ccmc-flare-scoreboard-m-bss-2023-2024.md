---
id: v3r1t4s-ccmc-flare-scoreboard-m-bss-2023-2024
type: entity
tags: [v3r1t4s, v3r1t4s/earth-and-sky, kind/standard]
inbound_links: 1
confidence: 0.8
last_ingested_sources: [".raw/V3R1T4S/bank/targets.json@7dd4480"]
status: "open"
priority: ""
notes: ""
category: earth-and-sky
kind: standard
tractability: 2.5
compute: "laptop-hours (scoreboard forecasts via HAPI in seconds; GOES-16 flare summary 6 MB; SWPC region summaries and HMI SHARP keywords via plain GET)"
disclosure: open
status_checked: "2026-10-15"
---
# NASA CCMC Flare Scoreboard: a reproducible 24-hour M-class flare forecast that beats every scoreboard model's Brier skill score over 2023-2024

# Overview

> Bank id `ccmc-flare-scoreboard-m-bss-2023-2024` · standard · tractability 2.5 · laptop-hours (scoreboard forecasts via HAPI in seconds; GOES-16 flare summary 6 MB; SWPC region summaries and HMI SHARP keywords via plain GET) · disclosure **open**
> Bank says open as of 2026-10-15. Statuses go stale — re-check the primary source before any work.

## Statement

The NASA CCMC Flare Scoreboard (Leila Mays and the CCMC team; models by NOAA SWPC, SIDC/ROB, ASSA, SPS, AMOS and others) archives real-time full-disk flare probabilities through a public HAPI service. Scored here against GOES-16 XRS science-quality flare peaks (NOAA NCEI flsum v2-2-1; 1,278 M1+ peaks in 2023-2024), using 24-hour windows that start at most 1 h after issue and comparing with climatology over the same windows, the Brier skill scores for 2023-01-01..2024-12-31 are (computed 2026-10-15): NOAA_1 0.2145 when P(M+) = 1-(1-M)(1-X) (0.1727 if its M value is read as M+), SIDC_Operator 0.1446, ASSA_24H_1 0.1446, SPS 0.1141, AMOS_v1 -0.113. A 3-day persistence baseline scores 0.106 on the NOAA windows. Base rate of M+ days is 0.57 (solar maximum). Open task: a forecast built only from data public before each issue time that beats the best of these on the same windows.

## Success criterion

A saved forecast file (one 00:00-24:00 UT P(>=M1.0) per day, 2023-01-01..2024-12-31) plus code that regenerates it using only data timestamped at least 2 hours before each window start (GOES XRS 1-min fluxes, NOAA SWPC solar region summaries, HMI SHARP NRT keywords) and training data ending before 2023-01-01, whose Brier skill score against climatology, with outcomes = any GOES-16 flsum EVENT_PEAK of class M or X in the window, is strictly greater (direction: max) than the best full-disk model's BSS on its own matched windows, computed by the skeptic from the HAPI service https://ccmc.gsfc.nasa.gov/flare-scoreboard/hapi/catalog re-fetched live immediately before claiming, using for each model the most favourable reading of its M probability; the margin must exceed the 95% block-bootstrap (27-day blocks) interval of the BSS difference, i.e. the lower bound of the difference must be > 0.

## Partial wins

- {"id": "p1", "statement": "Beat the SIDC_Operator and ASSA_24H_1 BSS (0.1446) on their own windows with the same rules and bootstrap test."}
- {"id": "p2", "statement": "A forecast with BSS > 0.2145 on the NOAA windows whose reliability diagram slope lies within 0.9-1.1 (well calibrated), even if the bootstrap lower bound is not above 0."}
- {"id": "p3", "statement": "Beat the best scoreboard model on the X-class 24-hour forecast (BSS, same windows) for 2023-2024."}

## Verification

Skeptic downloads the HAPI forecasts and the GOES-16 flsum NetCDF, runs a standalone Brier/BSS script with the window matching rule above, regenerates the claimed forecast from code with a data-cutoff harness (inputs read through a function that refuses timestamps later than window start minus 2 h), and runs the block bootstrap. Under 1 hour.

## Angles

- Conventional: logistic regression or gradient boosting on SWPC region-summary features (McIntosh class, area, spot count) plus recent flare history (counts and peak flux of the last 24-72 h), calibrated with isotonic regression.
- Conventional: SHARP-keyword models (total unsigned flux, R-value, free-energy proxies) aggregated over the disk, combined with persistence.
- Cross-domain import (seismology): epidemic-type aftershock (ETAS / Hawkes) models of flare self-excitation, giving a background-plus-triggering rate turned into a 24 h probability.
- Cross-domain import (sports and election forecasting): forecast combination - a weighted pool of the scoreboard's own historical behaviour is not allowed, but pooling your own diverse models with weights fitted on pre-2023 data often beats any single model in Brier score.
- Cross-domain import (credit scoring): monotone-constrained boosting and Platt calibration for rare-event probabilities under base-rate drift across the solar cycle.

## Pitfalls

- Hindsight leakage: training or tuning on 2023-2024 outcomes, or using science-quality data products released months later as if available in real time, inflates skill; the 2-hour cutoff and pre-2023 training rule are mandatory.
- Window mismatch: scoreboard models issue at different times (NOAA ~22 UT for 00-24 UT, SIDC 12:30 UT); comparing your 00-24 UT score to a model's differently aligned windows is not like for like - match windows per model.
- Probability definitions differ (M-only vs M-or-greater); give each comparator its most favourable reading, as above.
- At a 0.57 base rate, small BSS gains are within bootstrap noise; autocorrelated days require block bootstrap, not i.i.d. resampling.
- GOES satellite or calibration changes (GOES-16 to GOES-18/19) shift flare counts near class thresholds; use the single stated flsum file.

## Sources

- https://ccmc.gsfc.nasa.gov/scoreboards/flare/
- https://ccmc.gsfc.nasa.gov/flare-scoreboard/hapi/catalog
- https://data.ngdc.noaa.gov/platforms/solar-space-observing-satellites/goes/goes16/l2/data/xrsf-l2-flsum_science/
- https://www.ngdc.noaa.gov/stp/space-weather/swpc-products/daily_reports/solar_region_summaries/
- Status source: https://ccmc.gsfc.nasa.gov/flare-scoreboard/hapi/catalog

## Citations

- [Problem page](../../../../.raw/V3R1T4S/known-unknowns/earth-and-sky/ccmc-flare-scoreboard-m-bss-2023-2024.md)
- [Bank entry](../../../../.raw/V3R1T4S/bank/targets.json) (id `ccmc-flare-scoreboard-m-bss-2023-2024`, commit `7dd4480`)

## Related Nodes

- [[V3R1T4S Earth and sky]]
- [[V3R1T4S]]
