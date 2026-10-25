---
id: v3r1t4s-ptbxl-ecg-macro-auc-fold10
type: entity
tags: [v3r1t4s, v3r1t4s/disease-research, kind/standard]
inbound_links: 1
confidence: 0.8
last_ingested_sources: [".raw/V3R1T4S/bank/targets.json@7dd4480"]
status: "open"
priority: ""
notes: ""
category: disease-research
kind: standard
tractability: 2.5
compute: "laptop-hours"
disclosure: open
status_checked: "2026-10-15"
---
# PTB-XL ECG classification: beat the best published macro-AUC on the fixed fold-10 test set

# Overview

> Bank id `ptbxl-ecg-macro-auc-fold10` · standard · tractability 2.5 · laptop-hours · disclosure **open**
> Bank says open as of 2026-10-15. Statuses go stale — re-check the primary source before any work.

## Statement

PTB-XL (Wagner, Strodthoff et al., Scientific Data 2020; open access on PhysioNet, no registration) contains 21,799 12-lead 10-second ECGs with cardiologist statements and a recommended stratified 10-fold split (folds 1-8 train, 9 validation, 10 test). Strodthoff, Wagner, Schaeffter and Samek's benchmark (IEEE JBHI 2021) publishes a results table in the helme/ecg_ptbxl_benchmarking README for six label sets (all statements, diagnostic, diagnostic subclass, superclass, form, rhythm). The README table tops out at 0.925 (all), 0.937 (diagnostic), 0.930 (subclass and superclass), 0.899 (form), 0.957 (rhythm); the README table is the benchmark authors' own 2020 results, not a community leaderboard; the best published value we found for all statements is 0.9417 macro-AUC (4S4+1FC structured state-space model, Temesgen Mehari and Nils Strodthoff, arXiv:2211.07579). The form-statement task (morphology, 19 labels) is the least saturated. A 100 Hz version of the data is under 1 GB, so small 1D CNNs train on a laptop in about an hour.

## Success criterion

Predictions on PTB-XL fold 10 for one benchmark label set (all, diagnostic, subdiagnostic, superdiagnostic, form or rhythm), from a model trained on folds 1-8 and selected on fold 9 only, whose term-centric macro-AUC computed by the skeptic with utils.evaluate_experiment from the benchmark repository is STRICTLY HIGHER (direction: max) than the README leaderboard maximum (re-fetched live immediately before claiming) and every fold-10 value for that label set found by the NOVELTY check, by at least 0.003, and the improvement must hold as the mean over 5 training seeds (not the best seed).

## Partial wins

- {"id": "p1", "statement": "Form statements: mean over 5 seeds above the README best by >= 0.005 macro-AUC and above any literature value found."}
- {"id": "p2", "statement": "Match the 0.9417 all-statements state-space-model result within 0.002 with a model that trains on a laptop CPU in under 2 hours, with released code."}

## Verification

Skeptic downloads PTB-XL 1.0.3 from PhysioNet (open access), re-runs the attacker's training for the declared seeds with the benchmark's label preparation, computes macro-AUC on fold 10 with the repository's evaluation code, and checks the training code never loads fold-10 labels before final evaluation. Hours.

## Angles

- Structured state-space and dilated-convolution models are current best; combine them with test-time augmentation over random 2.5 s crops, which the benchmark's best entries already use, and average logits across crops and seeds.
- Cross-domain import (speech / audio tagging): multi-label audio tagging tricks (mixup between recordings, label smoothing per class, SpecAugment-style time masking per lead) transfer directly to 12-channel 1D signals.
- Cross-domain import (physics): use beat-synchronous averaging and vectorcardiogram (3D dipole) features as additional input channels; morphology ('form') labels are about beat shape, which averaging exposes.
- Hierarchical label structure: PTB-XL statements form a tree; train on all levels jointly with consistency losses so rare form statements borrow strength from their parents.
- Self-supervised pretraining on the unlabeled signal of folds 1-9 only (contrastive predictive coding), then fine-tune.

## Pitfalls

- Fold 10 has the cleanest labels (human-validated) and is the test set; using it for early stopping, threshold choice or model selection invalidates the result, as the README warns.
- Label-set mismatch: papers use 71, 44 or filtered subsets of statements; compare only like-for-like with the benchmark's label preparation (min-sample filtering included).
- Reporting the best of many seeds inflates AUC by about the size of the gaps; the criterion uses the 5-seed mean.
- Patient leakage: the recommended folds keep each patient in one fold; re-splitting randomly leaks patients and inflates scores.
- This is a research benchmark; a higher macro-AUC is not evidence of clinical usefulness and must not be framed as diagnostic advice.
- The README table is static (2020 models only); beating it is not a record. The bar is the best fold-10 value in the literature for the same label set, including the 2022-2023 state-space-model papers.

## Sources

- https://raw.githubusercontent.com/helme/ecg_ptbxl_benchmarking/master/README.md
- https://physionet.org/content/ptb-xl/1.0.3/
- https://github.com/helme/ecg_ptbxl_benchmarking
- https://arxiv.org/abs/2211.07579
- https://arxiv.org/abs/2004.13701
- https://arxiv.org/abs/2308.15291
- Status source: https://raw.githubusercontent.com/helme/ecg_ptbxl_benchmarking/master/README.md

## Citations

- [Problem page](../../../../.raw/V3R1T4S/known-unknowns/disease-research/ptbxl-ecg-macro-auc-fold10.md)
- [Bank entry](../../../../.raw/V3R1T4S/bank/targets.json) (id `ptbxl-ecg-macro-auc-fold10`, commit `7dd4480`)

## Related Nodes

- [[V3R1T4S Disease research]]
- [[V3R1T4S]]
