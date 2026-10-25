---
id: v3r1t4s-care-enzyme-reaction-retrieval-hard
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
tractability: 3.5
compute: "laptop-hours"
disclosure: open
status_checked: "2026-10-15"
---
# CARE benchmark: beat the best published accuracy for retrieving the enzyme class (EC number) of an unseen reaction

# Overview

> Bank id `care-enzyme-reaction-retrieval-hard` · harvest · tractability 3.5 · laptop-hours · disclosure **open**
> Bank says open as of 2026-10-15. Statuses go stale — re-check the primary source before any work.

## Statement

CARE (Classification And Retrieval of Enzymes; Jason Yang, Ariane Mora, Shengchao Liu, Bruce Wittmann, Anima Anandkumar, Frances Arnold, Yisong Yue; NeurIPS Datasets and Benchmarks 2024, arXiv:2406.15669) fixes train/test splits for two tasks. Task 2 asks: given a chemical reaction, rank EC numbers so the correct one comes first. On the medium split (all reactions of the test EC numbers held out) and hard split (all reactions of the test EC level-3 classes held out), published accuracy is low: hard split level-3 accuracy 9.8% and level-2 accuracy 22.2% (CREEP with text), level-1 57.6% (CREEP); medium split level-4 accuracy 7.4%, level-3 59.5% (CREEP with text). The paper itself says 'performance on the harder splits is weak across the board'. Task 1's <30%-identity protein split (CLEAN 55.1% level-4) is a second front. All splits, baselines and per-entry result files (task1_baselines/results_summary, task2_baselines/results_summary) are public.

## Success criterion

A ranked EC-number output file for every entry of a CARE test split, in the repository's results_summary format, whose k=1 accuracy at a given EC level, recomputed by the skeptic with the repository's performance_evaluation.ipynb, is STRICTLY HIGHER (direction: max) than the best method for that split and level in arXiv:2406.15669 Tables 2/4 and the repository results (re-fetched live immediately before claiming) by at least 3 percentage points, and higher than any value for that split and level in later published work found by the NOVELTY check. Training uses only the split's designated train files (plus the optional files the README lists for that split).

## Partial wins

- {"id": "p1", "statement": "Task 2 hard split: level-3 accuracy above the published best by >= 3 points (predicting EC classes never seen with any training reaction)."}
- {"id": "p2", "statement": "Task 2 medium split: level-4 accuracy above the published best by >= 3 points."}
- {"id": "p3", "statement": "Task 1 <30% identity split: level-4 accuracy above CLEAN's published value by >= 3 points with a CPU-feasible method (e.g. small protein language model embeddings plus retrieval)."}

## Verification

Skeptic downloads the splits from Zenodo record 14004425 (or the repository), checks the output file covers every test entry exactly once, runs performance_evaluation.ipynb, and confirms from training logs and code that no test-split file or EC-to-reaction mapping that includes test reactions was used. Minutes.

## Angles

- Hard split means the right EC level-3 class has no training reaction, so retrieval must go through another modality: rank candidate ECs by similarity of the query reaction to the reaction CENTRES (atom-mapped bond changes) implied by EC class definitions, which are text and exist for unseen classes.
- Cross-domain import (zero-shot classification in vision): describe each EC class by attributes (bond type broken/formed, cofactor, substrate class) parsed from the EC nomenclature and learn a reaction-to-attribute model, as zero-shot learning does for unseen object classes.
- Cross-domain import (information retrieval): reciprocal rank fusion of several weak rankers (DRFP similarity, reaction-centre fingerprint, text similarity of EC names) is robust and needs no learned weights.
- Exploit hierarchy: predict level 1, then level 2 conditioned on level 1, etc., with a hierarchical softmax; errors at deep levels are less costly to the shallow-level metrics.
- Use the optional protein2EC file: embed sequences of enzymes with known ECs (small ESM-2 on CPU) and connect reactions to ECs through predicted substrate-binding residues or Pfam domains.

## Pitfalls

- The hard and medium splits hold out entire EC numbers/classes; using full EC-to-reaction databases (Rhea, BRENDA, KEGG) that include the held-out reactions is leakage even if it looks like 'external knowledge'.
- ChatGPT-style baselines were flagged in the paper as possibly leaked; an LLM-based method has the same problem and must be shown not to recall the test reactions.
- Promiscuous-split and k=1 accuracy conventions differ (k equals number of true ECs there); use the notebook's exact definitions.
- Later papers may already report higher numbers on CARE; the NOVELTY skeptic must search for them before a claim.

## Sources

- https://arxiv.org/html/2406.15669
- https://github.com/jsunn-y/CARE
- https://arxiv.org/abs/2406.15669
- https://zenodo.org/records/14004425
- Status source: https://arxiv.org/html/2406.15669

## Citations

- [Problem page](../../../../.raw/V3R1T4S/known-unknowns/biology/care-enzyme-reaction-retrieval-hard.md)
- [Bank entry](../../../../.raw/V3R1T4S/bank/targets.json) (id `care-enzyme-reaction-retrieval-hard`, commit `7dd4480`)

## Related Nodes

- [[V3R1T4S Biology]]
- [[V3R1T4S]]
