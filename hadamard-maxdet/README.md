# Hadamard Maximal Determinant (`1 <= n <= 120`) — System Overview, `13h 05m` Campaign Telemetry & Lessons Learned

> **Live Open-Science Deliverables (`we* + @mizopl`):**
> - **Living `1 <= n <= 120` Catalog & Verifier (`v2.0`):** <https://github.com/mizopl/hadamard-maxdet> (`120/120` orders curated, `50/50` explicit open-order `{+1, -1}` witness matrices including the first archived $89 \times 89$ witness, `8` new $n \equiv 1 \pmod 4$ determinant records, `27` alternative record-tying witnesses [`19` provably Hadamard-inequivalent], and `catalog/references.bib`).
> - **Self-Contained Reproducible Benchmark Package (`0.6 s` stdlib verifier):** [`../solutions/hadamard-maxdet-records/`](../solutions/hadamard-maxdet-records/) (upstream submission: [`elder-plinius/V3R1T4S PR #1053`](https://github.com/elder-plinius/V3R1T4S/pull/1053)).
> - **Upstream Technical Cross-Check on $n \equiv 3 \pmod 4$:** [`Math-AI-Caltech/hadamard-maxdet Issue #1`](https://github.com/Math-AI-Caltech/hadamard-maxdet/issues/1) (`7/7` CSV verification, second Hadamard-inequivalent Type 2 witness at $n = 51$, and `5` exact `CP-SAT INFEASIBLE` cyclotomic certificates).
> - **Deep Mathematical & Algorithmic Field Notes:** **[`LESSONS_LEARNED.md`](./LESSONS_LEARNED.md)**.

---

## 1. Summary of Results & One-Command Verification

Posed by Jacques Hadamard (1893) following J. J. Sylvester (1867), the maximal determinant problem asks for the largest $|\det X|$ over $n \times n$ sign matrices $X \in \{-1, +1\}^{n \times n}$ (equivalently, $D$-optimal weighing designs minimizing $\det(X^T X)^{-1}$). While Hadamard's orthogonal bound $n^{n/2}$ is attainable only for $n = 1, 2$ and $n \equiv 0 \pmod 4$, the remaining residue classes $n \equiv 1, 2, 3 \pmod 4$ are governed by the upper bounds of Barba (1933), Ehlich (1964), and Wojtas (1964).

In a single **`13 h 05 min`** human-steered multi-agent session (`2026-11-10 11:49 UTC` to `2026-11-11 00:55 UTC`), **`we*`** established **8 new constructive determinant records** in $n \equiv 1 \pmod 4$ (reporting normalized integers $D_{\text{norm}} = |\det X| / 2^{n-1}$ per [OEIS A003432](https://oeis.org/A003432)):

| Order $n$ | Previous $D_{\text{norm}}$ & Literature Baseline | New $D_{\text{norm}}$ (`we*`, Nov 2026) | Gain | Barba Ratio $R_{\text{prev}} \to R_{\text{new}}$ | Constructive Mechanism |
| ---: | :--- | :--- | ---: | :---: | :--- |
| **81** | $196 \cdot 20^{39}$ (Farmakis & Kounias, 1987) | **$200 \cdot 20^{39}$** | **+2.0408%** | $0.7723 \to \mathbf{0.7881}$ | 18 closed-four Hadamard switches on $H_{80}$ + `[OS-1]` border + 2-col `Schur-4` |
| **89** | $220 \cdot 22^{43}$ (Farmakis & Kounias, 1987)† | **$226 \cdot 22^{43}$** | **+2.7273%** | $0.7516 \to \mathbf{0.7721}$ | 13 closed-four switches on $\mathrm{Paley}(43) \otimes H_2$ + `[OS-1]` border + `Schur-4` |
| **93** | $239 \cdot 23^{45}$ (Orrick & Solomon, 2003/2007) | **$243 \cdot 23^{45}$** | **+1.6736%** | $0.7640 \to \mathbf{0.7768}$ | Asymmetric Goethals–Seidel $H_{92}$ ($A^T \ne A$, `[9,3,1,-1]`) + full-chirality `[OS-1]` |
| **97** | $256 \cdot 24^{47}$ (Solomon & Orrick, 2003/2007) | **$264 \cdot 24^{47}$** | **+3.1250%** | $0.7678 \to \mathbf{0.7918}$ | Asymmetric Goethals–Seidel $H_{96}$ (`[8,4,4,0]`) + `[OS-1]` + `Schur-4` polish |
| **101** | $7110 \cdot 25^{48}$ (Orrick & Solomon, 2003/2007) | **$7626 \cdot 25^{48}$** | **+7.2574%** | $0.8024 \to \mathbf{0.8606}$ | Doubly 3-normalized `[OS-2]` $H_{100}$ + coupled 6-entry rank-2 core/border flip |
| **105** | $3.8474 \times 10^{74}$ (T. Rokicki, 2005) | **$7413 \cdot 26^{50}$** ($4.1559 \times 10^{74}$) | **+8.0164%** | $0.7022 \to \mathbf{0.7585}$ | Chiral-slot Asymmetric GS $H_{104}$ (`[-6,-4,4,6]`) + `[OS-1]` + rank-1 unfreezing |
| **109** | $1.8775 \times 10^{78}$ (T. Rokicki, 2005)‡ | **$309 \cdot 27^{53}$** ($2.2503 \times 10^{78}$) | **+19.8565%** | $0.6482 \to \mathbf{0.7769}$ | Asymmetric Goethals–Seidel $H_{108}$ (`[9,3,3,3]`) + full-chirality `[OS-1]` |
| **117** | $7.2315 \times 10^{85}$ (T. Rokicki, 2005) | **$335 \cdot 29^{57}$** ($7.6161 \times 10^{85}$) | **+5.3179%** | $0.7186 \to \mathbf{0.7568}$ | Chiral-slot Asymmetric GS $H_{116}$ (`[-7,-7,-3,3]`) + full-chirality `[OS-1]` |

<sub>† On $n = 89$, `220 * 22^43` was derived analytically by Farmakis & Kounias (1987) without an archived $89 \times 89$ matrix in Orrick's `MaxDet` catalog; `M089.txt` supplies an explicit `{+1, -1}` witness, completing `50/50` open orders $23 \le n \le 119$. ‡ Also `+6.1856%` above merged `V3R1T4S PR #155` (`291 * 27^53`).</sub>

Alongside these 8 strict improvements, the campaign produced **27 dual-verified record-tying witnesses** (**19 provably Hadamard-inequivalent** modulo signed row/column permutations $P_1 Y P_2$ and transposition $P_1 Y^T P_2$, including a second inequivalent Type 2 two-circulant witness at $n = 51$) and **5 exact `OR-Tools CP-SAT INFEASIBLE` cyclotomic subgroup certificates** on $n = 51, 55$.

```bash
# Zero-dependency exact verification (~0.6 s stdlib Bareiss + 14-prime CRT; ~1.2 s with SymPy):
python3 ../solutions/hadamard-maxdet-records/verify-it-yourself/verify.py
python3 ../solutions/hadamard-maxdet-records/verify-it-yourself/verify.py --corrupt   # adversarial 1-sign flip (must exit 1)
```

---

## 2. How the `we*` Discovery System Works (Architecture Overview)

Rather than running a single long-context chatbot or an unstructured evolutionary loop over millions of random candidates, **`we*`** (`@mizopl` + federated Gemini and Claude Code agentic workflows) operates as a **role-separated, epistemically gated research architecture**:

```text
  Human Steering (@mizopl: 27 short prompts, ~870 tokens total — scope horizon, quality bar & honesty rules)
         │
         ├──► Supervisory Architect & Epistemic Watchdog (periodic audit of bets, stalls, and scope parity)
         │         │
         │         ├──► Dedicated Proof Worker (1 thread = 1 problem; iterative Python/Numba/BLAS experiments)
         │         ├──► Targeted Theoretical Scout (36-min isolated derivation of n = 51, 55 cyclotomic equations)
         │         ├──► Adversarial Tug-of-War Arena (2-advocate debate triggered automatically upon stalling)
         │         └──► Zero-Context Cold-Check Panel (3 independent blind verifiers + adversarial mutation gate)
         │
         └──► Parallel Catalog Thread (curating 1 <= n <= 120 historical baselines, provenance & open-science release)
```

Five operational mechanisms govern every campaign:

1. **Single-Example X-Ray Before Search (`Stage 0` Dissection):**
   No heuristic search is allowed before dissecting concrete optimal instances and verifier invariants in `< 30` lines of Python. Here, computing exact Gram spectra $G = M M^T$ on archived matrices `d49, d85, d101` reverse-engineered the unpublished *"Orrick & Solomon, to appear"* `[OS-1]` and `[OS-2]` block-replacement formulas in **21 minutes** — turning blind $n^2$-bit search into targeted algebraic surgery on order-$(n-1)$ Hadamard cores.
2. **Ex-Ante Brier-Calibrated Micro-Bets & Anti-Goodhart Accounting:**
   Before running a compute wave, the worker pre-registers an explicit falsifiable hypothesis, probability $p \in (0, 1)$, and wall-clock time-to-live (TTL) in an append-only ledger (`11` bets logged, `0` left open, `Brier = 0.266`). Partial misses are scored strictly (`Bet #6` broke a 39-year record on $n = 81$, yet was scored `0` because it had predicted $\ge 2$ new orders within 90 minutes).
3. **Deterministic Stall Detection & Adversarial Tug-of-War Gates:**
   Across `169+` historical `we*` bets, empirical win rates drop sharply after two consecutive non-winning iterations (`71.6% -> 31.1%`). When the worker hit consecutive `0`-outcomes on $n \equiv 3 \pmod 4$ (`Bets #4–#6`), a dedicated **Adversarial Tug-of-War subagent** pitted *Hypothesis H* against a counter-proposal *H'* over four structured rebuttals — exposing hidden symmetry locks and redirecting compute away from frozen manifolds toward warm asymmetric Goethals–Seidel cores (`Bets #8–#10`).
4. **Append-Only Dead-End & Coverage Ledgers Across Context Compactions:**
   Long campaigns span thousands of tool calls (`39` rolling context compactions in the discovery triad). Instead of re-reading raw chat logs, agents persist structured scoreboards recording exact tested vs. untested orders and falsified mechanisms, preventing post-compaction amnesia or duplicate dead-end runs.
5. **Judge-vs-Proposal Separation & Multi-Engine Zero-Trust Verification:**
   Fast `float64` Sherman–Morrison rank-1/rank-2 updates and FFT surrogates are treated strictly as *candidate generators*. Every candidate is immediately gated by exact arbitrary-precision Bareiss elimination, 14-prime 61-bit CRT modular elimination, `SymPy` Bareiss cross-check, closed-form `generator_params` reconstruction, an automated `--corrupt` mutation gate (`9/9` corrupted objects rejected), and blind zero-context refereeing.

---

## 3. End-to-End Stopwatch, Token Footprint & Compute Provenance (`13 h 05 min`)

### 3.1 Chronological Stage-by-Stage Stopwatch (`2026-11-10` to `2026-11-11`)

| Stage | Window (`UTC` / `CET`) | Duration | Pre-Registered Bets | Compute Used | Key Milestones, Dead Ends & Breakthroughs |
| :--- | :---: | :---: | :---: | :--- | :--- |
| **0. Literature X-Ray & `[OS]` Dissection** | `11:49–12:10 UTC`<br>(`12:49–13:10 CET`) | **`21 min`** | Pre-Bet X-Ray | Local M1 (`< 3 min` CPU) | Cached 50 archived `MaxDet` pages, Rokicki's 2005 logs (`105, 109, 117`), and `Math-AI-Caltech/hadamard-maxdet`. Mapped the Barba ratio cliff above $n = 101$ and reconstructed `[OS-1]`/`[OS-2]` algebra from $G = M M^T$ on `d49, d85, d101`. |
| **1. Initial `[OS-1]/[OS-2]` & Seam-Unfreezing Sprint** | `12:10–13:07 UTC`<br>(`13:10–14:07 CET`) | **`57 min`** | `Bet #1` (`0.65` $\to$ **WIN**)<br>`Bet #2` (`0.75` $\to$ **WIN**)<br>`Bet #3` (`0.50` $\to$ **WIN**) | Local M1 (`~22 min` CPU) | **5 world records within 78 minutes of start:** `n = 105, 109 (+15.20%), 117` at minute `38` (`12:27 UTC`); `n = 101` (`+7.2574%`, $R = 0.8606$) via 6-entry rank-2 core/border flip at minute `53`; `n = 89` (first archived $89 \times 89$ witness) at minute `78`. |
| **2. Valley of Dead Ends, Tug-of-War & `Closed-Four` Escape** | `13:07–20:06 UTC`<br>(`14:07–21:06 CET`) | **`6 h 59 min`** | `Bet #4` (`0.65` $\to$ `0`)<br>`Bet #5` (`0.65` $\to$ `0`)<br>`Bet #6` (`0.50` $\to$ `0*`)<br>`Bet #7` (`0.65` $\to$ `0*`) | Local M1 (`~145 min` wall / `~260` core-min) | Isolated 4 obstructions ($16/16$ 1-flip local optimality on $3 \pmod 4$; symmetric GS ceiling; cold $B \ge 4$ spin glass $R \le 0.51$; $c = 9$ root-of-unity cancellation) + ran adversarial **Tug-of-War** (`18:27–18:37 UTC`). Mining Orrick's footnotes showed `n = 81` was a 1987 `[FK]` holdout; 18 `Closed-Four` switches broke **6th record `n = 81` (`+2.0408%`)** and upgraded **`n = 89` (`+2.7273%`)** at `18:09 UTC`. |
| **3. Warm Asymmetric GS & 32-Fold Chirality Harvest** | `20:06–22:28 UTC`<br>(`21:06–23:28 CET`) | **`2 h 22 min`** | `Bet #8` (`0.65` $\to$ **WIN**)<br>`Bet #9` (`0.65` $\to$ **WIN**)<br>`Bet #10` (`0.65` $\to$ `0*`) | Local M1 (`~68 min` wall / `~205` core-min) | Relaxed Williamson symmetry ($A^T \ne A$) via Asymmetric & Even-$k$ Negacyclic GS cores and fixed the $S R = R S^{-1}$ anti-diagonal shift-gauge blind spot (~90% hidden column triplets): **7th record `n = 93`** in **`19.8 s`** (`20:26 UTC`); **8th record `n = 97` (`+3.1250%`)** + `n = 93` (`+1.6736%`) + `n = 109` (**`+19.8565%`**) at `21:38 UTC`; final `n = 105` (**`+8.0164%`**) & `n = 117` (**`+5.3179%`**) upgrades at `22:28 UTC`. |
| **4. Cyclotomic Scout, Colab `CP-SAT` & Inequivalent Ties** | `21:45–00:03 UTC`<br>(`22:45–01:03 CET`) | **`1 h 35 min`** *(overlapping)* | Parallel Scout +<br>`Bet #11` (`0.55` $\to$ `0*`) | Colab (`27.4 min` wall) + Local M1 (`~24 min`) | Scout derived Gaussian-period & PAF equations on $n = 51, 55$; 12-worker `CP-SAT` on Colab proved **5 exact `INFEASIBLE` theorems** (`0.29–1.64 s`); exported closed-form `generator_params` for all `8` records + **`27` record-tying witnesses (`19` Hadamard-inequivalent, incl. Type 2 `n = 51`)**. |
| **5. Zero-Trust Mutation Gate & 4-Target Release** | `00:03–00:55 UTC`<br>(`01:03–01:55 CET`) | **`52 min`** | Release Audit | Local M1 (`~10 min` verify) | Passed Bareiss + 14-prime CRT + SymPy + `9/9` `--corrupt` mutation gate + blind cold-check review (`36.96 s`); published `V3R1T4S PR #1053` (`00:42 UTC`), `mizopl/hadamard-maxdet v2.0`, `mizopl/we-star` Row `#36`, and `Math-AI-Caltech/hadamard-maxdet#1` (`00:51 UTC`). |

### 3.2 Multi-Agent Token Telemetry (`transcript_full.jsonl` Ground Truth)

Tokens are measured directly from untruncated JSONL session logs (at `3.8 chars/token` standard for Python + math), reporting both **Net Unique Stream Tokens** (all unique input/tool outputs, model reasoning/`thinking`, and emitted code/prose) and **Cumulative Rolling-Window Prefill Tokens** (bounded by periodic context compactions keeping active windows at `60k–155k` tokens):

| Role | Active Span (`CET`) | Steps / LLM Turns / Tool Calls | Compactions | Input / Tool Tokens | `thinking` Tokens | Code + Prose Tokens | **Net Unique Tokens** | Est. Cached Prefill | Human Prompts (`Tokens`) |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **1. Primary Discovery Worker** | `12:49 – 01:55` (`13h 05m`) | `2,504` / `904` / `1,448` | `26` | `~2.28M` | `~314k` | `~625k` | **`~3.22M`** | `~63.6M` | `5` (`~105 tok`) |
| **2. Supervisory Architect / Auditor** *(Hadamard slice)* | `12:49 – 02:08` *(shared)* | `993` / `494` / `483` | `12` | `~1.03M` | `~66k` | `~232k` | **`~1.32M`** | `~32.9M` | `17` (`~537 tok`) |
| **3. Cyclotomic Scout Subagent** *(`n = 51, 55`)* | `22:45 – 23:21` (`35.7m`) | `135` / `54` / `73` | `1` | `~176k` | `~17k` | `~50k` | **`~0.24M`** (`244k`) | `~3.9M` | `0` (`0 tok`) |
| **4. Tug-of-War & 3x Blind Cold-Check Gates** | `19:27–19:37` + `01:35–01:48` | `43` / `21` / `21` | `0` | `~71k` | `~6k` | `~12k` | **`~0.09M`** (`89k`) | `~0.7M` | `0` (`0 tok`) |
| **Subtotal — Core Discovery & Audit Fleet** | **`13h 05m`** | **`3,675` / `1,473` / `2,025`** | **`39`** | **`~3.55M`** | **`~403k`** | **`~920k`** | **`~4.87M`** | **`~101.1M`** | **`22` (`~642 tok`)** |
| **5. Parallel `1 <= n <= 120` Catalog & Provenance Thread** | `13:00 – 02:08` *(parallel)* | `819` / `342` / `567` | `14` | `~0.91M` | `~66k` | `~337k` | **`~1.32M`** | `~26.3M` | `5` (`~228 tok`) |
| **Grand Total (Discovery + `1 <= n <= 120` Catalog)** | **`13h 05m`** | **`4,494` / `1,815` / `2,592`** | **`53`** | **`~4.47M`** | **`~469k`** | **`~1.26M`** | **`~6.19M`** | **`~127.3M`** | **`27` (`~870 tok`)** |

### 3.3 Hardware Ledger: Local `16 GB` Apple M1 CPU vs. Google Colab

- **Local Apple M1 Laptop (`16 GB` unified RAM, capped at `<= 4` single-threaded CPU workers, `OMP_NUM_THREADS=1`):**
  - **`4 h 31 min` (`271.4 min`) active wall-clock compute** (`255.8 min` background compute union + `15.6 min` synchronous algebraic probes), totaling **`8.70` M1 CPU core-hours** (`~1.92` average active cores) across `50` iterative Python / Numba / BLAS scripts (`16,045` lines of code).
  - **100% (`8 / 8`) of the new world records and 100% (`27 / 27`) of the record-tying witnesses were discovered, optimized, and certified entirely on the local M1 CPU.** Replacing black-box matrix evaluation with exact algebraic projections (`32.4 ms` `Nullspace-4` linear projection, `20 us` bit-parallel `uint64` closed-four switching, and `@njit` zero-allocation scalar-DFT screening) provided a `100x–15,000x` per-move speedup over naive determinant updates.
- **Google Colab Cloud Offload (`27.4 min` total wall-clock, `0` GPU minutes used for matrix search):**
  - Invoked **only once** in Stage 4 (`Bet #11`, `23:35–00:27 CET`): **`13.0 min` (`781 s`)** of active 12-vCPU `OR-Tools CP-SAT` execution (plus `14.4 min` container spin-up/retry) to prove the **5 exact `CP-SAT INFEASIBLE` cyclotomic / Gaussian-period non-existence theorems** on $n = 51$ and $n = 55$.

---

## 4. Key Lessons Learned & Productive Dead Ends

Full algebraic derivations and equations are documented in **[`LESSONS_LEARNED.md`](./LESSONS_LEARNED.md)**. In brief:

1. **Break Hidden Symmetry Assumptions (`A^T != A` Asymmetric GS + Anti-Diagonal Chirality Gauge):** Classical Williamson and symmetric Goethals–Seidel cores lock row/column Gram spectra at the 2003–2007 ceiling on $n \le 97$. Dropping $A^T = A$ and removing a silent `e_0 = 0` shift-gauge restriction (since the back-circulant matrix $R$ satisfies $S R = R S^{-1}$, breaking cyclic shift invariance and hiding ~90% of `[OS-1]` column triplets) immediately unlocked **`n = 93, 97, 105, 109, 117`**.
2. **Walk Across Hadamard Equivalence Classes via Closed-Four Switching (`n = 81, 89`):** Reading provenance footnotes showed $n = 81$ was a 1987 Farmakis–Kounias holdout, yet its archived core $H_{80}$ was trapped at excess $L_1 = 608$. Applying $2 \times 4$ closed-four Hadamard switches in `20 us` (`uint64` bit-parallel) jumped across equivalence classes to $L_1 = 640$ (`n = 81`, `+2.04%`) and $L_1 = 728$ (`n = 89`, `+2.73%`).
3. **Unfreeze the Core–Border Seam via Rank-2 Updates & `32.4 ms` `Nullspace-4` Projection (`n = 101`):** Treating the Hadamard core $H_{n-1}$ as immutable misses coupled boundary-core interactions; a 6-entry rank-2 flip across the `[OS-2]` seam raised $n = 101$ by `+7.26%` ($R = 0.8606$), later reproduced deterministically in `32.4 ms` by linear nullspace projection.
4. **Enforce Exact Integer Gates Against `float64` Sherman–Morrison Drift:** Above $n \approx 80$, thousands of incremental `float64` rank-1 inverse updates near ill-conditioned Fourier blocks produced phantom determinant spikes (`4.6e9`), caught immediately by mandatory exact Bareiss elimination and fixed via periodic full `slogdet` resets every $\le 64$ steps.
5. **Convert Search Stalls into Exact Impossibility Theorems (`n = 51, 55`):** Six dead ends were logged explicitly — including $16/16$ 1-flip local optimality of known $n \equiv 3 \pmod 4$ 2-circulants, cold $B \ge 4$ spin-glass freezing ($R \le 0.51$), and $c = 9$ root-of-unity border cancellation ($\sum_{t \in \{1,4,7\}} \zeta_9^t = 0$) — turning unyielding strata into 5 machine-checked `CP-SAT INFEASIBLE` theorems.
6. **Human-in-the-Loop Leverage (`~870` Tokens Steering `~4.87M` Discovery Tokens):** `27` brief human interventions (`< 0.02%` of session tokens) prevented premature settlement after the first 3 records at minute 38, commissioned the unified `1 <= n <= 120` public catalog, synchronized the parallel $n = 51$ scout, and enforced strict scholarly separation between the **8 strictly higher determinant records** and the **19 Hadamard-inequivalent record-tying classes**.
