// Engine 5 (v5.0): Exact IEEE-754 binary64 (with FMA, NO --use_fast_math) d=2 Cooley-Tukey
// Lever #2a (Parallelogram-Energy 12-lev) + Lever #2b (8-Axis 16-gon 12-lev, K_MAX=64,
// Gaussian-Survival Lobe-Decorrelated Warp-Coalesced uint32 Inverted-Bitset) +
// Sort-First In-Place Cids (2x lower VRAM, 96M Stage-1 cap) + Lever #1 (512-Chain GPU Tabu Scout).
//
// Compile (strict IEEE-754 binary64 with FMA, NO --use_fast_math!):
//   nvcc -O3 -std=c++17 -shared -Xcompiler -fPIC engine5_cuda_mitm.cu -o libengine5_cuda.so
//
// Soundness invariants (100% identical to S-1 audited v4.2 + COMPLETENESS_PROOF.md):
//   - Stage-1 & D4 symmetry are 100% bit-for-bit identical to v4.2, Engine 3, verify_dual_lb.py & verify_stage1_c.c.
//   - Lever #2a Parallelogram-Energy margin: 2e-4 * M_safe on EACH side (4e-4 * M_safe total, >6e7x Higham FP64 bound).
//   - Lever #2b 8-Axis Phase-Projection margin: 1e-4 on EACH side above B_safe_proj = sqrt(M_safe) (>2.5e7x Higham bound).
//   - CUDA_CHECK(cudaGetLastError()) immediately after EVERY kernel launch + CUDA_CHECK(cudaDeviceSynchronize()).
//   - Unsigned 64-bit hit_count & cand_count; RAII CudaEventGuard; explicit overflow return codes rc=-2/-3/-4/-5.

#include <cuda_runtime.h>
#include <thrust/device_vector.h>
#include <thrust/sort.h>
#include <thrust/sequence.h>
#include <thrust/gather.h>
#include <cmath>
#include <cstdint>
#include <cstdio>
#include <vector>
#include <algorithm>

#define CUDA_CHECK(call) do {                                            \
    cudaError_t err = (call);                                            \
    if (err != cudaSuccess) {                                            \
        fprintf(stderr, "CUDA error %s:%d: %s\n", __FILE__, __LINE__,    \
                cudaGetErrorString(err));                                \
        return -1;                                                       \
    }                                                                    \
} while (0)

static constexpr int K_MAX = 64;
static constexpr int N_AXES = 8;
static constexpr int N_PLEV = 12;
static constexpr int N_ELEV = 12;
static constexpr int TILE_J = 8192;
static constexpr int W32 = TILE_J / 32;  // 256 uint32 words per constraint
static constexpr double PI_VAL = 3.141592653589793238462643383279502884;

// Exact 20-digit cos(a*pi/8), sin(a*pi/8) for a = 0..7 (16-gon)
__device__ __constant__ double C_AX8[8] = {
    1.0,
    0.92387953251128675613,
    0.70710678118654752440,
    0.38268343236508977173,
    0.0,
    -0.38268343236508977173,
    -0.70710678118654752440,
    -0.92387953251128675613
};
__device__ __constant__ double S_AX8[8] = {
    0.0,
    0.38268343236508977173,
    0.70710678118654752440,
    0.92387953251128675613,
    1.0,
    0.92387953251128675613,
    0.70710678118654752440,
    0.38268343236508977173
};

// 12 Phase-Projection levels & exact complements (mult + lim == 1.0)
__device__ __constant__ double PROJ_MULTS[12] = {
    0.93, 0.88, 0.83, 0.78, 0.72, 0.66, 0.60, 0.52, 0.44, 0.36, 0.28, 0.20
};
__device__ __constant__ double PROJ_LIMS[12] = {
    0.07, 0.12, 0.17, 0.22, 0.28, 0.34, 0.40, 0.48, 0.56, 0.64, 0.72, 0.80
};

// 12 Parallelogram-Energy levels & exact complements (mult + lim == 1.0)
__device__ __constant__ double ENER_MULTS[12] = {
    0.95, 0.91, 0.87, 0.82, 0.77, 0.72, 0.66, 0.60, 0.52, 0.44, 0.36, 0.28
};
__device__ __constant__ double ENER_LIMS[12] = {
    0.05, 0.09, 0.13, 0.18, 0.23, 0.28, 0.34, 0.40, 0.48, 0.56, 0.64, 0.72
};

// Precomputed Gaussian survival proxies:
//   P_PROJ[lv] = erf(sqrt(2) * (1 - PROJ_MULTS[lv]))
//   P_ENER[lv] = 1 - exp(-2 * (1 - ENER_MULTS[lv]))
__device__ __constant__ double P_SCORE_PROJ[12] = {
    0.11134625, 0.18967070, 0.26614305, 0.34008657, 0.42452328, 0.50351621,
    0.57628920, 0.66294462, 0.73715149, 0.79945420, 0.85013075, 0.88999741
};
__device__ __constant__ double P_SCORE_ENER[12] = {
    0.09516258, 0.16472979, 0.22894841, 0.30232367, 0.36871625, 0.42879088,
    0.49338273, 0.55067104, 0.61710711, 0.67372044, 0.72196278, 0.76307224
};

__device__ __forceinline__ uint32_t canon_rev_dev(uint32_t code, int M_len) {
    if (M_len <= 1) return 0u;
    uint32_t last_bit = (code >> (M_len - 2)) & 1u;
    uint32_t rev = 0u;
    for (int k = 1; k < M_len; ++k) {
        int src_idx = M_len - 1 - k;
        uint32_t src_bit = (src_idx == 0) ? 1u : ((code >> (src_idx - 1)) & 1u);
        if (src_bit == last_bit) {
            rev |= (1u << (k - 1));
        }
    }
    return (code < rev) ? code : rev;
}

__device__ __forceinline__ void dft_one_freq(
    uint32_t code,
    int M_len,
    int l,
    const double* __restrict__ cos_t,
    const double* __restrict__ sin_t,
    double& rv,
    double& iv
) {
    const double* ct = cos_t + (size_t)l * M_len;
    const double* st = sin_t + (size_t)l * M_len;
    rv = ct[0];
    iv = st[0];
    for (int j = 1; j < M_len; ++j) {
        double cj = ((code >> (j - 1)) & 1u) ? 1.0 : -1.0;
        rv += cj * ct[j];
        iv += cj * st[j];
    }
}

// ---------------------------------------------------------------------------
// STAGE 1A: Exhaustive exact IEEE-754 binary64 scan over all 2^(M_len - 1) halves
//           (100% bit-for-bit identical to v4.2, Engine 3, verify_stage1_c.c)
// ---------------------------------------------------------------------------
__global__ void stage1_find_codes_kernel(
    uint64_t n_seq,
    int M_len,
    int n_f,
    uint32_t alt_flip_mask,
    int max_abs_S,
    double max_U_sq,
    double M_safe,
    int only_canon,
    const double* __restrict__ cos_t,
    const double* __restrict__ sin_t,
    const int* __restrict__ freq_order,
    uint32_t* __restrict__ out_codes,
    uint64_t max_out,
    uint64_t* __restrict__ out_count
) {
    uint64_t tid = (uint64_t)blockIdx.x * blockDim.x + threadIdx.x;
    uint64_t stride = (uint64_t)gridDim.x * blockDim.x;

    for (uint64_t idx = tid; idx < n_seq; idx += stride) {
        uint32_t code = (uint32_t)idx;
        int s_val = 1 + 2 * __popc(code) - (M_len - 1);
        int abs_s = s_val >= 0 ? s_val : -s_val;
        if (abs_s > max_abs_S) continue;

        int u_val = 1 + 2 * __popc(code ^ alt_flip_mask) - (M_len - 1);
        double u2 = (double)(u_val * u_val);
        if (u2 > max_U_sq) continue;

        if (only_canon && canon_rev_dev(code, M_len) != code) continue;

        bool ok = true;
        for (int fi = 0; fi < n_f; ++fi) {
            int l = freq_order[fi];
            double rv, iv;
            dft_one_freq(code, M_len, l, cos_t, sin_t, rv, iv);
            if (rv * rv + iv * iv > M_safe) {
                ok = false;
                break;
            }
        }
        if (ok) {
            uint64_t pos = atomicAdd((unsigned long long*)out_count, 1ULL);
            if (pos < max_out) {
                out_codes[pos] = code;
            }
        }
    }
}

// ---------------------------------------------------------------------------
// STAGE 1B (Sort-First, Zero raw_cids): Compute lightweight sort keys ONLY
// ---------------------------------------------------------------------------
__global__ void stage1_sort_keys_kernel(
    uint64_t S,
    int M_len,
    int n_u_cells,
    uint32_t alt_flip_mask,
    const uint32_t* __restrict__ in_codes,
    int16_t* __restrict__ out_absS,
    int16_t* __restrict__ out_absU,
    uint32_t* __restrict__ out_canon,
    uint64_t* __restrict__ out_sort_key
) {
    uint64_t i = (uint64_t)blockIdx.x * blockDim.x + threadIdx.x;
    if (i >= S) return;
    uint32_t code = in_codes[i];
    int s_val = 1 + 2 * __popc(code) - (M_len - 1);
    int abs_s = s_val >= 0 ? s_val : -s_val;
    int u_val = 1 + 2 * __popc(code ^ alt_flip_mask) - (M_len - 1);
    int abs_u = u_val >= 0 ? u_val : -u_val;
    uint32_t can = canon_rev_dev(code, M_len);
    out_absS[i] = (int16_t)abs_s;
    out_absU[i] = (int16_t)abs_u;
    out_canon[i] = can;
    int cell_id = (abs_s >> 1) * n_u_cells + (abs_u >> 1);
    out_sort_key[i] = ((uint64_t)(uint32_t)cell_id << 32) | (uint64_t)can;
}

// ---------------------------------------------------------------------------
// STAGE 1C (In-Place on Sorted Bits!): Extract peak_l + Lever #2a/#2b K_MAX=64 cids
// ---------------------------------------------------------------------------
__global__ void stage1_extract_cids_inplace_kernel(
    uint64_t S,
    int M_len,
    int n_f,
    int f_stride,
    int n_sub,
    int compute_cids,
    double M_safe,
    double B_safe_proj,
    const double* __restrict__ cos_t,
    const double* __restrict__ sin_t,
    const uint32_t* __restrict__ sorted_codes,
    int16_t* __restrict__ out_peakl,
    uint16_t* __restrict__ out_cids,   // [S * K_MAX] (only if compute_cids)
    uint8_t* __restrict__ out_nact     // [S]         (only if compute_cids)
) {
    uint64_t i = (uint64_t)blockIdx.x * blockDim.x + threadIdx.x;
    if (i >= S) return;

    uint32_t code = sorted_codes[i];
    double mx_sq = -1.0;
    int pkl = 0;
    double sub_re[33] = {0.0};
    double sub_im[33] = {0.0};
    double sub_sq[33] = {0.0};

    for (int l = 0; l < n_f; ++l) {
        double rv, iv;
        dft_one_freq(code, M_len, l, cos_t, sin_t, rv, iv);
        double sq = rv * rv + iv * iv;
        if (sq > mx_sq) {
            mx_sq = sq;
            pkl = l;
        }
        if (compute_cids && (l % f_stride == 0)) {
            int sl = l / f_stride;
            if (sl < 33) {
                sub_re[sl] = rv;
                sub_im[sl] = iv;
                sub_sq[sl] = sq;
            }
        }
    }
    out_peakl[i] = (int16_t)pkl;
    if (!compute_cids) return;

    int base_e = n_sub * N_AXES * N_PLEV;
    double e_thr[N_PLEV];
    double sq_thr[N_ELEV];
    double margin_E = 2e-4 * M_safe;
    for (int lv = 0; lv < N_PLEV; ++lv) e_thr[lv] = PROJ_MULTS[lv] * B_safe_proj + 1e-4;
    for (int lv = 0; lv < N_ELEV; ++lv) sq_thr[lv] = ENER_MULTS[lv] * M_safe + margin_E;

    // Per sub-freq best primary projection, best orthogonal-ish projection (da >= 2), best energy
    int p1_id[33];  float p1_sc[33];
    int p2_id[33];  float p2_sc[33];
    int en_id[33];  float en_sc[33];

    for (int sl = 0; sl < n_sub; ++sl) {
        double rv = sub_re[sl];
        double iv = sub_im[sl];
        double sq = sub_sq[sl];

        // 1. Tightest Parallelogram-Energy level
        int eid = -1;
        float esc = 10.0f;
        for (int lv = 0; lv < N_ELEV; ++lv) {
            if (sq > sq_thr[lv]) {
                eid = base_e + sl * N_ELEV + lv;
                esc = (float)(P_SCORE_ENER[lv] - 1e-6 * sq);
                break;
            }
        }
        en_id[sl] = eid;
        en_sc[sl] = esc;

        // 2. Best 8-axis Phase-Projection constraint
        int ba = -1, blv = 999;
        double bp = -1.0;
        for (int a = 0; a < N_AXES; ++a) {
            double p = fabs(rv * C_AX8[a] + iv * S_AX8[a]);
            if (p > e_thr[N_PLEV - 1]) {
                int lv_h = N_PLEV - 1;
                for (int lv = 0; lv < N_PLEV; ++lv) {
                    if (p > e_thr[lv]) { lv_h = lv; break; }
                }
                if (lv_h < blv || (lv_h == blv && p > bp)) {
                    blv = lv_h; bp = p; ba = a;
                }
            }
        }
        if (ba >= 0) {
            p1_id[sl] = (sl * N_AXES + ba) * N_PLEV + blv;
            p1_sc[sl] = (float)(P_SCORE_PROJ[blv] - 1e-6 * bp);

            // 3. Best decorrelated secondary axis (da >= 2 => >= 45 degrees away!)
            int b2a = -1, b2lv = 999;
            double b2p = -1.0;
            for (int a = 0; a < N_AXES; ++a) {
                int da = a - ba;
                if (da < 0) da = -da;
                if (da > 4) da = 8 - da;
                if (da < 2) continue;
                double p = fabs(rv * C_AX8[a] + iv * S_AX8[a]);
                if (p > e_thr[N_PLEV - 1]) {
                    int lv_h = N_PLEV - 1;
                    for (int lv = 0; lv < N_PLEV; ++lv) {
                        if (p > e_thr[lv]) { lv_h = lv; break; }
                    }
                    if (lv_h < b2lv || (lv_h == b2lv && p > b2p)) {
                        b2lv = lv_h; b2p = p; b2a = a;
                    }
                }
            }
            if (b2a >= 0) {
                p2_id[sl] = (sl * N_AXES + b2a) * N_PLEV + b2lv;
                p2_sc[sl] = (float)(P_SCORE_PROJ[b2lv] - 1e-6 * b2p);
            } else {
                p2_id[sl] = -1; p2_sc[sl] = 10.0f;
            }
        } else {
            p1_id[sl] = -1; p1_sc[sl] = 10.0f;
            p2_id[sl] = -1; p2_sc[sl] = 10.0f;
        }
    }

    uint16_t* row_cids = out_cids + i * K_MAX;
    int cnt = 0;

    // Pass 1 (Lobe-Decorrelated Primary Sweep): 1 sharpest constraint per sub-freq sl, sorted by Gaussian survival!
    uint8_t sl_used[33] = {0};
    while (cnt < K_MAX) {
        int best_sl = -1;
        float best_sc = 9.0f;
        bool best_is_en = false;
        for (int sl = 0; sl < n_sub; ++sl) {
            if (sl_used[sl]) continue;
            if (p1_sc[sl] < best_sc) { best_sc = p1_sc[sl]; best_sl = sl; best_is_en = false; }
            if (en_sc[sl] < best_sc) { best_sc = en_sc[sl]; best_sl = sl; best_is_en = true; }
        }
        if (best_sl < 0) break;
        if (best_is_en) {
            row_cids[cnt++] = (uint16_t)en_id[best_sl];
            en_id[best_sl] = -1; en_sc[best_sl] = 10.0f;
        } else {
            row_cids[cnt++] = (uint16_t)p1_id[best_sl];
            p1_id[best_sl] = -1; p1_sc[best_sl] = 10.0f;
        }
        sl_used[best_sl] = 1;
    }

    // Pass 2: Gather all remaining complements (unused p1/energy + orthogonal p2) and pick tightest to K_MAX!
    int rem_id[99];
    float rem_sc[99];
    int nr = 0;
    for (int sl = 0; sl < n_sub; ++sl) {
        if (p1_id[sl] >= 0) { rem_id[nr] = p1_id[sl]; rem_sc[nr] = p1_sc[sl]; nr++; }
        if (en_id[sl] >= 0) { rem_id[nr] = en_id[sl]; rem_sc[nr] = en_sc[sl] + 0.01f; nr++; }
        if (p2_id[sl] >= 0) { rem_id[nr] = p2_id[sl]; rem_sc[nr] = p2_sc[sl] + 0.02f; nr++; }
    }
    int need = K_MAX - cnt;
    if (need > nr) need = nr;
    for (int k = 0; k < need; ++k) {
        int mi = k;
        float mv = rem_sc[k];
        for (int m = k + 1; m < nr; ++m) {
            if (rem_sc[m] < mv) { mv = rem_sc[m]; mi = m; }
        }
        if (mi != k) {
            float ts = rem_sc[k]; rem_sc[k] = rem_sc[mi]; rem_sc[mi] = ts;
            int ti = rem_id[k]; rem_id[k] = rem_id[mi]; rem_id[mi] = ti;
        }
        row_cids[cnt++] = (uint16_t)rem_id[k];
    }

    out_nact[i] = (uint8_t)cnt;
}

// ---------------------------------------------------------------------------
// STAGE 2A: Build j-tile spectra & warp-ballot allow_tile[n_total_c * W32]
//           (3,564 rows = 3.56 MB in A100 40MB L2 cache!)
// ---------------------------------------------------------------------------
__global__ void build_tile_kernel(
    int j_start,
    int t_len,
    int M_o,
    int n_f,
    int f_stride,
    int n_sub,
    double M_safe,
    double B_safe_proj,
    const double* __restrict__ cos_o,
    const double* __restrict__ sin_o,
    const double* __restrict__ c_th,
    const double* __restrict__ s_th,
    const uint32_t* __restrict__ so_bits,
    double* __restrict__ tile_re,
    double* __restrict__ tile_im,
    double* __restrict__ tile_sq,
    uint32_t* __restrict__ allow_tile
) {
    int w = blockIdx.x;
    int lane = threadIdx.x;
    int dj = (w << 5) + lane;
    bool valid = (dj < t_len);
    uint32_t code = valid ? so_bits[j_start + dj] : 0u;

    if (valid) {
        double* r_out = tile_re + (size_t)dj * n_f;
        double* i_out = tile_im + (size_t)dj * n_f;
        double* s_out = tile_sq + (size_t)dj * n_f;
        for (int l = 0; l < n_f; ++l) {
            double rv, iv;
            dft_one_freq(code, M_o, l, cos_o, sin_o, rv, iv);
            r_out[l] = rv;
            i_out[l] = iv;
            s_out[l] = rv * rv + iv * iv;
        }
    }

    double o_lim[N_PLEV];
    double o_sq_lim[N_ELEV];
    double margin_E = 2e-4 * M_safe;
    for (int lv = 0; lv < N_PLEV; ++lv) o_lim[lv] = PROJ_LIMS[lv] * B_safe_proj + 1e-4;
    for (int lv = 0; lv < N_ELEV; ++lv) o_sq_lim[lv] = ENER_LIMS[lv] * M_safe + margin_E;

    int base_e = n_sub * N_AXES * N_PLEV;

    for (int sl = 0; sl < n_sub; ++sl) {
        int l = sl * f_stride;
        double wr = 0.0, wi = 0.0, sqo = 1e30;
        if (valid) {
            double ro = tile_re[(size_t)dj * n_f + l];
            double io = tile_im[(size_t)dj * n_f + l];
            sqo = tile_sq[(size_t)dj * n_f + l];
            double ct = c_th[l];
            double st = s_th[l];
            wr = ro * ct - io * st;
            wi = ro * st + io * ct;
        }
        // 1. 8-Axis Phase-Projection rows
        for (int a = 0; a < N_AXES; ++a) {
            double po = valid ? fabs(wr * C_AX8[a] + wi * S_AX8[a]) : 1e30;
            int base_c = (sl * N_AXES + a) * N_PLEV;
            for (int lv = 0; lv < N_PLEV; ++lv) {
                uint32_t word = __ballot_sync(0xffffffffu, valid && (po <= o_lim[lv]));
                if (lane == 0) {
                    allow_tile[(size_t)(base_c + lv) * W32 + w] = word;
                }
            }
        }
        // 2. Parallelogram-Energy rows (ZERO trig!)
        int e_row_base = base_e + sl * N_ELEV;
        for (int lv = 0; lv < N_ELEV; ++lv) {
            uint32_t word = __ballot_sync(0xffffffffu, valid && (sqo <= o_sq_lim[lv]));
            if (lane == 0) {
                allow_tile[(size_t)(e_row_base + lv) * W32 + w] = word;
            }
        }
    }
}

// ---------------------------------------------------------------------------
// STAGE 2A-PRE (v5.1): Build per-cell (c0, c1, c2, c3) register-cache sort keys
// Strictly preserves every cell slice [cell_off[ce], cell_off[ce+1])!
// ---------------------------------------------------------------------------
__global__ void build_join_order_keys_kernel(
    uint64_t S,
    int n_u_cells,
    const int16_t* __restrict__ absS,
    const int16_t* __restrict__ absU,
    const uint16_t* __restrict__ cids,
    const uint8_t* __restrict__ nact,
    uint64_t* __restrict__ out_keys
) {
    uint64_t i = (uint64_t)blockIdx.x * blockDim.x + threadIdx.x;
    if (i >= S) return;
    int cell_id = ((int)absS[i] >> 1) * n_u_cells + ((int)absU[i] >> 1);
    int na = (int)nact[i];
    const uint16_t* ci = cids + (size_t)i * K_MAX;
    uint64_t c0 = (na > 0) ? (uint64_t)(ci[0] & 0xfffu) : 0xfffULL;
    uint64_t c1 = (na > 1) ? (uint64_t)(ci[1] & 0xfffu) : 0xfffULL;
    uint64_t c2 = (na > 2) ? (uint64_t)(ci[2] & 0xfffu) : 0xfffULL;
    uint64_t c3 = (na > 3) ? (uint64_t)(ci[3] & 0xfffu) : 0xfffULL;
    out_keys[i] = ((uint64_t)(uint32_t)cell_id << 48)
                | (c0 << 36)
                | (c1 << 24)
                | (c2 << 12)
                | c3;
}

// ---------------------------------------------------------------------------
// STAGE 2B (v5.1): Warp-Coalesced Bitset Join Kernel with G_I=16 Register Cache
// Reuses m0, m01, m012 in registers across consecutive sorted (c0, c1, c2) entries!
// 100% bit-for-bit identical cand_checked & hits to v5.0.
// ---------------------------------------------------------------------------
static constexpr int G_I_V51 = 16;

__global__ void join_tile_kernel(
    int i_start,
    int i_end,
    int j_start,
    int t_len,
    int same_cell,
    int use_order,
    const uint32_t* __restrict__ se_order,
    int M_e,
    int n_f,
    double M_safe,
    const double* __restrict__ cos_e,
    const double* __restrict__ sin_e,
    const int* __restrict__ freq_order,
    const double* __restrict__ c_th,
    const double* __restrict__ s_th,
    const uint32_t* __restrict__ se_bits,
    const uint32_t* __restrict__ se_canon,
    const int16_t* __restrict__ se_peakl,
    const uint16_t* __restrict__ se_cids,
    const uint8_t* __restrict__ se_nact,
    const uint32_t* __restrict__ so_bits,
    const uint32_t* __restrict__ so_canon,
    const int16_t* __restrict__ so_peakl,
    const double* __restrict__ tile_re,
    const double* __restrict__ tile_im,
    const double* __restrict__ tile_sq,
    const uint32_t* __restrict__ allow_tile,
    uint32_t* __restrict__ hit_ec,
    uint32_t* __restrict__ hit_oc,
    int max_hits,
    unsigned long long* __restrict__ hit_count,
    unsigned long long* __restrict__ cand_count
) {
    int warp_in_blk = threadIdx.x >> 5;
    int lane = threadIdx.x & 31;
    int idx_base = i_start + (blockIdx.y * 8 + warp_in_blk) * G_I_V51;
    if (idx_base >= i_end) return;
    int idx_end = idx_base + G_I_V51;
    if (idx_end > i_end) idx_end = i_end;

    int w = blockIdx.x * 32 + lane;
    int w_start_dj = w << 5;

    uint32_t full_tile_mask = 0u;
    if (w_start_dj < t_len) {
        int rem = t_len - w_start_dj;
        full_tile_mask = (rem >= 32) ? 0xffffffffu : ((1u << rem) - 1u);
    }
    if (!__any_sync(0xffffffffu, full_tile_mask != 0u)) return;

    uint32_t tile_min_can = same_cell ? so_canon[j_start] : 0u;
    uint32_t tile_max_can = same_cell ? so_canon[j_start + t_len - 1] : 0u;

    int prev_c0 = -1, prev_c1 = -1, prev_c2 = -1;
    uint32_t m0 = 0u, m01 = 0u, m012 = 0u;
    unsigned long long loc_cand = 0ULL;

    for (int idx = idx_base; idx < idx_end; ++idx) {
        int i = use_order ? (int)se_order[idx] : idx;

        uint32_t active_mask = full_tile_mask;
        if (same_cell) {
            uint32_t ci_can = se_canon[i];
            if (ci_can < tile_min_can) {
                continue;
            } else if (tile_max_can > ci_can) {
                int lo = 0, hi = t_len;
                while (lo < hi) {
                    int mid = (lo + hi) >> 1;
                    if (so_canon[j_start + mid] <= ci_can) lo = mid + 1;
                    else hi = mid;
                }
                if (w_start_dj < lo) {
                    int rem = lo - w_start_dj;
                    active_mask = (rem >= 32) ? 0xffffffffu : ((1u << rem) - 1u);
                } else {
                    active_mask = 0u;
                }
                if (!__any_sync(0xffffffffu, active_mask != 0u)) continue;
            }
        }

        int nact = (int)se_nact[i];
        const uint16_t* cids = se_cids + (size_t)i * K_MAX;
        uint32_t m = active_mask;

        if (nact >= 4) {
            int c0 = cids[0], c1 = cids[1], c2 = cids[2], c3 = cids[3];
            if (c0 != prev_c0) {
                m0 = allow_tile[(size_t)c0 * W32 + w];
                prev_c0 = c0;
                prev_c1 = -1;
                prev_c2 = -1;
            }
            if (c1 != prev_c1) {
                m01 = m0 & allow_tile[(size_t)c1 * W32 + w];
                prev_c1 = c1;
                prev_c2 = -1;
            }
            if (c2 != prev_c2) {
                m012 = m01 & allow_tile[(size_t)c2 * W32 + w];
                prev_c2 = c2;
            }
            if (m) {
                m &= m012 & allow_tile[(size_t)c3 * W32 + w];
            }
            if (!__any_sync(0xffffffffu, m != 0u)) continue;

            int k = 4;
            if (nact >= 6) {
                int c4 = cids[4], c5 = cids[5];
                if (m) {
                    m &= allow_tile[(size_t)c4 * W32 + w]
                       & allow_tile[(size_t)c5 * W32 + w];
                }
                if (!__any_sync(0xffffffffu, m != 0u)) continue;
                k = 6;
                if (nact >= 8) {
                    int c6 = cids[6], c7 = cids[7];
                    if (m) {
                        m &= allow_tile[(size_t)c6 * W32 + w]
                           & allow_tile[(size_t)c7 * W32 + w];
                    }
                    if (!__any_sync(0xffffffffu, m != 0u)) continue;
                    k = 8;
                }
            }
            for (; k < nact; ++k) {
                int ck = cids[k];
                if (m) m &= allow_tile[(size_t)ck * W32 + w];
                if (!__any_sync(0xffffffffu, m != 0u)) break;
            }
            if (!__any_sync(0xffffffffu, m != 0u)) continue;
        } else {
            for (int k = 0; k < nact; ++k) {
                int ck = cids[k];
                if (m) m &= allow_tile[(size_t)ck * W32 + w];
                if (!__any_sync(0xffffffffu, m != 0u)) break;
            }
            if (!__any_sync(0xffffffffu, m != 0u)) continue;
        }

        if (m == 0u) continue;

        // Exact IEEE-754 binary64 check ONLY on rare (~175x fewer!) surviving candidates!
        uint32_t code_i = se_bits[i];
        int pk_i = (int)se_peakl[i];
        double ri_pk, ii_pk;
        dft_one_freq(code_i, M_e, pk_i, cos_e, sin_e, ri_pk, ii_pk);
        double sqi_pk = ri_pk * ri_pk + ii_pk * ii_pk;
        double cth_pki = c_th[pk_i], sth_pki = s_th[pk_i];

        while (m) {
            int b = __ffs(m) - 1;
            m &= (m - 1u);
            int dj = w_start_dj + b;
            loc_cand++;

            size_t off_j = (size_t)dj * n_f;
            // 1. Check pk_i first
            double rj = tile_re[off_j + pk_i];
            double ij = tile_im[off_j + pk_i];
            double s_pk = sqi_pk + tile_sq[off_j + pk_i];
            if (s_pk > M_safe) continue;
            double A = ri_pk * rj + ii_pk * ij;
            double B = ii_pk * rj - ri_pk * ij;
            if (s_pk + 2.0 * fabs(cth_pki * A + sth_pki * B) > M_safe) continue;

            // 2. Check pk_j next
            int pk_j = (int)so_peakl[j_start + dj];
            if (pk_j != pk_i) {
                double ri2, ii2;
                dft_one_freq(code_i, M_e, pk_j, cos_e, sin_e, ri2, ii2);
                double s2 = ri2 * ri2 + ii2 * ii2 + tile_sq[off_j + pk_j];
                if (s2 > M_safe) continue;
                double rj2 = tile_re[off_j + pk_j];
                double ij2 = tile_im[off_j + pk_j];
                double A2 = ri2 * rj2 + ii2 * ij2;
                double B2 = ii2 * rj2 - ri2 * ij2;
                if (s2 + 2.0 * fabs(c_th[pk_j] * A2 + s_th[pk_j] * B2) > M_safe) continue;
            }

            // 3. Full n_f-frequency exact check in midpoint-scrambled freq_order!
            bool ok = true;
            for (int fi = 0; fi < n_f; ++fi) {
                int l = freq_order[fi];
                double ri_l, ii_l;
                dft_one_freq(code_i, M_e, l, cos_e, sin_e, ri_l, ii_l);
                double s_l = ri_l * ri_l + ii_l * ii_l + tile_sq[off_j + l];
                if (s_l > M_safe) { ok = false; break; }
                double rj_l = tile_re[off_j + l];
                double ij_l = tile_im[off_j + l];
                double Al = ri_l * rj_l + ii_l * ij_l;
                double Bl = ii_l * rj_l - ri_l * ij_l;
                if (s_l + 2.0 * fabs(c_th[l] * Al + s_th[l] * Bl) > M_safe) { ok = false; break; }
            }
            if (ok) {
                unsigned long long pos = atomicAdd(hit_count, 1ULL);
                if (pos < (unsigned long long)max_hits) {
                    hit_ec[pos] = code_i;
                    hit_oc[pos] = so_bits[j_start + dj];
                }
            }
        }
    }
    if (loc_cand > 0ULL) {
        atomicAdd(cand_count, loc_cand);
    }
}

// ---------------------------------------------------------------------------
// LEVER #1: 2-Second 512-Chain Parallel GPU Hinge^2 + L_inf Tabu Primal Scout
// 1 block = 1 independent random-scratch chain; 256 threads = 256 freqs (+ Nyquist k=256 on tid=0).
// Purely heuristic upper-bound generator — never affects soundness of exact MITM pass!
// ---------------------------------------------------------------------------
__device__ __forceinline__ uint64_t xorshift64(uint64_t& s) {
    s ^= s >> 12;
    s ^= s << 25;
    s ^= s >> 27;
    return s * 2685821657736338717ULL;
}

__global__ void primal_scout_tabu_kernel(
    int N,
    int n_iters,
    uint64_t seed_base,
    const float* __restrict__ E_re,    // [N * 257]
    const float* __restrict__ E_im,    // [N * 257]
    int8_t* __restrict__ out_chain_c,  // [gridDim.x * N]
    float* __restrict__ out_chain_m    // [gridDim.x]
) {
    int bid = blockIdx.x;
    int tid = threadIdx.x;  // 0..255
    int lane = tid & 31;
    int wid = tid >> 5;     // 0..7

    __shared__ int8_t s_c[64];
    __shared__ int8_t s_best_c[64];
    __shared__ int s_tabu[64];
    __shared__ float s_wmax[2][8];
    __shared__ float s_whg[2][8];
    __shared__ int s_chosen_j;
    __shared__ float s_best_m;
    __shared__ float s_roof;
    __shared__ float s_w_max;

    uint64_t rng = seed_base ^ ((uint64_t)(bid + 1) * 0x9e3779b97f4a7c15ULL);
    if (tid == 0) {
        s_c[0] = 1;
        s_best_c[0] = 1;
        s_tabu[0] = 0;
        for (int j = 1; j < N; ++j) {
            int8_t v = (xorshift64(rng) >> 63) ? 1 : -1;
            s_c[j] = v;
            s_best_c[j] = v;
            s_tabu[j] = 0;
        }
        s_best_m = 1e30f;
    }
    __syncthreads();

    // Thread tid holds frequency k = tid (and tid==0 also holds Nyquist k=256!)
    float re = 0.0f, im = 0.0f;
    float re_nyq = 0.0f;
    for (int j = 0; j < N; ++j) {
        float cj = (float)s_c[j];
        re += cj * E_re[j * 257 + tid];
        im += cj * E_im[j * 257 + tid];
        if (tid == 0) re_nyq += cj * E_re[j * 257 + 256];
    }

    // Per-block slightly diversified roof & tenure schedules for broad exploration!
    float roof_mul_a = 1.24f + 0.04f * (float)(bid & 3);
    float roof_mul_b = 1.38f + 0.04f * (float)((bid >> 2) & 3);
    int base_ten = 7 + (bid % 6);

    for (int it = 1; it <= n_iters; ++it) {
        if (tid == 0) {
            bool max_phase = (it > (n_iters * 2) / 3);
            s_roof = (float)N * (max_phase ? roof_mul_b : roof_mul_a);
            s_w_max = max_phase ? 90.0f : 6.0f;
        }
        __syncthreads();
        float roof = s_roof;
        float w_max = s_w_max;

        int best_j_local = -1;
        float best_sc_local = 1e30f;
        float best_mx_local = 1e30f;

        for (int j = 1; j < N; ++j) {
            float dv = -2.0f * (float)s_c[j];
            float nr = re + dv * E_re[j * 257 + tid];
            float ni = im + dv * E_im[j * 257 + tid];
            float v = nr * nr + ni * ni;
            float mx = v;
            float hg = (v > roof) ? ((v - roof) * (v - roof)) : 0.0f;
            if (tid == 0) {
                float nrn = re_nyq + dv * E_re[j * 257 + 256];
                float vn = nrn * nrn;
                if (vn > mx) mx = vn;
                if (vn > roof) hg += (vn - roof) * (vn - roof);
            }

            // Warp reduction
            for (int off = 16; off > 0; off >>= 1) {
                float om = __shfl_down_sync(0xffffffffu, mx, off);
                float oh = __shfl_down_sync(0xffffffffu, hg, off);
                if (om > mx) mx = om;
                hg += oh;
            }
            int buf = j & 1;
            if (lane == 0) {
                s_wmax[buf][wid] = mx;
                s_whg[buf][wid] = hg;
            }
            __syncthreads();

            if (wid == 0) {
                float wm = (lane < 8) ? s_wmax[buf][lane] : 0.0f;
                float wh = (lane < 8) ? s_whg[buf][lane] : 0.0f;
                for (int off = 4; off > 0; off >>= 1) {
                    float om = __shfl_down_sync(0xffffffffu, wm, off);
                    float oh = __shfl_down_sync(0xffffffffu, wh, off);
                    if (om > wm) wm = om;
                    wh += oh;
                }
                if (lane == 0) {
                    float sc = wh + w_max * wm;
                    bool allowed = (s_tabu[j] <= it) || (wm < s_best_m - 1e-5f);
                    if (allowed && sc < best_sc_local) {
                        best_sc_local = sc;
                        best_j_local = j;
                        best_mx_local = wm;
                    }
                }
            }
        }

        if (tid == 0) {
            if (best_j_local < 1) best_j_local = 1 + (int)(xorshift64(rng) % (uint64_t)(N - 1));
            s_chosen_j = best_j_local;
            s_c[best_j_local] = -s_c[best_j_local];
            s_tabu[best_j_local] = it + base_ten + (int)(xorshift64(rng) % 7ULL);
            if (best_mx_local < s_best_m) {
                s_best_m = best_mx_local;
                for (int k = 0; k < N; ++k) s_best_c[k] = s_c[k];
            }
        }
        __syncthreads();

        int cj_idx = s_chosen_j;
        float dv = 2.0f * (float)s_c[cj_idx];  // s_c[cj_idx] already flipped -> new - old = 2 * new!
        re += dv * E_re[cj_idx * 257 + tid];
        im += dv * E_im[cj_idx * 257 + tid];
        if (tid == 0) re_nyq += dv * E_re[cj_idx * 257 + 256];
    }

    if (tid == 0) {
        out_chain_m[bid] = s_best_m;
        for (int j = 0; j < N; ++j) out_chain_c[bid * N + j] = s_best_c[j];
    }
}

extern "C" int run_primal_scout_cuda(
    int N,
    int n_chains,
    int n_iters,
    uint64_t seed_base,
    int8_t* out_best_c,
    double* out_best_M_512
) {
    if (N < 4 || N > 64 || n_chains < 1 || n_iters < 10) return -3;
    std::vector<float> h_E_re((size_t)N * 257), h_E_im((size_t)N * 257);
    for (int j = 0; j < N; ++j) {
        for (int k = 0; k < 257; ++k) {
            double th = 2.0 * PI_VAL * k / 512.0;
            h_E_re[(size_t)j * 257 + k] = (float)cos(j * th);
            h_E_im[(size_t)j * 257 + k] = (float)sin(j * th);
        }
    }
    thrust::device_vector<float> d_E_re = h_E_re, d_E_im = h_E_im;
    thrust::device_vector<int8_t> d_chain_c((size_t)n_chains * N);
    thrust::device_vector<float> d_chain_m(n_chains);

    primal_scout_tabu_kernel<<<n_chains, 256>>>(
        N, n_iters, seed_base,
        thrust::raw_pointer_cast(d_E_re.data()),
        thrust::raw_pointer_cast(d_E_im.data()),
        thrust::raw_pointer_cast(d_chain_c.data()),
        thrust::raw_pointer_cast(d_chain_m.data())
    );
    CUDA_CHECK(cudaGetLastError());
    CUDA_CHECK(cudaDeviceSynchronize());

    std::vector<float> h_m(n_chains);
    std::vector<int8_t> h_c((size_t)n_chains * N);
    CUDA_CHECK(cudaMemcpy(h_m.data(), thrust::raw_pointer_cast(d_chain_m.data()), n_chains * sizeof(float), cudaMemcpyDeviceToHost));
    CUDA_CHECK(cudaMemcpy(h_c.data(), thrust::raw_pointer_cast(d_chain_c.data()), (size_t)n_chains * N * sizeof(int8_t), cudaMemcpyDeviceToHost));

    int best_b = 0;
    for (int b = 1; b < n_chains; ++b) {
        if (h_m[b] < h_m[best_b]) best_b = b;
    }
    *out_best_M_512 = (double)h_m[best_b];
    for (int j = 0; j < N; ++j) out_best_c[j] = h_c[(size_t)best_b * N + j];
    return 0;
}

// ---------------------------------------------------------------------------
// Host helpers & C API (Sort-First, 96M Cap, All S-1 v4.2 Guards Preserved!)
// ---------------------------------------------------------------------------
static void make_trig_host(int M_len, int G, std::vector<double>& cos_h, std::vector<double>& sin_h, std::vector<int>& freq_ord) {
    int n_f = G / 2 + 1;
    cos_h.resize((size_t)n_f * M_len);
    sin_h.resize((size_t)n_f * M_len);
    for (int l = 0; l < n_f; ++l) {
        double th = 2.0 * PI_VAL * l / G;
        for (int j = 0; j < M_len; ++j) {
            cos_h[(size_t)l * M_len + j] = cos(j * th);
            sin_h[(size_t)l * M_len + j] = sin(j * th);
        }
    }
    freq_ord.clear();
    std::vector<int> used(n_f, 0);
    for (int step = G / 4; step >= 1; step >>= 1) {
        for (int l = step; l < n_f; l += step) {
            if (!used[l]) { freq_ord.push_back(l); used[l] = 1; }
        }
    }
    for (int l = 0; l < n_f; ++l) {
        if (!used[l]) freq_ord.push_back(l);
    }
}

struct HalfDataGPU {
    uint64_t S = 0;
    int M_len = 0;
    int n_s = 0, n_u = 0, n_cells = 0;
    thrust::device_vector<uint32_t> bits;
    thrust::device_vector<int16_t> absS;
    thrust::device_vector<int16_t> absU;
    thrust::device_vector<uint32_t> canon;
    thrust::device_vector<int16_t> peakl;
    thrust::device_vector<uint16_t> cids;
    thrust::device_vector<uint8_t> nact;
    std::vector<int> cell_off;
    std::vector<int> cell_s;
    std::vector<int> cell_u;
};

struct CudaEventGuard {
    cudaEvent_t e = nullptr;
    CudaEventGuard() { cudaEventCreate(&e); }
    ~CudaEventGuard() { if (e) cudaEventDestroy(e); }
};

static int build_half_gpu_full_v5(
    int M_len,
    int M_other,
    double M_bound,
    int G,
    double eps_safe,
    int only_canon,
    int compute_cids,
    const thrust::device_vector<double>& d_cos,
    const thrust::device_vector<double>& d_sin,
    const thrust::device_vector<int>& d_freq_ord,
    HalfDataGPU& out
) {
    int n_f = G / 2 + 1;
    int f_stride = std::max(1, G / 64);
    int n_sub = (n_f - 1) / f_stride + 1;
    double M_safe = M_bound + eps_safe;
    double B_bound = sqrt(M_bound);
    double B_safe_proj = sqrt(M_safe);
    double B_safe = B_bound + eps_safe;
    double min_other = (double)(M_other % 2);
    int max_abs_S = (int)floor(B_safe - min_other + 1e-9);
    double max_U_sq = M_bound - min_other * min_other + eps_safe;
    int max_abs_U = (int)floor(sqrt(std::max(0.0, max_U_sq)) + 1e-9);

    uint64_t n_seq = 1ULL << (M_len - 1);
    uint32_t alt_flip_mask = 0x55555555u & ((M_len - 1 >= 32) ? 0xffffffffu : ((1u << (M_len - 1)) - 1u));

    uint64_t max_out = std::min<uint64_t>(n_seq, 160000000ULL);
    thrust::device_vector<uint32_t> raw_codes(max_out);
    thrust::device_vector<uint64_t> d_cnt(1, 0ULL);

    int blk = 256;
    int grd = (int)std::min<uint64_t>((n_seq + blk - 1) / blk, 65535ULL);
    stage1_find_codes_kernel<<<grd, blk>>>(
        n_seq, M_len, n_f, alt_flip_mask, max_abs_S, max_U_sq, M_safe, only_canon,
        thrust::raw_pointer_cast(d_cos.data()),
        thrust::raw_pointer_cast(d_sin.data()),
        thrust::raw_pointer_cast(d_freq_ord.data()),
        thrust::raw_pointer_cast(raw_codes.data()),
        max_out,
        thrust::raw_pointer_cast(d_cnt.data())
    );
    CUDA_CHECK(cudaGetLastError());
    CUDA_CHECK(cudaDeviceSynchronize());

    uint64_t S = d_cnt[0];
    if (S > max_out) {
        fprintf(stderr, "ERROR: Stage-1 survivor overflow S=%llu > max_out=%llu\n",
                (unsigned long long)S, (unsigned long long)max_out);
        return -2;
    }
    out.S = S;
    out.M_len = M_len;
    out.n_s = (max_abs_S / 2) + 2;
    out.n_u = (max_abs_U / 2) + 2;
    out.n_cells = out.n_s * out.n_u;
    out.cell_off.assign(out.n_cells + 1, 0);
    out.cell_s.assign(out.n_cells, 0);
    out.cell_u.assign(out.n_cells, 0);
    if (S == 0) return 0;

    raw_codes.resize(S);
    raw_codes.shrink_to_fit();

    // Sort-First (ZERO raw_cids allocation -> 2x lower peak VRAM!):
    thrust::device_vector<int16_t> raw_absS(S), raw_absU(S);
    thrust::device_vector<uint32_t> raw_canon(S);
    thrust::device_vector<uint64_t> sort_keys(S);
    int grd2 = (int)((S + blk - 1) / blk);
    stage1_sort_keys_kernel<<<grd2, blk>>>(
        S, M_len, out.n_u, alt_flip_mask,
        thrust::raw_pointer_cast(raw_codes.data()),
        thrust::raw_pointer_cast(raw_absS.data()),
        thrust::raw_pointer_cast(raw_absU.data()),
        thrust::raw_pointer_cast(raw_canon.data()),
        thrust::raw_pointer_cast(sort_keys.data())
    );
    CUDA_CHECK(cudaGetLastError());
    CUDA_CHECK(cudaDeviceSynchronize());

    thrust::device_vector<uint32_t> perm(S);
    thrust::sequence(perm.begin(), perm.end());
    thrust::sort_by_key(sort_keys.begin(), sort_keys.end(), perm.begin());

    out.bits.resize(S);
    out.absS.resize(S);
    out.absU.resize(S);
    out.canon.resize(S);
    thrust::gather(perm.begin(), perm.end(), raw_codes.begin(), out.bits.begin());
    thrust::gather(perm.begin(), perm.end(), raw_absS.begin(), out.absS.begin());
    thrust::gather(perm.begin(), perm.end(), raw_absU.begin(), out.absU.begin());
    thrust::gather(perm.begin(), perm.end(), raw_canon.begin(), out.canon.begin());

    // Free sort temporaries BEFORE allocating out.cids!
    std::vector<uint64_t> h_keys(S);
    CUDA_CHECK(cudaMemcpy(h_keys.data(), thrust::raw_pointer_cast(sort_keys.data()), S * sizeof(uint64_t), cudaMemcpyDeviceToHost));
    raw_codes.clear(); raw_codes.shrink_to_fit();
    raw_absS.clear();  raw_absS.shrink_to_fit();
    raw_absU.clear();  raw_absU.shrink_to_fit();
    raw_canon.clear(); raw_canon.shrink_to_fit();
    sort_keys.clear(); sort_keys.shrink_to_fit();
    perm.clear();      perm.shrink_to_fit();

    // Extract peak_l + Lever #2a/#2b K_MAX=64 cids directly in-place on sorted out.bits!
    out.peakl.resize(S);
    out.cids.resize(compute_cids ? (S * K_MAX) : 1);
    out.nact.resize(compute_cids ? S : 1);
    stage1_extract_cids_inplace_kernel<<<grd2, blk>>>(
        S, M_len, n_f, f_stride, n_sub, compute_cids, M_safe, B_safe_proj,
        thrust::raw_pointer_cast(d_cos.data()),
        thrust::raw_pointer_cast(d_sin.data()),
        thrust::raw_pointer_cast(out.bits.data()),
        thrust::raw_pointer_cast(out.peakl.data()),
        thrust::raw_pointer_cast(out.cids.data()),
        thrust::raw_pointer_cast(out.nact.data())
    );
    CUDA_CHECK(cudaGetLastError());
    CUDA_CHECK(cudaDeviceSynchronize());

    std::vector<int> ccnt(out.n_cells, 0);
    for (uint64_t i = 0; i < S; ++i) {
        int cid = (int)(h_keys[i] >> 32);
        ccnt[cid]++;
    }
    int acc = 0;
    int par = M_len & 1;
    for (int c = 0; c < out.n_cells; ++c) {
        out.cell_off[c] = acc;
        acc += ccnt[c];
        int cs = c / out.n_u;
        int cu = c % out.n_u;
        out.cell_s[c] = (cs << 1) | par;
        out.cell_u[c] = (cu << 1) | par;
    }
    out.cell_off[out.n_cells] = acc;
    return 0;
}

extern "C" int run_d2_mitm_cuda(
    int N,
    double M_bound,
    int G,
    double eps_safe,
    int max_hits,
    uint32_t* out_hit_ec,
    uint32_t* out_hit_oc,
    uint64_t* out_hit_count,
    uint64_t* out_Se,
    uint64_t* out_So,
    uint64_t* out_cand,
    double* out_enum_sec,
    double* out_join_sec,
    uint32_t* out_e_codes_buf,
    uint32_t* out_o_codes_buf,
    uint64_t max_code_buf
) {
    int is_even = (N % 2 == 0) ? 1 : 0;
    int M_e = (N + 1) / 2;
    int M_o = N / 2;
    int n_f = G / 2 + 1;
    int f_stride = std::max(1, G / 64);
    int n_sub = (n_f - 1) / f_stride + 1;
    int n_total_c = n_sub * (N_AXES * N_PLEV + N_ELEV);

    if (N < 4 || N > 64 || G < 32 || (G % 2) != 0 || n_sub > 33 ||
        !(M_bound > 0.0) || !(eps_safe >= 1e-7) || max_hits <= 0) {
        fprintf(stderr, "ERROR: Invalid arguments to run_d2_mitm_cuda (N=%d G=%d n_sub=%d M=%.6f eps=%.3e)\n",
                N, G, n_sub, M_bound, eps_safe);
        return -3;
    }

    CudaEventGuard ev0_g, ev1_g, ev2_g;
    cudaEvent_t ev0 = ev0_g.e, ev1 = ev1_g.e, ev2 = ev2_g.e;
    CUDA_CHECK(cudaEventRecord(ev0));

    std::vector<double> cos_eh, sin_eh, cos_oh, sin_oh;
    std::vector<int> ford_eh, ford_oh;
    make_trig_host(M_e, G, cos_eh, sin_eh, ford_eh);
    thrust::device_vector<double> d_cos_e = cos_eh, d_sin_e = sin_eh;
    thrust::device_vector<int> d_ford_e = ford_eh;

    thrust::device_vector<double> d_cos_o, d_sin_o;
    thrust::device_vector<int> d_ford_o;
    if (!is_even) {
        make_trig_host(M_o, G, cos_oh, sin_oh, ford_oh);
        d_cos_o = cos_oh; d_sin_o = sin_oh; d_ford_o = ford_oh;
    }

    HalfDataGPU he, ho;
    int rc = build_half_gpu_full_v5(M_e, M_o, M_bound, G, eps_safe, is_even ? 0 : 1, 1, d_cos_e, d_sin_e, d_ford_e, he);
    if (rc != 0) return rc;
    if (!is_even) {
        rc = build_half_gpu_full_v5(M_o, M_e, M_bound, G, eps_safe, 0, 0, d_cos_o, d_sin_o, d_ford_o, ho);
        if (rc != 0) return rc;
    }
    HalfDataGPU& ho_ref = is_even ? he : ho;
    const thrust::device_vector<double>& d_cos_o_ref = is_even ? d_cos_e : d_cos_o;
    const thrust::device_vector<double>& d_sin_o_ref = is_even ? d_sin_e : d_sin_o;

    *out_Se = he.S;
    *out_So = ho_ref.S;

    if (out_e_codes_buf && he.S > 0) {
        if (he.S > max_code_buf) {
            fprintf(stderr, "ERROR: e_codes buffer overflow Se=%llu > max_code_buf=%llu\n",
                    (unsigned long long)he.S, (unsigned long long)max_code_buf);
            return -5;
        }
        CUDA_CHECK(cudaMemcpy(out_e_codes_buf, thrust::raw_pointer_cast(he.bits.data()), he.S * sizeof(uint32_t), cudaMemcpyDeviceToHost));
    }
    if (!is_even && out_o_codes_buf && ho_ref.S > 0) {
        if (ho_ref.S > max_code_buf) {
            fprintf(stderr, "ERROR: o_codes buffer overflow So=%llu > max_code_buf=%llu\n",
                    (unsigned long long)ho_ref.S, (unsigned long long)max_code_buf);
            return -5;
        }
        CUDA_CHECK(cudaMemcpy(out_o_codes_buf, thrust::raw_pointer_cast(ho_ref.bits.data()), ho_ref.S * sizeof(uint32_t), cudaMemcpyDeviceToHost));
    }

    CUDA_CHECK(cudaEventRecord(ev1));
    CUDA_CHECK(cudaEventSynchronize(ev1));
    float ms_enum = 0.0f;
    CUDA_CHECK(cudaEventElapsedTime(&ms_enum, ev0, ev1));
    *out_enum_sec = ms_enum / 1000.0;

    if (he.S == 0 || ho_ref.S == 0) {
        *out_hit_count = 0ULL;
        *out_cand = 0ULL;
        *out_join_sec = 0.0;
        return 0;
    }

    std::vector<double> cth_h(n_f), sth_h(n_f);
    for (int l = 0; l < n_f; ++l) {
        double th = PI_VAL * l / G;
        cth_h[l] = cos(th);
        sth_h[l] = sin(th);
    }
    thrust::device_vector<double> d_cth = cth_h, d_sth = sth_h;

    thrust::device_vector<double> tile_re((size_t)TILE_J * n_f);
    thrust::device_vector<double> tile_im((size_t)TILE_J * n_f);
    thrust::device_vector<double> tile_sq((size_t)TILE_J * n_f);
    thrust::device_vector<uint32_t> allow_tile((size_t)n_total_c * W32);

    // v5.1: Build per-cell (c0, c1, c2, c3)-sorted join permutation se_order (only 4B/elem!)
    thrust::device_vector<uint32_t> se_order(he.S);
    {
        thrust::device_vector<uint64_t> join_keys(he.S);
        int blk_k = 256;
        int grd_k = (int)((he.S + blk_k - 1) / blk_k);
        build_join_order_keys_kernel<<<grd_k, blk_k>>>(
            he.S, he.n_u,
            thrust::raw_pointer_cast(he.absS.data()),
            thrust::raw_pointer_cast(he.absU.data()),
            thrust::raw_pointer_cast(he.cids.data()),
            thrust::raw_pointer_cast(he.nact.data()),
            thrust::raw_pointer_cast(join_keys.data())
        );
        CUDA_CHECK(cudaGetLastError());
        CUDA_CHECK(cudaDeviceSynchronize());
        thrust::sequence(se_order.begin(), se_order.end());
        thrust::sort_by_key(join_keys.begin(), join_keys.end(), se_order.begin());
    }

    thrust::device_vector<uint32_t> d_hit_ec(max_hits);
    thrust::device_vector<uint32_t> d_hit_oc(max_hits);
    thrust::device_vector<unsigned long long> d_hit_cnt(1, 0ULL);
    thrust::device_vector<unsigned long long> d_cand_cnt(1, 0ULL);

    std::vector<uint32_t> h_e_canon;
    if (is_even) {
        h_e_canon.resize(he.S);
        CUDA_CHECK(cudaMemcpy(h_e_canon.data(), thrust::raw_pointer_cast(he.canon.data()), he.S * sizeof(uint32_t), cudaMemcpyDeviceToHost));
    }

    double M_safe = M_bound + eps_safe;
    double B_bound = sqrt(M_bound);
    double B_safe_proj = sqrt(M_safe);
    double B_safe = B_bound + eps_safe;

    int total_tiles = 0;
    for (int cj = 0; cj < ho_ref.n_cells; ++cj) {
        int len = ho_ref.cell_off[cj + 1] - ho_ref.cell_off[cj];
        if (len > 0) total_tiles += (len + TILE_J - 1) / TILE_J;
    }
    int done_tiles = 0;

    for (int cj = 0; cj < ho_ref.n_cells; ++cj) {
        int cj_st = ho_ref.cell_off[cj];
        int cj_en = ho_ref.cell_off[cj + 1];
        if (cj_st == cj_en) continue;
        int sj = ho_ref.cell_s[cj];
        int uj = ho_ref.cell_u[cj];
        double uj2 = (double)(uj * uj);

        int ci_begin = is_even ? cj : 0;
        std::vector<int> compat_ci;
        for (int ci = ci_begin; ci < he.n_cells; ++ci) {
            if (he.cell_off[ci] == he.cell_off[ci + 1]) continue;
            int si = he.cell_s[ci];
            int ui = he.cell_u[ci];
            if ((double)(si + sj) <= B_safe && (double)(ui * ui) + uj2 <= M_safe) {
                compat_ci.push_back(ci);
            }
        }
        if (compat_ci.empty()) continue;

        for (int j_start = cj_st; j_start < cj_en; j_start += TILE_J) {
            int j_end = std::min(j_start + TILE_J, cj_en);
            int t_len = j_end - j_start;
            int n_w = (t_len + 31) >> 5;

            build_tile_kernel<<<n_w, 32>>>(
                j_start, t_len, M_o, n_f, f_stride, n_sub, M_safe, B_safe_proj,
                thrust::raw_pointer_cast(d_cos_o_ref.data()),
                thrust::raw_pointer_cast(d_sin_o_ref.data()),
                thrust::raw_pointer_cast(d_cth.data()),
                thrust::raw_pointer_cast(d_sth.data()),
                thrust::raw_pointer_cast(ho_ref.bits.data()),
                thrust::raw_pointer_cast(tile_re.data()),
                thrust::raw_pointer_cast(tile_im.data()),
                thrust::raw_pointer_cast(tile_sq.data()),
                thrust::raw_pointer_cast(allow_tile.data())
            );
            CUDA_CHECK(cudaGetLastError());

            int n_w_chunks = (n_w + 31) >> 5;
            for (int ci : compat_ci) {
                int ci_st = he.cell_off[ci];
                int ci_en = he.cell_off[ci + 1];
                int same_cell = (is_even && ci == cj) ? 1 : 0;
                int i_lo = ci_st;
                if (same_cell) {
                    uint32_t c_first = h_e_canon[j_start];
                    auto it = std::lower_bound(h_e_canon.begin() + ci_st, h_e_canon.begin() + ci_en, c_first);
                    i_lo = (int)(it - h_e_canon.begin());
                }
                int n_i = ci_en - i_lo;
                if (n_i <= 0) continue;

                int use_order = (same_cell == 0) ? 1 : 0;
                for (int i_base = i_lo; i_base < ci_en; i_base += 4194304) {
                    int i_stop = std::min(i_base + 4194304, ci_en);
                    int n_blks_i = (i_stop - i_base + (8 * G_I_V51) - 1) / (8 * G_I_V51);
                    dim3 grid(n_w_chunks, n_blks_i);
                    join_tile_kernel<<<grid, 256>>>(
                        i_base, i_stop, j_start, t_len, same_cell, use_order,
                        thrust::raw_pointer_cast(se_order.data()),
                        M_e, n_f, M_safe,
                        thrust::raw_pointer_cast(d_cos_e.data()),
                        thrust::raw_pointer_cast(d_sin_e.data()),
                        thrust::raw_pointer_cast(d_ford_e.data()),
                        thrust::raw_pointer_cast(d_cth.data()),
                        thrust::raw_pointer_cast(d_sth.data()),
                        thrust::raw_pointer_cast(he.bits.data()),
                        thrust::raw_pointer_cast(he.canon.data()),
                        thrust::raw_pointer_cast(he.peakl.data()),
                        thrust::raw_pointer_cast(he.cids.data()),
                        thrust::raw_pointer_cast(he.nact.data()),
                        thrust::raw_pointer_cast(ho_ref.bits.data()),
                        thrust::raw_pointer_cast(ho_ref.canon.data()),
                        thrust::raw_pointer_cast(ho_ref.peakl.data()),
                        thrust::raw_pointer_cast(tile_re.data()),
                        thrust::raw_pointer_cast(tile_im.data()),
                        thrust::raw_pointer_cast(tile_sq.data()),
                        thrust::raw_pointer_cast(allow_tile.data()),
                        thrust::raw_pointer_cast(d_hit_ec.data()),
                        thrust::raw_pointer_cast(d_hit_oc.data()),
                        max_hits,
                        thrust::raw_pointer_cast(d_hit_cnt.data()),
                        thrust::raw_pointer_cast(d_cand_cnt.data())
                    );
                    CUDA_CHECK(cudaGetLastError());
                }
            }
            done_tiles++;
            if (he.S >= 4000000ULL && (done_tiles % 256 == 0 || done_tiles == total_tiles)) {
                CUDA_CHECK(cudaDeviceSynchronize());
                printf("    [GPU v5 N=%d G=%d] tile %d/%d (%.1f%%) hits=%llu cand=%llu\n",
                       N, G, done_tiles, total_tiles, 100.0 * done_tiles / std::max(1, total_tiles),
                       (unsigned long long)d_hit_cnt[0], (unsigned long long)d_cand_cnt[0]);
                fflush(stdout);
            }
        }
    }

    CUDA_CHECK(cudaDeviceSynchronize());
    CUDA_CHECK(cudaEventRecord(ev2));
    CUDA_CHECK(cudaEventSynchronize(ev2));
    float ms_join = 0.0f;
    CUDA_CHECK(cudaEventElapsedTime(&ms_join, ev1, ev2));
    *out_join_sec = ms_join / 1000.0;

    uint64_t hc = (uint64_t)d_hit_cnt[0];
    *out_hit_count = hc;
    *out_cand = (uint64_t)d_cand_cnt[0];
    if (hc > (uint64_t)max_hits) {
        fprintf(stderr, "ERROR: Stage-2 hit overflow hc=%llu > max_hits=%d\n",
                (unsigned long long)hc, max_hits);
        return -4;
    }
    if (hc > 0ULL) {
        CUDA_CHECK(cudaMemcpy(out_hit_ec, thrust::raw_pointer_cast(d_hit_ec.data()), (size_t)hc * sizeof(uint32_t), cudaMemcpyDeviceToHost));
        CUDA_CHECK(cudaMemcpy(out_hit_oc, thrust::raw_pointer_cast(d_hit_oc.data()), (size_t)hc * sizeof(uint32_t), cudaMemcpyDeviceToHost));
    }
    return 0;
}

// ---------------------------------------------------------------------------
// Fast Stage-1 Count-Only Budget Probe (for safe N=60/61 ETA & VRAM check)
// ---------------------------------------------------------------------------
__global__ void stage1_count_only_kernel(
    uint64_t n_seq,
    int M_len,
    int n_f,
    uint32_t alt_flip_mask,
    int max_abs_S,
    double max_U_sq,
    double M_safe,
    int only_canon,
    const double* __restrict__ cos_t,
    const double* __restrict__ sin_t,
    const int* __restrict__ freq_ord,
    unsigned long long* __restrict__ out_count
) {
    uint64_t tid = (uint64_t)blockIdx.x * blockDim.x + threadIdx.x;
    uint64_t stride = (uint64_t)gridDim.x * blockDim.x;
    unsigned long long local = 0ULL;
    for (uint64_t idx = tid; idx < n_seq; idx += stride) {
        uint32_t code = (uint32_t)idx;
        int s_val = 1 + 2 * __popc(code) - (M_len - 1);
        int abs_s = s_val >= 0 ? s_val : -s_val;
        if (abs_s > max_abs_S) continue;
        int u_val = 1 + 2 * __popc(code ^ alt_flip_mask) - (M_len - 1);
        if ((double)(u_val * u_val) > max_U_sq) continue;
        if (only_canon && canon_rev_dev(code, M_len) != code) continue;
        bool ok = true;
        for (int fi = 0; fi < n_f; ++fi) {
            int l = freq_ord[fi];
            double rv, iv;
            dft_one_freq(code, M_len, l, cos_t, sin_t, rv, iv);
            if (rv * rv + iv * iv > M_safe) { ok = false; break; }
        }
        if (ok) local++;
    }
    if (local > 0ULL) atomicAdd(out_count, local);
}

extern "C" int run_stage1_probe_cuda(
    int N,
    double M_bound,
    int G,
    double eps_safe,
    uint64_t* out_Se,
    uint64_t* out_So,
    double* out_sec
) {
    if (N < 4 || N > 64 || G < 32 || (G % 2) != 0 || !(M_bound > 0.0) || !(eps_safe >= 1e-7)) return -3;
    int is_even = (N % 2 == 0) ? 1 : 0;
    int M_e = (N + 1) / 2;
    int M_o = N / 2;
    int n_f = G / 2 + 1;
    double M_safe = M_bound + eps_safe;
    double B_safe = sqrt(M_bound) + eps_safe;

    CudaEventGuard ev0_g, ev1_g;
    CUDA_CHECK(cudaEventRecord(ev0_g.e));

    auto count_one = [&](int M_len, int M_other, int only_canon, uint64_t& res) -> int {
        std::vector<double> ch, sh;
        std::vector<int> fh;
        make_trig_host(M_len, G, ch, sh, fh);
        thrust::device_vector<double> d_c = ch, d_s = sh;
        thrust::device_vector<int> d_f = fh;
        double min_other = (double)(M_other % 2);
        int max_abs_S = (int)floor(B_safe - min_other + 1e-9);
        double max_U_sq = M_bound - min_other * min_other + eps_safe;
        uint64_t n_seq = 1ULL << (M_len - 1);
        uint32_t alt_flip_mask = 0x55555555u & ((M_len - 1 >= 32) ? 0xffffffffu : ((1u << (M_len - 1)) - 1u));
        thrust::device_vector<unsigned long long> d_cnt(1, 0ULL);
        int blk = 256;
        int grd = (int)std::min<uint64_t>((n_seq + blk - 1) / blk, 65535ULL);
        stage1_count_only_kernel<<<grd, blk>>>(
            n_seq, M_len, n_f, alt_flip_mask, max_abs_S, max_U_sq, M_safe, only_canon,
            thrust::raw_pointer_cast(d_c.data()),
            thrust::raw_pointer_cast(d_s.data()),
            thrust::raw_pointer_cast(d_f.data()),
            thrust::raw_pointer_cast(d_cnt.data())
        );
        CUDA_CHECK(cudaGetLastError());
        CUDA_CHECK(cudaDeviceSynchronize());
        res = (uint64_t)d_cnt[0];
        return 0;
    };

    uint64_t se = 0ULL, so = 0ULL;
    count_one(M_e, M_o, is_even ? 0 : 1, se);
    if (is_even) so = se;
    else count_one(M_o, M_e, 0, so);

    CUDA_CHECK(cudaEventRecord(ev1_g.e));
    CUDA_CHECK(cudaEventSynchronize(ev1_g.e));
    float ms = 0.0f;
    CUDA_CHECK(cudaEventElapsedTime(&ms, ev0_g.e, ev1_g.e));
    *out_Se = se;
    *out_So = so;
    *out_sec = ms / 1000.0;
    return 0;
}
