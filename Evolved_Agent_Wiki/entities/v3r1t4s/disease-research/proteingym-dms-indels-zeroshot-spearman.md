---
id: v3r1t4s-proteingym-dms-indels-zeroshot-spearman
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
# ProteinGym indel benchmark (zero-shot): beat the best average Spearman on insertion/deletion DMS assays

# Overview

> Bank id `proteingym-dms-indels-zeroshot-spearman` · harvest · tractability 3 · laptop-hours · disclosure **open**
> Bank says open as of 2026-10-15. Statuses go stale — re-check the primary source before any work.

## Statement

ProteinGym's indel benchmark covers ~300k insertion/deletion mutants across 74 DMS assays (plus 1,555 clinical proteins). Indels are the neglected half of variant-effect prediction: the zero-shot indel leaderboard (summary CSV fetched 2026-10-13) has only ~24 baselines, nearly all autoregressive protein language models, and the frontier is PoET (200M) at average Spearman 0.517 (bootstrap SE 0.0), followed by ProGen2 M 0.465, ProGen2 Base 0.464, RITA L 0.457. A profile HMM scores 0.389 and WaveNet 0.368, i.e. plain alignment methods are within 0.13 of models with billions of parameters, and several categories are weak (low-MSA-depth 0.283 for the leader, Function_Expression 0.458). Most of the strong substitution-benchmark methods (GEMME, EVE, ESM-1b/1v, SaProt, ProSST, ESCOTT, VenusREM, RSALOR) are absent from the indel table entirely because they cannot score length changes, so a method that handles indels with alignment-and-profile machinery has unusually large headroom here on a CPU.

## Success criterion

Success means a saved score file with one real-valued score per mutant for ALL 74 indel DMS assays of the ProteinGym v1.3 indel benchmark (every assay, every mutant, mutated_sequence matched exactly), produced by a released zero-shot method (no training or tuning on any DMS_score in the benchmark, no per-assay hyperparameters, no use of the DMS_score_bin column), such that the repository's own scoring script (scripts/scoring_DMS_zero_shot/performance_substitutions_indels.sh, with the repo's aggregation: Spearman per assay, then by UniProt ID, then averaged across functional categories) yields an Average_Spearman STRICTLY GREATER (direction: max) than the best Average_Spearman in https://raw.githubusercontent.com/OATML-Markslab/ProteinGym/main/benchmarks/DMS_zero_shot/indels/Spearman/Summary_performance_DMS_indels_Spearman.csv , re-fetched live immediately before claiming, by at least 0.010 and by more than twice max(leader SE, runner-up SE, 0.005), with the skeptic computing a resampling interval over assays (the leader's Bootstrap_standard_error_Spearman is 0.0 as of 2026-10-15). The Function_Binding column is blank for the top rows, so no aggregation may invent a contribution from that category. Sign conventions must follow the benchmark (higher score = higher fitness); flipping signs per assay to rescue correlations is disqualifying.

## Partial wins

- {"id": "p1", "statement": "Beat the live best Average_Spearman in the Low_MSA_depth column (0.283 for PoET (200M) as fetched 2026-10-13) by >= 0.03 while staying within 0.02 of the live overall leader, with the full-benchmark score file and the repo's own aggregation."}
- {"id": "p2", "statement": "Beat every alignment-based baseline on the live indel table (profile HMM 0.389, WaveNet 0.368, Provean 0.347 as fetched 2026-10-13) by >= 0.03 average Spearman with a method that uses no neural network at all, end-to-end reproducible on a laptop in under 4 hours."}
- {"id": "p3", "statement": "Add a genuinely new baseline class to the indel benchmark: full-benchmark scores from a structure-aware or MSA-based method that the table currently lacks, reaching Average_Spearman >= 0.47 (i.e. above ProGen2 M/Base and RITA L as listed on 2026-10-13), with code, logs and a reproducible environment."}

## Verification

Skeptic downloads the v1.3 indel benchmark files per the repo README, verifies the attacker's score file has exactly one score per mutant for all 74 assays (counts and mutated_sequence hashes per assay, sha256 of the submission), confirms no DMS_score column was read by the scoring pipeline (code review plus running the attacker's scorer on a label-stripped copy of the inputs and checking identical outputs), runs the repository's indel performance script to recompute per-assay Spearman and the aggregation, and re-fetches the live summary CSV. Full re-scoring of 300k indel mutants by an alignment method is minutes to a few hours on CPU.

## Angles

- Profile-HMM done properly: the listed HMM baseline is a plain hmmer profile. Build per-family HMMs from deep, taxonomically reweighted MSAs, score indels with full forward-algorithm log-odds (not Viterbi), calibrate insert/delete state priors per family, and add length-aware normalisation; the table suggests this alone could approach the PLM frontier.
- CROSS-DOMAIN (compression / MDL): score an indel by the change in normalised compression distance between the mutated sequence and the family corpus (CTW, PPM, gzip-based NCD, or a family-specific grammar compressor). This is parameter-free, handles length changes natively (unlike substitution-only scorers), and is cheap on CPU.
- CROSS-DOMAIN (string algorithms / edit-distance geometry): treat each indel as a move in an edit-distance metric space and score it by the cost of the cheapest alignment of the mutant to the family profile under affine gap penalties learned from the family's own gap statistics (Gotoh with family-fitted gap opening/extension), including repeat-aware penalties from tandem-repeat detection.
- CROSS-DOMAIN (signal processing): represent the sequence as a multichannel signal of physicochemical property tracks, and treat insertions/deletions as phase runs; score by spectral/periodicity disruption (helical 3.6-residue periodicity, beta-strand alternation), which detects frame-like disruption that substitution models miss.
- CROSS-DOMAIN (ecology / community statistics): use MSA column occupancy and gap-pattern co-occurrence as a species-abundance problem (Hill numbers, rarefaction) to estimate how tolerant each region is to length change, giving a per-position indel-tolerance prior.
- Ensembling and calibration: combine a cheap alignment score with per-assay-independent rank normalisation and isotonic calibration per functional category; aggregate with rank-fusion rather than score averaging, since the metric is Spearman.
- Structure-informed gap tolerance: use public AlphaFold DB models for the target proteins to score indels by loop-versus-core location and by predicted local disorder, filling a model class the indel table currently lacks entirely.

## Pitfalls

- Fitting to the labels: indel assays are small, so any per-assay tuning (choosing a gap penalty, a window, or a sign per assay by looking at Spearman) is overfitting and must be rejected; the benchmark is zero-shot by definition.
- Partial coverage: scoring only the easy assays, or only single-residue indels, then comparing to an average computed over all 74 assays and all mutants. Low-MSA-depth and viral assays are the hardest and are exactly where the average is won or lost.
- Wrong aggregation: taking a plain mean over assays instead of the repository's UniProt-then-category aggregation, or comparing against the substitution leaderboard's numbers (0.5 vs 0.4 scales differ) or against the website rendering instead of the live CSV.
- MSA leakage: building alignments with a database or search that includes the assayed mutant sequences themselves (some DMS libraries are deposited), which silently injects labels through homology; search databases must predate or exclude the assay sequences.
- Seed and alignment variance: Spearman differences under 0.01 are within run-to-run MSA variance; a record needs margin over twice the listed bootstrap SE and a rerun from a clean environment.
- Function_Binding is empty for the leading rows of the indel summary CSV, so category aggregation is effectively over Activity/Expression; a claim must not be aggregated in a way that imputes a Function_Binding score.

## Sources

- https://raw.githubusercontent.com/OATML-Markslab/ProteinGym/main/benchmarks/DMS_zero_shot/indels/Spearman/Summary_performance_DMS_indels_Spearman.csv
- https://github.com/OATML-Markslab/ProteinGym
- https://github.com/OATML-Markslab/ProteinGym/tree/main/benchmarks
- https://proteingym.org/benchmarks
- Status source: https://raw.githubusercontent.com/OATML-Markslab/ProteinGym/main/benchmarks/DMS_zero_shot/indels/Spearman/Summary_performance_DMS_indels_Spearman.csv

## Citations

- [Problem page](../../../../.raw/V3R1T4S/known-unknowns/disease-research/proteingym-dms-indels-zeroshot-spearman.md)
- [Bank entry](../../../../.raw/V3R1T4S/bank/targets.json) (id `proteingym-dms-indels-zeroshot-spearman`, commit `7dd4480`)

## Related Nodes

- [[V3R1T4S Disease research]]
- [[V3R1T4S]]
