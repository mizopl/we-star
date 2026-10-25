---
id: v3r1t4s-openproblems-spatial-decomposition-r2
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
tractability: 3.5
compute: "laptop-hours"
disclosure: open
status_checked: "2026-10-15"
---
# Open Problems spatial decomposition: beat the best listed R^2 for cell-type proportions on a benchmark dataset

# Overview

> Bank id `openproblems-spatial-decomposition-r2` · harvest · tractability 3.5 · laptop-hours · disclosure **open**
> Bank says open as of 2026-10-15. Statuses go stale — re-check the primary source before any work.

## Statement

The Open Problems spatial-decomposition task (authors Alma Andersson, Giovanni Palla, Vitalii Kleshchevnikov, Hirak Sarkar, Scott Gigante and contributors) asks a method to estimate, for each simulated spatial-transcriptomics spot, the proportion of each cell type, given an annotated single-cell reference. Spots are simulated from real single-cell atlases, so the true proportions are known and the metric is R^2 between predicted and true proportions. In the latest public run (run_2024-11-20_19-08-52; the task has not been re-run since 2024) the best R^2 per dataset is strikingly low on several datasets: tabula_sapiens 0.014 (vanilla NMF), immune_cell_atlas 0.070 (Stereoscope), openproblems_v1 immune_cells -0.106 (vanilla NMF; every method below zero), openproblems_v1 pancreas 0.077, zebrafish 0.195, cengen 0.248, mouse_pancreas_atlas 0.330, gtex_v9 0.401, hypomap 0.543 (cell2location), dkd 0.548 (cell2location). Because the spots are simple mixtures, a well-normalised regression against reference profiles should do far better on several of these; the gap suggests the hard datasets are hard for reasons (many fine cell types, reference/spot normalisation mismatch) that a careful method can address on a laptop.

## Success criterion

For at least one dataset in the latest spatial-decomposition run (live page and newest scores file on the openproblems-data S3 bucket, re-fetched live immediately before claiming), a frozen method that reads ONLY spatial_masked.h5ad and single_cell_ref.h5ad produces proportions whose R^2, recomputed by the skeptic with the official r2 metric component of github.com/openproblems-bio/task_spatial_decomposition against solution.h5ad, is STRICTLY HIGHER (direction: max) than every non-control method's r2 for that dataset by at least 0.05 absolute. The same frozen method must be run on every dataset the attacker reports, and all results reported, not only the wins.

## Partial wins

- {"id": "p1", "statement": "First positive R^2 on openproblems_v1/immune_cells (every listed method is below zero), with one frozen method."}
- {"id": "p2", "statement": "Beat the best listed r2 by >= 0.05 on three or more datasets simultaneously with a single frozen configuration."}
- {"id": "p3", "statement": "A diagnosis, checkable from the public files, of why the low-scoring datasets are hard (e.g. number of cell types, collinearity of reference profiles measured by condition number, or normalisation mismatch), with a control experiment showing the fix."}

## Verification

Skeptic downloads spatial_masked.h5ad, single_cell_ref.h5ad and solution.h5ad for the dataset from the public S3 bucket, runs the attacker's code in a directory where solution.h5ad is absent, then scores the output with the official r2 component. Compare with the newest scores.yaml and the live page. Minutes to an hour for the smaller datasets (cengen, zebrafish, pancreas, immune_cells: references 0.6-0.7 GB).

## Angles

- Baseline sanity first: non-negative least squares on carefully matched normalisation (raw counts vs. reference mean counts per type, with library-size as a free scalar per spot) frequently beats elaborate models on simulated mixtures; check that the listed NNLS run used the right scale.
- Cross-domain import (hyperspectral unmixing in remote sensing): spots are linear mixtures of 'endmember' spectra; use fully constrained least squares with sum-to-one and non-negativity, plus endmember variability models (multiple reference profiles per type).
- Cross-domain import (chemometrics): choose informative genes by the condition number of the reference signature matrix (as in CIBERSORT's signature design) instead of highly variable genes, which removes collinearity between fine cell types.
- Poisson / negative-binomial likelihood regression with per-gene platform effects (RCTD-style) but fitted on a laptop with L-BFGS rather than full Bayesian inference.
- Cross-domain import (compressed sensing): most spots contain few cell types; add sparsity (L1 or group-lasso) to the proportions, which helps exactly where many fine types are collinear.
- Learn the simulation: the spot simulator is public code, so train a small supervised model on spots you simulate yourself from the reference (never from the solution) and apply it to the masked spots.

## Pitfalls

- solution.h5ad is publicly downloadable next to the inputs; any method that reads it, or reads the simulated_dataset.h5ad that contains the true proportions, is leakage. The skeptic runs the method without those files present.
- Re-simulating spots with the public simulator using cells that were actually used to build the test spots can leak the answer through identical cells; simulate only from the provided single_cell_ref.
- R^2 can be dominated by a few abundant cell types; check the official metric's averaging (per spot vs. pooled) and use exactly that implementation.
- Cherry-picking the one dataset where a tuned method wins while hiding regressions elsewhere is not a result; all datasets the method was run on must be reported.
- The listed run dates from November 2024; a newer run may already contain better methods. Re-list the S3 results prefix before claiming.

## Sources

- https://openproblems.bio/benchmarks/spatial_decomposition/
- https://github.com/openproblems-bio/task_spatial_decomposition
- https://openproblems-data.s3.amazonaws.com/?list-type=2&prefix=resources/task_spatial_decomposition/
- Status source: https://openproblems.bio/benchmarks/spatial_decomposition/

## Citations

- [Problem page](../../../../.raw/V3R1T4S/known-unknowns/biology/openproblems-spatial-decomposition-r2.md)
- [Bank entry](../../../../.raw/V3R1T4S/bank/targets.json) (id `openproblems-spatial-decomposition-r2`, commit `7dd4480`)

## Related Nodes

- [[V3R1T4S Biology]]
- [[V3R1T4S]]
