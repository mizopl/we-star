---
id: v3r1t4s-vesuvius-frag4-ink-f05-holdout
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
tractability: 1.5
compute: "laptop-hours"
disclosure: commit-only
status_checked: "2026-10-08"
---
# Herculaneum fragment ink detection: beat the 2023 Kaggle winners' own weights on the released hidden-test Fragment 4 (PHercParis1Fr39) under one pinned full-fragment F0.5 protocol, with a model that never saw Fragment 4

# Overview

> Bank id `vesuvius-frag4-ink-f05-holdout` · harvest · tractability 1.5 · laptop-hours · disclosure **commit-only**
> Bank says open as of 2026-10-08. Statuses go stale — re-check the primary source before any work.

## Statement

The 2023 Kaggle 'Vesuvius Challenge - Ink Detection' ($100K, closed 2023-06-14) trained on Fragments 1-3 and scored pixel F0.5 on a hidden fragment split into two pieces; the hidden fragment was released in Aug 2023 as Fragment 4 = PHercParis1Fr39 (substack '4th fragment released'). Verified live 2026-10-08 with plain curl (HTTP 200, no auth): dl.ash2txt.org/fragments/Frag4/PHercParis1Fr39.volpkg/working/54keV_exposed_surface/ holds PHercParis1Fr39_54keV_inklabels.png (6064 x 9791 px, values {0,1}, 7.76% ink, sha256 a6f39eb59422a4507313ec912185eb92b44e3dd9e2e8e6a97e7b571462ce18fc, last-modified 2023-03-01), PHercParis1Fr39_54keV_mask.png (74.8% valid, sha256 5d437887925ecd6a0f5b943c5b318a6a15c85e9fc97c95d442ada2255b4f51c7), extras/ (IR photo, mesh) and a 65-layer 3.24 um / 54 keV surface volume (65 x ~119 MB TIFF). Ink fraction inside the mask is 10.4% and differs between halves (left 9.0%, right 11.7%), so half-fragment scores are not interchangeable. scrollprize.org/winners (200) lists the Kaggle winners 1st ryches, 2nd RTX23090, 3rd wuyu; the leaderboard page is a JS shell under plain curl (the researcher's figures 0.682693 / 0.682443 / 0.681137 are UNVERIFIED by curl and, because Kaggle scored only the private piece of Frag4 while this target scores the whole masked fragment, they are context, never the bar). No public table reports full-Frag4 F0.5 for any model (searched 2026-10-08). Public weights that are DISQUALIFIED as initialisation because their cards list frag4 in training: scrollprize/resnet50_7.9um_scroll1_frags and scrollprize/resnet50_3um_01122024 (both 'frag1..frag6'). Public weights with no fragment training (clean): scrollprize/timesformer_GP_scroll1 (Scroll 1 segments), timesformer_large_scroll1_01122024, ink_9um (0139/1667/Paris4/0814), hecate (ink bucket), ink_detection_pipeline (GP model); the HF bucket scrollprize/datasets tree 'ink' (0009b, 0139, 0500p2, 1667, 814, 841, man5, phercparis4, unused) contains no fragment data. The open question: a reproducible model trained without any Fragment 4 bytes whose frozen full-Frag4 prediction beats the actual 2023 winning models run under the same protocol.

## Success criterion

Protocol (pinned, 'full-Frag4'): a frozen probability map over the whole of PHercParis1Fr39_54keV_inklabels.png's grid (6064 x 9791, resampled by the scout's pinned score_f05.py if the model works at lower resolution), scored as pixel F0.5 (beta 0.5) against inklabels > 0 only where mask > 0, at ONE binarisation threshold written into the attempt manifest (sha256 of weights + threshold) BEFORE the first Frag4 inference of that attempt. Gate A (comparability): the scout has run the human-fetched 2023 1st-place weights (and any other fetched winner) on Frag4 under this identical protocol with their published inference recipe (TTA and all), and recorded the threshold-optimal F0.5 per model in a hash-locked BASELINES.json file with the weights' sha256; the baseline B = max over fetched winners. Gate B (leakage): leak_audit.py hashes every file in the training manifest and every pretrained initialisation; any PHercParis1Fr39 path/hash, any Frag4 IR use, any unsupervised/transductive use of Frag4 bytes, or initialisation from weights whose documented training includes frag4 (resnet50_7.9um_scroll1_frags, resnet50_3um_01122024 or any card listing fragments beyond Frag1-3) fails the attempt. Gate C (selection): model and threshold selection must be justified by a logged Frag1-3 validation split score recorded before Frag4 scoring; every Frag4 scoring in the campaign is appended to FRAG4_EVALS.log and the claim reports the total count. Gate D (model-prior null): the same weights on the z-shuffled 65-layer Frag4 stack (pinned seed) must score F0.5 at most 0.5 x the claimed F0.5, and on the mask region with zero ink labels the predicted-ink fraction must not exceed the baseline model's. Success: F0.5 >= B + 0.02 on the whole masked fragment AND >= B + 0.01 on each of the two halves split at mask-bbox column 3031 (left/right) AND F0.5 >= the top private score shown live on the Kaggle leaderboard URL (direction max; read in a browser by the skeptic since the page is JS). This is an internal full-Frag4 benchmark: it never claims Kaggle leaderboard parity, and it is credited officially only if scrollprize.org/winners credits a Progress Prize submission made by the human.

## Partial wins

- {"id": "p1", "statement": "Scroll-to-fragment transfer, no winners' weights needed: a model trained ONLY on sealed-scroll labels from the HF bucket scrollprize/datasets (trees ink/ and ink_9um/; no fragment labels, no Frag1-4 bytes at all; initialisation only from weights with no fragment training) reaching F0.5 >= 0.55 on the whole masked Frag4 under the pinned protocol, with gates B, C and D satisfied and the threshold declared before Frag4 inference."}
- {"id": "p2", "statement": "Matching the winners on this Mac: with gate A done, a model trained on Fragments 1-3 only (gates B-D) whose full-Frag4 F0.5 is within 0.02 of B and wins on at least one of the two halves."}

## Verification

Skeptic downloads the two PNGs (150 KB; sha256 must match the statement), loads the claimed frozen map plus the manifest threshold, runs score_f05.py (minutes) for the whole fragment and both halves, and recomputes the baseline numbers from the scout's stored baseline maps with the same script (BASELINES.json must match within 1e-6). Runs leak_audit.py on the training manifest and initialisation weights. Spot-check: downloads 16 central layers of the Frag4 surface volume (1.9 GB), re-runs the submitted weights on 8 random 512 x 512 tiles (seeded) and requires Pearson r > 0.99 with the frozen map on those tiles. Re-runs the z-shuffle null on 8 tiles. Re-reads the Kaggle leaderboard page and scrollprize.org/data_datasets, /2026_open_problems and /winners before any claim.

## Angles

- Fine-tune the released GP TimeSformer-small (villa/ink-detection/optimized_inference supports MPS) on Frag1-3 only; pick epochs/thresholds on a Frag1-3 split, never on Frag4.
- p1: run ink_9um (seeds 42/43), Hecate 9.6 um and dense pseudo-label retrains on Frag4 pooled to ~9.7 um (3x XY, z mean-pooling), forward+reverse averaged, upsample the map to the label grid; calibrate the threshold on Frag1-3 pooled the same way.
- Reproduce the 2023 2.5D U-Net recipes (central 16-24 layers, large tiles, TTA; 3rd-place training code is on GitHub) on Frag1-3 with MPS, adding scroll pseudo-labels from the HF ink bucket as extra data.
- Depth-jittered training (random z-window within the 65 layers) to stop depth-locking, then average forward and reverse z-order predictions.
- Topology-aware post-processing calibrated on Frag1-3 (remove components smaller than a stroke, close gaps along the fiber direction) to raise precision, which F0.5 weights 4x over recall.

## Pitfalls

- Kaggle's private score was computed on one hidden piece of Frag4 (public LB on the other, and the two differ a lot), so 'beating 0.68 on the whole fragment' proves nothing; only the winners' weights re-run under the pinned protocol define the bar.
- Any peek at Frag4 (threshold sweep, epoch choice, visual checks, repeated attempts picking the best Frag4 score) is leakage; thresholds are declared before inference and the FRAG4_EVALS.log count is reported.
- resnet50_3um_01122024 and resnet50_7.9um_scroll1_frags were trained on frag4; fine-tuning from them is disqualifying.
- Scoring outside mask.png or at the wrong resolution inflates or deflates F0.5; resample the map to the label grid and score only masked pixels.
- Blurry high-recall maps collapse precision; letter-shaped hallucinations from Greek-text priors must be caught by the z-shuffle and blank-region nulls.
- Access gate: no download until the human has accepted the EduceLab-Scrolls terms; agents never run vesuvius.accept_terms, never logs in to Kaggle, never redistributes data.

## Sources

- https://dl.ash2txt.org/fragments/Frag4/PHercParis1Fr39.volpkg/working/54keV_exposed_surface/
- https://dl.ash2txt.org/fragments/Frag1/PHercParis2Fr47.volpkg/working/54keV_exposed_surface/
- https://dl.ash2txt.org/fragments/Frag2/PHercParis2Fr143.volpkg/working/54keV_exposed_surface/
- https://dl.ash2txt.org/fragments/Frag3/PHercParis1Fr34.volpkg/working/54keV_exposed_surface/
- https://www.kaggle.com/code/ryches/1st-place-solution/
- https://github.com/traptinblur/VCID_2023_3rd_place_code
- https://github.com/yukke42/kaggle-vesuvius-challenge-ink-detection
- https://huggingface.co/scrollprize/timesformer_GP_scroll1
- https://huggingface.co/scrollprize/ink_9um
- https://huggingface.co/scrollprize/hecate
- https://huggingface.co/api/buckets/scrollprize/datasets/tree/ink?recursive=false
- Status source: https://dl.ash2txt.org/fragments/Frag4/PHercParis1Fr39.volpkg/working/54keV_exposed_surface/

## Citations

- [Problem page](../../../../.raw/V3R1T4S/known-unknowns/herculaneum-scrolls/vesuvius-frag4-ink-f05-holdout.md)
- [Bank entry](../../../../.raw/V3R1T4S/bank/targets.json) (id `vesuvius-frag4-ink-f05-holdout`, commit `7dd4480`)

## Related Nodes

- [[V3R1T4S Herculaneum scrolls]]
- [[V3R1T4S]]
