---
id: v3r1t4s-ppi-bernett-gold-standard-auprc
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
tractability: 2.5
compute: "laptop-hours"
disclosure: open
status_checked: "2026-10-15"
---
# Leakage-free protein-protein interaction prediction: beat the best published AUPR on the Bernett gold-standard human dataset

# Overview

> Bank id `ppi-bernett-gold-standard-auprc` · standard · tractability 2.5 · laptop-hours · disclosure **open**
> Bank says open as of 2026-10-15. Statuses go stale — re-check the primary source before any work.

## Statement

Bernett, Blumenthal and List (Briefings in Bioinformatics 2024) showed that sequence-based PPI predictors that report 95-99% accuracy learn mostly sequence similarity and node degree, and that on a carefully de-leaked human split their performance falls to near random. They released a gold-standard dataset (figshare 21591618, version 4: Intra0/1/2 positive and negative pair files plus a SwissProt FASTA) with disjoint, similarity-minimised train/validation/test proteins and balanced degrees. On its test split, the methods Bernett et al. evaluated score AUROC 0.50-0.59 (Topsy-Turvy best). Hosseini, Golding and Ilie (C3PI, Briefings in Bioinformatics 2025) reached AUROC 0.703 / AUPRC 0.695, TUnA reports AUROC 0.700 / AUPRC 0.690, and Lu, Li, Tian, Nan et al. (DCAPPI, Computational and Structural Biotechnology Journal 2026, Table 5) report AUROC 0.702 / AUPRC 0.743. Everything sits around 0.70 AUROC, far from the 0.95+ seen on leaky benchmarks. Laptop-scale protein language model embeddings (ESM-2 8M-150M on CPU) are enough to compete.

## Success criterion

A score for every pair in the gold-standard test files (Intra2 positives and negatives, figshare 21591618 v4), produced by a model trained only on Intra1 (and validated on Intra0), whose AUPR recomputed by the skeptic with scikit-learn's average_precision_score is STRICTLY HIGHER (direction: max) than the best published AUPRC on this split (Table 5 of the DCAPPI paper at the Europe PMC full-text URL, re-fetched live immediately before claiming, plus any newer work found by the NOVELTY check) by at least 0.02, AND whose AUROC is strictly higher than the best published AUROC, with bootstrap 95% intervals over test pairs that exclude the published bests. No external PPI database (STRING, BioGRID, IntAct, HuRI) may be used.

## Partial wins

- {"id": "p1", "statement": "Beat the best published AUROC (0.703 as of 2026-10-13) by >= 0.02 with a CPU-trainable model, even if AUPRC does not clear its bar."}
- {"id": "p2", "statement": "A degree- and similarity-controlled ablation on the gold standard showing which part of the prediction comes from genuine pair-specific signal (e.g. permuting partners within degree bins), checkable from released code."}

## Verification

Skeptic downloads the gold-standard files through the figshare v2 API (https://api.figshare.com/v2/articles/21591618, which lists Intra0/1/2_pos_rr.txt, Intra0/1/2_neg_rr.txt and the SwissProt FASTA with direct ndownloader.figshare.com links; the figshare web page answers a plain GET with an empty 202), checks the score file covers each test pair exactly once, computes AUPR/AUROC with scikit-learn, bootstraps over pairs, and audits the code for any read of the test files during training and any external interaction database. Minutes.

## Angles

- Frozen small ESM-2 embeddings per protein, then a symmetric pair model (sum and elementwise product of embeddings) with strong regularisation; most of the gain may come from good per-protein features, not the pair architecture.
- Cross-domain import (recommender systems): factorisation machines / two-tower models trained with degree-debiased negative sampling, exactly the setting of cold-start users and items, which is what disjoint proteins are.
- Cross-domain import (structural biology): predicted interface propensity per residue (from a small structure-aware model or sequence-only interface predictors) aggregated into a pair score.
- Domain-domain interaction priors: map both proteins to Pfam domains and score pairs by domain co-occurrence statistics computed from the TRAINING split only.
- Co-evolution is unavailable for most human pairs, but paralog-based 'interolog' transfer within the training split can still carry signal; test it honestly under the gold-standard split.

## Pitfalls

- The whole point of the dataset is to remove leakage: any external PPI database, or a pretrained model fine-tuned on PPIs that include test proteins, re-introduces it. Pretrained protein language models trained on sequences alone are allowed; PPI-supervised checkpoints are not.
- Node-degree shortcuts: the dataset balances degrees, but a model can still exploit residual degree signal; report a degree-only baseline.
- Accuracy depends on a threshold; claim on AUPR (threshold-free) and report the others for context.
- The published record is assembled from papers rather than a live leaderboard, and DCAPPI's AUPRC exceeds its AUROC, which hints at different evaluation details; the skeptic must recompute on the official test files and the NOVELTY skeptic must search for newer results on this exact split.
- C3PI's own paper reports 0.977 AUROC / 0.878 AUPRC on a DIFFERENT dataset (its Table 3); quoting that as the gold-standard bar would make the target look saturated when it is not. Only values on the Bernett gold-standard split count.

## Sources

- https://www.ebi.ac.uk/europepmc/webservices/rest/PMC13505572/fullTextXML
- https://api.figshare.com/v2/articles/21591618
- https://github.com/daisybio/data-leakage-ppi-prediction
- https://www.ebi.ac.uk/europepmc/webservices/rest/PMC12713645/fullTextXML
- Status source: https://www.ebi.ac.uk/europepmc/webservices/rest/PMC13505572/fullTextXML

## Citations

- [Problem page](../../../../.raw/V3R1T4S/known-unknowns/biology/ppi-bernett-gold-standard-auprc.md)
- [Bank entry](../../../../.raw/V3R1T4S/bank/targets.json) (id `ppi-bernett-gold-standard-auprc`, commit `7dd4480`)

## Related Nodes

- [[V3R1T4S Biology]]
- [[V3R1T4S]]
