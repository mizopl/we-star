---
id: v3r1t4s-tcga-multiomics-survival-cindex-herrmann
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
tractability: 3
compute: "laptop-hours"
disclosure: open
status_checked: "2026-10-15"
---
# TCGA multi-omics survival: beat the best published C-index or integrated Brier score for a cancer cohort in the Herrmann benchmark

# Overview

> Bank id `tcga-multiomics-survival-cindex-herrmann` · harvest · tractability 3 · laptop-hours · disclosure **open**
> Bank says open as of 2026-10-15. Statuses go stale — re-check the primary source before any work.

## Statement

Moritz Herrmann, Philipp Probst, Roman Hornung, Vindi Jurinovic and Anne-Laure Boulesteix (Briefings in Bioinformatics 22(3), bbaa167, 2021) ran the largest honest comparison of survival-prediction methods on multi-omics cancer data: 18 TCGA cohorts, each with clinical variables plus copy number, miRNA, mutation and RNA features (about 100,000 features, 100-735 patients per cohort), 13 learners including Lasso, IPF-Lasso, priority-Lasso, GRridge, SGL, model-based and likelihood-based boosting, random forests, block forests, a clinical-only Cox model and Kaplan-Meier, all compared with repeated 5-fold cross-validation under Uno's C-index and the integrated Brier score. Their headline is sobering and still unbeaten in public: for most cohorts the molecular data add little or nothing over clinical variables alone. The per-cohort records are a literal published table (Table 5), machine-readable from the Europe PMC full-text XML: for example BLCA C-index 0.640 (CoxBoost favoring), BRCA 0.643 (CoxBoost favoring), COAD 0.656 (blockForest, versus clinical-only 0.541), HNSC 0.582 (blockForest), KIRC 0.761 (clinical only), KIRP 0.629 (GRridge), LAML 0.709 (ranger, versus clinical-only 0.596), LGG 0.749 (glmboost), LUAD 0.665 (prioritylasso), LUSC 0.537, OV 0.600, PAAD 0.686, SARC 0.685, SKCM 0.597, STAD 0.598, UCEC 0.686; integrated Brier scores are listed in the same row. The preprocessed data are on OpenML without registration (dataset ids in the repository's data/datset_ids.txt, e.g. BLCA 42279/42280, about 140 MB per part) and the full benchmark code is public, so a laptop can re-run a single cohort in hours.

## Success criterion

Success means, for one named TCGA cohort of the 18, a saved per-fold risk-prediction file produced under the benchmark's own protocol (the published cross-validation design, the OpenML datasets named in data/datset_ids.txt with their sha256 logged, the same feature blocks), such that EITHER (a) Uno's C-index, computed with the benchmark's own evaluation code over the same folds, is STRICTLY HIGHER (direction: max) than that cohort's C-index value in Table 5 of https://www.ebi.ac.uk/europepmc/webservices/rest/PMC8138887/fullTextXML - re-fetched and re-parsed immediately before claiming - by at least 0.02 absolute AND by more than the half-width of the published confidence interval for that cell; OR (b) the integrated Brier score is STRICTLY LOWER (direction: min) than that cohort's published ibrier by at least 0.01 absolute and by more than the published interval half-width. The attacker must additionally re-run, in the same environment and folds, the clinical-only Cox model and the published best learner for that cohort, and must beat BOTH the re-run values and the published values. Model selection, feature filtering, imputation and hyperparameter tuning must happen inside each training fold only; a single tuning decision made on full-cohort data voids the claim. Deliverables: the OpenML ids and sha256s, the fold assignment, the training code, per-fold predictions, and the verbatim metric output.

## Partial wins

- {"id": "p1", "statement": "Beat the clinical-only Cox reference by >= 0.03 Uno C-index on a cohort where Table 5 reports that no molecular learner beat clinical-only (as of 2026-10-15: ESCA, KIRC, STAD, UCEC for the C-index), with the full fold protocol and the same-environment clinical-only re-run. This is the benchmark's central open question, not a leaderboard decimal."}
- {"id": "p2", "statement": "Beat the published best C-index by >= 0.02 on three or more cohorts with ONE frozen method and one hyperparameter protocol, reported across all 18 cohorts so that cherry-picking is visible."}
- {"id": "p3", "statement": "A reproducibility result of record: re-run three published learners (blockForest, priority-Lasso, CoxBoost favoring) on five cohorts with the published code and report the discrepancy against Table 5 with full logs. Independently checkable and useful whether or not any record falls; must be reported as reproduction, not as a win."}

## Verification

Skeptic downloads the cohort's OpenML parts (about 140-300 MB per cohort, no registration), checks sha256 against the attacker's manifest, verifies the fold assignment matches the benchmark protocol and that no patient appears in both sides of a fold, re-computes Uno's C-index and the integrated Brier score from the attacker's per-fold risk files with their own script using the same evaluation time range convention, and re-fetches the Europe PMC XML to read the live Table 5 values. Then the skeptic re-runs the attacker's training for at least two folds (laptop-hours) and the clinical-only reference. Leakage audit: confirm that feature screening, imputation, standardisation and any block-weight estimation were performed inside training folds only, and that no outcome-derived feature crossed a fold boundary.

## Angles

- Conventional: block-structured regularisation done better - estimate per-block penalties by empirical Bayes rather than by the nested cross-validation the published priority-Lasso and IPF-Lasso use, which is extremely noisy at 100-300 patients.
- Conventional: target the metric. Uno's C-index is a rank statistic; train with a smooth concordance surrogate or a partial-likelihood plus rank penalty instead of pure partial likelihood, and calibrate separately for the Brier score.
- Cross-domain import (random matrix theory): the RNA and copy-number blocks are wide and noisy; Marchenko-Pastur eigenvalue shrinkage keeps only components outside the noise bulk before the Cox fit, which is the principled version of 'take the top principal components' and costs seconds.
- Cross-domain import (econometrics / instrumental thinking about confounding): clinical stage and age carry most of the signal and are correlated with molecular blocks; estimate the molecular contribution orthogonalised against the clinical model (partialling-out / double machine learning) so that the question 'do omics add anything' is answered with a procedure designed for exactly that question.
- Cross-domain import (reliability engineering / accelerated life testing): borrow parametric accelerated-failure-time families with covariate-dependent scale, which are standard in reliability and rarely tried in these benchmarks, and which can beat Cox models when hazards are non-proportional.
- Cross-domain import (compression / MDL): select the number of features per block by two-part code length rather than cross-validated partial likelihood; with 100-700 patients, selection noise is the dominant error source.
- Honest pooling: fit one model across cohorts with cohort-specific baseline hazards (stratified Cox or a hierarchical prior) to borrow strength for the small cohorts, which the per-cohort published protocol never does.

## Pitfalls

- Fold-boundary leakage through preprocessing is the dominant trap: variance filtering, imputation, standardisation, PCA or block-weight estimation performed on the whole cohort uses test patients' molecular data and inflates the C-index by far more than the 0.02 bar.
- Metric mismatch: Uno's C-index depends on the censoring-distribution weights and the chosen time range; Harrell's C-index, Antolini's time-dependent C-index and IPCW variants all give different numbers. Only the benchmark's definition and time range count.
- Small cohorts and wide intervals: several cohorts have fewer than 40 events (COAD 17, BRCA 72), so cross-validation estimates swing wildly. The margin must exceed the published interval half-width, and a win on one cohort with one seed is noise.
- Clinical-variable confusion: some published bests ARE the clinical-only Cox model; beating 'the molecular methods' while losing to clinical-only is not a win, and the write-up must state which reference was beaten.
- Dataset version drift: the OpenML datasets are split into two or three parts per cohort and must be rejoined exactly as the benchmark code does; a different join or a different feature-block assignment makes the comparison meaningless.
- Over-claiming: a better cross-validated C-index on a retrospective TCGA cohort is not a prognostic test for a patient, and these cohorts are old, heterogeneously treated and not representative of current care.

## Sources

- https://www.ebi.ac.uk/europepmc/webservices/rest/PMC8138887/fullTextXML
- https://github.com/HerrMo/multi-omics_benchmark_study
- https://raw.githubusercontent.com/HerrMo/multi-omics_benchmark_study/master/data/datset_ids.txt
- https://doi.org/10.1093/bib/bbaa167
- Status source: https://www.ebi.ac.uk/europepmc/webservices/rest/PMC8138887/fullTextXML

## Citations

- [Problem page](../../../../.raw/V3R1T4S/known-unknowns/disease-research/tcga-multiomics-survival-cindex-herrmann.md)
- [Bank entry](../../../../.raw/V3R1T4S/bank/targets.json) (id `tcga-multiomics-survival-cindex-herrmann`, commit `7dd4480`)

## Related Nodes

- [[V3R1T4S Disease research]]
- [[V3R1T4S]]
