# Hall of Fame: Ancestor v12 — Model-Agnostic Handoff Bridge (Retired 2026-10-18)

## Summary

Version 12 was the transitional handoff constitution created on 2026-10-18 when the human moved PROOFER and V3R1T4S from Claude Code (`claude -p`) to Google Antigravity (`agy -p`, Gemini). Under v12, Antigravity completed Priority 1 from `HANDOFF_ANTIGRAVITY.md` (paneling, gating, packaging, and submitting `C(94,13,5) <= 125,184` as draft PR `elder-plinius/V3R1T4S#397`, plus fixing `check_run.py` OOM dead end X8 by archiving 4,338 loose `.txt` files in `runs/2026-10-18-0304/data/ljcr_designs/` into `designs.tar.gz`) before executing the §4–§5 bring-up checklist to retire all remaining Claude-specific harness couplings in v13.

## Snapshots Preserved

- `ancestor_v12_CONSTITUTION_snapshot.md`
- `ancestor_v12_CLAUDE_snapshot.md`
- `ancestor_v12_GEMINI_snapshot.md`
- `ancestor_v12_PROOFER_snapshot.md`
- `ancestor_v12_HEARTBEAT_snapshot.md`
- `ancestor_v12_RUN_PROMPT_snapshot.txt`
- `ancestor_v12_run_sh_snapshot.sh`
- `ancestor_v12_preflight_sh_snapshot.sh`
- `ancestor_v12_tug_py_snapshot.py`

## Why Retired (v12 → v13)

- **Headless CLI remapped from `claude -p` to `agy -p` (`~/.local/bin/agy`, v1.4.2):** Note that legacy `@google/gemini-cli` (`gemini`) returns `IneligibleTierError` for individual accounts and instructs migrating to `agy`. Installed `~/.local/bin/agy` v1.4.2 and configured `~/.gemini/antigravity-cli/settings.json` with scoped `permissions.allow` and `permissions.deny` (`git push`, `gh pr create`, `sudo` mechanically denied; no `--dangerously-skip-permissions`).
- **`run.sh` and `settings.md` updated to v13 (`agy -p`):** Uses `--mode accept-edits --print-timeout 0s --add-dir "$W" --add-dir "$HOME/Desktop/PROOFER"` and expanded usage/quota regex (`usage limit|limit reached|rate limit|quota|resource_exhausted|429|resets (at )?[0-9]|overloaded`).
- **`preflight.sh` updated (X1, X8, X9):** X1 checks both `AGY_PRINT_TIMEOUT=0s` (or `CLAUDE_CODE_PRINT_BG_WAIT_CEILING_MS=0`) and executable `~/.local/bin/agy`; X8 warns if any `runs/*/data/` has > 500 loose files (`check_run.py` `secret_windows` OOM guard); X9 verifies `/opt/homebrew/bin/python3` comes before broken `/usr/bin/python3` on `PATH`.
- **`tug.py` and `tug-advocate.md` remapped:** Placed `tug-advocate.md` in `.agents/agents/tug-advocate.md` and `.gemini/agents/tug-advocate.md` (both vault and lab); updated `tug.py` `call()` to invoke `agy --agent tug-advocate --disable-slash-commands -p <prompt> --output-format json` and parse `out["response"]` / `out["status"] == "SUCCESS"` (retaining backward compatibility with `out["result"]`).
