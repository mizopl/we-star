---
id: v3r1t4s-glm-bolide-not-in-nasa-catalog
type: entity
tags: [v3r1t4s, v3r1t4s/earth-and-sky, kind/harvest]
inbound_links: 1
confidence: 0.8
last_ingested_sources: [".raw/V3R1T4S/bank/targets.json@7dd4480"]
status: "open"
priority: ""
notes: ""
category: earth-and-sky
kind: harvest
tractability: 2.5
compute: "laptop-hours"
disclosure: open
status_checked: "2026-10-15"
---
# Bolide in public GOES GLM lightning-mapper data absent from the NASA GLM bolide catalog

# Overview

> Bank id `glm-bolide-not-in-nasa-catalog` · harvest · tractability 2.5 · laptop-hours · disclosure **open**
> Bank says open as of 2026-10-15. Statuses go stale — re-check the primary source before any work.

## Statement

NASA's neo-bolide.ndc.nasa.gov publishes a curated catalogue of bolides detected by the GOES-16/17/18/19 Geostationary Lightning Mappers (public JSON API: 11,611 published events on 2026-10-15, latest event 2026-10-06, published 2026-10-12). GLM L2 LCFA files are public on the NOAA open-data S3 buckets (noaa-goes16/17/18/19). The pipeline uses classifiers on GLM group data plus human vetting, so faint, short or stereo-ambiguous bolides can be missed. Open task: a bolide in public GLM data, older than 2 months, that is absent from the live catalogue.

## Success criterion

A saved candidate (UTC time, lat/lon, GLM file names, group/event IDs, extracted light curve, detection code) such that: the light curve lasts >= 100 ms with a smooth single- or multi-peaked meteor shape and a spatial track of >= 3 pixels moving consistently; there is NO co-located lightning (no other GLM flashes within 50 km and +/- 2 min); the same detector run on a null set (one month of data in a lightning-active region, plus the candidate month with group times shuffled within flashes) gives an expected false count < 0.05 at the candidate's score over the searched span; ideally stereo detection by two GLMs; and no event within +/- 2 min / 200 km in the bolide JSON API and the CNEOS fireball API, both re-fetched live immediately before claiming.

## Partial wins

- {"id": "p1", "statement": "A stereo (two-GLM) candidate whose triangulated altitude is 20-90 km and whose ground track is non-lightning-like, absent from the catalog."}
- {"id": "p2", "statement": "A blind detector run over one month of GLM-16 data that recovers >= 90% of the catalog's events for that month, with the residual non-catalog detections listed and hand-vetted."}

## Verification

Skeptic downloads the cited GLM L2 files from the NOAA S3 bucket, re-extracts the groups, plots the light curve and track, checks for nearby lightning flashes in the same and adjacent files, and queries both catalogs live. Under 30 minutes.

## Angles

- Conventional: re-implement the published GLM bolide features (group duration, track linearity, energy ratio) with a random forest trained on catalog events vs lightning.
- Conventional: search overlap regions of GOES-East/West for stereo coincidences that single-satellite classifiers down-weight.
- Cross-domain import (particle physics triggers): a two-level trigger with a loose online cut and an offline likelihood ratio, estimating the false-positive rate on time-shifted data.
- Cross-domain import (exoplanet transit search): treat each pixel's group-energy time series like a light curve and apply matched filters (box/Gaussian templates) for meteor-shaped pulses.
- Cross-domain import (sports/ball tracking): RANSAC line fitting on event centroids to separate straight bolide tracks from branching lightning.

## Pitfalls

- Lightning is the dominant false positive; isolated 'bolt from the blue' flashes and sprites can be linear and short.
- Glint and instrument artefacts (sun glint over oceans, South Atlantic Anomaly hits, GLM 'blooming') create bright compact events.
- Catalog publication lags detection by days; candidates from the last 2 weeks may simply be unpublished - restrict to windows older than 2 months.
- Do not report to NASA; claim only the saved verified candidate.

## Sources

- https://neo-bolide.ndc.nasa.gov/
- https://neo-bolide.ndc.nasa.gov/service/event/public
- https://noaa-goes16.s3.amazonaws.com/?list-type=2&prefix=GLM-L2-LCFA/
- https://noaa-goes18.s3.amazonaws.com/?list-type=2&prefix=GLM-L2-LCFA/&max-keys=1
- https://noaa-goes19.s3.amazonaws.com/?list-type=2&prefix=GLM-L2-LCFA/&max-keys=1
- https://ssd-api.jpl.nasa.gov/fireball.api
- https://cneos.jpl.nasa.gov/fireballs/
- Status source: https://neo-bolide.ndc.nasa.gov/

## Citations

- [Problem page](../../../../.raw/V3R1T4S/known-unknowns/earth-and-sky/glm-bolide-not-in-nasa-catalog.md)
- [Bank entry](../../../../.raw/V3R1T4S/bank/targets.json) (id `glm-bolide-not-in-nasa-catalog`, commit `7dd4480`)

## Related Nodes

- [[V3R1T4S Earth and sky]]
- [[V3R1T4S]]
