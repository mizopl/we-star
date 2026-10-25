---
id: v3r1t4s-edit-metric-dna-codes-gc
type: entity
tags: [v3r1t4s, v3r1t4s/biology, kind/standard]
inbound_links: 1
confidence: 0.8
last_ingested_sources: [".raw/V3R1T4S/bank/targets.json@7dd4480"]
status: "open"
priority: ""
notes: ""
category: biology
kind: standard
tractability: 1.5
compute: "laptop-hours"
disclosure: open
status_checked: "2026-10-15"
---
# Edit-distance DNA codes with GC/homopolymer constraints: beat a published lower bound

# Overview

> Bank id `edit-metric-dna-codes-gc` · standard · tractability 1.5 · laptop-hours · disclosure **open**
> Bank says open as of 2026-10-15. Statuses go stale — re-check the primary source before any work.

## Statement

DNA data storage needs codes robust to insertions/deletions: quaternary codes of length n with minimum Levenshtein (edit) distance d and constant GC-content (optionally no homopolymer runs > 3). Published lower-bound tables exist: the M.Sc. thesis Bounds on edit metric codes with combinatorial DNA constraints by Jing Sun (Brock University, 2010), which tabulates lengths 1 to 9 and minimum distances 1 to 9, and the greedy constructions and bounds of Nabil Bennenni, Kenza Guenda and T. Aaron Gulliver (Greedy Construction of DNA Codes and New Bounds, arXiv:1505.06262). Construct a code strictly larger than the best published lower bound for some (n,d,constraint) cell.

## Success criterion

A codeword list for a parameter cell listed in https://brocku.scholaris.ca/items/43d5f016-9190-4ec2-8066-81f3860f672b (thesis tables) or https://arxiv.org/abs/1505.06262, checked for length, alphabet, exact constraint set as defined by that source, all-pairs Levenshtein distance >= d, in a cell that its source does not mark as optimal (the claimant must show this, since many small cells are already exhaustively solved), with size strictly larger than the published lower bound (sources re-fetched live immediately before claiming) and than any later value found by novelty search.

## Partial wins

- {"id": "tie-largest-cell", "statement": "Reproduce the largest-n published entry with our own search."}
- {"id": "clique-optimality", "statement": "Prove a small cell optimal via exact max-clique with checkable certificate."}

## Verification

Python checker with a C/numba Levenshtein all-pairs loop; n <= 9 for the thesis tables, larger n only if the arXiv:1505.06262 tables list that cell. The checker applies the exact constraint set (reverse-complement, fixed GC content) of whichever source the cell comes from. Minutes.

## Angles

- Varshamov-Tenengolts-style quaternary constructions (Tenengolts codes) restricted to GC slice, then greedy augmentation.
- Max-clique / VNS on the edit-distance conflict graph with symmetry reduction (reversal, complement).
- Cross-domain import (bioinformatics read alignment): use banded alignment + seed indexing to make conflict-graph construction fast, enabling larger n.
- Cross-domain import (error-correcting codes for racetrack memory / deletion channels): lift known deletion-correcting binary codes via GC-bit / base-pair maps.
- Cross-domain import (evolutionary game theory): replicator-dynamics continuous relaxation of max-clique (Motzkin-Straus) for warm starts.

## Pitfalls

- The table lives in a thesis PDF behind a repository landing page; the agent must locate and parse the exact table and its constraint definitions.
- Edit distance vs insertion/deletion-only distance vs Levenshtein with substitutions: different metrics, not comparable.
- Constraint definitions (GC exactly n/2 vs within a band; homopolymer max length) vary between sources.
- Tables may be stale; novelty search required.

## Sources

- https://brocku.scholaris.ca/items/43d5f016-9190-4ec2-8066-81f3860f672b
- https://arxiv.org/abs/1505.06262
- Status source: https://brocku.scholaris.ca/items/43d5f016-9190-4ec2-8066-81f3860f672b

## Citations

- [Problem page](../../../../.raw/V3R1T4S/known-unknowns/biology/edit-metric-dna-codes-gc.md)
- [Bank entry](../../../../.raw/V3R1T4S/bank/targets.json) (id `edit-metric-dna-codes-gc`, commit `7dd4480`)

## Related Nodes

- [[V3R1T4S Biology]]
- [[V3R1T4S]]
