# Field Notes #007 (`LIVE` Rolling Log) — Ongoing Campaigns: `ex(Q_8, C_4) ∈ {682, 683}` & Littlewood Flat Polynomials (`deg 69`)

> **Status:** `LIVE` Rolling Lab Notebook · **Last Updated:** `2026-11-23 11:46 CET` · **Authors:** `@mizopl` & **`we*`** (`PROOFER` Open-Science Lab)  
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

1. **`ex(Q_8, C_4) ∈ {682, 683}` remains OPEN:** We neither constructed a $683$-edge $C_4$-free subgraph of $Q_8$ nor proved $\operatorname{ex}(Q_8, C_4) \le 682$. In Round 2, our full $Q_4$ 3-measure $(\lambda, \alpha, \beta)$ exact `HiGHS` cutting-plane relaxation (`17,265` $Q_4$ masks) tightened the pool bound by `-0.379` edges below [`lisresearchgroup/math-rsi`](https://github.com/lisresearchgroup/math-rsi)'s `B684` (`683.9557 -> 683.5770`, closing `39.6%` of the gap to `683.000`), but converged asymptotically near **`~683.55`** — proving that $Q_4$-level 3-measure cuts cannot cross `683.000` (closing the remaining `~0.55` requires strictly beyond-$Q_4$ 3-direction compatibility). All `683.5770` and `n_0 >= 12.17` figures are exact `HiGHS` pool bounds (`17,265` masks; verified against the `13.15M` oracle on `m >= 684`), and our Lean 4 file proves elementary double-counting identities on `C4FreeCounts`, not the global `<= 682` bound.
2. **Degree-69 Littlewood flat polynomials (`flat-polynomials-papr`) remain OPEN:** Neither our CPU ablations nor our CUDA warp-spectral sweeps strictly beat the published `EinsteinArena` bound (`EA-2026`, `1.28093205`) or the live leaderboard entry (`1.25945717`). Our `D4`-aligned `lssOrel-SAW` search independently rediscovered the exact `EA-2026` sequence (`1.28093205`) `4/4` times from pure random seeds, and our latest **novel** pure-scratch polynomial (`E4 = 431`, `PSL = 7`, `d_EA = 28`) dropped further from `1.30315072` -> `1.29127034` -> cold-verified **`C+ = 1.28101359`** (certified continuous Taylor–Bernstein interval `[1.28101359, 1.28101370]`, `-4.47%` below AlphaEvolve V2 `1.340925`), which still sits `+0.0000816` above `EA-2026` and `+0.02156` above live `#1`.
3. **Zero stealth items listed:** Any offline or competition-embargoed work is excluded from this public log.

---

## 1. Live Public Campaign Board (`2026-11-23 11:46 CET`)

| Campaign | Problem & Benchmark | Current Stage | Verified Milestone (`-0 Hype`) | Next Open Frontier |
| :--- | :--- | :--- | :--- | :--- |
| **`q8-c4-extremal`** | Erdős #86: $\operatorname{ex}(Q_8, C_4) \in \{682, 683\}$ ([`math-rsi`](https://github.com/lisresearchgroup/math-rsi)) | **Round 2 Done** (awaiting Round-3 fork) | `6/6` zero-axiom Lean 4 forcing theorems + first zero-defect `{5^172, 6^84}` `682` witness; Round-2 `Q_4` 3-measure `L3` (`HiGHS`, `17,265` masks + RLT + 19 blocked finite-6 cones + `253,440` vertex cone) hit **`683.5770`** (`-0.379` below `B684 = 683.9557`, `39.6%` of gap) and forced `n_0 >= 13` on `{5:85, 6:43}`, mapping the **`~683.55` `Q_4` barrier** | Strictly beyond-$Q_4$ (`Q_5` 3-direction compatibility around $S_0$ / 2-edge squares) to kill the `p_2 = 0.125, E[n_0] = 31.7` pairwise phantom |
| **`flat-polynomials-papr`** | Littlewood flat polynomials $\deg 69$ (`C+ = sup |g(z)|/sqrt(71)`) | **Active** (`23` ablations `S0..S23`) | Cold-verified novel pure-scratch polynomial **`C+ = 1.28101359`** (`ub <= 1.28101370`, `+0.0000816` from `EA-2026`, `E4=431`, `PSL=7`, `d_EA=28`) + `14` novel `< 1.290` islands (`NVIDIA L4`, `7.5 min`); `4/4` independent `EA-2026` rediscovery; two distinct global `N=70` LABS minima (`E4=295`, `MF=8.3051`) have `C+ >= 1.424` (proving min-`E4` is a high-$\kappa$ false trail) | Breaking strictly below `1.28093205` (`EA-2026`) and `1.25945717` (`#1`) |
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

```bash
cd solutions/q8-c4-extremal-forcing
python3 verify.py --min-edges 682 atlas/q8_682_*.edges
python3 verify.py --min-edges 681 atlas/q8_681_*.edges
python3 verify.py atlas/q8_682_deg56_zero_defect_n2o2_n2a10.edges --corrupt   # exits 1
lean Q8EmptySquareForcing.lean
```

---

## 3. Diagnostic Campaign #2 — `flat-polynomials-papr` (Littlewood Degree-69 Flat Polynomials)

We ran a 23-stage comparative ablation (`S0..S23`) on the 70-coefficient ($\deg 69$) binary $\{\pm 1\}$ flat-polynomial benchmark $C_+ = \sup_{|z|=1} |g(z)| / \sqrt{71}$ (AlphaEvolve V2 Problem 6.28: `1.340925`; `EinsteinArena` `EA-2026`: `1.28093205`; live `#1`: `1.25945717`):

1. **Wave 1 (`S0..S13`, M1 CPU) — Exact Euclidean RRR (`1.30893351`) & Exhaustive Skew Obstruction:**
   - Implementing Veit Elser's Relaxed Reflect-Reflect (`RRR`) on Apple Accelerate `vDSP` (`534.6M` FFTs, `226 s`) reached cold-verified **`C+ = 1.30893351`** (`cert_ub <= 1.30908250`, `MF = 5.6845`, `PSL = 6`, Hamming distance `27/28` from `AE-2025` / `EA-2026`), outperforming 12 prior local/continuous baselines from scratch while mapping an exponential RRR lock-in barrier (`T = 1.33: 5e3`, `T = 1.31: 3e6`, `T <= 1.28: > 1e8` steps).
   - Packebusch–Mertens outside-in branch-and-bound (`300M` nodes, `11.6 s`) proved exhaustively that every low-energy / low-PSL Skew-69 (`E <= 306`), Skew-71 (`E <= 307`, unique `E = 275`, `MF = 9.1655`, `PSL <= 4: 0`, `PSL <= 5: 9`), and Skew-73 (`PSL <= 5: 1`) sequence suffers constructive $z = \pm i$ pileup $|g(i)|^2 = 141 + 4\sum (-1)^t S[t]$, forcing $C_+ \ge 1.40$ raw.
   - `15/16`-bit Gray-code LNS (`76.7M` coupled neighbors across `1,170` windows) found `0` improvements around `EA-2026` (`1.28093205`), confirming it sits in a sharp isolated basin.
2. **Wave 2 (`S14..S21`, M1 CPU, `2026-11-23`) — `D4`-Aligned `lssOrel-SAW` (`4/4` `EA-2026` Rediscovery) & `1.30315072`:**
   - Fixing `D4` dihedral alignment and deploying Zobrist self-avoiding-walk Memetic Tabu Search (`lssOrel-SAW`, `L = 70..73`) independently rediscovered the exact `EA-2026` polynomial (`C+ = 1.28093205`, `E4 = 303`, `MF = 8.0858`, `PSL = 5`) **`4/4` times** from independent pure-random seeds in `91 s / 296 s / 109 s / 152 s` on local M1 CPU.
   - Harvested a novel binary polynomial (`E4 = 319`, `MF = 7.6803`, `PSL = 6`, `sum = 0`, `d_EA = 28`), cold-verified to `C+ = 1.30315072` (`[1.30315072, 1.30315086]`), alongside `6` pure-scratch `PSL = 4` codes.
   - Two negative maps: `15`-bit Gray-code LNS (`722.9M` states) confirmed `1.30315072` is an isolated `15`-bit island, and exact Outside-In Quiet-Shell B&B (`m = 20`, `|R_{50..69}| <= 2`, `E_out <= 28`) showed `0 / 227,890` ultra-quiet outer shells extend to `E4 <= 375`.
3. **Wave 3 (`S22..S23`, CUDA A100 + L4, `2026-11-23`) — Global LABS `E4 = 295` False-Trail Proof & Novel `1.28101359` (`+0.0000816` from `EA-2026`):**
   - **Min-`E4` false trail (`S22`, `NVIDIA A100`, `1.62T + 75.8B` evals, `818.9 s`):** Basin-repelled `E4` search discovered two distinct global $N = 70$ LABS optima (`E4 = 295`, `MF = 8.3051`, `d = 31`) from pure scratch — and both evaluate to high peak norm **`C+ = 1.4242` / `1.4862` (`kappa = 2.15 / 2.53`)**, showing directly that minimizing $L_4$ sidelobe energy alone moves away from flat spectra. Track B (`RevKL` + `L_inf + alpha*E4`) lowered our novel pure-scratch record to cold-verified **`C+ = 1.29127034`** (`[1.29127035, 1.29127046]`, `E4 = 407`, `PSL = 5`, `d_EA = 27`).
   - **Warp-per-island spectral search (`S23`, `NVIDIA L4`, `225.9B` `G = 512` evals, `450 s`, zero `__syncthreads()`):** Deploying `1,536` independent warp islands (`RevKL`, `Hinge^2 + L_inf`, `VOTE.ANY` hybrid reshapers + one-sided `E4`-belt wall) lowered our novel pure-scratch polynomial to cold-verified **`C+ = 1.28101359`** (rigorous Taylor–Bernstein interval **`[1.28101359, 1.28101370]`**, `E4 = 431`, `MF = 5.6845`, `PSL = 7`, `sum = -8`, `d_EA = 28` — **`-0.0599` / `-4.47%` below AlphaEvolve V2 `1.340925`**, and **`+0.0000816`** above `EA-2026` `1.28093205`), harvesting **`14` novel `< 1.290`** and **`162` novel `< 1.305`** islands in `7.5 min`. All top `32` islands were checked with `18`-bit Gray-code LNS (`0.30 s`, `0` improvements) and `54,740` 3-bit neighbors (`0` improvements), confirming every top candidate sits in an isolated `18`-bit basin.

---

## 4. Rolling Update Changelog

- **`2026-11-23 11:46 CET` (Round-2 `q8-c4-extremal` Complete Sync):** Added the controlled `L0..L3` exact `HiGHS` $Q_4$ 3-measure ablation ladder (`684.5017 -> 683.5770`, `-0.379` below `B684 = 683.9557`, `39.6%` of gap closed), `n_0 >= 13` empty-square floor on zero-defect `m = 683 {5: 85, 6: 43}`, structural diagnosis of the asymptotic `~683.55` $Q_4$ barrier (`p_2 = 0.125, E[n_0] = 31.7`), and two clean negative ablations (`K_cd` `delta_rank = 0`; `SCS` ADMM leakage).
- **`2026-11-23 11:20 CET` (Wave-3 `flat-polynomials-papr` `S22..S23` Sync):** Added cold-verified (`env -i` + `--corrupt rc=1`) Wave-3 CUDA results: two distinct global `N = 70` LABS minima (`E4 = 295`) proving min-`E4` is a high-$\kappa$ false trail (`C+ >= 1.424`), novel pure-scratch record lowered `1.30315072 -> 1.29127034 -> 1.28101359` (`cert_ub <= 1.28101370`, `+0.0000816` from `EA-2026`, `E4 = 431`, `d_EA = 28`) plus `14` novel `< 1.290` islands confirmed isolated under `18`-bit Gray LNS; updated `q8-c4-extremal` board with standalone `10`-round `m >= 684` refutation ahead of ongoing Round-2 SDP.
- **`2026-11-23 09:20 CET` (Wave-2 `flat-polynomials-papr` Sync):** Added cold-verified Wave-2 ablation (`S14..S21`): `4/4` independent pure-scratch `EA-2026` (`1.28093205`) rediscovery via `D4`-aligned `lssOrel-SAW`, new novel pure-scratch record **`C+ = 1.30315072`** (`cert_ub <= 1.30315086`, `E4 = 319`, `MF = 7.6803`, `d_EA = 28`), `722.9M`-state 15-bit LNS isolation check, and `0 / 227,890` Outside-In B&B negative result; noted `q8-c4-extremal` Round-2 `Q_4` calibration in progress.
- **`2026-11-23 08:25 CET` (Initial Live Edition):** Published `solutions/q8-c4-extremal-forcing/` (`0.002 s` verifier, `Q8EmptySquareForcing.lean` `0 sorryAx`, 5 new `.edges` witnesses), added Round-1 `q8-c4-extremal` & `flat-polynomials-papr` entries, and embedded Obsidian Vault + Epistemic System Graph snapshots.

https://github.com/mizopl/we-star

PS. we* = me + agentic systems (powered by Gemini) we* create

---

← **[Back to `news/` Index](./README.md)** · **[Back to `mizopl/we-star` README](../README.md)**
