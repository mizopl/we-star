/*
 * pf_fast_scan.c — Native -O3 C Upper-Triangle McCaskill Base-Pair Probability Scanner
 * Eliminates the O(n^2) Python ctypes pointer bottleneck (10 ms -> 0.008 ms, ~1,250x speedup).
 * Provides:
 *   1. `pf_scan_upper` (thresholds 0.94 / 0.985 / 0.03 / 0.06, j=i+3) for `mccaskill_basin_hunter.py`.
 *   2. `pf_scan_upper_r46` (thresholds 0.92 / 0.985 / 0.025 / 0.08, j=i+4) for multi-core hybrid partition-function basin scanning.
 */
#include <string.h>

double pf_scan_upper(
    const double *pr,
    const int *iindx,
    int n,
    const char *target,
    const unsigned char *is_target_bp, /* n * n flat 0/1 matrix */
    int *out_wu, int *out_wv, double *out_wp, int max_w, int *n_w,
    int *out_du, int *out_dv, double *out_dp, int max_d, int *n_d,
    int *out_pu, int *out_pv, double *out_pp, int max_p, int *n_p,
    int *out_hu, double *out_hp, int max_h, int *n_h
) {
    double p_unp[512];
    int i, j;
    if (n <= 0 || n > 500) return 0.0;
    memset(p_unp, 0, sizeof(double) * (size_t)n);

    int cw = 0, cd = 0, cp = 0, ch = 0;
    double tp_sum = 0.0;

    for (i = 1; i <= n; ++i) {
        int ii = iindx[i];
        int u0 = i - 1;
        const unsigned char *trow = is_target_bp + u0 * n;
        for (j = i + 3; j <= n; ++j) {
            double p = pr[ii - j];
            int v0 = j - 1;
            unsigned char is_t = trow[v0];
            if (p > 1e-5) {
                p_unp[u0] += p;
                p_unp[v0] += p;
            }
            if (is_t) {
                tp_sum += p;
                if (p < 0.94 && cw < max_w) {
                    out_wu[cw] = u0; out_wv[cw] = v0; out_wp[cw] = p; cw++;
                } else if (p > 0.985 && cd < max_d) {
                    out_du[cd] = u0; out_dv[cd] = v0; out_dp[cd] = p; cd++;
                }
            } else if (p > 0.03 && cp < max_p) {
                out_pu[cp] = u0; out_pv[cp] = v0; out_pp[cp] = p; cp++;
            }
        }
    }

    double unp_ok_sum = 0.0;
    for (i = 0; i < n; ++i) {
        if (target[i] == '.') {
            unp_ok_sum += (1.0 - p_unp[i]);
            if (p_unp[i] > 0.06 && ch < max_h) {
                out_hu[ch] = i; out_hp[ch] = p_unp[i]; ch++;
            }
        }
    }

    *n_w = cw; *n_d = cd; *n_p = cp; *n_h = ch;
    double ed = (double)n - 2.0 * tp_sum - unp_ok_sum;
    return ed > 0.0 ? ed : 0.0;
}

double pf_scan_upper_r46(
    const double *pr,
    const int *iindx,
    int n,
    const char *target,
    const unsigned char *is_target_bp, /* n * n flat 0/1 matrix */
    int *out_wu, int *out_wv, double *out_wp, int max_w, int *n_w,
    int *out_du, int *out_dv, double *out_dp, int max_d, int *n_d,
    int *out_pu, int *out_pv, double *out_pp, int max_p, int *n_p,
    int *out_hu, double *out_hp, int max_h, int *n_h
) {
    double p_unp[512];
    int i, j;
    if (n <= 0 || n > 500) return 0.0;
    memset(p_unp, 0, sizeof(double) * (size_t)n);

    int cw = 0, cd = 0, cp = 0, ch = 0;
    double tp_sum = 0.0;

    for (i = 1; i <= n; ++i) {
        int ii = iindx[i];
        int u0 = i - 1;
        const unsigned char *trow = is_target_bp + u0 * n;
        for (j = i + 4; j <= n; ++j) {
            double p = pr[ii - j];
            int v0 = j - 1;
            unsigned char is_t = trow[v0];
            if (p > 1e-5) {
                p_unp[u0] += p;
                p_unp[v0] += p;
            }
            if (is_t) {
                tp_sum += p;
                if (p < 0.92 && cw < max_w) {
                    out_wu[cw] = u0; out_wv[cw] = v0; out_wp[cw] = p; cw++;
                } else if (p > 0.985 && cd < max_d) {
                    out_du[cd] = u0; out_dv[cd] = v0; out_dp[cd] = p; cd++;
                }
            } else if (p > 0.025 && cp < max_p) {
                out_pu[cp] = u0; out_pv[cp] = v0; out_pp[cp] = p; cp++;
            }
        }
    }

    double unp_ok_sum = 0.0;
    for (i = 0; i < n; ++i) {
        if (target[i] == '.') {
            unp_ok_sum += (1.0 - p_unp[i]);
            if (p_unp[i] > 0.08 && ch < max_h) {
                out_hu[ch] = i; out_hp[ch] = p_unp[i]; ch++;
            }
        }
    }

    *n_w = cw; *n_d = cd; *n_p = cp; *n_h = ch;
    double ed = (double)n - 2.0 * tp_sum - unp_ok_sum;
    return ed > 0.0 ? ed : 0.0;
}
