---
id: v3r1t4s-miplib2017-open-primal-bound
type: entity
tags: [v3r1t4s, v3r1t4s/optimization-benchmarks, kind/harvest]
inbound_links: 1
confidence: 0.8
last_ingested_sources: [".raw/V3R1T4S/bank/targets.json@7dd4480"]
status: "open"
priority: ""
notes: ""
category: optimization-benchmarks
kind: harvest
tractability: 2.5
compute: "laptop-hours"
disclosure: open
status_checked: "2026-10-08"
---
# MIPLIB 2017: improve the best known objective of an open collection instance

# Overview

> Bank id `miplib2017-open-primal-bound` · harvest · tractability 2.5 · laptop-hours · disclosure **open**
> Bank says open as of 2026-10-08. Statuses go stale — re-check the primary source before any work.

## Statement

MIPLIB 2017 tags 212 collection instances as 'open' (no proven optimal solution); the tag page lists each instance's best known objective (marked *), or 'NA' for the 6 open instances with no known feasible solution (datt256, nucorsav, neos-3603137-hoteo, neos-3355323-arnon, supportcase30, fhnw-binpack4-58). Instance pages record every improved solution with submitter and date; improvements still arrive from individuals using local search and ML-guided heuristics (ex1010-pi: 236 Rothberg 2020 -> 234 Hattori Jan 2023 -> 233 Davletshin Oct 2023). The .solu file was last revised Sep 24 2026 (v37). Find a feasible solution with a strictly better objective (in the instance's OBJSENSE) than the listed best known objective for any open instance.

## Success criterion

A .sol file (MIPLIB format: 'varname value' lines in the original variable space of the posted .mps.gz) for one instance whose Status column is 'open' on https://miplib.zib.de/tag_open.html (one HTML <tr> per instance: Instance, Status, ..., Objective, Tags), that the MIPLIB solution checker (the checker/ directory of https://miplib.zib.de/downloads/miplib2017-testscript-v1.0.4.zip, built locally against GMP and zlib; usage 'solchecker model.mps.gz sol.sol 1e-6 1e-6') reports as feasible for the current https://miplib.zib.de/WebData/instances/<name>.mps.gz with 'Check SOL: Integrality 1 Constraints 1' at linear and integrality tolerance 1e-6, and whose objective, recomputed by the checker from the MPS objective row (including any objective offset/RHS and the OBJSENSE section; min unless the MPS says MAX), is strictly better than the objective shown for that instance on the open tag page AND on https://miplib.zib.de/instance_details_<name>.html, both re-fetched live immediately before claiming; the improvement must exceed 1e-6 * max(1, |objective|). The checker must first reproduce the posted best solution's objective for that instance (e.g. tokyometro solution 4 -> 8263.1, verified by the vetter 2026-10-08). The .sol file, checker build, instance sha256 and page snapshots are saved together. Nothing is submitted to MIPLIB; the write-up goes to the human.

## Partial wins

- {"id": "open-no-solution-first-feasible", "statement": "A checker-validated feasible solution (tolerance 1e-6) for an open instance whose Objective cell reads 'NA' on the tag page and which is '=unkn=' in the current .solu file at claim time (live 2026-10-08: datt256, nucorsav, neos-3603137-hoteo, neos-3355323-arnon, supportcase30, fhnw-binpack4-58); non-trivial because these defeated the solvers used to build MIPLIB."}
- {"id": "tie-bks-different-solution", "statement": "A checker-validated feasible solution for an open instance whose objective ties the listed best known objective within 1e-6 * max(1,|obj|) and whose integer-variable assignment differs from every solution posted on that instance's page in at least 1% of the integer variables (checked mechanically from the downloaded .sol.gz files); an alternative optimum-candidate, independently checkable."}
- {"id": "close-open-instance", "statement": "Prove optimality of an open instance (dual bound equal to the best known objective within 1e-6) with an open-source solver run that the skeptic can repeat in under 1 hour on this Mac from the saved model and parameters, or a certificate (VIPR / exact SCIP) that checks mechanically."}

## Verification

Unzip https://miplib.zib.de/downloads/miplib2017-testscript-v1.0.4.zip, 'make' in checker/ (on macOS: make CXXFLAGS="-O2 -I/opt/homebrew/include" LDFLAGS="-L/opt/homebrew/lib" with Homebrew gmp; builds in seconds, verified 2026-10-08). Download https://miplib.zib.de/WebData/instances/<name>.mps.gz and the current best solution https://miplib.zib.de/downloads/solutions/<name>/<k>/<name>.sol.gz linked from the instance page; run 'solchecker <name>.mps.gz <posted>.sol 1e-6 1e-6' and confirm it reproduces the listed objective, then run it on the claimed .sol. Minutes. Objective must be taken from the checker's recomputation, not from the file's '=obj=' comment. Re-fetch tag_open.html and the instance page with plain curl and parse the Status and Objective cells.

## Angles

- Pick open instances with modest size and a combinatorial structure that has a strong dedicated local search: set covering / set partitioning (ex1010-pi 25k binaries, improved three times by 3-flip local search), binpacking, scheduling; run the specialised heuristic for hours seeded from the posted best solution.
- Solution-polishing: fix most integer variables at the posted BKS, free a neighbourhood (random, constraint-based or objective-guided), solve the sub-MIP with HiGHS/SCIP/CP-SAT to optimality, iterate (RINS/LNS style) with 10 parallel workers.
- Instances whose latest improvement is by an individual in 2023 or later signal slack; instances with integer objectives and small coefficient ranges are safest against tolerance games.
- For the 'NA' instances, try feasibility-first approaches: CP-SAT on the pure-integer ones, feasibility pump with many restarts, and problem-specific constructive heuristics after reading the instance's description page.

## Pitfalls

- Tolerance games: a 'better' objective obtained by exploiting feasibility slack (fractional integer variables within tolerance, constraint violations near tolerance) is not a win; require 1e-6 and an improvement well above tolerance; prefer instances with integer objectives.
- OBJSENSE and offset: some MPS files declare MAX or carry an objective constant; reading 'min' by default or ignoring the RHS of the objective row flips or shifts the comparison. Use the checker's recomputed objective.
- Status drift: the 'open' tag is updated as instances are solved; re-fetch both the tag page and the instance page at claim time. An 'improvement' on an instance that has become closed indicates a checker bug.
- Instance file version: use the .mps.gz currently linked from the instance page, not a cached copy from another library with the same name.
- Presolved variants: the solution must be in the original variable space of the posted .mps.gz; the checker reports 'unexpected variable' for anything else (two harmless '#' comment lines appear in CPLEX-written .sol files).
- https://miplib.zib.de/downloads/solchecker.zip does not exist (it returns the HTML home page); the checker lives inside the testscript archive.

## Sources

- https://miplib.zib.de/tag_open.html
- https://miplib.zib.de/download.html
- https://miplib.zib.de/downloads/open-v2.test
- https://miplib.zib.de/downloads/miplib2017-testscript-v1.0.4.zip
- https://miplib.zib.de/downloads/miplib2017-v37.solu
- https://miplib.zib.de/WebData/instances/tokyometro.mps.gz
- https://miplib.zib.de/WebData/instances/ex1010-pi.mps.gz
- https://miplib.zib.de/downloads/solutions/tokyometro/4/tokyometro.sol.gz
- https://miplib.zib.de/instance_details_tokyometro.html
- https://miplib.zib.de/instance_details_ex1010-pi.html
- Status source: https://miplib.zib.de/tag_open.html

## Citations

- [Problem page](../../../../.raw/V3R1T4S/known-unknowns/optimization-benchmarks/miplib2017-open-primal-bound.md)
- [Bank entry](../../../../.raw/V3R1T4S/bank/targets.json) (id `miplib2017-open-primal-bound`, commit `7dd4480`)

## Related Nodes

- [[V3R1T4S Optimization benchmarks]]
- [[V3R1T4S]]
