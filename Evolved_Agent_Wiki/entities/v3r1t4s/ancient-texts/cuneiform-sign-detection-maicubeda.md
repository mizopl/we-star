---
id: v3r1t4s-cuneiform-sign-detection-maicubeda
type: entity
tags: [v3r1t4s, v3r1t4s/ancient-texts, kind/harvest]
inbound_links: 1
confidence: 0.8
last_ingested_sources: [".raw/V3R1T4S/bank/targets.json@7dd4480"]
status: "open"
priority: ""
notes: ""
category: ancient-texts
kind: harvest
tractability: 2
compute: "laptop-hours"
disclosure: open
status_checked: "2026-10-08"
---
# Cuneiform sign detection on the open MaiCuBeDa 3D-rendering benchmark: beat the published AP@50/AP@75 under a frozen split

# Overview

> Bank id `cuneiform-sign-detection-maicubeda` · harvest · tractability 2 · laptop-hours · disclosure **open**
> Bank says open as of 2026-10-08. Statuses go stale — re-check the primary source before any work.

## Statement

The Mainz Cuneiform Benchmark Dataset (MaiCuBeDa Hilprecht, heiDATA doi:10.11588/DATA/QSNIQ2, CC BY-SA 4.0, version 1 released 2025-08-06 with description dated 2023-08-29; about 9.3 GB: three ~3 GB zips of MSII / VirtualLight / Mixed renderings with char/line/word/wedge crops and W3C JSON-LD annotations, plus annotations.ttl, line/word/translit metadata; Journal of Open Archaeology Data 2025, doi:10.5334/joad.172) is the open benchmark for locating cuneiform signs on 3D-scan renderings. Stotzner, Homburg and Mara (ICCV 2023 workshops, arXiv 2308.11277) train a RepPoints/ResNet-18 single-class detector on 512x512 patches cut from 873 segments of 490 tablets (10,311 patches, 21,228 sign annotations) with a 2:1:1 segment-level split, and report in Table 2 per training base and test rendering; best per test rendering: Mixed test AP@50 0.636 / AP@75 0.431 ('Complete with IA' = all renderings + HeiCuBeDa photographs, illumination augmentation); VL test AP@50 0.626 / AP@75 0.545 (Complete with IA) and AP@90 0.364 (VL with IA); MSII test AP@50 0.632 (Complete) / AP@75 0.437 (MSII). A June 2026 eBL paper (arXiv 2606.22608, DETR on a separate photo dataset of Lewenstein et al. 2026) does not evaluate on MaiCuBeDa and releases only weights and inference outputs on Zenodo, so MaiCuBeDa remains the only open, checkable benchmark. Status 2026-10-08 (vetter): no published result found exceeding the 2023 Table 2 values on MaiCuBeDa (the JOAD 2025 dataset paper cites only the 2023 baselines); heiDATA's HTML landing page is behind the Anubis bot filter, but the Dataverse API and /api/access/datafile/{id} return 200 to plain curl GET (HEAD returns 503; ranged GET returns 206), verified on readme.txt, utils.zip and the first KB of both large zips.

## Success criterion

On MaiCuBeDa version 1 (heiDATA file ids and hashes recorded), the claimant names one test rendering R in {Mixed, VirtualLight, MSII}, publishes a deterministic segment-level 2:1:1 train/val/test split rule (e.g. sorted segment-id hash) and a deterministic 512x512 patch-cropping rule, and freezes (hash) the split and patch list before any training; no patch may overlap across splits. A detector trained ONLY on the train split (val for model selection) produces a frozen class-agnostic detections file (COCO JSON, hash committed before scoring) that, scored with pycocotools on the test patches of rendering R, achieves AP@50 AND AP@75 strictly above the BEST AP@50 and the BEST AP@75 reported for test rendering R in any row of Table 2 of arXiv 2308.11277 (re-read immediately before claiming). In addition the claimant retrains the paper's RepPoints/ResNet-18 baseline under the same frozen split with the same training base as one Table 2 row and freezes its detections (hash); the verifier's rescoring of that file must land within 0.03 AP@50 of that row's paper value, proving the split is comparable. Evaluation is sign-class-agnostic (localisation only) at 512x512 patch level, pycocotools defaults, all annotations counted unless a documented filter is applied identically to both files.

## Partial wins

- {"id": "p1", "statement": "Same protocol (frozen split, frozen detections, reproduced baseline), beating the best Table 2 AP@50 for the chosen test rendering by at least 0.02 absolute, or beating AP@90 0.364 on VirtualLight test patches."}
- {"id": "p2", "statement": "Cross-rendering generalisation: a detector trained only on one rendering type (e.g. MSII) scores AP@50 on the held-out test patches of another rendering (e.g. VirtualLight) at least 0.05 above the Table 2 row for the same train-to-test direction (re-read live), with frozen detections, the same frozen split, and the reproduced baseline control."}

## Verification

The verifier downloads via plain curl GET from the heiDATA API only the annotation files and the zip of the chosen test rendering (about 3 GB; ranged GET works, HEAD does not), verifies hashes, regenerates the split and patch list from the published rules, checks that both frozen detections files' hashes predate scoring, rescores both (new system and reproduced baseline) with pycocotools, and checks no patch overlap across splits. No retraining by the verifier; under one hour on a 10-core Mac with a normal connection.

## Angles

- Small anchor-free detectors (YOLO-n/s, FCOS-lite) at 512 px train in CPU-hours on 10k patches; sign boxes are small and dense, so tune anchor-free heads and NMS thresholds for crowded scenes.
- Multi-rendering fusion: stack MSII curvature, VirtualLight and Mixed renderings of the same patch as channels (the paper trains them separately).
- Test-time augmentation with illumination rotations (the dataset's VirtualLight directions) and box-level weighted fusion directly targets AP@75/AP@90.
- Use the wedge-level annotations (4,700 wedges in the dataset) as auxiliary supervision for sign boundaries.
- Reproduce the RepPoints baseline first on the frozen split; without it no comparison survives the CRITERION skeptic.

## Pitfalls

- The paper's exact split is not shipped; comparing to its numbers without the reproduced-baseline control on your own split is apples to oranges. 'Complete' training rows also use HeiCuBeDa photographs (doi:10.11588/data/IE8CCN), which must be fetched separately if that row is reproduced.
- Patches overlap at segment level: a random patch-level split leaks near-identical crops into test and inflates AP by 10+ points. Split by segment (as the paper does) and verify no patch overlap across splits.
- AP numbers depend on the IoU protocol and on whether annotations marked uncertain/partial are counted; follow pycocotools defaults and document any filtering.
- Training-time augmentation that uses the test rendering (e.g. VirtualLight directions reserved for test) is leakage.
- The eBL 2026 DETR dataset is not released; its numbers cannot be used as a record or checked here.
- heiDATA HEAD requests return 503 and the HTML landing page sits behind a bot filter: use plain GET (ranged if needed) on /api/access/datafile/{id}; never retry through a challenge page.

## Sources

- https://heidata.uni-heidelberg.de/api/datasets/:persistentId/?persistentId=doi:10.11588/DATA/QSNIQ2
- https://heidata.uni-heidelberg.de/api/datasets/:persistentId/?persistentId=doi:10.11588/DATA/8TCR5C
- https://arxiv.org/abs/2308.11277
- https://ar5iv.labs.arxiv.org/html/2308.11277
- https://arxiv.org/abs/2606.22608
- https://zenodo.org/records/17395154
- Status source: https://heidata.uni-heidelberg.de/api/datasets/:persistentId/?persistentId=doi:10.11588/DATA/QSNIQ2

## Citations

- [Problem page](../../../../.raw/V3R1T4S/known-unknowns/ancient-texts/cuneiform-sign-detection-maicubeda.md)
- [Bank entry](../../../../.raw/V3R1T4S/bank/targets.json) (id `cuneiform-sign-detection-maicubeda`, commit `7dd4480`)

## Related Nodes

- [[V3R1T4S Ancient texts and fragments]]
- [[V3R1T4S]]
