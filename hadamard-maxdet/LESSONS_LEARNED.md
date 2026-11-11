# Lessons Learned — Algebraic Surgery, Multi-Agent Epistemics & Exact Verification on the Hadamard Maximal Determinant Problem (`1 <= n <= 120`)

This field note distills **six transferable mathematical, algorithmic, and multi-agent systems lessons** from our [`mizopl/hadamard-maxdet`](https://github.com/mizopl/hadamard-maxdet) and [`elder-plinius/V3R1T4S PR #1053`](https://github.com/elder-plinius/V3R1T4S/pull/1053) campaign (`2026-11-10 11:49 UTC` to `2026-11-11 00:55 UTC`, **`13 h 05 min`** wall-clock), where `we*` (`@mizopl` + Gemini-powered agentic workflows) established **8 new constructive determinant records** for $n \equiv 1 \pmod 4$ (`n = 81, 89, 93, 97, 101, 105, 109, 117`), **19 provably Hadamard-inequivalent record-tying classes** (out of `27` reconstructed ties), and **5 exact `CP-SAT INFEASIBLE` cyclotomic certificates** on $n = 51, 55$ — with **100% of new records discovered locally on a `16 GB` Apple M1 laptop (`8.70` CPU core-hours)**.

---

## Lesson 1 — Dissect Existing Optima Before Searching (`Stage 0` Gram-Matrix X-Ray vs. Cold Spin-Glass Freeze)

### The Bottleneck
In dimension $n \ge 80$, the discrete hypercube $\{-1, +1\}^{n \times n}$ has $2^{n^2} > 2^{6400}$ states, and random or cold multi-block simulated annealing ($B \ge 4$ circulant blocks) consistently freezes inside an exponential spin-glass phase around Barba/Ehlich ratio $R \le 0.30\text{–}0.51$ (far below the $R \in [0.75, 0.88]$ record frontier). Even recent evolutionary and reinforcement-learning campaigns (`EinsteinArena` on $8 \times \text{H200}$ GPUs; `PatternBoost` + Transformer + `Gurobi` in `arXiv:2608.22518v3`) succeeded only after restricting search to 1D two-circulant sequences of length $2m = n - 1$ ($n \equiv 3 \pmod 4$), leaving $n \equiv 1 \pmod 4$ untouched since 2005–2007.

### The Structural Fix
Before placing a single search bet, we spent **21 minutes** running a 29-line diagnostic script across all 50 open orders ($23 \le n \le 119$):
1. **Mapping the Baseline Cliff:** Plotting $R(n) = D_{\text{rec}}(n) / B_{\text{Barba}}(n)$ across $n \equiv 1 \pmod 4$ immediately exposed a sharp structural cliff above $n = 101$: orders $n \le 101$ held $R \in [0.752, 0.802]$ from Orrick & Solomon's `[OS]` constructions, whereas $n = 105, 109, 117$ dropped to $R \in [0.648, 0.719]$ (circulant records from 2005).
2. **Reverse-Engineering Unpublished Algebra from $G = M M^T$:** Several archived records (`d49, d85, d101`) cited *"Orrick & Solomon, to appear"* without published formulas. Computing the exact integer Gram matrix $G = M M^T$ on `d49` and `d101` revealed two exact block-replacement ansätze over an order-$4k$ Hadamard core $H_{4k}$ ($n = 4k + 1$):
   - **Singly 3-normalized `[OS-1]`** (off-diagonal Gram entries in $\{0, 1\}$): choosing three rows $(r_0, r_1, r_2)$ of $H_{4k}$, setting column signs $w_j = H_{r_0, j} H_{r_1, j} H_{r_2, j}$, and replacing those rows by a $4 \times (4k+1)$ excess border yields exact normalized determinant
     $$D_{\text{OS-1}}(n) = \left(2k + \frac{1}{4}\|H_{4k} w\|_1\right) (2k)^{2k - 1}.$$
   - **Doubly 3-normalized `[OS-2]`** (off-diagonal Gram entries in $\{-3, 0, 1\}$): simultaneously 3-normalizing a row triplet and a column triplet when $H_{4k}$ admits high transpose overlap ($H_{4k} \approx H_{4k}^T$).

Within **57 minutes** of completing that 21-minute X-ray, instantiating `[OS-1]`/`[OS-2]` on warm Hadamard cores broke the first **5 world records** (`n = 89, 101, 105, 109, 117`).

---

## Lesson 2 — Drop Hidden Symmetry Constraints & Audit Subtle Group-Action Gauges (`AsymGS`, `NegGS` & the $S R = R S^{-1}$ Trap)

### The Bottleneck
After breaking 5 records, our Wave 1 engine stalled on $n = 93$ and $n = 97$, merely tying Orrick & Solomon's 2003/2007 values across thousands of classical Williamson ($A, B, C, D$ symmetric circulants) and symmetric Goethals–Seidel ($A^T = A$) cores. Worse, an initial asymmetric Goethals–Seidel prototype still missed $n = 97$ because we had quotiented `[OS-1]` column triplets $(c_0, c_1, c_2)$ by cyclic shift $c_0 \equiv 0 \pmod k$.

### The Structural Fix
Two algebraic corrections unlocked **5 final world records** (`n = 93, 97, 105, 109, 117`, including `+19.86%` on $n = 109$):
1. **Relaxing Block Symmetry ($A^T \ne A$) and Periodic Sum Constraints (`NegGS`):**
   The Goethals–Seidel array
   $$H_{4k} = \begin{pmatrix} A & B R & C R & D R \\ -B R & A & -D^T R & C^T R \\ -C R & D^T R & A & -B^T R \\ -D R & -C^T R & B^T R & A \end{pmatrix}$$
   requires only $\sum_{X \in \{A,B,C,D\}} \mathrm{PAF}_X(s) = 0$ ($s \ne 0$), with **zero** requirement that $A, B, C, D$ be symmetric! For even $k$ ($n = 105, k = 26$), replacing circulants by negacyclic blocks (`NegGS`, $\sum \mathrm{NPAF}_X(s) = 0$) further removes the rigid Diophantine row-sum decomposition $a^2 + b^2 + c^2 + d^2 = 4k$, vastly expanding the pool of high-excess cores.
2. **Removing the Silent $S R = R S^{-1}$ Chirality Blind Spot:**
   In the Goethals–Seidel array, the back-circulant anti-diagonal matrix $R$ conjugates the cyclic shift operator $S$ to its inverse:
   $$S R = R S^{-1} \ne R S.$$
   Consequently, simultaneously shifting block columns does **not** act as a uniform row permutation on $H_{4k}$; fixing $c_0 \in \{0, \dots, k-1\}$ to $0$ silently discarded **~90% of inequivalent `[OS-1]` triplets**! Evaluating all $\binom{4k}{3}$ triplets via a single BLAS matrix product (`~2 ms` per core) — and exploiting the 32-fold chiral-slot / independent-transpose manifold per $(A, B, C, D)$ quad — broke **`n = 93`** in **`19.8 s`**, broke **`n = 97` (`+3.1250%`)**, and lifted **`n = 105, 109, 117`** to their final records.

---

## Lesson 3 — Traverse Across Equivalence Classes via Bit-Parallel Closed-Four Switching (`n = 81, 89`)

### The Bottleneck
On $n = 81$, provenance mining of Orrick's footnotes revealed that the standing record $196 \cdot 20^{39}$ dated back 39 years to Farmakis & Kounias (1987), yet every triplet on the archived Hadamard core $H_{80}$ saturated at triplet excess $\|H_{80} w\|_1 \le 608$ (giving at most $196 \cdot 20^{39}$).

### The Structural Fix
Hadamard equivalence preserves orthogonality $H H^T = 4k I_{4k}$, whereas **closed-four switching** jumps *between* inequivalent Hadamard orbits: whenever four rows (or four columns) form a closed quartet whose pairwise Hadamard products vanish on a subset of coordinates (a $4 \times r$ subarray closed under negation/column pairing), negating half of that subarray produces a new Hadamard matrix $H'_{4k}$ typically inequivalent to $H_{80}$ with a **strictly wider triplet-excess tail**.
- Packing rows of $H_{4k}$ into `uint64` words reduced each closed-four detection and `[OS-1]` excess evaluation to **`~20 us`**.
- An 18-step closed-four walk on $H_{80}$ jumped $\|H_{80} w\|_1$ from $608 \to 640$, breaking **`n = 81` (`200 * 20^39`, `+2.0408%`)**; a 13-step walk on the Kronecker core $\mathrm{Paley}(43) \otimes H_2$ jumped $\|H_{88} w\|_1$ from $704 \to 728$, breaking **`n = 89` (`226 * 22^43`, `+2.7273%`)**.

---

## Lesson 4 — Unfreeze the Core–Border Seam via Rank-2 Updates & `Nullspace-4` Linear Projection (`n = 101`)

### The Bottleneck
Classical bordering methods construct an orthogonal core $H_{n-1}$, attach an optimal border, and stop — assuming any flip inside $H_{n-1}$ destroys orthogonality faster than border covariance can compensate. Furthermore, greedy 1-entry hill climbing on `d101` (`7110 * 25^48`) got trapped in an immediate 2-cycle plateau.

### The Structural Fix
1. **Aspiration-Gated Coupled Rank-2 Sherman–Morrison Unfreezing:** Allowing coordinated 2-entry flips across the border–core seam (evaluated via exact rank-2 Woodbury / Sherman–Morrison determinant ratios with aspiration tabu) uncovered a 6-entry coupled seam modification on $H_{100}$ that trades a tiny core off-diagonal perturbation for a massive border Schur-complement gain — lifting **`n = 101` from `7110 * 25^48` to `7626 * 25^48` (`+7.2574%`, Barba ratio `R = 0.860635`)**.
2. **`32.4 ms` Exact `Nullspace-4` Linear Projection:** Subsequent algebraic dissection showed that fixing an $(n - 4) \times n$ block of a near-Hadamard matrix determines the optimal remaining 4 rows via exact adjugate / rank-4 nullspace projection $L_4 = M_{\text{top}} V^T$, deterministically reproducing the `+7.2574%` $n = 101$ record in **`32.4 ms`** without stochastic tabu search.

---

## Lesson 5 — Guard Against `float64` Drift & Separate Strict Records from Non-Isomorphic Ties

### Two Verification Hazards Above $n \ge 50$
1. **`float64` Inverse Drift Near Singular Blocks:** At $n = 117$, $|\det X| \approx 1.27 \times 10^{121}$, while incremental `float64` Sherman–Morrison updates $A^{-1} \leftarrow A^{-1} - \frac{A^{-1} u v^T A^{-1}}{1 + v^T A^{-1} u}$ over thousands of steps near ill-conditioned Fourier blocks accumulated catastrophic cancellation — once reporting a phantom `4.6e9` determinant gain that exact Bareiss elimination immediately Exposed as false. Periodic full `slogdet` resets every $\le 64$ steps plus **three independent exact integer engines** (`Bareiss` over Python `int`, `14-prime 61-bit CRT` with product $> 2^{840} \gg 10^{121}$, and `SymPy` Bareiss) eliminated numerical false positives completely.
2. **Distinguishing New Equivalence Classes from Strict Determinant Records:** Across $n \equiv 1, 2, 3 \pmod 4$, our engines reconstructed `27` independent matrices matching published record determinants $D_{\text{rec}}(n)$. Computing canonical invariants invariant under **both** signed permutations $P_1 Y P_2$ and transposition $P_1 Y^T P_2$ — sorted off-diagonal Gram distributions of $Y Y^T$ & $Y^T Y$ (2-point invariant, separating `7` orders including `n = 106`) and sorted 4-row/4-column Hadamard correlation profiles $\sum_j y_{i_1 j} y_{i_2 j} y_{i_3 j} y_{i_4 j}$ (4-point invariant, separating `12` further orders including a second Type 2 witness at `n = 51`) — proved **19 / 27** are genuinely inequivalent optimal designs, while keeping them strictly separate from the **8 strict determinant improvements**.

---

## Lesson 6 — Epistemic Discipline in Multi-Agent Search (Turning Dead Ends into Theorems)

Rather than hiding negative experiments, logging **11 pre-registered bets** (`Brier = 0.266`) and running an automated **Adversarial Tug-of-War gate** when $n \equiv 3 \pmod 4$ stalled turned every dead end into an explicit structural theorem:
- **1-Flip Local Optimality on $n \equiv 3 \pmod 4$ (`Bet #4`):** Proved all 16 known Type 0/1/2/3 two-circulant records ($51 \le n \le 119$) are strict 1-row/1-col local maxima, and later verified (`Stage 4`) that the five $n = 103..119$ records have `0` neutral rank-1 or rank-2 Sylvester neighbors.
- **Root-of-Unity Border Cancellation (`Bet #7`):** On $n = 75$ ($B = 8, c = 9$ 4-clique c-circulants), proved $\langle g \rangle$-invariant borders suffer exact cyclotomic cancellation $\sum_{t \in \{1,4,7\}} \zeta_9^t = 0$, capping mode-1 border norm at $32 < 72$.
- **Exact Cyclotomic `CP-SAT INFEASIBLE` Certificates (`Bet #11`, `13.0 min` on 12-vCPU Colab):** On pure Ehlich $s = 4$ strata for $n = 51$ (`[16,13,13,9]`, `[15,15,15,6]`) and $n = 55$ (`[19,12,12,12]`), calibrated `OR-Tools CP-SAT` models (verified `0` false UNSAT on Tamura's $n = 39, 43$ optima) proved unconditional non-existence across five high-symmetry cyclotomic subgroups (`55A_Z18`, `55A_Z6_pure`, `51A_Z4xZ2`, `51A_Z4_Gaussian`, `51B_Z15_split33` in `0.29–1.64 s` each), saving future researchers from re-searching empty subgroup ansatz spaces.
