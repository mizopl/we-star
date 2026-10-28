---
id: brain
type: synthesis
tags: [brain, meta-heuristic, research-decisions, constitution, proofer, clss]
inbound_links: 3
confidence: 0.88
last_ingested_sources: ["memory/predictions.tsv", "scripts/brain.py", "LOG.md", ".raw/V3R1T4S/kit/RUN.md", ".raw/V3R1T4S/kit/LESSONS.md"]
---
# BRAIN (ancestor_v13_BRAIN)

## Overview

BRAIN is the meta-heuristic decision layer above individual runs (`scripts/brain.py`), governing target and lens selection, compute budget allocation, independent calibration bet scoring, infrastructure preflight gates, and **CLSS (*Compositional Lifting + Seam Surgery + Bit-Parallel Exact Oracle*)** seam scanning.

## 1. Key Empirical Observations

| # | Observation | Evidence | Tag |
|---\lvert ---\rvert---\lvert ---\rvert
| O1 | First breakthrough came from **smaller-first (`H-sibling`)** on a sibling sequence with a fast deterministic verifier (`A054759` on the torus, PR #366) | Run 1225 -> 1252; P0006 hit | NUMERICAL |
| O2 | **Half of early dead ends were infrastructure, not mathematics:** X1–X10 converted into `preflight.sh` checks (0 repeats after K4) | Graph: 36 dead; `preflight.sh` 0 FAIL | NUMERICAL |
| O3 | Brier calibration across resolved predictions tracked via `calibration.md` | `predictions.tsv` | NUMERICAL |
| O4 | Systematic **underconfidence in exact algorithmic engineering** and **overconfidence in single-session wall-clock capacity** | Prediction ledger | HEURISTIC |
| O5 | Self-scoring bias eliminated by **K3 (independent resolution by commander or fresh skeptic)** | Commander postdictions | NUMERICAL |
| O6 | **Exponential tail cost growth:** ~1.6x per width step; handled via block bets and `jobs.py` | Runtime logs | NUMERICAL |
| O7 | **Two Clocks (K2):** long compute jobs run asynchronously via `jobs.py` without burning LLM session tokens | `jobs.py list` | NUMERICAL |
| O8 | **Scouting & PREREG criterion audit:** verifies finite-$n$ satisfiability before compute commitment | Scouting logs | NUMERICAL |
| O9 | **Outlet-queue damping ($V_{\text{outlet}}$, K8):** damps repeated claims on the same target when `outbox/` has unsubmitted packages | `brain.py` | NUMERICAL |
| O12 | **CLSS Breakthrough Law (K9):** largest record leaps arise from (1) a sub-second bit-parallel exact oracle, (2) parameter-relaxed compositional lifting, and (3) deterministic seam surgery (`prune.c`, `merge.c`, flip-graph `reduce`, SAT-window) on the boundary between composed sub-objects | Covering designs & FMM runs | NUMERICAL |

## 2. The BRAIN Control Loop (`brain.py`)

```
SENSE (brain.py status) -> MODEL (posteriors + costs.tsv + S_CLSS) -> DECIDE (brain.py scan + vs_sample + tug) -> DISPATCH (run.sh / jobs.py) -> SCORE (postdict.py) -> UPDATE
```

$$I(a) = \frac{p(a) \cdot V(a) \cdot V_{\text{outlet}}(a)}{C(a)} + 0.25\,\text{Unc}(a) + 0.40\,S_{\text{CLSS}}(a) + \text{ExploreBonus}(a)$$

## 3. Enacted Constitutional Rules (`K1–K9`)

- **K1 (§12.1):** Decision index $I(a)$ and 1-in-5 exploration quota (`brain.py scan` / `brain.py decide`).
- **K2 (§12.2):** Two clocks — jobs > 15 min queued via `jobs.py`.
- **K3 (§12.3):** Independent bet resolution (`PROOFER_ROLE=run` blocked from `resolve`).
- **K4 (§12.4):** Automated `preflight.sh` checks generated from infrastructure dead ends (`X1–X10`).
- **K5 (§12.5):** Explicit empirical cost model (`memory/costs.tsv`).
- **K6 (§12.6):** Reasoning-graph and Verbalized Sampling telemetry (`brain.py status`).
- **K7 (§12.7):** Inner-loop ratchet restricted to targets with a fast deterministic verifier (`< 60s`).
- **K8 (§12.8):** Outlet-queue damping ($V_{\text{outlet}}$).
- **K9 (§15):** Four-stage CLSS Autoresearch Solver Protocol.
