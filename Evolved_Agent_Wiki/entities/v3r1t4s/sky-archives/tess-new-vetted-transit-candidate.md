---
id: v3r1t4s-tess-new-vetted-transit-candidate
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
tractability: 3
compute: "laptop-hours (one sector of 2-min SPOC light curves is ~20,000 files / ~40 GB; keep any sub-sample under 200 GB, e.g. Tmag < 12 M dwarfs or a single sector; pip install lightkurve transitleastsquares wotan triceratops astroquery into a virtual environment first)"
disclosure: open
status_checked: "2026-10-08"
---
# New vetted transiting-planet candidate in public TESS light curves (not in TOI/CTOI/Archive)

# Overview

> Bank id `tess-new-vetted-transit-candidate` · harvest · tractability 3 · laptop-hours (one sector of 2-min SPOC light curves is ~20,000 files / ~40 GB; keep any sub-sample under 200 GB, e.g. Tmag < 12 M dwarfs or a single sector; pip install lightkurve transitleastsquares wotan triceratops astroquery into a virtual environment first) · disclosure **open**
> Bank says open as of 2026-10-08. Statuses go stale — re-check the primary source before any work.

## Statement

Find a periodic transit signal in public TESS 2-min/20-s SPOC light curves or SPOC/QLP FFI light curves (MAST) whose host (TIC id, and any star within 3 arcsec) is absent from the live ExoFOP TOI and CTOI tables and from the NASA Exoplanet Archive toi/pscomppars tables, and that passes a fixed vetting suite: TLS/BLS detection with injection-recovery-calibrated significance, odd/even depth agreement, no secondary eclipse, in-transit centroid shift consistent with zero at pixel level (TESScut), TRICERATOPS FPP < 0.5 and NFPP < 0.1 ('likely planet' tier of Giacalone+2021), and no ephemeris match to any known EB (TESS-EBs HLSP, VSX) within 1 TESS pixel (21 arcsec). An agent may only claim 'new vetted candidate', never 'planet'. Only PERIODIC signals with >= 3 individual transit events in the analysed data qualify here; single or double events belong to kepler-tess-single-transit-long-period-candidate. Absence checks are done by downloading whole ra/dec/id/ephemeris column lists with plain TAP/CSV requests (e.g. select+pl_name,hostname,ra,dec,cb_flag+from+pscomppars) and cross-matching LOCALLY; ADQL cone functions (contains/point/circle) in the Exoplanet Archive URL trigger a Cloudflare block and must not be used or retried. SIMBAD TAP cone queries are fine.

## Success criterion

A saved bundle {TIC id, Gaia DR3 id, sector list, raw light-curve file URIs, detrended light curve, period/epoch/duration/depth, TLS result, odd-even and secondary-eclipse statistics, per-pixel/centroid test output, TRICERATOPS FPP+NFPP with the exact input files, injection-recovery completeness curve, null-test numbers, and every catalog file used for the absence checks with its download timestamp} such that: (1) ABSENCE, all re-fetched live immediately before claiming: the TIC id and every Gaia DR3 source within 3 arcsec are absent from the ExoFOP TOI CSV (https://exofop.ipac.caltech.edu/tess/download_toi.php?sort=toi&output=csv, including its 'Previous CTOI' column) and CTOI CSV (https://exofop.ipac.caltech.edu/tess/download_ctoi.php?sort=ctoi&output=csv, which carries Planet Hunters TESS and other community submissions), and from the Exoplanet Archive toi, pscomppars, k2pandc and cumulative tables (plain column downloads via TAP, matched locally by id and by 3-arcsec position); no entry of those tables, of the TESS-EBs HLSP, of Gaia DR3 vari_eclipsing_binary, or of VSX (api.list cone) within 2 arcmin shares the ephemeris (period within 0.1% or an exact 2x/0.5x alias AND epoch within 0.05 d modulo the period); a SIMBAD TAP cone of 3 arcsec on the host returns no object whose otype is a planet or planet candidate (Pl, Pl?) or an eclipsing binary (EB*, EB?), which catches literature candidates that the Archive tables ingest with a lag; and the signal does not match (same 2-arcmin + ephemeris rule) any SPOC TCE in the MAST tcestats lists (https://archive.stsci.edu/missions/tess/catalogs/tce/) - a TCE match is logged as the partial win tess-rediscovered-tce, never as new; (2) >= 3 individual transit events with the dip visible in the target aperture at each; (3) odd/even depth difference < 3 sigma; (4) secondary eclipse at phase 0.5 < 3 sigma and the depth is inconsistent with an EB at the TIC stellar radius; (5) TRICERATOPS FPP < 0.5 and NFPP < 0.1 (also report whether FPP < 0.015 and NFPP < 0.001, the validation tier, but validation is NOT claimed); (6) the signal is recovered in > 90% of >= 100 injections of the same depth/period/duration into the same light curve through the same detrending; (7) the centroid/pixel-level (TESScut difference-image) test shows the dip on the target; (8) null test: the identical search pipeline run on the flux-inverted light curve and on 20 phase-scrambled copies (transit windows shuffled) returns a maximum SDE/significance below the injection-calibrated detection threshold and below the claimed signal; the numbers are saved in the bundle; (9) the host star id (TIC/KIC/EPIC/Gaia DR3) is not the host of any already-claimed (a confirmed result listed in this repository's RESULTS.md) claim under any other astronomy target of this bank, so the same signal is never counted twice across tess-new-vetted-transit-candidate / kepler-k2-new-vetted-transit-candidate / kepler-tess-single-transit-long-period-candidate / kepler-eb-circumbinary-transit-candidate. Claims are 'new vetted candidate' only, never 'planet'.

## Partial wins

- {"id": "tess-reproduce-known-toi", "statement": "Pipeline re-detects, from raw MAST light curves alone, at least 20 randomly chosen known TOIs with TFOPWG disposition PC/CP/KP (period within 0.1% and depth within 20%) and correctly rejects at least 10 TOIs with disposition FP (EB/NEB), with the confusion matrix saved; this is the calibration gate for any new claim."}
- {"id": "tess-new-candidate-no-triceratops", "statement": "A signal passing items (1)-(3),(5),(6) of the success criterion with TRICERATOPS either not run or 0.5 <= FPP < 0.9: an 'unvetted new candidate', logged with all artifacts, explicitly NOT claimed as vetted."}
- {"id": "tess-injection-recovery-map", "statement": "A per-target injection-recovery completeness map (period x depth grid, >= 400 injections) for a defined sample of >= 200 light curves, published as a CSV, showing the detection threshold of the pipeline; non-trivial because it sets the floor for all later claims."}
- {"id": "tess-rediscovered-tce", "statement": "A signal passing (2)-(8) whose only catalog match is a SPOC/QLP TCE that never became a TOI/CTOI: logged as 'rediscovered TCE, independently vetted' with the TCE id; not claimed as new."}

## Verification

Skeptic re-downloads the named light-curve files from MAST (URIs in the bundle), re-runs the saved detrending + TLS script at the claimed period (minutes), recomputes odd/even and secondary statistics from the saved phase-folded data, re-runs TRICERATOPS from the saved input files (tens of minutes with the saved star list), and re-fetches the TOI CSV, CTOI CSV and Archive TAP tables to confirm absence by TIC id and by a 3-arcsec cone match on the TIC RA/Dec. All under one hour on this Mac. The skeptic also re-runs the SIMBAD cone, the TCE-list match and the null test from the saved files. No ADQL cone functions are sent to the Exoplanet Archive.

## Angles

- Search where the official pipelines are weakest: FFI-only targets with Tmag 12-14 in the QLP/SPOC-FFI HLSPs, single-sector M dwarfs, and targets near the TESS pixel-saturation limit, which the TOI process under-samples.
- Multi-sector stitching of the 2-min light curves of a star observed in >= 10 sectors (continuous viewing zones) to reach depths ~200 ppm that single-sector searches miss; use wotan biweight with window = 3x the max duration.
- Second-planet search: mask the known TOI transits in multi-TOI systems and re-run TLS on the residuals (TOI systems with one known candidate are the highest-prior place for an unlisted second one).
- Build the vetting suite as a reusable CLI that takes a TIC id and period and emits the full bundle, then calibrate it on the ExoFOP CSV (PC vs FP dispositions) before searching.
- Use the ExoFOP 'TESS Disposition'/'TFOPWG Disposition' columns to build the negative training set (NEB/EB/BEB) for the pipeline's rejection stage.

## Pitfalls

- A TCE or signal that is merely 'not yet a TOI' is not new if it already appears in the TOI, CTOI, KOI, K2 or Exoplanet Archive tables under any TIC/KIC/EPIC alias: cross-match by coordinates (3 arcsec) AND by TIC/KIC/EPIC/Gaia DR3 id, not by name alone.
- Momentum-dump / scattered-light / reaction-wheel artifacts in TESS (every ~3-4 d at orbit perigee, sector edges) mimic single transits; require the dip to be absent in the background flux and present in the target aperture only.
- Nearby eclipsing binaries diluted into the aperture produce flat-bottomed, equal-depth transits that pass odd/even: the centroid test and TRICERATOPS nearby-star scenarios (NFPP) are mandatory, not optional.
- Detrending with too short a window (wotan/biweight < 3x transit duration) injects or erases shallow transits; the injection-recovery step must use the same detrending as the search.
- Bootstrapped 'SDE > 7' from TLS/BLS is not a significance: compute the false-alarm level from transit-shaped injections on the same light curve with the same pipeline.
- ExoFOP TOI and CTOI tables are updated in batches (the Archive toi table shows latest toi_created 2026-08-27 and rowupdate 2026-10-01): a signal found today could already be queued; the claim must be re-checked against the live CSVs immediately before claiming, and any TIC that appears as a 'Previous CTOI' is not new.
- Exoplanet Archive TAP URLs containing contains(point(...),circle(...)) are blocked by Cloudflare (seen 2026-10-08): download the ra/dec columns and match locally; never retry through a 403.
- A SPOC TCE that the TOI team never promoted is NOT a new candidate: the MAST tcestats lists (132 sector files) must be matched by position and ephemeris.
- Single and double transit events are out of scope here (they belong to the single-transit target); do not phase-fold two events and call the result periodic.

## Sources

- https://archive.stsci.edu/tess/bulk_downloads/bulk_downloads_ffi-tp-lc-dv.html
- https://archive.stsci.edu/missions/tess/download_scripts/sector/tesscurl_sector_1_lc.sh
- https://archive.stsci.edu/hlsp/qlp
- https://archive.stsci.edu/hlsp/tess-spoc
- https://mast.stsci.edu/tesscut/api/v0.1/sector?ra=84.291188&dec=-80.469119
- https://exofop.ipac.caltech.edu/tess/download_toi.php?sort=toi&output=csv
- https://exofop.ipac.caltech.edu/tess/download_ctoi.php?sort=ctoi&output=csv
- https://exoplanetarchive.ipac.caltech.edu/TAP/sync?query=select+count(*)+as+n+from+toi&format=csv
- https://exoplanetarchive.ipac.caltech.edu/TAP/sync?query=select+count(*)+as+n+from+pscomppars&format=csv
- https://archive.stsci.edu/hlsps/tess-ebs/hlsp_tess-ebs_tess_lcf-ffi_s0001-s0026_tess_v1.0_cat.csv
- https://github.com/stevengiacalone/triceratops
- https://pypi.org/pypi/lightkurve/json
- https://pypi.org/pypi/transitleastsquares/json
- https://pypi.org/pypi/wotan/json
- https://pypi.org/pypi/triceratops/json
- https://pypi.org/pypi/astroquery/json
- https://archive.stsci.edu/missions/tess/catalogs/tce/
- https://gea.esac.esa.int/tap-server/tap/sync?REQUEST=doQuery&LANG=ADQL&FORMAT=csv&QUERY=select+count(*)+from+gaiadr3.vari_eclipsing_binary
- https://simbad.cds.unistra.fr/simbad/sim-tap/sync?REQUEST=doQuery&LANG=ADQL&FORMAT=csv&QUERY=select+main_id,otype,ra,dec+from+basic+where+contains(point('ICRS',ra,dec),circle('ICRS',289.0758,51.7572,0.001))=1
- https://exoplanetarchive.ipac.caltech.edu/TAP/sync?query=select+pl_name,hostname,ra,dec,cb_flag+from+pscomppars&format=csv
- https://vsx.aavso.org/index.php?view=api.list&ra=291.0&dec=42.5&radius=0.1&format=json
- Status source: https://archive.stsci.edu/tess/bulk_downloads/bulk_downloads_ffi-tp-lc-dv.html

## Citations

- [Problem page](../../../../.raw/V3R1T4S/known-unknowns/sky-archives/tess-new-vetted-transit-candidate.md)
- [Bank entry](../../../../.raw/V3R1T4S/bank/targets.json) (id `tess-new-vetted-transit-candidate`, commit `7dd4480`)

## Related Nodes

- [[V3R1T4S Sky archives]]
- [[V3R1T4S]]
