---
id: v3r1t4s-immrep22-tcr-epitope-microauc
type: entity
tags: [v3r1t4s, v3r1t4s/disease-research, kind/harvest]
inbound_links: 1
confidence: 0.8
last_ingested_sources: [".raw/V3R1T4S/bank/targets.json@7dd4480"]
status: "CONFIRMED_SOLUTION"
priority: ""
notes: ""
category: disease-research
kind: harvest
tractability: 4
compute: "laptop-hours"
disclosure: open
status_checked: "2026-10-15"
---
# IMMREP22 TCR-epitope specificity: beat the best published per-epitope micro-AUC on the public paired-chain benchmark

# Overview

> Bank id `immrep22-tcr-epitope-microauc` · harvest · tractability 4 · laptop-hours · disclosure **open**
> Bank says open as of 2026-10-15. Statuses go stale — re-check the primary source before any work.

## Statement

Deciding which T-cell receptor recognises which peptide is the computational bottleneck of neoantigen-directed cell therapy: once a tumour peptide is nominated, somebody has to guess which TCRs in a patient's repertoire can see it. The IMMREP22 workshop (Working Group 6 of the 2022 Dresden 'Dynamics of Immune Repertoires' workshop, organised by Morten Nielsen, Virag Sharma and colleagues; Nielsen et al., ImmunoInformatics 2023) froze a fully public benchmark for exactly this task: paired alpha/beta TCRs from VDJdb with annotated specificity to 17 peptides, plus an unpublished healthy-donor CD8 control repertoire from A. Eugster used as negatives, split 80:20 into training and test per epitope, with CDR1/CDR2/CDR3 of both chains pre-extracted (Stitchr + ANARCI). Everything needed to score a model is in the repository: training_data/, test_set/ with labels, negativeData_controls/, evaluation/evaluate.py, and the result tables for 22 published method variants. As re-read live on 2026-10-15 from evaluation/microaucs.csv, the best average micro-AUC across the 17 epitopes is 0.8473 (tcrexab), then TCRGP 0.8468, tcrdist3 0.8403, tcrexb 0.8301, netTCR_cdr123ab 0.8246, TCRAI 0.8234; the random baseline sits at 0.4901. Per-epitope the spread is enormous (for ATDALMTGF several methods exceed 0.95 while for NQKLIANQF most sit near 0.5), so the frontier is not one number but seventeen, and the data are a few thousand short amino-acid strings: this is a CPU-only, laptop-hours problem where kernel methods and careful negative handling have repeatedly beaten deep models.

## Success criterion

Success means a saved prediction file giving one real-valued score to every TCR in the IMMREP22 test_set/ file for a chosen epitope (or for all 17), produced by a model trained only on that epitope's training_data/ file plus the released control repertoire, scored with the repository's own evaluation/evaluate.py at a pinned commit, whose micro-AUC is STRICTLY HIGHER (direction: max) than the maximum over ALL method rows in the live https://raw.githubusercontent.com/viragbioinfo/IMMREP_2022_TCRSpecificity/main/evaluation/microaucs.csv - re-fetched and re-parsed immediately before claiming - by at least 0.02 absolute on the _Average column, or by at least 0.03 absolute on a single named epitope column. No test-set TCR, and no label of any test-set TCR, may enter training, feature construction, hyperparameter selection, early stopping or thresholding; hyperparameters may be chosen only by cross-validation inside the training file of OTHER epitopes or inside the training split of the same epitope. The claim must ship: the pinned commit and sha256 of the data files used, the training script, the per-epitope score files, the verbatim evaluate.py output, and a same-environment re-run of at least two published baselines whose micro-AUCs land within 0.01 of the published values (otherwise the comparison is void).

## Partial wins

- {"id": "p1", "statement": "Beat the live best micro-AUC by >= 0.03 on each of the five hardest epitopes (as of 2026-10-15 the columns where the published best stays under 0.80: NQKLIANQF, TTDPSFLGRY, LTDEMIAQY, NLVPMVATV, TPRVTGGGAM), with one frozen configuration chosen without looking at those epitopes' test labels."}
- {"id": "p2", "statement": "Beat the live best average rank in evaluation/epitoperank.csv (3.284, tcrexab, as of 2026-10-15; lower is better) by >= 0.25 under the same no-leakage protocol, which measures consistency across epitopes rather than a single lucky column."}
- {"id": "p3", "statement": "A negative-sampling audit of record: show, with the released control repertoire, how much of each published method's micro-AUC is explained by distinguishing VDJdb-derived TCRs from healthy-donor control TCRs rather than by epitope specificity, by re-scoring the SAME predictions against (a) swapped-epitope negatives only and (b) control-repertoire negatives only. Mechanically checkable from the saved scores and not reported in the published tables."}

## Verification

Skeptic clones the repository at the attacker's pinned commit, checks sha256 of training_data/, test_set/ and negativeData_controls/ against the attacker's manifest, confirms that every test TCR appears exactly once in the attacker's score file and that no test TCR string occurs in the training file used, re-runs evaluation/evaluate.py on the supplied scores (minutes) and then re-trains the attacker's model end-to-end (laptop-minutes to laptop-hours) to confirm the micro-AUC is reproduced. The live record is read by curling microaucs.csv and taking the column maximum with the skeptic's own script. Leakage audit: grep the training code for any read of test_set/, check that no sequence-similarity index was built over the test file, and confirm the control TCRs used as negatives in training are disjoint from those in the test file.

## Angles

- Conventional: distance-based classifiers over the full CDR1/CDR2/CDR3 of both chains (the repository ships A1/A2/A3 and B1/B2/B3) with a learned substitution metric; the current leaders are a nearest-neighbour method and a Gaussian process, so the frontier is about the metric, not the architecture.
- Conventional: proper handling of the two negative classes - swapped-epitope negatives and healthy-donor control negatives have different statistics, and reweighting or training two heads and combining them is an obvious and untested move.
- Cross-domain import (cryptanalysis / distinguisher design): treat specificity prediction as a distinguishing game between two generative sources of CDR3 sequences and build an explicit log-likelihood-ratio distinguisher, where each source is modelled by a V(D)J generation model (the standard IGoR/SONIA machinery) corrected by an epitope-specific selection factor. This directly optimises the quantity the AUC measures instead of a surrogate classification loss.
- Cross-domain import (compression / normalised compression distance): define TCR-TCR similarity by the compressibility of concatenated CDR sequences, which needs no alignment, no substitution matrix and no training, and use it as a kernel; parameter-free similarity measures are strongest exactly in the small-sample regime these per-epitope training sets occupy (dozens to a few hundred positives).
- Cross-domain import (ecology / species-abundance statistics): a repertoire is a sample from a highly uneven community, so Good-Turing and rarefaction estimators give a principled correction for how much of an apparent epitope-specific motif is sampling depth rather than signal; use the correction to down-weight motifs that look specific only because of unequal sampling.
- Cross-domain import (statistical physics): fit a Potts/direct-coupling model over aligned CDR3 positions per epitope and use the statistical energy as the score, capturing pairwise residue couplings that position-weight matrices miss; pseudo-likelihood DCA on a few hundred sequences runs in seconds on a CPU.
- Multi-epitope transfer: train one model across all 17 epitopes with the peptide as an input (rather than 17 independent models) and measure whether sharing helps or hurts per-epitope micro-AUC; the published tables mix both styles and never isolate this.

## Pitfalls

- Negative-set artefacts dominate this benchmark: positives come from VDJdb and many negatives come from one control cohort, so a model can score well by detecting dataset provenance (sequencing protocol, V-gene usage, CDR3 length distribution) rather than specificity. Any claim must include the negative-source ablation, and a win that vanishes when only swapped-epitope negatives are used must be reported as such.
- Test-label peeking is trivially easy because the test files ship with labels in the repository. The skeptic must re-run training from the attacker's code rather than trust a score file, and must grep for reads of test_set/.
- Near-duplicate TCRs: VDJdb aggregates studies, so clonally related or identical CDR3s can straddle the 80:20 split. Report the maximum similarity (e.g. TCRdist or Levenshtein) between each test TCR and the training set, and show the gain is not confined to the near-duplicate tail.
- Metric substitution: micro-AUC pooled over an epitope is not the same as macro-AUC, average precision, or the epitope-rank metric in epitoperank.csv; comparing one against a record from another is a fatal error, and small epitopes swing by far more than the 0.02 bar.
- Stale-table comparison: the record must be re-read from the live CSV, and the NOVELTY check must look for later papers reporting higher numbers on this exact benchmark (several re-benchmarks of IMMREP data have appeared since 2023).
- Over-claiming: a higher AUC on 17 mostly viral epitopes with laboratory negatives says nothing about finding tumour-reactive TCRs in a patient, where the epitopes are private neoantigens and the negative space is astronomically larger. The write-up must say so.

## Sources

- https://github.com/viragbioinfo/IMMREP_2022_TCRSpecificity
- https://raw.githubusercontent.com/viragbioinfo/IMMREP_2022_TCRSpecificity/main/evaluation/microaucs.csv
- https://raw.githubusercontent.com/viragbioinfo/IMMREP_2022_TCRSpecificity/main/evaluation/epitoperank.csv
- https://doi.org/10.1016/j.immuno.2023.100024
- Status source: https://raw.githubusercontent.com/viragbioinfo/IMMREP_2022_TCRSpecificity/main/evaluation/microaucs.csv

## Citations

- [Problem page](../../../../.raw/V3R1T4S/known-unknowns/disease-research/immrep22-tcr-epitope-microauc.md)
- [Bank entry](../../../../.raw/V3R1T4S/bank/targets.json) (id `immrep22-tcr-epitope-microauc`, commit `7dd4480`)

## Related Nodes

- [[V3R1T4S Disease research]]
- [[V3R1T4S]]
