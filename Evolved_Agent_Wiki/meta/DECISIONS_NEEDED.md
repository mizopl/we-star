# DECISIONS NEEDED

> **For the human operator(s).** This file is maintained by the Librarian Agent.
> Items here have been open too long to stay buried in the agent's internal hot cache.
> Each item needs a human decision. Once decided, reply in chat — the agent will mark it resolved.

*Last updated: — (fresh instance, no items yet)*

---

## 🔴 CRITICAL

_(none yet)_

## 🟠 IMPORTANT

_(none yet)_

## 🟡 MINOR

_(none yet)_

---

### Format reference (see CONSTITUTION.md §5)

```
**[OPEN/RESOLVED]** Title
- **First flagged:** Cycle N
- **Issue:** description
- **Action needed:** recommended resolution
```

Any contradiction open for >30 cycles must be promoted here automatically.
Entries are never deleted — only marked `[RESOLVED: YYYY-MM-DD]`.

**[OPEN]** | Cycle 3 | V3R1T4S bank criterion for `square-grid-lattice-gas-exact-counts-oeis` requires a(N)^(1/N²) within 1e-3 of the entropy constant; dry run measured a 5e-3 gap for open-board A006506 at n=39 (HEURISTIC), so a correct new A006506/A028420 term could fail it literally. Torus sequences (A054759, A027683) unaffected. | Decide whether to raise it upstream (human-only outward action); meanwhile the hunt targets partial p1 (torus) first.
**[RESOLVED: 2026-10-17]** (moved to launchd; Desktop mirror works) | Cycle 3 | Grant Full Disk Access to `/usr/sbin/cron` so nightly runs can mirror into this Desktop wiki. | System Settings → Privacy & Security → Full Disk Access → + `/usr/sbin/cron`.
**[RESOLVED: 2026-10-18]** draft PR https://github.com/elder-plinius/V3R1T4S/pull/366 (by mizopl) | Cycle 4 | First CONFIRMED_PARTIAL: A054759(15) packaged in `~/v3r1t4s/outbox/2026-10-17-anonymous-8ee58c17-fd616054/`. | Say "submit 2026-10-17-anonymous-8ee58c17-fd616054" for a draft PR to V3R1T4S (then an explicit "yes"); an OEIS b-file extension is yours to send by hand. Optionally change the credit name from `anonymous-8ee58c17`.
**[RESOLVED: 2026-10-18]** human ran crontab -r | Cycle 4 | The crontab still holds 2 V3R1T4S lines; macOS blocks `crontab` edits from the agent (probably a permission dialog). They are harmless (run.sh exits when called by cron). | Run `crontab -r` in your own terminal (the crontab holds only these 2 lines). The scheduler is now launchd.
**[OPEN]** | Cycle 5 | V3R1T4S kit update `04fdfba` is available: check_run.py is stricter on short private files (+ a test). No rule is loosened and no outward action is added. | Say "update V3R1T4S to 04fdfba48c6e277fe083b6811f1a5deb3c52b74e" to adopt it; the repo stays pinned until then.
