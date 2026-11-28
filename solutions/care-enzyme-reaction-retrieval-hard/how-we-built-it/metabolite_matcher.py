#!/usr/bin/env python3
"""metabolite_matcher.py — Pure organic-chemistry exact metabolite & carbon/heteroatom signature matcher for intra-EC3 L4 scoring.

Strictly matches canonicalized uncharged SMILES appearing in `Reaction` SMILES
against the official `text2EC.csv` L4 nomenclature (ZERO test data, ZERO external DBs).
"""
from __future__ import annotations

import pathlib
import sys
import numpy as np
import pandas as pd
from rdkit import Chem, RDLogger

RDLogger.DisableLog("rdApp.*")

ROOT = pathlib.Path(__file__).resolve().parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import features_v2 as f2  # noqa: E402

# Canonical biochemistry vocabulary: (key, SMILES_list, L4_keywords_tuple)
METABOLITE_VOCAB = [
    ("glucose", ["OC1OC(CO)C(O)C(O)C1O", "OCC1OC(O)C(O)C(O)C1O"], ("glucose", "glucos", "d-glucose", "glucopyranos")),
    ("glucose_6p", ["O=P(O)(O)OCC1OC(O)C(O)C(O)C1O"], ("glucose-6-phosphate", "glucose 6-phosphate")),
    ("glucose_1p", ["O=P(O)(O)OC1OC(CO)C(O)C(O)C1O"], ("glucose-1-phosphate", "glucose 1-phosphate")),
    ("galactose", ["OC1C(O)C(O)C(CO)OC1O"], ("galactose", "galactos")),
    ("mannose", ["OC1C(O)C(O)OC(CO)C1O"], ("mannose", "mannos")),
    ("fructose", ["OCC1(O)OC(CO)C(O)C1O", "OCC(=O)C(O)C(O)C(O)CO"], ("fructose", "fructos")),
    ("fructose_6p", ["O=P(O)(O)OCC1OC(O)(CO)C(O)C1O"], ("fructose-6-phosphate", "fructose 6-phosphate")),
    ("xylose", ["OC1COC(O)C(O)C1O"], ("xylose", "xylos")),
    ("ribose", ["OC1OC(CO)C(O)C1O", "O=CC(O)C(O)C(O)CO"], ("ribose", "ribos")),
    ("ribose_5p", ["O=P(O)(O)OCC1OC(O)C(O)C1O"], ("ribose-5-phosphate", "ribose 5-phosphate")),
    ("arabinose", ["OC1OCC(O)C(O)C1O"], ("arabinose", "arabinos")),
    ("glycerol", ["OCC(O)CO"], ("glycerol",)),
    ("glycerol_3p", ["O=P(O)(O)OCC(O)CO"], ("glycerol-3-phosphate", "glycerol 3-phosphate")),
    ("glycerate", ["O=C(O)C(O)CO"], ("glycerate", "glyceric")),
    ("lactate", ["CC(O)C(=O)O"], ("lactate", "l-lactate", "d-lactate")),
    ("pyruvate", ["CC(=O)C(=O)O"], ("pyruvate",)),
    ("malate", ["O=C(O)CC(O)C(=O)O"], ("malate",)),
    ("oxaloacetate", ["O=C(O)CC(=O)C(=O)O"], ("oxaloacetate",)),
    ("succinate", ["O=C(O)CCC(=O)O"], ("succinate",)),
    ("fumarate", ["O=C(O)/C=C/C(=O)O", "O=C(O)C=CC(=O)O"], ("fumarate",)),
    ("citrate", ["O=C(O)CC(O)(C(=O)O)CC(=O)O"], ("citrate", "isocitrate")),
    ("isocitrate", ["O=C(O)CC(C(=O)O)C(O)C(=O)O"], ("isocitrate",)),
    ("2og", ["O=C(O)CCC(=O)C(=O)O"], ("2-oxoglutarate", "oxoglutarate", "ketoglutarate")),
    ("glyoxylate", ["O=CC(=O)O"], ("glyoxylate",)),
    ("glycolate", ["O=C(O)CO"], ("glycolate",)),
    ("formate", ["O=CO"], ("formate",)),
    ("formaldehyde", ["C=O"], ("formaldehyde",)),
    ("methanol", ["CO"], ("methanol",)),
    ("ethanol", ["CCO"], ("ethanol", "alcohol")),
    ("acetaldehyde", ["CC=O"], ("acetaldehyde", "aldehyde")),
    ("acetate", ["CC(=O)O"], ("acetate", "acetyl")),
    ("acetyl_coa", ["CC(=O)SCCNC(=O)CCNC(=O)C(O)C(C)(C)COP(=O)(O)OP(=O)(O)OCC1OC(n2cnc3c(N)ncnc32)C(O)C1OP(=O)(O)O"], ("acetyl-coa", "acetyl coa")),
    ("propionate", ["CCC(=O)O"], ("propionate", "propionyl")),
    ("butyrate", ["CCCC(=O)O"], ("butyrate", "butyryl", "butanoate")),
    ("malonate", ["O=C(O)CC(=O)O"], ("malonate", "malonyl")),
    ("oxalate", ["O=C(O)C(=O)O"], ("oxalate",)),
    ("urea", ["NC(N)=O"], ("urea", "urease")),
    ("glycine", ["NCC(=O)O"], ("glycine",)),
    ("alanine", ["CC(N)C(=O)O"], ("alanine", "l-alanine", "d-alanine")),
    ("beta_alanine", ["NCCC(=O)O"], ("beta-alanine", "3-aminopropanoate")),
    ("serine", ["NC(CO)C(=O)O"], ("serine",)),
    ("threonine", ["CC(O)C(N)C(=O)O"], ("threonine",)),
    ("cysteine", ["NC(CS)C(=O)O"], ("cysteine",)),
    ("methionine", ["CSCCC(N)C(=O)O"], ("methionine",)),
    ("aspartate", ["NC(CC(=O)O)C(=O)O"], ("aspartate",)),
    ("asparagine", ["NC(=O)CC(N)C(=O)O"], ("asparagine",)),
    ("glutamate", ["NC(CCC(=O)O)C(=O)O"], ("glutamate",)),
    ("glutamine", ["NC(=O)CCC(N)C(=O)O"], ("glutamine",)),
    ("valine", ["CC(C)C(N)C(=O)O"], ("valine",)),
    ("leucine", ["CC(C)CC(N)C(=O)O"], ("leucine",)),
    ("isoleucine", ["CCC(C)C(N)C(=O)O"], ("isoleucine",)),
    ("proline", ["O=C(O)C1CCCN1"], ("proline",)),
    ("phenylalanine", ["NC(Cc1ccccc1)C(=O)O"], ("phenylalanine",)),
    ("tyrosine", ["NC(Cc1ccc(O)cc1)C(=O)O"], ("tyrosine",)),
    ("tryptophan", ["NC(Cc1c[nH]c2ccccc12)C(=O)O"], ("tryptophan",)),
    ("histidine", ["NC(Cc1c[nH]cn1)C(=O)O"], ("histidine",)),
    ("lysine", ["NCCCC[C@H](N)C(=O)O", "NCCCCC(N)C(=O)O"], ("lysine",)),
    ("arginine", ["N=C(N)NCCCC(N)C(=O)O"], ("arginine",)),
    ("ornithine", ["NCCCC(N)C(=O)O"], ("ornithine",)),
    ("gaba", ["NCCCC(=O)O"], ("4-aminobutyrate", "aminobutyrate")),
    ("taurine", ["NCCS(=O)(=O)O"], ("taurine",)),
    ("putrescine", ["NCCCCN"], ("putrescine", "diamine")),
    ("spermidine", ["NCCCCNCCCN"], ("spermidine",)),
    ("histamine", ["NCCc1c[nH]cn1"], ("histamine",)),
    ("dopamine", ["NCCc1ccc(O)c(O)c1"], ("dopamine",)),
    ("tryptamine", ["NCCc1c[nH]c2ccccc12"], ("tryptamine",)),
    ("choline", ["C[N+](C)(C)CCO"], ("choline",)),
    ("betaine", ["C[N+](C)(C)CC(=O)O"], ("betaine",)),
    ("creatine", ["CN(CC(=O)O)C(N)=N"], ("creatine",)),
    ("benzoate", ["O=C(O)c1ccccc1"], ("benzoate",)),
    ("salicylate", ["O=C(O)c1ccccc1O"], ("salicylate",)),
    ("catechol", ["Oc1ccccc1O"], ("catechol",)),
    ("phenol", ["Oc1ccccc1"], ("phenol",)),
    ("shikimate", ["O=C(O)C1=CC(O)C(O)C(O)C1"], ("shikimate",)),
    ("quinate", ["O=C(O)C1(O)CC(O)C(O)C(O)C1"], ("quinate",)),
    ("cholesterol", ["CC(C)CCCC(C)C1CCC2C3CC=C4CC(O)CCC4(C)C3CCC12C"], ("cholesterol",)),
    ("adenosine", ["Nc1ncnc2c1ncn2C1OC(CO)C(O)C1O"], ("adenosine",)),
    ("inosine", ["O=c1[nH]cnc2c1ncn2C1OC(CO)C(O)C1O"], ("inosine",)),
    ("guanosine", ["Nc1nc2c(ncn2C2OC(CO)C(O)C2O)c(=O)[nH]1"], ("guanosine",)),
    ("uridine", ["O=c1ccn(C2OC(CO)C(O)C2O)c(=O)[nH]1"], ("uridine",)),
    ("cytidine", ["Nc1ccn(C2OC(CO)C(O)C2O)c(=O)n1"], ("cytidine",)),
    ("xanthine", ["O=c1[nH]c(=O)c2[nH]cnc2[nH]1"], ("xanthine",)),
    ("hypoxanthine", ["O=c1[nH]cnc2[nH]cnc12"], ("hypoxanthine",)),
    ("uracil", ["O=c1cc[nH]c(=O)[nH]1"], ("uracil",)),
    ("orotate", ["O=C(O)c1cc(=O)[nH]c(=O)[nH]1"], ("orotate",)),
    ("mannitol", ["OCC(O)C(O)C(O)C(O)CO"], ("mannitol", "sorbitol", "galactitol", "iditol")),
    ("xylitol", ["OCC(O)C(O)C(O)CO"], ("xylitol", "arabitol", "ribitol")),
    ("inositol", ["OC1C(O)C(O)C(O)C(O)C1O"], ("inositol",)),
    ("ascorbate", ["O=C1OC(C(O)CO)C(O)=C1O"], ("ascorbate", "dehydroascorbate")),
    ("sucrose", ["OCC1OC(OC2(CO)OC(CO)C(O)C2O)C(O)C(O)C1O"], ("sucrose",)),
    ("trehalose", ["OCC1OC(OC2OC(CO)C(O)C(O)C2O)C(O)C(O)C1O"], ("trehalose",)),
    ("maltose", ["OCC1OC(OC2C(O)C(O)C(O)OC2CO)C(O)C(O)C1O"], ("maltose", "cellobiose", "lactose")),
    ("cinnamate", ["O=C(O)C=Cc1ccccc1"], ("cinnamate",)),
    ("coumarate", ["O=C(O)C=Cc1ccc(O)cc1"], ("coumarate",)),
    ("caffeate", ["O=C(O)C=Cc1ccc(O)c(O)c1"], ("caffeate",)),
    ("ferulate", ["COc1cc(C=CC(=O)O)ccc1O"], ("ferulate",)),
    ("mevalonate", ["CC(O)(CCO)CC(=O)O"], ("mevalonate",)),
    ("dhap", ["O=C(CO)COP(=O)(O)O"], ("glycerone", "dihydroxyacetone")),
    ("pep", ["C=C(OP(=O)(O)O)C(=O)O"], ("phosphoenolpyruvate",)),
    ("nitrite", ["O=NO"], ("nitrite",)),
    ("cyanide", ["C#N"], ("cyanide", "mandelonitrile", "cyanohydrin")),
    ("pnp", ["O=[N+]([O-])c1ccc(O)cc1"], ("4-nitrophenyl", "nitrophenyl")),
    ("indole", ["c1ccc2[nH]ccc2c1"], ("indole",)),
]


def build_metabolite_lut():
    lut = {}
    for k_idx, (name, smis, _) in enumerate(METABOLITE_VOCAB):
        for s in smis:
            m = Chem.MolFromSmiles(s)
            if m is None:
                continue
            um = f2.uncharge_biochem(m)
            lut[Chem.MolToSmiles(um, isomericSmiles=False)] = k_idx
            lut[Chem.MolToSmiles(m, isomericSmiles=False)] = k_idx
    return lut


def build_ec_metabolite_matrix(ec_df: pd.DataFrame) -> np.ndarray:
    """Return `(n_ec, len(METABOLITE_VOCAB))` binary indicator matrix over `l4` text."""
    M = np.zeros((len(ec_df), len(METABOLITE_VOCAB)), dtype=np.float32)
    for r, l4 in enumerate(ec_df["l4"].astype(str)):
        low = l4.lower()
        if not low:
            continue
        for c, (_, _, kws) in enumerate(METABOLITE_VOCAB):
            if any(k in low for k in kws):
                M[r, c] = 1.0
    # Upweight rare specific metabolites via IDF-like scaling
    df_cnt = np.maximum(M.sum(axis=0, keepdims=True), 1.0)
    idf = np.log1p(len(ec_df) / df_cnt).astype(np.float32)
    return M * idf


def featurize_metabolites_rxns(reactions: list[str]) -> np.ndarray:
    """Return `(n_rxn, len(METABOLITE_VOCAB))` presence matrix (1.0 if metabolite on R or P)."""
    lut = build_metabolite_lut()
    uniq = set()
    for r in reactions:
        for side in r.split(">>"):
            for s in side.split("."):
                s = s.strip()
                if s and s != "[H+]":
                    uniq.add(s)
    s_to_id = {}
    for s in uniq:
        if s in lut:
            s_to_id[s] = lut[s]
            continue
        m = Chem.MolFromSmiles(s)
        if m is None:
            continue
        um = f2.uncharge_biochem(m)
        cs = Chem.MolToSmiles(um, isomericSmiles=False)
        if cs in lut:
            s_to_id[s] = lut[cs]

    X = np.zeros((len(reactions), len(METABOLITE_VOCAB)), dtype=np.float32)
    for i, r in enumerate(reactions):
        for side in r.split(">>"):
            for s in side.split("."):
                idx = s_to_id.get(s.strip())
                if idx is not None:
                    X[i, idx] = 1.0
    return X
