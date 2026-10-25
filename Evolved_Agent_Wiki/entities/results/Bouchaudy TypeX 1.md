---
id: bouchaudy-typex-1
type: entity
tags: [v3r1t4s, ciphers, commit-only, quarry]
inbound_links: 1
confidence: 0.7
last_ingested_sources: ["~/v3r1t4s/proofer/picks/scout-ciphers-2026-10-18/SHA256SUMS"]
status: "watch"
priority: "1"
---
# Bouchaudy TypeX 1

# Overview

Charter v3 quarry 7 (2026-10-18). This is Problem 1 of J.-F. Bouchaudy's TypeX challenge, part of his Cipher Machines Challenge. The setter rates it "easy", but it has had **0 solvers since 2023-03-28**. According to the setter, the only obstacle is building a faithful simulator of the TypeX machine. Solved sibling Problem 2 can be used to validate one.

**COMMIT-ONLY:** the setter is alive, so keys, plaintext and leads exist only in `~/v3r1t4s/private/bouchaudy-typex-1/`, never in this vault. A result leaves the machine only as a salted commitment in a PR, and the human emails the solution to the setter.

- How it was chosen: a 22-page scout of the challenge series. The tug gate deadlocked (every turn refused by the API filter, X7), so per §13.3 the commander decided by BRAIN index.
- Bet P0032: p = 0.35 for CONFIRMED_SOLUTION by 2026-10-25.

## Citations
- Setter's page: http://www.jfbouch.fr/crypto/challenges/TYPEX/index.html (fetched 2026-10-17T23:51Z, HTTP 200)

## Related Nodes
- [[V3R1T4S]] · [[BRAIN]]
