---
id: v3r1t4s-cat-drug-discovery
type: concept
tags: [v3r1t4s, v3r1t4s/category]
inbound_links: 2
confidence: 0.9
last_ingested_sources: [".raw/V3R1T4S/bank/categories.json@7dd4480"]
---
# V3R1T4S Drug discovery

# Overview

Molecular property, binding, docking and design leaderboards scored on official splits. — 12 open problems in the bank.

## Status (live)

```dataview
TABLE status, priority, kind, tractability, disclosure
FROM "wiki/entities/v3r1t4s/drug-discovery"
SORT tractability DESC
```

## Problems

| Problem | Kind | Tractability | Disclosure |
|---|---|---|---|
| [[polaris-moleculeace-activity-cliff-mse]] | harvest | 4 | open |
| [[polaris-novartis-cyp3a4-aafe]] | harvest | 3.5 | open |
| [[polaris-pkis2-kinase-small-leaderboards]] | harvest | 3.5 | open |
| [[polaris-tdcommons-mirror-admet-leaderboards]] | harvest | 3.5 | open |
| [[polaris-adme-fang-biogen-endpoints]] | harvest | 3 | open |
| [[tdc-admet-cyp-inhibition-auprc]] | harvest | 3 | open |
| [[tdc-admet-excretion-spearman-leaderboards]] | harvest | 3 | open |
| [[tdc-admet-regression-mae-caco2-ppbr-ld50]] | harvest | 3 | open |
| [[tdc-admet-small-classification-auprc-auroc]] | harvest | 3 | open |
| [[tdc-dti-dg-bindingdb-patent-pcc]] | harvest | 3 | open |
| [[posebusters-redock-pb-valid-rate]] | harvest | 2.5 | open |
| [[tdc-docking-drd3-oracle-budgeted-generation]] | harvest | 2.5 | open |

## Citations

- [Category README](../../../../.raw/V3R1T4S/known-unknowns/drug-discovery/README.md)
- [categories.json](../../../../.raw/V3R1T4S/bank/categories.json)

## Related Nodes

- [[V3R1T4S]]
- [[V3R1T4S Status Board]]
