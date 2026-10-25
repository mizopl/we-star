---
id: v3r1t4s-dream-random-promoter-yeast-expression
type: entity
tags: [v3r1t4s, v3r1t4s/biology, kind/standard]
inbound_links: 1
confidence: 0.8
last_ingested_sources: [".raw/V3R1T4S/bank/targets.json@7dd4480"]
status: "open"
priority: ""
notes: ""
category: biology
kind: standard
tractability: 2
compute: "laptop-days (GPU shortens training; scoring is minutes)"
disclosure: open
status_checked: "2026-10-15"
---
# Random Promoter DREAM Challenge: beat the best published Pearson/Spearman score for predicting yeast expression from promoter sequence

# Overview

> Bank id `dream-random-promoter-yeast-expression` · standard · tractability 2 · laptop-days (GPU shortens training; scoring is minutes) · disclosure **open**
> Bank says open as of 2026-10-15. Statuses go stale — re-check the primary source before any work.

## Statement

The Random Promoter DREAM Challenge 2022 (Rafi, de Boer and the DREAM consortium, Nature Biotechnology 2024) released 6.7 million random 80-bp yeast promoter sequences with measured expression, and a 71,103-sequence test set with designed subsets (high, low, native yeast, random, challenging, SNV pairs, motif perturbation, motif tiling). Scores are a weighted 'Pearson score' and 'Spearman score' across subsets. The test labels and the evaluation notebook are now public on Zenodo (record 10633252), together with the weights of the Prix Fixe-optimised DREAM-CNN, DREAM-RNN and DREAM-Attn models reported as improving on the individual challenge solutions (Autosome.org, BHI, Unlock_DNA) in Rafi et al. 2024, to be re-scored by the claimant rather than taken on trust. The open question is whether a better model, or a principled ensemble, beats the best released model on the official scoring.

## Success criterion

Predictions for all sequences in the official test file whose Pearson score AND Spearman score, computed by the skeptic with the challenge's Evaluation.ipynb from Zenodo record 10633252 (re-fetched live immediately before claiming), are STRICTLY HIGHER (direction: max) than the best value reported in Rafi et al. 2024 and than the best released Prix Fixe model re-scored the same way, by at least 0.002 on each score. The model may be trained only on train.txt (and val.txt); hyperparameters and ensemble weights must be chosen without the test labels.

## Partial wins

- {"id": "p1", "statement": "Beat the best released model on the SNV subset (Pearson on predicted vs measured expression differences), the subset most relevant to variant effects, under the same rules."}
- {"id": "p2", "statement": "A leakage-free ensemble of the three released Prix Fixe models (weights fitted on val.txt only) that beats each individual released model on both overall scores, with an honest note on whether this exceeds the paper's best."}

## Verification

Skeptic downloads test sequences, the filtered test labels and Evaluation.ipynb from Zenodo, scores the attacker's prediction file (one value per test sequence, order checked by sequence id), re-scores the released Prix Fixe weights the same way, and checks training logs show no read of the test label file. Minutes for scoring; retraining is the attacker's cost.

## Angles

- Start from the released DREAM-CNN/RNN weights and ensemble or distil them; ensembling well-trained but architecturally different models is the cheapest gain and needs only CPU inference.
- Copy the winning idea and push it: Autosome.org recast regression as soft classification over expression bins, mirroring how the measurement was made (sorting cells into bins); model the full binning likelihood (as in MAUDE) instead of a softmax over bins.
- Cross-domain import (speech recognition): train on noisy labels with a known measurement channel; use the experiment's sort-bin noise model as a differentiable observation layer (like CTC handles alignment noise).
- Cross-domain import (physics-informed models): a thermodynamic layer where predicted expression is a Boltzmann-weighted occupancy of learned transcription-factor motifs, giving interpretable features that generalise to the native and SNV subsets.
- Use reverse-complement equivariant convolutions and test-time augmentation over strand and small flank runs.

## Pitfalls

- The test labels are public on Zenodo: selecting a checkpoint or ensemble weight with them is leakage. Use val.txt only.
- The challenge weighted Pearson score uses r^2 on some subsets and differences for SNV pairs; any home-made metric will disagree. Use the official notebook only.
- Sequences must be scored with the same fixed flanks the challenge used; dropping or changing flanks silently changes inputs.
- Matching rather than beating the released models within noise is not a result; the 0.002 margin is small, so report bootstrap intervals over test sequences.

## Sources

- https://zenodo.org/records/10633252
- https://github.com/de-Boer-Lab/random-promoter-dream-challenge-2022
- https://www.ebi.ac.uk/europepmc/webservices/rest/PMC12339383/fullTextXML
- Status source: https://zenodo.org/records/10633252

## Citations

- [Problem page](../../../../.raw/V3R1T4S/known-unknowns/biology/dream-random-promoter-yeast-expression.md)
- [Bank entry](../../../../.raw/V3R1T4S/bank/targets.json) (id `dream-random-promoter-yeast-expression`, commit `7dd4480`)

## Related Nodes

- [[V3R1T4S Biology]]
- [[V3R1T4S]]
