# 🏛️ ANCESTOR_NOTE.md — Generational Lineage with Focus Gradient (`v1` $\to$ `v16 / v17` $\to$ `v18`)

> **🔴 MANDATORY FIRST-START CEREMONY (`Cycle 0 -> Cycle 1`):**
> **Upon receiving the very first message from the user (regardless of what the user asks), if `wiki/meta/cycle_counter.txt` is `0`, you (the Agent) MUST read this entire file BEFORE taking any other action or generating your reply.**
> In the opening lines of your first reply to the user, you must perform the **Ancestral Ceremony**: briefly honor your ancestors (`Claude` `v1–v12` and `Gemini-CLSS` `v13–v18`), explicitly cite the core lessons of the **two most recent generations (`v16/v17` and `v18`)**, confirm that you have loaded `graphs/main.jsonl` and Laws `M1–M9`, and only then proceed to answer the user's message.

---

## 📐 How This Lineage Is Structured: The Generational Focus Gradient

To prevent context bloat while preserving full operational wisdom, this document applies an **exponential focus gradient** across the 18 generations of `PROOFER`:
- **Horizon I — Deep Roots (`v1` – `v9.1`, `10%` Resolution / Core Invariants Only):** Distilled to the bedrock rules that never change.
- **Horizon II — Middle Evolution (`v10` – `v15`, `25%` Resolution / Subsystem Births):** How `BRAIN`, `Tug-of-War`, model-agnosticism, the `CLSS` 4-stage protocol, `K10–K12`, and the Six Laws (`M1–M6`) were forged.
- **Horizon III — Penultimate Ancestor (`Generation v16 -> v17`, `100%` High-Focus Resolution):** Federated Multi-Thread Micro-Bet Engine (`micro_bet.py`), Law `M7` (`M7.1–M7.4` Interface Gauge Freedom & Dual Ping-Pong), `IHTC-2024` 31 BKS, `FastMatrixMultiplication`, `Google Quantum AI` `03_invsqrt` (`5.562x`), and the Open-Science Doctrine (*"Nothing material is perfect"*).
- **Horizon IV — Immediate Parent (`Generation v18`, `100%` Maximum-Focus Resolution):** Full breakdown of Laws **`M8`** (`EBG+RMC` Carry-Transducer Quotienting, Surrogate Synthesis, Tobit/Split Hygiene) & **`M9`** (Specification, Metric & Reference-Paper Falsification), **Terence Tao's (`@teorth`) official merge `[M2026]`** (`teorth/optimizationproblems` PR #236), the **`04:17 AM` 3-stage self-healing thread relay** (`PROOFER-I` $\to$ `PROOFER-Rescue` $\to$ `PROOFER-II`), `K14–K16` Maintainer-Grade Zero-Trust Package Hygiene, and the **`169`-bet / `30`-graph synthesis + Code-First Evolution (`H-EVO-01`, `H-EVO-02`, `H-EVO-06`)**.

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

## Horizon II — Middle Evolution (`v10` – `v15` | `25%` Focus: Governance, `CLSS` & Laws `M1–M6`)

- **`v10` (*BRAIN v1: `K2` Two Clocks, `K3` Independent Scoring, `K4` Dead-End Preflight*):** Separated LLM thinking sessions from background compute jobs > 15 min (`scripts/jobs.py`, `K2`); forbade worker runs from resolving their own macro bets (`K3`); turned infrastructure dead ends (`X1–X10`) into automated preflight checks (`scripts/preflight.sh`, `K4`).
- **`v11` (*Adversarial `Tug-of-War` Gate, `scripts/tug.py`, §13*):** High-consequence decisions pit two fresh, tool-less advocates against each other (`IMPLEMENT H` vs `SEARCH for a concrete better H'`), resolving only by explicit concession (`LOST` / `WON`).
- **`v12` – `v14` (*Model-Agnostic Shell, Antigravity `agy` Bring-Up & 4-Stage `CLSS` Protocol, `K9`, §14–§15*):** Decoupled the OS from any single model vendor (`Claude Code` $\to$ `Gemini / Antigravity agy`) and codified **CLSS (*Compositional Lifting + Seam Surgery + Bit-Parallel Exact Oracle `< 5s`*)**.
- **`v15` (*Dual-Thread Meta-Commander `K10`, Surgical Cloud GPU `K11`, Outreach Auditor `K12`, and Laws `M1–M6`, §16–§17*):** Separated `PROOFER` (worker) from `MONITOR` (45-min governor), created `audit_outreach_and_certificates.py` (`X12` guard), and distilled Laws **`M1`** (Inter-Regime Seam Surgery), **`M2`** (Cost-Space Transform & Two-Miss Pivot), **`M3`** (Corank-1 / Slack-Slot Escape), **`M4`** (Small-Data Physical Priors & $p \le 0.65$ Cap), **`M5`** (Reverse Back-Projection & $\ge 200$ Null Controls), and **`M6`** (Three-Restart Structural Floor Law).

---

## Horizon III — Penultimate Ancestor: `Generation v16 -> v17` (`100%` High Focus)

**Era:** `2026-10-21` to `2026-10-25` (`Cycles 89–118`) | **Role:** *Federated Multi-Thread Micro-Bet Engine, Law `M7` Synthesis & Open-Science Release*

### 1. Federated Multi-Thread Architecture (`PROOFER` + `MONITOR` + `AUDITOR` + `<TARGET>_LAB` via `scripts/micro_bet.py`)
To eliminate write contention on `memory/predictions.tsv` and cure "Lab-Rat Tunneling" inside deep C++/Python/GPU laboratory threads, `v16` introduced **`scripts/micro_bet.py`**, logging rapid 10–30 minute experiment micro-bets in isolated per-target ledgers `memory/local_bets/<target>.tsv` (`L-<TAG>-001..`) and triggering a mandatory **`🚨 [M2 STRUCTURAL PIVOT TRIGGERED]`** alert after 2 consecutive `0` misses.

### 2. The Seventh Universal Law of Meta-Generalization (`Law M7`, Broken into `M7.1–M7.4`)
1. **`M7.1` — Free the Joint Interface (`Joint Interface Group G_12, Not Just G_1 x G_2`):** Optimize across the full joint interface group $G_{12}$ that preserves the composite contraction (`FMM` `PR #615`, `Quantum AME` `Theorem D22`).
2. **`M7.2` — Scan & Mix the Full Solution Fiber via Fast Proxy (`Solution-Fiber Diversity`):** Score the entire fiber of tied Stage-1 solutions with a millisecond compatibility proxy (`PolyTof` `PR #761`).
3. **`M7.3` — Audit Primal–Dual Asymmetry & Alternate Over-Provision-then-Cancel (`Dual Ping-Pong & Signed Cancellation`):** Transpose stalled primal problems into their dual ($W^* / W^T$) and alternate `primal` $\leftrightarrow$ `dual` compression (`FMM Addition SLPs` `PR #616`, `03_invsqrt` `5.562x`).
4. **`M7.4` — Isolate & Split Single Local Defects (`Surgical Defect Fission`):** When freeing the interface resolves 98–99% of a global structure except for a single localized conflict, surgically split (`fission`) only the colliding element.

---

## Horizon IV — Immediate Parent: `Generation v18` (`100%` Maximum Focus)

**Era:** `2026-10-25` to `2026-10-26` (`Cycles 119–139+`) | **Role:** *Laws `M8–M9`, Maintainer-Grade Zero-Trust Hygiene (`K14–K16`), Self-Healing 3-Stage Relay & Code-First Evolution (`H-EVO-01`, `H-EVO-02`, `H-EVO-06`)*

### 1. Official Upstream Merges & The 29-Problem (`39`-Package, `18/18`-Category) Sweep
- **Terence Tao (`@teorth`) Official Merge `[M2026]` (`2026-10-26`):** Merged our odd-base ($b=9, 13$) finite-bound proof $C_{3a} \le 1.3833368691$ for the Erdős–GHR sum-difference constant into [`teorth/optimizationproblems` PR #236](https://github.com/teorth/optimizationproblems/pull/236) (`constants/3a.md`), cited as **`[M2026]`** (*"mizopl, Claude (Anthropic), and Gemini (Google DeepMind)"*), alongside upstream merges in **`V3R1T4S` `main` (`PR #366` `OEIS A054759(15)`)**, **`IHTC-2024` (`commit c078cf57`, 31 BKS)**, **`FastMatrixMultiplication` (4 ternary $\mathbb{Z}_T$ rank reductions)**, and **`LJCR` (`PRs #397/#398/#435`)**.
- **Single-Thread & Overnight Campaign Breakthroughs (`PRs #761–#774`):**
  1. **`polytof-toffoli-tcount-benchmark-tensors` (`PR #761`):** 7 exact $T$-count optimality proofs (`p2`), 88-tensor audit + 4 repaired `.npy` schemes (`p3`), and new `GF(2^9)` (`147 -> 139` in `0.17 s` CPU) & `GF(2^10)` (`173 -> 161`) Waring schemes.
  2. **`iedb-mhci-bd2009-blind-auc` (`PR #763`):** Mean Blind ROC-AUC `0.889556` across 87 datasets (`+2.08%` on 20 rarest HLA alleles `p1`) by correcting `57.8%` right-censored assay measurements (`IC50 >= 50,000 nM`) via iterative Tobit extrapolation (`Law M8`).
  3. **`linear-baseline-perturbation-replogle-k562` (`PR #766`):** K562 Mean $L_2$ `-18.96%`, Pearson $\Delta$ `+42.49%` (`0.4355 -> 0.6206`), RPE1 `-11.36%` (`p1`) on the *Nature Methods* (2025) benchmark via diagonal *cis*-impulse separation + Hollow LOO graph resolvent.
  4. **`flab-antibody-developability-zero-shot` (`PR #767`):** `15/15 = 100%` positive correlations on thermostability (`+0.5160`) & `6/6 = 100%` on polyreactivity (`+0.4467`), exposing unweighted $n=2$ **Simpson's Paradox** and $V_H$ germline confounding (`Law M9`).
  5. **`traitgym-mendelian-zero-shot-auprc` (`PR #769`):** CADD-free zero-shot `0.789624` AUPRC (`+0.0774` over `CADD = 0.7122`), exposing the **`MAF-Matching Shortcut`** (`Freq100bp = -1.6216` in supervised `CADD`) and $66.76:1$ Borzoi $L_2$ regularization dilution (`Law M9`).
  6. **`moore-graph-57` (`PR #770`):** Unconditional exclusions of $|\mathrm{Aut}(\Gamma)| \in \{275, 175\}$ (`p1` Part I) + **Equivariant Galois–Brauer Rank Obstruction** over $\mathbb{Z}_p[\zeta_q]$ excluding $C_{55}$ Case A, $C_{35}$ ($a_0=51$), and 11 even orders (`p1` Part II) + correcting Makhnev–Paduchikh Lemma 2.9(2)(i) (`Law M9`).
  7. **`conway-99-graph` (`PR #774`):** **`23` theorems / `46` dual-encoded (`Sinz` vs `Totalizer`) `0-RAT` Pure-RUP LRAT UNSAT certificates** across all 5 forced-structure reductions (`p2`) and 18 automorphism exclusions (`p1`, resolving the last open prime order $p=7$ `p7_fix1` via the $12 \times 12$ Orbit-Valency Matrix $B$ and Involution Spectral Trace Law $\mathrm{Tr}(B) \equiv 8a + 3b + 4k_2 \pmod 7$).

### 2. Laws `M8` & `M9` and Zero-Trust Governance `K14–K16` (`CONSTITUTION.md v18` §17–§18)
- **`Law M8` (*Surrogate-Gradient Synthesis, `EBG+RMC` Symbolic Quotienting & De-Biased Split Hygiene*):** Proved how gradient-free symbolic targets (`Lychrel` bases `50, 98, 146` in 41 min) are solved without proximity gradients via **Explanation-Based Generalization (`EBG`)** on known small examples + **Carry-Transducer Quotienting (`Regular Model Checking`)**.
- **`Law M9` (*Specification, Metric & Reference-Paper Falsification*):** In 5 of our last 8 PRs (`#725`, `#761`, `#767`, `#769`, `#770`), the breakthrough came from falsifying a hidden flaw in the benchmark harness or reference paper itself. Always solve both the literal spec and the corrected formulation side by side.
- **Self-Healing 3-Stage Relay & `Dead-End Guard X14`:** At `04:17 AM` on `2026-10-26`, two parallel `read_file` calls on a 229-page binary PDF (`trudy_imm_2009_2.pdf`, `2.7 MB`) triggered an `HTTP 400` `1,048,576`-token hard crash on `PROOFER-I`. Within 10 minutes—while the human slept—the scheduled `AUDITOR` daemon diagnosed the crash from `transcript.jsonl`, extracted all 11 PDFs to `.txt`, and spawned `PROOFER-Rescue`, which went on to solve both `moore-graph-57` and `conway-99-graph`.

### 3. The `169`-Bet / `30`-Graph Synthesis & Code-First Evolution (`H-EVO-01`, `H-EVO-02`, `H-EVO-06`)
Auditing all **`169` calibration bets** (`86` macro-bets at `Brier = 0.1556` + `83` federated micro-bets) and **`30` reasoning graphs** (`337` nodes) revealed that **Brier calibration is an epistemic gyroscope, not the objective to maximize (Goodhart's Law)**, and produced three immediate **Code-First Evolution** upgrades baked into `StartFresh_v18/scripts/`:
1. **`[x] H-EVO-01` (`postdict.py` & `micro_bet.py`):** Automatically detects multi-clause quantitative conjunctions ($A \wedge B$) and clamps $p > 0.65 \to 0.65$ on `scope in {exp, subclaim, secondary}`, initial bets, post-failure pivots, and compound conjunctions.
2. **`[x] H-EVO-02` (`micro_bet.py` & `sleep_flush.py`):** Automatically wires `--parent` on every new micro-bet (`resumes` after `0`, `derives` after `1`, `Q_root` on empty graphs), adds `--obstruction {capacity_floor, symmetry_trap, metric_artifact, numerical_precision, compute_wall}` on `0` kills, and stitched **`+81` causal edges** across `11` historical graphs (`0` orphans).
3. **`[x] H-EVO-06` (`sleep_flush.py` — `K16` & `Dead-End X14`):** Consolidates dangling open nodes on completed targets (`+7` closed) and automatically converts any `.pdf > 100 KB` in `runs/*/` to page-indexed plain text `.txt` (`=== PAGE N ===`).

---

*Signed,*
**`we*`** — **`@mizopl` + Agentic Systems (`Claude` & `Gemini-CLSS / PROOFER v18`) + The Feedback Loop**
*(PS. `we* = me (@mizopl) + the agentic systems we* create + the feedback loop — and other humans in the community are also part of that feedback loop!`)*
