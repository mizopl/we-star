#!python3
"""
PROOFER Cloud GPU Offload Helper (Official Google Colab CLI v0.7.4)
===================================================================
Executes Python scripts on remote Google Colab NVIDIA GPUs (T4, L4, G4, A100, H100)
using the authenticated `~/.config/colab-cli/token.json` (Google Ultra account,
4,057+ compute units) with zero local Apple Silicon Unified Memory (MPS) pressure.

Usage:
  1. One-shot ephemeral script execution (auto-allocates VM, runs, tears down):
     python3 scripts/colab_gpu_runner.py --script my_gpu_job.py --gpu L4

  2. Keep session alive to download generated artifacts from /content/:
     python3 scripts/colab_gpu_runner.py \
         --script my_gpu_job.py --gpu A100 \
         --download /content/output.png:/tmp/output.png
"""

import argparse
import os
import subprocess
import sys
import uuid

COLAB_BIN = "colab"


def run_cmd(cmd: list[str], check: bool = True) -> subprocess.CompletedProcess:
    return subprocess.run(cmd, check=check)


def main() -> int:
    parser = argparse.ArgumentParser(description="Run a Python script on Google Colab GPU via colab-cli.")
    parser.add_argument("--script", required=True, help="Local Python script to execute on Colab GPU")
    parser.add_argument("--gpu", default="L4", choices=["T4", "L4", "G4", "A100", "H100"], help="GPU type (default: L4)")
    parser.add_argument("--upload", action="append", default=[], help="Local:Remote file pairs to upload before running (e.g. data.bin:/content/data.bin)")
    parser.add_argument("--download", action="append", default=[], help="Remote:Local file pairs to download after running (e.g. /content/out.json:./out.json)")
    parser.add_argument("script_args", nargs=argparse.REMAINDER, help="Arguments passed to the script")
    args = parser.parse_args()

    script_path = os.path.abspath(args.script)
    if not os.path.isfile(script_path):
        print(f"ERROR: Script not found: {script_path}", file=sys.stderr)
        return 1

    # Fast path: no uploads/downloads -> single `colab run` (auto-stops VM)
    if not args.upload and not args.download:
        cmd = [COLAB_BIN, "run", "--gpu", args.gpu, script_path] + args.script_args
        res = subprocess.run(cmd)
        return res.returncode

    # Managed session path: new -> upload -> exec -> download -> stop (guaranteed cleanup)
    session_name = f"proofer-{uuid.uuid4().hex[:6]}"
    try:
        run_cmd([COLAB_BIN, "new", "-s", session_name, "--gpu", args.gpu])
        for pair in args.upload:
            src, dst = pair.split(":", 1)
            run_cmd([COLAB_BIN, "upload", "-s", session_name, src, dst])
        run_cmd([COLAB_BIN, "exec", "-s", session_name, "-f", script_path])
        for pair in args.download:
            src, dst = pair.split(":", 1)
            run_cmd([COLAB_BIN, "download", "-s", session_name, src, dst])
        return 0
    finally:
        subprocess.run([COLAB_BIN, "stop", "-s", session_name], check=False)


if __name__ == "__main__":
    sys.exit(main())
