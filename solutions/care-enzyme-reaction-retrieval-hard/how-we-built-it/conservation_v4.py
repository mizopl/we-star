#!/usr/bin/env python3
"""conservation_v4.py — Fast (<2s), zero-leakage Reaction-SMILES biochemical conservation & cofactor-truncation rules."""
from __future__ import annotations

import pathlib
import sys
import numpy as np
import pandas as pd
from rdkit import Chem

ROOT = pathlib.Path(__file__).resolve().parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import features_v2 as f2  # noqa: E402


_METALS = frozenset({
    "[Na+]", "[K+]", "[Ca+2]", "[Ca2+]", "[Mg+2]", "[Mg2+]",
    "[Co]", "[Co+2]", "[Fe+2]", "[Fe+3]", "[Cu+]", "[Cu+2]", "[Zn+2]", "[H]",
})


def extract_fast_conservation_feats(rxns: list[str], mech_raw: np.ndarray) -> np.ndarray:
    """Extract 24 stoichiometric/cofactor-truncation interaction features strictly from `Reaction` SMILES + `mech`."""
    fi = f2.FLAG_IDX
    nf = len(f2.FLAG_NAMES)
    nfg = len(f2.FG_NAMES)
    atom_off = nf + 2 * nfg
    sr_off = atom_off + len(f2.ATOM_LIST)
    si = f2.SUB_IDX

    atp_smis = {s for s, k in f2.COFACTOR_LUT.items() if k == "ATP"}
    adp_smis = {s for s, k in f2.COFACTOR_LUT.items() if k == "ADP"}
    amp_smis = {s for s, k in f2.COFACTOR_LUT.items() if k == "AMP"}
    gtp_smis = {s for s, k in f2.COFACTOR_LUT.items() if k == "GTP"}
    gdp_smis = {s for s, k in f2.COFACTOR_LUT.items() if k == "GDP"}
    nad_smis = {s for s, k in f2.COFACTOR_LUT.items() if k in ("NAD+", "NADP+")}
    nadh_smis = {s for s, k in f2.COFACTOR_LUT.items() if k in ("NADH", "NADPH")}
    pi_smis = {s for s, k in f2.COFACTOR_LUT.items() if k == "Pi"}

    frag_cat: dict[str, str] = {}
    uniq_frags: set[str] = set()
    parsed: list[tuple[str, list[str], list[str]]] = []
    for r in rxns:
        lhs, rhs = r.split(">>")
        lf = [x.strip() for x in lhs.split(".") if x.strip() and x.strip() != "[H+]"]
        rf = [x.strip() for x in rhs.split(".") if x.strip() and x.strip() != "[H+]"]
        parsed.append((r, lf, rf))
        uniq_frags.update(lf)
        uniq_frags.update(rf)

    for s in uniq_frags:
        if s in f2.COFACTOR_LUT:
            cs = s
        else:
            m = Chem.MolFromSmiles(s)
            cs = Chem.MolToSmiles(f2.uncharge_biochem(m), isomericSmiles=False) if m is not None else s
        if cs in atp_smis:
            frag_cat[s] = "ATP"
        elif cs in adp_smis:
            frag_cat[s] = "ADP"
        elif cs in amp_smis:
            frag_cat[s] = "AMP"
        elif cs in gtp_smis:
            frag_cat[s] = "GTP"
        elif cs in gdp_smis:
            frag_cat[s] = "GDP"
        elif cs in nad_smis:
            frag_cat[s] = "NAD"
        elif cs in nadh_smis:
            frag_cat[s] = "NADH"
        elif cs in pi_smis:
            frag_cat[s] = "Pi"
        elif s in _METALS:
            frag_cat[s] = "METAL"
        else:
            frag_cat[s] = "OTHER"

    out = np.zeros((len(rxns), 24), dtype=np.float32)
    for i, (r, lf, rf) in enumerate(parsed):
        lc = {frag_cat.get(x, "OTHER") for x in lf}
        rc = {frag_cat.get(x, "OTHER") for x in rf}
        l_other = sum(1 for x in lf if frag_cat.get(x, "OTHER") == "OTHER")
        r_other = sum(1 for x in rf if frag_cat.get(x, "OTHER") == "OTHER")

        atp_cons = float(("ATP" in lc) and ("ATP" not in rc))
        gtp_cons = float(("GTP" in lc) and ("GTP" not in rc))
        nad_cleaved = float(("NAD" in lc) and ("NAD" not in rc) and ("NADH" not in rc))
        only_pi_rhs = float(len(rf) >= 1 and all(frag_cat.get(x) in ("Pi", "ADP", "GDP") for x in rf) and ("Pi" in rc))
        atp_pi_only = float(atp_cons and len(rf) == 1 and ("Pi" in rc))
        atp_trunc_lig = float(atp_cons and ("ADP" not in rc) and ("AMP" not in rc) and ("Pi" not in rc) and r_other == 1 and l_other >= 1)
        nad_lig_join = float(nad_cleaved and l_other >= 2 and r_other == 1)

        out[i, 0] = len(lf)
        out[i, 1] = len(rf)
        out[i, 2] = len(rf) - len(lf)
        out[i, 3] = l_other
        out[i, 4] = r_other
        out[i, 5] = float("*" in r)
        out[i, 6] = float("[Co" in r or "[Fe" in r)
        out[i, 7] = float(("METAL" in lc) or ("METAL" in rc))
        out[i, 8] = atp_cons
        out[i, 9] = gtp_cons
        out[i, 10] = nad_cleaved
        out[i, 11] = atp_pi_only
        out[i, 12] = float(atp_cons and only_pi_rhs)
        out[i, 13] = atp_trunc_lig
        out[i, 14] = nad_lig_join

    has_pi = mech_raw[:, fi["has_pi"]]
    has_ppi = mech_raw[:, fi["has_ppi"]]
    has_atp_adp = mech_raw[:, fi["has_atp_adp"]]
    has_ntp_ppi = mech_raw[:, fi["has_ntp_ppi"]]
    has_gdp = mech_raw[:, fi["has_gdp"]]
    has_coa = mech_raw[:, fi["has_coa"]]
    sr_aa = mech_raw[:, sr_off + si["alpha_amino_acid"]]
    out[:, 15] = has_atp_adp * has_pi
    out[:, 16] = has_gdp * has_pi
    out[:, 17] = has_ntp_ppi * np.maximum(has_coa, sr_aa)
    out[:, 18] = mech_raw[:, fi["is_iso"]] * np.maximum(has_ppi, np.maximum(has_pi, np.maximum(has_ntp_ppi, out[:, 8])))
    for k in range(5):
        out[:, 19 + k] = (np.abs(mech_raw[:, atom_off + k]) < 1e-4).astype(np.float32)
    return out


def build_rule_delta_v4(ec_df: pd.DataFrame) -> np.ndarray:
    """24-column correction matrix calibrated strictly against enzyme conservation laws."""
    D = np.zeros((len(ec_df), 24), dtype=np.float32)
    for r, row in enumerate(ec_df.itertuples()):
        ec1, ec2, ec3 = row.ec1, row.ec2, row.ec3
        if ec1 == "7":
            D[r, 11] = 10.0
            D[r, 12] = 5.0
        elif ec3 == "3.6.3":
            D[r, 11] = 2.5
        elif ec1 in ("2", "3", "4", "5"):
            D[r, 11] = -3.0

        if ec1 == "6":
            D[r, 13] = 6.5
            D[r, 14] = 8.0 if ec3 == "6.5.1" else 2.5
        elif ec1 in ("3", "4", "5"):
            D[r, 13] = -2.5

        if ec1 == "6":
            D[r, 15] = 4.5
        elif ec2 == "2.7":
            D[r, 15] = -4.0

        if ec3 == "6.3.4":
            D[r, 16] = 7.5
        elif ec1 == "6":
            D[r, 16] = 2.0
        elif ec2 == "2.4":
            D[r, 16] = -5.0

        if ec3 in ("6.1.1", "6.2.1"):
            D[r, 17] = 6.5
        elif ec1 == "6":
            D[r, 17] = 3.0
        elif ec3 in ("2.7.7", "2.7.8"):
            D[r, 17] = -4.5

        if ec1 == "5":
            D[r, 18] = -7.5
        elif ec1 == "6":
            D[r, 18] = 3.0
    return D
