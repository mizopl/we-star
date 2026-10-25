#!/usr/bin/env python3
"""
CLSS Move A — Blind Out-of-Sample GPU Test on Open Cells AME(8, 5) & AME(7, 4)
==============================================================================
Completes the 5/5 Open-Cell Barrier Atlas for n = 7, 8 in the Huber-Wyderka table:
  - n = 7 open cells: AME(7, 4), AME(7, 6)
  - n = 8 open cells: AME(8, 4), AME(8, 5), AME(8, 6)

Pre-Registered Blind Prediction for AME(8, 5) [before GPU execution]:
  - Regime I Law: eta*(8, 5) = sqrt(15/28) = 0.731925  (A_4^* = 37.500)
  - Predicted Frobenius barrier:
      Delta_F^pred(8, 5) = (1 / 25) * sqrt(15 / 28) = 0.029277002
"""

import argparse
import itertools
import json
import math
import time
import numpy as np
import torch


def build_orbits_and_cuts(n, D, device):
    k = n // 2
    N = D ** n
    if n == 2 * k:
        cuts35 = [(0,) + c for c in itertools.combinations(range(1, n), k - 1)]
    else:
        cuts35 = list(itertools.combinations(range(n), k))

    def canon(S):
        S_set = set(S)
        Sc_set = set(range(n)) - S_set
        cands = []
        for sh in range(n):
            cands.append(tuple(sorted((x + sh) % n for x in S_set)))
            if n == 2 * k:
                cands.append(tuple(sorted((x + sh) % n for x in Sc_set)))
        return min(cands)

    orb_map = {}
    for c in cuts35:
        orb_map.setdefault(canon(c), []).append(c)
    orb_reps = sorted(orb_map.keys())
    weights = torch.tensor([len(orb_map[o]) / len(cuts35) for o in orb_reps], dtype=torch.float64, device=device)

    grid = np.arange(N, dtype=np.int64).reshape((D,) * n)
    shifts = [np.transpose(grid, tuple((i + s) % n for i in range(n))).reshape(-1) for s in range(n)]
    shift_idx = torch.tensor(np.stack(shifts, axis=0), dtype=torch.long, device=device)

    def make_gather_tables(cut_list):
        fwd, inv = [], []
        for S in cut_list:
            Sc = tuple(i for i in range(n) if i not in S)
            p = np.transpose(grid, S + Sc).reshape(-1)
            fwd.append(p)
            inv.append(np.argsort(p))
        return (
            torch.tensor(np.stack(fwd, axis=0), dtype=torch.long, device=device),
            torch.tensor(np.stack(inv, axis=0), dtype=torch.long, device=device),
        )

    orb_fwd, orb_inv = make_gather_tables(orb_reps)
    all_fwd, all_inv = make_gather_tables(cuts35)
    return orb_reps, weights, orb_fwd, orb_inv, cuts35, all_fwd, all_inv, shift_idx


def build_f5_graph_seed_8_5(device):
    """
    Constructs the optimal Z_8-circulant graph state over F_5:
      r = [0, 1, 0, 2, 0, 2, 0, 1] mod 5
    which satisfies 26 / 35 four-party cuts (5 out of 7 cyclic orbits have exact 0.0 error).
    """
    r = [0, 1, 0, 2, 0, 2, 0, 1]
    A = np.zeros((8, 8), dtype=np.int64)
    for i in range(8):
        for j in range(8):
            A[i, j] = r[(j - i) % 8]
    N = 5 ** 8
    idx = torch.arange(N, device=device, dtype=torch.long)
    digits = []
    tmp = idx
    for _ in range(8):
        digits.append(tmp % 5)
        tmp = tmp // 5
    X = torch.stack(digits[::-1], dim=1).to(torch.float64)  # (390625, 8)
    A_upper = torch.tensor(np.triu(A, 1), dtype=torch.float64, device=device)
    quad = torch.sum(X * (X @ A_upper.T), dim=1) % 5.0
    phase = (2.0 * math.pi / 5.0) * quad
    psi = torch.exp(1j * phase).to(torch.complex128) / math.sqrt(float(N))
    return psi


def eval_orbits(psi, orb_fwd, R, C):
    num_orb = orb_fwd.shape[0]
    M = psi[orb_fwd].view(num_orb, R, C)
    G = torch.bmm(M, M.conj().transpose(1, 2))
    tr2 = torch.real(torch.sum(G * G.conj(), dim=(1, 2)))
    frobs = torch.sqrt(torch.clamp(tr2 - 1.0 / R, min=0.0))
    return frobs, M, G


def run_cell_hunt(n, D, device, smoke=False, graph_seed=None):
    k = n // 2
    R = D ** k
    C = D ** (n - k)
    N = D ** n
    t0 = time.time()

    orb_reps, weights, orb_fwd, orb_inv, cuts35, all_fwd, all_inv, shift_idx = build_orbits_and_cuts(n, D, device)
    num_orb = len(orb_reps)
    eyeR = torch.eye(R, dtype=torch.complex128, device=device).unsqueeze(0)

    print("\n" + "=" * 78, flush=True)
    print(f"CLSS BLIND GPU ENGINE: Open Cell AME({n}, {D}) [Space: {D}^{n} = {N:,} complex128]", flush=True)
    print(f"  Cuts: {len(cuts35)} of size {R}x{C} ({num_orb} Z_{n} orbits)", flush=True)
    print("=" * 78, flush=True)

    seed_frobs_list = None
    if graph_seed is not None:
        with torch.no_grad():
            sf, _, _ = eval_orbits(graph_seed, orb_fwd, R, C)
            seed_frobs_list = [round(float(x), 7) for x in sf.cpu().tolist()]
            seed_mean = float(torch.sum(weights * sf).item())
        print(f"[BASELINE ALGEBRAIC SEED] {num_orb}-orbit Frobenius errors: {seed_frobs_list}", flush=True)
        print(f"  (Baseline max_Frob = {max(seed_frobs_list):.7f} | weighted mean_Frob = {seed_mean:.7f})", flush=True)

    n_restarts = 1 if smoke else 6
    ns_steps = 10 if smoke else (90 if n == 8 else 150)
    adam_steps = 15 if smoke else (180 if n == 8 else 300)
    lbfgs_iter = 8 if smoke else 50
    stage2_ns_steps = 8 if smoke else 60
    stage2_adam_steps = 6 if smoke else 40

    stage1_logs = []
    stage2_logs = []
    best_mean = 1e9
    best_max = 1e9
    best_orbits = None

    for r in range(n_restarts):
        torch.manual_seed(9500 + 100 * n + 10 * D + r * 37)
        noise = torch.randn(N, dtype=torch.complex128, device=device)
        noise = noise[shift_idx].mean(dim=0)
        noise = noise / torch.linalg.norm(noise)

        if graph_seed is not None and r < 3:
            eps = 0.08 + 0.08 * r
            psi = graph_seed + eps * noise
            seed_type = f"F5_Graph_eps_{eps:.2f}"
        else:
            psi = noise
            seed_type = f"Haar_Z{n}_random_{r + 1}"
        psi = psi[shift_idx].mean(dim=0)
        psi = psi / torch.linalg.norm(psi)

        # Stage 1A: Weighted Z_n Newton-Schulz Isometric Projection
        with torch.no_grad():
            for _ in range(ns_steps):
                _, M, G = eval_orbits(psi, orb_fwd, R, C)
                M_iso = 0.5 * torch.bmm(3.0 * eyeR - R * G, M)
                flat = M_iso.reshape(num_orb, N)
                gathered = torch.gather(flat, 1, orb_inv)
                psi_p = (weights.unsqueeze(1) * gathered).sum(dim=0)
                psi_p = psi_p[shift_idx].mean(dim=0)
                psi_p = psi_p / torch.linalg.norm(psi_p)
                psi = 0.25 * psi + 0.75 * psi_p
                psi = psi / torch.linalg.norm(psi)

        # Stage 1B: AdamW on Weighted Purity + Max-Orbit Penalty
        w_param = psi.clone().detach().requires_grad_(True)
        opt = torch.optim.AdamW([w_param], lr=0.015)
        sched = torch.optim.lr_scheduler.CosineAnnealingLR(opt, T_max=adam_steps, eta_min=2e-4)
        for _ in range(adam_steps):
            opt.zero_grad()
            ps = w_param[shift_idx].mean(dim=0)
            ps = ps / torch.linalg.norm(ps)
            frobs, _, _ = eval_orbits(ps, orb_fwd, R, C)
            loss = torch.sum(weights * (frobs ** 2)) + 0.25 * torch.max(frobs ** 2)
            loss.backward()
            opt.step()
            sched.step()

        # Stage 1C: Exact L-BFGS Polish with Strong Wolfe
        w_lbfgs = (w_param.detach()[shift_idx].mean(dim=0))
        w_lbfgs = (w_lbfgs / torch.linalg.norm(w_lbfgs)).clone().detach().requires_grad_(True)
        lbfgs = torch.optim.LBFGS([w_lbfgs], lr=1.0, max_iter=lbfgs_iter, history_size=20, line_search_fn="strong_wolfe")

        def closure():
            lbfgs.zero_grad()
            ps = w_lbfgs[shift_idx].mean(dim=0)
            ps = ps / torch.linalg.norm(ps)
            frobs, _, _ = eval_orbits(ps, orb_fwd, R, C)
            loss = torch.sum(weights * (frobs ** 2)) * 1e4
            loss.backward()
            return loss

        lbfgs.step(closure)

        with torch.no_grad():
            psi_s1 = w_lbfgs.detach()[shift_idx].mean(dim=0)
            psi_s1 = psi_s1 / torch.linalg.norm(psi_s1)
            frobs1, _, _ = eval_orbits(psi_s1, orb_fwd, R, C)
            max_f1 = float(torch.max(frobs1).item())
            mean_f1 = float(torch.sum(weights * frobs1).item())
            orb_f1 = [round(float(x), 7) for x in frobs1.cpu().tolist()]

        print(
            f"  [Restart {r+1}/{n_restarts} Stage 1 (Z_{n}, {seed_type})] "
            f"max_Frob = {max_f1:.6e} | mean_Frob = {mean_f1:.6e} | orbits = {orb_f1} | t = {time.time()-t0:.1f}s",
            flush=True,
        )
        stage1_logs.append(
            {
                "restart": r + 1,
                "seed_type": seed_type,
                "max_frob": max_f1,
                "mean_frob": mean_f1,
                "orbits": orb_f1,
                "cum_elapsed_sec": round(time.time() - t0, 2),
            }
        )
        if mean_f1 < best_mean:
            best_mean = mean_f1
            best_max = max_f1
            best_orbits = orb_f1

        # Stage 2: Full 35-Cut Unconstrained Symmetry-Breaking Polish on r in (0, 3)
        if smoke or r in (0, 3):
            psi_u = psi_s1.clone().detach()
            noise_u = torch.randn_like(psi_u)
            noise_u = noise_u / torch.linalg.norm(noise_u)
            psi_u = (psi_u + 1e-3 * noise_u)
            psi_u = psi_u / torch.linalg.norm(psi_u)

            with torch.no_grad():
                for _ in range(stage2_ns_steps):
                    acc_u = torch.zeros_like(psi_u)
                    for start in range(0, 35, 7):
                        sub_fwd = all_fwd[start : start + 7]
                        sub_inv = all_inv[start : start + 7]
                        M = psi_u[sub_fwd].view(7, R, C)
                        G = torch.bmm(M, M.conj().transpose(1, 2))
                        M_iso = 0.5 * torch.bmm(3.0 * eyeR - R * G, M)
                        flat = M_iso.reshape(7, N)
                        acc_u += torch.gather(flat, 1, sub_inv).sum(dim=0) / 35.0
                    psi_u = 0.25 * psi_u + 0.75 * acc_u
                    psi_u = psi_u / torch.linalg.norm(psi_u)

            w_full = psi_u.clone().detach().requires_grad_(True)
            opt2 = torch.optim.AdamW([w_full], lr=5e-4)
            for _ in range(stage2_adam_steps):
                opt2.zero_grad()
                for start in range(0, 35, 7):
                    sub_fwd = all_fwd[start : start + 7]
                    psi_n = w_full / torch.linalg.norm(w_full)
                    M = psi_n[sub_fwd].view(7, R, C)
                    G = torch.bmm(M, M.conj().transpose(1, 2))
                    tr2 = torch.real(torch.sum(G * G.conj(), dim=(1, 2)))
                    f2 = torch.clamp(tr2 - 1.0 / R, min=0.0)
                    loss_c = torch.sum(f2) / 35.0
                    loss_c.backward()
                opt2.step()

            with torch.no_grad():
                psi_final = w_full.detach() / torch.linalg.norm(w_full.detach())
                frobs35_list = []
                for start in range(0, 35, 7):
                    sub_fwd = all_fwd[start : start + 7]
                    f_sub, _, _ = eval_orbits(psi_final, sub_fwd, R, C)
                    frobs35_list.append(f_sub)
                frobs35 = torch.cat(frobs35_list, dim=0)
                max_f2 = float(torch.max(frobs35).item())
                mean_f2 = float(torch.mean(frobs35).item())
                frobs_orb2, _, _ = eval_orbits(psi_final, orb_fwd, R, C)
                orb_f2 = [round(float(x), 7) for x in frobs_orb2.cpu().tolist()]

            print(
                f"  [Restart {r+1}/{n_restarts} Stage 2 (35-Cut Unconstrained)] "
                f"max_Frob = {max_f2:.6e} | mean_Frob = {mean_f2:.6e} | t = {time.time()-t0:.1f}s",
                flush=True,
            )
            stage2_logs.append(
                {
                    "restart": r + 1,
                    "max_35cut_frob": max_f2,
                    "mean_35cut_frob": mean_f2,
                    "orbit_reps_frob": orb_f2,
                    "cum_elapsed_sec": round(time.time() - t0, 2),
                }
            )
            if mean_f2 < best_mean:
                best_mean = mean_f2
                best_max = max_f2
                best_orbits = orb_f2

    dp_haar = (R + C) / (R * C + 1.0) - 1.0 / R
    df_haar = math.sqrt(dp_haar)
    eta_star = best_mean / df_haar
    Ak_star = R * math.comb(n, k) * (best_mean ** 2)

    return {
        "target": f"AME({n}, {D})",
        "baseline_seed_orbit_frobs": seed_frobs_list,
        "best_max_frob": best_max,
        "best_mean_frob": best_mean,
        "best_orbit_frobs": best_orbits,
        "haar_frob": df_haar,
        "eta_star": round(eta_star, 6),
        "eta_star_sq": round(eta_star ** 2, 6),
        "irreducible_shor_laflamme_A_k_star": round(Ak_star, 6),
        "stage1_restarts": stage1_logs,
        "stage2_restarts": stage2_logs,
        "elapsed_sec": round(time.time() - t0, 2),
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--smoke", action="store_true")
    args = parser.parse_args()

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    if torch.cuda.is_available():
        print(
            f"[GPU DETECTED] {torch.cuda.get_device_name(0)} "
            f"(VRAM: {torch.cuda.get_device_properties(0).total_memory / 1e9:.2f} GB)",
            flush=True,
        )
    else:
        print("[CPU MODE] Running local smoke test on CPU", flush=True)

    # Pre-registered blind prediction for AME(8, 5)
    pred_8_5 = math.sqrt(15.0 / 28.0) / 25.0
    print(f"\n[PRE-REGISTERED BLIND PREDICTION] AME(8, 5): Delta_F^pred = {pred_8_5:.7f} (eta^pred = 0.731925, A_4^pred = 37.500)", flush=True)

    f5_seed = build_f5_graph_seed_8_5(device)
    res_8_5 = run_cell_hunt(8, 5, device, smoke=args.smoke, graph_seed=f5_seed)
    res_7_4 = run_cell_hunt(7, 4, device, smoke=args.smoke, graph_seed=None)

    rel_err_8_5 = abs(res_8_5["best_mean_frob"] - pred_8_5) / pred_8_5 * 100.0
    summary = {
        "pre_registered_prediction_8_5": {
            "formula": "(1/25) * sqrt(15/28)",
            "predicted_delta_f": pred_8_5,
            "predicted_eta": math.sqrt(15.0 / 28.0),
            "predicted_A_4_star": 37.5,
            "measured_best_mean_frob": res_8_5["best_mean_frob"],
            "measured_best_max_frob": res_8_5["best_max_frob"],
            "measured_eta_star": res_8_5["eta_star"],
            "measured_A_4_star": res_8_5["irreducible_shor_laflamme_A_k_star"],
            "relative_error_pct": round(rel_err_8_5, 4),
            "inside_mean_max_bracket": (res_8_5["best_mean_frob"] <= pred_8_5 <= res_8_5["best_max_frob"]),
        },
        "AME_8_5": res_8_5,
        "AME_7_4": res_7_4,
    }
    print("\n=== CLSS MOVE A SUMMARY (AME(8, 5) & AME(7, 4)) ===", flush=True)
    print(json.dumps(summary, indent=2), flush=True)


if __name__ == "__main__":
    main()
