---
id: v3r1t4s-jarvis-mlearn-mlff-force-mae
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
tractability: 3
compute: "laptop-hours"
disclosure: open
status_checked: "2026-10-15"
---
# JARVIS-Leaderboard mlearn force fields (Cu, Ge, Li, Mo, Ni, Si): beat the best listed test force MAE with a model trained on a laptop

# Overview

> Bank id `jarvis-mlearn-mlff-force-mae` · harvest · tractability 3 · laptop-hours · disclosure **open**
> Bank says open as of 2026-10-15. Statuses go stale — re-check the primary source before any work.

## Statement

The JARVIS-Leaderboard (Kamal Choudhary and co-workers, NIST; npj Comput. Mater. 2024) scores machine-learned interatomic potentials on the mlearn DFT datasets of Yunxing Zuo, Shyue Ping Ong and co-workers (J. Phys. Chem. A 124, 731, 2020): six elements, a few hundred training configurations each, fixed train/val/test splits in the public GitHub repository. The metric for the *_forces tasks is the mean absolute error of force components on the test structures (eV/A). Best listed values (checked live 2026-10-15): Cu 0.0177 (matgl_mlearn), Ge 0.0720 (alignnff_mlearn_all_wt1), Li 0.0273 (snap_mlearn), Mo 0.1843 (snap_mlearn), Ni 0.0618 (snap_mlearn), Si 0.0694 (alignnff_mlearn_wt1); most entries date from 2023 and none is a modern equivariant or atomic-cluster-expansion model trained on these splits. Zuo et al. reported GAP and MTP errors (their Figure 3) that may already be lower for some elements on their own split, so a win is judged against both. The datasets are small enough to train on a CPU in hours.

## Success criterion

Success means a trained model, its training script and a predictions file for one mlearn_<element>_forces task such that the force MAE on the leaderboard's official test split, recomputed by the checker from the benchmark json in the repository, is STRICTLY LOWER (direction: min) than the best MAE listed on that task's live leaderboard page re-fetched immediately before claiming, by at least 5% relative; AND the model was trained only on the train (and val) ids of that benchmark json, with no pretraining on any dataset containing the test configurations; AND re-running the saved model on the test structures reproduces the predictions file to 1e-6 eV/A; AND the result is compared against Zuo et al. 2020 and any later paper reporting a lower force MAE on the same mlearn test set (found by a literature search), with the comparison stated in the claim.

## Partial wins

- {"id": "p1", "statement": "The same 5% improvement on the corresponding *_energy or *_stresses task for the same element, with the same training-split and re-run rules."}
- {"id": "p2", "statement": "A single model that is within 10% of the best listed force MAE on all six elements simultaneously while being at least 5x faster at inference than the listed best model (timing script included)."}

## Verification

Checker (< 30 min on CPU): download jarvis_leaderboard/benchmarks/AI/MLFF/mlearn_<el>_forces.json.zip from GitHub; load the claimed model; run it on the test ids; compute the force-component MAE exactly as the leaderboard does (flattened components); compare with the live page; grep the training script and data loader for test ids; confirm no external pretrained weights unless their training data provably exclude the mlearn test structures.

## Angles

- Train a small linear or nonlinear atomic cluster expansion (ACE) or MTP model; these polynomial-basis potentials are CPU-friendly and were near the top in Zuo et al., but no ACE/MTP entry exists on the JARVIS tasks.
- Kernel-methods import: a SOAP-GAP or sparse Gaussian-process force model with careful hyperparameter search; small data favours kernels over deep networks.
- Fine-tune an open universal potential (MACE-MP, CHGNet) on the train split only, after checking that its pretraining data do not contain the mlearn test configurations (the mlearn structures are custom DFT runs, not Materials Project relaxations, but this must be verified).
- Physics priors from metallurgy: add an embedded-atom (EAM) baseline and fit the ML model to the residual (delta-learning); Mo, the hardest element, has large forces from stiff bcc bonds where a physical baseline helps.
- Statistics import: ensemble five seeds and average; report bootstrap confidence intervals on the test MAE to show the 5% margin is not noise.

## Pitfalls

- Test-label leakage: the test labels are public in the repository; any hyperparameter tuning on the test split, or pretraining on data containing the test configurations, invalidates the claim. Tune on val only.
- Metric mismatch: the leaderboard 'Multimae' for forces is a component-wise MAE in eV/A; per-atom force-vector norms or RMSE give different numbers.
- Several leaderboard entries were submitted on the same date with suspiciously different scores (pretrained vs fine-tuned); compare against the best listed number, not a convenient one, and against Zuo et al. and later literature for the same split.
- The 81-300 structure test sets are small; improvements under about 5% are within seed-to-seed noise.

## Sources

- https://pages.nist.gov/jarvis_leaderboard/
- https://pages.nist.gov/jarvis_leaderboard/AI/MLFF/mlearn_Mo_forces/
- https://pages.nist.gov/jarvis_leaderboard/AI/MLFF/mlearn_Si_forces/
- https://github.com/usnistgov/jarvis_leaderboard
- https://raw.githubusercontent.com/usnistgov/jarvis_leaderboard/main/jarvis_leaderboard/benchmarks/AI/MLFF/mlearn_Mo_forces.json.zip
- https://arxiv.org/abs/1906.08888
- Status source: https://pages.nist.gov/jarvis_leaderboard/AI/MLFF/mlearn_Mo_forces/

## Citations

- [Problem page](../../../../.raw/V3R1T4S/known-unknowns/physics/jarvis-mlearn-mlff-force-mae.md)
- [Bank entry](../../../../.raw/V3R1T4S/bank/targets.json) (id `jarvis-mlearn-mlff-force-mae`, commit `7dd4480`)

## Related Nodes

- [[V3R1T4S Physics]]
- [[V3R1T4S]]
