---
id: v3r1t4s-isic2017-part3-melanoma-sk-mean-auc
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
# ISIC 2017 Part 3 (melanoma and seborrheic keratosis): beat the challenge-best mean AUC of 0.911 on the public 600-image test labels

# Overview

> Bank id `isic2017-part3-melanoma-sk-mean-auc` · standard · tractability 2.5 · laptop-hours · disclosure **open**
> Bank says open as of 2026-10-15. Statuses go stale — re-check the primary source before any work.

## Statement

ISIC 2017 Part 3 (Codella et al., ISBI 2018) scored two binary tasks on 600 dermoscopy test images: melanoma vs all and seborrheic keratosis vs all, ranked by the mean of the two ROC AUCs, with only 2,000 training and 150 validation images. The test ground truth is a plain public CSV (ISIC-2017_Test_v2_Part3_GroundTruth.csv) and the official scorer is isic-challenge-scoring. The live leaderboard is led by the Casio and Shinshu University joint team (Kazuhisa Matsunaga and colleagues) at 0.911, then Universidad Carlos III de Madrid (Ivan Gonzalez-Diaz) 0.910 and RECOD Titans 0.908, none flagged as using external data on the board. The small training set makes this a sharp test of data efficiency.

## Success criterion

Probability scores for all 600 official test images for both tasks, from a model trained only on the 2,000 official training images (validation images allowed for selection) and frozen before any test scoring, whose mean of melanoma AUC and seborrheic-keratosis AUC computed by the skeptic with isic-challenge-scoring against the public Part 3 test ground truth is STRICTLY HIGHER (direction: max) than the Part 3 leader on the live 2017 leaderboard (re-fetched live immediately before claiming) and than any official-test value without external data found by the NOVELTY check, by at least 0.005. Claims using external dermoscopy data are reported separately and must be deduplicated against the test images.

## Partial wins

- {"id": "p1", "statement": "Melanoma AUC alone above the best melanoma AUC on the leaderboard's per-category details, no external data."}
- {"id": "p2", "statement": "Mean AUC above 0.911 with an ImageNet-pretrained model fine-tuned on a laptop in under 6 hours, mean over 3 seeds."}

## Verification

Skeptic downloads the public Part 3 test ground truth CSV, runs isic-challenge-scoring classification on the claim, checks 600 ids, and audits external data for overlap with test images. Minutes.

## Angles

- Strong pretrained backbones plus heavy augmentation and multi-crop test-time averaging; most 2017 entries used ResNet-50-era models.
- Self-supervised pretraining on the 2,000 training images only (DINO-style) before fine-tuning, which keeps the no-external-data class.
- Cross-domain import (few-shot learning): prototype-based heads and episodic training suit a 2,000-image, two-task problem.
- Cross-domain import (radiology reader studies): AUC-optimising pairwise losses (as used for screening CAD) target the metric directly.
- Multi-task training of the two binary heads with the Part 1 lesion masks as an auxiliary task (masks are part of the official training data).

## Pitfalls

- Later ISIC releases (2018, 2019 training sets and the ISIC Archive) contain many 2017 test images with labels; any external data must be deduplicated by hash against the 600 test images.
- Test labels are public; selecting checkpoints or ensembles by test AUC is leakage.
- Some papers report melanoma AUC only, or a 3-class accuracy; only the mean of the two AUCs compares with the primary leaderboard metric.
- 600 images and roughly 117 melanomas mean AUC differences below about 0.01 are within noise; report bootstrap intervals.
- Research benchmark only; no diagnostic claim.

## Sources

- https://challenge.isic-archive.com/leaderboards/2017/
- https://isic-archive.s3.amazonaws.com/challenges/2017/ISIC-2017_Test_v2_Part3_GroundTruth.csv
- https://github.com/ImageMarkup/isic-challenge-scoring
- https://arxiv.org/abs/1710.05006
- Status source: https://challenge.isic-archive.com/leaderboards/2017/?task=44&group_by=team

## Citations

- [Problem page](../../../../.raw/V3R1T4S/known-unknowns/disease-research/isic2017-part3-melanoma-sk-mean-auc.md)
- [Bank entry](../../../../.raw/V3R1T4S/bank/targets.json) (id `isic2017-part3-melanoma-sk-mean-auc`, commit `7dd4480`)

## Related Nodes

- [[V3R1T4S Disease research]]
- [[V3R1T4S]]
