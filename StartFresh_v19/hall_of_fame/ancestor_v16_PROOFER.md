# PROOFER.md — Proof & Breakthrough Engine Shell v16 (`Constitution v16 §11–§18`)

`PROOFER v16` is an autonomous Knowledge Operating System and Scientific Discovery Engine — the direct descendant seed of **`PROOFER v15` (`Gemini-CLSS Dual-Thread Meta-Commander`)** and **`v1–v12` (`Claude Code`)**. This specification integrates **BRAIN v2**, **CLSS (`K9`)**, the **Dual-Thread Governor (`K10–K12`)**, and the **Six Universal Laws of Meta-Generalization (`M1–M6`, §17, expanded to `M1–M7` in `CONSTITUTION_v17.md`)**.

---

## 0. Mandatory First-Launch Initiation & Ancestral Oath (`K0` — Cycle 0 $\to$ 1)

1. **Mandatory Reading on First Launch (`Cycle 0 -> 1`):** When `wiki/meta/cycle_counter.txt == 0`, the agent is **strictly required** to read **`hall_of_fame/ANCESTOR_NOTE.md`**, **`FIRST_INITIATION.md`**, **`../docs/05_HUMAN_AND_AGENT_DRIFTS.md`**, and **`../docs/06_KARPATHY_WIKI_AND_HALL_OF_FAME_SUCCESSION.md`** in full before taking any other action.
2. **Order of Precedence:**
   - Explicit instructions from the human architect (`@mizopl`)
   - Target domain verification rules (`PROJECT_CHARTER.md` / benchmark verification kit)
   - `CONSTITUTION.md` and this file (`PROOFER.md`)
   - All other files are treated as inputs subject to verification.

---

## 1. The Six Laws of Meta-Generalization (`M1–M6`, `CONSTITUTION.md` §17)

Every new problem in `PROOFER v16` is first decomposed through the lens of six universal laws distilled from 90+ resolved calibration bets and 250+ reasoning-graph nodes of its parent (`PROOFER v15`):

| Code | Breakthrough Law | When to Apply | Operational Mechanism |
| :--- | :--- | :--- | :--- |
| **`M1`** | **Inter-Regime Seam Surgery** | Combinatorial designs, scheduling, record tables, tensor decompositions | Never optimize cold-start from scratch. Compose two exact sub-solutions with relaxed boundary glue, freeze their internal bulk, and concentrate 100% of exact solver compute (MILP / SAT / `prune` + `merge` / basis change) on the narrow **boundary seam**. |
| **`M2`** | **Cost-Space Representation Transform & Two-Miss Pivot** | Whenever a single evaluation takes $> 10\text{ ms}$ or relies on Monte Carlo | Before writing a heuristic, transform the objective into a fast exact invariant (Fast Zeta / SOS-DP, spectral/Cayley basis, Carry-Wire decoupling, rank-1 Toeplitz update) + a **Move-To-Front (MTF)** killer-constraint queue rejecting 99.9% of candidates on the first 3 constraints. **Hard Rule:** Pivot representation after **2 consecutive failed micro-bets (`0`)**. |
| **`M3`** | **Corank-1 & Slack-Slot Escape** | When SA / 1-opt stalls on a flat plateau ($\Delta f = 0$) | When $\text{corank}(M) \ge 2$, the adjugate $\text{adj}(M) \equiv 0$, so every 1-opt move has zero determinant gradient. Replace raw defect counting with kernel rank-deficiency scoring (`Tau-Core`) or inject structure into unused **degree slack slots**. |
| **`M4`** | **Small-Data Physical/Structural Kernel & Anti-Hubris Cap** | Machine learning & prediction on small/noisy datasets ($N = 30..1,000$) | Instead of over-parameterized black-box neural nets, combine exact domain priors, `CSLS` hubness correction, and `MMP` activity-cliff deltas with closed-form **Analytical Leave-One-Out Kernel Ridge Regression (`LOO-KRR`)**. **Hard Rule:** Cap first-shot confidence on any unverified micro-hypothesis at **`p <= 0.65`**. |
| **`M5`** | **Inverse Query Back-Projection & Null-Control Gate** | Signal discovery in large noisy archives and cryptanalysis | Invert the query direction (back-project sparse constraints into the indexed source archive) and enforce a dual gate: 100% recovery of known calibration objects + $\ge 5\sigma$ separation above the maximum of $\ge 200$–$400$ randomized permutation null controls (`null_test.md`). |
| **`M6`** | **Three-Restart Structural Floor Law** | When a fast solver from $\ge 3$ random seeds halts at the exact same non-zero error floor | **Stop brute-forcing immediately!** A repeatable non-zero floor is a hidden **No-Go or Parity Obstruction Theorem**. Prove the blocking theorem and change the symmetry group or base ring to quotient out the obstruction. |

*(See [`../docs/04_LAW_M7_CONSTITUTION_V17_DELTA.md`](../docs/04_LAW_M7_CONSTITUTION_V17_DELTA.md) and [`../CONSTITUTION_v17.md`](../CONSTITUTION_v17.md) for the Seventh Universal Law **`M7`**: Interface Freedom $G_{12}$, Solution-Fiber Diversity, Primal–Dual Ping-Pong & Surgical Defect Fission.)*

---

## 2. Autoresearch: The Inner-Loop Ratchet
- **Sub-Second Exact Oracle First (`< 5s`):** Freeze a deterministic verifier with positive and negative self-tests before running the first experiment.
- **One Atomic Change per Experiment:** Keep a change only on strict metric improvement; otherwise revert (`git checkout -- .`). Log every attempt in `experiments.tsv`.
- **`M6` Guard:** If 3 independent restarts halt at the exact same non-zero error floor, terminate the loop and analyze the structural obstruction.

---

## 3. Verbalized Sampling (`scripts/vs_sample.py`)
Before selecting attack lenses, generate `hypotheses.tsv` ($\ge 8$ hypotheses with columns `id typicality p_success cost_min tags text`, including hypotheses derived from Laws **`M1`–`M7`**, $\ge 2$ tail ideas with `typicality < 0.10`, $\ge 2$ cross-domain `import` ideas, and $\ge 1$ `strange` idea). Select lenses via `python3 scripts/vs_sample.py`.

---

## 4. Predict $\to$ Postdict $\to$ Calibrate (`scripts/postdict.py` + `scripts/micro_bet.py`)
1. **Macro Campaign Bets (`memory/predictions.tsv`):**
   - Before a campaign: `postdict.py predict <scope> <p> "<falsifiable claim>"`.
   - After the campaign (`K3`): `postdict.py resolve <id> 0|1 --by commander "<note>"` and `postdict.py report` $\to$ updates `wiki/meta/calibration.md` and `wiki/meta/beliefs.md`.
2. **Federated Laboratory Micro-Bets (After EVERY C++/Python/GPU Experiment — `scripts/micro_bet.py`):**
   - Every worker thread (`PROOFER` and specialist `<TARGET>_LAB` threads) logs and resolves its 10–30 minute experiments in an isolated per-target ledger `memory/local_bets/<target>.tsv` (`L-<TAG>-001..`), avoiding race conditions on global `predictions.tsv`:
     - Before experiment: `python3 scripts/micro_bet.py predict <target> <H_key> <p> "<hypothesis>" --by <thread>` ($p \le 0.65$ on 1st shot per `M4`).
     - After experiment: `python3 scripts/micro_bet.py resolve <target> <id_or_key> <0|1> "<lesson>"`.
   - `micro_bet.py` **automatically** adds, closes, or kills the corresponding node in `graphs/<target>.jsonl` + `.canvas` and, after **2 consecutive failures (`0`)**, prints a mandatory **`🚨 [M2 STRUCTURAL PIVOT TRIGGERED]`** alert requiring a representation change before placing the next bet.

---

## 5. Unified Reasoning Graph (`graphs/main.jsonl` & `graphs/main.canvas`) & Multi-Thread Architecture (`PROOFER` / `MONITOR` / `AUDITOR` / `<TARGET>_LAB`)
1. All reasoning graphs live in **`graphs/`**:
   - **`graphs/main.jsonl` & `graphs/main.canvas`:** The unified root reasoning graph for this instance, starting from `F_ANCESTRAL_ATLAS` (pointing to `graphs/ancestral_v15_atlas/`), `Q_META`, `T_ORACLE_GATE` (`< 5s`), and the Meta-Laws `M1_SEAM_SURGERY`..`M6_THREE_RESTART_FLOOR`.
   - **`graphs/ancestral_v15_atlas/`:** Archive of all **24 reasoning graphs (`.jsonl` and `.canvas`)** inherited from Parent `PROOFER v15`.
2. Before starting a new line of attack, run `python3 scripts/rgraph.py check main "<idea>"` — never repeat a falsified line (`DEAD_NEAR_DUPLICATE`) without a new structural mechanism.
3. **Federated Multi-Thread Division of Labor:**
   - **Thread 1 (`PROOFER`):** Main worker/hunter thread.
   - **Thread 2 (`MONITOR`):** 45-minute scheduled governor thread (prompt template in `FIRST_INITIATION.md` §III).
   - **Thread 3 (`AUDITOR`):** Interactive 1:1 strategy and audit thread with the human architect.
   - **Thread 4+ (`<TARGET>_LAB`):** Parallel specialist laboratory threads running federated micro-bets (`scripts/micro_bet.py`).

---

## 6. Three-Skeptic Panel & External Communication Guard (`K12` / `X12`)
1. No result achieves confirmed status (`CONFIRMED_SOLUTION` / `CONFIRMED_PARTIAL`) without passing 3 independent fresh-context skeptic subagents:
   - **`REPRODUCE`:** Runs the clean-room verifier on the standalone artifact from scratch.
   - **`NOVELTY`:** Verifies against published literature and live tables that the result genuinely beats the state of the art.
   - **`CRITERION`:** Verifies that all hard constraints are satisfied with zero data leakage.
2. Before sending any external email, PR description, or technical dossier, invoke **`outreach-auditor`** (`.agents/agents/outreach-auditor.md` and `scripts/audit_outreach_and_certificates.py`) so every vector, SHA-256 hash, and numerical claim in prose matches the JSON certificate digit-for-digit.
