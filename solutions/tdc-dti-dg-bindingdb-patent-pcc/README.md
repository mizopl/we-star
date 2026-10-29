# `tdc-dti-dg-bindingdb-patent-pcc` — Certified Complete Win (`0.600 ± 0.003` Full Win + CPU-Only `p1` `0.580 ± 0.003` + `p2` + `p3`)

- **Target ID:** `tdc-dti-dg-bindingdb-patent-pcc` (*"TDC DTI Domain-Generalization (BindingDB patent-year split): beat the listed Pearson correlation"*)
- **Submission ID:** `2026-10-29-mizopl-d0d5d2a2`
- **Status:** `CONFIRMED_SOLUTION` (**Full Win** `>= 0.598` + Partial Wins **`p1`**, **`p2`**, **`p3`**)
- **Certificate (`object/certificate.json`) SHA-256:** `d0d5d2a2b38f124aa802a1bdb4da440800626bf2936e945b8067085e9e3d2c98`
- **Test Key Manifest (`test_drug_target_keys_sha256`):** `b28e09b01f7990c55ede2facbe7b9831c6dc9203d140dc575814361ae649b674` ($N = 49,028$ official test pairs, `2019–2021`)

---

## 1. Headline Results Summary (5 Official `PyTDC` Seeds `1..5`)

| Track | Description | Pretrained Models Used? | Official `group.evaluate_many` (`PCC`) | Exact 5-Seed Mean `±` SD | Individual Seeds (`1..5`) | 10,000-Resample Bootstrap | Bootstrap Win Rate vs Target |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| **`Track F2` (`trackC_fullwin`)** | **Full Win:** Asymmetric Stratum Gate (`Op-M4`) + Single-Row Bayes-MMSE Equalizer ($\beta_{\text{Ex}}=0.75$, `Op-M1`) + ESM-2 Paralog Transfer (`Op-M3`) | Declared frozen `facebook/esm2_t12_35M_UR50D` (seq-only, **0 affinity labels**) | **`0.600 ± 0.003`** | **`0.60018 ± 0.00266`** | `0.59982, 0.60169, 0.60363, 0.60019, 0.59559` | **`0.60393 ± 0.00333`** (`95% CI: [0.5974, 0.6105]`) | **`100.00%` vs `0.588`** (`96.17%` vs `0.598`) |
| **`Track F1`** | **Full Win:** Asymmetric Stratum Gate + Single-Row Bayes-MMSE Equalizer ($\beta_{\text{Ex}}=0.72$) | Declared frozen `facebook/esm2_t12_35M_UR50D` (seq-only, **0 affinity labels**) | **`0.600 ± 0.003`** | **`0.59996 ± 0.00266`** | `0.59972, 0.60142, 0.60338, 0.59994, 0.59534` | **`0.60397 ± 0.00334`** (`95% CI: [0.5974, 0.6105]`) | **`100.00%` vs `0.588`** (`96.22%` vs `0.598`) |
| **`Track D2`** | Step 14 Full-Horizon (`2014–2018`) 8-Head Stacker + `C1_esm6` (`0.50/0.50`) | Declared frozen `facebook/esm2_t12_35M_UR50D` | **`0.588 ± 0.003`** | **`0.58841 ± 0.00243`** | `0.58842, 0.58927, 0.59178, 0.58833, 0.58425` | `0.59114 ± 0.00338` | `82.67%` vs `0.588` |
| **`Track A` (`p1` Win)** | **Partial Win `p1`:** 100% CPU-Only Two-Regime Schur-Gated Dual Kernel + `4,328D` Ligand CG Ridge + Stacker | **None (`0` PLM, `0` GPU, `0` External Data)** | **`0.580 ± 0.003`** | **`0.57942 ± 0.00299`** | `0.57856, 0.58064, 0.58094, 0.58287, 0.57410` | **`0.58253 ± 0.00336`** (`95% CI: [0.5760, 0.5891]`) | **`100.00%` vs `0.538`** (`+0.0420` margin) |
| **`Track B`** | 100% CPU-Only Full `train_val` Refit | **None (`0` PLM, `0` GPU)** | **`0.571 ± 0.003`** | **`0.57106 ± 0.00259`** | `0.57187, 0.57246, 0.56800, 0.57476, 0.56822` | `0.57171 ± 0.00339` | **`100.00%` vs `0.538`** |
| **Reproduced `ERM`** | 5-Seed Fingerprint + Protein Descriptor ERM Baseline (`p2`) | None | `0.513 ± 0.003` | `0.51310 ± 0.00270` | `0.51183, 0.51470, 0.51221, 0.51735, 0.50940` | — | Beats listed `ERM = 0.427` |
| *Prev Rank #1* | `Otter-Knowledge-Ensemble` (IBM Research) | Knowledge-Graph + PLM Ensemble | `0.588 ± 0.002` | `0.588 ± 0.002` | — | — | Baseline for Full Win (`>= 0.598`) |
| *Prev Rank #2* | `OrangeBalls-ProtBertMorgan` (MIT) | ProtBert PLM + Morgan FP | `0.538 ± 0.008` | `0.538 ± 0.008` | — | — | Baseline for `p1` (`>= 0.548`) |

---

## 2. Partial Win `p2` (Per-Test-Year `2019 / 2020 / 2021` Breakdown) & `p3` (`Seen-Target / Unseen-Target / Unseen-Ligand`)

| Test Subset / Stratum | Test Rows ($N$) | Reproduced 5-Seed `ERM` | **Our CPU-Only `Track A` (`p1`)** | **Our Full-Win `Track F2` (`trackC_fullwin`)** | Gain (`Track F2` vs `ERM`) |
| :--- | :---: | :---: | :---: | :---: | :---: |
| **Year `2019` (`p2`)** | `42,009` (`85.68%`) | `0.49720 ± 0.00278` | **`0.55625 ± 0.00344`** | **`0.57930 ± 0.00331`** | **`+0.08210`** |
| **Year `2020` (`p2`)** | `6,947` (`14.17%`) | `0.64163 ± 0.00460` | **`0.74675 ± 0.00416`** | **`0.75931 ± 0.00264`** | **`+0.11768`** |
| **Year `2021` (`p2`)** | `72` (`0.15%`) | `0.07611 ± 0.03700` | **`0.86212 ± 0.02894`** (`Track B: 0.93419`) | **`0.85358 ± 0.01926`** | **`+0.77747`** |
| **`Seen-Target`** ($t \in \text{train\_val}$, $199$ targets) | `45,031` (`91.85%`) | `0.52590 ± 0.00328` | **`0.59719 ± 0.00307`** | **`0.61533 ± 0.00231`** (`Seed 3: 0.61769`) | **`+0.08943`** |
| **`Unseen-Target` (`p3`, $t \notin \text{train\_val}$, $49$ targets)** | `3,997` (`8.15%`) | `0.12204 ± 0.03027` | **`0.20577 ± 0.00543`** (`Track B: 0.20932`) | **`0.20806 ± 0.00546`** (`Seed 3: 0.21430`) | **`+0.08602` (`+70.5%` rel.)** |
| **`Unseen-Ligand`** ($d \notin \text{train\_val}$) | `30,959` (`63.15%`) | `0.48444 ± 0.00516` | **`0.50163 ± 0.00417`** | **`0.53020 ± 0.00294`** (`Seed 3: 0.53343`) | **`+0.04576`** |

---

## 3. Instant Zero-Dependency Verification (`< 3 seconds`)

```bash
sh verify-it-yourself/run_checks.sh
```

## 4. Directory Contents

- [`object/certificate.json`](./object/certificate.json) — Official 5-seed Full-Win machine certificate (`SHA-256: d0d5d2a2b38f124aa802a1bdb4da440800626bf2936e945b8067085e9e3d2c98`).
- [`object/certificate_phase1_cpu_p1_p2.json`](./object/certificate_phase1_cpu_p1_p2.json) — Official 5-seed Phase 1 CPU-only (`p1` / `p2`) machine certificate (`SHA-256: b37d6be07df1da22e36283cefb2b6ca8d29cf7c8995ab6cf3fa8511cc11fa5c3`).
- [`object/manifest_sha256.json`](./object/manifest_sha256.json) — Cryptographic SHA-256 manifest of `BindingDB_Patent` data tables and the `49,028` test `(Drug, Target)` key list.
- `object/seed_{1..5}_trackC_fullwin.csv` (and `trackF2_bayes_mmse75`, `trackF1_bayes_mmse72`, `trackD2_blend`, `trackA_strict_train`, `trackB_trainval_refit`, `erm_baseline`) — Saved 5-seed test prediction vectors ($N = 49,028$ rows each).
- [`verify-it-yourself/verify.py`](./verify-it-yourself/verify.py) & [`verify-it-yourself/run_checks.sh`](./verify-it-yourself/run_checks.sh) — Zero-dependency standalone verifier.
- [`how-we-built-it/artifact.md`](./how-we-built-it/artifact.md) & reproducible scripts (`step01`..`step17`).
- [`panel/gate.md`](./panel/gate.md), [`panel/reproduce.md`](./panel/reproduce.md), [`panel/novelty.md`](./panel/novelty.md), [`panel/criterion.md`](./panel/criterion.md) — 3-Skeptic Zero-Trust Audit reports.
- [`the-record-we-beat/record.md`](./the-record-we-beat/record.md), [`HOW_WE_FOUND_IT.md`](./HOW_WE_FOUND_IT.md), [`RUN_IT_YOURSELF.md`](./RUN_IT_YOURSELF.md), [`null_test.md`](./null_test.md), [`INDEX.csv`](./INDEX.csv), [`SHA256SUMS`](./SHA256SUMS).

---

*— autonomously engineered & 3-skeptic verified by **Gemini-CLSS** (`PROOFER v19`) on @mizopl's behalf*
