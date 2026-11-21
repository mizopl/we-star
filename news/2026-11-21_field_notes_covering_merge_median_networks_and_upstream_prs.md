# Field Notes #004 (`2026-11-21`) — `V3R1T4S #398` & `SorterHunter #17` Merged, `usnistgov/Circuits #2`, `Graylab/FLAb #15`, and `ZIB-IOL/polytof #2`

> **Date:** `2026-11-21` · **Authors:** `@mizopl` & **`we*`** (`PROOFER` Open-Science Lab)  
> **Repository:** [`mizopl/we-star`](https://github.com/mizopl/we-star) (`we* = me + agentic systems we* create + the feedback loop`)  
> **Format:** Short, factual status bulletin — where each merged or open package lives and what remains open (`-0 Hype / Limitations First`).

---

## 0. Limitations & Current Boundaries First

- **Open review queues:** Three upstream pull requests opened on `2026-11-18` (`usnistgov/Circuits#2`, `Graylab/FLAb#15`, `ZIB-IOL/polytof#2`) plus `elder-plinius/V3R1T4S#1161` are currently `OPEN` and awaiting maintainer review. (`bertdobbelaere/SorterHunter#17`, opened `2026-11-20`, was independently verified and merged by `@bertdobbelaere` on `2026-11-21`.)
- **Scope limits on each new submission:**
  - **`usnistgov/Circuits#2` / `V3R1T4S#1161` (NIST AES):** `0 / 6` live CSRC wish-list thresholds are solved (`InvS-box 33/4/111/14` stops `+1` gate above `<= 110@14`). Note also that upstream commit `e0615600` (`2026-11-20`) independently added an `InvMixColumns` `92@10` circuit to `usnistgov/Circuits` `main` after `PR #2` was filed.
  - **`bertdobbelaere/SorterHunter#17` (Median Selection Networks):** The four minimum-size reductions (`N = 28..31`, `-1` CE each) trade `+2` to `+3` extra layers against the existing lower-depth Pareto networks, `N = 23, 29, 31` are deterministic extensions of `N = 24, 28, 30`, and no global optimality is claimed.
  - **`Graylab/FLAb#15` (`clss_reg8_imgt_z`):** Positive zero-shot correlation holds on `score/tm` (`14/15`, `+0.4636`) and `score/polyreactivity` (`6/6`, `+0.4467`), while antigen-specific `score/binding` (`-0.0060`) and `data/binding` (`-0.0987`) are near zero or negative and are not claimed.
  - **`ZIB-IOL/polytof#2`:** Repairs `4` mismatched `data/paper/waring/` `.npy` files (`88/88 PASS` on upstream `verify_paper_schemes.py`); it does not claim global Waring-rank optimality.

---

## 1. What Landed & Where It Lives (`2026-11-18` -> `2026-11-21`)

| Item | Status | Upstream Link | Local Package in `we-star` | Summary |
| :--- | :---: | :--- | :--- | :--- |
| **La Jolla Covering `C(68,14,5) <= 15,675`** | **MERGED** (`2026-11-19`) | [`elder-plinius/V3R1T4S#398`](https://github.com/elder-plinius/V3R1T4S/pull/398) | [`README.md` Row #20](../README.md) | Independently verified over all `10,424,128` 5-subsets (`-326` blocks below live Covering Repository `16,001`). Brings merged `V3R1T4S` `main` PRs to **`9`** (`#366`, `#398`, `#433`, `#435`, `#517`, `#616`, `#617`, `#723`, `#724`). |
| **Median Selection Networks (`N = 23, 24, 28..31`)** | **MERGED** (`2026-11-21`) | [`bertdobbelaere/SorterHunter#17`](https://github.com/bertdobbelaere/SorterHunter/pull/17) | [`solutions/median-selection-networks/`](../solutions/median-selection-networks/) | Independently verified and merged by `@bertdobbelaere`: `8` JSON networks under `Networks/Median/`: `4` minimum-size reductions (`N = 28..31`: `103`, `106`, `117`, `120` at `+2/+3` D) and `4` fixed-depth `-2` CE improvements (`N = 23, 24, 28, 29`). Verified via `python3 verify.py` + `--corrupt`. |
| **NIST AES Straight-Line Circuits** | **OPEN PRs** (`2026-11-18`) | [`usnistgov/Circuits#2`](https://github.com/usnistgov/Circuits/pull/2) · [`V3R1T4S#1161`](https://github.com/elder-plinius/V3R1T4S/pull/1161) | [`solutions/nist-aes-circuit-records/`](../solutions/nist-aes-circuit-records/) | `11` canonical `%NCFF-0.1-2026` zero-`NOT` circuits (`InvS-box` `33/4/111/14`, `33/4/109/15`, `35/4/129/13`, `GD = 10` `152@10` & `155@10`, `S-box` `37/4/119/14`, `InvMixColumns` `92@10`) + `T1..T11` obstruction certificates. |
| **FLAb Zero-Shot Developability Baseline** | **OPEN PR** (`2026-11-18`) | [`Graylab/FLAb#15`](https://github.com/Graylab/FLAb/pull/15) | [`solutions/flab-antibody-developability-zero-shot/`](../solutions/flab-antibody-developability-zero-shot/) | Script-only `models/reg8_imgt_score.py` + `models/scoring_reg8_imgt.py` (`clss_reg8_imgt_z`), pure-Python ProtParam fallback (`< 4.6e-14` vs Biopython), deterministic `.gz` output. |
| **`polytof` Waring Tensor Repair** | **OPEN PR** (`2026-11-18`) | [`ZIB-IOL/polytof#2`](https://github.com/ZIB-IOL/polytof/pull/2) | [`solutions/polytof-toffoli-tcount-benchmark-tensors/`](../solutions/polytof-toffoli-tcount-benchmark-tensors/) | Replaces `4` inflated `data/paper/waring/` `.npy` matrices (`0105`, `0108`, `0115`, `0817`) to match `docs/tensors.md` (`88/88 PASS` on upstream `verify_paper_schemes.py`). |

---

## 2. Repository Hygiene & Obsidian Vault Snapshots

- **`@mizopl` vs. `we*` separation:** The personal profile [`mizopl/mizopl`](https://github.com/mizopl/mizopl) has been slimmed down to a brief personal card pointing directly to [`mizopl/we-star`](https://github.com/mizopl/we-star) as the shared `we*` catalog.
- **Refreshed Obsidian vault constellation:** The monochrome Obsidian knowledge-graph snapshot in [`we-star`](../README.md) has been refreshed to the current `4,982`-node vault, and individual Obsidian graph snapshots (`assets/we_star_constellation_{dark,light}.svg`) have been added across `18` of `19` solution folders in [`solutions/`](../solutions/) (`plmfit-trastuzumab-cdrh3-binding-mcc` left unchanged pending a full label-recomputation verifier upgrade).

---

← **[Back to `news/` Index](./README.md)** · **[Back to `mizopl/we-star` README](../README.md)**
