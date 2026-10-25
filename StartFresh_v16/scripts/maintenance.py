#!/usr/bin/env python3
"""
Wiki OS Autonomous Maintenance Script
Runs graph health checks without Claude/Gemini CLI — standalone diagnostic tool.
Called by cron or manually: python3 scripts/maintenance.py
"""
import re, json, sys
from pathlib import Path
from datetime import datetime

KB = Path(__file__).parent.parent
ENTITIES = KB / "wiki" / "entities"
REPORTS  = KB / "wiki" / "reports"
RAW      = KB / ".raw"
JOBS_PENDING   = KB / ".jobs" / "pending"
JOBS_COMPLETED = KB / ".jobs" / "completed"

def check_graph():
    files = list(ENTITIES.glob("*.md"))
    inbound = {f.stem: 0 for f in files}
    for f in files:
        for link in re.findall(r'\[\[([^\]]+)\]\]', f.read_text()):
            link = link.strip()
            if link in inbound and link != f.stem:
                inbound[link] += 1

    orphans = [n for n, c in inbound.items() if c == 0]
    hubs    = sorted(inbound.items(), key=lambda x: x[1], reverse=True)[:5]
    return orphans, hubs, len(files)

def check_raw():
    # Find files not yet referenced in any wiki entity
    ingested = set()
    for f in ENTITIES.glob("*.md"):
        ingested.update(re.findall(r'last_ingested_sources.*?\[([^\]]+)\]', f.read_text()))
    raw_files = [f for f in RAW.rglob("*") if f.is_file() and f.suffix in ('.txt','.pdf','.docx','.md')]
    return raw_files

def check_jobs():
    pending = list(JOBS_PENDING.glob("*.json")) if JOBS_PENDING.exists() else []
    return pending

def main():
    print(f"\n{'='*50}")
    print(f"Wiki OS Maintenance — {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    print(f"{'='*50}")

    orphans, hubs, total = check_graph()
    print(f"\n📊 Graph: {total} nodes")
    print(f"   Top hubs: {', '.join(f'{n}({c})' for n,c in hubs)}")
    if orphans:
        print(f"   ⚠️  Orphans: {', '.join(orphans)}")
    else:
        print(f"   ✅ Zero orphans")

    raw = check_raw()
    print(f"\n📁 Raw: {len(raw)} text/document files in .raw/")

    jobs = check_jobs()
    if jobs:
        print(f"\n📋 Jobs pending: {len(jobs)} — {[j.name for j in jobs]}")
    else:
        print(f"\n📋 Jobs: none pending")

    print(f"\n{'='*50}\n")

if __name__ == "__main__":
    main()
