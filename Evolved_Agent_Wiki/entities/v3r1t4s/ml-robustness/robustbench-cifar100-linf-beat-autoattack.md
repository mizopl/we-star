---
id: v3r1t4s-robustbench-cifar100-linf-beat-autoattack
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
tractability: 3
compute: "laptop-hours"
disclosure: open
status_checked: "2026-10-09"
---
# RobustBench CIFAR-100 Linf (eps 8/255): lower a listed model's robust accuracy below the best published value with a stronger attack

# Overview

> Bank id `robustbench-cifar100-linf-beat-autoattack` · harvest · tractability 3 · laptop-hours · disclosure **open**
> Bank says open as of 2026-10-09. Statuses go stale — re-check the primary source before any work.

## Statement

The RobustBench CIFAR-100 Linf eps=8/255 leaderboard lists 38 open-weight models (model_info/cifar100/Linf, verified 2026-10-09 via the GitHub API). Only 4 carry an 'external' value: Wang2023Better_WRN-70-16 42.67->42.66 and Wang2023Better_WRN-28-10 38.83->38.77 (both MALT, Melamed et al. 2024), Bai2024MixedNUTS 41.91->41.80 (the paper's own adaptive AutoAttack), and Amini2024MeanSparse_S-WRN-70-16 44.78->42.25 (APGD with BPDA through the MeanSparse operator; a 2.5-point drop showing post-hoc 'robustness enhancers' can be strongly over-estimated by AutoAttack). Beyond the leaderboard, four papers have published lower-than-AutoAttack numbers for CIFAR-100 models that were NOT folded into the table: Adaptive Auto Attack / A3 (arXiv:2203.05154, Table 1: 12 models, e.g. Gowal2020Uncovering_extra 36.86, Rebuffi2021Fixing_70_16 34.55, Rebuffi 28_10 32.00, Addepalli2021Towards_WRN34 30.31, Addepalli2021Towards_PARN18 27.09, Wu2020 28.78, Hendrycks2019 28.31, Sitawarin2020 24.51, Rice2020Overfitting 18.90, Gowal2020Uncovering 29.99, LBGAT 34-20 30.12 and 34-10 29.18 at eps 0.031), AutoAE (arXiv:2211.12713, Table 1: Gowal_extra 36.86, Rebuffi 70_16 34.62, Rebuffi 28_10 32.02, LBGAT 34-20 30.13, Gowal 30.00), MALT (arXiv:2407.02240, Table 1: Gowal_extra 36.81, Cui2023Decoupled_WRN-28-10 39.18 unchanged), and PMA/PMA+ (arXiv:2411.15210, Tables 3 and 6: Wang 70-16 42.63, Cui2023Decoupled 28-10 39.17, Wang 28-10 38.77, Gowal_extra 36.85, XCiT-L12 34.95, Rebuffi 70_16 34.63, XCiT-M12 34.13, Pang2022 WRN70_16 33.00). The bar for any model is therefore the minimum over the live table and all of these. Headroom argument: standard AutoAttack's APGD-T and FAB-T attack only the 9 highest-scoring wrong classes (autoattack.py set_version: n_target_classes = 9), i.e. 9 of 99 on CIFAR-100, and MALT also stops at 9, so wider targeted sweeps, per-image loss selection and BPDA-style attacks on the post-hoc defenses have real room. As of 2026-10-09 about 18 of the 38 models have NO published stronger-than-AutoAttack number at all (see partial win p1). CPU-realistic entries: Rade2021Helper_R18_ddpm (28.88, no published adaptive number), Rebuffi2021Fixing_R18_ddpm (28.50, none), Addepalli2022Efficient_RN18 (27.67, none), Addepalli2021Towards_PARN18 (27.14; A3 27.09), Rice2020Overfitting PreActRN18 (18.95; A3 18.90), and the WRN-28-10 / WRN-34-10 entries overnight.

## Success criterion

Success means a saved tensor of adversarial inputs for the FULL standard CIFAR-100 test set (all 10,000 torchvision CIFAR100(train=False) images in their standard order, fine labels, [0,1] range, no normalisation applied before the model) against one model loaded unmodified via robustbench.utils.load_model(model_name, dataset='cifar100', threat_model='Linf') in eval mode, with (a) every perturbation satisfying max|x_adv - x| <= 8/255 (float64 check, tolerance 1e-6) and 0 <= x_adv <= 1; (b) skeptic-recomputed robust accuracy (fraction of the 10,000 images whose adversarial argmax equals the label; clean-misclassified images count as non-robust; argmax ties count as not fooled) that is LOWER by at least 10 images (0.10 points) than the BAR, where BAR = min over: min(autoattack_acc, external) in the live https://raw.githubusercontent.com/RobustBench/robustbench/master/model_info/cifar100/Linf/<Model>.json re-fetched immediately before claiming (direction: min); every robust accuracy published for the same model and threat model in A3 (arXiv:2203.05154, Table 1), AutoAE (arXiv:2211.12713, Table 1), MALT (arXiv:2407.02240, Table 1) and PMA/PMA+ (arXiv:2411.15210, Tables 3 and 6); and every value for that model found by the NOVELTY skeptic in arXiv papers of the last 24 months and in open RobustBench issues/PRs; and (c) the skeptic's recomputed clean accuracy matches the model_info clean_acc to within 0.05 points, proving the right model, test set and label set were used. Fewer than 10 images below the BAR is seed noise, not a win.

## Partial wins

- {"id": "p1", "statement": "The full-test-set result of the success criterion (>= 10 images below live min(autoattack_acc, external), same perturbation, prediction and clean-accuracy checks) for a CIFAR-100 Linf model with NO published stronger-than-AutoAttack evaluation: no 'external' field, not in A3 Table 1, not in AutoAE Table 1, not in MALT Table 1, not in PMA Tables 3/6, and nothing found by the NOVELTY skeptic's 24-month sweep. As of 2026-10-09 that set is: Bai2023Improving_edm, Bai2023Improving_trades, Cui2023Decoupled_WRN-34-10, Cui2023Decoupled_WRN-34-10_autoaug, Debenedetti2022Light_XCiT-S12, Pang2022Robustness_WRN28_10, Jia2022LAS-AT_34_10, Jia2022LAS-AT_34_20, Addepalli2022Efficient_RN18, Addepalli2022Efficient_WRN_34_10, Cui2020Learnable_34_10_LBGAT9_eps_8_255, Cui2020Learnable_34_10_LBGAT0, Sehwag2021Proxy, Chen2024Data_WRN_34_10, Chen2021LTD_WRN34_10, Rade2021Helper_R18_ddpm, Rebuffi2021Fixing_R18_ddpm, Chen2020Efficient; the skeptic must re-derive this set live, not trust the list."}
- {"id": "p2", "statement": "For one of the post-hoc / ensemble defenses Amini2024MeanSparse_S-WRN-70-16 (live autoattack 44.78, external 42.25), Bai2024MixedNUTS (41.91, external 41.80), Bai2023Improving_edm (38.72, no external) or Bai2023Improving_trades (35.15, no external): a full-test-set robust accuracy at least 10 images below BOTH the live min(autoattack_acc, external) and every value for that model published in the papers enumerated in the success criterion or found by the NOVELTY skeptic, passing the same perturbation, prediction and clean-accuracy checks. These are the defenses AutoAttack is known to over-estimate, so the attack must be run on the exact robustbench-loaded model (the operator / mixing network included), not on a surrogate."}
- {"id": "p3", "statement": "Attack-strength finding, not a leaderboard change: for one RN18/PreActRN18 CIFAR-100 Linf model, at least 50 test images that are still correctly classified after the skeptic's own standard AutoAttack run (version='standard', seed 0, on the same robustbench-loaded model) but are misclassified by the attacker's saved perturbations (eps and range checks as in the success criterion). The attacker's method must be a single disclosed procedure with a stated compute budget; a union over many AutoAttack seeds, restarts or random-start reruns of the standard attacks does not qualify, and the skeptic reports how many of the 50 standard AutoAttack with seed 1 also finds."}

## Verification

Skeptic's own script, on CPU: (1) pip-install robustbench from GitHub at a pinned commit and load the model with robustbench.utils.load_model(model_name, dataset='cifar100', threat_model='Linf'); record the sha256 of the downloaded weights file and confirm it matches a fresh download; model.eval. (2) Load torchvision CIFAR100(train=False) with ToTensor only, fine labels, standard order; recompute clean accuracy and require |clean - model_info clean_acc| <= 0.05. (3) Load the attacker's x_adv tensor; check shape (10000,3,32,32), dtype, then in float64: max|x_adv - x| <= 8/255 + 1e-6 and 0 <= x_adv <= 1 for every image. (4) Recompute adversarial argmax in eval mode in batches; robust_acc = mean(argmax(model(x_adv)) == y), with ties counted as correct (not fooled). (5) Re-fetch the live model_info JSON for the model, compute BAR as in the success criterion (also reading the four enumerated papers' tables and the NOVELTY skeptic's sweep), and require BAR - robust_acc >= 0.10. (6) For p3 run AutoAttack(version='standard', seed=0) from fra31/auto-attack on the same model and count images AutoAttack leaves correct that the attacker's x_adv fools. Every number quoted with URL and fetch time.

## Angles

- Wide targeted APGD: for each image unbroken by APGD-CE, run targeted DLR attacks against many more than the 9 wrong classes standard AutoAttack and MALT try (all 99 ranked by clean logit on an RN18 is cheap); this is the most obvious headroom on a 100-class problem.
- Restart-heavy APGD on the robust subset only, transfer-seeded starts from other CIFAR-100 robust models, hypercube-vertex local search, float64 gradients; target the RN18/PreActRN18 entries first, then WRN-28-10.
- Exploit the post-hoc defenses: for MeanSparse, attack the underlying model's features through the sparsification operator with a straight-through or smoothed surrogate (BPDA-style; the 42.25 external already came from APGD+BPDA, so beat that) and verify on the exact model; for MixedNUTS / Bai2023Improving adaptive-smoothing ensembles attack the mixing network's confidence pathway so the non-robust branch is selected.
- Square Attack with a large query budget (20k-50k) on the residual unbroken images of a small model; black-box success where white-box fails is the flagged over-estimation signal.
- Loss diversity per image: keep the best of CE, DLR, CW-margin, probability-margin (PMA) and a logit-difference-to-second-class loss with adaptive step sizes, selecting per image rather than per attack run.
- Prefer the ~18 models with no published stronger evaluation (p1 list): there the bar is the plain AutoAttack number and nobody has tried harder yet.

## Pitfalls

- Mixing up CIFAR-100 fine labels with coarse labels, applying normalisation before the robustbench model (it normalises internally), or using a differently ordered test set; recompute clean accuracy first and compare with the model_info clean_acc (must match to within 0.05 points) before trusting anything.
- Eps or range violations hidden by float32 saving or image formats; check in float64 on the saved tensor.
- Treating the leaderboard value or the 'external' value as the thing to beat is not enough: A3 Table 1 (12 CIFAR-100 models), AutoAE Table 1 (5), MALT Table 1 (4) and PMA/PMA+ Tables 3/6 (8) publish lower numbers that were never folded into the table (e.g. Gowal2020Uncovering_extra 36.88 listed vs 36.81 MALT; XCiT-L12 35.08 listed vs 34.95 PMA+). The NOVELTY skeptic must check all four plus 24 months of arXiv.
- Evaluation drift: PMA's own AutoAttack reruns differ from the RobustBench values by up to 0.13 points (XCiT-L12 35.04 vs 35.08), and A3 used eps 0.031 for the LBGAT models; differences under 10 images are noise, and a mismatch in clean accuracy means a different pipeline, not a stronger attack.
- Attacking a wrapper (softmax outputs, temperature scaling, different normalisation) instead of the robustbench-loaded model in eval mode, or counting clean-misclassified images as successes.
- For p3, a union over many AutoAttack seeds trivially produces extra broken images; that is seed variance, not attack strength.

## Sources

- https://robustbench.github.io/
- https://github.com/RobustBench/robustbench
- https://github.com/RobustBench/robustbench/tree/master/model_info/cifar100/Linf
- https://github.com/fra31/auto-attack
- https://arxiv.org/abs/2203.05154
- https://arxiv.org/abs/2211.12713
- https://arxiv.org/abs/2407.02240
- https://arxiv.org/abs/2411.15210
- Status source: https://robustbench.github.io/

## Citations

- [Problem page](../../../../.raw/V3R1T4S/known-unknowns/ml-robustness/robustbench-cifar100-linf-beat-autoattack.md)
- [Bank entry](../../../../.raw/V3R1T4S/bank/targets.json) (id `robustbench-cifar100-linf-beat-autoattack`, commit `7dd4480`)

## Related Nodes

- [[V3R1T4S ML robustness]]
- [[V3R1T4S]]
