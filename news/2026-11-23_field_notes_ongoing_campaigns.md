# Field Notes #007 (`LIVE` Rolling Log) — Ongoing Campaigns: `ex(Q_8, C_4) ∈ {682, 683}` & Littlewood Flat Polynomials (`deg 69`)

> **Status:** `LIVE` Rolling Lab Notebook · **Last Updated:** `2026-11-23 17:46 CET` · **Authors:** `@mizopl` & **`we*`** (`PROOFER` Open-Science Lab)  
> **Repository:** [`mizopl/we-star`](https://github.com/mizopl/we-star) (`we* = me + agentic systems we* create + the feedback loop`)  
> **Update Policy:** This dispatch is updated continuously as public campaigns land new cold-verified theorems, witnesses, or falsified dead-end maps. Only machine-checked results (`0 sorryAx` Lean 4, exact MILP/SAT, or `< 1 s` offline verifiers with `--corrupt` exit `1`) are added.  
> **Cold Verifiers:** [`solutions/q8-c4-extremal-forcing/verify.py`](../solutions/q8-c4-extremal-forcing/verify.py) (`0.002 s`, `--corrupt` exits `1`) · [`Q8EmptySquareForcing.lean`](../solutions/q8-c4-extremal-forcing/Q8EmptySquareForcing.lean) (`Lean 4 v4.35.0`, `0 sorryAx`)

<p align="center">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="./assets/ongoing_campaigns_obsidian_constellation_dark.svg">
    <source media="(prefers-color-scheme: light)" srcset="./assets/ongoing_campaigns_obsidian_constellation_light.svg">
    <img alt="Ongoing campaigns (q8-c4-extremal and flat-polynomials) inside the we* Obsidian Vault constellation" src="./assets/ongoing_campaigns_obsidian_constellation_light.svg" width="560">
  </picture>
  <br>
  <sub><b>Figure 1 · Obsidian Vault Constellation:</b> Live <code>Ongoing Campaigns</code> anchor (<code>q8-c4-extremal-forcing</code> &amp; <code>Q8EmptySquareForcing.lean</code>) pinpointed inside the 5,000+ node <code>we*</code> Obsidian knowledge galaxy (<a href="./assets/ongoing_campaigns_obsidian_constellation_dark.svg">dark</a> · <a href="./assets/ongoing_campaigns_obsidian_constellation_light.svg">light</a>).</sub>
</p>

<p align="center">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="./assets/ongoing_campaigns_system_graph_dark.svg">
    <source media="(prefers-color-scheme: light)" srcset="./assets/ongoing_campaigns_system_graph_light.svg">
    <img alt="Ongoing campaigns position on the we* epistemic system graph" src="./assets/ongoing_campaigns_system_graph_light.svg" width="880">
  </picture>
  <br>
  <sub><b>Figure 2 · Epistemic System Graph:</b> <code>q8-c4-extremal</code> pinpointed at the living apex of the <code>we*</code> public chronological trunk alongside sibling public campaigns (<a href="./assets/ongoing_campaigns_system_graph_dark.svg">dark</a> · <a href="./assets/ongoing_campaigns_system_graph_light.svg">light</a>).</sub>
</p>

---

## 0. Scope & Limitations First (`-0 Hype`)

None of the active problems below is solved yet — this rolling dispatch tracks **verified intermediate steps, new structural witnesses, formal Lean 4 lemmas, and quantified dead ends** while the campaigns remain live:

1. **`ex(Q_8, C_4) ∈ {682, 683}` remains OPEN:** We neither constructed a $683$-edge $C_4$-free subgraph of $Q_8$ nor proved $\operatorname{ex}(Q_8, C_4) \le 682$. Across Rounds 2–3, tightening from our $Q_4$ 3-measure relaxation (`683.5770`, `39.6%` of gap) to a **$Q_5$ column-lifted hybrid** (`+314` 4-flag `E_4` equations + `6 h_5` + `Q_4 L3`, adversarially hardened across `>45M` $2^{80}$ evaluations to `22,107` certified $C_4$-free $Q_5$ masks) lowered the pool upper bound by **`-0.676` edges below [`lisresearchgroup/math-rsi`](https://github.com/lisresearchgroup/math-rsi)'s `B684`** (`683.9557 -> 683.2796`, closing **`70.7%`** of the gap to `683.000`), while explicitly exposing a **`+0.28`-edge barrier (`683.2796 > 683.000`)** that requires true $Q_5$-level PSD blocks (not $Q_4$-only PSD/cones) or targeted $Q_6/Q_7$ SAT/DRAT cuts to cross. All `683.5770`, `683.2796`, and `n_0 >= 11 / 13` figures are exact `HiGHS` pool bounds (with `Q_5` masks certified $C_4$-free and adversarially hardened, not a global $2^{80}$ exhaustion), and our Lean 4 file proves elementary double-counting identities on `C4FreeCounts`, not the global `<= 682` bound.
2. **Degree-69 Littlewood flat polynomials (`flat-polynomials-papr`) — `3` distinct islands strictly below `EA-2026`, live `#1` matched twice from scratch (strictly beating `#1` remains OPEN):** Across Waves 4–5 (`482.8B` `G = 512` CUDA evals on `T4`/`L4`), our pure-scratch solvers independently discovered the live `EinsteinArena` `#1` polynomial (`C+ = 1.259457173221`, certified `[1.259457175649, 1.259457303746]`, `-1.68%` below `EA-2026` `1.28093205` and `-6.08%` below AlphaEvolve V2 `1.340925`) **twice** from independent random seeds, plus **two additional distinct cold-verified islands strictly below `EA-2026`** (`1.27340279` and `1.28072749`). However, **`0` polynomials strictly below `1.259457173221`** were found across `460.4B` Wave-5 evals, and capture–recapture (`Chao1 = 6.8` for `C+ < 1.285`) indicates near-saturation of the `< 1.285` manifold reachable by spectral-SAW.
3. **Zero stealth items listed:** Any offline or competition-embargoed work is excluded from this public log.

---

## 1. Live Public Campaign Board (`2026-11-23 17:46 CET`)

| Campaign | Problem & Benchmark | Current Stage | Verified Milestone (`-0 Hype`) | Next Open Frontier |
| :--- | :--- | :--- | :--- | :--- |
| **`q8-c4-extremal`** | Erdős #86: $\operatorname{ex}(Q_8, C_4) \in \{682, 683\}$ ([`math-rsi`](https://github.com/lisresearchgroup/math-rsi)) | **Round 3 Done** (`Q_5` hybrid barrier mapped) | `6/6` zero-axiom Lean 4 forcing theorems + first zero-defect `{5^172, 6^84}` `682` witness; Round-2 `Q_4 L3` hit **`683.5770`** & forced `n_0 >= 11` across all `783` `m=683` profiles (`>= 13` on `{5:85, 6:43}`); Round-3 **`Q_5 + 314 E_4 + Q_4 L3`** (`22,107` adversarially hardened $C_4$-free $Q_5$ masks) hit **`683.2796`** (**`-0.676` below `B684`**, **`70.7%`** of gap closed; `Q_5 L0 + E_4` already `683.2799` with `0` PSD cuts!) | True **`Q_5`-level PSD blocks** ($Q_3$-rooted flag matrices coupling orthogonal $Q_4$ halves) or targeted $Q_6/Q_7$ SAT/DRAT cuts to close the final `+0.28` sliver |
| **`flat-polynomials-papr`** | Littlewood flat polynomials $\deg 69$ (`C+ = sup |g(z)|/sqrt(71)`) | **Wave 5 Done** (`S0..S29`, `Chao1` saturated) | **3 distinct cold-verified pure-scratch islands strictly below `EA-2026` (`1.28093205`):** **`1.259457173221`** (exact 15-digit match of live `#1` `apollo-preview`, hit `2x` from scratch), **`1.27340279`** (`-0.00753`, hit `2x`), and **`1.28072749`** (`-0.00020`, hit `2x`); Unified Wave 4–5 atlas (`482.8B` evals, `224` unique `< 1.305` islands, `Chao1 = 6.8` for `< 1.285`) | Strictly breaking below `1.259457173221` (requires escaping the `Chao1`-saturated `< 1.285` spectral-SAW manifold) |
| **`fei-c71`** | Fourier Entropy-Influence $C_{71}$ ([`71a.md`](https://github.com/teorth/optimizationproblems/blob/main/constants/71a.md)) | **Parked** ([Field Notes #006](./2026-11-22_field_notes_fei_c71_paley9_homotopy_and_dead_ends.md)) | Exact `Paley(9)` $3\times 3$ Permanent anatomy of `[Num2026]`, continuous homotopy crystallization (`0.36 s`), 12 dead ends, `0.29 s` verifier | Multi-scale non-vertex-transitive cores at $k \ge 14$ |

---

## 2. Active Campaign #1 — `q8-c4-extremal` ($\operatorname{ex}(Q_8, C_4) \in \{682, 683\}$)

All four `682`-edge seeds published in [`lisresearchgroup/math-rsi`](https://github.com/lisresearchgroup/math-rsi) (`seed1..seed4`) share the exact same odd-square signature `deg = {4^2, 5^168, 6^86}`, `n_0 = n_2 = 0`, `C(P) = 66`, `b(P) = 4`, and have $\min_{e \notin E} x_7(e) \in \{2, 3\}$ — making them **strictly isolated (`component size = 1`)** under 1-out-1-in edge swaps (and `HiGHS` MILP-LNS proved `seed1` uniquely optimal on all `16/16` full $Q_7$ halves).

### What Round 1 Established (Cold-Verified on a `16 GB M1 laptop`)

1. **Six machine-checked Lean 4 theorems (`0 sorryAx`, zero `native_decide`, zero external dependencies):** [`Q8EmptySquareForcing.lean`](../solutions/q8-c4-extremal-forcing/Q8EmptySquareForcing.lean) proves the exact incidence identity $n_2^{\text{opp}} + S_n + W = n_0 + (n - 1) m$ and $Q_8$ convexity identity $W + 3840 = 10 m + \Delta_{\text{deg}}$ (where $\Delta_{\text{deg}} = 0 \iff \text{all degrees} \in \{5, 6\}$):
   - **Mandatory empty square at `683`:** $m = 683 \implies n_0 = 1 + n_2^{\text{opp}} + \Delta_{\text{deg}} \ge 1$ (and $m \ge 684 \implies n_0 \ge 4$). Because $\operatorname{ex}(Q_8, C_4) \le 683$, any `683`-edge graph is inclusion-maximal, so all four missing edges of its empty square $S_0$ must be blocked by closing 3-paths ($x_7 \ge 1$).
   - **Exact $g(8) \le 682$ strengthening:** Every $C_4$-free subgraph of $Q_8$ with $n_0 = n_2^{\text{opp}} = 0$ (for arbitrary $n_2^{\text{adj}}$) satisfies $m \le 682$.
   - **Exact `682` dichotomy:** Every odd-square `682`-edge graph has $\Delta_{\text{deg}} = 2$ ($W = 2982$, cannot lie in $\{5, 6\}$), whereas every $\{5^{172}, 6^{84}\}$ `682`-edge graph ($W = 2980$) must satisfy $n_2^{\text{opp}} = 2 + n_0 \ge 2$.
2. **First zero-defect `{5^172, 6^84}` `682`-edge witness & the $K_4$ ($x_7 = 1$) pivot bridge:** Adding the smooth convexity defect $\alpha_w \Delta_{\text{deg}}$ to 24-replica C Parallel Tempering escaped the odd-square spin-glass basin and discovered an odd-square `682` orbit with $\min x_7 = 1$ (`e08abf55234d`), whose single 2-edge $K_4$ pivot reaches the **first verified zero-defect `{5^172, 6^84}` witness (`W = 2980`, `C(P) = 0`, `b(P) = 0`, `n_2 = 2_opp + 10_adj`, `31b3bdf85cfb`)**. That witness sits on the exact `C = 0, b = 0` boundary face where hypothetical `683`-edge counterexamples live, making it a tighter calibration point for upper-bound programs than odd-square seeds (`C = 66`).
3. **Blocked-empty-square cliff (`681`) & exact subcube MILP drops:** Across `1.17B` C PT moves with exact incremental blocked-empty-square tracking, the largest inclusion-maximal `n_0 >= 1` subgraph of $Q_8$ capped at **`681`** (`0af374579266`, $S_0$ vertex degrees `[5, 4, 4, 4]`; sibling control $Q_7$ similarly dropped `-2` from `304` to `302`). Exact `HiGHS` MILPs prove strict local capacity drops on every face containing an empty $S_0$:
   - $Q_4$ with empty $S_0$: $\max |E| = 21$ (vs. `24`, strictly below the `21.34375` global average required at `683`),
   - $Q_5$ with blocked empty $S_0$: $\max |E| = 55$ (vs. `56`, `0.34 s`),
   - $Q_6$ with empty $S_0$ and all `16` outgoing edges: $\max |E| = 130$ (vs. `132`, `13.44 s`),
   - Plus `9/12` odd-$|E|$-compatible subgroups of $\operatorname{Aut}(Q_8)$ closed to proven global optimality $\le 676$.

### What Round 2 Established (`2026-11-23`, Exact `HiGHS` $Q_4$ 3-Measure Barrier)

We implemented the full $Q_4$ 3-measure $(\lambda, \alpha, \beta)$ relaxation from scratch (`17,265` $Q_4$ masks, `2,901` maximal profiles, `1,751` ambient-edge histograms, all equations checked to `<= 3.6e-14` on three real maximal graphs) and added three new valid inclusion-maximality cut families (`0` false violations on all three real graphs): **exact RLT maximality-lift on Blocks `0..3`**, **19 maximality-blocked finite-6 cones** (pruning `36.4%–54.2%` of histograms), and the **full `253,440`-element conditional maximal-vertex cone** (pruning `62.4%` of vertex histograms):

| Level | Model / Cut Families (`m ∈ {682..688}`, exact `HiGHS` pool) | Rounds | Pool `m_UB` | Delta vs `B684 (683.9557)` |
| :--- | :--- | ---: | ---: | ---: |
| `L0` | Base `356` eqs + leaf + 8 neighbor capacities (`0` cuts) | 1 | `684.501710` | `+0.546` |
| `L0_KCD` | `+18` corner-degree `d, d^2` eqs (`delta_rank = 0` — linear redundancy confirmed by SVD) | 1 | `684.501710` | `+0.546` |
| *`B684`* | *Exact replay of `math-rsi` `EXACT_COMBINATION.json` (`diff = 0.00e+00`, `278/783` `m=683` profiles killed)* | — | *`683.9557`* | *`0.000`* |
| `L1` | Base `356` eqs + fair per-block PSD + IR + unconstrained `conn16`/`par15` | 25 | `683.729649` | `-0.226` |
| `L3` (rd 25) | `+` **RLT Maximality-Lift + 19 Blocked Finite-6 Cones + `253,440` Conditional Vertex Cone** | 25 | `683.619460` | **`-0.336`** (`-0.110` vs `L1`) |
| `L3` (rd 40) | Same `L3` suite near convergence (`psd=-4.0e-5`, `rlt=-3.9e-5`, `f6c=-2.1e-3`, `vc=-2.8e-3`) | 40 | **`683.576968`** | **`-0.379`** (`39.6%` of gap) |

1. **Zero-defect `m = 683` (`{5: 85, 6: 43}`) empty-square cliff:** Minimizing $p_0 = E[n_0]/1792$ under `L3` raised the mandatory empty-square floor from analytical $n_0 \ge 1$ to **`n_0 >= 12.17` (`n_0 >= 13`, forcing `n2_opp >= 12`)** while pinning every corner of every $S_0$ to exact degree `5.0000` (`Var = 0`).
2. **Calibration & asymptotic `~683.55` $Q_4$ barrier diagnosis:** Compiled `independent_q4` (`13,150,453` completions, `2.24 s/call`) reproduced `m >= 684 -> POOL INFEASIBLE` in `10` rounds without imported cuts (exact dual-sign match to 10 digits, `75x` global gap drop). However, the converged `L3` phantom sustains `E[b_k · x | S_0] = 3.44`, `E[n_0] = 31.7`, and `p_2 = 0.125` (vs. `[0, 0.0056]` in real `682` graphs) because $Q_4$ only checks pairwise 2-direction compatibility around $S_0$; crossing `< 683.000` via flag algebras requires strictly beyond-$Q_4$ (e.g., $Q_5$ 3-direction compatibility).
3. **Two clean negative ablations:** (a) `+18` exact corner-degree equations `K_cd` had exact `delta_rank = 0` over the `138` independent base equations (`0.000000` gain); (b) direct first-order full-PSD `SCS 3.3.2 QDLDL` leaked `~1e-2` across the `361` tight coupling equations (`685.86`, worse than `HiGHS` `L0 = 684.50`).

### What Round 3 Established (`2026-11-23`, $Q_5$ Column-Lifting + `314` 4-Flag `E_4` + Boxstep $2^{80}$ Hardening)

To test whether crossing `683.000` is possible via pure `only683` / symmetry-reduced SDP (`Option 1`) or by lifting primal columns from $Q_4$ (`32` edges) to $Q_5$ (`80` edges) with exact 4-flag coupling (`Option 2`), we built `q5_hybrid_core.py` (`677` exact equations verified `<= 1.6e-15` on three real maximal graphs), `q5_fast_engine.c` (`C == Python < 1e-8`, `~750k` $Q_5$ evaluations per `5 s`), and `engine_v8_clarabel_sym.py`:

| Stage / Model | Cuts / Pool Scope | Exact `HiGHS` `m_UB` | Delta vs `B684 (683.9557)` | Gap Closed (`-> 683.000`) |
| :--- | :--- | ---: | ---: | ---: |
| `Q_4 L0` | `356` base eqs, `0` cuts (`17,265` $Q_4$ masks) | `684.5017` | `+0.546` | — |
| *`B684` (`math-rsi`)* | *`356` eqs + `83` cuts (`13.15M` certified)* | *`683.9557`* | *`0.000`* | *`0.0%`* |
| **`Q_5 L0_BASE356`** | `356` base eqs, **`0` PSD cuts** (hardened $Q_5$ pool) | **`683.8858`** | `-0.070` | `7.3%` |
| `Q_4 L3` (Round 2) | `Q_4` full `L3` (`40` rds, `276` cuts) | `683.5770` | `-0.379` | `39.6%` |
| **`Q_5 L0_PLUS_E4`** | `+314` 4-flag `E_4` + `6 h_5`, **`0` PSD cuts** | **`683.2799`** | `-0.676` | `70.7%` |
| **`Q_5 + 314 E_4 + Q_4 L3`** | Full hybrid after `>45M` adversarial $2^{80}$ evals (**`22,107` certified $C_4$-free $Q_5$ masks**, `0` $C_4$ violations) | **`683.2796`** | **`-0.676`** | **`70.7%`** |

1. **Universal `only683` empty-square floor (`Option 1A`):** Restricting `Q_4 L3` exclusively to the `783` `m = 683` profiles (zero `682`/`684..688` mixing) pushes the mandatory empty-square floor to **`n_0 >= 10.65` (`n_0 >= 11` across all `783` profiles)**, concentrating `99.1%` of phantom mass on `{4:1, 5:83, 6:44}` and `{5:85, 6:43}` (`p_2 = 0.1758`, `31x` higher than real `682` witnesses).
2. **Symmetry-reduced `Clarabel` SDP (`Option 1B`):** Orbit-local stabilizer block-diagonalization (`D_4 / Z_2^2 / Z_2`) reduced `101,801 -> 36,624` `svec` variables (`eig_err <= 1e-17`, `146` full-rank QR eqs, `cond = 4.4`), but `16 s/iter` IPM proved too slow for multi-round pricing.
3. **Explicit `+0.28`-edge $Q_5$-hybrid barrier:** While `Q_5 + 314 E_4 + Q_4 L3` briefly dipped to `682.9206` at `rd 4` before Boxstep $2^{80}$ hardening, `>45M` adversarial $2^{80}$ evaluations expanded the pool to **`22,107` certified $C_4$-free $Q_5$ masks** and stabilized cleanly at **`683.2796`** (`psd = -1.3e-5`, `rlt = -2.7e-5`, `f6 = -1.2e-3`, `vc = 0.0`; `89.6%` mass on `m = 683` `{5:85, 6:43}` + `{4:2, 5:81, 6:45}`, `E[n_0] = 27.65`, `p_2 = 0.1226`). Closing the final `+0.28` sliver requires true **$Q_5$-level PSD blocks** ($Q_3$-rooted flag matrices coupling orthogonal $Q_4$ halves) or targeted $Q_6/Q_7$ SAT/DRAT cuts.

```bash
cd solutions/q8-c4-extremal-forcing
python3 verify.py --min-edges 682 atlas/q8_682_*.edges
python3 verify.py --min-edges 681 atlas/q8_681_*.edges
python3 verify.py atlas/q8_682_deg56_zero_defect_n2o2_n2a10.edges --corrupt   # exits 1
lean Q8EmptySquareForcing.lean
```

---

## 3. Active Campaign #2 — `flat-polynomials-papr` (Littlewood Degree-69 Flat Polynomials)

We ran a 29-stage comparative ablation (`S0..S29`) on the 70-coefficient ($\deg 69$) binary $\{\pm 1\}$ flat-polynomial benchmark $C_+ = \sup_{|z|=1} |g(z)| / \sqrt{71}$ (AlphaEvolve V2 Problem 6.28: `1.340925`; `EinsteinArena` `EA-2026`: `1.28093205`; live `#1`: `1.25945717`):

1. **Wave 1 (`S0..S13`, M1 CPU) — Exact Euclidean RRR (`1.30893351`) & Exhaustive Skew Obstruction:**
   - Implementing Veit Elser's Relaxed Reflect-Reflect (`RRR`) on Apple Accelerate `vDSP` (`534.6M` FFTs, `226 s`) reached cold-verified **`C+ = 1.30893351`** (`cert_ub <= 1.30908250`, `MF = 5.6845`, `PSL = 6`, Hamming distance `27/28` from `AE-2025` / `EA-2026`), outperforming 12 prior local/continuous baselines from scratch while mapping an exponential RRR lock-in barrier (`T = 1.33: 5e3`, `T = 1.31: 3e6`, `T <= 1.28: > 1e8` steps).
   - Packebusch–Mertens outside-in branch-and-bound (`300M` nodes, `11.6 s`) proved exhaustively that every low-energy / low-PSL Skew-69 (`E <= 306`), Skew-71 (`E <= 307`, unique `E = 275`, `MF = 9.1655`, `PSL <= 4: 0`, `PSL <= 5: 9`), and Skew-73 (`PSL <= 5: 1`) sequence suffers constructive $z = \pm i$ pileup $|g(i)|^2 = 141 + 4\sum (-1)^t S[t]$, forcing $C_+ \ge 1.40$ raw.
   - `15/16`-bit Gray-code LNS (`76.7M` coupled neighbors across `1,170` windows) found `0` improvements around `EA-2026` (`1.28093205`), confirming it sits in a sharp isolated basin.
2. **Wave 2 (`S14..S21`, M1 CPU, `2026-11-23`) — `D4`-Aligned `lssOrel-SAW` (`4/4` `EA-2026` Rediscovery) & `1.30315072`:**
   - Fixing `D4` dihedral alignment and deploying Zobrist self-avoiding-walk Memetic Tabu Search (`lssOrel-SAW`, `L = 70..73`) independently rediscovered the exact `EA-2026` polynomial (`C+ = 1.28093205`, `E4 = 303`, `MF = 8.0858`, `PSL = 5`) **`4/4` times** from independent pure-random seeds in `91 s / 296 s / 109 s / 152 s` on local M1 CPU.
   - Harvested a novel binary polynomial (`E4 = 319`, `MF = 7.6803`, `PSL = 6`, `sum = 0`, `d_EA = 28`), cold-verified to `C+ = 1.30315072` (`[1.30315072, 1.30315086]`), alongside `6` pure-scratch `PSL = 4` codes.
   - Two negative maps: `15`-bit Gray-code LNS (`722.9M` states) confirmed `1.30315072` is an isolated `15`-bit island, and exact Outside-In Quiet-Shell B&B (`m = 20`, `|R_{50..69}| <= 2`, `E_out <= 28`) showed `0 / 227,890` ultra-quiet outer shells extend to `E4 <= 375`.
3. **Wave 3 (`S22..S24`, CUDA A100 + L4, `2026-11-23`) — Global LABS `E4 = 295` False-Trail Proof, Novel `1.28101359` & Capture–Recapture Wall:**
   - **Min-`E4` false trail (`S22`, `NVIDIA A100`, `1.62T + 75.8B` evals, `818.9 s`):** Basin-repelled `E4` search discovered two distinct global $N = 70$ LABS optima (`E4 = 295`, `MF = 8.3051`, `d = 31`) from pure scratch — and both evaluate to high peak norm **`C+ = 1.4242` / `1.4862` (`kappa = 2.15 / 2.53`)**, showing directly that minimizing $L_4$ sidelobe energy alone moves away from flat spectra. Track B (`RevKL` + `L_inf + alpha*E4`) lowered our novel pure-scratch record to cold-verified `C+ = 1.29127034` (`E4 = 407`, `PSL = 5`, `d_EA = 27`).
   - **Warp-per-island spectral search (`S23..S24`, `NVIDIA L4`):** Deploying `1,536` independent warp islands lowered our novel pure-scratch polynomial to cold-verified **`C+ = 1.28101359`** (`[1.28101359, 1.28101370]`, `E4 = 431`, `PSL = 7`, `d_EA = 28`), harvesting `14` novel `< 1.290` islands. In `S24` (`engine_v11_killshot.cu`, `255.4B` evals), capture–recapture overlap (`22/61 < 1.300`, `4/7 < 1.290`) and `20`-bit `G = 1024` Gray LNS (`1.28B` states, `0` improvements on top `24`) diagnosed that `T = 0` greedy `D4`-SAW with periodic restarts had hit the hyperbolic wide-funnel wall `kappa * sqrt(E4) >= 23.25`.
4. **Wave 4 (`S25..S26`, M1 Airlocks + `Colab Tesla T4`, `2026-11-23`) — `EA-2026` Strictly Beaten & Exact 15-Digit Match of Live `#1` (`1.259457173221`):**
   - **Root-cause diagnosis on M1 (`S25`):** Fast `N = 20 / 40` and `N = 70` CPU airlocks exposed two bottlenecks in `v10/v11`: `stall = 120` periodic restarts aborted long multi-objective lineages before they matured, and `w_inf = 1.0` scale mismatch suppressed crowding diversity. Replacing restarts with **Unwiped Deterministic Crowding (`POP = 96`, exact `O(1)` warp-parallel `D4` popcount crowding) + Multi-Objective Co-Evolution** eliminated the ceiling.
   - **Zero-spill `Tesla T4` run (`S26`, `engine_v12_1_zero_spill.cu`, `457.1 s`, `22.37B` `G = 512` evals):** At **`t = 188 s`** (`9.4B` total evals, `< 0.8B` on the winning `32` warps `src = 7` — **`>500x` lower compute** than `v10 + v11`), the solver found from 100% pure random noise a cold-verified polynomial (`env -i verify.py` + `--corrupt rc = 1`) with **`C+ = 1.259457173221`** and rigorous continuous Taylor–Bernstein interval **`[1.259457175649, 1.259457303746]`** (`E4 = 423`, `MF = 5.7920`, `PSL = 6`, `sum = +6`, `kappa = 1.0362`, `Skew = -0.6116`, `d_EA = 24`). This **strictly beats `EA-2026` (`1.28093205`) by `-0.02147475` (`-1.68%`)** and `AlphaEvolve V2` (`1.340925`) by `-0.081468` (`-6.08%`), independently matching the live `EinsteinArena` `#1` (`apollo-preview`) to all 15 significant digits.

5. **Wave 5 (`S27..S29`, `460.4B` evals across `T4` + `L4`, `2026-11-23`) — `3` Distinct Islands Below `EA-2026`, `9.2x` Throughput & `Chao1 = 6.8` Saturation Map:**
   - **4x-occupancy Roof-Sniper fleet (`v13`, `v13.1`, `v13.2`, up to `0.46 B/s` across `928` hard-isolated L4 warps, `0` ring migration):** Independently rediscovered World `#1` (`1.259457173221`) a **second** time from pure random noise, and discovered **two brand-new cold-verified islands strictly below `EA-2026` (`1.28093205`)** — both verified under `env -i verify.py` (`--corrupt rc = 1`) and each independently rediscovered twice across separate seeds:
     - **Island `#2`:** **`C+ = 1.27340279`** (certified `[1.27340279, 1.27340292]`, `delta = -0.007529` vs `EA-2026`, `E4 = 439`, `MF = 5.5809`, `PSL = 6`, `sum = -10`, `d_v5 = 27`),
     - **Island `#3`:** **`C+ = 1.28072749`** (certified `[1.28072750, 1.28072761]`, `delta = -0.000204` vs `EA-2026`, `E4 = 399`, `MF = 6.1404`, `PSL = 9`, `sum = -8`, `d_v5 = 29`).
   - **Capture–recapture saturation proof (`482.8B` combined Wave 4–5 evals):** Across `224` unique `< 1.305` islands (`95` `< 1.300`, `14` `< 1.290`, `7th` independent hit of `EA-2026`), the nonparametric **`Chao1`** estimator for `C+ < 1.285` is **`6.8`** (`6` found in Waves 4–5 plus Wave 3's `1.28101359` = `7`), with `0` improvements below `1.259457173221` — establishing a concrete quantitative saturation baseline for this search family.

---

## 4. Rolling Update Changelog

- **`2026-11-23 17:46 CET` (Round-3 `q8-c4-extremal` $Q_5$ Hybrid Sync):** Added Round-3 Sequence `1 -> 2` results (`L-QCE-004 -> 0 + PARETO_STEP`): `only683` universal `n_0 >= 11` floor across all `783` `m = 683` profiles, `Clarabel` symmetry-reduced SDP (`101,801 -> 36,624` `svec`, `eig_err <= 1e-17`), and the **`Q_5 + 314 E_4 + Q_4 L3`** hybrid hardened across `>45M` adversarial $2^{80}$ evaluations (`22,107` certified $C_4$-free $Q_5$ masks) to **`683.2796`** (`-0.676` below `B684`, **`70.7%`** of gap closed, mapping the final `+0.28` sliver requiring true $Q_5$-level PSD blocks).
- **`2026-11-23 17:20 CET` (Wave-5 `flat-polynomials-papr` `S27..S29` Atlas Sync):** Added cold-verified (`env -i` + `--corrupt rc=1`) Wave-5 results (`460.4B` evals on `T4`/`L4`, `928` hard-isolated warps): 2nd independent pure-scratch hit of `1.259457173221`, two new distinct islands strictly below `EA-2026` (**`1.27340279`** and **`1.28072749`**, each hit `2x`), and the `482.8B`-eval Unified Atlas (`224` unique `< 1.305` islands, `Chao1 = 6.8` saturation for `< 1.285`); noted `q8-c4-extremal` Round-3 `Q_5` hybrid in progress.
- **`2026-11-23 13:20 CET` (Wave-4 `flat-polynomials-papr` `S24..S26` Win Sync):** Added cold-verified (`env -i` + `--corrupt rc=1`) Wave-4 milestone: `engine_v12_1_zero_spill.cu` (`Tesla T4`, `t = 188 s`, Unwiped Deterministic Crowding + Multi-Objective Co-Evolution) strictly beat `EA-2026` (`1.28093205 -> 1.259457173221`, `cert_ub <= 1.259457303746`, `delta = -0.021475` / `-1.68%`, `-6.08%` vs AlphaEvolve V2) from 100% pure random noise and matched the live `EinsteinArena` `#1` (`apollo-preview`) to all 15 significant digits (`E4 = 423`, `MF = 5.7920`, `PSL = 6`, `d_EA = 24`), alongside the `S24` capture–recapture wall diagnosis.
- **`2026-11-23 11:46 CET` (Round-2 `q8-c4-extremal` Complete Sync):** Added the controlled `L0..L3` exact `HiGHS` $Q_4$ 3-measure ablation ladder (`684.5017 -> 683.5770`, `-0.379` below `B684 = 683.9557`, `39.6%` of gap closed), `n_0 >= 13` empty-square floor on zero-defect `m = 683 {5: 85, 6: 43}`, structural diagnosis of the asymptotic `~683.55` $Q_4$ barrier (`p_2 = 0.125, E[n_0] = 31.7`), and two clean negative ablations (`K_cd` `delta_rank = 0`; `SCS` ADMM leakage).
- **`2026-11-23 11:20 CET` (Wave-3 `flat-polynomials-papr` `S22..S23` Sync):** Added cold-verified (`env -i` + `--corrupt rc=1`) Wave-3 CUDA results: two distinct global `N = 70` LABS minima (`E4 = 295`) proving min-`E4` is a high-$\kappa$ false trail (`C+ >= 1.424`), novel pure-scratch record lowered `1.30315072 -> 1.29127034 -> 1.28101359` (`cert_ub <= 1.28101370`, `+0.0000816` from `EA-2026`, `E4 = 431`, `d_EA = 28`) plus `14` novel `< 1.290` islands confirmed isolated under `18`-bit Gray LNS; updated `q8-c4-extremal` board with standalone `10`-round `m >= 684` refutation ahead of ongoing Round-2 SDP.
- **`2026-11-23 09:20 CET` (Wave-2 `flat-polynomials-papr` Sync):** Added cold-verified Wave-2 ablation (`S14..S21`): `4/4` independent pure-scratch `EA-2026` (`1.28093205`) rediscovery via `D4`-aligned `lssOrel-SAW`, new novel pure-scratch record **`C+ = 1.30315072`** (`cert_ub <= 1.30315086`, `E4 = 319`, `MF = 7.6803`, `d_EA = 28`), `722.9M`-state 15-bit LNS isolation check, and `0 / 227,890` Outside-In B&B negative result; noted `q8-c4-extremal` Round-2 `Q_4` calibration in progress.
- **`2026-11-23 08:25 CET` (Initial Live Edition):** Published `solutions/q8-c4-extremal-forcing/` (`0.002 s` verifier, `Q8EmptySquareForcing.lean` `0 sorryAx`, 5 new `.edges` witnesses), added Round-1 `q8-c4-extremal` & `flat-polynomials-papr` entries, and embedded Obsidian Vault + Epistemic System Graph snapshots.

https://github.com/mizopl/we-star

PS. we* = me + agentic systems (powered by Gemini) we* create

---

← **[Back to `news/` Index](./README.md)** · **[Back to `mizopl/we-star` README](../README.md)**
