---
id: v3r1t4s-fermi-gbm-offline-tgf-missed
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
tractability: 1.5
compute: "laptop-hours"
disclosure: open
status_checked: "2026-10-15"
---
# Terrestrial gamma-ray flash in public Fermi GBM TTE data, absent from the GBM TGF catalog

# Overview

> Bank id `fermi-gbm-offline-tgf-missed` · standard · tractability 1.5 · laptop-hours · disclosure **open**
> Bank says open as of 2026-10-15. Statuses go stale — re-check the primary source before any work.

## Statement

The Fermi GBM TGF catalogue tables at the FSSC (Roberts et al. 2018, JGR Space Physics; the page calls the current tables the second catalogue) list 4,144 TGFs from 2008-07-11 to 2016-07-31, including an offline search of time-tagged-event data; TTE became continuous (CTTE) on 2012-11-26, after which the catalogue is more uniform. GBM daily TTE/CTTE data are public at HEASARC. The catalogue's sensitivity is inhomogeneous. Open task: a statistically significant TGF in public CTTE data inside 2012-11-26..2016-07-31 that the catalogue does not list.

## Success criterion

A saved candidate (UTC to 1 microsecond, detector list, TTE file names, photon list, detection code) inside the continuous-TTE period 2012-11-26..2016-07-31 (when the catalogue's offline search ran on full-orbit data) with >= 10 counts in <= 1 ms across >= 2 BGO+NaI detectors, hard spectrum (BGO counts > 100 keV), not during SAA passage, not a cosmic-ray shower signature (simultaneous saturation in all 14 detectors); the same pipeline run on a null set (the photon lists with arrival times scrambled within +/- 1 s blocks, and on orbits over oceans at high geomagnetic latitude where TGFs are rare) yields an expected false count < 0.05 over all searched data at the candidate's statistic; and no entry within +/- 1 ms in all six catalogue tables at https://fermi.gsfc.nasa.gov/ssc/data/access/gbm/tgf/ re-fetched live immediately before claiming, nor in any later public GBM TGF list found by search. Candidates after 2016-07-31 count only as partial win p3.

## Partial wins

- {"id": "p1", "statement": "A candidate in 2012-11-26..2016-07-31 with null-test expected false count < 0.5 (rather than 0.05), otherwise vetted as above."}
- {"id": "p2", "statement": "Independent re-detection of >= 95% of catalogue offline-search TGFs for one month with the same pipeline, establishing sensitivity."}
- {"id": "p3", "statement": "A vetted TGF after 2016-07-31 meeting all criteria, labelled 'not yet catalogued' (no public list covers that period), ideally with WWLLN-independent evidence such as a coincident GBM-only lightning-region orbit."}

## Verification

Skeptic downloads the cited daily TTE files from HEASARC, re-bins the photon list around the time, recomputes the background from +/- 1 s, recomputes Poisson significance and trials factor, and checks the catalog table. Under 45 minutes.

## Angles

- Conventional: multi-timescale Poisson search (50 us .. 1 ms) on summed BGO+NaI photon lists with a sliding background.
- Conventional: restrict to orbits over tropical thunderstorm regions (from orbit position) to raise the prior.
- Cross-domain import (neutrino/IceCube burst searches): unbinned maximum-likelihood with a time-clustering test statistic and scrambled-time background.
- Cross-domain import (network intrusion detection): change-point detection (Bayesian Blocks, CUSUM) on the photon arrival stream.

## Pitfalls

- Cosmic-ray air showers and particle events produce short bursts in all detectors - require a TGF-like detector pattern.
- Instrumental dead-time and pulse pile-up distort counts of very bright events.
- Look-elsewhere: the number of bins searched over years is enormous; per-bin significance is meaningless without trials correction.
- The GBM team may maintain a newer TGF list beyond the 2016 catalog; search for it before claiming.

## Sources

- https://fermi.gsfc.nasa.gov/ssc/data/access/gbm/tgf/
- https://heasarc.gsfc.nasa.gov/FTP/fermi/data/gbm/daily/
- Status source: https://fermi.gsfc.nasa.gov/ssc/data/access/gbm/tgf/

## Citations

- [Problem page](../../../../.raw/V3R1T4S/known-unknowns/earth-and-sky/fermi-gbm-offline-tgf-missed.md)
- [Bank entry](../../../../.raw/V3R1T4S/bank/targets.json) (id `fermi-gbm-offline-tgf-missed`, commit `7dd4480`)

## Related Nodes

- [[V3R1T4S Earth and sky]]
- [[V3R1T4S]]
