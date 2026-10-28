#!/usr/bin/env python3
"""Compute-job queue: the second clock (CONSTITUTION v10 §12, K2).

Long computations (> 15 min) never live inside an LLM session. A run SUBMITS a job and ends; a launchd ticker
(`jobs.py tick`, every 5 min, no LLM) starts queued jobs when resources allow, enforces each job's wall cap, and
records the outcome. The next run HARVESTS results from the job folder.

One folder per job: <WORKDIR>/jobs/<name>/
  spec.json    {name, cwd, cmd, cap_min, mem_gib, run, submitted}      (written once)
  state        queued | running | done | failed | timeout | adopted   (one word)
  pid          process-group leader PID while running
  out.log      stdout+stderr of the command
  events.log   append-only: ts state note

Usage:
  jobs.py submit NAME --cwd DIR --cap-min N --mem-gib G [--run RUNID] -- CMD...
  jobs.py adopt NAME --pid PID --cwd DIR --log FILE [--run RUNID]   (register a job that is already running)
  jobs.py tick                                                     (launchd, every 5 min)
  jobs.py list
  jobs.py requeue NAME                                             (failed/timeout -> queued again)
"""
import json
import os
import shlex
import signal
import subprocess
import sys
import time
from pathlib import Path

W = Path(os.environ.get("PROOFER_HOME", os.environ.get("V3R1T4S_WORKDIR", Path(__file__).resolve().parent.parent)))
JOBS = W / "jobs"
MAX_MEM_GIB = 7.0          # total budget for queued jobs started by the ticker
MIN_FREE_PCT = 20          # macOS memory_pressure free percentage required to start a job


def now():
    return time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())


def event(d, state, note=""):
    (d / "state").write_text(state + "\n")
    with open(d / "events.log", "a") as f:
        f.write(f"{now()} {state} {note}\n")


def alive(pid):
    try:
        os.kill(pid, 0)
        return True
    except (ProcessLookupError, PermissionError):
        return False


def free_pct():
    try:
        out = subprocess.run(["memory_pressure", "-Q"], capture_output=True, text=True, timeout=30).stdout
        return int(out.split("free percentage:")[1].split("%")[0])
    except Exception:
        return 100


def jobs():
    for d in sorted(JOBS.glob("*/")):
        if (d / "spec.json").exists():
            yield d, json.loads((d / "spec.json").read_text()), (d / "state").read_text().strip()


def submit(a):
    name, rest = a[0], a[1:]
    cmd = rest[rest.index("--") + 1:]
    opts = dict(zip(rest[:rest.index("--")][0::2], rest[:rest.index("--")][1::2]))
    d = JOBS / name
    if d.exists():
        sys.exit(f"job {name} exists")
    d.mkdir(parents=True)
    # Absolute cwd: the launchd ticker starts in "/" (X4: relative cwd made 2 jobs fail at once, 2026-10-17).
    spec = {"name": name, "cwd": os.path.abspath(opts["--cwd"]), "cmd": cmd, "cap_min": float(opts["--cap-min"]),
            "mem_gib": float(opts["--mem-gib"]), "run": opts.get("--run", ""), "submitted": now()}
    (d / "spec.json").write_text(json.dumps(spec, indent=1))
    event(d, "queued", shlex.join(cmd))
    print(f"queued {name}")


def adopt(a):
    name, rest = a[0], a[1:]
    opts = dict(zip(rest[0::2], rest[1::2]))
    d = JOBS / name
    d.mkdir(parents=True, exist_ok=False)
    spec = {"name": name, "cwd": opts["--cwd"], "cmd": ["(adopted)"], "cap_min": 0, "mem_gib": 0,
            "run": opts.get("--run", ""), "submitted": now(), "log": opts["--log"]}
    (d / "spec.json").write_text(json.dumps(spec, indent=1))
    (d / "pid").write_text(opts["--pid"])
    event(d, "adopted", f"pid {opts['--pid']} log {opts['--log']}")
    print(f"adopted {name}")


def paused_seconds(d):
    """Sum intervals between 'paused' and 'resumed' in events.log (or detected activity after pause)."""
    if not (d / "events.log").exists():
        return 0.0
    total = 0.0
    pause_ts = None
    for line in (d / "events.log").read_text().splitlines():
        parts = line.split(None, 2)
        if len(parts) < 2:
            continue
        try:
            ts = time.mktime(time.strptime(parts[0], "%Y-%m-%dT%H:%M:%SZ")) - time.timezone
        except Exception:
            continue
        st = parts[1]
        if st == "paused" and pause_ts is None:
            pause_ts = ts
        elif st in ("resumed", "running") and pause_ts is not None:
            total += max(0.0, ts - pause_ts)
            pause_ts = None
    if pause_ts is not None:
        total += max(0.0, time.time() - pause_ts)
    return total


def tick():
    JOBS.mkdir(exist_ok=True)
    used = 0.0
    for d, spec, state in jobs():
        if state not in ("running", "adopted"):
            continue
        pid = int((d / "pid").read_text())
        if alive(pid):
            started = os.path.getmtime(d / "pid")
            active_sec = (time.time() - started) - paused_seconds(d)
            if spec["cap_min"] and active_sec > spec["cap_min"] * 60:
                os.killpg(pid, signal.SIGTERM)          # our own process group, by exact id
                event(d, "timeout", f"cap {spec['cap_min']} min (active {active_sec/60:.1f}m)")
            else:
                used += spec["mem_gib"]
            continue
        if state == "adopted":
            event(d, "done", "adopted process exited (check its own log for success)")
            continue
        rc_file = d / "rc"
        rc = rc_file.read_text().strip() if rc_file.exists() else "?"
        event(d, "done" if rc == "0" else "failed", f"rc={rc}")
    for d, spec, state in jobs():
        if state != "queued":
            continue
        if used + spec["mem_gib"] > MAX_MEM_GIB or free_pct() < MIN_FREE_PCT:
            break                                     # FIFO: wait for resources
        cwd = spec["cwd"] if os.path.isabs(spec["cwd"]) else str(W / spec["cwd"])
        sh = (f"{{ cd {shlex.quote(cwd)} && nice -n 10 {shlex.join(spec['cmd'])}; }} > {shlex.quote(str(d/'out.log'))} 2>&1; "
              f"echo $? > {shlex.quote(str(d/'rc'))}")
        p = subprocess.Popen(["/bin/sh", "-c", sh], start_new_session=True,
                             stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        (d / "pid").write_text(str(p.pid))
        event(d, "running", f"pid {p.pid}")
        used += spec["mem_gib"]


def requeue(a):
    d = JOBS / a[0]
    for f in ("pid", "rc"):
        (d / f).unlink(missing_ok=True)
    event(d, "queued", "requeued")
    print(f"requeued {a[0]}")


def extend(a):
    d = JOBS / a[0]
    new_cap = float(a[1])
    spec = json.loads((d / "spec.json").read_text())
    old_cap = spec.get("cap_min", 0)
    spec["cap_min"] = new_cap
    (d / "spec.json").write_text(json.dumps(spec, indent=1))
    with open(d / "events.log", "a") as f:
        f.write(f"{now()} running cap extended {old_cap}m -> {new_cap}m\n")
    print(f"extended {a[0]} cap {old_cap}m -> {new_cap}m")


def lst():
    for d, spec, state in jobs():
        pid = (d / "pid").read_text().strip() if (d / "pid").exists() else "-"
        p_min = paused_seconds(d) / 60.0
        p_note = f" (paused {p_min:.0f}m)" if p_min >= 1.0 else ""
        print(f"{spec['name']:40} {state:8} pid={pid:7} cap={spec['cap_min']}m mem={spec['mem_gib']}G run={spec['run']}{p_note}")


if __name__ == "__main__":
    c, a = (sys.argv[1] if len(sys.argv) > 1 else ""), sys.argv[2:]
    {"submit": lambda: submit(a), "adopt": lambda: adopt(a), "tick": tick, "list": lst,
     "requeue": lambda: requeue(a), "extend": lambda: extend(a)}.get(c, lambda: sys.exit(__doc__))()
