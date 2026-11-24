/*
 * Standalone Independent C11 Stage-1 Completeness & SHA-256 Cross-Auditor
 * (ZERO CUDA, ZERO Numba, ZERO shared solver code, < 2 MB RAM via streaming FIPS-180-4 SHA-256).
 *
 * Compile:
 *   clang -O3 -std=c11 verify_stage1_c.c -lm -o verify_stage1_c
 * Usage:
 *   ./verify_stage1_c <M_len> <M_other> <M_bound> <G> <eps_safe> <only_canon:0|1>
 * Prints:
 *   S=<count> sha256=<64-hex> elapsed_s=<sec>
 */
#include <math.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>

static const double PI_VAL = 3.141592653589793238462643383279502884;

/* ---------------- Minimal FIPS 180-4 SHA-256 (streaming, O(1) RAM) ---------------- */
typedef struct {
    uint32_t state[8];
    uint64_t bitlen;
    uint8_t data[64];
    size_t datalen;
} sha256_ctx;

static const uint32_t K256[64] = {
    0x428a2f98u,0x71374491u,0xb5c0fbcfu,0xe9b5dba5u,0x3956c25bu,0x59f111f1u,0x923f82a4u,0xab1c5ed5u,
    0xd807aa98u,0x12835b01u,0x243185beu,0x550c7dc3u,0x72be5d74u,0x80deb1feu,0x9bdc06a7u,0xc19bf174u,
    0xe49b69c1u,0xefbe4786u,0x0fc19dc6u,0x240ca1ccu,0x2de92c6fu,0x4a7484aau,0x5cb0a9dcu,0x76f988dau,
    0x983e5152u,0xa831c66du,0xb00327c8u,0xbf597fc7u,0xc6e00bf3u,0xd5a79147u,0x06ca6351u,0x14292967u,
    0x27b70a85u,0x2e1b2138u,0x4d2c6dfcu,0x53380d13u,0x650a7354u,0x766a0abbu,0x81c2c92eu,0x92722c85u,
    0xa2bfe8a1u,0xa81a664bu,0xc24b8b70u,0xc76c51a3u,0xd192e819u,0xd6990624u,0xf40e3585u,0x106aa070u,
    0x19a4c116u,0x1e376c08u,0x2748774cu,0x34b0bcb5u,0x391c0cb3u,0x4ed8aa4au,0x5b9cca4fu,0x682e6ff3u,
    0x748f82eeu,0x78a5636fu,0x84c87814u,0x8cc70208u,0x90befffaU,0xa4506cebu,0xbef9a3f7u,0xc67178f2u
};

static inline uint32_t rotr32(uint32_t x, uint32_t n) { return (x >> n) | (x << (32u - n)); }

static void sha256_transform(sha256_ctx *ctx, const uint8_t data[64]) {
    uint32_t m[64];
    for (int i = 0, j = 0; i < 16; ++i, j += 4) {
        m[i] = ((uint32_t)data[j] << 24) | ((uint32_t)data[j+1] << 16) |
               ((uint32_t)data[j+2] << 8) | ((uint32_t)data[j+3]);
    }
    for (int i = 16; i < 64; ++i) {
        uint32_t s0 = rotr32(m[i-15], 7) ^ rotr32(m[i-15], 18) ^ (m[i-15] >> 3);
        uint32_t s1 = rotr32(m[i-2], 17) ^ rotr32(m[i-2], 19) ^ (m[i-2] >> 10);
        m[i] = m[i-16] + s0 + m[i-7] + s1;
    }
    uint32_t a = ctx->state[0], b = ctx->state[1], c = ctx->state[2], d = ctx->state[3];
    uint32_t e = ctx->state[4], f = ctx->state[5], g = ctx->state[6], h = ctx->state[7];
    for (int i = 0; i < 64; ++i) {
        uint32_t S1 = rotr32(e, 6) ^ rotr32(e, 11) ^ rotr32(e, 25);
        uint32_t ch = (e & f) ^ ((~e) & g);
        uint32_t t1 = h + S1 + ch + K256[i] + m[i];
        uint32_t S0 = rotr32(a, 2) ^ rotr32(a, 13) ^ rotr32(a, 22);
        uint32_t maj = (a & b) ^ (a & c) ^ (b & c);
        uint32_t t2 = S0 + maj;
        h = g; g = f; f = e; e = d + t1;
        d = c; c = b; b = a; a = t1 + t2;
    }
    ctx->state[0] += a; ctx->state[1] += b; ctx->state[2] += c; ctx->state[3] += d;
    ctx->state[4] += e; ctx->state[5] += f; ctx->state[6] += g; ctx->state[7] += h;
}

static void sha256_init(sha256_ctx *ctx) {
    ctx->datalen = 0; ctx->bitlen = 0;
    ctx->state[0] = 0x6a09e667u; ctx->state[1] = 0xbb67ae85u;
    ctx->state[2] = 0x3c6ef372u; ctx->state[3] = 0xa54ff53au;
    ctx->state[4] = 0x510e527fu; ctx->state[5] = 0x9b05688cu;
    ctx->state[6] = 0x1f83d9abu; ctx->state[7] = 0x5be0cd19u;
}

static void sha256_update(sha256_ctx *ctx, const uint8_t *data, size_t len) {
    for (size_t i = 0; i < len; ++i) {
        ctx->data[ctx->datalen++] = data[i];
        if (ctx->datalen == 64) {
            sha256_transform(ctx, ctx->data);
            ctx->bitlen += 512;
            ctx->datalen = 0;
        }
    }
}

static void sha256_final(sha256_ctx *ctx, uint8_t hash[32]) {
    size_t i = ctx->datalen;
    if (ctx->datalen < 56) {
        ctx->data[i++] = 0x80;
        while (i < 56) ctx->data[i++] = 0x00;
    } else {
        ctx->data[i++] = 0x80;
        while (i < 64) ctx->data[i++] = 0x00;
        sha256_transform(ctx, ctx->data);
        memset(ctx->data, 0, 56);
    }
    ctx->bitlen += ctx->datalen * 8ULL;
    for (int k = 0; k < 8; ++k) ctx->data[63 - k] = (uint8_t)(ctx->bitlen >> (8 * k));
    sha256_transform(ctx, ctx->data);
    for (int k = 0; k < 8; ++k) {
        hash[4*k+0] = (uint8_t)(ctx->state[k] >> 24);
        hash[4*k+1] = (uint8_t)(ctx->state[k] >> 16);
        hash[4*k+2] = (uint8_t)(ctx->state[k] >> 8);
        hash[4*k+3] = (uint8_t)(ctx->state[k]);
    }
}

static inline uint32_t canon_rev_u32(uint32_t code, int M_len) {
    if (M_len <= 1) return 0u;
    uint32_t last_bit = (code >> (M_len - 2)) & 1u;
    uint32_t rev = 0u;
    for (int k = 1; k < M_len; ++k) {
        int src_idx = M_len - 1 - k;
        uint32_t src_bit = (src_idx == 0) ? 1u : ((code >> (src_idx - 1)) & 1u);
        if (src_bit == last_bit) rev |= (1u << (k - 1));
    }
    return (code < rev) ? code : rev;
}

int main(int argc, char **argv) {
    if (argc != 7) {
        fprintf(stderr, "Usage: %s <M_len> <M_other> <M_bound> <G> <eps_safe> <only_canon>\n", argv[0]);
        return 2;
    }
    int M_len = atoi(argv[1]);
    int M_other = atoi(argv[2]);
    double M_bound = atof(argv[3]);
    int G = atoi(argv[4]);
    double eps_safe = atof(argv[5]);
    int only_canon = atoi(argv[6]);
    if (M_len < 2 || M_len > 32 || G < 32 || (G % 2) != 0) return 3;

    struct timespec ts0, ts1;
    clock_gettime(CLOCK_MONOTONIC, &ts0);

    int n_f = G / 2 + 1;
    double *cos_t = (double *)malloc((size_t)n_f * M_len * sizeof(double));
    double *sin_t = (double *)malloc((size_t)n_f * M_len * sizeof(double));
    int *freq_ord = (int *)malloc((size_t)n_f * sizeof(int));
    int *used = (int *)calloc((size_t)n_f, sizeof(int));

    for (int l = 0; l < n_f; ++l) {
        double th = 2.0 * PI_VAL * l / G;
        for (int j = 0; j < M_len; ++j) {
            cos_t[(size_t)l * M_len + j] = cos(j * th);
            sin_t[(size_t)l * M_len + j] = sin(j * th);
        }
    }
    int fo_n = 0;
    for (int step = G / 4; step >= 1; step >>= 1) {
        for (int l = step; l < n_f; l += step) {
            if (!used[l]) { freq_ord[fo_n++] = l; used[l] = 1; }
        }
    }
    for (int l = 0; l < n_f; ++l) if (!used[l]) freq_ord[fo_n++] = l;

    double B_safe = sqrt(M_bound) + eps_safe;
    double M_safe = M_bound + eps_safe;
    double min_other = (double)(M_other % 2);
    int max_abs_S = (int)floor(B_safe - min_other + 1e-9);
    double max_U_sq = M_bound - min_other * min_other + eps_safe;

    uint64_t n_seq = 1ULL << (M_len - 1);
    uint32_t alt_flip_mask = 0x55555555u & ((M_len - 1 >= 32) ? 0xffffffffu : ((1u << (M_len - 1)) - 1u));

    sha256_ctx ctx;
    sha256_init(&ctx);
    uint64_t S = 0ULL;

    for (uint64_t idx = 0; idx < n_seq; ++idx) {
        uint32_t code = (uint32_t)idx;
        int s_val = 1 + 2 * __builtin_popcount(code) - (M_len - 1);
        int abs_s = s_val >= 0 ? s_val : -s_val;
        if (abs_s > max_abs_S) continue;

        int u_val = 1 + 2 * __builtin_popcount(code ^ alt_flip_mask) - (M_len - 1);
        if ((double)(u_val * u_val) > max_U_sq) continue;

        if (only_canon && canon_rev_u32(code, M_len) != code) continue;

        int ok = 1;
        for (int fi = 0; fi < n_f; ++fi) {
            int l = freq_ord[fi];
            const double *ct = cos_t + (size_t)l * M_len;
            const double *st = sin_t + (size_t)l * M_len;
            double rv = ct[0], iv = st[0];
            for (int j = 1; j < M_len; ++j) {
                double cj = ((code >> (j - 1)) & 1u) ? 1.0 : -1.0;
                rv += cj * ct[j];
                iv += cj * st[j];
            }
            if (rv * rv + iv * iv > M_safe) { ok = 0; break; }
        }
        if (ok) {
            /* Little-endian uint32_t matches numpy.uint32.tobytes() on x86_64/arm64 */
            uint8_t le[4] = {
                (uint8_t)(code & 0xffu),
                (uint8_t)((code >> 8) & 0xffu),
                (uint8_t)((code >> 16) & 0xffu),
                (uint8_t)((code >> 24) & 0xffu)
            };
            sha256_update(&ctx, le, 4);
            S++;
        }
    }

    uint8_t hash[32];
    sha256_final(&ctx, hash);
    clock_gettime(CLOCK_MONOTONIC, &ts1);
    double elapsed = (ts1.tv_sec - ts0.tv_sec) + 1e-9 * (ts1.tv_nsec - ts0.tv_nsec);

    printf("S=%llu sha256=", (unsigned long long)S);
    for (int i = 0; i < 32; ++i) printf("%02x", hash[i]);
    printf(" elapsed_s=%.3f\n", elapsed);

    free(cos_t); free(sin_t); free(freq_ord); free(used);
    return 0;
}
