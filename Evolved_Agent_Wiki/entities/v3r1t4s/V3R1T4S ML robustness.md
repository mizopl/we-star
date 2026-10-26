---
id: v3r1t4s-cat-ml-robustness
type: concept
tags: [v3r1t4s, v3r1t4s/category]
inbound_links: 2
confidence: 0.9
last_ingested_sources: [".raw/V3R1T4S/bank/categories.json@7dd4480"]
---
# V3R1T4S ML robustness

# Overview

Stronger attacks and soundness counterexamples on public, locally run benchmark models. — 5 open problems in the bank.

## Status (live)

```dataview
TABLE status, priority, kind, tractability, disclosure
FROM "wiki/entities/v3r1t4s/ml-robustness"
SORT tractability DESC
```

## Problems

| Problem | Kind | Tractability | Disclosure |
|---\lvert ---\rvert---\lvert ---\rvert
| [[robustbench-cifar100-linf-beat-autoattack]] | harvest | 3 | open |
| [[vnncomp-2026-unsolved-instance-counterexample]] | harvest | 3 | open |
| [[robustbench-cifar10-l2-beat-autoattack]] | standard | 2 | open |
| [[robustbench-cifar10-linf-beat-autoattack]] | harvest | 2 | open |
| [[vnncomp-verifier-holds-soundness-counterexample]] | harvest | 2 | open |

## Citations

- [Category README](../../../../.raw/V3R1T4S/known-unknowns/ml-robustness/README.md)
- [categories.json](../../../../.raw/V3R1T4S/bank/categories.json)

## Related Nodes

- [[V3R1T4S]]
- [[V3R1T4S Status Board]]
