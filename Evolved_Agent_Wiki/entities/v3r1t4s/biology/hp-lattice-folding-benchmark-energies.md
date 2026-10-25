---
id: v3r1t4s-hp-lattice-folding-benchmark-energies
type: entity
tags: [v3r1t4s, v3r1t4s/biology, kind/harvest]
inbound_links: 1
confidence: 0.8
last_ingested_sources: [".raw/V3R1T4S/bank/targets.json@7dd4480"]
status: "open"
priority: ""
notes: ""
category: biology
kind: harvest
tractability: 2
compute: "laptop-hours"
disclosure: open
status_checked: "2026-10-15"
---
# HP lattice protein folding: beat a best-known energy on a standard 2D/3D benchmark sequence

# Overview

> Bank id `hp-lattice-folding-benchmark-energies` · harvest · tractability 2 · laptop-hours · disclosure **open**
> Bank says open as of 2026-10-15. Statuses go stale — re-check the primary source before any work.

## Statement

The hydrophobic-polar (HP) lattice model (E = -1 per non-bonded H-H lattice contact, self-avoiding walk) has a standard benchmark set: 2D square-lattice S1-1..S1-11 (20-100 residues) and 3D cubic S2-1..S2-10 (48-mers) listed in Chris Thachuk, Alena Shmygelska and Holger Hoos (BMC Bioinformatics 2007, Table 1), plus the longer 3D cubic chains of length 64, 88, 103, 124 and 136 compiled by Thomas Wüst and David Landau (arXiv 1301.3466). For the long 3D chains the best-known energies (e.g. 3D103 = -58, 3D136 = -83 as reported there) are NOT proven ground states. Find a valid conformation with energy strictly lower than the best published value for any benchmark sequence whose optimality is not proven.

## Success criterion

A conformation file (sequence + absolute lattice coordinates or relative move string) for a benchmark sequence taken verbatim from https://www.ebi.ac.uk/europepmc/webservices/rest/PMC2071922/fullTextXML (Table 1) or the 3D long-chain table of https://arxiv.org/abs/1301.3466, such that an independent checker confirms (a) the decoded HP string equals the published sequence character-for-character, (b) consecutive residues are unit lattice neighbours, (c) no two residues share a site, and (d) the count of non-consecutive H-H unit-distance contacts gives an energy strictly lower (more negative) than the lowest value published for that sequence in either table AND in any later paper found by a NOVELTY literature search (2013-2026, e.g. arXiv 2504.15634); both tables re-fetched live immediately before claiming, and the sequence must not be one with a published proof of optimality (e.g. CPSP exact results for 3D 48-mers).

## Partial wins

- {"id": "tie-3d136-independent", "statement": "Independently reach the published best energy (-83 or whatever the table lists) for the 3D cubic 136-mer with our own code from a random start; checker-confirmed; non-trivial because PERM variants stalled at -80."}
- {"id": "fcc-or-tri-new-best", "statement": "A new best-known energy for one of the same sequences on the 3D FCC or 2D triangular lattice where a published table (with URL) exists, strictly below the published value."}
- {"id": "exact-lower-bound-3d103", "statement": "A machine-checkable certificate (e.g. CPSP-style H-core bound or ILP dual bound) that the 3D103 ground state is >= some value, closing part of the gap to -58."}

## Verification

~50-line Python checker: expand the H/P run-length notation exactly as printed, decode moves/coordinates, assert self-avoidance and unit steps, count H-H topological contacts (|i-j|>1, Manhattan distance 1). Run first on a known-optimal 2D 20-mer to reproduce -9. Seconds per check.

## Angles

- Pull-move local search + replica exchange Monte Carlo (Thachuk 2007) and FRESS fragment regrowth, seeded from many random starts, 10 cores in parallel on the 3D103/124/136 chains.
- PERM/nPERM chain growth with importance sampling and Wang-Landau flat-histogram reweighting to escape the -80 basin on the 136-mer.
- Constraint programming: CPSP-style approach (build maximally compact H-cores first, then thread the chain through with a CP-SAT solver) - exact for 48-mers, as a large-neighbourhood move on long chains.
- Cross-domain import (VLSI placement/routing): treat the chain as a net routed through a 3D grid and use rip-up-and-reroute of 10-20 residue windows with a SAT/ILP router maximizing H-H adjacency.
- Cross-domain import (statistical physics of spin glasses): parallel tempering with population annealing and cluster moves borrowed from Ising spin-glass ground-state search.
- Cross-domain import (game AI): Nested Monte Carlo Search / NRPA over move sequences (the method that solved Eterna100 RNA design) with a learned policy prior.

## Pitfalls

- Run-length notation: H^i/P^i and (s)^i must be expanded exactly; a single off-by-one residue changes the instance. Assert sequence length equals the published length.
- Many 2D S1 and all 3D 48-mer values are already proven optimal (CPSP); 'beating' them means the checker is wrong. Only target sequences without an optimality proof.
- Energy conventions differ between papers (some count E=-1 per contact, some report positive contact counts; some exclude i,i+2 contacts which are impossible on bipartite square/cubic lattices anyway). Reproduce a published optimum first.
- Different papers use differently labelled 3D sequences (the 2025 RL paper relabels and mixes 2D/3D); match the exact string, not the label.
- NOVELTY: the tables are static papers; a lower energy might already exist in post-2013 literature. Search before claiming.

## Sources

- https://www.ebi.ac.uk/europepmc/webservices/rest/PMC2071922/fullTextXML
- https://arxiv.org/abs/1301.3466
- https://arxiv.org/pdf/2504.15634
- Status source: https://www.ebi.ac.uk/europepmc/webservices/rest/PMC2071922/fullTextXML

## Citations

- [Problem page](../../../../.raw/V3R1T4S/known-unknowns/biology/hp-lattice-folding-benchmark-energies.md)
- [Bank entry](../../../../.raw/V3R1T4S/bank/targets.json) (id `hp-lattice-folding-benchmark-energies`, commit `7dd4480`)

## Related Nodes

- [[V3R1T4S Biology]]
- [[V3R1T4S]]
