# Lessons Learned — Engineering Exact Galois Certificates & Zero-Axiom Lean 4 Proofs for `unitaryfoundation/stabrank` in `3h 34m`

This field note distills **five transferable mathematical, formal-verification, and open-source CI lessons** from our [`unitaryfoundation/stabrank`](https://github.com/unitaryfoundation/stabrank) campaign ([`PR #193`](https://github.com/unitaryfoundation/stabrank/pull/193), [`PR #194`](https://github.com/unitaryfoundation/stabrank/pull/194), and [`Issue #195`](https://github.com/unitaryfoundation/stabrank/issues/195)), where `we*` (`@mizopl` + Gemini-powered agentic workflows) went from a cold start (`16:04 CET`) to `35` exact `tier=verified` bounds (`20.46 s` total single-core runtime) and `10` zero-axiom (`0 sorryAx`) Lean 4 modules (`19:38 CET`) in **`3 hours 34 minutes`**.

---

## Lesson 1 — Replace Floating-Point Margins (`lstsq`) with Codimension-2 Cyclotomic Galois Quotients ($\mathbb{Z}[i]$ & $\mathbb{Z}[\omega_3]$)

### The Bottleneck
Numerical rank-exclusion scripts typically project stabilizer dictionaries onto random $\mathbb{C}^k$ subspaces and test candidate covers via floating-point QR / least-squares (`1e-8` tolerances). On `unitaryfoundation/stabrank`, this had two costs:
1. **Tier ceiling:** Any bound relying on a floating-point margin is capped at `tier = reproduced` rather than `tier = verified` (`"exact": true`).
2. **Runtime blowup:** Exhaustive rank-4 exclusions at $m=5$ took `1,649 s` in floating-point Python or required external multi-hour batch manifests (`tier = attested`).

### The Structural Fix
Every $n$-qubit stabilizer state (after clearing normalization) has exact Gaussian-integer entries in $\{0, \pm 1, \pm i\} \subset \mathbb{Z}[i]$, and every $n$-qutrit stabilizer state has exact Eisenstein-integer entries in $\{0, 1, \omega_3, \omega_3^2\} \subset \mathbb{Z}[\omega_3]$. Meanwhile, standard magic-state tensor powers live in a quadratic extension above the stabilizer base field:
- **Qubits (`qubit_H`, `qubit_T`):** $\psi_m = A_m + \sqrt{d}\, B_m$ over $\mathbb{Q}(i, \sqrt{d}) / \mathbb{Q}(i)$ ($d=2$ for `qubit_H`, $d=3$ for `qubit_T`), where $A_m, B_m \in \mathbb{Z}[i]^{2^m}$.
- **Qutrits (`H3`):** $|H_3\rangle^{\otimes m}$ splits as $v_0^{(m)} + \sqrt{3}\, v_1^{(m)}$ over $\mathbb{Q}(\omega_3, \sqrt{3}) / \mathbb{Q}(\omega_3)$, because $\sqrt{3}$ is real while $\mathbb{Q}(\omega_3) = \mathbb{Q}(\sqrt{-3})$ is imaginary quadratic.

Because the nontrivial Galois automorphism $\sigma(\sqrt{d}) = -\sqrt{d}$ fixes every stabilizer vector entrywise, **any** complex linear combination $\sum_{j=1}^r c_j s_j = \psi_m$ automatically spans **both** $A_m$ and $B_m$ over the base cyclotomic field! Quotienting by the 2D Galois plane $P_m = \mathrm{span}(A_m, B_m)$ instead of a 1D complex line cuts the quotient dimension by an extra degree of freedom:
- **Rank-3 exclusions become 0-pivot hash lookups:** In $\mathbb{Q}(\omega_3)^{27} / V_3(H_3)$, three stabilizer states spanning $V_3(H_3)$ must project to **collinear rays**. Canonicalizing each $\mathbb{Z}[\omega_3]$-ray via multiplication by $\bar{z} = (a-b) - b\omega_3$ and dividing by row $\gcd$ proves $\chi(|H_3\rangle^{\otimes 3}) \ge 4$ across all `30,240` 3-qutrit stabilizer states in **`0.11 s` with zero pivots and zero symmetry assumptions**.
- **Rank-4 exclusions on $m=5, 6$ drop from `1,649 s` to `7.08 s` (`350x` speedup):** Combining 2-qubit Pauli flat reduction ($D_5 \to D_4 \to D_3$) with the 1-pivot $\mathbb{Z}[i]$ Galois quotient certifies all four $m=5,6$ rank-5 lower bounds in exact integer arithmetic with zero external files.

---

## Lesson 2 — Change the Ambient Dictionary Before Enumerating (`D_4` Slice-and-Lift & Even-Qubit Clifford Postselection)

Before optimizing an inner loop on an $n$-qubit stabilizer dictionary $D_n$ (which grows super-exponentially: $|D_2| = 60$, $|D_3| = 1{,}080$, $|D_4| = 36{,}720$, $|D_5| = 2{,}423{,}520$), check whether an exact Clifford reduction drops $n$ by $1$ or $2$:
1. **`cat` states ($m=7..10$ in `3.66 s` vs `460 s` — `125x` faster):** Because $\chi(|c_5\rangle) = \chi(|c_6\rangle) = 3$, instead of lifting $c_6 \to c_7$ directly on $D_5$ (`2.42M` states), slicing two qubits down to $D_4$ (`36,720` states, `100` symmetry orbits) enumerates all exact $\mathbb{Z}[i]$ rank-3 decompositions of $|c_5\rangle$, filters those lifting to $|c_6\rangle$, and proves none lift to $|c_7\rangle$ (hence $\chi(|c_m\rangle) \ge 4$ for $m=7..10$ by projection monotonicity).
2. **Two-qubit `CS` states ($m=3, 4$ in `2.61 s`):** Applying single-qubit $H$ on the second qubit of each pair and postselecting on $\langle 0|_2$ maps $|\text{CS}\rangle = \frac{1}{2}(|00\rangle + |01\rangle + |10\rangle + i|11\rangle)$ onto an exact single-qubit Gaussian-integer state $|\Psi_1\rangle \propto 2|0\rangle + (1+i)|1\rangle \in \mathbb{Z}[i]^2$, turning an 8-qubit ($4^4 = 256$) `CS` lower bound into a 3-qubit ($D_3 = 1{,}080$) exact $\mathbb{Z}[i]$ calculation!

---

## Lesson 3 — Zero-Axiom (`0 sorryAx`) Lean 4 Proofs via Cyclotomic Reflection & Ephemeral Cloud Builds

1. **Reflect transcendental amplitudes into polynomial rings over $\mathbb{Z}$ before calling `decide` / `ring`:**
   In `ReflectQutrit.lean`, the Norrell state $|N\rangle = (|0\rangle + |1\rangle - 2|2\rangle)/\sqrt{6}$ has irrational normalization $\sqrt{6}^{-m}$, which makes direct `Complex` arithmetic slow in Lean 4. Factoring out $(\sqrt{6})^{-m}$ once (`norrellVec_eq_ev`) reduces every $m=5$ (`243`-amplitude) witness identity in `NorrellM5StabRank.lean` ($\chi(|N\rangle^{\otimes 5}) \le 10, \gamma = 0.41918$) to pure integer-ring evaluation, compiling in **`1.96 s`**!
2. **Algebraic ratio-period obstructions for $m=1$ lower bounds (`M1Lower.lean`):**
   Instead of enumerating every stabilizer group at $m=1$, `IsStabP.pow_period_eq` shows that any single prime-dimension stabilizer vector's nonzero amplitude ratios are roots of unity ($(z_1/z_0)^4 = 1$ for $p=2$; $(z_i/z_0)^{12} = 1$ for $p=3$), settling $\chi > 1$ (and thus $\chi = 2$) across `qubit_H`, `qubit_T`, `H3`, and `N` in `5.36 s` total.
3. **Ephemeral cloud offload for heavy `.olean` caches:**
   A full Mathlib build cache occupies several gigabytes of disk and RAM. Offloading `lake exe cache get && LEAN_NUM_THREADS=2 lake build` to an ephemeral Linux container kept local laptop storage clean while verifying `#print axioms` (`[propext, Classical.choice, Quot.sound]`, `0 sorryAx`) on all 10 modules.

---

## Lesson 4 — Strict `Judge-vs-Submission Separation` on Fork Pull Requests

Before opening a PR from an external fork, read `.github/workflows/` line by line!
- In `unitaryfoundation/stabrank`, `.github/workflows/submissions.yml` sandboxes untrusted fork PRs (`SAME_REPO == "false"`): it checks out `$BASE` (`main`), overlays `bounds/*.json`, and checks out **only newly added** `verify_challenge/cert_*.py` scripts (`git diff --diff-filter=A`).
- Had we modified an existing helper script in `verify_challenge/` or bundled a workflow patch inside our proof PR, our local run would have passed while upstream CI silently ignored or rejected the diff.
- **Best Practice:** Keep proof/data PRs (`PR #193` for `bounds/` + `A`-only `cert_*.py`; `PR #194` for `lean_proofs/` only) **100% disjoint from verifier and CI infrastructure**, and submit any CI improvements (such as `lake exe cache get` and fork-PR `lean_proofs/` staging) as a dedicated standalone issue ([`Issue #195`](https://github.com/unitaryfoundation/stabrank/issues/195)).

---

## Lesson 5 — Audit Static-Site Leaderboard Aggregators Before Finalizing `provenance.author`

Automated scientific benchmarks frequently build contributor leaderboards straight from JSON provenance metadata. Inspecting `site_challenge/build.py` (`contributors()`) revealed that entries are grouped by the **exact `provenance.author` string** (`agg.setdefault(who, ...)` $\to$ `people/<slug>.html`), rather than by GitHub handle alone:
- Upgrading an existing literature or baseline bound without updating `provenance.author` (or mixing `"@handle"` and `"Team + @handle"` across waves) splits a single campaign into multiple fragmented rows on the public leaderboard.
- Auditing `site_challenge/build.py` before maintainer review allowed us to unify all `35` bounds in [`PR #193`](https://github.com/unitaryfoundation/stabrank/pull/193) under a single canonical string (`"author": "we* + @mizopl"`, `"github": ["mizopl"]`, `"llm": [{"model": "gemini", ...}]`).
