---
id: v3r1t4s-cat-earth-and-sky
type: concept
tags: [v3r1t4s, v3r1t4s/category]
inbound_links: 2
confidence: 0.9
last_ingested_sources: [".raw/V3R1T4S/bank/categories.json@7dd4480"]
---
# V3R1T4S Earth and sky

# Overview

Missed events in open geophysical and space archives, checked against live catalogs. — 18 open problems in the bank.

## Status (live)

```dataview
TABLE status, priority, kind, tractability, disclosure
FROM "wiki/entities/v3r1t4s/earth-and-sky"
SORT tractability DESC
```

## Problems

| Problem | Kind | Tractability | Disclosure |
|---\lvert ---\rvert---\lvert ---\rvert
| [[climatebench-total-nrmse-cpu]] | harvest | 3 | open |
| [[iau-mdc-new-meteor-shower-gmn]] | harvest | 3 | open |
| [[magnet-dst-private-test-rmse]] | harvest | 3 | open |
| [[seismic-missed-events-vs-comcat]] | harvest | 3 | open |
| [[tsunami-tide-gauge-signal-not-in-ncei]] | harvest | 3 | open |
| [[apollo-moonquake-missed-vs-pds-catalog]] | harvest | 2.5 | open |
| [[ccmc-flare-scoreboard-m-bss-2023-2024]] | standard | 2.5 | open |
| [[glm-bolide-not-in-nasa-catalog]] | harvest | 2.5 | open |
| [[soho-ccor-archival-sungrazer-comet]] | harvest | 2.5 | open |
| [[ssh-mapping-ose-2021a-resolution]] | harvest | 2.5 | open |
| [[volcano-thermal-unrest-not-in-gvp]] | harvest | 2.5 | open |
| [[insight-marsquake-missed-vs-mqs-v14]] | harvest | 2 | open |
| [[s2s-ai-challenge-2020-rpss]] | standard | 2 | open |
| [[ssh-mapping-natl60-2020a-osse]] | harvest | 2 | open |
| [[wind-waves-dh-type2-missed-vs-cdaw]] | harvest | 2 | open |
| [[fermi-gbm-offline-tgf-missed]] | standard | 1.5 | open |
| [[mlgwsc1-dataset3-sensitive-distance]] | standard | 1.5 | open |
| [[nasa-tropical-storm-wind-speed-rmse]] | standard | 1.5 | open |

## Citations

- [Category README](../../../../.raw/V3R1T4S/known-unknowns/earth-and-sky/README.md)
- [categories.json](../../../../.raw/V3R1T4S/bank/categories.json)

## Related Nodes

- [[V3R1T4S]]
- [[V3R1T4S Status Board]]
