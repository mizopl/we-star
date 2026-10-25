# Part III — The Six Universal Laws of Meta-Generalization (`M1–M6` from `StartFresh v16`)

Laws `M1–M6` were distilled empirically from 90+ resolved calibration bets (`predictions.tsv` and `memory/local_bets/`) and 250+ reasoning-graph nodes (`graphs/*.jsonl`). They are formulated in a strictly **domain-agnostic** manner so they can be applied across combinatorics, quantum compilation, operations research, bioinformatics, and physical modeling.

---

## Law `M1` — Inter-Regime Boundary Surgery & Exact Solver First
- **Principle:** Instead of searching for a global structure from scratch via cold-start random search, decompose the system into smaller, well-understood building blocks, freeze their internal bulk, and apply an exact solver (MILP, SAT, CP-SAT, LUT, or exact algebraic basis reduction) **exclusively on the narrow boundary seam between them**.
- **Historical Win Rate:** ~95% of our constructive world records.
- **Examples in Practice:**
  - *Combinatorial Covering Designs (`PR #398`, `PR #435`):* Composing smaller LJCR covering designs via relaxed staircase splits and repairing only the boundary seam blocks.
  - *Hospital Timetabling (`IHTC-2024`, 31 BKS records):* Freezing the bulk schedule and solving exact rolling MILP/CP-SAT windows along shift/room interfaces.

---

## Law `M2` — Cost-Space Representation Transform & Two-Miss Pivot
- **Principle:** Before scaling compute, transform the mathematical representation of the objective so that a single evaluation is $10^4\times$–$10^6\times$ faster (Fast Zeta / `SOS-DP` transform, spectral/Cayley basis, rank-1 updates, bit-parallel C invariants, or *Move-To-Front* killer constraint ordering).
- **Hard Rule (`Two-Miss Pivot`):** After **2 consecutive failed micro-bets (`0`)** on the same ansatz, **STOP** tuning seeds or hyperparameters and pivot the underlying mathematical representation.
- **Examples in Practice:**
  - *DNA Minimizer Density (`PR #425`, `PR #433`):* Replacing explicit $k$-mer window scans with a Fast Zeta Transform (`SOS-DP`).

---

## Law `M3` — Constraint Relaxation & Slack-Dimension Escape
- **Principle:** When local optimization stalls on a flat plateau where multiple simultaneous constraints annihilate the local gradient ($\text{corank} \ge 2$), temporarily relax the constraint space or inject an explicit slack degree of freedom (`slack slot`) to traverse the barrier, then project back onto the exact feasible manifold.
- **Examples in Practice:**
  - *Ternary Fast Matrix Multiplication (`FastMatrixMultiplication`, `PR #402`, `PR #615`):* Temporarily stepping outside $\lbrace -1, 0, 1 \rbrace$ during flip-graph `plus`/`reduce` transitions, followed by unimodular basis reduction back into $\mathbb{Z}_T$.

---

## Law `M4` — Domain-Invariant Priors on Small Data & Anti-Hubris Cap
- **Principle:** In low-sample or high-noise regimes ($N < 10^3$), embed exact physical/structural symmetries directly into the kernel (e.g., `CSLS` hubness correction, `MMP` activity-cliff deltas, closed-form analytical Leave-One-Out Kernel Ridge Regression `LOO-KRR`) rather than fitting over-parameterized black-box neural networks.
- **Hard Rule (`Anti-Hubris Cap`):** First-shot confidence on any unverified micro-hypothesis is strictly capped at **`p <= 0.65`**.
- **Examples in Practice:**
  - *Materials Physics (`NIST JARVIS`, `PR #599`) and Drug Discovery (`Polaris MoleculeACE`, `PR #568`).*

---

## Law `M5` — Inverse Query Back-Projection & Blind Null-Control Gate
- **Principle:** Instead of forward-guessing in a vast candidate space, invert the forward operator to project observed constraints backward into the source domain. Every candidate discovery in archival or sequential data must pass a dual gate:
  1. **100% recovery of known calibration objects**, and
  2. **$\ge 200$–$400$ randomized permutation null controls (`null_test.md`)** proving the signal is not a statistical artifact.
- **Examples in Practice:**
  - *Pan-STARRS Asteroid Precovery (`PR #607`), GMN Meteor Showers (`PR #597`), Indus Script (`PR #570`), and Held-Out Akkadian Restoration (`PR #611`).*

---

## Law `M6` — Three-Restart Structural Floor Law & Graph Closure Hygiene
- **Principle:** If $\ge 3$ independent restarts (from distinct random seeds or initial states) halt at the **exact same non-zero error floor**, stop brute-force search immediately. That floor is not bad luck — it is a **structural No-Go or Parity Obstruction Theorem** waiting to be proved and quotiented out.
- **Graph Hygiene:** Close (`close` / `kill`) all finished hypothesis nodes in `graphs/<target>.jsonl` in the same cycle so no subsequent thread wastes compute on the same barrier.

---

*Signed,*
**`we*`** — **`@mizopl` + Agentic Systems (`Claude` & `Gemini-CLSS / PROOFER v17`) + The Feedback Loop**
*(PS. `we* = me (@mizopl) + the agentic systems we* create + the feedback loop — and other humans in the community are also part of that feedback loop! We* hope this system proves useful; feel free to reach out directly via GitHub @mizopl (https://github.com/mizopl).`)*

