#!/bin/sh
# PROOFER preflight (CONSTITUTION v10 §12, K4): every infrastructure dead end in the reasoning graph
# becomes a check here. Run by run.sh before the agent starts; output goes to logs/preflight.txt,
# and the run must read it. Exit 1 = do not start the agent (blocking); WARN lines do not block.
W="$HOME/v3r1t4s"; FAIL=0
ok()   { echo "ok:   $*"; }
warn() { echo "WARN: $*"; }
fail() { echo "FAIL: $*"; FAIL=1; }

# X1: headless runs must not drop background subagents
[ "$CLAUDE_CODE_PRINT_BG_WAIT_CEILING_MS" = 0 ] && ok "X1 bg-wait ceiling disabled" || fail "X1 CLAUDE_CODE_PRINT_BG_WAIT_CEILING_MS is not 0"
# X2: cron cannot log in; the scheduler must be launchd
[ "$(ps -o comm= -p $PPID 2>/dev/null | sed 's|.*/||')" = cron ] && fail "X2 started by cron (no keychain)" || ok "X2 not started by cron"
launchctl list 2>/dev/null | grep -q com.proofer.v3r1t4s.jobs && ok "K2 job ticker loaded" || warn "K2 job ticker (com.proofer.v3r1t4s.jobs) not loaded"
# X3: never resume before the announced reset
if [ -f "$W/RESUME_AFTER" ] && [ "$(date +%s)" -lt "$(cat "$W/RESUME_AFTER")" ]; then fail "X3 before limit reset ($(date -r "$(cat "$W/RESUME_AFTER")"))"; else ok "X3 no pending limit reset"; fi
# Disk (kit preflight) and memory (H1708A swap thrash)
FREE_GB=$(df -g "$HOME" | awk 'NR==2{print $4}')
[ "$FREE_GB" -ge 10 ] && ok "disk ${FREE_GB} GB free" || fail "disk ${FREE_GB} GB free (< 10 GB)"
MEMFREE=$(memory_pressure -Q 2>/dev/null | sed -n 's/.*free percentage: \([0-9]*\)%.*/\1/p')
[ "${MEMFREE:-100}" -ge 15 ] && ok "memory free ${MEMFREE}%" || warn "memory free ${MEMFREE}%: start no new heavy compute (H1708A)"
# F22 + K2: compute already in flight (never start a duplicate on the same result folder)
RUNNING=$(grep -lxE 'running|adopted' "$W"/jobs/*/state 2>/dev/null | wc -l | tr -d ' ')
echo "info: $RUNNING compute job(s) running or adopted in jobs/; harvest them, never duplicate them"
for s in "$W"/jobs/*/state; do [ -f "$s" ] && echo "info:   $(basename "$(dirname "$s")"): $(cat "$s")"; done
# X4: every queued job must have an existing cwd (relative paths broke the ticker, which starts in "/")
for sp in "$W"/jobs/*/spec.json; do
  [ -f "$sp" ] || continue
  c=$(python3 -c "import json,sys,os;c=json.load(open(sys.argv[1]))['cwd'];print(c if os.path.isabs(c) else os.path.join(sys.argv[2],c))" "$sp" "$W")
  [ -d "$c" ] || warn "X4 job $(basename "$(dirname "$sp")") cwd missing: $c"
done
# X6: private/ holds only secrets; outbox/ holds only package folders (check_run rules)
ls "$W"/outbox 2>/dev/null | while read f; do [ -d "$W/outbox/$f" ] || echo "WARN: X6 non-folder in outbox/: $f (move to archive/)"; done
[ -d "$W/private/superseded-packages" ] && echo "WARN: X6 superseded packages inside private/ (move to archive/)"
# No timeout(1) on this Mac (lesson from run 1225)
command -v timeout >/dev/null && ok "timeout available" || echo "info: no timeout(1); use jobs.py caps or Python signal.alarm"
exit $FAIL
