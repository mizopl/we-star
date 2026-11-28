#!/usr/bin/env python3
"""colab_care_stage2_t5_hard.py — Stage-2 GPU Runner for HardFull + MedFull-T5v2 + HardFull-T5v2.

Runs cleanly after Stage-1 (`care_gpu_stage1_ckpt.npz` already holds cv_cb, cv_t5, med_cb, med_mtr).
Checkpoints after EVERY stage so 0 compute is ever lost.
"""
from __future__ import annotations

import gc
import os
import pathlib
import tarfile
import time
import numpy as np
import pandas as pd
import torch
import torch.nn as nn
import torch.nn.functional as F
from torch.utils.data import DataLoader, Dataset, Sampler
from transformers import AutoModel, AutoTokenizer, T5Model

os.environ["TOKENIZERS_PARALLELISM"] = "false"
os.environ["PYTORCH_CUDA_ALLOC_CONF"] = "expandable_segments:True"

DATA_DIR = pathlib.Path("/content/care_data")
BUNDLE_PATH = pathlib.Path("/content/care_colab_bundle.tar.gz")
CKPT_PATH = pathlib.Path("/content/care_gpu_stage2_ckpt.npz")
OUT_PATH = pathlib.Path("/content/care_gpu_stage2_outputs.npz")


def extract_and_verify_bundle():
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    if not (DATA_DIR / "ec_meta.csv").exists():
        with tarfile.open(BUNDLE_PATH, "r:gz") as tar:
            tar.extractall(DATA_DIR)
    for fn in ("medium_test_rxns_only.csv", "hard_test_rxns_only.csv"):
        cols = list(pd.read_csv(DATA_DIR / fn, nrows=2).columns)
        assert cols == ["t5_prompt", "lhs_org", "rhs_org", "Reaction"], f"LEAK_GUARD_FAIL on {fn}: {cols}"
    print("[AIR_GAP_VERIFIED] Test CSVs contain strictly Reaction SMILES columns.", flush=True)
    if torch.cuda.is_available():
        print(f"[GPU] {torch.cuda.get_device_name(0)} | VRAM={torch.cuda.get_device_properties(0).total_memory/1e9:.1f}GB | BF16={torch.cuda.is_bf16_supported()}", flush=True)


def build_text_embeddings(ec_df: pd.DataFrame, aux: dict, device: torch.device):
    tok = AutoTokenizer.from_pretrained("allenai/scibert_scivocab_uncased")
    sci = AutoModel.from_pretrained("allenai/scibert_scivocab_uncased").to(device).eval()

    def _enc(texts: list[str]) -> np.ndarray:
        embs = []
        with torch.no_grad(), torch.amp.autocast("cuda", dtype=torch.bfloat16):
            for i in range(0, len(texts), 128):
                batch = tok([s if s else "enzyme" for s in texts[i : i + 128]], padding=True, truncation=True, max_length=96, return_tensors="pt").to(device)
                out = sci(**batch).last_hidden_state
                mask = batch["attention_mask"].unsqueeze(-1).float()
                pooled = (out.float() * mask).sum(1) / mask.sum(1).clamp(min=1e-6)
                embs.append(F.normalize(pooled, dim=-1).cpu().numpy())
        return np.vstack(embs).astype(np.float32)

    S123 = _enc([f"{r.l1}; {r.l2}; {r.l3_clean}" for r in ec_df.itertuples()])
    S4 = _enc(ec_df["l4"].fillna("").astype(str).tolist())
    l4_empty = (ec_df["l4"].fillna("").str.len() == 0).values
    S4[l4_empty] = 0.0

    B_l2 = aux["B_l2"].astype(np.float32)
    B_l3 = aux["B_l3"].astype(np.float32)
    B_l4 = aux["B_l4"].astype(np.float32)
    E123 = np.hstack([B_l3 * 1.1, B_l2 * 0.5, S123]).astype(np.float32)
    E123 /= np.maximum(np.linalg.norm(E123, axis=1, keepdims=True), 1e-6)
    E4 = np.hstack([B_l4 * 1.1, S4]).astype(np.float32)
    E4 /= np.maximum(np.linalg.norm(E4, axis=1, keepdims=True), 1e-6)
    E4[l4_empty] = 0.0
    del sci
    torch.cuda.empty_cache()
    print(f"[TEXT] Built SciBERT+BGE E123={E123.shape}, E4={E4.shape}", flush=True)
    return E123, E4, (~l4_empty).astype(np.float32)


def pretokenize(tok, texts: list[str], max_len: int) -> list[list[int]]:
    out = []
    for i in range(0, len(texts), 2048):
        enc = tok(texts[i : i + 2048], truncation=True, max_length=max_len, padding=False)
        out.extend(enc["input_ids"])
    return out


class BucketBatchSampler(Sampler):
    def __init__(self, lengths: list[int], bs: int, seed: int = 42):
        self.lengths = np.asarray(lengths, dtype=np.float32)
        self.bs = bs
        self.rng = np.random.default_rng(seed)

    def __iter__(self):
        noisy = self.lengths + self.rng.uniform(-6.0, 6.0, size=len(self.lengths))
        order = np.argsort(noisy)
        batches = [order[i : i + self.bs].tolist() for i in range(0, len(order), self.bs)]
        self.rng.shuffle(batches)
        for b in batches:
            yield b

    def __len__(self):
        return (len(self.lengths) + self.bs - 1) // self.bs


class PreTokDataset(Dataset):
    def __init__(self, a_ids, b_ids, mech, y4=None, y1=None, y2=None, y3=None):
        self.a_ids, self.b_ids, self.mech = a_ids, b_ids, mech.astype(np.float32)
        self.y4, self.y1, self.y2, self.y3 = y4, y1, y2, y3

    def __len__(self):
        return len(self.a_ids)

    def __getitem__(self, i):
        if self.y4 is not None:
            return self.a_ids[i], self.b_ids[i], self.mech[i], self.y4[i], self.y1[i], self.y2[i], self.y3[i]
        return self.a_ids[i], self.b_ids[i], self.mech[i]


def pad_seqs(seqs: list[list[int]], pad_id: int) -> tuple[torch.Tensor, torch.Tensor]:
    mx = max(len(s) for s in seqs)
    B = len(seqs)
    ids = torch.full((B, mx), pad_id, dtype=torch.long)
    mask = torch.zeros((B, mx), dtype=torch.long)
    for r, s in enumerate(seqs):
        n = len(s)
        ids[r, :n] = torch.tensor(s, dtype=torch.long)
        mask[r, :n] = 1
    return ids, mask


class ReactionT5MultiTask(nn.Module):
    def __init__(self, d_mech: int, n_ec2: int, n_ec3: int, d_t123: int, d_t4: int):
        super().__init__()
        self.t5 = T5Model.from_pretrained("sagawa/ReactionT5v2-forward")
        h = self.t5.config.d_model
        self.mech_net = nn.Sequential(nn.Linear(d_mech, 256), nn.LayerNorm(256), nn.GELU())
        self.fusion = nn.Sequential(
            nn.Linear(2 * h + 256, 768), nn.LayerNorm(768), nn.GELU(), nn.Dropout(0.25),
            nn.Linear(768, 768), nn.LayerNorm(768), nn.GELU(), nn.Dropout(0.15),
        )
        self.h1 = nn.Linear(768, 7)
        self.h2 = nn.Linear(768, n_ec2)
        self.w3 = nn.Linear(768, n_ec3, bias=False)
        self.ht123 = nn.Linear(768, d_t123)
        self.ht4 = nn.Linear(768, d_t4)

    def forward(self, enc_ids, enc_mask, dec_ids, dec_mask, mech):
        out = self.t5(input_ids=enc_ids, attention_mask=enc_mask, decoder_input_ids=dec_ids, decoder_attention_mask=dec_mask, use_cache=False)
        em = enc_mask.unsqueeze(-1).float()
        h_enc = (out.encoder_last_hidden_state.float() * em).sum(1) / em.sum(1).clamp(min=1e-6)
        dm = dec_mask.unsqueeze(-1).float()
        h_dec = (out.last_hidden_state.float() * dm).sum(1) / dm.sum(1).clamp(min=1e-6)
        hm = self.mech_net(mech.float())
        z = self.fusion(torch.cat([h_enc, h_dec, hm], dim=-1))
        z3 = F.normalize(z, dim=-1)
        w3n = F.normalize(self.w3.weight.float(), dim=-1)
        return self.h1(z), self.h2(z), 20.0 * (z3 @ w3n.T), F.normalize(self.ht123(z), dim=-1), F.normalize(self.ht4(z), dim=-1)


class SiameseChemBERTaMultiTask(nn.Module):
    def __init__(self, model_name: str, d_mech: int, n_ec2: int, n_ec3: int, d_t123: int, d_t4: int, mode: str = "siamese"):
        super().__init__()
        self.mode = mode
        self.enc = AutoModel.from_pretrained(model_name)
        h = self.enc.config.hidden_size
        self.mech_net = nn.Sequential(nn.Linear(d_mech, 256), nn.LayerNorm(256), nn.GELU())
        in_d = (4 * h + 256) if mode == "siamese" else (h + 256)
        self.fusion = nn.Sequential(
            nn.Linear(in_d, 768), nn.LayerNorm(768), nn.GELU(), nn.Dropout(0.25),
            nn.Linear(768, 768), nn.LayerNorm(768), nn.GELU(), nn.Dropout(0.15),
        )
        self.h1 = nn.Linear(768, 7)
        self.h2 = nn.Linear(768, n_ec2)
        self.w3 = nn.Linear(768, n_ec3, bias=False)
        self.ht123 = nn.Linear(768, d_t123)
        self.ht4 = nn.Linear(768, d_t4)

    def _pool(self, ids, mask):
        out = self.enc(input_ids=ids, attention_mask=mask).last_hidden_state.float()
        m = mask.unsqueeze(-1).float()
        return (out * m).sum(1) / m.sum(1).clamp(min=1e-6)

    def forward(self, ids_a, mask_a, ids_b, mask_b, mech):
        hm = self.mech_net(mech.float())
        if self.mode == "siamese":
            hl = self._pool(ids_a, mask_a)
            hr = self._pool(ids_b, mask_b)
            feat = torch.cat([hl, hr, hr - hl, hl * hr, hm], dim=-1)
        else:
            hc = self._pool(ids_a, mask_a)
            feat = torch.cat([hc, hm], dim=-1)
        z = self.fusion(feat)
        z3 = F.normalize(z, dim=-1)
        w3n = F.normalize(self.w3.weight.float(), dim=-1)
        return self.h1(z), self.h2(z), 20.0 * (z3 @ w3n.T), F.normalize(self.ht123(z), dim=-1), F.normalize(self.ht4(z), dim=-1)


def run_stage(
    tag: str, arch: str, model_name: str,
    tr_df: pd.DataFrame, tr_mech: np.ndarray,
    te_df: pd.DataFrame, te_mech: np.ndarray,
    ec_df: pd.DataFrame, E123: np.ndarray, E4: np.ndarray, l4_v: np.ndarray,
    epochs: int, bs: int, lr: float, device: torch.device, grad_accum: int = 1, seed: int = 42,
):
    t0 = time.perf_counter()
    torch.manual_seed(seed); np.random.seed(seed)

    ec_list = ec_df["ec"].tolist()
    ec_to_idx = {e: i for i, e in enumerate(ec_list)}
    tr_y4 = np.array([ec_to_idx[e] for e in tr_df["EC number"].astype(str)], dtype=np.int64)
    tr_y1 = np.array([int(ec_df["ec1"].values[y]) - 1 for y in tr_y4], dtype=np.int64)
    seen_ec2 = sorted(set(ec_df["ec2"].values[tr_y4].tolist()))
    c2_map = {c: i for i, c in enumerate(seen_ec2)}
    tr_y2 = np.array([c2_map[c] for c in ec_df["ec2"].values[tr_y4]], dtype=np.int64)
    seen_ec3 = sorted(set(ec_df["ec3"].values[tr_y4].tolist()))
    c3_map = {c: i for i, c in enumerate(seen_ec3)}
    tr_y3 = np.array([c3_map[c] for c in ec_df["ec3"].values[tr_y4]], dtype=np.int64)

    pri3 = np.bincount(tr_y3, minlength=len(seen_ec3)).astype(np.float32)
    log_pri3 = torch.from_numpy(np.log(np.maximum(pri3 / pri3.sum(), 1e-6))).to(device)
    pri2 = np.bincount(tr_y2, minlength=len(seen_ec2)).astype(np.float32)
    log_pri2 = torch.from_numpy(np.log(np.maximum(pri2 / pri2.sum(), 1e-6))).to(device)

    tok = AutoTokenizer.from_pretrained(model_name)
    pad_id = tok.pad_token_id if tok.pad_token_id is not None else 0

    def norm_mech(M):
        M = M.copy()
        M[:, 56:129] = np.sign(M[:, 56:129]) * np.log1p(np.abs(M[:, 56:129]))
        return M

    tr_mn, te_mn = norm_mech(tr_mech), norm_mech(te_mech)
    tr_p = tr_df["t5_prompt"].fillna(".").astype(str).tolist()
    tr_l = tr_df["lhs_org"].fillna(".").astype(str).tolist()
    tr_r = tr_df["rhs_org"].fillna(".").astype(str).tolist()
    te_p = te_df["t5_prompt"].fillna(".").astype(str).tolist()
    te_l = te_df["lhs_org"].fillna(".").astype(str).tolist()
    te_r = te_df["rhs_org"].fillna(".").astype(str).tolist()

    if arch == "t5":
        tr_a = pretokenize(tok, tr_p, 168); tr_b = pretokenize(tok, tr_r, 128)
        te_a = pretokenize(tok, te_p, 168); te_b = pretokenize(tok, te_r, 128)
    elif arch == "siamese":
        tr_a = pretokenize(tok, tr_l, 144); tr_b = pretokenize(tok, tr_r, 144)
        te_a = pretokenize(tok, te_l, 144); te_b = pretokenize(tok, te_r, 144)
    else:
        tr_a = pretokenize(tok, [f"{l}>>{r}" for l, r in zip(tr_l, tr_r)], 200); tr_b = tr_a
        te_a = pretokenize(tok, [f"{l}>>{r}" for l, r in zip(te_l, te_r)], 200); te_b = te_a

    print(f"[{tag}] Pre-tokenized in {time.perf_counter()-t0:.1f}s (mean_len={np.mean([len(s) for s in tr_a]):.1f})", flush=True)

    def collate_fn(batch):
        has_y = len(batch[0]) == 7
        a_s, b_s = [b[0] for b in batch], [b[1] for b in batch]
        mech = torch.from_numpy(np.stack([b[2] for b in batch]))
        a, ma = pad_seqs(a_s, pad_id)
        if arch == "t5":
            dec_raw, dec_m = pad_seqs(b_s, pad_id)
            b_ids = torch.cat([torch.full((len(batch), 1), pad_id, dtype=torch.long), dec_raw[:, :-1]], dim=1)
            mb = dec_m.clone(); mb[:, 0] = 1
        elif arch == "siamese":
            b_ids, mb = pad_seqs(b_s, pad_id)
        else:
            b_ids, mb = a, ma
        if has_y:
            return (a, ma, b_ids, mb, mech,
                    torch.tensor([b[3] for b in batch], dtype=torch.long),
                    torch.tensor([b[4] for b in batch], dtype=torch.long),
                    torch.tensor([b[5] for b in batch], dtype=torch.long),
                    torch.tensor([b[6] for b in batch], dtype=torch.long))
        return a, ma, b_ids, mb, mech

    lens = [len(a) + (len(b) if arch != "joint" else 0) for a, b in zip(tr_a, tr_b)]
    tr_loader = DataLoader(PreTokDataset(tr_a, tr_b, tr_mn, tr_y4, tr_y1, tr_y2, tr_y3), batch_sampler=BucketBatchSampler(lens, bs=bs, seed=seed), num_workers=0, pin_memory=True, collate_fn=collate_fn)
    te_loader = DataLoader(PreTokDataset(te_a, te_b, te_mn), batch_size=bs * 2, shuffle=False, num_workers=0, pin_memory=True, collate_fn=collate_fn)

    if arch == "t5":
        net = ReactionT5MultiTask(tr_mn.shape[1], len(seen_ec2), len(seen_ec3), E123.shape[1], E4.shape[1]).to(device)
    else:
        net = SiameseChemBERTaMultiTask(model_name, tr_mn.shape[1], len(seen_ec2), len(seen_ec3), E123.shape[1], E4.shape[1], mode=arch).to(device)

    E123_t, E4_t, l4_vt = torch.from_numpy(E123).to(device), torch.from_numpy(E4).to(device), torch.from_numpy(l4_v).to(device)
    head_params = [p for n, p in net.named_parameters() if not (n.startswith("t5.") or n.startswith("enc."))]
    back_params = [p for n, p in net.named_parameters() if (n.startswith("t5.") or n.startswith("enc."))]
    opt = torch.optim.AdamW([{"params": back_params, "lr": lr}, {"params": head_params, "lr": lr * 6.0}], weight_decay=0.015)
    steps_per_ep = (len(tr_loader) + grad_accum - 1) // grad_accum
    sched = torch.optim.lr_scheduler.OneCycleLR(opt, max_lr=[lr, lr * 6.0], total_steps=epochs * steps_per_ep, pct_start=0.08)

    p1_avg = np.zeros((len(te_df), 7), dtype=np.float32)
    p2_avg = np.zeros((len(te_df), len(seen_ec2)), dtype=np.float32)
    p3_avg = np.zeros((len(te_df), len(seen_ec3)), dtype=np.float32)
    z123_avg = np.zeros((len(te_df), E123.shape[1]), dtype=np.float32)
    z4_avg = np.zeros((len(te_df), E4.shape[1]), dtype=np.float32)
    n_snap = 0

    for ep in range(1, epochs + 1):
        net.train()
        tot_loss = 0.0
        opt.zero_grad()
        t_ep = time.perf_counter()
        for step_i, (a, ma, b_ids, mb, mech, y4, y1, y2, y3) in enumerate(tr_loader):
            a, ma, b_ids, mb, mech = a.to(device, non_blocking=True), ma.to(device, non_blocking=True), b_ids.to(device, non_blocking=True), mb.to(device, non_blocking=True), mech.to(device, non_blocking=True)
            y4, y1, y2, y3 = y4.to(device, non_blocking=True), y1.to(device, non_blocking=True), y2.to(device, non_blocking=True), y3.to(device, non_blocking=True)
            with torch.amp.autocast("cuda", dtype=torch.bfloat16):
                l1, l2, l3, z123, z4 = net(a, ma, b_ids, mb, mech)
            l1, l2, l3, z123, z4 = l1.float(), l2.float(), l3.float(), z123.float(), z4.float()
            loss_1 = F.cross_entropy(l1, y1)
            loss_2 = F.cross_entropy(l2 + 0.40 * log_pri2, y2, label_smoothing=0.05)
            loss_3 = F.cross_entropy(l3 + 0.45 * log_pri3, y3, label_smoothing=0.05)
            t123 = E123_t[y4]
            lg123 = 18.0 * (z123 @ t123.T); lbl = torch.arange(len(y4), device=device)
            loss_123 = 0.5 * (F.cross_entropy(lg123, lbl) + F.cross_entropy(lg123.T, lbl)) + (1.0 - (z123 * t123).sum(-1)).mean()
            vm = l4_vt[y4] > 0.5
            if vm.sum() >= 8:
                z4v = z4[vm]; t4 = E4_t[y4[vm]]
                lg4 = 18.0 * (z4v @ t4.T); lbl4 = torch.arange(len(z4v), device=device)
                loss_4 = 0.5 * (F.cross_entropy(lg4, lbl4) + F.cross_entropy(lg4.T, lbl4)) + (1.0 - (z4v * t4).sum(-1)).mean()
            else:
                loss_4 = torch.tensor(0.0, device=device)
            loss = (0.6 * loss_1 + 0.5 * loss_2 + 1.1 * loss_3 + 0.75 * loss_123 + 0.65 * loss_4) / grad_accum
            loss.backward()
            tot_loss += float(loss.item()) * grad_accum
            if (step_i + 1) % grad_accum == 0 or (step_i + 1) == len(tr_loader):
                torch.nn.utils.clip_grad_norm_(net.parameters(), 1.5)
                opt.step(); sched.step(); opt.zero_grad()
            if ep == 1 and step_i == 60:
                print(f"  [{tag}] step 60/{len(tr_loader)} in {time.perf_counter()-t_ep:.1f}s (max_vram={torch.cuda.max_memory_allocated()/1e9:.1f}GB)", flush=True)

        print(f"[{tag}] ep={ep}/{epochs} loss={tot_loss/len(tr_loader):.4f} ep_dt={time.perf_counter()-t_ep:.1f}s total={time.perf_counter()-t0:.1f}s", flush=True)
        if ep >= max(1, epochs - 1):
            net.eval()
            p1_l, p2_l, p3_l, z1_l, z4_l = [], [], [], [], []
            with torch.no_grad(), torch.amp.autocast("cuda", dtype=torch.bfloat16):
                for a, ma, b_ids, mb, mech in te_loader:
                    l1, l2, l3, z123, z4 = net(a.to(device), ma.to(device), b_ids.to(device), mb.to(device), mech.to(device))
                    p1_l.append(F.softmax(l1.float(), dim=-1).cpu().numpy())
                    p2_l.append(F.softmax(l2.float(), dim=-1).cpu().numpy())
                    p3_l.append(F.softmax(l3.float(), dim=-1).cpu().numpy())
                    z1_l.append(z123.float().cpu().numpy())
                    z4_l.append(z4.float().cpu().numpy())
            p1_avg += np.vstack(p1_l); p2_avg += np.vstack(p2_l); p3_avg += np.vstack(p3_l)
            z123_avg += np.vstack(z1_l); z4_avg += np.vstack(z4_l)
            n_snap += 1

    p1_avg /= n_snap; p2_avg /= n_snap; p3_avg /= n_snap
    z123_avg /= np.maximum(np.linalg.norm(z123_avg, axis=1, keepdims=True), 1e-6)
    z4_avg /= np.maximum(np.linalg.norm(z4_avg, axis=1, keepdims=True), 1e-6)

    del net, opt, sched, tr_loader, te_loader
    gc.collect()
    torch.cuda.empty_cache()
    return {
        "p1": p1_avg, "p2": p2_avg, "p3": p3_avg,
        "z123": z123_avg.astype(np.float16), "z4": z4_avg.astype(np.float16),
        "seen_ec2": np.array(seen_ec2, dtype=str),
        "seen_ec3": np.array(seen_ec3, dtype=str),
    }


def main():
    t_all = time.perf_counter()
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    extract_and_verify_bundle()

    ec_df = pd.read_csv(DATA_DIR / "ec_meta.csv", dtype=str)
    for c in ("l1", "l2", "l3_clean", "l4"):
        ec_df[c] = ec_df[c].fillna("")
    aux = dict(np.load(DATA_DIR / "aux_feats.npz"))
    E123, E4, l4_v = build_text_embeddings(ec_df, aux, device)

    med_tr = pd.read_csv(DATA_DIR / "medium_train.csv")
    med_te = pd.read_csv(DATA_DIR / "medium_test_rxns_only.csv")
    hard_tr = pd.read_csv(DATA_DIR / "hard_train.csv")
    hard_te = pd.read_csv(DATA_DIR / "hard_test_rxns_only.csv")

    results = {"E123": E123.astype(np.float16), "E4": E4.astype(np.float16), "l4_valid": l4_v}

    # Fast HardFull ChemBERTa models FIRST (~15m total -> checkpointed!)
    r_hard_cb = run_stage(
        "HardFull-SiameseCB", "siamese", "seyonec/ChemBERTa-zinc-base-v1",
        hard_tr, aux["hard_tr_mech"], hard_te, aux["hard_te_mech"],
        ec_df, E123, E4, l4_v, epochs=11, bs=96, lr=7e-5, device=device, grad_accum=1, seed=137,
    )
    for k, v in r_hard_cb.items(): results[f"hard_cb_{k}"] = v
    np.savez_compressed(CKPT_PATH, **results)
    print(f"[CKPT_SAVED] after HardFull-SiameseCB ({time.perf_counter()-t_all:.1f}s)", flush=True)

    r_hard_mtr = run_stage(
        "HardFull-CB77MTR", "joint", "DeepChem/ChemBERTa-77M-MTR",
        hard_tr, aux["hard_tr_mech"], hard_te, aux["hard_te_mech"],
        ec_df, E123, E4, l4_v, epochs=14, bs=128, lr=1e-4, device=device, grad_accum=1, seed=2026,
    )
    for k, v in r_hard_mtr.items(): results[f"hard_mtr_{k}"] = v
    np.savez_compressed(CKPT_PATH, **results)
    print(f"[CKPT_SAVED] after HardFull-CB77MTR ({time.perf_counter()-t_all:.1f}s)", flush=True)

    # Full Medium ReactionT5v2 (5 epochs over 57.6k = 9.4x MedCV-epochs updates -> ~58m!)
    r_med_t5 = run_stage(
        "MedFull-T5v2", "t5", "sagawa/ReactionT5v2-forward",
        med_tr, aux["med_tr_mech"], med_te, aux["med_te_mech"],
        ec_df, E123, E4, l4_v, epochs=5, bs=48, lr=8e-5, device=device, grad_accum=2, seed=42,
    )
    for k, v in r_med_t5.items(): results[f"med_t5_{k}"] = v
    np.savez_compressed(CKPT_PATH, **results)
    print(f"[CKPT_SAVED] after MedFull-T5v2 ({time.perf_counter()-t_all:.1f}s)", flush=True)

    # Full Hard ReactionT5v2 (5 epochs over 33.4k -> ~32m!)
    r_hard_t5 = run_stage(
        "HardFull-T5v2", "t5", "sagawa/ReactionT5v2-forward",
        hard_tr, aux["hard_tr_mech"], hard_te, aux["hard_te_mech"],
        ec_df, E123, E4, l4_v, epochs=5, bs=48, lr=8e-5, device=device, grad_accum=2, seed=42,
    )
    for k, v in r_hard_t5.items(): results[f"hard_t5_{k}"] = v

    for k, v in results.items():
        if np.issubdtype(v.dtype, np.floating):
            assert np.isfinite(v).all(), f"Non-finite values in {k}"

    np.savez_compressed(OUT_PATH, **results)
    print(f"[ALL_STAGE2_GPU_DONE] Saved {OUT_PATH} ({OUT_PATH.stat().st_size/1e6:.2f} MB) in {time.perf_counter()-t_all:.1f}s", flush=True)


if __name__ == "__main__":
    main()
