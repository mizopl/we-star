# Calibration (generated — overwritten by scripts/postdict.py report)

*Generated:* 2026-10-22T03:27Z · resolved 77 · open 3 · Brier 0.164 (0 = perfect, 0.25 = coin flip at p=0.5)

## By scope

| Scope | n | Brier | mean p | hit rate |
|---|---|---|---|---|
| algorithms | 1 | 0.303 | 0.45 | 1.00 |
| exp | 9 | 0.173 | 0.38 | 0.44 |
| lens | 29 | 0.237 | 0.66 | 0.69 |
| minimizer-density-record-tables | 2 | 0.006 | 0.93 | 1.00 |
| optimization-benchmarks | 3 | 0.174 | 0.65 | 1.00 |
| panel | 2 | 0.081 | 0.77 | 1.00 |
| target | 28 | 0.072 | 0.72 | 0.86 |
| tug | 3 | 0.388 | 0.45 | 1.00 |

## Calibration bins

| p bin | n | mean p | hit rate | verdict |
|---|---|---|---|---|
| 0.0–0.2 | 9 | 0.06 | 0.33 | underconfident |
| 0.2–0.4 | 6 | 0.29 | 0.33 | ok |
| 0.4–0.6 | 12 | 0.49 | 0.92 | underconfident |
| 0.6–0.8 | 12 | 0.67 | 0.67 | ok |
| 0.8–1.0 | 38 | 0.89 | 0.92 | ok |

## Open predictions

- `P0032` (target/bouchaudy-typex-1, p=0.35) Bouchaudy TypeX Problem 1 reaches CONFIRMED_SOLUTION (commit-only panel + gate + CHECK_RUN PASS) by 2026-10-25
- `P0077` (target/fmm-4x4x4-rank47-3x3x3-rank22, p=0.70) On fmm-4x4x4-rank47-3x3x3-rank22 (algorithms, Moonshot), we will achieve a verified milestone (p1: rank-48 scheme for <4,4,4> over Z or ZT, or p2: rank-47 scheme for <4,4,4> over Z/4Z) in Run 2026-10-21-2035
- `P0080` (tug/pherc1203-last-step, p=0.78) SEARCH winner: On the 8 coupled xz/yz + Lasagna v2 upper-Z sheets (z_HI_L2=1400..3300), Option C's dual-branch (L2 + L1-dipole/dual-energy M2/M3) ensemble achieves higher peak z_ens and >=15% lower reed-fiber false-positive variance than L2-only Option A. (by next_run)
