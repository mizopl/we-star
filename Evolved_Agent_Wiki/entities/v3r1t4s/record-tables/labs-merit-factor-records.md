---
id: v3r1t4s-labs-merit-factor-records
type: entity
tags: [v3r1t4s, v3r1t4s/record-tables, kind/harvest]
inbound_links: 1
confidence: 0.8
last_ingested_sources: [".raw/V3R1T4S/bank/targets.json@7dd4480"]
status: "open"
priority: ""
notes: ""
category: record-tables
kind: harvest
tractability: 2
compute: "laptop-hours"
disclosure: open
status_checked: "2026-10-03"
---
# Low-autocorrelation binary sequences: best-known merit factors for lengths 67-600

# Overview

> Bank id `labs-merit-factor-records` · harvest · tractability 2 · laptop-hours · disclosure **open**
> Bank says open as of 2026-10-03. Statuses go stale — re-check the primary source before any work.

## Statement

For a +-1 sequence s of length L, the aperiodic autocorrelations are C_k = sum_i s_i s_{i+k}, the energy is E = sum_{k=1}^{L-1} C_k^2, and the merit factor is F = L^2/(2E). Optimal E is known for all L <= 66 (Packebusch-Mertens 2016), and optimal skew-symmetric values are known up to 119. For larger L, only best-known values exist. They were improved in 2025 for 16 lengths in 92..120 (arXiv:2504.00987) and in Jun 2026 for 35 lengths in 450..527 plus L=573 (arXiv:2607.09688). Any sequence with lower energy than the best known for its length is a new record. OPEN and active as of 2026-10-03. Latest: Psenicnik-Boskovic-Popic-Brest, arXiv:2607.09688 (17 Jun 2026). Lengths 121..449 and above 527 may be softer.

## Success criterion

Success means an explicit +-1 sequence of length L with 67 <= L <= 600 whose exactly computed integer energy E = sum_{k>=1} C_k^2 is STRICTLY SMALLER (direction: min) than the best published energy for that L at verification time, taken as the minimum over the tables in arXiv:2607.09688, arXiv:2504.00987, the Boskovic et al. LABS records repository cited there, and any newer arXiv result. Compare integer energies, never rounded merit factors. For L <= 66 the optimum is proven; lower energy there means a bug.

## Partial wins

- {"id": "p1", "statement": "A skew-symmetric record: a skew-symmetric +-1 sequence of odd length L >= 121 whose exact energy is strictly below the best published skew-symmetric energy for that L at verification time (even if not below the unrestricted record)."}
- {"id": "p2", "statement": "A proven skew-symmetric optimum at L = 121 (one step past the published skew frontier of 119): an exhaustive branch-and-bound with re-runnable code and logs that the skeptic re-executes, reporting the optimal skew energy and a sequence attaining it."}

## Verification

Compute C_k exactly with integer arithmetic (numpy int64 correlate or a direct O(L^2) loop) and E = sum C_k^2 as a Python int. Compare integer energies, not rounded merit factors. Calibrate by recomputing the energy of a published record sequence for a nearby L. Check that the length and alphabet are correct.

## Angles

- Run memetic tabu search (Gallardo-Cotta-Fernandez style) with O(L) incremental energy updates per flip, as massively parallel restarts on 10 cores. Target lengths in 121..449 that the 2026 paper did not focus on.
- Do a two-stage search: first in the skew-symmetric subspace for odd L (half the variables), then unrestricted refinement, following arXiv:2607.09688.
- Use Legendre/rotated-Legendre and Jacobi sequence seeds with appended segments (Kirilusha-Narayanaswamy style) followed by local search, for large L.
- Use self-avoiding-walk search with Thompson-sampling prioritization of search regions.

## Pitfalls

- Comparing rounded merit factors. Compare exact integer energies.
- Best-known tables are scattered across papers with no single live table, so assemble the baseline from all cited sources and state which one was beaten.
- For L <= 66 the optimum is proven, and for skew-symmetric odd L <= 119 the skew optimum is proven but general sequences can beat it (2504.00987 did so for 99, 107, 109, 113, 119).

## Sources

- https://arxiv.org/abs/2607.09688
- https://arxiv.org/abs/2504.00987
- https://arxiv.org/abs/1512.02475
- Status source: https://arxiv.org/abs/2607.09688

## Citations

- [Problem page](../../../../.raw/V3R1T4S/known-unknowns/record-tables/labs-merit-factor-records.md)
- [Bank entry](../../../../.raw/V3R1T4S/bank/targets.json) (id `labs-merit-factor-records`, commit `7dd4480`)

## Related Nodes

- [[V3R1T4S Record tables]]
- [[V3R1T4S]]
