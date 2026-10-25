---
id: v3r1t4s-ssh-mapping-natl60-2020a-osse
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
tractability: 2
compute: "laptop-hours"
disclosure: open
status_checked: "2026-10-15"
---
# Ocean data challenge 2020a (SSH mapping OSSE, NATL60): beat a leaderboard resolution score

# Overview

> Bank id `ssh-mapping-natl60-2020a-osse` · harvest · tractability 2 · laptop-hours · disclosure **open**
> Bank says open as of 2026-10-15. Statuses go stale — re-check the primary source before any work.

## Statement

The 2020a OSSE challenge reconstructs NATL60 model SSH from simulated nadir (and SWOT) tracks. README leaderboard: best 4-nadir mu(RMSE) 0.95 (4DVarQG), lambda_x 0.82 deg, lambda_t 5.84 days; best 1 SWOT + 4 nadir mu 0.96, lambda_x 0.62 deg, lambda_t 4.35 days (4DVarNet v2022). Data on a public OPeNDAP mirror; evaluation notebooks in repo. Open task: beat a best leaderboard metric in a given observation configuration.

## Success criterion

A saved NetCDF reconstruction for the 42-day evaluation period (2012-10-22..2012-12-02), scored by the repository's unmodified evaluation notebook, that strictly improves lambda_x or lambda_t (direction: min) over the best entry of the same observation configuration in the README leaderboard at https://github.com/ocean-data-challenges/2020a_SSH_mapping_NATL60 re-fetched live immediately before claiming, without worse mu(RMSE), AND over the best value for the same configuration and metric reported in any paper of the last 24 months that uses this challenge setup (including Li et al., GMD 19, 7349-7367, 2026, and 4DVarNet follow-ups); training may use reference data only in 2013-01-02..2013-09-30; reference data 2012-12-02..2013-01-02 never used. A README-only improvement is partial win p3.

## Partial wins

- {"id": "p1", "statement": "A non-neural method beating all OI/DUACS/MIOST/DYMOST/BFN rows in lambda_t for 4 nadirs."}
- {"id": "p2", "statement": "Matching the best 4-nadir lambda_x (0.82 deg) with a model trained in under 2 CPU-hours."}
- {"id": "p3", "statement": "Beating the README best for a configuration when a paper already reports a better value (README-only improvement)."}

## Verification

Skeptic runs the official evaluation notebook on the saved map against the reference files from the OPeNDAP mirror; checks training-window compliance by inspecting the data-loading code. Under 1 hour.

## Angles

- Conventional: 4DVar with a QG model and tuned background error, warm-started from DUACS-like OI.
- Conventional: small 3D CNN emulator of the OI-to-truth residual trained on the allowed 2013 window.
- Cross-domain import (video super-resolution / inpainting): temporal-attention inpainting networks treating unobserved pixels as masks.
- Cross-domain import (numerical weather prediction): ensemble Kalman smoother with localisation (EnKS/LETKF) using a cheap QG ensemble.
- Cross-domain import (seismic tomography): sparsity-promoting inversion with total-variation regularisation on vorticity fronts.

## Pitfalls

- Leakage from the forbidden reference window or from the evaluation period itself.
- Leaderboard rounding: ties at 2 decimals are not improvements.
- Scores in different observation configurations are not comparable.
- The data mirror is 'temporary'; if it disappears, AVISO+ requires an account - do not sign up, drop the target.

## Sources

- https://github.com/ocean-data-challenges/2020a_SSH_mapping_NATL60
- https://ige-meom-opendap.univ-grenoble-alpes.fr/thredds/catalog/meomopendap/extract/MEOM/OCEAN_DATA_CHALLENGES/2020a_SSH_mapping_NATL60/catalog.html
- https://gmd.copernicus.org/articles/19/7349/2026/
- Status source: https://github.com/ocean-data-challenges/2020a_SSH_mapping_NATL60

## Citations

- [Problem page](../../../../.raw/V3R1T4S/known-unknowns/earth-and-sky/ssh-mapping-natl60-2020a-osse.md)
- [Bank entry](../../../../.raw/V3R1T4S/bank/targets.json) (id `ssh-mapping-natl60-2020a-osse`, commit `7dd4480`)

## Related Nodes

- [[V3R1T4S Earth and sky]]
- [[V3R1T4S]]
