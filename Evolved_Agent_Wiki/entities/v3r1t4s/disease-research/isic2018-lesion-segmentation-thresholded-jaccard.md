---
id: v3r1t4s-isic2018-lesion-segmentation-thresholded-jaccard
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
# ISIC 2018 skin-lesion segmentation: beat the challenge-winning thresholded Jaccard on the public test ground truth

# Overview

> Bank id `isic2018-lesion-segmentation-thresholded-jaccard` · standard · tractability 2.5 · laptop-hours · disclosure **open**
> Bank says open as of 2026-10-15. Statuses go stale — re-check the primary source before any work.

## Statement

ISIC 2018 Task 1 (lesion boundary segmentation, International Skin Imaging Collaboration; Codella et al. 2019) scored 66 teams on 1,000 dermoscopy test images with the thresholded Jaccard index: per-image Jaccard, set to 0 when below 0.65, then averaged. The final leaderboard (challenge.isic-archive.com/leaderboards/2018) is topped by team MT at 0.802, then Holidayburned and imsight at 0.799. The test images AND test ground-truth masks are now public as plain S3 downloads (ISIC2018_Task1_Test_GroundTruth.zip, 9.7 MB; inputs 2.4 GB; training 11 GB), so the official metric can be recomputed offline. Many later papers claim higher 'Jaccard' on ISIC 2018, but usually mean Jaccard (not thresholded) on random splits of the training set, which is not this benchmark.

## Success criterion

Binary masks for all 1,000 official ISIC 2018 Task 1 test images, from a model trained only on the 2,594 official training images (plus optionally the 100 validation images) and frozen before any test scoring, whose thresholded Jaccard (per-image Jaccard, values < 0.65 set to 0, mean over images) computed by the skeptic against ISIC2018_Task1_Test_GroundTruth.zip is STRICTLY HIGHER (direction: max) than the Task 1 leader on the live leaderboard (re-fetched live immediately before claiming) and than any thresholded-Jaccard value on the official test set found in later literature, by at least 0.005. No external dermoscopy segmentation data (e.g. ISIC 2016/2017 masks, PH2) unless declared, and a declared-external-data claim is reported separately (the leaderboard flags external data).

## Partial wins

- {"id": "p1", "statement": "Exceed 0.802 thresholded Jaccard with NO external data and a model trainable on a laptop (CPU/MPS) in under 12 hours."}
- {"id": "p2", "statement": "Reduce the number of test images below the 0.65 cutoff (failures) relative to a reproduced strong baseline, with an analysis of failure types; the thresholded metric is dominated by these failures."}

## Verification

Skeptic downloads ISIC2018_Task1_Test_GroundTruth.zip from the public ISIC S3 URL and scores the 1,000 claimed masks with the official scorer (pip install isic-challenge-scoring; isic-challenge-scoring segmentation <gt_dir> <pred_dir>). This reports the thresholded Jaccard used for ranking. The skeptic checks mask sizes against the original images, audits training code for any read of test masks, and hash-deduplicates every external training image against the 1,000 test images. Re-runs inference from released weights on a sample. Minutes for scoring.

## Angles

- Optimise the actual metric: thresholded Jaccard punishes outright failures, so add a failure detector (predicted-mask quality regression) and fall back to a second model on low-confidence images.
- Modern pretrained encoders (ImageNet ConvNeXt/EfficientNet U-Nets) at moderate resolution with heavy colour and hair augmentation, plus multi-scale test-time augmentation; most 2018 entries predate these.
- Cross-domain import (interactive segmentation / SAM-style promptable models): use an automatically generated box prompt from a coarse model and refine with a promptable segmenter, keeping training data rules.
- Cross-domain import (cartography): boundary smoothing with active contours or conditional random fields on the probability map, as several top 2018 teams did, now applied to a stronger base.
- Exploit the shape prior: lesions are mostly single connected blobs; keep the largest connected component and fill holes, which removes many sub-0.65 failures cheaply.

## Pitfalls

- Mean Jaccard is not thresholded Jaccard; many papers report the former (or Dice) and on random training-set splits. Only thresholded Jaccard on the official 1,000-image test set compares to the leaderboard.
- Test ground truth is public: choosing epochs, thresholds or TTA settings by test score is leakage. Use the 100-image validation set or a training split.
- Images and masks must be evaluated at original resolution; scoring downsampled masks inflates Jaccard.
- External data changes the comparison class; the leaderboard marks it, and claims must too.
- This is an image-analysis benchmark; it says nothing about clinical melanoma diagnosis and must not be framed that way.
- The ISIC Archive and later ISIC releases contain many Task 1 test images, some with lesion masks. Any external dermoscopy data, not only ISIC 2016/2017 masks, must be hash-deduplicated against the test images, or the claim is leakage.

## Sources

- https://challenge.isic-archive.com/leaderboards/2018/
- https://challenge.isic-archive.com/data/
- https://isic-archive.s3.amazonaws.com/challenges/2018/ISIC2018_Task1_Test_GroundTruth.zip
- https://github.com/ImageMarkup/isic-challenge-scoring
- Status source: https://challenge.isic-archive.com/leaderboards/2018/

## Citations

- [Problem page](../../../../.raw/V3R1T4S/known-unknowns/disease-research/isic2018-lesion-segmentation-thresholded-jaccard.md)
- [Bank entry](../../../../.raw/V3R1T4S/bank/targets.json) (id `isic2018-lesion-segmentation-thresholded-jaccard`, commit `7dd4480`)

## Related Nodes

- [[V3R1T4S Disease research]]
- [[V3R1T4S]]
