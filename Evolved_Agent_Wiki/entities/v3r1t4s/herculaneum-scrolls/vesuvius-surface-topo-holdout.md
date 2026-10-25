---
id: v3r1t4s-vesuvius-surface-topo-holdout
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
tractability: 2
compute: "laptop-hours"
disclosure: commit-only
status_checked: "2026-10-08"
---
# Papyrus surface detection: beat the released Kaggle-2026 1st-place nnU-Net (surface_m7_nnunet) on a frozen 88-volume holdout of the open 320^3 training mirror under a pinned open topology-aware composite metric

# Overview

> Bank id `vesuvius-surface-topo-holdout` · harvest · tractability 2 · laptop-hours · disclosure **commit-only**
> Bank says open as of 2026-10-08. Statuses go stale — re-check the primary source before any work.

## Statement

Kaggle 'Vesuvius Challenge - Surface Detection' (2025-11-13 to 2026-02-13, $200K; scrollprize.org/winners: 1st 'Vesuvius Team', 2nd 'risk of overfitting', 3rd 'W & A') scored recto-surface segmentation of 320^3 CT chunks with a composite of TopoScore (Betti matching), SurfaceDice@2 voxels and a VOI-based score; the hidden test labels were never released and the exact metric code lives in the login-gated Kaggle dataset sohier/vesuvius-metric-resources. Verified live 2026-10-08 (plain curl, no login): the TRAIN set is mirrored in the HF bucket scrollprize/datasets at surfaces/kaggle/images and surfaces/kaggle/labels (892 files each, ids sample_00001..sample_00916 with gaps; labels 15.9 GB total; one label inspected = 320x320x320 uint8). Label values are {0 background, 1 surface, 2 ignore} (surface_m7_nnunet model card) and the ignore class is large: 45-88% of voxels in four inspected labels (sample_00007: 84.8%), so the ignore convention decides the score. The 1st-place single model is public: huggingface.co/scrollprize/surface_m7_nnunet (nnU-Net v2 ResEnc-L, 3d_fullres 192^3, fold_0 checkpoint_best ~783 MB, permissive open-source licence, trained on all 786 'Dataset100_VesuviusSurface' volumes, i.e. contaminated for any mirror holdout). Betti-Matching-3D (MIT, github.com/nstucki/Betti-Matching-3D) builds on this Mac at master commit db623be7456ae451beb422af3bbcea94e9863a8f (cmake + pybind11) and took 174 s on a worst-case speckled synthetic 320^3 pair, so per-volume runtime caps are part of the protocol. Frozen holdout: every mirror sample whose numeric id satisfies id % 10 == 7 (88 volumes). Open problem #2 on scrollprize.org/2026_open_problems (surface topology). No public post-competition leaderboard exists.

## Success criterion

Metric (pinned, open): score_surface.py, written by the scout on day 1 and frozen by sha256 in a hash-locked METRIC.sha256 file before the baseline run; it (1) sets every voxel with label == 2 to 0 in BOTH label and prediction, (2) binarises the label as == 1 and the prediction at the threshold declared in the attempt manifest (default > 0 for binary masks), (3) computes TopoScore = weighted topological F1 from Betti matching with github.com/nstucki/Betti-Matching-3D at commit db623be7456ae451beb422af3bbcea94e9863a8f (dims 0/1/2 weighted .34/.33/.33, inactive dims skipped, wall-clock cap 10 min per volume, a cap hit = TopoScore 0 for that mask), SurfaceDice at tolerance 2 voxels, and VOI score = 1 / (1 + VOI) with 26-connectivity components, and (4) composite = 0.30 x TopoScore + 0.35 x SurfaceDice + 0.35 x VOI score. Any change to the script resets every stored score. Success: binary 320^3 masks for ALL 88 holdout volumes (id % 10 == 7), from a model whose training manifest (leak_audit.py) lists only mirror ids with id % 10 != 7 plus optional other open data, with NO pretrained weights unless their documented training data provably excludes every holdout id (scrollprize surface checkpoints incl. surface_m7_nnunet, surface_recto*, fiber_* are presumed contaminated and are disallowed as initialisation or ensemble members); mean composite >= baseline mean + 0.02 AND per-volume wins on >= 53 of 88 volumes AND mean SurfaceDice not more than 0.01 below the baseline's. Internal benchmark: the Kaggle URL is re-read for context only, no leaderboard parity is claimed, and official credit exists only if scrollprize.org/winners credits a Progress Prize submission made by the human.

## Partial wins

- {"id": "p1", "statement": "Post-processing only: a deterministic function (hole filling, merger cutting, component pruning, distance-based thinning) applied to surface_m7_nnunet's own softmax probabilities on the 88 holdout volumes (produced and stored by the scout), with parameters chosen on non-holdout volumes only, raising the mean composite by >= 0.02 and winning on >= 53 of 88 volumes; the skeptic re-applies the code to the stored probabilities."}
- {"id": "p2", "statement": "From scratch on this Mac: a model with no pretrained weights, trained <= 12 logged wall-clock hours on non-holdout mirror volumes, whose holdout mean composite is within 0.05 of the contaminated baseline and whose mean SurfaceDice is within 0.05 of it."}
- {"id": "p3", "statement": "Topology at constant overlap: under the full-win training rules, mean TopoScore >= baseline + 0.05 while mean SurfaceDice is not more than 0.01 below the baseline's, with TopoScore wins on >= 53 of 88 volumes."}

## Verification

Skeptic fetches the 88 holdout labels from the HF resolve URLs (about 60 MB), checks METRIC.sha256 against the script, builds Betti-Matching-3D once at the pinned commit (minutes), verifies sha256 of all 88 submitted masks and of the stored baseline masks, then re-scores a seeded random subset of 20 holdout volumes (seed 0 over the sorted id list) for both submission and baseline within one hour (<= 3 min per volume at the cap) and requires |recomputed - stored| < 1e-6 for every one of them; the 88-volume means are then taken from the hash-locked stored tables. leak_audit.py checks the training manifest for holdout ids and disallowed initialisations. Label ignore handling is checked by asserting the script zeroes label==2 voxels.

## Angles

- Day 1: install nnunetv2 + torch (MPS), run surface_m7_nnunet with nnUNetv2_predict -device mps on the 88 holdout volumes (store softmax and masks), freeze score_surface.py and BASELINE.json.
- p1: topology-aware post-processing of the stored m7 probabilities (cut thin bridges between sheets, fill small holes along the sheet, prune components below a size chosen on non-holdout data).
- Train a small 3D U-Net (128^3 patches, MPS) with clDice / skeleton-recall losses on non-holdout volumes; distance-transform regression thresholded to a 1-2 voxel sheet (open problem #2 suggestion).
- Fiber-direction priors derived on the fly from the CT (structure tensor) to cut mergers between adjacent wraps; no fiber_* checkpoints.
- Report TopoScore, SurfaceDice and VOI separately per volume so p3 can be checked.

## Pitfalls

- Label value 2 is ignore and covers most voxels; binarising labels at > 0 would count ignore as surface and wreck every score. The pinned script zeroes label==2 in both arrays.
- The open metric is not Kaggle's exact code (login-gated); pin the script by sha256, never claim leaderboard parity, and never edit the script after the baseline run.
- The baseline trained on the holdout, so a loss means nothing and the holdout rule (id % 10 == 7) must never be 'fixed' after seeing results.
- Betti matching can take minutes on noisy masks (174 s measured on a speckled synthetic); the 10-minute cap and the 20-volume skeptic subset are part of the protocol, and submitting noisy masks to time out the baseline is impossible because baseline scores are stored and hash-locked.
- Label noise (approximate recto labels) caps achievable scores; gains under 0.02 are inside label noise, hence the margin.
- Access gate: data only after the human accepted the terms; never redistribute the mirror.

## Sources

- https://huggingface.co/api/buckets/scrollprize/datasets/tree/surfaces/kaggle/images?recursive=false
- https://huggingface.co/api/buckets/scrollprize/datasets/tree/surfaces/kaggle/labels?recursive=false
- https://huggingface.co/scrollprize/surface_m7_nnunet
- https://github.com/nstucki/Betti-Matching-3D
- https://scrollprize.org/2026_open_problems
- https://dl.ash2txt.org/datasets/seg-derived-recto-surfaces/
- Status source: https://huggingface.co/api/buckets/scrollprize/datasets/tree/surfaces/kaggle/images?recursive=false

## Citations

- [Problem page](../../../../.raw/V3R1T4S/known-unknowns/herculaneum-scrolls/vesuvius-surface-topo-holdout.md)
- [Bank entry](../../../../.raw/V3R1T4S/bank/targets.json) (id `vesuvius-surface-topo-holdout`, commit `7dd4480`)

## Related Nodes

- [[V3R1T4S Herculaneum scrolls]]
- [[V3R1T4S]]
