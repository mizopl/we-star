#!/usr/bin/env python3
"""Build & cache denoised BGE-small-en-v1.5 text embeddings for text2EC.csv."""
import pathlib
import sys
import time
import numpy as np
from sentence_transformers import SentenceTransformer

ROOT = pathlib.Path(__file__).resolve().parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import features_v2 as f2  # noqa: E402


def main():
    t0 = time.perf_counter()
    ec_df = f2.prepare_denoised_text2ec()
    for c3 in ("1.1.1", "2.3.1", "3.5.1", "4.1.1", "6.2.1"):
        print(f"  {c3:6s} -> {ec_df[ec_df['ec3']==c3]['l3_clean'].iloc[0]}")

    st = SentenceTransformer("BAAI/bge-small-en-v1.5", device="cpu")
    B_l2 = st.encode([s if s else "enzyme" for s in ec_df["l2"]], batch_size=64, normalize_embeddings=True, show_progress_bar=False).astype(np.float32)
    B_l2[ec_df["l2"].str.len().values == 0] = 0.0
    B_l3 = st.encode([s if s else "enzyme" for s in ec_df["l3_clean"]], batch_size=64, normalize_embeddings=True, show_progress_bar=False).astype(np.float32)
    B_l4 = st.encode([s if s else "enzyme" for s in ec_df["l4"]], batch_size=64, normalize_embeddings=True, show_progress_bar=False).astype(np.float32)
    B_l4[ec_df["l4"].str.len().values == 0] = 0.0

    out_p = ROOT / "cache" / "ec_bge_spaces_v2.npz"
    out_p.parent.mkdir(parents=True, exist_ok=True)
    np.savez_compressed(
        out_p,
        B_l2=B_l2,
        B_l3=B_l3,
        B_l4=B_l4,
        l3_clean=np.array(ec_df["l3_clean"].tolist(), dtype=str),
    )
    print(f"Saved {out_p} in {time.perf_counter()-t0:.1f}s")


if __name__ == "__main__":
    main()
