---
type: concept
id: concept-bilinear-slp-and-quantum-synthesis
title: "Bilinear Straight-Line Programs (SLP), Flip-Graph Rank Reduction & Quantum Circuit Synthesis"
confidence: 5
created: 2026-10-23
updated: 2026-10-23
tags:
  - quantum-compilation
  - bilinear-complexity
  - tower-field
  - flip-graph
  - boyar-peralta
  - mbuc
sources:
  - "V3R1T4S PR #313 (@HindsightWise): flip4.py & dag_cone_collapse.py"
  - "V3R1T4S PR #205 (@calgulbenkian): bpopt.c & slpopt.c"
  - "Google Quantum AI Kaggle (ID: 161954): BET-Q-009, BET-DQI-011, BET-DQI-013"
---

# Bilinear Straight-Line Programs (SLP), Flip-Graph Rank Reduction & Quantum Circuit Synthesis

Reusable cross-domain methods linking **Fast Matrix Multiplication / Bilinear Tensor Decomposition (`V3R1T4S`)** with **Fault-Tolerant Quantum Circuit Compilation (`Toffoli + CNOT` minimization)**:

## 1. Kauers–Moosbauer Flip-Graph Rank Reduction over $\mathbb{F}_2$ (`flip4.py`)
Any bilinear map $B: \mathbb{F}_2^m \times \mathbb{F}_2^n \to \mathbb{F}_2^p$ (such as finite-field multiplication in $\mathbb{F}_{2^{12}}$ or $\mathbb{F}_{2^6}$) with rank-$R$ decomposition
$$T = \sum_{r=1}^R u_r \otimes v_r \otimes w_r$$
synthesizes into a **0-ancilla quantum circuit with exactly $R$ Toffoli (`CCX`) gates** flanked by linear CNOT (`CX`) networks $(U, V, W)$.
- **`flip` move (rank-preserving):** Given two triples $a, b$ sharing a common factor in one mode (e.g., $u_a = u_b = x$),
  $$x \otimes v_a \otimes w_a \oplus x \otimes v_b \otimes w_b = x \otimes (v_a \oplus v_b) \otimes w_a \oplus x \otimes v_b \otimes (w_b \oplus w_a).$$
- **`reduce` move (rank $-1$):** Whenever two triples agree in two modes, merge them into one ($R \to R - 1$); whenever a vector becomes $0$, drop the triple.

## 2. Boyar–Peralta & DAG Cone Collapse for Pre/Post CNOT Networks (`bpopt.c`, `dag_cone_collapse.py`)
Once the bilinear triples $(u_r, v_r, w_r)$ are fixed, synthesizing the linear evaluation maps $U, V$ and interpolation map $W$ with minimum `CX` gates is equivalent to the **Shortest Linear Program (SLP) problem over $\mathbb{F}_2$**:
- Iteratively extract the pair of columns $(i, j)$ with maximum overlap across remaining target rows (`Boyar–Peralta` greedy / beam heuristic) or collapse multi-fanout cones (`dag_cone_collapse.py`).
- Ordering the $R$ Toffoli products greedily by minimum incremental LUP pivot distance on the live basis matrices $(A, B, C)$ eliminates intermediate ancilla wires (`0` extra qubits).

## 3. Canright Composite Tower-Field Inversion + 0-Toffoli MBUC (`tower_inv.py`)
For inversion $x \mapsto x^{-1}$ in $\mathbb{F}_{2^{2k}}$, decompose as a quadratic tower over $\mathbb{F}_{2^k}$ in a normal basis $[y, y^{2^k}]$ with trace $1$ and norm $\lambda$:
- $a^{-1} = (a_1 y + (a_0 + a_1))\Delta^{-1}$ where $\Delta = a_0(a_0 + a_1) + \lambda a_1^2 \in \mathbb{F}_{2^k}$.
- All intermediate tower registers ($\Delta, \Delta^{-1}$, sub-multipliers) are uncomputed with **0 Toffoli gates** via $X$-basis measurement (`HMR`) followed by parity-conditioned `CZ` phase corrections (`MBUC`).

## 4. Multi-Scale Empirical Gate-Activity Pruning with Held-Out Attribution (`BET-DQI-012 / 013`)
When static constant propagation (`0/1/U`) cannot prove semantic invariants (such as polynomial degree triangles in synchronized EEA decoders):
1. Bit-pack simulate $N_{\text{train}} \ge 1.6 \times 10^5$ problem-distributed shots and record every Toffoli-like gate (`CCX`, `CCZ`, `CSWAP`) that ever fires non-trivially (`active.npy`).
2. Partition the circuit into $M \in [4 \times 10^3, 4 \times 10^4]$ natural structural segments and attribute shot failures on an independent held-out set ($N_{\text{val}} \ge 2 \times 10^5$ shots) to individual segments.
3. Prune only zero-active gates inside segments with zero held-out hits, optimizing the exact verifier repetition-factor trade-off $R(\varepsilon_+) Q^2 T$.
