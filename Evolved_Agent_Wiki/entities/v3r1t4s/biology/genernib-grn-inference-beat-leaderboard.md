---
id: v3r1t4s-genernib-grn-inference-beat-leaderboard
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
# geneRNIB: beat the best listed gene-regulatory-network inference scores on a perturbation dataset

# Overview

> Bank id `genernib-grn-inference-beat-leaderboard` · standard · tractability 2.5 · laptop-hours · disclosure **open**
> Bank says open as of 2026-10-15. Statuses go stale — re-check the primary source before any work.

## Statement

geneRNIB (Open Problems gene regulatory network inference benchmark, bioRxiv 2025.02.25.640181) is a living benchmark in which a method outputs a weighted transcription-factor-to-target network from single-cell data, and the network is scored against held-out perturbation data and curated transcription-factor binding evidence. The public raw score table (all_scores.csv linked from the leaderboard page, 120 rows covering 11 datasets including Norman and Replogle CRISPR screens in K562, Xaira CRISPRi in HEK293T and HCT116, 300BCG, Nakatake and two multiome datasets) shows modest absolute values: on 300BCG the best listed gs_f1 is 0.570 (Geneformer) while a plain Pearson-correlation baseline reaches 0.469 and the negative control 0.034, and transcription-factor-binding F1 values sit near 0.11-0.13 for every method. Several metrics do not separate deep methods from correlation baselines at all. Inputs are public h5ad files on the openproblems-data S3 bucket and the evaluation runs from the repository without Docker for the baseline path.

## Success criterion

A network file in the benchmark's expected format for one dataset, produced by a method that reads only that dataset's public input files, whose scores recomputed by the skeptic with the task_grn_inference evaluation components are STRICTLY HIGHER (direction: max) than every non-control method listed for that dataset in all_scores.csv (re-fetched live immediately before claiming) on at least two of the dataset's applicable metrics, by at least 5% relative on each, and no worse than the best listed method on the others; the same frozen method must be run on at least three datasets and all scores reported.

## Partial wins

- {"id": "p1", "statement": "Beat every listed method's transcription-factor-binding F1 (tfb_f1, around 0.11-0.13 on 300BCG as of 2026-10-15) by at least 10% relative on one dataset without losing on the regression metrics."}
- {"id": "p2", "statement": "Show, with the published scores and your own reruns, that a correlation or regression baseline matches the deep methods on a metric where they are credited with an advantage, and publish the corrected comparison."}
- {"id": "p3", "statement": "A frozen method that beats the best listed method on the same metric in both a CRISPRi knockout dataset (Replogle or Xaira) and an observational dataset, showing it is not exploiting one perturbation design."}

## Verification

Skeptic downloads the dataset's inference inputs from the openproblems-data S3 bucket over plain HTTPS, runs the attacker's frozen inference script, then runs the repository's evaluation components (conda path, no Docker needed for evaluation), and compares with all_scores.csv downloaded from the leaderboard page. Hours at most for the smaller transcriptomics datasets.

## Angles

- The benchmark scores a network by how well it predicts held-out perturbation effects, so optimise that objective directly: fit a sparse linear response model from perturbation data and read the network off the coefficients, rather than inferring a network and hoping it transfers.
- Cross-domain import (causal inference in economics): CRISPRi knockouts are instrumental variables; estimate edges with two-stage least squares on the perturbation design instead of correlation.
- Cross-domain import (compressed sensing): with thousands of perturbations and far more candidate edges, use structured sparsity priors (group lasso over transcription-factor modules) with an explicit recovery guarantee argument.
- Use the multiome datasets' chromatin accessibility to restrict candidate edges to accessible motif matches before any statistics, which also makes the laptop version feasible.
- Check metric applicability first: the leaderboard marks which metrics pass quality criteria per dataset, and targeting a metric that is merely applicable but not quality-passing wastes effort.

## Pitfalls

- Using a curated network database (DoRothEA, ChEA, TRRUST, or the benchmark's own ground-truth resources) as an input feature contaminates the ground-truth metrics; only the dataset's own files may be read.
- The overall leaderboard score is a percentile aggregate across datasets and modalities, so a gain in one normalised rank can come from other methods' failures; the criterion therefore uses raw per-dataset metric values.
- Negative and positive controls appear in the score table and must be excluded when computing 'the best listed method'.
- Some metric columns are empty for some datasets; treating a blank as zero manufactures a false best value.
- A better network here is a better hypothesis generator, not a demonstrated regulatory mechanism in any patient or tissue.

## Sources

- https://genernib-documentation.readthedocs.io/en/latest/leaderboard.html
- https://github.com/openproblems-bio/task_grn_inference
- https://www.biorxiv.org/content/10.1101/2025.02.25.640181v1
- Status source: https://genernib-documentation.readthedocs.io/en/latest/leaderboard.html

## Citations

- [Problem page](../../../../.raw/V3R1T4S/known-unknowns/biology/genernib-grn-inference-beat-leaderboard.md)
- [Bank entry](../../../../.raw/V3R1T4S/bank/targets.json) (id `genernib-grn-inference-beat-leaderboard`, commit `7dd4480`)

## Related Nodes

- [[V3R1T4S Biology]]
- [[V3R1T4S]]
