---
id: brain
type: synthesis
tags: [brain, meta-heuristic, research-decisions, constitution, proofer, clss]
inbound_links: 3
confidence: 0.88
last_ingested_sources: ["~/v3r1t4s/proofer/memory/predictions.tsv", "~/v3r1t4s/proofer/scripts/brain.py", "~/v3r1t4s/LOG.md", ".raw/V3R1T4S/kit/RUN.md", ".raw/V3R1T4S/kit/LESSONS.md"]
---
# BRAIN

# Overview

`BRAIN` is the meta-layer **above** individual target runs: the meta-heuristic and executable decision engine (`~/v3r1t4s/proofer/scripts/brain.py`) that decides *what* to work on and *how* to attack it, learns from its own calibration bets and dead-end branches, and scans the `V3R1T4S` problem bank for the **CLSS (*Compositional Lifting + Seam Surgery + Bit-Parallel Exact Oracle*)** paradigm and Laws `M1–M7`. Individual `V3R1T4S` runs are the muscles (attack, skeptic panel, verification gate). `BRAIN` is the prefrontal cortex: budget allocation, selecting the next move, deciding when to pivot away from a stalling hypothesis, and accounting for prediction errors.

**Constitutional Status (`CONSTITUTION` v14–v17 §12–§17):** Proposals **K1–K12 and Laws M1–M7 are enacted as binding law and executable code** (`brain.py`, `micro_bet.py`, `jobs.py`, `postdict.py`, `preflight.sh`, `tug.py`). Initial conclusions were grounded in data from Cycles 1–19 (2026-10-17..18): 6 runs, 36 bets (32 resolved, Brier `0.203`), 116 reasoning-graph nodes (`36` dead, `4` closed), and subsequently scaled across 49 cycles to **29 verified `V3R1T4S` packages across all 18/18 categories**, **31 official `IHTC-2024` BKS records**, and **30 Quantum `AME/MDS` certificates**.

---

## 1. Empirical Observations (Evidence from Cycles 1–19)

| # | Observation | Data | Label |
|---|---|---|---|
| O1 | The first confirmed breakthrough came from a **smaller-first** attack on a sibling sequence with a fast deterministic checker (`A054759` torus counts instead of `A006506`) | run 1225 → 1252; P0006 p=0.20 hit; PR #366 | NUMERICAL |
| O2 | **Half of early dead ends were infrastructure, not mathematics**: `X1–X10` converted into automated `preflight.sh` gates (`0` repeats after `K4`) | graph: 36 dead; `preflight.sh` 0 FAIL | NUMERICAL |
| O3 | Calibration across the first 32 resolved bets: Brier **0.203** (`target` mean `0.667`, `lens` mean `0.688`, `exp` mean `0.455`) | `calibration.md`, 32 resolved bets | NUMERICAL |
| O4 | Systematic **underconfidence toward exact computational engineering** and **overconfidence regarding how much fits into a single session** | prediction ledger | HEURISTIC |
| O5 | Worker runs **graded their own bets too generously** prior to `K3` (`P0002`, `P0014`); from `v10` onward only the Commander or a fresh Monitor session resolves bets | commander postdictions | NUMERICAL |
| O6 | **Compute cost grows exponentially in the tail**: `×1.6` per transfer-matrix width; the final 5 of 40 cells of antidiagonal 79 account for ~75% of total runtime | `secs` column, F21 | NUMERICAL |
| O7 | **Two Clocks (`K2`) work flawlessly:** worker pool `w39` progressed in the background to `33/37` modular residues with zero LLM token burn | `jobs.py list` | NUMERICAL |
| O8 | **Scouting and `PREREG` caught a flawed success criterion** ($10^{-3}$ growth clause mathematically unreachable at finite $n$) before any compute was wasted | dry run 1221, F5 | NUMERICAL |
| O9 | **Submission throughput (`outbox/`) can become the bottleneck**: 21 records generated in a single run require separate 1-cell-per-PR skeptic panels | run 0304, PR #397, PR #398 | NUMERICAL |
| O12 | **Generalized Breakthrough Law — CLSS (*Compositional Lifting + Seam Surgery*):** the largest step-change jumps over published record tables (21 new records in `covering-designs-record`, including `-4,019` and `-10,186` blocks) occur where we (1) build a sub-second bit-parallel oracle in C/NumPy, (2) relax rigid classical recursive gluing (staircase subsets, block partitions), and (3) apply local exact surgery (`prune.c`, `merge.c`, flip-graph `reduce`, SAT-window) exclusively on the **seam** between glued sub-objects | run 0304 (`stair_build.py` + `prune.c` + `merge.c`) | NUMERICAL |

## 2. Diagnosis: Four Failure Classes

1. **Infrastructure Failures** (O2, O7): the environment kills valid work. Prevented by `preflight.sh` (`X1–X12`) and the `jobs.py` background queue (`K2`).
2. **Budget Failures** (O4, O6): sound mathematical idea, wrong runtime estimate. Prevented by `proofer/memory/costs.tsv` (`K5`) and offloading exponential compute tails to `jobs.py`.
3. **Epistemic Failures** (O3, O5): grading one's own homework. Prevented by independent bet resolution (`K3`) and 3 fresh context-isolated skeptics.
4. **Strategic Failures** (O9, O1, O12): local-minimum tunneling and missing compositional seams. Solved in `v14–v17` by the executable scanner **`brain.py scan`** (`K1`, `K8`, `K9`) and Micro-Bet Governor **`micro_bet.py`** (`K10`, `M1–M7`).

## 3. BRAIN v2 Decision Loop (`brain.py`)

```
SENSE (brain.py status) → MODEL (posteriors + costs.tsv + S_CLSS) → DECIDE (brain.py scan + vs_sample + tug) → DISPATCH (run.sh / jobs.py) → SCORE (postdict.py) → UPDATE
```

- **Decision Index (`K1` + `K8` + `K9`):**
  $$I(a) = \frac{p(a) \cdot V(a) \cdot V_{\text{outlet}}(a)}{C(a)} + 0.25\,\text{Unc}(a) + 0.40\,S_{\text{CLSS}}(a) + \text{ExploreBonus}(a)$$
  where $S_{\text{CLSS}}(a) \in [0,1]$ scores the 4 components of the CLSS paradigm:
  1. **Fast Exact Oracle (`oracle`, $0..0.30$):** verification in seconds via bit-slicing, bitmasks, BFS girth, Brent equations, or exact Bareiss integer determinants.
  2. **Compositional Scaffold (`scaffold`, $0..0.25$):** ability to compose smaller objects, voltage lifts, symmetric prefixes, or block tensor decompositions.
  3. **Seam Surgery Amenability (`surgery`, $0..0.25$):** presence of a boundary seam between sub-objects where `prune`/`merge`, flip-graph `reduce` transitions, or SAT/CP-SAT suffix repair removes redundancy.
  4. **Partial-Win Ladder (`partials`, $0..0.20$):** named `p1`, `p2` milestones enabling the `H-sibling` (`smaller-first`) strategy.

## 3a. DECIDE as an Adversarial Tug-of-War (`v11`, §13)

| Biological Brain | PROOFER |
|---|---|
| Competing neural populations | Two advocates in isolated contexts (`tug-advocate.md`), tool-less (`agy --agent tug-advocate --disable-slash-commands`) |
| Mutual lateral inhibition | Structured rounds: critique → rebuttal → counter-critique in both directions |
| Decision threshold crossing | Explicit concession by one side: exactly one `LOST` and one `WON` |
| Evidence accumulation across bouts | Replay with the full public transcript plus **only that advocate's own** private notes |
| Unresolved tie | `DEADLOCK` after round limit; resolved by `brain.py` index or human architect |

## 4. Operational Heuristics

- **H-CLSS** (O12, K9): before launching stochastic search from scratch, build a sub-second bit-parallel oracle in C/NumPy (`< 5 s`), compose a starting state from known smaller building blocks with a relaxed boundary seam, and apply exact local surgery (`prune`/`merge`/flip-reduce/SAT-suffix) exclusively on the seam.
- **H-sibling** (O1): before attacking the flagship target, find a sibling problem sharing the same machinery with a cheaper checker and solve it first.
- **H-tail** (O6): when compute costs grow geometrically, place bets in stages. Price the final block separately and dispatch it via `jobs.py`.
- **H-verify-is-a-run** (O4): budget 20–45 minutes of a dedicated session for independent verification and the 3-skeptic panel.
- **H-infra-first** (O2): every new execution pipeline gets a 60-second smoke test before full deployment.
- **H-scout-criterion** (O8): scouting always verifies whether the formal success criterion is mathematically satisfiable at finite $n$.
- **H-outlet** (O9, K8): when an unsubmitted package is waiting in `outbox/`, `V_outlet` dampens duplicate packages on the same target and promotes a fresh domain.

## 5. Constitutional Laws of BRAIN (`v10` → `v17`: **K1–K12 & M1–M7 Enacted**)

| # | Constitutional Provision | Status | Enforcing Script |
|---|---|---|---|
| K1 ✅ | **§12.1 Decision Index & Exploration Quota**: `brain.py scan` + `brain.py decide` (`proofer/memory/decisions.tsv`) | Enacted v14 | `proofer/scripts/brain.py` |
| K2 ✅ | **§12.2 Two Clocks**: compute > 15 min queued in `jobs/` + `launchd` ticker + `X11` pause-aware cap | Enacted v10/v15 | `proofer/scripts/jobs.py` |
| K3 ✅ | **§12.3 Independent Bet Resolution**: `PROOFER_ROLE=run` blocked from calling `resolve` | Enacted v10 | `proofer/scripts/postdict.py` |
| K4 ✅ | **§12.4 Infrastructure Dead-End Preflight**: `X1–X12` + `K1/K9/K10` in `preflight.sh` | Enacted v10–v16 | `proofer/scripts/preflight.sh` |
| K5 ✅ | **§12.5 Explicit Cost Model**: `proofer/memory/costs.tsv` | Enacted v14 | `proofer/scripts/brain.py` |
| K6 ✅ | **§12.6 Verbalized Sampling & Reasoning-Graph Telemetry**: `brain.py status` | Enacted v14 | `proofer/scripts/brain.py` |
| K7 ✅ | **§12.7 Ratchet Applicability Gate**: only with a fast deterministic oracle (`< 60 s`) | Enacted v14 | `CONSTITUTION.md` §12.7 |
| K8 ✅ | **§12.8 Outbox Throughput Multiplier ($V_{\text{outlet}}$)** | Enacted v14 | `proofer/scripts/brain.py` |
| K9 ✅ | **§15 CLSS Protocol (*Compositional Lifting + Seam Surgery*)** | Enacted v14 | `proofer/scripts/brain.py` + `PROOFER.md` §10 |
| K10 ✅ | **§16 Dual-Thread Meta-Commander & Continuous Autoresearch Governor**: `brain.py audit` + 45-min schedule | Enacted v15 | `proofer/scripts/brain.py` + `HEARTBEAT.md` |
| K11 ✅ | **§17 Federated Multi-Thread Micro-Bet Engine (`M1–M6`)**: `micro_bet.py` + 2-miss pivot | Enacted v16 | `proofer/scripts/micro_bet.py` |
| K12 ✅ | **§17 Law `M7` Cross-Domain Structural Isomorphism & Outreach Auditor (`X12`)** | Enacted v17 | `CONSTITUTION_v17.md` §17 |

## Citations

- BRAIN v2 & CLSS Engine: `~/v3r1t4s/proofer/scripts/brain.py`
- Bet, Decision & Cost Ledgers: `~/v3r1t4s/proofer/memory/{predictions,decisions,costs}.tsv`
- Evolutionary Report v14: [Meta_Analysis_Report_v14.md](../reports/01_meta_analysis_evolution_v9_to_v17/Meta_Analysis_Report_v14.md)
- Kit: [kit/RUN.md](../../.raw/V3R1T4S/kit/RUN.md), [kit/LESSONS.md](../../.raw/V3R1T4S/kit/LESSONS.md)

## Related Nodes

- [[V3R1T4S]] · [[V3R1T4S Status Board]] · [[results/A054759(15) result]] · [[results/C(94,13,5) result]] · [[results/C(68,14,5) result]]
