# Dossier: `sorting-network-size-records`

- **Category:** `record-tables`
- **Primary Status Source:** `https://bertdobbelaere.github.io/sorting_networks_extended.html` (fetched `2026-10-19T01:45:22Z`, HTTP `200`, `297,884` bytes, `sha256: 5515e5d7862caaf31058225ff215850c1987704f6bcd9b5920590e2478d41a53`, page revision `Tue Oct 13 20:10:24 2026`).
- **Companion Sources:** `https://bertdobbelaere.github.io/sorting_networks_avgswaps.html` (`sha256: c97e747ded90e0fbf3ce63003663a31d6e7f5d43611ca1e2f172bf952607ac92`, updated `2026-10-18`), `https://github.com/bertdobbelaere/SorterHunter`, Chengu Wang (`arXiv:2511.04107`).

## Best Verified So Far (Run `2026-10-19-0142`)
- **Full Table Verification (`54/54` `extended` and `31/31` `avgswaps` for $n=2..32$, `65/68` `extended` and `30/32` `avgswaps` for $n=33..64$):**
  - Every published network for $n=2..32$ in both tables passes exact $0\text{-}1$ sorting verification (`check_sn_bits` 64-bit word bit-slicing over all $2^n$ binary inputs and `check_sorting_network.py` exact Layer-1 $3^k \cdot 2^{n-2k}$ reachable-output-set propagation) with 0 header `(size, depth)` mismatches and 0 redundant comparators (`6,708/6,708` single-comparator removals tested for $n=13..32$, `redundant=0`).
  - Reverse-engineered the exact mechanism of Justin Lyson's `2026-10-13` improvement `N44L311D17 -> N43L304D17`: injecting $+\infty$ on interior wire $w=16$ (`reduce_by_infinity(44, w=16, +inf)`) yields a valid $(306, 17)$ sorter on $n=43$ in which two comparators (`#126 (15,42)` and `#146 (38,42)`) become provably idempotent/redundant (`ci & ~cj == 0` in 1 forward pass), pruning to `(304, 17)`.
- **Quantitative Near-Misses on $17 \le n \le 32$ (`attempts/optimizer/code/opt_out.txt`):**
  - **Depth compression ($d \to d-1$):**
    - `ext_N24L120D13` $\to (121, 12)$ (vs live $(122, 12)$): **`3` unsorted states** out of $2^{24}$ (`|R_4| = 5,315`).
    - `ext/avg_N25L130D15` $\to (130, 14)$ (vs live $(130, 15)$): **`4` unsorted states** out of $2^{25}$ (`|R_4| = 5,014`).
    - `avg_N21L99D15` $\to (99, 14)$ (vs live $(99, 15)$): **`5` unsorted states** out of $2^{21}$ (`|R_3| = 4,778`).
    - `ext_N23L114D14` $\to (114, 13)$ (vs live $(115, 13)$): **`5` unsorted states** out of $2^{23}$ (`|R_4| = 3,168`).
  - **Size reduction ($s \to s-1$ at fixed depth $d \le d_{\text{orig}}$):**
    - **6 networks sit at `unsorted_count = 1` (`score = 1025`, 1 failing binary vector with 1 adjacent inversion):** `ext_N17L74D10 -> (73,10)`, `ext_N29L166D14 -> (165,14)`, `ext/avg_N29L164D15 -> (163,15)`, `ext_N31L180D14 -> (179,14)`, and `ext_N32L185D14 -> (184,14)`.
    - **9 networks reach `unsorted_count = 2` (`score = 2050`):** `ext_N17L72D11` (`4 -> 2` at $(71,11)$), `ext_N19L87D11` (`(86,11)`), `ext_N20L93D11` (`(92,11)`), `ext_N23L116D12` (`(115,12)`), `ext_N26L141D13` (`3 -> 2` at $(140,13)$), `ext_N27L152D13` (`(151,13)`), `ext_N28L155D14` (`4 -> 2` at $(154,14)`), `avg_N31L180D14` (`3 -> 2` at $(179,14)`), and `avg_N32L185D14` (`(184,14)`).

## Covered Search Spaces (Exhaustive & Uncapped)
- Single-comparator redundancy (`1-minimality`) across all 41 networks for $n=13..32$ in `sorting_networks_extended.html` (4,462 removals) and all 20 networks for $n=13..32$ in `sorting_networks_avgswaps.html` (2,246 removals): 100% covered (`0` redundant comparators).
- Extreme channel deletions ($1 \le t+b \le 3$ for $n=14..35 \to 13..32$, 547 cases; $1 \le t+b \le 4$ in `channel_del_scan.c`), interior wire $\pm\infty$ trajectory deletions ($0 < c < n-1$ for $n=14..33$, 2,514 cases), and adjacent-layer comparator contractions (1,257 cases), each followed by exact iterative 1-minimal pruning: 100% covered (`0` strictly undominated pairs; 36 exact Pareto-frontier ties reproduced).
- Exact suffix branch-and-bound re-synthesis (`suffix_synth.c`) for fixed prefixes $L_1 \dots L_k$ at $k \in \{d-2, d-1\}$ across all 61 published networks for $n=17..32$: 100% covered (`NO_SOL`).

## Dead Angles (`rgraph.py` `sorting-network-size-records`)
- **`D0142_SC1`**: `sorting_networks_avgswaps.html` (updated `2026-10-18`) has 61 distinct comparator lists vs `sorting_networks_extended.html`, but `0/63` entries are undominated on `(size, depth)`.
- **`D0142_SC2`**: Every published network for $n=13..32$ in both `extended` and `avgswaps` is strictly 1-minimal (`0` redundant comparators out of 6,708 removals).
- **`D0142_SC3` / `D0142_CO2`**: Extreme channel deletions ($1..4$ wires) + iterative 1-minimal pruning remove up to 9 comparators per reduced network and reproduce 36 exact Pareto ties (e.g. `N32(185,14) -> N30(172,14)` and `N29(166,14)`), showing Dobbelaere already closed extreme-wire projections on $n \le 32$.
- **`D0142_SC4`**: Single interior wire $\pm\infty$ trajectory deletion + 1-minimal pruning on $n=14..33 \to 13..32$ yields 260 valid sorters and reproduces Pareto ties, but 0 strict improvements on $n \le 32$.
- **`D0142_SC5`**: Cross-network layer splices $A[:\ell_A] + B[\ell_B:]$ across `extended`, `avgswaps`, and wire-reversed duals for $n=13..32$ yield 958 valid sorters and 52 1-comparator seam prunings (Pareto ties), but simultaneous 2-comparator drops leave $\ge 1$ unsorted vector.
- **`D0142_CO1`**: Keeping the first $d-2$ or $d-3$ layers of any published $n=17..32$ network fixed and re-synthesizing only the suffix (`suffix_synth.c`) cannot reduce size or depth because published suffixes are already optimal for their prefixes.
- **`D0142_CO3`**: Interior 2–3 layer convex-neck window re-synthesis (`cross_layer_window.c`) and unequal-split prefix + Batcher/Van Voorhis merge seam pruning yield 0 improvements on $n=17..32$.
- **`D0142_OP1` / `D0142_OP2` / `D0142_OP3`**: Suffix-only MCMC/Tabu + 1-opt/2-opt defect-trajectory pruning (`opt_suffix.c`) reaches `unsorted=3` on `N24 (121,12)` and `unsorted=1` on 6 size-reduction targets, and proves that on `unsorted=1` suffixes every depth-feasible 1-opt or 2-opt edit that sorts $v_0$ induces $\ge 1$ collateral unsorted vector $v_1 \in R_k$.

## Live Leads
- **`L0142_JOINT`**: Joint prefix-suffix search — perturb layers $2..4$ of the prefix to shrink or reshape $|R_4|$ before running exact SAT (CaDiCaL) suffix completion, targeting the lowest-defect configurations found in this run: `N24 (121,12)` (`unsorted=3`), `N25 (130,14)` (`unsorted=4`), `N29 (165,14)` (`unsorted=1`), `N31 (179,14)` (`unsorted=1`), and `N32 (184,14)` (`unsorted=1`).

## Working Tools
- `runs/2026-10-19-0142/code/check_sn_bits.c` (`check_sn_bits`): multithreaded C 64-bit word bit-sliced exhaustive $2^n$ verifier + `--check-1minimal`.
- `runs/2026-10-19-0142/code/check_sorting_network.py`: dual-method Python/NumPy verifier (bit-sliced $2^n$ + exact Layer-1 $3^k \cdot 2^{n-2k}$ reachable-output-set propagation).
- `runs/2026-10-19-0142/attempts/settled-check/code/audit_tables.py`: full table extractor, DAG-component reachable-set verifier, and $\pm\infty$ trajectory / contraction auditor.
- `runs/2026-10-19-0142/attempts/constructor/code/{suffix_synth.c,channel_del_scan.c,cross_layer_window.c}`: exact C branch-and-bound suffix synthesizer and multi-wire projection scanner.
- `runs/2026-10-19-0142/attempts/optimizer/code/{opt_suffix.c,prep_rk.py}`: multithreaded C bit-parallel reachable-set suffix optimizer with defect-trajectory pruning.

## Beliefs
- On `sorting-network-size-records`, Dobbelaere's `SorterHunter` table (updated `2026-10-10` and `2026-10-13`) is already closed under 1-minimality, 1–4 wire extreme projections, 1-wire $\pm\infty$ interior trajectory projections ($n \le 32$), and fixed-prefix ($k \ge d-3$) suffix re-optimization. Breaking a cell on $n \in 17..32$ requires either a dedicated C/SAT solver (`CaDiCaL`) over a deeper prefix cut ($k \le d-5$) or co-evolving prefix layers $2..4$ jointly with exact suffix completion.
