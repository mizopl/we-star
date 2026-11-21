/*
 * median_oracle.c — CLSS-1 Bit-Parallel Exact Zero-One Oracle for Median Selection Networks
 *
 * Exact formal specification (verified against bertdobbelaere/SorterHunter & Knuth TAOCP 5.3.4):
 *   - Odd n = 2k + 1: wire k must output 0 for all inputs of weight <= k, and 1 for all weight >= k + 1.
 *     By monotonicity of comparator networks, checking ONLY weight slices w = k and w = k + 1 is
 *     100% necessary and sufficient for all 2^n inputs.
 *   - Even n = 2k: unordered middle pair {k - 1, k} must output:
 *       (0, 0) for weight <= k - 1,
 *       {0, 1} (sum == 1) for weight == k,
 *       (1, 1) for weight >= k + 1.
 *     By monotonicity + weight conservation (Theorem B): checking ONLY weight slices
 *       w = k - 1 (y[k-1]==0 && y[k]==0) and w = k + 1 (y[k-1]==1 && y[k]==1)
 *     is 100% necessary and sufficient for all 2^n inputs (w == k is automatically forced!).
 *     Furthermore, if the network is vertically symmetric (i <-> n-1-i), w = k - 1 alone suffices!
 *
 * Usage:
 *   median_oracle <mode: slices|slices3|full|sym> <n> <L> <a0> <b0> <a1> <b1> ...
 *   OR read from stdin with "-" as mode-followed args:
 *   median_oracle --batch <mode>
 *     stdin lines: <n> <L> <a0> <b0> ...
 */

#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>

#define MAX_N 32
#define MAX_L 512
#define LOW_BITS 9
#define MAX_LOW_CHUNKS 4

typedef struct {
    int count;
    int nchunks;
    uint64_t bits[MAX_LOW_CHUNKS][LOW_BITS];
    uint64_t mask[MAX_LOW_CHUNKS];
} LowSlice;

static LowSlice g_low[LOW_BITS + 1];
static int g_low_init = 0;

static void init_low_slices(int low_n) {
    memset(g_low, 0, sizeof(g_low));
    int lim = 1 << low_n;
    for (int x = 0; x < lim; x++) {
        int w = __builtin_popcount((unsigned)x);
        LowSlice *ls = &g_low[w];
        int idx = ls->count++;
        int ch = idx >> 6;
        int bit = idx & 63;
        if (ch + 1 > ls->nchunks) ls->nchunks = ch + 1;
        ls->mask[ch] |= (1ULL << bit);
        for (int b = 0; b < low_n; b++) {
            if ((x >> b) & 1) {
                ls->bits[ch][b] |= (1ULL << bit);
            }
        }
    }
    g_low_init = low_n;
}

static inline void eval_net_64(uint64_t *w, const int *ca, const int *cb, int L) {
    for (int i = 0; i < L; i++) {
        int a = ca[i], b = cb[i];
        uint64_t wa = w[a], wb = w[b];
        w[a] = wa & wb;
        w[b] = wa | wb;
    }
}

/* Count failing vectors on a single weight slice w_target.
 * check_type:
 *   0: odd n, want y[k] == 0
 *   1: odd n, want y[k] == 1
 *   2: even n, want y[k-1] == 0 && y[k] == 0
 *   3: even n, want y[k-1] == 1 && y[k] == 1
 *   4: even n, want (y[k-1] ^ y[k]) == 1
 * If stop_on_first != 0, returns immediately on first failure (>0).
 */
static uint64_t check_weight_slice(int n, int L, const int *ca, const int *cb,
                                   int w_target, int check_type, int stop_on_first) {
    int low_n = (n < LOW_BITS) ? n : LOW_BITS;
    if (g_low_init != low_n) init_low_slices(low_n);
    int hi_n = n - low_n;
    int k = n / 2;
    uint64_t errors = 0;
    uint64_t wires[MAX_N];

    int r_min = w_target - hi_n;
    if (r_min < 0) r_min = 0;
    int r_max = (w_target < low_n) ? w_target : low_n;

    for (int r = r_min; r <= r_max; r++) {
        int hi_w = w_target - r;
        const LowSlice *ls = &g_low[r];
        if (ls->nchunks == 0) continue;

        uint32_t hi_lim = 1U << hi_n;
        uint32_t hi = (hi_w == 0) ? 0U : ((1U << hi_w) - 1U);

        for (;;) {
            /* Fill high wires once per hi combination */
            uint64_t hi_wires[MAX_N];
            for (int j = 0; j < hi_n; j++) {
                hi_wires[low_n + j] = ((hi >> j) & 1U) ? ~0ULL : 0ULL;
            }

            for (int ch = 0; ch < ls->nchunks; ch++) {
                for (int b = 0; b < low_n; b++) wires[b] = ls->bits[ch][b];
                for (int j = 0; j < hi_n; j++) wires[low_n + j] = hi_wires[low_n + j];

                eval_net_64(wires, ca, cb, L);

                uint64_t bad = 0;
                uint64_t m = ls->mask[ch];
                if (check_type == 0) {
                    bad = wires[k] & m;
                } else if (check_type == 1) {
                    bad = (~wires[k]) & m;
                } else if (check_type == 2) {
                    bad = (wires[k - 1] | wires[k]) & m;
                } else if (check_type == 3) {
                    bad = (~(wires[k - 1] & wires[k])) & m;
                } else {
                    bad = (~(wires[k - 1] ^ wires[k])) & m;
                }
                if (bad) {
                    errors += (uint64_t)__builtin_popcountll(bad);
                    if (stop_on_first) return errors;
                }
            }

            if (hi_w == 0) break;
            /* Gosper's hack for next hi_w-bit subset of hi_n bits */
            uint32_t c = hi & (uint32_t)(-(int32_t)hi);
            uint32_t r2 = hi + c;
            if (r2 >= hi_lim) break;
            hi = (((r2 ^ hi) >> 2) / c) | r2;
        }
    }
    return errors;
}

static uint64_t check_full_2n(int n, int L, const int *ca, const int *cb, int stop_on_first) {
    uint64_t errors = 0;
    int k = n / 2;
    if (n % 2 == 1) {
        for (int w = 0; w <= n; w++) {
            int ct = (w <= k) ? 0 : 1;
            errors += check_weight_slice(n, L, ca, cb, w, ct, stop_on_first);
            if (stop_on_first && errors) return errors;
        }
    } else {
        for (int w = 0; w <= n; w++) {
            int ct = (w < k) ? 2 : ((w == k) ? 4 : 3);
            errors += check_weight_slice(n, L, ca, cb, w, ct, stop_on_first);
            if (stop_on_first && errors) return errors;
        }
    }
    return errors;
}

static int is_vertically_symmetric(int n, int L, const int *ca, const int *cb) {
    if (n % 2 == 1) return 0;
    /* Check layer-by-layer (canonical greedy layering) symmetry: (a,b) <-> (n-1-b, n-1-a) */
    int wire_layer[MAX_N];
    int ce_layer[MAX_L];
    int max_d = 0;
    memset(wire_layer, 0, sizeof(wire_layer));
    for (int i = 0; i < L; i++) {
        int a = ca[i], b = cb[i];
        int d = (wire_layer[a] > wire_layer[b]) ? wire_layer[a] : wire_layer[b];
        ce_layer[i] = d;
        wire_layer[a] = d + 1;
        wire_layer[b] = d + 1;
        if (d + 1 > max_d) max_d = d + 1;
    }
    for (int d = 0; d < max_d; d++) {
        for (int i = 0; i < L; i++) {
            if (ce_layer[i] != d) continue;
            int ma = n - 1 - cb[i];
            int mb = n - 1 - ca[i];
            int found = 0;
            for (int j = 0; j < L; j++) {
                if (ce_layer[j] == d && ca[j] == ma && cb[j] == mb) {
                    found = 1;
                    break;
                }
            }
            if (!found) return 0;
        }
    }
    return 1;
}

static uint64_t verify_mode(const char *mode, int n, int L, const int *ca, const int *cb,
                            int count_all) {
    int k = n / 2;
    int stop = !count_all;
    uint64_t errs = 0;
    if (strcmp(mode, "full") == 0) {
        return check_full_2n(n, L, ca, cb, stop);
    } else if (strcmp(mode, "slices3") == 0) {
        if (n % 2 == 1) {
            errs += check_weight_slice(n, L, ca, cb, k, 0, stop);
            if (stop && errs) return errs;
            errs += check_weight_slice(n, L, ca, cb, k + 1, 1, stop);
            return errs;
        } else {
            errs += check_weight_slice(n, L, ca, cb, k - 1, 2, stop);
            if (stop && errs) return errs;
            errs += check_weight_slice(n, L, ca, cb, k, 4, stop);
            if (stop && errs) return errs;
            errs += check_weight_slice(n, L, ca, cb, k + 1, 3, stop);
            return errs;
        }
    } else if (strcmp(mode, "sym") == 0) {
        if (n % 2 == 0 && is_vertically_symmetric(n, L, ca, cb)) {
            return check_weight_slice(n, L, ca, cb, k - 1, 2, stop);
        }
        /* fallback to slices */
    }
    /* default: slices (2 critical slices — 100% exact by monotonicity!) */
    if (n % 2 == 1) {
        errs += check_weight_slice(n, L, ca, cb, k, 0, stop);
        if (stop && errs) return errs;
        errs += check_weight_slice(n, L, ca, cb, k + 1, 1, stop);
        return errs;
    } else {
        errs += check_weight_slice(n, L, ca, cb, k - 1, 2, stop);
        if (stop && errs) return errs;
        errs += check_weight_slice(n, L, ca, cb, k + 1, 3, stop);
        return errs;
    }
}

int main(int argc, char **argv) {
    if (argc < 3) {
        fprintf(stderr, "Usage: %s <slices|slices3|full|sym> [--count] <n> <L> <a0> <b0> ...\n", argv[0]);
        fprintf(stderr, "   or: %s --batch <slices|slices3|full|sym> [--count]\n", argv[0]);
        return 2;
    }
    if (strcmp(argv[1], "--batch") == 0) {
        const char *mode = argv[2];
        int count_all = (argc >= 4 && strcmp(argv[3], "--count") == 0);
        int n, L;
        int ca[MAX_L], cb[MAX_L];
        while (scanf("%d %d", &n, &L) == 2) {
            if (n < 3 || n > MAX_N || L < 0 || L > MAX_L) {
                fprintf(stderr, "Invalid n=%d L=%d\n", n, L);
                return 2;
            }
            for (int i = 0; i < L; i++) {
                if (scanf("%d %d", &ca[i], &cb[i]) != 2) return 2;
            }
            struct timespec t0, t1;
            clock_gettime(CLOCK_MONOTONIC, &t0);
            uint64_t errs = verify_mode(mode, n, L, ca, cb, count_all);
            clock_gettime(CLOCK_MONOTONIC, &t1);
            double ms = (t1.tv_sec - t0.tv_sec) * 1000.0 + (t1.tv_nsec - t0.tv_nsec) / 1e6;
            printf("%s %llu %.3f\n", errs == 0 ? "PASS" : "FAIL", (unsigned long long)errs, ms);
            fflush(stdout);
        }
        return 0;
    }

    const char *mode = argv[1];
    int argi = 2;
    int count_all = 0;
    if (argi < argc && strcmp(argv[argi], "--count") == 0) {
        count_all = 1;
        argi++;
    }
    int n = atoi(argv[argi++]);
    int L = atoi(argv[argi++]);
    if (n < 3 || n > MAX_N || L < 0 || L > MAX_L || argc < argi + 2 * L) {
        fprintf(stderr, "Bad args n=%d L=%d\n", n, L);
        return 2;
    }
    int ca[MAX_L], cb[MAX_L];
    for (int i = 0; i < L; i++) {
        ca[i] = atoi(argv[argi++]);
        cb[i] = atoi(argv[argi++]);
    }
    struct timespec t0, t1;
    clock_gettime(CLOCK_MONOTONIC, &t0);
    uint64_t errs = verify_mode(mode, n, L, ca, cb, count_all);
    clock_gettime(CLOCK_MONOTONIC, &t1);
    double ms = (t1.tv_sec - t0.tv_sec) * 1000.0 + (t1.tv_nsec - t0.tv_nsec) / 1e6;
    printf("%s %llu %.3f\n", errs == 0 ? "PASS" : "FAIL", (unsigned long long)errs, ms);
    return errs == 0 ? 0 : 1;
}
