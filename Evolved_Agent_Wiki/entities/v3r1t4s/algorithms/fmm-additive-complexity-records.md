---
id: v3r1t4s-fmm-additive-complexity-records
type: entity
tags: [v3r1t4s, v3r1t4s/algorithms, kind/harvest]
inbound_links: 1
confidence: 1.0
last_ingested_sources: [".raw/V3R1T4S/bank/targets.json@7dd4480", "runs/2026-10-22-0110/RESULT.md", "outbox/2026-10-22-mizopl-e47a7dd8/README.md"]
status: "CONFIRMED_SOLUTION"
priority: "high"
notes: "CONFIRMED_SOLUTION + p3 in Run 2026-10-22-0110 (Draft PR #616, 2026-10-22-mizopl-e47a7dd8, commit ae9e38f): 48 verified ZT SLPs over Z beating live addition_reduced_ZT min cr on 9 exact-SOTA formats (2x4x7 157 vs 168 [-11], 2x5x5 145 vs 147 [-2], 4x5x8 447 vs 466 [-19], 4x6x7 464 vs 468 [-4], 5x5x6 406 vs 411 [-5], 5x5x8 548 vs 555 [-7], 5x6x6 492 vs 499 [-7], 5x6x7 573 & 576 vs 577 [-4], 5x7x7 680 vs 694 [-14]), 2 ZT-best formats (4x4x8 338 vs 339, 3x3x6 152 vs 153), and 21 newly addition-reduced SOTA-rank ZT formats."
category: algorithms
kind: harvest
tractability: 3
compute: "laptop-hours"
disclosure: open
status_checked: "2026-10-22"
---
# Fast matrix multiplication: fewer additions for a fixed best-known rank (straight-line program records)

# Overview

> Bank id `fmm-additive-complexity-records` · harvest · tractability 3 · laptop-hours · disclosure **open**
> **Status (`2026-10-22`):** **`CONFIRMED_SOLUTION` + `p3`** in Run [`2026-10-22-0110`](file://~/v3r1t4s/runs/2026-10-22-0110/RESULT.md), packaged in [`outbox/2026-10-22-mizopl-e47a7dd8`](file://~/v3r1t4s/outbox/2026-10-22-mizopl-e47a7dd8/README.md) and opened as Draft PR [#616](https://github.com/elder-plinius/V3R1T4S/pull/616) (`commit ae9e38f`, `3/3` skeptics `pass: true`, `CHECK_RUN: PASS`, `K12` auditor `0 ERRORS`, `P0079` resolved `1` with Brier `0.090`).

## Certified Solution Summary (`2026-10-22-mizopl-e47a7dd8`, PR [#616](https://github.com/elder-plinius/V3R1T4S/pull/616))

Using **Matroid-Optimal Distance-1 Target Closure ($\text{Cl}_1$)**, **Tellegen Transposition on $W^T$** ($\text{cr}(W^T) = \text{cr}(W) + \text{nz\_rows}(W) - \text{nz\_cols}(W)$), **Exact Residual-Reduction Lookahead** ($r(t) = t - s^* b^*(t)$), and **Multi-Threaded Stepping-Stone LNS** (`clss_cl1_tellegen_reducer.cpp`, `sha256: c4dbcec6...`), we certified **48 explicit ternary (`ZT`) straight-line programs** over $\mathbb{Z}[A, B]$ (`CERTIFICATE.json`, `sha256: e47a7dd8...`, `verify.py`, `sha256: d0a55797...`):

1. **9 Distinct Exact-SOTA-Rank Formats with $\max(n, m, p) \le 8$ Strictly Beating Live `addition_reduced_ZT` Minimum `cr` (`CONFIRMED_SOLUTION` + `p3` $\ge 3$ by $3\times$):**
   - **`2x4x7` ($m = 45$):** `cr = 157` (`26, 58, 73`, `sha256: 13925cb4...`, **`-11`** vs live `168`) and `cr = 164` (`27, 64, 73`, `sha256: 2d85f22f...`, **`-4`** vs live `168`).
   - **`2x5x5` ($m = 40$):** `cr = 145` (`28, 58, 59`, `sha256: c7e30b3f...`, **`-2`** vs live `147`).
   - **`4x5x8` ($m = 118$):** `cr = 447` (`96, 141, 210`, `sha256: 6a20a2b0...`, **`-19`** vs live `466`).
   - **`4x6x7` ($m = 123$):** `cr = 464` (`112, 138, 214`, `sha256: 2b78b41c...`, **`-4`** vs live `468`).
   - **`5x5x6` ($m = 110$):** `cr = 406` (`105, 110, 191`, `sha256: 4cbc3596...`, **`-5`** vs live `411`).
   - **`5x5x8` ($m = 144$):** `cr = 548` (`130, 156, 262`, `sha256: 26e8fee0...`, **`-7`** vs live `555`).
   - **`5x6x6` ($m = 130$):** `cr = 492` (`128, 139, 225`, `sha256: b17cdb71...`, **`-7`** vs live `499`).
   - **`5x6x7` ($m = 150$):** `cr = 573` (`143, 165, 265`, `sha256: e7b7f15c...`, **`-4`** vs live `577`) and `cr = 576` (`144, 168, 264`, `sha256: e2e3d0b0...`, **`-1`** on the exact same `cn = 2039` tensor).
   - **`5x7x7` ($m = 176$):** `cr = 680` (`170, 197, 313`, `sha256: d8735ca9...`, **`-14`** vs live `694`).
2. **2 Additional $\mathbb{Z}_T$-Best Formats Strictly Beating Live `addition_reduced_ZT` Minimum `cr`:**
   - **`4x4x8` ($m = 96$):** `cr = 338` (`73, 101, 164`, `sha256: eae68290...`) vs live `339` (`cr_val = 340`, **`-1` / `-2`**).
   - **`3x3x6` ($m = 43$):** `cr = 152` (`32, 46, 74`, `sha256: 1753cc9f...`) vs live `153` (**`-1`**).
3. **21 Newly Addition-Reduced Exact-SOTA-Rank $\mathbb{Z}_T$ Formats (`6` also strictly below older higher-rank `cr`: `2x6x6_m56` `221 < 224`, `3x5x6_m68` `245 < 252`, `3x6x8_m108` `381 < 411`, `4x7x8_m161` `625 < 646`, `4x8x8_m180` `734 < 746`, `5x7x8_m204` `835 < 837`) + 14 Secondary Variant Improvements.**

## Statement

For a fixed FMM scheme rank, the number of additions/subtractions in the straight-line program (SLP) that evaluates the scheme is a secondary but citable record: <2,2,2>:7 needs 15 (proved optimal), <3,3,3>:23 was reduced to 58 additions (Perminov, arXiv:2512.21980, Dec 2025; cf. arXiv:2601.05272 claiming 59 total operations under its own convention), and Perminov's repository publishes addition-reduced ternary schemes for every format up to 16x16x16 (schemes/results/addition_reduced_ZT, reduced_known.json; tool ternary_addition_reducer) while the Lille catalogue cites 'best-known complexity' variants per format (e.g. 4x4x4:48 by Dumas-Pernet-Sedoglavic-Stapleton-Tichavsky 2026) and matmulcatalog publishes an 'adds' column (naive count nz(U)+nz(V)+nz(W)-2r-np) and warns its SLP counts are upper bounds from a greedy heuristic.

## Citations

- [Problem page](../../../../.raw/V3R1T4S/known-unknowns/algorithms/fmm-additive-complexity-records.md)
- [Bank entry](../../../../.raw/V3R1T4S/bank/targets.json) (id `fmm-additive-complexity-records`, commit `7dd4480`)
- [Verified Run `2026-10-22-0110`](file://~/v3r1t4s/runs/2026-10-22-0110/RESULT.md)
- [Draft PR #616 (`2026-10-22-mizopl-e47a7dd8`)](https://github.com/elder-plinius/V3R1T4S/pull/616)

## Related Nodes

- [[V3R1T4S Algorithms]]
- [[V3R1T4S]]
