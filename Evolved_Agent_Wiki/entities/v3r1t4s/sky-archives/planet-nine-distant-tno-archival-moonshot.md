---
id: v3r1t4s-planet-nine-distant-tno-archival-moonshot
type: entity
tags: [v3r1t4s, v3r1t4s/sky-archives, kind/moonshot]
inbound_links: 1
confidence: 0.8
last_ingested_sources: [".raw/V3R1T4S/bank/targets.json@7dd4480"]
status: "open"
priority: ""
notes: ""
category: sky-archives
kind: moonshot
tractability: 1
compute: "laptop-hours to laptop-days (DECam frames are ~0.5-1 GB each; restrict to < 200 GB by selecting fields with >= 3 public epochs in the predicted Planet Nine region or ecliptic-latitude bands; shift-and-stack on 10 cores is feasible for a few square degrees per day)"
disclosure: open
status_checked: "2026-10-08"
---
# MOONSHOT - Planet Nine or a new extreme distant TNO candidate in public archival survey images

# Overview

> Bank id `planet-nine-distant-tno-archival-moonshot` · moonshot · tractability 1 · laptop-hours to laptop-days (DECam frames are ~0.5-1 GB each; restrict to < 200 GB by selecting fields with >= 3 public epochs in the predicted Planet Nine region or ecliptic-latitude bands; shift-and-stack on 10 cores is feasible for a few square degrees per day) · disclosure **open**
> Bank says open as of 2026-10-08. Statuses go stale — re-check the primary source before any work.

## Statement

Detect in public archival imaging (DECam frames via the NOIRLab SIA service, Pan-STARRS1 3pi cutouts, ZTF science images; optionally the IRAS/AKARI far-IR route of arXiv:2504.17288 / 2506.12854) a slow-moving source (< ~1 arcmin/yr for Planet Nine at 400-800 au; < 4 arcsec/hr for a > 100 au object) linked across >= 3 epochs on >= 2 nights with a bound heliocentric orbit fit (r > 100 au), that is absent from the MPC Distant.txt / TNO list / MPCORB.DAT and from JPL SBDB. Pan-STARRS1 DR2 (Brown & Batygin 2024), ZTF and DES have already excluded ~78% of the Brown & Batygin 2021 Planet Nine parameter space to V ~ 21.5, and Rubin LSST formally began its 10-year survey on 2026-06-29/30 (alerts since late Feb 2026), so this is a long-odds search of remaining faint/high-latitude/galactic-plane regions. No MPC submission is made; the claim is 'linked moving-object candidate not in any public orbit catalog'. Any 'new object' claim (main or partial) also requires absence from the MPC NEOCP/PCCP pages and from the MPC Isolated Tracklet File (itf.txt.gz, ~130 MB, refreshed daily) within 30 arcsec of each epoch position.

## Success criterion

A saved bundle {all frame identifiers and download URLs, cutouts at each epoch, source centroids with uncertainties, the linking solution (motion vector), a heliocentric orbit fit (saved code) with residuals < 0.5 arcsec, the implied r, a, e, i, and static-sky and known-object checks} such that: >= 3 detections on >= 2 distinct nights, consistent with a single bound orbit with r > 100 au, each detection > 5 sigma with no static source at that position in other-epoch frames or Gaia DR3/PS1 catalogs within 2 arcsec, no object within 30 arcsec of any epoch position in a SkyBoT cone search at that epoch, absence of any ITF tracklet (https://www.minorplanetcenter.net/iau/ITF/itf.txt.gz) and NEOCP/PCCP object within 30 arcsec of each epoch position, and absence from https://minorplanetcenter.net/iau/MPCORB/Distant.txt, https://minorplanetcenter.net/iau/lists/TNOs.html, https://minorplanetcenter.net/iau/MPCORB/MPCORB.DAT and JPL SBDB (all re-fetched live immediately before claiming). An agent may only claim 'candidate'; 'Planet Nine' is never claimed. Additionally the object (any epoch position within 30 arcsec) is not the subject of any already-claimed (a confirmed result listed in this repository's RESULTS.md) claim under any other astronomy target of this bank, so the same signal is never counted twice across tess-new-vetted-transit-candidate / kepler-k2-new-vetted-transit-candidate / kepler-tess-single-transit-long-period-candidate / kepler-eb-circumbinary-transit-candidate.

## Partial wins

- {"id": "p9-recover-known-etno", "statement": "Blind recovery, from public DECam/PS1 frames, of >= 3 known extreme TNOs (e.g. Sedna, 2012 VP113, 2015 TG387, Leleakuhonua) at the predicted positions with astrometry within 1 arcsec; proves the shift-and-stack / linking chain."}
- {"id": "p9-new-ordinary-tno", "statement": "A linked >= 3-epoch, >= 2-night moving object with a bound orbit fit at r > 30 au absent from MPCORB/Distant.txt/SBDB (an ordinary new TNO candidate from archival data, as DEEP found 105 new TNOs in DECam data); same verification chain. The ITF and NEOCP/PCCP checks of the main criterion apply."}
- {"id": "p9-coverage-exclusion-map", "statement": "A reproducible sky-coverage and depth map (per field: epochs, limiting magnitude, motion-rate sensitivity) of the public DECam frames NOT included in the DES/PS1/ZTF Planet Nine exclusion analyses, delivered as a CSV with the frame lists; non-trivial because it defines the remaining search space."}

## Verification

Skeptic re-downloads the named frames/cutouts, re-measures the centroids, re-runs the saved orbit-fit code on the saved astrometry, runs SkyBoT at each epoch, and queries Distant.txt/TNOs/MPCORB and SBDB for any object within the error ellipse. Under one hour for a single candidate.

## Angles

- Public DECam frames (non-DES programs) in the Brown & Batygin 2021 predicted sky region at high galactic latitude that were not part of the DES/PS1/ZTF exclusion analyses; shift-and-stack along the predicted motion range.
- Galactic-plane crossing of the predicted orbit, where all optical searches are least complete; use difference imaging against a deep template.
- The IRAS (1983) vs AKARI (2006-07) far-IR route: candidate pairs from arXiv:2504.17288 / 2506.12854 can be followed up in public optical archives at the predicted 2010-2025 positions.
- Ordinary new TNO discovery as a realistic sub-goal (DEEP found 105 new TNOs in DECam data): the same pipeline, lower bar.
- Use Gaia DR3 + PS1 as the static-sky mask to suppress the dominant false positives before linking.

## Pitfalls

- Asteroids, Centaurs and known TNOs at the predicted position (SkyBoT must be run at every epoch) and spurious linkings of unrelated transients/artifacts across nights: require a single orbit fit with residuals < 0.5 arcsec and > 5 sigma detections.
- Static faint galaxies and variable stars masquerading as slow movers between epochs years apart; require absence at the position in other-epoch frames and in PS1/Gaia catalogs.
- Claims of a 'Planet Nine candidate' (e.g. the 2025 IRAS/AKARI pair) are routinely not confirmed; an agent may never upgrade 'candidate' to 'planet' and must state the excluded-parameter-space context.
- Rubin LSST alerts (since 2026-06-30) and the MPC NEOCP/distant lists update daily; a candidate must be re-checked against the live MPC files on the day of the claim.
- A tracklet already sitting in the MPC ITF or on the NEOCP/PCCP is not a new object: both are checked by position and epoch before any 'new' claim.

## Sources

- https://astroarchive.noirlab.edu/api/sia/voimg?POS=180.0,-30.0&SIZE=0.2&format=json
- https://ps1images.stsci.edu/cgi-bin/ps1filenames.py?ra=187.706&dec=12.391&filters=r
- https://ps1images.stsci.edu/cgi-bin/ps1cutouts?pos=187.706+12.391&filter=r&size=240&output_size=240&format=fits
- https://irsa.ipac.caltech.edu/ibe/search/ztf/products/sci?POS=255.9302,11.8654&ct=csv
- https://minorplanetcenter.net/iau/MPCORB/Distant.txt
- https://minorplanetcenter.net/iau/lists/TNOs.html
- https://minorplanetcenter.net/iau/lists/Centaurs.html
- https://minorplanetcenter.net/iau/MPCORB/MPCORB.DAT
- https://ssd-api.jpl.nasa.gov/sbdb.api?sstr=2024%20YR4
- https://ssp.imcce.fr/webservices/skybot/api/conesearch.php?-ep=2459000.0&-ra=0&-dec=0&-rd=0.5&-mime=text&-output=basic&-loc=500
- https://ar5iv.labs.arxiv.org/html/2401.17977
- https://arxiv.org/html/2504.17288v1
- https://arxiv.org/html/2506.12854v1
- https://www.minorplanetcenter.net/iau/ITF/itf.txt.gz
- https://minorplanetcenter.net/iau/NEO/toconfirm_tabular.html
- Status source: https://astroarchive.noirlab.edu/api/sia/voimg?POS=180.0,-30.0&SIZE=0.2&format=json

## Citations

- [Problem page](../../../../.raw/V3R1T4S/known-unknowns/sky-archives/planet-nine-distant-tno-archival-moonshot.md)
- [Bank entry](../../../../.raw/V3R1T4S/bank/targets.json) (id `planet-nine-distant-tno-archival-moonshot`, commit `7dd4480`)

## Related Nodes

- [[V3R1T4S Sky archives]]
- [[V3R1T4S]]
