---
id: v3r1t4s-iau-mdc-new-meteor-shower-gmn
type: entity
tags: [v3r1t4s, v3r1t4s/earth-and-sky, kind/harvest]
inbound_links: 1
confidence: 0.8
last_ingested_sources: [".raw/V3R1T4S/bank/targets.json@7dd4480"]
status: "CONFIRMED_SOLUTION"
priority: ""
notes: ""
category: earth-and-sky
kind: harvest
tractability: 3
compute: "laptop-hours"
disclosure: open
status_checked: "2026-10-15"
---
# New meteor shower in public Global Meteor Network orbits, absent from the live IAU MDC shower list

# Overview

> Bank id `iau-mdc-new-meteor-shower-gmn` · harvest · tractability 3 · laptop-hours · disclosure **open**
> Bank says open as of 2026-10-15. Statuses go stale — re-check the primary source before any work.

## Statement

The Global Meteor Network (GMN) publishes all its multi-station meteoroid orbits openly (traj_summary_yearly_2019..2026, ~3 GB total, refreshed daily). The IAU Meteor Data Center (MDC) maintains the list of all showers (established + working list + pending), last updated 2026-10-09, with a full-data file streamfulldata2026.txt. GMN itself keeps announcing new showers (M2025-L1/L2, O1, O2, P1, Q1, V1, M2026-P1 per eMeteorNews), which shows that unannounced compact orbit clusters still exist in the open data. Open task: find a statistically significant orbit cluster (new shower or outburst) in the public GMN data that matches no entry in the live MDC list and no GMN/CAMS/eMeteorNews report.

## Success criterion

A saved list of >= 15 GMN trajectory IDs (from traj_summary_yearly_*.txt) forming a cluster whose mean orbit has D_SH < 0.10 to each member's median-orbit and whose mean orbit has D_SH >= 0.20 (and radiant separation > 5 deg at matched solar longitude +/- 5 deg) from EVERY entry of streamfulldata2026.txt re-fetched live immediately before claiming; cluster significance must exceed 5 sigma against a sporadic background estimated from the same solar-longitude window in other years (or shuffled-solar-longitude bootstrap); meteors observed by >= 3 independent stations in >= 2 countries; and no eMeteorNews / WGN / arXiv report (last 24 months) of a shower with that radiant, solar longitude and velocity.

## Partial wins

- {"id": "p1", "statement": "A confirmed new one-year outburst (>= 10 meteors within 6 h, D_SH < 0.08, >= 5 sigma over sporadic background) not in the MDC list nor in eMeteorNews, even if not recurring."}
- {"id": "p2", "statement": "An annual recurrence of a working-list shower in >= 3 GMN years where the MDC entry rests on a single-year detection, with mean orbit consistent (D_SH < 0.1); non-trivial because it moves evidence toward establishment."}
- {"id": "p3", "statement": "A parent-body association: a candidate cluster whose mean orbit has D_SH < 0.15 to a JPL SBDB comet/NEO orbit with a successful meteoroid-stream integration (e.g. via REBOUND) placing ejecta at the observed node."}

## Verification

Skeptic downloads the cited traj_summary_yearly file(s) (minutes), extracts the listed IDs, recomputes the mean orbit and pairwise D_SH (Southworth-Hawkins) with a standalone script, re-runs the background estimate with a different random seed, re-fetches streamfulldata2026.txt live and recomputes D_SH to every listed shower; manual search of eMeteorNews and MDC 'new reports'. Under 30 minutes.

## Angles

- Conventional: DBSCAN / HDBSCAN in (lambda-lambda_sun, beta, v_g) sun-centred ecliptic coordinates per solar-longitude window, followed by D_SH / D_N refinement; scan low-activity Southern-hemisphere windows where camera coverage grew after 2023.
- Conventional: compare yearly activity profiles to find one-night outbursts (the dominant GMN discovery mode, e.g. M2025-Q1).
- Cross-domain import (particle physics): treat the radiant map as a 'bump hunt' with look-elsewhere correction (sideband background from adjacent solar longitudes, global p-value via toy Monte Carlo) instead of ad hoc D-criterion thresholds.
- Cross-domain import (astronomy/genomics): use the clustering-on-orbital-elements idea from asteroid family detection (hierarchical clustering method, Zappala) or single-linkage with Bonferroni-corrected null shuffles as used for gene-expression clusters.
- Cross-domain import (seismology): template matching - take known weak showers' mean orbits as templates and scan other years for repeat 'events' at the same node.

## Pitfalls

- Most 'new' clusters are already in the MDC working list under an obscure code or in the removed/pending lists - compare against ALL lists in streamfulldata2026.txt, not just established showers.
- Single-station or poorly converged trajectories create spurious radiant concentrations; filter on GMN quality columns (convergence angle, number of stations, velocity uncertainty).
- Observing-geometry artefacts: camera network growth and lunar phase change detection rates, mimicking 'activity'; the background must be from the same stations/season.
- GMN announces showers fast on eMeteorNews; a cluster from 2026 data may already be reported days ago - check the site immediately before claiming.
- Do not report to the MDC or GMN; claim only the verified saved cluster.

## Sources

- https://www.ta3.sk/IAUC22DB/MDC2022/Roje/roje_lista.php
- https://globalmeteornetwork.org/data/traj_summary_data/
- https://www.ta3.sk/IAUC22DB/MDC2022/Etc/streamfulldata2026.txt
- https://www.ta3.sk/IAUC22DB/MDC2022/Dokumenty/new_reports.php
- Status source: https://www.ta3.sk/IAUC22DB/MDC2022/Roje/roje_lista.php

## Citations

- [Problem page](../../../../.raw/V3R1T4S/known-unknowns/earth-and-sky/iau-mdc-new-meteor-shower-gmn.md)
- [Bank entry](../../../../.raw/V3R1T4S/bank/targets.json) (id `iau-mdc-new-meteor-shower-gmn`, commit `7dd4480`)

## Related Nodes

- [[V3R1T4S Earth and sky]]
- [[V3R1T4S]]
