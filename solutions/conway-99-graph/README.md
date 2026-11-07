# Conway's 99-Graph Problem (`conway-99-graph`, $\mathrm{srg}(99, 14, 1, 2)$) — Canonical Repository Pointer

> **🔗 Canonical Standalone Repository (`Single Source of Truth`):**
> **[`https://github.com/mizopl/conway-99-graph`](https://github.com/mizopl/conway-99-graph)**

To avoid duplicating ~40 MB of `.lrat`/`.cnf` SAT certificates, Lean 4 formalizations, and `(0, 7, 0)` LEGO solver scripts inside `mizopl/we-star`, all executable verifiers, certificates, and documentation for Conway's 99-Graph Problem live in the dedicated standalone repository **[`mizopl/conway-99-graph`](https://github.com/mizopl/conway-99-graph)**.

---

## Quick Links into [`mizopl/conway-99-graph`](https://github.com/mizopl/conway-99-graph)

- **[`README.md`](https://github.com/mizopl/conway-99-graph/blob/main/README.md):** Overview of all **27 theorems (`54` dual-encoded Sinz vs. Totalizer Pure-RUP LRAT `0 RAT` certificates)** across Track `p2` ([`V3R1T4S PR #774`](https://github.com/elder-plinius/V3R1T4S/pull/774): 5 forced-structure reductions / 10 certificates, `r4_s6_p3_fix9` `n_clauses = 442`) and Track `p1` ([`V3R1T4S PR #840`](https://github.com/elder-plinius/V3R1T4S/pull/840): 22 automorphism exclusions / 44 certificates), the **42 zero-axiom (`0 sorryAx`) Lean 4 theorems compressed into `5 Master Theorems`**, and the `(0, 7, 0)` involution sector reduction.
- **[`SIGN_OFF_TABLE.md`](https://github.com/mizopl/conway-99-graph/blob/main/SIGN_OFF_TABLE.md):** Exhaustive Case-Partition Sign-Off Matrix (`Law M40` / `CLSS-E12`, rows `C99-01` through `C99-09b`), including the unconditional $B_0$-free LEGO closure of all $k_{\text{type1}}(S_r) \ge 1$ strata (`1+2+3`, `1+1+2+2`, `1+1+4` — re-certified across all `56 / 56` `Stab8` classes in 8-domain mode with sorted row-mask pools [`tot_b1 = 338,775,503`, `tot_nodes = 42,659,924,261`, `sols = 0`, commit [`4ca6b95`](https://github.com/mizopl/conway-99-graph/commit/4ca6b95d3feea1c2a8c618c307497777f5c8ff3b)] in collaboration with `@ibenarb` — and `1+5` via Lean 4 `Theorem 4: seven_triangle_type1_handshaking`) and the operator retrospective ***"Hints for Humans in the Loop: A Way to Proof"***.
- **[`lean/Conway99/ChiralNullspaceAndHandshaking.lean`](https://github.com/mizopl/conway-99-graph/blob/main/lean/Conway99/ChiralNullspaceAndHandshaking.lean):** Complete Lean 4 formalization (`42` theorems, `5 Master Theorems`, `0 sorryAx`).
- **[`RUN_IT_YOURSELF.md`](https://github.com/mizopl/conway-99-graph/blob/main/RUN_IT_YOURSELF.md) & [`verify-it-yourself/`](https://github.com/mizopl/conway-99-graph/tree/main/verify-it-yourself):** One-command pure-Python standard-library verification suite (`verify.py` + `null_ktype1_ge1_unconditional_lego_summary.json`).

---

— autonomously engineered & 3-skeptic verified by **Gemini-CLSS** (`PROOFER v19`) on `@mizopl`'s behalf
