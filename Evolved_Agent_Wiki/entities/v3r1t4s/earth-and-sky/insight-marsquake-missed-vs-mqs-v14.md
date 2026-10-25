---
id: v3r1t4s-insight-marsquake-missed-vs-mqs-v14
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
tractability: 2
compute: "laptop-hours to laptop-days (one station, ~1,400 sols of 20-100 sps three-component data, a few tens of GB via FDSN dataselect)"
disclosure: open
status_checked: "2026-10-15"
---
# Marsquake in open InSight SEIS waveforms absent from the Marsquake Service catalogue V14 and the MarsQuakeNet extension

# Overview

> Bank id `insight-marsquake-missed-vs-mqs-v14` · harvest · tractability 2 · laptop-hours to laptop-days (one station, ~1,400 sols of 20-100 sps three-component data, a few tens of GB via FDSN dataselect) · disclosure **open**
> Bank says open as of 2026-10-15. Statuses go stale — re-check the primary source before any work.

## Statement

NASA's InSight lander recorded Martian seismicity with one station (XB.ELYSE) from 2019 to 2022. The InSight Marsquake Service (MQS; Clinton, Ceylan, Giardini, Stahler, Horleston and colleagues) released catalogue V14 (2023-04-01, DOI 10.12686/a21), served live by the EarthScope mars-event FDSN service (2,715 rows on 2026-10-15). Dahmen et al. (2022, JGR Planets, 'MarsQuakeNet') used a deep denoiser/detector to extend the catalogue by about 60% (1,297 to 2,079 events, mostly low SNR), and Dahmen et al. (2024, GJI) added further low-frequency events; MQS has announced a final reference catalogue (over 1,900 events) that was not found as a public data release on 2026-10-15. Waveforms are open via FDSN dataselect. Open task: a marsquake clearly recorded on SEIS that is in none of these lists.

## Success criterion

A saved event package (UTC onset, event class by MQS conventions - LF/BB/HF/VF/24 - with the 2.4 Hz resonance or P/S evidence, spectrograms, FDSN request URLs, detection code) such that: the event has SNR >= 3 in its MQS-class band on the vertical and at least one horizontal channel; it is not a glitch, donk, lander/wind transient or atmospheric pressure signal (checks: polarisation, VBB/SP consistency, co-located pressure and wind sensor data quiet within +/- 10 min); the detector's false-alarm rate measured on a null set (the same pipeline run on time-reversed and phase-randomised data from the same sols) implies an expected false count < 0.05 over the searched span at the event's statistic; and no event within +/- 10 min in the live mars-event service at https://service.earthscope.org/irisws/mars-event/1/query?format=text and in the MarsQuakeNet and Dahmen 2024 supplementary lists and any public MQS final catalogue, all re-fetched live immediately before claiming. If a list cannot be fetched, the result is reported as a partial win only.

## Partial wins

- {"id": "p1", "statement": "An event absent from V14 that IS in the MarsQuakeNet list, independently recovered with a different method and the null test above (confirms an ML-only detection)."}
- {"id": "p2", "statement": "A new distance or back-azimuth for a V14 event that has none, from re-picked P/S phases with stated uncertainties."}
- {"id": "p3", "statement": "A blind detector that recovers >= 90% of V14 quality-A/B events in one season with a measured false-alarm rate, saved and re-runnable."}

## Verification

Skeptic downloads the cited waveform windows (and pressure/wind channels) via FDSN dataselect, reproduces spectrograms and polarisation, reruns the detector's null test with a different random seed, and queries the mars-event service and the supplementary lists. About 1 hour.

## Angles

- Conventional: template matching with V14 high-frequency events (which repeat with similar spectra) across all quiet evening hours, where Martian wind noise is lowest.
- Conventional: spectrogram-energy detector at the 2.4 Hz resonance with sol-of-day noise baselines.
- Cross-domain import (gravitational-wave searches): chi-square signal-consistency vetoes and time-slide backgrounds to control glitch false alarms on a single noisy station.
- Cross-domain import (bioacoustics): animal-call detectors trained with few labels on spectrogram patches (e.g. BirdNET-style), adapted to the HF/VF spectral templates.
- Cross-domain import (wind-turbine condition monitoring): regress out wind- and pressure-driven noise from co-located meteorological channels before detection.

## Pitfalls

- Most 'new' low-SNR events are already in MarsQuakeNet's list; that list must be checked, not only V14.
- Lander and tether thermal 'donks', glitches and wind gusts create impulsive signals; the polarisation and atmospheric-channel checks are mandatory.
- Daytime wind noise dominates; detections clustered in windy hours are suspect - examine the null-test rate by local time.
- The mars-event service lists multiple rows per event for some IDs; match by time window, not by row count.
- Do not report to MQS; claim only the saved verified package.

## Sources

- https://service.earthscope.org/irisws/mars-event/1/query?format=text
- https://www.insight.ethz.ch/en/seismicity/catalog/v14/
- https://service.earthscope.org/fdsnws/dataselect/1/
- https://service.earthscope.org/fdsnws/station/1/
- Status source: https://service.earthscope.org/irisws/mars-event/1/query?format=text

## Citations

- [Problem page](../../../../.raw/V3R1T4S/known-unknowns/earth-and-sky/insight-marsquake-missed-vs-mqs-v14.md)
- [Bank entry](../../../../.raw/V3R1T4S/bank/targets.json) (id `insight-marsquake-missed-vs-mqs-v14`, commit `7dd4480`)

## Related Nodes

- [[V3R1T4S Earth and sky]]
- [[V3R1T4S]]
