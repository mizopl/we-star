---
id: v3r1t4s-jarvis-small-data-exfoliation-tc-mae
type: entity
tags: [v3r1t4s, v3r1t4s/physics, kind/harvest]
inbound_links: 1
confidence: 0.8
last_ingested_sources: [".raw/V3R1T4S/bank/targets.json@7dd4480"]
status: "CONFIRMED_SOLUTION"
priority: ""
notes: ""
category: physics
kind: harvest
tractability: 3
compute: "laptop-hours"
disclosure: open
status_checked: "2026-10-15"
---
# JARVIS-Leaderboard small-data materials properties (exfoliation energy, superconducting Tc): beat the best listed test MAE

# Overview

> Bank id `jarvis-small-data-exfoliation-tc-mae` · harvest · tractability 3 · laptop-hours · disclosure **open**
> Bank says open as of 2026-10-15. Statuses go stale — re-check the primary source before any work.

## Statement

Two small JARVIS-DFT property tasks on the JARVIS-Leaderboard (Kamal Choudhary et al., NIST) are realistic on a CPU: dft_3d_exfoliation_energy (812 layered materials, fixed 650/81/81 train/val/test split; best listed test MAE 40.887 meV/atom, matminer_xgboost, University of Toronto, May 2023) and dft_3d_Tc_supercon (electron-phonon superconducting transition temperatures from the JARVIS BCS workflow; best listed test MAE 1.5187 K, AtomGPT, May 2024). Structures and splits are public in the GitHub repository. Both tasks have few submissions and no entries since 2024. Checked live 2026-10-15: both pages HTTP 200.

## Success criterion

Success means a trained model, training script and predictions file for dft_3d_exfoliation_energy or dft_3d_Tc_supercon such that the test MAE, recomputed by the checker on the official test ids of the benchmark json, is STRICTLY LOWER (direction: min) than the best MAE on that task's live leaderboard page re-fetched immediately before claiming, by at least 5% relative AND by more than the half-width of a 1000-sample bootstrap 90% confidence interval of the claimed model's MAE; AND the model was trained only on train (and val) ids with no external data containing the test materials' labels; AND re-running the saved model reproduces the predictions file.

## Partial wins

- {"id": "p1", "statement": "The same rules on one further small JARVIS AI single-property task with fewer than 2000 materials and at least three listed entries (for example dft_3d_max_efg or dft_3d_dfpt_piezo_max_dij), named before the run starts."}
- {"id": "p2", "statement": "A 5-fold cross-validation study on the union of train and val showing the claimed model's advantage over a reproduced matminer_xgboost (or AtomGPT) baseline with a paired test, published with the predictions."}

## Verification

Checker (< 15 min): download the benchmark json.zip from jarvis_leaderboard/benchmarks/AI/SinglePropertyPrediction/; load the claimed model; predict the test ids from the JARVIS-DFT structures (jarvis-tools dft_3d dataset); compute MAE and bootstrap interval; compare with the live page; inspect the training script for test-id use.

## Angles

- Physics features for exfoliation: interlayer distance, layer-normal vdW contact area, layer charge transfer and a dispersion-only (D3-like) interlayer energy computed directly from the structure, fed to gradient boosting; exfoliation energy is largely a vdW-contact quantity.
- Superconductivity priors (McMillan / Allen-Dynes): predict lambda and omega_log-like proxies (light-element content, Debye-temperature estimates from a universal potential's phonons) and map them through the Allen-Dynes formula, learning only the residual.
- Transfer from universal potentials: use frozen MACE-MP or CHGNet embeddings as descriptors for a small kernel ridge or boosted-tree head (pretraining labels are energies/forces, not exfoliation energies or Tc, but confirm no Tc labels leak).
- Small-data statistics: nested cross-validation for hyperparameters, monotone constraints, and ensembles; the 81-structure exfoliation test set punishes overfitting.
- Geometry import from topology/crystallography: dimensionality and layer-identification algorithms (lattice-graph connected components) to compute per-layer descriptors robustly.

## Pitfalls

- Test sets are tiny (81 materials for exfoliation); a 2-3% MAE gain is noise. The bootstrap margin is mandatory.
- Test labels are public in the repository and in JARVIS-DFT; any use of them, or of models pretrained on JARVIS property labels (for example AtomGPT checkpoints trained on full JARVIS-DFT), is leakage.
- Some leaderboard rows are mislabeled or duplicated (rows named after other tasks appear on some pages); compare with the best genuine row for the exact task and note anomalies rather than treating them as the bar.
- Units: exfoliation energy in meV/atom, Tc in K; per-formula-unit or eV values give fake improvements.

## Sources

- https://pages.nist.gov/jarvis_leaderboard/AI/SinglePropertyPrediction/dft_3d_exfoliation_energy/
- https://pages.nist.gov/jarvis_leaderboard/AI/SinglePropertyPrediction/dft_3d_Tc_supercon/
- https://github.com/usnistgov/jarvis_leaderboard
- https://raw.githubusercontent.com/usnistgov/jarvis_leaderboard/main/jarvis_leaderboard/benchmarks/AI/SinglePropertyPrediction/dft_3d_exfoliation_energy.json.zip
- https://raw.githubusercontent.com/usnistgov/jarvis_leaderboard/main/jarvis_leaderboard/benchmarks/AI/SinglePropertyPrediction/dft_3d_Tc_supercon.json.zip
- Status source: https://pages.nist.gov/jarvis_leaderboard/AI/SinglePropertyPrediction/dft_3d_exfoliation_energy/

## Citations

- [Problem page](../../../../.raw/V3R1T4S/known-unknowns/physics/jarvis-small-data-exfoliation-tc-mae.md)
- [Bank entry](../../../../.raw/V3R1T4S/bank/targets.json) (id `jarvis-small-data-exfoliation-tc-mae`, commit `7dd4480`)

## Related Nodes

- [[V3R1T4S Physics]]
- [[V3R1T4S]]
