# Part VII — The Atlas of Productive Failures & Falsified Hypotheses: How Well-Diagnosed Dead Ends (`kill` Nodes) Birthed Our Best Theorems

> *"A falsified hypothesis logged with an exact algebraic diagnosis of why it failed is not wasted compute—it is half a theorem."* — **PROOFER Epistemic Principle (`Law M2`)**

---

## 1. Core Epistemic Thesis: Why `kill` Nodes Are First-Class Scientific Assets

Traditional scientific publications suffer from severe survivorship bias: papers present only the final victorious derivation (`close` nodes), silently discarding the 80% of plausible conjectures, ansatze, and search heuristics that failed along the way (`kill` nodes). When those negative results vanish into scratchpads, future researchers—and future autonomous agents—are condemned to repeat the exact same dead ends.

In **PROOFER (`CONSTITUTION v17`)**, every non-trivial campaign is governed by the append-only reasoning graph (`rgraph.py`) and the **Federated Micro-Bet Engine (`micro_bet.py`)**. Under **Law M2 (The Two-Miss Pivot)**, two consecutive negative micro-bets (`L-*-* = 0`) on the same structural ansatz automatically trigger an algebraic diagnosis and a mandatory representation pivot:

1. **No Anonymous Failures:** Every `kill` node in `StartFresh_v16/graphs/ancestral_v15_atlas/*.jsonl` must record the exact quantitative obstruction—a prime divisor invariant, a Frobenius parity mismatch, a Poisson expectation ceiling, or a borrow-propagation horizon—that killed the hypothesis.
2. **Negative Certificates as Boundary Theorems:** When an exhaustive GPU or SAT sweep proves that an entire symmetry class contains zero solutions, that `kill` node becomes an exact **No-Go Theorem** delineating the phase boundary of the problem.
3. **Obstruction-Driven Invention:** In every major campaign across the V3R1T4S repository, the winning theorem was not guessed out of thin air; it was algebraically forced by inspecting the exact failure mode of a preceding `kill` node.

```mermaid
flowchart LR
    H1["Initial Ansatz (open)"] --> MB1["Micro-Bet 1 (< 60s)"]
    MB1 -- "Miss (L = 0)" --> D1["Diagnostic Node (falsify)"]
    D1 --> MB2["Micro-Bet 2 (Refined Parameter)"]
    MB2 -- "Second Miss (Law M2 Trigger)" --> KILL["Formal Dead-End Certificate (kill)"]
    KILL -- "Extract Exact Algebraic Obstruction" --> PIVOT["Representation Pivot (Law M2 / M7)"]
    PIVOT --> THM["Breakthrough Construction / Theorem (close)"]
```

---

## 2. Master Overview: 10 Falsified Hypotheses That Forced Breakthroughs

| # | Domain & `.jsonl` Graph | Dead-End / `kill` Node ID | Exact Algebraic / Operational Obstruction | Resulting Breakthrough Theorem / World Record (`close`) |
| :--- | :--- | :--- | :--- | :--- |
| **1** | **Lychrel Numbers**<br>`lychrel-new-base-proof.jsonl` | `D1_KUITCHE_2023_BASES_3_TO_10`<br>`D2_BASE_12_ODD_CORE_PARITY` | Kuitché (2023) patterns fail mechanically on bases $3..10$; $\gcd(b-1,b+1)=1$ in base $12$ kills odd-length cores. | **Carry-Wire Decoupling Theorem** ($b \equiv 2 \pmod{24}$: unconditional Lychrel proofs in bases $50, 98, 146$, `PR #517`). |
| **2** | **Quantum `AME(20, 17)`**<br>`ame-states-open-cells-huber-table.jsonl` | `L-ASOC-001` (`C2 = -C1`)<br>`L-ASOC-004` (`G40-Jacobi`) | Antisymmetric block ansatz has Poisson $\lambda = 43.17$ bad cuts; `G40` search trapped at `9/4970` bad orbits due to $84$ hidden odd-Frobenius orbits. | **Theorem D22 (Chiral Interface Gauge Dressing)** & **Theorem D28 (177-Orbit Frobenius Parity Law)** $\to$ `AME(20, 17)`, `AME(20, 16)`, `AME(20, 13)` (`0/184,755` bad minors, `PR #614`). |
| **3** | **Quantum `AME(19, 11)` & `AME(20, 11)`**<br>`ame-states-open-cells-huber-table.jsonl` | `L-ASOC-017` (`D31` Exhaustion)<br>`L-ASOC-020` (`D33` Exhaustion) | Exhausting $2,357,947,690$ symmetric $19$-circulants and $1,224,806,400$ $G_{40}$ pairs over $\mathbb{F}_{11}$ yields zero `AME` states. | **Exact Phase Boundary** $q_c(G_{40}, n=20) = 13$ & **Theorem D33B (Disjoint QNR Coset Breakthrough)**, slashing bad orbits over $\mathbb{F}_{11}$ from `31/4970` to `12/4970`. |
| **4** | **Pure Quantum Codes (`[[15,0,8]]`)**<br>`ame-states-open-cells-huber-table.jsonl` | `CODETABLES_15_0_8_IMPURE` | Published `codetables.de` entries `[[15,0,8]]_5` ($w_{\text{pure}}=7$, $190$ bad cuts) and `[[15,0,8]]_7` ($w_{\text{pure}}=1$, $3,003$ bad cuts) are impure. | **Pure Bordered-Circulant `AME(15, 7)`** (`0/6,435` singular cuts over $\mathbb{F}_7$, `PR #576`, independently confirmed by Dr. Markus Grassl). |
| **5** | **Ternary Fast Matrix Mult.**<br>`fmm-ternary-integer-ring-upgrade.jsonl` | `F1320_OBSTACLE` | Default `<4,3,3>` block row ordering `(0,1,2,3)` induces irreducible $\pm 2$ additive seam collisions across $U, V, W$. | **Signed Sub-Block Gauge Conjugation** $\pi = (0,1,3,2) \in B_4$, eliminating all $\pm 2$ entries (`PR #402`, `#432`, `#615`). |
| **6** | **FMM `<4,4,4>` Rank-47 Search**<br>`fmm-4x4x4-rank47-3x3x3-rank22.jsonl` | `D2035_DEGROOTE`<br>`L-F4R3-002` | Prime invariants $p \in \lbrace 2,3,5 \rbrace$ forbid direct $GL_4(\mathbb{Q})^{\times 3}$ De Groote conjugation of `DPS-48` to $\mathbb{Z}$; top-down flip walk traps at rank $49$. | Saved weeks of doomed rational gauge search; redirected compute to **Exact $2$-Adic Hensel Lifting** and ternary seam surgery. |
| **7** | **Additive Complexity SLPs**<br>`fmm-additive-complexity-records.jsonl` | `H0110_L1` (`L-FACR-001 = 0`) | Purely syntactic forward Common Subexpression Elimination (CSE) stalls at `cr = 391` on `<4,5,6>` (vs `345` SOTA). | **Tellegen $W^T$ Dual Transposition + Matroid $\text{Cl}_1$ Over-Provision-then-Cancel**, yielding **48 SLP world records (`PR #616`)**. |
| **8** | **Fault-Tolerant Quantum Circuits**<br>`03_invsqrt` campaign | `NAIVE_MSB_FIRST_SUBTRACTION` | Subtracting partial products largest-row-first (`A0 -> A1 -> A2`) dirties every upper accumulator bit via carry ripples. | **Smallest-Row-First Reversal (`A2 -> A1 -> A0`) + Exact Borrow-Horizon Truncation (`v14`)**, saving **$-548$ Toffolis and $-8$ qubits**. |
| **9** | **DNA Minimizer Density**<br>`minimizer-density-record-tables.jsonl` | `MONTE_CARLO_NOISE_FLOOR` | Stochastic sequence sampling exhibits $\sim 10^{-4}$ variance, masking genuine density improvements on $(w,k)$ tables. | **Exact Fast Zeta Transform (`SOS-DP`)** over all $4^{w+k-1}$ windows ($>10,000\times$ speedup, **17 world records**, `PR #425, #433`). |
| **10** | **Agentic Infrastructure**<br>`preflight.sh` & `CONSTITUTION v17` | `X1`–`X12` & `Drift A4` | `SIGSTOP` background starvation (`X11`), broken `/usr/bin/python3` stub (`X9`), prose-to-certificate transcription error (`X12`). | **12 Automated Preflight Gates (`preflight.sh`)** & **Subagent `outreach-auditor` (`K12`)** enforcing zero-trust digit-for-digit verification. |

---

## 3. Ten Concrete Case Studies from the Ancestral `.jsonl` Atlas

### Case Study 1: Lychrel Numbers and the Base-12 Parity Obstruction (`lychrel-new-base-proof.jsonl`)
- **The Dead Ends (`D1_KUITCHE_2023_BASES_3_TO_10` & `D2_BASE_12_ODD_CORE_PARITY_OBSTRUCTION`):** We began by mechanically testing the constructions claimed in Kuitché (2023) across bases $3 \le b \le 10$ and found explicit palindrome collisions or algebraic induction breakdowns in every single base (`D1`). Attempting to salvage the approach in base $b = 12$ hit a second wall (`D2`): because $\gcd(b-1, b+1) = \gcd(11, 13) = 1$, odd-length core digits cannot absorb the alternating $2$-cycle carry parity without breaking divisibility.
- **The Pivot & Theorem:** Diagnosing *why* $\gcd(b-1, b+1)$ failed in base $12$ revealed that if we choose $b \equiv 2 \pmod{24}$, two structural miracles occur simultaneously: $b-2$ is divisible by $24$, and carry wires across four inner state registers decouple completely from outer mirror digits. This directly birthed the **Carry-Wire Decoupling Theorem** (`PR #517`), yielding the first unconditional machine-certified Lychrel-seed proofs in bases $b = 50, 98, 146$.

### Case Study 2: Quantum `AME(20, 17)` and the Hidden 84 Frobenius Orbits (`ame-states-open-cells-huber-table.jsonl`)
- **The Dead Ends (`L-ASOC-001` & `L-ASOC-004`):** In searching for an open Absolutely Maximally Entangled state of $20$ qudits over $\mathbb{F}_{17}$, our first micro-bet (`L-ASOC-001`) tested the antisymmetric double-circulant ansatz $C_2 = -C_1$. It failed with a Poisson expectation of $\lambda = 43.17$ singular cuts. Switching to the twisted dihedral group $G_{40}$ with a 1-D Jacobi sweep (`L-ASOC-004`) pushed the defect down to `9/4970` bad orbits, where it hit a hard local-minimum wall.
- **The Pivot & Theorem:** Inspecting the $9$ stubborn orbits revealed that our solver had partitioned the $4,970$ orbits assuming only $93$ self-conjugate ($b=1$) orbits existed. Exact orbit enumeration proved that **$84$ additional odd-Frobenius ($b=1$) orbits were masquerading inside the generic set**, making $93 + 84 = 177$ total (**Theorem D28: 177-Orbit Frobenius Parity Law**). Coupling this exact invariant with **Theorem D22 (Chiral Interface Gauge Dressing)** immediately broke the `9/4970` barrier, producing `0/184,755` singular $10 \times 10$ minors across **three open cells**: `AME(20, 17)`, `AME(20, 16)`, and `AME(20, 13)` (`PR #614`).

### Case Study 3: Exhaustive No-Go Theorems for `AME(19, 11)` and `AME(20, 11)` (`L-ASOC-017` & `L-ASOC-020`)
- **The Dead Ends (`D31` & `D33`):** Could the $19$-circulant or $G_{40}$ constructions descend to $\mathbb{F}_{11}$? Rather than running endless heuristic hill-climbers, we wrote an exact zero-allocation Metal/C symbiosis kernel and exhausted all $11^9 = 2,357,947,690$ symmetric $19$-circulants over $\mathbb{F}_{11}$ (`L-ASOC-017`, Theorem `D31`) and all $1,224,806,400$ self-dual $G_{40}$ pairs (`L-ASOC-020`, Theorem `D33`). Both returned `0` valid states.
- **The Pivot & Theorem:** These two `kill` nodes proved an exact algebraic phase-transition boundary $q_c(G_{40}, n=20) = 13$ for single-interface gauge dressing. Furthermore, analyzing the $31/4970$ floor of `D33` revealed that non-zero entries on the quadratic residue coset $S_0$ caused systemic determinant collisions—Directly birthing **Theorem D33B (Disjoint QNR Coset Support)**, which zeroed $S_0$ and slashed the $\mathbb{F}_{11}$ defect from `31/4970` to `12/4970` in $20$ seconds.

### Case Study 4: Discovering Impure Stabilizer Codes in `codetables.de` (`PR #576`)
- **The Dead End (`CODETABLES_15_0_8_IMPURE`):** While benchmarking $15$-qudit stabilizer states, we audited the reference `[[15, 0, 8]]_5` and `[[15, 0, 8]]_7` self-dual stabilizer codes listed in Grassl's `codetables.de`. Our exact minor verifier revealed that neither code was pure: `[[15, 0, 8]]_5` had pure weight $w_{\text{pure}} = 7$ ($190$ singular cuts), and `[[15, 0, 8]]_7` had $w_{\text{pure}} = 1$ ($3,003$ singular cuts). Thus, neither yielded a genuine `AME(15, q)` state.
- **The Pivot & Theorem:** Recognizing that cyclic group generators over $\mathbb{F}_7$ suffered from trivial weight-1 stabilizer vectors when unbordered, we switched to a **pure bordered-circulant architecture** over $\mathbb{F}_7$, achieving `0/6,435` singular $7 \times 7$ cuts (`PR #576`, independently verified by Dr. Markus Grassl).

### Case Study 5: Ternary Fast Matrix Multiplication Seam Collisions (`fmm-ternary-integer-ring-upgrade.jsonl`)
- **The Dead End (`F1320_OBSTACLE`):** When lifting low-rank bilinear matrix multiplication schemes into restricted ternary/half-ternary coefficient rings $\lbrace -1, 0, +1, \pm 1/2 \rbrace$, standard block concatenation on `<4,3,3>` under the natural basis ordering `(0,1,2,3)` repeatedly stalled because shared rank-1 boundary terms collided with $\pm 2$ coefficients.
- **The Pivot & Theorem:** Instead of perturbing individual rank-1 summands, we diagnosed the $\pm 2$ obstacle as a relative parity mismatch across block interfaces. Applying a **Signed Sub-Block Gauge Conjugation** $\pi = (0,1,3,2) \in B_4$ inverted the interface signs and eliminated every $\pm 2$ collision cleanly (`PR #402`, `#432`, `#615`).

### Case Study 6: The De Groote Rational Gauge Obstruction on `<4,4,4>` (`fmm-4x4x4-rank47-3x3x3-rank22.jsonl`)
- **The Dead Ends (`D2035_DEGROOTE` & `L-F4R3-002`):** Two natural pathways toward `<4,4,4>` integer rank-47 were tested early: (a) applying continuous $GL_4(\mathbb{Q})^{\times 3}$ De Groote equivalence transformations to clear denominators in known rank-48 rational schemes (`DPS-48`), and (b) running unconstrained top-down flip-graph walks from the trivial rank-64 tensor (`L-F4R3-002`). Both failed: `D2035_DEGROOTE` proved via invariant prime divisors $p \in \lbrace 2, 3, 5 \rbrace$ of determinant ratios that `DPS-48` lies in an algebraically isolated rational orbit that *cannot* be conjugated to $\mathbb{Z}$, while `L-F4R3-002` trapped at rank $49$.
- **The Pivot & Theorem:** Proving `D2035_DEGROOTE` saved weeks of futile numerical gauge optimization and immediately redirected our compute to **exact $2$-adic Hensel lifting (`hensel_lift.py`)** and structured Kaporin/Sedoglavic seam surgery.

### Case Study 7: Why Forward CSE Stalls on Matrix Multiplication SLPs (`fmm-additive-complexity-records.jsonl`)
- **The Dead End (`H0110_L1`, `L-FACR-001 = 0`):** Our initial micro-bet on reducing the additive complexity of Straight-Line Programs (SLPs) applied greedy syntactic Common Subexpression Elimination (CSE) in the forward direction ($U, V \to W$). On `<4,5,6>`, forward CSE stalled at `cr = 391`, far behind the `345` SOTA (`L-FACR-001 = 0`).
- **The Pivot & Theorem:** Diagnosing `H0110_L1` showed that syntactic CSE only detects axial $2$-patches ($x_i \pm x_j$), whereas dense $W$-combination matrices hide deep **Matroid $\text{Cl}_1$ diagonal $4$-patches** ($\pm x_i \pm x_j \pm x_k \pm x_l = (x_i \pm x_j) \pm (x_k \pm x_l)$). Moreover, by **Tellegen's Transposition Theorem**, transposing the post-addition matrix $W \mapsto W^T$ turns wide fan-out trees into narrow fan-in trees where $\text{Cl}_1$ cancellation flourishes. Combining **Tellegen $W^T$ Dual Transposition** with **Over-Provision-then-Cancel** produced **48 unconditional SLP world records (`PR #616`)**.

### Case Study 8: Carry-Ripple Contamination in Quantum Inverse Square Root (`03_invsqrt`)
- **The Dead End (`NAIVE_MSB_FIRST_SUBTRACTION`):** In compiling fault-tolerant Clifford+$T$ circuits for fixed-point $1/\sqrt{x}$ Newton-Raphson iterations, subtracting shifted partial products in standard largest-row-first order (`A0 -> A1 -> A2`) triggered full-width borrow ripples that dirtied every high-order accumulator ancilla, making clean uncomputation exorbitant.
- **The Pivot & Theorem:** Reversing the subtraction schedule to **Smallest-Row-First (`A2 -> A1 -> A0`)** localized the active borrow cone, enabling **Exact Borrow-Horizon Truncation (`v14`)** and eliminating **$-548$ Toffoli gates and $-8$ logical qubits** with zero precision loss across 100% of inputs.

### Case Study 9: Breaking the Monte Carlo Noise Floor in DNA Minimizers (`minimizer-density-record-tables.jsonl`)
- **The Dead End (`MONTE_CARLO_NOISE_FLOOR`):** Standard literature heuristics for $(w, k)$ DNA minimizer orderings evaluate density on random $10^7$-base strings. Our early runs revealed that Monte Carlo variance ($\sim 10^{-4}$) was larger than the actual density gaps between elite orderings, causing hill-climbers to chase phantom statistical fluctuations.
- **The Pivot & Theorem:** We replaced stochastic sampling entirely with an **Exact Fast Zeta / Sum-Over-Subsets Dynamic Program (`SOS-DP`)** over the de Bruijn state space of all $4^{w+k-1}$ windows. This delivered a **$>10,000\times$ speedup** with zero variance and unlocked **17 exact world records** (`PR #425, #433`).

### Case Study 10: Operational Crashes Turned into Constitutional Guards (`X1`–`X12` in `preflight.sh`)
- **The Dead Ends (`X1`–`X12` & `Drift A4`):** Autonomous long-horizon loops failed in subtle operational ways: background processes launched inside subshells inherited open stdout descriptors and froze under `SIGSTOP` (`X11`); macOS `/usr/bin/python3` invoked a broken Xcode shim instead of Homebrew Python (`X9`); an early outreach email draft transposed two digits when copying a vector from a valid JSON certificate into prose (`X12`); and unverified session summaries drifted from disk state (`Drift A4`).
- **The Pivot & Theorem:** Every single operational failure was codified into a permanent mechanical gate in `preflight.sh` and `CONSTITUTION v17`: background jobs require `< /dev/null > log 2>&1 &`; `/opt/homebrew/bin/python3` is hard-enforced; and the dedicated **`outreach-auditor` (`K12`)** subagent blocks any external communication until every quoted vector, SHA-256 hash, and parameter tuple matches its JSON certificate digit-for-digit.
