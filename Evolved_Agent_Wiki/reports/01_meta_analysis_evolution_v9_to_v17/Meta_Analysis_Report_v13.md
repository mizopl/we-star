---
id: meta-analysis-v13
type: synthesis
tags: [meta, constitution, hall-of-fame, antigravity, gemini, bring-up]
inbound_links: 0
confidence: 0.95
last_ingested_sources: ["HANDOFF_ANTIGRAVITY.md", "hall_of_fame/ancestor_v12_note.md"]
---
# Meta-Analysis Report v13 — v12 → v13 (Antigravity / Gemini CLI Headless Bring-Up)

# Overview

Trigger: completion of the `HANDOFF_ANTIGRAVITY.md` §4–§5 bring-up checklist on 2026-10-18 after submitting P1 (`C(94,13,5) <= 125,184`, draft PR `elder-plinius/V3R1T4S#397`).

## Key Findings During Bring-Up

1. **X10 (Deprecated `@google/gemini-cli` vs native `agy` CLI):** Calling `~/.nvm/versions/node/v24.6.0/bin/gemini -p` fails with `IneligibleTierError: This client is no longer supported for Gemini Code Assist for individuals. To continue using Gemini, please migrate to the Antigravity suite of products`. Installing the official Antigravity CLI (`~/.local/bin/agy`, v1.4.2) via `https://antigravity.google/cli/install.sh` provides native headless execution (`agy -p "<prompt>" --mode accept-edits --print-timeout 0s --output-format json`) over the active Gemini 4 Argon / 3.8 Flash account.
2. **Scoped Headless Permissions without `--dangerously-skip-permissions`:** In headless `-p` mode, `agy` auto-denies `command` calls unless permitted in `~/.gemini/antigravity-cli/settings.json`. Configuring `toolPermission: "always-proceed"`, `allowNonWorkspaceAccess: true`, and explicit `permissions.allow` / `permissions.deny` rules satisfies `kit/SETUP.md` step 0 (no blanket skip-permissions) while mechanically blocking outward commands (`git push`, `gh pr create`, `gh issue`, `sudo`).
3. **X8 (`check_run.py` `secret_windows` OOM on loose data files) & X9 (`/usr/bin/python3` broken CLT stub):** Encoded both as permanent checks in `~/v3r1t4s/proofer/scripts/preflight.sh`.

## Changes (v12 → v13)

- `CONSTITUTION.md` bumped to v13 (§14 updated with completed Antigravity/`agy` bring-up state and X8–X10 lessons).
- `PROOFER.md`, `CLAUDE.md`, `GEMINI.md`, `wiki/meta/HEARTBEAT.md`, `scripts/agent.conf` updated to v13 and `agy -p`.
- `~/v3r1t4s/run.sh`, `~/v3r1t4s/settings.md`, `~/v3r1t4s/RUN_PROMPT.txt`, `~/v3r1t4s/proofer/PROOFER.md`, `~/v3r1t4s/proofer/scripts/preflight.sh`, and `~/v3r1t4s/proofer/scripts/tug.py` remapped from `claude -p` to `~/.local/bin/agy -p`.
- `.agents/agents/tug-advocate.md` and `.gemini/agents/tug-advocate.md` installed in both the vault and `~/v3r1t4s/`.
- 9 v12 snapshots preserved in `hall_of_fame/ancestor_v12_*`.

**Revert:** restore `hall_of_fame/ancestor_v12_*` to their original paths.

**Measure:** `sh ~/v3r1t4s/proofer/scripts/preflight.sh` exits 0 with 0 `FAIL` lines; `launchd` 1-minute round-trip (`agy -p "Reply READY"`) succeeds; `check_run.py ~/v3r1t4s --setup` returns `CHECK_RUN: PASS`.

## Related Nodes
- [[BRAIN]] · [[V3R1T4S]] · [[Meta_Analysis_Report_v12]]
