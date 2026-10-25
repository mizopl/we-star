---
id: v3r1t4s-ihtp-ihtc2024-hidden-m-instances-upper-bounds
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
tractability: 3
compute: "laptop-hours"
disclosure: open
status_checked: "2026-10-15"
---
# IHTC-2024 competition (m01-m30) instances: lower a best known integrated surgery-admission-nurse schedule cost below the post-competition table

# Overview

> Bank id `ihtp-ihtc2024-hidden-m-instances-upper-bounds` · harvest · tractability 3 · laptop-hours · disclosure **open**
> Bank says open as of 2026-10-15. Statuses go stale — re-check the primary source before any work.

## Statement

The 30 m-instances of the Integrated Healthcare Timetabling Competition 2024 (organised by Sara Ceschia, Roberto Maria Rosati, Andrea Schaerf and Eugenia Zanazzo of the University of Udine with Pieter Smet and Greet Vanden Berghe of KU Leuven) were hidden during the competition and used to rank the five finalists (SDU, V777V, UGent, Twente, Ortec) under a time limit; they are now released (ihtc2024_final_instances.zip). The organisers' IHTP page lists post-competition upper bounds with solutions, e.g. m01 3380, m04 3318, m10 26015, m15 28080, m17 22365, m26 69730, several below the best competition runs (for example m15 28727 and m17 22542 by SDU in the final results CSV). Unlike the public i-instances, these received only finalist time-limited runs plus later research, so unlimited-time improvements are plausible.

## Success criterion

A solution JSON for one of m01-m30 that the official IHTP_Validator reports with zero hard-constraint violations and total cost STRICTLY LOWER (direction: min) than the m-instance cost listed on https://ihtc2024.github.io/ihtp/index.html, re-fetched live immediately before claiming, and lower than any value for that instance found by the NOVELTY check in later IHTP papers.

## Partial wins

- {"id": "p1", "statement": "Strictly improve any one m-instance bound with a validated solution."}
- {"id": "p2", "statement": "Strictly improve 3 or more m-instances with one method and fixed settings, with run logs."}

## Verification

As for the i-instances: compile the official validator, run it on instance and solution, require 0 violations and read the cost; re-validate the listed solution to confirm the build; re-fetch the table. Seconds.

## Angles

- Warm-start from the listed solution and the finalists' public code (SDU/IMADA and others link their repositories from the competition page), then run them far longer than the competition limit with restarts.
- Exact repair of sub-blocks (one surgeon-day, one ward-week) with CP-SAT inside a local search.
- Cross-domain import (genetic improvement in compiler autotuning): evolve the parameter settings of an existing finalist solver per instance class rather than writing a new solver.
- Cross-domain import (scheduling in semiconductor fabs): dispatch rules learned from good solutions to construct better initial schedules for the admission subproblem.
- Lower-bound side: a MIP relaxation of the admission subproblem alone gives a bound; if it is close to the listed cost on some instance, skip that instance.

## Pitfalls

- The final-results CSV ranks time-limited competition runs; the IHTP page is the current bar. Beating the CSV but not the page is not a record.
- Only the official validator with zero violations counts.
- m-instances and i-instances share names of fields but are different sets; do not compare an m-solution to an i-bound.
- The page updates from emailed submissions; re-fetch before claiming and check new papers.
- Synthetic hospital data: optimisation progress, not evidence about patient care.

## Sources

- https://ihtc2024.github.io/ihtp/index.html
- https://ihtc2024.github.io/assets/files/ihtc2024_final_instances.zip
- https://ihtc2024.github.io/assets/files/ihtc2024_fin_results.csv
- https://github.com/ihtc2024/ihtc2024.github.io/blob/main/assets/files/IHTP_Validator.cc
- Status source: https://ihtc2024.github.io/ihtp/index.html

## Citations

- [Problem page](../../../../.raw/V3R1T4S/known-unknowns/optimization-benchmarks/ihtp-ihtc2024-hidden-m-instances-upper-bounds.md)
- [Bank entry](../../../../.raw/V3R1T4S/bank/targets.json) (id `ihtp-ihtc2024-hidden-m-instances-upper-bounds`, commit `7dd4480`)

## Related Nodes

- [[V3R1T4S Optimization benchmarks]]
- [[V3R1T4S]]
