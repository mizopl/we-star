---
id: v3r1t4s-pcam-patchcamelyon-from-scratch-accuracy
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
# PatchCamelyon (lymph-node metastasis patches): beat 89.8% accuracy / 0.963 AUC on the official test split without external pretraining

# Overview

> Bank id `pcam-patchcamelyon-from-scratch-accuracy` · standard · tractability 2.5 · laptop-hours · disclosure **open**
> Bank says open as of 2026-10-15. Statuses go stale — re-check the primary source before any work.

## Statement

PatchCamelyon (Bastiaan Veeling, Jasper Linmans, Jim Winkens, Taco Cohen, Max Welling; MICCAI 2018) turns CAMELYON16 breast-cancer lymph-node slides into 327,680 96x96 H&E patches with binary labels (tumour in the centre 32x32), with fixed train (262,144) / validation (32,768) / test (32,768) splits whose test labels are public (Zenodo record 2546921, plain download). The benchmark table in the official repository README lists the rotation-equivariant GDensenet at 89.8% accuracy and 0.963 AUC. Despite its size, PCam has a well-known accuracy plateau around 90% for models trained from scratch, attributed to label noise and slide-level domain shift between splits; foundation models pretrained on large external pathology corpora report higher, but they belong to a different comparison class. The from-scratch cell is laptop-trainable and still informative.

## Success criterion

Test-split predictions for all 32,768 PCam test patches from a model trained from random initialisation (no pretrained weights, no external images) on the official train split, with selection on the official validation split only, whose accuracy is STRICTLY HIGHER (direction: max) than the best from-scratch accuracy in the README benchmark table at https://github.com/basveeling/pcam (re-fetched live immediately before claiming) and than any from-scratch official-test accuracy found by the NOVELTY check, by at least 0.5 percentage points, with AUC not below 0.963; reported as the mean over 3 seeds.

## Partial wins

- {"id": "p1", "statement": "Exceed 89.8% accuracy (3-seed mean) with a model under 1M parameters trained on a laptop CPU/MPS in under 8 hours."}
- {"id": "p2", "statement": "A documented analysis of the accuracy plateau: per-slide error breakdown using the official meta CSVs, showing which slides drive test errors (a methodology result)."}

## Verification

Skeptic downloads the test labels and meta CSV from Zenodo, checks MD5s against the README, computes accuracy and AUC from the claimed predictions, and re-trains one seed from the released script to confirm. Audits that no pretrained weights or external data were loaded. Hours for one retrain.

## Angles

- Rotation and reflection equivariance (p4m group convolutions, steerable filters) is the README baseline's key idea; combine it with modern training (long schedules, mixup, EMA weights).
- Stain augmentation and stain normalisation computed from the training split only, targeting the slide-level colour shift between splits.
- Cross-domain import (noisy-label learning from web-scale vision): co-teaching or small-loss selection to discount the noisy centre-region labels.
- Cross-domain import (texture analysis in materials science): wavelet scattering or gray-level co-occurrence features as a parameter-light second model for ensembling.
- Use the 64 px context ring explicitly: predict the centre label from a model that sees the whole 96 px patch with centre-weighted attention.

## Pitfalls

- Foundation-model or ImageNet-pretrained results are a different class; mixing classes produces a false record. Pathology foundation models may also have seen CAMELYON16 slides.
- Test labels are public; early stopping or seed selection on test accuracy is leakage.
- Patches from the same slide share appearance; validation-split tuning is the only honest selection, since the test slides differ.
- The README table is short and old; the NOVELTY check must cover from-scratch literature results on the official split before claiming.
- Patch classification on a curated benchmark is far from slide-level clinical diagnosis; frame results accordingly.

## Sources

- https://github.com/basveeling/pcam
- https://raw.githubusercontent.com/basveeling/pcam/master/README.md
- https://zenodo.org/records/2546921
- https://arxiv.org/abs/1806.03962
- Status source: https://raw.githubusercontent.com/basveeling/pcam/master/README.md

## Citations

- [Problem page](../../../../.raw/V3R1T4S/known-unknowns/disease-research/pcam-patchcamelyon-from-scratch-accuracy.md)
- [Bank entry](../../../../.raw/V3R1T4S/bank/targets.json) (id `pcam-patchcamelyon-from-scratch-accuracy`, commit `7dd4480`)

## Related Nodes

- [[V3R1T4S Disease research]]
- [[V3R1T4S]]
