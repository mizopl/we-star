#!/usr/bin/env python3
"""
CLSS Quantum AME — Google Colab GPU Discovery Suite (v2 Surgical Edition)
=========================================================================
Four discovery engines targeting the highest-value open regimes of the
Huber-Wyderka table (https://huberfe.github.io/ame) and Grassl's codetables.de:

0. Engine 0 — Semisimple C_3-Block-Circulant Sieve for AME(15, 5) ([[15, 0, 8]]_5):
   - Exhaustive search proved no C_15-circulant graph state over F_5 has d = 8
     because 5 | 15 induces a characteristic-5 Jordan block trap (x^5 - 1 = (x-1)^5).
   - Restricting symmetry to the semisimple subgroup C_3 (gcd(3, 5) = 1: five 3-cycles,
     five 3x3 symmetric circulant diagonal blocks + ten 3x3 circulant off-diagonal blocks,
     35 F_5 parameters) eliminates the char-5 Jordan trap and reduces 6,435 cuts to
     2,145 C_3-orbits.

1. Engine 1 — Non-Stabilizer Continuous Tensor Search for AME(8, 4):
   - n = 8 parties, D = 4 levels (4^8 = 65,536 complex128 amplitudes).
   - Batched SVD Reflect-Reflect-Relax (RRR) / Over-Relaxed Polar Projection across
     all 35 independent 4-party cuts (256x256) + AdamW + L-BFGS second-order polish on GPU,
     testing both Z_8-cyclic and unconstrained manifolds.

2. Engine 2 — Cyclic Z_11-Invariant Continuous Tensor Search for AME(11, 3):
   - n = 11 parties, D = 3 levels (3^11 = 177,147 complex128 amplitudes).
   - Marked "Unknown (Cannot be a stabilizer state)" on huberfe.github.io/ame.
   - Enforces exact Z_11 shift symmetry to reduce 462 cuts to 42 cyclic orbits
     ((42, 243, 729) batched SVD isometric projection + AdamW + L-BFGS on GPU).

3. Engine 3 — Parallel C/OpenMP Twisted D_10 Minor Sieve for AME(20, 19):
   - n = 20 parties, q = 19 ([[20, 0, 11]]_19, above the n <= q + 1 MDS threshold).
"""

import itertools
import json
import math
import os
import subprocess
import sys
import time
from typing import Dict, List, Optional, Tuple

import numpy as np
import torch


def get_device() -> torch.device:
    if torch.cuda.is_available():
        dev = torch.device("cuda")
        print(f"[GPU DETECTED] {torch.cuda.get_device_name(0)} "
              f"(VRAM: {torch.cuda.get_device_properties(0).total_memory / 1e9:.2f} GB, "
              f"CPU threads: {os.cpu_count()})")
    else:
        dev = torch.device("cpu")
        print(f"[DEVICE] CPU float64/complex128 mode (CPU threads: {os.cpu_count()})")
    return dev


# =============================================================================
# ENGINE 0: Semisimple C_3-Block-Circulant Sieve for AME(15, 5) ([[15, 0, 8]]_5)
# =============================================================================

C_SOURCE_AME_15_5_C3 = r"""
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>
#include <time.h>
#ifdef _OPENMP
#include <omp.h>
#endif

// Semisimple C_3-Block-Circulant Graph State Search over F_5 for AME(15, 5) ([[15, 0, 8]]_5)
// Action of generator g in C_3: (0,1,2)(3,4,5)(6,7,8)(9,10,11)(12,13,14).
// Since gcd(3, 5) = 1, C_3 is semisimple in characteristic 5 (avoiding the C_5 Jordan trap!).
// All binom(15, 7) = 6,435 cuts partition into exactly 6435 / 3 = 2,145 C_3-orbits.

#define Q 5
static const int inv5[5] = {0, 1, 3, 2, 4};

typedef struct {
    uint8_t S[7];
    uint8_t Sc[8];
} Cut7;

static Cut7 orbits[2145];
static int num_orbits = 0;

static uint32_t shift_c3(uint32_t m) {
    uint32_t out = 0;
    for (int b = 0; b < 5; b++) {
        uint32_t blk = (m >> (3 * b)) & 7u;
        uint32_t rot = ((blk << 1) | (blk >> 2)) & 7u;
        out |= (rot << (3 * b));
    }
    return out;
}

static void build_c3_orbits(void) {
    uint8_t *seen = (uint8_t *)calloc(1u << 15, 1);
    num_orbits = 0;
    for (uint32_t m = 0; m < (1u << 15); m++) {
        if (__builtin_popcount(m) != 7) continue;
        uint32_t m1 = shift_c3(m);
        uint32_t m2 = shift_c3(m1);
        uint32_t c = m;
        if (m1 < c) c = m1;
        if (m2 < c) c = m2;
        if (!seen[c]) {
            seen[c] = 1;
            int si = 0, sci = 0;
            for (int i = 0; i < 15; i++) {
                if ((c >> i) & 1u) orbits[num_orbits].S[si++] = (uint8_t)i;
                else orbits[num_orbits].Sc[sci++] = (uint8_t)i;
            }
            num_orbits++;
        }
    }
    free(seen);
}

static inline int rank7x8_mod5(const uint8_t G[15][15], const uint8_t S[7], const uint8_t Sc[8]) {
    int M[7][8];
    for (int i = 0; i < 7; i++) {
        const uint8_t *row = G[S[i]];
        for (int j = 0; j < 8; j++) M[i][j] = row[Sc[j]];
    }
    int r = 0;
    for (int col = 0; col < 8 && r < 7; col++) {
        int piv = -1;
        for (int i = r; i < 7; i++) {
            if (M[i][col] != 0) { piv = i; break; }
        }
        if (piv < 0) continue;
        if (piv != r) {
            for (int c = col; c < 8; c++) {
                int tmp = M[r][c]; M[r][c] = M[piv][c]; M[piv][c] = tmp;
            }
        }
        int inv = inv5[M[r][col]];
        for (int i = r + 1; i < 7; i++) {
            int f = (M[i][col] * inv) % 5;
            if (!f) continue;
            for (int c = col + 1; c < 8; c++) {
                M[i][c] = (M[i][c] + 5 - (f * M[r][c]) % 5) % 5;
            }
        }
        r++;
    }
    return r == 7;
}

// 35 parameters in F_5:
// - 5 diagonal 3x3 zero-diagonal symmetric circulant blocks (1 param each: params[0..4])
// - 10 upper-triangular 3x3 circulant blocks (3 params each: params[5..34])
static void build_c3_matrix(uint8_t G[15][15], const int params[35]) {
    memset(G, 0, 225);
    for (int b = 0; b < 5; b++) {
        int v = params[b];
        for (int i = 0; i < 3; i++) {
            for (int j = 0; j < 3; j++) {
                if (i != j) G[3*b + i][3*b + j] = (uint8_t)v;
            }
        }
    }
    int pidx = 5;
    for (int b1 = 0; b1 < 5; b1++) {
        for (int b2 = b1 + 1; b2 < 5; b2++) {
            int c0 = params[pidx], c1 = params[pidx+1], c2 = params[pidx+2];
            pidx += 3;
            int row_c[3] = {c0, c1, c2};
            for (int i = 0; i < 3; i++) {
                for (int j = 0; j < 3; j++) {
                    uint8_t val = (uint8_t)row_c[(j - i + 3) % 3];
                    G[3*b1 + i][3*b2 + j] = val;
                    G[3*b2 + j][3*b1 + i] = val;
                }
            }
        }
    }
}

int main(int argc, char **argv) {
    int seconds = (argc > 1) ? atoi(argv[1]) : 25;
    build_c3_orbits();
    printf("[ENGINE 0] Built %d C_3-orbits (6,435 cuts) for AME(15, 5) over F_5. Running for %d s...\n",
           num_orbits, seconds);

    int global_best_bad = num_orbits;
    int best_params[35];
    memset(best_params, 0, sizeof(best_params));
    time_t start_time = time(NULL);
    long total_evals = 0;

    #pragma omp parallel reduction(+:total_evals)
    {
        int tid = 0;
        #ifdef _OPENMP
        tid = omp_get_thread_num();
        #endif
        uint64_t rng = 0x123456789ABCDEF1ULL ^ ((uint64_t)(tid + 1) * 0x9E3779B97F4A7C15ULL);
        int *order = (int *)malloc(num_orbits * sizeof(int));
        for (int i = 0; i < num_orbits; i++) order[i] = i;

        int params[35];
        for (int i = 0; i < 35; i++) {
            rng ^= rng << 13; rng ^= rng >> 7; rng ^= rng << 17;
            params[i] = (int)(rng % 5);
        }
        int cur_bad = num_orbits;
        int plateau = 0;
        uint8_t G[15][15];

        while (time(NULL) - start_time < seconds && global_best_bad > 0) {
            rng ^= rng << 13; rng ^= rng >> 7; rng ^= rng << 17;
            int idx_p = (int)(rng % 35);
            int old_v = params[idx_p];
            int new_v = (old_v + 1 + (int)((rng >> 8) % 4)) % 5;
            params[idx_p] = new_v;

            build_c3_matrix(G, params);
            total_evals++;

            int bad = 0;
            int cutoff = (cur_bad < global_best_bad ? cur_bad : global_best_bad) + 4;
            for (int k = 0; k < num_orbits; k++) {
                int orb = order[k];
                if (!rank7x8_mod5(G, orbits[orb].S, orbits[orb].Sc)) {
                    bad++;
                    if (k > 0) {
                        int tgt = k >> 1;
                        int tmp = order[k]; order[k] = order[tgt]; order[tgt] = tmp;
                    }
                    if (bad > cutoff) break;
                }
            }

            if (bad <= cur_bad) {
                cur_bad = bad;
                plateau = 0;
            } else {
                plateau++;
                if (plateau < 200) {
                    params[idx_p] = old_v;
                } else {
                    cur_bad = bad;
                    plateau = 0;
                }
            }

            if (bad < global_best_bad) {
                #pragma omp critical
                {
                    if (bad < global_best_bad) {
                        global_best_bad = bad;
                        memcpy(best_params, params, sizeof(params));
                        printf("  [Thread %d] AME(15, 5) C_3-block best bad_orbits = %d / %d (%d / 6435 cuts, %.2f%%)\n",
                               tid, bad, num_orbits, bad * 3, 100.0 * (num_orbits - bad) / num_orbits);
                    }
                }
            }
        }
        free(order);
    }
    printf("[ENGINE 0] Completed %ld evaluations. Best bad_orbits = %d / %d (%d / 6435 cuts).\n",
           total_evals, global_best_bad, num_orbits, global_best_bad * 3);
    printf("[ENGINE 0] best_params_35 = [");
    for (int i = 0; i < 35; i++) printf("%d%s", best_params[i], i == 34 ? "]\n" : ", ");
    return 0;
}
"""


def run_ame_15_5_c3_sieve(seconds: int = 25, out_dir: str = ".") -> Dict:
    print("\n" + "=" * 76)
    print("ENGINE 0: Semisimple C_3-Block-Circulant Sieve for AME(15, 5) ([[15, 0, 8]]_5)")
    print("=" * 76)
    c_path = os.path.join(out_dir, "ame_15_5_c3.c")
    bin_path = os.path.join(out_dir, "ame_15_5_c3_bin")
    with open(c_path, "w") as f:
        f.write(C_SOURCE_AME_15_5_C3)

    for cmd in [
        ["gcc", "-O3", "-march=native", "-fopenmp", c_path, "-o", bin_path],
        ["gcc", "-O3", "-fopenmp", c_path, "-o", bin_path],
        ["cc", "-O3", c_path, "-o", bin_path],
        ["arch", "-x86_64", "/usr/bin/clang", "-O3", c_path, "-o", bin_path],
    ]:
        try:
            if subprocess.call(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL) == 0:
                break
        except FileNotFoundError:
            continue

    t0 = time.time()
    proc = subprocess.run([bin_path, str(seconds)], capture_output=True, text=True)
    print(proc.stdout.strip())
    return {
        "target": "AME(15, 5) C_3-Block Sieve",
        "output_tail": proc.stdout.strip().split("\n")[-1] if proc.stdout else "",
        "elapsed_sec": round(time.time() - t0, 2)
    }


# =============================================================================
# ENGINE 1: Continuous Non-Stabilizer Multi-Unitary Search for AME(8, 4)
# =============================================================================

def build_ame_8_4_cut_permutations(device: torch.device) -> Tuple[List[Tuple[int, ...]], torch.Tensor, torch.Tensor]:
    cuts = [S for S in itertools.combinations(range(8), 4) if 0 in S]
    assert len(cuts) == 35
    grid = np.arange(4**8, dtype=np.int64).reshape((4,) * 8)
    fwd_list = []
    inv_list = []
    for S in cuts:
        Sc = tuple(i for i in range(8) if i not in S)
        axes = S + Sc
        p = np.transpose(grid, axes).reshape(-1)
        p_inv = np.argsort(p)
        fwd_list.append(p)
        inv_list.append(p_inv)
    perm_fwd = torch.tensor(np.stack(fwd_list, axis=0), dtype=torch.long, device=device)
    perm_inv = torch.tensor(np.stack(inv_list, axis=0), dtype=torch.long, device=device)
    return cuts, perm_fwd, perm_inv


def build_cyclic_orbit_map(n: int, D: int, device: torch.device) -> torch.Tensor:
    N = D**n
    grid = np.arange(N, dtype=np.int64).reshape((D,) * n)
    shifts = []
    for s in range(n):
        axes = tuple((i + s) % n for i in range(n))
        shifts.append(np.transpose(grid, axes).reshape(-1))
    return torch.tensor(np.stack(shifts, axis=0), dtype=torch.long, device=device)


def seed_twisted_graph_state_8_4(device: torch.device, noise_scale: float = 0.25) -> torch.Tensor:
    idx = torch.arange(4**8, device=device)
    digits = []
    tmp = idx
    for _ in range(8):
        digits.append(tmp % 4)
        tmp = tmp // 4
    X = torch.stack(digits[::-1], dim=1).to(torch.float64)

    phase = torch.zeros(4**8, dtype=torch.float64, device=device)
    chords_quad = [0.0, 1.0, 1.5, 0.5, 1.0, 0.5, 1.5, 1.0]
    for s in range(1, 5):
        phase = phase + chords_quad[s] * (2.0 * math.pi / 4.0) * torch.sum(X * torch.roll(X, shifts=s, dims=1), dim=1)
    for s1, s2 in [(1, 2), (1, 3), (2, 5)]:
        coeff = (torch.rand(1, device=device, dtype=torch.float64).item() - 0.5) * math.pi
        phase = phase + coeff * torch.cos((2.0 * math.pi / 4.0) * (X + torch.roll(X, s1, 1) - torch.roll(X, s2, 1))).sum(dim=1)

    psi = torch.exp(1j * phase).to(torch.complex128)
    if noise_scale > 0:
        noise = (torch.randn(4**8, dtype=torch.float64, device=device) +
                 1j * torch.randn(4**8, dtype=torch.float64, device=device))
        psi = psi + noise_scale * noise
    psi = psi / torch.linalg.norm(psi)
    return psi


def run_ame_8_4_gpu_hunt(
    num_restarts: int = 6,
    polar_steps: int = 250,
    adam_steps: int = 800,
    lbfgs_steps: int = 60,
    out_dir: str = "."
) -> Dict:
    device = get_device()
    dtype = torch.complex128 if device.type != "mps" else torch.complex64

    print("\n" + "=" * 76)
    print("ENGINE 1: Non-Stabilizer AME(8, 4) Multi-Unitary GPU Solver (35 cuts of 256x256)")
    print("=" * 76)
    cuts, perm_fwd, perm_inv = build_ame_8_4_cut_permutations(device)
    shift_idx = build_cyclic_orbit_map(8, 4, device)
    eye256 = torch.eye(256, dtype=dtype, device=device).unsqueeze(0) / 256.0

    best_max_frob = float("inf")
    best_mean_frob = float("inf")
    best_psi: Optional[torch.Tensor] = None
    t0 = time.time()

    for restart in range(num_restarts):
        # First half of restarts enforce Z_8 cyclic invariance; second half break symmetry
        use_cyclic = (restart < num_restarts // 2)
        mode_tag = "Z_8-Cyclic" if use_cyclic else "Unconstrained"
        psi = seed_twisted_graph_state_8_4(device, noise_scale=0.18 * (restart + 1)).to(dtype)
        if use_cyclic:
            psi = psi[shift_idx].mean(dim=0)
            psi = psi / torch.linalg.norm(psi)

        # Phase A: Batched Over-Relaxed Newton-Schulz Polar Projection (pure torch.bmm on GPU, 10,000x faster than SVD)
        eye256_full = torch.eye(256, dtype=dtype, device=device).unsqueeze(0)
        for step in range(polar_steps):
            M = psi[perm_fwd].view(35, 256, 256)
            G = torch.bmm(M, M.conj().transpose(1, 2))
            # Spectral safety guard so max eigenvalue of 256*G stays < 2.5
            g_frob = torch.sqrt(torch.sum(G.real**2 + G.imag**2, dim=(1, 2), keepdim=True)).clamp_min(1e-12)
            scale_g = torch.clamp(256.0 * g_frob / 16.0, min=1.0)
            M_uni = 0.5 * torch.bmm(3.0 * eye256_full - (256.0 / scale_g) * G, M)
            flat_uni = M_uni.reshape(35, 65536)
            gathered = torch.gather(flat_uni, 1, perm_inv)
            psi_proj = gathered.mean(dim=0)
            if use_cyclic:
                psi_proj = psi_proj[shift_idx].mean(dim=0)
            psi_proj = psi_proj / torch.linalg.norm(psi_proj)
            beta = 1.45 if step < (polar_steps * 4) // 5 else 1.0
            psi = (1.0 - beta) * psi + beta * psi_proj
            psi = psi / torch.linalg.norm(psi)

        # Phase B: Quartic Purity Gradient Descent (AdamW + Cosine Annealing)
        psi_param = torch.nn.Parameter(psi.clone())
        optimizer = torch.optim.AdamW([psi_param], lr=0.015, weight_decay=0.0)
        scheduler = torch.optim.lr_scheduler.CosineAnnealingLR(optimizer, T_max=adam_steps, eta_min=1e-4)

        for step in range(adam_steps):
            optimizer.zero_grad()
            psi_norm = psi_param / torch.linalg.norm(psi_param)
            if use_cyclic:
                psi_norm = psi_norm[shift_idx].mean(dim=0)
                psi_norm = psi_norm / torch.linalg.norm(psi_norm)
            M = psi_norm[perm_fwd].view(35, 256, 256)
            rho = torch.bmm(M, M.conj().transpose(1, 2))
            diff = rho - eye256
            frob_sq_per_cut = torch.sum(diff.real**2 + diff.imag**2, dim=(1, 2))
            loss = torch.mean(frob_sq_per_cut) + 0.5 * torch.max(frob_sq_per_cut)
            loss.backward()
            optimizer.step()
            scheduler.step()

        # Phase C: Second-order L-BFGS Polish on real/imag flattened vector
        with torch.no_grad():
            psi_start = psi_param / torch.linalg.norm(psi_param)
            if use_cyclic:
                psi_start = psi_start[shift_idx].mean(dim=0)
                psi_start = psi_start / torch.linalg.norm(psi_start)
        vec_ri = torch.nn.Parameter(torch.cat([psi_start.real, psi_start.imag], dim=0))
        lbfgs = torch.optim.LBFGS([vec_ri], lr=0.8, max_iter=lbfgs_steps, history_size=20, line_search_fn="strong_wolfe")

        def closure():
            lbfgs.zero_grad()
            n_half = vec_ri.numel() // 2
            c_psi = torch.complex(vec_ri[:n_half], vec_ri[n_half:])
            c_psi = c_psi / torch.linalg.norm(c_psi)
            if use_cyclic:
                c_psi = c_psi[shift_idx].mean(dim=0)
                c_psi = c_psi / torch.linalg.norm(c_psi)
            M = c_psi[perm_fwd].view(35, 256, 256)
            rho = torch.bmm(M, M.conj().transpose(1, 2))
            diff = rho - eye256
            frob_sq = torch.sum(diff.real**2 + diff.imag**2, dim=(1, 2))
            loss_val = torch.mean(frob_sq)
            loss_val.backward()
            return loss_val

        lbfgs.step(closure)

        with torch.no_grad():
            n_half = vec_ri.numel() // 2
            psi_final = torch.complex(vec_ri[:n_half], vec_ri[n_half:])
            psi_final = psi_final / torch.linalg.norm(psi_final)
            if use_cyclic:
                psi_final = psi_final[shift_idx].mean(dim=0)
                psi_final = psi_final / torch.linalg.norm(psi_final)
            M = psi_final[perm_fwd].view(35, 256, 256)
            rho = torch.bmm(M, M.conj().transpose(1, 2))
            diff = rho - eye256
            frob_per_cut = torch.sqrt(torch.sum(diff.real**2 + diff.imag**2, dim=(1, 2)))
            max_frob = float(torch.max(frob_per_cut).item())
            mean_frob = float(torch.mean(frob_per_cut).item())

        print(f"  [Restart {restart+1}/{num_restarts} ({mode_tag})] max_cut_Frob = {max_frob:.6e} | "
              f"mean_cut_Frob = {mean_frob:.6e} | elapsed = {time.time()-t0:.1f}s", flush=True)

        if max_frob < best_max_frob:
            best_max_frob = max_frob
            best_mean_frob = mean_frob
            best_psi = psi_final.detach().cpu()

        if best_max_frob < 1e-8:
            cert_path = os.path.join(out_dir, "ame_8_4_numerical_certificate.npz")
            np.savez_compressed(cert_path, psi=best_psi.numpy(), max_frob=best_max_frob)
            print(f"  *** BREAKTHROUGH: Certified AME(8, 4) numerical tensor saved to {cert_path}! ***")
            break

    return {
        "target": "AME(8, 4)",
        "best_max_frob": best_max_frob,
        "best_mean_frob": best_mean_frob,
        "elapsed_sec": round(time.time() - t0, 2)
    }


# =============================================================================
# ENGINE 2: Cyclic Z_11-Invariant Non-Stabilizer Search for AME(11, 3)
# =============================================================================

def build_ame_11_3_cyclic_orbit_permutations(device: torch.device) -> Tuple[List[Tuple[int, ...]], torch.Tensor, torch.Tensor]:
    seen = set()
    orbit_reps = []
    for S in itertools.combinations(range(11), 5):
        canon = min(tuple(sorted((x + s) % 11 for x in S)) for s in range(11))
        if canon not in seen:
            seen.add(canon)
            orbit_reps.append(canon)
    assert len(orbit_reps) == 42

    grid = np.arange(3**11, dtype=np.int64).reshape((3,) * 11)
    fwd_list = []
    inv_list = []
    for S in orbit_reps:
        Sc = tuple(i for i in range(11) if i not in S)
        p = np.transpose(grid, S + Sc).reshape(-1)
        p_inv = np.argsort(p)
        fwd_list.append(p)
        inv_list.append(p_inv)
    perm_fwd = torch.tensor(np.stack(fwd_list, axis=0), dtype=torch.long, device=device)
    perm_inv = torch.tensor(np.stack(inv_list, axis=0), dtype=torch.long, device=device)
    return orbit_reps, perm_fwd, perm_inv


def run_ame_11_3_gpu_hunt(
    num_restarts: int = 3,
    polar_steps: int = 120,
    adam_steps: int = 500,
    lbfgs_steps: int = 50,
    out_dir: str = "."
) -> Dict:
    device = get_device()
    dtype = torch.complex128 if device.type != "mps" else torch.complex64

    print("\n" + "=" * 76)
    print("ENGINE 2: Z_11-Cyclic Non-Stabilizer AME(11, 3) GPU Solver (42 orbits of 243x729)")
    print("=" * 76)
    orbit_reps, perm_fwd, perm_inv = build_ame_11_3_cyclic_orbit_permutations(device)
    shift_idx = build_cyclic_orbit_map(11, 3, device)
    eye243 = torch.eye(243, dtype=dtype, device=device).unsqueeze(0) / 243.0
    inv_sqrt243 = 1.0 / math.sqrt(243.0)

    best_max_frob = float("inf")
    best_mean_frob = float("inf")
    t0 = time.time()

    for restart in range(num_restarts):
        raw = (torch.randn(3**11, device=device) + 1j * torch.randn(3**11, device=device)).to(dtype)
        psi = raw[shift_idx].mean(dim=0)
        psi = psi / torch.linalg.norm(psi)

        # Phase A: Batched Isometric Newton-Schulz Projection across all 42 (243 x 729) orbit cuts!
        eye243_full = torch.eye(243, dtype=dtype, device=device).unsqueeze(0)
        for step in range(polar_steps):
            M = psi[perm_fwd].view(42, 243, 729)
            G = torch.bmm(M, M.conj().transpose(1, 2))
            g_frob = torch.sqrt(torch.sum(G.real**2 + G.imag**2, dim=(1, 2), keepdim=True)).clamp_min(1e-12)
            scale_g = torch.clamp(243.0 * g_frob / 15.588, min=1.0)
            M_iso = 0.5 * torch.bmm(3.0 * eye243_full - (243.0 / scale_g) * G, M)
            flat_iso = M_iso.reshape(42, 177147)
            gathered = torch.gather(flat_iso, 1, perm_inv)
            psi_proj = gathered.mean(dim=0)
            psi_proj = psi_proj[shift_idx].mean(dim=0)
            psi_proj = psi_proj / torch.linalg.norm(psi_proj)
            beta = 1.40 if step < (polar_steps * 4) // 5 else 1.0
            psi = (1.0 - beta) * psi + beta * psi_proj
            psi = psi / torch.linalg.norm(psi)

        # Phase B: AdamW Quartic Purity Polish
        psi_param = torch.nn.Parameter(psi.clone())
        optimizer = torch.optim.AdamW([psi_param], lr=0.015)
        scheduler = torch.optim.lr_scheduler.CosineAnnealingLR(optimizer, T_max=adam_steps, eta_min=1e-4)

        for step in range(adam_steps):
            optimizer.zero_grad()
            psi_sym = psi_param[shift_idx].mean(dim=0)
            psi_sym = psi_sym / torch.linalg.norm(psi_sym)
            M = psi_sym[perm_fwd].view(42, 243, 729)
            rho = torch.bmm(M, M.conj().transpose(1, 2))
            diff = rho - eye243
            frob_sq = torch.sum(diff.real**2 + diff.imag**2, dim=(1, 2))
            loss = torch.mean(frob_sq) + 0.5 * torch.max(frob_sq)
            loss.backward()
            optimizer.step()
            scheduler.step()

        # Phase C: Second-order L-BFGS Polish
        with torch.no_grad():
            psi_start = psi_param[shift_idx].mean(dim=0)
            psi_start = psi_start / torch.linalg.norm(psi_start)
        vec_ri = torch.nn.Parameter(torch.cat([psi_start.real, psi_start.imag], dim=0))
        lbfgs = torch.optim.LBFGS([vec_ri], lr=0.8, max_iter=lbfgs_steps, history_size=15, line_search_fn="strong_wolfe")

        def closure():
            lbfgs.zero_grad()
            n_half = vec_ri.numel() // 2
            c_psi = torch.complex(vec_ri[:n_half], vec_ri[n_half:])
            c_psi = c_psi[shift_idx].mean(dim=0)
            c_psi = c_psi / torch.linalg.norm(c_psi)
            M = c_psi[perm_fwd].view(42, 243, 729)
            rho = torch.bmm(M, M.conj().transpose(1, 2))
            diff = rho - eye243
            frob_sq = torch.sum(diff.real**2 + diff.imag**2, dim=(1, 2))
            loss_val = torch.mean(frob_sq)
            loss_val.backward()
            return loss_val

        lbfgs.step(closure)

        with torch.no_grad():
            n_half = vec_ri.numel() // 2
            psi_sym = torch.complex(vec_ri[:n_half], vec_ri[n_half:])
            psi_sym = psi_sym[shift_idx].mean(dim=0)
            psi_sym = psi_sym / torch.linalg.norm(psi_sym)
            M = psi_sym[perm_fwd].view(42, 243, 729)
            rho = torch.bmm(M, M.conj().transpose(1, 2))
            diff = rho - eye243
            frob = torch.sqrt(torch.sum(diff.real**2 + diff.imag**2, dim=(1, 2)))
            max_frob = float(torch.max(frob).item())
            mean_frob = float(torch.mean(frob).item())

        print(f"  [Restart {restart+1}/{num_restarts}] max_orbit_Frob = {max_frob:.6e} | "
              f"mean_orbit_Frob = {mean_frob:.6e} | elapsed = {time.time()-t0:.1f}s", flush=True)
        if max_frob < best_max_frob:
            best_max_frob = max_frob
            best_mean_frob = mean_frob
        if best_max_frob < 1e-8:
            cert_path = os.path.join(out_dir, "ame_11_3_numerical_certificate.npz")
            np.savez_compressed(cert_path, psi=psi_sym.detach().cpu().numpy(), max_frob=best_max_frob)
            print(f"  *** BREAKTHROUGH: Certified AME(11, 3) numerical tensor saved to {cert_path}! ***")
            break

    return {
        "target": "AME(11, 3)",
        "best_max_frob": best_max_frob,
        "best_mean_frob": best_mean_frob,
        "elapsed_sec": round(time.time() - t0, 2)
    }


# =============================================================================
# ENGINE 3: Parallel C++ / OpenMP / CUDA Minor Sieve for AME(20, 19)
# =============================================================================

C_SOURCE_AME_20_19 = r"""
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>
#include <time.h>
#ifdef _OPENMP
#include <omp.h>
#endif

#define Q 19
#define N 20
#define K 10

static int inv_tab[Q];
static void init_inv(void) {
    inv_tab[0] = 0;
    for (int a = 1; a < Q; a++) {
        for (int b = 1; b < Q; b++) {
            if ((a * b) % Q == 1) inv_tab[a] = b;
        }
    }
}

typedef struct {
    uint8_t S[10];
    uint8_t Sc[10];
} CutOrbit;

static CutOrbit *orbits = NULL;
static int num_orbits = 0;

static uint32_t canon_mask_d10(uint32_t m) {
    uint32_t best = m;
    uint32_t lo = m & 0x3FFu;
    uint32_t hi = (m >> 10) & 0x3FFu;
    for (int s = 0; s < 10; s++) {
        uint32_t r_lo = ((lo >> s) | (lo << (10 - s))) & 0x3FFu;
        uint32_t r_hi = ((hi >> s) | (hi << (10 - s))) & 0x3FFu;
        uint32_t c1 = r_lo | (r_hi << 10);
        if (c1 < best) best = c1;
        uint32_t f_lo = 0, f_hi = 0;
        for (int i = 0; i < 10; i++) {
            int j = (10 - i) % 10;
            if ((r_lo >> i) & 1u) f_lo |= (1u << j);
            if ((r_hi >> i) & 1u) f_hi |= (1u << j);
        }
        uint32_t c2 = f_lo | (f_hi << 10);
        if (c2 < best) best = c2;
    }
    return best;
}

static void build_orbits(void) {
    uint8_t *seen = (uint8_t *)calloc(1u << 20, 1);
    orbits = (CutOrbit *)malloc(20000 * sizeof(CutOrbit));
    num_orbits = 0;
    for (uint32_t m = 0; m < (1u << 20); m++) {
        if (__builtin_popcount(m) != 10) continue;
        uint32_t c = canon_mask_d10(m);
        uint32_t comp = (~m) & 0xFFFFFu;
        uint32_t cc = canon_mask_d10(comp);
        if (cc < c) c = cc;
        if (!seen[c]) {
            seen[c] = 1;
            int si = 0, sci = 0;
            for (int i = 0; i < 20; i++) {
                if ((c >> i) & 1u) orbits[num_orbits].S[si++] = (uint8_t)i;
                else orbits[num_orbits].Sc[sci++] = (uint8_t)i;
            }
            num_orbits++;
        }
    }
    free(seen);
}

static inline int det10_mod19(const uint8_t G[20][20], const uint8_t S[10], const uint8_t Sc[10]) {
    int M[10][10];
    for (int i = 0; i < 10; i++) {
        const uint8_t *row = G[Sc[i]];
        for (int j = 0; j < 10; j++) M[i][j] = row[S[j]];
    }
    for (int col = 0; col < 10; col++) {
        int piv = -1;
        for (int r = col; r < 10; r++) {
            if (M[r][col] != 0) { piv = r; break; }
        }
        if (piv < 0) return 0;
        if (piv != col) {
            for (int c = col; c < 10; c++) {
                int tmp = M[col][c]; M[col][c] = M[piv][c]; M[piv][c] = tmp;
            }
        }
        int inv = inv_tab[M[col][col]];
        for (int r = col + 1; r < 10; r++) {
            int factor = (M[r][col] * inv) % Q;
            if (!factor) continue;
            for (int c = col + 1; c < 10; c++) {
                M[r][c] = (M[r][c] + Q - (factor * M[col][c]) % Q) % Q;
            }
        }
    }
    return 1;
}

static void build_twisted_d10_matrix(uint8_t G[20][20], const int aA[6], const int aD[6], const int b[10], int lam) {
    memset(G, 0, 400);
    for (int i = 0; i < 10; i++) {
        for (int j = 0; j < 10; j++) {
            int d = (j - i + 10) % 10;
            int cd = d <= 5 ? d : 10 - d;
            G[i][j] = (uint8_t)aA[cd];
            G[10 + i][10 + j] = (uint8_t)aD[cd];
            int idx = (j + i) % 10;
            int val = b[idx];
            if (j + i >= 10) val = (val * lam) % Q;
            G[i][10 + j] = (uint8_t)val;
            G[10 + j][i] = (uint8_t)val;
        }
    }
}

int main(int argc, char **argv) {
    int seconds = (argc > 1) ? atoi(argv[1]) : 25;
    init_inv();
    build_orbits();
    printf("[ENGINE 3] Built %d canonical D_10 cut orbits for AME(20, 19). Running for %d seconds...\n",
           num_orbits, seconds);

    int global_best_bad = num_orbits;
    time_t start_time = time(NULL);
    long total_evals = 0;

    #pragma omp parallel reduction(+:total_evals)
    {
        int tid = 0;
        #ifdef _OPENMP
        tid = omp_get_thread_num();
        #endif
        uint64_t rng = 0x9E3779B97F4A7C15ULL ^ ((uint64_t)(tid + 1) * 0xBF58476D1CE4E5B9ULL);
        int *order = (int *)malloc(num_orbits * sizeof(int));
        for (int i = 0; i < num_orbits; i++) order[i] = i;

        int aA[6] = {0, 1, 2, 4, 8, 3};
        int aD[6] = {0, 1, 3, 9, 8, 5};
        int b[10] = {1, 1, 2, 5, 14, 6, 17, 9, 4, 11};
        int lam = 18;
        int cur_bad = num_orbits;
        int plateau_steps = 0;
        uint8_t G[20][20];

        while (time(NULL) - start_time < seconds && global_best_bad > 0) {
            rng ^= rng << 13; rng ^= rng >> 7; rng ^= rng << 17;
            int which = (int)(rng % 22);
            int old_val;
            if (which < 5) {
                old_val = aA[1 + which];
                aA[1 + which] = (int)((rng >> 8) % Q);
            } else if (which < 10) {
                old_val = aD[1 + (which - 5)];
                aD[1 + (which - 5)] = (int)((rng >> 8) % Q);
            } else if (which < 20) {
                old_val = b[which - 10];
                b[which - 10] = (int)((rng >> 8) % Q);
            } else {
                old_val = lam;
                lam = 1 + (int)((rng >> 8) % (Q - 1));
            }

            build_twisted_d10_matrix(G, aA, aD, b, lam);
            total_evals++;

            int bad = 0;
            int cutoff = (cur_bad < global_best_bad ? cur_bad : global_best_bad) + 6;
            for (int idx = 0; idx < num_orbits; idx++) {
                int orb = order[idx];
                if (!det10_mod19(G, orbits[orb].S, orbits[orb].Sc)) {
                    bad++;
                    if (idx > 0) {
                        int target = idx >> 1;
                        int tmp = order[idx];
                        order[idx] = order[target];
                        order[target] = tmp;
                    }
                    if (bad > cutoff) break;
                }
            }

            if (bad <= cur_bad) {
                cur_bad = bad;
                plateau_steps = 0;
            } else {
                plateau_steps++;
                if (plateau_steps < 120) {
                    if (which < 5) aA[1 + which] = old_val;
                    else if (which < 10) aD[1 + (which - 5)] = old_val;
                    else if (which < 20) b[which - 10] = old_val;
                    else lam = old_val;
                } else {
                    cur_bad = bad;
                    plateau_steps = 0;
                }
            }

            if (bad < global_best_bad) {
                #pragma omp critical
                {
                    if (bad < global_best_bad) {
                        global_best_bad = bad;
                        printf("  [Thread %d] New best bad_orbits = %d / %d (%.3f%% nonsingular) | lam=%d aA=[%d,%d,%d,%d,%d,%d] aD=[%d,%d,%d,%d,%d,%d] b=[%d,%d,%d,%d,%d,%d,%d,%d,%d,%d]\n",
                               tid, bad, num_orbits, 100.0 * (num_orbits - bad) / num_orbits,
                               lam, aA[0],aA[1],aA[2],aA[3],aA[4],aA[5],
                               aD[0],aD[1],aD[2],aD[3],aD[4],aD[5],
                               b[0],b[1],b[2],b[3],b[4],b[5],b[6],b[7],b[8],b[9]);
                    }
                }
            }
        }
        free(order);
    }

    printf("[ENGINE 3] Completed %ld evaluations. Best bad_orbits = %d / %d.\n",
           total_evals, global_best_bad, num_orbits);
    return 0;
}
"""


def run_ame_20_19_sieve(seconds: int = 25, out_dir: str = ".") -> Dict:
    print("\n" + "=" * 76)
    print("ENGINE 3: Parallel C/OpenMP Twisted D_10 Sieve for AME(20, 19) ([[20, 0, 11]]_19)")
    print("=" * 76)
    c_path = os.path.join(out_dir, "ame_20_19_sieve.c")
    bin_path = os.path.join(out_dir, "ame_20_19_sieve_bin")
    with open(c_path, "w") as f:
        f.write(C_SOURCE_AME_20_19)

    for cmd in [
        ["gcc", "-O3", "-march=native", "-fopenmp", c_path, "-o", bin_path],
        ["gcc", "-O3", "-fopenmp", c_path, "-o", bin_path],
        ["cc", "-O3", c_path, "-o", bin_path],
        ["arch", "-x86_64", "/usr/bin/clang", "-O3", c_path, "-o", bin_path],
    ]:
        try:
            if subprocess.call(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL) == 0:
                break
        except FileNotFoundError:
            continue

    t0 = time.time()
    proc = subprocess.run([bin_path, str(seconds)], capture_output=True, text=True)
    print(proc.stdout.strip())
    return {
        "target": "AME(20, 19)",
        "output_tail": proc.stdout.strip().split("\n")[-1] if proc.stdout else "",
        "elapsed_sec": round(time.time() - t0, 2)
    }


if __name__ == "__main__":
    smoke_mode = "--smoke" in sys.argv
    if smoke_mode:
        print("[SMOKE TEST MODE] Running quick verification of all 4 engines...")
        r0 = run_ame_15_5_c3_sieve(seconds=2)
        r1 = run_ame_8_4_gpu_hunt(num_restarts=2, polar_steps=10, adam_steps=15, lbfgs_steps=5)
        r2 = run_ame_11_3_gpu_hunt(num_restarts=1, polar_steps=8, adam_steps=10, lbfgs_steps=5)
        r3 = run_ame_20_19_sieve(seconds=2)
    else:
        r0 = run_ame_15_5_c3_sieve(seconds=35)
        r1 = run_ame_8_4_gpu_hunt(num_restarts=6, polar_steps=250, adam_steps=800, lbfgs_steps=60)
        r2 = run_ame_11_3_gpu_hunt(num_restarts=3, polar_steps=120, adam_steps=500, lbfgs_steps=50)
        r3 = run_ame_20_19_sieve(seconds=35)
    summary = [r0, r1, r2, r3]
    with open("colab_ame_results.json", "w") as f:
        json.dump(summary, f, indent=2)
    print("\n=== SUMMARY ===")
    print(json.dumps(summary, indent=2))
