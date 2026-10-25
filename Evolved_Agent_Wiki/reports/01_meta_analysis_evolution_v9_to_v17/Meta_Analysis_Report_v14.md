# Meta Analysis Report v14 — BRAIN v2 & CLSS Autoresearch Engine (2026-10-18)

## 1. Generalizing What Works: The CLSS Solver Paradigm

Across 19 cycles, 6 V3R1T4S runs, 32 resolved predictions (Brier `0.203`), and **3 confirmed & submitted Pull Requests**:
- **PR [#366](https://github.com/elder-plinius/V3R1T4S/pull/366):** `A054759(15) = 4310182149988584261406143524214457416387448` (`CONFIRMED_PARTIAL` p1, `square-grid-lattice-gas-exact-counts-oeis`),
- **PR [#397](https://github.com/elder-plinius/V3R1T4S/pull/397):** `C(94,13,5) <= 125,184` vs CR `129,203` (`-4,019` blocks, `CONFIRMED_SOLUTION`, `covering-designs-record`),
- **PR [#398](https://github.com/elder-plinius/V3R1T4S/pull/398):** `C(68,14,5) <= 15,675` vs CR/LJCR `16,004` (`-329` blocks, `CONFIRMED_SOLUTION`, `covering-designs-record`, plus 19 more verified record-beating designs),

every breakthrough followed a single four-stage problem-solving architecture that we now formalize as **CLSS (*Compositional Lifting + Seam Surgery + Bit-Parallel Exact Oracle*)**:

1. **Stage I — Sub-Second / Bit-Parallel Exact Oracle (`Oracle First`):**
   - Never search with a slow Python verifier. Before generating a single candidate, build a bit-parallel C or NumPy exact checker (62-bit prime CRT kernel, 1-bit/uint8 combinadic rank table, 64-bit word bit-sliced 0-1 evaluator, or exact integer Brent-equation tensor verifier) that checks a candidate in `< 5` seconds and includes a built-in positive/negative self-test.
2. **Stage II — Parameter-Relaxed Compositional Lifting (`Macro-Scaffold`):**
   - Pure random/SA search from scratch fails at medium-to-large $N$ because valid structures have measure $\approx 0$.
   - Pure classical recursion (e.g. rigid 2-part splits, Kronecker tensor products, un-pruned block glue) leaves **boundary seams** because literature authors tied parameters uniformly across sub-blocks.
   - Relaxing the compositional glue (per-$j$ split parameters, nested staircase subsets $S_0 \subset S_1 \subset \dots$, voltage graph lifts, or basis-transformed block decompositions) immediately drops the upper bound and creates intentional overlap at the seam.
3. **Stage III — Deterministic Seam Surgery (`Micro-Repair`):**
   - Concentrate compute *exclusively on the seam* between composed pieces: greedy redundant-element pruning (`prune.c`), pair-to-single replacement (`merge.c`), ternary flip-graph `reduce`/`plus` walks along seam rank-one terms, or exact SAT/CP-SAT window repair on the final layers.
4. **Stage IV — Dual-Decomposition / 1-Minimality Self-Break:**
   - Every candidate must survive a structural minimality or dual-decomposition check (`0` redundant blocks, two independent decompositions, or exact integer + symbolic verification) before touching the 3-skeptic panel.

---

## 2. Applying CLSS Autoresearch to PROOFER Itself (Shell v13 → v14)

Applying our own methodology to the PROOFER harness revealed an obvious "seam" in our meta-layer:
- In `BRAIN.md` §5, only `K2` (job queue), `K3` (independent scoring), and `K4` (preflight from infra dead ends) had been enacted in v10. Proposals `K1` (decision index & exploration quota), `K5` (explicit cost model `costs.tsv`), `K6` (graph & VS telemetry), `K7` (ratchet applicability rule), and `K8` (outlet queue damping) remained un-enacted prose.
- Per the rule *"prose alone decays, scripts don't"*, Shell **v14** enacts `K1`, `K5`, `K6`, `K7`, `K8`, plus **`K9` (CLSS Seam-First Solver Protocol)** via the executable engine **`~/v3r1t4s/proofer/scripts/brain.py`**:
  - `brain.py status`: computes Beta posteriors from `predictions.tsv`, outlet multiplier $V_{\text{outlet}}$ from `outbox/` vs `archive/SUBMITTED-*.txt`, and graph telemetry (`116` nodes, `36` dead, `4` closed).
  - `brain.py scan`: scores all 287 V3R1T4S targets by their CLSS Seam Score $S_{\text{CLSS}} \in [0, 1]$ and composite BRAIN Index $I(a)$, applying a $+0.20$ exploration bonus to untouched domains and emitting a validated `vs_sample.py` distribution.
  - `brain.py decide`: logs every target/lens allocation to `~/v3r1t4s/proofer/memory/decisions.tsv`.

---

## 3. New Domain Selection (`brain.py scan` + `vs_sample.py`, seed `1431196859`)

Running `brain.py scan --top 15` + `vs_sample.py` (`VS_SAMPLE: PASS`) selected two brand-new domains with maximal CLSS score (`0.920`) and index (`1.138`):
1. **`algorithms` / `fmm-ternary-integer-ring-upgrade`** (`top-ev`, $p=0.47$, CLSS `0.920`, `idx=1.138`):
   - **Why CLSS strikes here:** Across the 680 matrix-multiplication formats $\langle n,m,p\rangle$ ($\max \le 16$) in Perminov's live table (`dronperminov/FastMatrixMultiplication`), 296 formats have $R_{\text{ZT}} > R_{\mathbb{Q}}$ and 18 have $R_{\text{ZT}} > R_{\mathbb{Z}}$. Applying **Compositional Lifting** (generalized block-splitting / sub-tensor gluing of existing ZT/Z schemes across all $(n_1+n_2, m, p)$ and Kronecker/border combinations) + **Seam Surgery** (ternary flip-graph reduction & basis change on $\mathbb{Q}/\mathbb{Z}$ schemes) + **Exact Integer Brent-Equation Oracle** tests hundreds of formats in seconds.
2. **`graphs-games-automata` / `cage-upper-bounds`** (`top-ev`, $p=0.47$, CLSS `0.920`, `idx=1.138`):
   - Excision + voltage lifts + local edge-swap surgery on $(k,g)$-cages and girth-diameter / mixed cages (`p1`/`p2`).
3. **`record-tables` / `sorting-network-size-records`** (`CLSS=0.920`, `idx=0.938`):
   - Bit-sliced 64-bit 0-1 principle oracle + reflection-symmetric prefix composition + C-bitset/SAT comparator pruning across the Pareto `(size, depth)` front on Dobbelaere's table.
