# Exact Cyclotomic Galois Certificates & Zero-Axiom Lean 4 Proofs for [`unitaryfoundation/stabrank`](https://github.com/unitaryfoundation/stabrank)

> **Upstream Deliverables (`we* + @mizopl`):**
> - **[`unitaryfoundation/stabrank PR #193`](https://github.com/unitaryfoundation/stabrank/pull/193) (`fc1495d`):** **`35 / 35` bounds certified at `tier = verified`** (`26` upgrades from `cited` / `reproduced` / `attested` to exact arithmetic + `9` new cells) across **8 tracks** (`qubit_H`, `qubit_T`, `cat`, `CS`, `H3`, `N`, `S`, `T3`) via **5 self-contained $\mathbb{Z}[i]$ and $\mathbb{Z}[\omega_3]$ certificate scripts** running in **`20.46 s` total** on a single Apple M1 core (up to **`350x` faster** than floating-point `lstsq` scripts, with zero floating-point margin and zero external batch files).
> - **[`unitaryfoundation/stabrank PR #194`](https://github.com/unitaryfoundation/stabrank/pull/194) (`6fc15c5`):** **`10 / 10` Lean 4 proof modules (`0 sorryAx`)** settling all 4 remaining single-copy ($m=1$) magic-state cells (`qubit_H`, `qubit_T`, `H3`, `N` at $\chi = 2$) in both directions and formalizing constructive upper bounds for `qubit_T` ($m=7, 8 \le 9, \gamma = 0.3962$), `Norrell` ($m=5 \le 10, \gamma = 0.41918$ — best known finite-$m$ Norrell exponent on the board), and `H3` ($m=5 \le 12$).
> - **[`unitaryfoundation/stabrank Issue #195`](https://github.com/unitaryfoundation/stabrank/issues/195):** Standalone CI & `lean_certify.py` engineering proposal (`lake exe cache get` Mathlib caching + `submissions.yml` fork-PR `lean_proofs/` staging), separated cleanly from our proof PRs.
> - **Deep Methodological & Open-Source Notes:** See **[`LESSONS_LEARNED.md`](./LESSONS_LEARNED.md)**.

---

## 1. One-Command Standalone Verification (`~21 s` on 1 CPU Core)

This directory bundles all `35` `bounds/*.json` submissions and `5` `verify_challenge/cert_*.py` scripts from [`PR #193`](https://github.com/unitaryfoundation/stabrank/pull/193), all `12` `lean_proofs/` files from [`PR #194`](https://github.com/unitaryfoundation/stabrank/pull/194), and the minimal Apache-2.0 upstream schema and verification helpers (`schema/bound.schema.json`, `stabrank_verify.py`, `validate_bounds.py`, `qutrit_codes.py`, `rank_exclusion.py`, `rank_exclusion_codes.py`) from [`unitaryfoundation/stabrank`](https://github.com/unitaryfoundation/stabrank) (`commit edde871`).

```bash
python3 verify.py
```

`verify.py` checks:
1. `jsonschema` (`Draft202012Validator`), cross-field tier rules, filename-to-payload bijective parity, and exact claim-line matching across all `35` JSON submissions;
2. Full execution of all `5` exact $\mathbb{Z}[i]$ / $\mathbb{Z}[\omega_3]$ certificate scripts and symbolic upper-bound witness checks via `stabrank_verify.py` (`35/35 PASS` at `tier = verified`);
3. Static `0 sorry` / `0 admit` / `0 axiom` audit and theorem-signature verification across all `10` Lean 4 proof modules.

*(To compile the 10 Lean 4 modules from scratch against Mathlib inside a full clone of [`unitaryfoundation/stabrank`](https://github.com/unitaryfoundation/stabrank), copy `lean_proofs/` over `edde871` and run `cd lean_proofs && lake exe cache get && LEAN_NUM_THREADS=2 lake build LeanProofs`.)*

---

## 2. End-to-End Discovery Stopwatch & Compute Provenance Ledger (`3h 34m` Total)

Because [`unitaryfoundation/stabrank`](https://github.com/unitaryfoundation/stabrank) explicitly tracks LLM discovery velocity and compute provenance (`docs/ledger.json` & `CONTRIBUTING.md`), below is the complete wall-clock log of our `we*` (`@mizopl` + Gemini-powered agentic system) campaign on **2026-11-10**, extracted verbatim from our pre-registered micro-bet ledger (`4/4` ex-ante predictions won, **`Brier = 0.138`**) and GitHub PR creation timestamps:

| Stage | Wall-Clock Window (`CET`) | Duration | Ex-Ante Bet (`p` $\to$ Outcome) | Deliverables & Verification Receipt |
| :--- | :---: | :---: | :---: | :--- |
| **`Stage 0` (`X-Ray & CI Audit`)** | `16:04 – 16:07` | **`3 min`** | — | Audited `bound.schema.json`, `stabrank_verify.py` (`900 s` default / `3600 s` cap 1-core cliff, `"exact": true` $\to$ `tier=verified`), `site_challenge/build.py` author aggregation, and `submissions.yml` fork-PR sandboxing (`--diff-filter=A`). |
| **`Wave 1` (`Qubit Galois Descent`)** | `16:07 – 16:50` | **`43 min`** | `L-USP-001` (`p = 0.50` $\to$ **`1` WIN**) | Built [`cert_qubit_galois_m3_m4.py`](./verify_challenge/cert_qubit_galois_m3_m4.py) (`0.50 s`) and [`cert_qubit_galois_m5_m6_rank4.py`](./verify_challenge/cert_qubit_galois_m5_m6_rank4.py) (`7.08 s`, **`350x` faster** than `1649 s` float `lstsq`). Upgraded/added **`14/14` `qubit_H` & `qubit_T` lower bounds** ($m=3..6$, ranks $3..5$, including new `qubit_H-m6-lower-5.json`) to `tier=verified` (`exact: true`). |
| **`Wave 2` (`cat` & `CS` Lifts)** | `16:52 – 17:11` | **`19 min`** | `L-USP-002` (`p = 0.65` $\to$ **`1` WIN**) | Built [`cert_cat_m7_to_m10_lift.py`](./verify_challenge/cert_cat_m7_to_m10_lift.py) (`3.66 s`, **`125x` faster** than `460 s` $D_5$ search) and [`cert_cs_m3_m4_exact.py`](./verify_challenge/cert_cs_m3_m4_exact.py) (`2.61 s`, **`17x` faster** via $(I\otimes H)^{\otimes m}$ postselection) + 3 constructive upper witnesses (`cat` $m=9,10$ rank `9`, `CS` $m=4$ rank `9`). **`7/7 PASS tier=verified`**. |
| **`Wave 3` (`Qutrit Galois` + [`PR #193`](https://github.com/unitaryfoundation/stabrank/pull/193))** | `17:15 – 17:52` | **`37 min`** | `L-USP-003` (`p = 0.70` $\to$ **`1` WIN**) | Built [`cert_qutrit_galois_m3_m5.py`](./verify_challenge/cert_qutrit_galois_m3_m5.py) (`6.61 s`) using exact $\mathbb{Z}[\omega_3]$ projective ray canonicalization and regular-representation $\mathbb{Q}$-rank across `H3`, `N`, `S`, `T3` ($m=3..5$, including `T3` `rank=6`) + `cat` $m=7,8$ upgrades (`14/14 PASS`). Passed adversarial mutation & zero-context review gates; opened **[`PR #193`](https://github.com/unitaryfoundation/stabrank/pull/193)**. |
| **`Wave 4` (`Lean 4 0 sorryAx` + [`PR #194`](https://github.com/unitaryfoundation/stabrank/pull/194) + [`Issue #195`](https://github.com/unitaryfoundation/stabrank/issues/195))** | `17:53 – 19:38` | **`1h 45m`** (`105 min`) | `L-USP-004` (`p = 0.70` $\to$ **`1` WIN**) | Extended `ReflectQutrit.lean` with Norrell state $|N\rangle$, proved `M1Lower.lean` (`stabRank = 2` on all 4 open $m=1$ cells), generated & compiled 8 upper-bound modules (`QubitHM1`, `QubitTM1`, `H3M1`, `NorrellM1`, `QubitTM7`, `QubitTM8`, `NorrellM5`, `H3M5`) on an ephemeral Google Colab worker (`0 sorryAx`), and opened **[`PR #194`](https://github.com/unitaryfoundation/stabrank/pull/194)** + **[`Issue #195`](https://github.com/unitaryfoundation/stabrank/issues/195)**. |
| **TOTAL (`End-to-End`)** | **`16:04 – 19:38`** | **`3h 34m`** (`214 min`) | **`4 / 4` WIN (`Brier = 0.138`)** | **`35` exact `tier=verified` bounds (`20.46 s` 1-core runtime) + `10` zero-axiom Lean 4 modules + `1` upstream CI architecture issue.** |

- **Local Hardware:** Apple M1 laptop (`16 GB` unified RAM), `<= 2` active cores during verification.
- **Ephemeral Cloud Offload (Wave 4 only):** 1 short-lived Google Colab Linux container (`LEAN_NUM_THREADS=2`, torn down immediately after `lake build`) used solely to avoid unpacking a multi-gigabyte Mathlib `.olean` cache onto local laptop storage.

---

## 3. Summary of `PR #193` — `35` Certified `tier=verified` Bounds (`20.46 s` Total)

| Wave | Certificate Script / Witness | 1-Core Runtime | Certified Bounds (`35` Total) | Previous Tier (`edde871`) $\to$ New Tier | Exact Algebraic Mechanism |
| :--- | :--- | :---: | :--- | :--- | :--- |
| **1A** | [`cert_qubit_galois_m3_m4.py`](./verify_challenge/cert_qubit_galois_m3_m4.py) | **`0.50 s`** | `qubit_H`: $m=3$ (`r=3`), $m=4$ (`r=3,4`), $m=5,6$ (`r=4`)<br>`qubit_T`: $m=3,4,5$ (`r=3`), $m=5,6$ (`r=4`) (`10` bounds) | `reproduced` (float margin) $\to$ **`verified` (`exact: true`)** | 0-pivot & 1-pivot Codimension-2 Galois Quotient over $\mathbb{Q}(i, \sqrt{d})/\mathbb{Q}(i)$ ($d=2,3$) on $D_3$ (`1,080` states) & $D_4$ (`36,720` states) |
| **1B** | [`cert_qubit_galois_m5_m6_rank4.py`](./verify_challenge/cert_qubit_galois_m5_m6_rank4.py) | **`7.08 s`** | `qubit_H`: $m=5$ (`r=5`), $m=6$ (`r=5`, **NEW**)<br>`qubit_T`: $m=5$ (`r=5`), $m=6$ (`r=5`) (`4` bounds) | `reproduced` (`1649 s`) / `attested` (`~37 h`) / missing $\to$ **`verified` (`exact: true`)** | 2-step Pauli flat reduction $D_5 \to D_4 \to D_3$ + exact $\mathbb{Z}[i]$ 4-cover Galois quotient on $D_3$ (`2,406` / `2,372` orbits, zero external batch files) |
| **2A & 3A** | [`cert_cat_m7_to_m10_lift.py`](./verify_challenge/cert_cat_m7_to_m10_lift.py) + `cat-m9/10-upper-9.json` | **`3.66 s`** (`125x` faster) | `cat`: $m=7,8$ (`r=3`), $m=9,10$ (`r=4`, **NEW**)<br>`cat`: $m=9,10$ (`upper r=9`, **NEW**, $\gamma = 0.3962$) (`6` bounds) | `cited` / missing $\to$ **`verified` (`exact: true`)** | 2-step exact $\mathbb{Z}[i]$ slice-and-lift $c_5 \to c_6 \to c_7$ starting from $D_4$ (`36,720` states, `100` orbits) instead of $D_5$ (`2.42M` states) + recursive `<cat_2|` contraction witnesses |
| **2B** | [`cert_cs_m3_m4_exact.py`](./verify_challenge/cert_cs_m3_m4_exact.py) + `CS-m4-upper-9.json` | **`2.61 s`** (`17x` faster) | `CS`: $m=3$ (`r=4`), $m=4$ (`r=4`, **NEW**)<br>`CS`: $m=4$ (`upper r=9`, **NEW**, $\gamma = 0.7925$) (`3` bounds) | `reproduced` / missing $\to$ **`verified` (`exact: true`)** | Even-qubit Clifford postselection $(\langle 0|_2(I\otimes H))^{\otimes m}|\text{CS}\rangle^{\otimes m} \propto (2|0\rangle + (1+i)|1\rangle)^{\otimes m} \in \mathbb{Z}[i]^{2^m}$ verified by both $D_2$ slice-and-lift and unconditional 1-pivot $D_3$ sweep |
| **3B** | [`cert_qutrit_galois_m3_m5.py`](./verify_challenge/cert_qutrit_galois_m3_m5.py) | **`6.61 s`** | `H3`: $m=3$ (`r=4`), $m=4$ (`r=3, 4` **NEW**)<br>`N`: $m=3$ (`r=4`), $m=4$ (`r=3, 4` **NEW**)<br>`S`: $m=3,4,5$ (`r=4`)<br>`T3`: $m=3,4,5$ (`r=6`) (`12` bounds) | `reproduced` (random $\mathbb{C}^6$ float projection) / missing $\to$ **`verified` (`exact: true`)** | Exact $\mathbb{Z}[\omega_3]$ projective ray canonicalization ($\bar{z} = (a-b)-b\omega_3$ + row $\gcd$) & regular-representation $2k \times 2d$ $\mathbb{Q}$-rank (`0.11 s` 0-pivot $\tau$-Galois on `H3`; `12`/`74`/`173` pivot orbits on `S`/`N`/`T3`) |

Together with upstream upper bounds, Wave 3 settles $\chi(|H_3\rangle^{\otimes 3}) = 4$, $\chi(|N\rangle^{\otimes 3}) = 4$, $\chi(|S\rangle^{\otimes 3}) = 4$, and $\chi(|S\rangle^{\otimes 4}) = 4$ tightly in both directions at `verified` / `lean` tier.

---

## 4. Summary of `PR #194` — `10` Zero-Axiom (`0 sorryAx`) Lean 4 Modules

| Lean 4 Module | Compile Time (`2` threads) | Key Machine-Checked Theorems (`0 sorryAx`) | Mathematical Content |
| :--- | :---: | :--- | :--- |
| [`ReflectQutrit.lean`](./lean_proofs/LeanProofs/ReflectQutrit.lean) | `49.32 s` | `norrellVec_eq_ev` | Reflects the $m$-qutrit Norrell state $|N\rangle^{\otimes m} = ((|0\rangle + |1\rangle - 2|2\rangle)/\sqrt{6})^{\otimes m}$ into $\mathbb{Z}[\omega_3, \sqrt{3}]$ via `norZ : ZMod 3 -> Z`. |
| [`M1Lower.lean`](./lean_proofs/LeanProofs/M1Lower.lean) | `5.36 s` | `qubit_h_m1_stabRankP_eq_two`, `qubit_t_m1_stabRankP_eq_two`, `h3_m1_stabRank_eq_two`, `norrell_m1_stabRank_eq_two` | Proves $\chi > 1$ (and hence $\chi = 2$) for all 4 remaining single-copy states via the exact stabilizer ratio period condition `IsStabP.pow_period_eq` ($(z_1/z_0)^4 = 1$ for $p=2$; $(z_i/z_0)^{12} = 1$ for $p=3$). |
| [`QubitHM1StabRank.lean`](./lean_proofs/LeanProofs/QubitHM1StabRank.lean), [`QubitTM1StabRank.lean`](./lean_proofs/LeanProofs/QubitTM1StabRank.lean), [`H3M1StabRank.lean`](./lean_proofs/LeanProofs/H3M1StabRank.lean), [`NorrellM1StabRank.lean`](./lean_proofs/LeanProofs/NorrellM1StabRank.lean) | `4.96 – 8.38 s` each | `qubit_h_m1_stabRankP_le_two`, `qubit_t_m1_stabRankP_le_two`, `h3_m1_stabRank_le_two`, `norrell_m1_stabRank_le_two` | Explicit 2-term computational-basis stabilizer decompositions completing $\chi = 2$ in Lean 4. |
| [`NorrellM5StabRank.lean`](./lean_proofs/LeanProofs/NorrellM5StabRank.lean) | **`1.96 s`** | `norrell_m5_stabRankP_le_ten`, `norrell_m5_stabRank_le_ten` | Formalizes the 10-term stabilizer decomposition $\chi(|N\rangle^{\otimes 5}) \le 10$ across $3^5 = 243$ amplitudes, certifying the best known finite-$m$ Norrell exponent $\gamma = \log_3(10)/5 \approx 0.41918$. |
| [`H3M5StabRank.lean`](./lean_proofs/LeanProofs/H3M5StabRank.lean) | **`1.95 s`** | `h3_m5_stabRankP_le_twelve`, `h3_m5_stabRank_le_twelve` | Formalizes the 12-term decomposition $\chi(|H_3\rangle^{\otimes 5}) \le 12$ across $3^5 = 243$ amplitudes. |
| [`QubitTM7StabRank.lean`](./lean_proofs/LeanProofs/QubitTM7StabRank.lean) & [`QubitTM8StabRank.lean`](./lean_proofs/LeanProofs/QubitTM8StabRank.lean) | `34.89 s` & **`2.05 s`** | `qubit_t_m7_stabRankP_le_nine`, `qubit_t_m8_stabRankP_le_nine` | Formalizes $\chi(|\text{qubit\_T}\rangle^{\otimes 7}) \le 9$ ($2^7 = 128$ amplitudes) and $\chi(|\text{qubit\_T}\rangle^{\otimes 8}) \le 9$ ($2^8 = 256$ amplitudes, $\gamma = \log_2(9)/8 \approx 0.3962$). |

---

## 5. What We Did Not Touch, Open Frontier & Invitation to Reuse / Cite

- **What Remains Open (`Honest Scope Boundary`):**
  1. **`qubit_H` and `qubit_T` at $m=5, \text{rank}=6$ (`attested` $\to$ `verified`):** Our Wave 1C audit confirmed that after 2-qubit Pauli flat reduction to $D_3$, the 1D-kernel 5-cover search spans `5,939,465` (`qubit_H`) and `6,115,136` (`qubit_T`) orbits (~`36.4–37.2` CPU-hours in Python), exceeding `stabrank`'s `3600 s` single-core `verified` budget unless compressed via a new invariant or formalized directly as a Lean 4 proof (`tier = lean`).
  2. **Higher-$m$ Qubit & Qutrit Upper Bounds ($m \ge 6$ for `Norrell`/`H3`, $m \ge 9$ for `qubit_H`/`qubit_T`):** As shown in our companion package [`../solutions/magic-state-stabilizer-rank-exponents/`](../solutions/magic-state-stabilizer-rank-exponents/) (`V3R1T4S PR #1039`), every pure tensor-box subspace $V_A \otimes V_B$ is algebraically obstructed below current records across all 9 open strata (`qubit_T` $m=7..10$, `qubit_H` $m=7,8$, `Norrell` $m=6$, `H3` $m=4,6$), meaning any strict exponent improvement must use genuinely entangled stabilizer dictionary vectors across tensor splits.
- **License & Upstream Credit:** All files in this directory are released under **Apache License 2.0** ([`LICENSE`](./LICENSE)), matching [`unitaryfoundation/stabrank`](https://github.com/unitaryfoundation/stabrank). Bundled unmodified verification helpers (`schema/bound.schema.json`, `stabrank_verify.py`, `validate_bounds.py`, `qutrit_codes.py`, `rank_exclusion.py`, `rank_exclusion_codes.py`) are copyright the [`unitaryfoundation/stabrank`](https://github.com/unitaryfoundation/stabrank) authors (Vincent Russo et al., Unitary Foundation).

```bibtex
@misc{westar2026stabrank,
  author       = {{we* (@mizopl and Gemini-powered agentic systems)}},
  title        = {Exact Cyclotomic Galois Certificates and Zero-Axiom {Lean 4} Proofs for {unitaryfoundation/stabrank}},
  year         = {2026},
  howpublished = {\url{https://github.com/mizopl/we-star/tree/main/stabrank}},
  note         = {Upstream PRs \#193 and \#194 on unitaryfoundation/stabrank}
}
```
