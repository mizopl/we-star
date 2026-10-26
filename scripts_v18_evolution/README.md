# `scripts_v18_evolution/` — Code-First Implementation of Evolution Hypotheses `H-EVO-01`, `H-EVO-02`, and `H-EVO-06` (`CONSTITUTION v18` Frozen)

> **Why Code-First Evolution instead of `CONSTITUTION v19`?**
> As documented in **[`docs/05_HUMAN_AND_AGENT_DRIFTS.md`](../docs/05_HUMAN_AND_AGENT_DRIFTS.md)**, **[`docs/06_KARPATHY_WIKI_AND_HALL_OF_FAME_SUCCESSION.md`](../docs/06_KARPATHY_WIKI_AND_HALL_OF_FAME_SUCCESSION.md)**, and **[`docs/11_EPISTEMIC_LEDGER_REASONING_GRAPHS_AND_EVOLUTION_HYPOTHESES.md`](../docs/11_EPISTEMIC_LEDGER_REASONING_GRAPHS_AND_EVOLUTION_HYPOTHESES.md)**, adding more prose rules to an already well-converged constitutional prompt (`CONSTITUTION.md v18`, 280 lines) risks **rule dilution and instruction drift**. When an empirical audit reveals a mechanical failure mode (such as agents forgetting `--parent` flags in CLI calls, bundling multi-clause conjunctions at $p > 0.80$, or leaving dangling open nodes after a run finishes), the right fix is **not** a longer prompt — it is **enforcing the invariant directly in the Python tool layer**.

---

## 1. Causal Origin: What the `169`-Bet & `30`-Graph Synthesis Revealed (`docs/11`)

In **[`docs/11_EPISTEMIC_LEDGER_REASONING_GRAPHS_AND_EVOLUTION_HYPOTHESES.md`](../docs/11_EPISTEMIC_LEDGER_REASONING_GRAPHS_AND_EVOLUTION_HYPOTHESES.md)**, we audited all **`169` calibration predictions** (`86` macro-bets in `memory/predictions.tsv` + `83` federated micro-bets across `14` targets in `memory/local_preds/*.tsv`) and all **`30` reasoning graphs** (`337` nodes in `graphs/*.jsonl`). Three concrete mechanical bottlenecks stood out:

1. **Compound-Conjunction & Sub-Claim Overconfidence (`H-EVO-01`):**
   - While `tug` (`Brier = 0.0289`), `run` (`0.1235`), `lens` (`0.1304`), and `scout` (`0.1361`) were tightly calibrated (`overall macro Brier = 0.1556`), **`scope=exp` had a `44.4%` win rate (`Brier = 0.2528`)**, and several high-conviction micro-bets (`L-GQC-001` $p=0.80 \to 0$, `Brier = 0.640`; `L-IMBB-001/002` $p=0.65 \to 0$; `P0074` $p=0.95 \to 0$, `Brier = 0.902`) failed because the prediction bundled multiple clauses ($A \wedge B$) or assigned $p > 0.75$ to an unverified first/pivot experiment.
2. **Orphan Reasoning-Graph Nodes When `--parent` Was Omitted (`H-EVO-02`):**
   - Whenever a worker invoked `micro_bet.py predict <target> <key> <p> "<text>"` without explicitly passing `--parent <prev_key>`, `rgraph.py` created an isolated node with `0` incoming edges. Across `11` historical targets (including `ame-states-open-cells-huber-table`, `google-quantum-compilation`, and `iedb-mhci-bd2009-blind-auc`), **`81` sequential causal transitions** were recorded in the `.tsv` ledger timestamps but missing from the `.jsonl` / `.canvas` edge list.
3. **Dangling Open Nodes After Run Completion & Binary-PDF Context Overflow (`H-EVO-06` / `K16` / `Dead-End Guard X14`):**
   - Seven early reasoning graphs retained open `hypothesis` / `experiment` nodes after the target had already achieved a verified `closed` / `result` node.
   - At `04:17 AM` on `2026-10-26`, two parallel `read_file` calls on a 229-page binary PDF (`trudy_imm_2009_2.pdf`, `2.7 MB`) overflowed the `1,048,576`-token hard API ceiling (`Dead-End X14`).

---

## 2. Summary of the Three Upgraded Scripts in This Directory

| Script | Hypotheses Operationalized | Key Mechanical Upgrades |
| :--- | :--- | :--- |
| **[`micro_bet.py`](./micro_bet.py)** | **`[x] H-EVO-01`**<br>**`[x] H-EVO-02`** | 1. **Auto-Parent Causal Wiring (`H-EVO-02`):** If `--parent` is omitted on `micro_bet.py predict`, automatically links the new node to the most recent bet node in `graphs/<target>.jsonl` using edge relation **`resumes`** after a `0` kill or **`derives`** after a `1` win. If the graph is empty, automatically initializes a root question node (`Q_root`) first. If the node key already exists in `rgraph.py`, calls `rgraph.py link` so the causal edge is never dropped.<br>2. **Structured Obstruction-Typed Kills (`H-EVO-02`):** Adds `--obstruction {capacity_floor, symmetry_trap, metric_artifact, numerical_precision, compute_wall}` to `micro_bet.py resolve <target> <id> 0` (and automatically infers the obstruction tag from the resolution text when omitted).<br>3. **Anti-Hubris & Conjunction Ceiling (`H-EVO-01` / `M4`):** Automatically clamps $p > 0.65 \to 0.65$ on the first bet of a target, immediately after a failed bet (`outcome=0`), or when the prediction text bundles multiple quantitative inequality clauses (`A ∧ B`). |
| **[`postdict.py`](./postdict.py)** | **`[x] H-EVO-01`** | 1. **Sub-Claim (`scope=exp`) & Compound-Conjunction Calibration Cap (`H-EVO-01` / `M4`):** Automatically clamps $p > 0.65 \to 0.65$ whenever `scope` is in `{"exp", "subclaim", "secondary"}` (historical hit rate `44.4%`) or when the prediction text bundles multiple quantitative thresholds (`A ∧ B`), unless `--allow-high-p` is explicitly passed after Stage I oracle confirmation.<br>2. **Quadratic Brier Asymmetry Warning:** Emits a pre-commit calibration warning whenever $p > 0.85$ (`Brier >= 0.723` on a miss). |
| **[`sleep_flush.py`](./sleep_flush.py)** | **`[x] H-EVO-02`**<br>**`[x] H-EVO-06`**<br>**`[x] K16 / M6`** | 1. **Synaptic Causal-Edge Stitching (`H-EVO-02`):** Scans all `graphs/*.jsonl`, connects sequential orphan nodes (`derives` after wins/open nodes, `resumes` after `kill` nodes), and recompiles all Obsidian `.canvas` visual boards.<br>2. **Completed-Target Node Consolidation (`K16` / `M6`):** Automatically closes superseded open `hypothesis`/`experiment`/`lead` nodes on targets that already possess verified `closed`/`result` certificates (while respecting `--active-target <target>`).<br>3. **Binary-PDF Pre-Read & Token-Ceiling Guard (`H-EVO-06` / `Dead-End Guard X14`):** Scans `runs/*/` for any `.pdf` $> 100\text{ KB}$ lacking a companion `.txt` file and automatically extracts page-indexed plain text (`=== PAGE N ===`) via `pypdf` so no agent can trigger the `1M`-token binary-PDF crash. |
| **[`stitched_graphs/`](./stitched_graphs/)** | **Verified Output Artifacts** | Contains all **`30` reasoning graphs (`.jsonl` + `.canvas`)** after running `sleep_flush.py` (`337` total nodes: `148` closed, `117` dead, `+81` stitched causal edges, `+7` consolidated dangling nodes). |

---

## 3. Live Empirical Verification (`2026-10-26`)

1. **Retroactive Graph Consolidation (`sleep_flush.py` across all `30` graphs):**
   - **Targets updated:** `11` reasoning graphs
   - **Causal edges stitched (`H-EVO-02`):** **`+81` edges** (e.g., `ame-states-open-cells-huber-table`: `2` $\to$ `26` edges across `27` nodes; `google-quantum-compilation`: `0` $\to$ `12` edges across `13` nodes; `iedb-mhci-bd2009-blind-auc`: `0` $\to$ `10` edges across `11` nodes; `immrep22-tcr-epitope-microauc`: `0` $\to$ `8` edges across `9` nodes)
   - **Dangling open nodes closed (`K16` / `H-EVO-06`):** **`+7` nodes** (`337` total nodes: `148` closed, `117` dead, `72` active Moonshot frontier nodes)
2. **Real-Time Live Verification on `conway-99-graph` (`PROOFER-II`):**
   - Immediately after deploying the upgraded `micro_bet.py`, our active worker on `conway-99-graph` registered micro-bet **`L-C9G-008`** (`H8_18case_full_package`) without passing `--parent`.
   - `micro_bet.py` automatically detected the preceding resolved node **`L-C9G-007`** (`outcome=1`) and wired the causal edge **`L-C9G-007 --<derives>--> L-C9G-008`** in [`stitched_graphs/conway-99-graph.jsonl`](./stitched_graphs/conway-99-graph.jsonl), producing a `100%` connected `8`-node, `7`-edge reasoning tree (`L-C9G-001`..`L-C9G-008`).
