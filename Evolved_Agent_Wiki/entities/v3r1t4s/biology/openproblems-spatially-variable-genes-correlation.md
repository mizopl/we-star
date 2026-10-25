---
id: v3r1t4s-openproblems-spatially-variable-genes-correlation
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
tractability: 3
compute: "laptop-hours"
disclosure: open
status_checked: "2026-10-15"
---
# Open Problems spatially variable genes: beat the best ranking correlation on the hardest simulated spatial datasets

# Overview

> Bank id `openproblems-spatially-variable-genes-correlation` · harvest · tractability 3 · laptop-hours · disclosure **open**
> Bank says open as of 2026-10-15. Statuses go stale — re-check the primary source before any work.

## Statement

The Open Problems spatially-variable-genes task (Zhijian Li, Zain M. Patel, Dongyuan Song and contributors, built on the SVG benchmarking work of the Pinello lab, bioRxiv 2023.12.02.569717) simulates spatial transcriptomics data with scDesign3 so that the true spatial variability of every gene is known, then scores a method by the correlation between its gene ranking and the truth. In the public run run_2024-09-26_08-24-11 (score_uns.yaml on the openproblems-data S3 bucket, 50 datasets) most Visium datasets are near-saturated above 0.95, but several are not: slide-tags human skin melanoma tops out at 0.698 (SPARK-X; the next method, SpaGFT, reaches only 0.345), MERFISH human cortex 1 at 0.800 and cortex 2 at 0.798, Visium human heart at 0.777, Stereo-seq Drosophila embryo e10 at 0.769 and e7 at 0.775, slide-tags human cortex at 0.873 with a large gap to second place. Datasets, simulated matrices and solutions are plain HTTPS objects (tens of megabytes each), and the metric is a rank correlation the skeptic can recompute in seconds.

## Success criterion

For at least one dataset of the latest spatially-variable-genes run (live page https://openproblems.bio/benchmarks/spatially_variable_genes/ and the newest score file under resources/task_spatially_variable_genes/results/ on the openproblems-data S3 bucket, both re-fetched live immediately before claiming), a frozen method that reads only the simulated dataset file (never solution.h5ad) outputs a gene ranking whose correlation metric, recomputed by the skeptic with the official metric component of github.com/openproblems-bio/task_spatially_variable_genes, is STRICTLY HIGHER (direction: max) than every non-control method listed for that dataset by at least 0.02 absolute, with the same frozen method run on at least five datasets of different technologies and all results reported.

## Partial wins

- {"id": "p1", "statement": "Slide-tags human skin melanoma: beat the best listed value (0.698 for SPARK-X as of 2026-10-15) by at least 0.02 with a method that also stays within 0.02 of the best on the easy Visium datasets."}
- {"id": "p2", "statement": "A single frozen method that is within 0.02 of the best listed value on every one of the 50 datasets, which no listed method achieves (the leaders change by technology)."}
- {"id": "p3", "statement": "A checkable diagnosis of why the sparse, bead-based technologies (slide-tags, Stereo-seq, MERFISH) break the leading methods, for example spot-density inhomogeneity, demonstrated by a control experiment on the public simulated files."}

## Verification

Skeptic downloads simulated_dataset.h5ad and solution.h5ad for the claimed dataset from the public S3 bucket over plain HTTPS (12-50 MB each for the slide-tags and MERFISH sets), runs the attacker's frozen code in a directory where solution.h5ad is absent, scores with the official metric component, and compares with the newest score_uns.yaml and the live page. Minutes per dataset.

## Angles

- The truth comes from a Gaussian-process simulator mixed with a shuffled non-spatial model, so the task is a two-component hypothesis test; derive the exact likelihood ratio for that generative model instead of using a generic spatial statistic.
- Cross-domain import (geostatistics): variogram-based estimators handle irregular sampling better than grid-oriented statistics, which may be exactly what breaks methods on bead-based technologies.
- Cross-domain import (signal processing): treat each gene as a point process on an irregular sampling grid and use a Lomb-Scargle-style periodogram, standard for unevenly sampled astronomical time series, adapted to two dimensions.
- Rank correlation rewards getting the middle of the ranking right; calibrate per-gene statistics by expression level so that lowly expressed genes are not all pushed to one end.
- Ensemble the existing open-source detectors (SPARK-X, nnSVG, Moran's I, SpaGFT, Spanve) by rank fusion, with weights chosen per technology using only the simulated input, and check whether that alone beats every single method.

## Pitfalls

- Reading solution.h5ad, even to choose a hyperparameter or a technology-specific setting, is test-label peeking; the frozen method must decide everything from the input file.
- Controls such as true_ranking score 1.0 and must never be counted as a method to beat or as a baseline to tie.
- The simulated data come from one simulator; a method tuned to scDesign3's Gaussian-process assumption may win here and fail on real tissue, which the claim must state.
- One dataset in the run has a NaN entry for boostgp; treating missing values as zeros when computing 'the best listed method' produces a false bar.
- The run shown on the live page is from 2024; if a newer run appears, the newest score file is the bar, not the numbers quoted here.

## Sources

- https://openproblems.bio/benchmarks/spatially_variable_genes/
- https://github.com/openproblems-bio/task_spatially_variable_genes
- https://openproblems-data.s3.amazonaws.com/resources/task_spatially_variable_genes/results/run_2024-09-26_08-24-11/score_uns.yaml
- https://www.biorxiv.org/content/10.1101/2023.12.02.569717v1
- Status source: https://openproblems.bio/benchmarks/spatially_variable_genes/

## Citations

- [Problem page](../../../../.raw/V3R1T4S/known-unknowns/biology/openproblems-spatially-variable-genes-correlation.md)
- [Bank entry](../../../../.raw/V3R1T4S/bank/targets.json) (id `openproblems-spatially-variable-genes-correlation`, commit `7dd4480`)

## Related Nodes

- [[V3R1T4S Biology]]
- [[V3R1T4S]]
