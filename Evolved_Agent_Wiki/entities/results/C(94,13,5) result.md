---
id: result-c-94-13-5
type: synthesis
tags: [v3r1t4s, result, CONFIRMED_SOLUTION, covering-designs]
inbound_links: 2
confidence: 0.99
last_ingested_sources: ["~/v3r1t4s/runs/2026-10-18-0304/panel/gate.md", "~/v3r1t4s/outbox/2026-10-18-mizopl-e1080bec/INDEX.csv"]
---
# C(94,13,5) result

# Overview

**`C(94,13,5) <= 125,184`** is an explicit $(94,13,5)$ covering design (`sha256 e1080beca9b83194c0ebe19400b30ebc7bdc3dab17230e7bf153eddc625bc908`) with `125,184` distinct 13-element blocks over `{0..93}` covering all $\binom{94}{5} = 54,891,018$ 5-subsets of a 94-set (`uncovered = 0`), strictly improving on the live Covering Repository record (`129,203`, by `4,019` blocks) and the La Jolla Covering Repository record (`129,337`, by `4,153` blocks).

- **Status:** `CONFIRMED_SOLUTION` (main bank criterion for `covering-designs-record`), run `2026-10-18-0304`. Three fresh-context Antigravity skeptics passed (`REPRODUCE`, `NOVELTY`, `CRITERION`), the honesty gate passed, and `check_run.py` printed `CHECK_RUN: PASS` on both the package and the workspace.
- **Method:** generalized two-part combining construction ($94 = 47 + 47$, Gordon-Kuperberg-Patashnik 1995 style) built from on-disk LJCR $v=47$ ingredient designs (`125,236` blocks), followed by pair-merge local reduction (`merge.c`, replacing `52` pairs of blocks whose uniquely covered 5-subsets span at most 13 points by single blocks to reach `125,184`).
- **1-Minimality:** Verified by the `CRITERION` skeptic to have `0` redundant blocks (`redundant_blocks = 0`): every block uniquely covers between `15` and `510` 5-subsets.
- **Outward:** Submitted on 2026-10-18 on the human's explicit `"yes"` as **draft PR [elder-plinius/V3R1T4S#397](https://github.com/elder-plinius/V3R1T4S/pull/397)**, credit `mizopl` (package `2026-10-18-mizopl-e1080bec`, branch `mizopl:claim/2026-10-18-mizopl-e1080bec`, commit `ef5cec0`).

## Citations
- Gate and panel: `~/v3r1t4s/runs/2026-10-18-0304/panel/`
- Bank definition: [targets.json](../../.raw/V3R1T4S/bank/targets.json) (id `covering-designs-record`)

## Related Nodes
- [[covering-designs-record]]
- [[V3R1T4S]]
