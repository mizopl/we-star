---
id: v3r1t4s-proteingym-clinical-substitutions-auc
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
tractability: 2.5
compute: "laptop-hours"
disclosure: open
status_checked: "2026-10-15"
---
# ProteinGym clinical substitutions (ClinVar benign/pathogenic): beat the leaderboard's best average AUC

# Overview

> Bank id `proteingym-clinical-substitutions-auc` · harvest · tractability 2.5 · laptop-hours · disclosure **open**
> Bank says open as of 2026-10-15. Statuses go stale — re-check the primary source before any work.

## Statement

ProteinGym's clinical substitution benchmark scores variant-effect predictors on annotated human clinical missense variants (benign vs pathogenic) across 2,525 clinical proteins (count to be re-derived from the pinned v1.3 release notes at claim time), aggregated by UniProt ID and by functional category, reported as average AUC with a bootstrapped standard error. The public summary table (fetched 2026-10-13) is topped by PoET (200M) at 0.920, TranceptEVE L 0.920, GEMME 0.919, EVE 0.914, ESM-1b 0.892, then the dbNSFP clinical predictors (Provean 0.886, SIFT 0.878, SIFT4G 0.877, MutationAssessor 0.877, MutPred 0.875, PrimateAI 0.855, LIST-S2 0.842, LRT 0.805). Only a handful of the ~35 baselines present on the DMS leaderboards have been scored on the clinical benchmark at all, and the top of the table is a dead heat between an MSA-conditioned generative model and a 2019 epistatic-conservation method (GEMME), which runs in minutes per family on a CPU. Whether a cheap alignment-statistics or ensemble method can pass 0.920 on this benchmark is open, and the repository explicitly invites new baselines ('How to contribute?').

## Success criterion

Success means a saved score file giving one real-valued score per variant for EVERY variant in the ProteinGym clinical substitution benchmark (v1.3 release, all clinical protein files, no proteins dropped), produced by a method whose code and inputs are released, such that the benchmark's own scoring script (scripts/scoring_DMS_zero_shot/*, performance computed exactly as in the repository: AUC per protein, aggregated by UniProt ID then across functional categories) yields an Average_AUC STRICTLY GREATER (direction: max) than the best Average_AUC in https://raw.githubusercontent.com/OATML-Markslab/ProteinGym/main/benchmarks/clinical_zero_shot/substitutions/AUC/Summary_performance_clinical_substitutions_AUC.csv , re-fetched live immediately before claiming, by at least 0.005 absolute AND by more than twice max(leader SE, runner-up SE, 0.002), with the skeptic recomputing a target-resampling interval (the leader's Bootstrap_standard_error_AUC is 0.0 as of 2026-10-15, so the row SE alone is not a constraint). The method must not use, directly or as a feature, any clinical label source for the benchmark proteins (ClinVar, HGMD, dbNSFP pathogenicity columns, gnomAD-trained pathogenicity scores, or any supervised pathogenicity predictor), and must be applied uniformly to all proteins with no per-protein tuning. A run whose score file omits variants, or re-bins/re-thresholds the labels, does not count.

## Partial wins

- {"id": "p1", "statement": "Beat the best MSA-free (single-sequence) baseline's Average_AUC on the live clinical substitutions table by > 2 bootstrap SEs using only single-sequence information, no alignments and no structures."}
- {"id": "p2", "statement": "Beat GEMME's live Average_AUC (an alignment-only method) with a method that is itself alignment-only and runs end-to-end on a laptop in under 6 hours wall clock for the whole benchmark, with timing logs."}
- {"id": "p3", "statement": "A reproducible per-protein audit: a list of >= 50 clinical proteins where the leaderboard-leading model's released scores give AUC < 0.6, together with a method that exceeds AUC 0.8 on those same proteins without degrading the overall Average_AUC below the live leader minus 0.005."}

## Verification

Skeptic clones OATML-Markslab/ProteinGym at a pinned commit, downloads the v1.3 clinical substitution benchmark (curl from marks.hms.harvard.edu as documented in the repo README), checks the attacker's score file covers exactly the benchmark variant set (row counts and mutant ids per protein, sha256 of the submitted file), runs the repository's own performance scripts to recompute AUC per protein and the UniProt/category aggregation, and re-fetches the live summary CSV for the current leader (its header has a duplicated Model_rank column, so parse it explicitly rather than with a naive read_csv). The protein count and the scoring-script path are re-derived from the pinned v1.3 release notes at claim time. Label-leakage audit: grep the attacker's code and any model weights/manifest for dbNSFP, ClinVar, HGMD or gnomAD-derived pathogenicity inputs, and confirm the released pipeline reproduces the submitted scores for a random sample of 20 proteins on the skeptic's machine.

## Angles

- Cheap-and-strong alignment statistics: rebuild deep MSAs per protein (jackhmmer/MMseqs2 against UniRef) and combine site-specific conservation, pairwise couplings (plmDCA/pseudo-likelihood) and solvent-accessibility weighting in the spirit of RSALOR and GEMME; the open question is whether better MSA construction (depth, diversity reweighting, taxonomic filtering) alone passes 0.920.
- CROSS-DOMAIN (coding theory / information theory): treat each protein family alignment as a noisy channel code and score a variant by its syndrome weight under a learned low-density parity-check-style factor graph over coupled columns; minimum-description-length (compression) scoring of 'sequence with variant' versus 'sequence without' gives a parameter-free pathogenicity index that can be computed with gzip/CTW-style universal compressors over aligned columns.
- CROSS-DOMAIN (statistical physics): compute variant effects as free-energy differences in a Potts model of the family fitted by pseudo-likelihood, including entropic contributions from a local sampling of the sequence neighbourhood (thermodynamic integration / umbrella sampling over mutational coordinates) rather than a single point energy.
- CROSS-DOMAIN (phylogenetics as signal processing): score variants by rate-shift detection on the family tree, i.e. a matched filter over per-site substitution-rate spectra across clades (SiteRM-style ultrafast phylogenetics beat large PLMs on variant effect), which is pure CPU work.
- Rank aggregation: ensemble the public per-protein scores of existing baselines with Borda/Copeland voting, Thurstone models, or isotonic calibration per MSA-depth bin; leaderboards aggregate by category, so improving the worst categories (low-MSA-depth, small proteins) matters more than the average.
- Target the structure of the metric: AUC is aggregated per protein, so proteins with few variants dominate variance; invest compute in deep MSAs for exactly those proteins, and use conformal/variance-aware shrinkage toward a conservation prior where alignments are shallow.
- CROSS-DOMAIN (linguistics): borrow distributional-semantics tests (collocation strength, mutual information between columns, morphological alternation detection) to detect positions under grammar-like constraint, then weight variant penalties by constraint type instead of by raw conservation.

## Pitfalls

- Label leakage through dbNSFP-derived features or any pathogenicity predictor trained on ClinVar: the benchmark's clinical labels come from the same curated sources, so any supervised pathogenicity score (or a PLM fine-tuned on ClinVar) inflates AUC without being a real advance. The clinical baselines on this table are deliberately unsupervised or classic conservation tools.
- Protein-set cherry-picking: dropping hard proteins, scoring only proteins with many variants, or scoring a subset and comparing to a table computed on all 2,525 proteins. The aggregation (by UniProt ID, then by category) must be rerun with the repository's script on the full set.
- Benchmark-version confusion: the summary CSV is regenerated as new baselines land, and the DMS and clinical tables share model names. Comparing to a cached number, to the DMS substitutions AUC, or to the website's rendering instead of the live CSV is a false positive; direction is max and the bar is the live best row.
- Bootstrap noise: Average_AUC differences of 0.001-0.003 are inside the reported bootstrap SE; also MSA re-generation changes alignment-based scores run to run, so a single lucky MSA seed is not a record.
- Circularity in evaluation: many 'benign' labels are frequency-derived, so a method using allele frequency (gnomAD) re-derives the label definition. Even a weak frequency feature must be treated as leakage.

## Sources

- https://raw.githubusercontent.com/OATML-Markslab/ProteinGym/main/benchmarks/clinical_zero_shot/substitutions/AUC/Summary_performance_clinical_substitutions_AUC.csv
- https://github.com/OATML-Markslab/ProteinGym
- https://raw.githubusercontent.com/OATML-Markslab/ProteinGym/main/README.md
- https://github.com/OATML-Markslab/ProteinGym/tree/main/benchmarks
- https://proteingym.org/benchmarks
- Status source: https://raw.githubusercontent.com/OATML-Markslab/ProteinGym/main/benchmarks/clinical_zero_shot/substitutions/AUC/Summary_performance_clinical_substitutions_AUC.csv

## Citations

- [Problem page](../../../../.raw/V3R1T4S/known-unknowns/disease-research/proteingym-clinical-substitutions-auc.md)
- [Bank entry](../../../../.raw/V3R1T4S/bank/targets.json) (id `proteingym-clinical-substitutions-auc`, commit `7dd4480`)

## Related Nodes

- [[V3R1T4S Disease research]]
- [[V3R1T4S]]
