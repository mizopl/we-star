#!/usr/bin/env python3
"""build_prot_full_256.py — Deterministic 256-dim Amino-Acid + Dipeptide EC Prototype Builder.

Builds L2-normalized 256-dim TruncatedSVD protein class prototypes `(4960, 256)` strictly from
official CARE README catalog files (`processed_data/protein2EC.csv` and `processed_data/text2EC.csv`).
Zero test-label access, zero external databases. Auto-invoked by `engine_v5.py` if
`cache/prot_full_256.npy` is absent.
"""
from __future__ import annotations

import argparse
import pathlib
import time

import numpy as np
import pandas as pd
from sklearn.decomposition import TruncatedSVD
from sklearn.preprocessing import normalize

ROOT = pathlib.Path(__file__).resolve().parent
DATA_ROOT = ROOT / "data" / "CARE_datasets" / "processed_data"
CACHE_DIR = ROOT / "cache"


def build_prot_full_256(out_path: pathlib.Path | None = None, svd_dim: int = 256) -> np.ndarray:
    t0 = time.perf_counter()
    if out_path is None:
        out_path = CACHE_DIR / "prot_full_256.npy"
    out_path.parent.mkdir(parents=True, exist_ok=True)

    ec_list = pd.read_csv(DATA_ROOT / "text2EC.csv")["EC number"].astype(str).tolist()
    ec_to_i = {e: i for i, e in enumerate(ec_list)}
    p2ec = pd.read_csv(DATA_ROOT / "protein2EC.csv", usecols=["EC number", "Sequence"])

    aa = "ACDEFGHIKLMNPQRSTVWY"
    aa_idx = {c: i for i, c in enumerate(aa)}
    mat = np.zeros((len(ec_list), 420), dtype=np.float64)
    cnts = np.zeros(len(ec_list), dtype=np.float64)

    for ec, seq in zip(p2ec["EC number"].astype(str), p2ec["Sequence"].astype(str)):
        ei = ec_to_i.get(ec, -1)
        if ei < 0:
            continue
        L = max(len(seq), 1)
        v = np.zeros(420, dtype=np.float64)
        prev = -1
        for ch in seq:
            idx = aa_idx.get(ch, -1)
            if idx >= 0:
                v[idx] += 1.0
                if prev >= 0:
                    v[20 + prev * 20 + idx] += 1.0
            prev = idx
        v[:20] /= L
        v[20:] /= max(L - 1, 1)
        mat[ei] += v
        cnts[ei] += 1.0

    mat /= np.maximum(cnts[:, None], 1.0)
    mat_norm = normalize(mat.astype(np.float32), norm="l2")
    svd = TruncatedSVD(n_components=svd_dim, random_state=42)
    emb = normalize(svd.fit_transform(mat_norm), norm="l2").astype(np.float32)
    np.save(out_path, emb)
    print(f"[DONE] Saved {out_path} shape={emb.shape} dtype={emb.dtype} in {time.perf_counter()-t0:.1f}s", flush=True)
    return emb


def main() -> int:
    ap = argparse.ArgumentParser(description="Build 256-dim AA+dipeptide protein class prototypes from protein2EC.csv")
    ap.add_argument("--out", type=pathlib.Path, default=CACHE_DIR / "prot_full_256.npy")
    args = ap.parse_args()
    build_prot_full_256(args.out)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
