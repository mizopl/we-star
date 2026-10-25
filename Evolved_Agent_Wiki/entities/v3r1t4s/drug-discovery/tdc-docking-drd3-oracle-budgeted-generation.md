---
id: v3r1t4s-tdc-docking-drd3-oracle-budgeted-generation
type: entity
tags: [v3r1t4s, v3r1t4s/drug-discovery, kind/harvest]
inbound_links: 1
confidence: 0.8
last_ingested_sources: [".raw/V3R1T4S/bank/targets.json@7dd4480"]
status: "open"
priority: ""
notes: ""
category: drug-discovery
kind: harvest
tractability: 2.5
compute: "laptop-hours"
disclosure: open
status_checked: "2026-10-15"
---
# TDC Docking Benchmark Group (DRD3, 5,000-call docking oracle): beat the Graph-GA top-100/top-10/top-1 records

# Overview

> Bank id `tdc-docking-drd3-oracle-budgeted-generation` · harvest · tractability 2.5 · laptop-hours · disclosure **open**
> Bank says open as of 2026-10-15. Statuses go stale — re-check the primary source before any work.

## Statement

The TDC Docking Benchmark Group defines a budgeted de novo design task: generate molecules with the best DRD3 docking scores using at most a fixed number of oracle calls (the leaderboard reports 5,000-call and smaller budgets), starting from ZINC 250K, with the oracle being a docking score computed through TDC's pyscreener wrapper. The leaderboard lists only five 2021-era generators plus a 'Best-in-data' reference row (Top100 -12.080, Top10 -12.590, Top1 -12.800, Diversity 0.864, %Pass 0.780, Top1-P -11.700, M1 5.100). Rank 1 is Graph-GA (a fragment-based genetic algorithm with ZERO learned parameters): Top100 -14.811 +- 0.413, Top10 -15.930 +- 0.336, Top1 -16.533 +- 0.309, Diversity 0.626 +- 0.092, %Pass 0.393 +- 0.308, Top1-P -14.267 +- 0.450; then SMILES-LSTM (-13.017 Top100), GCPN, MARS and MolDQN. That a parameter-free GA leads by 1.8 kcal/mol over a 3M-parameter LSTM, and that nothing has been added in years, is exactly the profile of a stale, beatable table; the oracle is CPU docking, so 5,000 calls is laptop-hours to laptop-days on 10 cores.

## Success criterion

Success means a saved generation record for the DRD3 benchmark at a declared oracle budget that the leaderboard reports (5,000 calls unless a smaller listed budget is explicitly claimed), consisting of: the full ordered log of every oracle call (SMILES plus returned score, length <= the budget), the final top-100 SMILES dictionary in the format the TDC docking group expects, the exact oracle configuration (pyscreener/docking software name and version, receptor file and its sha256, box centre and size, exhaustiveness, number of poses, random seed), and 3 independent runs with different seeds. It counts only if (a) the skeptic, re-running the SAME documented oracle configuration on the submitted top-100 SMILES, reproduces each molecule's score to within 0.3 kcal/mol, (b) the mean over the 3 runs of Top100 (and separately Top10, Top1) is strictly BETTER, i.e. more negative (direction: min), than the corresponding rank-1 value in the live leaderboard table at https://tdcommons.ai/benchmark/docking_group/drd3/ , re-fetched immediately before claiming, by at least the listed rank-1 std for that column, (c) the number of distinct oracle calls never exceeded the claimed budget (checked from the log, counting repeated SMILES as the benchmark does), (d) the submitted molecules satisfy the benchmark's own auxiliary filters as reported by the leaderboard columns - Diversity, %Pass (the medicinal-chemistry filter rate) and M1 are recomputed and reported, and the claim is void if %Pass falls below the 'Best-in-data' reference row's value, and (e) every submitted molecule is novel with respect to ZINC 250K (no InChIKey match) and chemically valid by RDKit with correct valences. No synthesis route, procurement information or experimental protocol is part of this target; the deliverable is a scored SMILES list only.

## Partial wins

- {"id": "p1", "statement": "Beat the live rank-1 Top100 value with the %Pass column no worse than the 'Best-in-data' reference row (Graph-GA's own %Pass is 0.393 +- 0.308, far below the data reference 0.780), i.e. a quality-constrained improvement rather than a raw-score one."}
- {"id": "p2", "statement": "A budget-efficiency result: match or beat the live rank-1 Top10 value using at most half the claimed oracle budget, with the full call log proving the budget, verified by re-scoring the final top-10."}
- {"id": "p3", "statement": "An oracle-reproducibility artefact: a documented, pinned docking-oracle configuration (receptor sha256, box, software version, seed) plus a re-scoring script under which a published method's released DRD3 molecules reproduce their reported scores to within 0.3 kcal/mol - a reusable verification harness, reported as infrastructure rather than a record."}

## Verification

Skeptic installs the docking stack the attacker pinned (pyscreener plus the named docking binary), downloads the receptor from the attacker's manifest and checks its sha256, re-docks the submitted top-100 SMILES with the identical configuration on 10 CPU cores, compares each score to the attacker's log (tolerance 0.3 kcal/mol), recomputes Top100/Top10/Top1, Diversity, %Pass and M1 with TDC's own definitions, counts the oracle calls in the log against the budget, checks RDKit validity and ZINC-250K InChIKey novelty, then re-fetches the live leaderboard table and compares column by column. Re-docking 100 ligands is well under an hour on CPU; re-running the attacker's whole search is optional and is the laptop-days part.

## Angles

- Make the genetic algorithm smarter, not bigger: Graph-GA with zero parameters is the record, so the headroom is in the search operators - fragment libraries mined from the best-scoring hits so far, adaptive mutation rates, crowding/fitness sharing to avoid premature convergence, and an explicit archive (MAP-Elites style) binned by scaffold and size so diversity and %Pass do not collapse the way Graph-GA's do.
- Surrogate-assisted screening under a hard call budget: fit a cheap docking-score surrogate (fingerprint booster or Gaussian process) on the calls made so far and spend real oracle calls only on surrogate-predicted elites with high acquisition value - classic Bayesian optimisation over a discrete space, which the current leaderboard (one BO-free GA and four RL/VAE methods) never applied here.
- CROSS-DOMAIN (cryptanalysis / key-space hill climbing with restarts): treat the molecular graph edit sequence as a key, run many short simulated-annealing climbs with tabu lists over recently tried fragments, and restart from an elite pool - the standard recipe for beating a plain GA in a rugged discrete landscape at a fixed evaluation budget.
- CROSS-DOMAIN (coding theory / sphere packing in fingerprint space): maintain a covering code over fingerprint space so oracle calls are spent on mutually distant candidates (maximising information per call), which simultaneously raises the Diversity column that Graph-GA sacrifices.
- CROSS-DOMAIN (statistical physics / parallel tempering and population annealing): run several populations at different mutation 'temperatures' with periodic swaps, which escapes the local optima that fixed-rate GAs settle into.
- CROSS-DOMAIN (ecology / island biogeography and niche construction): island-model GA with migration between sub-populations defined by scaffold niches, with niche-specific selection pressure - a well-studied way to keep diversity while improving the best score.
- Pose-quality filtering before counting a hit: re-score elites with a second, independent scoring function and discard molecules whose score depends on an implausible pose, which protects the %Pass and plausibility columns and avoids scoring-function exploitation.

## Pitfalls

- Oracle mismatch: docking scores depend on the receptor file, box definition, exhaustiveness, software and seed. A 'record' computed with a different docking configuration than TDC's pyscreener DRD3 oracle is meaningless; the configuration must be pinned, hashed and reproducible by the skeptic, and scores must be reproduced within 0.3 kcal/mol.
- Scoring-function exploitation (the classic docking false positive): GAs reliably discover huge, greasy, poly-aromatic or strained molecules that score extremely well and are physically nonsense. This is why the claim is void if %Pass drops below the 'Best-in-data' reference and why Diversity and M1 must be reported - Graph-GA's own %Pass of 0.393 shows the record itself is partly this artefact.
- Oracle-budget cheating: calling the oracle during 'development' and then reporting only the final run's calls, caching scores across runs, or using a surrogate trained on out-of-budget oracle calls. The full ordered call log for each of the 3 runs, with repeated SMILES counted as TDC counts them, is the only acceptable evidence.
- Single-run luck: Graph-GA's listed stds are large (0.3-0.4 kcal/mol on the score columns, 0.3 on %Pass), so one lucky run can beat the mean. Three seeded runs and the std-based margin are mandatory.
- Column shopping: the table has Top100, Top10, Top1, Top1-P, Diversity, Novelty, %Pass and M1. Beating Top1 alone (a single lucky molecule) while Top100 is worse is not beating the benchmark; the claimed column must be stated and the others reported.
- Novelty trap: this leaderboard is 2021-era while the molecular-optimisation literature (PMO/mol_opt and later work) has moved on; the NOVELTY skeptic must check whether better DRD3 docking-oracle results under the same budget are already published before anything is claimed.

## Sources

- https://tdcommons.ai/benchmark/docking_group/drd3/
- https://tdcommons.ai/benchmark/docking_group/overview/
- https://github.com/mims-harvard/TDC
- Status source: https://tdcommons.ai/benchmark/docking_group/drd3/

## Citations

- [Problem page](../../../../.raw/V3R1T4S/known-unknowns/drug-discovery/tdc-docking-drd3-oracle-budgeted-generation.md)
- [Bank entry](../../../../.raw/V3R1T4S/bank/targets.json) (id `tdc-docking-drd3-oracle-budgeted-generation`, commit `7dd4480`)

## Related Nodes

- [[V3R1T4S Drug discovery]]
- [[V3R1T4S]]
