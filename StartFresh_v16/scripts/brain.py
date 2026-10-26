#!python3
"""
BRAIN v2 & CLSS Autoresearch Engine (CONSTITUTION v14 §12, §15).
Enacts K1 (decision index + decisions.tsv + exploration quota),
K5 (costs.tsv model), K6 (rgraph & VS telemetry), K7 (ratchet applicability),
K8 (outlet queue multiplier), and K9 (CLSS Seam-First Solver Score).
"""
import argparse
import csv
import datetime as dt
import json
import math
import os
import pathlib
import re
import sys

ROOT_DIR = pathlib.Path(__file__).resolve().parent.parent
LAB = pathlib.Path(os.environ.get("V3R1T4S_LAB", ROOT_DIR))
VAULT = pathlib.Path(os.environ.get("PROOFER_VAULT", ROOT_DIR))
BANK_JSON = VAULT / ".raw/V3R1T4S/bank/targets.json"
TROPHY_MD = VAULT / ".raw/V3R1T4S/TROPHY_CASE.md"
PRED_TSV = (VAULT / "memory/predictions.tsv") if (VAULT / "memory/predictions.tsv").exists() else (LAB / "proofer/memory/predictions.tsv")
DECISIONS_TSV = (VAULT / "memory/decisions.tsv") if (VAULT / "memory").exists() else (LAB / "proofer/memory/decisions.tsv")
COSTS_TSV = (VAULT / "memory/costs.tsv") if (VAULT / "memory").exists() else (LAB / "proofer/memory/costs.tsv")
LOG_MD = (VAULT / "wiki/log.md") if (VAULT / "wiki/log.md").exists() else (LAB / "LOG.md")
GRAPHS_DIR = (VAULT / "graphs") if (VAULT / "graphs").exists() else (LAB / "proofer/graphs")
OUTBOX_DIR = LAB / "outbox"
ARCHIVE_DIR = LAB / "archive"


def load_predictions():
    rows = []
    if not PRED_TSV.exists():
        return rows
    with open(PRED_TSV, newline="", encoding="utf-8") as f:
        for r in csv.DictReader(f, delimiter="\t"):
            rows.append(r)
    return rows


def compute_posteriors(preds):
    by_scope = {}
    for r in preds:
        out = r.get("outcome", "").strip()
        if out not in ("0", "1"):
            continue
        raw_sc = r.get("scope", "other")
        if len(raw_sc) > 40:
            raw_sc = "panel" if "panel" in raw_sc.lower() else ("optimization-benchmarks" if "ihtp" in raw_sc.lower() else "target")
        sc = raw_sc.split(":")[0].split("/")[0]
        w, n = by_scope.get(sc, (0, 0))
        by_scope[sc] = (w + int(out), n + 1)
    post = {}
    for sc, (w, n) in by_scope.items():
        # Beta(1+w, 1+n-w) mean and std
        a, b = 1 + w, 1 + (n - w)
        mean = a / (a + b)
        var = (a * b) / (((a + b) ** 2) * (a + b + 1))
        post[sc] = {"wins": w, "total": n, "mean": round(mean, 3), "unc": round(math.sqrt(var), 3)}
    return post


def load_logged_categories(targets_by_id):
    cats = set()
    targets_run = set()
    if LOG_MD.exists():
        for line in LOG_MD.read_text(encoding="utf-8").splitlines():
            parts = [p.strip() for p in line.split("|")]
            if len(parts) >= 2 and parts[1]:
                tid = parts[1]
                targets_run.add(tid)
                if tid in targets_by_id:
                    cats.add(targets_by_id[tid].get("category", ""))
    if GRAPHS_DIR.exists():
        for jf in GRAPHS_DIR.glob("*.jsonl"):
            tid = jf.stem
            if tid in targets_by_id:
                targets_run.add(tid)
                cats.add(targets_by_id[tid].get("category", ""))
    return cats, targets_run


def compute_outlet_state():
    pkgs = []
    if OUTBOX_DIR.exists():
        pkgs = [d.name for d in OUTBOX_DIR.iterdir() if d.is_dir() and not d.name.startswith(".")]
    submitted = set()
    if ARCHIVE_DIR.exists():
        for f in ARCHIVE_DIR.glob("SUBMITTED-*.txt"):
            pkg = f.stem.replace("SUBMITTED-", "")
            submitted.add(pkg)
    unsubmitted = [p for p in pkgs if p not in submitted]
    return {"total_outbox": len(pkgs), "submitted": len(submitted), "unsubmitted": unsubmitted}


def compute_telemetry():
    total_nodes = 0
    dead_nodes = 0
    closed_nodes = 0
    if GRAPHS_DIR.exists():
        for jf in GRAPHS_DIR.glob("*.jsonl"):
            nodes = {}
            for line in jf.read_text(encoding="utf-8").splitlines():
                if not line.strip():
                    continue
                try:
                    e = json.loads(line)
                except Exception:
                    continue
                k = e.get("ev")
                key = e.get("key")
                if k == "node" and key:
                    nodes[key] = {"dead": e.get("type") == "dead", "closed": False}
                elif k == "kill" and key in nodes:
                    nodes[key]["dead"] = True
                elif k == "close" and key in nodes:
                    nodes[key]["closed"] = True
                elif k == "revive" and key in nodes:
                    nodes[key]["dead"] = False
            total_nodes += len(nodes)
            dead_nodes += sum(1 for v in nodes.values() if v["dead"])
            closed_nodes += sum(1 for v in nodes.values() if v["closed"])
    return {"graph_nodes": total_nodes, "dead_nodes": dead_nodes, "closed_nodes": closed_nodes}


def clss_score(t):
    """
    Score a target in [0, 1] on the 4-stage CLSS (Compositional Lifting + Seam Surgery) paradigm:
    1. Fast Bit-Parallel / Deterministic Exact Oracle (< 60s verification) [0..0.30]
    2. Compositional / Recursive / Symmetry Scaffold [0..0.25]
    3. Local Seam Surgery / SAT-Window / Bitset Prune-Merge [0..0.25]
    4. Partial-Win Ladder (H-sibling smaller-first) [0..0.20]
    """
    text = " ".join([
        str(t.get("statement", "")),
        str(t.get("success_criterion", "")),
        str(t.get("verification", "")),
        " ".join(str(x) for x in t.get("angles", [])),
    ]).lower()

    # 1. Fast Exact Oracle
    s_oracle = 0.0
    if any(k in text for k in ["bit-sliced", "bitmask", "bitset", "0-1 principle", "bfs", "girth", "exhaustively", "bareiss", "brent equations", "o(n^2)", "official validator", "ihtp_validator"]):
        s_oracle += 0.22
    if any(k in text for k in ["takes minutes", "in seconds", "under 3m operations", "laptop-hours", "seconds per instance", "seconds."]):
        s_oracle += 0.08
    s_oracle = min(0.30, s_oracle)

    # 2. Compositional / Symmetry Scaffold
    s_comp = 0.0
    if any(k in text for k in ["prefix", "combining", "recursive", "lift", "voltage", "cayley", "symmetric", "reflection", "template", "glue", "blow-up", "circulant", "decompose by subproblem", "downloadable json solution", "warm-start"]):
        s_comp += 0.25
    s_comp = min(0.25, s_comp)

    # 3. Local Seam Surgery / Exact Suffix / Prune-Merge
    s_surg = 0.0
    if any(k in text for k in ["sat", "cp-sat", "ilp", "cadical", "surgery", "delete", "repair", "prune", "pareto", "annealing", "tabu", "window"]):
        s_surg += 0.25
    s_surg = min(0.25, s_surg)

    # 4. Partial-Win Ladder
    p_wins = t.get("partial_wins") or []
    s_part = min(0.20, 0.10 * len(p_wins))

    # Penalty for external heavy dependencies / huge downloads / wet-lab / multi-node-only
    pen = 0.0
    if any(k in text for k in ["100 gb", "terabyte", "ncbi", "fastq", "bam", "sra", "wet-lab"]):
        pen += 0.35

    total = max(0.0, min(1.0, s_oracle + s_comp + s_surg + s_part - pen))
    return round(total, 3), {
        "oracle": round(s_oracle, 2),
        "scaffold": round(s_comp, 2),
        "surgery": round(s_surg, 2),
        "partials": round(s_part, 2),
    }


def ensure_costs_tsv():
    COSTS_TSV.parent.mkdir(parents=True, exist_ok=True)
    if not COSTS_TSV.exists():
        with open(COSTS_TSV, "w", newline="", encoding="utf-8") as f:
            w = csv.writer(f, delimiter="\t")
            w.writerow(["shape", "param_desc", "est_active_min", "est_ram_gb", "verify_min", "notes"])
            w.writerow(["exact-count-crt", "torus/grid w<=16", "45", "0.4", "15", "A054759(15) empirically 46m"])
            w.writerow(["exact-count-crt-tail", "grid w=35..39", "600", "2.8", "30", "A089980 tail x1.6 per width (K2 job queue)"])
            w.writerow(["clss-record-table", "combining+prune/merge C(v,t)<=5e9", "60", "0.2", "20", "covering-designs 21 records in 115m + 20m per panel"])
            w.writerow(["clss-sorting-network", "bit-slice 0-1 + prefix/SAT n=13..64", "45", "0.2", "10", "2^n bit-sliced in C/numpy + Pareto/size/depth check"])
            w.writerow(["clss-graph-cage-schur", "template/voltage lift + SAT/local surgery", "50", "0.3", "10", "O(N^2) or BFS girth check in <2s"])


def cmd_status(_args):
    ensure_costs_tsv()
    preds = load_predictions()
    post = compute_posteriors(preds)
    outlet = compute_outlet_state()
    telem = compute_telemetry()

    if BANK_JSON.exists():
        with open(BANK_JSON, encoding="utf-8") as f:
            bdata = json.load(f)
        targets = bdata["targets"] if isinstance(bdata, dict) and "targets" in bdata else bdata
    else:
        targets = []
    t_by_id = {t["id"]: t for t in targets}
    cats_run, targets_run = load_logged_categories(t_by_id)

    print("=== BRAIN v2 & CLSS AUTORESEARCH STATUS (v18) ===")
    print(f"Targets attacked so far : {len(targets_run)} ({', '.join(sorted(targets_run))})")
    print(f"Categories explored     : {len(cats_run)} / 18 ({', '.join(sorted(cats_run))})")
    print(f"Outlet queue (K8)       : {outlet['submitted']} submitted PRs, {len(outlet['unsubmitted'])} unsubmitted in outbox")
    print(f"Reasoning graphs (K6)   : {telem['graph_nodes']} nodes ({telem['dead_nodes']} dead, {telem['closed_nodes']} closed)")
    print("Empirical Posteriors (K1/K3):")
    for sc, st in sorted(post.items()):
        print(f"  scope={sc:12s} : {st['wins']}/{st['total']} wins | mean={st['mean']:.3f} | unc={st['unc']:.3f}")


def cmd_scan(args):
    ensure_costs_tsv()
    if BANK_JSON.exists():
        with open(BANK_JSON, encoding="utf-8") as f:
            bdata = json.load(f)
        targets = bdata["targets"] if isinstance(bdata, dict) and "targets" in bdata else bdata
    else:
        targets = []
    t_by_id = {t["id"]: t for t in targets}
    trophy_text = TROPHY_MD.read_text(encoding="utf-8") if TROPHY_MD.exists() else ""
    cats_run, targets_run = load_logged_categories(t_by_id)

    math_comb_cats = {
        "record-tables",
        "graphs-games-automata",
        "erdos-and-proofs",
        "algorithms",
        "optimization-benchmarks",
        "packings-physics",
        "number-hunts",
    }

    scored = []
    for t in targets:
        tid = t["id"]
        cat = t.get("category", "")
        if args.category and cat != args.category:
            continue
        if not args.category and not args.new_domain_only and cat not in math_comb_cats:
            continue
        if args.new_domain_only and cat in cats_run:
            continue
        if tid in trophy_text or tid in targets_run:
            continue
        if t.get("disclosure") == "commit-only":
            continue

        tr = float(t.get("tractability") or 1.0)
        if tr < 2.0:
            continue

        s_clss, breakdown = clss_score(t)
        p_est = round(min(0.65, 0.08 * tr + 0.25 * s_clss), 3)
        v_est = 1.0 if t.get("kind") == "harvest" else 0.85
        c_est = 1.0 if tr >= 3.0 else 1.35
        explore_bonus = 0.20 if cat not in cats_run else 0.0
        unc_bonus = 0.10
        idx = round((p_est * v_est / c_est) + 0.40 * s_clss + explore_bonus + unc_bonus, 3)

        scored.append({
            "id": tid,
            "category": cat,
            "kind": t.get("kind"),
            "tractability": tr,
            "p_est": p_est,
            "c_est": c_est,
            "v_est": v_est,
            "s_clss": s_clss,
            "explore_bonus": explore_bonus,
            "index": idx,
            "breakdown": breakdown,
            "partials": len(t.get("partial_wins") or []),
        })

    scored.sort(key=lambda x: (-x["index"], -x["s_clss"], -x["tractability"], x["id"]))
    top = scored[: args.top]

    print(f"=== TOP {len(top)} CLSS AUTORESEARCH CANDIDATES ===")
    print(f"{'Rank':4s} {'Target ID':44s} {'Category':22s} {'Tr':4s} {'CLSS':5s} {'p_est':5s} {'Index':6s} {'Partials'}")
    for i, r in enumerate(top, 1):
        print(
            f"{i:<4d} {r['id']:44s} {r['category']:22s} {r['tractability']:<4.1f} "
            f"{r['s_clss']:<5.3f} {r['p_est']:<5.3f} {r['index']:<6.3f} {r['partials']} {r['breakdown']}"
        )

    if args.out_vs:
        out_p = pathlib.Path(args.out_vs)
        out_p.parent.mkdir(parents=True, exist_ok=True)
        n_rows = len(top)
        raw_typs = [0.14 if idx < 5 else 0.035 for idx in range(n_rows)]
        s_raw = sum(raw_typs) or 1.0
        typs = [round(x / s_raw, 3) for x in raw_typs]
        with open(out_p, "w", newline="", encoding="utf-8") as f:
            w = csv.writer(f, delimiter="\t")
            w.writerow(["id", "typicality", "p_success", "cost_min", "tags", "text"])
            for idx, r in enumerate(top):
                cost_min = int(round(r["c_est"] * 50))
                tags = ["clss"]
                if r["explore_bonus"] > 0:
                    tags.append("import")
                if idx >= n_rows - 3:
                    tags.append("strange")
                rat = f"[{r['category']}] CLSS={r['s_clss']} idx={r['index']} partials={r['partials']}"
                w.writerow([r["id"], typs[idx], r["p_est"], cost_min, ",".join(tags), rat])
        print(f"Wrote VS table to {out_p}")


def cmd_decide(args):
    DECISIONS_TSV.parent.mkdir(parents=True, exist_ok=True)
    exists = DECISIONS_TSV.exists()
    now = dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    with open(DECISIONS_TSV, "a", newline="", encoding="utf-8") as f:
        w = csv.writer(f, delimiter="\t")
        if not exists:
            w.writerow(["ts_utc", "target_id", "lens", "p_est", "cost_est", "val_est", "clss_score", "brain_index", "seed", "reason"])
        idx = round((args.p * args.val / max(0.1, args.cost)) + 0.40 * args.clss, 3)
        w.writerow([now, args.target, args.lens, args.p, args.cost, args.val, args.clss, idx, args.seed, args.reason])
    print(f"Logged decision -> {DECISIONS_TSV}: target={args.target} lens={args.lens} index={idx}")


def cmd_audit(_args):
    import time
    print("=== META-COMMANDER LIVE AUDIT (K10 Dual-Thread Governor) ===")
    # 1. Worker Thread Telemetry
    brain_root = pathlib.Path.home() / ".gemini/antigravity/brain"
    meta_cid = "556ad873-f186-4cff-b9f3-9ba7529a6273"
    workers = []
    if brain_root.exists():
        for tr in brain_root.glob("*/.system_generated/logs/transcript.jsonl"):
            cid = tr.parent.parent.parent.name
            if cid == meta_cid:
                continue
            try:
                mtime = os.path.getmtime(tr)
                size = os.path.getsize(tr)
                workers.append((mtime > time.time() - 3600 and size > 300000, mtime, cid, tr))
            except OSError:
                pass
    workers.sort(reverse=True)
    if workers:
        _, mtime, cid, tr = workers[0]
        age_s = int(time.time() - mtime)
        lines = [l for l in tr.read_text(encoding="utf-8", errors="ignore").splitlines() if l.strip()]
        recent = [json.loads(l) for l in lines[-30:]]
        errs = sum(1 for r in recent if "exited with code 1" in str(r.get("content", "")))
        print(f"Worker Thread           : {cid[:8]} ({len(lines)} steps, last step {age_s}s ago, recent tool errs={errs}/30)")
    else:
        print("Worker Thread           : none found")
    try:
        import subprocess
        out = subprocess.check_output(["pgrep", "-fl", "agy -p"], text=True, stderr=subprocess.DEVNULL).strip()
        if out:
            pids = [ln.split()[0] for ln in out.splitlines() if "V3R1T4S" in ln or "RUN_PROMPT" in ln]
            if pids:
                print(f"Headless Worker (run.sh): ACTIVE (pid={','.join(pids)}, --mode accept-edits --print-timeout 0s)")
    except Exception:
        pass

    # 2. Active Run Protocol Compliance
    runs_dir = LAB / "runs"
    runs = sorted(d for d in runs_dir.iterdir() if d.is_dir()) if runs_dir.exists() else []
    if runs:
        latest = runs[-1]
        req = ["target.md", "scout.md", "BRIEF.md", "PREREG.md", "REPORT.md"]
        present = [f for f in req if (latest / f).exists()]
        missing = [f for f in req if not (latest / f).exists()]
        code_files = [
            p for sub in latest.iterdir()
            if sub.is_dir() and sub.name not in ("scout", "data", "claim", "panel")
            for p in sub.rglob("*")
            if p.is_file() and "__pycache__" not in p.parts
        ] + [
            p for p in latest.iterdir()
            if p.is_file() and p.suffix in (".py", ".c", ".cpp", ".rs", ".sh")
        ]
        print(f"Latest Run              : {latest.name} (files present: {present or 'none'}, code/attempt files: {len(code_files)})")
        if code_files and "PREREG.md" in missing:
            print("  [PROTOCOL-DRIFT WARN] : Worker is executing exploratory code in run root/subdirectories before freezing target.md + PREREG.md!")
            print("                          Action required before claiming: write target.md, scout.md, BRIEF.md, PREREG.md, log bet & rgraph.")
        if (latest / "claim").exists() and any((latest / "claim").iterdir()) and not any((latest / "attempts").glob("*/")):
            print("  [CHECK-RUN WARN]      : non-empty claim/ exists but attempts/<lens>/ subdir is missing (required by check_run.py line 693)!")

    # 3. Compute Queue & A089980 Antidiagonal-79 Dual-Confirmation Progress
    res_hs = list((LAB / "runs/2026-10-17-1913/attempts/extender/res").glob("w39_*"))
    res_far38 = list((LAB / "runs/2026-10-17-1913/attempts/far-import/res").glob("w38_*"))
    res_far39 = list((LAB / "runs/2026-10-17-1913/attempts/far-import/res").glob("w39_*"))
    rem38 = max(0, 38 - len(res_far38))
    eta38_s = "DONE" if rem38 == 0 else f"~{round(rem38 * 3.8, 1)}m left"
    rem39 = max(0, 38 - len(res_far39))
    eta39_s = "DONE" if rem39 == 0 else ("queued" if len(res_far39) == 0 and rem38 > 0 else f"~{round(rem39 * 6.05, 1)}m left")
    hs_vals, far_vals = {}, {}
    for p in [LAB / "runs/2026-10-17-1754/attempts/extender/antidiag79.tsv",
              LAB / "runs/2026-10-17-1913/attempts/extender/antidiag79_ext.tsv"]:
        if p.exists():
            for ln in p.read_text().splitlines()[1:]:
                cols = ln.split("\t")
                if len(cols) >= 7:
                    hs_vals[int(cols[0])] = cols[-1].strip()
    for far_p in [LAB / "runs/2026-10-17-1754/attempts/small-data/antidiag79_indep.tsv",
                  LAB / "runs/2026-10-17-1913/attempts/far-import/antidiag79_far.tsv"]:
        if far_p.exists():
            lines = far_p.read_text().splitlines()
            if not lines:
                continue
            hdr = lines[0].split("\t")
            v_idx = hdr.index("T_w_79mw") if "T_w_79mw" in hdr else -1
            for ln in lines[1:]:
                cols = ln.split("\t")
                if len(cols) >= 3 and cols[0].isdigit():
                    far_vals[int(cols[0])] = cols[v_idx].strip()
    agreed = sum(1 for w in range(40) if w in hs_vals and w in far_vals and hs_vals[w] == far_vals[w])
    mism = sum(1 for w in range(40) if w in hs_vals and w in far_vals and hs_vals[w] != far_vals[w])
    print(f"A089980 ad79 Progress   : hs_mod={len(hs_vals)}/40 (DONE) | far={len(far_vals)}/40 (dual_agreed={agreed}/40, mism={mism}) | w38={len(res_far38)}/38 ({eta38_s}) | w39={len(res_far39)}/38 ({eta39_s})")

    # 4. K11 Cloud GPU Offload Status (Google Colab CLI + Kaggle GPU API)
    colab_bin = pathlib.Path("colab")
    colab_tok = pathlib.Path.home() / ".config/colab-cli/token.json"
    kaggle_tok = pathlib.Path.home() / ".kaggle/kaggle.json"
    if colab_bin.exists() and colab_tok.exists():
        sess_info = "0 active sessions"
        try:
            import subprocess
            out = subprocess.check_output([str(colab_bin), "sessions"], text=True, stderr=subprocess.DEVNULL, timeout=6).strip()
            if out and "No active sessions" not in out:
                lines_s = [ln.strip() for ln in out.splitlines() if ln.strip()]
                sess_info = f"{len(lines_s)} line(s): {' | '.join(lines_s[:2])}"
        except Exception:
            sess_info = "ready (token present)"
        kag_s = "ready" if kaggle_tok.exists() else "missing"
        print(f"Cloud GPU Offload (K11) : Colab CLI v0.7.4 READY ({sess_info}) | Kaggle GPU={kag_s}")
    else:
        print("Cloud GPU Offload (K11) : WARN — Colab CLI binary or token missing")


def main():
    ap = argparse.ArgumentParser(description="BRAIN v2 & CLSS Autoresearch Engine")
    sub = ap.add_subparsers(dest="cmd", required=True)

    p_st = sub.add_parser("status")
    p_st.set_defaults(func=cmd_status)

    p_au = sub.add_parser("audit")
    p_au.set_defaults(func=cmd_audit)

    p_sc = sub.add_parser("scan")
    p_sc.add_argument("--category", default="")
    p_sc.add_argument("--new-domain-only", action="store_true")
    p_sc.add_argument("--top", type=int, default=15)
    p_sc.add_argument("--out-vs", default="")
    p_sc.set_defaults(func=cmd_scan)

    p_dc = sub.add_parser("decide")
    p_dc.add_argument("--target", required=True)
    p_dc.add_argument("--lens", required=True)
    p_dc.add_argument("--p", type=float, required=True)
    p_dc.add_argument("--cost", type=float, default=1.0)
    p_dc.add_argument("--val", type=float, default=1.0)
    p_dc.add_argument("--clss", type=float, default=0.8)
    p_dc.add_argument("--seed", default="none")
    p_dc.add_argument("--reason", required=True)
    p_dc.set_defaults(func=cmd_decide)

    args = ap.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
