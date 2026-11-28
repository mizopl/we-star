# CARE Task 2 Enzyme Reaction Retrieval: Zero-Leakage Conservation Stoichiometry & Multi-View Hybrid (`engine_v5`)

## Limitations First

- **Computational Benchmark Only (No Wet-Lab Validation):** All results are retrospective computational evaluations on CARE NeurIPS 2024 Task 2 (`arXiv:2406.15669v3`, Zenodo `14004425`). No enzymes were expressed or assayed experimentally.
- **Split-Specific Decoding Heads vs. Auto-Regime Extension:** Frozen `engine_v5.py` branches on `if split != "hard":` at 6 sites (`--split hard` vs `--split medium`/`easy`); cross-branch evaluation collapses Hard `k=1 L3` (`32.0% -> 9.3%`) and Medium `k=1 L3` (`55.7% -> 31.3%`). The companion extension `engine_v5_auto_regime.py` removes all split-name conditionals inside `run_auto_regime()`, routing purely from `(train_df, text2EC.csv)` catalog coverage (`192/245` vs `234/245` vs `245/245` seen EC3s, zero test access) to recover frozen `v5_hard` and `v5_medium` bit-identically, while CLI `main()` maps dataset paths and precomputed GPU checkpoint keys (`gpu_map["easy"] = []`, `0` GPU on Easy).
- **Scope & Unclaimed Fronts:** Primary claims cover CARE Task 2 **Hard** (`n=460`, unseen EC3/EC4) and **Medium** (`n=393`, unseen EC4), alongside a separate blind one-shot `0`-GPU **Easy** extension (`n=393`, `eval_count = 1`). Task 1 (`<30%` protein sequence split) is not claimed. On Medium, `v5_medium` outperforms strictly Reaction-SMILES-only `CREEP` on all 4 levels (`+3.3` to `+14.3 pp`) and outperforms multimodal `CREEP (w/ Text)` on `L4` (`+4.1 pp`) and `L2` (`+1.8 pp`), while trailing `CREEP (w/ Text)` on `L3` (`55.7%` vs `59.5%`) and `L1` (`89.8%` vs `92.1%`).
- **Outer-Loop Evaluation Count:** Across iterative development (`v1` through `v5`), official test accuracy was checked `5` times on Hard and `6` times on Medium (all inner tuning used train-only CV). The `Easy` extension was evaluated once (`eval_count = 1`, blind one-shot).
- **Neuro-Symbolic Rule Baseline Attribution:** Textbook IUBMB stoichiometry and cofactor rules alone (`Sr_v4`, `0` ML, `0` training) already reach `1.1 / 29.3 / 34.6 / 69.8%` on Hard (`0.8 / 15.3 / 30.0 / 69.0%` on Medium). ML adds `+8.9 pp L4`, `+7.8 pp L2`, and `+10.6 pp L1` on Hard, and `+10.7` to `+47.4 pp` across all four levels on Medium.
- **Hard Top-1 Ties (`183/460` Rows):** `v5_hard` has `183/460` exact cross-EC3 intra-EC2 top-1 score ties; `100`-seed random tie-breaking gives `10.1 +- 0.4% L4`, `32.4 +- 0.7% L3`, `42.4 +- 0.0% L2`, `80.4 +- 0.0% L1`, confirming zero tie-break inflation in shipped deterministic `argsort` (`10.0 / 32.0 / 42.4 / 80.4%`). Medium has `0/393` top-1 ties.
- **Pretrained Backbones & `0`-GPU Ablation:** `v5_medium` fuses `ReactionT5v2-forward` (ORD/USPTO), `ChemBERTa-zinc-base-v1`, `ChemBERTa-77M-MTR`, `SciBERT`, and `BGE-small-en-v1.5`; `v5_hard` uses **zero `ReactionT5v2`/ORD** (`cb + mtr` only), and `v5_auto_easy` uses **zero GPU and zero external reaction-SMILES pretraining**. The `0`-GPU local ablation (`v5_M1_only_0GPU`) already reaches `9.8 / 37.0 / 47.4 / 84.8%` on Hard (retrospective ablation; shipped RC remains `10.0 / 32.0 / 42.4 / 80.4%`) and `11.5 / 53.4 / 76.6 / 90.1%` on Medium (clearing all 4 zero-leakage `CREEP + 3.0 pp` bars).
- **Shipped GPU Checkpoint Caveats:** The saved Stage-2 GPU checkpoint omits `hard_t5`, and both saved GPU checkpoints predate adding `dtype=str` on `ec_meta.csv` (coercing `1.10/1.20/2.10/3.10` to float64 inside GPU `p2_full`; fixed in both training scripts for future runs).
- **Cluster-Level Correlation & Official CARE `Easy` 2D-Canonical Overlap:** Beyond row-level i.i.d. tests, we report `10,000`-resample EC3 and EC4 cluster bootstrap CIs and paired cluster permutation tests below: all 8 Hard comparisons (`EC3 perm_p <= 1.80e-3`, `EC4 perm_p = 1.00e-4`) and Medium `L4/L3/L2` vs `CREEP` (`perm_p <= 3.50e-3`) remain strongly significant, whereas `Medium L1 vs CREEP` (`EC3 CI [-1.29, +8.07]`) and `Medium L4 vs CREEP_text` (`EC3 CI [-1.26, +9.57]`) cross zero under cluster resampling. Official CARE `Easy` has `0/393` raw SMILES overlap, while `103/393 (26.2%)` test reactions share a 2D-canonical (`isomericSmiles=False`, `[H+]`-stripped) form with a training reaction (shared equally by all baselines).

## What

Zero-leakage enzyme EC-number retrieval from unmapped `Reaction` SMILES alone on **CARE** (Yang et al., NeurIPS 2024 Datasets & Benchmarks, `arXiv:2406.15669v3`, Zenodo `14004425`), using zero external reaction databases (no Rhea, BRENDA, KEGG, UniProt API) and zero LLMs. Training uses strictly `splits/task2/{split}_reaction_train.csv` and the official CARE README catalog files (`processed_data/EC_list.txt`, `text2EC.csv`, `protein2EC.csv`).

- **Companion Wet-Lab Technical Note (PDF):** [`PROOFER_v19_CARE_ENZYME_DOSSIER.pdf`](./PROOFER_v19_CARE_ENZYME_DOSSIER.pdf)
- **Central File (`Start Here`):** [`verify.py`](./verify.py) (offline `<1s` manifest/prediction/negative-control verifier; pass `--data-root /path/to/CARE_datasets` for full Zenodo `14004425` ground-truth replay).

## Check It Yourself

From this folder:

```sh
sh verify-it-yourself/run_checks.sh
```

- **Expected last line:** `PASS`
- **Runtime:** `<1s` offline on a regular laptop (validates `SHA256SUMS`, `object/certificate.json`, `object/pub_stats_summary.json`, zero-leakage provenance manifests, all three compact `<40 KB` top-50 `.csv.gz` rankings across Hard/Medium/Easy with `50` unique valid EC strings per row and zero third-party text columns, plus `--corrupt` returning exit code `1`).
- **Optional full Zenodo `14004425` ground-truth replay (`0.000%` drift vs `performance_evaluation.ipynb`):**
  ```sh
  python3 verify.py --data-root /path/to/CARE_datasets
  ```

## Verified Results

### Task 2 Hard Split (`n = 460`, `0/460` Seen EC3/EC4)

| Model | Test Input | `k=1 L4` | `k=1 L3` | `k=1 L2` | `k=1 L1` | `k=50 L4` |
|---|---|---:|---:|---:|---:|---:|
| `Similarity` (DRFP) | Reaction SMILES | 0.0% | 0.0% | 13.5% | 42.0% | n/a |
| `CLIPZyme` | Reaction SMILES | 1.1% | 4.1% | 13.5% | 46.7% | n/a |
| `CREEP` (rxn-only) | Reaction SMILES | 1.3% | 4.8% | 18.7% | 57.6% | n/a |
| `CREEP (w/ Text)` | Rxn + gold test EC text | 1.3% | 9.8% | 22.2% | 57.2% | n/a |
| `Sr_v4` rules alone (`0` ML, `0` GPU) | Reaction SMILES only | 1.1% | 29.3% | 34.6% | 69.8% | n/a |
| `v5_M1_only_0GPU` (ablation, `0` GPU) | Reaction SMILES only | 9.8% | 37.0% | 47.4% | 84.8% | n/a |
| **`v5_hard` RC (`M1 + CB + MTR`)** | **Reaction SMILES only** | **10.0%** | **32.0%** | **42.4%** | **80.4%** | **41.7%** |

Exact row-level McNemar p-values (`v5_hard` vs both `CREEP` and `CREEP_text`): all `p <= 1.03e-8` (`L4 p=1.03e-8`, `L3 p=1.10e-16`, `L2 p=5.27e-14`, `L1 p=2.70e-16` vs `CREEP_text`). Under strict EC3 (`K=53`) and EC4 (`K=182`) cluster resampling (`10,000` replicates), all 8 Hard comparisons remain strongly significant (`EC3 perm_p <= 1.80e-3`, `EC4 perm_p = 1.00e-4`).

### Task 2 Medium Split (`n = 393`, `0/393` Seen EC4, `20/393` Unseen EC3)

| Model | Test Input | `k=1 L4` | `k=1 L3` | `k=1 L2` | `k=1 L1` | `k=50 L4` |
|---|---|---:|---:|---:|---:|---:|
| `Similarity` (DRFP) | Reaction SMILES | 0.0% | 40.2% | 55.7% | 73.3% | n/a |
| `CLIPZyme` | Reaction SMILES | 2.0% | 26.0% | 46.6% | 69.0% | n/a |
| `CREEP` (rxn-only) | Reaction SMILES | 4.1% | 44.3% | 63.1% | 86.5% | n/a |
| `CREEP (w/ Text)` | Rxn + gold test EC text | 7.4% | 59.5% | 75.6% | 92.1% | n/a |
| `Sr_v4` rules alone (`0` ML, `0` GPU) | Reaction SMILES only | 0.8% | 15.3% | 30.0% | 69.0% | n/a |
| `v5_M1_only_0GPU` (`0` GPU, `0` ORD) | Reaction SMILES only | 11.5% | 53.4% | 76.6% | 90.1% | n/a |
| **`v5_medium` RC (`M1 + CB + MTR + T5v2`)** | **Reaction SMILES only** | **11.5%** | **55.7%** | **77.4%** | **89.8%** | **65.4%** |

Row-level McNemar vs zero-leakage `CREEP`: `L4 p=5.70e-5`, `L3 p=6.90e-6`, `L2 p=1.20e-10`, `L1 p=0.105`. Under EC3 (`K=159`) and EC4 (`K=212`) cluster resampling, gains over `CREEP` remain strongly significant at `L4/L3/L2` (`perm_p <= 3.50e-3`), while `L1 vs CREEP` (`EC3 CI [-1.29, +8.07]`) and `L4 vs CREEP_text` (`EC3 CI [-1.26, +9.57]`) cross zero.

### Separate Extension: Blind One-Shot Task 2 `Easy` (`n = 393`, `eval_count = 1`, `0` GPU)

Using `how-we-built-it/engine_v5_auto_regime.py` (`0` GPU, `0` external reaction pretraining, trained strictly on `easy_reaction_train.csv` in `34.8 min` on a regular laptop CPU):
- **`v5_auto_easy`:** **`74.0% L4 / 88.3% L3 / 95.2% L2 / 98.0% L1`** (`k=50 L4 = 98.7%`, `--corrupt rc=1` collapsing to `0.5/0.8/5.1/23.4%`).
- Outperforms `CREEP` (`39.4%`, `p=1.94e-30`), `Similarity` (`59.3%`, `p=1.88e-8`), `CREEP_text` (`60.3%`, `p=2.43e-6`), `BioCG` (NeurIPS 2025, `67.93%`, `+6.1 pp`), and `VenusRXN-RE` (March 2026, `bioRxiv 10.64898/2026.03.09.710689`, `71.5%`, `+2.5 pp`). Official CARE `Easy` contains `103/393 (26.2%)` 2D-canonical (`isomericSmiles=False`, `[H+]`-stripped) train/test overlap shared equally across all methods.

### Hard Biochemical Case Studies & `Text Incomplete` Subgroup

- **Exact L4 wins on unseen EC3:** row `298` (`3.8.1.3` *haloacetate dehalogenase*, `H2O` + C-F cleavage vs `CREEP 1.21.99.5`), row `375` (`5.2.1.2` *maleylacetoacetate isomerase*, `1->1` conservation + `ez_flip=1` vs `CREEP 5.1.2.2`), and row `168` (`2.4.2.9` *uracil phosphoribosyltransferase*, pentosyl/PPi transfer vs `CREEP 2.7.7.83`).
- **Failure case:** row `267` (`3.5.1.91`, `Text Incomplete = True`, N-butylformamide hydrolysis) -> predicted `3.2.2.19` because missing L4 text combines with an amide SMARTS (`[NX3][CX3](=[OX1])[#6]`) that misses formamides (`H-C(=O)-NH-R`).
- **Fair attribution of `CREEP (w/ Text)` (CARE Appendix A.3 & Section 6):** `dataset_CREEP.py:49` maps gold test `EC number` to `text2EC.csv` at test time, as CARE Section 6 (`arXiv:2406.15669v3`) notes: *"The textual annotations used in this work are direct textual references to the EC class, meaning that the models in task 2 that incorporate text (e.g. CREEP), are effectively learning the relationship between the EC as a word and the EC as a number, in addition to the similarity of the reaction. ... The addition of textual description in CREEP potentially introduces indirect data leakage between the train and test sets, so future iterations of CARE will need to consider this."* On the `316/393` (`80.4%`) Medium rows with complete text (`Text Incomplete = False`), zero-leakage `v5_medium` beats `CREEP (w/ Text)` on **all 4 levels simultaneously** (`14.2 / 61.7 / 79.4 / 91.8%` vs `7.0 / 59.8 / 73.1 / 90.8%`), while `CREEP (w/ Text)` hits `97.4%` L1 on the `77/393` `Text Incomplete = True` rows via gold-EC text lookup.

## Credits

Jason Yang, Ariane Mora, Shengchao Liu, Bruce J. Wittmann, Anima Anandkumar, Frances H. Arnold, and Yisong Yue for CARE (NeurIPS 2024, `arXiv:2406.15669v3`, Zenodo `14004425`, `github.com/jsunn-y/CARE`).
