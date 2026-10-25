---
id: v3r1t4s-apollo-moonquake-missed-vs-pds-catalog
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
compute: "laptop-hours (Apollo PSE long-period data 1969-1977 via FDSN dataselect, network XA, a few GB per station-year)"
disclosure: open
status_checked: "2026-10-15"
---
# New deep moonquake or impact in open Apollo Passive Seismic Experiment data, absent from the PDS expanded lunar event catalogue

# Overview

> Bank id `apollo-moonquake-missed-vs-pds-catalog` · harvest · tractability 2.5 · laptop-hours (Apollo PSE long-period data 1969-1977 via FDSN dataselect, network XA, a few GB per station-year) · disclosure **open**
> Bank says open as of 2026-10-15. Statuses go stale — re-check the primary source before any work.

## Statement

The PDS Geosciences Node hosts the Apollo Passive Seismic Experiment expanded event catalogue (bundle by Renee Weber; levent.1008weber.csv, 13,057 events, built on Nakamura's catalogue and including Bulow et al. 2005/2007 template-matched deep moonquakes), plus deep-moonquake location tables (Nakamura 2005). Apollo 12, 14, 15 and 16 seismic data (network XA, stations S12-S16) are served openly by EarthScope FDSN dataselect. Deep moonquakes recur from fixed 'nests' at tidal periodicities, so template matching keeps finding members missed by visual cataloguing. Open task: a new event (deep moonquake nest member, shallow moonquake or meteoroid impact) recorded on >= 2 stations that the PDS catalogue does not list.

## Success criterion

A saved event package (UTC time, station/channel list, FDSN request URLs, waveforms, template or detector code) such that: for a deep moonquake, normalised cross-correlation >= 0.5 with the stack of a catalogued nest on >= 2 stations with consistent relative arrival times (within 2 s of the nest's moveout) and occurrence phase consistent with the nest's tidal periodicity; for other types, coherent arrivals on >= 2 stations with a location solution (RMS <= 3 s); the detection statistic exceeds the maximum obtained on a null set (the same templates correlated with time-reversed data and with data circularly shifted between stations by >= 1 h) over the full searched span; data-gap, thermal moonquake (sunrise/sunset) and instrument-glitch checks pass; and no event within +/- 5 min in levent.1008weber.csv and the other tables of https://pds-geosciences.wustl.edu/lunar/urn-nasa-pds-apollo_seismic_event_catalog/data/ re-fetched live immediately before claiming, nor in any published expanded deep-moonquake list of the last 24 months found by search.

## Partial wins

- {"id": "p1", "statement": "A new member of a catalogued nest seen on a single station with CC >= 0.6 and the null test passed (single-station detections are weaker evidence)."}
- {"id": "p2", "statement": "Recovery of >= 90% of one nest's catalogued events in one year with a measured false-alarm rate, saved and re-runnable."}
- {"id": "p3", "statement": "Relocation of a catalogued nest with formal errors at least 30% smaller than Nakamura 2005, using added arrival picks."}

## Verification

Skeptic fetches the cited waveform windows, recomputes cross-correlations against the nest stack built from the catalogue times, reruns the time-reversed and shifted nulls, and checks the PDS tables. Under 1 hour.

## Angles

- Conventional: multi-station template matching (EQcorrscan-style) for each well-sampled deep moonquake nest, scanning windows predicted by the nest's tidal phase.
- Conventional: subspace detectors built from the SVD of each nest's catalogued waveforms, more tolerant of waveform variability.
- Cross-domain import (astronomy): use the tidal (27.2-day / 206-day) periodicity as a prior, the way periodic transit searches fold light curves.
- Cross-domain import (genomics): locality-sensitive hashing of spectrogram fingerprints (as in FAST for earthquakes) to find repeats without templates.
- Cross-domain import (structural health monitoring): thermal-moonquake rejection with temperature-cycle models tied to lunar sunrise and sunset.

## Pitfalls

- Data glitches, timing jumps and telemetry dropouts are common in Apollo data; reject candidates near gaps or timing discontinuities.
- Thermal moonquakes repeat at sunrise/sunset and can correlate with templates; check lunar local time at each station.
- Bulow et al. already template-matched many nests; their events are in the Weber catalogue - search it by time, not by event type.
- Correlation maxima chosen over long scans need the null test; per-window significance is meaningless without it.
- Do not contact PDS or the catalogue authors; claim only the saved package.

## Sources

- https://pds-geosciences.wustl.edu/missions/apollo/seismic_event_catalog.htm
- https://pds-geosciences.wustl.edu/lunar/urn-nasa-pds-apollo_seismic_event_catalog/data/
- https://service.earthscope.org/fdsnws/station/1/
- https://service.earthscope.org/fdsnws/dataselect/1/
- Status source: https://pds-geosciences.wustl.edu/lunar/urn-nasa-pds-apollo_seismic_event_catalog/data/

## Citations

- [Problem page](../../../../.raw/V3R1T4S/known-unknowns/earth-and-sky/apollo-moonquake-missed-vs-pds-catalog.md)
- [Bank entry](../../../../.raw/V3R1T4S/bank/targets.json) (id `apollo-moonquake-missed-vs-pds-catalog`, commit `7dd4480`)

## Related Nodes

- [[V3R1T4S Earth and sky]]
- [[V3R1T4S]]
