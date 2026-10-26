---
id: v3r1t4s-cat-ancient-texts
type: concept
tags: [v3r1t4s, v3r1t4s/category]
inbound_links: 2
confidence: 0.9
last_ingested_sources: [".raw/V3R1T4S/bank/categories.json@7dd4480"]
---
# V3R1T4S Ancient texts and fragments

# Overview

Unidentified papyri, tablet fragments, lacunae and sign detection, scored against held-out data. — 4 open problems in the bank.

## Status (live)

```dataview
TABLE status, priority, kind, tractability, disclosure
FROM "wiki/entities/v3r1t4s/ancient-texts"
SORT tractability DESC
```

## Problems

| Problem | Kind | Tractability | Disclosure |
|---\lvert ---\rvert---\lvert ---\rvert
| [[ebl-unidentified-fragment-overlaps]] | harvest | 3 | open |
| [[akkadian-lacuna-restoration-heldout]] | harvest | 2 | open |
| [[cuneiform-sign-detection-maicubeda]] | harvest | 2 | open |
| [[dclp-unidentified-literary-papyri]] | harvest | 2 | open |

## Citations

- [Category README](../../../../.raw/V3R1T4S/known-unknowns/ancient-texts/README.md)
- [categories.json](../../../../.raw/V3R1T4S/bank/categories.json)

## Related Nodes

- [[V3R1T4S]]
- [[V3R1T4S Status Board]]
