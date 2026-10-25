---
id: v3r1t4s-status-board
type: synthesis
tags: [v3r1t4s, dashboard]
inbound_links: 19
confidence: 1.0
last_ingested_sources: [".raw/V3R1T4S/bank/targets.json@7dd4480"]
---
# V3R1T4S Status Board

# Overview

Live status board of all problems in the `V3R1T4S` bank (rendered via the Obsidian **Dataview** plugin). Statuses are updated in the YAML frontmatter of each problem note (`status` field); `priority` and `notes` are also preserved across syncs.

**Statuses:** `open` → `watch` → `scouting` → `attacking` → `PROMISING` → `CONFIRMED_PARTIAL` / `CONFIRMED_SOLUTION`, or `dead` / `skip`.
The `CONFIRMED_*` statuses can only be granted after passing the 3-skeptic panel + `check_run.py` PASS (`V3R1T4S` Rule 3).

## Active Targets (Everything Outside `open`)

```dataview
TABLE status, priority, category, kind, tractability, notes
FROM "wiki/entities/v3r1t4s"
WHERE status AND status != "open"
SORT priority DESC, tractability DESC
```

## Status Counts

```dataview
TABLE length(rows) AS "Problems"
FROM "wiki/entities/v3r1t4s"
WHERE status
GROUP BY status
```

## Highest-Tractability Open Targets (`tractability >= 3.5`, Laptop-Amenable)

```dataview
TABLE category, kind, tractability, compute, disclosure
FROM "wiki/entities/v3r1t4s"
WHERE status = "open" AND tractability >= 3.5
SORT tractability DESC
```

## Citations

- [bank/targets.json](../../.raw/V3R1T4S/bank/targets.json)

## Related Nodes

- [[V3R1T4S]]
