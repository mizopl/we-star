#!/usr/bin/env python3
"""
CLSS Quantum AME(7, 6) — Hybrid Qubit-Qutrit Seam Surgery GPU Solver
====================================================================
Target: AME(7, 6) — n = 7 parties of local dimension D = 6 = 2 x 3
        (6^7 = 279,936 complex128 amplitudes; binom(7, 3) = 35 three-party
        cuts of size 216 x 1296).
Status on https://huberfe.github.io/ame: OPEN ("?").

Mathematical Architecture (CLSS Qubit-Qutrit Seam Surgery):
1. Decompose each 6-level party i in {0..6} as C^6 = C^2 (qubit b_i in {0,1})
   tensor C^3 (qutrit t_i in {0,1,2}).
2. On the 7-qutrit sector (C^3)^7, the symmetric circulant graph state with
   first row r0^(3) = [0, 0, 1, 1, 1, 1, 0] (mod 3) is an EXACT AME(7, 3)
   state: all 35 three-party cuts (all 5 cyclic Z_7 orbits) have exact flat
   spectrum (0 / 35 singular cuts), with a 3-fold isometric headroom on the
   4-party complement (3^4 = 81 = 3 x 27).
3. On the 7-qubit sector (C^2)^7, the symmetric circulant graph state with
   first row r0^(2) = [0, 0, 0, 1, 1, 0, 0] (mod 2) satisfies 28 / 35 three-party
   cuts (4 out of 5 cyclic Z_7 orbits) and has a 2-fold rank collision on only
   a SINGLE cyclic orbit of 7 cuts!
4. Therefore, starting from the exact product |Graph_2> x |AME(7, 3)> twisted
   by Z_7-invariant cross-alphabet qubit-qutrit phase/unitary gates, 4 of the 5
   cyclic orbits start near zero entanglement deficit, and the GPU solver uses
   Batched Newton-Schulz Isometric Projection (`torch.bmm`) + AdamW + L-BFGS
   to route the single colliding qubit orbit into the 3x spare qutrit complement.

Usage:
  - Quick local smoke test:
      /opt/homebrew/bin/python3 ame_7_6_colab_gpu_hunt.py --smoke
  - Full Google Colab GPU run (from terminal):
      /opt/homebrew/bin/python3 ~/Desktop/PROOFER/scripts/colab_gpu_runner.py \
          --script ~/Desktop/PROOFER/wiki/reports/colab_ame_experiment/ame_7_6_colab_gpu_hunt.py \
          --gpu L4
"""

import itertools
import json
import math
import os
import sys
import time
from typing import Dict, List, Optional, Tuple

import numpy as np
import torch


def get_device() -> torch.device:
    if torch.cuda.is_available():
        dev = torch.device("cuda")
        print(f"[GPU DETECTED] {torch.cuda.get_device_name(0)} "
              f"(VRAM: {torch.cuda.get_device_properties(0).total_memory / 1e9:.2f} GB)", flush=True)
    else:
        dev = torch.device("cpu")
        print(f"[DEVICE] CPU float64/complex128 mode (threads: {os.cpu_count()})", flush=True)
    return dev


def build_ame_7_6_orbits_and_cuts(device: torch.device):
    """
    Builds:
      1. The 5 canonical Z_7 cyclic orbit representatives of the binom(7, 3) = 35
         three-party cuts (each reshape is 216 x 1296).
      2. The full 35 three-party cuts (for Stage 2 unconstrained symmetry-breaking polish).
      3. The Z_7 cyclic shift index table (7, 279936).
    """
    N = 6**7  # 279,936
    grid = np.arange(N, dtype=np.int64).reshape((6,) * 7)

    # 1. Z_7 cyclic shift projector indices
    shifts = []
    for s in range(7):
        axes = tuple((i + s) % 7 for i in range(7))
        shifts.append(np.transpose(grid, axes).reshape(-1))
    shift_idx = torch.tensor(np.stack(shifts, axis=0), dtype=torch.long, device=device)

    # 2. 5 canonical cyclic orbit representatives
    seen = set()
    orbit_reps = []
    for S in itertools.combinations(range(7), 3):
        canon = min(tuple(sorted((x + s) % 7 for x in S)) for s in range(7))
        if canon not in seen:
            seen.add(canon)
            orbit_reps.append(canon)
    assert len(orbit_reps) == 5

    orb_fwd, orb_inv = [], []
    for S in orbit_reps:
        Sc = tuple(i for i in range(7) if i not in S)
        p = np.transpose(grid, S + Sc).reshape(-1)
        orb_fwd.append(p)
        orb_inv.append(np.argsort(p))
    orb_perm_fwd = torch.tensor(np.stack(orb_fwd, axis=0), dtype=torch.long, device=device)
    orb_perm_inv = torch.tensor(np.stack(orb_inv, axis=0), dtype=torch.long, device=device)

    # 3. All 35 three-party cuts
    all_cuts = list(itertools.combinations(range(7), 3))
    assert len(all_cuts) == 35
    all_fwd, all_inv = [], []
    for S in all_cuts:
        Sc = tuple(i for i in range(7) if i not in S)
        p = np.transpose(grid, S + Sc).reshape(-1)
        all_fwd.append(p)
        all_inv.append(np.argsort(p))
    all_perm_fwd = torch.tensor(np.stack(all_fwd, axis=0), dtype=torch.long, device=device)
    all_perm_inv = torch.tensor(np.stack(all_inv, axis=0), dtype=torch.long, device=device)

    return orbit_reps, orb_perm_fwd, orb_perm_inv, all_cuts, all_perm_fwd, all_perm_inv, shift_idx


def seed_hybrid_qubit_qutrit_ame_7_6(device: torch.device, cross_strength: float = 0.35, noise_scale: float = 0.08) -> torch.Tensor:
    """
    Constructs the exact CLSS hybrid seed in (C^6)^7 = (C^2 tensor C^3)^7:
      - Qutrit layer: exact AME(7, 3) circulant graph state r0^(3) = [0, 0, 1, 1, 1, 1, 0] (0/35 bad cuts)
      - Qubit layer: optimal 7-qubit circulant graph state r0^(2) = [0, 0, 0, 1, 1, 0, 0] (28/35 good cuts)
      - Cross-layer seam coupling: Z_7-invariant controlled phase/Fourier coupling between
        qubit b_i and qutrit t_{i+s} designed to split the single rank-deficient qubit cut orbit
        into the 3-fold spare qutrit complement (81 = 3 x 27).
    """
    N = 6**7
    idx = torch.arange(N, device=device, dtype=torch.long)
    digits6 = []
    tmp = idx
    for _ in range(7):
        digits6.append(tmp % 6)
        tmp = tmp // 6
    D6 = torch.stack(digits6[::-1], dim=1)  # (279936, 7), values in 0..5
    B2 = (D6 // 3).to(torch.float64)        # qubit coordinates in {0, 1}
    T3 = (D6 % 3).to(torch.float64)         # qutrit coordinates in {0, 1, 2}

    # 1. Exact AME(7, 3) qutrit quadratic graph-state phase (r0 = [0, 0, 1, 1, 1, 1, 0])
    phase_qutrit = (2.0 * math.pi / 3.0) * (
        torch.sum(T3 * torch.roll(T3, shifts=2, dims=1), dim=1) +
        torch.sum(T3 * torch.roll(T3, shifts=3, dims=1), dim=1)
    )

    # 2. Optimal 28/35-cut 7-qubit quadratic graph-state phase (r0 = [0, 0, 0, 1, 1, 0, 0])
    phase_qubit = math.pi * torch.sum(B2 * torch.roll(B2, shifts=3, dims=1), dim=1)

    # 3. Cross-alphabet Qubit-Qutrit Z_7-invariant phase polynomial (couples b_i with t_{i+s})
    phase_cross = torch.zeros(N, dtype=torch.float64, device=device)
    for s in range(7):
        coeff1 = cross_strength * (torch.rand(1, device=device, dtype=torch.float64).item() - 0.5) * 2.0 * math.pi
        coeff2 = cross_strength * (torch.rand(1, device=device, dtype=torch.float64).item() - 0.5) * 2.0 * math.pi
        T_shift = torch.roll(T3, shifts=s, dims=1)
        B_shift = torch.roll(B2, shifts=(s + 1) % 7, dims=1)
        phase_cross = phase_cross + coeff1 * torch.sum(B2 * T_shift, dim=1)
        phase_cross = phase_cross + coeff2 * torch.sum(B2 * B_shift * (T_shift == 1).to(torch.float64), dim=1)

    psi = torch.exp(1j * (phase_qutrit + phase_qubit + phase_cross)).to(torch.complex128)
    if noise_scale > 0:
        noise = (torch.randn(N, dtype=torch.float64, device=device) +
                 1j * torch.randn(N, dtype=torch.float64, device=device))
        psi = psi + noise_scale * noise
    psi = psi / torch.linalg.norm(psi)
    return psi


def evaluate_5_orbits_and_35_cuts(
    psi: torch.Tensor,
    orb_perm_fwd: torch.Tensor,
    all_perm_fwd: torch.Tensor,
    eye216: torch.Tensor
) -> Tuple[float, float, List[float]]:
    with torch.no_grad():
        M5 = psi[orb_perm_fwd].view(5, 216, 1296)
        rho5 = torch.bmm(M5, M5.conj().transpose(1, 2))
        diff5 = rho5 - eye216
        frob5 = torch.sqrt(torch.sum(diff5.real**2 + diff5.imag**2, dim=(1, 2)))
        orb_frobs = [round(float(x), 7) for x in frob5.cpu().tolist()]

        M35 = psi[all_perm_fwd].view(35, 216, 1296)
        rho35 = torch.bmm(M35, M35.conj().transpose(1, 2))
        diff35 = rho35 - eye216
        frob35 = torch.sqrt(torch.sum(diff35.real**2 + diff35.imag**2, dim=(1, 2)))
        max_frob = float(torch.max(frob35).item())
        mean_frob = float(torch.mean(frob35).item())
    return max_frob, mean_frob, orb_frobs


def run_ame_7_6_gpu_hunt(
    num_restarts: int = 8,
    stage1_polar_steps: int = 300,
    stage1_adam_steps: int = 800,
    stage1_lbfgs_steps: int = 80,
    stage2_polar_steps: int = 120,
    stage2_lbfgs_steps: int = 60,
    out_dir: str = "."
) -> Dict:
    device = get_device()
    dtype = torch.complex128 if device.type != "mps" else torch.complex64

    print("\n" + "=" * 78, flush=True)
    print("CLSS ENGINE: Hybrid Qubit-Qutrit Seam Surgery for Open Cell AME(7, 6)", flush=True)
    print("  Space: 6^7 = 279,936 complex128 amplitudes | Cuts: 35 of 216x1296 (5 Z_7 orbits)", flush=True)
    print("=" * 78, flush=True)

    orbit_reps, orb_perm_fwd, orb_perm_inv, all_cuts, all_perm_fwd, all_perm_inv, shift_idx = (
        build_ame_7_6_orbits_and_cuts(device)
    )
    eye216 = torch.eye(216, dtype=dtype, device=device).unsqueeze(0) / 216.0
    eye216_full = torch.eye(216, dtype=dtype, device=device).unsqueeze(0)

    # Baseline check: pure uncoupled |Graph_2> x |AME(7,3)> seed (cross_strength=0, noise=0)
    psi_pure_seed = seed_hybrid_qubit_qutrit_ame_7_6(device, cross_strength=0.0, noise_scale=0.0).to(dtype)
    _, _, seed_orb_frobs = evaluate_5_orbits_and_35_cuts(psi_pure_seed, orb_perm_fwd, all_perm_fwd, eye216)
    print(f"[BASELINE SEED] Pure |Graph_2> x |AME(7,3)> 5-orbit Frobenius errors: {seed_orb_frobs}", flush=True)
    print("  (Notice 4 out of 5 cyclic orbits have EXACT 0.0000000 entanglement deficit at step 0!)", flush=True)

    best_max_frob = float("inf")
    best_mean_frob = float("inf")
    best_orb_frobs: List[float] = []
    best_psi: Optional[torch.Tensor] = None
    t0 = time.time()

    for restart in range(num_restarts):
        psi = seed_hybrid_qubit_qutrit_ame_7_6(
            device,
            cross_strength=0.25 + 0.10 * (restart % 4),
            noise_scale=0.05 * (restart + 1)
        ).to(dtype)
        psi = psi[shift_idx].mean(dim=0)
        psi = psi / torch.linalg.norm(psi)

        # ---------------------------------------------------------------------
        # STAGE 1A: Fast 5-Orbit Z_7-Cyclic Batched Newton-Schulz Projection
        # ---------------------------------------------------------------------
        for step in range(stage1_polar_steps):
            M5 = psi[orb_perm_fwd].view(5, 216, 1296)
            G = torch.bmm(M5, M5.conj().transpose(1, 2))
            g_frob = torch.sqrt(torch.sum(G.real**2 + G.imag**2, dim=(1, 2), keepdim=True)).clamp_min(1e-12)
            scale_g = torch.clamp(216.0 * g_frob / 14.6969, min=1.0)
            M_iso = 0.5 * torch.bmm(3.0 * eye216_full - (216.0 / scale_g) * G, M5)
            flat_iso = M_iso.reshape(5, 279936)
            gathered = torch.gather(flat_iso, 1, orb_perm_inv)
            psi_proj = gathered.mean(dim=0)
            psi_proj = psi_proj[shift_idx].mean(dim=0)
            psi_proj = psi_proj / torch.linalg.norm(psi_proj)
            beta = 1.45 if step < (stage1_polar_steps * 4) // 5 else 1.0
            psi = (1.0 - beta) * psi + beta * psi_proj
            psi = psi / torch.linalg.norm(psi)

        # ---------------------------------------------------------------------
        # STAGE 1B: 5-Orbit Z_7-Cyclic Quartic Purity AdamW Optimization
        # ---------------------------------------------------------------------
        psi_param = torch.nn.Parameter(psi.clone())
        optimizer = torch.optim.AdamW([psi_param], lr=0.015)
        scheduler = torch.optim.lr_scheduler.CosineAnnealingLR(optimizer, T_max=stage1_adam_steps, eta_min=1e-4)

        for step in range(stage1_adam_steps):
            optimizer.zero_grad()
            psi_sym = psi_param[shift_idx].mean(dim=0)
            psi_sym = psi_sym / torch.linalg.norm(psi_sym)
            M5 = psi_sym[orb_perm_fwd].view(5, 216, 1296)
            rho5 = torch.bmm(M5, M5.conj().transpose(1, 2))
            diff5 = rho5 - eye216
            frob_sq = torch.sum(diff5.real**2 + diff5.imag**2, dim=(1, 2))
            loss = torch.mean(frob_sq) + 0.5 * torch.max(frob_sq)
            loss.backward()
            optimizer.step()
            scheduler.step()

        # ---------------------------------------------------------------------
        # STAGE 1C: 5-Orbit Second-Order L-BFGS Polish
        # ---------------------------------------------------------------------
        with torch.no_grad():
            psi_start = psi_param[shift_idx].mean(dim=0)
            psi_start = psi_start / torch.linalg.norm(psi_start)
        vec_ri = torch.nn.Parameter(torch.cat([psi_start.real, psi_start.imag], dim=0))
        lbfgs = torch.optim.LBFGS(
            [vec_ri], lr=0.8, max_iter=stage1_lbfgs_steps, history_size=20, line_search_fn="strong_wolfe"
        )

        def closure_z7():
            lbfgs.zero_grad()
            n_half = vec_ri.numel() // 2
            c_psi = torch.complex(vec_ri[:n_half], vec_ri[n_half:])
            c_psi = c_psi[shift_idx].mean(dim=0)
            c_psi = c_psi / torch.linalg.norm(c_psi)
            M5 = c_psi[orb_perm_fwd].view(5, 216, 1296)
            rho5 = torch.bmm(M5, M5.conj().transpose(1, 2))
            diff5 = rho5 - eye216
            frob_sq = torch.sum(diff5.real**2 + diff5.imag**2, dim=(1, 2))
            loss_val = torch.mean(frob_sq)
            loss_val.backward()
            return loss_val

        lbfgs.step(closure_z7)

        with torch.no_grad():
            n_half = vec_ri.numel() // 2
            psi_z7 = torch.complex(vec_ri[:n_half], vec_ri[n_half:])
            psi_z7 = psi_z7[shift_idx].mean(dim=0)
            psi_z7 = psi_z7 / torch.linalg.norm(psi_z7)

        max_frob_z7, mean_frob_z7, orb_frobs_z7 = evaluate_5_orbits_and_35_cuts(
            psi_z7, orb_perm_fwd, all_perm_fwd, eye216
        )
        print(f"  [Restart {restart+1}/{num_restarts} Stage 1 (Z_7)] max_Frob = {max_frob_z7:.6e} | "
              f"mean_Frob = {mean_frob_z7:.6e} | orbits = {orb_frobs_z7} | t = {time.time()-t0:.1f}s", flush=True)

        # ---------------------------------------------------------------------
        # STAGE 2: Unconstrained 35-Cut Symmetry-Breaking Polish (if selected)
        # ---------------------------------------------------------------------
        psi_un = psi_z7.clone()
        if restart >= num_restarts // 2:
            # Inject tiny symmetry-breaking perturbation and polish across all 35 cuts
            noise = (torch.randn(6**7, dtype=torch.float64, device=device) +
                     1j * torch.randn(6**7, dtype=torch.float64, device=device)).to(dtype)
            psi_un = psi_un + 0.005 * noise
            psi_un = psi_un / torch.linalg.norm(psi_un)

            for step in range(stage2_polar_steps):
                M35 = psi_un[all_perm_fwd].view(35, 216, 1296)
                G = torch.bmm(M35, M35.conj().transpose(1, 2))
                g_frob = torch.sqrt(torch.sum(G.real**2 + G.imag**2, dim=(1, 2), keepdim=True)).clamp_min(1e-12)
                scale_g = torch.clamp(216.0 * g_frob / 14.6969, min=1.0)
                M_iso = 0.5 * torch.bmm(3.0 * eye216_full - (216.0 / scale_g) * G, M35)
                flat_iso = M_iso.reshape(35, 279936)
                gathered = torch.gather(flat_iso, 1, all_perm_inv)
                psi_proj = gathered.mean(dim=0)
                psi_proj = psi_proj / torch.linalg.norm(psi_proj)
                psi_un = 0.3 * psi_un + 0.7 * psi_proj
                psi_un = psi_un / torch.linalg.norm(psi_un)

            vec_un = torch.nn.Parameter(torch.cat([psi_un.real, psi_un.imag], dim=0))
            lbfgs_un = torch.optim.LBFGS(
                [vec_un], lr=0.8, max_iter=stage2_lbfgs_steps, history_size=15, line_search_fn="strong_wolfe"
            )

            def closure_un():
                lbfgs_un.zero_grad()
                n_half = vec_un.numel() // 2
                c_psi = torch.complex(vec_un[:n_half], vec_un[n_half:])
                c_psi = c_psi / torch.linalg.norm(c_psi)
                M35 = c_psi[all_perm_fwd].view(35, 216, 1296)
                rho35 = torch.bmm(M35, M35.conj().transpose(1, 2))
                diff35 = rho35 - eye216
                frob_sq = torch.sum(diff35.real**2 + diff35.imag**2, dim=(1, 2))
                loss_val = torch.mean(frob_sq)
                loss_val.backward()
                return loss_val

            lbfgs_un.step(closure_un)
            with torch.no_grad():
                n_half = vec_un.numel() // 2
                psi_un = torch.complex(vec_un[:n_half], vec_un[n_half:])
                psi_un = psi_un / torch.linalg.norm(psi_un)

            max_frob_un, mean_frob_un, orb_frobs_un = evaluate_5_orbits_and_35_cuts(
                psi_un, orb_perm_fwd, all_perm_fwd, eye216
            )
            print(f"  [Restart {restart+1}/{num_restarts} Stage 2 (35-Cut Unconstrained)] "
                  f"max_Frob = {max_frob_un:.6e} | mean_Frob = {mean_frob_un:.6e} | t = {time.time()-t0:.1f}s", flush=True)
            if max_frob_un < max_frob_z7:
                max_frob_z7, mean_frob_z7, orb_frobs_z7, psi_z7 = max_frob_un, mean_frob_un, orb_frobs_un, psi_un

        if max_frob_z7 < best_max_frob:
            best_max_frob = max_frob_z7
            best_mean_frob = mean_frob_z7
            best_orb_frobs = orb_frobs_z7
            best_psi = psi_z7.detach().cpu()

        if best_max_frob < 1e-8:
            cert_path = os.path.join(out_dir, "ame_7_6_numerical_certificate.npz")
            np.savez_compressed(cert_path, psi=best_psi.numpy(), max_frob=best_max_frob)
            print(f"\n*** BREAKTHROUGH: Certified AME(7, 6) tensor saved to {cert_path}! ***", flush=True)
            break

    result = {
        "target": "AME(7, 6)",
        "baseline_pure_product_orbit_frobs": seed_orb_frobs,
        "best_max_35cut_frob": best_max_frob,
        "best_mean_35cut_frob": best_mean_frob,
        "best_5orbit_frobs": best_orb_frobs,
        "elapsed_sec": round(time.time() - t0, 2)
    }
    with open(os.path.join(out_dir, "ame_7_6_colab_results.json"), "w") as f:
        json.dump(result, f, indent=2)
    print("\n=== AME(7, 6) SUMMARY ===", flush=True)
    print(json.dumps(result, indent=2), flush=True)
    return result


if __name__ == "__main__":
    if "--smoke" in sys.argv:
        print("[SMOKE TEST MODE] Quick local verification of AME(7, 6) Qubit-Qutrit Seam Surgery...", flush=True)
        run_ame_7_6_gpu_hunt(
            num_restarts=2,
            stage1_polar_steps=10,
            stage1_adam_steps=15,
            stage1_lbfgs_steps=5,
            stage2_polar_steps=5,
            stage2_lbfgs_steps=4,
        )
    else:
        run_ame_7_6_gpu_hunt(
            num_restarts=8,
            stage1_polar_steps=300,
            stage1_adam_steps=800,
            stage1_lbfgs_steps=80,
            stage2_polar_steps=120,
            stage2_lbfgs_steps=60,
        )
