"""Generate a Lean module that proves an upper bound from a stored witness.

Reads a bound file under bounds/ (schema of verify_challenge/stabrank_verify.py)
and writes LeanProofs/<Module>.lean, a proof of `stabRankP p ψ ≤ rank` against
the concrete qudit stabilizer predicate `IsStabP p`, in the reflection style of
LeanProofs/Stabilizer/Reflect.lean:

* every term is entered as `stabTerm p n k x0 W Q l` with its pivot columns,
  so `isStabP_stabTerm` and `affinePtP_injective_of_pivots` give `IsStabP`;
* every coefficient is written as an integer vector `Cj` in a fixed basis of
  the ring the identity lives in, with the `1/√(p^k)` normalisation of the
  term, a common scalar (a power of `sin(π/8)`, `sin β` or `√(3-√3)`, a
  power of the target's rational normalisation, or `(1/√2)^m` for the Strange
  cells) and a common denominator
  `Den` folded in;
* the pointwise identity `Den · target = Σ_j Cj · ζ^(phase_j)` is decided by
  the kernel on the integer vectors over all `p^n` digit strings (`key`),
  and the shared lemmas `ev_termZ`, `<orbit>_eq_ev` carry it to `ℂ`.

The script checks the integer identity itself before writing anything. With
`--bases` it writes LeanProofs/ReflectBases.lean instead: the bases, the
multiplication matrices, and their `Represents` proofs, whose
`linear_combination` cofactors come from polynomial division.

Usage:
    uv run --extra challenge python lean_proofs/tools/gen_witness_lean.py \
        bounds/qubit_H-m5-upper-6.json
    uv run --extra challenge python lean_proofs/tools/gen_witness_lean.py --bases
"""
from __future__ import annotations

import argparse
import json
import os
import sys
from fractions import Fraction

import sympy as sp

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
LEAN_DIR = os.path.join(ROOT, "lean_proofs", "LeanProofs")


# ------------------------------------------------------------- the ring ----
class Ring:
    """ℚ[g_1, …, g_s] modulo one reduction rule per generator.

    A rule `(e, poly)` for generator `g` says `g^e = poly` with `poly` an
    element of lower degree in `g`; elements are dicts from exponent tuples
    (each exponent below its threshold) to rationals.
    """

    def __init__(self, names, rules):
        self.names = list(names)
        self.rules = list(rules)          # list of (threshold, dict)
        self.s = len(names)

    def zero(self):
        return {}

    def const(self, q):
        q = Fraction(q)
        return {tuple([0] * self.s): q} if q else {}

    def gen(self, i, power=1):
        e = [0] * self.s
        e[i] = power
        return self.reduce({tuple(e): Fraction(1)})

    def add(self, a, b):
        out = dict(a)
        for k, v in b.items():
            out[k] = out.get(k, Fraction(0)) + v
            if out[k] == 0:
                del out[k]
        return out

    def scale(self, a, q):
        q = Fraction(q)
        return {k: v * q for k, v in a.items()} if q else {}

    def neg(self, a):
        return self.scale(a, -1)

    def mul(self, a, b):
        out = {}
        for ka, va in a.items():
            for kb, vb in b.items():
                k = tuple(x + y for x, y in zip(ka, kb))
                out[k] = out.get(k, Fraction(0)) + va * vb
        return self.reduce(out)

    def reduce(self, a):
        """Bring every exponent below its threshold using the rules."""
        work = dict(a)
        out = {}
        while work:
            k, v = work.popitem()
            if v == 0:
                continue
            for i, (thr, poly) in enumerate(self.rules):
                if k[i] >= thr:
                    rest = list(k)
                    rest[i] -= thr
                    for kp, vp in poly.items():
                        kk = tuple(x + y for x, y in zip(rest, kp))
                        work[kk] = work.get(kk, Fraction(0)) + v * vp
                    break
            else:
                out[k] = out.get(k, Fraction(0)) + v
        return {k: v for k, v in out.items() if v != 0}

    def pow(self, a, n):
        out = self.const(1)
        for _ in range(n):
            out = self.mul(out, a)
        return out

    def mul_raw(self, a, b):
        """Product without reduction (a polynomial in the generators)."""
        out = {}
        for ka, va in a.items():
            for kb, vb in b.items():
                k = tuple(x + y for x, y in zip(ka, kb))
                out[k] = out.get(k, Fraction(0)) + va * vb
        return {k: v for k, v in out.items() if v != 0}

    def divide(self, a):
        """Write the unreduced polynomial `a` as Σ_g q_g (g^thr_g - poly_g) + rem.

        Returns (quotients, remainder) with one quotient polynomial per
        generator; the remainder is the reduced form of `a`.
        """
        quots = [dict() for _ in range(self.s)]
        work = dict(a)
        rem = {}
        while work:
            k, v = work.popitem()
            if v == 0:
                continue
            for i, (thr, poly) in enumerate(self.rules):
                if k[i] >= thr:
                    rest = list(k)
                    rest[i] -= thr
                    rest = tuple(rest)
                    quots[i][rest] = quots[i].get(rest, Fraction(0)) + v
                    for kp, vp in poly.items():
                        kk = tuple(x + y for x, y in zip(rest, kp))
                        work[kk] = work.get(kk, Fraction(0)) + v * vp
                    break
            else:
                rem[k] = rem.get(k, Fraction(0)) + v
        quots = [{k: v for k, v in q.items() if v != 0} for q in quots]
        return quots, {k: v for k, v in rem.items() if v != 0}

    def eq(self, a, b):
        return self.reduce(self.add(a, self.neg(b))) == {}

    def coords(self, a, basis):
        """Coordinates of `a` in the list `basis` of exponent tuples."""
        a = self.reduce(a)
        idx = {k: i for i, k in enumerate(basis)}
        out = [Fraction(0)] * len(basis)
        for k, v in a.items():
            if k not in idx:
                raise ValueError(f"monomial {k} is outside the basis")
            out[idx[k]] = v
        return out

    def matrix(self, theta, basis):
        """Column j = coordinates of theta * basis[j]."""
        cols = []
        for k in basis:
            b = {k: Fraction(1)}
            cols.append(self.coords(self.mul(theta, b), basis))
        r = len(basis)
        return [[cols[j][i] for j in range(r)] for i in range(r)]


# --------------------------------------------------------- the orbits ------
# Generators, reduction rules, Lean basis, and how the coefficient parser maps
# sympy atoms. Each orbit also fixes the "scalar" s' pulled out of the target,
# so that target = s' * ev(tgt) with tgt an integer vector computed in Lean.

def make_orbit(orbit, m):
    if orbit in ("qubit_H", "qubit_T"):
        # generators: s2, s3, i, th   (th = sin(pi/8) or sin(beta))
        names = ["s2", "s3", "i", "th"]
        if orbit == "qubit_H":
            th_sq = {(0, 0, 0, 0): Fraction(1, 2), (1, 0, 0, 0): Fraction(-1, 4)}
        else:
            th_sq = {(0, 0, 0, 0): Fraction(1, 2), (0, 1, 0, 0): Fraction(-1, 6)}
        R = Ring(names, [(2, {(0, 0, 0, 0): Fraction(2)}),
                         (2, {(0, 0, 0, 0): Fraction(3)}),
                         (2, {(0, 0, 0, 0): Fraction(-1)}),
                         (2, th_sq)])
        s2, s3, i, th = (R.gen(k) for k in range(4))
        if orbit == "qubit_H":
            basis = [(0, 0, 0, 0), (1, 0, 0, 0), (0, 0, 1, 0), (1, 0, 1, 0)]
            lean = dict(module_prefix="QubitH", shared="ReflectQubit", basis="B4",
                        zeta_mat="MI4", zeta_rep="MI4_represents", target="hVec",
                        target_ev="hVec_eq_ev", tgt="tgtH", dim=4, theorem_stem="qubit_h")
        else:
            basis = [(a, b, c, 0) for c in (0, 1) for b in (0, 1) for a in (0, 1)]
            lean = dict(module_prefix="QubitT", shared="ReflectQubit", basis="B8",
                        zeta_mat="MI8", zeta_rep="MI8_represents", target="tVec",
                        target_ev="tVec_eq_ev", tgt="tgtT", dim=8, theorem_stem="qubit_t")
        p, zeta = 2, i
        sqrt_p = s2
        # target amplitude at a digit string with a zeros:
        #   H: cos^a sin^(m-a) = th^(m%2) / 4^(m/2) * (1+s2)^a (2-s2)^(m/2)
        #   T: cT^a (e^{i pi/4} sT)^(m-a)
        #      = th^(m%2) / (2^m 6^(m/2)) * (s2 s3 + s2)^a (s2 + i s2)^(m-a) (3 - s3)^(m/2)
        h = m // 2
        if orbit == "qubit_H":
            scalar_rat = Fraction(1, 4 ** h)
            def tgt(a):
                return R.mul(R.pow(R.add(R.const(1), s2), a),
                             R.pow(R.add(R.const(2), R.neg(s2)), h))
        else:
            scalar_rat = Fraction(1, 2 ** m * 6 ** h)
            def tgt(a):
                return R.mul(R.mul(R.pow(R.add(R.mul(s2, s3), s2), a),
                                   R.pow(R.add(s2, R.mul(i, s2)), m - a)),
                             R.pow(R.add(R.const(3), R.neg(s3)), h))
        th_pow = m % 2
        atoms = {"sqrt2": s2, "sqrt3": s3, "I": i}
        quad = ("s2", 0, 2) if orbit == "qubit_H" else ("s3", 1, 3)
        return dict(R=R, p=p, zeta=zeta, sqrt_p=sqrt_p, basis=basis, lean=lean,
                    tgt=tgt, scalar_rat=scalar_rat, th=th, th_pow=th_pow, atoms=atoms,
                    quad=quad, stat="count0")
    if orbit == "H3":
        # generators: w (omega_3), s3, th (= N = sqrt(3 - sqrt 3)), s2
        names = ["w", "s3", "th", "s2"]
        R = Ring(names, [(2, {(0, 0, 0, 0): Fraction(-1), (1, 0, 0, 0): Fraction(-1)}),
                         (2, {(0, 0, 0, 0): Fraction(3)}),
                         (2, {(0, 0, 0, 0): Fraction(3), (0, 1, 0, 0): Fraction(-1)}),
                         (2, {(0, 0, 0, 0): Fraction(2)})])
        w, s3, th, s2 = (R.gen(k) for k in range(4))
        basis = [(0, 0, 0, 0), (1, 0, 0, 0), (0, 1, 0, 0), (1, 1, 0, 0)]
        lean = dict(module_prefix="H3", shared="ReflectQutrit", basis="B3",
                    zeta_mat="Mw3", zeta_rep="Mw3_represents", target="h3Vec",
                    target_ev="h3Vec_eq_ev", tgt="tgtH3", dim=4, theorem_stem="h3")
        h = m // 2
        # amplitude with a zeros: (N(3+s3)/6)^a (N s3/6)^(m-a)
        #   = th^(m%2) / 6^m * (3+s3)^a s3^(m-a) (3-s3)^(m/2)
        scalar_rat = Fraction(1, 6 ** m)
        def tgt(a):
            return R.mul(R.mul(R.pow(R.add(R.const(3), s3), a), R.pow(s3, m - a)),
                         R.pow(R.add(R.const(3), R.neg(s3)), h))
        # i = (2w + 1)/sqrt3 = (2w+1) s3 / 3
        i_elt = R.scale(R.mul(R.add(R.scale(w, 2), R.const(1)), s3), Fraction(1, 3))
        atoms = {"sqrt2": s2, "sqrt3": s3, "I": i_elt}
        return dict(R=R, p=3, zeta=w, sqrt_p=s3, basis=basis, lean=lean, tgt=tgt,
                    scalar_rat=scalar_rat, th=th, th_pow=m % 2, atoms=atoms,
                    quad=("s3", 1, 3), stat="count0")
    if orbit == "T3":
        # generators: w (omega_9), s3
        names = ["w", "s3"]
        R = Ring(names, [(6, {(0, 0): Fraction(-1), (3, 0): Fraction(-1)}),
                         (2, {(0, 0): Fraction(3)})])
        w, s3 = R.gen(0), R.gen(1)
        basis = [(t, e) for e in (0, 1) for t in range(6)]
        lean = dict(module_prefix="T3", shared="ReflectQutrit", basis="B9",
                    zeta_mat="Mw9c", zeta_rep="Mw9c_represents", target="t3TargetM",
                    target_ev="t3TargetM_eq_ev", tgt="tgtT3", dim=12, theorem_stem="t3")
        # amplitude at digit sum d: (1/sqrt3)^m w^d; the scalar is (1/sqrt3)^m
        # = (s3/3)^m, whose inverse in the ring is s3^m
        def tgt(d):
            return R.pow(w, d)
        i_elt = R.scale(R.mul(R.add(R.scale(R.pow(w, 3), 2), R.const(1)), s3), Fraction(1, 3))
        atoms = {"sqrt3": s3, "I": i_elt}
        return dict(R=R, p=3, zeta=R.pow(w, 3), sqrt_p=s3, basis=basis, lean=lean,
                    tgt=tgt, scalar_inv=R.pow(s3, m), th=None, th_pow=0, atoms=atoms,
                    quad=None, stat="digitSum", w9=w)
    if orbit == "S":
        # generators: w (omega_3), s2, s3. The coefficients of the Strange cells
        # are read in ℚ(ω₃, √2, √3) and land in ℤ[ω₃] once the √3^k term
        # normalisation and the √2^m of the target are folded in; the Lean
        # basis is B3 of the H₃ cells with zero √3 coordinates.
        names = ["w", "s2", "s3"]
        R = Ring(names, [(2, {(0, 0, 0): Fraction(-1), (1, 0, 0): Fraction(-1)}),
                         (2, {(0, 0, 0): Fraction(2)}),
                         (2, {(0, 0, 0): Fraction(3)})])
        w, s2, s3 = (R.gen(k) for k in range(3))
        basis = [(0, 0, 0), (1, 0, 0), (0, 0, 1), (1, 0, 1)]
        lean = dict(module_prefix="Strange", shared="ReflectQutrit", basis="B3",
                    zeta_mat="Mw3", zeta_rep="Mw3_represents", target="strangeVec",
                    target_ev="strangeVec_eq_ev", tgt="tgtS", dim=4, theorem_stem="strange")
        # amplitude at a digit string: (1/sqrt2)^m times the product of the
        # digit signs (0, 1, -1 at 0, 1, 2); the scalar's inverse is s2^m
        def tgt(x):
            sgn = 1
            for d in x:
                sgn *= {0: 0, 1: 1, 2: -1}[d]
            return R.const(sgn)
        i_elt = R.scale(R.mul(R.add(R.scale(w, 2), R.const(1)), s3), Fraction(1, 3))
        atoms = {"sqrt2": s2, "sqrt3": s3, "I": i_elt}
        return dict(R=R, p=3, zeta=w, sqrt_p=s3, basis=basis, lean=lean, tgt=tgt,
                    scalar_inv=R.pow(s2, m), th=None, th_pow=0, atoms=atoms,
                    quad=None, stat="digits")
    if orbit == "N":
        # generators: w (omega_3), s2, s3. The coefficients of the Norrell cells
        # are read in ℚ(ω₃, √2, √3) and land in ℤ[ω₃, √3] once the √3^k term
        # normalisation and the (√2 √3 / 6)^m of the target are folded in.
        names = ["w", "s2", "s3"]
        R = Ring(names, [(2, {(0, 0, 0): Fraction(-1), (1, 0, 0): Fraction(-1)}),
                         (2, {(0, 0, 0): Fraction(2)}),
                         (2, {(0, 0, 0): Fraction(3)})])
        w, s2, s3 = (R.gen(k) for k in range(3))
        basis = [(0, 0, 0), (1, 0, 0), (0, 0, 1), (1, 0, 1)]
        lean = dict(module_prefix="Norrell", shared="ReflectQutrit", basis="B3",
                    zeta_mat="Mw3", zeta_rep="Mw3_represents", target="norrellVec",
                    target_ev="norrellVec_eq_ev", tgt="tgtN", dim=4, theorem_stem="norrell")
        # amplitude at a digit string: (sqrt2 * sqrt3 / 6)^m times the product
        # of the digit factors (1, 1, -2 at 0, 1, 2); the scalar's inverse in R
        # is (s2 * s3)^m since (s2 * s3 / 6) * (s2 * s3) = 1.
        def tgt(x):
            fac = 1
            for d in x:
                fac *= {0: 1, 1: 1, 2: -2}[d]
            return R.const(fac)
        i_elt = R.scale(R.mul(R.add(R.scale(w, 2), R.const(1)), s3), Fraction(1, 3))
        atoms = {"sqrt2": s2, "sqrt3": s3, "I": i_elt}
        return dict(R=R, p=3, zeta=w, sqrt_p=s3, basis=basis, lean=lean, tgt=tgt,
                    scalar_inv=R.pow(R.mul(s2, s3), m), th=None, th_pow=0, atoms=atoms,
                    quad=None, stat="digits")
    raise ValueError(f"unsupported orbit {orbit!r}")


# ------------------------------------------------- coefficient parsing -----
def sqrt_rational(q):
    """√q for a rational q ≥ 0 as (rational, e2, e3) with q = rational² 2^e2 3^e3."""
    q = Fraction(q)
    if q < 0:
        return None
    if q == 0:
        return Fraction(0), 0, 0
    num, den = q.numerator, q.denominator
    out_n, out_d, e2, e3 = 1, 1, 0, 0
    for prime, ee in ((2, "e2"), (3, "e3")):
        while num % (prime * prime) == 0:
            num //= prime * prime
            out_n *= prime
        while den % (prime * prime) == 0:
            den //= prime * prime
            out_d *= prime
        if num % prime == 0:
            num //= prime
            if ee == "e2":
                e2 += 1
            else:
                e3 += 1
        if den % prime == 0:
            den //= prime
            out_d *= prime
            if ee == "e2":
                e2 += 1
            else:
                e3 += 1
    r = sp.Integer(num) / sp.Integer(den)
    s = sp.sqrt(r)
    if not s.is_Rational:
        return None
    return Fraction(out_n, out_d) * Fraction(int(s.p), int(s.q)), e2, e3


class CoeffParser:
    def __init__(self, orb):
        self.orb = orb
        self.R = orb["R"]

    def const_sqrt(self, q):
        r = sqrt_rational(q)
        if r is None:
            return None
        c, e2, e3 = r
        R, names = self.R, self.R.names
        out = R.const(c)
        if e2:
            if "s2" not in names:
                return None
            out = R.mul(out, R.gen(names.index("s2")))
        if e3:
            if "s3" not in names:
                return None
            out = R.mul(out, R.gen(names.index("s3")))
        return out

    def quad_parts(self, elt):
        """Write an element of ℚ(√d) as (a, b) with elt = a + b √d, or None."""
        name, gi, d = self.orb["quad"]
        R = self.R
        a = b = Fraction(0)
        for k, v in elt.items():
            if any(k[j] for j in range(R.s) if j != gi):
                return None
            if k[gi] == 0:
                a += v
            elif k[gi] == 1:
                b += v
            else:
                return None
        return a, b

    def sqrt_quadratic(self, elt, numeric):
        """√elt inside ℚ(√d), choosing the root whose value is `numeric`."""
        parts = self.quad_parts(elt)
        if parts is None:
            return None
        a, b = parts
        name, gi, d = self.orb["quad"]
        R = self.R
        sd = R.gen(gi)
        if b == 0:
            return self.const_sqrt(a)
        disc = a * a - d * b * b
        r = sqrt_rational(disc)
        if r is None or r[1] or r[2]:
            return None
        rd = r[0]
        for sign in (1, -1):
            u2 = (a + sign * rd) / 2
            if u2 <= 0:
                continue
            # u = c 2^(e2/2) 3^(e3/2); the root may leave ℚ(√d) for the
            # biquadratic field, which is why u⁻¹ is built from the generators
            u = self.const_sqrt(u2)
            if u is None:
                continue
            ru = sqrt_rational(u2)
            c, e2, e3 = ru
            inv = R.const(Fraction(1) / c)
            if e2:
                inv = R.mul(inv, R.scale(R.gen(R.names.index("s2")), Fraction(1, 2)))
            if e3:
                inv = R.mul(inv, R.scale(R.gen(R.names.index("s3")), Fraction(1, 3)))
            v = R.scale(inv, b / 2)
            cand = R.add(u, R.mul(sd, v))
            for s in (1, -1):
                cc = R.scale(cand, s)
                if abs(complex(self.numeric(cc)) - complex(numeric)) < 1e-30:
                    return cc
        return None

    def numeric(self, elt):
        """High-precision complex value of a ring element."""
        R = self.R
        vals = []
        for n in R.names:
            if n == "s2":
                vals.append(sp.sqrt(2))
            elif n == "s3":
                vals.append(sp.sqrt(3))
            elif n == "i":
                vals.append(sp.I)
            elif n == "w":
                vals.append(sp.exp(2 * sp.pi * sp.I / (9 if self.orb["lean"]["module_prefix"] == "T3" else 3)))
            elif n == "th":
                if self.orb["lean"]["module_prefix"] == "QubitH":
                    vals.append(sp.sin(sp.pi / 8))
                elif self.orb["lean"]["module_prefix"] == "QubitT":
                    vals.append(sp.sin(sp.acos(1 / sp.sqrt(3)) / 2))
                else:
                    vals.append(sp.sqrt(3 - sp.sqrt(3)))
        total = sp.Integer(0)
        for k, v in elt.items():
            term = sp.Rational(v.numerator, v.denominator)
            for e, val in zip(k, vals):
                term *= val ** e
            total += term
        return sp.N(total, 50)

    def parse(self, expr):
        R = self.R
        expr = sp.sympify(expr)
        if expr.is_Rational:
            return R.const(Fraction(int(expr.p), int(expr.q)))
        if expr == sp.I:
            return self.orb["atoms"]["I"]
        if expr.is_Add:
            out = R.zero()
            for t in expr.args:
                out = R.add(out, self.parse(t))
            return out
        if expr.is_Mul:
            out = R.const(1)
            for t in expr.args:
                out = R.mul(out, self.parse(t))
            return out
        if expr.is_Pow:
            base, ex = expr.args
            if ex.is_Integer and int(ex) > 0:
                return R.pow(self.parse(base), int(ex))
            if ex.is_Integer and int(ex) < 0:
                # only 1/sqrt(k) style shows up; handle rational bases
                if base.is_Rational:
                    return R.const(Fraction(1) / Fraction(int(base.p), int(base.q)) ** (-int(ex)))
                raise ValueError(f"negative power of {base}")
            if ex == sp.Rational(1, 2):
                if base.is_Rational:
                    c = self.const_sqrt(Fraction(int(base.p), int(base.q)))
                    if c is None:
                        raise ValueError(f"cannot take sqrt of {base}")
                    return c
                rad = self.parse(base)
                # sqrt of an element of the quadratic subfield
                target = sp.N(sp.sqrt(base), 50)
                r = self.sqrt_quadratic(rad, target)
                if r is not None:
                    return r
                # divide by th^2 and retry
                if self.orb["th"] is not None:
                    th2 = R.mul(self.orb["th"], self.orb["th"])
                    inv = self.invert_quadratic(th2)
                    r = self.sqrt_quadratic(R.mul(rad, inv), target / self.numeric(self.orb["th"]))
                    if r is not None:
                        return R.mul(r, self.orb["th"])
                    if "I" in self.orb["atoms"]:
                        r = self.sqrt_quadratic(R.neg(R.mul(rad, inv)),
                                                target / (sp.I * self.numeric(self.orb["th"])))
                        if r is not None:
                            return R.mul(self.orb["atoms"]["I"], R.mul(r, self.orb["th"]))
                if "I" in self.orb["atoms"]:
                    r = self.sqrt_quadratic(R.neg(rad), target / sp.I)
                    if r is not None:
                        return R.mul(self.orb["atoms"]["I"], r)
                raise ValueError(f"cannot recognise sqrt({base})")
            raise ValueError(f"unsupported power {expr}")
        if isinstance(expr, sp.exp):
            arg = sp.simplify(expr.args[0] / (sp.I * sp.pi))
            if not arg.is_Rational:
                raise ValueError(f"exp argument {expr.args[0]} is not a rational multiple of i pi")
            k = arg * 9 / 2
            if not k.is_Integer:
                raise ValueError(f"exp argument {expr.args[0]} is not a ninth root of unity")
            return R.pow(self.orb["w9"], int(k) % 9)
        raise ValueError(f"unsupported expression {expr!r}")

    def invert_quadratic(self, elt):
        parts = self.quad_parts(elt)
        if parts is None:
            raise ValueError("not in the quadratic subfield")
        a, b = parts
        name, gi, d = self.orb["quad"]
        R = self.R
        nrm = a * a - d * b * b
        return R.scale(R.add(R.const(a), R.scale(R.gen(gi), -b)), Fraction(1) / nrm)


# ------------------------------------------------------ the witness --------
def pivots(W, k, n):
    piv = []
    for j in range(k):
        found = None
        for c in range(n):
            if W[j][c] == 1 and all(W[jj][c] == 0 for jj in range(k) if jj != j):
                found = c
                break
        if found is None:
            return None
        piv.append(found)
    return piv


def upper(Q, k, p):
    return [[Q[i][j] % p if i <= j else 0 for j in range(k)] for i in range(k)]


def digits(idx, p, n):
    """Digit string of an index, digit i = idx / p^i mod p (as in `digitsP`)."""
    return [(idx // p ** i) % p for i in range(n)]


def term_value_Z(orb, term, C, x):
    """The integer vector `termZ` at digit string x, following Reflect.lean."""
    R = orb["R"]
    p = orb["p"]
    k, x0, W, Q, l, piv = term["k"], term["x0"], term["W"], term["Q"], term["l"], term["piv"]
    n = len(x0)
    y = [(x[piv[j]] - x0[piv[j]]) % p for j in range(k)]
    img = [(x0[c] + sum(y[r] * W[r][c] for r in range(k))) % p for c in range(n)]
    if img != list(x):
        return R.zero()
    D = 4 if p == 2 else p
    phase = (D // p) * sum(Q[i][j] * y[i] * y[j] for i in range(k) for j in range(k)) \
        + sum(l[i] * y[i] for i in range(k))
    return R.mul(C, R.pow(orb["zeta"], phase % D))


def lean_vec(vals):
    return "![" + ", ".join(str(v) for v in vals) + "]"


def lean_mat(rows):
    return "![" + ", ".join(lean_vec(r) for r in rows) + "]"


def lean_int(q):
    q = Fraction(q)
    if q.denominator != 1:
        raise ValueError("non-integral coordinate")
    return str(q.numerator) if q >= 0 else f"({q.numerator})"


WORDS = {2: "two", 3: "three", 4: "four", 5: "five", 6: "six", 7: "seven", 8: "eight",
         9: "nine", 10: "ten", 12: "twelve", 15: "fifteen", 16: "sixteen", 18: "eighteen",
         27: "twentyseven"}


def generate(path, check_only=False, chunks=1):
    sub = json.load(open(path))
    orbit, m, rank = sub["orbit"], int(sub["m"]), int(sub["rank"])
    assert sub["direction"] == "upper"
    orb = make_orbit(orbit, m)
    R, p = orb["R"], orb["p"]
    parser = CoeffParser(orb)
    L = orb["lean"]
    terms_in = sub["witness"]["terms"]
    coeffs_in = sub["witness"]["coeffs"]
    n = m
    D = 4 if p == 2 else p

    terms = []
    for t in terms_in:
        k = int(t["k"])
        x0 = [int(a) % p for a in t["x0"]]
        W = [[int(a) % p for a in row] for row in t.get("W", [])]
        Q = upper([[int(a) for a in row] for row in t.get("Q", [[0] * k] * k)], k, p)
        l = [int(a) % D for a in t.get("l", [0] * k)]
        piv = pivots(W, k, n)
        if piv is None:
            raise SystemExit(f"term {len(terms)} of {path}: no pivot columns; re-parametrise it")
        terms.append(dict(k=k, x0=x0, W=W, Q=Q, l=l, piv=piv))

    # coefficient vectors: C_j = Den * c_j / sqrt(p)^k_j / (th^th_pow * scalar_rat)
    inv_sqrt_p = R.scale(orb["sqrt_p"], Fraction(1, p))     # 1/sqrt p = sqrt p / p
    if "scalar_inv" in orb:
        scalar_inv = orb["scalar_inv"]
    else:
        scalar_inv = R.const(Fraction(1) / orb["scalar_rat"])
        if orb["th_pow"]:
            # divide by th: multiply by th / th^2
            th = orb["th"]
            th2 = R.mul(th, th)
            scalar_inv = R.mul(scalar_inv, R.mul(th, parser.invert_quadratic(th2)))
    raw = []
    for j, (t, c) in enumerate(zip(terms, coeffs_in)):
        e = parser.parse(c)
        e = R.mul(e, R.pow(inv_sqrt_p, t["k"]))
        e = R.mul(e, scalar_inv)
        if orb["th"] is not None:
            ti = R.names.index("th")
            if any(k[ti] for k in e):
                raise SystemExit(f"coefficient {j} of {path} is not th^{orb['th_pow']} times an "
                                 f"element of the basis ring: {c}")
        raw.append(e)
    den = 1
    for e in raw:
        for v in e.values():
            den = den * v.denominator // sp.gcd(den, v.denominator)
    den = int(den)
    Cs = [R.coords(R.scale(e, den), orb["basis"]) for e in raw]

    # the integer identity, exactly, at every digit string
    N = p ** n
    for idx in range(N):
        x = digits(idx, p, n)
        if orb["stat"] == "count0":
            tgt = orb["tgt"](sum(1 for d in x if d == 0))
        elif orb["stat"] == "digitSum":
            tgt = orb["tgt"](sum(x))
        else:
            tgt = orb["tgt"](x)
        lhs = R.scale(tgt, den)
        rhs = R.zero()
        for t, C in zip(terms, raw):
            rhs = R.add(rhs, term_value_Z(orb, t, R.scale(C, den), x))
        if not R.eq(lhs, rhs):
            raise SystemExit(f"{path}: integer identity fails at index {idx} (digits {x})")
    print(f"{os.path.basename(path)}: integer identity holds at all {N} indices; Den = {den}")
    if check_only:
        return None

    # ------------------------------------------------------------ emit ----
    stem = L["theorem_stem"]
    module = f"{L['module_prefix']}M{m}StabRank"
    ns = f"{L['module_prefix']}M{m}"
    word = WORDS.get(rank, str(rank))
    thm = f"{stem}_m{m}_stabRankP_le_{word}"
    dim = L["dim"]
    zn = f"ZMod {p}"
    zl = f"ZMod (stabPeriod {p})"
    basis, zmat, zrep = L["basis"], L["zeta_mat"], L["zeta_rep"]
    target_expr = f"{L['target']} {m}"
    fin_n = f"Fin ({p} ^ {n})"

    def tgt_of(idx_expr):
        if orb["stat"] == "digitSum":
            return f"{L['tgt']} {m} {idx_expr}"
        return f"{L['tgt']} {m} (digitsP {p} {n} {idx_expr})"

    def ident(idx_expr):
        return f"Den • {tgt_of(idx_expr)} = rhsZ (digitsP {p} {n} {idx_expr})"

    def header(title, imports):
        out = ["/-"] + title + ["-/"] + [f"import {i}" for i in imports]
        out += ["", "set_option linter.style.longLine false", "", "namespace StabRank", "",
                "open Stabilizer", "", f"namespace {ns}", ""]
        return out

    common_doc = [
        f"`χ(|{orbit}⟩^⊗{m}) ≤ {rank}` against `stabRankP {p}`, from the witness of",
        f"`bounds/{os.path.basename(path)}`.",
        "",
        "Generated by `lean_proofs/tools/gen_witness_lean.py`; do not edit by hand. The",
        f"terms are the file's, entered as `stabTerm {p} {n} k x0 W Q l` with the pivot",
        "columns of `W` (`Q` is read as an upper-triangular form, as the verifier reads",
        f"it). Each coefficient is the integer vector `Cj` in the basis `{basis}` of",
        f"`LeanProofs/{L['shared']}.lean`: the file's coefficient, divided by the",
        f"`√{p}^k` normalisation of its term and by the common scalar in front of the",
        f"target (`{L['target_ev']}`), times `Den = {den}`. The pointwise identity is",
        f"decided by the kernel on integer vectors at all {N} digit strings (`key`) and",
        "carried to `ℂ` by `ev_termZ`.",
    ]
    if chunks > 1:
        common_doc += [
            "",
            f"The kernel check is split into {chunks} slices of {N // chunks} indices, one",
            f"module `{ns}Key<q>` each, on the data of `{ns}Data`; `forall_fin_of_chunks`",
            "of `Stabilizer/Chunks.lean` puts them together here.",
        ]

    # the data: scalar, terms, coefficient vectors, Den, rhsZ
    data = [orb_scalar_lean(orbit, m), ""]
    for j, t in enumerate(terms):
        k = t["k"]
        data.append(f"def x0_{j} : Fin {n} → {zn} := {lean_vec(t['x0'])}")
        data.append(f"def W{j} : Fin {k} → Fin {n} → {zn} := {lean_mat(t['W']) if k else '![]'}")
        data.append(f"def Q{j} : Fin {k} → Fin {k} → {zn} := {lean_mat(t['Q']) if k else '![]'}")
        data.append(f"def l{j} : Fin {k} → {zl} := {lean_vec(t['l']) if k else '![]'}")
        data.append(f"def piv{j} : Fin {k} → Fin {n} := {lean_vec(t['piv']) if k else '![]'}")
        data.append(f"theorem piv{j}_ok : ∀ j j', W{j} j (piv{j} j') = if j = j' then 1 else 0 := by")
        data.append("  decide +kernel")
        data.append(f"noncomputable def t{j} : {fin_n} → ℂ := stabTerm {p} {n} {k} x0_{j} W{j} Q{j} l{j}")
        data.append(f"theorem t{j}_isStab : IsStabP {p} t{j} :=")
        data.append(f"  isStabP_stabTerm {p} {n} {k} _ _ _ _ (affinePtP_injective_of_pivots _ _ piv{j} piv{j}_ok)")
        data.append(f"def C{j} : Fin {dim} → ℤ := {lean_vec(lean_int(q) for q in Cs[j])}")
        data.append("")
    data.append(f"def Den : ℤ := {den}")
    data.append("")
    data.append("/-- The integer side of `Σ_j C_j · σ_j` at a digit string. -/")
    data.append(f"def rhsZ (x : Fin {n} → {zn}) : Fin {dim} → ℤ :=")
    parts = [f"termZ {zmat} C{j} x0_{j} W{j} Q{j} l{j} piv{j} x" for j in range(len(terms))]
    data.append("  " + "\n    + ".join(parts))
    data.append("")
    if chunks > 1:
        data.append(f"/-- The index `q * {N // chunks} + i` of slice `q`. -/")
        data.append(f"def cidx (q : Fin {chunks}) (i : Fin {N // chunks}) : {fin_n} := chunkIdx (c := {chunks}) (N := {N // chunks}) q i")
        data.append("")

    # the kernel check
    key = []
    if chunks == 1:
        key.append("set_option maxRecDepth 100000 in")
        key.append("set_option maxHeartbeats 0 in")
        key.append("/-- The identity on integer vectors, decided by the kernel at every index. -/")
        key.append(f"theorem key : ∀ idx : {fin_n}, {ident('idx')} := by")
        key.append("  decide +kernel")
        key.append("")
    else:
        key.append("/-- The identity on integer vectors at every index, from the slices. -/")
        key.append(f"theorem key : ∀ idx : {fin_n}, {ident('idx')} :=")
        key.append(f"  forall_fin_of_chunks (c := {chunks}) (N := {N // chunks}) _ (fun q => by")
        key.append("    fin_cases q")
        key.append("    exacts [" + ", ".join(f"key{q}" for q in range(chunks)) + "])")
        key.append("")

    # the assembly
    coef = f"scalar / {den} * ev {basis} (Cs j)" if den != 1 else f"scalar * ev {basis} (Cs j)"
    asm = []
    asm.append(f"noncomputable def terms : Fin {rank} → ({fin_n} → ℂ) :=")
    asm.append("  " + lean_vec(f"t{j}" for j in range(rank)))
    asm.append(f"def Cs : Fin {rank} → Fin {dim} → ℤ := {lean_vec(f'C{j}' for j in range(rank))}")
    asm.append("")
    asm.append("theorem terms_isStab : ∀ j, IsStabP " + str(p) + " (terms j) := by")
    asm.append("  intro j")
    asm.append("  fin_cases j")
    asm.append("  exacts [" + ", ".join(f"t{j}_isStab" for j in range(rank)) + "]")
    asm.append("")
    asm.append("set_option linter.unusedSimpArgs false in")
    asm.append(f"theorem target_eq : {target_expr} = ∑ j, ({coef}) • terms j := by")
    asm.append("  funext idx")
    asm.append("  have hk := congrArg (ev " + basis + ") (key idx)")
    asm.append("  rw [ev_zsmul] at hk")
    asm.append("  simp only [rhsZ, ev_add, Den, Int.cast_one, Int.cast_ofNat, one_mul, "
               + ", ".join(f"ev_termZ {basis} {zrep} piv{j}_ok" for j in range(rank)) + "] at hk")
    asm.append(f"  have ht : {target_expr} idx = scalar * ev {basis} ({tgt_of('idx')}) := by")
    asm.append(f"    have h := {L['target_ev']} {m} idx")
    asm.append("    try simp only [Nat.reduceMod, Nat.reduceDiv, pow_zero, pow_one] at h")
    asm.append("    unfold scalar")
    asm.append("    linear_combination h")
    asm.append("  rw [Finset.sum_apply, ht]")
    asm.append("  simp only [Pi.smul_apply, smul_eq_mul, Fin.sum_univ_succ, Fin.sum_univ_zero, Matrix.cons_val_zero,")
    asm.append("    Matrix.cons_val_succ, add_zero, terms, Cs, " + ", ".join(f"t{j}" for j in range(rank)) + ", stabTerm]")
    asm.append(f"  linear_combination (scalar / {den}) * hk" if den != 1 else "  linear_combination scalar * hk")
    asm.append("")
    asm.append(f"end {ns}")
    asm.append("")
    asm.append(f"/-- **χ(|{orbit}⟩^⊗{m}) ≤ {rank} against `IsStabP {p}`.** -/")
    asm.append(f"theorem {thm} : stabRankP {p} ({target_expr}) ≤ {rank} :=")
    asm.append(f"  stabRankP_le_of_terms {p} {ns}.terms _ {ns}.terms_isStab {ns}.target_eq")
    if p == 3:
        asm.append("")
        asm.append("/-- The same bound against the qutrit predicate `IsStab`. -/")
        asm.append(f"theorem {stem}_m{m}_stabRank_le_{word} : Stabilizer.stabRank (IsStab (n := {m})) ({target_expr}) ≤ {rank} := by")
        asm.append("  rw [stabRank_eq_stabRankP]")
        asm.append(f"  exact {thm}")
    asm.append("")
    asm.append("end StabRank")

    written = []

    def write(name, lines):
        out_path = os.path.join(LEAN_DIR, name + ".lean")
        with open(out_path, "w") as f:
            f.write("\n".join(lines) + "\n")
        written.append(os.path.relpath(out_path, ROOT))

    if chunks == 1:
        write(module, header(common_doc, [f"LeanProofs.{L['shared']}"]) + data + key + asm)
    else:
        data_doc = [f"The data of `{module}`: the terms, coefficient vectors and integer side of",
                    f"the witness of `bounds/{os.path.basename(path)}`. Generated by",
                    "`lean_proofs/tools/gen_witness_lean.py`; do not edit by hand."]
        write(f"{ns}Data", header(data_doc, [f"LeanProofs.{L['shared']}",
                                             "LeanProofs.Stabilizer.Chunks"]) + data
              + [f"end {ns}", "", "end StabRank"])
        for q in range(chunks):
            kdoc = [f"Slice {q} of {chunks} of the kernel check of `{module}`: the identity at",
                    f"the indices `q * {N // chunks} + i`. Generated by",
                    "`lean_proofs/tools/gen_witness_lean.py`; do not edit by hand."]
            body = ["set_option maxRecDepth 100000 in", "set_option maxHeartbeats 0 in",
                    f"theorem key{q} : ∀ i : Fin {N // chunks}, {ident(f'(cidx ⟨{q}, by norm_num⟩ i)')} := by",
                    "  decide +kernel", "", f"end {ns}", "", "end StabRank"]
            write(f"{ns}Key{q}", header(kdoc, [f"LeanProofs.{ns}Data"]) + body)
        write(module, header(common_doc, [f"LeanProofs.{ns}Key{q}" for q in range(chunks)])
              + key + asm)
    for w in written:
        print(f"wrote {w}")
    print(f"module LeanProofs.{module}, theorem {thm}")
    return dict(module=f"LeanProofs.{module}", theorem=thm)

def update_bound(path, module, theorem):
    """Record the Lean proof in the bound file: the `lean` field and a note."""
    sub = json.load(open(path))
    p = ORBIT_P_LOCAL[sub["orbit"]]
    sentence = (f" Now at the lean tier: {theorem} in {module} proves stabRankP {p} "
                f"|{sub['orbit']}>^{sub['m']} <= {sub['rank']} against IsStabP {p} from this "
                "witness, the pointwise identity being decided by the kernel on integer "
                "coordinate vectors (see lean_proofs/LeanProofs/Stabilizer/Reflect.lean).")
    if module not in sub.get("notes", ""):
        sub["notes"] = sub.get("notes", "").rstrip() + sentence
    out = {}
    for k, v in sub.items():
        if k == "witness":
            out["lean"] = {"module": module, "theorem": theorem}
        if k != "lean":
            out[k] = v
    if "lean" not in out:
        out["lean"] = {"module": module, "theorem": theorem}
    with open(path, "w") as f:
        json.dump(out, f, indent=2, ensure_ascii=False)
        f.write("\n")
    print(f"updated {os.path.relpath(path, ROOT)}")


ORBIT_P_LOCAL = {"H3": 3, "T3": 3, "S": 3, "N": 3, "qubit_H": 2, "qubit_T": 2}


def orb_scalar_lean(orbit, m):
    """The common scalar s' with target = s' * ev(tgt), matching <orbit>_eq_ev
    after `Nat.reduceMod`, `Nat.reduceDiv`, `pow_zero`, `pow_one`."""
    h, e = m // 2, m % 2
    if orbit == "qubit_H":
        th = "(sH : ℂ)" if e else None
        body = f"{th} / 4 ^ {h}" if th else f"1 / 4 ^ {h}"
    elif orbit == "qubit_T":
        th = "(sT : ℂ)" if e else None
        body = f"{th} / (2 ^ {m} * 6 ^ {h})" if th else f"1 / (2 ^ {m} * 6 ^ {h})"
    elif orbit == "H3":
        th = "NH3C" if e else None
        body = f"{th} / 6 ^ {m}" if th else f"1 / 6 ^ {m}"
    elif orbit == "T3":
        body = f"((1 / Real.sqrt 3 : ℝ) : ℂ) ^ {m}"
    elif orbit == "S":
        body = f"(1 / (Real.sqrt 2 : ℂ)) ^ {m}"
    elif orbit == "N":
        body = f"((Real.sqrt 2 : ℂ) * (Real.sqrt 3 : ℂ) / 6) ^ {m}"
    else:
        raise ValueError(orbit)
    return f"/-- The scalar in front of the target in `{orbit}` at `m = {m}`. -/\nnoncomputable def scalar : ℂ := {body}"


# ----------------------------------------------------- the bases module ----
LEAN_ATOM = {"s2": "(Real.sqrt 2 : ℂ)", "s3": "(Real.sqrt 3 : ℂ)", "i": "Complex.I",
             "w3": "omega3", "w9": "omega9"}


def lean_rat(q):
    q = Fraction(q)
    if q.denominator == 1:
        return f"({q.numerator} : ℂ)"
    return f"({q.numerator} / {q.denominator} : ℂ)"


def lean_poly(elt, names):
    """A ring element as a Lean expression in the atoms (no reduction)."""
    if not elt:
        return "(0 : ℂ)"
    parts = []
    for k, v in sorted(elt.items()):
        factors = [lean_rat(v)]
        for e, n in zip(k, names):
            if e == 1:
                factors.append(LEAN_ATOM[n])
            elif e > 1:
                factors.append(f"{LEAN_ATOM[n]} ^ {e}")
        parts.append(" * ".join(factors))
    return "(" + " + ".join(parts) + ")"


def represents_block(R, names, hyps, bname, mname, theta_elt, theta_lean, basis, doc):
    """Lean text: the matrix `mname` and `Represents bname mname theta_lean`."""
    M = R.matrix(theta_elt, basis)
    lines = [f"/-- {doc} -/",
             f"def {mname} : Fin {len(basis)} → Fin {len(basis)} → ℤ :=",
             "  " + lean_mat([[lean_int(q) for q in row] for row in M])]
    # cofactors for each basis element
    cands = []
    for j, k in enumerate(basis):
        b = {k: Fraction(1)}
        lhs = R.mul_raw(theta_elt, b)
        rhs = {}
        for i, ki in enumerate(basis):
            if M[i][j]:
                rhs = R.add(rhs, {ki: M[i][j]})
        diff = R.add(lhs, R.neg(rhs))
        quots, rem = R.divide(diff)
        if rem:
            raise ValueError(f"{mname}: column {j} does not reduce")
        terms = [f"{lean_poly(q, names)} * {hyps[gi]}" for gi, q in enumerate(quots) if q]
        cands.append(" + ".join(terms) if terms else None)
    uniq = []
    for c in cands:
        if c not in uniq:
            uniq.append(c)
    hyp_haves = "\n".join(f"  have {h} := {lemma}" for h, lemma in HYP_LEMMAS.items() if h in hyps.values())
    lines += [f"theorem {mname}_represents' : Represents {bname} {mname} {theta_lean} := by",
              hyp_haves,
              "  simp only [Represents, Fin.forall_fin_succ, IsEmpty.forall_iff, and_true]",
              "  refine " + "⟨" + ", ".join("?_" for _ in basis) + "⟩",
              f"  all_goals simp only [{bname}, {mname}, Fin.sum_univ_succ, Fin.sum_univ_zero,",
              "    Matrix.cons_val_zero, Matrix.cons_val_succ, Int.cast_zero, Int.cast_one, Int.cast_neg,",
              "    Int.cast_ofNat]",
              "  all_goals first"]
    for c in uniq:
        lines.append("    | ring1" if c is None else f"    | linear_combination {c}")
    return "\n".join(lines)


HYP_LEMMAS = {"h2": "sqrt2_sq_c", "h3": "sqrt3_sq_c", "hI": "Complex.I_sq",
              "hw3": "omega3_sq_eq", "hw9": "omega9_pow_six"}


def emit_bases(out_path=None):
    L = []
    A = L.append
    A("/-")
    A("The bases and multiplication matrices of the reflection proofs.")
    A("")
    A("Generated by `lean_proofs/tools/gen_witness_lean.py --bases`; do not edit by")
    A("hand. For each ring the witnesses live in, a ℤ-basis `B` of it as a vector of")
    A("complex numbers, and for each multiplier the cells need (the phase root of")
    A("unity `ζ`, and the factors of the target amplitudes), its integer matrix `M`")
    A("on that basis with the proof `Represents B M θ`. Each column identity is a")
    A("polynomial identity in the atoms modulo `√2² = 2`, `√3² = 3`, `i² = -1`,")
    A("`ω₃² = -1 - ω₃`, `ω₉⁶ = -ω₉³ - 1`, closed by `linear_combination` with the")
    A("cofactors found by polynomial division. `LeanProofs/ReflectQubit.lean` and")
    A("`LeanProofs/ReflectQutrit.lean` build the target lemmas on top of this.")
    A("-/")
    A("import LeanProofs.Stabilizer.Reflect")
    A("import LeanProofs.QubitShared")
    A("import LeanProofs.T3M2Pointwise")
    A("")
    A("set_option linter.style.longLine false")
    A("set_option linter.unusedSimpArgs false")
    A("")
    A("namespace StabRank")
    A("")
    A("open Stabilizer")
    A("")
    A("/-- The ninth cyclotomic relation, from `ω₉³ = ω₃` and `ω₃² + ω₃ + 1 = 0`. -/")
    A("theorem omega9_pow_six : omega9 ^ 6 = -omega9 ^ 3 - 1 := by")
    A("  have h := omega3_sq_add_omega3_add_one")
    A("  rw [← omega9_cube] at h")
    A("  linear_combination h")
    A("")

    def basis_lean(names, basis):
        out = []
        for k in basis:
            fs = []
            for e, n in zip(k, names):
                if e == 1:
                    fs.append(LEAN_ATOM[n])
                elif e > 1:
                    fs.append(f"{LEAN_ATOM[n]} ^ {e}")
            out.append(" * ".join(fs) if fs else "1")
        return "![" + ", ".join(out) + "]"

    # ℤ[√2, i]
    orb = make_orbit("qubit_H", 2)
    R, basis = orb["R"], orb["basis"]
    names = ["s2", "s3", "i", "th"]
    g = {n: R.gen(i) for i, n in enumerate(R.names)}
    hyps = {0: "h2", 1: "h3", 2: "hI"}
    A("/-! ### `ℤ[√2, i]`, for the H-type qubit cells -/")
    A("")
    A("/-- The basis `1, √2, i, i√2`. -/")
    A(f"noncomputable def B4 : Fin 4 → ℂ := {basis_lean(names, basis)}")
    A("theorem B4_zero : B4 ⟨0, by norm_num⟩ = 1 := rfl")
    A("")
    for mname, th, tl, doc in (
            ("MI4", g["i"], "Complex.I", "Multiplication by `i`."),
            ("M1ps2", R.add(R.const(1), g["s2"]), "(1 + (Real.sqrt 2 : ℂ))",
             "Multiplication by `1 + √2`, the ratio `cos(π/8) / sin(π/8)`."),
            ("M2ms2", R.add(R.const(2), R.neg(g["s2"])), "(2 - (Real.sqrt 2 : ℂ))",
             "Multiplication by `2 - √2 = 4 sin²(π/8)`.")):
        A(represents_block(R, names, hyps, "B4", mname, th, tl, basis, doc))
        A("")
    A("theorem MI4_represents : Represents B4 MI4 (zeta 2) := by")
    A("  rw [zeta_two]; exact MI4_represents'")
    A("")

    # ℤ[√2, √3, i]
    orb = make_orbit("qubit_T", 2)
    R, basis = orb["R"], orb["basis"]
    g = {n: R.gen(i) for i, n in enumerate(R.names)}
    A("/-! ### `ℤ[√2, √3, i]`, for the T-type qubit cells -/")
    A("")
    A("/-- The basis `1, √2, √3, √2√3, i, i√2, i√3, i√2√3`. -/")
    A(f"noncomputable def B8 : Fin 8 → ℂ := {basis_lean(names, basis)}")
    A("theorem B8_zero : B8 ⟨0, by norm_num⟩ = 1 := rfl")
    A("")
    for mname, th, tl, doc in (
            ("MI8", g["i"], "Complex.I", "Multiplication by `i`."),
            ("Ma8", R.add(R.mul(g["s2"], g["s3"]), g["s2"]),
             "((Real.sqrt 2 : ℂ) * (Real.sqrt 3 : ℂ) + (Real.sqrt 2 : ℂ))",
             "Multiplication by `√2(√3 + 1) = 2 cos β / sin β`."),
            ("Mb8", R.add(g["s2"], R.mul(g["i"], g["s2"])),
             "((Real.sqrt 2 : ℂ) + Complex.I * (Real.sqrt 2 : ℂ))",
             "Multiplication by `√2(1 + i) = 2 e^{iπ/4}`."),
            ("Mc8", R.add(R.const(3), R.neg(g["s3"])), "(3 - (Real.sqrt 3 : ℂ))",
             "Multiplication by `3 - √3 = 6 sin² β`.")):
        A(represents_block(R, names, hyps, "B8", mname, th, tl, basis, doc))
        A("")
    A("theorem MI8_represents : Represents B8 MI8 (zeta 2) := by")
    A("  rw [zeta_two]; exact MI8_represents'")
    A("")

    # ℤ[ω₃, √3]
    orb = make_orbit("H3", 2)
    R, basis = orb["R"], orb["basis"]
    names = ["w3", "s3", "th", "s2"]
    g = {n: R.gen(i) for i, n in enumerate(R.names)}
    hyps = {0: "hw3", 1: "h3"}
    A("/-! ### `ℤ[ω₃, √3]`, for the H₃ cells -/")
    A("")
    A("/-- The basis `1, ω₃, √3, √3 ω₃`. -/")
    A(f"noncomputable def B3 : Fin 4 → ℂ := {basis_lean(names, basis)}")
    A("theorem B3_zero : B3 ⟨0, by norm_num⟩ = 1 := rfl")
    A("")
    for mname, th, tl, doc in (
            ("Mw3", g["w"], "omega3", "Multiplication by `ω₃`."),
            ("M3ps3", R.add(R.const(3), g["s3"]), "(3 + (Real.sqrt 3 : ℂ))",
             "Multiplication by `3 + √3`, six times the `|0⟩` amplitude over `N`."),
            ("Ms3", g["s3"], "(Real.sqrt 3 : ℂ)",
             "Multiplication by `√3`, six times the `|1⟩`, `|2⟩` amplitude over `N`."),
            ("M3ms3", R.add(R.const(3), R.neg(g["s3"])), "(3 - (Real.sqrt 3 : ℂ))",
             "Multiplication by `3 - √3 = N²`.")):
        A(represents_block(R, names, hyps, "B3", mname, th, tl, basis, doc))
        A("")
    A("theorem Mw3_represents : Represents B3 Mw3 (zeta 3) := by")
    A("  rw [zeta_three]; exact Mw3_represents'")
    A("")

    # ℤ[ω₉, √3]
    orb = make_orbit("T3", 2)
    R, basis = orb["R"], orb["basis"]
    names = ["w9", "s3"]
    g = {n: R.gen(i) for i, n in enumerate(R.names)}
    hyps = {0: "hw9", 1: "h3"}
    A("/-! ### `ℤ[ω₉, √3]`, for the T₃ cells -/")
    A("")
    A("/-- The basis `ω₉^t` and `√3 ω₉^t` for `t < 6`. -/")
    A(f"noncomputable def B9 : Fin 12 → ℂ := {basis_lean(names, basis)}")
    A("theorem B9_zero : B9 ⟨0, by norm_num⟩ = 1 := rfl")
    A("")
    for mname, th, tl, doc in (
            ("Mw9", g["w"], "omega9", "Multiplication by `ω₉`."),
            ("Mw9c", R.pow(g["w"], 3), "(omega9 ^ 3)", "Multiplication by `ω₉³ = ω₃`.")):
        A(represents_block(R, names, hyps, "B9", mname, th, tl, basis, doc))
        A("")
    A("theorem Mw9c_represents : Represents B9 Mw9c (zeta 3) := by")
    A("  rw [zeta_three, ← omega9_cube]; exact Mw9c_represents'")
    A("")
    A("end StabRank")
    text = "\n".join(L) + "\n"
    out_path = out_path or os.path.join(LEAN_DIR, "ReflectBases.lean")
    with open(out_path, "w") as f:
        f.write(text)
    print(f"wrote {os.path.relpath(out_path, ROOT)}")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("bounds", nargs="*")
    ap.add_argument("--bases", action="store_true",
                    help="write LeanProofs/ReflectBases.lean (bases and matrices)")
    ap.add_argument("--check", action="store_true", help="only check the integer identity")
    ap.add_argument("--chunks", type=int, default=1,
                    help="split the kernel check into this many slice modules")
    ap.add_argument("--update-bound", action="store_true",
                    help="also record the module and theorem in the bound file "
                         "(after the module has been built)")
    args = ap.parse_args()
    if args.bases:
        emit_bases()
        return 0
    for b in args.bounds:
        info = generate(b, check_only=args.check, chunks=args.chunks)
        if info and args.update_bound:
            update_bound(b, info["module"], info["theorem"])
    return 0


if __name__ == "__main__":
    sys.exit(main())
