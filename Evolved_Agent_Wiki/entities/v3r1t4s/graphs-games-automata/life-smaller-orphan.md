---
id: v3r1t4s-life-smaller-orphan
type: entity
tags: [v3r1t4s, v3r1t4s/graphs-games-automata, kind/standard]
inbound_links: 1
confidence: 0.8
last_ingested_sources: [".raw/V3R1T4S/bank/targets.json@7dd4480"]
status: "open"
priority: ""
notes: ""
category: graphs-games-automata
kind: standard
tractability: 1.5
compute: "laptop-hours"
disclosure: open
status_checked: "2026-10-03"
---
# Game of Life orphan with a smaller bounding box

# Overview

> Bank id `life-smaller-orphan` · standard · tractability 1.5 · laptop-hours · disclosure **open**
> Bank says open as of 2026-10-03. Statuses go stale — re-check the primary source before any work.

## Statement

An orphan is a finite rectangular pattern, every cell specified on or off, with no predecessor under Conway's Life (B3/S23). Find an orphan whose bounding-box area is below that of the smallest known orphan (8x12 = 96, Eker 2016), or certify by UNSAT proof that no orphan fits in a box size (height >= 5) not previously ruled out.

## Success criterion

(1) An m x n pattern with 5 <= min(m,n) and m*n STRICTLY LESS than the smallest orphan area listed on LifeWiki's Garden of Eden page as confirmed by a human in a browser at verification time (96 as of 2026-10-03 per Wikipedia). (2) Two independently written CNF encodings of 'there exists an (m+2) x (n+2) predecessor' are both UNSAT under CaDiCaL and kissat, and at least one DRAT/LRAT proof is checked by drat-trim or cake_lpr. (3) Sanity: the encoders return SAT with simulation-verified predecessors on 100 random non-orphans and on Eker's 8x12 with one cell flipped where applicable. (4) A human confirms on LifeWiki's Garden of Eden page that no orphan of area <= m*n is already listed. Do not bypass Cloudflare; the human gate is mandatory.

## Partial wins

- {"id": "p1", "statement": "A DRAT/LRAT-certified proof (two independent encodings, checked by drat-trim or cake_lpr) that no orphan exists in some h x w box with h >= 5 that is not already ruled out in the literature (human LifeWiki/forum check required; height <= 4 is already known)."}
- {"id": "p2", "statement": "An orphan of height h in {5, 6, 7} strictly narrower than the narrowest height-h orphan listed on LifeWiki at verification time (human-checked; 2016 values for context: widths 83, 21, 15), certified as in (2)-(3)."}

## Verification

Write an independent CNF encoder: each inner cell's next state is a function of its 3x3 neighbourhood, encoded with totalizer or cardinality clauses or directly as a 512-row truth table. Solve with cadical153 and kissat (pip install python-sat). Emit DRAT and check it with drat-trim. Cross-check the encoder on random SAT instances by simulating the predecessor it finds with a numpy Life step. A human then checks LifeWiki's Garden of Eden page in a browser.

## Angles

- Start from Eker's 8x12 and its symmetric relatives. Delete a row or column and run a MaxSAT/CEGAR loop: find the cells to flip so that the shrunken pattern has no predecessor. Each SAT counterexample (a found predecessor) becomes a blocking constraint.
- Search directly for 9x10 (area 90) and 8x11 (area 88) orphans with a 2-QBF formulation: there exists a pattern such that for all predecessors the image differs. Solve by CEGAR with incremental SAT and run the 10 cores on different symmetry restrictions (mirror, 180-degree, none).
- Tile-based composition: orphans often contain small 'unexplainable' sub-motifs. Mine the minimal unsatisfiable cores of known orphans and pack them more tightly.
- Lower-bound direction: prove 'no orphan fits in 7x7' or another unknown small box via cube-and-conquer over all patterns modulo symmetry. A DRAT-certified negative result counts as a partial win.

## Pitfalls

- Orphan and Garden of Eden are different notions. A GoE is a whole configuration; an orphan is a finite patch with all cells, including off cells, specified.
- The predecessor region must be the full (m+2) x (n+2) border-extended box.
- The record status could not be verified on LifeWiki because of Cloudflare. A human must confirm before claiming.
- SAT encodings with an off-by-one in birth or survival rules (B3/S23).
- Wade (2023) already proved that 4-high orphans do not exist. Re-proving height <= 4 impossibility is not new.
- Achim's orphan page is outdated (2004 record). Do not use it as the current record.
- Do not try to bypass the Cloudflare challenge. The human gate is mandatory.

## Sources

- https://en.wikipedia.org/wiki/Garden_of_Eden_(cellular_automaton)
- https://conwaylife.com/wiki/Garden_of_Eden
- http://wwwhomes.uni-bielefeld.de/achim/orphan.html
- https://arxiv.org/abs/1912.00692
- https://arxiv.org/abs/2210.07837
- Status source: https://en.wikipedia.org/wiki/Garden_of_Eden_(cellular_automaton)

## Citations

- [Problem page](../../../../.raw/V3R1T4S/known-unknowns/graphs-games-automata/life-smaller-orphan.md)
- [Bank entry](../../../../.raw/V3R1T4S/bank/targets.json) (id `life-smaller-orphan`, commit `7dd4480`)

## Related Nodes

- [[V3R1T4S Graphs, games and automata]]
- [[V3R1T4S]]
