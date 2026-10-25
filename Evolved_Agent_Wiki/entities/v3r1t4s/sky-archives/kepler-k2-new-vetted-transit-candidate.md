---
id: v3r1t4s-kepler-k2-new-vetted-transit-candidate
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
compute: "laptop-hours (do NOT fetch the full Kepler or K2 light-curve sets; restrict to a defined sub-sample under 200 GB, e.g. one K2 campaign (~20k targets, ~10 GB) or Kepler M dwarfs; pip install lightkurve transitleastsquares wotan triceratops astroquery)"
disclosure: open
status_checked: "2026-10-08"
---
# New vetted transit candidate in archival Kepler or K2 light curves (not in KOI/K2 candidate tables)

# Overview

> Bank id `kepler-k2-new-vetted-transit-candidate` · harvest · tractability 3 · laptop-hours (do NOT fetch the full Kepler or K2 light-curve sets; restrict to a defined sub-sample under 200 GB, e.g. one K2 campaign (~20k targets, ~10 GB) or Kepler M dwarfs; pip install lightkurve transitleastsquares wotan triceratops astroquery) · disclosure **open**
> Bank says open as of 2026-10-08. Statuses go stale — re-check the primary source before any work.

## Statement

Re-search public Kepler (Q1-Q17 DR25 PDCSAP) or K2 (campaigns 0-19) light curves at MAST with a modern detrending + TLS pipeline for a periodic transit whose host (KIC/EPIC and any Gaia DR3 source within 3 arcsec) is absent from the NASA Exoplanet Archive KOI cumulative table, the Q1-Q17 DR25 TCE table, the K2 planets-and-candidates table (k2pandc) and pscomppars, and from the TOI/CTOI tables for the same sky position; the candidate must pass the same vetting suite as the TESS target (odd/even, secondary, pixel-level centroid using the Kepler target pixel files, TRICERATOPS FPP < 0.5 / NFPP < 0.1, injection-recovery). Recent surveys (TFAW K2 reanalysis: 24 previously unpublished candidates; K2-OjOS) show the archive still contains unlisted candidates. Claims are 'new vetted candidate' only. Only PERIODIC signals with >= 3 transit events qualify; the host must not be a Villanova Kepler EB (those belong to kepler-eb-circumbinary-transit-candidate). Absence checks are done by downloading whole ra/dec/id/ephemeris column lists with plain TAP/CSV requests (e.g. select+pl_name,hostname,ra,dec,cb_flag+from+pscomppars) and cross-matching LOCALLY; ADQL cone functions (contains/point/circle) in the Exoplanet Archive URL trigger a Cloudflare block and must not be used or retried. SIMBAD TAP cone queries are fine.

## Success criterion

A saved bundle (as in tess-new-vetted-transit-candidate, with KIC/EPIC id, Gaia DR3 id, quarter/campaign list, MAST file URIs, null-test numbers and every catalog file used with its download timestamp) such that: (1) ABSENCE, re-fetched live immediately before claiming: the host id and every Gaia DR3 source within 3 arcsec are absent from the Archive cumulative, q1_q17_dr25_tce, k2pandc, pscomppars and toi tables (plain column downloads, matched locally by id and 3-arcsec position; a DR25 TCE with period within 0.1% and epoch within 0.05 d modulo the period counts as the same signal) and from the ExoFOP TOI/CTOI CSVs by position; a SIMBAD TAP cone of 3 arcsec on the host returns no object whose otype is a planet or planet candidate (Pl, Pl?) or an eclipsing binary (EB*, EB?), which catches literature candidates that the Archive tables ingest with a lag; a VizieR all-catalogue position search (https://vizier.cds.unistra.fr/viz-bin/asu-tsv?-c=<RA>+<DEC>&-c.rs=3&-source=) is saved and shows no planet/candidate catalogue entry for the host; the KIC is not in the Villanova EB catalog (VizieR J/AJ/151/68); (2) >= 3 individual transit events; (3) odd/even < 3 sigma; (4) secondary < 3 sigma; (5) pixel-level test on the target pixel file shows the dip on the target; (6) TRICERATOPS FPP < 0.5 and NFPP < 0.1 (report the validation tier but do not claim it); (7) injection-recovery > 90% at the claimed depth/period through the same detrending; (8) null test: the identical search pipeline run on the flux-inverted light curve and on 20 phase-scrambled copies (transit windows shuffled) returns a maximum SDE/significance below the injection-calibrated detection threshold and below the claimed signal; the numbers are saved in the bundle; (9) for K2 the signal survives both a K2SFF/EVEREST-style systematics correction and a self-flat-field re-derivation (two independent detrendings); (10) the host star id (TIC/KIC/EPIC/Gaia DR3) is not the host of any already-claimed (a confirmed result listed in this repository's RESULTS.md) claim under any other astronomy target of this bank, so the same signal is never counted twice across tess-new-vetted-transit-candidate / kepler-k2-new-vetted-transit-candidate / kepler-tess-single-transit-long-period-candidate / kepler-eb-circumbinary-transit-candidate. Claims are 'new vetted candidate' only.

## Partial wins

- {"id": "kepler-k2-reproduce-tfaw", "statement": "Pipeline independently recovers, from MAST light curves alone, at least 10 of the TFAW-survey K2 candidates (period within 0.1%) and at least 20 KOI CANDIDATEs with koi_score > 0.9, plus rejects at least 10 koi_disposition FALSE POSITIVE KOIs flagged as EB; confusion matrix saved. Calibration gate."}
- {"id": "kepler-k2-second-candidate-in-known-system", "statement": "An additional transit candidate (not in the Archive tables) in a system already hosting a KOI/K2 candidate, found after masking the known transits, passing all vetting steps; checkable exactly like the main criterion but with higher prior."}
- {"id": "kepler-k2-unvetted-candidate", "statement": "A signal passing absence + odd/even + secondary + injection-recovery but with TRICERATOPS 0.5 <= FPP < 0.9 or pixel test inconclusive: logged as 'unvetted', never claimed."}

## Verification

Skeptic re-downloads the named light-curve / target-pixel files from MAST, re-runs the saved detrending + TLS at the claimed period, recomputes the odd/even, secondary, and pixel-level statistics from saved inputs, re-runs TRICERATOPS from the saved star list, and re-runs the four Archive TAP absence queries plus a 3-arcsec cone on the KIC/EPIC coordinates. Under one hour. Also re-runs the SIMBAD cone, the VizieR position search and the null test from saved files; no ADQL cone functions to the Archive.

## Angles

- K2 campaigns with the worst roll systematics (C0, C1, C10, C11) and overlapping campaigns (C5/C16/C18) where a two-campaign stitch doubles the baseline; K2-OjOS and TFAW found new candidates exactly there.
- Kepler stars with koi_score between 0.1 and 0.5 or TCEs that failed the Robovetter on a single metric (e.g. 'model-shift' only): re-vet with the modern suite; the DR25 TCE table lists them.
- Residual search in known KOI multi systems after masking all listed transits (stacking 4 years at a fixed trial period reaches ~100 ppm).
- Low-mass hosts (Teff < 4000 K from the KIC/Gaia DR3) where the Kepler pipeline's stellar-radius priors were worst and the transit depth of small planets is largest.
- Use the DR25 injected-planet completeness products as an external check on the pipeline's own injection-recovery.

## Pitfalls

- A TCE or signal that is merely 'not yet a TOI' is not new if it already appears in the TOI, CTOI, KOI, K2 or Exoplanet Archive tables under any TIC/KIC/EPIC alias: cross-match by coordinates (3 arcsec) AND by TIC/KIC/EPIC/Gaia DR3 id, not by name alone.
- Momentum-dump / scattered-light / reaction-wheel artifacts in TESS (every ~3-4 d at orbit perigee, sector edges) mimic single transits; require the dip to be absent in the background flux and present in the target aperture only.
- Nearby eclipsing binaries diluted into the aperture produce flat-bottomed, equal-depth transits that pass odd/even: the centroid test and TRICERATOPS nearby-star scenarios (NFPP) are mandatory, not optional.
- Detrending with too short a window (wotan/biweight < 3x transit duration) injects or erases shallow transits; the injection-recovery step must use the same detrending as the search.
- Bootstrapped 'SDE > 7' from TLS/BLS is not a significance: compute the false-alarm level from transit-shaped injections on the same light curve with the same pipeline.
- The DR25 TCE table contains ~34,000 threshold-crossing events; a signal present there is NOT new even if it never became a KOI - the absence check must include q1_q17_dr25_tce, and a match in period (within 0.1%) and epoch counts as the same signal.
- K2 'candidates' in the literature (TFAW, K2-OjOS, Kruse 2019, Zink 2021) may be absent from k2pandc with a lag; a literature search by EPIC id (ADS/arXiv) is required in addition to the table check.
- Exoplanet Archive TAP URLs containing contains(point(...),circle(...)) are blocked by Cloudflare (seen 2026-10-08): download the ra/dec columns and match locally; never retry through a 403.
- K2 literature candidates (TFAW thesis at diposit.ub.edu, K2-OjOS, Kruse 2019, Zink 2021) are checked mechanically through SIMBAD otype Pl?/Pl and the VizieR position search, not by reading papers; an entry in either is not new.

## Sources

- https://exoplanetarchive.ipac.caltech.edu/bulk_data_download/
- https://exoplanetarchive.ipac.caltech.edu/TAP/sync?query=select+count(*)+as+n+from+cumulative&format=csv
- https://exoplanetarchive.ipac.caltech.edu/TAP/sync?query=select+count(*)+as+n+from+k2pandc&format=csv
- https://exoplanetarchive.ipac.caltech.edu/TAP/sync?query=select+count(*)+as+n+from+q1_q17_dr25_tce&format=csv
- https://exoplanetarchive.ipac.caltech.edu/TAP/sync?query=select+count(*)+as+n+from+pscomppars&format=csv
- https://exofop.ipac.caltech.edu/tess/download_toi.php?sort=toi&output=csv
- https://exofop.ipac.caltech.edu/tess/download_ctoi.php?sort=ctoi&output=csv
- https://archive.stsci.edu/kepler/koi/search.php
- https://github.com/stevengiacalone/triceratops
- https://pypi.org/pypi/lightkurve/json
- https://pypi.org/pypi/transitleastsquares/json
- https://pypi.org/pypi/wotan/json
- https://pypi.org/pypi/triceratops/json
- https://pypi.org/pypi/astroquery/json
- https://simbad.cds.unistra.fr/simbad/sim-tap/sync?REQUEST=doQuery&LANG=ADQL&FORMAT=csv&QUERY=select+main_id,otype,ra,dec+from+basic+where+contains(point('ICRS',ra,dec),circle('ICRS',289.0758,51.7572,0.001))=1
- https://exoplanetarchive.ipac.caltech.edu/TAP/sync?query=select+pl_name,hostname,ra,dec,cb_flag+from+pscomppars&format=csv
- https://vizier.cds.unistra.fr/viz-bin/asu-tsv?-source=J/AJ/151/68/catalog&-out.max=3
- Status source: https://exoplanetarchive.ipac.caltech.edu/bulk_data_download/

## Citations

- [Problem page](../../../../.raw/V3R1T4S/known-unknowns/sky-archives/kepler-k2-new-vetted-transit-candidate.md)
- [Bank entry](../../../../.raw/V3R1T4S/bank/targets.json) (id `kepler-k2-new-vetted-transit-candidate`, commit `7dd4480`)

## Related Nodes

- [[V3R1T4S Sky archives]]
- [[V3R1T4S]]
