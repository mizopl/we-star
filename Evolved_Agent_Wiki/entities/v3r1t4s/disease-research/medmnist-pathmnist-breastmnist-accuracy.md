---
id: v3r1t4s-medmnist-pathmnist-breastmnist-accuracy
type: entity
tags: [v3r1t4s, v3r1t4s/disease-research, kind/harvest]
inbound_links: 1
confidence: 0.8
last_ingested_sources: [".raw/V3R1T4S/bank/targets.json@7dd4480"]
status: "open"
priority: ""
notes: ""
category: disease-research
kind: harvest
tractability: 3
compute: "laptop-hours"
disclosure: open
status_checked: "2026-10-15"
---
# MedMNIST v2: beat the best published accuracy/AUC on the colorectal-histology (PathMNIST) or breast-ultrasound (BreastMNIST) benchmark

# Overview

> Bank id `medmnist-pathmnist-breastmnist-accuracy` · harvest · tractability 3 · laptop-hours · disclosure **open**
> Bank says open as of 2026-10-15. Statuses go stale — re-check the primary source before any work.

## Statement

MedMNIST v2 (Nature Scientific Data 2023) is a standardised, CC-BY, laptop-scale image benchmark with fixed train/validation/test splits and a shipped Evaluator. Two of its subsets are cancer tasks: PathMNIST (colorectal-cancer histology, 9 tissue classes, ~100k images) and BreastMNIST (breast ultrasound, benign vs malignant, 780 images). The official benchmark table on medmnist.com lists, at 28x28: PathMNIST best AUC 0.990 / ACC 0.911 (ResNet-50), with ResNet-18 at 0.983/0.907, auto-sklearn 0.934/0.716, AutoKeras 0.959/0.834, Google AutoML Vision 0.944/0.728; BreastMNIST best AUC 0.919 / ACC 0.863 (Google AutoML Vision and ResNet-18 respectively), with ResNet-18 (28) 0.901/0.863, ResNet-50 (28) 0.857/0.812. At 224x224 PathMNIST ResNet-18 reaches 0.989/0.909 and BreastMNIST 0.891/0.833. The 28x28 variants are tiny (the whole MedMNIST 2D collection is ~708k images in npz form, hosted on Zenodo record 10519652), CPU-trainable in minutes to hours, and the official numbers come from plain ResNets and AutoML tools - so a careful modern training recipe has real headroom, especially on PathMNIST ACC (0.911) where the AUC is already 0.99 and on BreastMNIST where n=780 makes the published numbers soft. The honest difficulty is novelty: MedMNIST+ follow-up work has published stronger numbers, so the criterion must beat the live official table AND the best value the NOVELTY skeptic finds in the literature. Published results already exceed the official table. For example, MedViT-S (Manzari et al., 2023) reports PathMNIST test ACC 0.942 (as tabulated in arXiv:2304.10054, fully supervised table, alongside AUC 0.993; confirmed in the PDF on 2026-10-15). Treat the official table as a floor, not the bar.

## Success criterion

Success means a model trained only on the official MedMNIST train split (with the official validation split used for model selection and early stopping, and the official test split untouched until the end), evaluated by the medmnist package's own Evaluator on the official test split at a declared resolution, whose test ACC is STRICTLY HIGHER than the best ACC listed for that task and resolution on https://medmnist.com/ (re-fetched live immediately before claiming) by at least 0.5 percentage points, where the bar is max(live medmnist.com value, best literature value at the same resolution, including MedViT and MedMNIST+) AND whose test AUC is not lower than the live best AUC for that task and resolution by more than 0.002; the value must also strictly exceed the best published ACC for the same task and resolution found by the NOVELTY skeptic in the last 24 months (including the MedMNIST+ line of work, arXiv:2404.15786 and its repository), by the same margin. Because BreastMNIST's test split has only ~156 images, a BreastMNIST claim additionally requires the result as mean +/- std over 5 seeds with the full seed-level Evaluator outputs, and the margin must exceed 2x that std. Deliverables: pinned medmnist version, data sha256 against the Zenodo distribution, training script and exact config, the Evaluator's standard result CSV for each seed, and a log showing the test split was read exactly once per seed. Any use of external pretraining must be declared and must not include any dataset derived from the same source images (for PathMNIST: NCT-CRC-HE; for BreastMNIST: the BUSI collection).

## Partial wins

- {"id": "p1", "statement": "Beat the live best ACC for PathMNIST at 28x28 by >= 0.5 points with a model of fewer than 1M parameters trained from scratch on CPU in under 2 hours, with the full protocol. A compute-efficiency frontier result, independently checkable from the Evaluator output and the training log."}
- {"id": "p2", "statement": "Beat the live best ACC on BreastMNIST at 28x28 by >= 1.0 point as a mean over 5 seeds with the margin exceeding 2x the seed std, with per-seed Evaluator outputs. The small test split makes the published single-run numbers fragile, so a properly seeded improvement is a genuine contribution."}
- {"id": "p3", "statement": "A reproducibility and variance audit of the official table: re-run the published ResNet-18 (28) recipe on PathMNIST and BreastMNIST for 5 seeds each and report the mean +/- std of AUC and ACC, establishing how large a difference is meaningful on each task. A benchmark-methodology result, reported as such, and a prerequisite for believing any small win."}

## Verification

Skeptic installs the pinned medmnist package in a clean venv, downloads the npz files from the official Zenodo distribution and compares sha256 against the attacker's manifest, loads the attacker's saved test predictions, and runs the package's own Evaluator (python -m medmnist evaluate --path=...) to recompute AUC and ACC on the official test split (minutes). Then re-trains the attacker's recipe from the training split for at least 2 seeds (laptop-minutes to laptop-hours at 28x28) and confirms the metrics land in the claimed range. Record side: re-fetch medmnist.com and read the live table for that task and resolution, and check the NOVELTY skeptic's literature list. Leakage audit: confirm no test image or label was used for augmentation search, early stopping, calibration, batch-norm statistics or ensembling weights; confirm any pretraining corpus excludes the source datasets; confirm the resolution claimed matches the data files used.

## Angles

- Conventional: a modern training recipe at 28x28 - cosine schedule, label smoothing, mixup/cutmix, test-time augmentation, stochastic weight averaging - against the official plain-ResNet baselines; most of the published gap on small-image medical benchmarks is recipe, not architecture.
- Conventional: colour/stain normalisation for PathMNIST (histology stain variation is the dominant nuisance factor) and intensity standardisation plus aggressive geometric augmentation for the tiny BreastMNIST.
- Cross-domain import (signal processing): at 28x28 a learned filter bank is overkill - use a scattering transform (wavelet scattering) or steerable-filter features plus a linear/SVM head, which is translation- and rotation-stable, has almost no parameters, and is extremely strong in the small-sample regime that BreastMNIST represents.
- Cross-domain import (compression): classify by minimum compressed-length / normalised-compression-distance against class-conditional dictionaries (learned sparse codes or PPM-style models), and use the compression margin as a confidence score for selective ensembling; parameter-free, CPU-only and genuinely different from a CNN's inductive bias.
- Cross-domain import (statistical physics / spin-glass ensembling): treat the ensemble-weighting problem as finding a low-energy configuration over model subsets with an explicit diversity term, solved by simulated annealing on validation predictions only; this is the principled version of ad-hoc ensembling and directly targets the last half-point of accuracy.
- Cross-domain import (coding theory): error-correcting output codes for PathMNIST's 9 classes, training binary classifiers on designed codeword splits and decoding by minimum distance, which often beats a single softmax head on small images with confusable classes.
- Calibration and decision-threshold work for BreastMNIST's binary task: AUC and ACC reward different things, and optimising the threshold on the validation split alone (never the test split) is legitimate and cheap.

## Pitfalls

- MedMNIST ships test LABELS locally, so leakage is the default failure mode: any use of the test split for early stopping, augmentation search, threshold choice, batch-norm recalibration or ensemble weighting produces a number that is not comparable to the table. The skeptic must verify the test split is read once per seed.
- Source-dataset pretraining leakage: PathMNIST derives from the NCT-CRC-HE colorectal histology collection and BreastMNIST from a public breast-ultrasound collection; pretraining on those sources (or on any derivative, including other MedMNIST subsets built from them) means the test images were seen in training. Any pretraining corpus must be declared and audited.
- BreastMNIST's test split is ~156 images, so one image is ~0.64 accuracy points. Single-run claims there are meaningless; 5 seeds and a 2x-std margin are mandatory, and even then the result is fragile and must be reported with its uncertainty.
- Resolution and version confusion: the 28, 64, 128 and 224 variants have separate published numbers and separate files; comparing a 224-trained model against the 28x28 table (or vice versa) is a false record. The MedMNIST+ line of work publishes stronger numbers than medmnist.com for several subsets, so the official table alone is NOT the frontier.
- Metric cherry-picking: PathMNIST's AUC is already 0.990, so an AUC-only claim is uninformative while an ACC-only claim can hide a degraded AUC. Both must be reported and the AUC must not regress materially.
- Clinical over-claiming: these are downsampled research images with fixed splits; a benchmark gain says nothing about diagnostic use and the write-up must state that explicitly.
- PathMNIST's test set (CRC-VAL-HE-7K) is from a different centre than training. Fitting stain normalisation, colour statistics or batch-norm statistics on test images is transductive leakage.

## Sources

- https://medmnist.com/
- https://github.com/MedMNIST/MedMNIST
- https://doi.org/10.5281/zenodo.10519652
- https://arxiv.org/abs/2404.15786
- https://arxiv.org/abs/2304.10054
- Status source: https://medmnist.com/

## Citations

- [Problem page](../../../../.raw/V3R1T4S/known-unknowns/disease-research/medmnist-pathmnist-breastmnist-accuracy.md)
- [Bank entry](../../../../.raw/V3R1T4S/bank/targets.json) (id `medmnist-pathmnist-breastmnist-accuracy`, commit `7dd4480`)

## Related Nodes

- [[V3R1T4S Disease research]]
- [[V3R1T4S]]
