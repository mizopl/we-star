# `q8-c4-extremal-forcing` — Empty-Square Forcing (Lean 4) & Non-Odd-Square `682`-Edge Witness Atlas for $\operatorname{ex}(Q_8, C_4) \in \{682, 683\}$

> **Status:** Ongoing Research Artifact (Round 1 Complete · `ex(Q_8, C_4) ∈ {682, 683}` remains **OPEN**)  
> **Cold Verifier:** `verify.py` (`0.002 s` per witness under `env -i`, `--corrupt` exits `1`)  
> **Lean 4:** `Q8EmptySquareForcing.lean` (`Lean 4 v4.35.0`, `0 sorryAx`, zero `native_decide`, zero external dependencies)

## Limitations First (`-0 Hype`)

1. **Main problem remains open:** We neither constructed a $683$-edge $C_4$-free subgraph of $Q_8$ nor proved $\operatorname{ex}(Q_8, C_4) \le 682$.
2. **Scope of Lean 4 theorems:** `Q8EmptySquareForcing.lean` proves six algebraic double-counting identities on the abstract `C4FreeCounts` incidence structure (showing $n_0 = 1 + n_2^{\text{opp}} + \Delta_{\text{deg}} \ge 1$ at $m = 683$, $n_0 \ge 4$ at $m \ge 684$, and $m \le 682$ whenever $n_0 = n_2^{\text{opp}} = 0$, strengthening $g(8) \le 682$). It does **not** prove $\operatorname{ex}(Q_8, C_4) \le 682$.
3. **Prior art credited explicitly:** Lower bound $\ge 682$ due to Marinari–Parisi–Ritort (1995), Minamo Minamoto (`arXiv:2603.29127v5`, $g(8) = 682$), and `lisresearchgroup/math-rsi` (`archive/q8-683/`); upper bound $\le 683$ due to `lisresearchgroup/math-rsi` (`B684_EXCLUSION.md`, Nov 2026).

## New Cold-Verified Artifacts

| File | $|E|$ | Max | Odd-Sq | Degree Sequence | Squares $(n_0, n_1, n_2^{\text{opp}}+n_2^{\text{adj}}, n_3)$ | $W$ ($+\Delta$) | SHA-256 (12 hex) |
| :--- | ---: | :---: | :---: | :--- | :--- | :---: | :--- |
| `atlas/q8_682_odd_x7min1_pivot_bridge.edges` | 682 | Yes | Yes | $\{4^2, 5^{168}, 6^{86}\}$ | `(0, 301, 0+0, 1491)` | `2982 (+2)` | `e08abf55234d` |
| `atlas/q8_682_deg56_zero_defect_n2o2_n2a10.edges` | 682 | Yes | No | $\{5^{172}, 6^{84}\}$ | `(0, 295, 2+10, 1485)` | `2980 (+0)` | `31b3bdf85cfb` |
| `atlas/q8_682_deg41_nonodd_n2o1_n2a11.edges` | 682 | Yes | No | $\{4^1, 5^{170}, 6^{85}\}$ | `(0, 295, 1+11, 1485)` | `2981 (+1)` | `d9f494b089a6` |
| `atlas/q8_682_deg42_nonodd_n2o0_n2a12.edges` | 682 | Yes | No | $\{4^2, 5^{168}, 6^{86}\}$ | `(0, 295, 0+12, 1485)` | `2982 (+2)` | `133531616e98` |
| `atlas/q8_681_maximal_blocked_empty_sq_n0_1.edges` | 681 | Yes | No | $\{4^4, 5^{166}, 6^{86}\}$ | `(1, 295, 2+14, 1480)` | `2974 (+4)` | `0af374579266` |

## Reproduce Offline (`< 0.02 s` Python + Lean 4)

```bash
python3 verify.py --min-edges 682 atlas/q8_682_*.edges
python3 verify.py --min-edges 681 atlas/q8_681_*.edges
python3 verify.py atlas/q8_682_deg56_zero_defect_n2o2_n2a10.edges --corrupt   # exits 1
lean Q8EmptySquareForcing.lean
```
