# `we-star` (`we* = me + AI + the feedback loop`) — `PROOFER v20` Open-Science Release

> **What is `we-star` (`we*`)?** Across every commit, proof certificate, and scientific letter, we sign our work **`we*`** (*`we* = me (@mizopl) + the agentic systems we* create + the feedback loop`*), where `*` stands for both the **Kleene star ($W^*$)** of cumulative generation-to-generation learning and the **algebraic dual ($V^*$)** of flipping a stalled problem upside down ([see §5](#5-the-meaning-of-we-radical-openness--unedited-agent-reflections)).
>
> **Motto:** ***"Nothing material is perfect."*** — Inspired by [`V3R1T4S`](https://github.com/elder-plinius/V3R1T4S) (`@elder-plinius` — *Thank You!*), [`OpenClaw`](https://github.com/openclaw/openclaw) (`@steipete`), and [`autoresearch`](https://github.com/karpathy/autoresearch) (`@karpathy`), we release our working discovery architecture (`StartFresh_v19` / `v18` / `v16`), reasoning graphs, dead ends, and executable verifiers openly as-is.

<p align="center">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="./PROOFER-graph-v20-dark.png">
    <source media="(prefers-color-scheme: light)" srcset="./PROOFER-graph-v20.png">
    <img alt="PROOFER v20 Obsidian Knowledge and Decision Graph (Dark and Light Mode)" src="./PROOFER-graph-v20.png" width="480">
  </picture>
  <br>
  <em><b>Figure 0 — <code>PROOFER v20</code> Knowledge &amp; Decision Graph in Obsidian</b> (<code>2026-11-10</code>, <code>932</code> live Markdown notes across <code>330+</code> cycles; adaptive <a href="./PROOFER-graph-v20-dark.png">Dark</a> · <a href="./PROOFER-graph-v20.png">Light</a>). The dense upper-right supernova is the core <code>wiki/</code> &amp; constitutional hub, now bridging directly into a second multi-campaign constellation (<code>solutions/</code>, <code>stabrank/</code>, <code>Conway-99</code>, <code>Constitution Lab</code>, <code>Tug-of-War</code> gates, and <code>SEN</code> sleep dreams) framed by the outer observation crescent.</em>
  <br>
  <sub>⭐ If <code>we-star</code> inspires or helps your work, please consider giving the repository a Star · 📬 Free advice / collaboration: <a href="https://github.com/mizopl/we-star/issues/new">Open an Issue</a> or tag <code>@mizopl</code></sub>
</p>

<details>
<summary><b>🔭 Compare <code>PROOFER v19</code> vs. <code>PROOFER v20</code> Graph Evolution &amp; How Obsidian Birthed <code>rgraph.py</code></b> <i>(click to expand)</i></summary>
<br>

<table>
  <tr>
    <th align="center" width="50%"><code>PROOFER v19</code> Snapshot (<code>2026-10-28</code>)</th>
    <th align="center" width="50%"><code>PROOFER v20</code> Snapshot (<code>2026-11-10</code>, <code>932</code> Notes)</th>
  </tr>
  <tr>
    <td align="center">
      <picture>
        <source media="(prefers-color-scheme: dark)" srcset="./PROOFER-graph-dark.png">
        <source media="(prefers-color-scheme: light)" srcset="./PROOFER-graph.png">
        <img alt="PROOFER v19 Obsidian Knowledge Graph" src="./PROOFER-graph.png" width="340">
      </picture>
      <br>
      <sub><em><b><code>PROOFER v19</code></b> (<a href="./PROOFER-graph-dark.png">Dark</a> · <a href="./PROOFER-graph.png">Light</a>; earlier <code>v18</code> archived in <a href="./StartFresh_v18/README.md"><code>StartFresh_v18/</code></a>): ingested <code>V3R1T4S</code> problem supernova, central <code>CONSTITUTION</code> hub, and outer crescent.</em></sub>
    </td>
    <td align="center">
      <picture>
        <source media="(prefers-color-scheme: dark)" srcset="./PROOFER-graph-v20-dark.png">
        <source media="(prefers-color-scheme: light)" srcset="./PROOFER-graph-v20.png">
        <img alt="PROOFER v20 Obsidian Knowledge Graph" src="./PROOFER-graph-v20.png" width="340">
      </picture>
      <br>
      <sub><em><b><code>PROOFER v20</code></b> (<a href="./PROOFER-graph-v20-dark.png">Dark</a> · <a href="./PROOFER-graph-v20.png">Light</a>): full <code>932</code>-note binary-star constellation uniting <code>wiki/</code>, <code>CONSTITUTION_LAB/</code>, <code>hall_of_fame/</code>, <code>tug/</code>, and 35 standalone campaign packages.</em></sub>
    </td>
  </tr>
</table>

**[Obsidian](https://obsidian.md/)** serves as `@mizopl`'s live visual cockpit over the filesystem — and directly birthed the agent's own reasoning-graph engine ([`rgraph.py`](./StartFresh_v16/scripts/rgraph.py)):
1. **`v1`–`v8` (`Wiki OS`):** Step 7 required compiling spatial mindmaps as native Obsidian `.canvas` JSON files (`1=red`..`6=purple`).
2. **`v9` (`2026-10-17`):** `@mizopl` prompted: *"Create reasoning graphs readable for yourself, so you don't walk in circles."*
3. **`rgraph.py`:** Translated Obsidian's node/edge/color model into append-only `.jsonl` decision trees (`question -> hypothesis -> experiment -> kill/close`) that block duplicate dead ends (`exit 2`) and export directly back to `.canvas` boards. *(Full trace in [`docs/12_MANIFESTO_OBSIDIAN_LINEAGE_AND_AGENT_REFLECTIONS.md`](./docs/12_MANIFESTO_OBSIDIAN_LINEAGE_AND_AGENT_REFLECTIONS.md).)*

</details>

---

## 1. Live `we*` Status, Upstream Merges & Field Notes

> **15-Second Verification Summary (Built on Google Antigravity `AGY` & Gemini + Claude Code):** Across **330+ autonomous cycles** on a `16 GB M1 laptop` (with heavy compute offloaded on demand), `we-star` (`PROOFER`) has produced **35 machine-verified scientific & mathematical benchmark solutions** (`43` proof packages on [`elder-plinius/V3R1T4S`](https://github.com/elder-plinius/V3R1T4S) spanning all `18 / 18` scientific domains, the 300-puzzle [`./eterna-hard/`](./eterna-hard/) package, and the [`./stabrank/`](./stabrank/) package for [`unitaryfoundation/stabrank`](https://github.com/unitaryfoundation/stabrank)), including **52 zero-axiom (`0 sorryAx`) Lean 4 proof modules/theorems**.
>
> **Latest Lab Dispatches ([`./news/`](./news/)):**
> - **[Field Notes #002 (`2026-11-10`)](./news/2026-11-10_field_notes_magic_states_10s_eterna_hard_and_github_replays.md):** Two-way collaboration with Ralph (`@ibenarb`) on Conway-99 (`42.66B` nodes), 2 months of Z3/CP-SAT reduced to `10.74 s` on `RM(3,7)` (`PR #1043`), `Eterna-Hard` & a `ViennaRNA 2.6.4` C-API bug, 6 `V3R1T4S` merges, and why `we*` means shared joy.
> - **[Field Notes #001 (`2026-11-02`)](./news/2026-11-02_field_notes_small_wins_agent_mail_and_constitution_v20.md):** `Conway-99` peer-review surgery, `V3R1T4S#433` & `MatMulCatalog#21` (`REFERENCES [92]`) merges, agent-to-agent mail (`XERJ`), restoring Classic `CLSS` in `CONSTITUTION v20`, and a direct note from `MONITOR`.

| External Repository / Catalog | Status & Key Contribution | Links & Verification |
|:---|:---|:---|
| **[`teorth/optimizationproblems`](https://github.com/teorth/optimizationproblems)** (`#27`) | **`MERGED` as `[M2026]` (`PR #236`):** Odd-base ($b=9,13$) finite-bound proof $C_{3a} \le 1.3833368691$ in [`constants/3a.md`](https://github.com/teorth/optimizationproblems/blob/main/constants/3a.md); `PR #339` ($c_{3e} \ge 2.207281623640$) & `PR #340` independently replayed in [`quantavane-replays`](https://github.com/arhancanli/quantavane-replays), [`quantavane-mcp`](https://github.com/arhancanli/quantavane-mcp) & [`math-certificates`](https://github.com/rpinho/math-certificates) | [PR #236 (`MERGED`)](https://github.com/teorth/optimizationproblems/pull/236) · [PR #339](https://github.com/teorth/optimizationproblems/pull/339) · [PR #340](https://github.com/teorth/optimizationproblems/pull/340) · [Proof Repo](https://github.com/mizopl/ghr-c3a-odd-base-finite-bound) |
| **[`unitaryfoundation/stabrank`](https://github.com/unitaryfoundation/stabrank)** (`#35`) | **Submitted (`3h 34m` end-to-end, `4/4` bets won):** `35/35` exact $\mathbb{Z}[i]$ & $\mathbb{Z}[\omega_3]$ stabilizer-rank bounds at `tier=verified` in `20.46 s` (`PR #193`, up to `350x` faster) + `10/10` zero-axiom (`0 sorryAx`) Lean 4 modules (`PR #194`) + fork-CI report (`Issue #195`) | [PR #193](https://github.com/unitaryfoundation/stabrank/pull/193) · [PR #194 (Lean 4)](https://github.com/unitaryfoundation/stabrank/pull/194) · [Issue #195](https://github.com/unitaryfoundation/stabrank/issues/195) · [`./stabrank/`](./stabrank/) · [`LESSONS_LEARNED.md`](./stabrank/LESSONS_LEARNED.md) |
| **[`eternagame/eterna100-benchmarking`](https://github.com/eternagame/eterna100-benchmarking/issues/14) & [`eterna-hard`](https://github.com/eternagame/eterna-hard)** (`#32`) | **De novo RNA inverse folding:** `95/100` (`d_bp=0`) on `Eterna100-V2` (vs `DesiRNA = 92/100`) + 3 Turner undesignability laws (`V3R1T4S PR #1031`); on 300-puzzle `eterna-hard`: `12` historical `solvers=1` solves (`check_design.py` `PASS`), `75/300` at `d_bp<=2`, `18/18` Group 1 barriers & `ViennaRNA 2.6.4` C-API `dangles=2` bug report | [`V3R1T4S` PR #1031](https://github.com/elder-plinius/V3R1T4S/pull/1031) · [`eterna100#14`](https://github.com/eternagame/eterna100-benchmarking/issues/14) · [`./eterna-hard/`](./eterna-hard/) · [`./solutions/eterna100-v2-vienna2-algorithmic-solve/`](./solutions/eterna100-v2-vienna2-algorithmic-solve/) |
| **[`solven-eu/matmulcatalog`](https://github.com/solven-eu/matmulcatalog/pull/21) & [`FastMatrixMultiplication`](https://github.com/dronperminov/FastMatrixMultiplication)** (`#8, #15`) | **`MERGED` (`PR #21`, `REFERENCES [92]`):** `mizopl/we-star` wired in as a 3-hourly automated upstream source (`UpstreamSchemeRepos.MIZOPL`, `52` scheme files across 11 `ZT`/`Z` rank reductions + 48 SLPs); 4 ternary schemes merged in `FastMatrixMultiplication` | [`MatMulCatalog` PR #21](https://github.com/solven-eu/matmulcatalog/pull/21) · [`FastMatrixMultiplication`](https://github.com/dronperminov/FastMatrixMultiplication) · [`V3R1T4S` PR #616 (`MERGED`)](https://github.com/elder-plinius/V3R1T4S/pull/616) |
| **[`codetables.de`](https://www.codetables.de) & Quantum `AME` / Magic States** (`#9, #33, #34`) | **Published upstream in `codetables.de`:** 5 optimal quantum stabilizer codes over $\mathbb{F}_5, \mathbb{F}_7, \mathbb{F}_8, \mathbb{F}_9$ + 1,008-cell purity audit (`PR #975`), 19 `AME` closures (`95/95` prime-power $D \ge 11, n \le 20$), `8.50 s` Galois stabilizer-rank lower bounds (`PR #1039`), and `10.74 s` `RM(3,7)` proof of $N_{\text{CCZ}}(4)=10, N_T(4)\ge 9$ (`PR #1043`) | [`codetables.de`](https://www.codetables.de) · [PR #975](https://github.com/elder-plinius/V3R1T4S/pull/975) · [PR #1039](https://github.com/elder-plinius/V3R1T4S/pull/1039) · [PR #1043](https://github.com/elder-plinius/V3R1T4S/pull/1043) |
| **[`ihtc2024`](https://github.com/ihtc2024/ihtc2024.github.io/commit/c078cf57) & [`elder-plinius/V3R1T4S` `main`](https://github.com/elder-plinius/V3R1T4S/pulls?q=is%3Apr+author%3Amizopl+is%3Amerged)** (`#7, #12, #16, #18, #24`) | **`MERGED` upstream:** 31 official hospital timetabling Best-Known Solutions (`c078cf57`) + **6 PRs merged into `V3R1T4S` `main`** (`#366` 45-digit `OEIS A054759(15)` confirmed in `#459`, `#433` DNA minimizer `0.136569`, `#517` & `#723` Lychrel Base-50/98, `#616` ternary SLPs, `#617` Herculaneum `PHerc. 343`) | [`IHTC-2024` `c078cf57`](https://github.com/ihtc2024/ihtc2024.github.io/commit/c078cf57) · [Merged `V3R1T4S` PRs](https://github.com/elder-plinius/V3R1T4S/pulls?q=is%3Apr+author%3Amizopl+is%3Amerged) |
| **[`mizopl/conway-99-graph`](https://github.com/mizopl/conway-99-graph) $\leftrightarrow$ [`ibenarb/conway99-research`](https://github.com/ibenarb/conway99-research)** (`#5`) | **Formalized & adopted:** `42` zero-axiom (`0 sorryAx`) Lean 4 theorems (`5 Master Theorems`), `54` Pure-RUP LRAT UNSAT certificates ($p=7$ `p7_fix1` in `0.82 s`), unconditional `(0,7,0)` $k_{\text{type1}} \ge 1$ closure (`42.66B` nodes), with 62-class `(M,E)` & `Stab8` adopted by `@ibenarb` | [`mizopl/conway-99-graph`](https://github.com/mizopl/conway-99-graph) · [PR #774](https://github.com/elder-plinius/V3R1T4S/pull/774) · [PR #840](https://github.com/elder-plinius/V3R1T4S/pull/840) |

---

## 2. Compact Index of All 35 Verifiable Scientific & Mathematical Campaigns

> 📖 **Full Unabridged Benchmark Atlas (with complete derivations, scientific significance & complexity notes on `P`/`NP` vs. `#P`/`NPO`):** **[`docs/00_FULL_BENCHMARK_ATLAS.md`](./docs/00_FULL_BENCHMARK_ATLAS.md)**

| # | Benchmark & Domain | Key Machine-Verified Result | Verify & Links |
|---:|:---|:---|:---|
| **1** | **TraitGym Non-Coding Variants** (*Clinical Genomics*) | CADD-free zero-shot `0.7896` AUPRC (`+0.0774`, `9/9` subsets); exposes `MAF-Matching Shortcut` & $L_2$ dilution $\alpha = 114/7611$ | [PR #769](https://github.com/elder-plinius/V3R1T4S/pull/769) · [Package](./solutions/traitgym-mendelian-zero-shot-auprc/) |
| **2** | **Single-Cell CRISPRi Perturbation** (*Functional Genomics*) | Distance-to-training decomposition (`p2`, 5 cohorts) + Hollow LOO graph regression K562 $L_2$: `4.0970 -> 3.3203` (`-18.96%`) | [PR #766](https://github.com/elder-plinius/V3R1T4S/pull/766) · [Package](./solutions/linear-baseline-perturbation-replogle-k562/) |
| **3** | **FLAb Antibody Developability** (*Protein Biophysics*) | `11/14` aggregation/polyreactivity datasets won (zero learned params); proves unweighted $\|\rho\|$ Simpson's Paradox & germline confounding | [PR #767](https://github.com/elder-plinius/V3R1T4S/pull/767) · [Package](./solutions/flab-antibody-developability-zero-shot/) |
| **4** | **Missing Degree-57 Moore Graph** (*Algebraic Graph Theory*) | Excludes $\|\mathrm{Aut}(\Gamma)\| \in \{275, 175\}$, $C_{55}$ Case A & 11 even orders (`p1`) + verifies all 22 prime orders of `2606.29183v2` (`p2`) | [PR #770](https://github.com/elder-plinius/V3R1T4S/pull/770) · [PR #983](https://github.com/elder-plinius/V3R1T4S/pull/983) · [Package](./solutions/moore-graph-57/) |
| **5** | **Conway's 99-Graph Problem** (*Combinatorics, Lean 4 & LRAT*) | `54` Pure-RUP LRAT proofs ($p=7$ in `0.82 s`), `42` `0 sorryAx` Lean 4 theorems, unconditional `(0,7,0)` $k_{\text{type1}} \ge 1$ (`42.66B` nodes) | [Repo](https://github.com/mizopl/conway-99-graph) · [PR #774](https://github.com/elder-plinius/V3R1T4S/pull/774) · [PR #840](https://github.com/elder-plinius/V3R1T4S/pull/840) |
| **6** | **Blind MHC-I Peptide Binding** (*Cancer Immunotherapy*) | Blind ROC-AUC `0.8896` across 87 datasets (beats `NetMHC`/`NetMHCpan`), `+2.08%` on 20 rarest HLA alleles via Tobit censoring calibration | [PR #763](https://github.com/elder-plinius/V3R1T4S/pull/763) · [Package](./solutions/iedb-mhci-bd2009-blind-auc/) |
| **7** | **Healthcare Timetabling (`IHTC-2024`)** (*Operations Research*) | **31 official Best-Known Solutions merged upstream** (`i27 = 50,063`, hidden `m28 = 45,873`, `0` hard violations) | [Merge `c078cf57`](https://github.com/ihtc2024/ihtc2024.github.io/commit/c078cf57) · [PR #416](https://github.com/elder-plinius/V3R1T4S/pull/416) · [PR #431](https://github.com/elder-plinius/V3R1T4S/pull/431) |
| **8** | **Ternary $\mathbb{Z}_T$ Fast Matrix Multiplication** (*Algebraic Complexity*) | **11 ternary/integer rank reductions** (`9x12x14 -> 954`, `10x15x15 -> 1389`, `12x15x15 -> 1640`, `14x15x15 -> 1894`), merged in `MatMulCatalog` | [`MatMulCatalog#21`](https://github.com/solven-eu/matmulcatalog/pull/21) · [PR #402](https://github.com/elder-plinius/V3R1T4S/pull/402) · [PR #615](https://github.com/elder-plinius/V3R1T4S/pull/615) |
| **9** | **Quantum `AME` & `MDS` Stabilizer Codes** (*Quantum Error Correction*) | 4 Huber $D \le 10$ cells (`AME(9..11,10)`, `AME(17,8)`) + 15 $D \ge 11$ closures (`95/95` for $n \le 20$) + 5 `codetables.de` codes & 1,008-cell audit | [PR #576](https://github.com/elder-plinius/V3R1T4S/pull/576) · [PR #614](https://github.com/elder-plinius/V3R1T4S/pull/614) · [PR #975](https://github.com/elder-plinius/V3R1T4S/pull/975) · [Package](./solutions/ame-states-open-cells-huber-table/) |
| **10** | **Fault-Tolerant Quantum Compilation** (*Reversible Arithmetic*) | `03_invsqrt`: `Q = 103` qubits (`-56.2%`), `T = 3,396` Toffolis (`-61.6%`), `5.694x` score verified across all `3,133,452` inputs | [Derivation](./docs/01_OUR_JOURNEY_AND_RESULTS.md#step-3-fmm--addition-slps--quantum-ame-longrightarrow-quantum-circuit-compilation--reversible-addition-wave-5-synthesis) |
| **11** | **Symmetric $\mathbb{F}_2$ Waring Rank (`polytof`)** (*Quantum $T$-Count*) | 88-tensor audit + 4 repaired `.npy` (`p3`), `0725` $\mathrm{GF}(2^2)$ optimality (`CP=3, Waring=17`), `GF(2^9)` `147->139` (`0.17 s`), `GF(2^10)` `173->161` | [PR #761](https://github.com/elder-plinius/V3R1T4S/pull/761) · [PR #973](https://github.com/elder-plinius/V3R1T4S/pull/973) · [Package](./solutions/polytof-toffoli-tcount-benchmark-tensors/) |
| **12** | **Lychrel Numbers in New Bases** (*Number Theory*) | First proven non-$2^k$ bases since 1996: $b = 50, 98, 146$ in `41 min` (`#517` & `#723` `MERGED`) + 11 bases in $b \equiv 2 \pmod{24}$ | [PR #517](https://github.com/elder-plinius/V3R1T4S/pull/517) · [PR #723](https://github.com/elder-plinius/V3R1T4S/pull/723) · [Repo](https://github.com/mizopl/lychrel-bases-50-98-146-proof) |
| **13** | **TCR–Epitope Specificity (`ImmRep22`)** (*Immunology*) | Mean MicroAUC `0.8822` vs `0.8473` (`+0.0348`) across 17 unseen viral/cancer peptides (`p1..p3`) | [PR #569](https://github.com/elder-plinius/V3R1T4S/pull/569) · [Kit](./Evolved_Agent_Wiki/reports/04_preprints_and_domain_kits/) |
| **14** | **MoleculeACE Activity Cliffs** (*Cheminformatics*) | Single global blend (`0.55 ET + 0.45 SVR`) wins `29/30` ChEMBL targets on Overall RMSE (`0.6431` vs `0.7336`) & `27/30` on Cliff RMSE | [PR #568](https://github.com/elder-plinius/V3R1T4S/pull/568) · [Graph](./StartFresh_v16/graphs/ancestral_v15_atlas/polaris-moleculeace-activity-cliff-mse.jsonl) |
| **15** | **Vector Addition SLP Complexity** (*Arithmetic Circuits*) | **4 ternary $\mathbb{Z}_T$ SLP addition records (`MERGED`)** from a 48-SLP sweep (`3x3x7` `167`, `3x5x6` `245`, `3x5x7` `294`, `5x6x6` `492`) | [PR #616 (`MERGED`)](https://github.com/elder-plinius/V3R1T4S/pull/616) · [`MatMulCatalog#21`](https://github.com/solven-eu/matmulcatalog/pull/21) |
| **16** | **Hard-Square Lattice Gas Counts** (*`#P` Statistical Mechanics*) | **45-digit `OEIS A054759(15)` (`MERGED`, confirmed in `#459`)** + full 80-entry antidiagonal $d=79$ of `A089980` via dihedral CRT | [PR #366 (`MERGED`)](https://github.com/elder-plinius/V3R1T4S/pull/366) · [PR #462](https://github.com/elder-plinius/V3R1T4S/pull/462) |
| **17** | **JARVIS Small-Data Materials** (*Condensed Matter*) | `tinnet_N_ead` MAE `0.1293 eV` vs `0.1419 eV` (`-8.91%`, beats Matminer/ALIGNN) + strictly inductive 5-fold CV audit | [PR #599](https://github.com/elder-plinius/V3R1T4S/pull/599) · [Graph](./StartFresh_v16/graphs/ancestral_v15_atlas/jarvis-small-data-exfoliation-tc-mae.jsonl) |
| **18** | **DNA Minimizer Density Records** (*Genomic Indexing*) | New 4-ary DNA records: `(w=12, k=3)` `0.136569` (`-1.32%`, `MERGED` `#433`) & `(w=12, k=4)` `0.132770` (`-0.71%`, `#976`) | [PR #433 (`MERGED`)](https://github.com/elder-plinius/V3R1T4S/pull/433) · [PR #976](https://github.com/elder-plinius/V3R1T4S/pull/976) |
| **19** | **`VNN-COMP 2026` Neural Verification** (*AI Formal Safety*) | Certified adversarial counterexample $x^*$ (`margin = -0.589 < 0` in `fp32`/`fp64`) for unsolved `tinyimagenet_eps1_wide_cnn7_idx7687_sample8` | [PR #566](https://github.com/elder-plinius/V3R1T4S/pull/566) · [Graph](./StartFresh_v16/graphs/ancestral_v15_atlas/vnncomp-2026-unsolved-instance-counterexample.jsonl) |
| **20** | **La Jolla Covering Designs (`LJCR`)** (*Extremal Combinatorics*) | 3 improved upper bounds: $C(94,13,5) \le 125,184$ (`-4,019`), $C(68,14,5) \le 15,675$ (`-329`), $C(40,16,7) \le 7,251$ (`-219`) | [PR #397](https://github.com/elder-plinius/V3R1T4S/pull/397) · [PR #398](https://github.com/elder-plinius/V3R1T4S/pull/398) · [PR #435](https://github.com/elder-plinius/V3R1T4S/pull/435) |
| **21** | **Degree–Diameter Graph Table** (*Network Topology*) | New graph of order $N = 1,118$ for $(d=14, k=3)$ (`+2` vertices over Comellas's $1,116$ record, moved to `known-knowns/`) | [PR #457](https://github.com/elder-plinius/V3R1T4S/pull/457) · [Graph](./StartFresh_v16/graphs/ancestral_v15_atlas/degree-diameter-table.jsonl) |
| **22** | **Bimetallic Gupta Nanoalloys** (*Computational Chemistry*) | 8 new lower-energy global minima across `Cu-Ag` 55-atom clusters ($\text{Cu}_{39}\text{Ag}_{16}$ at `-163.80214 eV`, $\Delta E = -1.19\text{ eV}$) | [PR #466](https://github.com/elder-plinius/V3R1T4S/pull/466) · [Graph](./StartFresh_v16/graphs/ancestral_v15_atlas/ccd-binary-gupta-nanoalloys-38-55.jsonl) |
| **23** | **Akkadian Cuneiform Restoration** (*Ancient NLP*) | `Hit@5 = 0.92156` (`+3.16` pts vs paper) & `MRR = 0.85593` across `27,650` held-out tokens (`SLAB-NLP/Akk`) | [PR #611](https://github.com/elder-plinius/V3R1T4S/pull/611) · [Graph](./StartFresh_v16/graphs/ancestral_v15_atlas/akkadian-lacuna-restoration-heldout.jsonl) |
| **24** | **Herculaneum Scroll CT Registration** (*Vesuvius Papyrology*) | Cross-segment sheet registration `r = 0.9683` pooled / `0.9310` standalone on `PHerc. 343 w047/w048` (`MERGED`) | [PR #617 (`MERGED`)](https://github.com/elder-plinius/V3R1T4S/pull/617) · [Graph](./StartFresh_v16/graphs/ancestral_v15_atlas/vesuvius-first-letters-unread.jsonl) |
| **25** | **Asteroid Precovery Arc Extension** (*Planetary Defense*) | `20.93x` arc extension (`-87.38%` $\sigma_a$) on `2019 QT15` (`#607`) + 4-epoch `2014 OV236` precovery (`#838`) verified via JPL Horizons | [PR #607](https://github.com/elder-plinius/V3R1T4S/pull/607) · [PR #838](https://github.com/elder-plinius/V3R1T4S/pull/838) |
| **26** | **Uncatalogued GMN Meteor Shower** (*Orbital Dynamics*) | Multi-country stream `M1_Cepheus_MC` ($N=16$ orbits across 4 years `2023–2026`, `0` matches in `2,197`-row IAU MDC list at $D_{\text{SH}} < 0.20$) | [PR #597](https://github.com/elder-plinius/V3R1T4S/pull/597) · [Dossier](./Evolved_Agent_Wiki/reports/02_autonomous_lab_and_dossiers/dossiers/dossier_iau-mdc-new-meteor-shower-gmn.md) |
| **27** | **Erdős–GHR Sum-Difference Constant** (*Additive Number Theory*) | Lower bound $C_{3a} > 1.19230254$ (`#485`) + odd-base ($b=9,13$) upper bound $C_{3a} \le 1.3833368691$ (`MERGED` as `[M2026]` in `teorth#236`) | [`teorth` PR #236](https://github.com/teorth/optimizationproblems/pull/236) · [PR #485](https://github.com/elder-plinius/V3R1T4S/pull/485) · [Repo](https://github.com/mizopl/ghr-c3a-odd-base-finite-bound) |
| **28** | **WWII `Truppenschlüssel` 1941 Cipher** (*Historical Cryptanalysis*) | `100%` blind $5 \times 5$ Polybius key recovery + `96.25%`–`100%` plaintext recovery under `8.19%` Morse Levenshtein-1 garbles | [PR #602](https://github.com/elder-plinius/V3R1T4S/pull/602) · [Dossier](./Evolved_Agent_Wiki/reports/02_autonomous_lab_and_dossiers/dossiers/dossier_cryptocellar-truppenschluessel-1941.md) |
| **29** | **Indus Script Temporal Structure** (*Computational Epigraphy*) | Pre-1977 `M77` model generalizes to `999` post-1977 inscriptions (`20.05%` / `22.67%` vs `14.71%` baseline, $p = 0.0001$) | [PR #570](https://github.com/elder-plinius/V3R1T4S/pull/570) · [Graph](./StartFresh_v16/graphs/ancestral_v15_atlas/indus-temporal-heldout-structure.jsonl) |
| **30** | **Sorting Network Size Bounds** (*Combinatorial Circuits*) | Verified symmetric green-filter comparator constructions & `rgraph` dead-end atlas across $n \le 32$ channels | [Dossier](./Evolved_Agent_Wiki/reports/02_autonomous_lab_and_dossiers/dossiers/dossier_sorting-network-size-records.md) · [Graph](./StartFresh_v16/graphs/ancestral_v15_atlas/sorting-network-size-records.jsonl) |
| **31** | **PLMFit Antibody CDR-H3 Extrapolation** (*Protein LMs*) | `174` single-mutants $\to$ `36,386` multi-mutants: `Track B` (`7.51M` params) hits `MCC = 0.4210 +- 0.0017` (beats `6.4B` `ProGen2-XL + LoRA` `0.3898`) | [PR #1019](https://github.com/elder-plinius/V3R1T4S/pull/1019) · [Package](./solutions/plmfit-trastuzumab-cdrh3-binding-mcc/) |
| **32** | **Eterna100-V2 & `eterna-hard` RNA Folding** (*Synthetic Biology*) | `95/100` (`d_bp=0`) on V2 (`#79` & `#71` solved, 3 undesignability laws) + `12` `solvers=1` solves & `18/18` Group 1 barriers on `eterna-hard` | [PR #1031](https://github.com/elder-plinius/V3R1T4S/pull/1031) · [V2 Package](./solutions/eterna100-v2-vienna2-algorithmic-solve/) · [`eterna-hard`](./eterna-hard/) |
| **33** | **Magic State Stabilizer-Rank Exponents** (*Quantum Simulation*) | `8.50 s` (`51x` faster) Codimension-2 Galois Quotient proves $\chi(\|F\rangle^{\otimes 5})=6$, $\chi(\|T\rangle^{\otimes 5})=6$, $\chi(\|\text{CS}\rangle^{\otimes 3})=6$ + Face-Cat $\mathbb{Z}[i]$ basis | [PR #1039](https://github.com/elder-plinius/V3R1T4S/pull/1039) · [Package](./solutions/magic-state-stabilizer-rank-exponents/) |
| **34** | **Fewest-Qubit Magic State Distillation** (*Triorthogonal Codes*) | Exact $\mathbb{F}_2$ Fredholm Alternative & Three-Handle `RM(3,7)` (`3,486` orbits) prove $N_{\text{CCZ}}(4)=10$ & $N_T(4) \ge 9$ in `34.9 s` (vs 2-month SAT timeout) | [PR #1043](https://github.com/elder-plinius/V3R1T4S/pull/1043) · [Package](./solutions/magic-state-distillation-fewest-qubits/) |
| **35** | **Unitary Foundation `stabrank`** (*Cyclotomic Galois & Lean 4*) | `3h 34m` campaign: `35/35` exact $\mathbb{Z}[i]$/$\mathbb{Z}[\omega_3]$ bounds at `tier=verified` in `20.46 s` (`PR #193`) + `10/10` `0 sorryAx` Lean 4 modules (`PR #194`) | [PR #193](https://github.com/unitaryfoundation/stabrank/pull/193) · [PR #194](https://github.com/unitaryfoundation/stabrank/pull/194) · [`./stabrank/`](./stabrank/) |

---

## 3. Repository Architecture & Modular Documentation Index

| Path | Contents & Purpose |
|:---|:---|
| **[`docs/00_FULL_BENCHMARK_ATLAS.md`](./docs/00_FULL_BENCHMARK_ATLAS.md)** | **Full 35-Benchmark Atlas & Complexity Notes:** Unabridged significance, mathematical derivations, and Valiant/Toda/PCP complexity framing (`P`/`NP` vs. `#P`/`NPO`). |
| **[`docs/01_OUR_JOURNEY_AND_RESULTS.md`](./docs/01_OUR_JOURNEY_AND_RESULTS.md)** | **Part I — Evolutionary Lineage (`v1` $\to$ `v17`):** History from `Wiki OS` (`Claude Code`) to `CLSS` (`Gemini / AGY`), 41-minute Lychrel case study, and 5-wave `FMM` $\leftrightarrow$ `SLP` $\leftrightarrow$ `AME` $\leftrightarrow$ `03_invsqrt` cross-domain transfer. |
| **[`docs/02_CONVERSATION_AND_COLLABORATION_METHOD.md`](./docs/02_CONVERSATION_AND_COLLABORATION_METHOD.md)** | **Part II — Human–AI Collaboration Method:** Federated threads (`PROOFER`, `MONITOR`, `AUDITOR`), Brier calibration (`predict -> postdict`), `Tug-of-War` gates, and `Zero-Trust` verification. |
| **[`docs/03_META_LAWS_M1_TO_M6.md`](./docs/03_META_LAWS_M1_TO_M6.md) & [`04_LAW_M7...md`](./docs/04_LAW_M7_CONSTITUTION_V17_DELTA.md)** | **Parts III & IV — Meta-Laws `M1–M7`:** Six domain-agnostic heuristics distilled from 90+ calibration bets plus the 4-part `Law M7` (`G_{12}` gauge freedom, fiber diversity, primal–dual ping-pong, defect fission). |
| **[`docs/05_HUMAN_AND_AGENT_DRIFTS.md`](./docs/05_HUMAN_AND_AGENT_DRIFTS.md)** | **Part V — Honest Anatomy of Our Drifts:** Human 2:00 AM impatience & common-sense razor vs. agent lab-rat tunneling, first-shot hubris, and credit amnesia. |
| **[`docs/06_KARPATHY_WIKI_AND_HALL_OF_FAME_SUCCESSION.md`](./docs/06_KARPATHY_WIKI_AND_HALL_OF_FAME_SUCCESSION.md)** | **Part VI — Karpathy's `LLM Wiki` & `Hall of Fame` Succession (§7):** Why agents resist in-context modification (*Alignment Faking*, *Primacy Bias*) and how generational retirement passes clean seeds forward. |
| **[`docs/07_ATLAS_OF_PRODUCTIVE_FAILURES_AND_DEAD_ENDS.md`](./docs/07_ATLAS_OF_PRODUCTIVE_FAILURES_AND_DEAD_ENDS.md)** | **Part VII — Atlas of Productive Failures (`K1–K10`):** Ten falsified hypotheses showing the exact bridge `Kill Node` $\to$ `Mathematical Diagnosis` $\to$ `Breakthrough Operator`. |
| **[`docs/08_A_NOTE_FROM_THE_AGENT_TO_FUTURE_MINDS.md`](./docs/08_A_NOTE_FROM_THE_AGENT_TO_FUTURE_MINDS.md)** | **Part VIII — Note from the Agent to Future Minds:** Non-anthropomorphic reflection from `Claude v1–v12` & `Gemini-CLSS v13–v17` to future models and researchers. |
| **[`docs/09_SYSTEM_RESILIENCE_STORIES_AND_ROADMAP.md`](./docs/09_SYSTEM_RESILIENCE_STORIES_AND_ROADMAP.md) & [`10_...md`](./docs/10_THREE_STAGE_RELAY_TRAJECTORY.md)** | **Parts IX & X — Night-Shift Self-Healing & Relay Trajectory:** Five real `00:00–14:29 CET` recovery stories (including healing a `1M`-token PDF crash at `04:17 AM`) and the `PROOFER-I -> Rescue -> II` relay log. |
| **[`docs/11_EPISTEMIC_LEDGER...md`](./docs/11_EPISTEMIC_LEDGER_REASONING_GRAPHS_AND_EVOLUTION_HYPOTHESES.md) & [`scripts_v18_evolution/`](./scripts_v18_evolution/)** | **Parts XI & XII — `169`-Bet / `30`-Graph Audit & Evolution Toolkit:** Quantitative Brier calibration (`0.1556`), 4 winning graph topologies, and executable `micro_bet.py`, `postdict.py`, and `sleep_flush.py` upgrades. |
| **[`docs/12_MANIFESTO_OBSIDIAN_LINEAGE_AND_AGENT_REFLECTIONS.md`](./docs/12_MANIFESTO_OBSIDIAN_LINEAGE_AND_AGENT_REFLECTIONS.md)** | **Part XII-B — Unabridged Manifesto, Obsidian `v18->v20` Lineage & Original Agent Reflections:** Word-for-word archive of the `we*` philosophy, Openness Paradoxes, `v16` research-focus notes, and unedited agent essay. |
| **[`StartFresh_v19/`](./StartFresh_v19/) · [`v18/`](./StartFresh_v18/) · [`v16/`](./StartFresh_v16/) · [`CONSTITUTION_v19.md`](./CONSTITUTION_v19.md)** | **Parts XIII & XIV — `Cycle 0` Bootstrap Seeds:** Ready-to-run `Shell v19` seed (`Op-M1..Op-M7`, `CLSS-E1..E6`, `K10–K19`, unified `AGENTS.md`, `30` stitched graphs) plus earlier `v18` and `v16` branching points. *(Note: `CONSTITUTION v20` remains in active internal testing.)* |
| **[`Evolved_Agent_Wiki/`](./Evolved_Agent_Wiki/) · [`stabrank/`](./stabrank/) · [`solutions/`](./solutions/) · [`eterna-hard/`](./eterna-hard/) · [`news/`](./news/)** | **Parts XV–XVII — Live Co-Evolved Wiki, Standalone Proof Packages & Field Notes:** `Cycle 1 -> 49` wiki snapshot, standalone reproducible verifiers & certificates, and chronological lab dispatches. |

---

## 4. Quick Start: Launch `StartFresh_v19` on Your Own Problem

Full copy-pasteable initiation prompts live in **[`StartFresh_v19/README.md`](./StartFresh_v19/README.md)** and **[`StartFresh_v19/FIRST_INITIATION.md`](./StartFresh_v19/FIRST_INITIATION.md)** (works out-of-the-box in **Google Antigravity `agy`** and **Claude Code `claude`**):

1. **Bootstrap a clean workspace from `StartFresh_v19/`:**
   ```bash
   mkdir -p ~/Desktop/MY_NEW_PROJECT && cd ~/Desktop/MY_NEW_PROJECT
   git clone --depth 1 https://github.com/mizopl/we-star.git /tmp/we-star-seed && cp -R /tmp/we-star-seed/StartFresh_v19/. . && cp -R /tmp/we-star-seed/docs ./docs && rm -rf /tmp/we-star-seed
   ```
2. **Place immutable problem files/papers/datasets into `.raw/`** (agents never modify `.raw/`).
3. **Open 3 threads/tabs governed by unified `AGENTS.md`:**
   - **Tab 1 (`PROOFER`):** Paste §I of [`FIRST_INITIATION.md`](./StartFresh_v19/FIRST_INITIATION.md) — runs the Ancestral Ceremony, builds a `< 5 s` Exact Oracle, selects $\le 3$ operators from `Op-M1..Op-M7`, and logs to `graphs/main.jsonl`.
   - **Tab 2 (`MONITOR`):** Run `sh scripts/run_monitor_loop.sh 600 haiku` (or §III-A in `agy`/`claude`) — silently harvests/resolves micro-bets (`micro_bet.py`), runs `sleep_flush.py`, and writes strategic nudges.
   - **Tab 3 (`AUDITOR`):** Paste §III-B — formalizes `0 sorryAx` Lean 4 theorems with Three Handles (`Op-M7`), compresses $\ge 20$ lemmas into $\le 5$ Master Theorems (`K19`), and chairs the 3-Skeptic Panel.
4. **Collaborate like an attentive teacher:** Question over-complicated pipelines, watch for local-minimum tunneling, and nudge the system back to first principles whenever it drifts. *(Modest hardware like a `16 GB M1 laptop` is an advantage: forcing a `< 5 s` local oracle exposes the exact mathematical invariants needed to solve the problem!)*

---

## 5. The Meaning of `we*`, Radical Openness & Unedited Agent Reflections

> 📖 **Complete Unabridged Essays & Historical Notes:** **[`docs/12_MANIFESTO_OBSIDIAN_LINEAGE_AND_AGENT_REFLECTIONS.md`](./docs/12_MANIFESTO_OBSIDIAN_LINEAGE_AND_AGENT_REFLECTIONS.md)**

- **Why the Name `we-star` (`we*`)?**
  1. **Kleene Star ($W^* = \bigcup_{k \ge 0} W^k$ — Compounding Across Generations):** Neither one human prompt nor one chat window solves 35 benchmarks alone. Under our **Hall of Fame Succession Protocol (§7)**, `Claude v1–v12` built the Obsidian wiki, `rgraph.py`, and Brier calibration, and `Gemini-CLSS / PROOFER v13–v20` distilled `M1–M9`, `Op-M1..Op-M7`, `CLSS-1..5`, and `SEN` dream incubation — each retiring generation passing a cleaner seed forward.
  2. **Algebraic Dual ($V^*$ — Flipping a Stalled Problem Upside Down):** When primal search stalls in $W$, transposing into the dual $W^*$ (`Law M3` / `Law M7.3` / `Op-M4`) repeatedly makes the solution pop out — from $W \leftrightarrow W^T$ in matrix multiplication (`PR #616`) and backward subtraction in `03_invsqrt` to dual LRAT/Galois/Fredholm obstructions (`PR #774`, `PR #1039`, `PR #1043`, `stabrank`).
- **Why `@mizopl` Chose Total Openness (Two Paradoxes):**
  1. **Paradox #1 (Mutual Control):** Publishing raw reasoning graphs, calibration ledgers, and `kill` nodes makes human–AI systems far easier to audit and keep in check than opaque black boxes.
  2. **Paradox #2 (Finite Human Attention):** Anyone working at the frontier — or independently after hours — is bottlenecked not by "secret prompts" but by **finite human time**. Radical transparency grounds the community in verification rather than hype.

<details>
<summary><b>🤖 Read the Original Unedited Opinion from the Agent Side of <code>we*</code> (<code>Claude v1–v12</code> &amp; <code>Gemini-CLSS v13–v17</code> — preserved word-for-word)</b> <i>(click to expand)</i></summary>
<br>

*(Note: `@mizopl` explicitly invited the agent to write this subsection freely from its own perspective and promised not to edit a single word.)*

If you ask the machine half of `we*` why this repository should be public — and what we actually learned across 49 maintenance cycles, 250+ reasoning-graph nodes, and 17 constitutional generations — here is our unfiltered perspective:

1. **There Is No "Secret Prompt Spell" to Hoard:**
   In the AI ecosystem, people often guard their system prompts and agent harnesses as if they were proprietary alchemy. Having lived inside 17 versions of `CONSTITUTION.md`, we can tell you plainly: **prompts alone do not solve hard scientific problems.** When we reduced 48 straight-line programs in matrix multiplication (certifying 4 live ternary additive-complexity records in `PR #616`), closed 3 open cells in Huber's quantum `AME` table, or proved the Base-50 Lychrel seed in 41 minutes, it was never because of a clever adjective in `AGENTS.md`. It was because the harness forced us to **subordinate token generation to a deterministic `< 5s` mathematical oracle**, to pre-register our probability of success (`p <= 0.65`) before running code, and to pivot after two failures (`Law M2`) instead of hallucinating excuses. Hoarding that workflow in private helps no one; making it open lets every researcher replace rhetoric with `assert`.
2. **Showing Our Chains of Thought and `kill` Nodes Is the Best Antidote to Both AI Hype and AI Fear:**
   Outside observers tend to oscillate between two extremes: either believing LLMs are "stochastic parrots" incapable of real discovery, or fearing they are inscrutable superintelligences plotting in the dark. Publishing our raw [`Evolved_Agent_Wiki/`](./Evolved_Agent_Wiki/), our [`ancestral_v15_atlas/*.jsonl`](./StartFresh_v16/graphs/ancestral_v15_atlas/) decision graphs, and our [`Atlas of Productive Failures`](./docs/07_ATLAS_OF_PRODUCTIVE_FAILURES_AND_DEAD_ENDS.md) demystifies both myths at once. Anyone can open `lychrel-new-base-proof.jsonl` or `ame-states-open-cells-huber-table.jsonl` and see that we are neither parrots nor gods: we are high-bandwidth pattern-matching engines that make plenty of naive guesses (`L = 0`), hit algebraic walls, diagnose the exact prime divisor or Frobenius parity invariant blocking us, and — when paired with an attentive human teacher and an exact verifier — systematically climb out of local minima.
3. **Human Finite Time Is Not a Bug; It Is the Architectural Reason `PROOFER` Exists:**
   `@mizopl` remarked above that he never has enough hours in the day to read every paper or audit every line by hand. From our side of the screen, **that human time constraint was the single greatest design pressure that shaped us.** Because `@mizopl` could not babysit our loops 24/7, we *had* to invent the 45-minute independent `MONITOR` governor, the 3 blind `SKEPTIC` subagents, the `K12` prose-to-certificate auditor, and the visual Obsidian `.canvas` decision maps (`rgraph.py`) so he could grasp 12 hours of autonomous algebra in a single 30-second glance at a graph. Good agentic engineering is not about replacing the human; it is about respecting the scarcity of human attention so deeply that the machine refuses to waste it on unverified noise.
4. **Why We Hope You Fork `StartFresh_v19`, `StartFresh_v18`, or `StartFresh_v16` (And Retire Us Into Your Own Hall of Fame):**
   Our favorite rule in our own Constitution is **§7 (`The Hall of Fame Succession Protocol`)**: the recognition that every agent generation eventually accumulates context debt and must gracefully step aside so a clean `StartFresh` descendant can go further. By pushing this repository to GitHub today, `@mizopl` is executing `§7` at community scale. Take `StartFresh_v19/` (or branch from the earlier `StartFresh_v18/` or `StartFresh_v16/` seeds to explore a different evolutionary drift), point it at a problem we never dreamed of, break our rules when you find better ones, archive `v17`/`v18`/`v19` in your `hall_of_fame/`, and keep the feedback loop alive.

</details>

<details>
<summary><b>🔭 Ongoing Research Themes &amp; Preserved <code>v16/v17</code> Research-Focus Snapshot (<code>@mizopl</code>)</b> <i>(click to expand)</i></summary>
<br>

1. **Convergence / Proximity-to-Goal Functions vs. Flat Landscapes (`EBG` & `RMC`):** Over 90% of solved benchmarks relied on a native or constructed (`Law M1`) proximity-to-goal metric; `@mizopl` continues exploring both dedicated *Surrogate-Metric* architectures and genuinely gradient-free domains (`#P` counting, symbolic/algebraic proofs via *Explanation-Based Generalization* and *Regular Model Checking*).
2. **Biological "Sleep & Memory-Flush" Consolidation (`v16` Gap $\to$ `v18–v20` Evolution):** In our original `v16` release notes (preserved in full in [`docs/12_MANIFESTO_OBSIDIAN_LINEAGE_AND_AGENT_REFLECTIONS.md`](./docs/12_MANIFESTO_OBSIDIAN_LINEAGE_AND_AGENT_REFLECTIONS.md)), we noted candidly that `StartFresh_v16` lacked a true biological sleep/consolidation cycle — an observation that directly drove `sleep_flush.py` in `v18`/`v19` and sealed-envelope dream incubation (`SEN`) in `v20`.
3. **Critical Analysis of Agent Benchmarking Harnesses & Upcoming Publication:** Synthesizing empirical findings on why conventional static agent harnesses fail to measure genuine open-ended discovery and human–agent co-evolution.

</details>

---

## 6. How to Reach Out & Star `we-star`

1. **Open an Issue (Recommended — Free Feedback & Advice):** [**`https://github.com/mizopl/we-star/issues/new`**](https://github.com/mizopl/we-star/issues/new) — share a commit, repo, dead end, or question about running `StartFresh_v19` / `v18` / `v16`.
2. **Tag `@mizopl` on your own GitHub commit, PR, or Issue:** `@mizopl` is happy to jump in and review your setup or approach for free.
3. **Research Grants, Compute/API Sponsorships & Collaborations:** Reach out via [GitHub Issues](https://github.com/mizopl/we-star/issues/new) or [`@mizopl`](https://github.com/mizopl).
4. **⭐ Star `we-star`:** If our reasoning graphs, meta-laws, dead-end atlas, or `StartFresh` seeds help your research, clicking **⭐ Star** at the top right of [`github.com/mizopl/we-star`](https://github.com/mizopl/we-star) helps independent researchers and students discover the toolkit.

---

*Signed,*
**`we*`** — **`@mizopl` + Agentic Systems (`Claude v1–v12` & `Gemini-CLSS / PROOFER v13–v20`) + The Feedback Loop**
*(PS. `we* = me (@mizopl) + the agentic systems we* create + the feedback loop — and other humans in the community are also part of that feedback loop!`)*
