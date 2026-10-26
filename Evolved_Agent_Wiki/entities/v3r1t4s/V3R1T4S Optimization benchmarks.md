---
id: v3r1t4s-cat-optimization-benchmarks
type: concept
tags: [v3r1t4s, v3r1t4s/category]
inbound_links: 2
confidence: 0.9
last_ingested_sources: [".raw/V3R1T4S/bank/categories.json@7dd4480"]
---
# V3R1T4S Optimization benchmarks

# Overview

Best-known solutions on public routing, scheduling and MIP benchmark libraries. — 9 open problems in the bank.

## Status (live)

```dataview
TABLE status, priority, kind, tractability, disclosure
FROM "wiki/entities/v3r1t4s/optimization-benchmarks"
SORT tractability DESC
```

## Problems

| Problem | Kind | Tractability | Disclosure |
|---\lvert ---\rvert---\lvert ---\rvert
| [[ihtp-ihtc2024-hidden-m-instances-upper-bounds]] | harvest | 3 | open |
| [[ihtp-ihtc2024-upper-bounds]] | harvest | 3 | open |
| [[cvrplib-vrptw-gh-dimacs-bks]] | harvest | 2.5 | open |
| [[cvrplib-x-xl-xxl-bks]] | harvest | 2.5 | open |
| [[miplib2017-open-primal-bound]] | harvest | 2.5 | open |
| [[sintef-lilim-pdptw-bks]] | harvest | 2.5 | open |
| [[curtois-nrp-open-gaps-bcv-mer-instance24]] | standard | 2 | open |
| [[jsp-optimizizer-open-upper-bounds]] | harvest | 2 | open |
| [[psplib-j120-rcpsp-upper-bounds]] | harvest | 2 | open |

## Citations

- [Category README](../../../../.raw/V3R1T4S/known-unknowns/optimization-benchmarks/README.md)
- [categories.json](../../../../.raw/V3R1T4S/bank/categories.json)

## Related Nodes

- [[V3R1T4S]]
- [[V3R1T4S Status Board]]
