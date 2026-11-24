# `q8-c4-extremal-forcing` — Lean 4 Empty-Square Forcing, Independent $\mathbb{F}_2$ Gauge-Defect / Case 5A Replay & 10-Witness Atlas for $\operatorname{ex}(Q_8, C_4) \in \{682, 683\}$

> **Status:** Structural Archive (`PARKED` · `ex(Q_8, C_4) ∈ {682, 683}` remains **OPEN**)  
> **Cold Verifier:** [`verify.py`](./verify.py) (Python `>= 3.10`, `~0.1 s` wall time under `env -i PATH=/opt/homebrew/bin:/usr/bin:/bin`, verifies the exact 10 pinned `atlas/*.edges` witnesses, `min_x7`, Degree-Blocking Identity, and 14-orbit Case 5A exclusion; `--corrupt` injects `C4 > 0` at unchanged `|E|` and exits `1`)  
> **Lean 4:** [`Q8EmptySquareForcing.lean`](./Q8EmptySquareForcing.lean) (tested on Lean `4.36.0`, `6` axiom-checked theorems using standard axioms `[propext, Classical.choice, Quot.sound]`, `0 sorryAx`, zero `native_decide`, zero external dependencies)  
> **Companion Dispatch:** [Field Notes #007](../../news/2026-11-23_field_notes_ongoing_campaigns.md)

---

## Limitations First (`-0 Hype`)

1. **Main open problem remains OPEN:** We neither constructed a $683$-edge $C_4$-free subgraph of $Q_8$ nor proved $\operatorname{ex}(Q_8, C_4) \le 682$ (Erdős Problem #86 in dimension $8$).
2. **Upstream priority explicitly credited (`lisresearchgroup/math-rsi` commit `3880f52a`):**
   - Lower bound $\ge 682$: Marinari–Parisi–Ritort (1995), Minamoto (`arXiv:2603.29127v5`, odd-square maximum $g(8) = 682$), and [`lisresearchgroup/math-rsi`](https://github.com/lisresearchgroup/math-rsi) (`plugins/hypercube-extremal/archive/q8-683/`, `seed1..seed4`).
   - Upper bound $\le 683$: `lisresearchgroup/math-rsi` (`B684_EXCLUSION.md`, whose non-author whole-proof review is labeled `PASS · same-family · provisional` in `plugins/hypercube-extremal/archive/q8-683/README.md`).
   - Empty-square forcing identity: already appears as equation `(2)` of Lemma 6 in `lisresearchgroup/math-rsi` (`plugins/hypercube-extremal/archive/q7-304/source/ASTRA_主证明合订.md`).
   - Toggle / gauge-defect exclusions: `lisresearchgroup/math-rsi` (`plugins/hypercube-extremal/tools/cube_coevolve/configs/q8.json` line 19, and `q8-universal-two-deletion-four-toggle` in their research wiki) already records that a `683+` $C_4$-free graph requires at least `5` toggles from every odd-square graph and at least `3` deletions and `4` additions (`|δ| >= 7`, which strictly contains our Case 5A) from every odd-square `682` graph. We do **not** claim priority over `math-rsi`, and we do **not** replay their stronger `|δ| >= 7` (`>= 3 deletions, >= 4 additions`) odd-682 exclusion (neither on paper nor in code). Rather, our package provides: (i) an independent Lean 4 formalization of the abstract forcing identities, (ii) a self-contained **paper** proof of `|δ| >= 5` and the Case 5A reduction, and (iii) a machine-checked `verify.py` routine for the final 14-orbit / 31-triple Case 5A elimination plus 10 pinned witnesses.
3. **Scope of formal & algebraic results:** `Q8EmptySquareForcing.lean` proves `6` axiom-checked theorems (plus `q8_convexity_identity`) on the **abstract** incidence structure `C4FreeCounts` whose double-counting hypotheses (`h_tot`, `h_inc`, `h_wedge`) are assumed as structure fields rather than derived from a concrete graph. In Section 1.B, parity, `r = 0`, `|δ| = 3`, and the Case 5A reduction are paper proofs; only the Degree-Blocking Identity check on odd witnesses and the final 14-orbit / 31-triple Case 5A elimination are machine-checked by `verify.py`.
4. **Scope of exploratory LP/PSD & search notes (Section 3):** The finite-pool LP/PSD numbers in Section 3 (`683.5770`, `683.2796`, `683.1809`) are **exploratory pool-LP diagnostics — NOT certified upper bounds on $\operatorname{ex}(Q_8, C_4)$, and NOT reproducible from this standalone package** (their mask pools and solver code are not included here). Search/MILP summaries in Section 3 are unverified author logs, not global non-existence proofs.

---

## 1. Formal & Algebraic Results (Independent Replay + Lean 4)

### A. Abstract Lean 4 Empty-Square Forcing (`Q8EmptySquareForcing.lean`, `0 sorryAx`)
Notation: for a $C_4$-free spanning subgraph $H \subseteq Q_n$ with $m = |E(H)|$ edges, let $S_n = \binom{n}{2} 2^{n-2}$ be the number of 4-cycles in $Q_n$, $W = \sum_v \binom{\deg(v)}{2}$ the wedge sum, $(n_0, n_1, n_2^{\text{opp}}, n_2^{\text{adj}}, n_3)$ the 4-cycle counts by edge count (splitting 2-edge squares into opposite vs. adjacent pairs), $\operatorname{vDefect}(d) = \binom{d}{2} + 15 - 5d \ge 0$ ($\operatorname{vDefect}(d) = 0 \iff d \in \{5, 6\}$; $\operatorname{vDefect}(4) = \operatorname{vDefect}(7) = 1$, $\operatorname{vDefect}(3) = \operatorname{vDefect}(8) = 3$), $\Delta_{\text{deg}} = \sum_{v \in Q_8} \operatorname{vDefect}(\deg(v))$, and $g(8)$ the maximum edge count of an odd-square ($n_0 = n_2^{\text{opp}} = n_2^{\text{adj}} = 0$) $C_4$-free subgraph of $Q_8$. On the abstract `C4FreeCounts` structure, `Q8EmptySquareForcing.lean` proves (`6` theorems checked by `#print axioms`, plus `q8_convexity_identity`):
- **Identities (`empty_square_forcing_identity`, `q8_convexity_identity`):** $n_2^{\text{opp}} + S_n + W = n_0 + (n - 1) m$ and $W + 3840 = 10 m + \Delta_{\text{deg}}$.
- **Mandatory empty squares (`q8_683_forces_empty_square`, `q8_ge684_forces_empty_squares`):** $m = 683 \implies n_0 = 1 + n_2^{\text{opp}} + \Delta_{\text{deg}} \ge 1$; $m \ge 684 \implies n_0 \ge 4$.
- **Odd-square cap (`q8_odd_square_upper_682`):** $n_0 = n_2^{\text{opp}} = 0 \implies m \le 682$ (strengthening $g(8) \le 682$ to arbitrary $n_2^{\text{adj}}$).
- **Exact `682` dichotomy (`q8_682_odd_square_forces_defect_2`, `q8_682_deg56_forces_n2_opp_ge_2`):** Every odd-square `682` has $\Delta_{\text{deg}} = 2$ ($W = 2982$, cannot lie in $\{5, 6\}$), while every $\{5^{172}, 6^{84}\}$ `682` ($W = 2980$) must satisfy $n_2^{\text{opp}} = 2 + n_0 \ge 2$.

### B. Independent $\mathbb{F}_2$ Gauge-Defect Replay ($H = H_0 \oplus \delta$) & Case 5A Verification (`verify.py`)
Since $H^1(Q_8; \mathbb{F}_2) = 0$, every odd-square subgraph lies in the affine spin-glass coset $\mathcal{O}_8 = \{x_{\text{ref}} \oplus d_1(\phi) : \phi \in \mathbb{F}_2^{V(Q_8)}\}$ (where $x_{\text{ref}}(u, u \oplus e_i) = \bigoplus_{j < i} u_j$; every $H_0 \in \mathcal{O}_8$ is automatically $C_4$-free and satisfies $|E(H_0)| \le 682$). Given any $C_4$-free $H \subseteq Q_8$ and any $H_0 \in \mathcal{O}_8$, write $H = H_0 \oplus \delta$ with added edges $A = H \setminus H_0$ ($a = |A|$) and removed edges $R = H_0 \setminus H$ ($r = |R|$, $|\delta| = a + r$):
1. **Coboundary lower bound (paper):** $|d_2(\delta)| = n_{\text{even}}(H) = n_0 + n_2^{\text{opp}} + n_2^{\text{adj}} \le 7|\delta| \implies |\delta_{\min}(H)| \ge \lceil n_{\text{even}}(H) / 7 \rceil$.
2. **Parity & $a \le r$ exclusion for `683` (paper):** Every $H_0 \in \mathcal{O}_8$ satisfies $n_1 + n_3 = 1792$ and $n_1 + 3 n_3 = 7|E(H_0)|$, so $2 n_3 = 7|E(H_0)| - 1792$ and $|E(H_0)|$ is always **even**. Hence any `683`-edge graph has **odd** $|\delta|$ relative to every $H_0 \in \mathcal{O}_8$. Moreover, $|E(H)| = |E(H_0)| + a - r = 683$ with $|E(H_0)| \le 682$ forces $a \ge r + 1$, ruling out all cases with $a \le r$ (such as $(0,1)$, $(0,3)$, and $(1,2)$).
3. **Zero-removal exclusion for `683` (paper):** If $r = 0$, then $H \supseteq H_0$, so every 4-cycle of $Q_8$ inherits at least $1$ edge from $H_0$ in $H$, forcing $n_0(H) = 0$ and contradicting $n_0(H) \ge 1$ at $m = 683$. This rules out $(a, r) = (1, 0)$ ($|\delta| = 1$) and $(a, r) = (3, 0)$ (with $|E(H_0)| = 680$).
4. **Degree-Blocking Identity & $|\delta| = 3$ exclusion (paper + checked on odd witnesses by `verify.py`):** Let $e = (u, v) \notin H_0$ be any missing edge of $H_0 \in \mathcal{O}_8$. Each of the $7$ squares of $Q_8$ containing $e$ has $1$ or $3$ edges in $H_0$:
   - the $b_{H_0}(e)$ 3-squares contribute $2$ edges incident to $\{u, v\}$ each,
   - the $q_{\text{opp}}(e)$ 1-squares whose sole edge is opposite to $e$ contribute $0$ edges incident to $\{u, v\}$,
   - the remaining $7 - b_{H_0}(e) - q_{\text{opp}}(e)$ 1-squares contribute $1$ edge incident to $\{u, v\}$ each.
   Summing gives the exact identity $\deg_{H_0}(u) + \deg_{H_0}(v) = 7 + b_{H_0}(e) - q_{\text{opp}}(e) \le 7 + b_{H_0}(e)$.
   For the sole remaining $|\delta| = 3$ case $(a, r) = (2, 1)$ ($|E(H_0)| = 682$, single removed edge $f \in R$), every 3-square of $H_0$ containing an added edge $e_i \in A$ must also contain $f$ (otherwise $e_i$ closes a $C_4$ in $H$). Since two distinct edges of $Q_8$ share at most $1$ square, $b_{H_0}(e_i) \le 1 \implies \deg_{H_0}(u_i) + \deg_{H_0}(v_i) \le 8$. Since $\Delta_{\text{deg}}(H_0) = 2$ forces $\deg_{H_0}(v) \ge 4$ everywhere and allows at most two vertices of degree $4$ (the set $D_4 = \{v : \deg_{H_0}(v) = 4\}$ has $|D_4| \le 2$), both $e_1$ and $e_2$ must join that same pair of degree-4 vertices ($e_1 = e_2$), contradiction. Hence **every `683`-edge graph has odd $|\delta| \ge 5$ relative to every $H_0 \in \mathcal{O}_8$** (independently reproducing the `>= 5 toggles` exclusion recorded in `math-rsi`'s `configs/q8.json`).
5. **Exhaustive Case 5A exclusion (`verify.py`, `0.004 s` machine check):** Suppose $H = H_0 \oplus \delta$ (`|E(H)| = 683`) has **minimal** $|\delta| = 5$ among all $H_0 \in \mathcal{O}_8$, with $R = \{f_1, f_2\} \subset H_0$ (`r = 2`), $A = \{e_1, e_2, e_3\} \subset E(Q_8) \setminus H_0$ (`a = 3`), and $|E(H_0)| = 682$. Every 3-square of $H_0$ containing $e_i \in A$ must contain $f_1$ or $f_2$, so letting $s(e_i)$ be the number of distinct squares of $Q_8$ containing $e_i$ and at least one of $\{f_1, f_2\}$ ($s(e_i) \in \{0, 1, 2\}$), we have $b_{H_0}(e_i) \le s(e_i)$ and hence $\deg(u_i) + \deg(v_i) \le 7 + s(e_i) \le 9$. Because $\deg \ge 4$ everywhere and $|D_4| \le 2$:
   - $s(e_i) = 0$ is impossible ($\deg(u_i) + \deg(v_i) \le 7$),
   - $s(e_i) = 1$ forces both endpoints of $e_i$ in $D_4$ (fixing $D_4 = \{u_i, v_i\}$, at most one such edge) and forces that unique square to be a 3-square of $H_0$ (since $b \ge 1$),
   - $s(e_i) = 2$ forces at least one endpoint in $D_4$; if not both endpoints lie in $D_4$, then $\deg(u_i) + \deg(v_i) \ge 9 \implies b_{H_0}(e_i) = 2$, forcing **both** candidate squares to be 3-squares of $H_0$ (the **forced 3-square rule**: all other 3 edges of every forced 3-square belong to $H_0$, so they must be disjoint from $A$, form no $C_4$ inside $H_0$, and cannot complete an unblocked 3-square around another $e_j \in A$).
   - By minimality of $|\delta| = 5$, no vertex $v$ satisfies $|\delta \cap \operatorname{star}(v)| \ge 5$ (else flipping spin $\phi_v$ yields $|\delta'| \le 3$, ruled out by (2)–(4)).
   Fixing $f_1 = (0, 1)$ by edge-transitivity, $\operatorname{Stab}_{\operatorname{Aut}(Q_8)}(f_1)$ partitions all `1,023` choices of $f_2 \ne f_1$ into `14` exact orbits; `verify.py` checks all `31` candidate triples across all `14` orbit representatives (using complete hitting-set enumeration for $|D_4| \le 2$) and finds **`0` survivors** in `0.004 s`, giving an independent machine-checked replay of the distance-5 subcase of `math-rsi`'s `>= 3 deletions, >= 4 additions` odd-682 exclusion.

---

## 2. Cold-Verified 10-Witness Inclusion-Maximal Atlas (`atlas/*.edges`)

Notation used in the table and `verify.py`: `min_x7` is the minimum number of blocking 3-paths (`x_7(e) = b_H(e)`) over all missing edges $e \notin E(H)$ (`min_x7 >= 1` $\iff$ inclusion-maximal; `min_x7 = 1` enables a 1-out-1-in swap); `C(P)` and `b(P)` are the `math-rsi` parity-side vertex-degree penalty sums (`C(P) = 66 n_4 + 105 n_7 + ...`, `b(P) = 4 n_4 + 5 n_7 + ...`, both computed by `verify.py --json`; both equal `0` iff all degrees lie in `{5, 6}`).

All `10/10` witnesses below are pinned and verified by `verify.py` (exact filename set, `C4 = 0`, `inclusion_maximal = True`, exact `|E|`, `odd`, squares, `W (+Δ)`, `min_x7`, `|δ| >= ceil(n_even/7)`, and canonical `SHA-256`; the rightmost column notes author MILP diagnostics not recomputed by `verify.py`):

| Witness (`atlas/`) | $|E|$ | Odd-Sq | Degree Sequence | Squares $(n_0, n_1, n_2^{\text{opp}}+n_2^{\text{adj}}, n_3)$ | $W$ ($+\Delta$) | `min_x7` · `|δ|>=` | SHA-256 (12 hex) | Author MILP note *(not in `verify.py`)* |
| :--- | ---: | :---: | :--- | :--- | :---: | :---: | :--- | :--- |
| `q8_682_odd_x7min1_pivot_bridge.edges` | **682** | Yes | $\{4^2, 5^{168}, 6^{86}\}$ | `(0, 301, 0+0, 1491)` | `2982 (+2)` | `1` · `>=0` | `e08abf55234d` | `|δ_min|=0` (symm. diff. 2 from `deg56`) |
| `q8_682_odd_deg7_vertex.edges` | **682** | Yes | $\{4^1, 5^{171}, 6^{83}, 7^1\}$ | `(0, 301, 0+0, 1491)` | `2982 (+2)` | `3` · `>=0` | `eb026494fedc` | `|δ_min|=0`, asymm. bip. |
| `q8_682_deg56_zero_defect_n2o2_n2a10.edges` | **682** | **No** | **$\{5^{172}, 6^{84}\}$** | `(0, 295, 2+10, 1485)` | **`2980 (+0)`** | `1` · `>=2` | `31b3bdf85cfb` | `|δ_min|=2` (`|H_0|=682`, `+1/-1`), $C=b=0$ |
| `q8_682_deg41_nonodd_n2o1_n2a11.edges` | **682** | No | $\{4^1, 5^{170}, 6^{85}\}$ | `(0, 295, 1+11, 1485)` | `2981 (+1)` | `1` · `>=2` | `d9f494b089a6` | `|δ_min|=2` (`|H_0|=682`, `+1/-1`) |
| `q8_682_deg42_nonodd_n2o0_n2a12.edges` | **682** | No | $\{4^2, 5^{168}, 6^{86}\}$ | `(0, 295, 0+12, 1485)` | `2982 (+2)` | `1` · `>=2` | `133531616e98` | `|δ_min|=2` (`|H_0|=682`, `+1/-1`) |
| `q8_681_maximal_blocked_empty_sq_n0_1.edges` | **681** | No | $\{4^4, 5^{166}, 6^{86}\}$ | **`(1, 295, 2+14, 1480)`** | `2974 (+4)` | `1` · `>=3` | `0af374579266` | `|δ_min|=3` (`|H_0|=682`, `+1/-2`) |
| `q8_680_maximal_blocked_n0_2_n2a_24.edges` | **680** | No | $\{4^6, 5^{164}, 6^{86}\}$ | `(2, 291, 4+24, 1471)` | `2966 (+6)` | `1` · `>=5` | `a9a21b8bf56f` | `|δ_min|=6` (`|H_0|=680`, `+3/-3`) |
| `q8_678_maximal_blocked_n0_5_n2a_21.edges` | **678** | No | $\{4^{10}, 5^{161}, 6^{84}, 7^1\}$ | `(5, 293, 8+21, 1465)` | `2951 (+11)` | `1` · `>=5` | `0068718824c4` | `|δ_min|=6` (`|H_0|=680`, `+2/-4`) |
| `q8_678_maximal_high_n2a_78_n0_0.edges` | **678** | No | $\{4^8, 5^{164}, 6^{84}\}$ | `(0, 273, 6+78, 1435)` | `2948 (+8)` | `1` · `>=12` | `7e5ad9fb2310` | `|δ_min|=18` (`|H_0|=680`, `+8/-10`) |
| `q8_675_maximal_phantom_n0_4_n2a_94.edges` | **675** | No | $\{4^{11}, 5^{165}, 6^{79}, 7^1\}$ | `(4, 265, 15+94, 1414)` | `2922 (+12)` | `1` · `>=17` | `6e484827d543` | `|δ_min|=23` (`|H_0|=678`, `+10/-13`) |

---

## 3. Exploratory Diagnostic Summary *(Author Logs — Not Certified Bounds & Not Reproducible from This Package)*

The notes below summarize exploratory LP/PSD and search runs recorded in [Field Notes #007](../../news/2026-11-23_field_notes_ongoing_campaigns.md); they are **not** certified upper bounds on $\operatorname{ex}(Q_8, C_4)$ and are **not** verified by `verify.py`:
- **Pool-restricted $Q_4 / Q_5$ LP+PSD experiments (heuristic diagnostics only):** Over finite pools of legal $C_4$-free subcube masks expanded by adversarial simulated-annealing pricing, pool-LP objectives moved from `683.5770` (`Q_4` with maximality cuts) to `683.2796` (`Q_5` columns + 4-flag coupling, `22,107` masks) and `683.1809` (adding dim-5 `Q_5` PSD cuts, `26,648` masks). In direct `m ∈ {682, 683}` separation with additional `Q_3` bilinear RLT cuts (`31,571+` masks), **`m = 683.000000` remained strictly feasible in our pools** (at `E[n_0] ≈ 9.6–11.7`, `p2_adj ≈ 0.135–0.138`, near `{5:85, 6:43}`), indicating that our `Q_5`-level PSD+RLT relaxations did not refute `683`.
- **Kőnig bipartite-seam identity & search summary:** Splitting $Q_8 = A_0 \sqcup A_1 + M$ along any coordinate axis (`A_0, A_1` the two `Q_7` halves, `M` the cross-matching) gives the exact reduction
  $$\operatorname{ex}(Q_8, C_4) = \max_{\substack{G_0, G_1 \subseteq Q_7 \\ C_4\text{-free}}} \big(|E(G_0)| + |E(G_1)| + 128 - \nu(G_0 \cap G_1)\big),$$
  where $\nu$ is the maximum bipartite matching size. Exploratory C parallel-tempering and $\operatorname{Aut}(Q_7)$-gluing searches (including far-from-$\mathcal{O}_8$ barriers with `|δ| ∈ [85, 186]` capping at `667 / 664 / 658`) plus local $Q_7$-half MILPs and `24` symmetry-quotient MILPs found no `683`-edge witness.

---

## 4. Reproduce Offline (`~0.1 s` Wall Time, Python `>= 3.10` + Lean `4.36.0`)

```bash
# 1. Cold-verify all 10 pinned atlas witnesses + Degree-Blocking Identity + 14-orbit Case 5A exclusion
env -i PATH=/opt/homebrew/bin:/usr/bin:/bin python3 verify.py

# 2. Negative self-test (--corrupt injects C4 > 0 at unchanged |E|; must print [FAIL] ... C4>0 and exit 1)
env -i PATH=/opt/homebrew/bin:/usr/bin:/bin python3 verify.py --corrupt

# 3. Verify SHA-256 checksums
shasum -a 256 -c SHA256SUMS

# 4. Machine-check all 6 axiom-checked Lean 4 theorems (tested on Lean 4.36.0, 0 sorryAx)
lean Q8EmptySquareForcing.lean
```

— engineered & verified by **we\*** (`PROOFER` powered by Gemini + @mizopl)
