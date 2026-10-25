---
name: clss-solver
description: >-
  Four-Stage CLSS (Compositional Lifting + Seam Surgery + Bit-Parallel Exact
  Oracle) solver protocol and the Seven Universal Laws of Meta-Generalization
  (M1–M7). Use whenever attacking an open scientific, mathematical, combinatorial,
  quantum compilation, or optimization problem to achieve verified breakthroughs
  on consumer hardware.
---

# CLSS Solver & Meta-Generalization Laws (`M1–M7`)

## Overview
Apply this skill whenever solving a constructive, algorithmic, optimization, or proof problem. Never run blind brute-force search before building a fast deterministic oracle and identifying the structural seam.

## The 4-Stage CLSS Protocol (`CONSTITUTION.md` §15 / `K9`)

1. **Stage I — Sub-Second Exact Oracle First (`< 5s`, `Law M2`):**
   - Write and freeze a standalone, deterministic verification script (`verify_oracle.py` or compiled C verifier) before running any search.
   - Include **1 positive self-test** (reproducing the known baseline) and **1 negative self-test** (confirming a corrupted/perturbed candidate fails).
   - If single evaluation takes $> 10\text{ ms}$, transform the cost space first (Fast Zeta / `SOS-DP`, spectral/Cayley basis, rank-1 updates, bit-parallel bitmasks, or *Move-To-Front* killer-constraint ordering).

2. **Stage II — Parameter-Relaxed Compositional Lifting (`Law M1`, `M7.1`, `M7.2`):**
   - Decompose the target into smaller exact building blocks rather than searching cold-start from scratch.
   - **Free the Joint Interface (`M7.1`):** Identify the full joint symmetry group $G_{12}$ across coupled blocks (not just independent $G_1 \times G_2$).
   - **Scan the Full Solution Fiber (`M7.2`):** Solutions tied on their Stage-1 metric are not equivalent for Stage-2 composition; score the full fiber of tied Stage-1 candidates with a millisecond compatibility proxy and hybridize distinct orbits.

3. **Stage III — Deterministic Seam Surgery (`Law M1`, `M3`, `M4`, `M5`, `M7.3`, `M7.4`):**
   - Freeze the internal bulk of the building blocks and concentrate exact solver compute (MILP, SAT, CP-SAT, LUT, or unimodular basis reduction) strictly on the narrow **boundary seam**.
   - **Escape Flat Plateaus (`M3`):** If $\text{corank} \ge 2$ annihilates the 1-opt gradient, score kernel rank deficiency (`Tau-Core`) or inject a temporary slack slot.
   - **Primal–Dual Ping-Pong & Signed Cancellation (`M7.3`):** Audit primal–dual or operation-order asymmetry (e.g., reversing commutative row operations to shrink borrow/carry horizons) and allow non-monotone moves that over-provision an intermediate state and cancel the excess in the next step.
   - **Surgical Defect Fission (`M7.4`):** When 98–99% of a global structure succeeds except for one localized conflict, surgically split only the colliding element rather than discarding the global skeleton.

4. **Stage IV — 1-Minimality, Three-Restart Floor (`M6`) & 3-Skeptic Panel:**
   - **Three-Restart Floor (`M6`):** If $\ge 3$ independent restarts halt at the exact same non-zero error floor, stop brute-forcing immediately and prove the underlying No-Go / Parity Obstruction Theorem.
   - Prove 1-minimality or dual-decomposition agreement, then run the 3 independent fresh-context skeptics (`REPRODUCE`, `NOVELTY`, `CRITERION`).
