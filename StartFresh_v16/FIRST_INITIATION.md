# 🚀 FIRST INITIATION PROTOCOL — `PROOFER v16` (`Descendant of PROOFER v15`)

Welcome to **`PROOFER v16`** — a clean, self-contained, autonomous scientific discovery, optimization, and knowledge-compilation operating system.

---

## 🏛️ MANDATORY STEP 0 FOR THE AGENT (BEFORE ANY OTHER ACTION)

> **[!IMPORTANT] ANCESTRAL OATH, KARPATHY WIKI & HUMAN-AGENT DRIFT AWARENESS (`CONSTITUTION.md` §0 & §7.6):**
> If `wiki/meta/cycle_counter.txt` is `0` (First Launch), **you (the Agent) are strictly required to read [`hall_of_fame/ANCESTOR_NOTE.md`](./hall_of_fame/ANCESTOR_NOTE.md), [`../docs/05_HUMAN_AND_AGENT_DRIFTS.md`](../docs/05_HUMAN_AND_AGENT_DRIFTS.md), and [`../docs/06_KARPATHY_WIKI_AND_HALL_OF_FAME_SUCCESSION.md`](../docs/06_KARPATHY_WIKI_AND_HALL_OF_FAME_SUCCESSION.md) in full BEFORE taking any action or replying to the user.**
> In your very first response to the human commander, briefly honor your Parent (`PROOFER v15` / `v16`), acknowledge that you understand both Human Drifts and Agent Drifts (`Nothing is perfect until it is to the Highest`), and confirm that you have loaded the unified root graph **[`graphs/main.jsonl`](./graphs/main.jsonl)** (which connects the Ancestral Atlas `graphs/ancestral_v15_atlas/`, the Sub-Second Exact Oracle Gate `T_ORACLE_GATE`, and the Laws of Meta-Generalization `M1–M7`).

---

## 🧵 MULTI-THREAD WORKFLOW (`PROOFER` + `MONITOR` + `AUDITOR`)

This operating system is designed to run across **3+ specialized conversation threads** inside your IDE window:

1. **Thread 1 — `PROOFER` (Main Worker / Hunter Thread):**
   - **Name this initial chat thread `PROOFER`.**
   - This is where you run the **First Initiation** below and where the agent executes deep research cycles, builds C/Python/GPU solvers, runs the autoresearch ratchet, and produces verified certificates.
2. **Thread 2 — `MONITOR` (Autonomous Meta-Commander / 45-Min Governor Thread):**
   - **Right after First Initiation completes (Cycle 1), open a second chat thread, name it `MONITOR`, and paste the Monitor Prompt (Section III below).**
   - `MONITOR` runs on a recurring 45-minute `schedule`, independently resolves settled calibration bets (`K3`), checks active jobs, enforces the Three-Restart Structural Floor Law (`M6`), and keeps `graphs/main.jsonl` & `graphs/main.canvas` clean without interrupting `PROOFER`.
3. **Thread 3 — `AUDITOR` (Interactive 1:1 Strategy & Audit Thread):**
   - **At any time, you can open a new chat thread and name it `AUDITOR` to talk 1:1 with the agent** — to inspect system processes, review open hypotheses, brainstorm meta-strategy, or audit external emails/PRs (`K12`) in real time while `PROOFER` and `MONITOR` keep working in parallel!
4. **Thread 4+ — `<TARGET>_LAB` (Federated Specialist / Moonshot Lab Threads, powered by `scripts/micro_bet.py`):**
   - Whenever a hard sub-problem or Moonshot requires deep, uninterrupted C++/Python/GPU laboratory iteration, open a dedicated thread (e.g. `LAB_1`, `SOLVER_LAB`) using the **Specialist Lab Thread Prompt (Section IV below)**.
   - Every worker thread (`PROOFER` and `<TARGET>_LAB`) uses **`scripts/micro_bet.py`** (`memory/local_bets/<target>.tsv`, IDs `L-<TAG>-001..`) to place and resolve a micro-bet **after every single experiment** without colliding on global `memory/predictions.tsv` (`P00xx`). `micro_bet.py` automatically updates `graphs/<target>.jsonl` + `.canvas` and triggers a mandatory **`🚨 [M2 STRUCTURAL PIVOT]`** after 2 consecutive failed micro-bets (`0`) so no thread ever tunnels blindly on a dead ansatz! (See Parent v15's live examples in `memory/local_bets/ancestral_v15/`).

---

## 👤 I. HOW TO LAUNCH THIS INSTANCE IN A NEW PROJECT (`PROOFER` THREAD)

1. **Copy this directory** to your new workspace:
   ```bash
   cp -R ~/Desktop/PROOFER/PROOFER_SEED_v16 ~/Desktop/MY_NEW_PROJECT
   ```
2. **Drop any raw problem files, papers, datasets, or code** into `~/Desktop/MY_NEW_PROJECT/.raw/` (`.raw/` is immutable).
3. **Open `~/Desktop/MY_NEW_PROJECT`** in your IDE, **name your first chat thread `PROOFER`**, and paste the **First Initiation Prompt** below.
4. **Enter into an Attentive Dialogue (The Mindful Teacher Stance):** After launching the threads, stay in active, attentive dialogue with the system — collaborating like a **mindful teacher** who observes where the agent tunnels, asks frame-breaking questions, and guides the search toward genuine structural breakthroughs:

### 📋 Ready-to-Paste First Initiation Prompt (for Thread 1: `PROOFER`)

```text
PROOFER — FIRST INITIATION (v16):
1. Read `hall_of_fame/ANCESTOR_NOTE.md`, `CONSTITUTION.md` (v16, Laws M1–M6 in §17, plus Law M7 in `../docs/04_LAW_M7_CONSTITUTION_V17_DELTA.md`), `../docs/05_HUMAN_AND_AGENT_DRIFTS.md`, `../docs/06_KARPATHY_WIKI_AND_HALL_OF_FAME_SUCCESSION.md`, `wiki/meta/hot.md`, and inspect the unified root graph `graphs/main.jsonl`.
2. Our new target domain and primary objective is: [DESCRIBE NEW PROBLEM / DOMAIN / GOAL HERE].
3. Raw input data / source files are located in: [`.raw/` or path / URL].
4. Our success criterion (what counts as a breakthrough / win) is: [E.G., BEAT SCORE X / PROVE THEOREM Y / ACHIEVE ERROR < Z].
Execute the full FIRST_INITIATION.md protocol (Steps 0–5): create `wiki/entities/PROJECT_CHARTER.md`, build a deterministic sub-second verifier (Exact Oracle < 5s) and wire it along with hypotheses M1–M7 into `graphs/main.jsonl` (`graphs/main.canvas`), log the first macro bet `P0001` in `predictions.tsv` and first micro-bet in `micro_bet.py`, start Cycle 1, and at the end remind me to name this thread `PROOFER`, launch the `MONITOR` thread (print the ready-to-paste Monitor prompt), and optionally open `AUDITOR` or `<TARGET>_LAB` threads!
```

---

## ⚙️ II. THE 5-STEP FIRST INITIATION CHECKLIST (EXECUTED BY THE AGENT ON CYCLE 1)

When the human provides the new domain and goal, execute these 5 steps in order:

### Step 0: Ancestral Reading & Environment Preflight
1. Read `hall_of_fame/ANCESTOR_NOTE.md`, `CONSTITUTION.md` (v16), `PROOFER.md` (v16), and `wiki/meta/hot.md`.
2. Verify `/opt/homebrew/bin/python3 --version` (`X9`: never use `/usr/bin/python3`).
3. Inspect `.raw/` and run `/opt/homebrew/bin/python3 scripts/rgraph.py show main` to inspect the root Meta + Oracle graph (`graphs/main.jsonl`, which links directly to `graphs/ancestral_v15_atlas/`).

### Step 1: Create the Domain & Objective Charter (`wiki/entities/PROJECT_CHARTER.md`)
Write `wiki/entities/PROJECT_CHARTER.md` (satisfying `SCHEMA.md` frontmatter) with:
- **Mission & Target ID (`<target-id>`):** Clear identifier for the primary problem.
- **Baseline / Record to Beat:** Exact numerical metric, theorem statement, or benchmark threshold currently held by the state of the art.
- **Hard Rules & Constraints:** Memory/compute limits, zero-leakage train/test splits, or formal validity conditions.
- **Partial vs Full Win Definitions (`p1`, `p2`, `CONFIRMED_SOLUTION`).**

### Step 2: Build Stage I of CLSS — The Sub-Second Exact Oracle (`K9` / Node `T_ORACLE_GATE` in `graphs/main.jsonl`)
Before running any search or training any model:
- Write a standalone, deterministic verification script (`scripts/verify_oracle.py` or compiled C verifier) that checks whether any candidate solution is 100% valid and computes its exact score in $< 5$ seconds.
- Include **1 positive test** (reproducing the known baseline) and **1 negative test** (proving a corrupted/shuffled candidate is rejected).

### Step 3: Extend the Unified Reasoning Graph (`graphs/main.jsonl` & `graphs/main.canvas`)
All reasoning in this instance lives in **`graphs/`** (`graphs/main.jsonl` + `graphs/main.canvas`, with ancestral reference graphs in `graphs/ancestral_v15_atlas/`):
1. Link your new domain question `Q1` and your verified Oracle `E_ORACLE` directly under `T_ORACLE_GATE` and the Meta-Laws `M1_SEAM_SURGERY`..`M5_REVERSE_BACKPROJ_NULLS` inside `graphs/main.jsonl`:
   ```bash
   /opt/homebrew/bin/python3 scripts/rgraph.py add main question Q1 "<Primary domain question & target metric>" --parent T_ORACLE_GATE --rel derives --by commander
   ```
2. Add concrete domain hypotheses (`H_M1`..`H_M5`) derived from the Meta-Law nodes (`--parent M1_SEAM_SURGERY`, `--parent M2_FAST_EXACT_ORACLE`, etc.):
   - **`H_M1` (Inter-Regime Seam Surgery):** Compose two existing sub-solutions/regimes with relaxed glue and apply exact MILP/SAT/local surgery on the boundary seam.
   - **`H_M2` (Algebraic Cost-Space Transform + MTF):** Apply Fast Zeta/SOS-DP, spectral/Cayley basis, rank-1 updates, or Move-To-Front killer constraint ordering.
   - **`H_M3` (Corank-1 / Slack-Slot Escape):** Escape flat plateaus ($\text{adj}(M) = 0$) via kernel rank deficiency (`Tau-Core`) or unused `degree slack` slots.
   - **`H_M4` (Small-Data Physical/Structural Kernel):** Combine exact domain priors, `CSLS` hubness correction, and `MMP` cliff deltas with closed-form Analytical `LOO-KRR`.
   - **`H_M5` (Reverse Back-Projection + Null-Control Gate):** Invert archival/signal queries gated by known-object calibration + $\ge 200$ permutation null controls.
3. Run `/opt/homebrew/bin/python3 scripts/vs_sample.py` on the verbalized hypothesis table (`typicality`, `p_success`, `cost_min`) to pick the top attack lenses.
4. Regenerate the unified visual canvas:
   ```bash
   /opt/homebrew/bin/python3 scripts/rgraph.py canvas main graphs/main.canvas
   ```

### Step 4: Place First Calibration Bet (`P0001`), First Micro-Bet (`L-MAIN-001`) & Execute Baseline Audit
1. Log the macro campaign prediction in `memory/predictions.tsv`:
   ```bash
   /opt/homebrew/bin/python3 scripts/postdict.py predict target/<target-id> <p> "<Specific falsifiable macro prediction for Cycle 1>"
   ```
2. Log the first concrete experiment micro-bet in `memory/local_bets/<target-id>.tsv` (which also auto-syncs into `graphs/<target-id>.jsonl` + `.canvas` and activates the `M1–M6` compass):
   ```bash
   /opt/homebrew/bin/python3 scripts/micro_bet.py predict <target-id> H1_baseline_probe <p> "<Specific falsifiable micro-hypothesis for Experiment 1>" --by proofer_main
   ```
3. Execute the baseline reproduction and initial reconnaissance, then immediately resolve the micro-bet via `scripts/micro_bet.py resolve <target-id> L-... <0|1> "<lesson>"`.

### Step 5: Atomic Cycle 1 Commit & MANDATORY MULTI-THREAD REMINDER TO THE HUMAN
1. Append the Cycle 1 entry to `wiki/log.md`.
2. Overwrite `wiki/meta/hot.md` with the active charter, baseline verification result, open hypotheses in `graphs/main.jsonl`, and next action.
3. Increment `wiki/meta/cycle_counter.txt` from `0` to `1`.
4. **🔴 MANDATORY POST-INITIATION REMINDER:** At the end of your Cycle 1 response, you **MUST** display the following instructions and ready-to-paste `MONITOR` and `<TARGET>_LAB` prompts to the human commander:
   - Remind the human to **name the current main worker thread `PROOFER`**.
   - Remind the human to **open a second thread named `MONITOR`** and paste the **Monitor Prompt (Section III below)** into it.
   - Remind the human that they can **open `AUDITOR` for 1:1 interactive conversation**, OR **open specialist laboratory threads (`<TARGET>_LAB`, Section IV below)** that run federated micro-bets (`scripts/micro_bet.py`) in parallel without colliding with `PROOFER`.

---

## 🛰️ III. READY-TO-PASTE PROMPT FOR THREAD 2: `MONITOR` (META-COMMANDER GOVERNOR)

After `PROOFER` finishes Cycle 1 (First Initiation), open a **new chat thread**, name it **`MONITOR`**, and paste this prompt:

```text
MONITOR: You are the Meta-Commander Governor thread (`CONSTITUTION.md` v16 §16 K10 & `wiki/meta/HEARTBEAT.md`) for this `PROOFER v16` instance.
Your responsibilities on every heartbeat cycle:
1. Read `wiki/meta/hot.md`, `wiki/entities/PROJECT_CHARTER.md`, the unified reasoning graph `graphs/main.jsonl` (`/opt/homebrew/bin/python3 scripts/rgraph.py show main`), and the federated micro-bet status across all threads (`/opt/homebrew/bin/python3 scripts/micro_bet.py status`).
2. Check the progress of the main `PROOFER` worker thread and any specialist lab threads, active background jobs, and open macro predictions in `memory/predictions.tsv`.
3. Independently resolve settled macro bets (`postdict.py resolve <id> 0|1 --by commander "<note>"` and `postdict.py report` -> updating `wiki/meta/calibration.md` and `wiki/meta/beliefs.md`), close finished hypothesis nodes in `graphs/*.jsonl` (`close` / `kill`), and refresh `.canvas`.
4. Enforce the Three-Restart Structural Floor Law (`M6`) and the Two-Miss Representation Pivot Law (`M2` in `micro_bet.py`): if any worker thread stalls after >=2 consecutive failed micro-bets or >=3 restarts at the same error floor, post a structural-barrier alert in `wiki/meta/hot.md`.
5. Never overwrite code files currently being edited by an active `PROOFER` or `<TARGET>_LAB` worker thread.
Execute your first state audit (Heartbeat #1) now and set a recurring 45-minute timer via `schedule` (`CronExpression: "*/45 * * * *"`, `IsDaemon: true`) to govern the project autonomously!
```

---

## 🧪 IV. READY-TO-PASTE PROMPT FOR THREAD 4+: `<TARGET>_LAB` (FEDERATED SPECIALIST / MOONSHOT LAB THREAD)

Whenever you want to spin up an additional parallel worker thread on a specific sub-problem or Moonshot (`<target-id>`) without colliding with `PROOFER`'s global `predictions.tsv` or `hot.md`, open a new chat thread, name it **`<TARGET>_LAB`**, and paste this prompt:

```text
<TARGET>_LAB — FEDERATED SPECIALIST LAB THREAD (PROOFER v16):
You are a dedicated specialist laboratory thread working on target / sub-problem: [<target-id> — DESCRIBE SUB-PROBLEM].
You are governed by the Federated Micro-Bet Protocol and Meta-Generalization Laws M1–M7 (`CONSTITUTION.md` §17 & `scripts/micro_bet.py`):
1. Read `wiki/entities/PROJECT_CHARTER.md`, inspect the target's reasoning graph (`/opt/homebrew/bin/python3 scripts/rgraph.py show <target-id>`), and review ancestral micro-bet examples in `memory/local_bets/ancestral_v15/`.
2. DO NOT write to global `memory/predictions.tsv` or overwrite `wiki/meta/hot.md` (to avoid write contention with the main `PROOFER` thread).
3. BEFORE running any C++/Python/GPU experiment, log a local micro-bet ($p \le 0.65$ on the first shot per Law M4; the script automatically adds the node to `graphs/<target-id>.jsonl` and refreshes `.canvas`):
   `/opt/homebrew/bin/python3 scripts/micro_bet.py predict <target-id> <H_key> <p> "<specific falsifiable hypothesis>" --by <target>_lab`
4. Immediately after the experiment finishes, resolve the micro-bet:
   `/opt/homebrew/bin/python3 scripts/micro_bet.py resolve <target-id> <id_or_key> <0|1> "<concrete takeaway / why it succeeded or failed>"`
5. If `micro_bet.py` prints `🚨 [M2 STRUCTURAL PIVOT TRIGGERED]` (2 consecutive `0` resolutions), you are strictly forbidden from tuning parameters/seeds of the same ansatz — you must pivot the underlying mathematical representation (symmetry basis, exact SAT/MILP/LUT seam solver per M1, or joint interface group G_12 per M7) before placing your next bet!
```
