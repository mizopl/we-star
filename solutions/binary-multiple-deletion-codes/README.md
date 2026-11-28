# Three Pure-Scratch Binary Multiple-Deletion Codes Beating Table 2: (15,2)=137, (15,3)=31, and (16,3)=44, plus Pure-Kernel Lean 4.36.0 Upper Bounds up to `N = 4,096`

## Limitations First

- **Prior known `n <= 11` numerical values vs. new `n = 12` Table-2 tightenings:** The exact maximum cardinalities `M_2(7)=5`, `M_3(9)=5`, `M_2(8)=7`, `M_2(9)=11`, `M_3(10)=6`, `M_2(10)=16`, and `M_3(11)=8` were already established in prior literature via exhaustive search and SAT/ILP solvers (OEIS A057591, Kulkarni and Kiyavash 2013, Weindel and Heckel `arXiv:2504.00613v2`). We do not claim new numerical values for `n <= 11`; the contribution there is standalone zero-Mathlib pure-kernel Lean 4 formalization.
- **New `n = 12` upper-bound tightenings and remaining gaps:** On `(12, 3)` (`N = 4,096`), `Challenge.bounds_12_3` proves **`12 <= M_3(12) <= 13`** inside the Lean 4.36.0 kernel (tightening Table 2 `LP = 16` / 48-hour `ILP = 16` by `-3`, reducing Table 2's open gap from `4` to `1`; it does **not** prove `M_3(12) = 12`). On `(12, 2)` (`N = 4,096`), a companion exact big-integer certificate in `lean4_certs/companion_certs/` proves **`M_2(12) <= 49`** (tightening Table 2 `ILP = 53` by `-4` and `LP = 55` by `-6`, verified across all `7,332,535` pairs with `0` floats and `3/3 --corrupt` PASS) and is **not yet ported into Lean 4**. On `(10, 2)`, the Lean bound remains `16 <= M_2(10) <= 17` (continuous Schrijver theta-prime on the peeled 836-core is `17.7426`).
- **No `(16, 2)` frontier record or global optimality claimed for `n in {15, 16}`:** `Challenge.lower_bound_16_2_226` certifies validity of our `226`-word `(16, 2)` code (`minvol_226_v6356`, `|union D_2(C)| = 6,356`) inside the Lean 4 kernel (live EinsteinArena `#34` frontier is `226`), and `Cert_15_2` (`137`), `Cert_15_3` (`31`), `Cert_16_3` (`44`), and `Cert_16_2` (`219`) certify validity and full `2^n` 1-word inclusion-maximality. Validity and inclusion-maximality do **not** prove global cardinality optimality at `n in {15, 16}`.
- **No decoder efficiency or linearity claim.**

## What

Three pure-scratch binary multiple-deletion codes strictly improve the best-known constructive sizes in Table 2 of Weindel and Heckel (`arXiv:2504.00613v2`, TMLR June 2026): `(15,2)` has `137` distinct words (vs `136`, `|D_2|=3396`, `max LCS=12<13`), `(15,3)` has `31` distinct words (vs `30`, `|D_3|=1397`, `max LCS=11<12`), and `(16,3)` has `44` Klein-4-invariant distinct words (vs `42` and unmerged PR `#997=43`, `|D_3|=2344`, `max LCS=12<13`), paired with a standalone zero-Mathlib **Lean 4.36.0** certification suite (`lean4_certs/`, **`180` `.lean` files**, **`36/36` `Tier A` theorems**).

- `(15, 2)`: **137** distinct 15-bit words (`|D_2| = 3,396`, `max LCS = 12 < 13`, sorted-list `SHA-256` `2b226e2f0f7ab7fd...`), strictly above Table 2 `136` (`OnlineMIS`) and `CPro1` `132`.
- `(15, 3)`: **31** distinct 15-bit words (`|D_3| = 1,397`, `max LCS = 11 < 12`, sorted-list `SHA-256` `427002b54632ecc1...`), strictly above Table 2 `30` (`OnlineMIS`) and `CPro1` `29`.
- `(16, 3)`: **44** distinct 16-bit words (`|D_3| = 2,344`, `max LCS = 12 < 13`, Klein-4 `<c, r>`-invariant, sorted-list `SHA-256` `2580ff8bef1160cd...`), strictly above Table 2 `42` (`OnlineMIS`), `CPro1` `42`, and unmerged `V3R1T4S PR #997` (`43`). Three additional non-isomorphic `<rc>`, `<r>`, and `<c>` size-44 codes (`|D_3| = 2304, 2410, 2468`) are included under `object/companions/`.
- **Pure-kernel Lean 4.36.0 suite (`lean4_certs/`, `180` `.lean` files, `36/36` `Tier A` theorems):** `0` Mathlib, `0` internal imports in `DeletionCode/Statements.lean`, `0 sorryAx`, `0 admit`, `0 native_decide`, `0 Lean.ofReduceBool`, `0 Lean.trustCompiler`, `comparator.json` (`enable_nanoda: true`), and sequential `lake env leanchecker` PASS. Includes reusable `RecDual.lean`, `SchrijverPSD.lean`, `PeelReduce.lean`, and `FastSchrijver.lean` (Kronecker-GMP `Nat.mul` + 512-bit `Nat.land`, `>10x` pure-kernel speedup) engines certifying:
  - **`12 <= M_3(12) <= 13`** (`Challenge.bounds_12_3`, `N = 4,096`, `2` ball cliques + `106/106` `checkSubBall` `D_2` steps -> `3,090`-vertex core, rank-`48` PSD `2 + 259188 / 21721 = 13.9326 < 14`, tightening Table 2 `LP/ILP = 16` by `-3`),
  - **`M_2(16) >= 226`** (`Challenge.lower_bound_16_2_226`, `minvol_226_v6356`),
  - Exact `n <= 11` formalizations: `M_2(7)=5`, `M_3(9)=5`, `M_2(8)=7`, `M_2(9)=11` PSD, `M_3(10)=6`, `16 <= M_2(10) <= 17` PSD, and `M_3(11)=8` (`N = 2,048`), plus `2^n` inclusion-maximality on `137`, `31`, `44`, `219`.
- **Companion exact big-integer certificate (`lean4_certs/companion_certs/`, not yet in Lean 4):** **`M_2(12) <= 49`** (`N = 4,096`, `3,830`-vertex core, `985` orbits, `S = 24,941,860`, `T = 1,195,363,913`, `2 + T/S = 49.9260 < 50`), tightening Table 2 48-hour `ILP = 53` by `-4` and `LP = 55` by `-6`.

None of the constructive codes is a composition of published codebooks; all were built from scratch (word overlap with `CPro1` is `1` on `(15,2)`, `3` on `(15,3)`, and `10` on `(16,3)`; overlap with unmerged `PR #997` is `7`).

## Check it yourself

From this folder:

```sh
sh verify-it-yourself/run_checks.sh
```

Expected last line: `PASS` (under 1 second on a regular laptop; runs exact `D_s` disjointness, full pairwise DP `LCS`, Klein-4 invariance, Lean TCB/manifest parity, `SHA256SUMS`, and `--corrupt` negative control).

Optional full cold Lean 4.36.0 kernel verification from `lean4_certs/`:

```sh
cd lean4_certs && bash verify_all.sh
```

Optional exact big-integer verification of the companion `M_2(12) <= 49` certificate (`~25s`, requires `numpy`, `0` floats, includes `3/3 --corrupt` negative controls):

```sh
cd lean4_certs && python3 companion_certs/verify_peeled_psd.py companion_certs/cert_psd_12_2_peeled.json.gz --corrupt
```

## Compared to

Table 2 of Franziska Weindel and Reinhard Heckel, *LLM-Guided Search for Deletion-Correcting Codes*, TMLR 2026 (`arXiv:2504.00613v2`, fetched `2026-11-26T07:13:18Z`, HTTP 200, `sha256 = 4542bd58bc16be9bf47f6fc12f14fe86464c078c5a9c747058ee5698fbc7499a`):
- `(15, 2)`: `OnlineMIS = 136`, `ReduMIS = 135`, `CPro1 = 132`, LP upper bound `277`.
- `(15, 3)`: `OnlineMIS = 30`, `ReduMIS = t/o`, `CPro1 = 29`, LP upper bound `61`.
- `(16, 3)`: `OnlineMIS = 42`, `ReduMIS = t/o`, `CPro1 = 42`, LP upper bound `99`.
- `(12, 3)`: Table 2 `LP = 16`, 48-hour `ILP = 16` -> tightened to **`M_3(12) <= 13`** (`Challenge.bounds_12_3`, Lean 4 `Tier A`).
- `(12, 2)`: Table 2 `LP = 55`, 48-hour `ILP = 53` -> tightened to **`M_2(12) <= 49`** (exact big-integer Python in `companion_certs/`, not yet in Lean 4).

## Credits

Franziska Weindel and Reinhard Heckel (`arXiv:2504.00613v2`, TMLR 2026) for Table 2; Christopher D. Rosin (`arXiv:2505.23881`, `Constructive-Codes/CPro1`) for the public baseline codebooks; Landjev and Haralambiev (Serdica J. Comput. 2007) and the `OnlineMIS`/`ReduMIS` authors cited in Table 2; and the EinsteinArena `#34` contributors for public `(16,2)` structural benchmarks.
