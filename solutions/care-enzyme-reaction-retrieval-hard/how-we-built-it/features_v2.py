#!/usr/bin/env python3
"""features_v2.py — Zero-leakage, charge-normalized, stereo- & bond-complete RDKit + BGE feature extraction for CARE Task 2.

STRICT ANTI-LEAKAGE INVARIANT:
  - Reads ONLY `Reaction` SMILES (`reactants>>products`).
  - NEVER accesses `Mapped Reaction`, `Reaction Text`, or test `EC number`.
  - Candidate metadata comes strictly from official README files:
    `processed_data/text2EC.csv`, `processed_data/EC_list.txt`, and `processed_data/protein2EC_clustered50.csv`.
"""
from __future__ import annotations

import argparse
import pathlib
import re
import time
from collections import Counter
from typing import Dict, List

import numpy as np
import pandas as pd
from rdkit import Chem, RDLogger
from rdkit.Chem import MACCSkeys, rdFingerprintGenerator, rdMolDescriptors
from rdkit.Chem.MolStandardize import rdMolStandardize
from scipy import sparse

RDLogger.DisableLog("rdApp.*")

ROOT = pathlib.Path(__file__).resolve().parent
DATA_ROOT = ROOT / "data" / "CARE_datasets"
CACHE_DIR = ROOT / "cache"

_UNCHARGER = rdMolStandardize.Uncharger()

# Universal cofactors / redox / inorganic transfer reagents excluded from `sub_diff` / `sub_r` / `sub_p`
# NOTE: metabolic small substrates like pyruvate, glutamate, glucose, acetate, 2OG, succinate stay in `sub_*`
# while STILL detected as explicit biochemical flags!
TRUE_COFACTOR_PATTERNS: Dict[str, str] = {
    "NAD+": "NC(=O)c1ccc[n+](C2OC(COP(=O)(O)OP(=O)(O)OCC3OC(n4cnc5c(N)ncnc54)C(O)C3O)C(O)C2O)c1",
    "NADH": "NC(=O)C1=CN(C2OC(COP(=O)(O)OP(=O)(O)OCC3OC(n4cnc5c(N)ncnc54)C(O)C3O)C(O)C2O)C=CC1",
    "NADP+": "NC(=O)c1ccc[n+](C2OC(COP(=O)(O)OP(=O)(O)OCC3OC(n4cnc5c(N)ncnc54)C(OP(=O)(O)O)C3O)C(O)C2O)c1",
    "NADPH": "NC(=O)C1=CN(C2OC(COP(=O)(O)OP(=O)(O)OCC3OC(n4cnc5c(N)ncnc54)C(OP(=O)(O)O)C3O)C(O)C2O)C=CC1",
    "ATP": "Nc1ncnc2c1ncn2C1OC(COP(=O)(O)OP(=O)(O)OP(=O)(O)O)C(O)C1O",
    "ADP": "Nc1ncnc2c1ncn2C1OC(COP(=O)(O)OP(=O)(O)O)C(O)C1O",
    "AMP": "Nc1ncnc2c1ncn2C1OC(COP(=O)(O)O)C(O)C1O",
    "GTP": "Nc1nc2c(ncn2C2OC(COP(=O)(O)OP(=O)(O)OP(=O)(O)O)C(O)C2O)c(=O)[nH]1",
    "GDP": "Nc1nc2c(ncn2C2OC(COP(=O)(O)OP(=O)(O)O)C(O)C2O)c(=O)[nH]1",
    "GMP": "Nc1nc2c(ncn2C2OC(COP(=O)(O)O)C(O)C2O)c(=O)[nH]1",
    "UTP": "O=c1ccn(C2OC(COP(=O)(O)OP(=O)(O)OP(=O)(O)O)C(O)C2O)c(=O)[nH]1",
    "UDP": "O=c1ccn(C2OC(COP(=O)(O)OP(=O)(O)O)C(O)C2O)c(=O)[nH]1",
    "UMP": "O=c1ccn(C2OC(COP(=O)(O)O)C(O)C2O)c(=O)[nH]1",
    "CTP": "Nc1ccn(C2OC(COP(=O)(O)OP(=O)(O)OP(=O)(O)O)C(O)C2O)c(=O)n1",
    "CDP": "Nc1ccn(C2OC(COP(=O)(O)OP(=O)(O)O)C(O)C2O)c(=O)n1",
    "CMP": "Nc1ccn(C2OC(COP(=O)(O)O)C(O)C2O)c(=O)n1",
    "dATP": "Nc1ncnc2c1ncn2C1CC(O)C(COP(=O)(O)OP(=O)(O)OP(=O)(O)O)O1",
    "dADP": "Nc1ncnc2c1ncn2C1CC(O)C(COP(=O)(O)OP(=O)(O)O)O1",
    "dTTP": "Cc1cn(C2CC(O)C(COP(=O)(O)OP(=O)(O)OP(=O)(O)O)O2)c(=O)[nH]c1=O",
    "SAM": "C[S+](CCC(N)C(=O)O)CC1OC(n2cnc3c(N)ncnc32)C(O)C1O",
    "SAH": "Nc1ncnc2c1ncn2C1OC(CSCCC(N)C(=O)O)C(O)C1O",
    "CoA": "CC(C)(COP(=O)(O)OP(=O)(O)OCC1OC(n2cnc3c(N)ncnc32)C(O)C1OP(=O)(O)O)C(O)C(=O)NCCC(=O)NCCS",
    "FAD": "Cc1cc2nc3c(=O)[nH]c(=O)nc-3n(CC(O)C(O)C(O)COP(=O)(O)OP(=O)(O)OCC3OC(n4cnc5c(N)ncnc54)C(O)C3O)c2cc1C",
    "FADH2": "Cc1cc2c(cc1C)N(CC(O)C(O)C(O)COP(=O)(O)OP(=O)(O)OCC1OC(n3cnc4c(N)ncnc43)C(O)C1O)C1=C(N2)C(=O)NC(=O)N1",
    "FMN": "Cc1cc2nc3c(=O)[nH]c(=O)nc-3n(CC(O)C(O)C(O)COP(=O)(O)O)c2cc1C",
    "PAPS": "Nc1ncnc2c1ncn2C1OC(COP(=O)(O)OS(=O)(=O)O)C(O)C1OP(=O)(O)O",
    "PAP": "Nc1ncnc2c1ncn2C1OC(COP(=O)(O)O)C(O)C1OP(=O)(O)O",
    "PRPP": "O=P(O)(O)OCC1OC(OP(=O)(O)OP(=O)(O)O)C(O)C1O",
    "GSH": "NC(CCC(=O)NC(CS)C(=O)NCC(=O)O)C(=O)O",
    "DCPIP_ox": "O=C1C=CC(=Nc2cc(Cl)c(O)c(Cl)c2)C=C1",
    "DCPIP_red": "Oc1ccc(Nc2cc(Cl)c(O)c(Cl)c2)cc1",
    "Quinone": "O=C1C=CC(=O)C=C1",
    "Hydroquinone": "Oc1ccc(O)cc1",
    "H2O": "O",
    "O2": "O=O",
    "H2O2": "OO",
    "CO2": "O=C=O",
    "HCO3": "O=C(O)O",
    "NH3": "N",
    "Pi": "O=P(O)(O)O",
    "PPi": "O=P(O)(O)OP(=O)(O)O",
    "PyridoxalP": "Cc1ncc(COP(=O)(O)O)c(C=O)c1O",
}

ASSAY_AND_HUB_PATTERNS: Dict[str, str] = {
    "2OG": "O=C(O)CCC(=O)C(=O)O",
    "Succinate": "O=C(O)CCC(=O)O",
    "Glutamate": "NC(CCC(=O)O)C(=O)O",
    "Glutamine": "NC(=O)CCC(N)C(=O)O",
    "Pyruvate": "CC(=O)C(=O)O",
    "Acetate": "CC(=O)O",
    "Formate": "O=CO",
    "HCN": "C#N",
    "H2S": "S",
    "pNP": "O=[N+]([O-])c1ccc(O)cc1",
    "pNA": "Nc1ccc([N+](=O)[O-])cc1",
    "AMC": "Cc1cc(=O)oc2cc(N)ccc12",
    "FreeGlucose": "OCC1OC(O)C(O)C(O)C1O",
}


def uncharge_biochem(mol: Chem.Mol) -> Chem.Mol:
    """Safely neutralize carboxylate/phosphate/amine protonation states including zwitterions."""
    m = _UNCHARGER.uncharge(mol)
    changed = False
    rw = Chem.RWMol(m)
    for atom in rw.GetAtoms():
        fc = atom.GetFormalCharge()
        sym = atom.GetSymbol()
        if fc == -1 and sym in ("O", "S"):
            # Do NOT alter nitro [N+]([O-])=O!
            nbr_n_pos = any(nb.GetSymbol() == "N" and nb.GetFormalCharge() > 0 for nb in atom.GetNeighbors())
            if not nbr_n_pos:
                atom.SetFormalCharge(0)
                atom.SetNumExplicitHs(atom.GetTotalNumHs() + 1)
                changed = True
        elif fc == 1 and sym == "N" and not atom.GetIsAromatic() and atom.GetTotalDegree() < 4:
            # e.g. [NH3+]R -> NH2R (keep quaternary NR4+ or aromatic pyridinium [n+])
            atom.SetFormalCharge(0)
            atom.SetNumExplicitHs(max(0, atom.GetTotalNumHs() - 1))
            changed = True
    if changed:
        out = rw.GetMol()
        try:
            Chem.SanitizeMol(out)
            return out
        except Exception:
            return m
    return m


def _build_lut(patterns: Dict[str, str]) -> Dict[str, str]:
    lut: Dict[str, str] = {}
    for name, smi in patterns.items():
        m = Chem.MolFromSmiles(smi)
        if m is not None:
            um = uncharge_biochem(m)
            lut[Chem.MolToSmiles(um, isomericSmiles=False)] = name
            lut[Chem.MolToSmiles(m, isomericSmiles=False)] = name
    return lut


COFACTOR_LUT = _build_lut(TRUE_COFACTOR_PATTERNS)
SPECIES_LUT = _build_lut(ASSAY_AND_HUB_PATTERNS)

# Functional group SMARTS (30)
FG_SMARTS = {
    "alcohol_prim": Chem.MolFromSmarts("[CX4;H2][OX2H1]"),
    "alcohol_sec": Chem.MolFromSmarts("[CX4;H1]([#6])[OX2H1]"),
    "alcohol_any": Chem.MolFromSmarts("[CX4][OX2H1]"),
    "carbonyl": Chem.MolFromSmarts("[CX3]=[OX1]"),
    "aldehyde": Chem.MolFromSmarts("[CX3H1](=[OX1])[#6]"),
    "ketone": Chem.MolFromSmarts("[#6][CX3](=[OX1])[#6]"),
    "carboxyl": Chem.MolFromSmarts("[CX3](=[OX1])[OX2H1]"),
    "ester": Chem.MolFromSmarts("[#6][CX3](=[OX1])[OX2][#6]"),
    "lactone": Chem.MolFromSmarts("[CX3;R](=[OX1])[OX2;R][#6;R]"),
    "amide": Chem.MolFromSmarts("[NX3][CX3](=[OX1])[#6]"),
    "cyclic_amide": Chem.MolFromSmarts("[NX3;R][CX3;R](=[OX1])[#6;R]"),
    "amine_prim": Chem.MolFromSmarts("[NX3;H2][CX4]"),
    "amine_any": Chem.MolFromSmarts("[NX3;H2,H1,H0;!$(NC=O);!$([n])]"),
    "imine": Chem.MolFromSmarts("[CX3]=[NX2]"),
    "amidine": Chem.MolFromSmarts("[NX3][CX3]=[NX2]"),
    "alkene": Chem.MolFromSmarts("[CX3]=[CX3]"),
    "alkyne": Chem.MolFromSmarts("[CX2]#[CX2]"),
    "phosphate_ester": Chem.MolFromSmarts("[PX4](=[OX1])([OX2])[OX2][#6]"),
    "phospho_anhydride": Chem.MolFromSmarts("[PX4](=[OX1])[OX2][PX4](=[OX1])"),
    "halide": Chem.MolFromSmarts("[#6][F,Cl,Br,I]"),
    "thiol": Chem.MolFromSmarts("[CX4][SX2H1]"),
    "thioester": Chem.MolFromSmarts("[#6][CX3](=[OX1])[SX2][#6]"),
    "thioether": Chem.MolFromSmarts("[#6][SX2][#6]"),
    "disulfide": Chem.MolFromSmarts("[SX2][SX2]"),
    "ether": Chem.MolFromSmarts("[CX4][OX2][CX4]"),
    "epoxide": Chem.MolFromSmarts("[OX2r3]1[#6r3][#6r3]1"),
    "phenol": Chem.MolFromSmarts("[c][OX2H1]"),
    "glycosidic_acetal": Chem.MolFromSmarts("[CX4;R]([OX2][#6])[OX2;R][CX4;R]"),
    "hemiacetal_sugar": Chem.MolFromSmarts("[CX4;R]([OX2H1])[OX2;R][CX4;R]"),
    "nitrile": Chem.MolFromSmarts("[CX2]#[NX1]"),
    "sulfate": Chem.MolFromSmarts("[SX4](=[OX1])(=[OX1])([OX2])[OX2]"),
    "nitro": Chem.MolFromSmarts("[$([NX3](=O)=O),$([NX3+](=O)[O-])]"),
}
FG_NAMES = list(FG_SMARTS.keys())

# Substrate-class SMARTS for reactant & product profiles (helps L3 substrate scope & intra-EC3 L4!)
SUB_SMARTS = {
    "pyranose": Chem.MolFromSmarts("[C;R]1[O;R][C;R][C;R][C;R][C;R]1"),
    "furanose": Chem.MolFromSmarts("[C;R]1[O;R][C;R][C;R][C;R]1"),
    "purine": Chem.MolFromSmarts("n1cnc2ncnc12"),
    "pyrimidine": Chem.MolFromSmarts("n1ccnc(=O)[nH]1"),
    "steroid_core": Chem.MolFromSmarts("[C,c;R]12[C,c;R][C,c;R][C,c;R]3[C,c;R]([C,c;R]1)[C,c;R][C,c;R][C,c;R]1[C,c;R]3[C,c;R][C,c;R][C,c;R]21"),
    "alpha_amino_acid": Chem.MolFromSmarts("[NX3;H2,H1][CX4][CX3](=[OX1])[OX2H1]"),
    "indole": Chem.MolFromSmarts("c1ccc2[nH]ccc2c1"),
    "catechol": Chem.MolFromSmarts("[c]([OX2H1])[c]([OX2H1])"),
    "phenol_ring": Chem.MolFromSmarts("c1ccccc1[OX2H1]"),
    "phenylpropanoid": Chem.MolFromSmarts("c1ccccc1[CH]=[CH][CX3](=[OX1])"),
    "chromone_flavonoid": Chem.MolFromSmarts("O=c1ccc2ccccc2o1"),
    "long_acyl": Chem.MolFromSmarts("[CH2][CH2][CH2][CH2][CH2][CH2]"),
    "prenyl": Chem.MolFromSmarts("[CH3]C([CH3])=[CH][CH2]"),
    "alpha_oh_acid": Chem.MolFromSmarts("[OX2H1][CX4][CX3](=[OX1])[OX2H1]"),
    "alpha_oxo_acid": Chem.MolFromSmarts("[CX3](=[OX1])[CX3](=[OX1])[OX2H1]"),
    "choline_quat": Chem.MolFromSmarts("[NX4+]([CH3])([CH3])[CH3]"),
    "guanidine": Chem.MolFromSmarts("[NX3]C(=[NX2])[NX3]"),
    "imidazole": Chem.MolFromSmarts("c1c[nH]cn1"),
    "pyridine": Chem.MolFromSmarts("n1ccccc1"),
    "sugar_phos_bond": Chem.MolFromSmarts("[C;R]1([O,OH])[O;R][C;R][C;R]([CH2,OX2]P(=O))[C;R]1"),
    "haloarom": Chem.MolFromSmarts("[c][F,Cl,Br,I]"),
    "haloalk": Chem.MolFromSmarts("[CX4][F,Cl,Br,I]"),
    "aromatic_ring": Chem.MolFromSmarts("c1ccccc1"),
    "urea_moiety": Chem.MolFromSmarts("[NX3][CX3](=[OX1])[NX3]"),
}
SUB_NAMES = list(SUB_SMARTS.keys())
ATOM_LIST = ("C", "N", "O", "P", "S", "F", "Cl", "Br", "I")
FLAG_NAMES = [
    "is_iso", "is_chiral_only", "is_ez_only", "is_constit_iso",
    "is_redox", "org_split_h2o", "org_dehydr_h2o", "org_split_no_h2o", "org_join_atp", "org_2to2_transfer",
    "nad_ox", "nad_red", "nadp_ox", "nadp_red", "has_nad", "has_nadp", "has_nad_any",
    "has_atp_adp", "has_atp_amp", "has_ntp_ppi", "has_sam_sah",
    "has_2og_o2", "has_nad_o2", "o2_only_redox", "has_glut_2og",
    "has_fad", "has_dcpip", "has_quinone", "has_fes",
    "has_h2o2", "has_h2o_r", "has_h2o_p", "has_co2", "has_nh3", "has_pi", "has_ppi",
    "has_coa", "has_udp", "has_gdp", "has_paps", "has_prpp", "has_gsh",
    "prenyl_ppi", "free_glc_gain", "assay_chromogen",
    "ch_oh_co", "ald_carbox", "amine_co", "ester_h2o", "amide_h2o",
    "phos_h2o_no_atp", "has_hcn", "d_rings", "d_arom_rings", "d_norg", "d_maxh_norm",
]
FLAG_IDX = {k: i for i, k in enumerate(FLAG_NAMES)}
FG_IDX = {k: i for i, k in enumerate(FG_NAMES)}
SUB_IDX = {k: i for i, k in enumerate(SUB_NAMES)}


def _build_mol_cache(unique_smiles: set[str]):
    gen_r2_ch = rdFingerprintGenerator.GetMorganGenerator(radius=2, fpSize=2048, includeChirality=True)
    gen_r2_2d = rdFingerprintGenerator.GetMorganGenerator(radius=2, fpSize=2048, includeChirality=False)
    gen_r1 = rdFingerprintGenerator.GetMorganGenerator(radius=1, fpSize=1024, includeChirality=False)
    gen_ap = rdFingerprintGenerator.GetAtomPairGenerator(fpSize=1024)

    cache = {}
    for smi in unique_smiles:
        m_raw = Chem.MolFromSmiles(smi)
        if m_raw is None:
            cache[smi] = None
            continue
        m = uncharge_biochem(m_raw)
        csmi_2d = Chem.MolToSmiles(m, isomericSmiles=False)
        csmi_iso = Chem.MolToSmiles(m, isomericSmiles=True)

        cname = COFACTOR_LUT.get(csmi_2d)
        # Dummy-atom * cofactor signatures in CARE
        if cname is None and "*N1c2" in smi and "Nc2" in smi:
            cname = "Flavin_bound"
        elif cname is None and "[Fe" in smi and "[S" in smi:
            cname = "FeS_cluster"

        sname = SPECIES_LUT.get(csmi_2d)
        is_coa_deriv = (cname == "CoA") or ("SCCNC(=O)CCNC(=O)" in csmi_2d)
        is_udp_deriv = (cname in ("UDP", "UTP", "UMP")) or ("O=c1ccn(C2OC(COP(=O)" in csmi_2d)
        is_gdp_deriv = (cname in ("GDP", "GTP", "GMP")) or ("Nc1nc2c(ncn2C2OC(COP(=O)" in csmi_2d)
        is_prenyl_pp = ("CC(C)=CCC" in csmi_2d) and ("OP(=O)(O)OP(=O)" in csmi_2d)

        fp2_ch = gen_r2_ch.GetCountFingerprintAsNumPy(m).astype(np.float32)
        fp2_2d = gen_r2_2d.GetCountFingerprintAsNumPy(m).astype(np.float32)
        fp1 = gen_r1.GetCountFingerprintAsNumPy(m).astype(np.float32)
        fp_ap = gen_ap.GetCountFingerprintAsNumPy(m).astype(np.float32)
        fp_maccs = np.array(MACCSkeys.GenMACCSKeys(m), dtype=np.float32)

        atoms = {a: 0 for a in ATOM_LIST}
        for at in m.GetAtoms():
            sym = at.GetSymbol()
            if sym in atoms:
                atoms[sym] += 1
        rings = m.GetRingInfo().NumRings()
        arom_rings = rdMolDescriptors.CalcNumAromaticRings(m)
        heavy = m.GetNumHeavyAtoms()

        fg = np.array([len(m.GetSubstructMatches(pat)) for pat in FG_SMARTS.values()], dtype=np.float32)
        sub_c = np.array([1.0 if m.HasSubstructMatch(pat) else 0.0 for pat in SUB_SMARTS.values()], dtype=np.float32)

        cache[smi] = {
            "csmi_2d": csmi_2d,
            "csmi_iso": csmi_iso,
            "has_chiral_tag": ("@" in csmi_iso),
            "has_ez_tag": ("/" in csmi_iso or "\\" in csmi_iso),
            "cname": cname,
            "sname": sname,
            "is_cof": cname is not None,
            "is_coa_deriv": is_coa_deriv,
            "is_udp_deriv": is_udp_deriv,
            "is_gdp_deriv": is_gdp_deriv,
            "is_prenyl_pp": is_prenyl_pp,
            "fp2_ch": fp2_ch,
            "fp2_2d": fp2_2d,
            "fp1": fp1,
            "fp_ap": fp_ap,
            "fp_maccs": fp_maccs,
            "atoms": atoms,
            "rings": rings,
            "arom_rings": arom_rings,
            "heavy": heavy,
            "fg": fg,
            "sub_c": sub_c,
        }
    return cache


def featurize_reactions_v2(reactions: List[str], mol_cache=None):
    """Extract dense + multi-FP features strictly from `Reaction` SMILES."""
    if mol_cache is None:
        uniq = set()
        for r in reactions:
            lhs, rhs = r.split(">>")
            for side in (lhs, rhs):
                for s in side.split("."):
                    s = s.strip()
                    if s and s != "[H+]":
                        uniq.add(s)
        mol_cache = _build_mol_cache(uniq)

    n = len(reactions)
    rxn_diff_r2 = np.zeros((n, 2048), dtype=np.float32)
    rxn_diff_r1 = np.zeros((n, 1024), dtype=np.float32)
    rxn_ap_diff = np.zeros((n, 1024), dtype=np.float32)
    rxn_maccs_diff = np.zeros((n, 167), dtype=np.float32)
    sub_diff_r2 = np.zeros((n, 2048), dtype=np.float32)
    sub_r_r2 = np.zeros((n, 2048), dtype=np.float32)
    sub_p_r2 = np.zeros((n, 2048), dtype=np.float32)

    n_flags = len(FLAG_NAMES)
    n_fg = len(FG_NAMES)
    n_sub = len(SUB_NAMES)
    # mech: [flags(56), dfg(n_fg), afg(n_fg), datoms(9), sub_r_cls(n_sub), sub_p_cls(n_sub)]
    mech = np.zeros((n, n_flags + 2 * n_fg + len(ATOM_LIST) + 2 * n_sub), dtype=np.float32)
    fg_idx = {k: i for i, k in enumerate(FG_NAMES)}

    for i, r in enumerate(reactions):
        lhs, rhs = r.split(">>")
        r_mols = [mol_cache.get(s.strip()) for s in lhs.split(".") if s.strip() and s.strip() != "[H+]"]
        p_mols = [mol_cache.get(s.strip()) for s in rhs.split(".") if s.strip() and s.strip() != "[H+]"]
        r_mols = [m for m in r_mols if m is not None]
        p_mols = [m for m in p_mols if m is not None]

        rf2_ch = np.zeros(2048, dtype=np.float32); pf2_ch = np.zeros(2048, dtype=np.float32)
        rf1 = np.zeros(1024, dtype=np.float32); pf1 = np.zeros(1024, dtype=np.float32)
        rap = np.zeros(1024, dtype=np.float32); pap = np.zeros(1024, dtype=np.float32)
        rmac = np.zeros(167, dtype=np.float32); pmac = np.zeros(167, dtype=np.float32)
        rs_fp2 = np.zeros(2048, dtype=np.float32); ps_fp2 = np.zeros(2048, dtype=np.float32)
        rs_fp2_ch = np.zeros(2048, dtype=np.float32); ps_fp2_ch = np.zeros(2048, dtype=np.float32)

        rcof, pcof = set(), set()
        r_spec, p_spec = set(), set()
        r_atoms = {a: 0 for a in ATOM_LIST}; p_atoms = {a: 0 for a in ATOM_LIST}
        r_rings = p_rings = r_arom = p_arom = 0
        r_fg = np.zeros(n_fg, dtype=np.float32); p_fg = np.zeros(n_fg, dtype=np.float32)
        r_sub_c = np.zeros(n_sub, dtype=np.float32); p_sub_c = np.zeros(n_sub, dtype=np.float32)
        r_coa = p_coa = r_udp = p_udp = r_gdp = p_gdp = r_prenyl = False
        r_norg = p_norg = 0
        r_maxh = p_maxh = 0
        r_2d, r_iso, p_2d, p_iso = [], [], [], []
        has_chiral_diff_atoms = False
        has_ez_atoms = False

        for m in r_mols:
            rf2_ch += m["fp2_ch"]; rf1 += m["fp1"]; rap += m["fp_ap"]; rmac += m["fp_maccs"]
            for a, c in m["atoms"].items(): r_atoms[a] += c
            r_rings += m["rings"]; r_arom += m["arom_rings"]
            if m["cname"]: rcof.add(m["cname"])
            if m["sname"]: r_spec.add(m["sname"])
            if m["is_coa_deriv"]: r_coa = True
            if m["is_udp_deriv"]: r_udp = True
            if m["is_gdp_deriv"]: r_gdp = True
            if m["is_prenyl_pp"]: r_prenyl = True
            r_2d.append(m["csmi_2d"]); r_iso.append(m["csmi_iso"])
            if m["has_chiral_tag"]: has_chiral_diff_atoms = True
            if m["has_ez_tag"]: has_ez_atoms = True
            if not m["is_cof"]:
                rs_fp2 += m["fp2_2d"]
                rs_fp2_ch += m["fp2_ch"]
                r_fg += m["fg"]
                r_sub_c = np.maximum(r_sub_c, m["sub_c"])
                r_norg += 1
                if m["heavy"] > r_maxh: r_maxh = m["heavy"]

        for m in p_mols:
            pf2_ch += m["fp2_ch"]; pf1 += m["fp1"]; pap += m["fp_ap"]; pmac += m["fp_maccs"]
            for a, c in m["atoms"].items(): p_atoms[a] += c
            p_rings += m["rings"]; p_arom += m["arom_rings"]
            if m["cname"]: pcof.add(m["cname"])
            if m["sname"]: p_spec.add(m["sname"])
            if m["is_coa_deriv"]: p_coa = True
            if m["is_udp_deriv"]: p_udp = True
            if m["is_gdp_deriv"]: p_gdp = True
            p_2d.append(m["csmi_2d"]); p_iso.append(m["csmi_iso"])
            if m["has_chiral_tag"]: has_chiral_diff_atoms = True
            if m["has_ez_tag"]: has_ez_atoms = True
            if not m["is_cof"]:
                ps_fp2 += m["fp2_2d"]
                ps_fp2_ch += m["fp2_ch"]
                p_fg += m["fg"]
                p_sub_c = np.maximum(p_sub_c, m["sub_c"])
                p_norg += 1
                if m["heavy"] > p_maxh: p_maxh = m["heavy"]

        rxn_diff_r2[i] = pf2_ch - rf2_ch
        rxn_diff_r1[i] = pf1 - rf1
        rxn_ap_diff[i] = pap - rap
        rxn_maccs_diff[i] = pmac - rmac
        sub_diff_r2[i] = ps_fp2_ch - rs_fp2_ch
        sub_r_r2[i] = rs_fp2
        sub_p_r2[i] = ps_fp2

        same_2d = (sorted(r_2d) == sorted(p_2d))
        diff_iso = (sorted(r_iso) != sorted(p_iso))
        unimol_org = (r_norg == 1 and p_norg == 1)
        is_chiral_only = unimol_org and same_2d and diff_iso and has_chiral_diff_atoms and not has_ez_atoms
        is_ez_only = unimol_org and same_2d and diff_iso and has_ez_atoms and not is_chiral_only
        same_atoms_total = (r_atoms == p_atoms) and (len(r_mols) == len(p_mols))

        nad_ox = ("NAD+" in rcof and "NADH" in pcof)
        nad_red = ("NADH" in rcof and "NAD+" in pcof)
        nadp_ox = ("NADP+" in rcof and "NADPH" in pcof)
        nadp_red = ("NADPH" in rcof and "NADP+" in pcof)
        has_nad = nad_ox or nad_red
        has_nadp = nadp_ox or nadp_red
        has_nad_any = has_nad or has_nadp

        has_atp_adp = ("ATP" in rcof and "ADP" in pcof) or ("ADP" in rcof and "ATP" in pcof)
        has_atp_amp = ("ATP" in rcof and "AMP" in pcof) or ("AMP" in rcof and "ATP" in pcof)
        has_ntp_ppi = any((x in rcof and "PPi" in pcof) or ("PPi" in rcof and x in pcof) for x in ("UTP", "GTP", "CTP", "ATP", "dATP", "dTTP"))
        has_sam_sah = ("SAM" in rcof and "SAH" in pcof) or ("SAH" in rcof and "SAM" in pcof)
        has_2og_succ = ("2OG" in r_spec and "Succinate" in p_spec) or ("Succinate" in r_spec and "2OG" in p_spec)
        has_glut_2og = ("Glutamate" in r_spec and "2OG" in p_spec) or ("2OG" in r_spec and "Glutamate" in p_spec)
        has_fad = ("FAD" in rcof and "FADH2" in pcof) or ("FADH2" in rcof and "FAD" in pcof) or ("FMN" in (rcof | pcof)) or ("Flavin_bound" in (rcof | pcof))
        has_dcpip = ("DCPIP_ox" in rcof and "DCPIP_red" in pcof) or ("DCPIP_red" in rcof and "DCPIP_ox" in pcof)
        has_quinone = ("Quinone" in rcof and "Hydroquinone" in pcof) or ("Hydroquinone" in rcof and "Quinone" in pcof)
        has_fes = "FeS_cluster" in (rcof | pcof)

        has_o2 = "O2" in (rcof | pcof)
        has_h2o2 = "H2O2" in (rcof | pcof)
        has_h2o_r = "H2O" in rcof
        has_h2o_p = "H2O" in pcof
        has_h2o = has_h2o_r or has_h2o_p
        has_co2 = "CO2" in (rcof | pcof) or "HCO3" in (rcof | pcof)
        has_nh3 = "NH3" in (rcof | pcof)
        has_pi = "Pi" in (rcof | pcof)
        has_ppi = "PPi" in (rcof | pcof)
        has_coa = r_coa or p_coa
        has_udp = r_udp or p_udp
        has_gdp = r_gdp or p_gdp
        has_paps = ("PAPS" in rcof and "PAP" in pcof) or ("PAP" in rcof and "PAPS" in pcof)
        has_prpp = "PRPP" in (rcof | pcof)
        has_gsh = "GSH" in (rcof | pcof)

        is_redox = has_nad_any or has_o2 or has_h2o2 or has_2og_succ or has_fad or has_dcpip or has_quinone or has_fes
        is_constit_iso = unimol_org and (not same_2d) and same_atoms_total and not is_redox and not has_atp_adp and not has_atp_amp and not has_h2o
        is_iso = is_chiral_only or is_ez_only or is_constit_iso or (unimol_org and same_2d and diff_iso)

        # Reaction stoichiometry / seam topology with Conservation Loop (dO == +/-1 implicit H2O vs exact-atom Lyase)!
        dO_only_h2o = (not has_h2o) and (not is_redox) and (abs(p_atoms["O"] - r_atoms["O"]) == 1) and (p_atoms["C"] == r_atoms["C"]) and (p_atoms["N"] == r_atoms["N"])
        has_h2o_eff = has_h2o or dO_only_h2o
        exact_heavy_bal = (r_atoms == p_atoms)
        org_split_h2o = (
            (has_h2o and ((has_h2o_r and p_norg > r_norg) or (has_h2o_p and r_norg > p_norg)))
            or (dO_only_h2o and (p_norg != r_norg))
        ) and not is_redox and not has_atp_adp and not has_atp_amp
        org_dehydr_h2o = has_h2o and (r_norg == 1 and p_norg == 1) and not is_redox and not has_atp_adp and not has_atp_amp
        org_split_no_h2o = (not has_h2o_eff) and (not is_redox) and (not has_atp_adp) and (not has_atp_amp) and (
            (exact_heavy_bal and ((r_norg == 1 and p_norg >= 2) or (p_norg == 1 and r_norg >= 2)))
            or (has_co2 or has_nh3 or ("HCN" in (r_spec | p_spec)))
        )
        org_join_atp = (has_atp_amp or has_atp_adp) and ((r_norg >= 2 and p_norg == 1) or (p_norg >= 2 and r_norg == 1) or has_coa or has_co2 or has_nh3)
        org_2to2_transfer = (r_norg >= 2 and p_norg >= 2) and (not is_redox) and (not has_h2o_eff) and (not has_atp_amp)

        dfg = p_fg - r_fg
        afg = np.abs(dfg)
        datoms = np.array([p_atoms[a] - r_atoms[a] for a in ATOM_LIST], dtype=np.float32)

        # Paired organic transformation signatures
        ch_oh_co = (dfg[fg_idx["alcohol_any"]] * dfg[fg_idx["carbonyl"]] < 0)
        ald_carbox = (dfg[fg_idx["aldehyde"]] * dfg[fg_idx["carboxyl"]] < 0)
        amine_co = (dfg[fg_idx["amine_prim"]] * dfg[fg_idx["carbonyl"]] < 0)
        ester_h2o = (abs(dfg[fg_idx["ester"]]) > 0) and has_h2o_eff
        amide_h2o = (abs(dfg[fg_idx["amide"]]) > 0) and has_h2o_eff
        phos_h2o_no_atp = (abs(dfg[fg_idx["phosphate_ester"]]) > 0) and has_h2o_eff and not (has_atp_adp or has_atp_amp)
        prenyl_ppi = r_prenyl and has_ppi and not (has_atp_adp or has_atp_amp)
        free_glc_gain = ("FreeGlucose" in p_spec and "FreeGlucose" not in r_spec and (has_h2o_r or dO_only_h2o)) or ("FreeGlucose" in r_spec and "FreeGlucose" not in p_spec and (has_h2o_p or dO_only_h2o))

        flags = np.array([
            float(is_iso), float(is_chiral_only), float(is_ez_only), float(is_constit_iso),
            float(is_redox), float(org_split_h2o), float(org_dehydr_h2o), float(org_split_no_h2o),
            float(org_join_atp), float(org_2to2_transfer),
            float(nad_ox), float(nad_red), float(nadp_ox), float(nadp_red), float(has_nad), float(has_nadp), float(has_nad_any),
            float(has_atp_adp), float(has_atp_amp), float(has_ntp_ppi), float(has_sam_sah),
            float(has_2og_succ and has_o2), float(has_nad_any and has_o2), float(has_o2 and not has_nad_any and not has_2og_succ),
            float(has_glut_2og), float(has_fad), float(has_dcpip), float(has_quinone), float(has_fes),
            float(has_h2o2), float(has_h2o_r), float(has_h2o_p), float(has_co2), float(has_nh3),
            float(has_pi), float(has_ppi), float(has_coa), float(has_udp), float(has_gdp),
            float(has_paps), float(has_prpp), float(has_gsh),
            float(prenyl_ppi), float(free_glc_gain),
            float("pNP" in (r_spec | p_spec) or "pNA" in (r_spec | p_spec) or "AMC" in (r_spec | p_spec)),
            float(ch_oh_co), float(ald_carbox), float(amine_co), float(ester_h2o), float(amide_h2o),
            float(phos_h2o_no_atp), float("HCN" in (r_spec | p_spec)),
            float(p_rings - r_rings), float(p_arom - r_arom), float(p_norg - r_norg),
            float(np.clip((p_maxh - r_maxh) / 10.0, -3.0, 3.0)),
        ], dtype=np.float32)
        mech[i] = np.concatenate([flags, dfg, afg, datoms, r_sub_c, p_sub_c])

    def l2_norm(x: np.ndarray, signed_sqrt: bool = True) -> np.ndarray:
        sx = (np.sign(x) * np.sqrt(np.abs(x))) if signed_sqrt else x
        norms = np.linalg.norm(sx, axis=1, keepdims=True)
        norms[norms == 0] = 1.0
        return (sx / norms).astype(np.float16)

    return {
        "rxn_diff_r2": l2_norm(rxn_diff_r2),
        "rxn_diff_r1": l2_norm(rxn_diff_r1),
        "rxn_ap_diff": l2_norm(rxn_ap_diff),
        "rxn_maccs_diff": l2_norm(rxn_maccs_diff).astype(np.float32),
        "sub_diff_r2": l2_norm(sub_diff_r2),
        "sub_r_r2": l2_norm(sub_r_r2),
        "sub_p_r2": l2_norm(sub_p_r2),
        "mech": mech,
    }


def prepare_denoised_text2ec() -> pd.DataFrame:
    """Parse & denoise CARE `text2EC.csv` strictly from the file itself (0 external lookups)."""
    t2ec = pd.read_csv(DATA_ROOT / "processed_data" / "text2EC.csv")
    ec_list = np.loadtxt(DATA_ROOT / "processed_data" / "EC_list.txt", dtype=str)
    t2ec = t2ec.set_index("EC number").reindex(ec_list).reset_index()

    l1_txt, l2_txt, l3_txt, l4_txt = [], [], [], []
    for row in t2ec.itertuples():
        parts = [c.strip() for c in str(row.Text).split(";") if c.strip() and c.strip().lower() != "nan"]
        l1_txt.append(parts[0] if len(parts) >= 1 else "")
        l2_txt.append(parts[1] if len(parts) >= 2 else "")
        l3_txt.append(parts[2] if len(parts) >= 3 else "")
        if not bool(row._3) and len(parts) >= 4:
            l4_txt.append("; ".join(parts[3:]))
        else:
            l4_txt.append("")

    df = pd.DataFrame({
        "ec": t2ec["EC number"].astype(str),
        "ec1": t2ec["EC number"].astype(str).apply(lambda s: s.split(".")[0]),
        "ec2": t2ec["EC number"].astype(str).apply(lambda s: ".".join(s.split(".")[:2])),
        "ec3": t2ec["EC number"].astype(str).apply(lambda s: ".".join(s.split(".")[:3])),
        "l1": l1_txt,
        "l2": l2_txt,
        "l3": l3_txt,
        "l4": l4_txt,
        "full": t2ec["Text"].fillna("").astype(str),
        "incomplete": t2ec["Text Incomplete"].astype(bool),
    })

    ec2_l2 = df[df["l2"] != ""].groupby("ec2")["l2"].agg(lambda s: s.value_counts().index[0]).to_dict()
    ec3_l3 = df[df["l3"] != ""].groupby("ec3")["l3"].agg(lambda s: s.value_counts().index[0]).to_dict()
    df["l2"] = [v if v else ec2_l2.get(k, "") for v, k in zip(df["l2"], df["ec2"])]
    df["l3"] = [v if v else ec3_l3.get(k, "") for v, k in zip(df["l3"], df["ec3"])]

    # Consensus L4 suffixes within each EC3 to replace GO/UniProt scrape artifacts (e.g. 2.3.1, 4.1.1, 6.2.1)
    suf_re = re.compile(r"([a-z0-9\-]*(?:dehydrogenase|reductase|oxidase|peroxidase|monooxygenase|dioxygenase|oxygenase|hydroxylase|catalase|dismutase|transferase|kinase|phosphatase|esterase|lipase|lactonase|glycosidase|glucosidase|peptidase|proteinase|deacetylase|amidase|hydrolase|dehalogenase|deaminase|decarboxylase|aldolase|dehydratase|hydratase|synthase|lyase|cyclase|racemase|epimerase|isomerase|mutase|tautomerase|ligase|synthetase|carboxylase|phosphorylase))")
    root_re = re.compile(r"(dehydrogenase|reductase|oxidase|peroxidase|monooxygenase|dioxygenase|oxygenase|hydroxylase|acyltransferase|acetyltransferase|methyltransferase|glycosyltransferase|glucosyltransferase|aminotransferase|transaminase|transferase|kinase|phosphatase|esterase|lipase|lactonase|glycosidase|peptidase|deacetylase|amidase|hydrolase|dehalogenase|deaminase|decarboxylase|aldolase|dehydratase|hydratase|synthase|lyase|cyclase|racemase|epimerase|isomerase|mutase|tautomerase|ligase|synthetase|carboxylase|phosphorylase)")

    ec3_cons = {}
    for c3, grp in df.groupby("ec3"):
        l4s = [s.lower() for s in grp["l4"] if s]
        cnt = Counter()
        for s in l4s:
            for w in set(suf_re.findall(s)) | set(root_re.findall(s)):
                cnt[w] += 1
            if "coa ligase" in s or "-coa ligase" in s: cnt["coa ligase"] += 1
            if "(nad+)" in s: cnt["(nad+)"] += 1
            if "(nadp+)" in s: cnt["(nadp+)"] += 1
        kept = [w for w, c in cnt.most_common(6) if c >= 2 or (len(l4s) == 1 and c == 1)]
        ec3_cons[c3] = ", ".join(kept)

    valid_l3_prefix = (
        "acting on", "oxidoreductase", "hydrolase", "transferase", "lyase", "ligase",
        "isomerase", "racemase", "intramolecular", "carbon-", "hydro-lyase", "peptidase",
        "transaminase", "methyltransferase", "carboxylic", "thioester", "phosphoric",
        "sulfuric", "ammonia", "acid-", "2-oxoglutarate", "quinone", "with ", "adenylyl",
        "amidine", "amine-", "ether ", "pentosyl", "hexosyl", "halide", "phospho",
    )
    l3_ec3_cnt = df.groupby("l3")["ec3"].nunique().to_dict()
    l3_clean = []
    for row in df.itertuples():
        raw_l3 = str(row.l3).strip()
        cons = ec3_cons.get(row.ec3, "")
        rl = raw_l3.lower()
        is_clean = (l3_ec3_cnt.get(raw_l3, 0) >= 2) or rl.startswith(valid_l3_prefix)
        if is_clean and raw_l3:
            s = f"{raw_l3}. {cons}".strip(". ")
        else:
            s = f"{row.l2}; {cons}".strip("; ") if cons else raw_l3
        l3_clean.append(s)

    df["l3_clean"] = l3_clean
    df["l3_cons"] = [ec3_cons.get(k, "") for k in df["ec3"]]
    df["l123"] = (df["l1"] + " ; " + df["l2"] + " ; " + df["l3_clean"]).str.strip(" ;")
    return df


def build_and_cache_all():
    t0 = time.perf_counter()
    CACHE_DIR.mkdir(parents=True, exist_ok=True)

    # 1. Self-test uncharger
    for test_smi, expected in [
        ("O=P([O-])([O-])OP(=O)([O-])O", "PPi"),
        ("[NH3+]C(CCC(=O)[O-])C(=O)[O-]", "Glutamate"),
        ("Nc1ncnc2c1ncn2C1OC(COP(=O)([O-])OP(=O)([O-])OP(=O)([O-])[O-])C(O)C1O", "ATP"),
        ("NC(=O)c1ccc[n+](C2OC(COP(=O)([O-])OP(=O)([O-])OCC3OC(n4cnc5c(N)ncnc54)C(O)C3O)C(O)C2O)c1", "NAD+"),
        ("C[S+](CCC(N)C(=O)[O-])CC1OC(n2cnc3c(N)ncnc32)C(O)C1O", "SAM"),
    ]:
        cs = Chem.MolToSmiles(uncharge_biochem(Chem.MolFromSmiles(test_smi)), isomericSmiles=False)
        got = COFACTOR_LUT.get(cs) or SPECIES_LUT.get(cs)
        assert got == expected, f"Uncharge fail for {test_smi}: got {got}, cs={cs}"
    print("[SELFTEST] Uncharger matches all 5 ionic cofactors cleanly.")

    # 2. Gather unique SMILES across hard & medium splits once
    splits_df = {}
    uniq = set()
    for sp in ("hard", "medium"):
        tr_df = pd.read_csv(DATA_ROOT / "splits" / "task2" / f"{sp}_reaction_train.csv")
        te_df = pd.read_csv(DATA_ROOT / "splits" / "task2" / f"{sp}_reaction_test.csv")
        splits_df[sp] = (tr_df, te_df)
        for rxn in tr_df["Reaction"].astype(str).tolist() + te_df["Reaction"].astype(str).tolist():
            lhs, rhs = rxn.split(">>")
            for side in (lhs, rhs):
                for s in side.split("."):
                    s = s.strip()
                    if s and s != "[H+]":
                        uniq.add(s)

    print(f"Building shared v2 mol cache for {len(uniq)} unique SMILES...")
    mol_cache = _build_mol_cache(uniq)
    print(f"  mol cache built in {time.perf_counter()-t0:.1f}s")

    for sp in ("hard", "medium"):
        t1 = time.perf_counter()
        tr_df, te_df = splits_df[sp]
        tr_f = featurize_reactions_v2(tr_df["Reaction"].astype(str).tolist(), mol_cache)
        te_f = featurize_reactions_v2(te_df["Reaction"].astype(str).tolist(), mol_cache)
        payload = {}
        for k in tr_f:
            payload[f"tr_{k}"] = tr_f[k]
            payload[f"te_{k}"] = te_f[k]
        out_p = CACHE_DIR / f"v2_feats_{sp}.npz"
        np.savez_compressed(out_p, **payload)
        print(f"Saved {out_p} in {time.perf_counter()-t1:.1f}s")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--build-all", action="store_true")
    args = parser.parse_args()
    if args.build_all:
        build_and_cache_all()
