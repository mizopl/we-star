---
id: v3r1t4s-nih-thin-smear-malaria-patient-grouped-sensitivity
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
# NIH/NLM thin-smear malaria cells: beat the published sensitivity at matched specificity, and under a patient-grouped split

# Overview

> Bank id `nih-thin-smear-malaria-patient-grouped-sensitivity` · harvest · tractability 3 · laptop-hours · disclosure **open**
> Bank says open as of 2026-10-15. Statuses go stale — re-check the primary source before any work.

## Statement

Microscopy is still the reference test for malaria in most endemic settings, and the NIH/NLM thin-blood-smear cell dataset (data.lhncbc.nlm.nih.gov/public/Malaria/cell_images.zip, 353 MB, downloadable with a plain request) is the standard public benchmark: 27,558 segmented erythrocyte images, half parasitized, from patients at Chittagong Medical College Hospital, released by the Lister Hill National Center for Biomedical Communications. A 2026 study by Fatma Dehbi and Reda Mohamed Hamou in Frontiers in Medicine (PMC13553222) reports, on a fixed stratified 70:15:15 image-level split, a compact CNN with 95.26% accuracy at the default threshold and, after recall-weighted threshold optimisation, 97.05% sensitivity (95% CI 96.23-97.70) with ROC-AUC 0.9876, cutting missed parasitized cells from 177 to 61 - and states plainly that the split is image-level, not patient-level, because the public release has no patient identifiers. In fact the filenames encode patient codes (for example C33P1thinF...), so an honest patient-grouped evaluation is possible and, as far as this bank can establish, unreported: that is the open problem.

## Success criterion

Success means a released model plus saved per-image scores for the whole dataset under BOTH protocols, with the split files committed and hashed: (a) the published stratified image-level split regime, where the model's sensitivity at specificity no lower than the published specificity must be STRICTLY GREATER (direction: max) than the published sensitivity, re-read live from https://www.ebi.ac.uk/europepmc/webservices/rest/PMC13553222/fullTextXML immediately before claiming (97.05% as read 2026-10-15), by a margin whose 95% bootstrap interval over images excludes zero; and (b) a PATIENT-GROUPED split derived from the patient codes in the filenames (no patient's cells in both partitions; the derivation script released), where the same model's sensitivity, specificity and the drop relative to (a) are reported. A claim that reports only (a) is not a win; the honest contribution is the pair. Thresholds must be chosen on training/validation data only, and the claim is about this image benchmark, never about diagnosing any patient.

## Partial wins

- {"id": "p1", "statement": "Publish the patient-grouped split itself: a released, documented mapping from filenames to patient codes, the resulting grouped split, and the measured performance drop of a standard published architecture between image-level and patient-grouped evaluation, with intervals - a methodology result the field currently lacks."}
- {"id": "p2", "statement": "Match the published sensitivity at matched specificity with a model under 100k parameters running CPU-only inference at over 100 cells per second, with timings - the regime a field microscope station can actually run."}
- {"id": "p3", "statement": "A false-negative characterisation: cluster the parasitized cells missed by the published-style model, show at least one visually coherent failure mode (stain intensity, ring-stage size, focus), and exhibit a targeted fix that halves the misses in that cluster without raising the false-positive rate."}

## Verification

Skeptic downloads cell_images.zip over plain HTTPS, hashes it, rebuilds both split files from the claimant's released scripts and checks the patient-grouped split truly has no shared patient code, reruns the attacker's released inference to regenerate scores, recomputes sensitivity at the matched specificity operating point with bootstrap intervals over images and over patients, confirms the threshold was selected without the test partition (code review plus a rerun with the test partition scrambled), and re-reads the published metrics through Europe PMC. Under an hour on a CPU.

## Angles

- Operating-point engineering over architecture: the published work shows the ranking of models changes with the threshold objective, so calibrated probabilities plus an explicit cost-weighted decision rule is the cheapest honest gain.
- CROSS-DOMAIN (colour science / spectroscopy): Giemsa staining varies by site and batch; stain normalisation in an optical-density colour space (Macenko/Vahadane deconvolution, imported from histopathology) attacks the main nuisance variable before any learning.
- CROSS-DOMAIN (classical computer vision): ring-stage parasites are small chromatin dots - difference-of-Gaussians blob detection, morphological granulometry and Hu moments give interpretable features that a tiny classifier can use on a field laptop.
- CROSS-DOMAIN (metrology / measurement error): treat the per-cell call as an input to a parasitaemia estimate and propagate per-cell uncertainty to the slide level, which is what a microscopist actually reports.
- CROSS-DOMAIN (domain adaptation): patient codes let one build leave-one-patient-out evaluation and test domain-adversarial or style-transfer training that removes patient-specific staining signatures.
- Semi-supervised use of unlabelled cells from the same slides to regularise the small effective sample size once patients, not images, are the unit.

## Pitfalls

- Patient leakage: cells from one slide are near-duplicates, so image-level random splits inflate every metric; the patient-grouped protocol is the whole point of this target and the skeptic must verify the grouping.
- Threshold peeking: selecting the operating point on the test partition is how 97% sensitivities appear; threshold selection must be demonstrably confined to training/validation data.
- Metric substitution: with a balanced set, accuracy and ROC-AUC look excellent while the clinically relevant quantity (missed parasitized cells at acceptable specificity) barely moves; the claim must be sensitivity at matched specificity with counts.
- Single-site data: all slides come from one hospital and one staining protocol, so even a patient-grouped gain does not demonstrate transfer; no cross-site claim may be made from this dataset alone.
- Clinical overreach: this is cell-level image classification, not a diagnostic device; nothing here supports a diagnosis or a treatment decision for any person.

## Sources

- https://www.ebi.ac.uk/europepmc/webservices/rest/PMC13553222/fullTextXML
- https://data.lhncbc.nlm.nih.gov/public/Malaria/cell_images.zip
- https://lhncbc.nlm.nih.gov/LHC-research/LHC-projects/image-processing/malaria-datasheet.html
- https://bbbc.broadinstitute.org/BBBC041
- Status source: https://www.ebi.ac.uk/europepmc/webservices/rest/PMC13553222/fullTextXML

## Citations

- [Problem page](../../../../.raw/V3R1T4S/known-unknowns/disease-research/nih-thin-smear-malaria-patient-grouped-sensitivity.md)
- [Bank entry](../../../../.raw/V3R1T4S/bank/targets.json) (id `nih-thin-smear-malaria-patient-grouped-sensitivity`, commit `7dd4480`)

## Related Nodes

- [[V3R1T4S Disease research]]
- [[V3R1T4S]]
