---
id: v3r1t4s-climatebench-total-nrmse-cpu
type: entity
tags: [v3r1t4s, v3r1t4s/earth-and-sky, kind/harvest]
inbound_links: 1
confidence: 0.8
last_ingested_sources: [".raw/V3R1T4S/bank/targets.json@7dd4480"]
status: "open"
priority: ""
notes: ""
category: earth-and-sky
kind: harvest
tractability: 3
compute: "laptop-hours (training data a few GB; pattern-scaling and GP models train in minutes)"
disclosure: open
status_checked: "2026-10-15"
---
# ClimateBench: beat the best published total NRMSE for climate-model emulation on the SSP2-4.5 test scenario, on CPU

# Overview

> Bank id `climatebench-total-nrmse-cpu` · harvest · tractability 3 · laptop-hours (training data a few GB; pattern-scaling and GP models train in minutes) · disclosure **open**
> Bank says open as of 2026-10-15. Statuses go stale — re-check the primary source before any work.

## Statement

ClimateBench (Watson-Parris et al. 2022, JAMES) asks for emulators mapping emission scenarios to 2015-2100 NorESM2-LM fields of surface temperature (tas), diurnal temperature range (dtr), precipitation (pr) and 90th-percentile precipitation (pr90), scored by spatial, global and total NRMSE (total = spatial + 5 x global) against the 3-member ensemble mean of SSP2-4.5 over 2080-2100. The repository README lists only the 2022 baselines (best totals: tas 0.327, dtr 16.78, pr 3.17, pr90 4.34; CNN-LSTM). Lutjens et al. (arXiv:2408.05288, Table 1) collect all published scores. Best totals as of 2026-10-15: tas 0.284 and pr90 4.03 (linear pattern scaling, Lutjens et al.), dtr 10.7 (ClimaX, Nguyen et al. 2023), pr 3.10 (CNN-LSTM as reproduced by Nguyen et al. 2023). Open task: an emulator trainable on a laptop CPU whose total NRMSE beats the best published value for at least one variable.

## Success criterion

A saved, runnable emulator (code, fixed seeds, trained weights) trained only on the official ClimateBench training scenarios, evaluated with the official ClimateBench NRMSE script on the SSP2-4.5 test set (2080-2100), whose total NRMSE for a variable (tas, dtr, pr or pr90) is strictly lower than the best value for that variable in the README leaderboard at https://github.com/duncanwp/ClimateBench (re-fetched live immediately before claiming) AND lower than the best value for that variable reported in any peer-reviewed or arXiv ClimateBench paper (Lutjens et al. 2025 and ClimaX checked explicitly), with the same metric definition (total = spatial + 5 x global); no test-scenario data used in training or model selection; reproduction on CPU within 4 hours.

## Partial wins

- {"id": "p1", "statement": "Beat the best published total NRMSE for dtr (10.7, ClimaX) or pr (3.10) with a model of under 1M parameters trained on CPU in under 1 hour; these are the variables where linear pattern scaling loses."}
- {"id": "p2", "statement": "Beat the best published value on the spatial or the global component alone for any variable (Lutjens et al. Table 1 bars)."}
- {"id": "p3", "statement": "Match the best published total for tas (0.284) within 2% with a model that trains in under 10 CPU-minutes and uses no global-mean temperature input."}

## Verification

Skeptic downloads the ClimateBench data from Zenodo (a few GB), runs the provided training and evaluation scripts from a clean environment, and compares NRMSE to the README and the cited papers. Within 4 hours on CPU.

## Angles

- Conventional: pattern scaling with EOF-truncated emission inputs plus a GP correction for regional aerosol effects (the Lutjens et al. finding that linear models are hard to beat).
- Exploit ensemble-averaged training targets (Lutjens et al.) to reduce noise in training labels, while keeping the official test target.
- Cross-domain import (pharmacokinetics): impulse-response / convolution models of emissions to temperature (as in FaIR) give physically constrained global means; then downscale with patterns.
- Cross-domain import (econometrics): distributed-lag and error-correction models for the slow/fast response split.
- Cross-domain import (geostatistics): kriging residuals on the sphere with a Matern covariance for spatial NRMSE.

## Pitfalls

- The test target is a 3-member ensemble mean with sizeable internal variability (Lutjens et al.); gains smaller than the seed-to-seed spread are noise. Report 5 seeds.
- Using SSP2-4.5 (test) data for early stopping or hyperparameter choice is leakage.
- Some papers score against other targets (e.g. MPI-ESM 50-member means, Lutjens et al. Table 2) or other years; compare only like with like.
- Pattern-scaling variants that take simulated global-mean temperature as input use part of the target (Lutjens et al. note this about the original LPS); inputs must be emissions only.
- The README leaderboard is not the state of the art; check Lutjens et al. Table 1 and any newer ClimateBench paper.

## Sources

- https://github.com/duncanwp/ClimateBench
- https://doi.org/10.5281/zenodo.5196512
- https://arxiv.org/abs/2408.05288
- Status source: https://github.com/duncanwp/ClimateBench

## Citations

- [Problem page](../../../../.raw/V3R1T4S/known-unknowns/earth-and-sky/climatebench-total-nrmse-cpu.md)
- [Bank entry](../../../../.raw/V3R1T4S/bank/targets.json) (id `climatebench-total-nrmse-cpu`, commit `7dd4480`)

## Related Nodes

- [[V3R1T4S Earth and sky]]
- [[V3R1T4S]]
