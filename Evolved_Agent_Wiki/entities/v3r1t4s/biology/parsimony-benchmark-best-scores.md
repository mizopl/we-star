---
id: v3r1t4s-parsimony-benchmark-best-scores
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
tractability: 2
compute: "laptop-hours"
disclosure: open
status_checked: "2026-10-15"
---
# Maximum parsimony: a tree with fewer steps than the best-known score on a classic benchmark alignment

# Overview

> Bank id `parsimony-benchmark-best-scores` · standard · tractability 2 · laptop-hours · disclosure **open**
> Bank says open as of 2026-10-15. Statuses go stale — re-check the primary source before any work.

## Statement

Large classic phylogenetic alignments (Zilla 500-taxon rbcL, RDPII, ARB, PROTO) and the MPBoot TreeBASE/PANDIT benchmark collection have published best-known Fitch parsimony scores from PTM, TNT, PAUP* and MPBoot (e.g. Zilla best known 16218 steps (PTM), PAUP* 16221, TNT 16219, per Table 2 of Kevin Sundberg, Mark Clement, Quinn Snell, Dan Ventura, Michael Whiting and Keith Crandall, BMC Bioinformatics 13(S13):S8; in that table the PROTO row's two scores, 162,438 and 810,231, belong to different datasets, so read the column alignment carefully). Find an unrooted binary tree with strictly fewer parsimony steps than the best published score for any such public alignment.

## Success criterion

A Newick tree over exactly the taxa of a public benchmark alignment (from the MPBoot zenodo data or the dataset cited in https://www.ebi.ac.uk/europepmc/webservices/rest/PMC3426809/fullTextXML (Table 2)) whose Fitch (unordered, equal-weight, gaps treated as the publication specifies) parsimony score, computed by two independent implementations (our checker and TNT or PAUP*-free equivalent such as MPBoot/RAxML-NG --evaluate parsimony), is strictly lower than the best published score for that dataset, both tables re-fetched live immediately before claiming, and lower than any post-2012 score found by a novelty search.

## Partial wins

- {"id": "zilla-16218-tie", "statement": "Reach 16218 on Zilla from random starting trees with open tools within laptop-hours (TNT reportedly stopped at 16219)."}
- {"id": "mpboot-dataset-improvement", "statement": "Strictly beat the MPBoot-reported best score on any one TreeBASE dataset from the zenodo supplementary data."}

## Verification

Fitch algorithm checker in Python (O(taxa x sites)), cross-checked with a second implementation; must first reproduce a published score from a published tree. Minutes.

## Angles

- TNT 'new technology' search (sectorial search, ratchet, drift, tree fusing) with many replicates on 10 cores.
- MPBoot / IQ-TREE-style stochastic NNI+SPR with perturbation, then TBR polish.
- Cross-domain import (TSP/VRP metaheuristics): treat SPR/TBR as large-neighbourhood ruin-and-recreate (as in HGS-CVRP) with genetic crossover of trees by subtree-prune-and-graft fusion.
- Cross-domain import (Steiner tree / VLSI): parsimony is the Steiner tree in Hamming space; use Steiner-point heuristics (Lin-Kernighan style edge swaps) and ILP on small sectors.
- Exact sector solving: extract 15-25 taxon sectors and solve them optimally with branch and bound, reinsert.

## Pitfalls

- Gap/missing-data treatment and character weighting change the score; reproduce a published score first with the same convention.
- The PTM 16218 vs 16234 discrepancy across two tables shows settings differ; compare like with like.
- Static 2012-2018 tables: newer TNT runs may already have beaten them; novelty search required.
- Datasets must be the exact published alignment (taxon count, site count); downloading a different version of 'Zilla' invalidates the comparison.

## Sources

- https://www.ebi.ac.uk/europepmc/webservices/rest/PMC3426809/fullTextXML
- https://zenodo.org/records/1156452
- https://arxiv.org/abs/1306.1339
- Status source: https://www.ebi.ac.uk/europepmc/webservices/rest/PMC3426809/fullTextXML

## Citations

- [Problem page](../../../../.raw/V3R1T4S/known-unknowns/biology/parsimony-benchmark-best-scores.md)
- [Bank entry](../../../../.raw/V3R1T4S/bank/targets.json) (id `parsimony-benchmark-best-scores`, commit `7dd4480`)

## Related Nodes

- [[V3R1T4S Biology]]
- [[V3R1T4S]]
