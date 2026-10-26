---
id: v3r1t4s-cat-sky-archives
type: concept
tags: [v3r1t4s, v3r1t4s/category]
inbound_links: 2
confidence: 0.9
last_ingested_sources: [".raw/V3R1T4S/bank/categories.json@7dd4480"]
---
# V3R1T4S Sky archives

# Overview

New vetted candidates in public astronomy archives (never 'a planet', only 'a candidate'). — 7 open problems in the bank.

## Status (live)

```dataview
TABLE status, priority, kind, tractability, disclosure
FROM "wiki/entities/v3r1t4s/sky-archives"
SORT tractability DESC
```

## Problems

| Problem | Kind | Tractability | Disclosure |
|---\lvert ---\rvert---\lvert ---\rvert
| [[new-periodic-variables-not-in-vsx]] | harvest | 4 | open |
| [[asteroid-precovery-arc-extension]] | harvest | 3 | open |
| [[kepler-k2-new-vetted-transit-candidate]] | harvest | 3 | open |
| [[tess-new-vetted-transit-candidate]] | harvest | 3 | open |
| [[kepler-tess-single-transit-long-period-candidate]] | harvest | 2.5 | open |
| [[kepler-eb-circumbinary-transit-candidate]] | standard | 1.5 | open |
| [[planet-nine-distant-tno-archival-moonshot]] | moonshot | 1 | open |

## Citations

- [Category README](../../../../.raw/V3R1T4S/known-unknowns/sky-archives/README.md)
- [categories.json](../../../../.raw/V3R1T4S/bank/categories.json)

## Related Nodes

- [[V3R1T4S]]
- [[V3R1T4S Status Board]]
