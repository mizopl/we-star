---
id: result-c-68-14-5
type: synthesis
tags: [v3r1t4s, result, CONFIRMED_SOLUTION, covering-designs]
inbound_links: 2
confidence: 0.99
last_ingested_sources: ["~/v3r1t4s/runs/2026-10-18-0304/panel/cell_68_14_5/gate.md", "~/v3r1t4s/outbox/2026-10-18-mizopl-2b72790b/INDEX.csv"]
---
# C(68,14,5) result

# Overview

**`C(68,14,5) <= 15,675`** is an explicit $(68,14,5)$ covering design (`sha256 2b72790b8149daebd293b91cddae0105bc2a19b798b414d405e66f81828bcf07`, `632,514` bytes) with `15,675` distinct 14-element blocks over `{1..68}` covering all $\binom{68}{5} = 10,424,128$ 5-subsets of a 68-set (`uncovered = 0`), strictly improving on the live Covering Repository record (`16,004` at `2026-10-18T10:33:16Z`, by `329` blocks) and the La Jolla Covering Repository record (`16,004`, by `329` blocks).

- **Status:** `CONFIRMED_SOLUTION` (second panelled cell from run `2026-10-18-0304` on `covering-designs-record`). Three fresh-context Antigravity skeptics passed (`REPRODUCE`, `NOVELTY`, `CRITERION` in `runs/2026-10-18-0304/panel/cell_68_14_5/`), the honesty gate passed, and `check_run.py --package` printed `CHECK_RUN: PASS`.
- **Method:** Nested staircase combining construction ($68 = 36 + 32$, $S_0 \subset S_1 \subset S_2 \subset S_3$ with sizes $4, 7, 10, 14$ on the left and complementary $10, 7, 4, 0$ on the right) built from on-disk LJCR $v \in \{32,36\}$ ingredient designs (`15,688` unique blocks from `15,693` generated), followed by conservative greedy redundant-block pruning (`prune.c`, seed `1`), removing `13` redundant blocks to reach `15,675` blocks.
- **1-Minimality:** Verified by the `CRITERION` skeptic to have `0` redundant blocks (`redundant_blocks = 0`): every block uniquely covers between `6` and `337` 5-subsets (total uniquely covered 5-subsets = `1,259,808`).
- **Outward:** Submitted on 2026-10-18 on the human's explicit `"yes"` as **draft PR [elder-plinius/V3R1T4S#398](https://github.com/elder-plinius/V3R1T4S/pull/398)**, credit `mizopl` (package `2026-10-18-mizopl-2b72790b`, branch `mizopl:claim/2026-10-18-mizopl-2b72790b`, commit `aaaab57`).

## Citations
- Gate and panel: `~/v3r1t4s/runs/2026-10-18-0304/panel/cell_68_14_5/`
- Package: `~/v3r1t4s/outbox/2026-10-18-mizopl-2b72790b/`
- Bank definition: [targets.json](../../.raw/V3R1T4S/bank/targets.json) (id `covering-designs-record`)

## Related Nodes
- [[covering-designs-record]]
- [[C(94,13,5) result]]
- [[V3R1T4S]]
