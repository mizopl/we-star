---
id: v3r1t4s-asteroid-precovery-arc-extension
type: entity
tags: [v3r1t4s, v3r1t4s/sky-archives, kind/harvest]
inbound_links: 1
confidence: 0.8
last_ingested_sources: [".raw/V3R1T4S/bank/targets.json@7dd4480"]
status: "CONFIRMED_SOLUTION"
priority: ""
notes: ""
category: sky-archives
kind: harvest
tractability: 3
compute: "laptop-hours (cutouts are ~1-10 MB each; orbit propagation is seconds; the limiting step is choosing objects whose back-propagated positions fall in archive coverage; MPCORB.DAT is 319 MB, NEA.txt is small)"
disclosure: open
status_checked: "2026-10-08"
---
# Precovery of known asteroids in public ZTF / Pan-STARRS / DECam images, extending the observed arc

# Overview

> Bank id `asteroid-precovery-arc-extension` · harvest · tractability 3 · laptop-hours (cutouts are ~1-10 MB each; orbit propagation is seconds; the limiting step is choosing objects whose back-propagated positions fall in archive coverage; MPCORB.DAT is 319 MB, NEA.txt is small) · disclosure **open**
> Bank says open as of 2026-10-08. Statuses go stale — re-check the primary source before any work.

## Statement

For a known minor planet (MPCORB / NEA.txt / JPL SBDB), find and measure its image in public archival survey frames (ZTF science images via IRSA IBE, Pan-STARRS1 cutouts via ps1images, DECam via the NOIRLab SIA service) at an epoch EARLIER than the object's first observation recorded by JPL SBDB (orbit.first_obs) / MPC (MPCORB arc column; the object's full observation record via the MPC get-obs API, which answers a GET request carrying a JSON body {"desigs":[...],"output_format":["OBS80"]}, or the MPCAT-OBS NumObs/UnnObs files), such that the detection lies inside the back-propagated orbit covariance, its astrometry has residuals consistent with the orbit (< 2 arcsec, after refitting the orbit with the new point), and the source is absent from the static sky (not in Gaia DR3 / PS1 catalogs at that position and absent in other-epoch frames). No MPC submission is made; the claim is 'precovery detection, verified against the current orbit'. arXiv:2510.07588 (Oct 2025) ran an automated version on ZTF for ~3,000 NEAs, so novelty requires the specific epoch to be absent from the object's MPC observation record.

## Success criterion

A saved bundle {object designation, JPL SBDB JSON (orbit, covariance, first_obs) as fetched, the MPC observation record for the object as fetched (get-obs API OBS80 output or the MPCAT-OBS extract), archival image identifiers and download URLs, cutout FITS for every frame used, source detections with centroid and RA/Dec/uncertainty, predicted position and 3-sigma error ellipse from back-propagation (code saved), refit orbit residuals including the new points, static-sky check} such that: (1) the image epoch precedes JPL SBDB orbit.first_obs for that object (https://ssd-api.jpl.nasa.gov/sbdb.api?sstr=<designation>, re-fetched live immediately before claiming) by at least one apparition (> 60 days), and the MPC observation record for the object (get-obs API, re-fetched live) contains no observation within 1 day of that epoch; (2) >= 2 detections of the object in distinct frames (same night separated by >= 20 min, or different nights), each inside the propagated 3-sigma ellipse, with the measured motion vector between them consistent with the predicted rate and direction within 3 sigma; (3) the residual of each detection against the a-priori orbit is inside the 3-sigma ellipse AND the refit orbit residual at the new epochs is < 2 arcsec (< 1 arcsec for PS1), with the refit changing the semi-major axis by less than its a-priori 3-sigma; (4) the predicted magnitude is within 1.5 mag of the measured one; (5) no static source is present at any detection position in another-epoch frame or in Gaia DR3/PS1 catalogs within 2 arcsec, and a SkyBoT cone search at each epoch shows no other known object within 30 arcsec. Claim is 'precovery detection, verified against the current orbit'; nothing is submitted to the MPC.

## Partial wins

- {"id": "precovery-reproduce-known-obs", "statement": "For >= 10 objects, re-detect in public ZTF/PS1 frames observations that ARE in the MPC record (same epoch), recovering the recorded astrometry to < 1 arcsec; proves the image-retrieval and astrometry chain."}
- {"id": "precovery-single-detection-unvetted", "statement": "A single-frame detection satisfying (1),(3),(4),(5) with no second frame available: logged as 'unvetted single detection', never claimed."}
- {"id": "precovery-arc-doubling", "statement": "Stretch tier: a fully verified precovery (all of (1)-(5)) that doubles an object's data arc (new arc >= 2x JPL data_arc) for an object with data_arc < 365 d; independently checkable against SBDB."}
- {"id": "precovery-neocp-style-short-arc", "statement": "Stretch tier: a fully verified precovery (> 60 d earlier) for an object with n_obs_used < 50 in SBDB, where the added points reduce the semi-major-axis uncertainty by > 50% in the refit; the covariance before/after saved."}

## Verification

Skeptic re-fetches the SBDB JSON and the MPC get-obs record for the object, re-downloads the named cutouts from the saved URLs, re-measures the centroids with the saved script, re-propagates the orbit (saved code) to the frame epochs, and checks the ellipse, the motion vector and the residuals. Under one hour.

## Angles

- Target recently discovered NEAs (NEA.txt entries with first-observation year 2025-2026 and arcs < 1 year) whose back-propagated 2018-2024 positions fall in ZTF's northern footprint; the 2510.07588 pipeline shows ~500 arc-doublings were possible, so plenty remain for objects discovered after their run.
- Pan-STARRS1 (2010-2014 epochs, 3pi survey, r ~ 22) for objects discovered 2020+: a 10-year arc extension, with 1-arcsec-class astrometry.
- DECam public frames (NOIRLab SIA) for southern objects that ZTF/PS1 cannot reach.
- Synthetic tracking: shift-and-stack several ZTF frames from one night along the predicted motion to reach ~1 mag fainter than single frames.
- Use SkyBoT cone searches to reject the case where another known object is at the predicted position.

## Pitfalls

- Static stars, galaxies, hot pixels, cosmic rays and diffraction spikes at the predicted position: require the source to be absent in a different-epoch frame of the same field and in Gaia DR3/PS1 catalogs.
- A detection at an epoch already in the MPC observation record (possibly reported by the archive's own team, e.g. the ZTF precovery pipeline of arXiv:2510.07588) is not an arc extension: check the full observation list for the object, not just SBDB first_obs, and re-fetch both right before claiming.
- Error ellipses for short-arc objects can span degrees years back; a faint source somewhere inside a huge ellipse is likely a chance match - require a magnitude match and a refit residual < 2 arcsec, and prefer objects whose ellipse is < 1 arcmin.
- Proper motion of the archival survey's astrometric reference frame (PS1 vs Gaia epochs) must be handled: all astrometry must be reduced to Gaia DR3 at the frame epoch.
- The MPC db_search/show_object page does not list the observations themselves; use the get-obs API (GET with a JSON body; a POST returns 405) or the MPCAT-OBS files (NumObs.txt.gz 9.1 GB, UnnObs.txt.gz 0.46 GB, refreshed monthly) and save the response.
- A single faint source inside a large ellipse with a refit that absorbs it is the classic false precovery: the main claim needs >= 2 frames with a consistent motion vector.

## Sources

- https://ssd-api.jpl.nasa.gov/sbdb.api?sstr=2024%20YR4
- https://ssd-api.jpl.nasa.gov/sbdb_query.api?fields=full_name,epoch,e,a&sb-kind=a&limit=5
- https://minorplanetcenter.net/iau/MPCORB/MPCORB.DAT
- https://minorplanetcenter.net/iau/MPCORB/NEA.txt
- https://minorplanetcenter.net/db_search/show_object?object_id=2024+YR4
- https://minorplanetcenter.net/iau/ECS/MPCAT-OBS/MPCAT-OBS.html
- https://irsa.ipac.caltech.edu/ibe/search/ztf/products/sci?POS=255.9302,11.8654&ct=csv
- https://irsa.ipac.caltech.edu/ibe/data/ztf/products/sci/
- https://ps1images.stsci.edu/cgi-bin/ps1filenames.py?ra=187.706&dec=12.391&filters=r
- https://ps1images.stsci.edu/cgi-bin/ps1cutouts?pos=187.706+12.391&filter=r&size=240&output_size=240&format=fits
- https://astroarchive.noirlab.edu/api/sia/voimg?POS=180.0,-30.0&SIZE=0.2&format=json
- https://ssp.imcce.fr/webservices/skybot/api/conesearch.php?-ep=2459000.0&-ra=0&-dec=0&-rd=0.5&-mime=text&-output=basic&-loc=500
- https://arxiv.org/pdf/2510.07588
- https://data.minorplanetcenter.net/api/get-obs
- https://minorplanetcenter.net/iau/ECS/MPCAT-OBS/UnnObs.txt.gz
- Status source: https://ssd-api.jpl.nasa.gov/sbdb.api?sstr=2024%20YR4

## Citations

- [Problem page](../../../../.raw/V3R1T4S/known-unknowns/sky-archives/asteroid-precovery-arc-extension.md)
- [Bank entry](../../../../.raw/V3R1T4S/bank/targets.json) (id `asteroid-precovery-arc-extension`, commit `7dd4480`)

## Related Nodes

- [[V3R1T4S Sky archives]]
- [[V3R1T4S]]
