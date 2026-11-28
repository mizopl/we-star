# Pure-Kernel Lean 4.36.0 Certification Suite for Binary Multi-Deletion Codes

Standalone, zero-Mathlib Lean 4 (`v4.36.0`) kernel-checked proof suite for binary `s`-deletion-correcting codes of length `n`.

## Scope and Limitations First

1. **Prior known values vs. new Table-2 upper-bound tightening.**
   - The exact maximum code cardinalities `M_2(7) = 5`, `M_3(9) = 5`, `M_2(8) = 7`, `M_2(9) = 11`, `M_3(10) = 6`, `M_2(10) = 16`, and `M_3(11) = 8` were already established in prior literature via exhaustive search and SAT/ILP solvers (including OEIS A057591, Kulkarni and Kiyavash 2013, and Weindel and Heckel, arXiv:2504.00613v2). We do not claim new numerical cardinality values for those `n <= 11` parameters; the contribution there is standalone zero-Mathlib Lean 4 formalization.
   - On binary `(12, 3)` (`2^12 = 4,096` words), `Challenge.bounds_12_3` formally proves **`12 <= M_3(12) <= 13`** in the Lean 4.36.0 kernel (tightening both the `LP = 16` and 48-hour `ILP = 16` upper bounds reported in Weindel and Heckel, arXiv:2504.00613v2 Table 2, by `-3`, reducing Table 2's open gap from `4` to `1`). This does **not** prove `M_3(12) = 12`; closing `13 -> 12` remains open.
   - On binary `(12, 2)` (`2^12 = 4,096` words), a companion exact integer (non-Lean) Schrijver PSD certificate tightening Table 2 `ILP = 53` / `LP = 55` down to `M_2(12) <= 49` is included in `companion_certs/cert_psd_12_2_peeled.json.gz` (`3,830`-vertex peeled core, full-rank exact integer factor) and can be independently checked via `python3 companion_certs/verify_peeled_psd.py companion_certs/cert_psd_12_2_peeled.json.gz --corrupt` (`int64` overflow-checked exact integer verification with `0` floats, full `V x V` sweep, and `3/3` corruption rejections; not yet ported to Lean 4).
2. **Remaining open bounds in this suite.**
   - On `(10, 2)`, the formal upper bound proves `M_2(10) <= 17` alongside an explicit verified 16-word code (`16 <= M_2(10) <= 17`). On the peeled 836-vertex core, continuous Schrijver theta-prime evaluates to `17.7426`, so closing `17 -> 16` requires a relaxation beyond Schrijver theta-prime.
   - On `(16, 2)`, `Challenge.lower_bound_16_2_226` formally certifies **`M_2(16) >= 226`** (`minvol_226_v6356`, `|union D_2(C)| = 6,356`, zero collisions) directly inside the Lean 4 kernel. Companion modules `Cert_15_2` (`|C| = 137`), `Cert_15_3` (`|C| = 31`), `Cert_16_3` (`|C| = 44`), and `Cert_16_2` (`|C| = 219`) certify code validity and **inclusion-maximality** (no single word in `{0, 1}^n` can be appended to the code). Inclusion-maximality does **not** prove global cardinality optimality, and global upper bounds for `n in {15, 16}` remain open.
3. **Validation Tier (`Tier A`) and Trusted Computing Base.** All `36` target theorems listed in `AuditAxioms.lean` and `comparator.json` (`enable_nanoda: true`) compile under `leanprover/lean4:v4.36.0` with zero external libraries, `0 sorryAx`, `0 admit`, `0 native_decide`, `0 Lean.ofReduceBool`, `0 Lean.trustCompiler`, and `0` custom axioms, depending strictly on a subset of `[propext, Classical.choice, Quot.sound]`. `DeletionCode/Statements.lean` has `0` internal imports and defines the human-auditable TCB (`IsSubseq`, `InDelBall`, `HasCommonSubseqAtLeast`, `IsValidDeletionCode`, `IsInclusionMaximal`).
4. **One-command cold verification.** Run `bash verify_all.sh` from this directory (full cold sequential build, axiom audit, `comparator.json` parity, and `leanchecker`), or `bash verify_all.sh --quick` (`<30s` on a pre-built tree).

## Upper-Bound Hierarchy Comparison

Each row below compares the flat single-step deletion-ball LP bound (`LP_1`, Kulkarni and Kiyavash) and published Table-2 ILP bounds (Weindel and Heckel, arXiv:2504.00613v2) against the exact integer certificates formally checked in the Lean 4.36.0 kernel:

| `(n, s)` | `2^n` | `LP_1` / Table-2 `ILP` | `RecDual` (LP + CLQ + CG-1) | `PeelReduce + SchrijverPSD / FastSchrijver` (`T / S`) | Formal Theorem | Verified Result |
| :--- | ---: | :--- | :--- | :--- | :--- | :--- |
| `(7, 2)` | `128` | `5.76` (`<= 5`) / `5` | `DualLP` exact integer LP | not needed | `DeletionCode.DualLP.exact_opt_7_2` | `M_2(7) = 5` |
| `(9, 3)` | `512` | `5.50` (`<= 5`) / `5` | `DualLP` exact integer LP | not needed | `DeletionCode.DualLP.exact_opt_9_3` | `M_3(9) = 5` |
| `(8, 2)` | `256` | `8.25` (`<= 8`) / `8` | `312760360 / 40000000 = 7.8190` (`<= 7`) | not needed | `Challenge.exact_opt_8_2` | `M_2(8) = 7` |
| `(9, 2)` | `512` | `12.91` (`<= 12`) / `11` | `12.6095` (`<= 12`, unformalized) | rank `36`, `136` orbits: `737211 / 61585 = 11.9706` (`<= 11`) | `Challenge.exact_opt_9_2` | `M_2(9) = 11` |
| `(10, 3)` | `1024` | `7.53` (`<= 7`) / `6` | `279759124 / 39999995 = 6.9940` (`<= 6`) | peeled core `330` verts (`88` orbits) | `Challenge.exact_opt_10_3` | `M_3(10) = 6` |
| `(10, 2)` | `1024` | `20.47` (`<= 20`) / `16` | `795885064 / 39999994 = 19.8971` (`<= 19`, `Challenge.upper_bound_10_2`) | `2` balls + `20/20` `checkSubBall` -> `836` core, rank `96`: `2 + 63775738 / 3989359 = 17.9865` (`<= 17`) | `Challenge.upper_bound_10_2_psd` | `16 <= M_2(10) <= 17` |
| `(11, 3)` | `2048` | `10.90` (`<= 10`) / `8` | not formalized | `2` balls + `85` `D_2` steps (`80/85` `checkSubBall`) -> `1246` core, rank `32`: `2 + 43683368 / 6241589 = 8.9988` (`<= 8`) | `Challenge.exact_opt_11_3` | `M_3(11) = 8` |
| `(12, 3)` | `4096` | `16.27` (`<= 16`) / `16` (open) | not formalized | `2` balls + `106/106` `checkSubBall` (1 flat wave) -> `3090` core (`797` orbs), rank `48` `FastSchrijver`: `2 + 259188 / 21721 = 13.9326` (`<= 13`) | `Challenge.bounds_12_3` | **`12 <= M_3(12) <= 13`** |

Explicit code witnesses verified inside the kernel:
- `(8, 2)` (`|C| = 7`): `[0, 31, 42, 67, 188, 224, 255]`
- `(9, 2)` (`|C| = 11`): `[0, 7, 56, 63, 218, 292, 371, 407, 449, 504, 511]`
- `(10, 3)` (`|C| = 6`): `[0, 15, 180, 819, 960, 1023]`
- `(10, 2)` (`|C| = 16` lower bound): `[0, 15, 42, 120, 127, 193, 343, 460, 563, 674, 830, 896, 903, 981, 1008, 1023]`
- `(11, 3)` (`|C| = 8`): `[0, 15, 254, 312, 907, 1753, 1984, 2047]`
- `(12, 3)` (`|C| = 12` lower bound): `[0, 15, 240, 255, 780, 1390, 2197, 3315, 3840, 3855, 4080, 4095]`
- `(16, 2)` (`|C| = 226` lower bound): `DeletionCode.Cert_16_2_226.code` (`Challenge.lower_bound_16_2_226`)

## Complete 36-Theorem Inventory (`AuditAxioms.lean` and `comparator.json`)

### Reusable Core Theory and Engines
- `DeletionCode/Statements.lean`: zero-import TCB (`IsSubseq`, `InDelBall`, `HasCommonSubseqAtLeast`, `IsValidDeletionCode`, `IsInclusionMaximal`).
- `DeletionCode/Basic.lean`: `DeletionCode.disjoint_delBall_iff_no_common_subseq` (for all `s <= n`) and `DeletionCode.card_le_of_clique_cover`.
- `DeletionCode/RecDual.lean`: `DeletionCode.RecDual.weak_duality_rec_fast` (overlap-free 2x2 block recursion for `A_{n,s}^T y`, non-ball cliques via `canMatchNat`, rank-1 CG cuts, and `D_2 = <c, r>` symmetrization).
- `DeletionCode/SchrijverPSD.lean`: `DeletionCode.SchrijverPSD.weak_duality_schrijver_psd` and subgraph-restricted `weak_duality_schrijver_psd_on` (4-irrep Walsh-Hadamard integer Gram sum-of-squares verifier for all `s <= n`).
- `DeletionCode/PeelReduce.lean`: `DeletionCode.PeelReduce.weak_duality_peel_wave1_psd` and `weak_duality_peel_wave2_psd` (symbolic insertion-ball clique peeling, flat-wave `D_2`-orbit neighborhood domination, `checkSubBall` algebraic ball inclusion `D_s(x) subseteq D_s(y)`, and `canMatchNat_complete`).
- `DeletionCode/FastSchrijver.lean`: `DeletionCode.FastSchrijver.weak_duality_fast_peel_wave1_psd` (bit-parallel Kronecker-GMP `Nat.mul` polynomial-packed inner products + deletion-ball bitmask `Nat.land` edge verification, achieving `>10x` pure-kernel speedup with zero `native_decide`).

### Certified Instances
- **Challenge headline theorems (`Challenge.lean`):** `Challenge.exact_opt_8_2`, `Challenge.upper_bound_10_2`, `Challenge.exact_opt_10_3`, `Challenge.exact_opt_9_2`, `Challenge.upper_bound_10_2_psd`, `Challenge.exact_opt_11_3`, `Challenge.lower_bound_16_2_226`, `Challenge.bounds_12_3` (mirroring `DeletionCode.CutDual.exact_opt_8_2`, `DeletionCode.RecDual.cert_10_2_upper_bound`, `DeletionCode.RecDual.exact_opt_10_3`, `DeletionCode.SchrijverPSD.exact_opt_9_2`, `DeletionCode.PeelReduce.cert_10_2_psd_upper_bound`, `DeletionCode.PeelReduce.cert_10_2_psd_code_valid`, `DeletionCode.PeelReduce.exact_opt_11_3_psd`, `DeletionCode.Cert_16_2_226.valid`, `DeletionCode.PeelReduce.cert_12_3_psd_upper_bound`, `DeletionCode.PeelReduce.cert_12_3_psd_code_valid`).
- **Small LP exact optima and symmetry (`DeletionCode/DualLP.lean`):** `exact_opt_7_2`, `exact_opt_9_3`, `cert_16_3_klein4_invariant` (`|C| = 44` Klein-4 `<c, r>` invariance).
- **Large code validity and inclusion-maximality witnesses:** `Cert_15_2.valid` & `.inclusion_maximal` (`|C| = 137`), `Cert_15_3.valid` & `.inclusion_maximal` (`|C| = 31`), `Cert_16_3.valid` & `.inclusion_maximal` (`|C| = 44`), `Cert_16_2.valid` & `.inclusion_maximal` (`|C| = 219`), and `Cert_16_2_226.valid` (`|C| = 226`).

## Reusing `PeelReduce`, `SchrijverPSD`, and `FastSchrijver` on Other MIS and Code Problems

The verification engines are structured so external Lean 4 users can adapt them to other finite maximum independent set (MIS) or coding-theory conflict graphs without pulling in Mathlib:

1. **Integer Sum-of-Squares Gram bound (`SchrijverPSD.sos_gram_bound`):**
   Given any finite conflict graph `G = (V, E)` and an integer vector assignment `v : V -> Z^R` satisfying `||v(x)||^2 <= T - S`, `<v(x), v(y)> <= -S` for all distinct non-adjacent `x, y in V`, and exact positive integers `S > 0`, `T < (M + 1) * S`, the core algebraic identity `0 <= ||sum_{x in C} v(x)||^2 <= |C| * (T - |C| * S)` forces `|C| <= M` for every independent set `C` with zero floating-point arithmetic and zero square roots. Only `checkShift` and `applyD2` are binary-deletion-specific; replacing them adapts the verifier to non-binary alphabets (for instance `q = 4` DNA deletion codes with Watson-Crick complement and reversal) or general symmetric graphs.
2. **Pre-SDP graph reduction (`PeelReduce.lean`):**
   - **Symbolic clique peeling (`peel_balls_list`):** removing any clique `K` adds at most `1` to the independence number (`alpha(G) <= 1 + alpha(G \ K)`).
   - **Neighborhood domination (`peel_dom_single`, `peel_dom_orbit`, `peel_dom_wave_sound`):** if `x ~ y` and `N_H[x] subseteq N_H[y]` in the active subgraph `H`, replacing `y` by `x` preserves exact cardinality (`alpha(H) = alpha(H \ {y})`). Algebraic ball inclusion `checkSubBall` (`D_s(x) subseteq D_s(y)`) certifies `N[x] subseteq N[y]` in `O(C(n, s))` operations without scanning `H` (`20/20` on `(10, 2)`, `80/85` on `(11, 3)`, and `106/106` on `(12, 3)`).
3. **Bit-parallel Kronecker-GMP + `Nat.land` kernel acceleration (`FastSchrijver.lean`):**
   - In Lean 4's pure kernel (without `native_decide`), GMP C++ acceleration applies directly to `Nat` primitives (`Nat.mul`, `Nat.div`, `Nat.mod`, `Nat.ble`, `Nat.land`), while `List Int` recursion reduces in WHNF.
   - `FastSchrijver.kronecker_dot_eq` proves that shifting each entry by `+B` and packing a length-`r` block into base `K` (`r * (2B)^2 < K - 1`) recovers the exact inner product via ONE `Nat.mul` + `/` + `%`, while `land_ne_zero_implies_common_delBall` certifies conflict edges via ONE `Nat.land` on deletion-ball bitmasks.
   - On `(12, 3)` (`318,003` unordered orbit pairs, rank `48`), this reduced full sequential pair checking across 16 shards to `16s` build / `14s` `leanchecker` per shard (`~4` minutes total `leanchecker`, flat `<6 GB` swap on a 16 GB M1 laptop).
4. **Pure-kernel scaling notes for Lean 4.36.0 on modest RAM:**
   - Use `(by omega)` instead of `(by decide)` for arithmetic inequalities with large `Nat` literals.
   - Place sharded proof modules under a disjoint namespace prefix (for example `Cert_12_3_PSD_Shards/` separate from `Cert_12_3_PSD.lean`) so `lake env leanchecker DeletionCode.Cert_12_3_PSD` checks only the root module rather than re-checking every shard under the same prefix.
   - Build and `leanchecker`-verify heavy shards sequentially (`1` module at a time) to keep peak RAM compatible with 16 GB laptops and 7 GB CI runners.

## One-Command Cold Reproduction

Requires `elan` with the toolchain pinned in `lean-toolchain` (`leanprover/lean4:v4.36.0`) and Python 3 (standard library only).

```bash
# Full cold verification (TCB check, static forbidden-token scan, sequential lake build,
# AuditAxioms.lean + comparator.json 36/36 parity, and sequential lake env leanchecker):
bash verify_all.sh

# Fast verification on an already-built .lake cache (<30s):
bash verify_all.sh --quick
```

To enable continuous verification on GitHub Actions, copy `lean_verify.yml` into `.github/workflows/lean_verify.yml` (adjusting `working-directory` if this suite sits in a subdirectory).

---

Engineered and verified by **we\*** (`PROOFER` powered by Gemini + `@mizopl`).
https://github.com/mizopl/we-star
PS. we* = me + agentic systems (powered by Gemini) we* create
