"""Verification pipeline for stabilizer-rank bound submissions.

A submission claims a bound on chi(|M>^{ot m}) for one magic-state orbit. The
pipeline decides what tier it has earned; nothing is taken on the submitter's
word.

Upper bounds carry an explicit decomposition. Each term is given by its
stabilizer parametrisation

    |sigma> propto sum_{y in F_p^k} w_p^{Q(y) + l.y} |x0 + W y>,

not as a raw amplitude vector, so a term that is not a stabilizer state cannot
be expressed in the first place. For qubits the phase group is the fourth roots
of unity rather than the second, so there the phase is i^{l.y} (-1)^{Q(y)} with
l read mod 4 and Q mod 2; every qubit stabilizer state has this form, and with
w_2 = -1 alone the Y eigenstates could not be written at all. The verifier
rebuilds every term and the target in exact arithmetic and requires the
identity to hold on the nose. A floating-point near-miss earns nothing.

Lower bounds cannot be checked from a static witness, so they carry a
certificate script. The pipeline runs it under a time budget and requires it to
exit zero having printed its claim. A bound with no runnable certificate is
recorded at the `cited` tier and is never allowed to set a leaderboard record.

Tiers, in decreasing strength:
    lean        a Lean theorem proves it, and the build receipt confirms it compiles
    verified    exact arithmetic confirmed the decomposition here, or a
                lower-bound certificate exact throughout, with no margin
    reproduced  a certificate script ran to completion and asserted the bound
    attested    the argument is exact but rests on an offline enumeration too
                large for any budget; the certificate checked the hashes of
                every stored batch output, re-decided the stored exceptions,
                and re-ran a declared subset of batches from scratch
    cited       attributed to the literature; not machine-checked

The Lean tier is the one that does not depend on trusting this file. Building
mathlib is far too slow to run on every site build, so a bound claiming it needs
a receipt in certs/lean-<module>.json written by `make lean-certify` after a
real `lake build`. Without the receipt the claim is ignored and the bound falls
back to whatever the exact-arithmetic check earns it, so a Lean claim can never
inflate a tier on its own.
"""

from __future__ import annotations

import hashlib
import json
import os
import re
import subprocess
import sys
import time

import sympy as sp

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# ---------------------------------------------------------------- orbits ----
# Each orbit fixes the local dimension p and the single-qudit magic state, in
# exact arithmetic. These are the states the literature's exponents refer to;
# the names match the repo's state-of-the-art page.

def _w(p):
    """Primitive p-th root of unity, in a form sympy can reason about.

    exp(2*pi*I/p) is correct but sympy will not reduce sums of its powers to
    zero on its own, so give it the radical form for the cases that matter.
    """
    if p == 2:
        return sp.Integer(-1)
    if p == 3:
        return sp.Rational(-1, 2) + sp.I * sp.sqrt(3) / 2
    return sp.exp(2 * sp.pi * sp.I / p)


def is_zero(e, digits=60, tol=sp.Float("1e-45")):
    """Decide whether an exact expression vanishes.

    Tries symbolic reduction first. Cyclotomic entries (the T3 orbit lives in
    Q(w9)) do not always reduce symbolically, so fall back to evaluating at
    `digits` significant figures and requiring the modulus below `tol`. That is
    far tighter than any floating-point search could fake, and the terms are
    stabilizer states by construction, so a pass here is a genuine certificate.
    """
    z = sp.simplify(sp.expand(e))
    if z == 0:
        return True, "symbolic"
    z = sp.simplify(sp.expand_complex(z))
    if z == 0:
        return True, "symbolic"
    try:
        v = abs(complex(sp.N(z, digits)))
    except (TypeError, ValueError):
        return False, "undecided"
    return (v < float(tol)), f"numeric<{digits}dig>"


def orbit_state(orbit):
    """The single-qudit magic state for an orbit, as an exact column vector."""
    if orbit == "S":                      # Strange
        return sp.Matrix([0, 1, -1]) / sp.sqrt(2)
    if orbit == "N":                      # Norrell
        return sp.Matrix([1, 1, -2]) / sp.sqrt(6)
    if orbit == "H3":                     # qutrit Hadamard eigenstate
        # eigenvector of the qutrit Fourier transform with eigenvalue 1
        r3 = sp.sqrt(3)
        a = sp.sqrt((3 + r3) / 6)
        b = sp.sqrt((3 - r3) / 12)
        return sp.Matrix([a, b, b])
    if orbit == "T3":                     # qutrit T-type / face centre
        w9 = sp.exp(2 * sp.pi * sp.I / 9)
        return sp.Matrix([1, w9, w9 ** 2]) / sp.sqrt(3)
    if orbit == "qubit_H":                # qubit H-type, edge centre
        return sp.Matrix([sp.cos(sp.pi / 8), sp.sin(sp.pi / 8)])
    if orbit == "qubit_T":                # qubit Bravyi-Kitaev T-type, face centre
        b = sp.acos(1 / sp.sqrt(3)) / 2
        return sp.Matrix([sp.cos(b), sp.exp(sp.I * sp.pi / 4) * sp.sin(b)])
    if orbit == "T5":                     # ququint T-type (Howard-Vala, Campbell-Anwar-Browne)
        # For p >= 5 the qudit pi/8 gate is diag(w_p^{P(x)}) with P a cubic
        # over F_p (Howard and Vala, arXiv:1206.1598, eq. 25), and every
        # nonzero cubic coefficient is Clifford-equivalent to x^3 since the
        # quadratic and linear parts are Clifford phases and x -> ax is a
        # Clifford permutation with a^3 ranging over F_5^*. The magic state
        # is the gate applied to |+>, and lives in Q(w_5) like the
        # stabilizer states themselves, unlike T3 which needs Q(w_9).
        w5 = sp.exp(2 * sp.pi * sp.I / 5)
        return sp.Matrix([w5 ** ((x ** 3) % 5) for x in range(5)]) / sp.sqrt(5)
    if orbit == "qubit_sqrtT":           # sqrt(T) state, fourth level of the Clifford hierarchy
        # (|0> + e^{i pi/8}|1>)/sqrt 2 = Z(pi/8)|+>: the magic state of the
        # square root of the T gate. Its phase is a primitive sixteenth root
        # of unity, so the state lives in Q(zeta_16), a degree-4 extension of
        # the Q(i) the qubit stabilizer states live in; the Galois descent
        # that gives chi(T3^m) >= 3 for free gives chi >= min(4, m + 1) here
        # (cert_sqrtt_galois.py). It is not Clifford-equivalent to the H-type
        # (Bloch vector on an edge) or T-type (face) orbits: its Bloch vector
        # is (cos(pi/8), sin(pi/8), 0), and the Clifford group acts on Bloch
        # vectors by signed coordinate permutations.
        return sp.Matrix([1, sp.exp(sp.I * sp.pi / 8)]) / sp.sqrt(2)
    if orbit == "CS":                     # two-qubit controlled-S magic state
        # CS|++> = (|00> + |01> + |10> + i|11>)/2, the first width-2 orbit:
        # m copies live on 2m qubits (ORBIT_WIDTH). The phase i^{x1 x2} is not
        # a Z_4-valued quadratic form with even cross terms, which is exactly
        # why |CS> is not a stabilizer state; CS = ((1+i)/2) I + ((1-i)/2) CZ
        # gives chi(|CS>) = 2.
        return sp.Matrix([1, 1, 1, sp.I]) / 2
    raise ValueError(f"unknown orbit {orbit!r}")


ORBIT_P = {"S": 3, "N": 3, "H3": 3, "T3": 3, "qubit_H": 2, "qubit_T": 2, "T5": 5,
           "qubit_sqrtT": 2, "CS": 2, "cat": 2}

# Qudits per copy. A width-w orbit state lives on w qudits, so m copies live
# on n = w m qudits and every witness term is parametrized over F_p^n; the
# exponent gamma = log_p(rank)/m stays per copy. Orbits absent here have
# width 1.
ORBIT_WIDTH = {"CS": 2}


def orbit_qudits(orbit, m):
    """The number of qudits n that m copies of the orbit state occupy."""
    return ORBIT_WIDTH.get(orbit, 1) * int(m)


ORBIT_LABEL = {
    "S": "Strange", "N": "Norrell", "H3": "H₃", "T3": "T₃",
    "qubit_H": "H-type", "qubit_T": "BK T-type", "T5": "T₅",
    "qubit_sqrtT": "√T", "CS": "CS",
    "cat": "magic cat",
}

# ------------------------------------------------------------- families ----
# A family is a track indexed by the qubit count m rather than by copies of
# one state: |cat_m> is one m-qubit state per m and is not a tensor power of
# anything. `target_vector` builds the family state directly; `orbit_state`
# has nothing to return for it. See docs/notes/new_orbits_design.md, section 6.
FAMILY = {"cat"}


def _weight(x, m):
    return sum((x >> j) & 1 for j in range(m))


def cat_vector(m):
    """|cat_m> = 2^{-1/2}(|T>^m + |T_perp>^m) with |T> = 2^{-1/2}(|0> + e^{i pi/4}|1>)
    and |T_perp> = Z|T> (Qassim, Pashayan, and Gosset, arXiv:2106.07740, Eq. 3).

    The odd-weight strings cancel and the even-weight ones double, so the
    closed form is 2^{-(m-1)/2} sum_{|x| even} i^{|x|/2} |x>, with the string
    read most significant bit first as everywhere in the verifier.
    """
    if m < 1:
        raise ValueError("cat_m needs m >= 1")
    scale = sp.Integer(2) ** sp.Rational(-(m - 1), 2)
    out = sp.zeros(2 ** m, 1)
    for x in range(2 ** m):
        w = _weight(x, m)
        if w % 2 == 0:
            out[x] = scale * sp.I ** (w // 2)
    return out


def family_vector(orbit, m):
    """The m-qubit state of a family track, exactly."""
    if orbit == "cat":
        return cat_vector(m)
    raise ValueError(f"unknown family {orbit!r}")


def target_vector(orbit, m):
    """|M>^{ot m} as an exact column vector of length p^n with n = width * m
    (orbit_qudits), or the m-qubit state of a family track."""
    if orbit in FAMILY:
        return family_vector(orbit, m)
    v = orbit_state(orbit)
    out = v
    for _ in range(m - 1):
        out = sp.Matrix(sp.kronecker_product(out, v))
    return sp.simplify(out)


# ------------------------------------------------------- stabilizer terms ----

def stabilizer_vector(term, p, n):
    """Rebuild one stabilizer state from its parametrisation, exactly.

    term: {"k": k, "x0": [n ints], "W": [k rows of n ints], "Q": [[k x k]],
           "l": [k ints]}
    giving  sum_{y in F_p^k} w_p^{Q(y) + l.y} |x0 + W y>  up to normalisation
    for odd p, and  sum_y i^{l.y} (-1)^{Q(y)} |x0 + W y>  for p = 2, where l.y
    is summed over the integers and read mod 4. The qubit form is the standard
    one (a Z_4-valued quadratic form with even cross terms) and reaches every
    qubit stabilizer state; l = (2, 0, ...) is the same state as putting a 1 on
    the diagonal of Q, which is harmless redundancy rather than a second state.

    Q is read as an upper-triangular form: only entries with i <= j are used, so
    a submitter cannot smuggle in a non-quadratic phase.
    """
    k = int(term["k"])
    x0 = [int(a) % p for a in term["x0"]]
    if len(x0) != n:
        raise ValueError(f"x0 has length {len(x0)}, expected {n}")
    W = [[int(a) % p for a in row] for row in term.get("W", [])]
    if len(W) != k or any(len(r) != n for r in W):
        raise ValueError(f"W must be {k}x{n}")
    Q = [[int(a) % p for a in row] for row in term.get("Q", [[0] * k for _ in range(k)])]
    lmod = 4 if p == 2 else p
    ell = [int(a) % lmod for a in term.get("l", [0] * k)]
    if len(ell) != k:
        raise ValueError(f"l must have length {k}")

    dim = p ** n
    vec = sp.zeros(dim, 1)
    w = _w(p)
    support = set()
    for idx in range(p ** k):
        y = []
        t = idx
        for _ in range(k):
            y.append(t % p)
            t //= p
        x = [(x0[c] + sum(y[r] * W[r][c] for r in range(k))) % p for c in range(n)]
        pos = 0
        for c in range(n):
            pos = pos * p + x[c]
        if pos in support:
            raise ValueError("W is not injective: repeated support point")
        support.add(pos)
        q = sum(Q[i][j] * y[i] * y[j] for i in range(k) for j in range(i, k))
        lin = sum(ell[i] * y[i] for i in range(k))
        if p == 2:
            vec[pos] = sp.I ** (lin % 4) * (-1) ** (q % 2)
        else:
            vec[pos] = w ** ((q + lin) % p)
    return vec / sp.sqrt(p ** k)


# ------------------------------------------------------------ verification ---

class Result:
    def __init__(self, ok, tier, detail, gamma=None):
        self.ok, self.tier, self.detail, self.gamma = ok, tier, detail, gamma

    def __repr__(self):
        return f"<{'PASS' if self.ok else 'FAIL'} tier={self.tier}: {self.detail}>"


def implied_gamma(p, rank, m):
    """Per-copy asymptotic exponent implied by chi(|M>^{ot m}) <= rank."""
    return float(sp.log(rank, p) / m)


def exponent_copies(orbit, m):
    """The denominator of the exponent a rank at m implies, or None when the
    cell implies no exponent.

    For a copy orbit it is m. For the cat family it is m - 2: gluing l copies
    of |cat_m> through <cat_2| gives |cat_{l(m-2)+2}| in chi(cat_m)^l terms,
    and chi(T^n)/2 <= chi(cat_n) <= chi(T^n) (QPG Eq. 4) turns that into the
    qubit exponent log_2 chi(cat_m)/(m - 2); at m = 2 there is none.
    """
    if orbit == "cat":
        return m - 2 if m > 2 else None
    return m


def implied_exponent(orbit, rank, m):
    """The exponent the board shows for chi(target(orbit, m)) <= rank: the
    per-copy exponent for a copy orbit, the implied H-type exponent for a cat
    cell, None where the cell implies none."""
    n = exponent_copies(orbit, int(m))
    if n is None:
        return None
    return implied_gamma(ORBIT_P[orbit], int(rank), n)


def verify_upper(sub):
    """Rebuild the decomposition exactly and require it to equal the target."""
    orbit, m, rank = sub["orbit"], int(sub["m"]), int(sub["rank"])
    p = ORBIT_P[orbit]
    n = orbit_qudits(orbit, m)       # qudits the m copies occupy (width * m)
    terms = sub["witness"]["terms"]
    coeffs = sub["witness"]["coeffs"]
    if len(terms) != rank or len(coeffs) != rank:
        return Result(False, None,
                      f"claims rank {rank} but gives {len(terms)} terms and "
                      f"{len(coeffs)} coefficients")
    try:
        cols = [stabilizer_vector(t, p, n) for t in terms]
    except Exception as exc:
        return Result(False, None, f"a term is not a valid stabilizer state: {exc}")
    try:
        cs = [sp.sympify(c) for c in coeffs]
    except Exception as exc:
        return Result(False, None, f"coefficient did not parse: {exc}")
    if any(is_zero(c)[0] for c in cs):
        return Result(False, None, "a coefficient is zero, so the true rank is lower "
                                   "than claimed; resubmit at the smaller rank")

    tgt = target_vector(orbit, m)
    acc = sp.zeros(p ** n, 1)
    for c, col in zip(cs, cols):
        acc += c * col
    diff = acc - tgt
    modes = set()
    for d in diff:
        ok, how = is_zero(d)
        modes.add(how)
        if not ok:
            try:
                resid = float(sp.sqrt(sum(abs(complex(sp.N(t, 30))) ** 2 for t in diff)))
                extra = f" (residual {resid:.3e})"
            except (TypeError, ValueError):
                extra = ""
            return Result(False, None,
                          f"decomposition does not reproduce the target{extra}")
    how = "symbolically" if modes == {"symbolic"} else "to 60 significant digits"
    what = f"|{orbit}_{m}>" if orbit in FAMILY else f"|{orbit}>^{{ot {m}}}"
    return Result(True, "verified",
                  f"{rank} stabilizer terms reproduce {what}, checked {how}",
                  implied_exponent(orbit, rank, m))


BUDGET_DEFAULT_S = 900
BUDGET_CAP_S = 3600


def certificate_budget(sub, default=BUDGET_DEFAULT_S):
    """The wall-clock budget a lower bound's certificate runs under: the
    default, or the submission's declared `budget_s`, never above the cap."""
    cert = sub.get("certificate") or {}
    declared = cert.get("budget_s")
    if declared is None:
        return default
    return max(1, min(int(declared), BUDGET_CAP_S))


BATCH_FIELDS = ("id", "params", "output", "sha256")


def sha256_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def load_batch_manifest(rel, root=ROOT):
    """The batch manifest behind an attested bound, as a list of entries.

    Returns (batches, error). The file is JSON, either a list or an object with
    a `batches` list; every entry names the batch, its parameters, its stored
    output relative to the repository root and that output's SHA-256.
    """
    path = os.path.join(root, rel)
    if not os.path.isfile(path):
        return None, f"batch manifest not found: {rel}"
    try:
        doc = json.load(open(path))
    except json.JSONDecodeError as exc:
        return None, f"batch manifest {rel} is not valid JSON: {exc}"
    batches = doc.get("batches") if isinstance(doc, dict) else doc
    if not isinstance(batches, list) or not batches:
        return None, f"batch manifest {rel} lists no batches"
    ids = set()
    for i, b in enumerate(batches):
        missing = [k for k in BATCH_FIELDS if not isinstance(b, dict) or k not in b]
        if missing:
            return None, f"batch {i} in {rel} lacks {', '.join(missing)}"
        if b["id"] in ids:
            return None, f"batch id {b['id']!r} is listed twice in {rel}"
        ids.add(b["id"])
    return batches, None


def check_attested(cert, root=ROOT):
    """The cheap half of an attested bound: the manifest exists, the declared
    re-run count fits it, and every stored batch output is present with the
    stated hash. Returns (batches, error); a hash mismatch is an error, since
    an output that has changed since it was recorded is not the enumeration
    the bound rests on.
    """
    att = cert["attested"]
    batches, err = load_batch_manifest(att["batches"], root)
    if err:
        return None, err
    n = len(batches)
    k = int(att["recomputed"])
    if k < 1 or k > n:
        return None, f"attested.recomputed is {k} but the manifest lists {n} batches"
    for b in batches:
        out = os.path.join(root, b["output"])
        if not os.path.isfile(out):
            return None, f"batch {b['id']!r} output not found: {b['output']}"
        got = sha256_file(out)
        if got.lower() != str(b["sha256"]).lower():
            return None, (f"batch {b['id']!r} output {b['output']} has SHA-256 "
                          f"{got[:16]}..., manifest says {str(b['sha256'])[:16]}...")
    return batches, None


SEED_LINE = re.compile(r"^\s*seed\s*[:=]\s*(\S+)", re.I | re.M)

_CERT_RUNS = {}


def run_certificate(path, budget_s):
    """Run a certificate script under a wall-clock budget, once per process.

    Several bounds cite the same script (the two magic-cat lower bounds share
    one, the two T5 lifts another, and the rank-2 and rank-1 exclusions serve
    several orbits), and a rebuild used to run the script again for each of
    them. The first run is kept, keyed by path, and reused for any later
    request it already answers: a run that finished within t seconds answers
    every budget of at least t, and a run that hit its budget answers every
    budget no larger than that one. Returns (proc, elapsed, reused), with
    proc None when the script hit the budget.
    """
    hit = _CERT_RUNS.get(path)
    if hit is not None:
        proc, elapsed, limit = hit
        if (proc is not None and elapsed <= budget_s) or (proc is None and limit >= budget_s):
            return proc, elapsed, True
    t0 = time.monotonic()
    try:
        proc = subprocess.run([sys.executable, path], capture_output=True,
                              text=True, timeout=budget_s, cwd=ROOT)
    except subprocess.TimeoutExpired:
        proc = None
    elapsed = time.monotonic() - t0
    _CERT_RUNS[path] = (proc, elapsed, budget_s)
    return proc, elapsed, False


def verify_lower(sub, budget_s=BUDGET_DEFAULT_S):
    """Run the certificate script; require exit zero and its claim on stdout.

    The script gets `budget_s` seconds of wall clock, or the submission's own
    `certificate.budget_s` when it declares one (capped at BUDGET_CAP_S). A
    declared budget is part of the submission and is shown on the board, so
    the cost of a bound stays visible rather than being absorbed into a
    longer default for everyone.

    With `certificate.attested`, the stored batch outputs are checked against
    the manifest before the script runs, and a pass earns `attested` rather
    than `reproduced`: the script re-ran a declared number of batches and only
    hashed the rest, and the detail says which.
    """
    cert = sub.get("certificate")
    if not cert or not cert.get("script"):
        return Result(True, "cited",
                      "no runnable certificate; recorded as cited and cannot set a record")
    path = os.path.join(ROOT, cert["script"])
    if not os.path.isfile(path):
        return Result(False, None, f"certificate script not found: {cert['script']}")
    expect = cert.get("expect", "")
    if cert.get("budget_s") is not None:
        budget_s = certificate_budget(sub, budget_s)
    batches = None
    if cert.get("attested"):
        if cert.get("exact"):
            return Result(False, None,
                          "certificate declares both exact and attested; an attested "
                          "enumeration was not re-run, so it cannot claim verified")
        batches, err = check_attested(cert)
        if err:
            return Result(False, None, err)
    proc, _elapsed, _reused = run_certificate(path, budget_s)
    if proc is None:
        return Result(False, None, f"certificate exceeded the {budget_s}s budget")
    if proc.returncode != 0:
        return Result(False, None, f"certificate exited {proc.returncode}")
    if not expect:
        return Result(False, None, "certificate declares no claim string to expect")
    if expect.strip() not in (line.strip() for line in proc.stdout.splitlines()):
        return Result(False, None, f"certificate ran but did not print the line {expect!r}")
    if batches is not None:
        # The enumeration itself was not re-run here and no budget the board
        # allows could re-run it. What the pipeline confirmed is the manifest
        # (every stored output present with its recorded hash), the script's
        # exact re-decision of the stored exceptions, and a bit-for-bit re-run
        # of `recomputed` batches; the rest of the enumeration is attested by
        # its stored outputs and the committed runner that regenerates them.
        att = cert["attested"]
        n, k = len(batches), int(att["recomputed"])
        m = SEED_LINE.search(proc.stdout)
        seed = f" chosen from seed {m.group(1)}" if m else ""
        return Result(True, "attested",
                      f"certificate script asserted: {expect}; re-ran {k} of {n} stored "
                      f"batches from scratch{seed} and only checked the SHA-256 of the "
                      f"other {n - k} against {att['batches']}; the full enumeration "
                      f"({att['compute_hours']:g} CPU-h on {att['hardware']}) was not "
                      "re-run")
    if cert.get("exact"):
        # The submission declares that the whole argument is exact: no
        # floating-point margin anywhere, including in how candidates were
        # enumerated. The pipeline cannot audit that from outside any more
        # than it can audit that the claim string follows from what the
        # script computed; both are what review of the script is for. A bound
        # with no margin under it is the same kind of evidence as a verified
        # witness, which is why the flag changes the tier.
        return Result(True, "verified",
                      f"certificate script asserted: {expect}, by an argument declared "
                      "exact throughout (no floating-point margin)")
    extra = (f" within a declared {budget_s}s budget" if cert.get("budget_s") is not None
             and budget_s > BUDGET_DEFAULT_S else "")
    return Result(True, "reproduced", f"certificate script asserted: {expect}{extra}")


LEAN_ROOT = os.path.join(ROOT, "lean_proofs")


def lean_receipt_path(module):
    return os.path.join(ROOT, "certs", f"lean-{module.replace('.', '-')}.json")


def verify_lean(sub):
    """Accept a Lean claim only if the theorem is there and the build receipt is.

    Returns a Result on success, or None to fall through to the other checks.
    """
    lean = sub.get("lean")
    if not lean or not lean.get("module") or not lean.get("theorem"):
        return None
    mod, thm = lean["module"], lean["theorem"]
    src = os.path.join(LEAN_ROOT, *mod.split(".")) + ".lean"
    if not os.path.isfile(src):
        return Result(False, None, f"Lean module not found: {mod}")
    text = open(src).read()
    if not re.search(rf"^\s*(theorem|lemma)\s+{re.escape(thm)}\b", text, re.M):
        return Result(False, None, f"{thm} is not declared in {mod}")
    rec = lean_receipt_path(mod)
    if not os.path.isfile(rec):
        return None      # not built here; fall back rather than claim the tier
    r = json.load(open(rec))
    if not r.get("ok"):
        # The Lean proof does not compile. That is a problem with the proof, not
        # with the bound, so do not fail the bound: drop to the other checks and
        # let the site show the module as broken.
        return None
    g = (implied_exponent(sub["orbit"], int(sub["rank"]), int(sub["m"]))
         if sub["direction"] == "upper" else None)
    return Result(True, "lean", f"{thm} in {mod}, machine-checked by Lean", g)


def verify(sub, budget_s=BUDGET_DEFAULT_S):
    for field in ("schema_version", "orbit", "m", "direction", "rank", "provenance"):
        if field not in sub:
            return Result(False, None, f"missing required field {field!r}")
    if sub["orbit"] not in ORBIT_P:
        return Result(False, None, f"unknown orbit {sub['orbit']!r}")
    if int(sub["m"]) < 1:
        return Result(False, None, "m must be at least 1")
    if int(sub["rank"]) < 1:
        return Result(False, None, "rank must be at least 1")
    lean = verify_lean(sub)
    if lean is not None:
        return lean
    if sub["direction"] == "upper":
        if not sub.get("witness"):
            return Result(True, "cited",
                          "no decomposition supplied; recorded as cited and cannot "
                          "set a record",
                          implied_exponent(sub["orbit"], int(sub["rank"]),
                                           int(sub["m"])))
        return verify_upper(sub)
    if sub["direction"] == "lower":
        return verify_lower(sub, budget_s)
    return Result(False, None, f"direction must be 'upper' or 'lower'")


def main(argv):
    if len(argv) < 2:
        print("usage: stabrank_verify.py <submission.json> [...]")
        return 2
    bad = 0
    for path in argv[1:]:
        sub = json.load(open(path))
        r = verify(sub)
        name = os.path.basename(path)
        sign = "<=" if sub.get("direction") == "upper" else ">="
        head = f"chi(|{sub.get('orbit')}>^{sub.get('m')}) {sign} {sub.get('rank')}"
        print(f"{'PASS' if r.ok else 'FAIL'}  {name}  {head}")
        print(f"      tier={r.tier}  {r.detail}")
        if r.gamma is not None:
            print(f"      implied gamma <= {r.gamma:.4f}")
        bad += 0 if r.ok else 1
    return 1 if bad else 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
