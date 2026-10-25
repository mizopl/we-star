---
id: v3r1t4s-ssh-mapping-ose-2021a-resolution
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
# Ocean data challenge 2021a (SSH mapping OSE): beat the leaderboard effective resolution or RMSE score on real altimetry

# Overview

> Bank id `ssh-mapping-ose-2021a-resolution` · harvest · tractability 2.5 · laptop-hours · disclosure **open**
> Bank says open as of 2026-10-15. Statuses go stale — re-check the primary source before any work.

## Statement

The ocean-data-challenges 2021a OSE challenge reconstructs Gulf Stream sea-surface-height maps from real 2017 nadir altimetry with Cryosat-2 withheld for evaluation. The README leaderboard lists mu(RMSE), sigma(RMSE) and effective resolution lambda_x (km): best SSH-only lambda_x = 106 km (4DVarQG), best with SST = 100 km (ConvLSTM SSH-SST), best mu(RMSE)=0.90. Data (~GB) are on a public OPeNDAP mirror; the evaluation notebooks are in the repo. Open task: a reconstruction that beats a leaderboard best on the official metric.

## Success criterion

A saved NetCDF map over the challenge domain/period, built only from allowed observations (no Cryosat-2 c2 file used in any way), which when scored by the repository's own evaluation notebook (unmodified, run by the skeptic) gives lambda_x strictly smaller (direction: min) than the best entry in the SAME input category (SSH-only or SSH+SST) of the README leaderboard at https://github.com/ocean-data-challenges/2021a_SSH_mapping_OSE re-fetched live immediately before claiming, with mu(RMSE) not lower than that entry's; alternatively mu(RMSE) strictly higher at the leaderboard's 2-decimal rounding with lambda_x no worse. Must also beat any number reported for the 2021a OSE setup in papers of the last 24 months found by search (as of 2026-10-15 none was found that beats the README; the INR paper of Li et al., GMD 2026, uses different regions).

## Partial wins

- {"id": "p1", "statement": "An SSH-only method reaching lambda_x <= the best SSH-only leaderboard value with < 1 CPU-hour of training, verified with the unmodified notebook."}
- {"id": "p2", "statement": "A cheap (OI-class, no neural net) method beating DUACS and MIOST on both mu(RMSE) and lambda_x."}
- {"id": "p3", "statement": "Matching the best leaderboard row within rounding using only 3 of the 6 nadir missions (data-thinning robustness), verified with the notebook."}

## Verification

Skeptic clones the repo, downloads the obs and c2 evaluation file from the OPeNDAP mirror, runs the official evaluation notebook on the submitted NetCDF and compares to the live README; checks the method's code never opens the c2 file (grep + run in a sandbox without it). About 30-45 minutes on CPU.

## Angles

- Conventional: tuned multi-scale OI (two Gaussian covariance scales + flow-dependent anisotropy) and quasi-geostrophic back-and-forth nudging (BFN-QG) with tuned Rossby radius.
- Conventional: small CNN/U-Net trained on the OSSE NATL60 reference (allowed) and applied to OSE, with ensemble averaging.
- Cross-domain import (computer vision): implicit neural representations / neural fields (SIREN-style) fitted directly to along-track points with a QG-physics regulariser.
- Cross-domain import (geostatistics/mining): space-time kriging with a learned non-stationary covariance (SPDE / Gaussian-Markov random field, INLA-style) instead of fixed OI covariances.
- Cross-domain import (MRI compressed sensing): treat the SSH cube as sparse in a wavelet/curvelet basis and reconstruct by L1-regularised inversion from sub-Nyquist tracks.

## Pitfalls

- Leakage: any use of the withheld Cryosat-2 file (even for hyper-parameter tuning) voids the result.
- Using SST or other extra inputs moves the entry to a different leaderboard category; compare like with like.
- lambda_x depends on the PSD-based score threshold (0.5); an edited evaluation notebook can 'improve' it - only the unmodified notebook counts.
- Leaderboard values are rounded to 2 decimals / km; claimed ties are not wins.
- AVISO+ access needs an account; use only the public OPeNDAP mirror - never sign up.

## Sources

- https://github.com/ocean-data-challenges/2021a_SSH_mapping_OSE
- https://raw.githubusercontent.com/ocean-data-challenges/2021a_SSH_mapping_OSE/master/README.md
- Status source: https://github.com/ocean-data-challenges/2021a_SSH_mapping_OSE

## Citations

- [Problem page](../../../../.raw/V3R1T4S/known-unknowns/earth-and-sky/ssh-mapping-ose-2021a-resolution.md)
- [Bank entry](../../../../.raw/V3R1T4S/bank/targets.json) (id `ssh-mapping-ose-2021a-resolution`, commit `7dd4480`)

## Related Nodes

- [[V3R1T4S Earth and sky]]
- [[V3R1T4S]]
