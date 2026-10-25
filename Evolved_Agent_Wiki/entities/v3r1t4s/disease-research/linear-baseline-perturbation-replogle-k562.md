---
id: v3r1t4s-linear-baseline-perturbation-replogle-k562
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
# Unseen single-gene perturbations in leukaemia cells: beat the linear baseline that currently matches every foundation model

# Overview

> Bank id `linear-baseline-perturbation-replogle-k562` · harvest · tractability 3 · laptop-hours · disclosure **open**
> Bank says open as of 2026-10-15. Statuses go stale — re-check the primary source before any work.

## Statement

Constantin Ahlmann-Eltze, Wolfgang Huber and Simon Anders (Nature Methods, 2025, doi 10.1038/s41592-025-02772-6) asked whether single-cell foundation models can predict the transcriptional consequence of knocking down a gene that was never perturbed in training, and found that GEARS, scGPT, scFoundation, Geneformer, scBERT and UCE do not beat a deliberately simple linear baseline - a low-rank factorisation with one vector per read-out gene and one per perturbation - on the CRISPRi Perturb-seq datasets of Replogle et al. (K562 chronic myelogenous leukaemia and RPE1) and Adamson et al. (K562), measured as the L2 distance between predicted and observed expression over the 1,000 most highly expressed genes and as the Pearson delta, across five test-training splits. Every input is public and ungated: the Replogle K562 and RPE1 and Adamson datasets as distributed by GEARS on Harvard Dataverse, the analysis code at github.com/const-ae/linear_perturbation_prediction-Paper with the intermediate results archived on Zenodo, and the numeric values behind every figure in the Source Data files, which Europe PMC serves without registration. That makes this one of the few perturbation-prediction frontiers where the bar is a baseline anyone can re-run in minutes on a CPU, and where the honest open question - can anything actually beat it for unseen perturbations in a cancer cell line? - is still unanswered in public.

## Success criterion

Success means a model that, trained only on the training perturbations of each of the five published test-training splits of the Replogle K562 dataset as distributed by GEARS (sha256 logged), predicts the expression profile of each held-out perturbation, and whose median L2 distance over the 1,000 most highly expressed genes, computed with the repository's own scoring code at a pinned commit, is STRICTLY LOWER (direction: min) than BOTH (a) the attacker's same-environment, same-splits re-run of the paper's linear baseline and (b) the best value over all methods in the paper's published Source Data for that dataset and metric, re-fetched live immediately before claiming from https://www.ebi.ac.uk/europepmc/webservices/rest/PMC12328236/supplementaryFiles, by at least 5% of the linear baseline's own value and by at least 2x the across-split standard deviation. The same ordering must hold for the Pearson delta measure reported in the same Source Data. No held-out perturbation's measured cells may enter training, gene selection, normalisation, early stopping or hyperparameter choice, and any pretrained model used must have a declared pretraining corpus that does not include the held-out perturbations of these datasets. Deliverables: pinned commits, dataset sha256s, the split definitions, training and inference code, per-split prediction matrices, and the verbatim metric output for the attacker's model, the linear baseline and at least one published deep model re-run.

## Partial wins

- {"id": "p1", "statement": "The same strict improvement on the Replogle RPE1 dataset instead of (or in addition to) K562, under the identical protocol; a method that wins on only one of the two cell lines is a weaker but still reportable result and must be reported as such."}
- {"id": "p2", "statement": "Show that the gain, if any, is concentrated in perturbations whose target gene has close functional neighbours in the training set, by reporting the metric as a function of the distance between the held-out perturbation and its nearest training perturbation in an embedding declared before scoring. This quantifies what 'generalising to unseen perturbations' actually buys and is checkable from saved predictions."}
- {"id": "p3", "statement": "A reproduction of record: re-run the linear baseline and two published deep models on all five splits of both Replogle datasets and report agreement or disagreement with the published Source Data values, with full logs. Reported as a reproduction, not a record."}

## Verification

Skeptic downloads the GEARS-distributed Replogle K562 data from Harvard Dataverse (no registration), checks sha256 against the manifest, verifies the five split definitions and that held-out perturbations never appear in training, re-computes the L2 and Pearson delta metrics from the attacker's prediction matrices with the repository's own code at a pinned commit (minutes), then re-trains the attacker's model on at least two splits and re-runs the linear baseline in the same environment (laptop-hours). The live bar is read by fetching the Europe PMC supplementary files and reading the Source Data tables for the relevant figure. Leakage audit: confirm gene filtering and normalisation statistics were computed on training cells only, that no per-perturbation statistic was computed over the full dataset, and that any pretrained weights predate or exclude these datasets.

## Angles

- Conventional: strengthen rather than replace the baseline - add per-gene variance modelling, shrinkage toward the control profile, and a count-aware likelihood, and check how much of the deep models' claimed advantage disappears or reverses.
- Conventional: use prior biology that the linear model ignores - protein complex membership, pathway co-membership and co-essentiality correlations from public screens - as a structured prior over perturbation vectors, strictly without touching the held-out perturbations' measurements.
- Cross-domain import (statistical physics / linear response and cavity method): a knockdown is a field applied to a gene-regulatory network; estimate susceptibilities from the training perturbations with a TAP/cavity approximation, which predicts unseen fields rather than memorising seen ones.
- Cross-domain import (control theory / system identification): treat the training perturbations as input-output experiments on an unknown linear-plus-nonlinear system and identify the transfer operator with subspace identification methods, which come with identifiability diagnostics that tell you in advance which unseen perturbations are predictable.
- Cross-domain import (compression / MDL): choose the rank and sparsity by two-part code length instead of validation loss; the paper's result suggests the field is over-parameterising a problem whose information content is small, and MDL is the tool that measures exactly that.
- Cross-domain import (psychometrics / item response theory): perturbations are 'items' and genes are 'persons'; IRT-style models with discrimination and difficulty parameters handle extremely unbalanced response matrices and provide calibrated uncertainty for unseen items.
- Honest ceiling estimation: estimate the irreducible noise floor from biological and technical replicate perturbations in the Replogle data and report how much of the gap between the linear baseline and perfect prediction is even reachable.

## Pitfalls

- Pretraining contamination: any foundation model pretrained on corpora that include these Perturb-seq datasets has seen the held-out perturbations' effects. The pretraining corpus must be declared, and an undeclared one voids the claim.
- Metric substitution: the published comparison uses L2 over the 1,000 most highly expressed genes and the Pearson delta; switching to correlation over the top differentially expressed genes, or to all genes, changes the ranking entirely and is the single most common way papers in this area manufacture wins.
- Control-profile trivia: predicting the control (unperturbed) profile already scores respectably on several of these metrics, so any claim must include the control-only predictor as a baseline and beat it by a stated margin.
- Split and dataset drift: GEARS has distributed several versions of these datasets; a different version, gene filter or split seed makes the comparison incomparable. sha256s and split definitions must be logged.
- Near-duplicate perturbations: knocking down two members of the same complex produces near-identical profiles, so an apparent generalisation to an 'unseen' perturbation can be retrieval of its complex partner. Report the metric as a function of nearest-training-perturbation distance.
- Over-claiming: beating a linear baseline on CRISPRi in K562 is a statement about one leukaemia cell line measured one way, not about predicting a drug's effect in a patient's tumour.

## Sources

- https://www.ebi.ac.uk/europepmc/webservices/rest/PMC12328236/fullTextXML
- https://github.com/const-ae/linear_perturbation_prediction-Paper
- https://doi.org/10.5281/zenodo.14832393
- https://doi.org/10.1038/s41592-025-02772-6
- Status source: https://www.ebi.ac.uk/europepmc/webservices/rest/PMC12328236/fullTextXML

## Citations

- [Problem page](../../../../.raw/V3R1T4S/known-unknowns/disease-research/linear-baseline-perturbation-replogle-k562.md)
- [Bank entry](../../../../.raw/V3R1T4S/bank/targets.json) (id `linear-baseline-perturbation-replogle-k562`, commit `7dd4480`)

## Related Nodes

- [[V3R1T4S Disease research]]
- [[V3R1T4S]]
