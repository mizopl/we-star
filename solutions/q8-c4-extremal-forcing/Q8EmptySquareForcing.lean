/-
  Q8EmptySquareForcing.lean
  Self-contained, zero-dependency Lean 4 formalization on the ABSTRACT incidence
  structure `C4FreeCounts` (whose double-counting hypotheses `h_tot`, `h_inc`, `h_wedge`
  are assumed as structure fields rather than derived from a concrete graph object):
    1. Exact Empty-Square Forcing Identity:
         n2_opp + total_sq + W = n0 + (n - 1) * m.
    2. Exact Convexity Defect Identity on Q_8:
         W + 3840 = 10 * m + sumDefect ds,
       with sumDefect ds = 0 <-> every vertex has degree 5 or 6.
    3. Mandatory Empty-Square Theorems for Q_8 at m = 683 (n0 = 1 + n2_opp + sumDefect ds >= 1)
       and m >= 684 (n0 >= 4 + n2_opp + sumDefect ds >= 4).
    4. Exact upper bound g(8) <= 682 for any `C4FreeCounts` with n0 = 0 and n2_opp = 0
       (in particular any odd-square subgraph).
    5. Exact dichotomy at m = 682:
       - Any `C4FreeCounts` at m = 682 with n0 = n2_opp = 0 has sumDefect = 2 (W = 2982),
         so cannot have all degrees in {5, 6}.
       - Any `C4FreeCounts` at m = 682 with all degrees in {5, 6} (sumDefect = 0, W = 2980)
         must satisfy n2_opp = 2 + n0 >= 2 and therefore cannot be odd-square.

  Verification guarantees:
    - Zero external dependencies (pure Lean 4 core; tested on Lean 4.36.0).
    - Standard Lean 4 axioms only (`propext`, `Classical.choice`, `Quot.sound`);
      zero `sorryAx`, zero `native_decide`, zero `@[implemented_by]`, `autoImplicit := false`.
-/

set_option autoImplicit false

namespace Q8C4Extremal

/-- Exact integer choose-2: d * (d - 1) / 2. -/
def choose2 (d : Nat) : Nat := d * (d - 1) / 2

/-- Per-vertex convexity excess above the {5, 6} degree shell:
    choose2(d) + 15 - 5*d >= 0, with equality iff d = 5 or d = 6. -/
def vDefect (d : Nat) : Nat := choose2 d + 15 - 5 * d

theorem choose2_eq_half (d : Nat) : 2 * choose2 d = d * (d - 1) := by
  unfold choose2
  cases d with
  | zero => simp
  | succ k =>
    have h_even : 2 ∣ (k + 1) * k := by
      have hmod : k % 2 = 0 ∨ k % 2 = 1 := by omega
      rcases hmod with h0 | h1
      · refine ⟨(k + 1) * (k / 2), ?_⟩
        have hk : k = 2 * (k / 2) := by omega
        calc (k + 1) * k = (k + 1) * (2 * (k / 2)) := by rw [← hk]
          _ = 2 * ((k + 1) * (k / 2)) := by rw [Nat.mul_left_comm]
      · refine ⟨((k + 1) / 2) * k, ?_⟩
        have hk1 : k + 1 = 2 * ((k + 1) / 2) := by omega
        calc (k + 1) * k = (2 * ((k + 1) / 2)) * k := by rw [← hk1]
          _ = 2 * (((k + 1) / 2) * k) := by rw [Nat.mul_assoc]
    exact Nat.mul_div_cancel' h_even

theorem vDefect_identity (d : Nat) : choose2 d + 15 = 5 * d + vDefect d := by
  unfold vDefect
  have h2 := choose2_eq_half d
  have hge : 5 * d ≤ choose2 d + 15 := by
    have hsq : 10 * d ≤ d * (d - 1) + 30 := by
      match d with
      | 0 | 1 | 2 | 3 | 4 | 5 | 6 => decide
      | k + 7 =>
        have hexp : (k + 7) * (k + 6) = k * k + 13 * k + 42 := by
          simp [Nat.mul_add, Nat.add_mul]
          omega
        have : k + 7 - 1 = k + 6 := by omega
        rw [this, hexp]
        omega
    omega
  omega

theorem vDefect_zero_iff (d : Nat) : vDefect d = 0 ↔ (d = 5 ∨ d = 6) := by
  have h1 := vDefect_identity d
  have h2 := choose2_eq_half d
  constructor
  · intro hz
    have heq : d * (d - 1) + 30 = 10 * d := by omega
    match d with
    | 0 | 1 | 2 | 3 | 4 => simp at heq
    | 5 => exact Or.inl rfl
    | 6 => exact Or.inr rfl
    | k + 7 =>
      have hexp : (k + 7) * (k + 6) = k * k + 13 * k + 42 := by
        simp [Nat.mul_add, Nat.add_mul]
        omega
      have : k + 7 - 1 = k + 6 := by omega
      rw [this, hexp] at heq
      omega
  · intro h
    rcases h with rfl | rfl <;> decide

/-- Sum of choose2 over a vertex degree sequence. -/
def sumChoose2 : List Nat → Nat
  | [] => 0
  | d :: ds => choose2 d + sumChoose2 ds

/-- Sum of vertex convexity defects over a vertex degree sequence. -/
def sumDefect : List Nat → Nat
  | [] => 0
  | d :: ds => vDefect d + sumDefect ds

theorem sumChoose2_identity (ds : List Nat) :
    sumChoose2 ds + 15 * ds.length = 5 * ds.sum + sumDefect ds := by
  induction ds with
  | nil => simp [sumChoose2, sumDefect]
  | cons d tl ih =>
    simp only [sumChoose2, sumDefect, List.length_cons, List.sum_cons]
    have hd := vDefect_identity d
    omega

theorem sumDefect_zero_iff (ds : List Nat) :
    sumDefect ds = 0 ↔ ∀ x ∈ ds, x = 5 ∨ x = 6 := by
  induction ds with
  | nil => simp [sumDefect]
  | cons a tl ih =>
    simp only [sumDefect, List.mem_cons]
    constructor
    · intro hz x hx
      have h1 : vDefect a = 0 := by omega
      have h2 : sumDefect tl = 0 := by omega
      rcases hx with rfl | hmem
      · exact (vDefect_zero_iff x).mp h1
      · exact ih.mp h2 x hmem
    · intro hall
      have h1 : vDefect a = 0 := (vDefect_zero_iff a).mpr (hall a (Or.inl rfl))
      have h2 : sumDefect tl = 0 := ih.mpr (fun x hx => hall x (Or.inr hx))
      omega

/-- Exact Q_8 convexity identity on 256 vertices with handshaking sum 2*m:
    W + 3840 = 10 * m + sumDefect ds. -/
theorem q8_convexity_identity (ds : List Nat) (m : Nat)
    (hlen : ds.length = 256) (hhand : ds.sum = 2 * m) :
    sumChoose2 ds + 3840 = 10 * m + sumDefect ds := by
  have h := sumChoose2_identity ds
  omega

/-- Abstract C_4-free square & wedge double-counting invariants for Q_n.
    Motivation: a C_4-free subgraph H of Q_n with m edges, total_sq = C(n,2) * 2^(n-2)
    4-cycles, and wedge sum W = sum_v C(deg(v), 2) satisfies the three equations below.
    In this file those equations are ASSUMED as abstract structure fields (not derived
    from a concrete graph representation):
      h_tot:   n0 + n1 + n2_opp + n2_adj + n3 = total_sq
      h_inc:   n1 + 2 * (n2_opp + n2_adj) + 3 * n3 = (n - 1) * m
      h_wedge: n2_adj + 2 * n3 = W
-/
structure C4FreeCounts (n total_sq m W : Nat) where
  n0     : Nat
  n1     : Nat
  n2_opp : Nat
  n2_adj : Nat
  n3     : Nat
  h_tot   : n0 + n1 + n2_opp + n2_adj + n3 = total_sq
  h_inc   : n1 + 2 * (n2_opp + n2_adj) + 3 * n3 = (n - 1) * m
  h_wedge : n2_adj + 2 * n3 = W

/-- Theorem 1 (abstract `C4FreeCounts`): every `C4FreeCounts n total_sq m W` instance
    satisfies the exact Empty-Square Forcing Identity in Nat:
      n2_opp + total_sq + W = n0 + (n - 1) * m. -/
theorem empty_square_forcing_identity {n total_sq m W : Nat}
    (c : C4FreeCounts n total_sq m W) :
    c.n2_opp + total_sq + W = c.n0 + (n - 1) * m := by
  have h1 := c.h_tot
  have h2 := c.h_inc
  have h3 := c.h_wedge
  omega

/-- Theorem 2 (Q_8 at m = 683, abstract `C4FreeCounts`): Every `C4FreeCounts` instance
    at m = 683 on 256 vertices satisfies n0 = 1 + n2_opp + sumDefect ds >= 1. -/
theorem q8_683_forces_empty_square (ds : List Nat)
    (hlen : ds.length = 256) (hhand : ds.sum = 2 * 683)
    (c : C4FreeCounts 8 1792 683 (sumChoose2 ds)) :
    c.n0 = 1 + c.n2_opp + sumDefect ds ∧ c.n0 ≥ 1 := by
  have hconv := q8_convexity_identity ds 683 hlen hhand
  have hid := empty_square_forcing_identity c
  omega

/-- Theorem 3 (Q_8 at m >= 684, abstract `C4FreeCounts`): Every `C4FreeCounts` instance
    at m >= 684 on 256 vertices satisfies n0 >= 4 + n2_opp + sumDefect ds >= 4. -/
theorem q8_ge684_forces_empty_squares (ds : List Nat) (m : Nat)
    (hlen : ds.length = 256) (hhand : ds.sum = 2 * m) (hm : m ≥ 684)
    (c : C4FreeCounts 8 1792 m (sumChoose2 ds)) :
    c.n0 ≥ 4 + c.n2_opp + sumDefect ds ∧ c.n0 ≥ 4 := by
  have hconv := q8_convexity_identity ds m hlen hhand
  have hid := empty_square_forcing_identity c
  omega

/-- Theorem 4 (Exact Upper Bound g(8) <= 682, abstract `C4FreeCounts`):
    Any `C4FreeCounts` instance on 256 vertices with n0 = 0 and n2_opp = 0
    (in particular, any odd-square incidence count) satisfies m <= 682. -/
theorem q8_odd_square_upper_682 (ds : List Nat) (m : Nat)
    (hlen : ds.length = 256) (hhand : ds.sum = 2 * m)
    (c : C4FreeCounts 8 1792 m (sumChoose2 ds))
    (h_n0 : c.n0 = 0) (h_n2o : c.n2_opp = 0) :
    m ≤ 682 := by
  have hconv := q8_convexity_identity ds m hlen hhand
  have hid := empty_square_forcing_identity c
  omega

/-- Theorem 5a (682 Odd-Square Defect Forcing, abstract `C4FreeCounts`):
    Any `C4FreeCounts` instance at m = 682 with n0 = n2_opp = 0 MUST have
    sumDefect ds = 2 (W = 2982), so not all entries of ds lie in {5, 6}. -/
theorem q8_682_odd_square_forces_defect_2 (ds : List Nat)
    (hlen : ds.length = 256) (hhand : ds.sum = 2 * 682)
    (c : C4FreeCounts 8 1792 682 (sumChoose2 ds))
    (h_n0 : c.n0 = 0) (h_n2o : c.n2_opp = 0) :
    sumDefect ds = 2 ∧ sumChoose2 ds = 2982 ∧ ¬ (∀ x ∈ ds, x = 5 ∨ x = 6) := by
  have hconv := q8_convexity_identity ds 682 hlen hhand
  have hid := empty_square_forcing_identity c
  have hdef : sumDefect ds = 2 := by omega
  have hW : sumChoose2 ds = 2982 := by omega
  have hnot56 : ¬ (∀ x ∈ ds, x = 5 ∨ x = 6) := by
    intro hall
    have hz := (sumDefect_zero_iff ds).mpr hall
    omega
  exact ⟨hdef, hW, hnot56⟩

/-- Theorem 5b (682 Zero-Defect {5,6} Dichotomy, abstract `C4FreeCounts`):
    Any `C4FreeCounts` instance at m = 682 with all entries of ds in {5, 6}
    MUST satisfy n2_opp = 2 + n0 >= 2 and therefore cannot have n2_opp = 0. -/
theorem q8_682_deg56_forces_n2_opp_ge_2 (ds : List Nat)
    (hlen : ds.length = 256) (hhand : ds.sum = 2 * 682)
    (h56 : ∀ x ∈ ds, x = 5 ∨ x = 6)
    (c : C4FreeCounts 8 1792 682 (sumChoose2 ds)) :
    c.n2_opp = 2 + c.n0 ∧ c.n2_opp ≥ 2 := by
  have hconv := q8_convexity_identity ds 682 hlen hhand
  have hid := empty_square_forcing_identity c
  have hz := (sumDefect_zero_iff ds).mpr h56
  omega

end Q8C4Extremal

#print axioms Q8C4Extremal.empty_square_forcing_identity
#print axioms Q8C4Extremal.q8_683_forces_empty_square
#print axioms Q8C4Extremal.q8_ge684_forces_empty_squares
#print axioms Q8C4Extremal.q8_odd_square_upper_682
#print axioms Q8C4Extremal.q8_682_odd_square_forces_defect_2
#print axioms Q8C4Extremal.q8_682_deg56_forces_n2_opp_ge_2
