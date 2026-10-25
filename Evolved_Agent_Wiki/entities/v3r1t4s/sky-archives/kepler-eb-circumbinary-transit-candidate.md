---
id: v3r1t4s-kepler-eb-circumbinary-transit-candidate
type: entity
tags: [v3r1t4s, v3r1t4s/sky-archives, kind/standard]
inbound_links: 1
confidence: 0.8
last_ingested_sources: [".raw/V3R1T4S/bank/targets.json@7dd4480"]
status: "open"
priority: ""
notes: ""
category: sky-archives
kind: standard
tractability: 1.5
compute: "laptop-hours to laptop-days (2878 EB light curves ~ 1.5 GB; the N-body stacking search is CPU-heavy, so restrict to detached EBs with morph < 0.5 and P_bin 5-60 d, ~ 700 systems)"
disclosure: open
status_checked: "2026-10-08"
---
# New circumbinary transit candidate in a Kepler eclipsing binary (Villanova EB catalog)

# Overview

> Bank id `kepler-eb-circumbinary-transit-candidate` · standard · tractability 1.5 · laptop-hours to laptop-days (2878 EB light curves ~ 1.5 GB; the N-body stacking search is CPU-heavy, so restrict to detached EBs with morph < 0.5 and P_bin 5-60 d, ~ 700 systems) · disclosure **open**
> Bank says open as of 2026-10-08. Statuses go stale — re-check the primary source before any work.

## Statement

Among the Kepler eclipsing binaries of the Villanova catalog (Kirk+2016, VizieR J/AJ/151/68, 2878 systems in the VizieR snapshot), find an additional transit-like signal (>= 3 events of variable duration/interval consistent with a circumbinary orbit, found directly or by a stacked detection using N-body-predicted transit windows as in the STANLEY algorithm) in a detached EB that is not one of the known Kepler circumbinary-planet systems (pscomppars cb_flag=1: Kepler-16, -34, -35, -38, -47, -64/PH1, -413, -453, -1647, -1661 by transit, plus Kepler-1660 and Kepler-451 by eclipse timing, as of 2026-10-08) and not a tertiary eclipse already in the Villanova catalog or in the Borkovits+2016 Kepler triples catalog (VizieR J/MNRAS/455/4136, 222 systems). As of a Jan 2025 presentation, the STANLEY survey of ~700 Windemuth-catalog EBs had found one unpublished additional planet, so a new candidate must be flagged for Windemuth membership. Absence checks are done by downloading whole ra/dec/id/ephemeris column lists with plain TAP/CSV requests (e.g. select+pl_name,hostname,ra,dec,cb_flag+from+pscomppars) and cross-matching LOCALLY; ADQL cone functions (contains/point/circle) in the Exoplanet Archive URL trigger a Cloudflare block and must not be used or retried. SIMBAD TAP cone queries are fine.

## Success criterion

A saved bundle {KIC, Villanova ephemeris, detrended light curve with primary/secondary eclipses masked, list of transit events (epoch, duration, depth), N-body/analytic circumbinary model with the binary parameters from the Villanova catalog (or Windemuth+2019) that reproduces every event's time and duration within errors, pixel-level centroid test on each event, null test, and the catalog files used} such that: (1) ABSENCE, re-fetched live immediately before claiming: the KIC position (3 arcsec) matches no pscomppars row (plain column download incl. cb_flag, matched locally) and no ExoFOP TOI/CTOI row, the KIC is not in VizieR J/MNRAS/455/4136 (Borkovits+2016 triples), and a SIMBAD TAP cone of 3 arcsec on the host returns no object whose otype is a planet or planet candidate (Pl, Pl?) or an eclipsing binary (EB*, EB?), which catches literature candidates that the Archive tables ingest with a lag; (2) >= 3 events, each individually > 5 sigma, with the dip on target in the pixel-level test; (3) the events are not periodic at the binary period or its harmonics and are not fit (delta-BIC > 10 in favour of the circumbinary model) by a strictly periodic third-body eclipse model, ruling out tertiary eclipses; (4) the circumbinary N-body model reproduces every event time and duration within errors; (5) null test: the same stacking search at >= 100 random trial orbits of the same planet period range yields no detection as significant as the claim; (6) implied radius < 2 RJup; (7) the host star id (TIC/KIC/EPIC/Gaia DR3) is not the host of any already-claimed (a confirmed result listed in this repository's RESULTS.md) claim under any other astronomy target of this bank, so the same signal is never counted twice across tess-new-vetted-transit-candidate / kepler-k2-new-vetted-transit-candidate / kepler-tess-single-transit-long-period-candidate / kepler-eb-circumbinary-transit-candidate. Claim is 'new circumbinary transit candidate'.

## Partial wins

- {"id": "cbp-reproduce-known", "statement": "Pipeline recovers, from raw Kepler light curves, the transits of at least 5 known Kepler circumbinary planets (Kepler-16b, 34b, 35b, 38b, 47b/c/d, 64b, 413b, 453b, 1647b, 1661b) with correct epochs and the variable durations predicted by the N-body model; saved as a table."}
- {"id": "cbp-tertiary-eclipse-new", "statement": "A new eclipse of a third body (depth and duration implying a stellar or brown-dwarf radius) in a Villanova EB not flagged as a triple in the catalog's ETV/tertiary columns or in the literature; checkable by the same bundle minus the planetary-radius condition."}
- {"id": "cbp-stanley-style-upper-limits", "statement": "A per-EB injection-recovery completeness map (transiting-planet radius x period) for >= 100 detached Villanova EBs with the agent's search, delivered as a CSV; non-trivial because such limits exist only for the ~700 Windemuth systems."}
- {"id": "cbp-two-event-unvetted", "statement": "A two-event circumbinary-like signal passing (1),(3),(6) but with only 2 events: logged as unvetted (two events are always fit by both models), never claimed."}

## Verification

Skeptic re-downloads the KIC light curves from MAST, masks the eclipses with the saved Villanova ephemeris, confirms each listed event by re-fitting at the saved epoch, re-runs the saved N-body/analytic model to check it predicts the event times, and queries pscomppars + the Villanova page for the KIC. Under one hour. Also re-runs the Borkovits+2016 VizieR match, the SIMBAD cone and the random-orbit null test from the saved files.

## Angles

- Detached EBs (morph < 0.5) with P_bin between 7 and 40 d that are NOT in the Windemuth+2019 ~700-system sample (so untouched by STANLEY): the Villanova catalog has ~1,500 more systems.
- Stack transits at N-body-predicted windows over a grid of planet period and inclination (STANLEY-style) rather than fixed-period BLS, which fails for circumbinary transits of variable interval.
- Use eclipse-timing variations in the Villanova ETV files as a prior for the planet period before stacking.
- Look for lone, deep (> 1%) transit-like events outside eclipse in the ~1,000 long-period EBs where even one event is detectable at high significance.
- Re-examine known Kepler CBP systems for a second, smaller transiting planet with the known planet's transits masked.

## Pitfalls

- Tertiary stellar eclipses and eclipse-depth changes from binary precession or starspots produce aperiodic dips; a 'candidate' must have an implied radius < 2 RJup from the fit AND the Villanova ETV/tertiary flags checked.
- Imperfect eclipse masking leaves residual dips at the binary period/harmonics that a stacking search will lock on to; require the events to be non-commensurate with P_bin and show the masked light curve.
- The STANLEY team's unpublished 13th planet: a candidate in a Windemuth-catalog EB may already be known privately; the claim must say 'candidate not in public tables' and flag Windemuth membership explicitly.
- Very low tractability: with ~14 known planets from 2878 EBs and automated surveys already run, a new detection is unlikely; do not relax any threshold to manufacture one.
- Two events are always reproduced by a circumbinary model with free period/phase/inclination: the main claim needs >= 3 events; two-event signals are the unvetted partial win only.

## Sources

- https://keplerebs.villanova.edu/
- https://vizier.cds.unistra.fr/viz-bin/asu-tsv?-source=J/AJ/151/68/catalog&-out.max=3
- https://exoplanetarchive.ipac.caltech.edu/bulk_data_download/
- https://exoplanetarchive.ipac.caltech.edu/TAP/sync?query=select+count(*)+as+n+from+pscomppars&format=csv
- https://arxiv.org/pdf/2101.03186
- https://www.arxiv.org/abs/2503.20900
- https://pypi.org/pypi/lightkurve/json
- https://pypi.org/pypi/transitleastsquares/json
- https://pypi.org/pypi/wotan/json
- https://pypi.org/pypi/triceratops/json
- https://pypi.org/pypi/astroquery/json
- https://vizier.cds.unistra.fr/viz-bin/asu-tsv?-source=J/MNRAS/455/4136&-out.max=2
- https://exoplanetarchive.ipac.caltech.edu/TAP/sync?query=select+pl_name,hostname,ra,dec,cb_flag+from+pscomppars&format=csv
- https://simbad.cds.unistra.fr/simbad/sim-tap/sync?REQUEST=doQuery&LANG=ADQL&FORMAT=csv&QUERY=select+main_id,otype,ra,dec+from+basic+where+contains(point('ICRS',ra,dec),circle('ICRS',289.0758,51.7572,0.001))=1
- Status source: https://keplerebs.villanova.edu/

## Citations

- [Problem page](../../../../.raw/V3R1T4S/known-unknowns/sky-archives/kepler-eb-circumbinary-transit-candidate.md)
- [Bank entry](../../../../.raw/V3R1T4S/bank/targets.json) (id `kepler-eb-circumbinary-transit-candidate`, commit `7dd4480`)

## Related Nodes

- [[V3R1T4S Sky archives]]
- [[V3R1T4S]]
