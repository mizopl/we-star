#!/usr/bin/env python3
"""rules_v2.py — Deterministic biochemical reaction-center & substrate-to-EC compatibility matrices.

Strictly indexes named columns from `features_v2.py` (`FLAG_IDX`, `FG_IDX`, `SUB_IDX`)
against denoised `text2EC.csv` (`l1, l2, l3_clean, l4`) with ZERO test-label dependence.
"""
from __future__ import annotations

import pathlib
import sys
import numpy as np
import pandas as pd

ROOT = pathlib.Path(__file__).resolve().parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import features_v2 as f2  # noqa: E402


def build_rule_matrices_v2(ec_df: pd.DataFrame) -> tuple[np.ndarray, np.ndarray]:
    """Return `(W_ec123, W_l4)` matching `features_v2.mech` shape `(D_mech,)`."""
    n_ec = len(ec_df)
    n_flags = len(f2.FLAG_NAMES)
    n_fg = len(f2.FG_NAMES)
    n_atoms = len(f2.ATOM_LIST)
    n_sub = len(f2.SUB_NAMES)
    dim = n_flags + 2 * n_fg + n_atoms + 2 * n_sub

    dfg_off = n_flags
    afg_off = n_flags + n_fg
    atom_off = n_flags + 2 * n_fg
    sr_off = atom_off + n_atoms
    sp_off = sr_off + n_sub
    fi = f2.FLAG_IDX
    fgi = f2.FG_IDX
    si = f2.SUB_IDX

    W = np.zeros((n_ec, dim), dtype=np.float32)
    W4 = np.zeros((n_ec, dim), dtype=np.float32)

    for r, row in enumerate(ec_df.itertuples()):
        ec1, ec2, ec3 = row.ec1, row.ec2, row.ec3
        l2 = str(row.l2).lower()
        l3 = str(row.l3_clean).lower()
        l4 = str(row.l4).lower()
        txt123 = f"{row.l1} ; {l2} ; {l3}".lower()

        # --- Level 1 Global Gates (strong positive + negative constraints) ---
        W[r, fi["is_iso"]] = 6.0 if ec1 == "5" else -3.5
        W[r, fi["is_chiral_only"]] = 8.0 if ec2 == "5.1" else (2.0 if ec1 == "5" else -4.0)
        W[r, fi["is_ez_only"]] = 8.0 if ec2 == "5.2" else (2.0 if ec1 == "5" else -4.0)
        W[r, fi["is_constit_iso"]] = 5.5 if ec2 in ("5.3", "5.4", "5.5") else (1.5 if ec1 == "5" else -3.0)

        W[r, fi["is_redox"]] = 4.5 if ec1 == "1" else -2.5
        W[r, fi["org_split_h2o"]] = 4.5 if ec1 == "3" else (-1.0 if ec1 in ("2", "5", "6") else 0.0)
        W[r, fi["org_dehydr_h2o"]] = 6.0 if (ec3 == "4.2.1" or "dehydratase" in l3 or "hydro-lyase" in l3) else (1.5 if ec1 == "4" else -1.5)
        W[r, fi["org_split_no_h2o"]] = 4.5 if ec1 == "4" else (-1.0 if ec1 in ("1", "3", "5", "6") else 0.0)
        W[r, fi["org_join_atp"]] = 5.0 if ec1 == "6" else (-1.5 if ec1 in ("3", "4", "5") else 0.0)
        W[r, fi["org_2to2_transfer"]] = 4.0 if ec1 == "2" else (-0.8 if ec1 in ("4", "5") else 0.0)

        # --- Oxidoreductase Acceptors & Donors (EC 1.x.y) ---
        if "(nad+)" in txt123 or ("nad" in txt123 and "nadp" not in txt123):
            W[r, fi["has_nad"]] = 3.5
            W[r, fi["has_nadp"]] = -1.5
        elif "nadp" in txt123 and "nad or nadp" not in txt123:
            W[r, fi["has_nadp"]] = 3.5
            W[r, fi["has_nad"]] = -1.5
        if "nad" in txt123:
            W[r, fi["has_nad_any"]] = 4.5

        W[r, fi["has_2og_o2"]] = 7.5 if ec3 == "1.14.11" else (2.5 if ec1 == "1" else -3.5)
        if ec3 in ("1.14.13", "1.14.14", "1.14.12", "1.14.15", "1.14.19") or "monooxygenase" in l3:
            W[r, fi["has_nad_o2"]] = 6.0
        elif ec1 == "1":
            W[r, fi["has_nad_o2"]] = 1.5
        else:
            W[r, fi["has_nad_o2"]] = -2.5

        if ec3.endswith(".3") and ec1 == "1" or ec3 in ("1.13.11", "1.13.12") or ("oxygen" in l3 and "paired" not in l2):
            W[r, fi["o2_only_redox"]] = 5.0
        elif ec1 == "1":
            W[r, fi["o2_only_redox"]] = 1.5
        else:
            W[r, fi["o2_only_redox"]] = -2.0

        if ec2 == "1.11" or "peroxidase" in l3 or "peroxide" in l2:
            W[r, fi["has_h2o2"]] = 6.5
        elif ec1 == "1":
            W[r, fi["has_h2o2"]] = 1.0
        else:
            W[r, fi["has_h2o2"]] = -2.0

        if "quinone" in l3 or (ec1 == "1" and ec3.endswith(".5")):
            W[r, fi["has_quinone"]] = 6.5
            W[r, fi["has_dcpip"]] = 3.5
        elif ec1 == "1" and (ec3.endswith(".99") or ec3.endswith(".98") or "acceptor" in l3):
            W[r, fi["has_dcpip"]] = 4.5
        elif ec1 == "1":
            W[r, fi["has_dcpip"]] = 2.0
        else:
            W[r, fi["has_dcpip"]] = -3.0
            W[r, fi["has_quinone"]] = -2.5

        if "iron-sulfur" in l3 or (ec1 == "1" and ec3.endswith(".7")):
            W[r, fi["has_fes"]] = 6.5
        if "flavin" in l3 or "fad" in l3 or "fmn" in l3:
            W[r, fi["has_fad"]] = 4.5
        elif ec1 == "1":
            W[r, fi["has_fad"]] = 1.5

        # Donor groups for EC 1.x & EC 5.x
        if "ch-oh" in txt123 or "alcohol" in txt123:
            W[r, fi["ch_oh_co"]] = 4.5
        if "aldehyde or oxo" in l2 or "aldehyde" in txt123:
            W[r, fi["ald_carbox"]] = 4.0
            W[r, afg_off + fgi["aldehyde"]] = 1.8
        if "ch-ch" in txt123 or "desaturase" in l3:
            W[r, afg_off + fgi["alkene"]] = 2.2
        if "ch-nh2" in l2 or "ch-nh" in l2 or "transaminase" in l3:
            W[r, fi["amine_co"]] = 4.0
        if "diphenol" in l2 or ec2 == "1.13":
            W[r, sr_off + si["catechol"]] = 3.5 if ec3 == "1.13.11" or ec2 == "1.10" else 1.5

        # --- Transferase Pairs (EC 2.x.y) ---
        W[r, fi["has_sam_sah"]] = 8.0 if ec3 == "2.1.1" else (2.5 if ec1 == "2" else -4.0)
        W[r, fi["has_glut_2og"]] = 7.5 if ec3 == "2.6.1" else (2.0 if ec2 == "2.6" else -2.5)
        W[r, fi["has_paps"]] = 7.5 if (ec3 == "2.8.2" or "sulfotransferase" in txt123) else -2.0
        W[r, fi["has_gsh"]] = 6.0 if ("glutathione" in txt123 or "glutathione" in l4) else 0.0
        W[r, fi["has_prpp"]] = 5.5 if ec3 == "2.4.2" else (1.5 if ec2 == "2.4" else 0.0)
        if ec2 == "2.7":
            W[r, fi["has_atp_adp"]] = 5.5
            if ec3 == "2.7.1": W[r, afg_off + fgi["alcohol_any"]] = 1.2
            if ec3 == "2.7.2": W[r, afg_off + fgi["carboxyl"]] = 2.0
            if ec3 == "2.7.3": W[r, sr_off + si["guanidine"]] = 2.5
            if ec3 == "2.7.4": W[r, afg_off + fgi["phospho_anhydride"]] = 2.5
        elif ec1 == "6":
            W[r, fi["has_atp_adp"]] = 3.0
        elif ec1 in ("3", "4", "5"):
            W[r, fi["has_atp_adp"]] = -2.5

        W[r, fi["has_ntp_ppi"]] = 6.0 if ec3 in ("2.7.7", "2.7.8") else (3.5 if ec1 == "6" else -1.0)
        W[r, fi["has_atp_amp"]] = 6.5 if ec1 == "6" else (2.5 if ec3 == "2.7.9" else -2.0)

        if ec2 == "2.3" or "acyltransferase" in l3:
            W[r, fi["has_coa"]] = 4.5
        elif ec3 == "3.1.2":
            W[r, fi["has_coa"]] = 3.0
        elif ec2 == "6.2":
            W[r, fi["has_coa"]] = 4.5

        if ec2 == "2.4" or "glycosyltransferase" in txt123:
            W[r, fi["has_udp"]] = 4.5
            W[r, fi["has_gdp"]] = 4.5

        # --- Hydrolases (EC 3.x.y) ---
        if ec2 == "3.1":
            W[r, fi["ester_h2o"]] = 4.0
            if ec3 == "3.1.1":
                W[r, afg_off + fgi["ester"]] = 2.2
                W[r, afg_off + fgi["lactone"]] = 2.0
            elif ec3 == "3.1.2":
                W[r, afg_off + fgi["thioester"]] = 3.5
            elif ec3 in ("3.1.3", "3.1.4"):
                W[r, fi["phos_h2o_no_atp"]] = 6.0
                W[r, fi["has_pi"]] = 3.0
            elif ec3 == "3.1.6":
                W[r, afg_off + fgi["sulfate"]] = 4.0

        W[r, fi["free_glc_gain"]] = 6.5 if ec3 == "3.2.1" else (2.0 if ec2 == "3.2" else -1.0)
        if ec3 == "3.2.2":
            W[r, sr_off + si["purine"]] = 2.5
            W[r, sr_off + si["pyrimidine"]] = 2.5
            W[r, fi["has_h2o_r"]] = 1.5

        if ec3 in ("3.3.1", "3.3.2") or "ether" in l2:
            W[r, afg_off + fgi["ether"]] = 3.5
            W[r, afg_off + fgi["epoxide"]] = 4.0 if ec3 == "3.3.2" else 0.0

        if ec2 in ("3.4", "3.5"):
            W[r, fi["amide_h2o"]] = 3.5
            if ec2 == "3.4":
                W[r, fi["assay_chromogen"]] = 2.5
            if ec3 == "3.5.1":
                W[r, afg_off + fgi["amide"]] = 2.0
            elif ec3 == "3.5.2":
                W[r, afg_off + fgi["cyclic_amide"]] = 3.5
            elif ec3 in ("3.5.3", "3.5.4"):
                W[r, afg_off + fgi["amidine"]] = 3.5
            elif ec3 == "3.5.5":
                W[r, afg_off + fgi["nitrile"]] = 4.5

        if ec2 == "3.6":
            W[r, afg_off + fgi["phospho_anhydride"]] = 3.5
        if ec2 == "3.8":
            W[r, afg_off + fgi["halide"]] = 4.5

        # --- Lyases (EC 4.x.y) ---
        if ec3 == "4.1.1" or "decarboxylase" in l3:
            W[r, fi["has_co2"]] = 5.5 if ec3 == "4.1.1" else 3.0
        elif ec2 == "6.4":
            W[r, fi["has_co2"]] = 4.0
        if ec3 == "4.1.2":
            W[r, fi["has_hcn"]] = 6.0
            W[r, afg_off + fgi["aldehyde"]] = 1.8
        if ec3 == "4.2.3":
            W[r, fi["prenyl_ppi"]] = 7.5
            W[r, sr_off + si["prenyl"]] = 2.5
        elif ec3 == "2.5.1":
            W[r, fi["prenyl_ppi"]] = 2.5
        if ec2 == "4.3":
            W[r, fi["has_nh3"]] = 5.0
        if ec2 == "4.4":
            W[r, afg_off + fgi["thiol"]] = 2.5
        if ec2 == "4.5":
            W[r, afg_off + fgi["halide"]] = 4.5

        # --- Isomerases (EC 5.x) ---
        if ec3 == "5.1.1": W[r, sr_off + si["alpha_amino_acid"]] = 3.5
        if ec3 == "5.1.2": W[r, sr_off + si["alpha_oh_acid"]] = 3.5
        if ec3 in ("5.1.3", "5.3.1"):
            W[r, sr_off + si["pyranose"]] = 3.0
            W[r, sr_off + si["furanose"]] = 2.5

        # --- Ligases (EC 6.x) ---
        if ec2 == "6.2":
            W[r, fi["has_coa"]] = 4.5
            W[r, fi["has_atp_amp"]] = 4.5
        if ec3 == "6.3.1":
            W[r, fi["has_nh3"]] = 4.0
        if ec3 in ("6.1.1", "6.3.2"):
            W[r, sr_off + si["alpha_amino_acid"]] = 3.0
        if ec2 == "6.4":
            W[r, fi["has_co2"]] = 5.0

        # ===================================================================
        # W4: Intra-EC3 Substrate & Directional-Cofactor Rules for L4 ranking
        # ===================================================================
        if not l4:
            continue

        # Exact directional cofactor inside EC3 (vital in 1.1.1, 1.2.1, 1.3.1, 1.5.1, etc.)
        if "(nad+)" in l4 or "(nadh)" in l4:
            W4[r, fi["has_nad"]] += 4.5
            W4[r, fi["has_nadp"]] -= 2.5
        if "(nadp+)" in l4 or "(nadph)" in l4:
            W4[r, fi["has_nadp"]] += 4.5
            W4[r, fi["has_nad"]] -= 2.5
        if "(nad+)" in l4 or "dehydrogenase" in l4:
            W4[r, fi["nad_ox"]] += 1.5
            W4[r, fi["nadp_ox"]] += 1.5
        if "reductase" in l4:
            W4[r, fi["nad_red"]] += 1.5
            W4[r, fi["nadp_red"]] += 1.5

        if "gtp" in l4 or "guanosine" in l4:
            W4[r, fi["has_gdp"]] += 3.0
            W4[r, sr_off + si["purine"]] += 2.0
        if "udp" in l4 or "utp" in l4:
            W4[r, fi["has_udp"]] += 3.0
            W4[r, sr_off + si["pyrimidine"]] += 2.0
        if "coa" in l4:
            W4[r, fi["has_coa"]] += 3.0
        if "glutathione" in l4:
            W4[r, fi["has_gsh"]] += 4.0

        # Reactant + Product Substrate SMARTS matches against L4 enzyme name
        sub_kw_map = [
            ("pyranose", ("glucos", "galactos", "xylos", "mannos", "glucuron", "rhamnos", "sugar", "hexos", "pyran")),
            ("furanose", ("ribos", "arabinos", "fructos", "pentos", "furan", "nucleosid")),
            ("purine", ("adenos", "guanos", "inosin", "xanthin", "hypoxanth", "purine", "amp ", "gmp ")),
            ("pyrimidine", ("uridin", "cytidin", "thymid", "orot", "pyrimidin", "uracil", "cytosine")),
            ("steroid_core", ("steroid", "hydroxysteroid", "cholest", "cortis", "testosteron", "estradiol", "andro", "cholate", "bile", "ecdyson", "brassin")),
            ("alpha_amino_acid", ("amino-acid", "amino acid", "alanine", "glycine", "valine", "leucine", "serine", "threonine", "cysteine", "methionine", "aspartate", "glutamate", "lysine", "arginine", "histidine", "phenylalanine", "tyrosine", "tryptophan", "proline")),
            ("indole", ("indole", "tryptophan", "serotonin", "melatonin", "auxin", "kynuren")),
            ("catechol", ("catechol", "caffe", "dopamin", "protocatechu", "diphenol")),
            ("phenol_ring", ("phenol", "salicyl", "tyrosin", "coumar", "vanill", "nitrophenol")),
            ("phenylpropanoid", ("cinnam", "coumar", "caffe", "ferul", "sinap", "lign")),
            ("chromone_flavonoid", ("flavon", "chalcon", "isoflav", "catechin", "anthocyan", "quercetin", "coumarin")),
            ("long_acyl", ("fatty", "long-chain", "acyl-", "palmit", "stear", "ole", "myrist", "alkane", "ceramide", "lipase")),
            ("prenyl", ("terpene", "geranyl", "farnesyl", "prenyl", "limonene", "pinene", "squalene", "caroten", "isopren")),
            ("alpha_oh_acid", ("lactate", "malate", "glycolate", "hydroxyacid", "hydroxy-acid", "mandelate", "tartrate", "isocitrate")),
            ("alpha_oxo_acid", ("pyruvate", "oxoglutarate", "glyoxylate", "oxaloacetate", "oxo-acid", "oxoacid", "ketoglutarate", "keto-acid")),
            ("choline_quat", ("choline", "betaine", "carnitine")),
            ("guanidine", ("guanid", "arginin", "agmatin", "creatin")),
            ("imidazole", ("imidazol", "histidin", "histamin", "urocan")),
            ("pyridine", ("pyridin", "nicotin")),
            ("sugar_phos_bond", ("phosphate", "phospho", "6-phosphate", "1-phosphate")),
            ("haloarom", ("halo", "chloro", "bromo", "fluoro", "dehalogen")),
            ("haloalk", ("halo", "chloro", "bromo", "fluoro", "dehalogen")),
            ("urea_moiety", ("urea", "ureid", "allantoin")),
        ]
        for s_key, kws in sub_kw_map:
            if any(k in l4 for k in kws):
                W4[r, sr_off + si[s_key]] += 2.0
                W4[r, sp_off + si[s_key]] += 2.0

        # Specific FG signals in L4
        if "lacton" in l4: W4[r, afg_off + fgi["lactone"]] += 3.5
        if "ester" in l4 or "acetyl" in l4: W4[r, afg_off + fgi["ester"]] += 1.5
        if "nitrile" in l4: W4[r, afg_off + fgi["nitrile"]] += 3.5
        if "thio" in l4 or "disulfide" in l4:
            W4[r, afg_off + fgi["thiol"]] += 2.0
            W4[r, afg_off + fgi["thioether"]] += 2.0
            W4[r, afg_off + fgi["disulfide"]] += 2.5

    return W, W4
