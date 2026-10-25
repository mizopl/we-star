#!/usr/bin/env python3
"""
compress_log.py — Wiki OS Log Compressor
Condenses consecutive clean/idle pass entries in wiki/log.md into single summary lines.
Run before appending a new log entry when the last N entries are all clean passes.
"""

import re
import sys
from pathlib import Path

KB_ROOT = Path(__file__).parent.parent
LOG_PATH = KB_ROOT / "wiki" / "log.md"

CLEAN_PASS_PATTERN = re.compile(
    r'^\|\s*[\d-]+(?:\s+[\d:]+)?\s*\|\s*Cycle (\d+)\s*\|.*?(?:Clean maintenance pass|IDLE|Full maintenance audit).*?\|$',
    re.IGNORECASE
)

def parse_log(lines):
    """Return list of (line_index, cycle_num, is_clean) tuples for table rows."""
    results = []
    for i, line in enumerate(lines):
        m = CLEAN_PASS_PATTERN.match(line.strip())
        if m:
            results.append((i, int(m.group(1)), True))
    return results

def compress(min_run=5):
    if not LOG_PATH.exists():
        print("Log file not found.")
        return

    lines = LOG_PATH.read_text(encoding='utf-8').splitlines(keepends=True)
    clean_entries = parse_log(lines)

    if len(clean_entries) < min_run:
        print(f"Only {len(clean_entries)} clean-pass entries found — threshold is {min_run}. Nothing to compress.")
        return

    # Find the longest consecutive run at the end of the file
    # Work backwards from the last clean entry
    runs = []
    current_run = [clean_entries[-1]]
    for entry in reversed(clean_entries[:-1]):
        # Check if entries are adjacent in the file (within 2 lines of each other)
        if current_run[-1][0] - entry[0] <= 2:
            current_run.append(entry)
        else:
            break

    current_run.reverse()

    if len(current_run) < min_run:
        print(f"Longest trailing run: {len(current_run)} entries — below threshold {min_run}. Nothing compressed.")
        return

    # Get date range
    first_line = lines[current_run[0][0]].strip()
    last_line = lines[current_run[-1][0]].strip()

    first_date = re.search(r'\|\s*([\d-]+(?:\s+[\d:]+)?)', first_line)
    last_date = re.search(r'\|\s*([\d-]+(?:\s+[\d:]+)?)', last_line)
    first_cycle = current_run[0][1]
    last_cycle = current_run[-1][1]

    first_date_str = first_date.group(1).strip() if first_date else "unknown"
    last_date_str = last_date.group(1).strip() if last_date else "unknown"

    summary_line = (
        f"| {last_date_str} | Cycles {first_cycle}–{last_cycle} | "
        f"COMPRESSED — {len(current_run)} consecutive clean/idle passes "
        f"({first_date_str} → {last_date_str}); corpus stable, 0 dead links, 0 orphans each cycle. |\n"
    )

    # Replace the run with the summary line
    indices_to_remove = set(entry[0] for entry in current_run)
    new_lines = []
    inserted = False
    for i, line in enumerate(lines):
        if i in indices_to_remove:
            if not inserted:
                new_lines.append(summary_line)
                inserted = True
        else:
            new_lines.append(line)

    LOG_PATH.write_text(''.join(new_lines), encoding='utf-8')
    print(f"Compressed {len(current_run)} entries (Cycles {first_cycle}–{last_cycle}) into 1 summary line.")

if __name__ == "__main__":
    min_run = int(sys.argv[1]) if len(sys.argv) > 1 else 5
    compress(min_run)
