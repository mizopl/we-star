---
id: v3r1t4s-peer-fold-classification-superfamily-holdout
type: entity
tags: [v3r1t4s, v3r1t4s/biology, kind/harvest]
inbound_links: 1
confidence: 0.8
last_ingested_sources: [".raw/V3R1T4S/bank/targets.json@7dd4480"]
status: "open"
priority: ""
notes: ""
category: biology
kind: harvest
tractability: 3
compute: "laptop-hours"
disclosure: open
status_checked: "2026-10-15"
---
# PEER fold classification: beat the leaderboard's 32.1% accuracy on held-out SCOP superfamilies

# Overview

> Bank id `peer-fold-classification-superfamily-holdout` · harvest · tractability 3 · laptop-hours · disclosure **open**
> Bank says open as of 2026-10-15. Statuses go stale — re-check the primary source before any work.

## Statement

PEER (Minghao Xu and co-authors, TorchProtein/TorchDrug) maintains public leaderboards for protein-sequence tasks at torchprotein.ai/benchmark, with fixed splits, published dataset statistics and per-entry parameter counts. The hardest board is fold classification: entire SCOP 1.75 superfamilies are held out, so the test proteins have similar structures but dissimilar sequences to anything in training, and the model must name one of 1195 folding topologies. The top listed accuracy is 32.10% (+/- 0.72) for a multi-task ESM-1b with contact prediction, then 29.95% for frozen ESM-1b; a plain CNN and LSTM are far lower. Two thirds of the test set is still misclassified, with 12,312 training and 718 test proteins, which is small enough to train on a laptop CPU in hours with a modest model on top of cached embeddings. Related boards on the same page are also unsaturated (solubility 70.63%, subcellular localization 79.82%).

## Success criterion

Predicted fold labels for every protein in the PEER fold-classification test split, from a model trained only on the task's designated training set (plus publicly declared pretraining corpora that contain no SCOP 1.75 superfamily labels for the test superfamilies), whose test accuracy computed by the skeptic with the task's standard accuracy definition is STRICTLY HIGHER (direction: max) than the top accuracy listed on https://torchprotein.ai/benchmark for fold classification (re-fetched live immediately before claiming) by at least 1.5 percentage points, reported as mean and standard deviation over at least three seeds, and higher than any later published value found by the novelty check.

## Partial wins

- {"id": "p1", "statement": "Beat the top listed accuracy using a model of at most 150M parameters (the current leader uses about 659M), with the same seed protocol."}
- {"id": "p2", "statement": "Beat the top listed accuracy on the solubility board (70.63% as of 2026-10-15) or the subcellular localization board (79.82%) under the same rules, with all boards you ran reported."}
- {"id": "p3", "statement": "A published analysis, reproducible from the public split, of which of the 1195 folds account for the errors (for example singleton folds) and a method that fixes one named failure mode."}

## Verification

Skeptic obtains the PEER fold-classification split through the TorchProtein data loaders (public download, no registration), checks the prediction file covers each test protein exactly once, computes accuracy, reruns the attacker's training script from the released seed to reproduce the number within its stated standard deviation, and checks that no test superfamily appears in training. An hour or two.

## Angles

- Held-out superfamilies make this remote homology detection, so retrieval beats classification: embed training proteins, retrieve nearest neighbours and vote over their folds, which handles the 1195-way long tail better than a softmax head.
- Cross-domain import (few-shot vision): treat each fold as a class prototype and train with a metric-learning loss (ArcFace or supervised contrastive), standard for face recognition with thousands of rare classes.
- Cross-domain import (speech): fold topology is a global property of a long sequence; use attentive statistics pooling from speaker recognition rather than mean pooling of residue embeddings.
- Predict a cheap structural surrogate first (secondary-structure string, contact-map summary statistics) and classify on that, which is closer to what defines a fold than the raw sequence.
- Calibrate the long tail explicitly: with 1195 classes and 12,312 training proteins, many folds have a handful of examples, so class-balanced losses or logit adjustment may be worth more than a bigger encoder.

## Pitfalls

- Any structure-based tool that queries a database containing the test proteins' own structures (or their superfamily members) breaks the held-out-superfamily design; declare every external database and check its contents.
- The leaderboard reports mean and standard deviation over seeds; a single lucky seed above the bar is not a win, hence the three-seed requirement.
- Multi-task entries on this board use extra supervision (contact prediction, secondary structure) that is listed in the 'external data' column; a comparison must respect what each entry was allowed to use.
- The page hosts several boards with different metrics; quoting a solubility accuracy against the fold-classification bar is a category error.
- Leaderboards hosted on a project site can go stale, so the novelty check must search the literature for higher published numbers on the same split before any claim.

## Sources

- https://torchprotein.ai/benchmark
- https://github.com/DeepGraphLearning/PEER_Benchmark
- https://arxiv.org/abs/2206.02096
- Status source: https://torchprotein.ai/benchmark

## Citations

- [Problem page](../../../../.raw/V3R1T4S/known-unknowns/biology/peer-fold-classification-superfamily-holdout.md)
- [Bank entry](../../../../.raw/V3R1T4S/bank/targets.json) (id `peer-fold-classification-superfamily-holdout`, commit `7dd4480`)

## Related Nodes

- [[V3R1T4S Biology]]
- [[V3R1T4S]]
