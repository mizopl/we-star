---
id: v3r1t4s-archiveii-interfamily-secondary-structure-f1
type: entity
tags: [v3r1t4s, v3r1t4s/biology, kind/standard]
inbound_links: 1
confidence: 0.8
last_ingested_sources: [".raw/V3R1T4S/bank/targets.json@7dd4480"]
status: "open"
priority: ""
notes: ""
category: biology
kind: standard
tractability: 3
compute: "laptop-hours"
disclosure: open
status_checked: "2026-10-15"
---
# RNA secondary structure across families: beat the best published family-fold F1 on ArchiveII, especially telomerase RNA

# Overview

> Bank id `archiveii-interfamily-secondary-structure-f1` · standard · tractability 3 · laptop-hours · disclosure **open**
> Bank says open as of 2026-10-15. Statuses go stale — re-check the primary source before any work.

## Statement

Marcell Szikszai, Michael Wise, Amitava Datta, Max Ward and David Mathews (Bioinformatics 2022) showed that deep-learning RNA secondary-structure predictors collapse when tested on RNA families absent from training, and released the family-fold cross-validation split of ArchiveII (3,865 sequences, nine families) with code at github.com/marcellszi/dl-rna. Under that split, thermodynamic RNAstructure averages F1 0.60 while retrained MXfold2 reaches 0.51 and UFold 0.44. The strongest later result is RiNALMo (Rafael Penic and co-authors, arXiv:2403.00043), which reports mean F1 0.71 on the same nine-family evaluation and beats RNAstructure on eight of nine families, but collapses on telomerase RNA at F1 0.12 against RNAstructure's 0.50; its 150M variant reaches 0.08 there and RNA-FM 0.07. A single frozen model that keeps RiNALMo's mean and fixes telomerase, or that raises the mean itself, is an open and laptop-checkable result; the data are a few megabytes and scoring is base-pair F1.

## Success criterion

Predicted secondary structures (dot-bracket or base-pair lists) for every sequence of the ArchiveII family-fold evaluation set, produced by models trained strictly under the family-fold protocol (for each test family, no sequence of that family anywhere in training, pretraining corpora declared and checked for that family), whose per-family F1 scores computed by the skeptic with the dl-rna repository's scoring code give a mean over the nine families STRICTLY HIGHER (direction: max) than the best published mean for this split (0.71, RiNALMo, arXiv:2403.00043 Table S3, re-fetched live immediately before claiming) by at least 0.02, with no family below the RNAstructure value for that family, and higher than any later published value found by the novelty check.

## Partial wins

- {"id": "p1", "statement": "Telomerase RNA alone: F1 above RNAstructure's 0.50 with a learned model, under the family-fold rule, with the same frozen model's scores on all nine families reported (every published deep model is at or below 0.12 there)."}
- {"id": "p2", "statement": "A model under 150M parameters whose nine-family mean beats RNAstructure's 0.60 by at least 0.05 under the family-fold rule, trainable on a laptop."}
- {"id": "p3", "statement": "A reproducible diagnosis of the telomerase collapse (for example sequence length, pseudoknots, or embedding overlap with SRP RNA as the RiNALMo authors note) with a controlled experiment that isolates the cause."}

## Verification

Skeptic takes the ArchiveII family-fold splits from github.com/marcellszi/dl-rna, checks the prediction file covers every sequence, computes per-family base-pair F1 with the repository's scoring code, and audits training logs and pretraining corpora for any sequence of the held-out family (including homologues above a stated identity threshold). Minutes to score; retraining is the attacker's cost.

## Angles

- Hybridise rather than replace: use the learned model only to reweight the thermodynamic model's base-pair probabilities, so the worst case degrades to RNAstructure instead of to 0.12.
- Cross-domain import (domain generalisation in vision): train with family labels as domains and an explicit invariance penalty, so the network cannot rely on family-specific sequence signatures.
- Cross-domain import (natural language parsing): secondary structure is a nested bracketing; use a parser with an explicit grammar and learned rule scores, which cannot output physically impossible structures.
- Telomerase RNAs are the longest sequences in the set, so test whether the collapse is a length-extrapolation failure by training on artificially lengthened sequences of other families.
- Calibrate on an entirely different held-out family than the test family when picking any hyperparameter, so the protocol stays honest and the result transfers.

## Pitfalls

- Pretraining corpora (Rfam, RNAcentral, bpRNA) contain the held-out families; using them without filtering breaks the family-fold design even though no labelled structure was seen.
- ArchiveII and RNAStralign overlap heavily; training on RNAStralign and testing on ArchiveII is not the family-fold protocol and gives much higher numbers.
- Different papers score with different base-pair F1 conventions (shifted pairs allowed, pseudoknots counted or not); use the dl-rna scoring code and say which convention is used.
- Reporting only the mean hides a telomerase-style collapse; the criterion requires every family to stay at or above the thermodynamic baseline.
- Better secondary-structure prediction is one input to RNA therapeutic design, not a validated design; claims must stop at the benchmark.

## Sources

- https://www.ebi.ac.uk/europepmc/webservices/rest/PMC9364374/fullTextXML
- https://github.com/marcellszi/dl-rna
- https://arxiv.org/html/2403.00043
- https://arxiv.org/abs/2403.00043
- Status source: https://arxiv.org/html/2403.00043

## Citations

- [Problem page](../../../../.raw/V3R1T4S/known-unknowns/biology/archiveii-interfamily-secondary-structure-f1.md)
- [Bank entry](../../../../.raw/V3R1T4S/bank/targets.json) (id `archiveii-interfamily-secondary-structure-f1`, commit `7dd4480`)

## Related Nodes

- [[V3R1T4S Biology]]
- [[V3R1T4S]]
