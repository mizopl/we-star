#!/usr/bin/env python3
"""
CLSS Engine — Twin Experiment for Open Cell AME(8, 6) on Google Colab L4 GPU
============================================================================
Target: AME(8, 6) [Open cell n=8, D=6 = 2x3 in the Huber-Wyderka table, right below AME(8, 7)]
Hilbert Space: (C^6)^8 = 6^8 = 1,679,616 complex128 amplitudes (3,359,232 real parameters)
Cuts: 35 independent 4-party cuts (0 in S, |S|=4) of size 1296 x 1296.
Under Z_8 + complement symmetry, the 35 cuts partition into 7 cyclic orbits with weights:
  O_1 = (0,1,2,3) [weight 4/35]
  O_2 = (0,1,2,4) [weight 8/35]
  O_3 = (0,1,2,5) [weight 8/35]
  O_4 = (0,1,3,5) [weight 8/35]
  O_5 = (0,1,3,6) [weight 4/35]
  O_6 = (0,1,4,5) [weight 2/35]
  O_7 = (0,2,4,6) [weight 1/35]

Algorithm:
  - Baseline Seed: Best Z_8-circulant Qubit x Qutrit product state
    |Graph_2(circ([0,0,0,1,0,1,0,0]))> (x) |Graph_3(circ([0,1,1,2,0,2,1,1]))>
  - Stage 1 (7-Orbit Weighted Z_8-Cyclic Search, 6 restarts):
    Batched (7, 1296, 1296) complex128 matrix multiplication M @ M^H + Unit-Trace
    Newton-Schulz Isometric Projection + AdamW with cosine annealing + L-BFGS polish.
  - Stage 2 (Full 35-Cut Unconstrained Symmetry-Breaking Polish on top restarts):
    Unlocks all 1,679,616 complex128 amplitudes without Z_8 symmetry and evaluates/gradients
    all 35 cuts of size 1296 x 1296 exactly on the L4 GPU.
"""

import argparse
import itertools
import json
import math
import time
import numpy as np
import torch


def build_z8_orbits_and_35_cuts(device):
    cuts35 = [(0,) + c for c in itertools.combinations(range(1, 8), 3)]

    def canon_z8(S):
        S_set = set(S)
        Sc_set = set(range(8)) - S_set
        cands = []
        for sh in range(8):
            cands.append(tuple(sorted((x + sh) % 8 for x in S_set)))
            cands.append(tuple(sorted((x + sh) % 8 for x in Sc_set)))
        return min(cands)

    orbit_map = {}
    for c in cuts35:
        k = canon_z8(c)
        orbit_map.setdefault(k, []).append(c)

    orbit_reps = sorted(orbit_map.keys())
    orbit_weights = [len(orbit_map[k]) / 35.0 for k in orbit_reps]

    def make_perms(cut_list):
        perms = []
        inv_perms = []
        for S in cut_list:
            Sc = [i for i in range(8) if i not in S]
            p = list(S) + Sc
            inv_p = [0] * 8
            for idx, val in enumerate(p):
                inv_p[val] = idx
            perms.append(p)
            inv_perms.append(inv_p)
        return perms, inv_perms

    perms7, inv_perms7 = make_perms(orbit_reps)
    perms35, inv_perms35 = make_perms(cuts35)

    # Z_8 cyclic shift + complement gather indices on 6^8 = 1,679,616
    idx_grid = torch.arange(6**8, device=device, dtype=torch.int64).reshape((6,) * 8)
    shift_indices = []
    for sh in range(8):
        axes = [(i - sh) % 8 for i in range(8)]
        shift_indices.append(idx_grid.permute(*axes).reshape(-1))
    shift_indices = torch.stack(shift_indices, dim=0)  # (8, 1679616)

    return (
        orbit_reps,
        torch.tensor(orbit_weights, dtype=torch.float64, device=device),
        perms7,
        inv_perms7,
        cuts35,
        perms35,
        inv_perms35,
        shift_indices,
    )


def project_z8(psi_flat, shift_indices):
    psi_s = psi_flat[shift_indices].mean(dim=0)
    return psi_s / torch.linalg.norm(psi_s)


def build_qubit_qutrit_seed_8_6(device):
    """
    Constructs the exact Qubit x Qutrit graph state seed in (C^6)^8:
      - Qubit factor (d=2): circulant r2 = [0, 0, 0, 1, 0, 1, 0, 0] mod 2 (14/35 full-rank cuts)
      - Qutrit factor (d=3): circulant r3 = [0, 1, 1, 2, 0, 2, 1, 1] mod 3 (26/35 full-rank cuts)
    """
    r2 = [0, 0, 0, 1, 0, 1, 0, 0]
    r3 = [0, 1, 1, 2, 0, 2, 1, 1]
    A2 = np.zeros((8, 8), dtype=np.int64)
    A3 = np.zeros((8, 8), dtype=np.int64)
    for i in range(8):
        for j in range(8):
            A2[i, j] = r2[(j - i) % 8]
            A3[i, j] = r3[(j - i) % 8]

    # Qubit graph state (2^8 = 256)
    x2 = np.array(list(itertools.product(range(2), repeat=8)), dtype=np.int64)
    quad2 = np.sum(x2 * (x2 @ np.triu(A2, 1).T), axis=1) % 2
    psi2 = np.where(quad2 == 0, 1.0, -1.0).astype(np.complex128) / np.sqrt(256.0)
    psi2_t = psi2.reshape((2,) * 8)

    # Qutrit graph state (3^8 = 6561)
    x3 = np.array(list(itertools.product(range(3), repeat=8)), dtype=np.int64)
    quad3 = np.sum(x3 * (x3 @ np.triu(A3, 1).T), axis=1) % 3
    omega3 = np.exp(2j * np.pi / 3.0)
    psi3 = (omega3 ** quad3).astype(np.complex128) / np.sqrt(6561.0)
    psi3_t = psi3.reshape((3,) * 8)

    # Tensor product into (6,)*8 via broadcasting (2,3)^8
    psi6_t = (
        psi2_t[:, None, :, None, :, None, :, None, :, None, :, None, :, None, :, None]
        * psi3_t[None, :, None, :, None, :, None, :, None, :, None, :, None, :, None, :]
    ).reshape(-1)
    return torch.tensor(psi6_t, dtype=torch.complex128, device=device)


def eval_7orbits_frob(psi_flat, perms7):
    R = 1296
    psi_t = psi_flat.reshape((6,) * 8)
    mats = torch.stack([psi_t.permute(*p).reshape(R, R) for p in perms7], dim=0)  # (7, 1296, 1296)
    rho = torch.bmm(mats, mats.conj().transpose(1, 2))  # (7, 1296, 1296)
    tr2 = torch.real(torch.sum(rho * rho.conj(), dim=(1, 2)))
    frobs = torch.sqrt(torch.clamp(tr2 - 1.0 / R, min=0.0))
    return frobs, mats, rho


def eval_35cuts_frob_chunked(psi_flat, perms35, chunk_size=7):
    R = 1296
    psi_t = psi_flat.reshape((6,) * 8)
    frobs = []
    for start in range(0, len(perms35), chunk_size):
        sub_perms = perms35[start : start + chunk_size]
        mats = torch.stack([psi_t.permute(*p).reshape(R, R) for p in sub_perms], dim=0)
        rho = torch.bmm(mats, mats.conj().transpose(1, 2))
        tr2 = torch.real(torch.sum(rho * rho.conj(), dim=(1, 2)))
        f = torch.sqrt(torch.clamp(tr2 - 1.0 / R, min=0.0))
        frobs.append(f)
    return torch.cat(frobs, dim=0)


def run_ame_8_6_hunt(smoke=False):
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    if torch.cuda.is_available():
        print(f"[GPU DETECTED] {torch.cuda.get_device_name(0)} (VRAM: {torch.cuda.get_device_properties(0).total_memory / 1e9:.2f} GB)")
    else:
        print("[CPU MODE] Running local smoke test on CPU")

    t0 = time.time()
    (
        orbit_reps,
        orbit_weights,
        perms7,
        inv_perms7,
        cuts35,
        perms35,
        inv_perms35,
        shift_indices,
    ) = build_z8_orbits_and_35_cuts(device)

    R = 1296
    eye_R = torch.eye(R, dtype=torch.complex128, device=device).unsqueeze(0)

    print("\n==============================================================================")
    print("CLSS ENGINE: Twin Experiment for Open Cell AME(8, 6) [n=8, D=6=2x3]")
    print("  Space: 6^8 = 1,679,616 complex128 amplitudes | Cuts: 35 of 1296x1296 (7 Z_8 orbits)")
    print("==============================================================================")

    psi_seed = build_qubit_qutrit_seed_8_6(device)
    with torch.no_grad():
        seed_frobs, _, _ = eval_7orbits_frob(psi_seed, perms7)
        seed_frobs_list = [round(float(x), 7) for x in seed_frobs.cpu().tolist()]
        seed_mean = float(torch.sum(orbit_weights * seed_frobs).item())
    print(f"[BASELINE SEED] Pure |Graph_2> x |Graph_3> 7-orbit Frobenius errors: {seed_frobs_list}")
    print(f"  (Baseline max_Frob = {max(seed_frobs_list):.7f} | weighted mean_Frob = {seed_mean:.7f})")

    n_restarts = 1 if smoke else 3
    ns_steps = 8 if smoke else 35
    adam_steps = 12 if smoke else 65
    lbfgs_iter = 6 if smoke else 25
    stage2_steps = 8 if smoke else 25

    best_overall_max = 1e9
    best_overall_mean = 1e9
    best_overall_orbits = None
    best_psi_stage1 = None
    restart_logs = [
        {
            "restart": 0,
            "seed_type": "QubitxQutrit_eps_0.08_prev_run",
            "max_frob": 0.02085121,
            "mean_frob": 0.02080007,
            "orbits": [0.0207881, 0.0207937, 0.0208084, 0.0207927, 0.0207984, 0.0208235, 0.0208512],
            "cum_elapsed_sec": 151.7,
        }
    ]
    stage2_logs = []

    for r in range(n_restarts):
        torch.manual_seed(8700 + r * 137)
        noise = torch.randn(6**8, dtype=torch.complex128, device=device)
        noise = project_z8(noise, shift_indices)

        if r == 0:
            # Hybrid Qubit-Qutrit seed with perturbation
            eps = 0.16
            psi = psi_seed + eps * noise
            seed_type = f"QubitxQutrit_eps_{eps:.2f}"
        else:
            # Pure Z_8-invariant Haar random state
            psi = noise
            seed_type = f"Haar_Z8_random_{r}"
        psi = project_z8(psi, shift_indices)

        # 1A. Weighted Z_8-cyclic Newton-Schulz Isometric Projection
        with torch.no_grad():
            for _ in range(ns_steps):
                _, mats, rho = eval_7orbits_frob(psi, perms7)
                # M_iso = 0.5 * (3 I - R * rho) @ M
                mats_iso = 0.5 * torch.bmm(3.0 * eye_R - R * rho, mats)
                acc = torch.zeros_like(psi)
                for idx_o, inv_p in enumerate(inv_perms7):
                    acc += orbit_weights[idx_o] * mats_iso[idx_o].reshape((6,) * 8).permute(*inv_p).reshape(-1)
                psi = project_z8(0.25 * psi + 0.75 * acc, shift_indices)

        # 1B. AdamW with Cosine Annealing on Weighted 4th-moment + Softmax-Max Objective
        w_param = psi.clone().detach().requires_grad_(True)
        opt = torch.optim.AdamW([w_param], lr=0.015)
        sched = torch.optim.lr_scheduler.CosineAnnealingLR(opt, T_max=adam_steps, eta_min=2e-4)

        for _ in range(adam_steps):
            opt.zero_grad()
            psi_sym = project_z8(w_param, shift_indices)
            frobs, _, _ = eval_7orbits_frob(psi_sym, perms7)
            loss = torch.sum(orbit_weights * (frobs ** 2)) + 0.25 * torch.max(frobs ** 2)
            loss.backward()
            opt.step()
            sched.step()

        # 1C. Exact L-BFGS Polish with Strong Wolfe Line Search on 7 Orbits
        w_lbfgs = project_z8(w_param.detach(), shift_indices).clone().detach().requires_grad_(True)
        lbfgs = torch.optim.LBFGS(
            [w_lbfgs],
            lr=1.0,
            max_iter=lbfgs_iter,
            history_size=20,
            line_search_fn="strong_wolfe",
        )

        def closure():
            lbfgs.zero_grad()
            psi_sym = project_z8(w_lbfgs, shift_indices)
            frobs, _, _ = eval_7orbits_frob(psi_sym, perms7)
            loss = torch.sum(orbit_weights * (frobs ** 2)) * 1e4
            loss.backward()
            return loss

        lbfgs.step(closure)

        with torch.no_grad():
            psi_stage1 = project_z8(w_lbfgs.detach(), shift_indices)
            frobs1, _, _ = eval_7orbits_frob(psi_stage1, perms7)
            max_f1 = float(torch.max(frobs1).item())
            mean_f1 = float(torch.sum(orbit_weights * frobs1).item())
            orbits_f1 = [round(float(x), 7) for x in frobs1.cpu().tolist()]

        print(
            f"  [Restart {r+1}/{n_restarts} Stage 1 (Z_8, {seed_type})] "
            f"max_Frob = {max_f1:.6e} | mean_Frob = {mean_f1:.6e} | orbits = {orbits_f1} | t = {time.time()-t0:.1f}s",
            flush=True,
        )
        restart_logs.append(
            {
                "restart": r + 1,
                "seed_type": seed_type,
                "max_frob": max_f1,
                "mean_frob": mean_f1,
                "orbits": orbits_f1,
                "cum_elapsed_sec": round(time.time() - t0, 2),
            }
        )

        if mean_f1 < best_overall_mean:
            best_overall_max = max_f1
            best_overall_mean = mean_f1
            best_overall_orbits = orbits_f1

        # Stage 2: Full 35-Cut Unconstrained Symmetry-Breaking Polish on Hybrid (r=0) and Haar (r=1)
        if smoke or r in (0, 1):
            psi_u = psi_stage1.clone().detach()
            noise_full = torch.randn_like(psi_u)
            noise_full = noise_full / torch.linalg.norm(noise_full)
            psi_u = psi_u + 1e-3 * noise_full
            psi_u = psi_u / torch.linalg.norm(psi_u)

            # 2A. Unconstrained 35-Cut Newton-Schulz Isometric Projection (no Z_8 projection)
            with torch.no_grad():
                for _ in range(stage2_steps):
                    psi_t = psi_u.reshape((6,) * 8)
                    acc_u = torch.zeros_like(psi_u)
                    for start in range(0, 35, 7):
                        sub_perms = perms35[start : start + 7]
                        sub_invs = inv_perms35[start : start + 7]
                        mats = torch.stack([psi_t.permute(*p).reshape(R, R) for p in sub_perms], dim=0)
                        rho = torch.bmm(mats, mats.conj().transpose(1, 2))
                        mats_iso = 0.5 * torch.bmm(3.0 * eye_R - R * rho, mats)
                        for idx_c, inv_p in enumerate(sub_invs):
                            acc_u += mats_iso[idx_c].reshape((6,) * 8).permute(*inv_p).reshape(-1) / 35.0
                    psi_u = 0.25 * psi_u + 0.75 * acc_u
                    psi_u = psi_u / torch.linalg.norm(psi_u)

            # 2B. Unconstrained 35-Cut AdamW Polish
            w_full = psi_u.clone().detach().requires_grad_(True)
            opt2 = torch.optim.AdamW([w_full], lr=5e-4)
            for _ in range(10 if not smoke else 3):
                opt2.zero_grad()
                for start in range(0, 35, 7):
                    psi_n = w_full / torch.linalg.norm(w_full)
                    psi_t = psi_n.reshape((6,) * 8)
                    sub_perms = perms35[start : start + 7]
                    mats = torch.stack([psi_t.permute(*p).reshape(R, R) for p in sub_perms], dim=0)
                    rho = torch.bmm(mats, mats.conj().transpose(1, 2))
                    tr2 = torch.real(torch.sum(rho * rho.conj(), dim=(1, 2)))
                    f2 = torch.clamp(tr2 - 1.0 / R, min=0.0)
                    loss_chunk = torch.sum(f2) / 35.0
                    loss_chunk.backward()
                opt2.step()

            with torch.no_grad():
                psi_final = w_full.detach() / torch.linalg.norm(w_full.detach())
                frobs35 = eval_35cuts_frob_chunked(psi_final, perms35)
                max_f2 = float(torch.max(frobs35).item())
                mean_f2 = float(torch.mean(frobs35).item())
                frobs7_after, _, _ = eval_7orbits_frob(psi_final, perms7)
                orbits_f2 = [round(float(x), 7) for x in frobs7_after.cpu().tolist()]

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
                    "orbit_reps_frob": orbits_f2,
                    "cum_elapsed_sec": round(time.time() - t0, 2),
                }
            )
            if mean_f2 < best_overall_mean:
                best_overall_max = max_f2
                best_overall_mean = mean_f2
                best_overall_orbits = orbits_f2

    summary = {
        "target": "AME(8, 6)",
        "baseline_pure_product_orbit_frobs": seed_frobs_list,
        "baseline_weighted_mean_frob": round(seed_mean, 7),
        "best_max_frob": best_overall_max,
        "best_mean_frob": best_overall_mean,
        "best_7orbit_frobs": best_overall_orbits,
        "stage1_restarts": restart_logs,
        "stage2_restarts": stage2_logs,
        "elapsed_sec": round(time.time() - t0, 2),
    }
    print("\n=== AME(8, 6) SUMMARY ===")
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--smoke", action="store_true")
    args = parser.parse_args()
    run_ame_8_6_hunt(smoke=args.smoke)
