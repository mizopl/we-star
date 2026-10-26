#!python3
"""
Kaggle Cloud GPU Offload Runner for PROOFER / CLSS
==================================================
Pushes any heavy Python / PyTorch GPU script to Kaggle's free cloud GPU cluster
(NVIDIA T4 x2 / P100, 30h/week free quota), polls until completion, and downloads
all output artifacts back to a local directory — 0% local Mac RAM/GPU load.

Usage:
  python3 scripts/kaggle_gpu_runner.py \
      --script path/to/job.py \
      --slug mizopl/proofer-gpu-worker \
      --out-dir path/to/output_dir
"""
import argparse
import json
import os
import shutil
import subprocess
import sys
import tempfile
import time

KAGGLE_BIN = "kaggle"


def run_cmd(cmd, cwd=None):
    res = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True)
    return res.returncode, res.stdout.strip(), res.stderr.strip()


def push_and_wait(script_path, slug, title, out_dir, enable_gpu=True, enable_internet=True, poll_sec=20, timeout_sec=7200):
    os.makedirs(out_dir, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix="kaggle_job_") as tmpdir:
        target_script = os.path.join(tmpdir, os.path.basename(script_path))
        shutil.copy2(script_path, target_script)
        meta = {
            "id": slug,
            "title": title,
            "code_file": os.path.basename(script_path),
            "language": "python",
            "kernel_type": "script",
            "is_private": True,
            "enable_gpu": bool(enable_gpu),
            "enable_tpu": False,
            "enable_internet": bool(enable_internet),
            "dataset_sources": [],
            "competition_sources": [],
            "kernel_sources": [],
            "model_sources": [],
        }
        meta_path = os.path.join(tmpdir, "kernel-metadata.json")
        with open(meta_path, "w") as f:
            json.dump(meta, f, indent=2)

        print(f"[kaggle_gpu_runner] Pushing GPU kernel '{slug}' from {script_path}...")
        code, out, err = run_cmd([KAGGLE_BIN, "kernels", "push", "-p", tmpdir])
        if code != 0:
            raise RuntimeError(f"kaggle kernels push failed (exit {code}): {out}\n{err}")
        print(f"[kaggle_gpu_runner] Push response: {out}")

    t0 = time.time()
    while time.time() - t0 < timeout_sec:
        time.sleep(poll_sec)
        code, out, err = run_cmd([KAGGLE_BIN, "kernels", "status", slug])
        elapsed = int(time.time() - t0)
        print(f"[kaggle_gpu_runner] [{elapsed}s] {out}")
        out_lower = out.lower()
        if "complete" in out_lower:
            print(f"[kaggle_gpu_runner] Job complete! Downloading outputs to {out_dir}...")
            c2, o2, e2 = run_cmd([KAGGLE_BIN, "kernels", "output", slug, "-p", out_dir])
            print(o2)
            if c2 != 0:
                raise RuntimeError(f"kaggle kernels output failed: {e2}")
            return True
        if "error" in out_lower or "cancel" in out_lower:
            c2, o2, e2 = run_cmd([KAGGLE_BIN, "kernels", "output", slug, "-p", out_dir])
            raise RuntimeError(f"Kaggle kernel failed: {out}\nLogs downloaded to {out_dir}:\n{o2}\n{e2}")

    raise TimeoutError(f"Kaggle kernel {slug} timed out after {timeout_sec}s")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--script", required=True, help="Path to Python script to run on Kaggle GPU")
    ap.add_argument("--slug", default="mizopl/proofer-gpu-worker", help="Kaggle kernel id (username/slug)")
    ap.add_argument("--title", default="proofer-gpu-worker", help="Kaggle kernel title")
    ap.add_argument("--out-dir", required=True, help="Directory to download outputs and logs")
    ap.add_argument("--no-gpu", action="store_true", help="Disable GPU")
    ap.add_argument("--poll-sec", type=int, default=20, help="Polling interval in seconds")
    args = ap.parse_args()
    push_and_wait(
        script_path=args.script,
        slug=args.slug,
        title=args.title,
        out_dir=args.out_dir,
        enable_gpu=not args.no_gpu,
        poll_sec=args.poll_sec,
    )


if __name__ == "__main__":
    main()
