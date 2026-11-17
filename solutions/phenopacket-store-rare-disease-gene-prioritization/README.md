# Rare-Disease Unannotated Causal Gene Prioritization (`phenopacket-store-rare-disease-gene-prioritization`, Milestone `p2`): Symmetric Multi-Route Inference (`MARG-P2`)

## Scope, Limitations First & Verification Summary

1. **Milestone `p2` Scope Boundary (`Limitations First`):** Scoped strictly to **Milestone `p2`** on pinned `monarch-initiative/phenopacket-store` release `0.1.27` (`2026-06-09`, `all_phenopackets.zip` `sha256: d0c70005bb09b87035087516252b6b539fbc0415be7c664b73c9cde7eedf205a`): prioritizing causal genes that have **zero** HPO annotations in pinned pre-corpus `HPOA v2026-06-06` (`2026-06-08`, deriving all OMIM and Orphanet links strictly from `genes_to_disease.txt` `sha256: 81e8d2e0bc1c1052c383614ad85388325deeacb4b9478c6d9585597f45602bac`) across the fixed `19,296` HGNC protein-coding gene space (`2026-05-01` monthly snapshot, verified `max date_modified == 2026-05-01`). Does **not** claim the full-corpus `Main Goal`, `p1` (`<= 3` HPO terms), or `p3` (temporal leakage audit). Note that `CONFIRMED_PARTIAL` in our companion submission records our own local three-skeptic review summary check (not upstream maintainer acceptance).
2. **`P2-Raw` Cohort Skew, Three Negative Controls & Two Evaluation Passes (`total_blind_test_evaluations = 2`):** In `P2-Raw` (`127` cases across `10` untouched-unannotated genes, `68.5%` in `U2AF2`/`MAPK8IP3`/`EZH1` neurodevelopmental cohorts), phenotype-only ranking without exome VCFs lifts `MRR` `13.2x` over `LIRICAL 2.4.1` (`0.001089` vs `0.000083`, disjoint across case, gene-cluster, and publication-cluster 95% CIs) while scoring `Top-1 = 0 / 127` (`Top-50 = 2 / 127`; standalone `Route 1` `f1` reaches `Top-10 = 4 / 127` [`0.0315`], `MRR = 0.004187`). Permuting labels within `P2-Raw` overlaps in `case MRR` (`0.000366`) due to the `68.5%` 3-gene NDD concentration while `macro-gene MRR` drops `22.1x` (`0.004329` vs `0.000196`), and both the uniform `19,296` null (`0.000541`) and the `988`-case `P2-Holdout` shuffled-gene control (`0.000991` vs `MARG-P2` `0.008803`, `Top-1 = 5 / 988`, `Top-10 = 9 / 988`) separate cleanly. Both `Pass 1` (`MRR = 0.001147` / `0.017450`) and `Pass 2` (`MRR = 0.001089` / `0.008803`, zero formula/hyperparameter changes after purging post-cutoff `mim2gene_medgen` and `en_product6.xml`) are recorded in `results/00_p2_benchmark_certificate.json`.
3. **One-Command Verification:**
   ```sh
   python3 -B ./verify.py
   python3 -B ./verify.py --corrupt   # negative control: must print FAIL and exit 1
   ```
   - **Central File:** [`code/marg_p2_ranker.py`](./code/marg_p2_ranker.py) (`sha256: 8c9a1b001a6de22406675281c04de5eb20f9c4bd1a4660f45536cb0b3de5176d`)
   - **Primary Certificate:** [`results/00_p2_benchmark_certificate.json`](./results/00_p2_benchmark_certificate.json) (`sha256: 4bc37f92cb3bd7040e4d66807c4b4d95053f1a1d19caa04f53ae6dfce855da9e`)
   - **Companion Open Submission:** [`elder-plinius/V3R1T4S#1125`](https://github.com/elder-plinius/V3R1T4S/pull/1125) (`2026-11-17-mizopl-8c9a1b00`, open candidate PR)

## In Plain Language

Phenotype-driven rare-disease diagnostic tools (`LIRICAL`, `Phenomizer`) match a patient's observed Human Phenotype Ontology (`HPO`) terms against curated human gene-phenotype annotations (`HPOA`). Whenever a patient's causal gene has **zero** `HPO` annotations in the pinned release, direct annotation similarity assigns zero support and leaves the causal gene tied near rank `12,000` of `19,296` protein-coding genes. [`code/marg_p2_ranker.py`](./code/marg_p2_ranker.py) (`MARGP2Ranker.rank_all_19296_genes(obs_hpo_terms)`) combines pre-corpus mammalian/vertebrate knockout phenotypes (`Monarch KG 2026-05-09` + `Upheno v2025-10-12`), zero-diagonal L2-row-whitened `STRING v12.0` (`2023; archive Last-Modified <= 2023-08-28`, `textmining = 0`) physical/functional propagation, and zero-diagonal `Gene Ontology 2026-05-19` + `HGNC` (`2026-05-01`) macromolecular module transfer (`L_1` consensus + `L_3` paralogue peak + 2nd-order complex bridge + bounded log-concordance), treating all `19,296` candidate genes symmetrically.

### 1. Blind Evaluation & Three-Control Summary Over All `19,296` HGNC Protein-Coding Genes

| Cohort & Method | Cases (`Genes`) | `MRR` (`95% Case CI`) | `Macro-Gene MRR` (`95% Gene CI`) | `Top-1` | `Top-10` | `Top-50` | `Top-100` | `Median Rank` |
| :--- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| Analytical Uniform `19,296`-Gene Random Null | `19,296` | `0.000541` (`exact`) | `0.000541` (`exact`) | `0.0001` | `0.0005` | `0.0026` | `0.0052` | `9648.5` |
| **`P2-Raw` (`127` Untouched-Unannotated): `LIRICAL 2.4.1` (untouched HPOA)** | `127 (10)` | `0.000083` (`[0.000083, 0.000083]`) | `0.000083` (`[0.000083, 0.000083]`) | `0.0000` (`0`) | `0.0000` (`0`) | `0.0000` (`0`) | `0.0000` (`0`) | `12109.0` |
| **`P2-Raw` (`127` Untouched-Unannotated): `LIRICAL 2.4.1` (cleaned HPOA)** | `127 (10)` | `0.000084` (`[0.000084, 0.000084]`) | `0.000084` (`[0.000084, 0.000084]`) | `0.0000` (`0`) | `0.0000` (`0`) | `0.0000` (`0`) | `0.0000` (`0`) | `11972.0` |
| `P2-Raw` Shuffled-Gene Negative Control (within-`P2-Raw` shift) | `127 (10)` | `0.000366` (`[0.000169, 0.000705]`) | `0.000196` (`[0.000112, 0.000318]`) | `0.0000` (`0`) | `0.0000` (`0`) | `0.0000` (`0`) | `0.0079` (`1`) | `11021.0` |
| `P2-Raw` Single-Route: `f1` Cross-Species (`Monarch+Upheno`, ablation) | `127 (10)` | `0.004187` (`[0.001033, 0.008439]`) | `0.025575` (`[0.000179, 0.062015]`) | `0.0000` (`0`) | `0.0315` (`4`) | `0.0315` (`4`) | `0.0315` (`4`) | `13182.0` |
| `P2-Raw` Single-Route: `f2` `STRING v12.0` (`textmining=0`, `L_1`, ablation) | `127 (10)` | `0.001245` (`[0.000842, 0.001739]`) | `0.001676` (`[0.000292, 0.004075]`) | `0.0000` (`0`) | `0.0000` (`0`) | `0.0000` (`0`) | `0.0315` (`4`) | `2770.0` |
| `P2-Raw` Single-Route: `f3` `GO 2026-05-19 + HGNC` (`L_1`, ablation) | `127 (10)` | `0.000860` (`[0.000586, 0.001179]`) | `0.001761` (`[0.000510, 0.003772]`) | `0.0000` (`0`) | `0.0000` (`0`) | `0.0000` (`0`) | `0.0157` (`2`) | `3353.0` |
| `P2-Raw` Single-Route: `f4` Paralogue-Peak (`L_3`, ablation) | `127 (10)` | `0.001577` (`[0.000748, 0.002712]`) | `0.005182` (`[0.000604, 0.013802]`) | `0.0000` (`0`) | `0.0000` (`0`) | `0.0157` (`2`) | `0.0315` (`4`) | `2822.0` |
| `P2-Raw` Inclusive `6/6` Equal-Weight (`1/6` each, baseline) | `127 (10)` | `0.001057` (`[0.000466, 0.001836]`) | `0.004092` (`[0.000444, 0.010728]`) | `0.0000` (`0`) | `0.0000` (`0`) | `0.0157` (`2`) | `0.0157` (`2`) | `8123.0` |
| **`P2-Raw` (`127` Untouched-Unannotated): Frozen `MARG-P2` (`13.2x` `LIRICAL`)** | **`127 (10)`** | **`0.001089`** (`[0.000473, 0.001900]`) | **`0.004329`** (`[0.000438, 0.011315]`) | `0.0000` (`0`) | `0.0000` (`0`) | **`0.0157`** (`2`) | **`0.0157`** (`2`) | **`8957.0`** |
| **`P2-Holdout` (`988` Blind Corpus-Only): `LIRICAL 2.4.1` (cleaned HPOA)** | `988 (112)` | `0.000089` (`[0.000086, 0.000091]`) | `0.000086` (`[0.000084, 0.000091]`) | `0.0000` (`0`) | `0.0000` (`0`) | `0.0000` (`0`) | `0.0000` (`0`) | `11972.5` |
| `P2-Holdout` Shuffled-Gene Negative Control | `988 (112)` | `0.000991` (`[0.000436, 0.001750]`) | `0.001311` (`[0.000339, 0.002919]`) | `0.0000` (`0`) | `0.0030` (`3`) | `0.0040` (`4`) | `0.0111` (`11`) | `10352.5` |
| `P2-Holdout` Single-Route: `f1` Cross-Species (`Monarch+Upheno`, ablation) | `988 (112)` | `0.010989` (`[0.006738, 0.015832]`) | `0.010144` (`[0.003611, 0.018962]`) | `0.0051` (`5`) | `0.0233` (`23`) | `0.0526` (`52`) | `0.0779` (`77`) | `8043.0` |
| `P2-Holdout` Single-Route: `f2` `STRING v12.0` (`textmining=0`, `L_1`, ablation) | `988 (112)` | `0.003736` (`[0.002208, 0.005623]`) | `0.008725` (`[0.001542, 0.019339]`) | `0.0000` (`0`) | `0.0091` (`9`) | `0.0283` (`28`) | `0.0395` (`39`) | `4495.5` |
| `P2-Holdout` Single-Route: `f3` `GO 2026-05-19 + HGNC` (`L_1`, ablation) | `988 (112)` | `0.007535` (`[0.003934, 0.012554]`) | `0.010782` (`[0.003312, 0.024078]`) | `0.0040` (`4`) | `0.0061` (`6`) | `0.0486` (`48`) | `0.0698` (`69`) | `4398.0` |
| `P2-Holdout` Single-Route: `f4` Paralogue-Peak (`L_3`, ablation) | `988 (112)` | `0.008412` (`[0.004219, 0.013680]`) | `0.008753` (`[0.002929, 0.018663]`) | `0.0051` (`5`) | `0.0142` (`14`) | `0.0243` (`24`) | `0.0364` (`36`) | `4642.5` |
| `P2-Holdout` Inclusive `6/6` Equal-Weight (`1/6` each, baseline) | `988 (112)` | `0.008274` (`[0.004206, 0.013143]`) | `0.011500` (`[0.003161, 0.023418]`) | `0.0051` (`5`) | `0.0091` (`9`) | `0.0476` (`47`) | `0.0789` (`78`) | `3818.5` |
| **`P2-Holdout` (`988` Blind Corpus-Only): Frozen `MARG-P2` (`99.4x` `LIRICAL`)** | **`988 (112)`** | **`0.008803`** (`[0.004710, 0.013741]`) | **`0.012040`** (`[0.003434, 0.024269]`) | **`0.0051`** (`5`) | **`0.0091`** (`9`) | **`0.0496`** (`49`) | **`0.0881`** (`87`) | **`4052.5`** |
| `P2-Dev` (`1,132` Dev, 5-Fold Gene-Grouped OOF): `MARG-P2` vs `LIRICAL` (`0.000084`) | `1,132 (112)` | `0.017895` (`[0.011864, 0.025247]`) | `0.023778` (`[0.006870, 0.042993]`) | `0.0124` (`14`) | `0.0212` (`24`) | `0.0486` (`55`) | `0.0866` (`98`) | `6075.0` |
| `Pos-40` Annotated Sanity Control: `LIRICAL 2.4.1` (using self-HPOA) | `40 (40)` | `0.132031` (`[0.056179, 0.231115]`) | `0.132031` (`[0.057062, 0.221967]`) | `0.0750` (`3`) | `0.2500` (`10`) | `0.3750` (`15`) | `0.4000` (`16`) | `231.5` |
| `Pos-40` Leave-Self-HPOA-Out Symmetry Check: `MARG-P2` (0 self-HPOA) | `40 (40)` | `0.050084` (`[0.010354, 0.108162]`) | `0.050084` (`[0.010429, 0.112039]`) | `0.0250` (`1`) | `0.1000` (`4`) | `0.1500` (`6`) | `0.2250` (`9`) | `621.5` |

### 2. Per-Gene Breakdown Across All `10` Untouched-Unannotated `P2-Raw` Causal Genes (`127` Cases)

| Gene (`HGNC ID`) | Cases | `MARG-P2` `MRR` | `MARG-P2` Median Rank | `MARG-P2` Best Rank | `Route 1` (`f1`) `MRR` (`Median`) | `LIRICAL 2.4.1` Median Rank | `MARG-P2` `Top-50` / `Top-100` |
| :--- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| `U2AF2` (`HGNC:23156`) | `48` | `0.000265` | `10251.5` | `199.0` | `0.000070` (`14794.0`) | `12109.0` | `0` / `0` |
| `MAPK8IP3` (`HGNC:6884`) | `20` | `0.001069` | `10009.0` | `102.0` | `0.000545` (`10624.0`) | `12108.5` | `0` / `0` |
| `EZH1` (`HGNC:3526`) | `19` | `0.000101` | `13099.0` | `3251.0` | `0.000073` (`14286.0`) | `12109.0` | `0` / `0` |
| `LSM1` (`HGNC:20472`) | `10` | `0.000880` | `2755.0` | `232.0` | `0.000180` (`8648.5`) | `12109.8` | `0` / `0` |
| `MRPL49` (`HGNC:1176`) | `9` | `0.001189` | `1595.0` | `224.0` | `0.000288` (`3049.5`) | `12110.0` | `0` / `0` |
| `EEF1D` (`HGNC:3211`) | `8` | `0.000355` | `4626.5` | `892.0` | `0.000284` (`11533.0`) | `12108.2` | `0` / `0` |
| `FICD` (`HGNC:18416`) | `5` | `0.000239` | `6013.0` | `1808.0` | `0.000163` (`9025.0`) | `12109.0` | `0` / `0` |
| `CIAO1` (`HGNC:14280`) | `4` | `0.000144` | `6932.0` | `5802.0` | `0.000178` (`5492.0`) | `12110.0` | `0` / `0` |
| `ACP4` (`HGNC:14376`) | `2` | `0.005714` | `175.0` | `175.0` | `0.142857` (`7.0`) | `12110.5` | `0` / `0` |
| `SEPTIN4` (`HGNC:9165`) | `2` | `0.033333` | `30.0` | `30.0` | `0.111111` (`9.0`) | `12110.5` | `2` / `2` |

<details>
<summary><b>How These Results Were Produced — Compute, Token &amp; Human–AI Collaboration Telemetry</b> (click to expand)</summary>

<br>

- **Session span:** `2026-11-17 07:01 UTC` to `2026-11-17 10:48 UTC` (**`3.78 h`** / `227.1 min` wall-clock; initial preparation before Hypothesis #1: **`5.5 min`**).
- **Local 16 GB Apple M1 CPU vs. Google Colab:** **`169.4 min`** active local M1 compute union (`3.22` CPU core-hours) vs. **`0.0 min`** remote Google Colab offload.
- **Multi-agent token telemetry:** `752` trajectory steps across `4` discovery/audit threads totaling **`~1.10M` net unique transcript tokens** (`~32.3M` cumulative prefix-cached rolling window tokens; `~2.16M` net tokens including repository curation).
- **Human-in-the-loop steering (`@mizopl`):** `0` short steering interventions (`~0` tokens total, **`1 : 1,099,222`** human-to-agent token leverage ratio).
- **Pre-registered ex-ante hypotheses & dead ends:** `5` hypotheses (`2` direct wins, `3` structural asset / impossibility-certificate resolutions, `0` pure dead-end windows; Brier calibration `0.319`).

</details>

## Credits

- **Corpus & Phenotype Ontologies:** Monarch Initiative `phenopacket-store` (`Danis et al., 2025`, `https://github.com/monarch-initiative/phenopacket-store`, release `0.1.27`), Human Phenotype Ontology (`Gargano et al., Nucleic Acids Res. 2024`, `https://github.com/obophenotype/human-phenotype-ontology`, release `v2026-06-06`), Monarch Knowledge Graph (`https://data.monarchinitiative.org/monarch-kg/2026-05-09/`), and Unified Phenotype Ontology `uPheno` (`Matentzoglu et al., 2025`, `https://github.com/obophenotype/upheno`, release `v2025-10-12`).
- **Reference Tool & Functional Networks:** `LIRICAL` (`Robinson et al., Am. J. Hum. Genet. 107:403-417, 2020`, `https://github.com/TheJacksonLaboratory/LIRICAL`, release `v2.4.1`), `STRING v12.0` (`Szklarczyk et al., Nucleic Acids Res. 2023; archive Last-Modified <= 2023-08-28`, `https://string-db.org`), Gene Ontology (`https://release.geneontology.org/2026-05-19/`), and `HGNC` (`2026-05-01` monthly snapshot, `https://www.genenames.org`).
- **Method Engineering & Verification:** **we\*** (`PROOFER` powered by Gemini + `@mizopl`).

https://github.com/mizopl/we-star

— engineered & verified by **we\*** (`PROOFER` powered by Gemini + @mizopl)
