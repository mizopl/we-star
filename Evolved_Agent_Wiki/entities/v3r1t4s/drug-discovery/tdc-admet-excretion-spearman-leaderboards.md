---
id: v3r1t4s-tdc-admet-excretion-spearman-leaderboards
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
# TDC ADMET Spearman leaderboards (Half_Life_Obach, Clearance_Hepatocyte_AZ, Clearance_Microsome_AZ, VDss_Lombardo): beat rank 1

# Overview

> Bank id `tdc-admet-excretion-spearman-leaderboards` · harvest · tractability 3 · laptop-hours · disclosure **open**
> Bank says open as of 2026-10-15. Statuses go stale — re-check the primary source before any work.

## Statement

Four TDC ADMET benchmarks are scored by Spearman correlation on a fixed scaffold split, 5 seeds: Half_Life_Obach (667 molecules, rank 1 'CFA' 0.576 +- 0.025, runner-up MapLight 0.562 +- 0.008), Clearance_Hepatocyte_AZ (1,020, rank 1 'CFA' 0.536 +- 0.020, runner-up MapLight+GNN 0.498 +- 0.009), Clearance_Microsome_AZ (1,102, rank 1 MapLight+GNN 0.630 +- 0.010, runner-up MiniMol 0.628 +- 0.005) and VDss_Lombardo (1,130, rank 1 MapLight+GNN 0.713 +- 0.007, runner-up MapLight 0.707 +- 0.009). TDC itself notes Spearman is used for 'benchmarks that depend on factors beyond the chemical structure', i.e. these are rank-only, noisy, small-data PK endpoints where classical descriptor models already hold the top spots and the per-seed std is 0.005-0.025. The leaderboards carry no dates and the TDC repo's latest commits are April 2025. Open question: can a CPU-only model push the 5-seed mean Spearman above the listed rank-1 value on any of the four?

## Success criterion

Pick one of the four datasets. Success means 5 saved prediction files (seeds 1-5 from tdc.benchmark_group.admet_group, no re-splitting, official test order, manifest with sha256 of the test SMILES list) such that (a) the test split is byte-identical to the group's own, (b) the mean Spearman over the 5 seeds, recomputed by the skeptic through the group's own evaluate call, is strictly HIGHER (direction: max) than the rank-1 value in the live leaderboard table for that dataset at tdcommons.ai, re-fetched immediately before claiming, (c) the improvement exceeds max(listed rank-1 std, attacker's own 5-seed std) and is at least 0.010 in absolute Spearman, (d) a permutation test over test molecules (10,000 permutations) rejects equality with the listed rank-1 value at p<0.05 given the test size, and (e) training used only the official train_val rows for that seed, with any external data declared and shown to have zero stereo-stripped-InChIKey overlap with the test split.

## Partial wins

- {"id": "p1", "statement": "The full strict win on Clearance_Hepatocyte_AZ, where the gap between rank 1 (0.536) and rank 2 (0.498) is the largest of the four and the metric is most noise-dominated - verified live at https://tdcommons.ai/benchmark/admet_group/17clhepa/ ."}
- {"id": "p2", "statement": "A monotone-physiology result: a model whose predictions for one of the four endpoints are generated from a small, interpretable set of mechanistically motivated descriptors (<= 20 features, named) and still beat the live rank-1 Spearman under the same margin rule - a genuine 'small model beats leaderboard' claim, with the feature list and fitted signs reported."}
- {"id": "p3", "statement": "A cross-endpoint multi-task win: one single multi-task model (trained jointly on the official train_val splits of all four Spearman endpoints, same seed, no test rows) that beats the live rank-1 value on at least two of the four datasets simultaneously under the same margin rule."}

## Verification

As for the MAE leaderboards: PyTDC admet_group, group.get(<Benchmark>) for seeds 1-5, hash-check the test SMILES, load the attacker's 5 prediction vectors, call group.evaluate to get mean/std Spearman, apply the margin and permutation-test rules, then re-fetch the live leaderboard page and parse every listed Spearman. Spearman only needs the predicted ranking, so the skeptic must additionally confirm the prediction vector has no ties-by-construction tricks (e.g. constant blocks) that inflate the statistic, and should re-run the attacker's script for all 5 seeds (minutes to an hour on CPU at 667-1,130 molecules).

## Angles

- Optimise the metric that is actually scored: train with a differentiable rank surrogate (pairwise logistic / LambdaRank-style objective over train_val pairs, or SoftRank) instead of MSE. Spearman is invariant to monotone transforms, so rank-learning models have a structural advantage nobody on these four leaderboards appears to have used.
- Physiology-informed features for PK endpoints: fraction unbound proxies, ionisation state at pH 7.4 (acid/base/zwitterion class from pKa predictions), logD7.4, molecular volume, and the classic Lombardo VDss descriptor set; plus known mechanistic couplings (VDss and plasma protein binding, half-life ~ VDss/clearance) as engineered ratio features.
- CROSS-DOMAIN (ecology / rank-abundance statistics): model the endpoint as a rank-abundance curve and fit a copula between descriptor-space neighbourhood rank and label rank; copula/rank-transform regression is distribution-free and directly maximises monotone association, which is exactly Spearman.
- CROSS-DOMAIN (coding theory / ordinal ECOC): discretise the endpoint into K ordered bins, train binary classifiers for every threshold (and for Hadamard-coded bin subsets), and decode a rank score by minimum-distance decoding; threshold ensembles are robust to the heavy label noise of hepatocyte/microsome clearance assays.
- CROSS-DOMAIN (statistical physics / cavity-style resampling): bagged ensembles over scaffold-grouped bootstrap replicas with a Boltzmann weighting by out-of-fold Spearman, to pick a 'temperature' (regularisation) that maximises the rank statistic rather than squared error.
- CROSS-DOMAIN (signal processing): treat the 5 seeds as repeated measurements of one noisy channel and average predictions in rank space (Borda/Kemeny aggregation across seeds and across model families) rather than in label space; rank-space aggregation is the right estimator for a rank metric and is free.
- Transfer from the other three endpoints and from related public PK data (declared, InChIKey-filtered), since half-life, hepatocyte clearance and microsome clearance are mechanistically coupled; multi-task gradient boosting with endpoint one-hots is a few CPU-minutes.

## Pitfalls

- Seed and ties manipulation: with 135-243 test molecules, the Spearman standard error is roughly 0.05, far larger than the leaderboard's quoted 5-seed std; best-of-N-seeds or best-of-N-models reporting will cross any of these records by chance. Enforce the full 5-seed mean, the std-based margin and the permutation test.
- Scaffold leakage via pretrained descriptors: these endpoints are inside widely used ADMET training collections (ADMET-AI, ZairaChem, commercial descriptor servers), so a pretrained predictor may have seen the exact test molecules and their labels. Declared provenance plus InChIKey overlap checks are mandatory.
- Re-splitting / wrong split convention: the four benchmarks use TDC's scaffold split with a 20% test fraction produced by group.get(); regenerating it locally (different RDKit, different seed) silently changes the test set.
- Metric substitution: reporting Pearson or R^2 (or Spearman on log-transformed labels of a different unit) instead of the group's Spearman. Only the group's own evaluate output counts, and VDss/clearance unit conventions (L/kg, uL/min/1e6 cells, mL/min/g) must match TDC's.
- Measurement-duplicate leakage: Obach half-life and the AZ clearance sets contain the same drugs measured in multiple assays and the same chemical series across train/test; a 1-nearest-neighbour baseline already scores deceptively high, so any claim must beat an explicitly reported 1-NN-on-ECFP baseline as a sanity floor.
- Novelty trap: 2024-2026 submissions and papers (MiniMol, CFA, MapLight variants, TabPFN-style tabular models) may already report higher Spearman on these same splits than the stale table; the NOVELTY skeptic must check the last 24 months of literature naming the dataset.

## Sources

- https://tdcommons.ai/benchmark/admet_group/overview/
- https://tdcommons.ai/benchmark/admet_group/16halflife/
- https://tdcommons.ai/benchmark/admet_group/17clhepa/
- https://tdcommons.ai/benchmark/admet_group/18clmicro/
- https://tdcommons.ai/benchmark/admet_group/09vdss/
- Status source: https://tdcommons.ai/benchmark/admet_group/overview/

## Citations

- [Problem page](../../../../.raw/V3R1T4S/known-unknowns/drug-discovery/tdc-admet-excretion-spearman-leaderboards.md)
- [Bank entry](../../../../.raw/V3R1T4S/bank/targets.json) (id `tdc-admet-excretion-spearman-leaderboards`, commit `7dd4480`)

## Related Nodes

- [[V3R1T4S Drug discovery]]
- [[V3R1T4S]]
