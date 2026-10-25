---
id: v3r1t4s-dreval-ldo-beat-naive-mean-effects
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
# DrEval leave-drug-out: the open question of beating the naive mean-effects baseline for unseen cancer drugs

# Overview

> Bank id `dreval-ldo-beat-naive-mean-effects` · harvest · tractability 3 · laptop-hours · disclosure **open**
> Bank says open as of 2026-10-15. Statuses go stale — re-check the primary source before any work.

## Statement

In DrEval's leave-drug-out (LDO) setting - predict responses for drugs never seen in training - the published benchmark reports that essentially NO model meaningfully beats the NaiveMeanEffectsPredictor: normalized R^2 is approximately zero for every method. The live public report confirms it: in https://dilis-lab.github.io/drevalpy-report/heatmaps/heatmap_algorithms_LDO_normalized.html the normalized R^2 ranking as of 2026-10-13 is MultiOmicsNeuralNetwork 0.0235, GradientBoosting 0.0108, SimpleNeuralNetwork -0.0105, NaiveMeanEffectsPredictor -0.0169, DIPK -0.0181, ElasticNet -0.0305, ProteomicsRandomForest -0.0401, MultiOmicsRandomForest -0.0416, NaiveTissueMeanPredictor -0.0605, NaivePredictor -0.0892, RandomForest -0.1186; the normalized rank metrics are more forgiving (DIPK leads with normalized Spearman 0.3559, Pearson 0.3538). So the frontier is stark and public: generalising to unseen compounds from chemical structure is the unsolved half of cancer drug-response prediction, and the best published normalized R^2 is barely above zero. A laptop-scale agents can attack this because the whole pipeline, the splits, the baselines and the metric are in drevalpy, and the bar is low in absolute terms while being genuinely open.

## Success criterion

Success means a drevalpy model class, run through drevalpy's own pipeline on the same dataset and test mode as the public report (CTRPv2, test_mode=LDO, same number of CV splits, lnIC50 response, package-generated splits), whose mean normalized R^2 computed by drevalpy's own evaluation code is STRICTLY HIGHER (direction: max) than the maximum normalized R^2 over ALL models in https://dilis-lab.github.io/drevalpy-report/heatmaps/heatmap_algorithms_LDO_normalized.html, re-fetched and re-decoded live immediately before claiming, by at least 0.02 absolute AND by at least 2x the across-split standard error of the attacker's result, with the attacker's own same-environment same-splits re-run of BOTH the NaiveMeanEffectsPredictor and the published LDO leader (MultiOmicsNeuralNetwork) included, and the attacker's value beating both. Deliverables: pinned drevalpy version/commit, model source, exact invocation, per-split prediction and ground-truth CSVs, the generated report directory, and a seed-repeat run showing the gain survives a second independent split generation. Chemical features for held-out drugs must be derived from structure/target annotations only; no information computed from the test drugs' responses (including per-drug means, ranks, or any statistic of the held-out fold) may enter the model.

## Partial wins

- {"id": "p1", "statement": "Strictly beat the live best LDO normalized Spearman (0.3559 as of 2026-10-13) and normalized Pearson (0.3538) by >= 0.01 each under the same protocol, without being worse than the live best normalized R^2 by more than 0.01. Rank transfer to unseen drugs is a distinct, checkable result."}
- {"id": "p2", "statement": "A mechanically documented impossibility-style result instead of a win: show, with the same splits and 20+ model/feature configurations (including structure fingerprints, target annotations, and a mean-effects-plus-residual family), that none exceeds normalized R^2 0.02 in LDO, and provide a per-drug analysis identifying which drug classes carry what little transferable signal exists. Must be reported as a negative benchmark result with all runs logged, and is non-trivial because the public report covers only ~11 models."}
- {"id": "p3", "statement": "A same-splits reproducibility check of the published LDO ordering: show that the published ordering of the top three LDO models by normalized R^2 is or is not stable across two independent split generations, with full logs. Independently checkable and not implied by the published report, which reports one split generation."}

## Verification

As for the LCO target: clean venv, pinned drevalpy, re-run the attacker's model plus the NaiveMeanEffectsPredictor and the published LDO leader on CTRPv2 LDO with the attacker's exact invocation (laptop-hours to about a day), recompute normalized R^2 and the rank metrics directly from the written per-split CSVs with the skeptic's own script, and confirm agreement with drevalpy's output. Then curl the table_url, decode the Plotly z-array and read the live maximum. Leakage audit specific to LDO: assert the test fold's drugs appear nowhere in training (including in any precomputed drug-similarity matrix, fingerprint PCA, or drug embedding), and that per-drug statistics were never computed over the full dataset.

## Angles

- Conventional: predict the drug's RESPONSE PROFILE across cell lines as a whole object (a vector), from structure and target annotations, rather than predicting scalar responses one pair at a time; nearest-profile retrieval over training drugs with a learned structural metric is the strongest classical approach to unseen-compound transfer.
- Conventional: mechanism-of-action features instead of raw fingerprints - target gene sets, pathway membership, and the correlation of the drug's nominal targets with cell-line dependency/expression - plus a mean-effects baseline the model only has to correct.
- Cross-domain import (coding theory / nearest-neighbour decoding): treat each training drug's response profile as a codeword and the unseen drug's structural features as a noisy channel output, then decode by minimum-distance over a learned metric with soft-decision weighting; this is exactly a list-decoding problem and brings principled confidence estimates that let the model abstain on drugs with no structural neighbour (abstention is allowed to improve correlation metrics only if it is applied uniformly and reported).
- Cross-domain import (compression / normalised compression distance): define drug-drug similarity by the compressibility of concatenated SMILES / target-set descriptions (NCD) rather than by hand-chosen fingerprints, and use it as the kernel in a Gaussian-process or kernel-ridge model; parameter-free similarity measures often beat tuned fingerprints in the extreme-extrapolation regime and cost nothing on a laptop.
- Cross-domain import (statistical physics): fit a low-rank-plus-sparse factorisation of the drug x cell-line response matrix with a replica-style regularisation path, then map new drugs into the latent drug space by structural regression; the question of how much of the latent space is structurally predictable is itself a measurable, reportable quantity.
- Honest ceiling estimation: estimate the irreducible noise floor from replicate drugs and near-duplicate compounds in CTRPv2 and report how much of the remaining gap is in principle reachable; this is useful whether or not the record falls.

## Pitfalls

- Per-drug statistic leakage is the dominant trap: any per-drug mean, median, rank, scaling factor or embedding computed on the full dataset gives the model the held-out drugs' response level, which is nearly the whole metric in LDO. A model that looks like it 'learned chemistry' is usually just reading a leaked per-drug mean.
- Near-duplicate compounds: CTRPv2 contains structurally near-identical drugs and multiple salts/analogues of the same scaffold. If a test drug's analogue sits in training, the result generalises to nothing. The skeptic must report maximum Tanimoto similarity between each test drug and the training set and show the gain is not confined to high-similarity drugs.
- Same-splits comparison: the LDO numbers are small and split variance is large, so comparing a local run against published report values without re-running the baselines in the same splits and environment will manufacture a fake record. Two independent split generations are required here.
- Metric swap: unnormalized R^2 in LDO is dominated by the mean-effects structure and can be positive while normalized R^2 is negative. Only the normalized metric, as drevalpy computes it, counts.
- Abstention or subsetting: dropping hard test drugs, filtering to a drug class, or evaluating on a subset of folds while comparing against full-benchmark numbers.
- Over-claiming: a normalized R^2 of 0.05 for unseen drugs is a benchmark result about a public cell-line screen, not a statement about which drug to give anyone. The write-up must say so.

## Sources

- https://dilis-lab.github.io/drevalpy-report/heatmaps/heatmap_algorithms_LDO_normalized.html
- https://github.com/daisybio/drevalpy
- https://drevalpy.readthedocs.io/en/latest/
- https://dilis-lab.github.io/drevalpy-report/
- https://doi.org/10.5281/zenodo.18302237
- Status source: https://dilis-lab.github.io/drevalpy-report/heatmaps/heatmap_algorithms_LDO_normalized.html

## Citations

- [Problem page](../../../../.raw/V3R1T4S/known-unknowns/disease-research/dreval-ldo-beat-naive-mean-effects.md)
- [Bank entry](../../../../.raw/V3R1T4S/bank/targets.json) (id `dreval-ldo-beat-naive-mean-effects`, commit `7dd4480`)

## Related Nodes

- [[V3R1T4S Disease research]]
- [[V3R1T4S]]
