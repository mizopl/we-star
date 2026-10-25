---
id: v3r1t4s-tdc-admet-cyp-inhibition-auprc
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
# TDC ADMET CYP inhibition leaderboards (CYP2C9/CYP2D6/CYP3A4_Veith, 12-13k molecules, AUPRC): beat MapLight+GNN

# Overview

> Bank id `tdc-admet-cyp-inhibition-auprc` · harvest · tractability 3 · laptop-hours · disclosure **open**
> Bank says open as of 2026-10-15. Statuses go stale — re-check the primary source before any work.

## Statement

Three TDC ADMET benchmarks are large enough for real modelling yet still topped by a classical fingerprint+GNN hybrid: CYP2C9_Veith (12,092 molecules, AUPRC, rank 1 MapLight+GNN 0.859 +- 0.001, rank 2 ContextPred 0.839 +- 0.003), CYP2D6_Veith (13,130, AUPRC, rank 1 MapLight+GNN 0.790 +- 0.001, rank 2 ContextPred 0.739 +- 0.005) and CYP3A4_Veith (12,328, AUPRC, rank 1 MapLight+GNN 0.916 +- 0.000, rank 2 ContextPred 0.904 +- 0.002). The protocol is the group's scaffold split with 5 seeds and mean +- std from group.evaluate; the leaderboard pages are undated and the TDC repo's last commits are April 2025. CYP2D6 is the obvious target: rank 1 is 0.051 AUPRC above rank 2, the task is a well-defined qHTS inhibition readout from a single PubChem assay (Veith et al.), and 13k molecules with fingerprint features is minutes per fit on 10 CPU cores, so hundreds of model variants can be explored honestly inside train_val.

## Success criterion

Pick one of the three datasets. Success means 5 saved prediction files (seeds 1-5 from tdc.benchmark_group.admet_group, no re-splitting, official test order, probabilities in [0,1], manifest with sha256 of the test SMILES and labels) such that (a) the test split is byte-identical to the group's own, (b) the mean AUPRC over the 5 seeds, recomputed by the skeptic through the group's own evaluate call, is strictly HIGHER (direction: max) than the rank-1 AUPRC in the live leaderboard table for that dataset at tdcommons.ai, re-fetched immediately before claiming, (c) the improvement exceeds max(listed rank-1 std, attacker's own 5-seed std) and is at least 0.005 absolute, with a stratified 10,000-resample bootstrap over test molecules putting the attacker ahead in at least 95% of resamples, (d) fitting used only the official train_val rows of that seed, and (e) no external PubChem/ChEMBL record of the SAME assay endpoint for any test molecule was used, and every pretrained component is declared with provenance and shown to be free of the test molecules by stereo-stripped InChIKey. Transfer from the other two CYP inhibition datasets' train_val rows is allowed if declared and leakage-checked.

## Partial wins

- {"id": "p1", "statement": "The full strict win on CYP2D6_Veith (live rank 1 0.790), the weakest of the three records and the one with the largest rank-1-to-rank-2 gap."}
- {"id": "p2", "statement": "A reproduction-plus-margin result on any of the three: an independently re-implemented MapLight-style baseline (fingerprints + RDKit descriptors + gradient boosting, code and features reported) whose 5-seed mean AUPRC is within 0.005 of the live rank-1 value, PLUS an ablated addition that pushes it above the live rank-1 value under the margin rule."}
- {"id": "p3", "statement": "A low-prevalence-slice result: AUPRC restricted to the test molecules outside the 10 most populous Bemis-Murcko scaffolds (count reported, at least 500 molecules) that exceeds the pooled live rank-1 value, evidencing generalisation rather than scaffold memorisation."}

## Verification

PyTDC admet_group; group.get(<Benchmark>) for seeds 1-5; hash-check the test SMILES and labels against the manifest; load the attacker's 5 probability vectors; call group.evaluate for AUPRC mean/std; apply margin and bootstrap rules; verify the attacker's training rows are the official train_val rows and InChIKey-disjoint from test; re-fetch the live leaderboard page and parse every listed AUPRC. A full 5-seed retrain on 12-13k molecules with fingerprint features must be shown to run in under an hour on 10 CPU cores.

## Angles

- AUPRC-matched training: optimise average precision directly with a pairwise/listwise ranking loss restricted to positive-negative pairs, or use focal/asymmetric loss with prevalence-matched reweighting; log-loss-trained boosters leave AUPRC on the table at these class ratios.
- Multi-task across the three CYP inhibition datasets (train_val only): the same compounds and the same qHTS platform underlie all three, so a shared-representation multi-task booster or a stacked model that uses the other two endpoints' out-of-fold predictions as features is both legitimate and cheap.
- Feature-union stacking at scale: hashed ECFP4/6, FCFP, Avalon, MACCS, RDKit 2D, plus atom-pair and topological-torsion counts, each fed to its own LightGBM, then stacked by logistic regression on scaffold-grouped out-of-fold predictions - the straightforward way to pass a single MapLight+GNN entry.
- CROSS-DOMAIN (coding theory / ECOC over related endpoints): build codewords from the three inhibition labels plus the three substrate labels and decode the target bit by minimum-distance decoding, which extracts cross-endpoint redundancy as error correction.
- CROSS-DOMAIN (statistical physics / graph diffusion and belief propagation): construct a similarity graph over all molecules (structures only) and run label propagation from train_val labels as an additional transductive feature; diffusion handles scaffold-split shift better than i.i.d. learners and costs seconds.
- CROSS-DOMAIN (compression / NCD) as an ensemble member, and CROSS-DOMAIN (linguistics / SMILES BPE n-grams with tf-idf) as a second orthogonal view; both are fast enough at 13k molecules and decorrelate the errors of fingerprint models.
- Threshold-free calibration and rank aggregation across seeds: average predictions in rank space (Borda) across seeds and model families, which is the right aggregation for a ranking metric like AUPRC.

## Pitfalls

- Assay-source leakage: the Veith CYP inhibition labels come from a public PubChem qHTS assay, so downloading that assay (or using a model pretrained on it, including several public ADMET predictors) recovers test labels exactly. This is the single most likely false positive; provenance declarations and InChIKey checks are mandatory.
- Scaffold-split mis-tuning and re-splitting: hyper-parameters chosen under random CV are mis-set for a scaffold-split test set, and locally regenerated scaffold splits are incomparable. Use group.get() and scaffold-grouped internal CV.
- Metric swap: these three are scored by AUPRC (TDC uses AUPRC where positives are scarce). Reporting AUROC - which is much higher and less sensitive - as if it were the record is an easy, invalid 'win'.
- Seed cherry-picking against near-zero listed stds (0.000-0.003): the leaderboard value is a 5-seed mean, so the margin must exceed both stds and the bootstrap must pass; CYP3A4's 0.916 +- 0.000 in particular leaves no room for sloppy reporting.
- Duplicate/salt-form leakage across the scaffold boundary within TDC itself: report the stereo-stripped InChIKey overlap between train_val and test, and a 1-NN-on-ECFP baseline as a floor, so a 'win' is distinguishable from better memorisation.
- Novelty trap: MapLight, ADMET-AI, MiniMol, ZairaChem and 2024-2026 tabular/pretrained submissions report numbers on these exact splits; the NOVELTY skeptic must check the last 24 months for a higher published AUPRC on the same benchmark before any claim.

## Sources

- https://tdcommons.ai/benchmark/admet_group/overview/
- https://tdcommons.ai/benchmark/admet_group/10cyp2c9i/
- https://tdcommons.ai/benchmark/admet_group/11cyp2d6i/
- https://tdcommons.ai/benchmark/admet_group/12cyp3a4i/
- Status source: https://tdcommons.ai/benchmark/admet_group/overview/

## Citations

- [Problem page](../../../../.raw/V3R1T4S/known-unknowns/drug-discovery/tdc-admet-cyp-inhibition-auprc.md)
- [Bank entry](../../../../.raw/V3R1T4S/bank/targets.json) (id `tdc-admet-cyp-inhibition-auprc`, commit `7dd4480`)

## Related Nodes

- [[V3R1T4S Drug discovery]]
- [[V3R1T4S]]
