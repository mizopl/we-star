---
name: micro-bet-compass
description: >-
  Federated Micro-Bet and Reasoning Graph governance skill using micro_bet.py,
  rgraph.py, postdict.py, vs_sample.py, and tug.py. Use before and after every
  experiment to calibrate predictions, maintain Obsidian reasoning graphs,
  enforce the p <= 0.65 Anti-Hubris Cap (M4), and trigger mandatory structural
  pivots after 2 consecutive failures (M2).
---

# Federated Micro-Bet & Reasoning Graph Compass (`K3`, `M2`, `M4`, `M6`)

## Core Workflow for Every Experiment

1. **Check the Reasoning Graph Before Starting (`rgraph.py`):**
   ```bash
   python3 scripts/rgraph.py show <target-id>
   python3 scripts/rgraph.py check <target-id> "<candidate idea>"
   ```
   Never repeat a `DEAD_NEAR_DUPLICATE` line without a genuinely new structural mechanism.

2. **Place a Pre-Registered Micro-Bet Before Running Code (`micro_bet.py`, `Law M4`):**
   - Cap first-shot probability on any unverified micro-hypothesis at **`p <= 0.65`**:
   ```bash
   python3 scripts/micro_bet.py predict <target-id> <H_node_key> <p> "<falsifiable hypothesis>" --by <thread_name>
   ```
   - This automatically logs the bet in `memory/local_bets/<target-id>.tsv`, adds the hypothesis node to `graphs/<target-id>.jsonl`, and refreshes `graphs/<target-id>.canvas`.

3. **Resolve Immediately After the Experiment (`micro_bet.py`, `Law M2`):**
   ```bash
   python3 scripts/micro_bet.py resolve <target-id> <L_id_or_H_key> <0|1> "<concrete takeaway>"
   ```
   - If `micro_bet.py` outputs **`🚨 [M2 STRUCTURAL PIVOT TRIGGERED]`** (2 consecutive `0` resolutions), stop tuning seeds or hyperparameters on the current ansatz and change the underlying mathematical representation.

4. **Adversarial Decision Gate (`tug.py`) & Verbalized Sampling (`vs_sample.py`):**
   - Use `python3 scripts/vs_sample.py hypotheses.tsv` to sample diverse attack lenses (including low-typicality tail ideas and cross-domain imports).
   - For high-consequence strategic choices, run `python3 scripts/tug.py` (`IMPLEMENT` vs `SEARCH`) using the `.agents/agents/tug-advocate.md` subagent.
