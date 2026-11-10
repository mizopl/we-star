"""Every n-qutrit stabilizer state, as phase codes, fast enough for n = 4.

A qutrit stabilizer state is uniform in modulus on an affine flat and carries
a phase that is a power of w3 at each point, so it is determined up to a
global phase by an int8 vector of length 3^n: the exponent of w3 at each
support point and -1 off the support, normalised so the first nonzero entry
has exponent 0. That is 81 bytes for a four-qutrit state against 1296 for the
complex128 vector, and the 7,439,040 states on four qutrits fit in 600 MB.

Enumeration follows the parametrisation the verifier uses (RREF W, coset
representative supported off the pivots, quadratic-plus-linear phase), but
for each flat the whole family of phases is produced at once: the monomials
y_i, y_i^2, y_s y_t (s < t) are linearly independent as functions on F_3^k,
so the 3^(2k + k(k-1)/2) coefficient vectors give that many distinct states,
and their exponent tables are one integer matrix product mod 3. The count is
checked against 3^n prod_{j=1..n} (3^j + 1), which is what makes the
enumeration a dictionary rather than a sample.

`expand` turns a block of codes back into complex64 amplitudes with the
1/sqrt(3^k) normalisation, and `inner` computes <v | s_j> for every state in
chunks without ever holding the whole complex array.
"""

from __future__ import annotations

import itertools

import numpy as np

W3 = np.exp(2j * np.pi / 3)


def count(n, p=3):
    t = p ** n
    for k in range(1, n + 1):
        t *= p ** k + 1
    return t


def _rref_matrices(n, k, p=3):
    """Every k x n matrix in reduced row echelon form over F_p, with its pivots."""
    out = []
    for pivots in itertools.combinations(range(n), k):
        non_pivots = [j for j in range(n) if j not in pivots]
        # free entries: row r may be nonzero only in non-pivot columns to the right of pivot r
        free = [(r, c) for r in range(k) for c in non_pivots if c > pivots[r]]
        for vals in itertools.product(range(p), repeat=len(free)):
            W = np.zeros((k, n), dtype=np.int64)
            for r in range(k):
                W[r, pivots[r]] = 1
            for (r, c), v in zip(free, vals):
                W[r, c] = v
            out.append((W, pivots, non_pivots))
    return out


def _monomials(k, p=3):
    """Monomial evaluation matrix (p^k points x nmono) and the y-strings."""
    ys = np.array(list(itertools.product(range(p), repeat=k)), dtype=np.int64)  # (p^k, k)
    cols = [ys[:, i] for i in range(k)] + [ys[:, i] ** 2 for i in range(k)]
    cols += [ys[:, s] * ys[:, t] for s in range(k) for t in range(s + 1, k)]
    M = np.stack(cols, axis=1) if cols else np.zeros((p ** k, 0), dtype=np.int64)
    return ys, M % p


def all_codes(n, p=3, check=True):
    """(codes, k) for every n-qutrit stabilizer state.

    codes: int8 array (N, p^n), exponent of w_p at each point, -1 off support,
           first nonzero entry normalised to 0.
    k:     int8 array (N,), the flat dimension of each state.
    """
    if p != 3:
        raise ValueError("phase codes are for qutrits; qubits use qubit_states.all_states")
    dim = p ** n
    blocks, kblocks = [], []
    for k in range(n + 1):
        ys, M = _monomials(k, p)                       # (p^k, k), (p^k, nmono)
        nmono = M.shape[1]
        nphase = p ** nmono
        # exponent table (nphase, p^k): coefficient vectors in mixed radix p,
        # multiplied against the monomial matrix in chunks to bound memory
        expo = np.empty((nphase, p ** k), dtype=np.int8)
        MT = M.T.astype(np.int64)
        step = 1 << 18
        for lo in range(0, nphase, step):
            ids = np.arange(lo, min(lo + step, nphase), dtype=np.int64)
            coeffs = np.stack([(ids // p ** j) % p for j in range(nmono)], axis=1) \
                if nmono else np.zeros((len(ids), 0), dtype=np.int64)
            expo[lo:lo + len(ids)] = ((coeffs @ MT) % p).astype(np.int8)
        for W, pivots, non_pivots in _rref_matrices(n, k, p):
            # support points x(y) = x0 + W^T y for every coset representative x0
            for x0_free in itertools.product(range(p), repeat=n - k):
                x0 = np.zeros(n, dtype=np.int64)
                for j, c in enumerate(non_pivots):
                    x0[c] = x0_free[j]
                pts = (x0[None, :] + ys @ W) % p        # (p^k, n)
                idx = np.zeros(p ** k, dtype=np.int64)
                for c in range(n):
                    idx = idx * p + pts[:, c]
                block = np.full((expo.shape[0], dim), -1, dtype=np.int8)
                block[:, idx] = expo
                # normalise: the first support point in index order has exponent 0
                first = idx.min()
                shift = block[:, first][:, None]              # int8, in 0..p-1
                block[:, idx] = np.mod(block[:, idx] - shift, np.int8(p))
                blocks.append(block)
                kblocks.append(np.full(expo.shape[0], k, dtype=np.int8))
    codes = np.concatenate(blocks, axis=0)
    ks = np.concatenate(kblocks)
    if check and codes.shape[0] != count(n, p):
        raise AssertionError(f"enumerated {codes.shape[0]} states on {n} qutrits, "
                             f"expected {count(n, p)}")
    return codes, ks


def expand(codes, ks, p=3):
    """Complex128 amplitudes (dim, nblock) of a block of codes, unit norm.

    Double precision throughout: the parallel test compares overlaps against
    1 - 1e-6, which single precision on 81-dimensional vectors cannot resolve."""
    roots = np.exp(2j * np.pi * np.arange(p) / p)
    amp = np.where(codes >= 0, roots[np.clip(codes, 0, p - 1)], 0).astype(np.complex128)
    amp /= np.sqrt(p ** ks.astype(np.float64))[:, None]
    return amp.T


def inner(v, codes, ks, chunk=200_000, p=3):
    """<v | s_j> for every state j, computed in chunks; complex128 array (N,)."""
    v = np.asarray(v, dtype=np.complex128).conj()
    out = np.empty(codes.shape[0], dtype=np.complex128)
    for lo in range(0, codes.shape[0], chunk):
        out[lo:lo + chunk] = v @ expand(codes[lo:lo + chunk], ks[lo:lo + chunk], p)
    return out


def project(R, codes, ks, chunk=200_000, p=3):
    """R @ s_j for every state, for a small matrix R (r, dim); complex128 (r, N)."""
    R = np.asarray(R, dtype=np.complex128)
    out = np.empty((R.shape[0], codes.shape[0]), dtype=np.complex128)
    for lo in range(0, codes.shape[0], chunk):
        out[:, lo:lo + chunk] = R @ expand(codes[lo:lo + chunk], ks[lo:lo + chunk], p)
    return out


def encode(amp, p=3, tol=1e-4):
    """Inverse of `expand` for exact stabilizer states: codes of unit vectors
    whose entries are 0 or a common modulus times a p-th root of unity, up to a
    global phase. Raises if an entry is not of that form."""
    amp = np.asarray(amp)
    dim, nb = amp.shape
    mags = np.abs(amp)
    nz = mags > tol * mags.max(axis=0, keepdims=True)
    first = np.argmax(nz, axis=0)
    ref = amp[first, np.arange(nb)]
    ratio = amp / ref[None, :]
    ang = np.angle(ratio) / (2 * np.pi / p)
    e = np.rint(ang).astype(np.int64) % p
    ok = np.abs(ratio - np.exp(2j * np.pi * e / p)) < 1e-3
    if not np.all(ok | ~nz):
        raise AssertionError("an image amplitude is not a p-th root of unity times the reference")
    return np.where(nz, e, -1).astype(np.int8).T


if __name__ == "__main__":
    import sys
    import time
    n = int(sys.argv[1]) if len(sys.argv) > 1 else 3
    t = time.time()
    codes, ks = all_codes(n)
    print(f"{codes.shape[0]} states on {n} qutrits in {time.time() - t:.1f}s, "
          f"{codes.nbytes / 1e6:.0f} MB")
