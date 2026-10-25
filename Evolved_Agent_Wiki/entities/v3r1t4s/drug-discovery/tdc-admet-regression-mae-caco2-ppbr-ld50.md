---
id: v3r1t4s-tdc-admet-regression-mae-caco2-ppbr-ld50
type: entity
tags: [v3r1t4s, v3r1t4s/drug-discovery, kind/harvest]
inbound_links: 1
confidence: 0.8
last_ingested_sources: [".raw/V3R1T4S/bank/targets.json@7dd4480"]
status: "open"
priority: ""
notes: ""
category: drug-discovery
kind: harvest
tractability: 3
compute: "laptop-hours"
disclosure: open
status_checked: "2026-10-15"
---
# TDC ADMET Benchmark Group, MAE regression leaderboards (Caco2_Wang, PPBR_AZ, LD50_Zhu): beat rank 1 on the official scaffold split

# Overview

> Bank id `tdc-admet-regression-mae-caco2-ppbr-ld50` · harvest · tractability 3 · laptop-hours · disclosure **open**
> Bank says open as of 2026-10-15. Statuses go stale — re-check the primary source before any work.

## Statement

The Therapeutics Data Commons ADMET Benchmark Group fixes, for each of 22 datasets, a scaffold split (20% test) and an evaluation protocol: train with 5 seeds, report mean +- std of the metric through tdc.benchmark_group.admet_group.evaluate_many. The three MAE regression leaderboards with small-to-medium data are Caco2_Wang (906 molecules, rank 1 'CaliciBoost' MAE 0.256 +- 0.006, runner-up 'XG Boost' 0.274 +- 0.004 with 21 parameters), PPBR_AZ (1,797, rank 1 'Gradient Boost' 7.440 +- 0.024 with a single reported parameter, runner-up MapLight+GNN 7.526 +- 0.106) and LD50_Zhu (7,385, rank 1 'BaseBoosting KyQVZ6b2' 0.552 +- 0.009, runner-up ADMETrix 0.573 +- 0.010). All three leaders are classical gradient-boosting / descriptor models, i.e. no GPU is needed to be competitive, and the TDC leaderboard pages carry no dates while the TDC GitHub repo's last commits are from April 2025, so the tables are stale. The open question per dataset: can a better featurisation + ensembling recipe lower the 5-seed mean MAE below the listed rank-1 value?

## Success criterion

Pick one of the three datasets. Success means saved per-seed prediction files (5 files, seeds 1-5 as produced by tdc.benchmark_group.admet_group with the default path and no re-splitting, each giving one predicted value per official test molecule in the official order, plus a manifest with the sha256 of the downloaded TDC data files and of the train_val/test SMILES lists) such that (a) the test set is byte-identical to the group's own test split for that benchmark, (b) the mean MAE over the 5 seeds, recomputed by the skeptic with the group's own evaluate call, is strictly LOWER (direction: min) than the rank-1 MAE in the live leaderboard table at the dataset's tdcommons.ai page, re-fetched immediately before claiming, (c) the improvement is at least max(the listed rank-1 std, the attacker's own std across the 5 seeds) and at least 1.5% relative, (d) every model is fit only on the official train_val rows of that same seed (any internal validation must be carved out of train_val), and (e) no external dataset containing any test molecule's measured endpoint is used; if an external training set is used at all, the attacker must list it and show zero stereo-stripped-InChIKey overlap with the test split. Beating only the runner-up does not count.

## Partial wins

- {"id": "p1", "statement": "The full strict win on Caco2_Wang alone (906 molecules, smallest and stalest of the three), verified against the live table at https://tdcommons.ai/benchmark/admet_group/01caco2/ ."}
- {"id": "p2", "statement": "A reproduction-plus-margin result: an independently re-implemented runner-up-class baseline (plain XGBoost or Chemprop-RDKit) plus a declared, ablated addition (e.g. a conformal shrinkage step or a new descriptor block) whose 5-seed mean MAE beats the live rank-1 value on one dataset, with an ablation table showing the addition, not the baseline, produced the gain."}
- {"id": "p3", "statement": "A strict win on any OTHER TDC ADMET regression leaderboard listed on the group overview page (Lipophilicity_AstraZeneca MAE, Solubility_AqSolDB MAE) under the identical protocol and margin."}

## Verification

Skeptic pip-installs PyTDC, instantiates admet_group(path='data/'), calls group.get(<Benchmark>) for seeds 1-5 exactly as the submission instructions prescribe, checks the test SMILES list sha256 against the attacker's manifest, loads the 5 prediction files, calls group.evaluate_many / evaluate to obtain mean and std, confirms the margin rule, then re-fetches the dataset's leaderboard page and parses all listed MAE values. Re-running the attacker's training script for all 5 seeds must fit in under an hour on 10 CPU cores (906-7,385 molecules).

## Angles

- Descriptor-space brute force on CPU: RDKit 2D + Mordred-style descriptors + several fingerprint families, feature selection by out-of-fold permutation importance, then LightGBM/CatBoost/ExtraTrees/kernel-ridge stacked with a non-negative least-squares meta-learner fit on out-of-fold predictions of train_val only. The current leaders are exactly this class of model, so the gap is engineering, not scale.
- Scaffold-aware internal validation: because the official split is scaffold-based, use Bemis-Murcko-grouped CV inside train_val (GroupKFold on scaffolds) for every hyper-parameter choice; models tuned under random CV are systematically mis-tuned for this test set, which is a cheap, often-ignored 1-3% MAE.
- CROSS-DOMAIN (signal processing / robust statistics): MAE is an L1 target while most boosters optimise L2. Train with Huber/quantile (median) objectives, and post-process with an isotonic or median-calibrated mapping fit out-of-fold, which reduces MAE even when correlation is unchanged - directly exploiting the metric rather than the chemistry.
- CROSS-DOMAIN (ecology / species-distribution thinking): treat each molecule as a site described by physicochemical 'environment' variables (logP, TPSA, charge state at pH 7.4, H-bond counts) and fit a Gaussian-process / GAM 'response surface' with monotonicity constraints from known permeability and plasma-protein-binding physiology; mechanistic monotone priors buy accuracy where data are sparse (Caco2, PPBR).
- CROSS-DOMAIN (combinatorial search / cryptanalytic hill climbing): treat the recipe (descriptor blocks, transforms, model family, loss, calibration) as a discrete string and run a scaffold-CV-scored simulated-annealing/genetic search over it with a strict evaluation budget, exactly as one would search key schedules - CPU-cheap on 1-8k molecules and far more thorough than hand-tuning.
- Target transforms: for PPBR (percent bound, 0-100) model logit(fraction unbound) and invert; for LD50 model the log-dose directly but weight by assay-duplicate counts. Inverting a variance-stabilised transform is a classic few-percent MAE gain that leaderboard entries often skip.
- Semi-supervised use of unlabelled chemical space: self-training / pseudo-labelling on a large unlabelled set (ZINC/ChEMBL structures only, no labels) to regularise the feature space, with explicit InChIKey filtering against the test split.

## Pitfalls

- Re-splitting instead of using the group's split: the TDC scaffold split must come from group.get(); any locally generated scaffold split (different RDKit version, different seed, different 80/10/10 convention) gives an incomparable number. The skeptic must hash the test SMILES list.
- Seed cherry-picking: the leaderboard value is a mean over 5 seeds with a listed std. Reporting the best of 5 seeds, or using fewer seeds, is the single most common false positive here; the margin must exceed the larger of the two stds.
- Scaffold leakage through pretraining: ADMET-pretrained models and public descriptor services (and some AutoML submissions) were trained on datasets that INCLUDE Caco2_Wang / PPBR_AZ / LD50_Zhu rows, so the official 'test' molecules are inside their training data. Any pretrained component must have declared provenance and be checked for test-molecule overlap.
- Duplicate/near-duplicate molecules inside TDC itself (salts, tautomers, repeated measurements) crossing the scaffold boundary; a nearest-neighbour or memorising model then scores unrealistically well. Check stereo-stripped InChIKey overlap between train_val and test and report it.
- Metric mismatch: TDC uses MAE for these three and Spearman for others; computing MAE on standardised/z-scored labels, or on a different unit (log10 cm/s vs cm/s for Caco2, percent vs fraction for PPBR), silently changes the number. Score only through the group's own evaluate call.
- Novelty trap: published papers (ADMET-AI, MapLight, ZairaChem, CaliciBoost, MiniMol and 2024-2026 TabPFN-style submissions) report numbers on these same splits that may be better than the stale leaderboard row; the NOVELTY skeptic must search the last 24 months for the same benchmark name before any win is called.

## Sources

- https://tdcommons.ai/benchmark/admet_group/overview/
- https://tdcommons.ai/benchmark/admet_group/01caco2/
- https://tdcommons.ai/benchmark/admet_group/08ppbr/
- https://tdcommons.ai/benchmark/admet_group/19ld50/
- https://github.com/mims-harvard/TDC
- Status source: https://tdcommons.ai/benchmark/admet_group/overview/

## Citations

- [Problem page](../../../../.raw/V3R1T4S/known-unknowns/drug-discovery/tdc-admet-regression-mae-caco2-ppbr-ld50.md)
- [Bank entry](../../../../.raw/V3R1T4S/bank/targets.json) (id `tdc-admet-regression-mae-caco2-ppbr-ld50`, commit `7dd4480`)

## Related Nodes

- [[V3R1T4S Drug discovery]]
- [[V3R1T4S]]
