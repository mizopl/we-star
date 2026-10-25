---
id: v3r1t4s-robustbench-cifar10-linf-beat-autoattack
type: entity
tags: [v3r1t4s, v3r1t4s/ml-robustness, kind/harvest]
inbound_links: 1
confidence: 0.8
last_ingested_sources: [".raw/V3R1T4S/bank/targets.json@7dd4480"]
status: "open"
priority: ""
notes: ""
category: ml-robustness
kind: harvest
tractability: 2
compute: "laptop-hours"
disclosure: open
status_checked: "2026-10-09"
---
# RobustBench CIFAR-10 Linf (eps 8/255): a stronger attack that lowers a listed model's robust accuracy below the leaderboard value

# Overview

> Bank id `robustbench-cifar10-linf-beat-autoattack` · harvest · tractability 2 · laptop-hours · disclosure **open**
> Bank says open as of 2026-10-09. Statuses go stale — re-check the primary source before any work.

## Statement

RobustBench (robustbench.github.io) is the standard leaderboard for adversarially robust CIFAR-10 classifiers under Linf eps=8/255. Each of the 99 listed models (open weights, loaded with robustbench.utils.load_model) carries an 'autoattack_acc' (standard AutoAttack: APGD-CE, APGD-T, FAB-T, Square, full 10k test set) and, for 17 of them (verified 2026-10-09), an 'external' value from a stronger evaluation: the original authors' hybrid AutoAttack+MultiTargeted runs (Gowal2020/2021, Rebuffi2021 WRNs), APGD with BPDA for the two Amini2024MeanSparse models (non-differentiable operator), Adaptive AutoAttack for Bai2024MixedNUTS, transfer APGD for Kang2021Stable (unreliable: true) and 30-restart Square for Xiao2020Enhancing (unreliable: true). The leaderboard's own policy (README section 'Adding a new evaluation') is that any evaluation yielding a LOWER robust accuracy than AutoAttack gets added; the last such batch was the 'adaptive-eval' PR merged 2025-02-05, repo last pushed 2026-04-14. The open question for each model is whether its best-known robust accuracy can be lowered further by an adaptive or better-optimised attack. Known headroom is small: Adaptive Auto Attack (A3, Liu et al., CVPR 2022, arXiv:2203.05154, Table 1: 35 CIFAR-10 models) lowers AutoAttack by 0.04-0.16 points on adversarially trained models (avg 0.1), AutoAE (arXiv:2211.12713, Table: 20 CIFAR-10 Linf models) by 0.01-0.17 (median 0.05), PMA+ (arXiv:2411.15210, CVPR 2025, Tables 3/6: 10 top CIFAR-10 models) by 0.02-0.15, and MALT (arXiv:2407.02240, NeurIPS 2024) by 0.00-0.07 on CIFAR-100 only (no CIFAR-10 results). NONE of these published lower numbers has been copied into the model_info 'external' fields, so for roughly 30 models the literature already sits below the leaderboard value; a claim must beat the literature, not just the JSON. arXiv:2402.17018 (TMLR 2025) shows AutoAttack badly overestimating a randomized ensemble (90.8% -> 18.2%), but randomized defenses are not on this leaderboard. On this Mac (CPU only) the realistic targets are the ResNet-18 / PreActResNet-18 entries (Rade2021Helper_R18_ddpm 57.09, Rade2021Helper_R18_extra 57.67 [AutoAE: 57.63], Rebuffi2021Fixing_R18_ddpm 56.66, Sehwag2021Proxy_R18 55.54 [A3 lists a 'Proxy ResNet-18' at AA 54.43 -> 54.35, apparently a different checkpoint], Addepalli2022Efficient_RN18 52.48, Addepalli2021Towards_RN18 51.06 [A3: 51.02], Gowal2021Improving_R18_ddpm_100m 58.63 with external 58.50); a full 10k-image adaptive attack on an RN18 is laptop-hours (standard AutoAttack alone is several CPU-hours on an RN18). The result object is a tensor of 10,000 perturbed images.

## Success criterion

Success means a saved set of adversarial inputs for the FULL standard CIFAR-10 test set (10,000 images, the torchvision test split in its canonical order, pixel range [0,1], no normalisation outside the model) against one CIFAR-10 Linf model loaded unmodified via robustbench.utils.load_model(model_name, dataset='cifar10', threat_model='Linf') in eval mode, with weights downloaded fresh by the skeptic (never attacker-supplied), such that (a) every perturbation satisfies max|x_adv - x| <= 8/255 (checked in float64 with tolerance 1e-6) and 0 <= x_adv <= 1, (b) the robust accuracy, computed by the skeptic's own forward pass as the fraction of the 10,000 images whose clean prediction is correct AND whose adversarial prediction (argmax of logits; ties count as not fooled) is still correct, is STRICTLY LOWER (direction: min) than the model's best-known value min(autoattack_acc, external) in https://raw.githubusercontent.com/RobustBench/robustbench/master/model_info/cifar10/Linf/<Model>.json, re-fetched live immediately before claiming, by at least 10 images (0.10 percentage points, to exceed AutoAttack seed variance), and (c) the value is also strictly lower (by at least 1 image) than every robust accuracy already published for the same model name and threat model by Adaptive Auto Attack (arXiv:2203.05154 Table 1), AutoAE (arXiv:2211.12713, CIFAR-10 Linf table), PMA / PMA+ (arXiv:2411.15210 Tables 3 and 6), MALT (arXiv:2407.02240), and any arXiv paper of the last 24 months found by the NOVELTY skeptic; a published row counts as covering the model when its AutoAttack column matches the JSON autoattack_acc within 0.05. Models with footnotes changing eps (0.031 instead of 8/255) must be attacked at 8/255 exactly as RobustBench evaluates them. How x_adv was produced is irrelevant to the check (BPDA/transfer/anything is allowed): only the skeptic's plain forward pass on the unmodified deterministic model counts. Any 'robust accuracy' inferred from attack logs, per-image flags, subsets, or a different test order does not count.

## Partial wins

- {"id": "p1", "statement": "The same full-test-set result (perturbation, prediction and live re-fetch checks identical to the main criterion) for a model that NO published adaptive evaluation covers (not in A3 Table 1, not in the AutoAE CIFAR-10 Linf table, not in PMA/PMA+ Tables 3/6, not in MALT, and nothing found by the NOVELTY skeptic for the last 24 months; e.g. as of 2026-10-09 Rade2021Helper_R18_ddpm, Rebuffi2021Fixing_R18_ddpm, Addepalli2022Efficient_RN18, Gowal2021Improving_R18_ddpm_100m appear uncovered), with robust accuracy strictly lower than live min(autoattack_acc, external) by at least 20 images (0.20 points: above the 0.04-0.17 point gain that A3/AutoAE/PMA+ routinely obtain on adversarially trained models, so it is not merely re-running a known attack)."}
- {"id": "p2", "statement": "For a model whose live model_info has 'unreliable': true (as of 2026-10-09: Kang2021Stable autoattack 71.28 / external 64.20; Xiao2020Enhancing autoattack 18.50 / external 7.40, which must be attacked at 8/255), a full-test-set robust accuracy strictly lower by >= 10 images than BOTH the autoattack_acc and the external value, under the same checks (a)-(c)."}
- {"id": "p3", "statement": "A reproducible per-image result: at least 50 CIFAR-10 test images (indices listed), for one RN18/PreActRN18 model, on which the skeptic's own run of standard AutoAttack (autoattack package, version='standard', seed 0, full 4-attack ensemble, run on exactly those indices) finds no adversarial example but the attacker's saved perturbations (checked for eps, box and misclassification by the skeptic's forward pass) do. This is an attack-strength finding, not a leaderboard change, and must be reported as such; it never triggers a record claim."}

## Verification

Skeptic writes their own checker: pip install robustbench autoattack torch torchvision; load the model by name via robustbench.utils.load_model into a fresh cache (never accept attacker-supplied weights or model code), model.eval; load the torchvision CIFAR-10 test set (train=False, ToTensor only, canonical order) and confirm its sha256 against the attacker's manifest; load the attacker's x_adv tensor (shape 10000x3x32x32, dtype float32) and manifest; assert in float64 that (x_adv - x).abs.max <= 8/255 + 1e-6 and 0 <= x_adv <= 1; compute clean and adversarial predictions in batches on CPU (RN18: ~5 min; WRN-28-10: ~30 min); robust_acc = mean(clean_correct & adv_correct), reported as an integer count out of 10000. Re-fetch the live model_info JSON (quote URL and fetch time) and compare to min(autoattack_acc, external) * 100 images; then open A3 Table 1 (ar5iv 2203.05154), the AutoAE CIFAR-10 table (ar5iv 2211.12713) and PMA Tables 3/6 (arxiv.org/html/2411.15210) and compare against every row whose AutoAttack column matches the JSON autoattack_acc within 0.05. For p3 run AutoAttack standard (seed 0) on the listed indices and confirm it fails on each while the attacker's x_adv succeeds. If GitHub is unreachable the comparison is PENDING TABLE CHECK.

## Angles

- Start from AutoAttack's own robust set: run APGD-CE/APGD-T once on an RN18 model, keep only the images it fails on (~5,700), and spend the whole budget there with many random restarts, longer schedules (500-1000 steps), margin/DLR/CW losses with per-image loss selection, and targeted attacks against all 9 classes (AutoAttack's APGD-T uses only the top-3 non-true classes).
- Re-implement Adaptive Auto Attack (A3) ideas: adaptive initialisation from directions that fooled neighbouring images, online statistics-based discarding, plus a final 'minimum-margin' polishing pass; A3's own numbers for the covered models are the bar to beat.
- Composite/transfer seeding: generate adversarial examples from several other robust RobustBench models (transfer), then use them as starting points for APGD on the target; robust models share adversarial directions, and transfer starts often succeed where random starts do not.
- Gradient quality: attack in float64, use exact (not detached) BN statistics in eval mode, try input-space line search along the final APGD direction, and test boundary points at exactly +-8/255 corners (sign patterns) with coordinate-wise flips (a cheap 'bit-flip' local search over the hypercube vertices).
- Cheap full-set black-box top-up: Square Attack with 20k+ queries on the remaining unbroken images of an RN18 model is CPU-feasible and is exactly the signal AutoAttack's flags doc says indicates overestimation.
- Pick the model with the largest gap between 'reported' and 'autoattack_acc' or with large gaps between APGD-CE and APGD-T results (available from a local AutoAttack run), which indicates loss-landscape pathologies to exploit.

## Pitfalls

- Wrong model or wrong mode: not using robustbench.utils.load_model with the exact model_name, loading in train mode (BatchNorm uses batch statistics and makes the model look weaker), or using a different test split/order. Skeptic must check weights sha256 and eval mode.
- Perturbation bound violations hidden by float32 rounding, by saving to uint8 PNG, or by clipping after the eps check; always check in float64 on the saved tensor and reject any pixel over 8/255 by more than 1e-6.
- Counting images that are already misclassified on clean inputs as 'new' adversarial successes, or counting a prediction flip on an image whose clean prediction was wrong; robust accuracy must be recomputed from scratch, not inferred from AutoAttack's per-image logs.
- Seed noise: AutoAttack numbers differ by a few hundredths of a point between runs; a difference below 10 images is not a record. Also the website table and model_info JSON can lag each other: use the JSON (the website is generated from it) and quote fetch time.
- Novelty trap: A3 (2022) already reports lower numbers than AutoAttack for many RobustBench models; matching A3's number is not new. The NOVELTY skeptic must open A3 Table 1 and the model's 'external'/footnote fields.
- Changing the threat model (eps 0.031 vs 8/255, L2 instead of Linf, perturbing after normalisation) or attacking a logit-scaled/softmax wrapper instead of the leaderboard model.
- Published adaptive tables (A3, AutoAE, PMA) sometimes evaluate a different checkpoint under the same author/year: match rows by RobustBench model name AND an AutoAttack column within 0.05 of the JSON autoattack_acc (e.g. A3's 'Proxy ResNet-18' shows AA 54.43 while RobustBench Sehwag2021Proxy_R18 is 55.54). A row that does not match does not excuse ignoring it: the NOVELTY skeptic must say which checkpoint it is.
- The model_info 'external' fields do NOT include the A3 / AutoAE / PMA+ literature; roughly 30 models already have published numbers below the leaderboard value. Beating only the JSON number on such a model is NOT a record.
- Compute underestimation: standard AutoAttack on an RN18 over 10k images is several CPU-hours (APGD-T alone is 9 targets x 100 steps on ~5.7k images); a full adaptive campaign that only finishes on a subset cannot be scored. Partial coverage must be reported as p3 at most.

## Sources

- https://robustbench.github.io/
- https://github.com/RobustBench/robustbench
- https://github.com/RobustBench/robustbench/tree/master/model_info/cifar10/Linf
- https://github.com/fra31/auto-attack
- https://raw.githubusercontent.com/fra31/auto-attack/master/flags_doc.md
- Status source: https://robustbench.github.io/

## Citations

- [Problem page](../../../../.raw/V3R1T4S/known-unknowns/ml-robustness/robustbench-cifar10-linf-beat-autoattack.md)
- [Bank entry](../../../../.raw/V3R1T4S/bank/targets.json) (id `robustbench-cifar10-linf-beat-autoattack`, commit `7dd4480`)

## Related Nodes

- [[V3R1T4S ML robustness]]
- [[V3R1T4S]]
