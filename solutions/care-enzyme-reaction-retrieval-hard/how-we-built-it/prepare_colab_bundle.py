#!/usr/bin/env python3
"""prepare_colab_bundle.py — Build physically air-gapped tarball for Colab GPU Reaction Transformer training.

SECURITY / ANTI-LEAKAGE INVARIANT:
  - Test CSVs inside the tarball contain STRICTLY `Reaction` + cofactor-parsed reaction SMILES strings.
  - Zero `EC number`, zero `Mapped Reaction`, zero `Reaction Text` on any test row!
  - Precomputes RDKit cofactor/organic splits locally so Colab needs zero RDKit install.
"""
import pathlib
import sys
import tarfile
import time
import numpy as np
import pandas as pd
from rdkit import Chem, RDLogger
from sklearn.preprocessing import normalize

RDLogger.DisableLog("rdApp.*")

ROOT = pathlib.Path(__file__).resolve().parent
DATA_ROOT = ROOT / "data" / "CARE_datasets"
CACHE_DIR = ROOT / "cache"
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import features_v2 as f2  # noqa: E402


def parse_rxns_for_transformer(rxns: list[str], smi_cache: dict) -> tuple[list[str], list[str], list[str]]:
    t5_prompts, siam_lhs, siam_rhs = [], [], []
    for r in rxns:
        lhs, rhs = r.split(">>")
        l_org, l_cof, r_org, r_cof = [], [], [], []
        for s in lhs.split("."):
            s = s.strip()
            if not s or s == "[H+]":
                continue
            cs, cname = smi_cache.get(s, (s, None))
            if cname:
                l_cof.append(cs)
            else:
                l_org.append(cs)
        for s in rhs.split("."):
            s = s.strip()
            if not s or s == "[H+]":
                continue
            cs, cname = smi_cache.get(s, (s, None))
            if cname:
                r_cof.append(cs)
            else:
                r_org.append(cs)
        lo = ".".join(l_org) if l_org else ".".join(l_cof)
        ro = ".".join(r_org) if r_org else ".".join(r_cof)
        lc = ".".join(l_cof)
        rc = ".".join(r_cof)
        reag = f"{lc}>>{rc}" if (lc or rc) else "NONE"
        t5_prompts.append((f"REACTANT:{lo}REAGENT:{reag}", lo, ro, r))
    return (
        [x[0] for x in t5_prompts],
        [x[1] for x in t5_prompts],
        [x[2] for x in t5_prompts],
    )


def main():
    t0 = time.perf_counter()
    stage = CACHE_DIR / "colab_stage"
    stage.mkdir(parents=True, exist_ok=True)

    dfs = {}
    uniq = set()
    for sp in ("hard", "medium"):
        tr = pd.read_csv(DATA_ROOT / "splits" / "task2" / f"{sp}_reaction_train.csv")
        te = pd.read_csv(DATA_ROOT / "splits" / "task2" / f"{sp}_reaction_test.csv")
        dfs[(sp, "tr")] = tr
        dfs[(sp, "te")] = te
        for rxn in tr["Reaction"].astype(str).tolist() + te["Reaction"].astype(str).tolist():
            for side in rxn.split(">>"):
                for s in side.split("."):
                    s = s.strip()
                    if s and s != "[H+]":
                        uniq.add(s)

    smi_cache = {}
    for s in uniq:
        m = Chem.MolFromSmiles(s)
        if m is None:
            smi_cache[s] = (s, None)
            continue
        um = f2.uncharge_biochem(m)
        cs = Chem.MolToSmiles(um, isomericSmiles=False)
        cs_iso = Chem.MolToSmiles(m, isomericSmiles=True)
        cname = f2.COFACTOR_LUT.get(cs)
        if cname is None and "*N1c2" in s and "Nc2" in s:
            cname = "Flavin_bound"
        elif cname is None and "[Fe" in s and "[S" in s:
            cname = "FeS_cluster"
        # Preserve original stereo for organic molecules while stripping cofactors cleanly
        smi_cache[s] = (cs_iso, cname)

    for sp in ("hard", "medium"):
        tr = dfs[(sp, "tr")]
        t5_tr, lo_tr, ro_tr = parse_rxns_for_transformer(tr["Reaction"].astype(str).tolist(), smi_cache)
        pd.DataFrame({
            "t5_prompt": t5_tr,
            "lhs_org": lo_tr,
            "rhs_org": ro_tr,
            "Reaction": tr["Reaction"].astype(str),
            "EC number": tr["EC number"].astype(str),
        }).to_csv(stage / f"{sp}_train.csv", index=False)

        # STRICT TEST AIR-GAP: NEVER write EC number, Mapped Reaction, or Reaction Text!
        te = dfs[(sp, "te")]
        t5_te, lo_te, ro_te = parse_rxns_for_transformer(te["Reaction"].astype(str).tolist(), smi_cache)
        te_out = pd.DataFrame({
            "t5_prompt": t5_te,
            "lhs_org": lo_te,
            "rhs_org": ro_te,
            "Reaction": te["Reaction"].astype(str),
        })
        assert list(te_out.columns) == ["t5_prompt", "lhs_org", "rhs_org", "Reaction"]
        te_out.to_csv(stage / f"{sp}_test_rxns_only.csv", index=False)

    # Save exact Super-Hard Clustered Medium-CV indices (strictly from medium_train!)
    med_tr = dfs[("medium", "tr")]
    mf = np.load(CACHE_DIR / "v2_feats_medium.npz")
    rng = np.random.default_rng(77)
    val_ec4 = set(rng.choice(sorted(med_tr["EC number"].unique()), size=220, replace=False))
    is_vm = med_tr["EC number"].isin(val_ec4).values
    va_i = np.array(sorted([x for _, g in med_tr[is_vm].groupby("EC number") for x in rng.choice(g.index.values, size=min(2, len(g)), replace=False)]), dtype=np.int64)
    cand_tr = np.where(~is_vm)[0]
    sub_all = normalize(mf["tr_sub_diff_r2"].astype(np.float32), norm="l2")
    rxn_all = normalize(mf["tr_rxn_diff_r2"].astype(np.float32), norm="l2")
    keep = ((sub_all[cand_tr] @ sub_all[va_i].T).max(1) < 0.72) & ((rxn_all[cand_tr] @ rxn_all[va_i].T).max(1) < 0.74)
    tr_i = cand_tr[keep]
    np.savez_compressed(stage / "med_cv_idx.npz", tr_idx=tr_i, va_idx=va_i)

    # Copy denoised text2EC metadata & precomputed BGE spaces + compressed mech vectors
    ec_df = f2.prepare_denoised_text2ec()
    ec_df[["ec", "ec1", "ec2", "ec3", "l1", "l2", "l3_clean", "l4"]].to_csv(stage / "ec_meta.csv", index=False)
    bge = np.load(CACHE_DIR / "ec_bge_spaces_v2.npz")
    hf = np.load(CACHE_DIR / "v2_feats_hard.npz")
    np.savez_compressed(
        stage / "aux_feats.npz",
        B_l2=bge["B_l2"].astype(np.float16),
        B_l3=bge["B_l3"].astype(np.float16),
        B_l4=bge["B_l4"].astype(np.float16),
        med_tr_mech=mf["tr_mech"].astype(np.float16),
        med_te_mech=mf["te_mech"].astype(np.float16),
        hard_tr_mech=hf["tr_mech"].astype(np.float16),
        hard_te_mech=hf["te_mech"].astype(np.float16),
    )

    bundle = CACHE_DIR / "care_colab_bundle.tar.gz"
    with tarfile.open(bundle, "w:gz") as tar:
        for f in sorted(stage.iterdir()):
            tar.add(f, arcname=f.name)
    sz_mb = bundle.stat().st_size / (1024 * 1024)
    print(f"[BUNDLE_READY] {bundle} size={sz_mb:.2f} MB in {time.perf_counter()-t0:.1f}s (med_cv tr={len(tr_i)} va={len(va_i)})")


if __name__ == "__main__":
    main()
