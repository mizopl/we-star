#!/usr/bin/env bash
# verify_all.sh: Standalone, memory-safe cold verification for the 36/36 Zero-Mathlib
# Lean 4.36.0 Binary Multi-Deletion Code Certification Suite.
#
# Usage:
#   bash verify_all.sh          # Full sequential cold build + AuditAxioms + comparator parity + leanchecker
#   bash verify_all.sh --quick  # Static gates + AuditAxioms + comparator parity + core leanchecker (<30s)
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

QUICK=0
for arg in "$@"; do
  case "$arg" in
    --quick) QUICK=1 ;;
    -h|--help)
      echo "Usage: bash verify_all.sh [--quick]"
      exit 0
      ;;
    *)
      echo "Unknown option: $arg" >&2
      exit 2
      ;;
  esac
done

PYTHON_BIN="${PYTHON_BIN:-python3}"
if ! command -v "$PYTHON_BIN" >/dev/null 2>&1; then
  echo "FAIL: python3 not found in PATH" >&2
  exit 1
fi
if ! command -v lake >/dev/null 2>&1; then
  echo "FAIL: lake not found in PATH (install elan and toolchain from lean-toolchain)" >&2
  exit 1
fi

echo "=== 1. TCB Zero-Import Check & Static Forbidden-Token Scan ==="
"$PYTHON_BIN" - <<'PY'
import json
import os
import re
import sys

def strip_lean_comments(src: str) -> str:
    out = []
    i, n = 0, len(src)
    depth = 0
    in_str = False
    while i < n:
        ch = src[i]
        nxt = src[i + 1] if i + 1 < n else ""
        if depth == 0 and not in_str and ch == '"':
            in_str = True
            out.append(ch)
            i += 1
        elif in_str:
            out.append(ch)
            if ch == "\\" and i + 1 < n:
                out.append(src[i + 1])
                i += 2
                continue
            if ch == '"':
                in_str = False
            i += 1
        elif ch == "/" and nxt == "-":
            depth += 1
            out.append("  ")
            i += 2
        elif depth > 0 and ch == "-" and nxt == "/":
            depth -= 1
            out.append("  ")
            i += 2
        elif depth == 0 and ch == "-" and nxt == "-":
            while i < n and src[i] != "\n":
                i += 1
        elif depth == 0:
            out.append(ch)
            i += 1
        else:
            if ch == "\n":
                out.append("\n")
            i += 1
    return "".join(out)

# Check DeletionCode/Statements.lean has 0 imports
stmt_clean = strip_lean_comments(open("DeletionCode/Statements.lean", encoding="utf-8").read())
imports = re.findall(r"^\s*import\s+\S+", stmt_clean, re.MULTILINE)
if imports:
    sys.exit(f"FAIL [TCB]: DeletionCode/Statements.lean has non-empty imports: {imports}")
print("PASS [TCB]: DeletionCode/Statements.lean -> 0 imports")

# Check all .lean files outside .lake/ for forbidden tokens
forbidden = [
    ("sorry", re.compile(r"\bsorry\b")),
    ("admit", re.compile(r"\badmit\b")),
    ("native_decide", re.compile(r"\bnative_decide\b")),
    ("Lean.ofReduceBool", re.compile(r"\bLean\.ofReduceBool\b|\bofReduceBool\b")),
    ("Lean.trustCompiler", re.compile(r"\bLean\.trustCompiler\b|\btrustCompiler\b")),
    ("custom_axiom", re.compile(r"^\s*(?:private\s+|protected\s+)?axiom\s+", re.MULTILINE)),
]
lean_count = 0
violations = []
for root, dirs, files in os.walk("."):
    dirs[:] = [d for d in dirs if d != ".lake" and not d.startswith(".")]
    for fn in sorted(files):
        if not fn.endswith(".lean"):
            continue
        lean_count += 1
        path = os.path.join(root, fn)
        cleaned = strip_lean_comments(open(path, encoding="utf-8").read())
        for label, rx in forbidden:
            if rx.search(cleaned):
                violations.append(f"{path}: forbidden token '{label}'")
if violations:
    sys.exit("FAIL [STATIC]:\n  " + "\n  ".join(violations))
print(f"PASS [STATIC]: {lean_count} .lean files scanned -> 0 sorry, 0 admit, 0 native_decide, 0 ofReduceBool, 0 trustCompiler, 0 custom axioms")

# Check comparator.json manifest
comp = json.load(open("comparator.json", encoding="utf-8"))
if comp.get("enable_nanoda") is not True:
    sys.exit("FAIL [COMPARATOR]: comparator.json must set enable_nanoda: true")
print(f"PASS [COMPARATOR]: comparator.json valid (enable_nanoda=True, targets={len(comp.get('target_theorems', []))})")
PY

# Strictly sequential module order (1 heavy shard at a time so 7 GB CI runners & 16 GB laptops stay flat)
BUILD_MODULES=(
  DeletionCode.Statements
  DeletionCode.Basic
  DeletionCode.Cert_15_2
  DeletionCode.Cert_15_2Max
  DeletionCode.Cert_15_3
  DeletionCode.Cert_15_3Max
  DeletionCode.Cert_16_3
  DeletionCode.Cert_16_3Max
  DeletionCode.Cert_16_2
  DeletionCode.Cert_16_2Max
  DeletionCode.Cert_16_2_226
  DeletionCode.DualLP
  DeletionCode.CutDual
  DeletionCode.RecDual
  DeletionCode.SchrijverPSD
  DeletionCode.PeelReduce
  DeletionCode.FastSchrijver
  DeletionCode.Cert_8_2_Dual
  DeletionCode.Cert_10_2_Dual.S0
  DeletionCode.Cert_10_2_Dual.S1
  DeletionCode.Cert_10_2_Dual.S2
  DeletionCode.Cert_10_2_Dual.S3
  DeletionCode.Cert_10_2_Dual
  DeletionCode.Cert_10_3_Dual.S0
  DeletionCode.Cert_10_3_Dual.S1
  DeletionCode.Cert_10_3_Dual.S2
  DeletionCode.Cert_10_3_Dual.S3
  DeletionCode.Cert_10_3_Dual
  DeletionCode.Cert_9_2_PSD
  DeletionCode.Cert_10_2_PSD.Data
  DeletionCode.Cert_10_2_PSD.S0
  DeletionCode.Cert_10_2_PSD.S1
  DeletionCode.Cert_10_2_PSD.S2
  DeletionCode.Cert_10_2_PSD.S3
  DeletionCode.Cert_10_2_PSD.S4
  DeletionCode.Cert_10_2_PSD.S5
  DeletionCode.Cert_10_2_PSD
  DeletionCode.Cert_11_3_PSD_Shards.Data
  DeletionCode.Cert_11_3_PSD_Shards.Trees
  DeletionCode.Cert_11_3_PSD_Shards.P0
  DeletionCode.Cert_11_3_PSD_Shards.P1
  DeletionCode.Cert_11_3_PSD_Shards.P2
  DeletionCode.Cert_11_3_PSD_Shards.P3
  DeletionCode.Cert_11_3_PSD_Shards.P4
  DeletionCode.Cert_11_3_PSD_Shards.P5
  DeletionCode.Cert_11_3_PSD_Shards.S0
  DeletionCode.Cert_11_3_PSD_Shards.S1
  DeletionCode.Cert_11_3_PSD_Shards.S2
  DeletionCode.Cert_11_3_PSD_Shards.S3
  DeletionCode.Cert_11_3_PSD_Shards.S4
  DeletionCode.Cert_11_3_PSD_Shards.S5
  DeletionCode.Cert_11_3_PSD_Shards.S6
  DeletionCode.Cert_11_3_PSD_Shards.S7
  DeletionCode.Cert_11_3_PSD
  DeletionCode.Cert_12_3_PSD_Shards.Data
  DeletionCode.Cert_12_3_PSD_Shards.KData
  DeletionCode.Cert_12_3_PSD_Shards.Trees
  DeletionCode.Cert_12_3_PSD_Shards.P0
  DeletionCode.Cert_12_3_PSD_Shards.P1
  DeletionCode.Cert_12_3_PSD_Shards.P2
  DeletionCode.Cert_12_3_PSD_Shards.L0
  DeletionCode.Cert_12_3_PSD_Shards.L1
  DeletionCode.Cert_12_3_PSD_Shards.L2
  DeletionCode.Cert_12_3_PSD_Shards.L3
  DeletionCode.Cert_12_3_PSD_Shards.S0
  DeletionCode.Cert_12_3_PSD_Shards.S1
  DeletionCode.Cert_12_3_PSD_Shards.S2
  DeletionCode.Cert_12_3_PSD_Shards.S3
  DeletionCode.Cert_12_3_PSD_Shards.S4
  DeletionCode.Cert_12_3_PSD_Shards.S5
  DeletionCode.Cert_12_3_PSD_Shards.S6
  DeletionCode.Cert_12_3_PSD_Shards.S7
  DeletionCode.Cert_12_3_PSD_Shards.S8
  DeletionCode.Cert_12_3_PSD_Shards.S9
  DeletionCode.Cert_12_3_PSD_Shards.S10
  DeletionCode.Cert_12_3_PSD_Shards.S11
  DeletionCode.Cert_12_3_PSD_Shards.S12
  DeletionCode.Cert_12_3_PSD_Shards.S13
  DeletionCode.Cert_12_3_PSD_Shards.S14
  DeletionCode.Cert_12_3_PSD_Shards.S15
  DeletionCode.Cert_12_3_PSD
  DeletionCode
  Challenge
)

if [ "$QUICK" -eq 0 ]; then
  echo "=== 2. Sequential Lake Build (${#BUILD_MODULES[@]} modules) ==="
  for mod in "${BUILD_MODULES[@]}"; do
    echo "[BUILD] $mod"
    lake build "$mod"
  done
else
  echo "=== 2. Quick Mode: Skipping full lake build (using existing .lake cache) ==="
fi

echo "=== 3. AuditAxioms.lean & comparator.json Parity ==="
AUDIT_OUT="$(lake env lean AuditAxioms.lean 2>&1)"
echo "$AUDIT_OUT"
AUDIT_OUT="$AUDIT_OUT" "$PYTHON_BIN" - <<'PY'
import json
import os
import re
import sys

allowed = {"propext", "Classical.choice", "Quot.sound"}
out = os.environ["AUDIT_OUT"]
seen = {}
bad = []
for line in out.splitlines():
    m = re.match(r"^'([^']+)'\s+depends on axioms:\s*\[([^\]]*)\]", line.strip())
    if m:
        thm = m.group(1)
        axs = [a.strip() for a in m.group(2).split(",") if a.strip()]
        seen[thm] = axs
        extra = [a for a in axs if a not in allowed]
        if extra:
            bad.append(f"{thm}: disallowed axioms {extra}")
    elif "does not depend on any axioms" in line:
        m2 = re.match(r"^'([^']+)'\s+does not depend on any axioms", line.strip())
        if m2:
            seen[m2.group(1)] = []

if not seen or bad:
    sys.exit(f"FAIL [AXIOMS]: checked={len(seen)}, bad={bad}")

comp = json.load(open("comparator.json", encoding="utf-8"))
targets = comp.get("target_theorems", [])
missing = [t for t in targets if t not in seen]
if missing:
    sys.exit(f"FAIL [COMPARATOR_PARITY]: missing from AuditAxioms.lean: {missing}")
print(f"PASS [AXIOMS]: {len(seen)}/{len(seen)} theorems strictly in {sorted(allowed)}")
print(f"PASS [COMPARATOR_PARITY]: all {len(targets)}/{len(targets)} target_theorems audited")
PY

if [ "$QUICK" -eq 1 ]; then
  CHECK_MODULES=(
    DeletionCode.Statements
    DeletionCode.SchrijverPSD
    DeletionCode.PeelReduce
    DeletionCode.FastSchrijver
    DeletionCode.Cert_11_3_PSD
    DeletionCode.Cert_12_3_PSD
    Challenge
  )
  echo "=== 4. Quick Mode: Core Leanchecker (${#CHECK_MODULES[@]} modules) ==="
else
  # Note: `leanchecker <Prefix>` checks all modules matching `<Prefix>.*`, so prefix modules
  # (`Cert_10_2_Dual`, `Cert_10_3_Dual`, `Cert_10_2_PSD`, `Cert_15_*Max`, `Cert_16_*Max`)
  # automatically check their sub-shards once, while `Cert_11_3_PSD_Shards.*` and
  # `Cert_12_3_PSD_Shards.*` use disjoint prefixes so each shard is checked individually.
  CHECK_MODULES=(
    DeletionCode.Statements
    DeletionCode.Basic
    DeletionCode.Cert_15_2
    DeletionCode.Cert_15_2Max
    DeletionCode.Cert_15_3
    DeletionCode.Cert_15_3Max
    DeletionCode.Cert_16_3
    DeletionCode.Cert_16_3Max
    DeletionCode.Cert_16_2
    DeletionCode.Cert_16_2Max
    DeletionCode.Cert_16_2_226
    DeletionCode.DualLP
    DeletionCode.CutDual
    DeletionCode.RecDual
    DeletionCode.SchrijverPSD
    DeletionCode.PeelReduce
    DeletionCode.FastSchrijver
    DeletionCode.Cert_8_2_Dual
    DeletionCode.Cert_10_2_Dual
    DeletionCode.Cert_10_3_Dual
    DeletionCode.Cert_9_2_PSD
    DeletionCode.Cert_10_2_PSD
    DeletionCode.Cert_11_3_PSD_Shards.Data
    DeletionCode.Cert_11_3_PSD_Shards.Trees
    DeletionCode.Cert_11_3_PSD_Shards.P0
    DeletionCode.Cert_11_3_PSD_Shards.P1
    DeletionCode.Cert_11_3_PSD_Shards.P2
    DeletionCode.Cert_11_3_PSD_Shards.P3
    DeletionCode.Cert_11_3_PSD_Shards.P4
    DeletionCode.Cert_11_3_PSD_Shards.P5
    DeletionCode.Cert_11_3_PSD_Shards.S0
    DeletionCode.Cert_11_3_PSD_Shards.S1
    DeletionCode.Cert_11_3_PSD_Shards.S2
    DeletionCode.Cert_11_3_PSD_Shards.S3
    DeletionCode.Cert_11_3_PSD_Shards.S4
    DeletionCode.Cert_11_3_PSD_Shards.S5
    DeletionCode.Cert_11_3_PSD_Shards.S6
    DeletionCode.Cert_11_3_PSD_Shards.S7
    DeletionCode.Cert_11_3_PSD
    DeletionCode.Cert_12_3_PSD_Shards.Data
    DeletionCode.Cert_12_3_PSD_Shards.KData
    DeletionCode.Cert_12_3_PSD_Shards.Trees
    DeletionCode.Cert_12_3_PSD_Shards.P0
    DeletionCode.Cert_12_3_PSD_Shards.P1
    DeletionCode.Cert_12_3_PSD_Shards.P2
    DeletionCode.Cert_12_3_PSD_Shards.L0
    DeletionCode.Cert_12_3_PSD_Shards.L1
    DeletionCode.Cert_12_3_PSD_Shards.L2
    DeletionCode.Cert_12_3_PSD_Shards.L3
    DeletionCode.Cert_12_3_PSD_Shards.S0
    DeletionCode.Cert_12_3_PSD_Shards.S1
    DeletionCode.Cert_12_3_PSD_Shards.S2
    DeletionCode.Cert_12_3_PSD_Shards.S3
    DeletionCode.Cert_12_3_PSD_Shards.S4
    DeletionCode.Cert_12_3_PSD_Shards.S5
    DeletionCode.Cert_12_3_PSD_Shards.S6
    DeletionCode.Cert_12_3_PSD_Shards.S7
    DeletionCode.Cert_12_3_PSD_Shards.S8
    DeletionCode.Cert_12_3_PSD_Shards.S9
    DeletionCode.Cert_12_3_PSD_Shards.S10
    DeletionCode.Cert_12_3_PSD_Shards.S11
    DeletionCode.Cert_12_3_PSD_Shards.S12
    DeletionCode.Cert_12_3_PSD_Shards.S13
    DeletionCode.Cert_12_3_PSD_Shards.S14
    DeletionCode.Cert_12_3_PSD_Shards.S15
    DeletionCode.Cert_12_3_PSD
    Challenge
  )
  echo "=== 4. Full Sequential Leanchecker (${#CHECK_MODULES[@]} targets) ==="
fi

for mod in "${CHECK_MODULES[@]}"; do
  echo "[LEANCHECKER] $mod"
  lake env leanchecker "$mod"
done

echo "=== ALL_GATES_PASSED ==="
