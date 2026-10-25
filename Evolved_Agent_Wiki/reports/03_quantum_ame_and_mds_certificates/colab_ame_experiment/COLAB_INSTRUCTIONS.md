# Instructions for Running the `AME(7, 6)` GPU Experiment on Google Colab

Everything is prepared, smoke-tested locally (`--smoke` in `7.95 s`, `0` errors), and stored in this directory:
- **Primary `AME(7, 6)` Script (Direction 1):** [`ame_7_6_colab_gpu_hunt.py`](./ame_7_6_colab_gpu_hunt.py)
- **4-Engine Comparison Script (`AME(15,5)`, `AME(8,4)`, `AME(11,3)`, `AME(20,19)`):** [`colab_ame_gpu_experiment.py`](./colab_ame_gpu_experiment.py)
- **Saved Results from the Initial L4 GPU Run:** [`colab_l4_gpu_results_2026_10_21.json`](./colab_l4_gpu_results_2026_10_21.json)

---

## How to Launch the `AME(7, 6)` Experiment on Google Colab

Run the following command from your terminal (the runner provisions an `L4` or `A100` GPU instance on Google Colab, executes the script, saves the JSON output, and shuts down the runtime upon completion):

```bash
/opt/homebrew/bin/python3 ~/Desktop/PROOFER/scripts/colab_gpu_runner.py \
  --script ~/Desktop/PROOFER/wiki/reports/colab_ame_experiment/ame_7_6_colab_gpu_hunt.py \
  --gpu L4
```

---

## What Does `ame_7_6_colab_gpu_hunt.py` Do?

1. **Target:** The open cell **`AME(7, 6)`** ($n = 7$ particles of local dimension $D = 6 = 2 \times 3$, state space of $6^7 = 279,936$ complex amplitudes, $\binom{7}{3} = 35$ tripartite cuts of size $216 \times 1296$), listed as **open (`?`)** in the Huber–Wyderka table (`https://huberfe.github.io/ame`).
2. **Starting Construction (`CLSS` Qubit–Qutrit Seam Surgery):**
   - On the 7-qutrit layer ($\mathbb{F}_3$), it uses the exact circulant graph state $\mathrm{AME}(7, 3)$ with first row $r_0^{(3)} = [0, 0, 1, 1, 1, 1, 0] \pmod 3$, which has **0 / 35 singular cuts** and a $3\times$ dimension surplus on the 4-party side ($3^4 = 81 = 3 \times 27$).
   - On the 7-qubit layer ($\mathbb{F}_2$), it uses the optimal circulant $r_0^{(2)} = [0, 0, 0, 1, 1, 0, 0] \pmod 2$, which satisfies **28 of 35 cuts** (4 of the 5 cyclic $Z_7$ orbits start with **exact zero defect** `[0.0, 0.0, 0.0680414, 0.0, 0.0]`!).
3. **Two-Stage GPU Solver (Newton–Schulz `torch.bmm` + AdamW + L-BFGS `strong_wolfe`):**
   - **Stage 1 ($Z_7$-Cyclic, 5 Orbits of Size $216 \times 1296$):** Fast Newton–Schulz isometric projection and second-order L-BFGS polishing across the 5 cyclic orbit representatives ($7\times$ fewer matrices than all 35 cuts).
   - **Stage 2 (Full 35 Cuts Without Symmetry Constraints):** Releases the $Z_7$ cyclic symmetry constraints to test whether symmetry breaking allows the Frobenius defect to reach machine zero ($< 10^{-8}$).
