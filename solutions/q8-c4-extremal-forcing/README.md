# `q8-c4-extremal-forcing` — Lean 4 Empty-Square Forcing, $\mathbb{F}_2$ Gauge-Defect Exclusions, $Q_5$-PSD Barrier & 10-Witness Atlas for $\operatorname{ex}(Q_8, C_4) \in \{682, 683\}$

> **Status:** Complete Structural & Barrier Archive (`PARKED` after Rounds 1–6 + $\mathbb{F}_2$ Gauge-Defect Audit · `ex(Q_8, C_4) ∈ {682, 683}` remains **OPEN**)  
> **Cold Verifier:** [`verify.py`](./verify.py) (`~0.03 s` total under `env -i`, verifies all 10 witnesses + Degree-Blocking Identity + 14-orbit Case 5A exclusion; `--corrupt` exits `1`)  
> **Lean 4:** [`Q8EmptySquareForcing.lean`](./Q8EmptySquareForcing.lean) (`Lean 4 v4.35.0`, `0 sorryAx`, zero `native_decide`, zero external dependencies)  
> **Companion Dispatch:** [Field Notes #007](../../news/2026-11-23_field_notes_ongoing_campaigns.md)

---

## Limitations First (`-0 Hype`)

1. **Main open problem remains OPEN:** We neither constructed a $683$-edge $C_4$-free subgraph of $Q_8$ nor proved $\operatorname{ex}(Q_8, C_4) \le 682$ (Erdős Problem #86 in dimension $8$).
2. **Scope of Lean 4 & $\mathbb{F}_2$ algebraic theorems:** [`Q8EmptySquareForcing.lean`](./Q8EmptySquareForcing.lean) formalizes six double-counting & convexity identities on `C4FreeCounts` ($n_0 \ge 1$ at $683$, $n_0 \ge 4$ at $\ge 684$, $g(8) \le 682$, and the `682` dichotomy); our $\mathbb{F}_2$ gauge-defect theorems exclude all even $|\delta|$, $|\delta| = 1, 3$, and Case 5A ($|\delta| = 5, a = 3, r = 2, |E(H_0)| = 682$), leaving Case 5B ($a = 4, r = 1, |E(H_0)| = 680$) and odd $|\delta| \ge 7$ open. None of these proves $\operatorname{ex}(Q_8, C_4) \le 682$ globally.
3. **Scope of $Q_5$-PSD + $Q_3$-RLT and construction bounds:** Our $Q_4$ (`683.5770`), $Q_5$-hybrid (`683.2796`), and $Q_5$-PSD (`683.1809`) numbers are exact `HiGHS` LP pool bounds over adversarially hardened $C_4$-free pools (up to `31,571+` certified `0`-$C_4$ $Q_5$ masks), not global $2^{80}$ branch-and-bound exhaustions — and in direct `m ∈ {682, 683}` separation, `m = 683.000000` strictly survived $Q_5$-PSD + $Q_3$-RLT (`slk_ub = 0`), establishing that $Q_5$-level PSD+RLT alone does **not** refute `683`. Likewise, our `5.94B` C bipartite-seam moves (`3.02B` PT + `1.28B` phantom barriers + `1.64B` far-spin-glass), `209.7M` exact $\operatorname{Aut}(Q_7)$ gluings, `64/64` exact $Q_7$-half MILP-LNS windows, and `24` ruled-out $\operatorname{Aut}(Q_8)$ subgroups do not constitute a global non-existence proof.
4. **Prior art credited explicitly:** Lower bound $\ge 682$ due to Marinari–Parisi–Ritort (1995), Minamo Minamoto (`arXiv:2603.29127v5`, $g(8) = 682$), and [`lisresearchgroup/math-rsi`](https://github.com/lisresearchgroup/math-rsi) (`archive/q8-683/`, `seed1..seed4`); upper bound $\le 683$ due to `lisresearchgroup/math-rsi` (`B684_EXCLUSION.md`, Nov 2026).

---

## 1. Exact Machine-Checked Theorems

### A. Empty-Square Forcing & `682` Dichotomy (`Q8EmptySquareForcing.lean`, `0 sorryAx`)
For any $C_4$-free spanning subgraph $H \subseteq Q_n$ with $m = |E(H)|$, wedge sum $W = \sum_v \binom{\deg(v)}{2}$, square counts $(n_0, n_1, n_2^{\text{opp}}, n_2^{\text{adj}}, n_3)$ summing to $S_n = \binom{n}{2} 2^{n-2}$, and $Q_8$ convexity defect $\Delta_{\text{deg}} = \sum_{v \in Q_8} (\binom{\deg(v)}{2} + 15 - 5\deg(v)) \ge 0$ ($\Delta_{\text{deg}} = 0 \iff \forall v,\ \deg(v) \in \{5, 6\}$):
- **Identity (`empty_square_forcing_identity`, `q8_convexity_identity`):** $n_2^{\text{opp}} + S_n + W = n_0 + (n - 1) m$ and $W + 3840 = 10 m + \Delta_{\text{deg}}$.
- **Mandatory empty squares (`q8_683_forces_empty_square`, `q8_ge684_forces_empty_squares`):** $m = 683 \implies n_0 = 1 + n_2^{\text{opp}} + \Delta_{\text{deg}} \ge 1$; $m \ge 684 \implies n_0 \ge 4$.
- **Exact odd-square cap (`q8_odd_square_upper_682`):** $n_0 = n_2^{\text{opp}} = 0 \implies m \le 682$ (giving a 5-line proof of $g(8) \le 682$ independent of arbitrary $n_2^{\text{adj}}$).
- **Exact `682` dichotomy (`q8_682_odd_square_forces_defect_2`, `q8_682_deg56_forces_n2_opp_ge_2`):** Every odd-square `682` has $\Delta_{\text{deg}} = 2$ ($W = 2982$, cannot lie in $\{5, 6\}$), while every $\{5^{172}, 6^{84}\}$ `682` ($W = 2980$) must satisfy $n_2^{\text{opp}} = 2 + n_0 \ge 2$.

### B. $\mathbb{F}_2$ Gauge-Defect Decomposition ($H = H_0 \oplus \delta$) & Exhaustive Case 5A Exclusion (`verify.py`)
Since $H^1(Q_8; \mathbb{F}_2) = 0$, every odd-square subgraph lies in the affine spin-glass coset $\mathcal{O}_8 = \{x_{\text{ref}} \oplus d_1(\phi) : \phi \in \mathbb{F}_2^{V(Q_8)}\}$ (where $x_{\text{ref}}(u, u \oplus e_i) = \bigoplus_{j < i} u_j$, every $H_0 \in \mathcal{O}_8$ is automatically $C_4$-free and satisfies $|E(H_0)| \le 682$). Writing any $C_4$-free $H = H_0 \oplus \delta$ with $A = H \setminus H_0$ (`a` added) and $R = H_0 \setminus H$ (`r` removed, $|\delta| = a + r$):
1. **Coboundary bound:** $|d_2(\delta)| = n_{\text{even}}(H) = n_0 + n_2^{\text{opp}} + n_2^{\text{adj}} \le 7|\delta| \implies |\delta_{\min}(H)| \ge \lceil n_{\text{even}}(H) / 7 \rceil$.
2. **Parity theorem (all even $|\delta|$ impossible for `683`):** Every $H_0 \in \mathcal{O}_8$ satisfies $2 n_3 = 7|E(H_0)| - 1792$, so $|E(H_0)|$ is always **even**. Hence any `683`-edge graph has **odd** $|\delta|$.
3. **Degree-Blocking Identity & pure-algebra $|\delta| = 3$ exclusion:** For every missing edge $e = (u, v) \notin H_0$ of any $H_0 \in \mathcal{O}_8$, letting $b_{H_0}(e)$ be the number of 3-squares of $H_0$ containing $e$ and $q_{\text{opp}}(e)$ the number of 1-squares of $H_0$ containing $e$ whose unique edge is opposite to $e$,
   $$\deg_{H_0}(u) + \deg_{H_0}(v) = 7 + b_{H_0}(e) - q_{\text{opp}}(e) \le 7 + b_{H_0}(e).$$
   For $|\delta| = 3$ ($a = 2, r = 1, |E(H_0)| = 682$), both added edges must be unblocked by the single removed edge $f \implies b_{H_0}(e_i) \le 1 \implies \deg(u_i) + \deg(v_i) \le 8$. Since $\Delta_{\text{deg}}(H_0) = 2$ forbids degrees $\le 3$ and allows at most two degree-4 vertices in all of $Q_8$, both $e_1$ and $e_2$ must join the same unique pair of degree-4 vertices ($e_1 = e_2$), contradiction. Thus **every `683`-edge graph has odd $|\delta| \ge 5$ relative to every $H_0 \in \mathcal{O}_8$**.
4. **Exhaustive Case 5A exclusion (`verify.py`, `0.004 s`):** Across all `14/14` exact $\operatorname{Stab}_{\operatorname{Aut}(Q_8)}(f_1)$ orbits covering all `1,023` pairs $(f_1, f_2)$, spin-flip minimality ($|\delta \cap \operatorname{star}(v)| \le 4$), $|D_4| \le 2$, and the forced 3-square rule eliminate **all triples (`0` survivors)** — proving **no `683`-edge $C_4$-free graph lies within Hamming distance `5` of any `682`-edge odd-square graph**.

---

## 2. Cold-Verified 10-Witness Inclusion-Maximal Atlas (`atlas/*.edges`)

All `10/10` witnesses are cold-verified `C4 = 0`, `inclusion_maximal = True` (`env -i python3 verify.py`), with exact minimal $\mathbb{F}_2$ gauge defect $|\delta_{\min}|$ computed by exact `HiGHS` MILP (`st = 0`):

| Witness (`atlas/`) | $|E|$ | Odd-Sq | Degree Sequence | Squares $(n_0, n_1, n_2^{\text{opp}}+n_2^{\text{adj}}, n_3)$ | $W$ ($+\Delta$) | Exact $|\delta_{\min}|$ (`|H_0|`, `+a/-r`) | SHA-256 (12 hex) |
| :--- | ---: | :---: | :--- | :--- | :---: | :--- | :--- |
| `q8_682_odd_x7min1_pivot_bridge.edges` | **682** | Yes | $\{4^2, 5^{168}, 6^{86}\}$ | `(0, 301, 0+0, 1491)` | `2982 (+2)` | `0` (`682`, `+0/-0`) · $\min x_7 = 1$ bridge | `e08abf55234d` |
| `q8_682_odd_deg7_vertex.edges` | **682** | Yes | $\{4^1, 5^{171}, 6^{83}, 7^1\}$ | `(0, 301, 0+0, 1491)` | `2982 (+2)` | `0` (`682`, `+0/-0`) · asymm. bip., $\nu=37$ | `eb026494fedc` |
| `q8_682_deg56_zero_defect_n2o2_n2a10.edges` | **682** | **No** | **$\{5^{172}, 6^{84}\}$** | `(0, 295, 2+10, 1485)` | **`2980 (+0)`** | `2` (`682`, `+1/-1`) · $C(P)=b(P)=0$ | `31b3bdf85cfb` |
| `q8_682_deg41_nonodd_n2o1_n2a11.edges` | **682** | No | $\{4^1, 5^{170}, 6^{85}\}$ | `(0, 295, 1+11, 1485)` | `2981 (+1)` | `2` (`682`, `+1/-1`) | `d9f494b089a6` |
| `q8_682_deg42_nonodd_n2o0_n2a12.edges` | **682** | No | $\{4^2, 5^{168}, 6^{86}\}$ | `(0, 295, 0+12, 1485)` | `2982 (+2)` | `2` (`682`, `+1/-1`) | `133531616e98` |
| `q8_681_maximal_blocked_empty_sq_n0_1.edges` | **681** | No | $\{4^4, 5^{166}, 6^{86}\}$ | **`(1, 295, 2+14, 1480)`** | `2974 (+4)` | `3` (`682`, `+1/-2`) · $S_0$ degs `[5,4,4,4]` | `0af374579266` |
| `q8_680_maximal_blocked_n0_2_n2a_24.edges` | **680** | No | $\{4^6, 5^{164}, 6^{86}\}$ | `(2, 291, 4+24, 1471)` | `2966 (+6)` | `6` (`680`, `+3/-3`) · `16/16` $Q_7$ opt `≤680` | `a9a21b8bf56f` |
| `q8_678_maximal_blocked_n0_5_n2a_21.edges` | **678** | No | $\{4^{10}, 5^{161}, 6^{84}, 7^1\}$ | `(5, 293, 8+21, 1465)` | `2951 (+11)` | `6` (`680`, `+2/-4`) | `0068718824c4` |
| `q8_678_maximal_high_n2a_78_n0_0.edges` | **678** | No | $\{4^8, 5^{164}, 6^{84}\}$ | `(0, 273, 6+78, 1435)` | `2948 (+8)` | `18` (`680`, `+8/-10`) | `7e5ad9fb2310` |
| `q8_675_maximal_phantom_n0_4_n2a_94.edges` | **675** | No | $\{4^{11}, 5^{165}, 6^{79}, 7^1\}$ | `(4, 265, 15+94, 1414)` | `2922 (+12)` | `23` (`678`, `+10/-13`) · `-8` vs $Q_5$ phantom | `6e484827d543` |

---

## 3. Summary of Mapped Obstruction & Construction Barriers (Rounds 1–6)

- **$Q_4 \to Q_5$-Hybrid $\to Q_5$-PSD+RLT Escalation (`HiGHS` exact simplex, Boxstep $2^{80}$ hardened):**
  - `math-rsi B684` baseline: **`683.9557`** (`0.0%` of gap to `683.000`).
  - `Q_4 L3` (RLT maximality-lift + `19` blocked finite-6 cones + `253,440` conditional vertex cone): **`683.5770`** (`39.6%` of gap); pure `m = 683` forced **`n_0 >= 11`** across all `783` profiles (`n_0 >= 13` on `{5:85, 6:43}`).
  - `Q_5 + 314 E_4 + Q_4 L3` (`22,107` certified `0`-$C_4$ $Q_5$ masks): **`683.2796`** (`70.7%` of gap).
  - `Q_5 + 314 E_4 + Q_5-PSD + Q_4 L3` (`Q3-Pairs`, `Q2-Cubic`, `Q2-Cubic Maximality`, `Q1-Q3Pairs`, `26,648` masks): **`683.1809`** (**`-0.775` below `B684`, `81.1%` of gap closed**).
  - **Direct `m ∈ {682, 683}` separation with `Q5-PSD + Q3-Bilin` (`31,571+` masks):** `m = 683.000000` still survived strictly (`slk_ub = 0`, `E[n_0] = 9.64–11.73`, `p2_adj ≈ 0.135–0.138`, `~{5:85, 6:43}`), proving that refuting `683` analytically requires coupling beyond $Q_5$-level PSD+RLT.
- **Exact Kőnig Bipartite-Seam Compression & Global Frustration Chasm:**
  - Lossless compression $\operatorname{ex}(Q_8, C_4) = \max_{G_0, G_1 \subset Q_7} (|E(G_0)| + |E(G_1)| + 128 - \nu(G_0 \cap G_1))$ verified `24/24` on real cuts, `100k` incremental parity checks, and cold-start recovery of $\operatorname{ex}(Q_7, C_4) = 304$ in `2.79 s`.
  - Across `209.7M` exact $\operatorname{Aut}(Q_7)$ gluings, `3.02B` 4-island PT moves, `1.28B` phantom-zone barrier moves, `1.64B` far-from-spin-glass moves (`|δ| ∈ [85, 186]` capped at `667 → 664 → 658`), `64/64` exact proven non-odd-square $Q_7$-half MILP-LNS windows (`<= 0.01 s`/half), and `24` ruled-out $\operatorname{Aut}(Q_8)$ subgroups, zero `683`-edge graphs were found.

---

## 4. Reproduce Offline (`< 0.05 s` Python + Lean 4)

```bash
# 1. Cold-verify all 10 inclusion-maximal atlas witnesses + Degree-Blocking Identity + 14-orbit Case 5A exclusion
env -i PATH=/usr/bin:/bin:/opt/homebrew/bin python3 verify.py

# 2. Negative self-test (--corrupt injects a C_4 and must exit with rc=1)
env -i PATH=/usr/bin:/bin:/opt/homebrew/bin python3 verify.py --corrupt

# 3. Verify SHA-256 checksums
shasum -a 256 -c SHA256SUMS

# 4. Machine-check all 6 Lean 4 theorems (0 sorryAx, pure Lean 4 core)
lean Q8EmptySquareForcing.lean
```

— engineered & verified by **we\*** (`PROOFER` powered by Gemini + @mizopl)
