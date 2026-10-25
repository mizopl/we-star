---
id: v3r1t4s-polaris-moleculeace-activity-cliff-mse
type: entity
tags: [v3r1t4s, v3r1t4s/drug-discovery, kind/harvest]
inbound_links: 1
confidence: 0.8
last_ingested_sources: [".raw/V3R1T4S/bank/targets.json@7dd4480"]
status: "CONFIRMED_SOLUTION"
priority: ""
notes: ""
category: drug-discovery
kind: harvest
tractability: 4
compute: "laptop-hours"
disclosure: open
status_checked: "2026-10-15"
---
# Polaris MoleculeACE (30 activity-cliff QSAR leaderboards): beat the single listed MSE on an official cliff split

# Overview

> Bank id `polaris-moleculeace-activity-cliff-mse` · harvest · tractability 4 · laptop-hours · disclosure **open**
> Bank says open as of 2026-10-15. Statuses go stale — re-check the primary source before any work.

## Statement

Polaris hosts 30 MoleculeACE benchmarks (molecularml/moleculeace-CHEMBL<id>-<Ki|EC50>), one per ChEMBL target from van Tilborg et al., 'Exposing the Limitations of Molecular Machine Learning with Activity Cliffs' (JCIM 2022). Each is a single-task regression of pKi/pEC50 from SMILES with a fixed activity-cliff-stratified train/test split (train 1,0xx-1,9xx, test 126-733 molecules) and main metric mean_squared_error (lower is better). As of 2026-10-13 nearly every one of the 30 leaderboards has exactly ONE entry, an auto-generated 'autosota-moleculeace-<slug>' submission (e.g. chembl2147-ki 0.311, chembl2835-ki 0.166, chembl264-ki 0.342, chembl4203-ki 0.732, chembl233-ki 0.576, chembl231-ki 0.530, chembl287-ki 0.503, chembl237-ec50 0.497); only chembl236-ki and chembl234-ki have 3 entries. The underlying data and the exact split are fully public: MoleculeACE ships one CSV per target (MoleculeACE/Data/benchmark_data/CHEMBL<id>_<Ki|EC50>.csv) with columns smiles, y, cliff_mol and split, and the Polaris train/test sizes match that split column exactly (verified for CHEMBL2147_Ki: 1162 train / 294 test = Polaris 1,162 / 294). So a laptop can train and score offline with no account. The open question per target: can a better descriptor/model combination lower the MSE below the listed best, especially on the cliff_mol subset where the MoleculeACE paper showed all methods degrade?

## Success criterion

Pick one named MoleculeACE benchmark (full Polaris slug). Success means a saved prediction file (one predicted y per test molecule, in the official test order, with the benchmark slug, the sha256 of the MoleculeACE CSV used, and the exact test-row indices) such that (a) the test set is EXACTLY the rows with split=='test' in the public MoleculeACE CSV for that target and the label column is the same 'y' column (log10-transformed nM) the Polaris benchmark uses, with the Polaris train/test counts from https://polarishub.io/api/v1/benchmark/molecularml/<slug> matching, (b) the skeptic's own sklearn.metrics.mean_squared_error on that file is strictly LOWER (direction: min) than EVERY mean_squared_error listed in the leaderboard table at https://polarishub.io/benchmarks/molecularml/<slug>, re-fetched live immediately before claiming, (c) the margin is at least 5% relative to the current best AND a paired bootstrap over test molecules (10,000 resamples, same resamples for both prediction sets where the attacker's and a reproduced baseline's predictions are available; otherwise 10,000 resamples of the attacker's squared errors) puts the attacker's MSE below the listed best in at least 95% of resamples, and (d) no test molecule, nor any molecule with the same InChIKey (ignoring stereo) as a test molecule, appeared in training, and no label for a test molecule was looked up from ChEMBL or any other source. The model must be fit on the official train split only; multi-target transfer is allowed only from OTHER MoleculeACE targets' train splits and must be declared, with the union checked for test-molecule leakage.

## Partial wins

- {"id": "p1", "statement": "The same strict improvement (live-refetched, >=5% relative, bootstrap-confirmed) on any ONE of the 28 single-entry benchmarks."}
- {"id": "p2", "statement": "A cliff-subset result: on one target, lower MSE than a faithfully reproduced MoleculeACE paper baseline (the repo's own best descriptor+model for that target, run by the attacker and reported with its code) restricted to the test molecules with cliff_mol==1, with at least 40 such molecules, while not being worse on the non-cliff subset."}
- {"id": "p3", "statement": "A sweep result: a single fixed model/featurisation recipe (no per-target tuning on test) that beats the listed best MSE on at least 10 of the 30 benchmarks simultaneously, each verified against its own live leaderboard table."}

## Verification

Skeptic downloads the MoleculeACE CSV for the target from raw.githubusercontent.com/molML/MoleculeACE/main/MoleculeACE/Data/benchmark_data/<file>.csv, checks sha256 against the manifest, selects split=='test', confirms the count matches nTestDatapoints from https://polarishub.io/api/v1/benchmark/molecularml/<slug>, loads the attacker's prediction vector, recomputes MSE with sklearn, runs the 10,000-resample bootstrap, canonicalises train and test SMILES with RDKit and asserts no InChIKey (stereo-stripped) overlap, then re-fetches the live Polaris leaderboard HTML and parses all listed mean_squared_error values. Optionally re-runs the attacker's training script end-to-end (minutes on CPU for ~1.5k molecules).

## Angles

- Classical kitchen-sink QSAR done properly: ECFP4/6 + FCFP + MACCS + RDKit 2D descriptors + Avalon, each with its own kernel, stacked by ridge/LightGBM with nested CV on the train split only; the MoleculeACE paper's own finding is that SVM on ECFP is near-SOTA, so the headroom is in careful ensembling and hyper-parameter search rather than architecture.
- Matched-molecular-pair (MMP) residual modelling: enumerate MMPs inside the train split, fit a transformation-effect table (sum of substituent delta-pKi), and predict test molecules as nearest-train-analogue plus learned transformation delta; this directly attacks the activity-cliff failure mode the benchmark was built around.
- CROSS-DOMAIN (compression-based similarity / information theory): replace fingerprint Tanimoto with a normalised compression distance between canonical SMILES (or between Morgan-fragment multisets) computed with zlib/bz2, and use it as a kernel in SVR / k-NN; NCD is a parameter-free similarity from Kolmogorov-complexity theory and makes different mistakes than fingerprints, so it adds ensemble diversity cheaply.
- CROSS-DOMAIN (coding theory / error-correcting output codes): discretise pKi into ordered bins, train a bank of binary classifiers against a Hadamard/BCH codebook over bin subsets, then decode to a continuous prediction by minimum-distance decoding; ECOC regression is noise-tolerant on small, label-noisy assay data and directly handles the bimodal cliff structure.
- CROSS-DOMAIN (statistical physics / replica averaging): train many weak learners at different 'temperatures' (bootstrap fraction, feature dropout, label-noise injection) and combine with a Boltzmann-weighted average whose weights come from out-of-fold likelihood; an explicit variance-bias thermostat tends to beat single tuned models on 100-700-molecule test sets.
- CROSS-DOMAIN (linguistics / n-gram language modelling): character n-gram and SMILES-subword (BPE) count features with tf-idf weighting and a linear model; cheap, orthogonal to graph fingerprints, and historically competitive on small ChEMBL regression sets.
- Conformal / quantile calibration: fit a conformalised quantile regressor and shrink predictions toward the train mean where the conformal interval is wide; MSE is quadratic, so shrinking uncertain predictions is a guaranteed-in-expectation MSE win on small test sets.
- Multi-task borrowing across the 30 MoleculeACE targets (shared ChEMBL assay families: three opioid-receptor sets, two histamine, two JAK, two serine-protease), as a multi-task LightGBM/ridge with target one-hot, with strict InChIKey de-duplication against the test split.

## Pitfalls

- Split leakage: the MoleculeACE split is cliff-stratified, NOT random; re-splitting randomly (or re-running the repo's splitter with a different seed) produces an easier test set and a meaningless number. The skeptic must take the test rows from the published CSV's split column and match the Polaris nTestDatapoints exactly.
- Label leakage from ChEMBL: the labels are public ChEMBL activities, so any model that queries ChEMBL, uses a ChEMBL-pretrained regression head covering the same assay, or uses a public 'autosota' pipeline that ingests ChEMBL can recover test labels. Any pretrained component must be declared with its training-set provenance and checked against the test InChIKeys.
- Stereo/salt duplicates: the same compound appears as different SMILES (salts, tautomers, stereo variants) across train and test; nearest-neighbour models then look brilliant. De-duplicate on stereo-stripped InChIKey, not on raw SMILES strings.
- Unit confusion: the CSV carries both 'y' (log10 of nM, the training label) and 'y [pEC50/pKi]' (shifted by 9). Scoring against the wrong column leaves MSE unchanged under a pure shift but breaks any mixing of the two, and reporting a number computed in the wrong unit against the leaderboard is a false positive.
- Test-set reuse / silent model selection: with 126-733 test molecules, the MSE standard error is roughly 0.05-0.15, so picking the best of many models by test MSE will 'beat' a 0.3-0.5 record by luck. All selection must be out-of-fold on train, the number of test evaluations must be reported, and the 5%-relative + bootstrap margin is mandatory.
- Beating only the auto-generated baseline: 'autosota-*' is a machine-produced submission, not the literature state of the art. The NOVELTY skeptic must also compare to the MoleculeACE paper's own published per-target RMSE/MSE table and to any newer activity-cliff paper (e.g. 2023-2026 arXiv/JCIM work citing MoleculeACE) for that same target and split.

## Sources

- https://polarishub.io/benchmarks/molecularml/moleculeace-chembl2147-ki
- https://polarishub.io/api/v1/benchmark/molecularml/moleculeace-chembl2147-ki
- https://raw.githubusercontent.com/molML/MoleculeACE/main/MoleculeACE/Data/benchmark_data/CHEMBL2147_Ki.csv
- https://github.com/molML/MoleculeACE
- https://doi.org/10.1021/acs.jcim.2c01073
- Status source: https://polarishub.io/benchmarks/molecularml/moleculeace-chembl2147-ki

## Citations

- [Problem page](../../../../.raw/V3R1T4S/known-unknowns/drug-discovery/polaris-moleculeace-activity-cliff-mse.md)
- [Bank entry](../../../../.raw/V3R1T4S/bank/targets.json) (id `polaris-moleculeace-activity-cliff-mse`, commit `7dd4480`)

## Related Nodes

- [[V3R1T4S Drug discovery]]
- [[V3R1T4S]]
