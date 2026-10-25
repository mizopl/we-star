---
id: v3r1t4s-nasa-tropical-storm-wind-speed-rmse
type: entity
tags: [v3r1t4s, v3r1t4s/earth-and-sky, kind/standard]
inbound_links: 1
confidence: 0.8
last_ingested_sources: [".raw/V3R1T4S/bank/targets.json@7dd4480"]
status: "open"
priority: ""
notes: ""
category: earth-and-sky
kind: standard
tractability: 1.5
compute: "laptop-days (about 70k train and 45k test single-band 366x366 IR images, ~20 GB; CNN training on Apple-silicon GPU or CPU for days)"
disclosure: open
status_checked: "2026-10-15"
---
# NASA/Radiant Earth tropical-storm wind-speed challenge: beat the winning RMSE from GOES infrared imagery on the released test labels

# Overview

> Bank id `nasa-tropical-storm-wind-speed-rmse` · standard · tractability 1.5 · laptop-days (about 70k train and 45k test single-band 366x366 IR images, ~20 GB; CNN training on Apple-silicon GPU or CPU for days) · disclosure **open**
> Bank says open as of 2026-10-15. Statuses go stale — re-check the primary source before any work.

## Statement

The 'Wind-dependent Variables: Predict Wind Speeds of Tropical Storms' challenge (DrivenData 2021; data assembled by Radiant Earth Foundation and the NASA IMPACT team, Manil Maskey and colleagues) asks for each storm image the maximum sustained wind speed (kt) using that image and earlier images of the same storm. Winning private RMSE: 6.256 (vecxoz, 51-model ensemble), then 6.417 (KarimAmer), 6.456 (Daniel_FG); the winners' public-split scores were 6.677, 6.867 and 6.839. The full dataset including test_set_labels.csv is downloadable by plain GET from Source Cooperative (data.source.coop/nasa/tropical-storm-competition). The private/public split is not published, so the honest comparison is on the whole test set: the winner's whole-test RMSE must lie between its private and public scores (6.256-6.677). Open task: whole-test RMSE strictly below 6.256 with a causal model.

## Success criterion

Saved predictions for every image in test_set_features.csv plus code and weights, where each prediction uses only images of the same storm with relative_time less than or equal to that image's (no future frames, no test labels), trained only on the training set, whose RMSE against test_set_labels.csv over the whole test set is strictly lower (direction: min) than the 1st-place private score in the README at https://github.com/drivendataorg/wind-dependent-variables re-fetched live immediately before claiming (6.256 on 2026-10-15), and lower than any whole-test or private-split RMSE on this dataset reported in a paper of the last 24 months.

## Partial wins

- {"id": "p1", "statement": "Whole-test RMSE below 6.677 (the winner's public-split score, so below at least one of the winner's two split scores) with a single model trained in under 24 laptop-hours."}
- {"id": "p2", "statement": "Whole-test RMSE below 7.0 with no deep network (e.g. a Dvorak-style feature pipeline with gradient boosting) - a strong interpretable baseline."}
- {"id": "p3", "statement": "Beat the winner's released code re-run on the whole test set (its whole-test RMSE recomputed by the skeptic)."}

## Verification

Skeptic downloads the test labels from Source Cooperative, recomputes RMSE with a standalone script, inspects the data loader to confirm causal frame use (and re-runs inference with all future frames of each storm deleted to confirm identical predictions). Under 1 hour for scoring; inference re-run depends on model size.

## Angles

- Conventional: pretrained CNN backbones on stacks of the current and prior frames, plus a sequence model over storm history, with test-time augmentation by rotation (storms are rotation-equivariant up to hemisphere flip).
- Conventional: smooth predictions along each storm's timeline with a causal Kalman filter, since intensity changes slowly.
- Cross-domain import (Dvorak technique, operational meteorology): explicit features - eye temperature, coldest ring, cloud-top symmetry - as inputs alongside learned features.
- Cross-domain import (medical imaging): rotation-equivariant CNNs (polar-coordinate transforms around the storm centre) as used for histopathology.
- Cross-domain import (video understanding): temporal shift modules / optical flow between frames to capture intensification.

## Pitfalls

- Non-causal use of later frames from the same storm (or bidirectional sequence models) is leakage; the challenge allowed only prior images.
- Comparing a whole-test RMSE to a public-split RMSE is not like for like; use the rule above.
- Storm-level overlap: random image-level validation splits leak storms; validate by storm.
- Labels are best-track wind speeds in 5-kt steps; differences below ~0.05 kt RMSE are noise.
- Do not submit to DrivenData; scoring is local.

## Sources

- https://github.com/drivendataorg/wind-dependent-variables
- https://source.coop/nasa/tropical-storm-competition
- https://data.source.coop/nasa/tropical-storm-competition/test_set_labels.csv
- https://www.drivendata.org/competitions/72/predict-wind-speeds/leaderboard/
- Status source: https://github.com/drivendataorg/wind-dependent-variables

## Citations

- [Problem page](../../../../.raw/V3R1T4S/known-unknowns/earth-and-sky/nasa-tropical-storm-wind-speed-rmse.md)
- [Bank entry](../../../../.raw/V3R1T4S/bank/targets.json) (id `nasa-tropical-storm-wind-speed-rmse`, commit `7dd4480`)

## Related Nodes

- [[V3R1T4S Earth and sky]]
- [[V3R1T4S]]
