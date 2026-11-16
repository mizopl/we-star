"""All n-qubit stabilizer states, by closing the Clifford orbit of |0...0>.

stabilizer_extent.enumerate_stabilizer_states covers odd prime dimensions only,
and the qubit case is the one that needs care: the phase of a qubit stabilizer
state runs over the fourth roots of unity, not the second, so a parametrisation
written for w_p with p = 2 reaches only the real states and misses the Y
eigenstates entirely.

Closing the Clifford orbit sidesteps the parametrisation. The Clifford group
acts transitively on stabilizer states, so a breadth-first closure under H, S
and CNOT from |0...0> reaches all of them, and the known count
2^n prod_{k=1..n} (2^k + 1) checks that it did.

Every nonzero amplitude of a stabilizer state has the same modulus, so dividing
by the first nonzero entry puts every entry in {0, 1, -1, i, -i} exactly. The
deduplication key is exact integer data rather than a rounded float, which
matters here: rounding keys is what made an earlier search in this repository
miss 18 of 45 configurations.
"""

from __future__ import annotations

import numpy as np


def count(n):
    """2^n prod_{k=1..n} (2^k + 1), the number of n-qubit stabilizer states."""
    t = 1 << n
    for k in range(1, n + 1):
        t *= (1 << k) + 1
    return t


def _key(v):
    nz = np.flatnonzero(np.abs(v) > 1e-9)
    w = v / v[nz[0]]
    return (np.rint(w.real).astype(np.int8).tobytes()
            + np.rint(w.imag).astype(np.int8).tobytes())


def _clifford_generators(n):
    dim = 1 << n
    gates = []
    for j in range(n):
        H = np.zeros((dim, dim), complex)
        S = np.zeros((dim, dim), complex)
        for x in range(dim):
            b = (x >> j) & 1
            y = x ^ (1 << j)
            H[x if b == 0 else y, x] += 1 / np.sqrt(2)
            H[y if b == 0 else x, x] += (1 if b == 0 else -1) / np.sqrt(2)
            S[x, x] = 1j if b else 1
        gates += [H, S]
    for c in range(n):
        for t in range(n):
            if c == t:
                continue
            M = np.zeros((dim, dim), complex)
            for x in range(dim):
                M[x ^ (1 << t) if (x >> c) & 1 else x, x] = 1
            gates.append(M)
    return gates


def all_states(n, check=True):
    """Every n-qubit stabilizer state, one column each, deduped up to phase."""
    dim = 1 << n
    gates = _clifford_generators(n)
    start = np.zeros(dim, complex)
    start[0] = 1
    seen = {_key(start): start}
    frontier = [start]
    while frontier:
        nxt = []
        for v in frontier:
            for g in gates:
                w = g @ v
                k = _key(w)
                if k not in seen:
                    seen[k] = w
                    nxt.append(w)
        frontier = nxt
    out = np.stack(list(seen.values()), axis=1)
    if check and out.shape[1] != count(n):
        raise AssertionError(f"found {out.shape[1]} states on {n} qubits, "
                             f"expected {count(n)}")
    return out
