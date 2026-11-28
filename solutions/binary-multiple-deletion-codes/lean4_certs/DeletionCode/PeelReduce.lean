/-
  DeletionCode/PeelReduce.lean — Universal Zero-Mathlib Pure-Kernel "Onion Peeling" Graph
  Reduction Engine (Simplicial / Insertion-Ball Clique Removal + Iterated `D_2`-Orbit
  Neighborhood Domination `N_H[x] ⊆ N_H[y]`) for ALL Binary `s`-Deletion-Correcting Codes (`s ≤ n`).

  Composes directly with `DeletionCode.SchrijverPSD.weak_duality_schrijver_psd_on`:
    1. Ball Clique Peeling: each insertion ball `I_s(z)` (`z < 2^(n-s)`) is a symbolic clique
       in `G_{n,s}` (`|C ∩ I_s(z)| ≤ 1`), removing `I_s(z)` for cost `+1` with ZERO pairwise checks!
    2. Iterated `D_2`-Orbit Domination: if `H ⊆ {0,1}^n` is `D_2`-invariant, `x ∈ H`, `x ∉ D_2(y)`,
       `x ~ y`, and `N_H[x] ⊆ N_H[y]`, then swapping `g(y) ↦ g(x)` for `g = 0,1,2,3` yields a
       valid code `C' ⊆ H \ D_2(y)` of IDENTICAL length (`|C'| = |C|`)!
    3. `O(1)` Hamming-weight branch pruning (`|wt(x) - wt(z)| > s → ¬ (x ~ z)`) + exact
       completeness of `canMatchNat` (`canMatchNat_complete`) make domination checking blazing fast
       in the pure Lean 4.36.0 kernel (0 Mathlib, 0 sorryAx, 0 native_decide / Lean.ofReduceBool).
-/
import DeletionCode.Basic
import DeletionCode.DualLP
import DeletionCode.CutDual
import DeletionCode.RecDual
import DeletionCode.SchrijverPSD

set_option maxRecDepth 65536

namespace DeletionCode.PeelReduce

open DeletionCode
open DeletionCode.DualLP
open DeletionCode.CutDual
open DeletionCode.RecDual
open DeletionCode.SchrijverPSD

/-! ## 1. Conflict Graph Edge Predicate, `D_2` Automorphisms, and Completeness of `canMatchNat` -/

/-- Two `n`-bit words conflict in `G_{n,s}` iff their `s`-deletion balls intersect. -/
def HasEdge (n s u v : Nat) : Prop :=
  ∃ d : List Bool, InDelBall s (natToWord n u) d ∧ InDelBall s (natToWord n v) d

theorem hasEdge_symm {n s u v : Nat} (h : HasEdge n s u v) : HasEdge n s v u := by
  rcases h with ⟨d, hu, hv⟩
  exact ⟨d, hv, hu⟩

/-- Encode `List Bool` back into `Nat` (LSB-first inverse of `natToWord`). -/
def wordToNat : List Bool → Nat
  | [] => 0
  | b :: bs => (if b then 1 else 0) + 2 * wordToNat bs

theorem wordToNat_lt : ∀ (w : List Bool), wordToNat w < 2 ^ w.length
  | [] => by simp [wordToNat]
  | b :: bs => by
    have ih := wordToNat_lt bs
    have hpow : 2 ^ (bs.length + 1) = 2 * 2 ^ bs.length := by rw [Nat.pow_succ, Nat.mul_comm]
    simp only [wordToNat, List.length_cons, hpow]
    cases b <;> simp <;> omega

theorem natToWord_wordToNat : ∀ (w : List Bool), natToWord w.length (wordToNat w) = w
  | [] => rfl
  | b :: bs => by
    have ih := natToWord_wordToNat bs
    cases b
    · simp only [wordToNat, List.length_cons, natToWord, Bool.false_eq_true, ↓reduceIte, Nat.zero_add]
      have hmod : (2 * wordToNat bs) % 2 = 0 := by omega
      have hdiv : (2 * wordToNat bs) / 2 = wordToNat bs := by omega
      simp [hmod, hdiv, ih]
    · simp only [wordToNat, List.length_cons, natToWord, ↓reduceIte]
      have hmod : (1 + 2 * wordToNat bs) % 2 = 1 := by omega
      have hdiv : (1 + 2 * wordToNat bs) / 2 = wordToNat bs := by omega
      simp [hmod, hdiv, ih]

/-- Every `g ∈ D_2` preserves edges of `G_{n,s}`. -/
theorem hasEdge_applyD2 {n s g u v : Nat} (hs : s ≤ n) (hu : u < 2 ^ n) (hv : v < 2 ^ n)
    (h : HasEdge n s u v) : HasEdge n s (applyD2 n g u) (applyD2 n g v) := by
  rcases h with ⟨d, hdu, hdv⟩
  have hdlen : d.length = n - s := by
    have := hdu.2
    rw [natToWord_length] at this
    omega
  let dNat := wordToNat d
  have hdlt : dNat < 2 ^ (n - s) := by
    rw [← hdlen]; exact wordToNat_lt d
  have hdw : natToWord (n - s) dNat = d := by
    rw [← hdlen]; exact natToWord_wordToNat d
  rw [← hdw] at hdu hdv
  exact ⟨natToWord (n - s) (applyD2 (n - s) g dNat),
    inDelBall_applyD2 hs hu hdlt hdu,
    inDelBall_applyD2 hs hv hdlt hdv⟩

/-- Exact completeness of `canMatchNat`: if `u, v` share a length-`L` subsequence with budgets
    `s1, s2` and `fuel ≥ L + s1 + s2`, then `canMatchNat fuel L s1 s2 u v = true`. -/
theorem canMatchNat_complete : ∀ (fuel L s1 s2 u v : Nat),
    L + s1 + s2 ≤ fuel →
    (∃ d : List Bool, d.length = L ∧
      IsSubseq d (natToWord (L + s1) u) ∧ IsSubseq d (natToWord (L + s2) v)) →
    canMatchNat fuel L s1 s2 u v = true
  | _, 0, _, _, _, _, _, _ => by simp [canMatchNat]
  | 0, L + 1, _, _, _, _, hfuel, _ => by omega
  | fuel + 1, L + 1, s1, s2, u, v, hfuel, ⟨d, hdlen, hdu, hdv⟩ => by
    cases d with
    | nil => simp at hdlen
    | cons c ds =>
      have hdslen : ds.length = L := by simpa using hdlen
      have hu_eq : natToWord ((L + 1) + s1) u = (u % 2 == 1) :: natToWord (L + s1) (u / 2) := by
        rw [Nat.succ_add]; rfl
      have hv_eq : natToWord ((L + 1) + s2) v = (v % 2 == 1) :: natToWord (L + s2) (v / 2) := by
        rw [Nat.succ_add]; rfl
      rw [hu_eq] at hdu
      rw [hv_eq] at hdv
      simp only [canMatchNat]
      by_cases hmod : u % 2 = v % 2
      · have hbeq : Nat.beq (u % 2) (v % 2) = true := by rw [hmod, Nat.beq_refl]
        simp only [hbeq, ↓reduceIte]
        have hdu' : IsSubseq ds (natToWord (L + s1) (u / 2)) := by
          cases hdu with
          | cons_keep _ h' => exact h'
          | cons_drop _ h' => exact isSubseq_of_cons_left h'
        have hdv' : IsSubseq ds (natToWord (L + s2) (v / 2)) := by
          cases hdv with
          | cons_keep _ h' => exact h'
          | cons_drop _ h' => exact isSubseq_of_cons_left h'
        exact canMatchNat_complete fuel L s1 s2 (u / 2) (v / 2) (by omega) ⟨ds, hdslen, hdu', hdv'⟩
      · have hbeq : Nat.beq (u % 2) (v % 2) = false := by
          cases hb : Nat.beq (u % 2) (v % 2)
          · rfl
          · exact absurd (Nat.eq_of_beq_eq_true hb) hmod
        simp only [hbeq, Bool.false_eq_true, ↓reduceIte]
        have hbit_ne : (u % 2 == 1) ≠ (v % 2 == 1) := by
          have hu2 : u % 2 < 2 := Nat.mod_lt u (by omega)
          have hv2 : v % 2 < 2 := Nat.mod_lt v (by omega)
          intro heq
          cases hu0 : u % 2 with
          | zero =>
            have hv1 : v % 2 = 1 := by omega
            simp [hu0, hv1] at heq
          | succ a =>
            have hu1 : u % 2 = 1 := by omega
            have hv0 : v % 2 = 0 := by omega
            simp [hu1, hv0] at heq
        -- Since first bits differ, at least one of `hdu` or `hdv` must be `cons_drop`!
        have hdrop : IsSubseq (c :: ds) (natToWord (L + s1) (u / 2)) ∨
                     IsSubseq (c :: ds) (natToWord (L + s2) (v / 2)) := by
          have aux : ∀ (bu bv : Bool) (wu wv : List Bool),
              bu ≠ bv → IsSubseq (c :: ds) (bu :: wu) → IsSubseq (c :: ds) (bv :: wv) →
              IsSubseq (c :: ds) wu ∨ IsSubseq (c :: ds) wv := by
            intro bu bv wu wv hne h1 h2
            cases h1 with
            | cons_drop _ h1' => exact Or.inl h1'
            | cons_keep _ _ =>
              cases h2 with
              | cons_drop _ h2' => exact Or.inr h2'
              | cons_keep _ _ => exact absurd rfl hne
          exact aux (u % 2 == 1) (v % 2 == 1) _ _ hbit_ne hdu hdv
        rcases hdrop with h1 | h2
        · have hs1_pos : 1 ≤ s1 := by
            have hl := h1.length_le
            rw [List.length_cons, hdslen, natToWord_length] at hl
            omega
          cases s1 with
          | zero => omega
          | succ s1' =>
            have h1' : IsSubseq (c :: ds) (natToWord ((L + 1) + s1') (u / 2)) := by
              have heq : (L + 1) + s1' = L + (s1' + 1) := by omega
              rw [heq]; exact h1
            have hdv_orig : IsSubseq (c :: ds) (natToWord ((L + 1) + s2) v) := by
              rw [hv_eq]; exact hdv
            have hres := canMatchNat_complete fuel (L + 1) s1' s2 (u / 2) v (by omega)
              ⟨c :: ds, by simp [hdslen], h1', hdv_orig⟩
            simp [hres]
        · have hs2_pos : 1 ≤ s2 := by
            have hl := h2.length_le
            rw [List.length_cons, hdslen, natToWord_length] at hl
            omega
          cases s2 with
          | zero => omega
          | succ s2' =>
            have h2' : IsSubseq (c :: ds) (natToWord ((L + 1) + s2') (v / 2)) := by
              have heq : (L + 1) + s2' = L + (s2' + 1) := by omega
              rw [heq]; exact h2
            have hdu_orig : IsSubseq (c :: ds) (natToWord ((L + 1) + s1) u) := by
              rw [hu_eq]; exact hdu
            have hres := canMatchNat_complete fuel (L + 1) s1 s2' u (v / 2) (by omega)
              ⟨c :: ds, by simp [hdslen], hdu_orig, h2'⟩
            cases s1 with
            | zero => simpa using hres
            | succ s1' =>
              simp only
              cases canMatchNat fuel (L + 1) s1' (s2' + 1) (u / 2) v <;> simp [hres]

theorem hasEdge_of_canMatch {n s u v : Nat} (hs : s ≤ n)
    (h : canMatchNat (n + s) (n - s) s s u v = true) : HasEdge n s u v := by
  obtain ⟨d, hlen, h1, h2⟩ := canMatchNat_sound (n + s) (n - s) s s u v h
  have hns : n - s + s = n := Nat.sub_add_cancel hs
  rw [hns] at h1 h2
  exact ⟨d, ⟨h1, by rw [natToWord_length, hlen]; omega⟩,
            ⟨h2, by rw [natToWord_length, hlen]; omega⟩⟩

theorem canMatch_of_hasEdge {n s u v : Nat} (hs : s ≤ n) (h : HasEdge n s u v) :
    canMatchNat (n + s) (n - s) s s u v = true := by
  rcases h with ⟨d, ⟨h1, hlen1⟩, ⟨h2, _⟩⟩
  have hdlen : d.length = n - s := by rw [natToWord_length] at hlen1; omega
  have hns : n - s + s = n := Nat.sub_add_cancel hs
  apply canMatchNat_complete (n + s) (n - s) s s u v (by omega)
  exact ⟨d, hdlen, by rw [hns]; exact h1, by rw [hns]; exact h2⟩

/-! ## 2. Hamming Weight & `O(1)` Weight-Difference Pruning Lemma -/

def wordWeight : List Bool → Nat
  | [] => 0
  | b :: bs => (if b then 1 else 0) + wordWeight bs

def popcountNat : Nat → Nat → Nat
  | 0, _ => 0
  | k + 1, x => x % 2 + popcountNat k (x / 2)

theorem popcountNat_le : ∀ (k x : Nat), popcountNat k x ≤ k
  | 0, _ => Nat.le_refl 0
  | k + 1, x => by
    have ih := popcountNat_le k (x / 2)
    have hm : x % 2 ≤ 1 := by omega
    simp only [popcountNat]
    omega

theorem popcountNat_eq_wordWeight : ∀ (k x : Nat), popcountNat k x = wordWeight (natToWord k x)
  | 0, _ => rfl
  | k + 1, x => by
    simp only [popcountNat, natToWord, wordWeight, popcountNat_eq_wordWeight k (x / 2)]
    have hm : x % 2 < 2 := Nat.mod_lt x (by omega)
    rcases Nat.lt_succ_iff_lt_or_eq.mp hm with h0 | h1
    · have hx0 : x % 2 = 0 := by omega
      simp [hx0]
    · simp [h1]

theorem wordWeight_subseq_bounds {u v : List Bool} (h : IsSubseq u v) :
    wordWeight u ≤ wordWeight v ∧ wordWeight v ≤ wordWeight u + (v.length - u.length) := by
  induction h with
  | nil => simp [wordWeight]
  | cons_keep b h' ih =>
    have hle := h'.length_le
    simp only [wordWeight, List.length_cons]
    cases b <;> simp <;> omega
  | cons_drop b h' ih =>
    have hle := h'.length_le
    simp only [wordWeight, List.length_cons]
    cases b <;> simp <;> omega

theorem popcount_diff_le_of_hasEdge {n s u v : Nat} (h : HasEdge n s u v) :
    popcountNat n u ≤ popcountNat n v + s ∧ popcountNat n v ≤ popcountNat n u + s := by
  rcases h with ⟨d, ⟨hdu, hlu⟩, ⟨hdv, hlv⟩⟩
  have b1 := wordWeight_subseq_bounds hdu
  have b2 := wordWeight_subseq_bounds hdv
  rw [popcountNat_eq_wordWeight, popcountNat_eq_wordWeight]
  omega

/-! ## 3. Sparse LSB-First Boolean Subset Tree (`BTree`) & `D_2`-Invariance -/

/-- Sparse depth-`n` LSB-first Boolean set tree (`zero` = all `false`, `one` = all `true`). -/
inductive BTree where
  | zero : BTree
  | one : BTree
  | node (l r : BTree) : BTree

def BTree.get (k : Nat) (t : BTree) (x : Nat) : Bool :=
  match t with
  | .zero => false
  | .one => true
  | .node l r => match k with
    | 0 => false
    | k' + 1 => if x % 2 == 0 then l.get k' (x / 2) else r.get k' (x / 2)
termination_by structural t

def BTree.mkNode : BTree → BTree → BTree
  | .zero, .zero => .zero
  | .one, .one => .one
  | l, r => .node l r

theorem BTree.get_mkNode (k : Nat) (l r : BTree) (x : Nat) :
    (BTree.mkNode l r).get (k + 1) x = if x % 2 == 0 then l.get k (x / 2) else r.get k (x / 2) := by
  cases l <;> cases r
  · simp [BTree.mkNode, BTree.get]
  · rfl
  · rfl
  · rfl
  · simp [BTree.mkNode, BTree.get]
  · rfl
  · rfl
  · rfl
  · rfl

/-- Clear a single word `x < 2^k` to `false` in `t`. -/
def BTree.clear : Nat → Nat → BTree → BTree
  | _, _, .zero => .zero
  | 0, _, .one => .zero
  | 0, _, .node _ _ => .zero
  | k + 1, x, .one =>
    if x % 2 == 0 then BTree.mkNode (BTree.clear k (x / 2) .one) .one
    else BTree.mkNode .one (BTree.clear k (x / 2) .one)
  | k + 1, x, .node l r =>
    if x % 2 == 0 then BTree.mkNode (BTree.clear k (x / 2) l) r
    else BTree.mkNode l (BTree.clear k (x / 2) r)

theorem BTree.get_clear : ∀ (k x y : Nat) (t : BTree),
    x < 2 ^ k → y < 2 ^ k →
    (t.clear k x).get k y = (if y == x then false else t.get k y)
  | _, _, _, .zero, _, _ => by simp [BTree.clear, BTree.get]
  | 0, x, y, .one, hx, hy => by
    have hx0 : x = 0 := by simpa using hx
    have hy0 : y = 0 := by simpa using hy
    subst hx0; subst hy0
    simp [BTree.clear, BTree.get]
  | 0, x, y, .node _ _, hx, hy => by
    have hx0 : x = 0 := by simpa using hx
    have hy0 : y = 0 := by simpa using hy
    subst hx0; subst hy0
    simp [BTree.clear, BTree.get]
  | k + 1, x, y, .one, hx, hy => by
    have hpow : 2 ^ (k + 1) = 2 * 2 ^ k := by rw [Nat.pow_succ, Nat.mul_comm]
    have hx' : x / 2 < 2 ^ k := by rw [hpow] at hx; omega
    have hy' : y / 2 < 2 ^ k := by rw [hpow] at hy; omega
    simp only [BTree.clear]
    by_cases hxm : x % 2 = 0 <;> by_cases hym : y % 2 = 0
    · simp only [hxm, beq_self_eq_true, ↓reduceIte, BTree.get_mkNode, hym]
      rw [BTree.get_clear k (x / 2) (y / 2) .one hx' hy']
      have hiff : (y / 2 == x / 2) = (y == x) := by
        cases h1 : (y == x)
        · have hne : y ≠ x := fun h => by simp [h] at h1
          have hne2 : y / 2 ≠ x / 2 := by omega
          exact beq_false_of_ne hne2
        · have heq : y = x := beq_iff_eq.mp h1
          subst heq; simp
      simp [hiff, BTree.get]
    · have hy1 : y % 2 = 1 := by omega
      have hne : y ≠ x := by omega
      have h10 : (1 == 0) = false := rfl
      simp [hxm, hy1, h10, BTree.get_mkNode, BTree.get, beq_false_of_ne hne]
    · have hx1 : x % 2 = 1 := by omega
      have hne : y ≠ x := by omega
      have h10 : (1 == 0) = false := rfl
      simp [hx1, hym, h10, BTree.get_mkNode, BTree.get, beq_false_of_ne hne]
    · have hx1 : x % 2 = 1 := by omega
      have hy1 : y % 2 = 1 := by omega
      have h10 : (1 == 0) = false := rfl
      simp only [hx1, h10, Bool.false_eq_true, ↓reduceIte, BTree.get_mkNode, hy1]
      rw [BTree.get_clear k (x / 2) (y / 2) .one hx' hy']
      have hiff : (y / 2 == x / 2) = (y == x) := by
        cases h1 : (y == x)
        · have hne : y ≠ x := fun h => by simp [h] at h1
          have hne2 : y / 2 ≠ x / 2 := by omega
          exact beq_false_of_ne hne2
        · have heq : y = x := beq_iff_eq.mp h1
          subst heq; simp
      simp [hiff, BTree.get]
  | k + 1, x, y, .node l r, hx, hy => by
    have hpow : 2 ^ (k + 1) = 2 * 2 ^ k := by rw [Nat.pow_succ, Nat.mul_comm]
    have hx' : x / 2 < 2 ^ k := by rw [hpow] at hx; omega
    have hy' : y / 2 < 2 ^ k := by rw [hpow] at hy; omega
    simp only [BTree.clear]
    by_cases hxm : x % 2 = 0 <;> by_cases hym : y % 2 = 0
    · simp only [hxm, beq_self_eq_true, ↓reduceIte, BTree.get_mkNode, hym]
      rw [BTree.get_clear k (x / 2) (y / 2) l hx' hy']
      have hiff : (y / 2 == x / 2) = (y == x) := by
        cases h1 : (y == x)
        · have hne : y ≠ x := fun h => by simp [h] at h1
          have hne2 : y / 2 ≠ x / 2 := by omega
          exact beq_false_of_ne hne2
        · have heq : y = x := beq_iff_eq.mp h1
          subst heq; simp
      simp [hiff, BTree.get, hym]
    · have hy1 : y % 2 = 1 := by omega
      have hne : y ≠ x := by omega
      have h10 : (1 == 0) = false := rfl
      simp [hxm, hy1, h10, BTree.get_mkNode, BTree.get, beq_false_of_ne hne]
    · have hx1 : x % 2 = 1 := by omega
      have hne : y ≠ x := by omega
      have h10 : (1 == 0) = false := rfl
      simp [hx1, hym, h10, BTree.get_mkNode, BTree.get, beq_false_of_ne hne]
    · have hx1 : x % 2 = 1 := by omega
      have hy1 : y % 2 = 1 := by omega
      have h10 : (1 == 0) = false := rfl
      simp only [hx1, h10, Bool.false_eq_true, ↓reduceIte, BTree.get_mkNode, hy1]
      rw [BTree.get_clear k (x / 2) (y / 2) r hx' hy']
      have hiff : (y / 2 == x / 2) = (y == x) := by
        cases h1 : (y == x)
        · have hne : y ≠ x := fun h => by simp [h] at h1
          have hne2 : y / 2 ≠ x / 2 := by omega
          exact beq_false_of_ne hne2
        · have heq : y = x := beq_iff_eq.mp h1
          subst heq; simp
      simp [hiff, BTree.get, hy1, h10]

/-- Clear the entire `D_2` orbit `{y, c(y), r(y), cr(y)}` from `t`. -/
def BTree.clearD2 (n y : Nat) (t : BTree) : BTree :=
  (((t.clear n (applyD2 n 0 y)).clear n (applyD2 n 1 y)).clear n (applyD2 n 2 y)).clear n (applyD2 n 3 y)

theorem BTree.get_clearD2 {n y z : Nat} (hy : y < 2 ^ n) (hz : z < 2 ^ n) (t : BTree) :
    (t.clearD2 n y).get n z =
      if z == applyD2 n 0 y || z == applyD2 n 1 y || z == applyD2 n 2 y || z == applyD2 n 3 y
      then false else t.get n z := by
  unfold BTree.clearD2
  rw [BTree.get_clear n _ z _ (applyD2_lt hy) hz,
      BTree.get_clear n _ z _ (applyD2_lt hy) hz,
      BTree.get_clear n _ z _ (applyD2_lt hy) hz,
      BTree.get_clear n _ z _ (applyD2_lt hy) hz]
  cases (z == applyD2 n 3 y) <;> cases (z == applyD2 n 2 y) <;>
  cases (z == applyD2 n 1 y) <;> cases (z == applyD2 n 0 y) <;> rfl

/-- `D_2`-invariance of a `BTree`. -/
def D2Inv (n : Nat) (t : BTree) : Prop :=
  ∀ x < 2 ^ n, ∀ g < 4, t.get n (applyD2 n g x) = t.get n x

theorem clearD2_d2Inv {n y : Nat} {t : BTree} (hy : y < 2 ^ n) (ht : D2Inv n t) :
    D2Inv n (t.clearD2 n y) := by
  intro x hx g hg
  rw [BTree.get_clearD2 hy (applyD2_lt hx) t, BTree.get_clearD2 hy hx t, ht x hx g hg]
  -- Show `applyD2 n g x ∈ D_2(y) ↔ x ∈ D_2(y)`!
  have hmem : ∀ h < 4, (applyD2 n g x == applyD2 n h y) = (x == applyD2 n (xorD2 g h) y) := by
    intro h hh
    have hiff : applyD2 n g x = applyD2 n h y ↔ x = applyD2 n (xorD2 g h) y := by
      constructor
      · intro heq
        have h1 := congrArg (applyD2 n g) heq
        rw [applyD2_involutive hx, applyD2_comp hg hh hy] at h1
        exact h1
      · intro heq
        rw [heq, applyD2_comp hg (xorD2_lt hg hh) hy]
        have hinv : xorD2 g (xorD2 g h) = h := by
          match g, h with
          | 0, 0 | 0, 1 | 0, 2 | 0, 3
          | 1, 0 | 1, 1 | 1, 2 | 1, 3
          | 2, 0 | 2, 1 | 2, 2 | 2, 3
          | 3, 0 | 3, 1 | 3, 2 | 3, 3 => rfl
          | g + 4, _ => omega
          | _, h + 4 => omega
        rw [hinv]
    cases h1 : (x == applyD2 n (xorD2 g h) y)
    · have hne : x ≠ applyD2 n (xorD2 g h) y := fun he => by simp [he] at h1
      exact beq_false_of_ne (fun he => hne (hiff.mp he))
    · exact beq_iff_eq.mpr (hiff.mpr (beq_iff_eq.mp h1))
  rw [hmem 0 (by omega), hmem 1 (by omega), hmem 2 (by omega), hmem 3 (by omega)]
  match g with
  | 0 => simp only [xorD2]
  | 1 | 2 | 3 =>
    simp only [xorD2]
    cases (x == applyD2 n 0 y) <;> cases (x == applyD2 n 1 y) <;>
    cases (x == applyD2 n 2 y) <;> cases (x == applyD2 n 3 y) <;> rfl
  | g + 4 => omega

/-- Build the exact complement of a union of insertion balls `I_s(z)` (`z ∈ balls`) as a sparse `BTree`. -/
def buildBallsComplGo (n s : Nat) (balls : List Nat) : Nat → Nat → Nat → BTree
  | 0, acc, _ =>
    if balls.all (fun z => !isSubseqB (natToWord (n - s) z) (natToWord n acc)) then .one else .zero
  | k + 1, acc, pow =>
    BTree.mkNode
      (buildBallsComplGo n s balls k acc (2 * pow))
      (buildBallsComplGo n s balls k (acc + pow) (2 * pow))

def buildBallsComplTree (n s : Nat) (balls : List Nat) : BTree :=
  buildBallsComplGo n s balls n 0 1

private theorem buildBallsComplGo_get (n s : Nat) (balls : List Nat) :
    ∀ (k acc pow r : Nat), r < 2 ^ k →
      (buildBallsComplGo n s balls k acc pow).get k r =
        balls.all (fun z => !isSubseqB (natToWord (n - s) z) (natToWord n (acc + r * pow)))
  | 0, acc, _, r, hr => by
    have hr0 : r = 0 := by simpa using hr
    subst hr0
    simp only [buildBallsComplGo, Nat.zero_mul, Nat.add_zero]
    cases h : balls.all (fun z => !isSubseqB (natToWord (n - s) z) (natToWord n acc)) <;>
      simp [BTree.get]
  | k + 1, acc, pow, r, hr => by
    have hpow : 2 ^ (k + 1) = 2 * 2 ^ k := by rw [Nat.pow_succ, Nat.mul_comm]
    have hr' : r / 2 < 2 ^ k := by rw [hpow] at hr; omega
    simp only [buildBallsComplGo, BTree.get_mkNode]
    by_cases hrm : r % 2 = 0
    · simp only [hrm, beq_self_eq_true, ↓reduceIte]
      rw [buildBallsComplGo_get n s balls k acc (2 * pow) (r / 2) hr']
      have heq : acc + r / 2 * (2 * pow) = acc + r * pow := by
        have h1 : r / 2 * (2 * pow) = (2 * (r / 2)) * pow := by
          rw [Nat.mul_comm 2 (r / 2), Nat.mul_assoc]
        have h2 : 2 * (r / 2) = r := by omega
        rw [h1, h2]
      rw [heq]
    · have hr1 : r % 2 = 1 := by omega
      have h10 : (1 == 0) = false := rfl
      simp only [hr1, h10, Bool.false_eq_true, ↓reduceIte]
      rw [buildBallsComplGo_get n s balls k (acc + pow) (2 * pow) (r / 2) hr']
      have heq : acc + pow + r / 2 * (2 * pow) = acc + r * pow := by
        have h1 : r / 2 * (2 * pow) = (2 * (r / 2)) * pow := by
          rw [Nat.mul_comm 2 (r / 2), Nat.mul_assoc]
        have h2 : 2 * (r / 2) + 1 = r := by omega
        have h3 : pow + (2 * (r / 2)) * pow = (2 * (r / 2) + 1) * pow := by
          rw [Nat.add_mul, Nat.one_mul, Nat.add_comm]
        rw [h1, Nat.add_assoc, h3, h2]
      rw [heq]

theorem buildBallsComplTree_get (n s : Nat) (balls : List Nat) {x : Nat} (hx : x < 2 ^ n) :
    (buildBallsComplTree n s balls).get n x =
      balls.all (fun z => !isSubseqB (natToWord (n - s) z) (natToWord n x)) := by
  simpa [buildBallsComplTree] using buildBallsComplGo_get n s balls n 0 1 x hx

/-! ## 4. Fast Branch-Pruned `BTree` Universal Sweep (for `D_2`-Invariance, Domination, Coverage) -/

/-- Sweep all alive leaves (`t.get k r = true`) in `t` with weight `wt ∈ [wtMin, wtMax]`,
    pruning `.zero` subtrees and impossible Hamming-weight subtrees in `O(1)`! -/
def BTree.forallAliveWeight (wtMin wtMax : Nat) (f : Nat → Bool) :
    Nat → Nat → Nat → Nat → BTree → Bool
  | _, _, _, _, .zero => true
  | 0, acc, _, wt, .one =>
    if wtMin ≤ wt && wt ≤ wtMax then f acc else true
  | 0, _, _, _, .node _ _ => true
  | k + 1, acc, pow, wt, .one =>
    if wt > wtMax || wt + (k + 1) < wtMin then true
    else
      match BTree.forallAliveWeight wtMin wtMax f k acc (2 * pow) wt .one with
      | true => BTree.forallAliveWeight wtMin wtMax f k (acc + pow) (2 * pow) (wt + 1) .one
      | false => false
  | k + 1, acc, pow, wt, .node l r =>
    if wt > wtMax || wt + (k + 1) < wtMin then true
    else
      match BTree.forallAliveWeight wtMin wtMax f k acc (2 * pow) wt l with
      | true => BTree.forallAliveWeight wtMin wtMax f k (acc + pow) (2 * pow) (wt + 1) r
      | false => false

private theorem forallAliveWeight_sound (wtMin wtMax : Nat) (f : Nat → Bool) :
    ∀ (k acc pow wt : Nat) (t : BTree),
      BTree.forallAliveWeight wtMin wtMax f k acc pow wt t = true →
      ∀ r < 2 ^ k, t.get k r = true →
        wtMin ≤ wt + popcountNat k r → wt + popcountNat k r ≤ wtMax →
        f (acc + r * pow) = true
  | _, _, _, _, .zero, _, _, _, hget, _, _ => by simp [BTree.get] at hget
  | 0, acc, _, wt, .one, h, r, hr, _, hlo, hhi => by
    have hr0 : r = 0 := by simpa using hr
    subst hr0
    simp only [popcountNat, Nat.add_zero] at hlo hhi
    simp only [BTree.forallAliveWeight, hlo, hhi, decide_true, Bool.and_self, ↓reduceIte] at h
    simpa using h
  | 0, _, _, _, .node _ _, _, _, _, hget, _, _ => by simp [BTree.get] at hget
  | k + 1, acc, pow, wt, .one, h, r, hr, _, hlo, hhi => by
    have hpow : 2 ^ (k + 1) = 2 * 2 ^ k := by rw [Nat.pow_succ, Nat.mul_comm]
    have hr' : r / 2 < 2 ^ k := by rw [hpow] at hr; omega
    have hpc_le : popcountNat (k + 1) r ≤ k + 1 := popcountNat_le (k + 1) r
    have hnot_prune : (wt > wtMax || wt + (k + 1) < wtMin) = false := by
      have h1 : ¬ (wt > wtMax) := by omega
      have h2 : ¬ (wt + (k + 1) < wtMin) := by omega
      simp [h1, h2]
    simp only [BTree.forallAliveWeight, hnot_prune, Bool.false_eq_true, ↓reduceIte] at h
    cases hl : BTree.forallAliveWeight wtMin wtMax f k acc (2 * pow) wt .one
    · simp [hl] at h
    · simp only [hl] at h
      by_cases hrm : r % 2 = 0
      · have hpc : popcountNat (k + 1) r = popcountNat k (r / 2) := by simp [popcountNat, hrm]
        rw [hpc] at hlo hhi
        have ih := forallAliveWeight_sound wtMin wtMax f k acc (2 * pow) wt .one hl (r / 2) hr' rfl hlo hhi
        have heq : acc + r / 2 * (2 * pow) = acc + r * pow := by
          have h1 : r / 2 * (2 * pow) = (2 * (r / 2)) * pow := by
            rw [Nat.mul_comm 2 (r / 2), Nat.mul_assoc]
          have h2 : 2 * (r / 2) = r := by omega
          rw [h1, h2]
        rwa [heq] at ih
      · have hr1 : r % 2 = 1 := by omega
        have hpc : popcountNat (k + 1) r = 1 + popcountNat k (r / 2) := by simp [popcountNat, hr1]
        rw [hpc] at hlo hhi
        have ih := forallAliveWeight_sound wtMin wtMax f k (acc + pow) (2 * pow) (wt + 1) .one h
          (r / 2) hr' rfl (by omega) (by omega)
        have heq : acc + pow + r / 2 * (2 * pow) = acc + r * pow := by
          have h1 : r / 2 * (2 * pow) = (2 * (r / 2)) * pow := by
            rw [Nat.mul_comm 2 (r / 2), Nat.mul_assoc]
          have h2 : 2 * (r / 2) + 1 = r := by omega
          have h3 : pow + (2 * (r / 2)) * pow = (2 * (r / 2) + 1) * pow := by
            rw [Nat.add_mul, Nat.one_mul, Nat.add_comm]
          rw [h1, Nat.add_assoc, h3, h2]
        rwa [heq] at ih
  | k + 1, acc, pow, wt, .node l r_tr, h, r, hr, hget, hlo, hhi => by
    have hpow : 2 ^ (k + 1) = 2 * 2 ^ k := by rw [Nat.pow_succ, Nat.mul_comm]
    have hr' : r / 2 < 2 ^ k := by rw [hpow] at hr; omega
    have hpc_le : popcountNat (k + 1) r ≤ k + 1 := popcountNat_le (k + 1) r
    have hnot_prune : (wt > wtMax || wt + (k + 1) < wtMin) = false := by
      have h1 : ¬ (wt > wtMax) := by omega
      have h2 : ¬ (wt + (k + 1) < wtMin) := by omega
      simp [h1, h2]
    simp only [BTree.forallAliveWeight, hnot_prune, Bool.false_eq_true, ↓reduceIte] at h
    cases hl : BTree.forallAliveWeight wtMin wtMax f k acc (2 * pow) wt l
    · simp [hl] at h
    · simp only [hl] at h
      simp only [BTree.get] at hget
      by_cases hrm : r % 2 = 0
      · simp only [hrm, beq_self_eq_true, ↓reduceIte] at hget
        have hpc : popcountNat (k + 1) r = popcountNat k (r / 2) := by simp [popcountNat, hrm]
        rw [hpc] at hlo hhi
        have ih := forallAliveWeight_sound wtMin wtMax f k acc (2 * pow) wt l hl (r / 2) hr' hget hlo hhi
        have heq : acc + r / 2 * (2 * pow) = acc + r * pow := by
          have h1 : r / 2 * (2 * pow) = (2 * (r / 2)) * pow := by
            rw [Nat.mul_comm 2 (r / 2), Nat.mul_assoc]
          have h2 : 2 * (r / 2) = r := by omega
          rw [h1, h2]
        rwa [heq] at ih
      · have hr1 : r % 2 = 1 := by omega
        have h10 : (1 == 0) = false := rfl
        simp only [hr1, h10, Bool.false_eq_true, ↓reduceIte] at hget
        have hpc : popcountNat (k + 1) r = 1 + popcountNat k (r / 2) := by simp [popcountNat, hr1]
        rw [hpc] at hlo hhi
        have ih := forallAliveWeight_sound wtMin wtMax f k (acc + pow) (2 * pow) (wt + 1) r_tr h
          (r / 2) hr' hget (by omega) (by omega)
        have heq : acc + pow + r / 2 * (2 * pow) = acc + r * pow := by
          have h1 : r / 2 * (2 * pow) = (2 * (r / 2)) * pow := by
            rw [Nat.mul_comm 2 (r / 2), Nat.mul_assoc]
          have h2 : 2 * (r / 2) + 1 = r := by omega
          have h3 : pow + (2 * (r / 2)) * pow = (2 * (r / 2) + 1) * pow := by
            rw [Nat.add_mul, Nat.one_mul, Nat.add_comm]
          rw [h1, Nat.add_assoc, h3, h2]
        rwa [heq] at ih

theorem forallAliveWeight_all {n wtMin wtMax : Nat} {f : Nat → Bool} {t : BTree}
    (h : BTree.forallAliveWeight wtMin wtMax f n 0 1 0 t = true) :
    ∀ x < 2 ^ n, t.get n x = true →
      wtMin ≤ popcountNat n x → popcountNat n x ≤ wtMax → f x = true := by
  intro x hx hget hlo hhi
  simpa using forallAliveWeight_sound wtMin wtMax f n 0 1 0 t h x hx hget (by simpa using hlo) (by simpa using hhi)

/-- Check `D_2`-invariance of `t` across all `2^n` words in one binary recursion. -/
def checkD2InvRec (n : Nat) (t : BTree) : Nat → Nat → Bool
  | 0, x =>
    let b := t.get n x
    (t.get n (applyD2 n 1 x) == b) &&
    (t.get n (applyD2 n 2 x) == b) &&
    (t.get n (applyD2 n 3 x) == b)
  | k + 1, x =>
    match checkD2InvRec n t k (2 * x) with
    | true => checkD2InvRec n t k (2 * x + 1)
    | false => false

private theorem checkD2InvRec_spec (n : Nat) (t : BTree) :
    ∀ (k base : Nat), checkD2InvRec n t k base = true →
      ∀ rem < 2 ^ k, ∀ g < 4,
        t.get n (applyD2 n g (base * 2 ^ k + rem)) = t.get n (base * 2 ^ k + rem)
  | 0, base, h, rem, hrem, g, hg => by
    have hr0 : rem = 0 := by simpa using hrem
    subst hr0
    simp only [Nat.pow_zero, Nat.mul_one, Nat.add_zero]
    simp only [checkD2InvRec, Bool.and_eq_true, beq_iff_eq] at h
    match g with
    | 0 => rfl
    | 1 => exact h.1.1
    | 2 => exact h.1.2
    | 3 => exact h.2
    | g + 4 => omega
  | k + 1, base, h, rem, hrem, g, hg => by
    simp only [checkD2InvRec] at h
    cases hl : checkD2InvRec n t k (2 * base)
    · simp [hl] at h
    · simp only [hl] at h
      have hpow : 2 ^ (k + 1) = 2 * 2 ^ k := by rw [Nat.pow_succ, Nat.mul_comm]
      have hlt2 : rem < 2 * 2 ^ k := hpow ▸ hrem
      by_cases hside : rem < 2 ^ k
      · have ih := checkD2InvRec_spec n t k (2 * base) hl rem hside g hg
        have heq : 2 * base * 2 ^ k + rem = base * 2 ^ (k + 1) + rem := by
          rw [hpow, Nat.mul_comm 2 base, Nat.mul_assoc]
        rwa [heq] at ih
      · have hrem' : rem - 2 ^ k < 2 ^ k := by omega
        have ih := checkD2InvRec_spec n t k (2 * base + 1) h (rem - 2 ^ k) hrem' g hg
        have heq : (2 * base + 1) * 2 ^ k + (rem - 2 ^ k) = base * 2 ^ (k + 1) + rem := by
          rw [Nat.add_mul, Nat.one_mul, hpow, Nat.mul_comm 2 base, Nat.mul_assoc]
          omega
        rwa [heq] at ih

theorem checkD2Inv_sound {n : Nat} {t : BTree} (h : checkD2InvRec n t n 0 = true) :
    D2Inv n t := by
  intro x hx g hg
  simpa using checkD2InvRec_spec n t n 0 h x hx g hg

/-! ## 5. Code Transformations: Ball-Clique Peeling and `D_2`-Orbit Domination -/

private theorem isValidDeletionCode_filter {n s : Nat} (p : Nat → Bool) :
    ∀ {C : List Nat}, IsValidDeletionCode n s C → IsValidDeletionCode n s (C.filter p)
  | [], hC => hC
  | a :: as, hC => by
    have h_as : IsValidDeletionCode n s as :=
      ⟨fun x hx => hC.1 x (List.mem_cons_of_mem a hx),
       fun i j hi hj hij =>
         hC.2 (i + 1) (j + 1) (Nat.succ_lt_succ hi) (Nat.succ_lt_succ hj) (by omega)⟩
    have h_head : ∀ x ∈ as,
        a ≠ x ∧
        (∀ d, ¬ (InDelBall s (natToWord n a) d ∧ InDelBall s (natToWord n x) d)) ∧
        ¬ HasCommonSubseqAtLeast (n - s) (natToWord n a) (natToWord n x) := by
      intro x hx
      obtain ⟨k, hk, rfl⟩ := List.getElem_of_mem hx
      exact hC.2 0 (k + 1) (Nat.zero_lt_succ _) (Nat.succ_lt_succ hk) (by omega)
    have ih := isValidDeletionCode_filter p h_as
    cases hpa : p a
    · simpa [hpa] using ih
    · simp only [List.filter_cons, hpa, ↓reduceIte]
      refine ⟨fun x hx => ?_, fun i j hi hj hij => ?_⟩
      · rcases List.mem_cons.mp hx with rfl | hmem
        · exact hC.1 x (List.mem_cons_self ..)
        · exact ih.1 x hmem
      · cases i with
        | zero =>
          cases j with
          | zero => exact absurd rfl hij
          | succ j' =>
            have hj' : j' < (as.filter p).length := Nat.lt_of_succ_lt_succ hj
            have hmem : (as.filter p)[j'] ∈ as := (List.mem_filter.mp (List.getElem_mem hj')).1
            exact h_head _ hmem
        | succ i' =>
          cases j with
          | zero =>
            have hi' : i' < (as.filter p).length := Nat.lt_of_succ_lt_succ hi
            have hmem : (as.filter p)[i'] ∈ as := (List.mem_filter.mp (List.getElem_mem hi')).1
            have h0 := h_head _ hmem
            refine ⟨h0.1.symm, fun d ⟨h1, h2⟩ => h0.2.1 d ⟨h2, h1⟩, fun ⟨d, hl, h1, h2⟩ => h0.2.2 ⟨d, hl, h2, h1⟩⟩
          | succ j' =>
            exact ih.2 i' j' (Nat.lt_of_succ_lt_succ hi) (Nat.lt_of_succ_lt_succ hj) (by omega)

private theorem length_filter_add_not {α : Type} (p : α → Bool) :
    ∀ (L : List α), (L.filter p).length + (L.filter (fun x => !p x)).length = L.length
  | [] => rfl
  | a :: as => by
    have ih := length_filter_add_not p as
    cases hpa : p a <;> simp [hpa] <;> omega

/-- Peeling one insertion ball `I_s(z)` (`z < 2^(n-s)`) drops code size by at most `1`! -/
theorem peel_one_ball {n s : Nat} (hs : s ≤ n) (z : Nat) {C : List Nat}
    (hC : IsValidDeletionCode n s C) :
    ∃ C' : List Nat,
      IsValidDeletionCode n s C' ∧
      C.length ≤ 1 + C'.length ∧
      (∀ x ∈ C', x ∈ C ∧ isSubseqB (natToWord (n - s) z) (natToWord n x) = false) := by
  let inB (x : Nat) : Bool := isSubseqB (natToWord (n - s) z) (natToWord n x)
  let C' := C.filter (fun x => !inB x)
  have hle1 : (C.filter inB).length ≤ 1 := by
    apply filter_len_le_one_of_pairwise inB C
    intro i j hi hj hij hpi hpj
    have h1 : InDelBall s (natToWord n C[i]) (natToWord (n - s) z) :=
      ⟨isSubseqB_sound hpi, by rw [natToWord_length, natToWord_length]; omega⟩
    have h2 : InDelBall s (natToWord n C[j]) (natToWord (n - s) z) :=
      ⟨isSubseqB_sound hpj, by rw [natToWord_length, natToWord_length]; omega⟩
    exact (hC.2 i j hi hj hij).2.1 (natToWord (n - s) z) ⟨h1, h2⟩
  have hsum := length_filter_add_not inB C
  refine ⟨C', isValidDeletionCode_filter _ hC, by dsimp only [C']; omega, fun x hx => ?_⟩
  rw [List.mem_filter] at hx
  refine ⟨hx.1, ?_⟩
  cases h : inB x
  · exact h
  · simp [h] at hx

/-- Peeling a list of insertion balls `balls` drops code size by at most `balls.length`! -/
theorem peel_balls_list {n s : Nat} (hs : s ≤ n) :
    ∀ (balls : List Nat) {C : List Nat}, IsValidDeletionCode n s C →
      ∃ C' : List Nat,
        IsValidDeletionCode n s C' ∧
        C.length ≤ balls.length + C'.length ∧
        ∀ x ∈ C', (buildBallsComplTree n s balls).get n x = true := by
  intro balls C hC
  suffices h : ∀ (bs : List Nat) {D : List Nat}, IsValidDeletionCode n s D →
      ∃ D' : List Nat, IsValidDeletionCode n s D' ∧ D.length ≤ bs.length + D'.length ∧
        ∀ x ∈ D', bs.all (fun z => !isSubseqB (natToWord (n - s) z) (natToWord n x)) = true by
    obtain ⟨C', hC', hlen, hall⟩ := h balls hC
    refine ⟨C', hC', hlen, fun x hx => ?_⟩
    rw [buildBallsComplTree_get n s balls (hC'.1 x hx)]
    exact hall x hx
  intro bs
  induction bs with
  | nil =>
    intro D hD
    exact ⟨D, hD, by simp, fun _ _ => rfl⟩
  | cons z zs ih =>
    intro D hD
    obtain ⟨D1, hD1, hlen1, hmem1⟩ := peel_one_ball hs z hD
    obtain ⟨D2, hD2, hlen2, hmem2⟩ := ih hD1
    -- Actually `D2` needs `z` excluded too: filter `D2` or maintain subset invariant!
    -- Even cleaner: filter `D` directly in one pass using `D2 ⊆ D1`!
    -- Wait: let's prove `D' ⊆ D` in the induction!
    have hstrong : ∀ (ls : List Nat) {E : List Nat}, IsValidDeletionCode n s E →
        ∃ E' : List Nat, IsValidDeletionCode n s E' ∧ E.length ≤ ls.length + E'.length ∧
          (∀ x ∈ E', x ∈ E) ∧
          (∀ x ∈ E', ls.all (fun w => !isSubseqB (natToWord (n - s) w) (natToWord n x)) = true) := by
      intro ls
      induction ls with
      | nil =>
        intro E hE
        exact ⟨E, hE, by simp, fun _ hx => hx, fun _ _ => rfl⟩
      | cons w ws ihw =>
        intro E hE
        obtain ⟨E1, hE1, hl1, hm1⟩ := peel_one_ball hs w hE
        obtain ⟨E2, hE2, hl2, hsub2, hm2⟩ := ihw hE1
        refine ⟨E2, hE2, by simp only [List.length_cons]; omega,
          fun x hx => (hm1 x (hsub2 x hx)).1, fun x hx => ?_⟩
        simp only [List.all_cons, Bool.and_eq_true, Bool.not_eq_true']
        exact ⟨(hm1 x (hsub2 x hx)).2, hm2 x hx⟩
    obtain ⟨E', hE', hlE, _, hmE⟩ := hstrong (z :: zs) hD
    exact ⟨E', hE', hlE, hmE⟩

/-- Single-vertex domination swap (`y ↦ x`): preserves code validity and EXACT length! -/
theorem peel_dom_single {n s x y : Nat} (hs : s ≤ n) (P : Nat → Prop)
    (hx_lt : x < 2 ^ n) (hxP : P x) (hxy_ne : x ≠ y)
    (hxy_edge : HasEdge n s x y)
    (hdom : ∀ z, P z → HasEdge n s x z → HasEdge n s y z)
    {C : List Nat} (hC : IsValidDeletionCode n s C) (hCP : ∀ u ∈ C, P u) :
    ∃ C' : List Nat,
      IsValidDeletionCode n s C' ∧
      C'.length = C.length ∧
      (∀ u ∈ C', P u ∧ u ≠ y) := by
  let f (u : Nat) : Nat := if u = y then x else u
  let C' := C.map f
  refine ⟨C', ?_, List.length_map .., ?_⟩
  · refine ⟨?_, ?_⟩
    · intro u hu
      rw [List.mem_map] at hu
      rcases hu with ⟨a, ha, rfl⟩
      by_cases hay : a = y
      · simp [f, hay, hx_lt]
      · simp [f, hay, hC.1 a ha]
    · intro i j hi hj hij
      have hiC : i < C.length := by simpa [C'] using hi
      have hjC : j < C.length := by simpa [C'] using hj
      have hpair := hC.2 i j hiC hjC hij
      simp only [C', List.getElem_map]
      have hdisj : ∀ d, ¬ (InDelBall s (natToWord n (f C[i])) d ∧ InDelBall s (natToWord n (f C[j])) d) := by
        intro d ⟨hd1, hd2⟩
        by_cases hiy : C[i] = y <;> by_cases hjy : C[j] = y
        · exact hpair.1 (hiy.trans hjy.symm)
        · simp only [f, hiy, hjy, ↓reduceIte] at hd1 hd2
          have hedge_xj : HasEdge n s x C[j] := ⟨d, hd1, hd2⟩
          have hedge_yj : HasEdge n s y C[j] := hdom C[j] (hCP C[j] (List.getElem_mem hjC)) hedge_xj
          rw [← hiy] at hedge_yj
          rcases hedge_yj with ⟨d', hd'1, hd'2⟩
          exact hpair.2.1 d' ⟨hd'1, hd'2⟩
        · simp only [f, hiy, hjy, ↓reduceIte] at hd1 hd2
          have hedge_xi : HasEdge n s x C[i] := ⟨d, hd2, hd1⟩
          have hedge_yi : HasEdge n s y C[i] := hdom C[i] (hCP C[i] (List.getElem_mem hiC)) hedge_xi
          rw [← hjy] at hedge_yi
          rcases hedge_yi with ⟨d', hd'1, hd'2⟩
          exact hpair.2.1 d' ⟨hd'2, hd'1⟩
        · simp only [f, hiy, hjy, ↓reduceIte] at hd1 hd2
          exact hpair.2.1 d ⟨hd1, hd2⟩
      have hne_f : f C[i] ≠ f C[j] := by
        intro heq
        by_cases hiy : C[i] = y <;> by_cases hjy : C[j] = y
        · exact hpair.1 (hiy.trans hjy.symm)
        · simp only [f, hiy, hjy, ↓reduceIte] at heq
          have hedge : HasEdge n s C[i] C[j] := by
            rw [hiy, ← heq]; exact hasEdge_symm hxy_edge
          rcases hedge with ⟨d, hd1, hd2⟩
          exact hpair.2.1 d ⟨hd1, hd2⟩
        · simp only [f, hiy, hjy, ↓reduceIte] at heq
          have hedge : HasEdge n s C[i] C[j] := by
            rw [hjy, heq]; exact hxy_edge
          rcases hedge with ⟨d, hd1, hd2⟩
          exact hpair.2.1 d ⟨hd1, hd2⟩
        · simp only [f, hiy, hjy, ↓reduceIte] at heq
          exact hpair.1 heq
      have hlcs := (disjoint_delBall_iff_no_common_subseq hs
        (natToWord_length n (f C[i])) (natToWord_length n (f C[j]))).mp hdisj
      exact ⟨hne_f, hdisj, hlcs⟩
  · intro u hu
    rw [List.mem_map] at hu
    rcases hu with ⟨a, ha, rfl⟩
    by_cases hay : a = y
    · simp [f, hay, hxP, hxy_ne]
    · simp [f, hay, hCP a ha]

/-- Full `D_2`-orbit domination step: removes `{y, c(y), r(y), cr(y)}` from `t` preserving code length! -/
theorem peel_dom_orbit {n s x y : Nat} {t : BTree}
    (hs : s ≤ n) (hx_lt : x < 2 ^ n) (hy_lt : y < 2 ^ n)
    (ht_inv : D2Inv n t)
    (hx_alive : t.get n x = true)
    (hdisj_orb : x ≠ applyD2 n 0 y ∧ x ≠ applyD2 n 1 y ∧ x ≠ applyD2 n 2 y ∧ x ≠ applyD2 n 3 y)
    (hxy_edge : HasEdge n s x y)
    (hdom : ∀ z < 2 ^ n, t.get n z = true → HasEdge n s x z → HasEdge n s y z)
    {C : List Nat} (hC : IsValidDeletionCode n s C)
    (hCt : ∀ u ∈ C, t.get n u = true) :
    ∃ C' : List Nat,
      IsValidDeletionCode n s C' ∧
      C'.length = C.length ∧
      ∀ u ∈ C', (t.clearD2 n y).get n u = true := by
  -- Helper: for any `g < 4`, `applyD2 n g x` is disjoint from the whole orbit `D_2(y)`!
  have hgx_ne : ∀ g < 4, ∀ h < 4, applyD2 n g x ≠ applyD2 n h y := by
    intro g hg h hh heq
    have h1 := congrArg (applyD2 n g) heq
    rw [applyD2_involutive hx_lt, applyD2_comp hg hh hy_lt] at h1
    have hlt4 := xorD2_lt hg hh
    match hxgh : xorD2 g h with
    | 0 => exact hdisj_orb.1 (by rwa [hxgh] at h1)
    | 1 => exact hdisj_orb.2.1 (by rwa [hxgh] at h1)
    | 2 => exact hdisj_orb.2.2.1 (by rwa [hxgh] at h1)
    | 3 => exact hdisj_orb.2.2.2 (by rwa [hxgh] at h1)
    | m + 4 => rw [hxgh] at hlt4; omega
  -- Helper: `g(x)` dominates `g(y)` inside `t` for every `g < 4`!
  have hdom_g : ∀ g < 4, ∀ z < 2 ^ n, t.get n z = true →
      HasEdge n s (applyD2 n g x) z → HasEdge n s (applyD2 n g y) z := by
    intro g hg z hz htz hedge
    have h1 := hasEdge_applyD2 (g := g) hs (applyD2_lt hx_lt) hz hedge
    rw [applyD2_involutive hx_lt] at h1
    have hgz_alive : t.get n (applyD2 n g z) = true := by rw [ht_inv z hz g hg]; exact htz
    have h2 := hdom (applyD2 n g z) (applyD2_lt hz) hgz_alive h1
    have h3 := hasEdge_applyD2 (g := g) hs hy_lt (applyD2_lt hz) h2
    rwa [applyD2_involutive hz] at h3
  -- Apply `peel_dom_single` sequentially for `g = 0, 1, 2, 3`!
  let P0 (u : Nat) : Prop := u < 2 ^ n ∧ t.get n u = true
  let P1 (u : Nat) : Prop := P0 u ∧ u ≠ applyD2 n 0 y
  let P2 (u : Nat) : Prop := P1 u ∧ u ≠ applyD2 n 1 y
  let P3 (u : Nat) : Prop := P2 u ∧ u ≠ applyD2 n 2 y
  have hC0 : ∀ u ∈ C, P0 u := fun u hu => ⟨hC.1 u hu, hCt u hu⟩
  obtain ⟨C1, hC1, hlen1, hCP1⟩ := peel_dom_single hs P0
    (applyD2_lt (g := 0) hx_lt) ⟨applyD2_lt hx_lt, by rw [ht_inv x hx_lt 0 (by omega)]; exact hx_alive⟩
    (hgx_ne 0 (by omega) 0 (by omega))
    (hasEdge_applyD2 (g := 0) hs hx_lt hy_lt hxy_edge)
    (fun z hz he => hdom_g 0 (by omega) z hz.1 hz.2 he) hC hC0
  obtain ⟨C2, hC2, hlen2, hCP2⟩ := peel_dom_single hs P1
    (applyD2_lt (g := 1) hx_lt)
    ⟨⟨applyD2_lt hx_lt, by rw [ht_inv x hx_lt 1 (by omega)]; exact hx_alive⟩, hgx_ne 1 (by omega) 0 (by omega)⟩
    (hgx_ne 1 (by omega) 1 (by omega))
    (hasEdge_applyD2 (g := 1) hs hx_lt hy_lt hxy_edge)
    (fun z hz he => hdom_g 1 (by omega) z hz.1.1 hz.1.2 he) hC1 hCP1
  obtain ⟨C3, hC3, hlen3, hCP3⟩ := peel_dom_single hs P2
    (applyD2_lt (g := 2) hx_lt)
    ⟨⟨⟨applyD2_lt hx_lt, by rw [ht_inv x hx_lt 2 (by omega)]; exact hx_alive⟩,
      hgx_ne 2 (by omega) 0 (by omega)⟩, hgx_ne 2 (by omega) 1 (by omega)⟩
    (hgx_ne 2 (by omega) 2 (by omega))
    (hasEdge_applyD2 (g := 2) hs hx_lt hy_lt hxy_edge)
    (fun z hz he => hdom_g 2 (by omega) z hz.1.1.1 hz.1.1.2 he) hC2 hCP2
  obtain ⟨C4, hC4, hlen4, hCP4⟩ := peel_dom_single hs P3
    (applyD2_lt (g := 3) hx_lt)
    ⟨⟨⟨⟨applyD2_lt hx_lt, by rw [ht_inv x hx_lt 3 (by omega)]; exact hx_alive⟩,
      hgx_ne 3 (by omega) 0 (by omega)⟩, hgx_ne 3 (by omega) 1 (by omega)⟩, hgx_ne 3 (by omega) 2 (by omega)⟩
    (hgx_ne 3 (by omega) 3 (by omega))
    (hasEdge_applyD2 (g := 3) hs hx_lt hy_lt hxy_edge)
    (fun z hz he => hdom_g 3 (by omega) z hz.1.1.1.1 hz.1.1.1.2 he) hC3 hCP3
  refine ⟨C4, hC4, by omega, fun u hu => ?_⟩
  have hp := hCP4 u hu
  rw [BTree.get_clearD2 hy_lt hp.1.1.1.1.1 t]
  have h0 : (u == applyD2 n 0 y) = false := beq_false_of_ne hp.1.1.1.2
  have h1 : (u == applyD2 n 1 y) = false := beq_false_of_ne hp.1.1.2
  have h2 : (u == applyD2 n 2 y) = false := beq_false_of_ne hp.1.2
  have h3 : (u == applyD2 n 3 y) = false := beq_false_of_ne hp.2
  simp [h0, h1, h2, h3, hp.1.1.1.1.2]

/-! ## 6. Executable Pure-Kernel Domination Checker & Master `Peel + Schrijver θ'` Theorem -/

/-- Verify one `D_2`-orbit domination step `(y, x)` (removing `D_2(y)` because `x` dominates `y` in `t`)
    with `O(1)` Hamming-weight subtree pruning. -/
def checkDomStep (n s : Nat) (t : BTree) (step : Nat × Nat) : Bool :=
  let y := step.1
  let x := step.2
  let bound := 2 ^ n
  decide (x < bound) &&
  decide (y < bound) &&
  t.get n x &&
  !Nat.beq x (applyD2 n 0 y) &&
  !Nat.beq x (applyD2 n 1 y) &&
  !Nat.beq x (applyD2 n 2 y) &&
  !Nat.beq x (applyD2 n 3 y) &&
  canMatchNat (n + s) (n - s) s s x y &&
  let wx := popcountNat n x
  let wtMin := wx - s
  let wtMax := wx + s
  BTree.forallAliveWeight wtMin wtMax
    (fun z =>
      if Nat.beq y z || Nat.beq x z then true
      else if canMatchNat (n + s) (n - s) s s x z then
        canMatchNat (n + s) (n - s) s s y z
      else true)
    n 0 1 0 t

theorem checkDomStep_sound {n s : Nat} {t : BTree} {step : Nat × Nat}
    (hs : s ≤ n) (ht_inv : D2Inv n t) (hchk : checkDomStep n s t step = true)
    {C : List Nat} (hC : IsValidDeletionCode n s C) (hCt : ∀ u ∈ C, t.get n u = true) :
    D2Inv n (t.clearD2 n step.1) ∧
    ∃ C' : List Nat,
      IsValidDeletionCode n s C' ∧
      C'.length = C.length ∧
      ∀ u ∈ C', (t.clearD2 n step.1).get n u = true := by
  unfold checkDomStep at hchk
  dsimp only at hchk
  simp only [Bool.and_eq_true, Bool.not_eq_true', decide_eq_true_eq] at hchk
  rcases hchk with ⟨⟨⟨⟨⟨⟨⟨⟨hx_lt, hy_lt⟩, hx_alive⟩, hne0⟩, hne1⟩, hne2⟩, hne3⟩, hmatch⟩, hfor⟩
  have hdisj : step.2 ≠ applyD2 n 0 step.1 ∧ step.2 ≠ applyD2 n 1 step.1 ∧
      step.2 ≠ applyD2 n 2 step.1 ∧ step.2 ≠ applyD2 n 3 step.1 :=
    ⟨fun h => by rw [h, Nat.beq_refl] at hne0; exact Bool.noConfusion hne0,
     fun h => by rw [h, Nat.beq_refl] at hne1; exact Bool.noConfusion hne1,
     fun h => by rw [h, Nat.beq_refl] at hne2; exact Bool.noConfusion hne2,
     fun h => by rw [h, Nat.beq_refl] at hne3; exact Bool.noConfusion hne3⟩
  have hxy_edge : HasEdge n s step.2 step.1 := hasEdge_of_canMatch hs hmatch
  have hdom : ∀ z < 2 ^ n, t.get n z = true → HasEdge n s step.2 z → HasEdge n s step.1 z := by
    intro z hz htz hxz
    have hwt := popcount_diff_le_of_hasEdge hxz
    have hlo : popcountNat n step.2 - s ≤ popcountNat n z := by omega
    have hhi : popcountNat n z ≤ popcountNat n step.2 + s := by omega
    have hf := forallAliveWeight_all hfor z hz htz hlo hhi
    by_cases hyz : step.1 = z
    · subst hyz
      have hrefl : HasEdge n s step.1 step.1 := by
        obtain ⟨d, hlen, hsub⟩ := exists_subseq_of_length (v := natToWord n step.1) (k := n - s)
          (by rw [natToWord_length]; omega)
        exact ⟨d, ⟨hsub, by rw [natToWord_length, hlen]; omega⟩,
                  ⟨hsub, by rw [natToWord_length, hlen]; omega⟩⟩
      exact hrefl
    · by_cases hxz_eq : step.2 = z
      · rw [← hxz_eq]; exact hasEdge_symm hxy_edge
      · have hb1 : Nat.beq step.1 z = false := by
          cases hb : Nat.beq step.1 z
          · rfl
          · exact absurd (Nat.eq_of_beq_eq_true hb) hyz
        have hb2 : Nat.beq step.2 z = false := by
          cases hb : Nat.beq step.2 z
          · rfl
          · exact absurd (Nat.eq_of_beq_eq_true hb) hxz_eq
        have hcm_xz : canMatchNat (n + s) (n - s) s s step.2 z = true :=
          canMatch_of_hasEdge hs hxz
        simp only [hb1, hb2, Bool.or_self, Bool.false_eq_true, ↓reduceIte, hcm_xz] at hf
        exact hasEdge_of_canMatch hs hf
  exact ⟨clearD2_d2Inv hy_lt ht_inv,
    peel_dom_orbit hs hx_lt hy_lt ht_inv hx_alive hdisj hxy_edge hdom hC hCt⟩

/-- Execute and verify a sequence of `D_2`-orbit domination steps, returning the reduced core `BTree`.
    Chunk-splittable via `checkDomSteps_append`! -/
def checkDomSteps (n s : Nat) (t : BTree) : List (Nat × Nat) → Option BTree
  | [] => some t
  | step :: rest =>
    match checkDomStep n s t step with
    | true => checkDomSteps n s (t.clearD2 n step.1) rest
    | false => none

theorem checkDomSteps_append (n s : Nat) (t t1 t2 : BTree) (s1 s2 : List (Nat × Nat))
    (h1 : checkDomSteps n s t s1 = some t1)
    (h2 : checkDomSteps n s t1 s2 = some t2) :
    checkDomSteps n s t (s1 ++ s2) = some t2 := by
  induction s1 generalizing t with
  | nil =>
    simp only [checkDomSteps, Option.some.injEq] at h1
    subst h1
    exact h2
  | cons st rest ih =>
    simp only [List.cons_append, checkDomSteps] at h1 ⊢
    cases hc : checkDomStep n s t st
    · simp [hc] at h1
    · simp only [hc] at h1 ⊢
      exact ih (t.clearD2 n st.1) h1

theorem checkDomSteps_sound {n s : Nat} (hs : s ≤ n) :
    ∀ (steps : List (Nat × Nat)) (t tFinal : BTree),
      D2Inv n t →
      checkDomSteps n s t steps = some tFinal →
      ∀ {C : List Nat}, IsValidDeletionCode n s C → (∀ u ∈ C, t.get n u = true) →
        ∃ C' : List Nat,
          IsValidDeletionCode n s C' ∧
          C'.length = C.length ∧
          ∀ u ∈ C', tFinal.get n u = true
  | [], t, tFinal, _, hchk, C, hC, hCt => by
    simp only [checkDomSteps, Option.some.injEq] at hchk
    subst hchk
    exact ⟨C, hC, rfl, hCt⟩
  | step :: rest, t, tFinal, ht_inv, hchk, C, hC, hCt => by
    simp only [checkDomSteps] at hchk
    cases hc : checkDomStep n s t step
    · simp [hc] at hchk
    · simp only [hc] at hchk
      obtain ⟨ht'_inv, C1, hC1, hlen1, hC1t⟩ := checkDomStep_sound hs ht_inv hc hC hCt
      obtain ⟨C2, hC2, hlen2, hC2t⟩ := checkDomSteps_sound hs rest (t.clearD2 n step.1) tFinal ht'_inv hchk hC1 hC1t
      exact ⟨C2, hC2, by omega, hC2t⟩

/-- Pure state-transition apply for a list of `D_2`-orbit domination steps. -/
def applyDomSteps (n : Nat) (t : BTree) : List (Nat × Nat) → BTree
  | [] => t
  | step :: rest => applyDomSteps n (t.clearD2 n step.1) rest

/-- Fast Bool-only domination sequence checker (avoids `BTree` equality comparison in `rfl`!). -/
def checkDomStepsB (n s : Nat) (t : BTree) : List (Nat × Nat) → Bool
  | [] => true
  | step :: rest =>
    match checkDomStep n s t step with
    | true => checkDomStepsB n s (t.clearD2 n step.1) rest
    | false => false

theorem checkDomStepsB_append (n s : Nat) (t : BTree) (s1 s2 : List (Nat × Nat))
    (h1 : checkDomStepsB n s t s1 = true)
    (h2 : checkDomStepsB n s (applyDomSteps n t s1) s2 = true) :
    checkDomStepsB n s t (s1 ++ s2) = true := by
  induction s1 generalizing t with
  | nil => exact h2
  | cons st rest ih =>
    simp only [List.cons_append, checkDomStepsB] at h1 ⊢
    simp only [applyDomSteps] at h2
    cases hc : checkDomStep n s t st
    · simp [hc] at h1
    · simp only [hc] at h1 ⊢
      exact ih (t.clearD2 n st.1) h1 h2

theorem checkDomSteps_of_B (n s : Nat) :
    ∀ (t : BTree) (steps : List (Nat × Nat)),
      checkDomStepsB n s t steps = true →
      checkDomSteps n s t steps = some (applyDomSteps n t steps)
  | _, [], _ => rfl
  | t, step :: rest, h => by
    simp only [checkDomStepsB] at h
    simp only [checkDomSteps, applyDomSteps]
    cases hc : checkDomStep n s t step
    · simp [hc] at h
    · simp only [hc] at h ⊢
      exact checkDomSteps_of_B n s (t.clearD2 n step.1) rest h

/-- Verify that EVERY alive word in `coreTree` has its canonical `D_2` representative inside `orbTree`. -/
def checkTreeCoveredByOrbs (n : Nat) (coreTree : BTree) (orbTree : OrbTree) : Bool :=
  BTree.forallAliveWeight 0 n (fun x => (orbTree.get n (canonD2 n x).2).isSome) n 0 1 0 coreTree

theorem checkTreeCoveredByOrbs_sound {n : Nat} {coreTree : BTree} {orbTree : OrbTree}
    (h : checkTreeCoveredByOrbs n coreTree orbTree = true) :
    ∀ x < 2 ^ n, coreTree.get n x = true → (orbTree.get n (canonD2 n x).2).isSome = true := by
  intro x hx hget
  exact forallAliveWeight_all h x hx hget (Nat.zero_le _) (popcountNat_le n x)

/--
  MASTER THEOREM: Pure-Kernel Onion-Peeling + Schrijver θ' PSD Upper Bound for ALL `(n, s)` (`s ≤ n`)!
  1. Peels `balls.length` symbolic insertion-ball cliques (`cost = +balls.length`, `0` edge checks).
  2. Peels iterated `D_2`-orbit domination steps `domSteps` (`cost = +0`).
  3. Certifies the shrunken core via `SchrijverPSD.weak_duality_schrijver_psd_on` (`cost ≤ M_core`).
  Conclusion: `∀ C, IsValidDeletionCode n s C → C.length ≤ balls.length + M_core`!
-/
theorem weak_duality_peel_schrijver_psd {n s r0 r1 r2 r3 S T M_core : Nat}
    (hs : s ≤ n) (hS : 0 < S) (hbound : T < (M_core + 1) * S)
    (balls : List Nat) (domSteps : List (Nat × Nat))
    (orbs : List OrbEntry)
    (hinv0 : checkD2InvRec n (buildBallsComplTree n s balls) n 0 = true)
    (hpeel : checkDomStepsB n s (buildBallsComplTree n s balls) domSteps = true)
    (hdiag : orbs.all (checkOrbDiag n r0 r1 r2 r3 (Int.ofNat T - Int.ofNat S)) = true)
    (hcover : checkTreeCoveredByOrbs n (applyDomSteps n (buildBallsComplTree n s balls) domSteps) (buildOrbTree n orbs) = true)
    (hpairs : checkOrbTri n s (- Int.ofNat S) orbs = true)
    {C : List Nat} (hC : IsValidDeletionCode n s C) :
    C.length ≤ balls.length + M_core := by
  obtain ⟨C1, hC1, hlen1, hC1t⟩ := peel_balls_list hs balls hC
  have ht0_inv : D2Inv n (buildBallsComplTree n s balls) := checkD2Inv_sound hinv0
  have hpeel_opt := checkDomSteps_of_B n s (buildBallsComplTree n s balls) domSteps hpeel
  obtain ⟨C2, hC2, hlen2, hC2t⟩ := checkDomSteps_sound hs domSteps _ _ ht0_inv hpeel_opt hC1 hC1t
  have hmem : ∀ x ∈ C2, ((buildOrbTree n orbs).get n (canonD2 n x).2).isSome = true :=
    fun x hx => checkTreeCoveredByOrbs_sound hcover x (hC2.1 x hx) (hC2t x hx)
  have hcore_le : C2.length ≤ M_core :=
    weak_duality_schrijver_psd_on hs hS hbound orbs hdiag hpairs hC2 hmem
  omega

/-! ## 7. Flat-Tree Parallel Wave Domination (Eliminates Nested `clearD2` WHNF Blowup!) -/

theorem BTree.get_clearD2_imp {n y z : Nat} (hy : y < 2 ^ n) (hz : z < 2 ^ n) (t : BTree)
    (h : (t.clearD2 n y).get n z = true) :
    t.get n z = true ∧
    z ≠ applyD2 n 0 y ∧ z ≠ applyD2 n 1 y ∧ z ≠ applyD2 n 2 y ∧ z ≠ applyD2 n 3 y := by
  rw [BTree.get_clearD2 hy hz t] at h
  cases h0 : (z == applyD2 n 0 y) <;> cases h1 : (z == applyD2 n 1 y) <;>
  cases h2 : (z == applyD2 n 2 y) <;> cases h3 : (z == applyD2 n 3 y)
  all_goals
    simp only [h0, h1, h2, h3, Bool.or_true, Bool.or_false,
      Bool.false_eq_true, ↓reduceIte] at h
  exact ⟨h,
    fun he => by rw [he, beq_self_eq_true] at h0; exact Bool.noConfusion h0,
    fun he => by rw [he, beq_self_eq_true] at h1; exact Bool.noConfusion h1,
    fun he => by rw [he, beq_self_eq_true] at h2; exact Bool.noConfusion h2,
    fun he => by rw [he, beq_self_eq_true] at h3; exact Bool.noConfusion h3⟩

theorem applyDomSteps_sub (n : Nat) :
    ∀ (steps : List (Nat × Nat)) (t : BTree),
      (∀ st ∈ steps, st.1 < 2 ^ n) →
      ∀ z < 2 ^ n, (applyDomSteps n t steps).get n z = true → t.get n z = true
  | [], _, _, _, _, h => h
  | st :: rest, t, hlt, z, hz, h => by
    have hst : st.1 < 2 ^ n := hlt st (List.mem_cons_self ..)
    have hrest : ∀ q ∈ rest, q.1 < 2 ^ n := fun q hq => hlt q (List.mem_cons_of_mem st hq)
    have h1 := applyDomSteps_sub n rest (t.clearD2 n st.1) hrest z hz h
    exact (BTree.get_clearD2_imp hst hz t h1).1

/-- Drop elements from `w` up to and including the first occurrence of `b`. -/
def dropUntil (b : Bool) : List Bool → Option (List Bool)
  | [] => none
  | c :: ws => if b == c then some ws else dropUntil b ws

theorem dropUntil_sound {b : Bool} {u : List Bool} :
    ∀ {wy wy' : List Bool}, dropUntil b wy = some wy' → IsSubseq u wy' → IsSubseq (b :: u) wy
  | [], _, h, _ => by simp [dropUntil] at h
  | c :: ws, wy', h, hsub => by
    simp only [dropUntil] at h
    cases hbc : (b == c)
    · simp only [hbc, Bool.false_eq_true, ↓reduceIte] at h
      exact .cons_drop c (dropUntil_sound h hsub)
    · simp only [hbc, ↓reduceIte, Option.some.injEq] at h
      subst h
      have heq : b = c := beq_iff_eq.mp hbc
      subst heq
      exact .cons_keep b hsub

private theorem isSubseq_eq_of_length_eq : ∀ {u v : List Bool}, IsSubseq u v → u.length = v.length → u = v
  | _, _, .nil, _ => rfl
  | _, _, .cons_keep b h, hl => by
    simp only [List.length_cons] at hl
    rw [isSubseq_eq_of_length_eq h (Nat.succ.inj hl)]
  | _, _, .cons_drop _ h, hl => by
    have hle := h.length_le
    simp only [List.length_cons] at hl
    omega

/--
  Fast algebraic ball-inclusion checker (`D_s(wx) ⊆ D_s(wy)`) for ALL `s ≤ n`!
  Checks EVERY `s`-deletion of `wx` is a subsequence of `wy` via greedy `dropUntil` in `O(C(n,s))`
  with ZERO tree traversals and ZERO `canMatchNat` calls (~500× faster & ~3000× less RAM)!
-/
def checkSubBall : Nat → List Bool → List Bool → Bool
  | 0, wx, wy => isSubseqB wx wy
  | _ + 1, [], _ => true
  | s + 1, b :: wx, wy =>
    match checkSubBall s wx wy with
    | false => false
    | true =>
      if wx.length < s + 1 then true
      else match dropUntil b wy with
        | none => false
        | some wy' => checkSubBall (s + 1) wx wy'

theorem checkSubBall_sound : ∀ (s : Nat) (wx wy : List Bool),
    checkSubBall s wx wy = true →
    ∀ d : List Bool, IsSubseq d wx → d.length + s = wx.length → IsSubseq d wy
  | 0, wx, wy, h, d, hd, hlen => by
    have heq : d = wx := isSubseq_eq_of_length_eq hd (by omega)
    subst heq
    exact isSubseqB_sound (by simpa [checkSubBall] using h)
  | s + 1, [], _, _, d, _, hlen => by
    simp at hlen
  | s + 1, b :: wx, wy, h, d, hd, hlen => by
    simp only [checkSubBall] at h
    cases hdrop : checkSubBall s wx wy
    · simp [hdrop] at h
    · simp only [hdrop] at h
      cases hd with
      | cons_drop _ h' =>
        simp only [List.length_cons] at hlen
        exact checkSubBall_sound s wx wy hdrop d h' (by omega)
      | cons_keep _ h' =>
        simp only [List.length_cons] at hlen
        have hnotlt : ¬ (wx.length < s + 1) := by omega
        simp only [hnotlt, ↓reduceIte] at h
        cases hdu : dropUntil b wy with
        | none => simp [hdu] at h
        | some wy' =>
          simp only [hdu] at h
          rename_i d'
          have hd' : IsSubseq d' wy' := checkSubBall_sound (s + 1) wx wy' h d' h' (by omega)
          exact dropUntil_sound hdu hd'

/-- Check ONE step `(y, x)` of a parallel domination wave on FIXED literal trees `tBefore` and `tAfter`.
    Fast path: if `D_s(x) ⊆ D_s(y)` (`checkSubBall = true`, covers 100% of `(10,2)` and 94% of `(11,3)`!),
    certifies `N[x] ⊆ N[y]` algebraically in <1ms with ZERO tree scan!
    Fallback path: scans only Hamming-weight-compatible alive leaves of `tBefore`. -/
def checkDomWaveStep (n s : Nat) (tBefore tAfter : BTree) (step : Nat × Nat) : Bool :=
  let y := step.1
  let x := step.2
  let bound := 2 ^ n
  decide (x < bound) &&
  decide (y < bound) &&
  tAfter.get n x &&
  if checkSubBall s (natToWord n x) (natToWord n y) then true
  else
    canMatchNat (n + s) (n - s) s s x y &&
    let wx := popcountNat n x
    BTree.forallAliveWeight (wx - s) (wx + s)
      (fun z =>
        if Nat.beq y z || Nat.beq x z then true
        else if canMatchNat (n + s) (n - s) s s x z then
          canMatchNat (n + s) (n - s) s s y z
        else true)
      n 0 1 0 tBefore

private theorem checkDomWave_aux {n s : Nat} (hs : s ≤ n) (tBefore tAfter : BTree) :
    ∀ (wave : List (Nat × Nat)) (tCur : BTree),
      D2Inv n tCur →
      (∀ z < 2 ^ n, tCur.get n z = true → tBefore.get n z = true) →
      applyDomSteps n tCur wave = tAfter →
      (∀ st ∈ wave, checkDomWaveStep n s tBefore tAfter st = true) →
      ∀ {C : List Nat}, IsValidDeletionCode n s C → (∀ u ∈ C, tCur.get n u = true) →
        D2Inv n tAfter ∧
        ∃ C' : List Nat,
          IsValidDeletionCode n s C' ∧
          C'.length = C.length ∧
          ∀ u ∈ C', tAfter.get n u = true
  | [], tCur, hinv, _, heq, _, C, hC, hCt => by
    simp only [applyDomSteps] at heq
    subst heq
    exact ⟨hinv, C, hC, rfl, hCt⟩
  | step :: rest, tCur, hinv, hsub, heq, hall, C, hC, hCt => by
    have hst := hall step (List.mem_cons_self ..)
    have hrest_all : ∀ q ∈ rest, checkDomWaveStep n s tBefore tAfter q = true :=
      fun q hq => hall q (List.mem_cons_of_mem step hq)
    have hrest_lt : ∀ q ∈ rest, q.1 < 2 ^ n := by
      intro q hq
      have hqchk := hrest_all q hq
      unfold checkDomWaveStep at hqchk
      dsimp only at hqchk
      simp only [Bool.and_eq_true, decide_eq_true_eq] at hqchk
      exact hqchk.1.1.2
    unfold checkDomWaveStep at hst
    dsimp only at hst
    simp only [Bool.and_eq_true, decide_eq_true_eq] at hst
    rcases hst with ⟨⟨⟨hx_lt, hy_lt⟩, hx_after⟩, hdom_body⟩
    have hx_cl : (tCur.clearD2 n step.1).get n step.2 = true := by
      have hsub_rest := applyDomSteps_sub n rest (tCur.clearD2 n step.1) hrest_lt step.2 hx_lt
      rw [← heq] at hx_after
      exact hsub_rest hx_after
    obtain ⟨hx_alive, hne0, hne1, hne2, hne3⟩ := BTree.get_clearD2_imp hy_lt hx_lt tCur hx_cl
    -- Extract BOTH `hxy_edge` and `hdom` from either the fast `checkSubBall` path or the tree-scan fallback!
    have h_edge_dom : HasEdge n s step.2 step.1 ∧
        (∀ z < 2 ^ n, tCur.get n z = true → HasEdge n s step.2 z → HasEdge n s step.1 z) := by
      cases hsb : checkSubBall s (natToWord n step.2) (natToWord n step.1)
      · simp only [hsb, Bool.false_eq_true, ↓reduceIte, Bool.and_eq_true] at hdom_body
        rcases hdom_body with ⟨hmatch, hfor⟩
        have hxy_edge : HasEdge n s step.2 step.1 := hasEdge_of_canMatch hs hmatch
        refine ⟨hxy_edge, ?_⟩
        intro z hz htz hxz
        have htz_bef : tBefore.get n z = true := hsub z hz htz
        have hwt := popcount_diff_le_of_hasEdge hxz
        have hf := forallAliveWeight_all hfor z hz htz_bef (by omega) (by omega)
        by_cases hyz : step.1 = z
        · subst hyz
          obtain ⟨d, hlen, hsubd⟩ := exists_subseq_of_length (v := natToWord n step.1) (k := n - s)
            (by rw [natToWord_length]; omega)
          exact ⟨d, ⟨hsubd, by rw [natToWord_length, hlen]; omega⟩,
                    ⟨hsubd, by rw [natToWord_length, hlen]; omega⟩⟩
        · by_cases hxz_eq : step.2 = z
          · rw [← hxz_eq]; exact hasEdge_symm hxy_edge
          · have hb1 : Nat.beq step.1 z = false := by
              cases hb : Nat.beq step.1 z
              · rfl
              · exact absurd (Nat.eq_of_beq_eq_true hb) hyz
            have hb2 : Nat.beq step.2 z = false := by
              cases hb : Nat.beq step.2 z
              · rfl
              · exact absurd (Nat.eq_of_beq_eq_true hb) hxz_eq
            have hcm_xz : canMatchNat (n + s) (n - s) s s step.2 z = true :=
              canMatch_of_hasEdge hs hxz
            simp only [hb1, hb2, Bool.or_self, Bool.false_eq_true, ↓reduceIte, hcm_xz] at hf
            exact hasEdge_of_canMatch hs hf
      · -- Fast algebraic path: `D_s(x) ⊆ D_s(y)` implies BOTH `x ~ y` AND `N[x] ⊆ N[y]` universally!
        have hsub_ball : ∀ d, InDelBall s (natToWord n step.2) d → InDelBall s (natToWord n step.1) d := by
          intro d ⟨hdx, hlen⟩
          refine ⟨checkSubBall_sound s (natToWord n step.2) (natToWord n step.1) hsb d hdx hlen, ?_⟩
          rw [natToWord_length] at hlen ⊢
          exact hlen
        have hxy_edge : HasEdge n s step.2 step.1 := by
          obtain ⟨d, hlen, hsubd⟩ := exists_subseq_of_length (v := natToWord n step.2) (k := n - s)
            (by rw [natToWord_length]; omega)
          have hbx : InDelBall s (natToWord n step.2) d := ⟨hsubd, by rw [natToWord_length, hlen]; omega⟩
          exact ⟨d, hbx, hsub_ball d hbx⟩
        refine ⟨hxy_edge, fun z _ _ ⟨d, hdx, hdz⟩ => ⟨d, hsub_ball d hdx, hdz⟩⟩
    obtain ⟨hxy_edge, hdom⟩ := h_edge_dom
    obtain ⟨C1, hC1, hlen1, hC1t⟩ :=
      peel_dom_orbit hs hx_lt hy_lt hinv hx_alive ⟨hne0, hne1, hne2, hne3⟩ hxy_edge hdom hC hCt
    have hinv' : D2Inv n (tCur.clearD2 n step.1) := clearD2_d2Inv hy_lt hinv
    have hsub' : ∀ z < 2 ^ n, (tCur.clearD2 n step.1).get n z = true → tBefore.get n z = true :=
      fun z hz hcl => hsub z hz (BTree.get_clearD2_imp hy_lt hz tCur hcl).1
    obtain ⟨hinv_after, C2, hC2, hlen2, hC2t⟩ :=
      checkDomWave_aux hs tBefore tAfter rest (tCur.clearD2 n step.1) hinv' hsub' heq hrest_all hC1 hC1t
    exact ⟨hinv_after, C2, hC2, by omega, hC2t⟩

/-- Verify one parallel domination wave `tBefore → tAfter` in flat O(1) tree depth! -/
theorem peel_dom_wave_sound {n s : Nat} (hs : s ≤ n) {tBefore tAfter : BTree}
    (wave : List (Nat × Nat))
    (hinv : D2Inv n tBefore)
    (happly : applyDomSteps n tBefore wave = tAfter)
    (hwave : ∀ st ∈ wave, checkDomWaveStep n s tBefore tAfter st = true)
    {C : List Nat} (hC : IsValidDeletionCode n s C) (hCt : ∀ u ∈ C, tBefore.get n u = true) :
    D2Inv n tAfter ∧
    ∃ C' : List Nat,
      IsValidDeletionCode n s C' ∧
      C'.length = C.length ∧
      ∀ u ∈ C', tAfter.get n u = true :=
  checkDomWave_aux hs tBefore tAfter wave tBefore hinv (fun _ _ h => h) happly hwave hC hCt

/--
  FAST FLAT-TREE MASTER THEOREM (1-Wave): `balls` -> `initTree` -> `wave1` -> `coreTree` -> `SchrijverPSD`!
  Uses pre-reduced literal `BTree`s so `lake build` and `leanchecker` take < 3 seconds on the peel step!
-/
theorem weak_duality_peel_wave1_psd {n s r0 r1 r2 r3 S T M_core : Nat}
    (hs : s ≤ n) (hS : 0 < S) (hbound : T < (M_core + 1) * S)
    (balls : List Nat) (initTree coreTree : BTree)
    (wave1 : List (Nat × Nat)) (orbs : List OrbEntry)
    (hinit : buildBallsComplTree n s balls = initTree)
    (hinv0 : checkD2InvRec n initTree n 0 = true)
    (happly1 : applyDomSteps n initTree wave1 = coreTree)
    (hwave1 : ∀ st ∈ wave1, checkDomWaveStep n s initTree coreTree st = true)
    (hdiag : orbs.all (checkOrbDiag n r0 r1 r2 r3 (Int.ofNat T - Int.ofNat S)) = true)
    (hcover : checkTreeCoveredByOrbs n coreTree (buildOrbTree n orbs) = true)
    (hpairs : checkOrbTri n s (- Int.ofNat S) orbs = true)
    {C : List Nat} (hC : IsValidDeletionCode n s C) :
    C.length ≤ balls.length + M_core := by
  obtain ⟨C1, hC1, hlen1, hC1t⟩ := peel_balls_list hs balls hC
  rw [hinit] at hC1t
  have ht0_inv : D2Inv n initTree := checkD2Inv_sound hinv0
  obtain ⟨_, C2, hC2, hlen2, hC2t⟩ := peel_dom_wave_sound hs wave1 ht0_inv happly1 hwave1 hC1 hC1t
  have hmem : ∀ x ∈ C2, ((buildOrbTree n orbs).get n (canonD2 n x).2).isSome = true :=
    fun x hx => checkTreeCoveredByOrbs_sound hcover x (hC2.1 x hx) (hC2t x hx)
  have hcore_le : C2.length ≤ M_core :=
    weak_duality_schrijver_psd_on hs hS hbound orbs hdiag hpairs hC2 hmem
  omega

/--
  FAST FLAT-TREE MASTER THEOREM (2-Wave, e.g. `(11, 3)`): `balls` -> `initTree` -> `wave1` -> `midTree` -> `wave2` -> `coreTree` -> `SchrijverPSD`!
-/
theorem weak_duality_peel_wave2_psd {n s r0 r1 r2 r3 S T M_core : Nat}
    (hs : s ≤ n) (hS : 0 < S) (hbound : T < (M_core + 1) * S)
    (balls : List Nat) (initTree midTree coreTree : BTree)
    (wave1 wave2 : List (Nat × Nat)) (orbs : List OrbEntry)
    (hinit : buildBallsComplTree n s balls = initTree)
    (hinv0 : checkD2InvRec n initTree n 0 = true)
    (happly1 : applyDomSteps n initTree wave1 = midTree)
    (hwave1 : ∀ st ∈ wave1, checkDomWaveStep n s initTree midTree st = true)
    (happly2 : applyDomSteps n midTree wave2 = coreTree)
    (hwave2 : ∀ st ∈ wave2, checkDomWaveStep n s midTree coreTree st = true)
    (hdiag : orbs.all (checkOrbDiag n r0 r1 r2 r3 (Int.ofNat T - Int.ofNat S)) = true)
    (hcover : checkTreeCoveredByOrbs n coreTree (buildOrbTree n orbs) = true)
    (hpairs : checkOrbTri n s (- Int.ofNat S) orbs = true)
    {C : List Nat} (hC : IsValidDeletionCode n s C) :
    C.length ≤ balls.length + M_core := by
  obtain ⟨C1, hC1, hlen1, hC1t⟩ := peel_balls_list hs balls hC
  rw [hinit] at hC1t
  have ht0_inv : D2Inv n initTree := checkD2Inv_sound hinv0
  obtain ⟨hmid_inv, C2, hC2, hlen2, hC2t⟩ := peel_dom_wave_sound hs wave1 ht0_inv happly1 hwave1 hC1 hC1t
  obtain ⟨_, C3, hC3, hlen3, hC3t⟩ := peel_dom_wave_sound hs wave2 hmid_inv happly2 hwave2 hC2 hC2t
  have hmem : ∀ x ∈ C3, ((buildOrbTree n orbs).get n (canonD2 n x).2).isSome = true :=
    fun x hx => checkTreeCoveredByOrbs_sound hcover x (hC3.1 x hx) (hC3t x hx)
  have hcore_le : C3.length ≤ M_core :=
    weak_duality_schrijver_psd_on hs hS hbound orbs hdiag hpairs hC3 hmem
  omega

end DeletionCode.PeelReduce
