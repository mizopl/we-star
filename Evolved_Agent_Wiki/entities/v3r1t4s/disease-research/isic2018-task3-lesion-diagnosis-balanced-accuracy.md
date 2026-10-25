---
id: v3r1t4s-isic2018-task3-lesion-diagnosis-balanced-accuracy
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
# ISIC 2018 Task 3 (HAM10000 diagnosis, 7 classes): beat the best balanced multiclass accuracy on the 1,512-image public test ground truth

# Overview

> Bank id `isic2018-task3-lesion-diagnosis-balanced-accuracy` · standard · tractability 2.5 · laptop-hours · disclosure **open**
> Bank says open as of 2026-10-15. Statuses go stale — re-check the primary source before any work.

## Statement

ISIC 2018 Task 3 asked for a 7-way diagnosis (melanoma, nevus, basal cell carcinoma, actinic keratosis/Bowen's, benign keratosis, dermatofibroma, vascular) of dermoscopy images, training on the 10,015-image HAM10000 set (Tschandl, Rosendahl and Kittler 2018) and scoring by balanced multiclass accuracy (mean per-class recall) on 1,512 test images. The test ground truth is now a plain public download (ISIC2018_Task3_Test_GroundTruth.zip) and the official scorer is the isic-challenge-scoring package. The live leaderboard (challenge.isic-archive.com/leaderboards/2018, Task 3) is topped by MetaOptima Technology at 0.885 and DAISYLab (Nils Gessert, Alexander Schlaefer and colleagues) at 0.856, both using external data; the best entry without external data is the Medical Image Analysis Group of Sun Yat-sen University at 0.845. Mean per-class recall is dominated by the rare classes (dermatofibroma, vascular, actinic keratosis), so calibration and class weighting matter more than raw accuracy.

## Success criterion

A prediction CSV for all 1,512 official Task 3 test images, from a model trained only on the official training data (and the 193 official validation images) and frozen before any test scoring, whose balanced multiclass accuracy computed by the skeptic with isic-challenge-scoring against ISIC2018_Task3_Test_GroundTruth is STRICTLY HIGHER (direction: max) than the best value in its comparison class on the live Task 3 leaderboard (re-fetched live immediately before claiming): 0.845 class for no external data, 0.885 class if external data is declared; and higher than any official-test value for the same class found by the NOVELTY check, by at least 0.005.

## Partial wins

- {"id": "p1", "statement": "No external data: exceed 0.845 with a model trainable on a laptop in under 12 hours, mean over 3 seeds."}
- {"id": "p2", "statement": "Any data class: report per-class recall showing improvement on the three rarest classes without loss on melanoma recall relative to a reproduced strong baseline."}

## Verification

Skeptic downloads the public test ground truth, runs isic-challenge-scoring classification gt.csv pred.csv, checks image ids and count (1,512), and audits training data: every external image must be hash-deduplicated against the 1,512 test images. Minutes for scoring.

## Angles

- Optimise the metric: balanced accuracy rewards per-class recall, so tune class-prior offsets on validation (logit adjustment) rather than using argmax of a frequency-biased model.
- Modern ImageNet-pretrained backbones (ConvNeXt, EfficientNetV2) at 384-512 px with colour constancy (Shades of Gray) preprocessing, which several top 2018 teams used.
- Cross-domain import (long-tailed recognition in ecology / iNaturalist): balanced softmax and deferred re-weighting were built for exactly this class imbalance.
- Cross-domain import (ensemble forecasting): weight ensemble members by their validation per-class recall, as forecast hubs weight by skill per target.
- Use the lesion-grouping file to keep images of the same lesion together in internal validation splits, so model selection is honest.

## Pitfalls

- The ISIC Archive and later releases include the test images with diagnoses; any external data from the Archive (or HAM10000-derived sets such as DermaMNIST) must be deduplicated against the test set, or the result is leakage.
- Test labels are public: choosing thresholds, epochs or ensemble weights by test score invalidates the claim.
- Accuracy, AUC and balanced accuracy differ; many papers report accuracy (~0.9+) or use random splits of HAM10000, which do not compare with the leaderboard.
- External-data and no-external-data entries are separate classes on the leaderboard; compare within the declared class.
- A dermoscopy benchmark gain is not a validated diagnostic tool and must not be framed as one.

## Sources

- https://challenge.isic-archive.com/leaderboards/2018/
- https://challenge.isic-archive.com/data/
- https://isic-archive.s3.amazonaws.com/challenges/2018/ISIC2018_Task3_Test_GroundTruth.zip
- https://github.com/ImageMarkup/isic-challenge-scoring
- https://arxiv.org/abs/1902.03368
- Status source: https://challenge.isic-archive.com/leaderboards/2018/?task=47&group_by=team

## Citations

- [Problem page](../../../../.raw/V3R1T4S/known-unknowns/disease-research/isic2018-task3-lesion-diagnosis-balanced-accuracy.md)
- [Bank entry](../../../../.raw/V3R1T4S/bank/targets.json) (id `isic2018-task3-lesion-diagnosis-balanced-accuracy`, commit `7dd4480`)

## Related Nodes

- [[V3R1T4S Disease research]]
- [[V3R1T4S]]
