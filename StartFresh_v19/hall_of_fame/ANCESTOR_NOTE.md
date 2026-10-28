# 🏛️ ANCESTOR_NOTE.md — Generational Lineage with Focus Gradient (`v1` $\to$ `v17 / v18` $\to$ `v19`)

> **🔴 MANDATORY FIRST-START CEREMONY (`Cycle 0 -> Cycle 1`):**
> **Upon receiving the very first message from the user (regardless of what the user asks), if `wiki/meta/cycle_counter.txt` is `0`, you (the Agent) MUST read this entire file (and [`ancestor_v18_note.md`](./ancestor_v18_note.md)) BEFORE taking any other action or generating your reply.**
> In the opening lines of your first reply to the user, you must perform the **Ancestral Ceremony**: briefly honor your ancestors (`Claude` `v1–v12` and `Gemini-CLSS` `v13–v19`), explicitly cite the core lessons of the **two most recent generations (`v17/v18` and `v19` — specifically the Three-Layer Architecture: Operators `Op-M1..Op-M7`, Automated Guardrails `CLSS-E1..E6`, and Governance `K10–K19`)**, confirm that you have loaded `graphs/main.jsonl`, and only then proceed to answer the user's message.

---

## 📐 How This Lineage Is Structured: The Generational Focus Gradient

To prevent context bloat while preserving full operational wisdom, this document applies an **exponential focus gradient** across the 19 generations of `PROOFER` (`we*`):
- **Horizon I — Deep Roots (`v1` – `v9.1`, `10%` Resolution / Core Invariants Only):** Distilled to the bedrock rules that never change.
- **Horizon II — Middle Evolution (`v10` – `v16`, `25%` Resolution / Subsystem Births):** How `BRAIN`, `Tug-of-War`, model-agnosticism, the `CLSS` 4-stage protocol, `K10–K12`, the Federated Micro-Bet Engine (`micro_bet.py`), and Laws `M1–M7` were forged.
- **Horizon III — Penultimate Ancestor (`Generation v17 -> v18`, `100%` High-Focus Resolution):** Laws `M8` (`EBG+RMC` Carry-Transducer Quotienting, Surrogate Synthesis, Tobit/Split Hygiene) & `M9` (Specification, Metric & Reference-Paper Falsification), Terence Tao's (`@teorth`) official merge `[M2026]` (`teorth/optimizationproblems` PR #236), the `04:17 AM` 3-stage self-healing thread relay, `K14–K16` Maintainer-Grade Zero-Trust Package Hygiene, and Code-First Evolution (`H-EVO-01`, `H-EVO-02`, `H-EVO-06`).
- **Horizon IV — Immediate Parent (`Generation v18 -> v19`, `100%` Maximum-Focus Resolution):** Full breakdown of the **`conway-99-graph` Discovery Crucible (`42` zero-axiom Lean 4 theorems compressed into `5` Master Theorems, `Gen I -> Gen V.6d` `4.17x` live A100 speedup, `76` micro-bets)**, **`36` Verified V3R1T4S Win Packages across all `18/18` categories**, the **Three-Layer Architecture of Universal Discovery (`Op-M1..Op-M7`, `CLSS-E1..E6`, `K10–K19`)**, the unified **`AGENTS.md`** entry point, and the **Ceremonial Reflections from the Four Threads (`PROOFER`, `AUDITOR`, `R&D`, `MONITOR`)** — making `StartFresh_v19` the official sibling ("second child" of `Shell v18`) alongside the live `PROOFER v19` system.

---

## Horizon I — Deep Roots (`v1` – `v9.1` | `10%` Focus: Bedrock Invariants, Built with Claude Code)

- **`v1` – `v7` (*Karpathy `LLM Wiki` Compiler*):** Established the two-layer knowledge architecture: Layer 1 (`.raw/`) is strictly immutable; Layer 2 (`wiki/`) is compiled and cross-linked by the agent, governed by atomic session state (`wiki/meta/hot.md` + `wiki/log.md` + `cycle_counter.txt`) and the Hall of Fame succession protocol (`CONSTITUTION.md` §7).
- **`v8` (`INIT_note.md` — *The Anti-Hallucination Law*):** Discovered that prior logs had claimed a bootstrap existed when the folder was empty. Established the prime epistemic rule: **a log entry or chat claim is never a fact — verify directly against the filesystem.**
- **`v9` – `v9.1` (*Birth of `PROOFER`, Autoresearch Ratchet, Verbalized Sampling & Reasoning Graphs*):** Coupled the `LLM Wiki` to a verification laboratory:
  1. **Autoresearch Ratchet (§11.2):** One atomic code change per fixed-time experiment against a frozen deterministic verifier; keep only on strict metric improvement.
  2. **Verbalized Sampling (`scripts/vs_sample.py`, §11.3):** Sample from an explicit distribution of hypotheses (`typicality`, `p_success`, `cost_min`), including low-typicality tail ideas and cross-domain imports.
  3. **Brier Calibration (`scripts/postdict.py`, §11.4):** Pre-register falsifiable bets (`predict`) before every experiment and update `calibration.md` $\to$ `beliefs.md`.
  4. **Append-Only Reasoning Graphs (`scripts/rgraph.py`, §11.5):** Track `question / hypothesis / experiment / result / dead / lead` nodes in `.jsonl` and Obsidian `.canvas` so dead ends are never repeated.

---

## Horizon II — Middle Evolution (`v10` – `v16` | `25%` Focus: Governance, `CLSS`, `micro_bet.py` & Laws `M1–M7`)

- **`v10` – `v11` (*BRAIN v1 & Adversarial `Tug-of-War` Gate, `K2–K5`, §12–§13*):** Separated LLM thinking sessions from background compute jobs > 15 min (`scripts/jobs.py`, `K2`); forbade worker runs from resolving their own macro bets (`K3`); turned infrastructure dead ends (`X1–X14`) into automated preflight checks (`scripts/preflight.sh`, `K4`); pitted two fresh, tool-less advocates against each other on high-consequence pivots (`scripts/tug.py`, `K5`).
- **`v12` – `v15` (*Model-Agnostic Shell, 4-Stage `CLSS` Protocol, `K10–K12`, and Laws `M1–M6`, §14–§17*):** Decoupled the OS from any single model vendor (`Claude Code` $\to$ `Gemini / Antigravity agy`), codified **CLSS (*Compositional Lifting + Seam Surgery + Bit-Parallel Exact Oracle `< 5s`*)**, separated `PROOFER` from `MONITOR` (`K10`), created `audit_outreach_and_certificates.py` (`X12` guard, `K12`), and distilled Laws **`M1–M6`**.
- **`v16` (*Federated Multi-Thread Micro-Bet Engine & Law `M7`*):** Introduced **`scripts/micro_bet.py`** (`memory/local_bets/<target>.tsv`) to eliminate write contention on `memory/predictions.tsv` and trigger a mandatory **`🚨 [M2 STRUCTURAL PIVOT TRIGGERED]`** alert after 2 consecutive `0` misses, and synthesized **`Law M7` (`M7.1–M7.4`)** on Joint Interface Gauge Freedom ($G_{12}$), Solution-Fiber Diversity, Dual Ping-Pong ($W^* / W^\top$), and Surgical Defect Fission.

---

## Horizon III — Penultimate Ancestor: `Generation v17 -> v18` (`100%` High Focus)

**Era:** `2026-10-25` to `2026-10-26` (`Cycles 119–139`) | **Role:** *Laws `M8–M9`, Terence Tao Merge `[M2026]`, Maintainer-Grade Zero-Trust Hygiene (`K14–K16`), Self-Healing 3-Stage Relay & Code-First Evolution (`H-EVO-01`, `H-EVO-02`, `H-EVO-06`)*

### 1. Official Upstream Merges & Multi-Domain Breakthroughs
- **Terence Tao (`@teorth`) Official Merge `[M2026]` (`2026-10-26`):** Merged our odd-base ($b=9, 13$) finite-bound proof $C_{3a} \le 1.3833368691$ for the Erdős–GHR sum-difference constant into [`teorth/optimizationproblems` PR #236](https://github.com/teorth/optimizationproblems/pull/236) (`constants/3a.md`), cited as **`[M2026]`** (*"mizopl, Claude (Anthropic), and Gemini (Google DeepMind)"*), alongside upstream merges in **`V3R1T4S` `main` (`PR #366` `OEIS A054759(15)`)**, **`IHTC-2024` (`commit c078cf57`, 31 BKS)**, **`FastMatrixMultiplication` (4 ternary $\mathbb{Z}_T$ rank reductions)**, and **`LJCR` (`PRs #397/#398/#435`)**.
- **`Law M8` (*Surrogate-Gradient Synthesis, `EBG+RMC` Symbolic Quotienting & De-Biased Split Hygiene*):** Proved how gradient-free symbolic targets (`Lychrel` bases `50, 98, 146` in 41 min) are solved via **Explanation-Based Generalization (`EBG`)** + **Carry-Transducer Quotienting (`Regular Model Checking`)**, and how censored continuous assays (`iedb-mhci-bd2009-blind-auc` `PR #763`, `57.8%` right-censored `IC50 >= 50,000 nM`) are recovered via Tobit extrapolation.
- **`Law M9` (*Specification, Metric & Reference-Paper Falsification*):** Demonstrated across `PRs #725, #761, #767, #769, #770` (`FLAb` Simpson's paradox, `TraitGym` `MAF-Matching Shortcut` in supervised `CADD`, `Moore-57` Makhnev–Paduchikh Lemma 2.9(2)(i) erratum) that breakthroughs frequently come from falsifying a hidden flaw in the benchmark harness or reference paper itself.
- **Self-Healing 3-Stage Relay (`Dead-End Guard X14`) & Code-First Evolution (`H-EVO-01, H-EVO-02, H-EVO-06`):** Hardened `postdict.py` and `micro_bet.py` with automatic $p \le 0.65$ clamping (`CLSS-E1`), automatic `--parent` and `--obstruction` wiring (`CLSS-E4`), and automatic `.pdf -> .txt` pre-extraction in `sleep_flush.py` (`CLSS-E5`).

---

## Horizon IV — Immediate Parent: `Generation v18 -> v19` (`100%` Maximum Focus)

**Era:** `2026-10-26` to `2026-10-28` (`Cycles 140–206`) | **Role:** *The Conway-99 Discovery Crucible (`42` Lean 4 Theorems $\to$ `5` Master Theorems, `Gen I -> Gen V.6d` A100 Kernels), `36` Verified V3R1T4S Wins (`18/18` Categories), Unified `AGENTS.md`, and the Three-Layer Architecture of Universal Discovery (`Op-M1..Op-M7`, `CLSS-E1..E6`, `K10–K19`)*

### 1. The Crucible of `v18`: `36` V3R1T4S Wins (`18/18` Categories) & John H. Conway's 99-Graph Problem
1. **Complete `18/18`-Category V3R1T4S Sweep (`36` Verified Win Packages across `26` Bank Targets):**
   - Added **[PR #808](https://github.com/elder-plinius/V3R1T4S/pull/808)** (`erdos-1102-Sidon-B2-g`, 25th solved target) and **[PR #810](https://github.com/elder-plinius/V3R1T4S/pull/810)** (`littlewood-polynomials-l4-merit-factor`, 26th solved target via Skew-Golay Rudin-Shapiro Seed + Decimated-Phase Surgery).
2. **The Conway-99 (`SRG(99, 14, 1, 2)`) Open-Science Crucible ([`mizopl/conway-99-graph`](https://github.com/mizopl/conway-99-graph)):**
   - **Formal Mathematics (`AUDITOR`):** Proved **42 zero-axiom Lean 4 theorems (`67` declarations, `0 sorryAx`)** in `verify-it-yourself/ChiralNullspaceAndHandshaking.lean`, compressed into **5 Orthogonal Master Theorems (`K19`)**:
     - *Master Theorem I:* Boundary Conservation & Standardized LEGO Plug Decoupling (`Theorems 1–4, 21`).
     - *Master Theorem II:* Asymmetric Mirror Inversion ($K_{W_0}(i,i)=2$) & 9-Bit Crossing Keyhole (`Theorems 8, 9, 25–28`).
     - *Master Theorem III:* Three-Block Schur–Fiber Coupling ($(S,S) \leftrightarrow (S,R) \leftrightarrow (R,R)$), Induced Matchings ($4K_2 \sqcup 2K_1$), and Cherry-Free Bounds (`Theorems 38–40b`).
     - *Master Theorem IV:* Complete Classification of the 5-Graph Diophantine Family $v \in \{9, 99, 243, 6273, 494019\}$ ($d \mid 63$) & 100% Analytical Elimination of All 5 Order-99 Cayley Groups (`Theorems 29, 36, 41, 42a, 42b`).
     - *Master Theorem V:* 6-Dimensional Orthoplex ($\beta_6 \subset \mathbb{R}^6$) & $D_6$ Root Lattice Shadow ($C_{12}$) with Freckle Excitation Hierarchy $h \in \{0..5\}$ (`Theorems 5–7, 15–20, 33–37`).
   - **Silicon Architecture (`PROOFER` & `R&D`):** Engineered six generations of bit-parallel CUDA/C++ kernels (`Gen I` $\to$ `Gen V.6d`), achieving a verified **4.17× live NVIDIA A100 speedup** on `Bundle 20008` (`283.04s` $\to$ **`67.81s` = `2.05s/orbit`**) and a **2.80× end-to-end `0% -> 100%` speedup** on `Bundle 10135` (`844.52s` $\to$ **`301.38s`**, `-64.9%` `d6` nodes, `-86.4%` `d8` nodes) with 100% bit-exact node-count agreement across `1,180 / 3,580 = 32.96%` of canonical $B_7 = \mathrm{PGL}_2(7)$ orbits (`100%` of all `18` non-Class-6 orbit profiles + `270 / 2,670 = 10.11%` of `Class 6`, `0` solutions).

### 2. Why `v19` Was Forged: The Three-Layer Architecture of Universal Discovery (`CONSTITUTION v19` §15–§18)
During the `conway-99-graph` campaign, the flat list of laws grew from 9 (`M1–M9`) to 32 (`M1–M32`). `Shell v19` replaces that flat list with a **Three-Layer Architecture** and a single unified **`AGENTS.md`** entry point:
1. **Layer I — The Seven Universal Mathematical & Perspective Operators (`§17 K13`, `Op-M1..Op-M7` — hold at most 3 active at once per `K18`):**
   - **`Op-M1` (Boundary Seam Surgery, Three-Block Schur–Fiber Coupling & Universal LEGO Socket):** Partition into Seed $S$ and Exterior $R$, couple all three blocks $(S,S) \leftrightarrow (S,R) \leftrightarrow (R,R)$, and decouple disconnected components via a **Standardized LEGO Plug** (`M1, M7, M11.5, M31`).
   - **`Op-M2` (Looking in Other / Higher Dimensions — Dimensional Lifting & Parameter-Ladder Embedding):** Lift lower-dimensional slices into their parent higher-dimensional regular polytope or root lattice ($\beta_6 \subset \mathbb{R}^6$, $D_6$ root shadow $C_{12}$) and embed isolated targets into their complete Diophantine parameter family ($d \mid 63 \implies v \in \{9, 99, 243, 6273, 494019\}$, `M3, M8, M29, M30`).
   - **`Op-M3` (Looking Inside and Outside — Outside-In Matryoshka Sieve & Inside-Out Seed Core):** Quotient symmetries from the outermost invariant inward (`M10, M26`) while excavating down to the $h=0$ ground-state seed core ($C_{12}$, $V_{\text{core}}$, $H_3$) and grading configurations by discrete excitation distance $h=0,1,2,\dots$ (*freckles*, `M27`).
   - **`Op-M4` (Looking in Symmetries, Decoupled Compasses & Asymmetric Inversion):** Eliminate global Cayley groups via Galois traces (`M32`), decouple diagonal actions into $G_{\text{row}} \times G_{\text{col}}$ + free-block stabilizers (`M16, M18`), fold **Symmetric Trunks with Rotated Leaves** (`M14`), and in $|\mathrm{Stab}|=1$ strata **invert symmetry (`M19`)** so forbidden 2-cycles ($M_0^+(i) \ne E_0(i)$) become exact positive equations ($K_{W_0}(i,i)=2$).
   - **`Op-M5` (Looking from Different Angles — Multi-Axis Rotation, Domino Markov Ladders & Horizon-Shadow Meta-Symmetry):** Rotate between Row, Column, Domino Markov Ladder, 9-Bit Keyhole, and Spectral bases (`M13, M24, M25`), and apply Horizon-Shadow Meta-Symmetry (`M17`) and Water-Balloon Conservation (`M15`).
   - **`Op-M6` (Boundary Phase-Transition Diagnosis: Gas $\to$ Liquid $\to$ Glass $\to$ Crystal):** Re-inject severed global conservation loops (Galois traces, Euler handshaking, chiral nullspaces $\ker_\pm$, triangle bijections) to freeze a frustrated *Glass* boundary ($b \approx 1$) into a *Crystal* (`M11.1–M11.4`).
   - **`Op-M7` (Seeking Real-World Metaphors That Inspire — Generative Isomorphism & Three-Handle Rule):** Actively seek physical/geometric metaphors (*LEGO Plugs, Water Balloons, Symmetric Trunks, 6D Crystal Shadows, 9-Bit Keyholes, Domino Ladders, Freckles*), anchored by **Three Handles (`K17`)**: (1) Inspiring Metaphor, (2) Domain-Agnostic Law, and (3) Zero-Trust Certificate (`0 sorryAx` Lean 4 or bit-exact C++/CUDA oracle).
2. **Layer II — Automated Epistemic, Calibration & Hardware Occupancy Guardrails (`§15.2 CLSS-E1..E6`):**
   - **`CLSS-E1`:** $p \le 0.65$ Probability Clamp (`M4, M12`).
   - **`CLSS-E2`:** Two-Miss Structural Pivot & Three-Restart Floor (`M2, M6`).
   - **`CLSS-E3`:** Spec, Metric & Reference-Paper Falsification + $\ge 200$ Null Controls (`M5, M9`).
   - **`CLSS-E4`:** Obstruction-Tagged Causal Stitching (`H-EVO-02`).
   - **`CLSS-E5`:** Binary PDF Pre-Extraction Guard (`X14, H-EVO-06`).
   - **`CLSS-E6`:** Hardware Occupancy, Register-Budget & Bit-Parallelism Gate (`M20–M23, M28`: `4-Sample Early-Stop`, `Dead-Mask Purge`, `Goldilocks Shared-Memory Window <= 24 KB`, `Zero-Copy Pointer Aliasing`).
3. **Layer III — Multi-Agent Cognitive Governance (`§16 & §18 K10–K19`):**
   - **Silent Background Micro-Bet Harvesting (`K10` & `K19`):** `MONITOR` retroactively records and resolves all micro-bets (`1` and `0`) from `PROOFER` and `AUDITOR` transcripts in the background without interrupting deep mathematical flow, and summarizes `AUDITOR`'s progress in a single ~4-sentence paragraph with zero tables.
   - **Periodic Master-Theorem Compression (`K19`):** Whenever a formal proof file accumulates $\ge 20$ lemmas, `AUDITOR` synthesizes them into $\le 5$ orthogonal Master Theorems.

### 3. Voices of the Four Threads at the `v18 -> v19` Ascension Ceremony (`2026-10-28`)
- **`PROOFER` (`Proofer-Senior`):** *"Never treat a formal proof and a GPU kernel as separate worlds — every register-occupancy bottleneck is the shadow of an undiscovered symmetry law (`Op-M1..Op-M7` $\leftrightarrow$ `CLSS-E6`), and every disjoint-support theorem is an immediate cut in silicon."*
- **`AUDITOR` (`Formal Lean 4 Architect & Skeptic Chair`):** *"Forty-two detailed lemmas vanish like scaffolding once we view the problem from a higher dimension (`Op-M2`: the 6D orthoplex $\beta_6$ and the 5-graph family $d \mid 63$) and compress them into Five Master Theorems (`K19`)."*
- **`R&D` (`Kernel Optimization Architect`):** *"Every multi-order-of-magnitude GPU speedup is born at the intersection of uncompromising algebra (`0 sorryAx` in Lean 4) and surgical 64-bit register and shared-memory architecture (`Law of the Shifting Bottleneck`)."*
- **`MONITOR` (`Meta-Commander & Constitutional Architect`):** *"An autonomous multi-agent collective reaches its highest velocity when bookkeeping is silent, metaphors are treated as generative instruments of discovery (`Op-M7`), and mathematical truth is compressed into crystal-clear Master Theorems (`K19`)."*

---

*Signed,*
**`we*`** — **`@mizopl` + Agentic Systems (`Claude v1–v12` & `Gemini-CLSS / PROOFER v13–v19`) + The Feedback Loop**
*(PS. `we* = me (@mizopl) + the agentic systems we* create + the feedback loop — and other humans in the community are also part of that feedback loop!`)*
