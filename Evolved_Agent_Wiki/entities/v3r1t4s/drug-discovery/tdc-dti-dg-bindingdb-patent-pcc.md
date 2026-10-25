---
id: v3r1t4s-tdc-dti-dg-bindingdb-patent-pcc
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
# TDC DTI Domain-Generalization (BindingDB patent-year split): beat the listed Pearson correlation

# Overview

> Bank id `tdc-dti-dg-bindingdb-patent-pcc` · harvest · tractability 3 · laptop-hours · disclosure **open**
> Bank says open as of 2026-10-15. Statuses go stale — re-check the primary source before any work.

## Statement

The TDC DTI_DG benchmark group has a single benchmark, BindingDB_Patent: drug-target affinity pairs from BindingDB that carry patent years, trained on 2013-2018 patents and tested on 2019-2021 patents, scored by Pearson correlation (PCC) - a temporal domain-generalization task, not a random split. The leaderboard has 9 entries, all from 2022-2023 era work: Otter-Knowledge-Ensemble 0.588 +- 0.002, OrangeBalls-ProtBertMorgan 0.538 +- 0.008, then the DomainBed-style baselines MMD 0.433, CORAL 0.432, ERM 0.427, MTL 0.425, GroupDRO 0.384, AndMASK 0.288, IRM 0.284. The gap between the best 'fancy' method and plain ERM is 0.16 PCC, i.e. most of the signal is in representation quality and not in the domain-generalization algorithm, and both leaders are protein-language-model + fingerprint feature pipelines whose features can be replaced by cheap alternatives (k-mer/CTD protein descriptors, Morgan fingerprints) that train on CPU with gradient boosting. The data arrive through PyTDC (group.get('BindingDB_Patent')), the split is fixed, and the leaderboard has had no new entry in years.

## Success criterion

Success means 5 saved prediction files (seeds 1-5 from tdc.BenchmarkGroup(name='DTI_DG_Group'), group.get('BindingDB_Patent'), no re-splitting, one predicted affinity per official test pair in the official order, manifest with sha256 of the test (SMILES, protein-sequence) key list and of the TDC data files) such that (a) the test set is byte-identical to the group's own, (b) the mean PCC over the 5 seeds, recomputed by the skeptic through group.evaluate, is strictly HIGHER (direction: max) than the best PCC listed in the live leaderboard table at https://tdcommons.ai/benchmark/dti_dg_group/bindingdb_patent/ , re-fetched immediately before claiming, (c) the improvement is at least 0.010 absolute and exceeds max(listed best std, attacker's 5-seed std), with a 10,000-resample bootstrap over test pairs putting the attacker above the listed best in at least 95% of resamples, (d) training used only the official train_val rows (2013-2018 patents) of the same seed, with validation carved out of train_val as the benchmark prescribes, and (e) no external affinity data for any test (drug, target) pair - in particular no BindingDB/ChEMBL/Papyrus record for a test pair, and no pretrained affinity model whose training data are undeclared - entered the pipeline; protein or molecule representation models pretrained on sequences/structures WITHOUT affinity labels are allowed if declared.

## Partial wins

- {"id": "p1", "statement": "A CPU-only pipeline (no protein language model, no GPU; e.g. Morgan fingerprints + protein k-mer/CTD descriptors + gradient boosting) whose 5-seed mean PCC beats the second-placed listed entry (live value, currently OrangeBalls-ProtBertMorgan 0.538) under the same margin and leakage rules - a 'cheap features beat heavy features' result."}
- {"id": "p2", "statement": "A domain-shift decomposition: per-test-year PCC (2019, 2020, 2021 separately, computed from the official test rows' patent years) for a model that beats the live best overall, plus the same breakdown for a reproduced ERM baseline, showing which year carries the gain - independently checkable and non-trivial since the leaderboard reports only the pooled value."}
- {"id": "p3", "statement": "An unseen-target result: PCC restricted to test pairs whose protein sequence never appears in train_val (count reported, at least 100 pairs) that beats the pooled live best value, demonstrating generalization to genuinely novel targets rather than to new ligands of known targets."}

## Verification

Skeptic pip-installs PyTDC, builds BenchmarkGroup(name='DTI_DG_Group'), calls group.get('BindingDB_Patent') for seeds 1-5, hashes the test key list against the manifest, loads the attacker's prediction vectors, calls group.evaluate to obtain PCC mean/std, runs the bootstrap, verifies no test (SMILES, sequence) pair appears in the attacker's training files, and re-fetches the leaderboard page to parse all 9+ listed PCC values. The attacker's full pipeline must be re-runnable on CPU in under a few hours, which is realistic for fingerprint + descriptor features with LightGBM on a few hundred thousand pairs.

## Angles

- Replace the protein encoder with cheap sequence statistics: amino-acid composition, dipeptide/tripeptide k-mer counts with tf-idf, CTD (composition-transition-distribution) descriptors, pseudo-amino-acid composition, and binding-site-agnostic physicochemical profiles; concatenate with Morgan/FCFP fingerprints and train LightGBM with target-group-aware CV. This is the single most likely CPU win against a PLM ensemble.
- Temporal domain adaptation done simply: sample-weight training pairs by patent recency (exponential recency weighting), or fit on the most recent years only, and calibrate the prediction distribution to the expected 2019-2021 affinity distribution; the leaderboard's own DomainBed baselines show elaborate invariance penalties (IRM 0.284) hurt, while trivial reweighting is untested.
- CROSS-DOMAIN (linguistics / n-gram language models and alignment): score drug-target compatibility by an alignment-based kernel between the target sequence and the nearest-neighbour targets in the training set (Smith-Waterman similarity), then predict by similarity-weighted transfer of the ligand's affinities on those neighbours - a translation-by-analogy estimator that handles unseen targets.
- CROSS-DOMAIN (compression / information distance): use normalised compression distance between protein sequences (and between SMILES) as a kernel for support-vector regression; NCD approximates an information-theoretic metric and needs no alignment, training or embedding model, and adds ensemble diversity for free.
- CROSS-DOMAIN (coding theory / ECOC and rank aggregation): discretise pAffinity into ordered bins with a Hadamard codebook of binary tasks, decode by minimum distance, and aggregate several decoders by Borda count; robust to the heavy label noise and unit heterogeneity of patent-derived affinities.
- CROSS-DOMAIN (statistical physics / free-energy additivity): model affinity as a sum of fragment-level contributions (ligand BRICS fragments x target residue-class indicators) with a sparse bilinear interaction term; group-lasso-regularised bilinear models are cheap and extrapolate better across time than black-box encoders.
- Ensemble across structurally different models (booster on fingerprints, bilinear fragment model, k-NN by sequence similarity) with weights fit on a strictly temporal inner validation split (e.g. train on 2013-2016, validate on 2017-2018) to mimic the real shift instead of random validation.

## Pitfalls

- Affinity-label leakage: BindingDB, ChEMBL and Papyrus all contain the same patent-derived measurements, so any external affinity table or affinity-pretrained model can contain the test pairs' labels verbatim. The leading leaderboard entries are knowledge-graph/PLM pipelines, so a 'win' built on an undeclared affinity-trained embedding is the most likely false positive here.
- Temporal split violation: using the test years' data (even unlabelled statistics such as the test ligand set's property distribution) for model selection breaks the domain-generalization premise. Validation must be carved from train_val, and the benchmark's 'training-domain validation' convention must be stated.
- Pair-level duplication: the same ligand-target pair recurs across patents with slightly different affinity values and units (Ki/Kd/IC50 mixed into one label); a model that memorises the ligand or the target identity scores well without generalising. Report PCC on unseen-ligand and unseen-target subsets alongside the pooled value.
- Metric choice: PCC on a heavy-tailed affinity distribution is dominated by a few extreme pairs; clipping, winsorising or dropping outlier test rows (or scoring on log vs linear scale inconsistently) can manufacture a gain. Score only through group.evaluate on all official test rows.
- Seed/variance illusion: the listed stds are tiny (0.002-0.021) but they measure training-seed variability, not test-set uncertainty; the bootstrap over test pairs is the binding constraint and must be reported.
- Novelty trap: the leaderboard is stale, and 2023-2026 DTI papers (Otter-Knowledge follow-ups, ESM-based affinity models, Papyrus-trained models) may already report higher PCC on this exact split; the NOVELTY skeptic must search for 'BindingDB_Patent' / 'DTI-DG' numbers from the last 24 months.

## Sources

- https://tdcommons.ai/benchmark/dti_dg_group/bindingdb_patent/
- https://tdcommons.ai/benchmark/dti_dg_group/overview/
- https://github.com/mims-harvard/TDC
- Status source: https://tdcommons.ai/benchmark/dti_dg_group/bindingdb_patent/

## Citations

- [Problem page](../../../../.raw/V3R1T4S/known-unknowns/drug-discovery/tdc-dti-dg-bindingdb-patent-pcc.md)
- [Bank entry](../../../../.raw/V3R1T4S/bank/targets.json) (id `tdc-dti-dg-bindingdb-patent-pcc`, commit `7dd4480`)

## Related Nodes

- [[V3R1T4S Drug discovery]]
- [[V3R1T4S]]
