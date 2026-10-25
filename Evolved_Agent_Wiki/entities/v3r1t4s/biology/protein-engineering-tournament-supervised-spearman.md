---
id: v3r1t4s-protein-engineering-tournament-supervised-spearman
type: entity
tags: [v3r1t4s, v3r1t4s/biology, kind/harvest]
inbound_links: 1
confidence: 0.8
last_ingested_sources: [".raw/V3R1T4S/bank/targets.json@7dd4480"]
status: "open"
priority: ""
notes: ""
category: biology
kind: harvest
tractability: 2.5
compute: "laptop-hours"
disclosure: open
status_checked: "2026-10-15"
---
# Protein Engineering Tournament pilot (supervised track): beat the best team Spearman on a released enzyme property

# Overview

> Bank id `protein-engineering-tournament-supervised-spearman` · harvest · tractability 2.5 · laptop-hours · disclosure **open**
> Bank says open as of 2026-10-15. Statuses go stale — re-check the primary source before any work.

## Statement

The pilot Protein Engineering Tournament (Chase Armer, Hassan Kane, Dana Cortade, Hanna Redestig, David Estell, Adil Yusuf, Nathan Rollins, Alex Spinner, Debora Marks, T. J. Brunette, Peter Kelly, Erika DeBenedictis; Proteins 2025, bioRxiv 2024.08.12.606135) released every dataset, every team submission and the scoring notebooks under CC BY at github.com/the-protein-engineering-tournament/pet-pilot-2023. In the supervised in-silico track, teams got train.csv and predicted held-out property values; the published board (doc/supervised-board.csv) shows average Spearman of 0.822 (nimbus) on alpha-amylase, 0.697 (exazyme) on imine reductase, 0.613 (tum-rostlab) on alkaline phosphatase PafA, and just 0.078 (exazyme) on beta-glucosidase B, where the other team scored -0.300. Test files with values are in the repository, so anyone can train on train.csv and score honestly. Two of the four events are barely above chance, which is where the headroom is. These are enzyme engineering targets of the kind used for biocatalysis and therapeutic protein optimisation.

## Success criterion

Predictions for every row of a supervised-track event's test file, from a model trained only on that event's train.csv (and publicly declared pretrained weights whose training data do not contain the event's measured values), whose average Spearman across the event's property columns, recomputed by the skeptic with the repository's evaluation.ipynb, is STRICTLY HIGHER (direction: max) than the best team value for that event in doc/supervised-board.csv (re-fetched live immediately before claiming) by at least 0.05, with the same frozen procedure run on all four supervised events and every result reported, and with a bootstrap 95% interval over test rows excluding the previous best.

## Partial wins

- {"id": "p1", "statement": "beta-glucosidase B: average Spearman above 0.30 (best team value 0.078 as of 2026-10-15) with the frozen procedure, on an event where both participating teams were near or below zero."}
- {"id": "p2", "statement": "One frozen procedure that beats the best team value on two of the four events at once, which no single team achieved."}
- {"id": "p3", "statement": "A per-property breakdown (the events score several measurements each) showing which property drives the average, plus a reproducible demonstration of whether small training sets or property noise set the ceiling."}

## Verification

Skeptic clones the repository (a few hundred megabytes), checks the prediction file covers each test row exactly once, runs the event's scoring cells from evaluation.ipynb, confirms from the training script that only train.csv was read, and compares with doc/supervised-board.csv. Minutes.

## Angles

- Training sets here are hundreds to thousands of variants of one protein, so a one-hot or substitution-matrix ridge regression is a strong baseline; establish it first and only then ask whether an embedding model beats it.
- Cross-domain import (chemometrics): several properties are measured per variant; partial least squares on the joint response borrows strength across correlated assays, which single-task models cannot.
- Cross-domain import (quantitative genetics): treat the measurements as a trait with additive effects plus epistasis and fit a kinship-style model on sequence similarity, which handles few examples and many positions.
- Zero-shot scores from a protein language model can serve as a prior for the regression rather than a competitor, which is where the supervised and zero-shot tracks meet.
- Beta-glucosidase B has the smallest training set; test explicitly whether the collapse there is sample size by subsampling the larger events to the same size.

## Pitfalls

- A 'test (with values).csv' file sits next to test.csv in the repository; reading it during training or model selection is test-label peeking and voids the claim.
- Some of the pilot's measurements appear in public enzyme databases and in protein language model training corpora; declare pretrained weights and check for the exact variants.
- The boards average Spearman across several property columns; quoting a single property's correlation against the board value is not the same quantity.
- Sample sizes are small (tens to hundreds of test rows), so Spearman is noisy; hence the 0.05 margin and bootstrap requirement.
- A better prediction on a pilot dataset is not a validated enzyme improvement, and the in-vitro track of the tournament showed how often computational picks fail expression and stability screens.

## Sources

- https://github.com/the-protein-engineering-tournament/pet-pilot-2023
- https://raw.githubusercontent.com/the-protein-engineering-tournament/pet-pilot-2023/main/doc/supervised-board.csv
- https://www.ebi.ac.uk/europepmc/webservices/rest/PMC12517241/fullTextXML
- https://www.biorxiv.org/content/10.1101/2024.08.12.606135v1
- Status source: https://raw.githubusercontent.com/the-protein-engineering-tournament/pet-pilot-2023/main/doc/supervised-board.csv

## Citations

- [Problem page](../../../../.raw/V3R1T4S/known-unknowns/biology/protein-engineering-tournament-supervised-spearman.md)
- [Bank entry](../../../../.raw/V3R1T4S/bank/targets.json) (id `protein-engineering-tournament-supervised-spearman`, commit `7dd4480`)

## Related Nodes

- [[V3R1T4S Biology]]
- [[V3R1T4S]]
