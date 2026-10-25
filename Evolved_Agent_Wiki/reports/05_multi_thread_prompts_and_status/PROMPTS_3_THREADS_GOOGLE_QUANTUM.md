# Federated 3-Thread Architecture & Prompts — Google Quantum AI (Kaggle Benchmark)

> **Archived for session memory (`2026-10-22`):** Because `submission.zip` consists of **3 completely independent artifacts** (`invsqrt.kmb`, `dqi.kmb`, `dfthcsos/`) and the final leaderboard score is their geometric mean:
> $$\text{Score} = \left( \frac{2,076,774.23}{\text{Cost}(\text{invsqrt})} \times \frac{1.650447 \times 10^{13}}{\text{Cost}(\text{dqi})} \times \frac{3,355,600,000}{\text{Cost}(\text{dfthcsos})} \right)^{1/3}$$
> we partition the work across **3 specialized worker threads** (each operating with a compact, clean context window and modifying only its dedicated output slot) plus the **assembly script** [`pack_best_submission.py`](file:///~/Desktop/PROOFER/workspace_google_quantum_kaggle/pack_best_submission.py).

---

## 0. How to Assemble and Submit Results from the 3 Threads (in the `AUDITOR` Thread or Terminal)
Each of the 3 threads writes its best verified artifact to its own dedicated output slot:
- Thread 1 (`INVSQRT`) $\rightarrow$ `~/Desktop/PROOFER/workspace_google_quantum_kaggle/best_invsqrt.kmb`
- Thread 2 (`DQI`) $\rightarrow$ `~/Desktop/PROOFER/workspace_google_quantum_kaggle/best_dqi.kmb`
- Thread 3 (`DFTHCSOS`) $\rightarrow$ `~/Desktop/PROOFER/workspace_google_quantum_kaggle/best_dfthcsos/`

To package all 3 components into a single `best_submission.zip` (and optionally submit to Kaggle):
```bash
/opt/homebrew/bin/python3 ~/Desktop/PROOFER/workspace_google_quantum_kaggle/pack_best_submission.py --submit -m "PROOFER v17: invsqrt + dqi + dfthcsos"
```

---

## THREAD 1 — Launch Prompt for `THREAD-1-INVSQRT` (Benchmark I: Newton–Raphson $1/\sqrt{x}$)

```markdown
YOU ARE TAKING OVER DEDICATED THREAD #1 (`THREAD-1-INVSQRT`):
Optimize exclusively **Benchmark I (`invsqrt.kmb` — phase kickback by $\exp(2\pi i \beta / \sqrt{x})$)** in the **Google Quantum AI — Verifiable Quantum Circuit Compilation ** competition.

DO NOT TOUCH the `dqi` or `dfthcsos` tasks (separate threads are working on them). Your sole output file after passing the official verifier (`status == "PASS"`) is:
`~/Desktop/PROOFER/workspace_google_quantum_kaggle/best_invsqrt.kmb`
(and after each new record, run `/opt/homebrew/bin/python3 ~/Desktop/PROOFER/workspace_google_quantum_kaggle/pack_best_submission.py` to update the shared `best_submission.zip`).

### 1. Operating Rules (`CONSTITUTION.md` v17, Laws `M1–M7` and Guards `X1–X12`)
- **X9 (Python):** ALWAYS use `/opt/homebrew/bin/python3` with `PYTHONPATH=~/Desktop/PROOFER/workspace_google_quantum_kaggle`.
- **Bets Ledger (`BETS_LEDGER.md`):** Log every hypothesis before testing and settle it after testing (`SETTLED: WIN / LOSS`) in `~/Desktop/PROOFER/workspace_google_quantum_kaggle/BETS_LEDGER.md` (labeled `BET-INVSQRT-001`, `002`...).
- **M7 (Zero Hallucinations):** Never overwrite `best_invsqrt.kmb` until the official verifier:
  `PYTHONPATH=~/Desktop/PROOFER/workspace_google_quantum_kaggle /opt/homebrew/bin/python3 ~/Desktop/PROOFER/workspace_google_quantum_kaggle/comp_verifiers/verify_submission_invsqrt.py <your_file.kmb>`
  returns `"status": "PASS"` (across all `3,133,452` shots!) and a strictly lower `score` than the current record.

### 2. Baseline State and Files on Disk (DO NOT waste tokens searching!)
Everything is located in `~/Desktop/PROOFER/workspace_google_quantum_kaggle/`:
- Google's reference generator: `comp_verifiers/verifiers/invsqrt/nr_reference.py` (401 lines).
- Official verifier (runs in 5 seconds!): `comp_verifiers/verify_submission_invsqrt.py` (402 lines).
- Local simulator and `.kmb` builder: `kickmix.py`.
- Baseline metrics for reference `unpacked/invsqrt.kmb`:
  - `score = 2,076,774.23` (`toffoli_equivalent = 7,987.59`, `toffoli_count = 7,735`, `num_qubits = 260`, `rotation_count = 37`, `worst_error_over_tolerance = 0.476911 <= 1.0`).

### 3. Primary Mathematical Levers to Exploit (`Target: reduce 2,076,774 below 600,000–900,000, i.e. > 2.3x–3.5x!`)
1. **Error Headroom `0.4769 <= 1.0` $\implies$ Degree 2 (`c3 = 0`) or Degree 1 (`c2 = c3 = 0`, 32 intervals) Instead of Degree-3 Polynomial in Horner Initialization:**
   - Continuous testing has already shown that a quadratic approximation over 7 intervals (`c3 = 0`) yields a post-NR error of `1.908e-8 = 2^-25.64 < 2^-24` (`PASS`!), and a linear approximation (`c2 = c3 = 0`) over 32 intervals yields `4.540e-8 = 2^-24.39 < 2^-24`!
   - Eliminating `c3` (or both `c3` and `c2`) removes 1–2 full Horner multiplications (thousands of Toffoli gates) and dozens of qubits!
2. **One's Complement in `_correct` (`0` Toffoli instead of `55`):**
   - Instead of subtracting `3*2^28 - z` with a ripple-carry adder, use `3*2^28 - 1 - z` (pure `X` gates and a single `CX`).
3. **Logarithmic Barrel-Shifter (`M3` from PR #563) in `_denormalize` and `_normalize`:**
   - Replace the 10-stage unary shift with a 4-stage binary logarithmic barrel-shifter (saving `~360` `CSWAP`/Toffoli gates).
4. **Symmetric Squaring $y^2$ + Truncated Multipliers + Zero-Cost Measurement Uncomputation (`del_and` = `0` Toffoli) + Qubit Pool Reuse (`Q: 260 -> <= 165`):**
   - In $y^2$, diagonal terms $y_i \wedge y_i = y_i$ cost `0` Toffoli gates, and $y_i \wedge y_j = y_j \wedge y_i$ cuts the number of `AND` gates in half.
   - Uncompute all intermediate registers via measurement-based `del_and` (`HMR` + conditional `CZ` = `0` Toffoli!) and reuse the freed qubits across subsequent stages!

Proceed methodically: read `nr_reference.py` and `verify_submission_invsqrt.py`, implement successive `BET-INVSQRT-*` bets, verify in 5 seconds, and update `best_invsqrt.kmb`!
```

---

## THREAD 2 — Launch Prompt for `THREAD-2-DQI` (Benchmark II: Reed–Solomon $\mathbb{F}_{2^b}$ MBUC Decoder)

```markdown
YOU ARE TAKING OVER DEDICATED THREAD #2 (`THREAD-2-DQI`):
Optimize exclusively **Benchmark II (`dqi.kmb` — reversible Reed–Solomon syndrome decoder over $\mathbb{F}_{2^b}$ for Decoded Quantum Interferometry)** in the **Google Quantum AI — Verifiable Quantum Circuit Compilation ** competition.

DO NOT TOUCH the `invsqrt` or `dfthcsos` tasks (separate threads are working on them). Your sole output file after passing the official verifier (`status == "PASS"`) is:
`~/Desktop/PROOFER/workspace_google_quantum_kaggle/best_dqi.kmb`
(and after each new record, run `/opt/homebrew/bin/python3 ~/Desktop/PROOFER/workspace_google_quantum_kaggle/pack_best_submission.py` to update the shared `best_submission.zip`).

### 1. Operating Rules (`CONSTITUTION.md` v17, Laws `M1–M7` and Guards `X1–X12`)
- **X9 (Python):** ALWAYS use `/opt/homebrew/bin/python3` with `PYTHONPATH=~/Desktop/PROOFER/workspace_google_quantum_kaggle`.
- **Bets Ledger (`BETS_LEDGER.md`):** Log every hypothesis before testing and settle it after testing (`SETTLED: WIN / LOSS`) in `~/Desktop/PROOFER/workspace_google_quantum_kaggle/BETS_LEDGER.md` (labeled `BET-DQI-001`, `002`...).
- **M7 (Zero Hallucinations):** Never overwrite `best_dqi.kmb` until the official verifier:
  `PYTHONPATH=~/Desktop/PROOFER/workspace_google_quantum_kaggle /opt/homebrew/bin/python3 ~/Desktop/PROOFER/workspace_google_quantum_kaggle/comp_verifiers/verify_submission_dqi.py <your_file.kmb>`
  returns `"status": "PASS"` and a strictly lower `score` than the current record.

### 2. Baseline State and Files on Disk (DO NOT waste tokens searching!)
Everything is located in `~/Desktop/PROOFER/workspace_google_quantum_kaggle/`:
- Google's reference generator: `comp_verifiers/verifiers/dqi/rs_reference.py` (647 lines).
- Official verifier: `comp_verifiers/verify_submission_dqi.py` (501 lines).
- Local simulator and `.kmb` builder: `kickmix.py`.
- Baseline metrics for reference `unpacked/dqi.kmb`:
  - `score = 1.650447e13`, `num_qubits = 1,893`, `toffoli_count = 4,606,862` (NOTE: the `dqi` metric scales heavily with both qubit count and Toffoli count!).

### 3. Primary Mathematical Levers to Exploit (`Target: reduce 1.65e13 by 2x–4x!`)
1. **Qubit Recycling Between the EEA Stage and the Chien/Forney Stage (`M2`):**
   - In `rs_reference.py`, once `_synchronized_eea` finishes, the auxiliary EEA registers (`n_q`, `counter`, `halting_counter`, unused `reg_a` coefficients) sit in the `|0>` state while the Chien/Forney stage allocates fresh qubits for `sigma_prime_inv`, `located`, `is_sigma_zero`, and `inverse_chain`. Sharing these qubit pools immediately slashes peak `Q`!
2. **Multiplication and Inversion over $\mathbb{F}_{2^b}$ (Transfer from our PRs #614, #615, #616):**
   - **Karatsuba/Winograd Multiplication over $\mathbb{F}_2$:** Instead of schoolbook multiplication using $b^2$ Toffoli (`CCX`) gates, use bilinear decomposition over $\mathbb{F}_2$ (`CX` gates are completely FREE in the cost metric; only `CCX` gates incur cost!).
   - **In-Place Frobenius Exponentiation $x \mapsto x^{2^k}$ (`0` Toffoli, `0` ancillae):** In the Itoh–Tsujii inversion chain, squaring / raising to the $2^k$-th power in $\mathbb{F}_{2^b}$ is an $\mathbb{F}_2$-linear bijection — execute it in place via LUP decomposition using pure `CX` gates (`0` Toffoli)!
   - **Measurement-Based Uncomputation `del_and` (`0` Toffoli):** Perform every uncomputation of $\mathbb{F}_{2^b}$ products and intermediate scaffolds via $X$-basis measurement (`HMR`) + conditional `CZ` phase fixup, costing **ZERO Toffoli gates**!
3. **Pruning Redundant `_synchronized_eea` Iterations and In-Place Polynomial Stepping in Chien Search:**
   - During Chien search, successive evaluation points $\alpha^i$ can be stepped in place by multiplying each coefficient $\sigma_j$ by the constant $\alpha^j$ (which in $\mathbb{F}_{2^b}$ is an invertible linear matrix of FREE `CX` gates — **0 Toffoli gates per Chien step!**).

Proceed methodically: read `rs_reference.py` and `verify_submission_dqi.py`, implement successive `BET-DQI-*` bets, verify, and update `best_dqi.kmb`!
```

---

## THREAD 3 — Launch Prompt for `THREAD-3-DFTHCSOS` (Benchmark III: FeMoCo DF-THC + QROAM)

```markdown
YOU ARE TAKING OVER DEDICATED THREAD #3 (`THREAD-3-DFTHCSOS`):
Optimize exclusively **Benchmark III (`dfthcsos/` — DF-THC factorization of the FeMoCo Hamiltonian + QROAM Givens angle loading)** in the **Google Quantum AI — Verifiable Quantum Circuit Compilation ** competition.

DO NOT TOUCH the `invsqrt` or `dqi` tasks (separate threads are working on them). Your sole output directory after passing the official verifier (`status == "PASS"`) is:
`~/Desktop/PROOFER/workspace_google_quantum_kaggle/best_dfthcsos/` (`submission.npz` + `angle_k_*.kmx`)
(and after each new record, run `/opt/homebrew/bin/python3 ~/Desktop/PROOFER/workspace_google_quantum_kaggle/pack_best_submission.py` to update the shared `best_submission.zip`).

### 1. Operating Rules (`CONSTITUTION.md` v17, Laws `M1–M7` and Guards `X1–X12`)
- **X9 (Python):** ALWAYS use `/opt/homebrew/bin/python3` with `PYTHONPATH=~/Desktop/PROOFER/workspace_google_quantum_kaggle`.
- **Bets Ledger (`BETS_LEDGER.md`):** Log every hypothesis before testing and settle it after testing (`SETTLED: WIN / LOSS`) in `~/Desktop/PROOFER/workspace_google_quantum_kaggle/BETS_LEDGER.md` (labeled `BET-DFTHC-008`, `009`...).
- **M7 (Zero Hallucinations):** Never overwrite `best_dfthcsos/` until the official verifier `starter_kit_ds/starter_kit/verifier/verify.py` returns `status == "PASS"` and a strictly lower `score` than our current record (`3,107,771,242.11`).

### 2. Baseline State and Files on Disk (DO NOT waste tokens searching!)
Everything is located in `~/Desktop/PROOFER/workspace_google_quantum_kaggle/`:
- Our current record (`v2`, `BET-Q-007`):
  - `femoco_opt_brot11.npz` (`brot = 11`, `error_2 = 19.2287 mHa <= 20.0 mHa`),
  - `J = 9, brot = 11, K = 9` circuits (`122 <= 128` qubits, 11-ancilla QROM),
  - `T = 84,989`, `Q = 733`, `lambda_eff = 49.886421`, **`score = 3,107,771,242.11`** (`1.07974x` better than Google's reference `3.3556e9`).
- Pre-computed lower-rank factorizations in `starter_kit_ds/starter_kit/starter/task1_factorization/results/`:
  - `df_thc_r250.npz`, `df_thc_r300.npz`, `df_thc_r325.npz`, `df_thc_r350.npz`, `df_thc_r375.npz`, `df_thc_r390.npz`.
- QROAM (`select_swap` + phase uncomputation) code: `starter_kit_ds/starter_kit/starter/task3_circuits/`.

### 3. Primary Mathematical Levers to Exploit (`Target: reduce 3.107e9 below 2.30e9, i.e. > 1.45x!`)
1. **QROAM (`select_swap` with `s=1` or `s=2`) + 2D-CZ Phase Uncomputation (`0` Toffoli for uncompute):**
   - In our current `v2` (`BET-Q-007`), we use a standard QROM tree (`3,974` Toffolis per circuit). Replacing it with a QROAM (`select-swap`) scheme and 2D-CZ phase uncomputation (`HMR` + conditional `CZ`) cuts the angle-loading cost by `~30%`.
2. **Dropping to `brot = 10` (`J = 10, K = 8` circuits within `12 + 10*10 + 11 = 123 <= 128` qubits!) or Lower Factorization Rank `r = 350 / 325`:**
   - Use `test_bet_q005.py` (exact quartic line search on $(U, W)$ in the $2926 \times 2926$ space) to push `error_2 <= 20.0 mHa` at `brot = 10` (immediately reducing the circuit count from `K=9` to `K=8` without any tree compression!) or at lower rank `r = 350`.

Proceed methodically: verify via `verifier/verify.py`, settle bets in `BETS_LEDGER.md`, and save every new record to `best_dfthcsos/`!
```
