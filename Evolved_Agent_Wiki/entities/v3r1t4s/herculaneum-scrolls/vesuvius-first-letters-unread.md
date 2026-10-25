---
id: v3r1t4s-vesuvius-first-letters-unread
type: entity
tags: [v3r1t4s, v3r1t4s/herculaneum-scrolls, kind/standard]
inbound_links: 1
confidence: 0.8
last_ingested_sources: [".raw/V3R1T4S/bank/targets.json@7dd4480"]
status: "CONFIRMED_PARTIAL"
priority: ""
notes: "Draft PR #617 (2026-10-19-mizopl-abd283e3, commit 1372cf9, sealed-envelopes/vesuvius-first-letters-unread/2026-10-19-mizopl-abd283e3.md)"
category: herculaneum-scrolls
kind: standard
tractability: 1
compute: "needs cluster"
disclosure: commit-only
status_checked: "2026-10-08"
---
# Herculaneum papyri: first legible letters in one of the 21 still-unread Vesuvius Challenge First Letters scrolls (official credit only)

# Overview

> Bank id `vesuvius-first-letters-unread` · standard · tractability 1 · needs cluster · disclosure **commit-only**
> Bank says open as of 2026-10-08. Statuses go stale — re-check the primary source before any work.

## Statement

The Vesuvius Challenge First Letters Prizes ($50,000 per scroll, at most 10 scrolls, deadline 2027-06-25 23:59 PT; scrollprize.org/prizes fetched 2026-10-08, HTTP 200) pay the first team to produce a programmatically generated image of a virtually unwrapped segment showing at least 10 visible, legible letters within a single 4 cm2 area of an eligible scroll volume, with tifxyz meshes, a 1 cm scale bar, letter sizes in px and mm, text rows annotated without obscuring letters, no manual character annotations (including annotations used as training data), ink outputs that do not overlap any training region, and open-sourcing of code, data, weights and results after winning. Status 2026-10-08: the prizes page still lists 22 eligible volumes, but the substack post of 2026-10-08 ('$50K First Letters Prize awarded for PHerc. 343') credits Erwin Nieuwlaar for PHerc. 343 (windings w047/w048 of the 8.64 um / 116 keV scan; spiral fitter + ink_9um seeds 42/43 + Hecate + his dense_native fine-tune; reproduction repo github.com/Nieuwlaar/pherc343-first-letters with the meshes, image, sidecar JSON and SHA256SUMS), so 21 volumes and 9 prizes remain: PHerc0125, 0175A, 0175B, 0191, 0211, 0257, 0268, 0306B, 0358, 0483A, 0483B, 0490A, 0490B, 0800, 0813, 0826, 0846A, 0846B, 1203, 1218, 1545 (volume ids on the prizes page). PHerc. 1667 was fully read (prize retired Dec 2025); ink was found in PHerc. 1447 (Grand Prize set); a published null attempt exists for PHerc. 0826 (winners page, Aug 2026 progress prize). Official recipe (substack 2026-08-18): VC3D -> spiral fit (GPU) or GrowPatch -> optional Lasagna flatten (GPU) -> vc_render_tifxyz -> ink_9um inference -> conservative iterative labelling. Data: CC BY-NC 4.0 plus EduceLab terms, streamed from the public S3 bucket vesuvius-challenge-open-data (OME-Zarr; PHerc0343 level 0 is 1.33 TB, level 2 about 21 GB); published surface (m7) and Lasagna predictions exist for PHerc0343 under PHerc0343/representations/predictions/.

## Success criterion

CONFIRMED (CONFIRMED_SOLUTION) exists ONLY when https://scrollprize.org/prizes or https://scrollprize.org/winners, re-fetched live immediately before claiming, publicly credits a First Letters award to a submission made by the human for a scroll that was on the eligible list and unclaimed at submission time. Nothing produced by an agent alone can be CONFIRMED: every reading of unread text, however convincing, is capped at PROMISING, no partial win may be awarded for a reading of unread text, and no reading leaves local files (no artifact, post, gallery page or upload; the EduceLab terms and the prize terms forbid publicising discoveries). Internal PROMISING requires all of: (a) the scroll is on the eligible list and unclaimed on scrollprize.org/prizes, /winners and the substack archive at verification time; (b) the image is rendered programmatically from the public CT volume and a submitted tifxyz mesh with a 1 cm scale bar, and contains no manual annotation of characters or text, none of the ink labels used anywhere in training were drawn on this scroll, and no pseudo-labels from the claimed region were used (no training/prediction overlap, checked by leak_audit over every labelling iteration); (c) blind reading: at least 2 independent readers who see only the unannotated image each identify at least 10 Greek letters, agreeing in identity and position, within one 4 cm2 window; (d) model-prior null: the same weights on a blank or non-papyrus region of the same scroll and on a z-shuffled render of the claimed region produce no letter-like structures (component statistics reported); (e) a second ink model of a different family shows the same strokes in the same window; (f) fiber continuity across the window is shown in the render (no sheet switch).

## Partial wins

- {"id": "p1", "statement": "Positive control, mechanical and about already-credited text: from the published PHerc. 343 meshes (github.com/Nieuwlaar/pherc343-first-letters outputs/, sha256 per SHA256SUMS) and the public PHerc0343 8.64 um volume streamed from S3, re-render the credited w047/w048 segment on this Mac, run the four named public 9 um models (ink_9um seeds 42 and 43, Hecate 9.6 um, Nieuwlaar/ink9um-dense-native), ensemble as in the repo, and obtain Pearson r >= 0.9 between the agent's ensemble map and the ink channel of the published award image within the credited 4 cm2 window, with the same leak_audit rules; this validates the local render + inference pipeline before any unread scroll is attempted."}

## Verification

Verifier re-renders the claimed window from the public zarr volume (streamed at the declared level) and the submitted tifxyz mesh with vc_render_tifxyz or an equivalent pinned script, re-runs the submitted weights on the rendered stack (MPS/CPU, minutes for a 4 cm2 window), checks correlation > 0.99 with the submitted image, runs leak_audit on the training manifest and labelling history, runs the blank-region and z-shuffle nulls and the second-model check, performs the blind letter count with 2 readers who see only the image, and re-fetches scrollprize.org/prizes, /winners and the substack archive to confirm eligibility and non-claim. For p1 the verifier checks the mesh sha256 against the repo's SHA256SUMS and recomputes the correlation.

## Angles

- Do p1 first: the published PHerc. 343 meshes make the GPU-bound spiral-fit and Lasagna steps unnecessary; VC3D renders on macOS (CPU) and the four 9 um models run on MPS/CPU.
- For unread scrolls use published m7 surface and Lasagna predictions from S3 (PHerc0343 shows the pattern; check <scroll>/representations/predictions/ for each eligible id) so only rendering and inference run locally; stream level-2 volumes.
- Prioritise eligible scrolls with 2.4 um or 8-9 um scans and outer, well-separated wraps where sheet switches are rare.
- Average forward and reverse z-order predictions and two model families; require agreement before any human looks, to suppress single-model hallucinations.
- Rank windings by a mechanical crackle/ink heatmap statistic (fraction of pixels above a fixed probability in 2x2 cm tiles) before any reading attempt.

## Pitfalls

- Ink models trained on Greek text hallucinate Greek letterforms; blind readers, the blank-region / z-shuffle nulls and the second-model check are mandatory, and a single-model image is never evidence.
- Pseudo-labels or fine-tuning on the claimed region, or any hand-drawn letter labels on the target scroll, violate the no-overlap / no-manual-annotation rules; leak_audit must cover every labelling iteration.
- Sheet switches splice strokes from two wraps into plausible letters; fiber continuity across the window must be shown.
- Publishing or posting a reading before the official announcement breaks the prize terms and the EduceLab terms; readings stay on the contributor's machine for the human.
- Full-resolution volumes are 1-3 TB per scroll and spiral fitting / Lasagna need CUDA; attempts that ignore the streamed-level and published-prediction route exhaust disk and time with nothing checkable.
- The prizes page lags announcements (it still listed PHerc0343 on 2026-10-08); check the substack archive too.

## Sources

- https://scrollprize.org/prizes
- https://scrollprize.org/winners
- https://scrollprize.substack.com/p/50k-first-letters-prize-awarded-for
- https://github.com/Nieuwlaar/pherc343-first-letters
- https://scrollprize.substack.com/p/from-ct-scan-to-ancient-text-a-first
- https://scrollprize.org/2026_open_problems
- https://vesuvius-challenge-open-data.s3.amazonaws.com/?list-type=2&prefix=PHerc0343/representations/predictions/&delimiter=/
- https://huggingface.co/scrollprize/ink_9um
- https://huggingface.co/scrollprize/hecate
- https://github.com/ScrollPrize/villa
- Status source: https://scrollprize.org/prizes

## Citations

- [Problem page](../../../../.raw/V3R1T4S/known-unknowns/herculaneum-scrolls/vesuvius-first-letters-unread.md)
- [Bank entry](../../../../.raw/V3R1T4S/bank/targets.json) (id `vesuvius-first-letters-unread`, commit `7dd4480`)

## Related Nodes

- [[V3R1T4S Herculaneum scrolls]]
- [[V3R1T4S]]
