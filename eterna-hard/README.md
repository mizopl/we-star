# Eterna-Hard (`Groups 1-3`, `Vienna 1.8.5`) + `eterna-validator` (`Martian 2`, `Vienna 2`): Solver, Designs & Barrier Certificates

Follow-up benchmark package for [`eternagame/eterna-hard`](https://github.com/eternagame/eterna-hard) and [`eternagame/eterna-validator`](https://github.com/eternagame/eterna-validator) requested by Prof. Rhiju Das (Stanford University / HHMI).

All results below were produced in two passes:
- **Phase I (`16h 22m` on a single `16 GB M1` laptop, `<= 4` CPU workers):** Python compositional-lifting + cutting-plane CEGIS port to `ViennaRNA 1.8.5` (`Turner 1999, dangles=1`) and `ViennaRNA 2.x` (`Turner 2004, dangles=2`) with exact nucleotide locks (`x`) and Kempe-swap pair-quota projections (`GC`/`AU`/`GU`), solving `11 / 300` on `eterna-hard` (`5` Group 1, `0` Group 2, `6` Group 3) + `1 / 1` on `eterna-validator/example/martian.csv`.
- **Phase II (`5h 42m` active multi-core C-kernel pass):** Native `-O3` C minimax cutting-plane accelerator ([`libR35_fast.c`](./libR35_fast.c), `3 ns` canonical-pair filter + move-to-front rival queue) and upper-triangle McCaskill partition-function scanner ([`pf_fast_scan.c`](./pf_fast_scan.c)), solving `+26` additional `eterna-hard` puzzles (`+6` Group 1, `+12` Group 2, `+8` Group 3) in `1.25 s - 110.66 s` per puzzle.

Total verified by unmodified [`eternagame/eterna-validator/check_design.py`](https://github.com/eternagame/eterna-validator/blob/main/check_design.py): **`37 / 300` (`12.3%`) across `eterna-hard` `Groups 1-3`** (`11 / 100` Group 1, `12 / 100` Group 2, `14 / 100` Group 3) **+ `1 / 1` on `eterna-validator/example/martian.csv`** (`38` total `check_design.py` solves; **`28 / 38`** strictly unique MFE under `--unique-mfe`: `27 / 37` on `Groups 1-3` + `1 / 1` on `martian.csv`).

---

## 1. One-Command Verification (`eterna-validator/check_design.py`)

Given local clones of [`eternagame/eterna-hard`](https://github.com/eternagame/eterna-hard) and [`eternagame/eterna-validator`](https://github.com/eternagame/eterna-validator), with `RNAFOLD_V1` pointing to `ViennaRNA-1.8.5/Progs/RNAfold` and `RNAFOLD_V2` pointing to `ViennaRNA 2.x` `RNAfold`:

```bash
# (A) Group 1: 11/11 designs pass; 11/11 puzzles solved (Vienna 1.8.5, solvers=1)
python3 check_design.py eterna-hard/groups/eterna-hard-group1.csv solved_group1.tsv

# (B) Group 2: 12/12 designs pass; 12/12 puzzles solved (Vienna 1.8.5, solvers=1)
python3 check_design.py eterna-hard/groups/eterna-hard-group2.csv solved_group2.tsv

# (C) Group 3: 14/14 designs pass; 14/14 puzzles solved (Vienna 1.8.5, solvers=1)
python3 check_design.py eterna-hard/groups/eterna-hard-group3.csv solved_group3.tsv

# (D) Validator multi-constraint control (#6158733 Mat - Martian 2: 1/1 pass, GU>=12, GC<=4, L=213, Vienna 2)
python3 check_design.py eterna-validator/example/martian.csv solved_martian.tsv
```

Full 100-row per-group frontier sweeps (`designs_group1.tsv`, `designs_group2.tsv`, `designs_group3.tsv`) can likewise be passed directly to `check_design.py` (`11/100`, `12/100`, and `14/100` pass). Under strict `--unique-mfe` (`RNASUBOPT` + `RNAEVAL` with `misc/rna_turner1999.par`), **`27 / 37`** `eterna-hard` solves (`9/11` Group 1, `8/12` Group 2, `10/14` Group 3) and **`1 / 1`** `martian.csv` (`28 / 38` overall) are certified strictly non-degenerate ground states (`n_mfe_tied = 1`).

---

## 2. Verified `check_design.py` Full Solves (`37 / 300` `eterna-hard` + `1 / 1` `martian.csv`)

| Group / File | `puzzle_id` | Title & Constraints | Engine | `--unique-mfe` | Solve Time | Verified Sequence |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| `Group 1` | `3058243` | `2 GU` (`SHAPE,0,GU,2`, `L=81`) | `Vienna 1.8.5` | `yes` | `0.20 s` | `CGGGGAGGGACGAGGAGGGAAACUACGGGACGCACGAAAAAAAAGCACAGGACACAGUAAAAAGCGGGGGGGACGGGGGGC` |
| `Group 1` | `3263351` | `3 AU` (`SHAPE,0,AU,3`, `L=49`) | `Vienna 1.8.5` | `yes` | `1.25 s` | `CGUGCCUGCUUGCUUGAGGAAACCUAUUGAACGUGACUGUGGACUGUGC` |
| `Group 1` | `3321286` | `Loop & Bulge` (`SHAPE,0`, `L=47`) | `Vienna 1.8.5` | `yes` | `12.12 s` | `ACUGGAGGGAAUUGGAAUGGGAGCGAUACGCACGACUGACGCGCAGG` |
| `Group 1` | `3349978` | `Less loops` (`SHAPE,0`, `L=59`) | `Vienna 1.8.5` | `yes` | `25.30 s` | `CACCCCACGGGACGGGACAGGGGGCUCCCAAAGGGAGGCGCGGCAGGCGGGAGAGGGUG` |
| `Group 1` | `3357791` | `Some loops` (`SHAPE,0`, `L=127`) | `Vienna 1.8.5` | `yes` | `16.46 s` | `AUCCAGUGGAAACGUCGGCACGCAGACGGAAACGCAGGGUCAGUCCGAUACGGUCAGCGAAACGCAGAGGCAAAGCCCAGUCCCAGGGCGAAAGCGCAGGGUGCACCCGAAAGGCGGGGAAAAAAAA` |
| `Group 1` | `3480541` | `Zanna : Wizzen` (`SHAPE,0,GU,5,GC,7`, `L=78`) | `Vienna 1.8.5` | `co-opt tie` | `11.78 s` | `GACAAAGUCAAGUUAAAAGUCAAAUGAGAGUAAAAUGAAAGAAAAAAAUAGAUGGACAGUAGGAGGAGACACGCGCAA` |
| `Group 1` | `3497795` | `1-1 with triloop` (`SHAPE,0`, `L=74`) | `Vienna 1.8.5` | `yes` | `7.50 s` | `CUGGGGGCAAGGAAACACGGCGGGCAAAGAAACAAAGGCGGCGGAAACACGGGCAAAGGCGGGCAAGGCGCGAG` |
| `Group 1` | `3620224` | `Based on Brourd's puzzle` (`SHAPE,0`, `L=68`) | `Vienna 1.8.5` | `yes` | `10.11 s` | `GGCAGGGAAGACGAAAGCACGCGAAAGACAGGUAGGACGAAAGCAAAGACCCCCACCUUCGGCGGGCC` |
| `Group 1` | `3654075` | `Move Along` (`SHAPE,0,GU,6,GC,9`, `L=114`) | `Vienna 1.8.5` | `co-opt tie` | `76.85 s` | `CUAAGAACGAAAGUCGGAAAAGUGUGAUAUCGAAAGAGCGAAGUCGAAGGAUGCAAGUUUAGAAAUAGAAUUCAGGAAAAAACAGUUAUGGGUGAAAAUGUAAACAAUUUAGAA` |
| `Group 1` | `3714598` | `Verity` (`SHAPE,0`, `L=126`) | `Vienna 1.8.5` | `yes` | `10.16 s` | `AGUGGCAGGACCCAGACCCACCCGGGGAAGUCGGCGAGUGGGAAACCCAAGGAAAACUAACGCCGCUCGGGCUGAAAAGACAACCCACGAGGAGAGGCAAGACGGGAAACGGCAAGGGCGGACGGC` |
| `Group 1` | `3720758` | `Flux` (`SHAPE,0,AU,5`, `L=78`) | `Vienna 1.8.5` | `yes` | `4.30 s` | `CGAGAGGAAACCUGGGGAGGGAAACACUGCAGCCUACGAAAGAGAGCACGAGGGAAACACUGGCGUCACGAAAGGAGG` |
| `Group 2` | `3161590` | `Interesting Intelligence` (`SHAPE,0,GU,4,GC,11`, `L=54`) | `Vienna 1.8.5` | `yes` | `18.28 s` | `CCCACAGGGUCUAGAUAGAGUUACUCACGCCAAUGGUUGUUUGGAGGCAUCGCC` |
| `Group 2` | `3163385` | `II2L` (`SHAPE,0,GU,4,GC,11`, `L=54`) | `Vienna 1.8.5` | `yes` | `97.27 s` | `GGCUAAGCCGAUAUAUAGAGAUUCUCAGGCCAAAGGUUGUGUGUCCCCAAUGGG` |
| `Group 2` | `4115808` | `Easy 4GU` (`SHAPE,0,GU,4`, `L=87`) | `Vienna 1.8.5` | `yes` | `66.78 s` | `GCCAGGAAACAGCGUUGCGUGGGACGGGAAACGAGGAAUUGCAAAUUUCGAGCGGGGAAACAGAAGGGGGUGGGGUGGGAAACAGGC` |
| `Group 2` | `4718738` | `Based on Hog's Owl` (`SHAPE,0`, `L=120`) | `Vienna 1.8.5` | `yes` | `110.66 s` | `GCGAGACAAAGCAGCUGCCCCGAAAGGGCCCGAAAAAGAAGAAAAAAAUAAAAAAAGGGUCGAAAGAGGCGAAAAUAAAAAAAUAAACAAAUAGCCGCGAAAGCGCAGCACCGAAAAAGG` |
| `Group 2` | `4732033` | `Easier Hog's BoostMe 28 mod` (`SHAPE,0`, `L=50`) | `Vienna 1.8.5` | `co-opt tie` | `27.53 s` | `ACGCACGUCGAAAGUUCAGCCGCAAGGGGUCAGAGGAAACCGGUCAGGGG` |
| `Group 2` | `4762862` | `Based on Tesla's Zoso` (`SHAPE,0,GC,19`, `L=89`) | `Vienna 1.8.5` | `co-opt tie` | `25.32 s` | `CCAUAGAGUAGAGAGACGAGGACUUCGGAUUGAAAAAUCGGAGCAGAGGAGAGAGAGACGAAAGCCCCCCCGCAAAGCCAGCAUGUACG` |
| `Group 2` | `4809779` | `Daniel B : Habit using Red mod` (`SHAPE,0,GU,2,GC,8,AU,3`, `L=56`) | `Vienna 1.8.5` | `yes` | `30.15 s` | `GGCGGGCGGGGGUGGGAGAAAUGUGAGCGGCGAGGGAGACGUGGGCACGGGUGGGC` |
| `Group 2` | `5028220` | `VirgieP3 : Squeek partial` (`SHAPE,0,GC,3,AU,22`, `L=98`) | `Vienna 1.8.5` | `co-opt tie` | `26.42 s` | `AAAAAUAUAAAAAAAUAUGAAAAUAAUUGACGACUCACAGCUAGGUACUUUAAAUAUGAAAAUAGAAAUAAUAAUGGAUCUUAAUACAAUAUGUAAAA` |
| `Group 2` | `5097853` | `Boost it right` (`SHAPE,0`, `L=50`) | `Vienna 1.8.5` | `yes` | `1.61 s` | `GGGUCCUGGAAGAAAUGAAAGCUGGGUGGAAUUGGAAACUGCUGCGGUCC` |
| `Group 2` | `5404826` | `Random Loops` (`SHAPE,0`, `L=55`) | `Vienna 1.8.5` | `yes` | `43.12 s` | `GCUGAAGUGGUGUGAUACUGACUGGAUGGGAAACGACUGGCCCUCUGCGAUUGGC` |
| `Group 2` | `8711679` | `Partial of "Kid on a Sky-Ride"` (`SHAPE,0`, `L=116`) | `Vienna 1.8.5` | `co-opt tie` | `65.61 s` | `AAAAAAAAAAAAAAAAAAAGCUGGGUCGGUGCGUGGGACGGCGGUGCGUAGAUUAUAUUUAUGCACGAGAGGCGAGGUGUGGUCGAAGUUUAGCGAAGUUAAACUUCGAGCCCAGA` |
| `Group 2` | `8718936` | `Tightened Tom` (`SHAPE,0,GU,3,GC,3,AU,3`, `L=40`) | `Vienna 1.8.5` | `yes` | `2.92 s` | `CGAGGUGUUUUCGAAAGGGAUUGUGAGAGUGAGUGUCUGG` |
| `Group 3` | `5583495` | `Unrestricted parachute man` (`SHAPE,0`, `L=64`) | `Vienna 1.8.5` | `co-opt tie` | `43.15 s` | `AACGGGGGACGGAAGGGGAGACGCAAGGGGAAAACGCACGGGGAAACGCAAGGGAAUAUCGCAA` |
| `Group 3` | `5741038` | `Choo's sequence extension` (`SHAPE,0`, `L=50`) | `Vienna 1.8.5` | `co-opt tie` | `3.30 s` | `GGGGACGUAGGGCAGGGGAGACGGAAACGCCGCACGAGACGCAGGGACCC` |
| `Group 3` | `5811869` | `Another Jerky` (`SHAPE,0`, `L=40`) | `Vienna 1.8.5` | `yes` | `4.26 s` | `CGACGCGGGACAGGGAGCGGAAACACGACGGACGAGGGCA` |
| `Group 3` | `5819498` | `4X4 L` (`SHAPE,0,AU,5`, `L=104`) | `Vienna 1.8.5` | `yes` | `56.06 s` | `GUCUUGGUGUCCUUGCUGGUAAUGGAAUUGUGGUGCCCUUGUUGCUAAAAUGUGAUGAAUCUGGAAAAGUGCUGCCCCUGGUGAAAAUGGUUAAAUGUUGAAGC` |
| `Group 3` | `5823364` | `Square` (`SHAPE,0`, `L=58`) | `Vienna 1.8.5` | `yes` | `37.03 s` | `GUGCUGGAAUUGUGAAACUGUGGAACUGGAAUGCUUUAUGCCCCUGCUUGCCUGGUGC` |
| `Group 3` | `5835186` | `NUNZIO'S Candle Stick` (`SHAPE,0,GC,2`, `L=50`) | `Vienna 1.8.5` | `yes` | `71.41 s` | `GUAGGGGGUUGGGCUGUAAAAUAGUGUCAUUAAGUGAUUUGAGUGUGUAU` |
| `Group 3` | `5837236` | `NUNZIO'S Long Candle Stick` (`SHAPE,0,GC,3`, `L=70`) | `Vienna 1.8.5` | `yes` | `90.60 s` | `GUGUGUGUGUGGGAGAGUGGUAUGAUGAAGUUAUAGUUCUAGGGUAGGAUCGAGUGUGUGGGGGGGGGGC` |
| `Group 3` | `5848426` | `Dmeyer : I can c you` (`SHAPE,0,GC,10`, `L=69`) | `Vienna 1.8.5` | `yes` | `36.32 s` | `GAUCAAUGAGUAUAAAAUACAGGAAUAUAAAAUAUAUAGCGCAGCAUCCAUAAUCAGUCAGCCAAAGGC` |
| `Group 3` | `5868257` | `NUNZIO's Mind's Eye` (`SHAPE,0`, `L=97`) | `Vienna 1.8.5` | `yes` | `4.94 s` | `GGACGAAAAUGGCAGGGAAAAAAAAAAAAAAAAAAAAAAAAAACCACCAGCAAAGCAGAGGCGCGAAACGGGACCCAGGGAAAAGCAAAAAAAGGAC` |
| `Group 3` | `5881353` | `Loop 1-...` (`SHAPE,0`, `L=71`) | `Vienna 1.8.5` | `yes` | `4.50 s` | `GCAAACAAACGAGGAAAGGACAAAAGGAAGGCAAAACCAAACGAAAAGGGGGGCACGGGACGCACGGGGGC` |
| `Group 3` | `5887125` | `1-...Loop 3` (`SHAPE,0`, `L=106`) | `Vienna 1.8.5` | `yes` | `6.60 s` | `GCAUCAAAAGGGGGAAAAGCAGCAGGAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAACGAGCAAAAGGCGCCAAAAACCGGAGAAAGGC` |
| `Group 3` | `5967883` | `Sequence Combination` (`SHAPE,0`, `L=83`) | `Vienna 1.8.5` | `co-opt tie` | `20.07 s` | `GGACCAGAGCCCGCCUGGCGAGGGAAUUGGAAUGGGAAUGGAAACAUACGACUGACGCGGCUGGGCGAGAGACGACGAGGCCU` |
| `Group 3` | `6104928` | `Tesla's Hook` (`SHAPE,0`, `L=78`) | `Vienna 1.8.5` | `co-opt tie` | `0.70 s` | `GCGGCAAAGGACGGGGCAGCAGGAAACGGGACGAGACAGCGGGACAAAGGGAAAAGGCGAAGGCACCAGCAAAAAGCA` |
| `Group 3` | `6184676` | `G Minor` (`SHAPE,0`, `L=46`) | `Vienna 1.8.5` | `yes` | `4.95 s` | `CCACGGGGGGAACGAUACGGGGAGACAACGCACGCAGGAAACAGGG` |
| `martian.csv` | `6158733` | `[VRNA_2]The Alternate Eterna100: Mat - Martian 2` (`GU>=12, GC<=4`, `L=213`) | `Vienna 2` | `yes` | `5.29 s` | `UGCUGCAAAGUAAAAUGGUUUAAUUAAUAGAGAAAAAAUUUAUUGUGAAUUAAAAUUAUGUCUAACAAAAAUAUUACUUUAUGUGAAAAAAAUAUAAAUAGUAUUAAAAUUGAUUUGAGUUUGAAAAAAAAAUUUGCGAUUGAUAAAAAAGGAUGUGAAACUAUAUGAAUUGAUAGAAAAAAUAUUGGUAAUUAUGUGACAACGAGGAAUCGU` |

---

## 3. 300-Puzzle Benchmark Statistics (`eterna-hard` `Groups 1-3`, `Vienna 1.8.5`)

- **Constraint satisfaction (`v_budget = 0`, all locked `x` bases and `GC`/`AU`/`GU`/`CONSECUTIVE_X` quotas satisfied):** **`299 / 300` (`99.7%`)** (`100/100` in Group 1, `100/100` in Group 2, `99/100` in Group 3; the sole positive-violation outlier is `#5905008 Mat - Lot of Locks 2` in Group 3 with 74 locked positions).
- **Base-pair symmetric-difference distance distribution (`d_bp` at `v_budget = 0`, `N = 300`):**
  - `d_bp = 0` (`check_design.py == PASS`): **`37 / 300` (`12.3%`)** (`11` Group 1, `12` Group 2, `14` Group 3; `38 / 301` including `martian.csv`)
  - `d_bp <= 1`: **`96 / 300` (`32.0%`)** (`37` at `d_bp = 0` + **`59` at `d_bp = 1`**: `28` Group 1, `19` Group 2, `12` Group 3; `97 / 301` including `martian.csv`)
  - `d_bp <= 2`: **`128 / 300` (`42.7%`)** (`+32` at `d_bp = 2`; cumulative `53` Group 1, `37` Group 2, `38` Group 3; `129 / 301` including `martian.csv`)
  - `d_bp <= 3`: **`148 / 300` (`49.3%`)**
  - `d_bp <= 5`: **`171 / 300` (`57.0%`)** (`63` Group 1, `55` Group 2, `53` Group 3)
  - `d_bp <= 10`: **`198 / 300` (`66.0%`)** (median `d_bp = 2.0` on Group 1, `5.0` on Group 2, `4.0` on Group 3, and **`4.0`** across all 300 puzzles)
- **Thermodynamic ground-state gap (`de_mfe = E(target) - E(MFE)` at `v_budget = 0`, `N = 300`):**
  - `de_mfe == 0.00 kcal/mol`: **`43 / 300`** (`37` solved at `d_bp = 0` + **`6` exact MFE ground-state degeneracies at `d_bp = 1`**: `#3151424 Brourd's Small and Crazy` [`E=-14.40`], `#3193338 Brourd's Combination` [`E=-22.20`], `#3439296 1 Locked nt` [`E=-11.10`], `#4627086 Easy Tesla's Particular` [`GU>=3, E=-23.00`], `#5404194 Sinker` [`E=-13.30`], and `#5877182 Stack & Loop` [`E=-15.95`]; see [`exact_ground_state_ties_de0.tsv`](./exact_ground_state_ties_de0.tsv)). Note that two Phase I ground-state ties (`#3357791 Some loops` and `#3161590 Interesting Intelligence`) were promoted to strict `--unique-mfe` full solves in Phase II.
  - `de_mfe <= 0.50 kcal/mol`: **`77 / 300`**; `de_mfe <= 1.00 kcal/mol`: **`95 / 300`**.
  - **Phase I local minimax barrier certificates (`Group 1`, `d_bp = 1`):** [`group1_barrier_certificates.json`](./group1_barrier_certificates.json) archives local cutting-plane minimax barrier certificates (`[0.00, +1.10] kcal/mol`) from the Phase I Group 1 `d_bp = 1` snapshot (`5` of those `18` puzzles were subsequently solved globally in Phase II once C-accelerated global coupling + Kempe swaps were enabled).

---

## 4. Technical Notes (`Vienna 2.x` to `Vienna 1.8.5` Port & C-API Pitfalls)

1. **`dangles=1` (`Vienna 1.8.5`) Single-Dot Multiloop Junction Competition (`ViennaRNA-1.8.5/lib/energy_par.c:53,91,250,262-266`):**
   On `.((....).).` 1-nt bulge branches inside multiloops, for the optimal inner assignment (`p0=GC, p1=CG, bg=A, fR=A/G`), the five internal energy terms between closed `.((....).).` and open `..(....)...` cancel to exact zero (`0.01 kcal/mol` units):
   $$\text{bulge}[1](+380) + \text{stack}[\text{GC},\text{GC}](-340) + \text{dangle3}[\text{GC}][\text{A/G}](-170) - (\text{dangle5}[\text{CG}][\text{G}](-20) + \text{dangle3}[\text{CG}][\text{A}](-110)) = 0.$$
   Thus the sole stabilizing term in `Turner 1999 (dangles=1)` is `dangle5[GC][fL='C'] = -30` (`-0.30 kcal/mol`). Across a shared single-dot junction `).((....).).`, `dangles=1` evaluates `min(dangle3[pair_left]['C'], dangle5[GC]['C'])`: if `pair_left` is `GC` (`-80`), `CG` (`-40`), `UG` (`-50`), or `UA` (`-50`), it steals `fL='C'` and pops the adjacent branch; restricting `pair_left` to `AU` (`-10`) or `GU` (`-10`) (`energy_par.c:264,266`) preserves the `-30` dangle and solved `#3620224`.
2. **Python `ViennaRNA 2.6.x` `eval_structure_simple` Default-Model Reset (`check_design.py:31-33` Counterpart):**
   Alongside the `Vienna 1.8.5` `subopt.c` `dangles=2` override noted in `check_design.py:31-33`, `ViennaRNA 2.6.4`'s Python binding `RNA.eval_structure_simple(seq, struct)` calls `vrna_eval_structure_simple()`, which instantiates a fresh default `vrna_md_t` (`Turner 2004, dangles=2`) on every call, silently ignoring global `RNA.params_load_RNA_Turner1999()` and `RNA.cvar.dangles = 1`. Replacing `RNA.eval_structure_simple` with `RNA.energy_of_struct(seq, struct)` (or `fold_compound(seq, md).eval_structure(struct)`) restores exact `0.01 kcal/mol` parity with `ViennaRNA-1.8.5`.
3. **Why Partition-Function Ensemble Defect (`Vienna 1.8.5 pf_fold`) Repels True `dangles=1` Solutions:**
   Just like `subopt.c`, `ViennaRNA-1.8.5`'s McCaskill partition function (`pf_fold` in `part_func.c`) evaluates ensemble probabilities under **`dangles=2`** rather than `dangles=1`. Empirically, `11 / 12` verified `dangles=1` MFE solutions on our hard control set exhibit apparent `pf_fold` ensemble defects of `ED = 13..33` (`#3357791 Some loops`: `ED_pf = 33.44`, `#5404826 Random Loops`: `ED_pf = 14.37`). Pure ensemble-defect minimization therefore actively walks *away* from valid `dangles=1` solutions unless coupled as a hybrid Stage-A basin proposer feeding an exact `dangles=1` C cutting-plane minimax polisher ([`libR35_fast.c`](./libR35_fast.c)).

---

## 5. Directory Manifest

- [`solved_group1.tsv`](./solved_group1.tsv), [`solved_group2.tsv`](./solved_group2.tsv), [`solved_group3.tsv`](./solved_group3.tsv), [`solved_martian.tsv`](./solved_martian.tsv): Drop-in TSVs verified directly by `check_design.py` (`11/11`, `12/12`, `14/14`, and `1/1` pass).
- [`all_38_solved_designs.tsv`](./all_38_solved_designs.tsv): Combined table of all `38` `check_design.py`-verified `d_bp = 0` designs (`37` `eterna-hard` + `1` `martian.csv`), including `unique_mfe` (`28/38`) and per-puzzle solve times.
- [`exact_ground_state_ties_de0.tsv`](./exact_ground_state_ties_de0.tsv): All `43` `Groups 1-3` designs achieving `de_mfe = 0.00 kcal/mol, v_budget = 0` (`37` solved at `d_bp = 0` + `6` exact ground-state degeneracies at `d_bp = 1`).
- [`frontier_300_summary.tsv`](./frontier_300_summary.tsv): Ranked table of all `300` `eterna-hard` designs across `Groups 1-3` (`group, puzzle_id, title, folder, d_bp, v_budget, de_mfe, sequence`).
- [`designs_group1.tsv`](./designs_group1.tsv), [`designs_group2.tsv`](./designs_group2.tsv), [`designs_group3.tsv`](./designs_group3.tsv): Full 100-puzzle `puzzle_id\tsequence` files for `Groups 1-3`.
- [`benchmark_300_summary.json`](./benchmark_300_summary.json): Machine-readable summary of `Groups 1-3` and `martian.csv` counts, `--unique-mfe` breakdown, and solved sequences.
- [`group1_barrier_certificates.json`](./group1_barrier_certificates.json): Phase I local cutting-plane minimax barrier certificates on Group 1.
- [`libR35_fast.c`](./libR35_fast.c), [`pf_fast_scan.c`](./pf_fast_scan.c): Native `-O3` C minimax cutting-plane evaluator (`3 ns` canonical-pair filter) and upper-triangle McCaskill `pr[]` scanner used in Phase II.
- [`cegis_eterna_hard_solver.py`](./cegis_eterna_hard_solver.py), [`adaptive_depth2_cutting_plane_solver.py`](./adaptive_depth2_cutting_plane_solver.py), [`certify_group1_barriers.py`](./certify_group1_barriers.py): Python solver and barrier certification scripts.
