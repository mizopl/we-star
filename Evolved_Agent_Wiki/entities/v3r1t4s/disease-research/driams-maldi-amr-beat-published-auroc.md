---
id: v3r1t4s-driams-maldi-amr-beat-published-auroc
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
# DRIAMS MALDI-TOF resistance prediction: beat the published per-species-drug AUROC on the public spectra

# Overview

> Bank id `driams-maldi-amr-beat-published-auroc` · harvest · tractability 3 · laptop-hours · disclosure **open**
> Bank says open as of 2026-10-15. Statuses go stale — re-check the primary source before any work.

## Statement

DRIAMS ('Database of Resistance Information on Antimicrobials and MALDI-TOF Mass Spectra', Dryad version 12 of 2025-08-19, CC0, 144 GB; mirrored on Zenodo record 5640517 as DRIAMS_A 86 GB, DRIAMS_B 3.7 GB, DRIAMS_C 12.4 GB and DRIAMS_D 42.6 GB, because Dryad's file endpoints are gated for plain downloads) is a public collection of ~300k clinical MALDI-TOF mass spectra with linked antimicrobial susceptibility labels from four hospitals, released with the Weis et al. study that predicted resistance directly from spectra and reported per-species-drug AUROC (notably for Staphylococcus aureus/oxacillin, Escherichia coli and Klebsiella pneumoniae/ceftriaxone). The accompanying code is public (github.com/BorgwardtLab/maldi_amr, frozen since 2022-10-07, so there is no maintained leaderboard: the bar is the paper). A claim must state which DRIAMS site it uses; the smaller sites, or the binned_6000 spectra of one site and species-drug pair, keep it laptop-sized. Spectra are 1-D signals of a few thousand bins, so training and evaluation are minutes-to-hours on a CPU, and the published AUROCs leave real headroom - particularly for cross-hospital (site-transfer) evaluation, which the original work flags as the hard regime. Rapid resistance phenotyping from routine mass spectra is a neglected, high-leverage corner of AMR with almost no community benchmark activity.

## Success criterion

Success means, for at least one species-antibiotic pair, a released model and saved per-spectrum predictions evaluated on a split that is defined before training and is at least as strict as the published one (same DRIAMS site, same species-drug pair, same label definition; patient/isolate identifiers never split across train and test), whose AUROC exceeds the published AUROC for that same species-drug pair and split regime (read live from the Weis et al. paper and github.com/BorgwardtLab/maldi_amr immediately before claiming) by at least 0.02 AND outside a 95% bootstrap interval over test spectra, with the number of positives/negatives, the full ROC and a precision-recall curve reported alongside. Spectra preprocessing must be the published pipeline or a documented superset applied identically to train and test, and the exact DRIAMS version and split files (sha256) must be published with the claim. A cross-site claim (train on site A, test on site B) must be compared only against published cross-site numbers.

## Partial wins

- {"id": "p1", "statement": "Beat the published cross-hospital (site-transfer) AUROC for one species-drug pair by >= 0.02 with no target-site labels used in training, bootstrap interval excluding zero."}
- {"id": "p2", "statement": "Match the published same-site AUROC to within 0.01 using only a linear model on <= 50 interpretable mass bins (peak list), with the bins named and the model released - an interpretability result, reported as such."}
- {"id": "p3", "statement": "A reproducible confound audit: demonstrate with held-out data how much of the published performance for one species-drug pair is attributable to species/site/acquisition-batch signal rather than resistance (e.g. by label permutation within batch, batch-only predictors, and acquisition-date splits), quantified and released as code."}

## Verification

Skeptic downloads the pinned DRIAMS version from the Zenodo mirror (record 5640517, plain HTTPS with range requests; DRIAMS-A alone is 86 GB, so fetch the declared site and use its binned_6000 spectra for the single species-drug pair claimed), verifies the attacker's split files by sha256 and checks no isolate/patient identifier appears in both train and test, reruns the attacker's released preprocessing and model to regenerate predictions, computes AUROC and AUPRC with bootstrap intervals, and re-reads the published numbers from the paper and the maldi_amr repo. Confound checks: train a predictor on acquisition metadata alone and on permuted labels within batch, and confirm the claimed signal is not reproduced.

## Angles

- CROSS-DOMAIN (signal processing, the natural fit): treat each spectrum as a signal, not a feature vector - baseline estimation (asymmetric least squares), variance-stabilising transforms, wavelet denoising and peak deconvolution with mass-calibration alignment (dynamic time warping across spectra) before any learning; most published gains in this field came from preprocessing, not architecture.
- CROSS-DOMAIN (compression / dictionary learning): learn a sparse dictionary of peak motifs (K-SVD / NMF) across all species, then classify in the sparse-code space; this shares statistical strength across species-drug pairs with very few positives.
- CROSS-DOMAIN (statistical physics / spin-glass style modelling): model peak co-occurrence as an interaction network and use its low-temperature modes as features, which captures correlated proteome runs rather than individual peaks.
- Domain adaptation across hospitals: optimal-transport or CORAL-style alignment of spectra distributions between DRIAMS sites, plus per-site calibration, aimed directly at the site-transfer regime the original paper found hardest.
- Label-efficiency: with few resistant isolates for some drugs, use multi-task learning across drugs of the same class, positive-unlabelled learning, and conformal prediction to get honest uncertainty; report precision-recall, not just AUROC.
- CROSS-DOMAIN (ecology): treat the peak list as a community-composition sample (relative abundances) and import diversity/ordination statistics (Aitchison geometry, CLR transforms) designed for compositional data, which spectra effectively are.

## Pitfalls

- Batch and site confounding: acquisition batch, hospital and even plate position correlate with resistance prevalence, so a model can score well by learning the batch. Any claim needs batch-aware splits and the permutation/metadata-only controls, otherwise it is a false positive.
- Replicate leakage: the same isolate or patient can contribute multiple spectra; random spectrum-level splits then put near-duplicates on both sides. Splits must be by isolate/patient identifier.
- Species leakage: species identification is itself derivable from the spectrum, and resistance prevalence differs sharply by species; models must be evaluated within a fixed species, as the published numbers are.
- AUROC on heavy imbalance: for rare resistance the AUROC can be high while precision is useless. The claim must include AUPRC and raw counts, and the comparator must be the published value for the same species-drug pair and split regime, not a different one.
- Version drift: DRIAMS has been re-released multiple times (Dryad version 12 of 2025-08-19); comparing a model trained on a newer release to numbers published on an older one is apples to oranges unless the exact version and subset are matched and stated.
- Dryad now serves file downloads behind a bot challenge; fetch DRIAMS from the Zenodo mirror and record which mirror and which version was used, because version numbering differs between the two hosts.

## Sources

- https://zenodo.org/api/records/5640517
- https://zenodo.org/records/5640517
- https://datadryad.org/dataset/doi:10.5061/dryad.bzkh1899q
- https://datadryad.org/api/v2/datasets/doi%3A10.5061%2Fdryad.bzkh1899q
- https://github.com/BorgwardtLab/maldi_amr
- Status source: https://zenodo.org/api/records/5640517

## Citations

- [Problem page](../../../../.raw/V3R1T4S/known-unknowns/disease-research/driams-maldi-amr-beat-published-auroc.md)
- [Bank entry](../../../../.raw/V3R1T4S/bank/targets.json) (id `driams-maldi-amr-beat-published-auroc`, commit `7dd4480`)

## Related Nodes

- [[V3R1T4S Disease research]]
- [[V3R1T4S]]
