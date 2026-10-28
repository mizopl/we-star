---
name: surrogate-metric-architect
description: >-
  Designs non-hackable surrogate Violation Energy functions (Law M1) and runs
  Known-Example Dissection / Explanation-Based Generalization (EBG) when a
  problem has a flat 0/1 decision landscape without a native proximity gradient.
  Use before launching any solver on needle-in-a-haystack NP witnesses or
  universal proofs (Lychrel, Quantum AME, Steiner Systems, Covering Congruences).
---

# Surrogate-Metric & Convergence Architect (`Law M1` + `EBG`)

## Overview
A solver without a proximity gradient is blind; a solver that invents its own proximity gradient while optimizing it will reward-hack itself (`CONSTITUTION v17 §12`). This skill separates **Surrogate Metric Design** from **Search Execution**.

## When to Trigger This Skill
Trigger immediately before launching a search or proof campaign whenever:
1. The verifier returns only `True / False` (`0 / 1`) with no native continuous or fine-grained integer score.
2. The native integer objective has wide plateaus (e.g., thousands of distinct circuits share the exact same Toffoli or addition count).
3. The problem is a universal claim ($\forall t \in \mathbb{N}$ or $\forall x \in X$) where finite numerical simulation creates a false illusion of progress (Dead End `K1`).

## Workflow

### Phase 1: Known-Example Dissection (`EBG`)
If any solved example exists in the literature (even for a smaller dimension $n$ or base $b$):
1. Write a dissection script in `python3` that traces the known witness step-by-step and prints its internal invariants (e.g., carry bit-vectors, syndrome weight distribution, rank profile).
2. Identify the **minimal structural invariant** that makes the example work.
3. Parameterize that invariant and compute the exact algebraic obstruction preventing it from working at the target parameter.

### Phase 2: Violation Energy Construction (`Law M1`)
If the problem requires finding an existential witness $x \in \Omega$:
1. Decompose the binary validity predicate $\bigwedge_{i=1}^m C_i(x)$ into quantitative constraint violations $v_i(x) \ge 0$:
   $$E_{\text{viol}}(x) = \sum_{i=1}^m w_i \, v_i(x)$$
   Examples across `PROOFER` domains:
   - **Quantum `AME(n, q)` / Stabilizer Codes:** Number of rank-deficient $k \times k$ bipartition minors + weighted count of low-weight symplectic codewords ($w < d$).
   - **Lychrel Automate Closure:** Number of reachable $(d_i, d_{L-1-i})$ digit pairs that trigger an unabsorbed carry across the invariant barrier (`0` violations = closed inductive automaton).
   - **Bilinear `FMM` / Addition `SLP` Tie-Breaking:** Minimum Hamming distance from current intermediate basis vectors to the remaining target rows, plus seam-rank deficiency (`Law M7.1`).
2. Implement **incremental delta evaluation** $\Delta E_{\text{viol}}(x \to x')$ in $O(1)$ or $O(n)$ time (Law `M7`: Hardware-Constrained Algorithmic Co-Evolution).

### Phase 3: The 3-Gate Certification
Run a standalone check confirming:
- **Exactness at Zero:** $E_{\text{viol}}(x) = 0 \iff \text{Valid}(x) = 1$.
- **Gradient Density:** > 25% of 1-step random neighbors around non-optimal states exhibit $\Delta E_{\text{viol}} \ne 0$.
- **Speed:** $\ge 1{,}000$ incremental evaluations per second on a single CPU core.
