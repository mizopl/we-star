---
id: v3r1t4s-cat-herculaneum-scrolls
type: concept
tags: [v3r1t4s, v3r1t4s/category]
inbound_links: 2
confidence: 0.9
last_ingested_sources: [".raw/V3R1T4S/bank/categories.json@7dd4480"]
---
# V3R1T4S Herculaneum scrolls

# Overview

Ink detection and surface segmentation on the public Vesuvius Challenge data. — 4 open problems in the bank.

## Status (live)

```dataview
TABLE status, priority, kind, tractability, disclosure
FROM "wiki/entities/v3r1t4s/herculaneum-scrolls"
SORT tractability DESC
```

## Problems

| Problem | Kind | Tractability | Disclosure |
|---\lvert ---\rvert---\lvert ---\rvert
| [[vesuvius-profilometer-ink-dice]] | harvest | 2.5 | commit-only |
| [[vesuvius-surface-topo-holdout]] | harvest | 2 | commit-only |
| [[vesuvius-frag4-ink-f05-holdout]] | harvest | 1.5 | commit-only |
| [[vesuvius-first-letters-unread]] | standard | 1 | commit-only |

## Citations

- [Category README](../../../../.raw/V3R1T4S/known-unknowns/herculaneum-scrolls/README.md)
- [categories.json](../../../../.raw/V3R1T4S/bank/categories.json)

## Related Nodes

- [[V3R1T4S]]
- [[V3R1T4S Status Board]]
