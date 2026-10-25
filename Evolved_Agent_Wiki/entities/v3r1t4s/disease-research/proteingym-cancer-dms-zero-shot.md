---
id: v3r1t4s-proteingym-cancer-dms-zero-shot
type: entity
tags: [v3r1t4s, v3r1t4s/disease-research, kind/harvest]
inbound_links: 1
confidence: 0.8
last_ingested_sources: [".raw/V3R1T4S/bank/targets.json@7dd4480"]
status: "open"
priority: ""
notes: ""
category: disease-research
kind: harvest
tractability: 4
compute: "laptop-hours"
disclosure: open
status_checked: "2026-10-15"
---
# ProteinGym zero-shot: beat the best public Spearman on a cancer-gene deep-mutational-scanning assay

# Overview

> Bank id `proteingym-cancer-dms-zero-shot` · harvest · tractability 4 · laptop-hours · disclosure **open**
> Bank says open as of 2026-10-15. Statuses go stale — re-check the primary source before any work.

## Statement

ProteinGym maintains a public, machine-readable benchmark of variant-effect predictors scored against deep mutational scanning assays, with per-assay Spearman correlations for 98 models in a plain CSV in the GitHub repo (benchmarks/DMS_zero_shot/substitutions/Spearman/DMS_substitutions_Spearman_DMS_level.csv; repo last pushed 2026-03-25). Several assays are cancer genes, and the per-assay public bests are far from saturated as of 2026-10-13: BRCA1_HUMAN_Findlay_2018 best 0.560 (S3F-MSA; PoET 200M 0.558, S2F-MSA 0.551) over 1,837 mutants; PTEN_HUMAN_Mighell_2018 best 0.561 (S3F-MSA) over 7,260 mutants; PTEN_HUMAN_Matreyek_2021 best 0.516 (VenusREM) over 5,083; MSH2_HUMAN_Jia_2020 best 0.409 (ESCOTT) over 16,749; P53_HUMAN_Kotler_2018 best 0.722 (ProSST K=1024) over 1,048; RASK_HUMAN_Weng_2022_abundance best 0.470 (Progen2 XL) over 26,012; BRCA2_HUMAN_Erwood_2022_HEK293T best 0.534 (RITA L) over 265; plus ERBB2, additional P53 assays and the RASH/RASK series. Because 98 model score files are distributed with the benchmark, laptop agents can attack this without training any large model: principled combination, calibration and structure-aware re-ranking of existing public scores, or running a small open model (ESM-2 35M/150M, site-independent and MSA-based methods) on CPU, are both in budget. The per-assay frontier for a single cancer gene is a narrow, mechanically checkable record.

## Success criterion

Success means a saved score file assigning one real-valued fitness prediction to every mutant in the ProteinGym reference CSV for a chosen cancer-gene DMS assay (the assay's own reference file as distributed by ProteinGym, sha256 logged), produced by a method that is ZERO-SHOT with respect to that assay - it may use sequence, structure, MSAs, and other models' published score files, but no measurement from ANY ProteinGym DMS assay of the same UniProt protein may enter the method, and no hyperparameter, weight, threshold, model-selection decision or combination weight may be chosen using the target assay's labels - such that the Spearman correlation, recomputed by the skeptic with the official ProteinGym scoring convention (same mutant set, same direction convention, same NaN handling), is STRICTLY HIGHER (direction: max) than the maximum over all model columns for that assay in the live DMS-level Spearman CSV (re-fetched immediately before claiming) by at least 0.015 absolute. Any hyperparameter or combination weight must be fitted on a declared set of NON-cancer-gene assays, or on no data at all, and the fitting set must be logged with a sha256-stamped pre-registration file written before the target assay is scored. Deliverables: the score file, the pre-registration file, the method code, the list of external score files used with their provenance, and the skeptic-recomputable Spearman.

## Partial wins

- {"id": "p1", "statement": "Beat the live per-assay best by >= 0.015 Spearman on at least three cancer-gene assays simultaneously with ONE method and ONE frozen configuration (pre-registered, fitted only on non-cancer assays). Multi-assay consistency with a single configuration is far stronger evidence than a single-assay win."}
- {"id": "p2", "statement": "Beat the live best on MSH2_HUMAN_Jia_2020 (0.409 as of 2026-10-13, the weakest of the large cancer-gene assays, 16,749 mutants) by >= 0.02 Spearman under the same rules."}
- {"id": "p3", "statement": "A leakage-free combination audit: show, with pre-registered weights fitted only on non-cancer assays, how much of the gap between the single best model and the ensemble ceiling is reachable per cancer-gene assay, and publish the per-assay reachable-ceiling estimate (computed by a leave-assay-out protocol over the ~97 public score columns). A methodological result, checkable from the public CSV plus the published score files."}

## Verification

Skeptic downloads the ProteinGym reference file for the assay and the attacker's score file, checks the mutant sets match exactly (and the sha256 of the reference file), recomputes Spearman with scipy against the assay's DMS_score column following the official convention, and re-fetches the live DMS-level Spearman CSV to read the per-assay maximum over model columns (minutes). Then the skeptic re-runs the attacker's method end-to-end from the logged inputs (laptop-minutes to laptop-hours if it only combines published score files; longer if it runs a model) and confirms the score file is reproduced bit-for-bit or to within a documented tolerance. Leakage audit: confirm the pre-registration file predates the scoring logs, grep the method code and any cached artefacts for reads of the target assay's labels (including through 'validation' splits), and verify that the declared fitting assays share no UniProt ID with the target.

## Angles

- Conventional: rank-space ensembling of the ~97 published score columns with weights fitted by leave-assay-out on non-cancer assays (Borda / Copeland aggregation, or a rank-correlation-optimal weighting), which is cheap and frequently beats the single best model per assay.
- Conventional: assay-aware calibration - DMS assays measure different properties (abundance vs activity vs organismal fitness, a column in the CSV), so condition the ensemble weights on the assay's declared selection type and MSA depth category, both of which are metadata columns in the public CSV rather than labels.
- Cross-domain import (coding theory / soft-decision decoding): treat each public predictor as a noisy channel observation of the true fitness ordering and combine them with a log-likelihood-ratio (soft-decision) decoder whose channel reliabilities are estimated from non-cancer assays; this is strictly better than majority/mean rank fusion and is exactly how one combines unequal-quality observations.
- Cross-domain import (statistical physics / Potts models and direct coupling analysis): fit an epistatic Potts model on the protein's MSA (pseudo-likelihood DCA, CPU-cheap) and use its statistical energy as an additional predictor, including pairwise couplings that single-site models miss; for tumour-suppressor domains with deep MSAs this is a genuinely different signal from protein language models.
- Cross-domain import (compression): score a variant by the increase in description length of the protein family when the variant is inserted, using a compressor trained on the MSA (e.g. context-mixing or PPM over aligned columns); parameter-free, label-free, and uncorrelated with language-model scores, which is what an ensemble needs.
- Structure-aware re-ranking: use a public predicted structure to add solvent accessibility and contact-number features (not labels) as a monotone correction to the ensemble score, with the correction's shape fitted only on non-cancer assays.
- Small-model CPU runs: ESM-2 (8M/35M/150M) masked-marginal scoring, site-independent models, and MSA-based methods are all CPU-feasible on single proteins, so the agent can add fresh score columns rather than only recombining old ones.

## Pitfalls

- The target assay's labels are PUBLIC, which makes this benchmark trivially leakable: any weight, threshold, model choice or 'validation' decision informed by the target assay's DMS scores invalidates the claim. The pre-registration file with sha256 and the leave-assay-out fitting rule are the only defence, and the skeptic must check timestamps and code paths rather than trusting a claim of blindness.
- Protein-level leakage: several cancer genes appear in MULTIPLE ProteinGym assays (two PTEN assays, four P53 assays, two RASK/VKOR1 assays). Fitting on one assay of the same protein and scoring another is leakage even though the assay ids differ. Exclusion must be by UniProt ID, not by assay id.
- Scoring-convention drift: Spearman sign conventions, excluded mutants, multi-mutant vs single-mutant subsets, and NaN handling all shift the number by more than the 0.015 bar. The skeptic must recompute with the official convention against the official reference file, not the attacker's own mutant list.
- Ensemble selection bias: choosing WHICH of the ~97 columns to ensemble by looking at per-assay performance in the public CSV is itself using the target assay's labels (the CSV reports Spearman against those labels). Column selection must be pre-registered or derived from non-cancer assays only.
- Novelty trap: the published columns already include strong ensembles and retrieval-augmented models (TranceptEVE, ProSST, VenusREM, S3F-MSA, PoET, AIDO Protein-RAG, Protriever); matching or marginally exceeding a published ensemble is not a result, and the NOVELTY skeptic must check recent preprints for already-published higher per-assay values.
- Clinical over-claiming: a higher Spearman on a laboratory mutational scan of a cancer gene says nothing about any individual's variant interpretation, and the write-up must not frame it as variant classification for patients.

## Sources

- https://raw.githubusercontent.com/OATML-Markslab/ProteinGym/main/benchmarks/DMS_zero_shot/substitutions/Spearman/DMS_substitutions_Spearman_DMS_level.csv
- https://proteingym.org/benchmarks
- https://github.com/OATML-Markslab/ProteinGym
- Status source: https://raw.githubusercontent.com/OATML-Markslab/ProteinGym/main/benchmarks/DMS_zero_shot/substitutions/Spearman/DMS_substitutions_Spearman_DMS_level.csv

## Citations

- [Problem page](../../../../.raw/V3R1T4S/known-unknowns/disease-research/proteingym-cancer-dms-zero-shot.md)
- [Bank entry](../../../../.raw/V3R1T4S/bank/targets.json) (id `proteingym-cancer-dms-zero-shot`, commit `7dd4480`)

## Related Nodes

- [[V3R1T4S Disease research]]
- [[V3R1T4S]]
