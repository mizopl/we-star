---
id: result-fmm-9x12x14-zt
type: synthesis
tags: [v3r1t4s, result, CONFIRMED_SOLUTION, algorithms, fmm]
inbound_links: 2
confidence: 0.99
last_ingested_sources: ["~/v3r1t4s/runs/2026-10-18-1320/panel/gate.md", "~/v3r1t4s/outbox/2026-10-18-mizopl-a873a293/INDEX.csv"]
---
# FMM 9x12x14 ZT result

# Overview

**`9x12x14: r = 954 in ZT = {-1, 0, 1}`** (`9x12x14_m954_ZT.json`, `sha256 a873a293abc4e1b7c659250591e544062ad26ca556af28f29b25e63998355b02`, `915,296` bytes) is an explicit bilinear Fast Matrix Multiplication scheme over $\mathbb{Z}$ with ternary coefficients in $\{-1,0,1\}$ for format $\langle 9, 12, 14 \rangle$ of rank $954$, verified in exact `int64` arithmetic across all $108 \times 168 \times 126 = 2,286,144$ Brent equations (`mismatches = 0`). It strictly improves on the live Perminov status table `ZT rank = 960` (by $6$ multiplications) and `Z rank = 960` (by $6$ multiplications) while remaining above the rational best `Q rank = 940`.

- **Status:** `CONFIRMED_SOLUTION` (primary packaged claim from run `2026-10-18-1320` on `fmm-ternary-integer-ring-upgrade`). Three fresh-context Antigravity skeptics passed (`REPRODUCE`, `NOVELTY`, `CRITERION` in `runs/2026-10-18-1320/panel/`), the honesty gate passed, and `check_run.py` printed `CHECK_RUN: PASS`.
- **CLSS Method (*Sign-Pure Sub-Block Conjugation*):** Starting from Smirnov's rational $\langle 3, 3, 4 \rangle$ rank-29 scheme (`3x3x4_tensor.mpl`, indexed as $\langle 4, 3, 3 \rangle$), we decomposed $\langle 4, 3, 3 \rangle = \langle 2, 3, 3 \rangle_{\text{top}} \oplus \langle 2, 3, 3 \rangle_{\text{bot}}$ into $11$ top-only, $9$ bottom-only, and $9$ shared rank-1 terms. Exhaustive search over the signed permutation group $B_4$ ($384$ elements) discovered that conjugating the second $\langle 2, 3, 3 \rangle$ sub-block by $\pi = (0, 1, 3, 2)$ makes all $20$ unshared terms 100% sign-pure (`up=0, um=11, wp=9, wm=0`), saving $2$ multiplications per step inside $\mathbb{Z}_T = \{-1,0,1\}$ (`<4,3,3>` rank 29 + `<2,3,3>` rank 15 $\to$ `<6,3,3>` rank $42$ in `ZT`). Taking the Kronecker product with Perminov's `ZT` scheme `3x4x2_m23_ZT.json` ($\langle 3, 4, 2 \rangle$, rank $23$) and subtracting `<6,2,2>` rank $18$ via $\langle 9, 12, 14 \rangle = \langle 9, 12, 12 \rangle \oplus \langle 9, 12, 2 \rangle$ yields $966 - 18 + 6 = 954$ in `ZT`.
- **Additional Verified `ZT` World Records from the Same Run (`runs/2026-10-18-1320/code/`):**
  1. **`10x15x15` (`10x15x15_m1389_ZT.json`, `sha256 cf0bb61b...`):** rank **`1,389`** in `ZT` (strictly beating live `ZT = 1,395` by $6$, matching `Z = 1,389`, above `Q = 1,385`; `5,062,500` Brent equations verified).
  2. **`12x15x15` (`12x15x15_m1640_ZT.json`, `sha256 bbcc185d...`):** rank **`1,640`** in `ZT` (strictly beating live `ZT = 1,650` and `Z = 1,650` by $10$, above `Q = 1,600`; `7,290,000` Brent equations verified).
  3. **`14x15x15` (`14x15x15_m1894_ZT.json`, `sha256 114ddc45...`):** rank **`1,894`** in `ZT` (strictly beating live `ZT = 1,905` by $11$ and live `Z = 1,895` by $1$, above `Q = 1,848`; `9,922,500` Brent equations verified via **5-to-6 Ternary Seam Surgery**).
- **Outward:** Submitted on 2026-10-18 on the human's explicit `"Yes"` as **draft PR [elder-plinius/V3R1T4S#402](https://github.com/elder-plinius/V3R1T4S/pull/402)**, credit `mizopl` (package `2026-10-18-mizopl-a873a293`, branch `mizopl:claim/2026-10-18-mizopl-a873a293`, commit `c1e6f75`).

## Citations
- Gate and panel: `~/v3r1t4s/runs/2026-10-18-1320/panel/`
- Package: `~/v3r1t4s/outbox/2026-10-18-mizopl-a873a293/`
- Bank definition: [targets.json](../../.raw/V3R1T4S/bank/targets.json) (id `fmm-ternary-integer-ring-upgrade`)

## Related Nodes
- [[fmm-ternary-integer-ring-upgrade]]
- [[BRAIN]]
- [[V3R1T4S]]
