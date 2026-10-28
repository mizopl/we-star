#!/bin/sh
# V3R1T4S scheduled run (PROOFER shell v9.1).
#   run.sh          normal run (cron 03:41)
#   run.sh dry      dry run (kit steps 0-3)
#   run.sh resume   only if a previous run hit a usage limit (cron every 20 min); max 8 resumes per day
W="$HOME/v3r1t4s"
# Headless runs must not drop subagents when the main turn ends (they were killed after 10 min on 2026-10-17).
CLAUDE_CODE_PRINT_BG_WAIT_CEILING_MS=0; export CLAUDE_CODE_PRINT_BG_WAIT_CEILING_MS
PATH="$HOME/.local/bin:/opt/homebrew/bin:/usr/local/bin:/usr/bin:/bin:$PATH"; export PATH
cd "$W" || exit 1
# Scheduler is launchd (com.proofer.v3r1t4s.*): cron has no keychain login ("Not logged in", 2026-10-17).
# A leftover cron entry must not consume RESUME or the lock.
[ "$(ps -o comm= -p $PPID 2>/dev/null | sed 's|.*/||')" = cron ] && exit 0
[ -f "$W/PAUSE" ] && exit 0
if [ "$1" = resume ]; then
  [ -f "$W/RESUME" ] || exit 0
  # Do not burn a resume attempt before the announced limit reset.
  [ -f "$W/RESUME_AFTER" ] && [ "$(date +%s)" -lt "$(cat "$W/RESUME_AFTER")" ] && exit 0
  N=$(cat "$W/.resumes-$(date +%Y-%m-%d)" 2>/dev/null || echo 0)
  [ "$N" -ge 8 ] && exit 0
fi
mkdir "$W/.lock" 2>/dev/null || exit 0          # a run is already going
mkdir -p "$W/logs"
L="$W/logs/$(date +%Y-%m-%d).log"
MON="$HOME/Desktop/PROOFER/scripts/monitor.py"
# Live monitor while the agent works; this loop's PID is ours and is stopped by exact PID below.
( while :; do python3 "$MON" >/dev/null 2>&1; sleep 120; done ) &
TICK=$!
trap 'kill $TICK 2>/dev/null; rmdir "$W/.lock"' EXIT
P="V3R1T4S scheduled run: read $W/RUN_PROMPT.txt and follow it exactly."
[ "$1" = dry ] && P="DRY RUN. $P"
if [ "$1" = resume ]; then
  rm -f "$W/RESUME" "$W/RESUME_AFTER"; echo $((N + 1)) > "$W/.resumes-$(date +%Y-%m-%d)"
  P="$P This run resumes work cut off by a usage limit: start from the dossiers' live leads and the reasoning graph."
fi
echo "=== $(date -u +%Y-%m-%dT%H:%M:%SZ) start ${1:-run}" >> "$L"
START=$(( $(wc -l < "$L" | tr -d ' ') + 1 ))
# Prompt first: --allowedTools is variadic and would swallow a trailing prompt.
nice -n 10 "$HOME/.local/bin/claude" -p "$P" --permission-mode acceptEdits \
  --allowedTools "Bash Read Write Edit Glob Grep Agent WebFetch WebSearch TodoWrite" >> "$L" 2>&1
RC=$?
echo "=== $(date -u +%Y-%m-%dT%H:%M:%SZ) end rc=$RC" >> "$L"
# Usage / rate limit hit? Leave a RESUME marker; the 20-min cron entry picks it up after the reset.
if tail -n +"$START" "$L" | grep -qiE 'usage limit|limit reached|rate limit|resets (at )?[0-9]|overloaded'; then
  date -u +%Y-%m-%dT%H:%M:%SZ > "$W/RESUME"
  # "resets 7pm" / "resets 12am" (local) -> epoch of the next such time, plus 3 min slack.
  tail -n +"$START" "$L" | grep -oiE 'resets [0-9]{1,2}(:[0-9]{2})? ?[ap]m' | tail -1 | python3 -c '
import sys, re, datetime as d
m = re.search(r"(\d{1,2})(?::(\d{2}))? ?([ap]m)", sys.stdin.read().lower())
if m:
    h = int(m.group(1)) % 12 + (12 if m.group(3) == "pm" else 0)
    now = d.datetime.now(); t = now.replace(hour=h, minute=int(m.group(2) or 0), second=0, microsecond=0)
    if t <= now: t += d.timedelta(days=1)
    print(int(t.timestamp()) + 180)
' > "$W/RESUME_AFTER.tmp" && [ -s "$W/RESUME_AFTER.tmp" ] && mv "$W/RESUME_AFTER.tmp" "$W/RESUME_AFTER" || rm -f "$W/RESUME_AFTER.tmp"
  echo "=== limit detected -> RESUME queued" >> "$L"
  osascript -e 'display notification "Limit hit - resume queued" with title "PROOFER"' 2>/dev/null
else
  osascript -e 'display notification "Run finished - see MONITOR" with title "PROOFER"' 2>/dev/null
fi
# Mirror into the PROOFER wiki (Desktop). Under cron this needs Full Disk Access for /usr/sbin/cron;
# if it fails, the next interactive "Run OS" mirrors instead.
python3 "$HOME/Desktop/PROOFER/scripts/pull_lab.py" >> "$L" 2>&1 || echo "pull_lab failed (TCC?)" >> "$L"
