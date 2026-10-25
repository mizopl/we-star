---
id: v3r1t4s-matbench-medium-structure-tasks-cpu
type: entity
tags: [v3r1t4s, v3r1t4s/physics, kind/harvest]
inbound_links: 1
confidence: 0.8
last_ingested_sources: [".raw/V3R1T4S/bank/targets.json@7dd4480"]
status: "open"
priority: ""
notes: ""
category: physics
kind: harvest
tractability: 2.5
compute: "laptop-days"
disclosure: open
status_checked: "2026-10-15"
---
# Matbench v0.1 medium tasks (phonons, dielectric, expt_is_metal, log_gvrh, log_kvrh, perovskites): beat the verified leaderboard score with CPU-trained models

# Overview

> Bank id `matbench-medium-structure-tasks-cpu` · harvest · tractability 2.5 · laptop-days · disclosure **open**
> Bank says open as of 2026-10-15. Statuses go stale — re-check the primary source before any work.

## Statement

Matbench v0.1 (Alexander Dunn, Qi Wang, Alex Ganose, Daniel Dopp and Anubhav Jain, npj Comput. Mater. 6, 138, 2020) scores materials-property models by nested 5-fold cross-validation with fixed folds; its verified leaderboard (checked live 2026-10-15) lists: matbench_phonons (1,265 structures, last phonon DOS peak) 28.7606 cm^-1 by MegNet (kgcnn v2.1.0); matbench_dielectric (4,764) 0.2711 by MODNet v0.1.12; matbench_expt_is_metal (4,921, ROC-AUC) 0.9209 by AMMExpress v2020; matbench_log_gvrh and matbench_log_kvrh (10,987) 0.0670 and 0.0491 log10(GPa) by coNGN; matbench_perovskites (18,928) 0.0269 eV/unit cell by coGN. These sizes are trainable on a laptop CPU in hours to days. The four smallest-data tasks (steels, expt_gap, glass, jdft2d) are covered by a separate entry and excluded here.

## Success criterion

Success means a complete Matbench v0.1 record for one of the six named tasks (predictions for all 5 test folds produced with the official matbench package folds, models trained only on each fold's training data) whose mean score is STRICTLY BETTER (direction: min for MAE, max for ROC-AUC) than the verified leaderboard value for that task on https://matbench.materialsproject.org/ re-fetched immediately before claiming, by at least the larger of 2% relative and the fold-to-fold standard deviation of the best listed entry divided by sqrt(5); AND re-running the saved per-fold models reproduces the predictions; AND a literature search finds no published Matbench-protocol score for that task that is better than the claim (reported with the claim either way).

## Partial wins

- {"id": "p1", "statement": "Beat the best leaderboard entry that uses no structure (composition-only) on a 'structure required' task by at least 10% relative, with the same protocol."}
- {"id": "p2", "statement": "A single CPU-trained model architecture that ranks first or second on at least three of the six tasks simultaneously under the protocol."}

## Verification

Checker (< 1 hour for prediction checks): load the claim's matbench results json (the format produced by MatbenchBenchmark.to_file); confirm task name, fold indices and that fold test indices match the official KFold (random_state 18012019, shuffle); recompute fold scores from predictions and the matbench dataset labels; re-run inference for one random fold from the saved model; compare with the live leaderboard value.

## Angles

- Universal-potential embeddings as features: frozen MACE-MP / CHGNet / ORB node embeddings pooled per structure feeding gradient boosting or a small MLP; cheap on CPU and strong on elastic and phonon targets (check that pretraining data do not contain the targets).
- Physics-informed phonon target: the last phonon DOS peak correlates with the highest optical frequency; predict it from a universal potential's Gamma-point Hessian (a few seconds per structure) and learn only the residual.
- Elasticity priors: compute bulk and shear moduli with a universal potential via strain-stress fits, then delta-learn log_kvrh and log_gvrh from those estimates.
- Dielectric: use Clausius-Mossotti style polarizability sums over ions plus band-gap proxies as features; refractive index scales with gap.
- Statistics: multi-seed ensembles and hyperparameter search inside the inner folds only; report paired fold-wise comparisons with the leaderboard entry.

## Pitfalls

- Fold leakage: hyperparameters tuned on outer test folds, or features from a model pretrained on Materials Project data containing the same structures' target labels (elastic moduli, dielectric constants), invalidate the claim.
- Universal potentials pretrained on MPtrj saw the structures but not phonon/dielectric/elastic labels; that is allowed only if stated, but any model trained on MP elasticity or dielectric labels is leakage.
- Unverified literature numbers: many papers quote Matbench scores without the official protocol or with different folds; only protocol-compliant fold predictions count, and the leaderboard's 'verified' value is the bar.
- Do not compare log10(GPa) MAE with GPa MAE, or ROC-AUC with accuracy.

## Sources

- https://matbench.materialsproject.org/
- https://github.com/materialsproject/matbench
- https://doi.org/10.1038/s41524-020-00406-3
- Status source: https://matbench.materialsproject.org/

## Citations

- [Problem page](../../../../.raw/V3R1T4S/known-unknowns/physics/matbench-medium-structure-tasks-cpu.md)
- [Bank entry](../../../../.raw/V3R1T4S/bank/targets.json) (id `matbench-medium-structure-tasks-cpu`, commit `7dd4480`)

## Related Nodes

- [[V3R1T4S Physics]]
- [[V3R1T4S]]
