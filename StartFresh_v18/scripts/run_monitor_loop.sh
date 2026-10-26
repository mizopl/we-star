#!/usr/bin/env sh
# PROOFER StartFresh_v18 — Autonomous MONITOR Loop for Claude Code & Antigravity
# Usage:
#   sh scripts/run_monitor_loop.sh [INTERVAL_SECONDS] [MODEL]
# Examples:
#   sh scripts/run_monitor_loop.sh 600 haiku     # Fast & joyful Haiku heartbeat every 10 minutes!
#   sh scripts/run_monitor_loop.sh 900 sonnet    # Sonnet heartbeat every 15 minutes
#   sh scripts/run_monitor_loop.sh 2700 agy      # Antigravity 45-minute heartbeat

set -eu

INTERVAL="${1:-600}"
MODEL="${2:-haiku}"

ROOT_DIR="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT_DIR"

export PATH="/opt/homebrew/bin:/usr/local/bin:$HOME/.local/bin:$PATH"

echo "================================================================"
echo "🛰️  PROOFER v18 — AUTONOMOUS MONITOR DAEMON (StartFresh_v18)"
echo "📂 Workspace : $ROOT_DIR"
echo "⏱️  Interval  : ${INTERVAL}s"
echo "🤖 Model     : $MODEL"
echo "📬 Mailbox   : wiki/meta/AUDITOR_INBOX.md"
echo "================================================================"

HB_COUNT=1
while true; do
    TS="$(date '+%Y-%m-%d %H:%M:%S')"
    echo ""
    echo "[$TS] 🔔 Starting HEARTBEAT #$HB_COUNT (model=$MODEL)..."

    PROMPT="MONITOR HEARTBEAT #$HB_COUNT: Read wiki/meta/HEARTBEAT.md, wiki/meta/hot.md, wiki/meta/AUDITOR_INBOX.md, and wiki/log.md (last 15 lines). Run 'python3 scripts/brain.py status', 'python3 scripts/rgraph.py show main', 'python3 scripts/micro_bet.py status', 'python3 scripts/postdict.py report', and 'python3 scripts/sleep_flush.py'. Audit the worker's current progress, check if any micro-bets or graph nodes are missing or if Law M1/M2/M6 requires a representation pivot, write clear and encouraging strategic coaching directives into wiki/meta/AUDITOR_INBOX.md (never overwrite the worker's active Python solver files!), and append a 1-line summary to wiki/meta/heartbeat.log."

    if [ "$MODEL" = "agy" ]; then
        /Users/blister/.local/bin/agy -p "$PROMPT" || echo "⚠️ agy heartbeat exited with non-zero code"
    else
        claude --model "$MODEL" -p "$PROMPT" || echo "⚠️ claude heartbeat exited with non-zero code"
    fi

    echo "[$(date '+%Y-%m-%d %H:%M:%S')] ✅ HEARTBEAT #$HB_COUNT complete. Sleeping ${INTERVAL}s..."
    HB_COUNT=$((HB_COUNT + 1))
    sleep "$INTERVAL"
done
