---
id: v3r1t4s-luna16-nodule-detection-cpm-10fold
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
tractability: 2
compute: "laptop-days"
disclosure: open
status_checked: "2026-10-15"
---
# LUNA16 lung-nodule detection and false-positive reduction: beat the best CPM (0.951 detection, 0.968 false-positive reduction) under the official 10-fold protocol

# Overview

> Bank id `luna16-nodule-detection-cpm-10fold` · standard · tractability 2 · laptop-days · disclosure **open**
> Bank says open as of 2026-10-15. Statuses go stale — re-check the primary source before any work.

## Statement

LUNA16 (Arnaud Setio, Colin Jacobs and co-authors, Medical Image Analysis 2017) is the standard benchmark for lung-cancer screening CT computer-aided detection: 888 LIDC-IDRI CT scans in 10 fixed subsets, 1,186 reference nodules (>= 3 mm, accepted by at least 3 of 4 radiologists), an official evaluation script, and the Competition Performance Metric (CPM: mean sensitivity at 1/8, 1/4, 1/2, 1, 2, 4 and 8 false positives per scan). Methods are evaluated by 10-fold cross-validation over the fixed subsets. The results page lists PAtech at 0.951 for full detection and PATech at 0.968 for the false-positive-reduction track (classifying the 754,975 supplied candidates in candidates_V2). Data, annotations, candidates and the evaluation script are on Zenodo under CC BY 4.0 (about 120 GB of scans).

## Success criterion

Per-subset prediction CSVs for all 888 scans, each subset predicted by a model that never saw that subset's scans or labels in training or selection (strict 10-fold over the official subsets), whose CPM computed by the skeptic with the official LUNA16 evaluation script (with annotations_excluded handling) is STRICTLY HIGHER (direction: max) than the top score of the same track on https://luna16.grand-challenge.org/Results/ (re-fetched live immediately before claiming) and than any strict-10-fold value for that track found by the NOVELTY check, by at least 0.005.

## Partial wins

- {"id": "p1", "statement": "False-positive-reduction track: CPM above 0.968 on candidates_V2 with a model small enough to train all 10 folds on a laptop in under 3 days."}
- {"id": "p2", "statement": "Detection track: CPM above 0.951 with all 10 folds released, or a documented reproduction showing that a published claim above 0.951 does or does not hold under the strict protocol."}

## Verification

Skeptic downloads annotations.csv, annotations_excluded and the evaluation script from Zenodo, runs the script on the merged predictions, and spot-checks 1-2 folds by retraining or by running released weights on that subset. Audits fold assignment (subset id per scan) and that no fold's model was tuned on its own test subset. Hours for scoring and audit; days for a full retrain.

## Angles

- False-positive reduction is laptop-friendly: extract 3D patches at candidate locations once (small disk footprint), then train compact 3D CNNs or 2.5D multi-view networks per fold.
- Cross-domain import (particle physics triggers): cascaded classifiers with increasing cost, as used in detector triggers, cut most easy negatives with a cheap model before an expensive one.
- Cross-domain import (astronomy point-source detection): matched filters and scale-space blob detectors on lung-masked CT give a strong, interpretable candidate generator.
- Ensembles across folds of different architectures and input scales, combined by rank averaging, typically add the last 0.005-0.01 CPM.
- Hard-negative mining focused on vessels and fissures, which dominate false positives at 1/8 and 1/4 FPs per scan where the CPM is weakest.

## Pitfalls

- All labels are public and evaluation is self-run cross-validation, so leakage is easy: any use of a fold's scans for training, early stopping or threshold choice for that fold's predictions invalidates the claim.
- Many papers re-split LIDC-IDRI or use different nodule definitions (all nodules, >= 1 radiologist); only the official 1,186-nodule reference and script compare with the results page.
- Detection and false-positive-reduction tracks are different tasks with different bars; do not compare a candidate classifier with the detection board.
- Pretraining on LIDC-IDRI-derived data (including public nodule datasets built from it) leaks test scans; declare and exclude.
- The results page closed to new entries years ago, so later literature claims must be checked; CPM gains do not imply screening benefit.

## Sources

- https://luna16.grand-challenge.org/Results/
- https://luna16.grand-challenge.org/Evaluation/
- https://zenodo.org/records/3723295
- https://zenodo.org/records/4121926
- https://arxiv.org/abs/1612.08012
- Status source: https://luna16.grand-challenge.org/Results/

## Citations

- [Problem page](../../../../.raw/V3R1T4S/known-unknowns/disease-research/luna16-nodule-detection-cpm-10fold.md)
- [Bank entry](../../../../.raw/V3R1T4S/bank/targets.json) (id `luna16-nodule-detection-cpm-10fold`, commit `7dd4480`)

## Related Nodes

- [[V3R1T4S Disease research]]
- [[V3R1T4S]]
