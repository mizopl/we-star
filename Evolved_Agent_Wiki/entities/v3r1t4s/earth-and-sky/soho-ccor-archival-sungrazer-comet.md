---
id: v3r1t4s-soho-ccor-archival-sungrazer-comet
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
# Unreported sungrazing comet in archival SOHO/LASCO or GOES-19 CCOR coronagraph images, absent from Sungrazer lists

# Overview

> Bank id `soho-ccor-archival-sungrazer-comet` · harvest · tractability 2.5 · laptop-hours · disclosure **open**
> Bank says open as of 2026-10-15. Statuses go stale — re-check the primary source before any work.

## Statement

The NRL Sungrazer Project homepage reads '5,204 Comets Discovered So Far' (2026-10-15); public report tables include LASCO C2/C3 and GOES-19 CCOR-1/CCOR-2 reports (new reports daily), and confirmations lag by about a year (July-August 2025 confirmations posted 2026-05-28). Archival frames (LASCO C2/C3 1996-, CCOR 2025-) are open data and faint Kreutz fragments are still found in old frames. Open task: a moving-object track in archival public coronagraph images, consistent with a sungrazer orbit, that matches no confirmed comet, no report in the Sungrazer report tables and no MPC/CBET designation.

## Success criterion

A saved file of >= 6 measured positions (frame filename, UTC, pixel x,y, helioprojective coords) from >= 2 hours of public LASCO C2/C3 or CCOR frames, fitting a parabolic Kreutz-group (or other named group) orbit with RMS residual <= 1 pixel and consistent brightness; visible in independent difference images made by the skeptic; the same search run on a null set (the same frames in shuffled time order, and with velocity grids mirrored to retrograde-to-Kreutz directions) yields an expected false-track count < 0.05 at the candidate's fit quality over the searched span; and no entry within 1 deg / 6 h in the Sungrazer confirmation lists, report tables (including retracted and 'additional observations' rows) and discovery tables re-fetched live immediately before claiming, nor in MPC/CBET comet circulars for that date.

## Partial wins

- {"id": "p1", "statement": "Independent recovery (>= 6 positions, orbit fit) of an archival Sungrazer report that is listed as unconfirmed/uncertain, upgrading its evidence; non-trivial because it requires the same pipeline."}
- {"id": "p2", "statement": "An automated detector that, run blind on one month of CCOR-1 archive, recovers >= 90% of that month's confirmed comets with <= 5 false tracks per day, saved as a reproducible notebook."}
- {"id": "p3", "statement": "A sungrazer seen simultaneously in two instruments (e.g. LASCO C3 + CCOR-2) whose combined astrometry yields a parallax-constrained orbit, for a comet listed in only one instrument."}

## Verification

Skeptic downloads the cited FITS frames from the public LASCO/CCOR archives, builds running-difference images, blinks the stated positions, re-fits a parabolic orbit with a standalone script (e.g. find_orb-style or Kreutz-template fit), and searches the live Sungrazer tables for date/position. Under 45 minutes.

## Angles

- Conventional: shift-and-stack along Kreutz-template trajectories (synthetic tracking) on archival C2 frames to reach below single-frame detection limits.
- Conventional: target archive periods with data gaps or low hunter activity (pre-2004 lists lack report times; early CCOR commissioning months).
- Cross-domain import (astronomy/exoplanets): KBMOD-style GPU-free 'shift-and-stack' / matched-filter likelihood over velocity grids, as used to find faint Kuiper-belt objects.
- Cross-domain import (particle physics tracking): Hough-transform / Kalman-filter track finding on difference-image detections, as in collider tracking chambers.
- Cross-domain import (video surveillance): background modelling with robust PCA to remove the F-corona and streamers before detection.

## Pitfalls

- Cosmic-ray hits, hot pixels and star/planet trails mimic tracks over 2-3 frames; require >= 6 frames and orbit consistency.
- Many 'new' tracks are known comets reported by hunters days or years ago; search all report tables, including retracted and 'additional observations' rows.
- Planets, background stars and Mercury/Venus ghosts move predictably; mask them with an ephemeris.
- Reporting to the Sungrazer form is a submission on the user's behalf and is not allowed; claim the saved verified track only.

## Sources

- https://sungrazer.nrl.navy.mil/index.php/confirmation_lists
- https://lasco-www.nrl.navy.mil/index.php?p=content/retrieve/products
- https://umbra.nascom.nasa.gov/pub/lasco/lastimage/
- https://sohoftp.nascom.nasa.gov/
- https://sungrazer.nrl.navy.mil/index.php/reports
- Status source: https://sungrazer.nrl.navy.mil/

## Citations

- [Problem page](../../../../.raw/V3R1T4S/known-unknowns/earth-and-sky/soho-ccor-archival-sungrazer-comet.md)
- [Bank entry](../../../../.raw/V3R1T4S/bank/targets.json) (id `soho-ccor-archival-sungrazer-comet`, commit `7dd4480`)

## Related Nodes

- [[V3R1T4S Earth and sky]]
- [[V3R1T4S]]
