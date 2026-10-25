---
id: v3r1t4s-isic2019-diagnosis-balanced-accuracy-with-unknown
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
# ISIC 2019 skin-lesion diagnosis with an 'unknown' class: beat the best balanced accuracy (0.636; 0.607 without external data) on the public test labels

# Overview

> Bank id `isic2019-diagnosis-balanced-accuracy-with-unknown` · harvest · tractability 3 · laptop-hours · disclosure **open**
> Bank says open as of 2026-10-15. Statuses go stale — re-check the primary source before any work.

## Statement

ISIC 2019 trained 8-class dermoscopy diagnosis on 25,331 images (HAM10000, BCN20000 and MSK) and tested on 8,238 images that also contain lesions of none of the 8 classes, which must be flagged as 'UNK'; the metric is balanced multiclass accuracy over 9 categories. The test ground truth is now a plain public CSV (ISIC_2019_Test_GroundTruth.csv) and the official scorer is isic-challenge-scoring. On the live leaderboard (images only) DAISYLab (Nils Gessert, Maximilian Nielsen, Mohsin Shaikh, Rene Werner, Alexander Schlaefer) leads with 0.636 using external data, and DysionAI leads the no-external-data class with 0.607; with metadata, DAISYLab 0.634 and Torus Actions 0.597. The open-set UNK requirement and the domain mix keep this well below the 0.85+ of ISIC 2018 Task 3, so it is genuinely unsaturated.

## Success criterion

A prediction CSV for all 8,238 official ISIC 2019 test images (9 columns including UNK), from a model trained only on the official 2019 training images (and optionally the official training metadata) and frozen before any test scoring, whose balanced multiclass accuracy computed by the skeptic with isic-challenge-scoring against ISIC_2019_Test_GroundTruth.csv is STRICTLY HIGHER (direction: max) than the best value in its comparison class (images-only or images+metadata; external data or not) on the live 2019 leaderboard (re-fetched live immediately before claiming) and than any official-test value found by the NOVELTY check, by at least 0.005.

## Partial wins

- {"id": "p1", "statement": "No external data, images only: exceed 0.607 with a laptop-trainable model, mean of 3 seeds."}
- {"id": "p2", "statement": "Improve UNK recall above every leaderboard entry's UNK recall (from the per-category details) while keeping overall balanced accuracy above 0.60, using an out-of-distribution detector calibrated only on training data."}

## Verification

Skeptic downloads the public ground-truth CSV, runs isic-challenge-scoring classification on the claimed CSV, checks 8,238 rows and image ids, and audits that no external image duplicates a test image (hash or ISIC id). Minutes.

## Angles

- Treat UNK as open-set recognition: energy scores or Mahalanobis distance on penultimate features, threshold set on held-out training classes (leave-one-class-out simulation), never on test.
- Domain-aware training: the three source collections differ in camera and crop; group-DRO or per-source normalisation reduces shortcut learning.
- Cross-domain import (anomaly detection in industrial inspection): PatchCore-style memory banks of training-patch features to flag lesions unlike any training class.
- Cross-domain import (selective classification in credit scoring): reject-option decision rules trading coverage for accuracy map directly onto when to output UNK.
- Exploit balanced accuracy: rare classes (DF, VASC, SCC) and UNK each count as much as nevus, so per-class bias correction on validation data is worth more than backbone size.

## Pitfalls

- BCN20000 and the ISIC Archive later published labelled images that include ISIC 2019 test images; any external data must be deduplicated against the test set or the claim is leakage.
- Public test labels make test-tuned UNK thresholds tempting; any threshold chosen by looking at test scores invalidates the result.
- Papers often report 8-class accuracy on random training splits without UNK; those numbers do not compare with the leaderboard.
- Images-only and images+metadata are separate tasks on the leaderboard; compare within the same task and external-data class.
- A benchmark gain in open-set skin-lesion classification is not clinical evidence; say so.

## Sources

- https://challenge.isic-archive.com/leaderboards/2019/
- https://challenge.isic-archive.com/data/
- https://isic-archive.s3.amazonaws.com/challenges/2019/ISIC_2019_Test_GroundTruth.csv
- https://github.com/ImageMarkup/isic-challenge-scoring
- https://arxiv.org/abs/1910.03910
- Status source: https://challenge.isic-archive.com/leaderboards/2019/

## Citations

- [Problem page](../../../../.raw/V3R1T4S/known-unknowns/disease-research/isic2019-diagnosis-balanced-accuracy-with-unknown.md)
- [Bank entry](../../../../.raw/V3R1T4S/bank/targets.json) (id `isic2019-diagnosis-balanced-accuracy-with-unknown`, commit `7dd4480`)

## Related Nodes

- [[V3R1T4S Disease research]]
- [[V3R1T4S]]
