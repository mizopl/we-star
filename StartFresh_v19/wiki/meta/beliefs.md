# Beliefs & Calibration Priors (`PROOFER v16` — Seeded from Parent `PROOFER v15`)

*Inherited Baseline (Parent `PROOFER v15`, 90 resolved bets):* Overall V3R1T4S Brier = **`0.168`**, Target Brier = **`0.073`** (`85–88%` hit rate on main targets).

## 1. Empirical Calibration Adjustments (Inherited from Parent `v15`)
- **Systematic Underconfidence on Constructive Seam Surgery (`M1` & `M2`):** In Parent `v15`, bets placed in the $p \in [0.40, 0.60]$ bin achieved a **`92%` hit rate (`11/12`)**, and tail bets in $p \in [0.00, 0.20]$ achieved a **`33%` hit rate (`3/9`)** whenever backed by a sub-second exact oracle (`M2`) and compositional seam surgery (`M1`). **Adjustment:** When a genuine inter-regime seam and $< 1\text{ s}$ exact verifier exist, assign prior $p \in [0.75, 0.90]$ rather than $0.40$.
- **Overconfidence Trap on Unchecked Symmetry Floors (`M6`):** Bets with $p \ge 0.65$ failed whenever local search or SA was launched into a symmetric ansatz before checking for an involution-parity, corank-2 adjugate (`adj(M) = 0`), or Shannon unicity obstruction. **Adjustment:** Never assign $p > 0.50$ to a pure search lens until the **Three-Restart Structural Floor (`M6`)** and unicity/parity checks are cleared.

## 2. Prior Success Probabilities by Mechanism (`M1–M6`)
- **`M1` (Inter-Regime Seam Surgery + MILP/SAT/Prune-Merge):** Prior $p = 0.85$
- **`M2` (Algebraic Cost-Space Transform: Fast Zeta / Spectral / Cayley / MTF):** Prior $p = 0.85$
- **`M3` (Corank-1 `Tau-Core` & Degree-Slack Slot Injection):** Prior $p = 0.75$
- **`M4` (Small-Data Analytical LOO-KRR + Physical/Structural Priors + CSLS):** Prior $p = 0.85$
- **`M5` (Reverse Back-Projection + Known-Object Calibration + $\ge 200$ Null Controls):** Prior $p = 0.85$
- **Cold-Start Unconstrained Heuristic / Blind Deep Learning on Small Data:** Prior $p = 0.10$ (avoid unless required as a baseline control)
