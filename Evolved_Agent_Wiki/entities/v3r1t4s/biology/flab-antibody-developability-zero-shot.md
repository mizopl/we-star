---
id: v3r1t4s-flab-antibody-developability-zero-shot
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
# FLAb antibody developability: beat the released zero-shot scores on a therapeutic-property category

# Overview

> Bank id `flab-antibody-developability-zero-shot` · standard · tractability 3 · laptop-hours · disclosure **open**
> Bank says open as of 2026-10-15. Statuses go stale — re-check the primary source before any work.

## Statement

FLAb (Fitness Landscapes for Antibodies, Gray lab at Johns Hopkins; github.com/Graylab/FLAb, last pushed 2026-08-17) collects 241 public antibody datasets in seven therapeutic-property categories (binding 132 datasets, polyreactivity 33, aggregation 31, thermostability 25, pharmacokinetics 9, expression 7, immunogenicity 4), each a CSV of heavy (and usually light) chain sequences with a measured fitness value. The repository also ships the scoring scripts for about 40 zero-shot methods (AntiBERTy, IgLM, ESM-2 at five sizes, ProGen2 variants, ESM-IF, ProteinMPNN, AbMPNN, IgFold, PyRosetta, and simple biophysical descriptors) and the resulting per-dataset score files under score/, so the current bar for any dataset or category is recomputable from the repository without running a single model. Published analyses of this resource report that general protein language models correlate weakly and inconsistently with antibody developability properties, which is why fifteen datasets with non-standard columns are excluded from automated scoring. Antibody developability is the step where many therapeutic candidates fail.

## Success criterion

Scores for every antibody in every dataset of one FLAb property category, produced by a method that never reads the fitness column of any dataset in that category, whose per-dataset Spearman correlations (sign-corrected using each dataset's documented direction of favourable values, taken from the category README, not from the data) give a category mean STRICTLY HIGHER (direction: max) than the category mean of every method whose score files are present under score/ in the repository, recomputed by the skeptic from those files (repository re-fetched live immediately before claiming), by at least 0.05, with per-dataset values published and the same method applied to at least two categories.

## Partial wins

- {"id": "p1", "statement": "Thermostability (25 datasets): beat every released zero-shot method's category mean Spearman by at least 0.05 with a method that runs on a laptop CPU."}
- {"id": "p2", "statement": "A method that is positively correlated on at least 80% of the datasets in a category, where the released language-model scores change sign from dataset to dataset."}
- {"id": "p3", "statement": "A reproducible analysis of how much of any method's apparent skill comes from sequence length or germline distance alone, with a length-and-germline-matched control."}

## Verification

Skeptic clones the repository (data plus released score files), checks the submitted score file covers every antibody of every dataset in the category exactly once, computes Spearman per dataset with the documented direction, recomputes the same statistic for each released method from the score/ files, and audits the attacker's code for reads of the fitness column. Minutes to recompute, plus the attacker's inference cost.

## Angles

- Antibodies differ from general proteins mainly in the hypervariable loops; score only the loop residues against an antibody-specific background instead of scoring the whole chain.
- Cross-domain import (formulation chemistry): aggregation and polyreactivity are surface-property problems, so compute patch-level hydrophobicity and charge from a predicted structure and regress nothing, which is a mechanism rather than a correlation.
- Cross-domain import (credit scoring): with 241 small datasets and inconsistent signs, treat it as a many-small-studies meta-analysis and estimate a pooled effect with random effects, rather than reporting one aggregate number.
- Germline distance is a known confound and a known weak predictor; build it as an explicit baseline and require any model to beat it.
- Pair heavy and light chains properly: several released scores treat the two chains independently, which cannot capture interface effects that drive aggregation.

## Pitfalls

- Using the dataset's own fitness values to choose the sign or a per-dataset threshold is label peeking; the direction must come from the documented metadata.
- Fifteen datasets with non-standard fitness column names are excluded from automated scoring; silently including or excluding datasets changes the category mean and must match the released protocol.
- Many FLAb antibodies are clinical-stage molecules whose sequences appear in public databases and in antibody language model training sets; a memorised ranking is not prediction.
- Categories are heavily unbalanced (132 binding datasets against 4 immunogenicity); a single aggregate across categories hides where the method works.
- A correlation gain on retrospective developability data is not evidence that a designed antibody will be safe or effective, and must not be described that way.

## Sources

- https://github.com/Graylab/FLAb
- https://raw.githubusercontent.com/Graylab/FLAb/main/README.md
- https://raw.githubusercontent.com/Graylab/FLAb/main/data/README.md
- Status source: https://github.com/Graylab/FLAb

## Citations

- [Problem page](../../../../.raw/V3R1T4S/known-unknowns/biology/flab-antibody-developability-zero-shot.md)
- [Bank entry](../../../../.raw/V3R1T4S/bank/targets.json) (id `flab-antibody-developability-zero-shot`, commit `7dd4480`)

## Related Nodes

- [[V3R1T4S Biology]]
- [[V3R1T4S]]
