---
id: v3r1t4s-code-test-ecg-abnormality-f1
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
# CODE-test 12-lead ECG: beat the published per-abnormality F1 on the 827-exam annotated test set

# Overview

> Bank id `code-test-ecg-abnormality-f1` · harvest · tractability 2.5 · laptop-hours · disclosure **open**
> Bank says open as of 2026-10-15. Statuses go stale — re-check the primary source before any work.

## Statement

Antonio H. Ribeiro and colleagues released CODE-test (Zenodo record 3765780, data.zip 218 MB, CC-licensed, no registration): 827 twelve-lead ECG tracings from the Brazilian CODE study, each annotated by consensus of cardiologists for six abnormalities (1st-degree AV block, right and left bundle branch block, sinus bradycardia, sinus tachycardia, atrial fibrillation). The companion paper (Nat Commun 11:1760, 2020) and the code at github.com/antonior92/automatic-ecg-diagnosis publish per-abnormality precision, recall, specificity and F1 for a residual network and for cardiology residents, medical students and emergency physicians on exactly this test set, with model weights public on Zenodo. Because the test labels, the tracings and the reference model are all public and the set is tiny, a stranger's laptop can rescore any new model in minutes - and the rare classes (AV block, atrial fibrillation; a few dozen positives each) are where the published F1 is weakest and where the honest uncertainty is largest.

## Success criterion

Success means a released model plus a saved per-exam, per-class score file for all 827 CODE-test exams (no exam dropped; sha256 of the score file published), trained only on data that excludes CODE-test (the public CODE-15% release or other public ECG corpora; the training exam identifiers must be released and checked disjoint from CODE-test), such that for at least one of the six abnormalities the F1 computed with the repository's own evaluation code is STRICTLY GREATER (direction: max) than the published value for the reference neural network on that abnormality, re-read live from the paper and from https://github.com/antonior92/automatic-ecg-diagnosis immediately before claiming, by a margin whose 95% bootstrap interval over exams excludes zero, while NO other abnormality's F1 falls by more than 0.01. Precision, recall, specificity and the confusion matrix must be reported per class; with only 827 exams, a claim without the interval over exams is not a result.

## Partial wins

- {"id": "p1", "statement": "Beat the reference network's published F1 on one of the rare classes (1st-degree AV block or atrial fibrillation) with the bootstrap interval excluding zero and no degradation elsewhere."}
- {"id": "p2", "statement": "Match the reference network's published F1 on all six classes to within 0.01 using a model with under 100k parameters that trains in under 2 hours on a CPU, with code and timings - an efficiency result for low-resource settings."}
- {"id": "p3", "statement": "A reproduction and uncertainty audit: recompute the published per-class metrics for the released reference weights on CODE-test, publish the bootstrap intervals the original report does not give, and document which published differences between the model and the human annotators are inside noise."}

## Verification

Skeptic downloads CODE-test from Zenodo (one 218 MB zip, plain HTTPS), hashes it, runs the attacker's released model to regenerate the score file (bit-for-bit or within a documented tolerance), recomputes per-class precision/recall/F1 with the repository's evaluation script, bootstraps over exams, re-runs the published reference weights as a control to confirm the published numbers reproduce on the skeptic's machine, and checks the released training-identifier list is disjoint from CODE-test. Minutes on CPU.

## Angles

- Label-efficiency over architecture: with a few dozen positives per rare class, class-balanced losses, focal loss and threshold selection on a held-out slice of the TRAINING data (never CODE-test) usually buy more F1 than a bigger network.
- CROSS-DOMAIN (signal processing): classical ECG engineering - baseline wander removal, QRS detection, beat alignment and template subtraction, RR-interval irregularity statistics - still beats raw deep learning for atrial fibrillation and bradycardia, and runs instantly on CPU.
- CROSS-DOMAIN (time-series / point processes): model the RR-interval sequence as a point process and test for the loss of regularity (sample entropy, Poincare dispersion, Markov-order tests) - atrial fibrillation is a rhythm problem, not a morphology problem.
- CROSS-DOMAIN (compression): normalised compression distance between a beat template and class-specific dictionaries gives a near-parameter-free classifier that is robust to amplitude scaling across recording devices.
- Calibration and decision policy: F1 depends on the operating point, so per-class threshold optimisation on training data, conformal prediction and reporting the full precision-recall curve is where honest gains live.
- Transfer from the public CODE-15% release (Zenodo 4916206) with careful de-duplication against the test exams, which is the only large public source of the same acquisition pipeline.

## Pitfalls

- Test-set reuse: the 827 exams are tiny and heavily reused in the literature; tuning thresholds, early stopping or model selection on CODE-test is the standard false positive here and must be shown absent in code.
- Patient overlap with CODE-15%: the same patients can appear in the public training release; exam and patient identifiers must be checked disjoint, or the result is memorisation.
- Multiplicity: six classes times many architectures means some class will look better by chance; the margin must survive a bootstrap over exams and the no-degradation rule for the other five classes.
- Metric mismatch: the published numbers use a specific threshold and averaging; comparing a tuned-threshold F1 to a default-threshold published F1, or a macro-average to a per-class value, is not a win.
- This is an annotated-benchmark gain, not evidence of clinical safety: the labels are consensus annotations on 10-second tracings from one country's screening programme.

## Sources

- https://zenodo.org/api/records/3765780
- https://zenodo.org/records/3765780
- https://github.com/antonior92/automatic-ecg-diagnosis
- https://www.nature.com/articles/s41467-020-15432-4
- https://zenodo.org/records/4916206
- Status source: https://zenodo.org/api/records/3765780

## Citations

- [Problem page](../../../../.raw/V3R1T4S/known-unknowns/disease-research/code-test-ecg-abnormality-f1.md)
- [Bank entry](../../../../.raw/V3R1T4S/bank/targets.json) (id `code-test-ecg-abnormality-f1`, commit `7dd4480`)

## Related Nodes

- [[V3R1T4S Disease research]]
- [[V3R1T4S]]
