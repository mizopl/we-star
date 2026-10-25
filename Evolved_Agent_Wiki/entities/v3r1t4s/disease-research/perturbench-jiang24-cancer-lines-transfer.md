---
id: v3r1t4s-perturbench-jiang24-cancer-lines-transfer
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
compute: "laptop-days (jiang24_processed.h5ad.gz is 15.2 GB compressed; budget ~60 GB free disk and out-of-core or pseudobulk processing)"
disclosure: open
status_checked: "2026-10-15"
---
# PerturBench Jiang24: beat the published best cytokine-perturbation transfer metrics across cancer cell lines

# Overview

> Bank id `perturbench-jiang24-cancer-lines-transfer` · harvest · tractability 3 · laptop-days (jiang24_processed.h5ad.gz is 15.2 GB compressed; budget ~60 GB free disk and out-of-core or pseudobulk processing) · disclosure **open**
> Bank says open as of 2026-10-15. Statuses go stale — re-check the primary source before any work.

## Statement

The Jiang24 task in PerturBench is perturbation-response transfer across cancer cell lines and cytokine contexts. The live paper (arXiv 2408.10609v4, Table 4) describes 30 biological states (6 cell lines x 5 cytokine treatments) with 70% of the perturbations from 9 of those states held out for validation and testing; the barcode-level split is published as jiang24_split.csv in the ungated Hugging Face repo altoslabs/perturbench (1,628,475 cells: 1,216,452 train, 189,264 validation, 222,759 test), and the state labels must be read from the h5ad obs table. The published scoreboard is remarkably flat. Table 4 (main metrics): best cosine logFC 0.64 +/- 8e-4 (Decoder), best cosine-logFC rank 0.32 +/- 8e-3 (Decoder; lower is better, 0.5 is random), best MMD PCA 0.32 +/- 5e-3 (SAMS-VAE*), best DEG recall 0.005 +/- 6e-4 (CPA* (noAdv)). Table 11 (additional metrics): RMSE mean 0.015 for CPA*, CPA* (noAdv), LA and Decoder, 0.016-0.017 for the SAMS-VAE variants and 0.038 for Linear; RMSE-mean rank best 0.32 +/- 5e-3 (Decoder) with everything else 0.38-0.45; MMD best 3.1 +/- 2e-3 (Linear) with most models at 8.0. A rank metric of 0.32-0.45 against a random baseline of 0.5 means essentially nothing is being learned about WHICH perturbation produces WHICH profile.

## Success criterion

Success means a model trained with PerturBench's own Jiang24 accessor and the published jiang24_split.csv, scored by the repo's own Evaluator at a pinned commit, that strictly beats the best published value for at least ONE metric in Table 4 OR Table 11 of the latest arXiv version (re-fetched live immediately before claiming; cosine logFC and DEG recall higher is better, all other metrics lower is better) by at least 3x the published std of the previous best AND over 5 independent seeds reported as mean +/- std, while not being worse than the previous best on either other metric by more than 1 published std. For the rank metric the margin must additionally be at least 0.02 absolute, since a rank metric near 0.5 is uninformative and small moves are noise. Deliverables: pinned commit, dataset and split sha256s, the held-out state (cell line x cytokine) assignment derived by joining jiang24_split.csv to the h5ad obs table, logged with its sha256, training script and config, full Evaluator output over all metrics and seeds, and same-environment same-split re-runs of the published Decoder and LA baselines landing within 1 published std of Tables 4 and 11 (otherwise the comparison is void). No held-out perturbation's cells may touch training, normalisation, gene selection, early stopping or HPO.

## Partial wins

- {"id": "p1", "statement": "Push the RMSE-mean rank metric below 0.25 over 5 seeds (published best 0.32, random 0.5), i.e. demonstrate real perturbation discrimination on this dataset, with the per-perturbation rank list saved and recomputed by the repo's Evaluator."}
- {"id": "p2", "statement": "Beat the published best MMD (3.1, Linear) by >= 0.3 over 5 seeds while keeping RMSE mean no worse than 0.016, i.e. a distributional-fit improvement that does not come from collapsing to the mean."}
- {"id": "p3", "statement": "A cell-line-stratified breakdown: report the three metrics separately for each held-out (cell line x cytokine) state for the attacker's model and for the re-run Decoder baseline, identifying which combinations carry transferable signal. Mechanically checkable from the saved predictions and not reported in the published table."}

## Verification

Clean venv, perturbench at the pinned commit, download jiang24_processed.h5ad.gz and jiang24_split.csv from the ungated Hugging Face dataset and verify sha256s against the manifest, join jiang24_split.csv to the h5ad obs table and confirm the derived held-out perturbation lists per state match the logged ones and are disjoint from training, load the attacker's predicted anndata and recompute all metrics with the repo's Evaluator (under an hour), re-train 2 of 5 seeds (laptop-days at this data size), and re-run the Decoder and LA baselines in the same environment to confirm the published values. Leakage audit as for the other PerturBench targets, plus an explicit check that no cells from a held-out (cytokine, cell line) combination entered training for that combination.

## Angles

- Conventional: factorise the response as cell-line context x perturbation effect with explicit multiplicative interaction (a bilinear or tensor model), which is the natural model for a 6-cell-line x 5-cytokine design and is far cheaper than the published autoencoders.
- Conventional: train with a listwise ranking loss on perturbation identity (the rank metric is the discriminative part of the benchmark) instead of RMSE alone, and report both.
- Cross-domain import (cryptanalysis / distinguisher design): the rank metric is literally a distinguishing game - can you match a predicted profile to its true perturbation among all held-out perturbations? Build an explicit likelihood-ratio distinguisher over per-gene response statistics (the standard differential-cryptanalysis framing), which optimises exactly the quantity being measured rather than an L2 proxy.
- Cross-domain import (statistical physics / mean-field cavity method): estimate per-perturbation fields and cell-line-specific susceptibilities with a cavity/TAP approximation, giving a transferable linear-response human per cell line; linear-response theory is the right language for 'same perturbation, different context'.
- Cross-domain import (combinatorial design): the 30 states (9 with held-out perturbations) form an incomplete factorial design; use design-of-experiments theory (D-optimal weighting of training combinations, Latin-square-style balance) to decide how to weight and augment training data, instead of training on everything uniformly.
- Variance control: with published RMSE stds of 1e-5 to 2e-4, metric noise is tiny but model-seed noise is not; measure the attacker's own seed variance before chasing the 3x-std bar, and prefer ensembles that provably reduce it.

## Pitfalls

- A rank metric of 0.32 vs random 0.5 means the benchmark is barely above chance; small improvements are extremely likely to be noise or preprocessing artefacts. The 0.02 absolute floor plus 5 seeds exists for this reason.
- The published dataset description (30 states: 6 cell lines x 5 cytokines, 9 states held out) and the barcode-level split file carry different information: the split csv has no state column at all. The attacker must log the derived per-state held-out perturbation lists and the skeptic must verify them against the downloaded h5ad rather than against the paper text.
- Collapse-to-mean wins: RMSE mean of 0.015 is achievable by predicting almost nothing (the Linear model's 0.038 is the only visibly bad value), so an RMSE claim without the rank metric and MMD is meaningless. All three must be reported.
- Preprocessing leakage: normalisation, HVG selection or control-mean statistics computed across all cells including held-out perturbations; and cross-combination leakage where a perturbation held out in one (cytokine, cell line) combination is used in training for the same combination.
- Metric reimplementation: recomputing RMSE rank or MMD with the attacker's own code, different PCA dimensionality, or a different kernel bandwidth. Only the repo's Evaluator at a pinned commit counts.
- Stale-table comparison against an older arXiv version; the record must be re-read live from the latest version.

## Sources

- https://arxiv.org/abs/2408.10609
- https://github.com/altoslabs/perturbench
- https://huggingface.co/datasets/altoslabs/perturbench
- https://arxiv.org/html/2408.10609v4
- Status source: https://arxiv.org/abs/2408.10609

## Citations

- [Problem page](../../../../.raw/V3R1T4S/known-unknowns/disease-research/perturbench-jiang24-cancer-lines-transfer.md)
- [Bank entry](../../../../.raw/V3R1T4S/bank/targets.json) (id `perturbench-jiang24-cancer-lines-transfer`, commit `7dd4480`)

## Related Nodes

- [[V3R1T4S Disease research]]
- [[V3R1T4S]]
