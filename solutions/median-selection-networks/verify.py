#!/usr/bin/env python3
"""
verify_staged_records.py — Standalone, env -i runnable cold verifier for staged
Median Selection Network world records (bertdobbelaere/SorterHunter format).

Verification layers (zero third-party Python dependencies):
  1. Strict JSON schema, comparator bounds (0 <= a < b < N), exact L, exact D,
     and exact layer-wise vertical symmetry check.
  2. Strict Pareto non-dominance check against live bertdobbelaere/SorterHunter
     commit a18ee17 (2026-11-08).
  3. Exact bit-parallel C Zero-One oracle (auto-compiled from local median_oracle.c):
       - N <= 24: exhaustive 2^N verification (--full) + critical slices + slices3.
       - N >= 25: exact critical weight-slice monotonicity verification (--slices
         AND --slices3: w in {k-1, k, k+1} for even N, w in {k, k+1} for odd N).
  4. Independent pure-Python 100,000-trial random integer array check (permutations,
     ties, and critical-weight inputs) asserting BOTH exact median AND exact
     partition property (all lower wires <= median <= all upper wires).
  5. --corrupt negative control: drops the final comparator from EVERY staged
     network and confirms the verifier detects the defect and exits with rc=1.
"""
import argparse
import glob
import hashlib
import json
import os
import random
import shutil
import subprocess
import sys
import tempfile
import time

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

# Live bertdobbelaere/SorterHunter (commit a18ee17, 2026-11-08) Pareto frontier
LIVE_A18EE17_PARETO = {
    22: [(74, 13), (75, 11)],
    23: [(77, 16), (78, 14), (79, 13), (83, 12)],
    24: [(82, 13), (83, 12), (86, 11)],
    25: [(85, 16), (86, 15), (87, 14), (93, 13)],
    26: [(94, 15), (95, 13), (98, 12)],
    27: [(97, 18), (98, 16), (99, 15), (102, 14), (105, 13)],
    28: [(104, 14), (105, 13), (111, 12)],
    29: [(107, 17), (108, 16), (114, 15), (118, 14)],
    30: [(118, 16), (119, 14), (122, 13)],
    31: [(121, 19), (122, 17), (124, 15), (128, 14)],
    32: [(128, 14), (132, 13)],
}


def compute_depth(n, nw):
    wd = [0] * n
    for a, b in nw:
        d = max(wd[a], wd[b]) + 1
        wd[a] = wd[b] = d
    return max(wd) if wd else 0


def check_vertical_symmetry(n, nw):
    if n % 2 == 1:
        return False
    wd = [0] * n
    layers = {}
    for a, b in nw:
        d = max(wd[a], wd[b])
        wd[a] = wd[b] = d + 1
        layers.setdefault(d, set()).add((a, b))
    for pairs in layers.values():
        for a, b in pairs:
            if (n - 1 - b, n - 1 - a) not in pairs:
                return False
    return True


def compile_oracle(oracle_src, oracle_bin):
    """Compile median_oracle.c portably (Linux/macOS standard cc, with macOS CLT SDK fallback)."""
    candidates = []
    for cand in (shutil.which("cc"), shutil.which("gcc"), shutil.which("clang"),
                 "/usr/bin/cc", "/usr/bin/clang", "/usr/bin/gcc"):
        if cand and os.path.exists(cand) and [cand, "-O3"] not in candidates:
            candidates.append([cand, "-O3"])
    clt_clang = "/Library/Developer/CommandLineTools/usr/bin/clang"
    clt_sdk = "/Library/Developer/CommandLineTools/SDKs/MacOSX.sdk"
    if os.path.exists(clt_clang):
        if os.path.isdir(clt_sdk):
            candidates.append([clt_clang, "-O3", "-isysroot", clt_sdk])
        candidates.append([clt_clang, "-O3"])
    last_err = ""
    for base_cmd in candidates:
        res = subprocess.run(base_cmd + [oracle_src, "-o", oracle_bin], capture_output=True, text=True)
        if res.returncode == 0 and os.path.isfile(oracle_bin):
            return
        last_err = (res.stderr or res.stdout or "").strip()
    raise RuntimeError(f"Failed to compile {oracle_src} with any available C compiler: {last_err}")


def run_oracle(oracle_bin, mode, n, nw):
    stdin_line = f"{n} {len(nw)} " + " ".join(f"{a} {b}" for a, b in nw) + "\n"
    proc = subprocess.run(
        [oracle_bin, "--batch", mode],
        input=stdin_line,
        text=True,
        capture_output=True,
        check=True,
    )
    parts = proc.stdout.strip().split()
    return parts[0] == "PASS", int(parts[1]), float(parts[2])


def run_int_crosscheck(n, nw, trials=100_000, seed=20261120):
    rng = random.Random(seed + n * 1000 + len(nw))
    k = n // 2
    gates = [(a, b) for a, b in nw]
    t0 = time.time()
    for trial in range(trials):
        if trial < trials // 2:
            arr = list(range(n))
            rng.shuffle(arr)
        elif trial < (4 * trials) // 5:
            arr = [rng.randrange(10) for _ in range(n)]
        else:
            w = rng.choice([k - 1, k, k + 1] if n % 2 == 0 else [k, k + 1])
            arr = [1] * w + [0] * (n - w)
            rng.shuffle(arr)
        s = sorted(arr)
        x = arr[:]
        for a, b in gates:
            if x[a] > x[b]:
                x[a], x[b] = x[b], x[a]
        if n % 2 == 1:
            if x[k] != s[k] or max(x[:k]) > x[k] or x[k] > min(x[k + 1:]):
                return False, trial, time.time() - t0
        else:
            pair = sorted((x[k - 1], x[k]))
            if pair != [s[k - 1], s[k]] or max(x[:k - 1]) > pair[0] or pair[1] > min(x[k + 1:]):
                return False, trial, time.time() - t0
    return True, trials, time.time() - t0


def classify_vs_live(n, L, D):
    pareto = LIVE_A18EE17_PARETO.get(n, [])
    min_L = min(p[0] for p in pareto)
    if L < min_L:
        return True, f"UNCONSTRAINED_MIN_SIZE_WR ({L} < {min_L})"
    for pL, pD in pareto:
        if pL <= L and pD <= D:
            return False, f"DOMINATED_BY ({pL},{pD})"
    return True, f"PARETO_WR ({L},{D})"


def main():
    ap = argparse.ArgumentParser(description="Cold verifier for staged SorterHunter median records.")
    ap.add_argument("--dir", default=SCRIPT_DIR, help="Directory with Median_*.json and median_oracle.c")
    ap.add_argument("--oracle", default="", help="Optional path to precompiled median_oracle binary")
    ap.add_argument("--corrupt", action="store_true", help="Drop final comparator from each file (must FAIL rc=1)")
    ap.add_argument("--int-trials", type=int, default=100_000, help="Random integer array trials per file")
    ap.add_argument("--write-manifest", action="store_true", help="Write verified MANIFEST.json in --dir")
    args = ap.parse_args()

    files = sorted(glob.glob(os.path.join(args.dir, "Median_*.json")))
    if not files:
        sys.stderr.write(f"ERROR: no Median_*.json files found in {args.dir}\n")
        return 2

    oracle_src = os.path.join(args.dir, "median_oracle.c")
    all_ok = True
    manifest_records = []

    with tempfile.TemporaryDirectory() as tmpd:
        precompiled = [
            args.oracle,
            os.path.join(args.dir, "median_oracle"),
            os.path.join(os.path.dirname(os.path.abspath(args.dir)), "median_oracle"),
        ]
        oracle_bin = next((p for p in precompiled if p and os.path.isfile(p) and os.access(p, os.X_OK)), "")
        if not oracle_bin:
            if not os.path.exists(oracle_src):
                sys.stderr.write(f"ERROR: missing {oracle_src}\n")
                return 2
            oracle_bin = os.path.join(tmpd, "median_oracle")
            compile_oracle(oracle_src, oracle_bin)

        # Cross-check mutual non-dominance among staged files
        staged_ld = {}
        for fpath in files:
            d = json.load(open(fpath, "r", encoding="utf-8"))
            staged_ld.setdefault(int(d["N"]), []).append((int(d["L"]), int(d["D"]), os.path.basename(fpath)))

        for n_val, pts in staged_ld.items():
            for L1, D1, f1 in pts:
                for L2, D2, f2 in pts:
                    if f1 != f2 and L2 <= L1 and D2 <= D1:
                        sys.stderr.write(f"ERROR: staged file {f1} is dominated by staged file {f2}\n")
                        return 2

        for fpath in files:
            fname = os.path.basename(fpath)
            raw_bytes = open(fpath, "rb").read()
            sha256 = hashlib.sha256(raw_bytes).hexdigest()
            d = json.loads(raw_bytes.decode("utf-8"))

            n = int(d["N"])
            L_decl = int(d["L"])
            D_decl = int(d["D"])
            sym_decl = bool(d["symmetric"])
            nw = [[int(a), int(b)] for a, b in d["nw"]]

            assert set(d.keys()) == {"N", "L", "D", "symmetric", "nw"}, f"{fname}: unexpected keys {set(d.keys())}"
            assert fname == f"Median_{n}_{L_decl}_{D_decl}.json", f"{fname}: filename mismatch"
            assert len(nw) == L_decl, f"{fname}: len(nw)={len(nw)} != L={L_decl}"
            assert compute_depth(n, nw) == D_decl, f"{fname}: depth mismatch"
            assert check_vertical_symmetry(n, nw) == sym_decl, f"{fname}: symmetry flag mismatch"
            for a, b in nw:
                assert 0 <= a < b < n, f"{fname}: invalid comparator ({a},{b})"

            is_wr, wr_cls = classify_vs_live(n, L_decl, D_decl)
            assert is_wr, f"{fname}: not strictly undominated vs live a18ee17 ({wr_cls})"

            eval_nw = nw[:-1] if args.corrupt else nw

            ok_s, err_s, ms_s = run_oracle(oracle_bin, "slices", n, eval_nw)
            ok_s3, err_s3, ms_s3 = run_oracle(oracle_bin, "slices3", n, eval_nw)
            if n <= 24:
                ok_f, err_f, ms_f = run_oracle(oracle_bin, "full", n, eval_nw)
                full_str = f"{'PASS' if ok_f else 'FAIL'}(errs={err_f},{ms_f:.2f}ms)"
            else:
                ok_f, err_f, ms_f = True, 0, 0.0
                full_str = "exact-by-monotonicity(slices3)"

            ok_int, int_cnt, int_s = run_int_crosscheck(n, eval_nw, trials=(2000 if args.corrupt else args.int_trials))

            file_ok = ok_s and ok_s3 and ok_f and ok_int
            if not file_ok:
                all_ok = False

            status = "PASS" if file_ok else "FAIL"
            print(
                f"{fname:24s} N={n:2d} L={len(eval_nw):3d} D={D_decl:2d} sym={str(sym_decl):5s} | "
                f"{status} | slices={ok_s}({err_s},{ms_s:.1f}ms) slices3={ok_s3}({err_s3},{ms_s3:.1f}ms) "
                f"full={full_str} int={ok_int}({int_cnt},{int_s:.2f}s) | {wr_cls}"
            )

            manifest_records.append({
                "file": fname,
                "sha256": sha256,
                "N": n,
                "L": L_decl,
                "D": D_decl,
                "symmetric": sym_decl,
                "live_a18ee17_pareto": LIVE_A18EE17_PARETO.get(n, []),
                "classification": wr_cls,
                "verification": {
                    "slices": {"pass": ok_s, "errs": err_s, "ms": round(ms_s, 3)},
                    "slices3": {"pass": ok_s3, "errs": err_s3, "ms": round(ms_s3, 3)},
                    "full_2n": (
                        {"pass": ok_f, "errs": err_f, "ms": round(ms_f, 3)}
                        if n <= 24 else {"skipped_reason": "N>24; exact equivalence proved by monotonicity on critical slices"}
                    ),
                    "random_int_trials": {"pass": ok_int, "trials": int_cnt, "sec": round(int_s, 3)},
                },
            })

    print(f"VERDICT: corrupt={args.corrupt} files={len(files)} status={'ALL_PASS' if all_ok else 'FAILED_AS_EXPECTED' if args.corrupt else 'FAIL'}")

    if args.write_manifest and not args.corrupt and all_ok:
        manifest = {
            "upstream_repo": "bertdobbelaere/SorterHunter",
            "upstream_commit": "a18ee17",
            "upstream_date": "2026-11-08",
            "records_count": len(manifest_records),
            "records": manifest_records,
        }
        mpath = os.path.join(args.dir, "MANIFEST.json")
        with open(mpath, "w", encoding="utf-8") as f:
            json.dump(manifest, f, indent=2)
        print(f"Wrote {mpath}")

    return 0 if all_ok else 1


if __name__ == "__main__":
    sys.exit(main())
