---
id: v3r1t4s-tdc-drugcomb-synergy-four-endpoints
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
tractability: 4
compute: "laptop-hours"
disclosure: open
status_checked: "2026-10-15"
---
# TDC DrugComb HSA/Loewe/Bliss/ZIP: lower the leaderboard MAE on a cancer drug-synergy endpoint

# Overview

> Bank id `tdc-drugcomb-synergy-four-endpoints` · harvest · tractability 4 · laptop-hours · disclosure **open**
> Bank says open as of 2026-10-15. Statuses go stale — re-check the primary source before any work.

## Statement

Besides the sensitivity endpoint, the TDC DrugCombo benchmark group scores four classical synergy endpoints on the same DrugComb cancer cell-line screens, each with its own leaderboard page: TDC.DrugComb_HSA (highest single agent), TDC.DrugComb_Loewe (Loewe additivity), TDC.DrugComb_Bliss (Bliss independence) and TDC.DrugComb_ZIP (zero interaction potency). As of 2026-10-15 each of the four leaderboards has exactly ONE entry, the same 7,141,297-parameter MLP: HSA 4.453 +/- 0.002, Loewe 9.184 +/- 0.001, Bliss 4.560 +/- 0.000, ZIP 4.027 +/- 0.003. All five DrugComb benchmarks (CSS plus the four synergy endpoints) share one split: the train_val and test tables have identical (Drug1_ID, Drug2_ID, Cell_Line_ID) triples, only the label column differs. Direct measurement on the downloaded benchmark files shows that the leaderboard entry reproduces a constant (train_val median) predictor to three decimals on all four endpoints (4.452 / 9.182 / 4.560 / 4.027) and is beaten everywhere by a per-cell-line median (4.438 / 9.118 / 4.518 / 3.946), so the public state of this benchmark is that no published model demonstrably learns drug-pair interaction at all. The open question is whether anything beats the per-cell-line median by a convincing margin.

## Success criterion

Success means, for at least ONE endpoint, a mean MAE from group.evaluate_many over the prescribed five seeds that is STRICTLY LOWER (direction: min) than ALL of: the live leaderboard best for that endpoint (re-fetched immediately before claiming), the constant train_val-median baseline, and the per-cell-line median baseline re-fitted by the attacker in the same run, by at least 0.15 MAE absolute for HSA/Bliss/ZIP and 0.30 for Loewe, and by at least 3x the claimed model's reported std. All three baselines' verbatim evaluate_many outputs must ship with the claim. The model may be trained only on that endpoint's train_val split and its seed-specific train/valid partitions; the test labels may be touched exactly once, by group.evaluate_many, at the end. Deliverables: pinned tdc version, data sha256 manifest, five per-seed prediction vectors per endpoint claimed, training script, verbatim evaluate_many output.

## Partial wins

- {"id": "p1", "statement": "Clear the bar on three or four endpoints with one method family, reported together with the explicit note that the four endpoints share a single split and are therefore not four independent results."}
- {"id": "p2", "statement": "Beat the per-cell-line median by >= 0.15 MAE on an endpoint using only features that depend on the drug pair (no cell-line-only features), demonstrating that the gain comes from drug-interaction signal rather than from cell-line main effects."}
- {"id": "p3", "statement": "Run the five-seed protocol twice with disjoint seed sets and report both means and stds, showing the gain exceeds between-seed-set variation."}

## Verification

Identical mechanics to the CSS target: clean venv with pinned tdc, re-download the benchmark and compare file sha256s, confirm prediction vector length and row order against benchmark['test'], re-run group.evaluate_many on the supplied five prediction dicts (minutes), re-fetch the endpoint's leaderboard page for the live best, then re-train from the attacker's script on fresh seeds (laptop-hours) to confirm the number is not a lucky seed. Leakage audit: assert that the set of (drug A, drug B, cell line) triples in each training split is disjoint from the test triples in BOTH drug orders, and that no scaler/encoder was fitted on test rows.

## Angles

- Conventional: train for the metric. Synergy scores are heavy-tailed and near-zero-centred, so an L1/Huber or median-quantile objective with gradient-boosted trees on fingerprints plus cell-line features should dominate an MSE-trained MLP on MAE.
- Conventional: multi-task learning across the four endpoints (they are deterministic functions of the same dose-response surfaces) with endpoint-specific heads, exploiting that Loewe/Bliss/ZIP/HSA share almost all of their signal; strictly respect per-endpoint test disjointness.
- Cross-domain import (compression / minimum description length): choose model complexity by MDL on the residual stream rather than by validation MAE, encoding the drug-pair x cell-line response matrix as a low-complexity code plus residual; MDL selection is far more robust than validation tuning when the target is mostly noise, which is the regime of Bliss/ZIP (MAE ~4 on a near-zero-centred score).
- Cross-domain import (combinatorial search / cryptanalysis-style meet-in-the-middle): search the space of feature-interaction subsets by hashing drug-target profiles into buckets and meeting in the middle on bucket pairs, rather than brute-force hyperparameter sweeps; this finds the few target-pair interactions that actually carry synergy signal within laptop budget.
- Cross-domain import (signal processing): model each endpoint as a linear functional of the two-drug dose-response surface and fit the surface (monotone 2-D spline / Hill-equation mixture) rather than the scalar score, then compute HSA/Loewe/Bliss/ZIP analytically from the fitted surface; this imposes the physical consistency constraints among the four endpoints that a scalar regressor cannot see.
- Robust loss and outlier handling: identify the heavy-tail rows (extreme Loewe values from poorly fitted curves), down-weight them with a robust (Tukey biweight) loss, and check whether the MAE gain comes mostly from the tail.

## Pitfalls

- All five DrugComb benchmarks share one split - the test triples are identical across CSS, HSA, Loewe, Bliss and ZIP (verified 2026-10-15), so multi-task training across endpoints does not leak, but winning on several endpoints is close to one result reported several times and must be described that way.
- A near-zero-centred target makes the median predictor extremely strong; the leaderboard entry IS effectively that predictor, so any criterion anchored to the leaderboard alone is vacuous. The per-cell-line median must be re-fitted and beaten in the same run.
- Test labels are local, so any tuning, early stopping or scaling statistic touching test rows invalidates the result; the evaluation call must be the single use of test labels.
- Near-zero-centred targets make a trivial constant/median predictor deceptively strong on MAE for Bliss and ZIP. A gain that disappears when compared against a per-cell-line median baseline is not a modelling result; the write-up must include that baseline.
- Protocol substitution: single-seed numbers, custom splits, subset evaluation, or the attacker's own MAE implementation instead of group.evaluate_many.
- Scale confusion between endpoints (Loewe MAE ~9 vs ZIP ~4) leading to comparison against the wrong leaderboard page; each endpoint has its own URL and its own bar.
- Reading any of this as evidence about combination therapy in patients. It is a benchmark on public cell-line screens and must be reported that way.

## Sources

- https://tdcommons.ai/benchmark/drugcombo_group/overview/
- https://tdcommons.ai/benchmark/drugcombo_group/drugcomb_hsa/
- https://tdcommons.ai/benchmark/drugcombo_group/drugcomb_loewe/
- https://tdcommons.ai/benchmark/drugcombo_group/drugcomb_bliss/
- https://tdcommons.ai/benchmark/drugcombo_group/drugcomb_zip/
- Status source: https://tdcommons.ai/benchmark/drugcombo_group/overview/

## Citations

- [Problem page](../../../../.raw/V3R1T4S/known-unknowns/disease-research/tdc-drugcomb-synergy-four-endpoints.md)
- [Bank entry](../../../../.raw/V3R1T4S/bank/targets.json) (id `tdc-drugcomb-synergy-four-endpoints`, commit `7dd4480`)

## Related Nodes

- [[V3R1T4S Disease research]]
- [[V3R1T4S]]
