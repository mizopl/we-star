---
id: v3r1t4s-kepler-tess-single-transit-long-period-candidate
type: entity
tags: [v3r1t4s, v3r1t4s/sky-archives, kind/harvest]
inbound_links: 1
confidence: 0.8
last_ingested_sources: [".raw/V3R1T4S/bank/targets.json@7dd4480"]
status: "open"
priority: ""
notes: ""
category: sky-archives
kind: harvest
tractability: 2.5
compute: "laptop-hours (single-event search is cheap; the cost is downloading: use the tesscurl sector scripts for a defined bright sub-sample or Kepler PDCSAP for Teff < 6000 K dwarfs, well under 200 GB)"
disclosure: open
status_checked: "2026-10-08"
---
# New single-/duo-transit long-period candidate in Kepler or TESS light curves

# Overview

> Bank id `kepler-tess-single-transit-long-period-candidate` · harvest · tractability 2.5 · laptop-hours (single-event search is cheap; the cost is downloading: use the tesscurl sector scripts for a defined bright sub-sample or Kepler PDCSAP for Teff < 6000 K dwarfs, well under 200 GB) · disclosure **open**
> Bank says open as of 2026-10-08. Statuses go stale — re-check the primary source before any work.

## Statement

Find a single or double transit-like event (<= 2 events in all available data; duration >= 5 h; depth consistent with Rp < 2 RJup at the Gaia DR3 stellar radius, implying P > ~100 d) in public Kepler or TESS light curves of a star that is not a Villanova Kepler EB, that is not in the TOI/CTOI/KOI/TCE/k2pandc/pscomppars tables, not in the Kawahara & Masuda 2019 Kepler snow-line table (VizieR J/AJ/157/218), not among the Foreman-Mackey+2016 (arXiv:1607.08237) / Herman+2019 (arXiv:1901.01974, 18 KICs) Kepler long-period candidates, not among the four Kepler >342 d candidates of arXiv:2608.23425 (Aug 2026), not among the 85 TESS duotransits of Hawthorn+2024 (arXiv:2310.17268; all non-TOI ones were submitted as CTOIs) and not among the 88 TESS single-transit candidates of Salinas+2025 (arXiv:2502.07542). Must survive: single-event shape fit (limb-darkened transit vs. box vs. Gaussian, transit model preferred by delta-BIC > 10), no momentum-dump / sector-edge / scattered-light coincidence, pixel-level centroid test, no matching EB ephemeris within 2 arcmin, and an ingress/egress duration consistent with the stellar density. Absence checks are done by downloading whole ra/dec/id/ephemeris column lists with plain TAP/CSV requests (e.g. select+pl_name,hostname,ra,dec,cb_flag+from+pscomppars) and cross-matching LOCALLY; ADQL cone functions (contains/point/circle) in the Exoplanet Archive URL trigger a Cloudflare block and must not be used or retried. SIMBAD TAP cone queries are fine.

## Success criterion

A saved bundle {star id, Gaia DR3 id, light-curve file URIs, event epoch(s), duration, depth, transit-model vs box vs Gaussian fits with delta-BIC, per-pixel in/out-of-event difference image, momentum-dump/quality-flag timeline around the event, stellar density from Gaia DR3 vs density implied by the fit, (for duo-transits) the list of allowed period aliases, null-test numbers, and the literature exclusion lists as machine-extracted id lists with their source URLs} such that: (1) ABSENCE, re-fetched live immediately before claiming: the host id and all Gaia DR3 sources within 3 arcsec are absent from the ExoFOP TOI/CTOI CSVs and the Archive toi/cumulative/q1_q17_dr25_tce/k2pandc/pscomppars tables (plain column downloads matched locally), from VizieR J/AJ/157/218 (KIC match), from the KIC lists extracted from the ar5iv/arXiv HTML of 1607.08237 and 1901.01974 and the four candidates named in arXiv:2608.23425, from the TIC lists extracted from arXiv:2310.17268 (Table A1) and arXiv:2502.07542, and from the Villanova EB catalog (J/AJ/151/68); a SIMBAD TAP cone of 3 arcsec on the host returns no object whose otype is a planet or planet candidate (Pl, Pl?) or an eclipsing binary (EB*, EB?), which catches literature candidates that the Archive tables ingest with a lag; (2) <= 2 events in all public data for the star (a third event makes it a periodic candidate for the TESS or Kepler/K2 target instead); (3) transit model preferred by delta-BIC > 10 over both alternatives; (4) event not within 0.5 d of a momentum dump, safe mode or sector/quarter boundary, and no flux drop of similar depth in the background or in neighbouring apertures; (5) difference-image centroid on target; (6) implied Rp < 2 RJup and fitted density within 3x of the Gaia DR3 stellar density; (7) null test: the same single-event detector run on the flux-inverted light curve returns zero events passing (3)-(6); (8) the host star id (TIC/KIC/EPIC/Gaia DR3) is not the host of any already-claimed (a confirmed result listed in this repository's RESULTS.md) claim under any other astronomy target of this bank, so the same signal is never counted twice across tess-new-vetted-transit-candidate / kepler-k2-new-vetted-transit-candidate / kepler-tess-single-transit-long-period-candidate / kepler-eb-circumbinary-transit-candidate. Claim is 'new single-transit candidate'.

## Partial wins

- {"id": "single-transit-reproduce-known", "statement": "The pipeline recovers, from raw MAST data, at least 10 of the Kawahara+2019 or Foreman-Mackey+2016 Kepler single-transit events (epoch within 0.05 d, depth within 20%) and at least 5 TESS duotransit candidates from Hawthorn+2024 that later became TOIs; results saved as a table."}
- {"id": "single-transit-period-alias-resolution", "statement": "For a known duo-transit TOI/CTOI with an ambiguous period, a new period determination (set of allowed aliases reduced by >= 50%) using additional public TESS sectors released since the candidate's listing, with the ephemeris and the sector data cited; checkable by re-folding."}
- {"id": "single-transit-unvetted", "statement": "An event passing absence, shape and quality-flag tests but with an inconclusive pixel-level test: logged as unvetted, not claimed."}

## Verification

Skeptic re-downloads the named light-curve and target-pixel files, re-fits the single event with the saved model code at the saved epoch (minutes), checks the quality flags and dump times from the FITS headers, reproduces the difference image, and re-runs the TAP/CSV absence checks plus a VizieR query on J/AJ/157/218. Under one hour. Also re-extracts the KIC/TIC exclusion lists from the saved arXiv HTML and re-runs the SIMBAD cone and the inverted-light-curve null test.

## Angles

- TESS continuous-viewing-zone stars with 20+ sectors: duo- and tri-transits with P = 100-400 d now exist in the public data but the SPOC/QLP searches require >= 2 transits per sector-pair run, so many remain unlisted.
- Kepler stars with 1-2 transits whose depth was below the Foreman-Mackey+2016 threshold (they searched only ~40,000 bright Sun-like stars): extend to Kp 15-16 and to M dwarfs.
- Systems with a known inner KOI/TOI showing TTVs (arXiv:2608.23425 found its four candidates exactly there): mask the inner transits and run the single-event search on the residuals.
- Use the stellar density consistency (Gaia DR3 radius + mass) as a built-in false-positive filter: an event whose duration implies a density off by > 3x is an EB or blend.
- For every TESS single-transit candidate, query all later public sectors for a second event to turn a mono into a duo (period aliases).

## Pitfalls

- Single dips coincident with TESS momentum dumps, orbit perigee ramps, Earth/Moon scattered light, or Kepler safe-mode/coarse-point recoveries are the dominant false positive; the quality-flag timeline must be in the bundle and the dip must not be present in the background pixels.
- Long-period single transits from grazing EBs are V-shaped: a V-shaped single event with implied Rp > 2 RJup or a duration inconsistent with the Gaia DR3 stellar density is not a candidate.
- Secular trends from starspots or flares (M dwarfs) detrended badly produce fake 'transits'; the bundle must show the raw and detrended curves and the detrending must be re-run by the skeptic.
- Kawahara & Masuda 2019 (VizieR J/AJ/157/218), Foreman-Mackey+2016 (1607.08237), Herman+2019 (1901.01974), Hawthorn+2024 (85 duotransits, 2310.17268), Salinas+2025 (88 single transits, 2502.07542) and arXiv:2608.23425 already list hundreds of events: matching by KIC/TIC id AND by epoch is mandatory; a known event re-found with a different detrending is not new.
- Exoplanet Archive TAP URLs containing contains(point(...),circle(...)) are blocked by Cloudflare (seen 2026-10-08): download the ra/dec columns and match locally; never retry through a 403.

## Sources

- https://archive.stsci.edu/tess/bulk_downloads/bulk_downloads_ffi-tp-lc-dv.html
- https://archive.stsci.edu/missions/tess/download_scripts/sector/tesscurl_sector_1_lc.sh
- https://archive.stsci.edu/hlsp/qlp
- https://archive.stsci.edu/hlsp/tess-spoc
- https://mast.stsci.edu/tesscut/api/v0.1/sector?ra=84.291188&dec=-80.469119
- https://exoplanetarchive.ipac.caltech.edu/bulk_data_download/
- https://vizier.cds.unistra.fr/viz-bin/asu-tsv?-source=J/AJ/157/218&-out.max=2
- https://exofop.ipac.caltech.edu/tess/download_toi.php?sort=toi&output=csv
- https://exofop.ipac.caltech.edu/tess/download_ctoi.php?sort=ctoi&output=csv
- https://exoplanetarchive.ipac.caltech.edu/TAP/sync?query=select+count(*)+as+n+from+toi&format=csv
- https://exoplanetarchive.ipac.caltech.edu/TAP/sync?query=select+count(*)+as+n+from+cumulative&format=csv
- https://exoplanetarchive.ipac.caltech.edu/TAP/sync?query=select+count(*)+as+n+from+q1_q17_dr25_tce&format=csv
- https://exoplanetarchive.ipac.caltech.edu/TAP/sync?query=select+count(*)+as+n+from+k2pandc&format=csv
- https://exoplanetarchive.ipac.caltech.edu/TAP/sync?query=select+count(*)+as+n+from+pscomppars&format=csv
- https://arxiv.org/abs/2608.23425
- https://arxiv.org/pdf/2310.17268
- https://pypi.org/pypi/lightkurve/json
- https://pypi.org/pypi/transitleastsquares/json
- https://pypi.org/pypi/wotan/json
- https://pypi.org/pypi/triceratops/json
- https://pypi.org/pypi/astroquery/json
- https://ar5iv.labs.arxiv.org/html/1607.08237
- https://ar5iv.labs.arxiv.org/html/1901.01974
- https://arxiv.org/abs/2502.07542
- https://simbad.cds.unistra.fr/simbad/sim-tap/sync?REQUEST=doQuery&LANG=ADQL&FORMAT=csv&QUERY=select+main_id,otype,ra,dec+from+basic+where+contains(point('ICRS',ra,dec),circle('ICRS',289.0758,51.7572,0.001))=1
- https://exoplanetarchive.ipac.caltech.edu/TAP/sync?query=select+pl_name,hostname,ra,dec,cb_flag+from+pscomppars&format=csv
- https://vizier.cds.unistra.fr/viz-bin/asu-tsv?-source=J/AJ/151/68/catalog&-out.max=3
- Status source: https://archive.stsci.edu/tess/bulk_downloads/bulk_downloads_ffi-tp-lc-dv.html

## Citations

- [Problem page](../../../../.raw/V3R1T4S/known-unknowns/sky-archives/kepler-tess-single-transit-long-period-candidate.md)
- [Bank entry](../../../../.raw/V3R1T4S/bank/targets.json) (id `kepler-tess-single-transit-long-period-candidate`, commit `7dd4480`)

## Related Nodes

- [[V3R1T4S Sky archives]]
- [[V3R1T4S]]
