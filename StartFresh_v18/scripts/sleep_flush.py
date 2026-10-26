#!/usr/bin/env python3
"""Sleep & Memory-Flush Consolidation Daemon (K16 / H-EVO-01 / H-EVO-06).

Performs append-only synaptic consolidation across `graphs/*.jsonl`:
  1. Stitch Orphan Causal Edges (`H-EVO-01`):
     Connects sequential unlinked hypothesis/experiment/result nodes (`derives`
     after closed/open nodes, `resumes` after `kill` nodes) so every reasoning
     graph has a connected causal tree (`0` orphan nodes).
  2. Close Superseded Open Nodes on Completed Targets (`K16` / `M6` / `H-EVO-06`):
     Closes dangling `hypothesis` / `experiment` / `lead` nodes on targets that
     already have verified `closed` or `result` nodes (skipping `--active-target`
     if specified).
  3. Re-compiles Obsidian `.canvas` files for all updated graphs.

Usage:
  sleep_flush.py [--active-target <target>] [--dry-run]
"""
import argparse
import json
import os
import subprocess
import sys
from pathlib import Path

KB = Path(os.environ.get("PROOFER_HOME", Path(__file__).resolve().parent.parent))
GRAPHS = Path(os.environ.get("PROOFER_GRAPHS", KB / "graphs"))
RGRAPH = Path(__file__).resolve().parent / "rgraph.py"
PYTHON = sys.executable


def now():
    return subprocess.run(["date", "-u", "+%Y-%m-%dT%H:%MZ"], capture_output=True, text=True).stdout.strip()


def fold_file(p: Path):
    nodes, edges, order = {}, [], []
    for line in p.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        e = json.loads(line)
        k = e.get("ev")
        if k == "node":
            key = e["key"]
            if key not in nodes:
                order.append(key)
            nodes[key] = {**e, "dead": e.get("type") == "dead", "why": "", "closed": ""}
        elif k == "edge":
            edges.append(e)
        elif k == "kill" and e.get("key") in nodes:
            nodes[e["key"]].update(dead=True, why=e.get("why", ""), killed=e.get("ts", ""))
        elif k == "close" and e.get("key") in nodes:
            nodes[e["key"]]["closed"] = e.get("why", "closed")
        elif k == "revive" and e.get("key") in nodes:
            nodes[e["key"]].update(dead=False, why="revived: " + e.get("why", ""))
    return nodes, edges, order


def emit(p: Path, ev: dict, dry_run: bool):
    ev["ts"] = now()
    if not dry_run:
        with open(p, "a", encoding="utf-8") as f:
            f.write(json.dumps(ev, ensure_ascii=False) + "\n")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--active-target", default="", help="Do not auto-close open nodes on this active target")
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    stitched_edges = 0
    closed_nodes = 0
    touched_targets = set()

    for p in sorted(GRAPHS.glob("*.jsonl")):
        target = p.stem
        nodes, edges, order = fold_file(p)
        if not order:
            continue

        has_parent = {e["dst"] for e in edges if e.get("src") in nodes and e.get("dst") in nodes}
        existing_pairs = {(e["src"], e["dst"]) for e in edges}

        # 1. Stitch orphan sequential nodes (H-EVO-01)
        for idx in range(1, len(order)):
            cur_k = order[idx]
            prev_k = order[idx - 1]
            if cur_k not in has_parent and (prev_k, cur_k) not in existing_pairs:
                prev_n = nodes[prev_k]
                rel = "resumes" if prev_n["dead"] else "derives"
                emit(p, {"ev": "edge", "src": prev_k, "dst": cur_k, "rel": rel}, args.dry_run)
                has_parent.add(cur_k)
                existing_pairs.add((prev_k, cur_k))
                stitched_edges += 1
                touched_targets.add(target)

        # 2. Close dangling open hypothesis/experiment/lead nodes on completed targets (H-EVO-06)
        if target != args.active_target:
            has_completion = any(
                n["closed"] or n.get("type") == "result"
                for n in nodes.values()
            )
            if has_completion:
                for k in order:
                    n = nodes[k]
                    if n.get("type") in ("hypothesis", "experiment", "lead") and not n["dead"] and not n["closed"]:
                        emit(
                            p,
                            {
                                "ev": "close",
                                "key": k,
                                "why": "[sleep_flush K16/M6] Consolidated: target completed with verified certificate",
                            },
                            args.dry_run,
                        )
                        closed_nodes += 1
                        touched_targets.add(target)

    if not args.dry_run:
        for t in sorted(touched_targets):
            cpath = GRAPHS / f"{t}.canvas"
            subprocess.run([PYTHON, str(RGRAPH), "canvas", t, str(cpath)], capture_output=True, text=True)

    # 3. Binary PDF Pre-Read & Token-Ceiling Guard (Dead-End Guard X14 / H-EVO-06)
    runs_dir = KB.parent / "runs"
    extracted_pdfs = 0
    if runs_dir.exists():
        for pdf in sorted(runs_dir.rglob("*.pdf")):
            if pdf.stat().st_size < 100_000:
                continue
            txt_path = pdf.with_suffix(".txt")
            if not txt_path.exists() or txt_path.stat().st_size == 0:
                if not args.dry_run:
                    try:
                        from pypdf import PdfReader
                        reader = PdfReader(str(pdf))
                        pages = []
                        for idx, page in enumerate(reader.pages, start=1):
                            pages.append(f"=== PAGE {idx} / {len(reader.pages)} ({pdf.name}) ===\n" + (page.extract_text() or ""))
                        txt_path.write_text("\n\n".join(pages), encoding="utf-8")
                        extracted_pdfs += 1
                    except Exception:
                        pass
                else:
                    extracted_pdfs += 1

    mode = "DRY-RUN" if args.dry_run else "APPLIED"
    print(
        f"=== [SLEEP & MEMORY-FLUSH ({mode})] ===\n"
        f"  Targets updated       : {len(touched_targets)}\n"
        f"  Causal edges stitched : +{stitched_edges} (H-EVO-01 / H-EVO-02)\n"
        f"  Dangling nodes closed : +{closed_nodes} (K16 / M6)\n"
        f"  Large PDFs guarded    : +{extracted_pdfs} (Dead-End X14 / H-EVO-06)"
    )


if __name__ == "__main__":
    main()
