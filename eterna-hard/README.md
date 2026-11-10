# Eterna-Hard (`Groups 1–3`, `Vienna 1.8.5`) + `eterna-validator` (`Martian 2`, `Vienna 2`) — Solver, Designs & Barrier Certificates

Follow-up benchmark package for [`eternagame/eterna-hard`](https://github.com/eternagame/eterna-hard) and [`eternagame/eterna-validator`](https://github.com/eternagame/eterna-validator) requested by Prof. Rhiju Das (Stanford University / HHMI).

All results below were generated in a `16h 22m` run on a single `16 GB M1` laptop (`<= 4` CPU workers) by porting the compositional-lifting + cutting-plane solver to `ViennaRNA 1.8.5` (`Turner 1999, dangles=1`) and `ViennaRNA 2.x` (`Turner 2004, dangles=2`) with exact lock propagation and Kempe-swap pair-budget projections (`GC`/`AU`/`GU` quotas).

---

## 1. One-Command Verification (`eterna-validator/check_design.py`)

Given local clones of [`eternagame/eterna-hard`](https://github.com/eternagame/eterna-hard) and [`eternagame/eterna-validator`](https://github.com/eternagame/eterna-validator) and `RNAFOLD_V1` pointing to `ViennaRNA-1.8.5/Progs/RNAfold`:

```bash
# (A) Group 1 (5/5 designs pass; 5/5 puzzles solved, Vienna 1.8.5)
python3 check_design.py eterna-hard/groups/eterna-hard-group1.csv solved_group1.tsv

# (B) Group 3 (6/6 designs pass; 6/6 puzzles solved, Vienna 1.8.5)
python3 check_design.py eterna-hard/groups/eterna-hard-group3.csv solved_group3.tsv

# (C) Flagship Vienna 2 validator constraint test (1/1 designs pass; GU>=12, GC<=4, L=213)
python3 check_design.py eterna-validator/example/martian.csv solved_martian.tsv
```

---

## 2. Verified `check_design.py` Full Solves (`d_bp = 0, v_budget = 0, de_mfe = 0.00 kcal/mol`)

| Group / File | `puzzle_id` | Title & Constraints | Engine | Solve Time | Verified Sequence |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `Group 1` | `3058243` | `2 GU` (`SHAPE,0,GU,2`, `L=81`, `solvers=1`) | `Vienna 1.8.5` | `0.20 s` | `CGGGGAGGGACGAGGAGGGAAACUACGGGACGCACGAAAAAAAAGCACAGGACACAGUAAAAAGCGGGGGGGACGGGGGGC` |
| `Group 1` | `3497795` | `1-1 with triloop` (`SHAPE,0`, `L=74`, `solvers=1`) | `Vienna 1.8.5` | `7.50 s` | `CUGGGGGCAAGGAAACACGGCGGGCAAAGAAACAAAGGCGGCGGAAACACGGGCAAAGGCGGGCAAGGCGCGAG` |
| `Group 1` | `3620224` | `Based on Brourd's puzzle` (`SHAPE,0`, `L=68`, `solvers=1`) | `Vienna 1.8.5` | `10.11 s` | `GGCAGGGAAGACGAAAGCACGCGAAAGACAGGUAGGACGAAAGCAAAGACCCCCACCUUCGGCGGGCC` |
| `Group 1` | `3714598` | `Verity` (`SHAPE,0`, `L=126`, `solvers=1`) | `Vienna 1.8.5` | `10.16 s` | `AGUGGCAGGACCCAGACCCACCCGGGGAAGUCGGCGAGUGGGAAACCCAAGGAAAACUAACGCCGCUCGGGCUGAAAAGACAACCCACGAGGAGAGGCAAGACGGGAAACGGCAAGGGCGGACGGC` |
| `Group 1` | `3720758` | `Flux` (`SHAPE,0,AU,5`, `L=78`, `solvers=1`) | `Vienna 1.8.5` | `4.30 s` | `CGAGAGGAAACCUGGGGAGGGAAACACUGCAGCCUACGAAAGAGAGCACGAGGGAAACACUGGCGUCACGAAAGGAGG` |
| `Group 3` | `5741038` | `Choo's sequence extension` (`SHAPE,0`, `L=50`, `solvers=1`) | `Vienna 1.8.5` | `3.30 s` | `GGGGACGUAGGGCAGGGGAGACGGAAACGCCGCACGAGACGCAGGGACCC` |
| `Group 3` | `5811869` | `Another Jerky` (`SHAPE,0`, `L=40`, `solvers=1`) | `Vienna 1.8.5` | `4.26 s` | `CGACGCGGGACAGGGAGCGGAAACACGACGGACGAGGGCA` |
| `Group 3` | `5868257` | `NUNZIO's Mind's Eye` (`SHAPE,0`, `L=97`, `solvers=1`) | `Vienna 1.8.5` | `4.94 s` | `GGACGAAAAUGGCAGGGAAAAAAAAAAAAAAAAAAAAAAAAAACCACCAGCAAAGCAGAGGCGCGAAACGGGACCCAGGGAAAAGCAAAAAAAGGAC` |
| `Group 3` | `5881353` | `Loop 1-...` (`SHAPE,0`, `L=71`, `solvers=1`) | `Vienna 1.8.5` | `4.50 s` | `GCAAACAAACGAGGAAAGGACAAAAGGAAGGCAAAACCAAACGAAAAGGGGGGCACGGGACGCACGGGGGC` |
| `Group 3` | `5887125` | `1-...Loop 3` (`SHAPE,0`, `L=106`, `solvers=1`) | `Vienna 1.8.5` | `6.60 s` | `GCAUCAAAAGGGGGAAAAGCAGCAGGAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAACGAGCAAAAGGCGCCAAAAACCGGAGAAAGGC` |
| `Group 3` | `6104928` | `Tesla's Hook` (`SHAPE,0`, `L=78`, `solvers=1`) | `Vienna 1.8.5` | `0.70 s` | `GCGGCAAAGGACGGGGCAGCAGGAAACGGGACGAGACAGCGGGACAAAGGGAAAAGGCGAAGGCACCAGCAAAAAGCA` |
| `martian.csv` | `6158733` | `[VRNA_2]The Alternate Eterna100: Mat – Martian 2` (`GU>=12, GC<=4`, `L=213`) | `Vienna 2` | `5.29 s` | `UGCUGCAAAGUAAAAUGGUUUAAUUAAUAGAGAAAAAAUUUAUUGUGAAUUAAAAUUAUGUCUAACAAAAAUAUUACUUUAUGUGAAAAAAAUAUAAAUAGUAUUAAAAUUGAUUUGAGUUUGAAAAAAAAAUUUGCGAUUGAUAAAAAAGGAUGUGAAACUAUAUGAAUUGAUAGAAAAAAUAUUGGUAAUUAUGUGACAACGAGGAAUCGU` |

---

## 3. 300-Puzzle Benchmark Statistics (`eterna-hard` `Groups 1–3`, `Vienna 1.8.5`)

- **Constraint satisfaction (`v_budget = 0`, all locked bases and `GC`/`AU`/`GU` quotas satisfied):** **`298 / 300` (`99.3%`)** (`100/100` in Group 1, `99/100` in Group 2, `99/100` in Group 3).
- **Base-pair distance distribution (`d_bp` at `v_budget = 0`, `N = 300`):**
  - `d_bp = 0`: **`11 / 300` (`3.7%`)** (`5` Group 1, `0` Group 2, `6` Group 3)
  - `d_bp <= 1`: **`48 / 300` (`16.0%`)** (`11` at `d_bp = 0` + `37` at `d_bp = 1`: `18` Group 1, `15` Group 2, `4` Group 3)
  - `d_bp <= 2`: **`74 / 300` (`24.7%`)** (`+26` at `d_bp = 2`: `31` Group 1, `25` Group 2, `18` Group 3)
  - `d_bp <= 3`: **`88 / 300` (`29.3%`)**
  - `d_bp <= 5`: **`113 / 300` (`37.7%`)** (`43` Group 1, `37` Group 2, `33` Group 3)
  - `d_bp <= 10`: **`150 / 300` (`50.0%`)** (median `d_bp = 7.0` on Group 1, `10.5` across all 300 puzzles)
- **Thermodynamic ground-state gap (`de_mfe = E(target) - E(MFE)` at `v_budget = 0`, `N = 300`):**
  - `de_mfe == 0.00 kcal/mol`: **`15 / 300`** (`11` solved at `d_bp = 0` + `4` exact MFE degeneracies at `d_bp = 1..2`: `#3357791 Some loops` [`d_bp=1, E=-41.50`], `#4627086 Easy Tesla's Particular` [`GU>=3, d_bp=1, E=-19.80`], `#3161590 Interesting Intelligence` [`GC<=11, GU>=4, d_bp=1, E=-6.90`], and `#3151424 Brourd's Small and Crazy` [`d_bp=2, E=-15.20`]; see [`exact_ground_state_ties_de0.tsv`](./exact_ground_state_ties_de0.tsv)).
  - `de_mfe <= 0.50 kcal/mol`: **`24 / 300`**; `de_mfe <= 1.00 kcal/mol`: **`30 / 300`**.
  - **Local minimax barrier certificates (`Group 1`, `d_bp = 1`):** All **`18 / 18`** Group 1 `d_bp = 1` designs are certified in [`group1_barrier_certificates.json`](./group1_barrier_certificates.json) with local cutting-plane minimax barriers in `[0.00, +1.10] kcal/mol` (`8` designs in `[+0.10, +0.20] kcal/mol`).

---

## 4. Technical Notes (`Vienna 2.x` $\to$ `1.8.5` Port)

1. **`dangles=2` (`Vienna 2`) vs `dangles=1` (`Vienna 1.8.5`) at Single-Dot Multiloop Junctions (`ViennaRNA-1.8.5/lib/energy_par.c:53,91,250,262-266`):**
   On `.((....).).` 1-nt bulge branches inside multiloops, for the optimal inner assignment (`p0=GC, p1=CG, bg=A, fR=A/G`), the five internal energy terms between closed `.((....).).` and open `..(....)...` cancel to exact zero (`0.01 kcal/mol` units):
   $$\text{bulge}[1](+380) + \text{stack}[\text{GC},\text{GC}](-340) + \text{dangle3}[\text{GC}][\text{A/G}](-170) - (\text{dangle5}[\text{CG}][\text{G}](-20) + \text{dangle3}[\text{CG}][\text{A}](-110)) = 0.$$
   Thus the sole stabilizing term in `Turner 1999 (dangles=1)` is `dangle5[GC][fL='C'] = -30` (`-0.30 kcal/mol`). Across a shared single-dot junction `).((....).).`, `dangles=1` evaluates `min(dangle3[pair_left]['C'], dangle5[GC]['C'])`: if `pair_left` is `GC` (`-80`), `CG` (`-40`), `UG` (`-50`), or `UA` (`-50`), it steals `fL='C'` and pops the adjacent branch; restricting `pair_left` to `AU` (`-10`) or `GU` (`-10`) (`energy_par.c:264,266`) preserves the `-30` dangle and solved `#3620224`.
2. **Python `ViennaRNA 2.6.x` C-API Counterpart to the `subopt.c` `dangles=2` Issue (`check_design.py:31-33`):**
   Alongside the `Vienna 1.8.5` `subopt.c` `dangles=2` override noted in `check_design.py:31-33`, `ViennaRNA 2.6.4`'s Python binding `RNA.eval_structure_simple(seq, struct)` calls `vrna_eval_structure_simple()`, which instantiates a fresh default `vrna_md_t` (`Turner 2004, dangles=2`) on every call — silently ignoring global `RNA.params_load_RNA_Turner1999()` and `RNA.cvar.dangles = 1`. Replacing `RNA.eval_structure_simple` with `RNA.energy_of_struct(seq, struct)` restored exact `0.01 kcal/mol` parity with `ViennaRNA-1.8.5`.

---

## 5. Directory Manifest

- [`solved_group1.tsv`](./solved_group1.tsv), [`solved_group3.tsv`](./solved_group3.tsv), [`solved_martian.tsv`](./solved_martian.tsv) — Drop-in TSVs verified by `check_design.py` (`5/5`, `6/6`, and `1/1` pass).
- [`all_12_solved_designs.tsv`](./all_12_solved_designs.tsv) — Combined table of all 12 `check_design.py`-verified `d_bp = 0` designs.
- [`exact_ground_state_ties_de0.tsv`](./exact_ground_state_ties_de0.tsv) — All 15 `Groups 1–3` designs achieving `de_mfe = 0.00 kcal/mol, v_budget = 0` (`11` at `d_bp = 0` + `4` exact ground-state degeneracies at `d_bp = 1..2`).
- [`frontier_300_summary.tsv`](./frontier_300_summary.tsv) — Ranked table of all 300 `eterna-hard` designs across `Groups 1–3` (`group, puzzle_id, title, folder, d_bp, v_budget, de_mfe, sequence`).
- [`designs_group1.tsv`](./designs_group1.tsv), [`designs_group2.tsv`](./designs_group2.tsv), [`designs_group3.tsv`](./designs_group3.tsv) — Full 100-puzzle `puzzle_id\tsequence` files for `Groups 1–3`.
- [`benchmark_300_summary.json`](./benchmark_300_summary.json) — Machine-readable summary of `Groups 1–3` counts and solved sequences.
- [`group1_barrier_certificates.json`](./group1_barrier_certificates.json) — Local cutting-plane minimax barrier certificates for all `18/18` Group 1 `d_bp = 1` designs.
- [`cegis_eterna_hard_solver.py`](./cegis_eterna_hard_solver.py), [`adaptive_depth2_cutting_plane_solver.py`](./adaptive_depth2_cutting_plane_solver.py), [`certify_group1_barriers.py`](./certify_group1_barriers.py) — Solver and barrier certification scripts.
