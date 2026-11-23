# Degree-69 Binary Littlewood Flat Polynomials (`N = 70`): Pure-Scratch Match of Live `#1`, Three Islands Below `EA-2026`, and Homotopic Sphere-Cube `ISIC-RRR`

> **Illustrated 24-Page Research Dossier (PDF):** [`PROOFER_v19_FLAT_POLYNOMIALS_DOSSIER.pdf`](./PROOFER_v19_FLAT_POLYNOMIALS_DOSSIER.pdf)  
> **Cold Verifier (`~1.5 s` for all 4 certificates, `--corrupt` exits `1`):** [`verify.py`](./verify.py)  
> **Companion Rolling Dispatch:** [Field Notes #007 (`Ongoing Campaigns`)](../../news/2026-11-23_field_notes_ongoing_campaigns.md)

---

## Limitations First (`-0 Hype`)

1. **No strict beat below the live EinsteinArena `#1` (`1.259457173221`):** Across 7 waves (`525.3B` GPU memetic evaluations in Waves 4–6 plus `6.91B` SAW-free GPU `ISIC-RRR` FFTs in Waves 6–7), our pure-scratch champion [`certificates/best_flat_poly_deg69_scratch_v5.json`](./certificates/best_flat_poly_deg69_scratch_v5.json) **matches** the live `apollo-preview` `#1` (`1.259457173221`) to all 15 significant digits on the `1,000,000`-point EinsteinArena grid (rigorous continuous Taylor–Bernstein interval `[1.259457175649, 1.259457303746]`), discovered twice independently from 100% pure random noise. We did **not** find a polynomial strictly below `1.259457173221`.
2. **Empirical saturation, not a formal impossibility proof:** Cross-paradigm capture–recapture (`Chao1 = 8.25` for `C+ < 1.285`), exhaustive exact `2^{d_H}` recombination (`0 / 359.8M` states `< 1.292`), `20`-bit Gray-code LNS (`0` improvements), and `27 / 27` continuous `ISIC-RRR` melt-and-refreeze returns to `#1` are empirical evidence of near-saturation below `1.285`, **not** a formal proof over $2^{70}$.
3. **Wave 7 (`engine_v15`, `5.00B` unconstrained pure-`L_inf` `ISIC-RRR` FFTs on `Tesla T4`) was a clean miss (`1.295149`):** Unconstrained high-`E4` `ISIC-RRR` did not improve on `#1` or even Wave 6's `23.6 s` `1.280727` RAW hit.

---

## Cold-Verified Scorecard (`env -i python3 verify.py`)

Problem: minimize $C^+(g) = \sup_{|z|=1} |g(z)| / \sqrt{71}$ for $g(z) = \sum_{j=0}^{69} c_j z^j$, $c_j \in \{-1, +1\}$, strictly from **100% pure random noise** (zero seeding from AlphaEvolve V2, EinsteinArena, or literature codes):

| Rank / Baseline | Certificate (`certificates/`) | `C+_EA` (`10^6` grid) | Certified `sup/sqrt(71)` Interval | `E4` (`MF`) | `PSL` | vs `AE-2025` (`1.340925`) | vs `EA-2026` (`1.280932`) |
| :--- | :--- | :---: | :---: | :---: | :-: | :---: | :---: |
| *AlphaEvolve V2* | *`arXiv:2511.02864` (Nov 2025)* | *`1.340925279456`* | *`[1.34092528, 1.34092543]`* | *`519` (`4.72`)* | *`8`* | *baseline* | *`+0.05999`* |
| *`EA-2026` Repo* | *`ours_2026.py` (rediscovered `7x` from scratch)* | *`1.280932052799`* | *`[1.28093205, 1.28093220]`* | *`303` (`8.09`)* | *`5`* | *`-0.05999`* | *baseline* |
| **Our `#3` (SAW)** | [`island_w5_rank3_12807.json`](./certificates/island_w5_rank3_12807.json) | **`1.280727494964`** | **`[1.280727495, 1.280727609]`** | `399` (`6.14`) | `9` | `-0.06020` | **`-0.000204` BEAT** |
| **Our `#3` (SAW-free `ISIC-RRR`, `23.6 s`)** | [`island_v14_isic_raw_12807.json`](./certificates/island_v14_isic_raw_12807.json) | **`1.280727493819`** | **`[1.280727495, 1.280727609]`** | `399` (`6.14`) | `9` | `-0.06020` | **`-0.000204` BEAT** |
| **Our `#2` (Pure Scratch)** | [`island_w5_rank2_12734.json`](./certificates/island_w5_rank2_12734.json) | **`1.273402789390`** | **`[1.273402790, 1.273402925]`** | `439` (`5.58`) | `6` | `-0.06752` | **`-0.007529` BEAT** |
| **Our `#1` (Live `#1` 15-Digit Match)** | [`best_flat_poly_deg69_scratch_v5.json`](./certificates/best_flat_poly_deg69_scratch_v5.json) | **`1.259457173221`** | **`[1.259457176, 1.259457304]`** | `423` (`5.79`) | `6` | **`-0.08147` (`-6.08%`)** | **`-0.021475` (`-1.68%`) BEAT** |

---

## Quick Cold Verification (`< 2 s`, `numpy` only)

```bash
cd solutions/flat-polynomials-papr
env -i PATH=/usr/bin:/bin:/opt/homebrew/bin python3 verify.py
env -i PATH=/usr/bin:/bin:/opt/homebrew/bin python3 verify.py --corrupt   # exits 1
```

---

## Key Algorithmic & Structural Findings (Full Details in the [24-Page PDF Dossier](./PROOFER_v19_FLAT_POLYNOMIALS_DOSSIER.pdf))

1. **Exact Hyperbolic Roof Law:** $C^+(g) = \sqrt{(70 + 2\kappa\sqrt{E_4})/71}$. Minimizing $E_4$ alone fails: two global $N = 70$ LABS optima (`E4 = 295`, `MF = 8.3051`) have high peak norms (`C+ = 1.4242 / 1.4862`, `kappa = 2.15 / 2.53`). Low $C^+$ lives in the band `E4 ∈ [399, 439]` with a flat, negatively skewed spectral roof (`Skew = -0.6115` for `#1`).
2. **Unwiped $D_4$-Crowding + Multi-Objective Co-Evolution (Wave 4):** Replacing premature restarts (`stall = 120`) with unwiped warp-parallel $D_4$ deterministic crowding broke past `1.280932` at `t = 188 s` on a single `Tesla T4` (`< 0.8B` evals on the winning 32 warps), independently hitting live `#1` (`1.259457173221`) from pure random noise (reproduced a second time in Wave 5).
3. **SAW-Free Homotopic Sphere-Cube `ISIC-RRR` (Wave 6):** Replacing discrete `{-1,+1}^{70}` projection in Veit Elser's `RRR` with the inflating sphere-in-cube manifold $A(r) = \{x \in [-1, 1]^{70} : \|x\|_2^2 = r^2\}$ (`r^2: 58 -> 70`) eliminated Gaussian tapering and beat `EA-2026` in **`23.6 s`** (`436.8M` FFTs, zero 1-bit SAW, zero polish), independently rediscovering island `#3` (`1.28072749`).
4. **Exhaustive Skew Obstruction & 25+ Falsified Directions:** Packebusch–Mertens B&B (`300M` nodes) proved all optimal Skew-69/71/73 sequences suffer constructive $z = \pm i$ pileup ($C^+ \ge 1.40$), and `0 / 227,890` ultra-quiet outer shells extend to `E4 <= 375`.

---

<details>
<summary><b>How These Results Were Produced — Compute, Token &amp; Human–AI Collaboration Telemetry</b> (click to expand)</summary>

<br>

- **Session span:** `2026-11-22 20:46 UTC` to `2026-11-23 18:28 UTC` (**`21.70 h`** / `1302.3 min` wall-clock; initial preparation before Hypothesis #1: **`45.0 min`**).
- **Local 16 GB Apple M1 CPU vs. Google Colab:** **`57.4 min`** active local M1 compute union (`0.96` CPU core-hours) vs. **`295.4 min`** remote Google Colab offload.
- **Multi-agent token telemetry:** `1,204` trajectory steps across `2` discovery/audit threads totaling **`~1.39M` net unique transcript tokens** (`~40.1M` cumulative prefix-cached rolling window tokens).
- **Human-in-the-loop steering (`@mizopl`):** `25` short steering interventions (`~490` tokens total, **`1 : 2,838`** human-to-agent token leverage ratio).
- **Pre-registered ex-ante hypotheses & dead ends:** `7` hypotheses (`1` direct win, `5` structural asset / impossibility-certificate resolutions, `1` pure dead-end window; Brier calibration `0.182`).

</details>
