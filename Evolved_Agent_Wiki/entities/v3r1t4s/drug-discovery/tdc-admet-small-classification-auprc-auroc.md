---
id: v3r1t4s-tdc-admet-small-classification-auprc-auroc
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
# TDC ADMET small classification leaderboards (CYP substrates, hERG, DILI, Bioavailability): beat rank 1 on the official scaffold split

# Overview

> Bank id `tdc-admet-small-classification-auprc-auroc` · harvest · tractability 3 · laptop-hours · disclosure **open**
> Bank says open as of 2026-10-15. Statuses go stale — re-check the primary source before any work.

## Statement

Six TDC ADMET classification benchmarks have fewer than 700 molecules, i.e. 95-135 test molecules, and their rank-1 scores sit far from ceiling: CYP2C9_Substrate_CarbonMangels (666 molecules, AUPRC, rank 1 MiniMol 0.474 +- 0.025, runner-up ZairaChem 0.441 +- 0.033), CYP2D6_Substrate_CarbonMangels (664, AUPRC, rank 1 ContextPred 0.736 +- 0.024), CYP3A4_Substrate_CarbonMangels (667, AUROC, rank 1 CFA 0.667 +- 0.019, runner-up MiniMol 0.663 +- 0.008), hERG (648, AUROC, rank 1 MapLight+GNN 0.880 +- 0.002, runner-up CFA 0.875 +- 0.014), DILI (475, AUROC, rank 1 MiniMol 0.956 +- 0.006) and Bioavailability_Ma (640, AUROC, rank 1 MiniMol 0.942 +- 0.002). CYP3A4_Substrate at AUROC 0.667 and CYP2C9_Substrate at AUPRC 0.474 are barely above chance-plus, which is the signature of an under-attacked task rather than a solved one. The protocol is TDC's: official scaffold split from group.get(), 5 seeds, mean +- std from group.evaluate. Leaderboard pages are undated; the TDC repo's last commits are April 2025.

## Success criterion

Pick one dataset. Success means 5 saved prediction files (seeds 1-5 from tdc.benchmark_group.admet_group, no re-splitting, official test order, predicted probabilities in [0,1], manifest with sha256 of the test SMILES list and labels) such that (a) the test split is byte-identical to the group's own, (b) the mean of the dataset's OWN metric (AUPRC for the CYP2C9/CYP2D6 substrate sets, AUROC for CYP3A4_Substrate, hERG, DILI, Bioavailability) over the 5 seeds, recomputed by the skeptic through the group's evaluate call, is strictly HIGHER (direction: max) than the rank-1 value in the live leaderboard table for that dataset, re-fetched immediately before claiming, (c) the improvement exceeds max(listed rank-1 std, attacker's own 5-seed std) and is at least 0.015 absolute, (d) a stratified bootstrap over test molecules (10,000 resamples) puts the attacker's metric above the listed rank-1 value in at least 95% of resamples, and (e) only the official train_val rows of the same seed were used for fitting and threshold-free probabilities were produced (no test-label-dependent calibration), with any external data declared and InChIKey-disjoint from the test split.

## Partial wins

- {"id": "p1", "statement": "The full strict win on CYP3A4_Substrate_CarbonMangels (AUROC, live rank 1 0.667) - the weakest absolute record in the whole ADMET group."}
- {"id": "p2", "statement": "The full strict win on CYP2C9_Substrate_CarbonMangels (AUPRC, live rank 1 0.474), where the positive class is small and the listed std is 0.025, so the bootstrap and 5-seed rules must both pass."}
- {"id": "p3", "statement": "A calibration-only result: using a published or re-implemented baseline's raw scores, show that a declared post-hoc transform fit only on train_val out-of-fold predictions (e.g. isotonic/Platt or a prevalence-corrected ranking) raises the 5-seed AUPRC of that baseline above the live rank-1 value on one of the two AUPRC benchmarks, with the untransformed baseline reported alongside."}

## Verification

PyTDC admet_group; group.get(<Benchmark>) for seeds 1-5; hash-check the test SMILES and labels; load the attacker's 5 probability vectors; call group.evaluate to obtain the dataset's own metric mean/std; apply margin and bootstrap rules; re-fetch the live leaderboard page and parse every listed value. All six datasets are <700 molecules, so the skeptic can re-run the attacker's whole 5-seed pipeline in minutes on CPU and confirm the numbers from scratch.

## Angles

- Metric-matched training: for the AUPRC benchmarks optimise a precision-recall surrogate (weighted/focal loss, AP-surrogate, or direct ranking loss on positive-negative pairs) rather than log-loss; with 30-60 positives in the test set, ranking the positives above the ambiguous middle is what moves AUPRC.
- Substrate-specific mechanistic features: CYP substrate recognition depends on site-of-metabolism accessibility, so add SMARTS counts for known soft spots (N-dealkylation, O-demethylation, aromatic hydroxylation motifs), partial charges on candidate atoms, and SASA-like proxies from a single fast 3D embedding - cheap on 667 molecules and orthogonal to fingerprints.
- CROSS-DOMAIN (linguistics / morphological parsing): parse SMILES into substituent 'morphemes' (BRICS/RECAP fragments) and build a fragment-presence language model per class, scoring molecules by log-likelihood ratio - a naive-Bayes-over-fragments classifier that is strong exactly when data are tiny and labels noisy.
- CROSS-DOMAIN (compression / NCD similarity): k-NN and kernel SVM with a normalised-compression-distance kernel over canonical SMILES; parameter-free, uncorrelated with ECFP Tanimoto, and ideal as a diversity component in a small-data ensemble.
- CROSS-DOMAIN (coding theory / error-correcting output codes over related endpoints): train the three CYP-substrate tasks plus the three CYP-inhibition tasks as a 6-bit codeword per molecule and decode the target bit by minimum-distance decoding; inhibition data (12k molecules each) act as a large, legitimate auxiliary signal for the 667-molecule substrate tasks.
- CROSS-DOMAIN (statistical physics / belief propagation on similarity graphs): build a molecular similarity graph over train_val+test structures (structures only, no test labels) and run label propagation / graph-diffusion from the train labels; transductive diffusion is a well-matched estimator for scaffold-split tasks and runs in seconds.
- Variance control: with 95-135 test molecules, the main lever is reducing prediction variance - average over many featurisations and many scaffold-grouped folds, and shrink probabilities toward the train prevalence where out-of-fold uncertainty is high.

## Pitfalls

- Tiny-test-set luck: 95-135 test molecules with 20-40 positives means the AUPRC/AUROC standard error is roughly 0.04-0.08. Any search over models selected on test will 'beat' these records; only out-of-fold selection on train_val plus the 5-seed, std-margin and bootstrap rules can distinguish signal from noise.
- Metric swap: CYP2C9/CYP2D6 substrate are AUPRC while CYP3A4 substrate, hERG, DILI and Bioavailability are AUROC. Reporting AUROC where AUPRC is scored (or vice versa) looks like a large gain and is a pure artefact; use the group's own evaluate output.
- Scaffold leakage via pretrained models and public AutoML pipelines: hERG, DILI and the CarbonMangels CYP sets are standard ingredients of ADMET pretraining collections, so a pretrained encoder may have memorised the test molecules' labels. Provenance must be declared and InChIKey overlap with test checked.
- Label-noise/duplicate traps: the CarbonMangels substrate sets and the hERG set contain near-duplicate structures and some contradictory labels across sources; de-duplicating or 'cleaning' the OFFICIAL test rows (or dropping hard test molecules) invalidates the comparison entirely.
- Threshold leakage: choosing a probability threshold, calibrating, or selecting an ensemble weight using the test labels. All calibration must be fit on train_val out-of-fold predictions only, and AUROC/AUPRC must be computed from raw scores.
- Novelty trap: MiniMol, CFA, ZairaChem, ContextPred and newer 2024-2026 tabular/pretrained submissions report numbers on these same splits; a claim must beat the live rank-1 value AND any higher number published for the same benchmark in the last 24 months.

## Sources

- https://tdcommons.ai/benchmark/admet_group/overview/
- https://tdcommons.ai/benchmark/admet_group/13cyp2c9s/
- https://tdcommons.ai/benchmark/admet_group/14cyp2d6s/
- https://tdcommons.ai/benchmark/admet_group/15cyp3a4s/
- https://tdcommons.ai/benchmark/admet_group/20herg/
- https://tdcommons.ai/benchmark/admet_group/22dili/
- https://tdcommons.ai/benchmark/admet_group/04bioav/
- Status source: https://tdcommons.ai/benchmark/admet_group/overview/

## Citations

- [Problem page](../../../../.raw/V3R1T4S/known-unknowns/drug-discovery/tdc-admet-small-classification-auprc-auroc.md)
- [Bank entry](../../../../.raw/V3R1T4S/bank/targets.json) (id `tdc-admet-small-classification-auprc-auroc`, commit `7dd4480`)

## Related Nodes

- [[V3R1T4S Drug discovery]]
- [[V3R1T4S]]
