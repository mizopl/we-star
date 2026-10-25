---
id: v3r1t4s-vesuvius-profilometer-ink-dice
type: entity
tags: [v3r1t4s, v3r1t4s/herculaneum-scrolls, kind/harvest]
inbound_links: 1
confidence: 0.8
last_ingested_sources: [".raw/V3R1T4S/bank/targets.json@7dd4480"]
status: "open"
priority: ""
notes: ""
category: herculaneum-scrolls
kind: harvest
tractability: 2.5
compute: "laptop-hours"
disclosure: commit-only
status_checked: "2026-10-08"
---
# Herculaneum optical-profilometry ink segmentation: beat the Sci. Rep. 2026 nnU-Net held-out Dice on the shipped 5-fold splits of scrollprize/profilometer, topography only

# Overview

> Bank id `vesuvius-profilometer-ink-dice` · harvest · tractability 2.5 · laptop-hours · disclosure **commit-only**
> Bank says open as of 2026-10-08. Statuses go stale — re-check the primary source before any work.

## Statement

Angelotti, Nicolardi, Henderson and Seales, 'Ink detection from surface topography of the Herculaneum papyri', Scientific Reports 16, 27835 (published 2026-06-18, version of record 2026-09-07, doi 10.1038/s41598-026-58467-1; arXiv:2603.27698v1, 2026-03-29) trained default 2D nnU-Net on height maps from optical profilometry of mechanically opened papyri (14 samples / 16 letters from PHerc. 248, 250, 500P2) with five sample-level cross-validation folds, so every sample is held out exactly once (n = 14). Verified live 2026-10-08 (nature.com tables, plain curl): Table 1 primary native height maps median Dice 0.890 [Q1 0.864, Q3 0.905] (plane-detrended 0.891 [0.867, 0.911]); Table 3 at the native row: matched-resolution 0.890 / mean 0.881 +- 0.039, and the native model on the degraded-input pipeline 0.899 (the highest native-row figure); Table 4 leave-one-papyrus-out: 248 held out 0.757 [0.733, 0.812], 250 held out 0.817 [0.755, 0.822], 500P2 held out 0.475 [0.454, 0.482], pooled mean 0.691. The dataset is public: huggingface.co/datasets/scrollprize/profilometer (CC BY-NC 4.0, 14 samples x {calibrated XYZ .txt, normalised uint16 height map _z.tif, brightfield _stack.tif, _label.png with nonzero = ink}, manifest.csv, configs/experiment.json (nnUNetv2 2.5.1 commit 834b80f, trainer nnUNetTrainer, 2d, plans nnUNetResEncUNetPlans_24G, 1000 epochs x 250 iterations, SGD), configs/nnunet/plans for resolution factors 1,2,3,4,6,8,10,16,32, folds/splits_final.json with folds 0-4 (val sizes 3,3,3,3,2) and LOPO folds 5-7). RESOLUTION DISCREPANCY (live): the paper calls the native sampling 0.34 um while the dataset's sampling.json and manifest record 0.68793625 um/px and the README carries a 2026-09-03 NOTICE that the authors are investigating; the factor-k rows of the paper correspond to the dataset's resolution factors k regardless of the physical label (0.34 x 32 = 10.88 um matches the paper's coarsest row). Therefore the released factor-1 data IS the paper's native-row data and the native-row numbers (0.890 / 0.899), not the 0.68 um row (0.817), are the baseline. No code was released. Open: higher held-out Dice on the shipped folds using topography only.

## Success criterion

Using exactly folds 0-4 of folds/splits_final.json (sha256 recorded), train one model per fold on that fold's train cases only, with inputs derived solely from the height data (_z.tif or the .txt XYZ, plus any functions of them); _stack.tif brightfield must not be read at any stage (training, pre-training, pseudo-labelling, selection), declared in the manifest and audited. Threshold and checkpoint selection use only the fold's train cases (an inner split), declared before predicting the held-out cases; seeds are fixed and recorded. Freeze binary masks for all 14 held-out cases at native resolution. Skeptic computes per-case Dice against _label.png (nonzero = ink; empty-empty = 1, else standard) with score_dice.py. Gate (calibration): the scout's reproduction of the paper's recipe from configs/experiment.json (nnUNetv2 2d, nnUNetResEncUNetPlans_24G plans shipped in configs/nnunet, same folds; a shortened schedule is allowed if logged) must reach a median >= 0.880 across the 14 held-out cases, with per-case scores stored in a hash-locked BASELINE.json file; without this gate no win is accepted. Success (all): median Dice over the 14 held-out cases >= 0.919 (= highest native-row median 0.899 + 0.02) AND mean >= 0.909 (= 0.889 + 0.02) AND per-case wins over the reproduced baseline on >= 10 of 14 cases AND the live-reread paper tables show no higher factor-1 figure (if they do, the bar moves to that figure + 0.02). Internal benchmark; official only if a journal/arXiv version or scrollprize.org credits a submission made by the human.

## Partial wins

- {"id": "p1", "statement": "Cross-papyrus generalisation on the shipped leave-one-papyrus-out folds 5-7 (train on two papyri, predict all cases of the third; same input, brightfield and selection rules): pooled mean Dice over the 14 held-out cases >= 0.741 (= Table 4 pooled mean 0.691 + 0.05) AND median Dice on the PHerc. 500P2 held-out cases >= 0.575 (= 0.475 + 0.10), with the calibration gate passed on folds 0-4."}
- {"id": "p2", "statement": "Resolution robustness: with every input first block-averaged by the dataset's factor 2 (nonoverlapping 2x2 mean on the continuous height as in configs/experiment.json) and nothing finer ever read, median held-out Dice on folds 0-4 at native label resolution >= 0.901 (= Table 3 factor-2 best figure 0.881 + 0.02), same rules otherwise."}

## Verification

Skeptic downloads folds/splits_final.json, configs/, the 14 _label.png (about 1.5 MB) and the 14 _z.tif (about 0.57 GB; the .txt files are optional), checks the submitted masks cover exactly the held-out cases of each fold, computes per-case Dice and the median/mean with score_dice.py (seconds), compares per case with BASELINE.json, and reads the training manifest for brightfield access (every opened path is logged by the pinned data loader). Retrains one fold with the submitted config and seed on MPS when the logged training time is <= 2 h per fold and requires that fold's per-case Dice within 0.03 of the claim; if the recipe exceeds 2 h per fold the claim is capped at PROMISING until a human reruns it.

## Angles

- Reproduce the shipped nnU-Net 2D recipe on MPS (shortened schedule logged) to pass the calibration gate, then add topography-derived channels (gradient magnitude, Laplacian, local roughness, multi-scale detrending) which the paper's detrending ablation suggests help slightly.
- Pretrained 2D encoders (timm) on height-map pseudo-RGB with heavy augmentation; small data favours strong priors; test-time flips/rotations.
- Thin-stroke losses (clDice / skeleton recall) and boundary refinement, since Dice on ink strokes is boundary-dominated.
- p1: domain-robust normalisation (per-sample percentile scaling, roughness equalisation) to lift the PHerc. 500P2 held-out fold, the paper's worst case (0.475).
- Leave-one-papyrus-out and per-papyrus reporting on every claim to show gains are not a single-papyrus artefact.

## Pitfalls

- Using the 0.68 um row (0.817) as the baseline because the dataset says 0.69 um/px fabricates a win; the released factor-1 data is the paper's native-row data (0.890 / 0.899).
- n = 14 held-out cases: medians move by 0.01-0.02 from seeds alone; fixed seeds, the paired 10-of-14 rule and the skeptic's fold retrain are mandatory.
- Brightfield (_stack.tif) makes the task trivial; any read of it, even for pre-training or label QA, voids the attempt.
- Re-splitting or selecting on held-out cases is leakage; use the shipped folds unchanged and inner splits for selection.
- Label polarity (nonzero = ink) and the empty-empty Dice convention must follow score_dice.py.
- The authors' sampling notice may lead to a revised Table; re-read the tables before any claim, and never lower the bar.

## Sources

- https://huggingface.co/datasets/scrollprize/profilometer
- https://huggingface.co/datasets/scrollprize/profilometer/resolve/main/folds/splits_final.json
- https://huggingface.co/datasets/scrollprize/profilometer/resolve/main/configs/experiment.json
- https://huggingface.co/datasets/scrollprize/profilometer/resolve/main/configs/sampling.json
- https://www.nature.com/articles/s41598-026-58467-1
- https://arxiv.org/abs/2603.27698
- Status source: https://huggingface.co/datasets/scrollprize/profilometer

## Citations

- [Problem page](../../../../.raw/V3R1T4S/known-unknowns/herculaneum-scrolls/vesuvius-profilometer-ink-dice.md)
- [Bank entry](../../../../.raw/V3R1T4S/bank/targets.json) (id `vesuvius-profilometer-ink-dice`, commit `7dd4480`)

## Related Nodes

- [[V3R1T4S Herculaneum scrolls]]
- [[V3R1T4S]]
