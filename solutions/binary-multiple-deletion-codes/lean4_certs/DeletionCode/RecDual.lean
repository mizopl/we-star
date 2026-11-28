/-
  DeletionCode/RecDual.lean — Universal Recursive Block-Matrix Dual Cutting-Plane Verifier
  for ALL Binary `s`-Deletion-Correcting Codes (`n, s` with `s ≤ n`).

  Exploits the exact overlap-free 2×2 block recursion of the `(n, s)` deletion-ball incidence
  matrix `A_{n,s} ∈ {0,1}^{2^(n-s) × 2^n}` (rows and columns indexed LSB-first by `STree`):

      A_{n+1, s} = [ A_{n, s}        A_{n, s-1}^{(0)} ]
                   [ A_{n, s-1}^{(1)} A_{n, s}        ]

  with base cases `A_{n, 0} = I_{2^n}` and `A_{s, s} = 1_{1 × 2^s}`.
  Its transpose evaluates `A_{n,s}^T y` recursively with O(1) `.zero` subtree pruning:
    1. Eliminates flat `bTree` ball witness tables, `del2Nat`/`del3Nat`, and `dedupNat`.
    2. Reuses the exact same `evalDual` operator for rank-1 Chvátal-Gomory cuts (`M23`, `CG25`, ...).
    3. Verifies non-ball cliques (`CLQ`) via zero-witness recursive `canMatchList` (`LCS ≥ n - s`).
    4. Checks all `2^n` words under `D_2 = <c, r>` in one structural `STree` pass (`checkSym2Rev`).

  Zero Mathlib, zero sorryAx, zero native_decide / Lean.ofReduceBool.
-/
import DeletionCode.Basic
import DeletionCode.DualLP
import DeletionCode.CutDual

set_option maxRecDepth 32768

namespace DeletionCode.RecDual

open DeletionCode
open DeletionCode.DualLP
open DeletionCode.CutDual

/-! ## 1. Boolean Subsequence Oracle (`isSubseqB`) and Exact Equivalence with `IsSubseq` -/

/-- Exact greedy-match Boolean subsequence checker matching the block recursion of `A_{n,s}`. -/
def isSubseqB : List Bool → List Bool → Bool
  | [], _ => true
  | _ :: _, [] => false
  | a :: u, b :: v => if a == b then isSubseqB u v else isSubseqB (a :: u) v

theorem isSubseq_of_cons_left {a : Bool} {u v : List Bool} (h : IsSubseq (a :: u) v) :
    IsSubseq u v :=
  IsSubseq.trans (.cons_drop a (IsSubseq.refl u)) h

theorem isSubseqB_sound : ∀ {u v : List Bool}, isSubseqB u v = true → IsSubseq u v
  | [], v, _ => IsSubseq.nil_left v
  | _ :: _, [], h => by simp [isSubseqB] at h
  | a :: u, b :: v, h => by
    simp only [isSubseqB] at h
    cases hab : (a == b)
    · simp only [hab, Bool.false_eq_true, ↓reduceIte] at h
      exact .cons_drop b (isSubseqB_sound h)
    · simp only [hab, ↓reduceIte] at h
      have heq : a = b := beq_iff_eq.mp hab
      subst heq
      exact .cons_keep a (isSubseqB_sound h)

theorem isSubseqB_complete : ∀ {u v : List Bool}, IsSubseq u v → isSubseqB u v = true
  | _, _, .nil => rfl
  | _, _, .cons_keep b h => by
    simp only [isSubseqB, beq_self_eq_true, ↓reduceIte]
    exact isSubseqB_complete h
  | [], _, .cons_drop _ _ => rfl
  | a :: u, b :: v, .cons_drop _ h => by
    simp only [isSubseqB]
    cases hab : (a == b)
    · simp only [Bool.false_eq_true, ↓reduceIte]
      exact isSubseqB_complete h
    · simp only [↓reduceIte]
      exact isSubseqB_complete (isSubseq_of_cons_left h)

theorem isSubseqB_false_of_lt_len {u v : List Bool} (h : v.length < u.length) :
    isSubseqB u v = false := by
  cases hb : isSubseqB u v with
  | false => rfl
  | true =>
    have hle := (isSubseqB_sound hb).length_le
    omega

/-! ## 2. Sparse LSB-First Binary Trees (`STree`) with Exact `.zero` Pruning -/

/-- Sparse LSB-first binary tree over `Nat` (`.zero` represents an entire zero subtree). -/
inductive STree where
  | zero : STree
  | leaf (v : Nat) : STree
  | node (l r : STree) : STree

/-- Well-formedness predicate: depth-`k` sparse tree (structurally recursive on `t` so `.zero` reduces definitionally). -/
def STree.WF (k : Nat) (t : STree) : Prop :=
  match t with
  | .zero => True
  | .leaf _ => k = 0
  | .node l r => match k with | 0 => False | k' + 1 => l.WF k' ∧ r.WF k'
termination_by structural t

def STree.get (k : Nat) (t : STree) (x : Nat) : Nat :=
  match t with
  | .zero => 0
  | .leaf v => match k with | 0 => v | _ => 0
  | .node l r => match k with | 0 => 0 | k' + 1 => if x % 2 == 0 then l.get k' (x / 2) else r.get k' (x / 2)
termination_by structural t

def STree.sum (k : Nat) (t : STree) : Nat :=
  match t with
  | .zero => 0
  | .leaf v => match k with | 0 => v | _ => 0
  | .node l r => match k with | 0 => 0 | k' + 1 => l.sum k' + r.sum k'
termination_by structural t

def STree.mkNode : STree → STree → STree
  | .zero, .zero => .zero
  | l, r => .node l r

def STree.leftHalf : STree → STree
  | .zero => .zero
  | t => .node t .zero

def STree.rightHalf : STree → STree
  | .zero => .zero
  | t => .node .zero t

def STree.const : Nat → Nat → STree
  | _, 0 => .zero
  | 0, v => .leaf v
  | k + 1, v => let s := STree.const k v; .node s s

def STree.add : STree → STree → STree
  | .zero, t => t
  | t, .zero => t
  | .leaf a, .leaf b => .leaf (a + b)
  | .node l1 r1, .node l2 r2 => .node (l1.add l2) (r1.add r2)
  | t, _ => t

def STree.mapZero (f : Nat → Nat) : STree → STree
  | .zero => .zero
  | .leaf v => let fv := f v; if fv == 0 then .zero else .leaf fv
  | .node l r => STree.mkNode (l.mapZero f) (r.mapZero f)

def STree.comp : STree → STree
  | .zero => .zero
  | .leaf v => .leaf v
  | .node l r => .node r.comp l.comp

/-- Interleaves two depth-`k` trees into a depth-`(k+1)` tree putting `a` at MSB=0 and `b` at MSB=1. -/
def STree.zipLeaf : Nat → STree → STree → STree
  | _, .zero, .zero => .zero
  | 0, a, b => .node a b
  | k + 1, .node l1 r1, .node l2 r2 => .node (STree.zipLeaf k l1 l2) (STree.zipLeaf k r1 r2)
  | k + 1, .node l1 r1, .zero => .node (STree.zipLeaf k l1 .zero) (STree.zipLeaf k r1 .zero)
  | k + 1, .zero, .node l2 r2 => .node (STree.zipLeaf k .zero l2) (STree.zipLeaf k .zero r2)
  | _, t, _ => t

/-- Exact bit-reversal operator `P_r` on depth-`k` `STree`: `(t.rev k).get k x = t.get k (bitRev k x)`. -/
def STree.rev : Nat → STree → STree
  | _, .zero => .zero
  | 0, t => t
  | k + 1, .node l r => STree.zipLeaf k (STree.rev k l) (STree.rev k r)
  | _, t => t

/-- Single-pass lower-bound check `∀ x < 2^k, Lmin ≤ t.get k x` using primitive `Nat.ble`. -/
def STree.allGe (Lmin : Nat) (k : Nat) (t : STree) : Bool :=
  match t with
  | .zero => Nat.beq Lmin 0
  | .leaf v => match k with | 0 => Nat.ble Lmin v | _ => false
  | .node l r => match k with
    | 0 => false
    | k' + 1 => match l.allGe Lmin k' with | true => r.allGe Lmin k' | false => false
termination_by structural t

def STree.insertAdd (k x w : Nat) (t : STree) : STree :=
  match w with
  | 0 => t
  | w' + 1 =>
    match t, k with
    | .zero, 0 => .leaf (w' + 1)
    | .leaf v, 0 => .leaf (v + (w' + 1))
    | .zero, k' + 1 =>
      if x % 2 == 0 then .node (STree.insertAdd k' (x / 2) (w' + 1) .zero) .zero
      else .node .zero (STree.insertAdd k' (x / 2) (w' + 1) .zero)
    | .node l r, k' + 1 =>
      if x % 2 == 0 then .node (STree.insertAdd k' (x / 2) (w' + 1) l) r
      else .node l (STree.insertAdd k' (x / 2) (w' + 1) r)
    | _, _ => t

theorem STree.mkNode_wf {k : Nat} {l r : STree} (hl : l.WF k) (hr : r.WF k) :
    (STree.mkNode l r).WF (k + 1) := by
  cases l <;> cases r <;> first | exact trivial | exact ⟨hl, hr⟩

theorem STree.get_mkNode (k : Nat) (l r : STree) (x : Nat) :
    (STree.mkNode l r).get (k + 1) x =
      if x % 2 == 0 then l.get k (x / 2) else r.get k (x / 2) := by
  cases l <;> cases r
  · simp [STree.mkNode, STree.get]
  all_goals rfl

theorem STree.leftHalf_wf {k : Nat} {t : STree} (ht : t.WF k) :
    t.leftHalf.WF (k + 1) := by
  cases t
  · trivial
  · exact ⟨ht, trivial⟩
  · exact ⟨ht, trivial⟩

theorem STree.rightHalf_wf {k : Nat} {t : STree} (ht : t.WF k) :
    t.rightHalf.WF (k + 1) := by
  cases t
  · trivial
  · exact ⟨trivial, ht⟩
  · exact ⟨trivial, ht⟩

theorem STree.const_wf (k v : Nat) : (STree.const k v).WF k := by
  induction k with
  | zero => cases v <;> first | trivial | rfl
  | succ k' ih =>
    cases v with
    | zero => trivial
    | succ _ => exact ⟨ih, ih⟩

theorem STree.get_const (k v x : Nat) : (STree.const k v).get k x = v := by
  induction k generalizing x with
  | zero => cases v <;> rfl
  | succ k' ih =>
    cases v with
    | zero => rfl
    | succ _ =>
      simp only [STree.const, STree.get]
      split <;> exact ih (x / 2)

theorem STree.add_wf : ∀ {k : Nat} {t1 t2 : STree}, t1.WF k → t2.WF k → (t1.add t2).WF k
  | _, .zero, _, _, h2 => h2
  | _, .leaf _, .zero, h1, _ => h1
  | _, .node _ _, .zero, h1, _ => h1
  | 0, .leaf _, .leaf _, _, _ => rfl
  | k + 1, .node _ _, .node _ _, h1, h2 => ⟨STree.add_wf h1.1 h2.1, STree.add_wf h1.2 h2.2⟩
  | 0, .node _ _, .leaf _, h1, _ => False.elim h1
  | 0, .leaf _, .node _ _, _, h2 => False.elim h2
  | 0, .node _ _, .node _ _, h1, _ => False.elim h1
  | _ + 1, .leaf _, .leaf _, h1, _ => by cases h1
  | _ + 1, .leaf _, .node _ _, h1, _ => by cases h1
  | _ + 1, .node _ _, .leaf _, _, h2 => by cases h2

theorem STree.get_add : ∀ {k : Nat} {t1 t2 : STree}, t1.WF k → t2.WF k →
    ∀ x, (t1.add t2).get k x = t1.get k x + t2.get k x
  | _, .zero, _, _, _, _ => by simp [STree.add, STree.get]
  | _, .leaf _, .zero, _, _, _ => by simp [STree.add, STree.get]
  | _, .node _ _, .zero, _, _, _ => by simp [STree.add, STree.get]
  | 0, .leaf _, .leaf _, _, _, _ => rfl
  | k + 1, .node l1 r1, .node l2 r2, h1, h2, x => by
    simp only [STree.add, STree.get]
    split
    · exact STree.get_add h1.1 h2.1 (x / 2)
    · exact STree.get_add h1.2 h2.2 (x / 2)
  | 0, .node _ _, .leaf _, h1, _, _ => False.elim h1
  | 0, .leaf _, .node _ _, _, h2, _ => False.elim h2
  | 0, .node _ _, .node _ _, h1, _, _ => False.elim h1
  | _ + 1, .leaf _, .leaf _, h1, _, _ => by cases h1
  | _ + 1, .leaf _, .node _ _, h1, _, _ => by cases h1
  | _ + 1, .node _ _, .leaf _, _, h2, _ => by cases h2

theorem STree.mapZero_wf (f : Nat → Nat) : ∀ {k : Nat} {t : STree}, t.WF k → (t.mapZero f).WF k
  | _, .zero, _ => trivial
  | 0, .leaf _, _ => by
    simp only [STree.mapZero]
    split <;> first | trivial | rfl
  | k + 1, .node _ _, h => STree.mkNode_wf (STree.mapZero_wf f h.1) (STree.mapZero_wf f h.2)
  | 0, .node _ _, h => False.elim h
  | _ + 1, .leaf _, h => by cases h

theorem STree.get_mapZero {f : Nat → Nat} (hf0 : f 0 = 0) :
    ∀ {k : Nat} {t : STree}, t.WF k → ∀ x, (t.mapZero f).get k x = f (t.get k x)
  | _, .zero, _, _ => by simp [STree.mapZero, STree.get, hf0]
  | 0, .leaf v, _, _ => by
    simp only [STree.mapZero, STree.get]
    cases hfv : (f v == 0)
    · simp [STree.get]
    · simp only [↓reduceIte, STree.get]
      exact (beq_iff_eq.mp hfv).symm
  | k + 1, .node l r, h, x => by
    simp only [STree.mapZero, STree.get_mkNode, STree.get]
    split
    · exact STree.get_mapZero hf0 h.1 (x / 2)
    · exact STree.get_mapZero hf0 h.2 (x / 2)
  | 0, .node _ _, h, _ => False.elim h
  | _ + 1, .leaf _, h, _ => by cases h

theorem STree.comp_wf : ∀ {k : Nat} {t : STree}, t.WF k → t.comp.WF k
  | _, .zero, _ => trivial
  | 0, .leaf _, _ => rfl
  | k + 1, .node _ _, h => ⟨STree.comp_wf h.2, STree.comp_wf h.1⟩
  | 0, .node _ _, h => False.elim h
  | _ + 1, .leaf _, h => by cases h

theorem STree.get_comp : ∀ {k : Nat} {t : STree}, t.WF k →
    ∀ {x : Nat}, x < 2 ^ k → t.comp.get k x = t.get k (bitComp k x)
  | _, .zero, _, _, _ => rfl
  | 0, .leaf _, _, _, _ => rfl
  | k + 1, .node l r, h, x, hx => by
    have hpow : 2 ^ (k + 1) = 2 * 2 ^ k := by rw [Nat.pow_succ, Nat.mul_comm]
    have hlt_pow : x < 2 * 2 ^ k := hpow ▸ hx
    have hdiv_lt : x / 2 < 2 ^ k := by omega
    have hbc_succ : bitComp (k + 1) x = 2 * bitComp k (x / 2) + (1 - x % 2) := by
      unfold bitComp; rw [hpow]; omega
    have hmod_bc : bitComp (k + 1) x % 2 = 1 - x % 2 := by rw [hbc_succ]; omega
    have hdiv_bc : bitComp (k + 1) x / 2 = bitComp k (x / 2) := by rw [hbc_succ]; omega
    simp only [STree.comp, STree.get, hmod_bc, hdiv_bc]
    by_cases hev : x % 2 = 0
    · have h10 : (1 == 0) = false := rfl
      simp only [hev, beq_self_eq_true, ↓reduceIte, Nat.sub_zero, h10, Bool.false_eq_true]
      exact STree.get_comp h.2 hdiv_lt
    · have h1 : x % 2 = 1 := by omega
      have h10 : (1 == 0) = false := rfl
      simp only [h1, h10, Bool.false_eq_true, Nat.sub_self, beq_self_eq_true, ↓reduceIte]
      exact STree.get_comp h.1 hdiv_lt
  | 0, .node _ _, h, _, _ => False.elim h
  | _ + 1, .leaf _, h, _, _ => by cases h

private theorem mod_pow2_div2 (k x : Nat) : (x % 2 ^ (k + 1)) / 2 = (x / 2) % 2 ^ k := by
  have hpow : 2 ^ (k + 1) = 2 * 2 ^ k := by rw [Nat.pow_succ, Nat.mul_comm]
  have hpos : 0 < 2 ^ k := Nat.two_pow_pos k
  have hq := Nat.div_add_mod x (2 * 2 ^ k)
  have hlt := Nat.mod_lt x (show 0 < 2 * 2 ^ k by omega)
  have hx2 := Nat.div_add_mod x 2
  have hrem : (x % (2 * 2 ^ k)) % 2 < 2 := Nat.mod_lt _ (by omega)
  have hm1 : 2 * 2 ^ k * (x / (2 * 2 ^ k)) = 2 * (2 ^ k * (x / (2 * 2 ^ k))) := Nat.mul_assoc 2 _ _
  have hdiv2 : x / 2 = 2 ^ k * (x / (2 * 2 ^ k)) + (x % (2 * 2 ^ k)) / 2 := by omega
  have hlt2 : (x % (2 * 2 ^ k)) / 2 < 2 ^ k := by omega
  rw [hpow, hdiv2, Nat.mul_add_mod_self_left, Nat.mod_eq_of_lt hlt2]

private theorem mod_pow2_mod2 (k x : Nat) : (x % 2 ^ (k + 1)) % 2 = x % 2 := by
  have hpow : 2 ^ (k + 1) = 2 * 2 ^ k := by rw [Nat.pow_succ, Nat.mul_comm]
  have hq := Nat.div_add_mod x (2 * 2 ^ k)
  have hm : (2 * 2 ^ k) * (x / (2 * 2 ^ k)) = 2 * (2 ^ k * (x / (2 * 2 ^ k))) := Nat.mul_assoc 2 _ _
  have hx_eq : x = 2 * (2 ^ k * (x / (2 * 2 ^ k))) + x % (2 * 2 ^ k) := by omega
  rw [hpow]
  calc x % (2 * 2 ^ k) % 2
      = (2 * (2 ^ k * (x / (2 * 2 ^ k))) + x % (2 * 2 ^ k)) % 2 := (Nat.mul_add_mod_self_left _ _ _).symm
    _ = x % 2 := congrArg (· % 2) hx_eq.symm

theorem STree.zipLeaf_wf : ∀ {k : Nat} {a b : STree}, a.WF k → b.WF k → (STree.zipLeaf k a b).WF (k + 1)
  | k, .zero, .zero, _, _ => by cases k <;> trivial
  | 0, .leaf _, .leaf _, _, _ => ⟨rfl, rfl⟩
  | 0, .leaf _, .zero, _, _ => ⟨rfl, trivial⟩
  | 0, .zero, .leaf _, _, _ => ⟨trivial, rfl⟩
  | k + 1, .node _ _, .node _ _, ha, hb => ⟨STree.zipLeaf_wf ha.1 hb.1, STree.zipLeaf_wf ha.2 hb.2⟩
  | k + 1, .node _ _, .zero, ha, _ => ⟨STree.zipLeaf_wf ha.1 trivial, STree.zipLeaf_wf ha.2 trivial⟩
  | k + 1, .zero, .node _ _, _, hb => ⟨STree.zipLeaf_wf trivial hb.1, STree.zipLeaf_wf trivial hb.2⟩
  | 0, .node _ _, _, ha, _ => False.elim ha
  | 0, _, .node _ _, _, hb => False.elim hb
  | _ + 1, .leaf _, _, ha, _ => by cases ha
  | _ + 1, _, .leaf _, _, hb => by cases hb

theorem STree.get_zipLeaf : ∀ {k : Nat} {a b : STree}, a.WF k → b.WF k →
    ∀ x, (STree.zipLeaf k a b).get (k + 1) x =
      if (x / 2 ^ k) % 2 == 0 then a.get k (x % 2 ^ k) else b.get k (x % 2 ^ k)
  | _, .zero, .zero, _, _, _ => by simp [STree.zipLeaf, STree.get]
  | 0, .leaf _, .leaf _, _, _, _ => by simp [STree.zipLeaf, STree.get]
  | 0, .leaf _, .zero, _, _, _ => by simp [STree.zipLeaf, STree.get]
  | 0, .zero, .leaf _, _, _, _ => by simp [STree.zipLeaf, STree.get]
  | k + 1, .node l1 r1, .node l2 r2, ha, hb, x => by
    have hpow : 2 ^ (k + 1) = 2 * 2 ^ k := by rw [Nat.pow_succ, Nat.mul_comm]
    have hdiv : (x / 2) / 2 ^ k = x / 2 ^ (k + 1) := by rw [Nat.div_div_eq_div_mul, hpow]
    simp only [STree.zipLeaf, STree.get, mod_pow2_mod2, mod_pow2_div2]
    split
    · rw [STree.get_zipLeaf ha.1 hb.1 (x / 2), hdiv]
    · rw [STree.get_zipLeaf ha.2 hb.2 (x / 2), hdiv]
  | k + 1, .node l1 r1, .zero, ha, _, x => by
    have hpow : 2 ^ (k + 1) = 2 * 2 ^ k := by rw [Nat.pow_succ, Nat.mul_comm]
    have hdiv : (x / 2) / 2 ^ k = x / 2 ^ (k + 1) := by rw [Nat.div_div_eq_div_mul, hpow]
    simp only [STree.zipLeaf, STree.get, mod_pow2_mod2, mod_pow2_div2]
    split
    · rw [STree.get_zipLeaf ha.1 (b := .zero) trivial (x / 2), hdiv]; rfl
    · rw [STree.get_zipLeaf ha.2 (b := .zero) trivial (x / 2), hdiv]; rfl
  | k + 1, .zero, .node l2 r2, _, hb, x => by
    have hpow : 2 ^ (k + 1) = 2 * 2 ^ k := by rw [Nat.pow_succ, Nat.mul_comm]
    have hdiv : (x / 2) / 2 ^ k = x / 2 ^ (k + 1) := by rw [Nat.div_div_eq_div_mul, hpow]
    simp only [STree.zipLeaf, STree.get, mod_pow2_mod2, mod_pow2_div2]
    split
    · rw [STree.get_zipLeaf (a := .zero) trivial hb.1 (x / 2), hdiv]; rfl
    · rw [STree.get_zipLeaf (a := .zero) trivial hb.2 (x / 2), hdiv]; rfl
  | 0, .node _ _, _, ha, _, _ => False.elim ha
  | 0, _, .node _ _, _, hb, _ => False.elim hb
  | _ + 1, .leaf _, _, ha, _, _ => by cases ha
  | _ + 1, _, .leaf _, _, hb, _ => by cases hb

private theorem bitRev_go_shift (k cur acc : Nat) :
    bitRev.go k cur acc = bitRev.go k cur 0 + acc * 2 ^ k := by
  induction k generalizing cur acc with
  | zero => simp [bitRev.go]
  | succ k' ih =>
    simp only [bitRev.go, Nat.mul_zero, Nat.zero_add]
    rw [ih (cur / 2) (2 * acc + cur % 2), ih (cur / 2) (cur % 2)]
    have hpow : 2 ^ (k' + 1) = 2 * 2 ^ k' := by rw [Nat.pow_succ, Nat.mul_comm]
    have hmul : (2 * acc + cur % 2) * 2 ^ k' = acc * (2 * 2 ^ k') + cur % 2 * 2 ^ k' := by
      rw [Nat.add_mul, Nat.mul_comm 2 acc, Nat.mul_assoc]
    rw [hpow, hmul]; omega

private theorem bitRev_succ_unfold (m y : Nat) :
    bitRev (m + 1) y = bitRev m (y / 2) + (y % 2) * 2 ^ m := by
  unfold bitRev
  change bitRev.go m (y / 2) (2 * 0 + y % 2) = bitRev.go m (y / 2) 0 + (y % 2) * 2 ^ m
  simp only [Nat.mul_zero, Nat.zero_add]
  exact bitRev_go_shift m (y / 2) (y % 2)

private theorem bitRev_succ_msb : ∀ (k x : Nat), x < 2 ^ (k + 1) →
    bitRev (k + 1) x = 2 * bitRev k (x % 2 ^ k) + (x / 2 ^ k)
  | 0, x, hx => by
    have hx2 : x < 2 := by simpa using hx
    unfold bitRev; simp only [bitRev.go, Nat.pow_zero, Nat.div_one, Nat.mul_zero, Nat.zero_add]
    omega
  | k + 1, x, hx => by
    have hpow1 : 2 ^ (k + 1) = 2 * 2 ^ k := by rw [Nat.pow_succ, Nat.mul_comm]
    have hpow2 : 2 ^ (k + 2) = 2 * 2 ^ (k + 1) := by rw [Nat.pow_succ, Nat.mul_comm]
    have hx' : x / 2 < 2 ^ (k + 1) := by rw [hpow2] at hx; omega
    have hdiv : (x / 2) / 2 ^ k = x / 2 ^ (k + 1) := by rw [Nat.div_div_eq_div_mul, hpow1]
    rw [bitRev_succ_unfold (k + 1) x, bitRev_succ_msb k (x / 2) hx', hdiv,
        bitRev_succ_unfold k (x % 2 ^ (k + 1)), mod_pow2_div2, mod_pow2_mod2, hpow1]
    have hmul : 2 * (bitRev k ((x / 2) % 2 ^ k) + x % 2 * 2 ^ k) =
        2 * bitRev k ((x / 2) % 2 ^ k) + x % 2 * (2 * 2 ^ k) := by
      rw [Nat.mul_add, Nat.mul_left_comm 2 (x % 2) (2 ^ k)]
    rw [hmul]; omega

theorem STree.rev_wf : ∀ {k : Nat} {t : STree}, t.WF k → (t.rev k).WF k
  | k, .zero, _ => by cases k <;> trivial
  | 0, .leaf _, _ => rfl
  | k + 1, .node _ _, h => STree.zipLeaf_wf (STree.rev_wf h.1) (STree.rev_wf h.2)
  | 0, .node _ _, h => False.elim h
  | _ + 1, .leaf _, h => by cases h

theorem STree.get_rev : ∀ {k : Nat} {t : STree}, t.WF k →
    ∀ {x : Nat}, x < 2 ^ k → (t.rev k).get k x = t.get k (bitRev k x)
  | k, .zero, _, _, _ => by cases k <;> rfl
  | 0, .leaf _, _, _, _ => rfl
  | k + 1, .node l r, h, x, hx => by
    have hpos : 0 < 2 ^ k := Nat.two_pow_pos k
    have hmod_lt : x % 2 ^ k < 2 ^ k := Nat.mod_lt x hpos
    have hdiv_lt : x / 2 ^ k < 2 := by
      rw [Nat.div_lt_iff_lt_mul hpos]
      rw [Nat.pow_succ, Nat.mul_comm] at hx
      exact hx
    have hbr := bitRev_succ_msb k x hx
    have hbr_mod : bitRev (k + 1) x % 2 = x / 2 ^ k := by
      rw [hbr, Nat.mul_add_mod_self_left, Nat.mod_eq_of_lt hdiv_lt]
    have hbr_div : bitRev (k + 1) x / 2 = bitRev k (x % 2 ^ k) := by
      rw [hbr]
      have h1 : (2 * bitRev k (x % 2 ^ k) + x / 2 ^ k) / 2 = bitRev k (x % 2 ^ k) + (x / 2 ^ k) / 2 :=
        Nat.mul_add_div (by omega) _ _
      have h2 : (x / 2 ^ k) / 2 = 0 := Nat.div_eq_of_lt hdiv_lt
      omega
    simp only [STree.rev]
    rw [STree.get_zipLeaf (STree.rev_wf h.1) (STree.rev_wf h.2) x]
    simp only [STree.get, hbr_mod, hbr_div, Nat.mod_eq_of_lt hdiv_lt]
    split
    · exact STree.get_rev h.1 hmod_lt
    · exact STree.get_rev h.2 hmod_lt
  | 0, .node _ _, h, _, _ => False.elim h
  | _ + 1, .leaf _, h, _, _ => by cases h

theorem STree.allGe_spec (Lmin : Nat) : ∀ {k : Nat} {t : STree}, t.WF k →
    t.allGe Lmin k = true → ∀ x < 2 ^ k, Lmin ≤ t.get k x
  | _, .zero, _, h, _, _ => by
    have h0 : Lmin = 0 := Nat.eq_of_beq_eq_true h
    simp [STree.get, h0]
  | 0, .leaf v, _, h, _, _ => by
    exact Nat.le_of_ble_eq_true h
  | k + 1, .node l r, ht, h, x, hx => by
    have hpow : 2 ^ (k + 1) = 2 * 2 ^ k := by rw [Nat.pow_succ, Nat.mul_comm]
    have hx' : x / 2 < 2 ^ k := by rw [hpow] at hx; omega
    simp only [STree.allGe] at h
    cases hl : l.allGe Lmin k
    · simp [hl] at h
    · simp only [hl] at h
      simp only [STree.get]
      split
      · exact STree.allGe_spec Lmin ht.1 hl (x / 2) hx'
      · exact STree.allGe_spec Lmin ht.2 h (x / 2) hx'
  | 0, .node _ _, ht, _, _, _ => False.elim ht
  | _ + 1, .leaf _, ht, _, _, _ => by cases ht

theorem STree.insertAdd_wf : ∀ {k : Nat} (x w : Nat) {t : STree}, t.WF k → (t.insertAdd k x w).WF k
  | _, _, 0, _, ht => by simp [STree.insertAdd, ht]
  | 0, _, _ + 1, .zero, _ => rfl
  | 0, _, _ + 1, .leaf _, _ => rfl
  | k + 1, x, w + 1, .zero, _ => by
    simp only [STree.insertAdd]
    split
    · exact ⟨STree.insertAdd_wf (x / 2) (w + 1) trivial, trivial⟩
    · exact ⟨trivial, STree.insertAdd_wf (x / 2) (w + 1) trivial⟩
  | k + 1, x, w + 1, .node l r, h => by
    simp only [STree.insertAdd]
    split
    · exact ⟨STree.insertAdd_wf (x / 2) (w + 1) h.1, h.2⟩
    · exact ⟨h.1, STree.insertAdd_wf (x / 2) (w + 1) h.2⟩
  | 0, _, _ + 1, .node _ _, h => False.elim h
  | _ + 1, _, _ + 1, .leaf _, h => by cases h

theorem STree.get_insertAdd : ∀ {k : Nat} {t : STree}, t.WF k →
    ∀ {x y : Nat} (w : Nat), x < 2 ^ k → y < 2 ^ k →
      (t.insertAdd k x w).get k y = t.get k y + if y = x then w else 0
  | _, _, _, _, _, 0, _, _ => by simp [STree.insertAdd]
  | 0, .zero, _, x, y, w + 1, hx, hy => by
    have hx0 : x = 0 := by simpa using hx
    have hy0 : y = 0 := by simpa using hy
    subst hx0; subst hy0; simp [STree.insertAdd, STree.get]
  | 0, .leaf v, _, x, y, w + 1, hx, hy => by
    have hx0 : x = 0 := by simpa using hx
    have hy0 : y = 0 := by simpa using hy
    subst hx0; subst hy0; simp [STree.insertAdd, STree.get]
  | k + 1, .zero, _, x, y, w + 1, hx, hy => by
    have hpow : 2 ^ (k + 1) = 2 * 2 ^ k := by rw [Nat.pow_succ, Nat.mul_comm]
    have hx' : x / 2 < 2 ^ k := by rw [hpow] at hx; omega
    have hy' : y / 2 < 2 ^ k := by rw [hpow] at hy; omega
    simp only [STree.insertAdd]
    by_cases hxm : x % 2 = 0 <;> by_cases hym : y % 2 = 0
    · simp only [hxm, hym, beq_self_eq_true, ↓reduceIte, STree.get]
      rw [STree.get_insertAdd (k := k) (t := .zero) trivial (w := w + 1) hx' hy']
      simp only [STree.get]
      have hiff : y / 2 = x / 2 ↔ y = x := by omega
      simp [hiff]
    · have hy1 : y % 2 = 1 := by omega
      have hne : y ≠ x := by omega
      have h10 : (1 == 0) = false := rfl
      simp [hxm, hy1, h10, STree.get, hne]
    · have hx1 : x % 2 = 1 := by omega
      have hne : y ≠ x := by omega
      have h10 : (1 == 0) = false := rfl
      simp [hx1, hym, h10, STree.get, hne]
    · have hx1 : x % 2 = 1 := by omega
      have hy1 : y % 2 = 1 := by omega
      have h10 : (1 == 0) = false := rfl
      simp only [hx1, hy1, h10, Bool.false_eq_true, ↓reduceIte, STree.get]
      rw [STree.get_insertAdd (k := k) (t := .zero) trivial (w := w + 1) hx' hy']
      simp only [STree.get]
      have hiff : y / 2 = x / 2 ↔ y = x := by omega
      simp [hiff]
  | k + 1, .node l r, h, x, y, w + 1, hx, hy => by
    have hpow : 2 ^ (k + 1) = 2 * 2 ^ k := by rw [Nat.pow_succ, Nat.mul_comm]
    have hx' : x / 2 < 2 ^ k := by rw [hpow] at hx; omega
    have hy' : y / 2 < 2 ^ k := by rw [hpow] at hy; omega
    simp only [STree.insertAdd]
    by_cases hxm : x % 2 = 0 <;> by_cases hym : y % 2 = 0
    · simp only [hxm, hym, beq_self_eq_true, ↓reduceIte, STree.get]
      rw [STree.get_insertAdd h.1 (w := w + 1) hx' hy']
      have hiff : y / 2 = x / 2 ↔ y = x := by omega
      simp [hiff]
    · have hy1 : y % 2 = 1 := by omega
      have hne : y ≠ x := by omega
      have h10 : (1 == 0) = false := rfl
      simp [hxm, hy1, h10, STree.get, hne]
    · have hx1 : x % 2 = 1 := by omega
      have hne : y ≠ x := by omega
      have h10 : (1 == 0) = false := rfl
      simp [hx1, hym, h10, STree.get, hne]
    · have hx1 : x % 2 = 1 := by omega
      have hy1 : y % 2 = 1 := by omega
      have h10 : (1 == 0) = false := rfl
      simp only [hx1, hy1, h10, Bool.false_eq_true, ↓reduceIte, STree.get]
      rw [STree.get_insertAdd h.2 (w := w + 1) hx' hy']
      have hiff : y / 2 = x / 2 ↔ y = x := by omega
      simp [hiff]
  | 0, .node _ _, h, _, _, _ + 1, _, _ => False.elim h
  | _ + 1, .leaf _, h, _, _, _ + 1, _, _ => by cases h

theorem STree.sum_insertAdd : ∀ {k : Nat} {t : STree}, t.WF k →
    ∀ {x : Nat} (w : Nat), x < 2 ^ k →
      (t.insertAdd k x w).sum k = t.sum k + w
  | _, _, _, _, 0, _ => by simp [STree.insertAdd]
  | 0, .zero, _, _, _ + 1, _ => by simp [STree.insertAdd, STree.sum]
  | 0, .leaf _, _, _, _ + 1, _ => by simp [STree.insertAdd, STree.sum]
  | k + 1, .zero, _, x, w + 1, hx => by
    have hpow : 2 ^ (k + 1) = 2 * 2 ^ k := by rw [Nat.pow_succ, Nat.mul_comm]
    have hx' : x / 2 < 2 ^ k := by rw [hpow] at hx; omega
    have ih := STree.sum_insertAdd (k := k) (t := .zero) trivial (w := w + 1) hx'
    simp only [STree.insertAdd]
    split <;> simp only [STree.sum, ih] <;> omega
  | k + 1, .node l r, h, x, w + 1, hx => by
    have hpow : 2 ^ (k + 1) = 2 * 2 ^ k := by rw [Nat.pow_succ, Nat.mul_comm]
    have hx' : x / 2 < 2 ^ k := by rw [hpow] at hx; omega
    simp only [STree.insertAdd]
    split
    · have ih := STree.sum_insertAdd h.1 (w := w + 1) hx'
      simp only [STree.sum, ih]; omega
    · have ih := STree.sum_insertAdd h.2 (w := w + 1) hx'
      simp only [STree.sum, ih]; omega
  | 0, .node _ _, h, _, _ + 1, _ => False.elim h
  | _ + 1, .leaf _, h, _, _ + 1, _ => by cases h

/-! ## 3. Exact Recursive Block-Matrix Dual Operator `evalDual` -/

/--
  Evaluates `A_{n,s}^T y` recursively for ANY `(n, s)` with `s ≤ n`:
    * `s = 0`: `A_{n,0}^T y = y` (identity)
    * `n = s`: `A_{s,s}^T [v] = const(s, v)` (all-ones row)
    * `n + 1, s + 1` (`s < n`):
        `[ A_{n,s+1}^T y0 + (A_{n,s}^{(1)})^T y1 ; (A_{n,s}^{(0)})^T y0 + A_{n,s+1}^T y1 ]`
  Prunes `.zero` subtrees in `O(1)`.
-/
def evalDual : Nat → Nat → STree → STree
  | _, _, .zero => .zero
  | _, 0, y => y
  | n + 1, s + 1, y =>
    if n == s then
      match y with
      | .leaf v => STree.const (n + 1) v
      | _ => .zero
    else
      match y with
      | .node y0 y1 =>
        let l1 := evalDual n (s + 1) y0
        let l2 := evalDual n s y1.rightHalf
        let r1 := evalDual n s y0.leftHalf
        let r2 := evalDual n (s + 1) y1
        .node (l1.add l2) (r1.add r2)
      | _ => .zero
  | 0, _ + 1, _ => .zero

private theorem evalDual_zero (n s : Nat) : evalDual n s .zero = .zero := by
  cases n <;> cases s <;> rfl

private theorem evalDual_s0 (n : Nat) (y : STree) : evalDual n 0 y = y := by
  cases n <;> cases y <;> rfl

theorem evalDual_wf : ∀ (n s : Nat) (y : STree), s ≤ n → y.WF (n - s) →
    (evalDual n s y).WF n
  | n, s, .zero, _, _ => by rw [evalDual_zero]; trivial
  | n, 0, .leaf v, _, hy => by rw [evalDual_s0]; exact hy
  | n, 0, .node l r, _, hy => by rw [evalDual_s0]; exact hy
  | 0, _ + 1, _, hs, _ => by omega
  | n + 1, s + 1, .leaf v, hs, hy => by
    simp only [evalDual]
    by_cases hns : n = s
    · subst hns
      simp only [beq_self_eq_true, ↓reduceIte]
      exact STree.const_wf (n + 1) v
    · have hsub : n + 1 - (s + 1) = (n - (s + 1)) + 1 := by omega
      rw [hsub] at hy
      cases hy
  | n + 1, s + 1, .node y0 y1, hs, hy => by
    simp only [evalDual]
    by_cases hns : n = s
    · subst hns
      rw [Nat.sub_self] at hy
      exact False.elim hy
    · have hbe : (n == s) = false := beq_false_of_ne hns
      simp only [hbe, Bool.false_eq_true, ↓reduceIte]
      have hle : s + 1 ≤ n := by omega
      have hsub : n + 1 - (s + 1) = (n - (s + 1)) + 1 := by omega
      have hsub' : n - s = (n - (s + 1)) + 1 := by omega
      rw [hsub] at hy
      have hl1 : (evalDual n (s + 1) y0).WF n := evalDual_wf n (s + 1) y0 hle hy.1
      have hr2 : (evalDual n (s + 1) y1).WF n := evalDual_wf n (s + 1) y1 hle hy.2
      have hl2 : (evalDual n s y1.rightHalf).WF n :=
        evalDual_wf n s y1.rightHalf (by omega) (by rw [hsub']; exact STree.rightHalf_wf hy.2)
      have hr1 : (evalDual n s y0.leftHalf).WF n :=
        evalDual_wf n s y0.leftHalf (by omega) (by rw [hsub']; exact STree.leftHalf_wf hy.1)
      exact ⟨STree.add_wf hl1 hl2, STree.add_wf hr1 hr2⟩

/-- Abstract tree-weighted sum over all length-`k` bit-strings satisfying predicate `p`. -/
def subseqSum (k : Nat) (y : STree) (p : List Bool → Bool) : Nat :=
  match y with
  | .zero => 0
  | .leaf v => match k with | 0 => if p [] then v else 0 | _ => 0
  | .node l r => match k with
    | 0 => 0
    | k' + 1 => subseqSum k' l (fun u => p (false :: u)) + subseqSum k' r (fun u => p (true :: u))
termination_by structural y

private theorem subseqSum_congr : ∀ (k : Nat) (y : STree) (p q : List Bool → Bool),
    (∀ u : List Bool, u.length = k → p u = q u) →
    subseqSum k y p = subseqSum k y q
  | _, .zero, _, _, _ => rfl
  | 0, .leaf _, _, _, hpq => by simp [subseqSum, hpq [] rfl]
  | k + 1, .node l r, p, q, hpq => by
    simp only [subseqSum]
    rw [subseqSum_congr k l _ _ (fun u hu => hpq (false :: u) (by simp [hu])),
        subseqSum_congr k r _ _ (fun u hu => hpq (true :: u) (by simp [hu]))]
  | 0, .node _ _, _, _, _ => rfl
  | _ + 1, .leaf _, _, _, _ => rfl

private theorem subseqSum_false : ∀ (k : Nat) (y : STree),
    subseqSum k y (fun _ => false) = 0
  | _, .zero => rfl
  | 0, .leaf _ => rfl
  | k + 1, .node l r => by simp [subseqSum, subseqSum_false k l, subseqSum_false k r]
  | 0, .node _ _ => rfl
  | _ + 1, .leaf _ => rfl

private theorem subseqSum_leftHalf (k : Nat) (y : STree) (p : List Bool → Bool) :
    subseqSum (k + 1) y.leftHalf p = subseqSum k y (fun u => p (false :: u)) := by
  cases y <;> simp [STree.leftHalf, subseqSum]

private theorem subseqSum_rightHalf (k : Nat) (y : STree) (p : List Bool → Bool) :
    subseqSum (k + 1) y.rightHalf p = subseqSum k y (fun u => p (true :: u)) := by
  cases y <;> simp [STree.rightHalf, subseqSum]

private theorem subseqSum_eq_get : ∀ (n : Nat) (y : STree), y.WF n →
    ∀ x, subseqSum n y (fun u => isSubseqB u (natToWord n x)) = y.get n x
  | _, .zero, _, _ => rfl
  | 0, .leaf _, _, _ => rfl
  | n + 1, .node l r, hy, x => by
    simp only [subseqSum, natToWord, STree.get]
    by_cases hev : x % 2 = 0
    · have h01 : (0 == 1) = false := rfl
      simp only [hev, beq_self_eq_true, ↓reduceIte, h01]
      have hl_eq : subseqSum n l (fun u => isSubseqB (false :: u) (false :: natToWord n (x / 2))) =
          subseqSum n l (fun u => isSubseqB u (natToWord n (x / 2))) := rfl
      have hr_zero : subseqSum n r (fun u => isSubseqB (true :: u) (false :: natToWord n (x / 2))) = 0 := by
        rw [subseqSum_congr n r _ (fun _ => false)]
        · exact subseqSum_false n r
        · intro u hu
          change isSubseqB (true :: u) (natToWord n (x / 2)) = false
          exact isSubseqB_false_of_lt_len (by rw [natToWord_length, List.length_cons, hu]; omega)
      rw [hl_eq, hr_zero, Nat.add_zero]
      exact subseqSum_eq_get n l hy.1 (x / 2)
    · have h1 : x % 2 = 1 := by omega
      have h10 : (1 == 0) = false := rfl
      have h11 : (1 == 1) = true := rfl
      simp only [h1, h10, h11, Bool.false_eq_true, ↓reduceIte]
      have hl_zero : subseqSum n l (fun u => isSubseqB (false :: u) (true :: natToWord n (x / 2))) = 0 := by
        rw [subseqSum_congr n l _ (fun _ => false)]
        · exact subseqSum_false n l
        · intro u hu
          change isSubseqB (false :: u) (natToWord n (x / 2)) = false
          exact isSubseqB_false_of_lt_len (by rw [natToWord_length, List.length_cons, hu]; omega)
      have hr_eq : subseqSum n r (fun u => isSubseqB (true :: u) (true :: natToWord n (x / 2))) =
          subseqSum n r (fun u => isSubseqB u (natToWord n (x / 2))) := rfl
      rw [hl_zero, Nat.zero_add, hr_eq]
      exact subseqSum_eq_get n r hy.2 (x / 2)
  | 0, .node _ _, hy, _ => False.elim hy
  | _ + 1, .leaf _, hy, _ => by cases hy

/--
  Core Exactness Theorem for `evalDual`:
  For ALL `s ≤ n`, ALL well-formed sparse weight trees `y`, and ALL `x`,
  `(evalDual n s y).get n x` equals the EXACT sum of `y(d)` over `d ∈ D_s(x)`.
-/
theorem evalDual_get_eq : ∀ (n s : Nat) (y : STree), s ≤ n → y.WF (n - s) →
    ∀ x, (evalDual n s y).get n x = subseqSum (n - s) y (fun u => isSubseqB u (natToWord n x))
  | n, s, .zero, _, _, _ => by rw [evalDual_zero]; rfl
  | n, 0, .leaf v, _, hy, x => by rw [evalDual_s0]; exact (subseqSum_eq_get n (.leaf v) hy x).symm
  | n, 0, .node l r, _, hy, x => by rw [evalDual_s0]; exact (subseqSum_eq_get n (.node l r) hy x).symm
  | 0, _ + 1, _, hs, _, _ => by omega
  | n + 1, s + 1, .leaf v, hs, hy, x => by
    simp only [evalDual]
    by_cases hns : n = s
    · subst hns
      simp only [beq_self_eq_true, ↓reduceIte, STree.get_const, Nat.sub_self, subseqSum, isSubseqB, ↓reduceIte]
    · have hsub : n + 1 - (s + 1) = (n - (s + 1)) + 1 := by omega
      rw [hsub] at hy
      cases hy
  | n + 1, s + 1, .node y0 y1, hs, hy, x => by
    simp only [evalDual]
    by_cases hns : n = s
    · subst hns
      rw [Nat.sub_self] at hy
      exact False.elim hy
    · have hbe : (n == s) = false := beq_false_of_ne hns
      simp only [hbe, Bool.false_eq_true, ↓reduceIte]
      have hle : s + 1 ≤ n := by omega
      have hsub : n + 1 - (s + 1) = (n - (s + 1)) + 1 := by omega
      have hsub' : n - s = (n - (s + 1)) + 1 := by omega
      rw [hsub] at hy
      have hl1_wf : (evalDual n (s + 1) y0).WF n := evalDual_wf n (s + 1) y0 hle hy.1
      have hr2_wf : (evalDual n (s + 1) y1).WF n := evalDual_wf n (s + 1) y1 hle hy.2
      have hl2_wf : (evalDual n s y1.rightHalf).WF n :=
        evalDual_wf n s y1.rightHalf (by omega) (by rw [hsub']; exact STree.rightHalf_wf hy.2)
      have hr1_wf : (evalDual n s y0.leftHalf).WF n :=
        evalDual_wf n s y0.leftHalf (by omega) (by rw [hsub']; exact STree.leftHalf_wf hy.1)
      have hl1_eq := evalDual_get_eq n (s + 1) y0 hle hy.1 (x / 2)
      have hr2_eq := evalDual_get_eq n (s + 1) y1 hle hy.2 (x / 2)
      have hl2_eq : (evalDual n s y1.rightHalf).get n (x / 2) =
          subseqSum (n - (s + 1)) y1 (fun u => isSubseqB (true :: u) (natToWord n (x / 2))) := by
        rw [evalDual_get_eq n s y1.rightHalf (by omega) (by rw [hsub']; exact STree.rightHalf_wf hy.2) (x / 2),
            hsub', subseqSum_rightHalf]
      have hr1_eq : (evalDual n s y0.leftHalf).get n (x / 2) =
          subseqSum (n - (s + 1)) y0 (fun u => isSubseqB (false :: u) (natToWord n (x / 2))) := by
        rw [evalDual_get_eq n s y0.leftHalf (by omega) (by rw [hsub']; exact STree.leftHalf_wf hy.1) (x / 2),
            hsub', subseqSum_leftHalf]
      rw [hsub]
      simp only [STree.get, subseqSum, natToWord]
      by_cases hev : x % 2 = 0
      · have h01 : (0 == 1) = false := rfl
        simp only [hev, beq_self_eq_true, ↓reduceIte, h01]
        rw [STree.get_add hl1_wf hl2_wf (x / 2), hl1_eq, hl2_eq]
        rfl
      · have h1 : x % 2 = 1 := by omega
        have h10 : (1 == 0) = false := rfl
        have h11 : (1 == 1) = true := rfl
        simp only [h1, h10, h11, Bool.false_eq_true, ↓reduceIte]
        rw [STree.get_add hr1_wf hr2_wf (x / 2), hr1_eq, hr2_eq]
        rfl

/-! ## 4. Universal Disjoint-Ball Sum Bound (Covers Both Balls and Rank-1 CG Cuts) -/

private theorem sum_map_zero_rec {α : Type} : ∀ (L : List α), (L.map (fun _ => 0)).sum = 0
  | [] => rfl
  | _ :: xs => by simp [sum_map_zero_rec xs]

private theorem sum_map_one_rec {α : Type} : ∀ (L : List α), (L.map (fun _ => 1)).sum = L.length
  | [] => rfl
  | _ :: xs => by simp [sum_map_one_rec xs, Nat.add_comm]

private theorem sum_map_add_rec {α : Type} (f g : α → Nat) :
    ∀ (L : List α), (L.map fun x => f x + g x).sum = (L.map f).sum + (L.map g).sum
  | [] => by simp
  | x :: xs => by
    simp only [List.map_cons, List.sum_cons, sum_map_add_rec f g xs]
    omega

private theorem sum_map_mul_right_rec {α : Type} (f : α → Nat) (c : Nat) :
    ∀ (L : List α), (L.map fun x => f x * c).sum = (L.map f).sum * c
  | [] => by simp
  | x :: xs => by
    simp only [List.map_cons, List.sum_cons, sum_map_mul_right_rec f c xs, Nat.add_mul]

private theorem sum_map_le_of_le_rec {α : Type} (f g : α → Nat) (hfg : ∀ x, f x ≤ g x) :
    ∀ (L : List α), (L.map f).sum ≤ (L.map g).sum
  | [] => by simp
  | x :: xs => by
    simp only [List.map_cons, List.sum_cons]
    have h1 := hfg x
    have h2 := sum_map_le_of_le_rec f g hfg xs
    omega

private theorem sum_ite_eq_mul_filter_rec {α : Type} (p : α → Bool) (w : Nat) :
    ∀ (L : List α), (L.map fun x => if p x = true then w else 0).sum = w * (L.filter p).length
  | [] => by simp
  | x :: xs => by
    by_cases hx : p x = true
    · simp [hx, sum_ite_eq_mul_filter_rec p w xs, Nat.mul_add, Nat.add_comm]
    · have hfx : p x = false := Bool.eq_false_iff.mpr hx
      simp [hfx, sum_ite_eq_mul_filter_rec p w xs]

/--
  Universal Disjointness Sum Lemma over `STree`:
  If no two distinct elements of `C` can both satisfy `P u C[i]` for any length-`k` word `u`,
  then the sum of `subseqSum k y (P · w)` over `w ∈ C` is bounded by `y.sum k`.
-/
theorem sum_subseqSum_le_gen : ∀ (k : Nat) (y : STree) {α : Type} (C : List α)
    (P : List Bool → α → Bool),
    y.WF k →
    (∀ i j (hi : i < C.length) (hj : j < C.length), i ≠ j →
      ∀ u : List Bool, u.length = k → ¬ (P u C[i] = true ∧ P u C[j] = true)) →
    (C.map fun w => subseqSum k y (fun u => P u w)).sum ≤ y.sum k
  | _, .zero, _, C, _, _, _ => by
    simp only [subseqSum, STree.sum, sum_map_zero_rec C, Nat.le_refl]
  | 0, .leaf v, _, C, P, _, hdisj => by
    simp only [subseqSum, STree.sum]
    have hle1 : (C.filter (fun w => P [] w)).length ≤ 1 := by
      apply filter_len_le_one_of_pairwise (fun w => P [] w) C
      intro i j hi hj hij hpi hpj
      exact hdisj i j hi hj hij [] rfl ⟨hpi, hpj⟩
    rw [sum_ite_eq_mul_filter_rec (fun w => P [] w) v C]
    calc v * (C.filter (fun w => P [] w)).length ≤ v * 1 := Nat.mul_le_mul_left v hle1
      _ = v := Nat.mul_one v
  | k + 1, .node l r, _, C, P, hy, hdisj => by
    simp only [subseqSum, STree.sum]
    rw [sum_map_add_rec (fun w => subseqSum k l (fun u => P (false :: u) w))
                        (fun w => subseqSum k r (fun u => P (true :: u) w)) C]
    have hl := sum_subseqSum_le_gen k l C (fun u w => P (false :: u) w) hy.1
      (fun i j hi hj hij u hu => hdisj i j hi hj hij (false :: u) (by simp [hu]))
    have hr := sum_subseqSum_le_gen k r C (fun u w => P (true :: u) w) hy.2
      (fun i j hi hj hij u hu => hdisj i j hi hj hij (true :: u) (by simp [hu]))
    omega
  | 0, .node _ _, _, _, _, hy, _ => False.elim hy
  | _ + 1, .leaf _, _, _, _, hy, _ => by cases hy

theorem sum_evalDual_le {n s : Nat} (hs : s ≤ n) (y : STree) (hy : y.WF (n - s))
    {C : List Nat} (hC : IsValidDeletionCode n s C) :
    (C.map fun x => (evalDual n s y).get n x).sum ≤ y.sum (n - s) := by
  have heq : C.map (fun x => (evalDual n s y).get n x) =
      C.map (fun x => subseqSum (n - s) y (fun u => isSubseqB u (natToWord n x))) := by
    apply List.map_congr_left
    intro x _
    exact evalDual_get_eq n s y hs hy x
  rw [heq]
  apply sum_subseqSum_le_gen (n - s) y C (fun u x => isSubseqB u (natToWord n x)) hy
  intro i j hi hj hij u hu ⟨h1, h2⟩
  have hb1 : InDelBall s (natToWord n C[i]) u :=
    ⟨isSubseqB_sound h1, by rw [natToWord_length, hu]; omega⟩
  have hb2 : InDelBall s (natToWord n C[j]) u :=
    ⟨isSubseqB_sound h2, by rw [natToWord_length, hu]; omega⟩
  exact (hC.2 i j hi hj hij).2.1 u ⟨hb1, hb2⟩

/-! ## 5. Zero-Witness Universal Recursive Clique Checker (`canMatchList`) -/

/--
  Zero-allocation direct-`Nat` structurally-recursive `LCS(u, v) ≥ L` checker with deletion
  budgets `s1, s2`. Avoids building `List Bool` thunks during pairwise clique verification!
-/
def canMatchNat : Nat → Nat → Nat → Nat → Nat → Nat → Bool
  | _, 0, _, _, _, _ => true
  | fuel + 1, L + 1, s1, s2, u, v =>
    if Nat.beq (u % 2) (v % 2) then canMatchNat fuel L s1 s2 (u / 2) (v / 2)
    else
      match s1 with
      | 0 => match s2 with | 0 => false | s2' + 1 => canMatchNat fuel (L + 1) 0 s2' u (v / 2)
      | s1' + 1 =>
        match canMatchNat fuel (L + 1) s1' s2 (u / 2) v with
        | true => true
        | false => match s2 with | 0 => false | s2' + 1 => canMatchNat fuel (L + 1) (s1' + 1) s2' u (v / 2)
  | 0, _ + 1, _, _, _, _ => false

theorem canMatchNat_sound : ∀ (fuel L s1 s2 u v : Nat),
    canMatchNat fuel L s1 s2 u v = true →
    ∃ d : List Bool, d.length = L ∧
      IsSubseq d (natToWord (L + s1) u) ∧ IsSubseq d (natToWord (L + s2) v)
  | _, 0, s1, s2, u, v, _ =>
    ⟨[], rfl, IsSubseq.nil_left (natToWord (0 + s1) u), IsSubseq.nil_left (natToWord (0 + s2) v)⟩
  | 0, _ + 1, _, _, _, _, h => by simp [canMatchNat] at h
  | fuel + 1, L + 1, s1, s2, u, v, h => by
    simp only [canMatchNat] at h
    cases heq : Nat.beq (u % 2) (v % 2)
    · simp only [heq, Bool.false_eq_true, ↓reduceIte] at h
      cases s1 with
      | zero =>
        cases s2 with
        | zero => simp at h
        | succ s2' =>
          obtain ⟨d, hlen, hdu, hdv⟩ := canMatchNat_sound fuel (L + 1) 0 s2' u (v / 2) h
          refine ⟨d, hlen, hdu, ?_⟩
          have hv_eq : natToWord ((L + 1) + (s2' + 1)) v = (v % 2 == 1) :: natToWord ((L + 1) + s2') (v / 2) := by
            rw [← Nat.add_assoc]; rfl
          rw [hv_eq]
          exact .cons_drop (v % 2 == 1) hdv
      | succ s1' =>
        simp only at h
        cases h1 : canMatchNat fuel (L + 1) s1' s2 (u / 2) v
        · simp only [h1] at h
          cases s2 with
          | zero => simp at h
          | succ s2' =>
            obtain ⟨d, hlen, hdu, hdv⟩ := canMatchNat_sound fuel (L + 1) (s1' + 1) s2' u (v / 2) h
            refine ⟨d, hlen, hdu, ?_⟩
            have hv_eq : natToWord ((L + 1) + (s2' + 1)) v = (v % 2 == 1) :: natToWord ((L + 1) + s2') (v / 2) := by
              rw [← Nat.add_assoc]; rfl
            rw [hv_eq]
            exact .cons_drop (v % 2 == 1) hdv
        · obtain ⟨d, hlen, hdu, hdv⟩ := canMatchNat_sound fuel (L + 1) s1' s2 (u / 2) v h1
          refine ⟨d, hlen, ?_, hdv⟩
          have hu_eq : natToWord ((L + 1) + (s1' + 1)) u = (u % 2 == 1) :: natToWord ((L + 1) + s1') (u / 2) := by
            rw [← Nat.add_assoc]; rfl
          rw [hu_eq]
          exact .cons_drop (u % 2 == 1) hdu
    · simp only [heq, ↓reduceIte] at h
      have hmod : u % 2 = v % 2 := Nat.eq_of_beq_eq_true heq
      obtain ⟨d, hlen, hdu, hdv⟩ := canMatchNat_sound fuel L s1 s2 (u / 2) (v / 2) h
      have hu_eq : natToWord ((L + 1) + s1) u = (u % 2 == 1) :: natToWord (L + s1) (u / 2) := by
        rw [Nat.succ_add]; rfl
      have hv_eq : natToWord ((L + 1) + s2) v = (u % 2 == 1) :: natToWord (L + s2) (v / 2) := by
        rw [Nat.succ_add, hmod]; rfl
      refine ⟨(u % 2 == 1) :: d, by simp [hlen], ?_, ?_⟩
      · rw [hu_eq]; exact .cons_keep (u % 2 == 1) hdu
      · rw [hv_eq]; exact .cons_keep (u % 2 == 1) hdv

def checkNatVsList (fuel L s u : Nat) : List Nat → Bool
  | [] => true
  | v :: vs => match canMatchNat fuel L s s u v with
    | true => checkNatVsList fuel L s u vs
    | false => false

private theorem checkNatVsList_sound {fuel L s u : Nat} :
    ∀ {vs : List Nat}, checkNatVsList fuel L s u vs = true →
      ∀ v ∈ vs, ∃ d : List Bool, d.length = L ∧
        IsSubseq d (natToWord (L + s) u) ∧ IsSubseq d (natToWord (L + s) v)
  | [], _, _, hmem => by cases hmem
  | v :: vs, h, z, hz => by
    simp only [checkNatVsList] at h
    cases hm : canMatchNat fuel L s s u v
    · simp [hm] at h
    · simp only [hm] at h
      rcases List.mem_cons.mp hz with rfl | hzs
      · exact canMatchNat_sound fuel L s s u z hm
      · exact checkNatVsList_sound h z hzs

def checkNatsClq (fuel L s : Nat) : List Nat → Bool
  | [] => true
  | u :: us => match checkNatVsList fuel L s u us with
    | true => checkNatsClq fuel L s us
    | false => false

private theorem checkNatsClq_sound {fuel L s : Nat} : ∀ {Q : List Nat},
    checkNatsClq fuel L s Q = true →
    ∀ i j (hi : i < Q.length) (hj : j < Q.length), i ≠ j →
      ∃ d : List Bool, d.length = L ∧
        IsSubseq d (natToWord (L + s) Q[i]) ∧ IsSubseq d (natToWord (L + s) Q[j])
  | [], _, i, _, hi, _, _ => absurd hi (Nat.not_lt_zero _)
  | u :: us, h, i, j, hi, hj, hij => by
    simp only [checkNatsClq] at h
    cases hu : checkNatVsList fuel L s u us
    · simp [hu] at h
    · simp only [hu] at h
      cases i with
      | zero =>
        cases j with
        | zero => exact absurd rfl hij
        | succ j' =>
          have hj' : j' < us.length := Nat.lt_of_succ_lt_succ hj
          exact checkNatVsList_sound hu us[j'] (List.getElem_mem hj')
      | succ i' =>
        cases j with
        | zero =>
          have hi' : i' < us.length := Nat.lt_of_succ_lt_succ hi
          obtain ⟨d, hlen, h1, h2⟩ := checkNatVsList_sound hu us[i'] (List.getElem_mem hi')
          exact ⟨d, hlen, h2, h1⟩
        | succ j' =>
          have hi' : i' < us.length := Nat.lt_of_succ_lt_succ hi
          have hj' : j' < us.length := Nat.lt_of_succ_lt_succ hj
          exact checkNatsClq_sound h i' j' hi' hj' (by omega)

/-- Universal zero-witness direct-`Nat` clique checker for ALL `(n, s)`. -/
def checkClqRec (n s : Nat) (Q : List Nat) : Bool :=
  isStrictAsc Q && Q.all (· < 2 ^ n) && checkNatsClq (n + s) (n - s) s Q

theorem checkClqRec_sound {n s : Nat} (hs : s ≤ n) {Q : List Nat}
    (hQ : checkClqRec n s Q = true) :
    Q.Nodup ∧ (∀ u ∈ Q, u < 2 ^ n) ∧
    (∀ u ∈ Q, ∀ v ∈ Q, u ≠ v →
      ∃ d : List Bool, InDelBall s (natToWord n u) d ∧ InDelBall s (natToWord n v) d) := by
  simp only [checkClqRec, Bool.and_eq_true, List.all_eq_true, decide_eq_true_eq] at hQ
  rcases hQ with ⟨⟨hasc, hlt⟩, hclq⟩
  refine ⟨strictAsc_nodup hasc, hlt, ?_⟩
  intro u hu v hv huv
  obtain ⟨i, hi, rfl⟩ := List.getElem_of_mem hu
  obtain ⟨j, hj, rfl⟩ := List.getElem_of_mem hv
  have hij : i ≠ j := fun h => huv (by subst h; rfl)
  obtain ⟨d, hlen, hd1, hd2⟩ := checkNatsClq_sound hclq i j hi hj hij
  have hns : n - s + s = n := Nat.sub_add_cancel hs
  rw [hns] at hd1 hd2
  exact ⟨d, ⟨hd1, by rw [natToWord_length, hlen]; omega⟩,
            ⟨hd2, by rw [natToWord_length, hlen]; omega⟩⟩

/-! ## 6. Building Sparse Trees for Balls, Cliques, and Rank-1 CG Cuts -/

def buildBallTree (k : Nat) (yList : List (Nat × Nat)) : STree :=
  yList.foldl (fun t p => t.insertAdd k p.1 p.2) .zero

private theorem buildBallTree_fold_spec (k : Nat) :
    ∀ (L : List (Nat × Nat)) (t : STree), t.WF k →
      (∀ p ∈ L, p.1 < 2 ^ k) →
      (L.foldl (fun acc p => acc.insertAdd k p.1 p.2) t).WF k ∧
      (L.foldl (fun acc p => acc.insertAdd k p.1 p.2) t).sum k = t.sum k + (L.map Prod.snd).sum
  | [], t, ht, _ => ⟨ht, by simp⟩
  | p :: ps, t, ht, hall => by
    have hp : p.1 < 2 ^ k := hall p (List.mem_cons_self ..)
    have hps : ∀ q ∈ ps, q.1 < 2 ^ k := fun q hq => hall q (List.mem_cons_of_mem p hq)
    have ht' : (t.insertAdd k p.1 p.2).WF k := STree.insertAdd_wf p.1 p.2 ht
    have hrec := buildBallTree_fold_spec k ps (t.insertAdd k p.1 p.2) ht' hps
    refine ⟨hrec.1, ?_⟩
    simp only [List.foldl_cons, List.map_cons, List.sum_cons]
    rw [hrec.2, STree.sum_insertAdd ht p.2 hp]
    omega

theorem buildBallTree_wf (k : Nat) (yList : List (Nat × Nat)) :
    (buildBallTree k yList).WF k := by
  unfold buildBallTree
  suffices ∀ (L : List (Nat × Nat)) (t : STree), t.WF k →
      (L.foldl (fun acc p => acc.insertAdd k p.1 p.2) t).WF k from this yList .zero trivial
  intro L
  induction L with
  | nil => intro t ht; exact ht
  | cons p ps ih => intro t ht; exact ih _ (STree.insertAdd_wf p.1 p.2 ht)

theorem buildBallTree_sum (k : Nat) (yList : List (Nat × Nat))
    (hy : ∀ p ∈ yList, p.1 < 2 ^ k) :
    (buildBallTree k yList).sum k = (yList.map Prod.snd).sum := by
  have h := buildBallTree_fold_spec k yList .zero trivial hy
  simpa [buildBallTree, STree.sum] using h.2

/-- Accumulate a single clique `(w, Q)` into a depth-`n` sparse `STree`. -/
def addClqToTree (n w : Nat) (Q : List Nat) (t : STree) : STree :=
  Q.foldl (fun acc x => acc.insertAdd n x w) t

private theorem addClqToTree_spec (n w : Nat) :
    ∀ (Q : List Nat) (t : STree), t.WF n → Q.Nodup → (∀ x ∈ Q, x < 2 ^ n) →
      (addClqToTree n w Q t).WF n ∧
      ∀ y < 2 ^ n, (addClqToTree n w Q t).get n y = t.get n y + if Q.contains y then w else 0
  | [], t, ht, _, _ => ⟨ht, by simp [addClqToTree]⟩
  | u :: us, t, ht, hnd, hlt => by
    rw [List.nodup_cons] at hnd
    have hu : u < 2 ^ n := hlt u (List.mem_cons_self ..)
    have hus : ∀ z ∈ us, z < 2 ^ n := fun z hz => hlt z (List.mem_cons_of_mem u hz)
    have ht' : (t.insertAdd n u w).WF n := STree.insertAdd_wf u w ht
    have hrec := addClqToTree_spec n w us (t.insertAdd n u w) ht' hnd.2 hus
    refine ⟨hrec.1, fun y hy => ?_⟩
    unfold addClqToTree at hrec ⊢
    simp only [List.foldl_cons]
    rw [hrec.2 y hy, STree.get_insertAdd ht w hu hy]
    by_cases hyu : y = u
    · subst hyu
      have hnot : us.contains y = false := by
        cases hc : us.contains y
        · rfl
        · exfalso; exact hnd.1 (by simpa [List.contains_eq_mem] using hc)
      have hcon : (y :: us).contains y = true := by simp [List.contains_eq_mem]
      rw [hnot, hcon]
      simp
    · have hcon : (u :: us).contains y = us.contains y := by
        cases hc : us.contains y
        · cases hc2 : (u :: us).contains y
          · rfl
          · exfalso
            have hm : y ∈ u :: us := by simpa [List.contains_eq_mem] using hc2
            rcases List.mem_cons.mp hm with rfl | hmem
            · exact hyu rfl
            · have : us.contains y = true := by simp [List.contains_eq_mem, hmem]
              rw [hc] at this; exact Bool.false_ne_true this
        · have hm : y ∈ us := by simpa [List.contains_eq_mem] using hc
          have : y ∈ u :: us := List.mem_cons_of_mem u hm
          simp [List.contains_eq_mem, this]
      rw [hcon]
      simp [hyu]

def buildClqsTree (n : Nat) (clqs : List (Nat × List Nat)) : STree :=
  clqs.foldl (fun t c => addClqToTree n c.1 c.2 t) .zero

theorem buildClqsTree_spec {n s : Nat} (hs : s ≤ n) :
    ∀ (clqs : List (Nat × List Nat)) (t : STree), t.WF n →
      (∀ c ∈ clqs, checkClqRec n s c.2 = true) →
      ∀ {C : List Nat}, IsValidDeletionCode n s C →
        (clqs.foldl (fun acc c => addClqToTree n c.1 c.2 acc) t).WF n ∧
        (C.map fun x => (clqs.foldl (fun acc c => addClqToTree n c.1 c.2 acc) t).get n x).sum ≤
          (C.map fun x => t.get n x).sum + (clqs.map Prod.fst).sum
  | [], t, ht, _, _, _ => ⟨ht, by simp⟩
  | c :: cs, t, ht, hclqs, C, hC => by
    have hc_snd := checkClqRec_sound hs (hclqs c (List.mem_cons_self ..))
    have hadd := addClqToTree_spec n c.1 c.2 t ht hc_snd.1 hc_snd.2.1
    have hcs := buildClqsTree_spec hs cs (addClqToTree n c.1 c.2 t) hadd.1
      (fun z hz => hclqs z (List.mem_cons_of_mem c hz)) hC
    refine ⟨hcs.1, ?_⟩
    simp only [List.foldl_cons, List.map_cons, List.sum_cons]
    have hstep_eq : C.map (fun x => (addClqToTree n c.1 c.2 t).get n x) =
        C.map (fun x => t.get n x + if c.2.contains x then c.1 else 0) := by
      apply List.map_congr_left
      intro x hx
      exact hadd.2 x (hC.1 x hx)
    have hle1 : (C.filter (fun x => c.2.contains x)).length ≤ 1 := by
      apply filter_len_le_one_of_pairwise (fun x => c.2.contains x) C
      intro i j hi hj hij hpi hpj
      simp only [List.contains_eq_mem, decide_eq_true_eq] at hpi hpj
      have hpair := hC.2 i j hi hj hij
      rcases hc_snd.2.2 C[i] hpi C[j] hpj hpair.1 with ⟨d, hd1, hd2⟩
      exact hpair.2.1 d ⟨hd1, hd2⟩
    have hclq_bound : (C.map fun x => if c.2.contains x then c.1 else 0).sum ≤ c.1 := by
      rw [sum_ite_eq_mul_filter_rec (fun x => c.2.contains x) c.1 C]
      calc c.1 * (C.filter (fun x => c.2.contains x)).length ≤ c.1 * 1 := Nat.mul_le_mul_left c.1 hle1
        _ = c.1 := Nat.mul_one c.1
    have hadd_sum : (C.map fun x => (addClqToTree n c.1 c.2 t).get n x).sum ≤
        (C.map fun x => t.get n x).sum + c.1 := by
      rw [hstep_eq, sum_map_add_rec (fun x => t.get n x) (fun x => if c.2.contains x then c.1 else 0) C]
      omega
    have hcs2 := hcs.2
    omega

/-- Rank-1 CG cut validity checker (`q ≥ 1`, `S ⊂ [0, 2^(n-s))`, `|S| / q ≤ rhs`). -/
def checkCgRec (nd q rhs : Nat) (S : List Nat) : Bool :=
  (0 < q) && S.all (· < nd) && decide (S.length / q ≤ rhs)

/-- Single rank-1 CG cut evaluated via the EXACT same recursive `evalDual` operator! -/
def evalCgCut (n s w q : Nat) (S : List Nat) : STree :=
  let ind := buildBallTree (n - s) (S.map (·, 1))
  (evalDual n s ind).mapZero (fun c => (c / q) * w)

theorem evalCgCut_wf {n s : Nat} (hs : s ≤ n) (w q : Nat) (S : List Nat) :
    (evalCgCut n s w q S).WF n := by
  unfold evalCgCut
  exact STree.mapZero_wf _ (evalDual_wf n s _ hs (buildBallTree_wf (n - s) _))

theorem sum_evalCgCut_le {n s w q rhs : Nat} (hs : s ≤ n) {S C : List Nat}
    (hcg : checkCgRec (2 ^ (n - s)) q rhs S = true) (hC : IsValidDeletionCode n s C) :
    (C.map fun x => (evalCgCut n s w q S).get n x).sum ≤ rhs * w := by
  simp only [checkCgRec, Bool.and_eq_true, List.all_eq_true, decide_eq_true_eq] at hcg
  rcases hcg with ⟨⟨hq, hS_lt⟩, hdiv_le⟩
  let ind := buildBallTree (n - s) (S.map (·, 1))
  have hind_wf : ind.WF (n - s) := buildBallTree_wf (n - s) _
  have hind_sum : ind.sum (n - s) = S.length := by
    have h1 : ∀ p ∈ S.map (·, 1), p.1 < 2 ^ (n - s) := by
      intro p hp
      rw [List.mem_map] at hp
      rcases hp with ⟨d, hd, rfl⟩
      exact hS_lt d hd
    have hsum := buildBallTree_sum (n - s) (S.map (·, 1)) h1
    have hlen : ((S.map (·, 1)).map Prod.snd).sum = S.length := by
      rw [List.map_map]
      exact sum_map_one_rec S
    exact hsum.trans hlen
  have heval_wf : (evalDual n s ind).WF n := evalDual_wf n s ind hs hind_wf
  have hf0 : (0 / q) * w = 0 := by simp
  have heq : C.map (fun x => (evalCgCut n s w q S).get n x) =
      C.map (fun x => ((evalDual n s ind).get n x / q) * w) := by
    apply List.map_congr_left
    intro x _
    exact STree.get_mapZero hf0 heval_wf x
  rw [heq, sum_map_mul_right_rec (fun x => (evalDual n s ind).get n x / q) w C]
  have hsum_raw : (C.map fun x => (evalDual n s ind).get n x).sum ≤ S.length := by
    rw [← hind_sum]
    exact sum_evalDual_le hs ind hind_wf hC
  have hq_mul : (C.map fun x => (evalDual n s ind).get n x / q).sum * q ≤ S.length := by
    rw [← sum_map_mul_right_rec (fun x => (evalDual n s ind).get n x / q) q C]
    have hterm := sum_map_le_of_le_rec
      (fun x => ((evalDual n s ind).get n x / q) * q)
      (fun x => (evalDual n s ind).get n x)
      (fun x => Nat.div_mul_le_self _ q) C
    omega
  have hdiv_sum : (C.map fun x => (evalDual n s ind).get n x / q).sum ≤ rhs := by
    have := (Nat.le_div_iff_mul_le hq).mpr hq_mul
    omega
  exact Nat.mul_le_mul_right w hdiv_sum

def buildCgsTree (n s : Nat) (cgs : List (Nat × Nat × Nat × List Nat)) : STree :=
  cgs.foldl (fun t cg => t.add (evalCgCut n s cg.1 cg.2.1 cg.2.2.2)) .zero

theorem buildCgsTree_spec {n s : Nat} (hs : s ≤ n) :
    ∀ (cgs : List (Nat × Nat × Nat × List Nat)) (t : STree), t.WF n →
      (∀ cg ∈ cgs, checkCgRec (2 ^ (n - s)) cg.2.1 cg.2.2.1 cg.2.2.2 = true) →
      ∀ {C : List Nat}, IsValidDeletionCode n s C →
        (cgs.foldl (fun acc cg => acc.add (evalCgCut n s cg.1 cg.2.1 cg.2.2.2)) t).WF n ∧
        (C.map fun x => (cgs.foldl (fun acc cg => acc.add (evalCgCut n s cg.1 cg.2.1 cg.2.2.2)) t).get n x).sum ≤
          (C.map fun x => t.get n x).sum + (cgs.map fun cg => cg.2.2.1 * cg.1).sum
  | [], t, ht, _, _, _ => ⟨ht, by simp⟩
  | cg :: cgs', t, ht, hcgs, C, hC => by
    have hcg_wf : (evalCgCut n s cg.1 cg.2.1 cg.2.2.2).WF n := evalCgCut_wf hs cg.1 cg.2.1 cg.2.2.2
    have hadd_wf : (t.add (evalCgCut n s cg.1 cg.2.1 cg.2.2.2)).WF n := STree.add_wf ht hcg_wf
    have hrec := buildCgsTree_spec hs cgs' (t.add (evalCgCut n s cg.1 cg.2.1 cg.2.2.2)) hadd_wf
      (fun z hz => hcgs z (List.mem_cons_of_mem cg hz)) hC
    refine ⟨hrec.1, ?_⟩
    simp only [List.foldl_cons, List.map_cons, List.sum_cons]
    have hstep_eq : C.map (fun x => (t.add (evalCgCut n s cg.1 cg.2.1 cg.2.2.2)).get n x) =
        C.map (fun x => t.get n x + (evalCgCut n s cg.1 cg.2.1 cg.2.2.2).get n x) := by
      apply List.map_congr_left
      intro x _
      exact STree.get_add ht hcg_wf x
    have hcg_le := sum_evalCgCut_le (w := cg.1) hs (hcgs cg (List.mem_cons_self ..)) hC
    have hstep_le : (C.map fun x => (t.add (evalCgCut n s cg.1 cg.2.1 cg.2.2.2)).get n x).sum ≤
        (C.map fun x => t.get n x).sum + cg.2.2.1 * cg.1 := by
      rw [hstep_eq, sum_map_add_rec (fun x => t.get n x) (fun x => (evalCgCut n s cg.1 cg.2.1 cg.2.2.2).get n x) C]
      omega
    have hrec2 := hrec.2
    omega

/-! ## 7. Combined Coverage Tree, Single-Pass `D_2` Checker, and Universal Weak Duality Theorem -/

/-- Single-orbit combined coverage tree `A_{n,s}^T y + C_CLQ^T λ + G_CG^T μ`. -/
def covTree1 (n s : Nat) (yList : List (Nat × Nat))
    (clqs : List (Nat × List Nat))
    (cgs : List (Nat × Nat × Nat × List Nat)) : STree :=
  let tBall := evalDual n s (buildBallTree (n - s) yList)
  let tClq := buildClqsTree n clqs
  let tCg := buildCgsTree n s cgs
  tBall.add (tClq.add tCg)

/-- Complement-symmetrized coverage tree `cov1(x) + cov1(bitComp n x)`. -/
def covSym2 (n s : Nat) (yList : List (Nat × Nat))
    (clqs : List (Nat × List Nat))
    (cgs : List (Nat × Nat × Nat × List Nat)) : STree :=
  let c1 := covTree1 n s yList clqs cgs
  c1.add c1.comp

/--
  Single structural pass checking `∀ x < 2^n, Lmin ≤ sym2(x) + sym2(bitRev n x)`.
  Maintains `revX = bitRev` incrementally down the tree with ZERO `bitRev` calls!
-/
def checkSym2Rev (n Lmin : Nat) (full : STree) : Nat → Nat → STree → Bool
  | 0, revX, .zero => decide (Lmin ≤ full.get n revX)
  | 0, revX, .leaf v => decide (Lmin ≤ v + full.get n revX)
  | k + 1, revX, .zero =>
    checkSym2Rev n Lmin full k (2 * revX) .zero &&
    checkSym2Rev n Lmin full k (2 * revX + 1) .zero
  | k + 1, revX, .node l r =>
    checkSym2Rev n Lmin full k (2 * revX) l &&
    checkSym2Rev n Lmin full k (2 * revX + 1) r
  | _, _, _ => false

theorem checkSym2Rev_spec (n Lmin : Nat) (full : STree) :
    ∀ (k revX : Nat) (t : STree), t.WF k →
      checkSym2Rev n Lmin full k revX t = true →
      ∀ x < 2 ^ k, Lmin ≤ t.get k x + full.get n (bitRev.go k x revX)
  | 0, revX, .zero, _, h, _, _ => by
    simp only [checkSym2Rev, decide_eq_true_eq] at h
    simpa [STree.get, bitRev.go] using h
  | 0, revX, .leaf v, _, h, _, _ => by
    simp only [checkSym2Rev, decide_eq_true_eq] at h
    simpa [STree.get, bitRev.go] using h
  | k + 1, revX, .zero, _, h, x, hx => by
    have hpow : 2 ^ (k + 1) = 2 * 2 ^ k := by rw [Nat.pow_succ, Nat.mul_comm]
    have hx' : x / 2 < 2 ^ k := by rw [hpow] at hx; omega
    simp only [checkSym2Rev, Bool.and_eq_true] at h
    simp only [bitRev.go]
    by_cases hev : x % 2 = 0
    · rw [hev, Nat.add_zero]
      exact checkSym2Rev_spec n Lmin full k (2 * revX) .zero trivial h.1 (x / 2) hx'
    · have h1 : x % 2 = 1 := by omega
      rw [h1]
      exact checkSym2Rev_spec n Lmin full k (2 * revX + 1) .zero trivial h.2 (x / 2) hx'
  | k + 1, revX, .node l r, ht, h, x, hx => by
    have hpow : 2 ^ (k + 1) = 2 * 2 ^ k := by rw [Nat.pow_succ, Nat.mul_comm]
    have hx' : x / 2 < 2 ^ k := by rw [hpow] at hx; omega
    simp only [checkSym2Rev, Bool.and_eq_true] at h
    simp only [STree.get, bitRev.go]
    by_cases hev : x % 2 = 0
    · simp only [hev, beq_self_eq_true, ↓reduceIte, Nat.add_zero]
      exact checkSym2Rev_spec n Lmin full k (2 * revX) l ht.1 h.1 (x / 2) hx'
    · have h1 : x % 2 = 1 := by omega
      have h10 : (1 == 0) = false := rfl
      simp only [h1, h10, Bool.false_eq_true, ↓reduceIte]
      exact checkSym2Rev_spec n Lmin full k (2 * revX + 1) r ht.2 h.2 (x / 2) hx'
  | 0, _, .node _ _, ht, _, _, _ => False.elim ht
  | _ + 1, _, .leaf _, ht, _, _, _ => by cases ht

/--
  Universal Pure-Kernel Recursive Weak Duality Upper Bound Theorem for ALL `(n, s)` (`s ≤ n`).
  Supports ball weights `yList`, non-ball cliques `clqs`, rank-1 CG cuts `cgs`, and `D_2 = <c, r>`
  orbit symmetrization with ZERO flat ball tables and ZERO clique edge witnesses!
-/
theorem weak_duality_rec {n s Lmin M : Nat} (hs : s ≤ n)
    (yList : List (Nat × Nat))
    (hy : yList.all (fun p => p.1 < 2 ^ (n - s)) = true)
    (clqs : List (Nat × List Nat))
    (hclqs : ∀ c ∈ clqs, checkClqRec n s c.2 = true)
    (cgs : List (Nat × Nat × Nat × List Nat))
    (hcgs : ∀ cg ∈ cgs, checkCgRec (2 ^ (n - s)) cg.2.1 cg.2.2.1 cg.2.2.2 = true)
    (hwords : checkSym2Rev n Lmin (covSym2 n s yList clqs cgs) n 0 (covSym2 n s yList clqs cgs) = true)
    (hbound : 4 * ((yList.map Prod.snd).sum + (clqs.map Prod.fst).sum +
        (cgs.map fun cg => cg.2.2.1 * cg.1).sum) < Lmin * (M + 1))
    {C : List Nat} (hC : IsValidDeletionCode n s C) :
    C.length ≤ M := by
  let tY := buildBallTree (n - s) yList
  let tBall := evalDual n s tY
  let tClq := buildClqsTree n clqs
  let tCg := buildCgsTree n s cgs
  let c1 := covTree1 n s yList clqs cgs
  let s2 := covSym2 n s yList clqs cgs
  have htY_wf : tY.WF (n - s) := buildBallTree_wf (n - s) yList
  have htBall_wf : tBall.WF n := evalDual_wf n s tY hs htY_wf
  have hclq_all := buildClqsTree_spec hs clqs .zero trivial hclqs hC
  have htClq_wf : tClq.WF n := hclq_all.1
  have hcg_all := buildCgsTree_spec hs cgs .zero trivial hcgs hC
  have htCg_wf : tCg.WF n := hcg_all.1
  have hc1_wf : c1.WF n := STree.add_wf htBall_wf (STree.add_wf htClq_wf htCg_wf)
  have hs2_wf : s2.WF n := STree.add_wf hc1_wf (STree.comp_wf hc1_wf)
  have hy_all : ∀ p ∈ yList, p.1 < 2 ^ (n - s) := by
    intro p hp
    have := List.all_eq_true.mp hy p hp
    simpa [decide_eq_true_eq] using this
  have hsum_c1 : ∀ {D : List Nat}, IsValidDeletionCode n s D →
      (D.map fun x => c1.get n x).sum ≤
        (yList.map Prod.snd).sum + (clqs.map Prod.fst).sum +
        (cgs.map fun cg => cg.2.2.1 * cg.1).sum := by
    intro D hD
    have hsplit : (D.map fun x => c1.get n x).sum =
        (D.map fun x => tBall.get n x).sum +
        (D.map fun x => tClq.get n x).sum +
        (D.map fun x => tCg.get n x).sum := by
      have hm : D.map (fun x => c1.get n x) =
          D.map (fun x => tBall.get n x + (tClq.get n x + tCg.get n x)) := by
        apply List.map_congr_left
        intro x _
        change (tBall.add (tClq.add tCg)).get n x = _
        rw [STree.get_add htBall_wf (STree.add_wf htClq_wf htCg_wf) x,
            STree.get_add htClq_wf htCg_wf x]
      rw [hm, sum_map_add_rec (fun x => tBall.get n x) (fun x => tClq.get n x + tCg.get n x) D,
          sum_map_add_rec (fun x => tClq.get n x) (fun x => tCg.get n x) D]
      omega
    have h1 : (D.map fun x => tBall.get n x).sum ≤ (yList.map Prod.snd).sum := by
      rw [← buildBallTree_sum (n - s) yList hy_all]
      exact sum_evalDual_le hs tY htY_wf hD
    have h2 : (D.map fun x => tClq.get n x).sum ≤ (clqs.map Prod.fst).sum := by
      have hspec := (buildClqsTree_spec hs clqs .zero trivial hclqs hD).2
      have hz : (D.map fun x => STree.zero.get n x).sum = 0 := sum_map_zero_rec D
      rw [hz, Nat.zero_add] at hspec
      exact hspec
    have h3 : (D.map fun x => tCg.get n x).sum ≤ (cgs.map fun cg => cg.2.2.1 * cg.1).sum := by
      have hspec := (buildCgsTree_spec hs cgs .zero trivial hcgs hD).2
      have hz : (D.map fun x => STree.zero.get n x).sum = 0 := sum_map_zero_rec D
      rw [hz, Nat.zero_add] at hspec
      exact hspec
    omega
  have hall_cov : ∀ x < 2 ^ n, Lmin ≤ s2.get n x + s2.get n (bitRev n x) :=
    checkSym2Rev_spec n Lmin s2 n 0 s2 hs2_wf hwords
  have hcov_C : ∀ x ∈ C, Lmin ≤ s2.get n x + s2.get n (bitRev n x) :=
    fun x hx => hall_cov x (hC.1 x hx)
  have h_lhs : Lmin * C.length ≤ (C.map fun x => s2.get n x + s2.get n (bitRev n x)).sum :=
    mul_length_le_sum Lmin (fun x => s2.get n x + s2.get n (bitRev n x)) C hcov_C
  have hs2_eq : ∀ x < 2 ^ n, s2.get n x = c1.get n x + c1.get n (bitComp n x) := by
    intro x hx
    change (c1.add c1.comp).get n x = _
    rw [STree.get_add hc1_wf (STree.comp_wf hc1_wf) x, STree.get_comp hc1_wf hx]
  have h_d2_eq : (C.map fun x => s2.get n x + s2.get n (bitRev n x)).sum =
      ((C.map (applyD2 n 0)).map fun x => c1.get n x).sum +
      ((C.map (applyD2 n 1)).map fun x => c1.get n x).sum +
      ((C.map (applyD2 n 2)).map fun x => c1.get n x).sum +
      ((C.map (applyD2 n 3)).map fun x => c1.get n x).sum := by
    have hm : C.map (fun x => s2.get n x + s2.get n (bitRev n x)) =
        C.map (fun x =>
          (c1.get n (applyD2 n 0 x) + c1.get n (applyD2 n 1 x)) +
          (c1.get n (applyD2 n 2 x) + c1.get n (applyD2 n 3 x))) := by
      apply List.map_congr_left
      intro x hx
      have hxl : x < 2 ^ n := hC.1 x hx
      have hrl : bitRev n x < 2 ^ n := by
        simpa [applyD2] using applyD2_lt (n := n) (g := 2) hxl
      rw [hs2_eq x hxl, hs2_eq (bitRev n x) hrl]
      simp [applyD2]
    rw [hm,
        sum_map_add_rec (fun x => c1.get n (applyD2 n 0 x) + c1.get n (applyD2 n 1 x))
                        (fun x => c1.get n (applyD2 n 2 x) + c1.get n (applyD2 n 3 x)) C,
        sum_map_add_rec (fun x => c1.get n (applyD2 n 0 x)) (fun x => c1.get n (applyD2 n 1 x)) C,
        sum_map_add_rec (fun x => c1.get n (applyD2 n 2 x)) (fun x => c1.get n (applyD2 n 3 x)) C]
    simp only [List.map_map, Function.comp_def]
    omega
  have hg0 := hsum_c1 (isValidDeletionCode_map_applyD2 hs (g := 0) hC)
  have hg1 := hsum_c1 (isValidDeletionCode_map_applyD2 hs (g := 1) hC)
  have hg2 := hsum_c1 (isValidDeletionCode_map_applyD2 hs (g := 2) hC)
  have hg3 := hsum_c1 (isValidDeletionCode_map_applyD2 hs (g := 3) hC)
  have h_tot : Lmin * C.length < Lmin * (M + 1) := by omega
  rcases Nat.lt_or_ge C.length (M + 1) with hlt | hge
  · omega
  · have : Lmin * (M + 1) ≤ Lmin * C.length := Nat.mul_le_mul_left Lmin hge
    omega

/-- Full `D_2 = <c, r>` symmetrized coverage tree `(I + P_r)(I + P_c) cov1` — evaluated ONCE! -/
def covSym4 (n s : Nat) (yList : List (Nat × Nat))
    (clqs : List (Nat × List Nat))
    (cgs : List (Nat × Nat × Nat × List Nat)) : STree :=
  let c1 := covTree1 n s yList clqs cgs
  let s2 := c1.add c1.comp
  s2.add (s2.rev n)

/--
  Fast Single-Pass Universal Pure-Kernel Weak Duality Theorem using `covSym4.allGe`:
  Computes `(I + P_r)(I + P_c) cov1` ONCE (instead of per-word lookups) and checks all `2^n`
  words in ONE `O(2^n)` tree traversal!
-/
theorem weak_duality_rec_fast {n s Lmin M : Nat} (hs : s ≤ n)
    (yList : List (Nat × Nat))
    (hy : yList.all (fun p => p.1 < 2 ^ (n - s)) = true)
    (clqs : List (Nat × List Nat))
    (hclqs : ∀ c ∈ clqs, checkClqRec n s c.2 = true)
    (cgs : List (Nat × Nat × Nat × List Nat))
    (hcgs : ∀ cg ∈ cgs, checkCgRec (2 ^ (n - s)) cg.2.1 cg.2.2.1 cg.2.2.2 = true)
    (hwords : (covSym4 n s yList clqs cgs).allGe Lmin n = true)
    (hbound : 4 * ((yList.map Prod.snd).sum + (clqs.map Prod.fst).sum +
        (cgs.map fun cg => cg.2.2.1 * cg.1).sum) < Lmin * (M + 1))
    {C : List Nat} (hC : IsValidDeletionCode n s C) :
    C.length ≤ M := by
  let tY := buildBallTree (n - s) yList
  let tBall := evalDual n s tY
  let tClq := buildClqsTree n clqs
  let tCg := buildCgsTree n s cgs
  let c1 := covTree1 n s yList clqs cgs
  let s2 := c1.add c1.comp
  let s4 := s2.add (s2.rev n)
  have htY_wf : tY.WF (n - s) := buildBallTree_wf (n - s) yList
  have htBall_wf : tBall.WF n := evalDual_wf n s tY hs htY_wf
  have hclq_all := buildClqsTree_spec hs clqs .zero trivial hclqs hC
  have htClq_wf : tClq.WF n := hclq_all.1
  have hcg_all := buildCgsTree_spec hs cgs .zero trivial hcgs hC
  have htCg_wf : tCg.WF n := hcg_all.1
  have hc1_wf : c1.WF n := STree.add_wf htBall_wf (STree.add_wf htClq_wf htCg_wf)
  have hs2_wf : s2.WF n := STree.add_wf hc1_wf (STree.comp_wf hc1_wf)
  have hs4_wf : s4.WF n := STree.add_wf hs2_wf (STree.rev_wf hs2_wf)
  have hy_all : ∀ p ∈ yList, p.1 < 2 ^ (n - s) := by
    intro p hp
    have := List.all_eq_true.mp hy p hp
    simpa [decide_eq_true_eq] using this
  have hsum_c1 : ∀ {D : List Nat}, IsValidDeletionCode n s D →
      (D.map fun x => c1.get n x).sum ≤
        (yList.map Prod.snd).sum + (clqs.map Prod.fst).sum +
        (cgs.map fun cg => cg.2.2.1 * cg.1).sum := by
    intro D hD
    have hsplit : (D.map fun x => c1.get n x).sum =
        (D.map fun x => tBall.get n x).sum +
        (D.map fun x => tClq.get n x).sum +
        (D.map fun x => tCg.get n x).sum := by
      have hm : D.map (fun x => c1.get n x) =
          D.map (fun x => tBall.get n x + (tClq.get n x + tCg.get n x)) := by
        apply List.map_congr_left
        intro x _
        change (tBall.add (tClq.add tCg)).get n x = _
        rw [STree.get_add htBall_wf (STree.add_wf htClq_wf htCg_wf) x,
            STree.get_add htClq_wf htCg_wf x]
      rw [hm, sum_map_add_rec (fun x => tBall.get n x) (fun x => tClq.get n x + tCg.get n x) D,
          sum_map_add_rec (fun x => tClq.get n x) (fun x => tCg.get n x) D]
      omega
    have h1 : (D.map fun x => tBall.get n x).sum ≤ (yList.map Prod.snd).sum := by
      rw [← buildBallTree_sum (n - s) yList hy_all]
      exact sum_evalDual_le hs tY htY_wf hD
    have h2 : (D.map fun x => tClq.get n x).sum ≤ (clqs.map Prod.fst).sum := by
      have hspec := (buildClqsTree_spec hs clqs .zero trivial hclqs hD).2
      have hz : (D.map fun x => STree.zero.get n x).sum = 0 := sum_map_zero_rec D
      rw [hz, Nat.zero_add] at hspec
      exact hspec
    have h3 : (D.map fun x => tCg.get n x).sum ≤ (cgs.map fun cg => cg.2.2.1 * cg.1).sum := by
      have hspec := (buildCgsTree_spec hs cgs .zero trivial hcgs hD).2
      have hz : (D.map fun x => STree.zero.get n x).sum = 0 := sum_map_zero_rec D
      rw [hz, Nat.zero_add] at hspec
      exact hspec
    omega
  have hall_cov : ∀ x < 2 ^ n, Lmin ≤ s4.get n x :=
    STree.allGe_spec Lmin hs4_wf hwords
  have hcov_C : ∀ x ∈ C, Lmin ≤ s4.get n x :=
    fun x hx => hall_cov x (hC.1 x hx)
  have h_lhs : Lmin * C.length ≤ (C.map fun x => s4.get n x).sum :=
    mul_length_le_sum Lmin (fun x => s4.get n x) C hcov_C
  have hs2_eq : ∀ x < 2 ^ n, s2.get n x = c1.get n x + c1.get n (bitComp n x) := by
    intro x hx
    change (c1.add c1.comp).get n x = _
    rw [STree.get_add hc1_wf (STree.comp_wf hc1_wf) x, STree.get_comp hc1_wf hx]
  have hs4_eq : ∀ x < 2 ^ n, s4.get n x = s2.get n x + s2.get n (bitRev n x) := by
    intro x hx
    change (s2.add (s2.rev n)).get n x = _
    rw [STree.get_add hs2_wf (STree.rev_wf hs2_wf) x, STree.get_rev hs2_wf hx]
  have h_d2_eq : (C.map fun x => s4.get n x).sum =
      ((C.map (applyD2 n 0)).map fun x => c1.get n x).sum +
      ((C.map (applyD2 n 1)).map fun x => c1.get n x).sum +
      ((C.map (applyD2 n 2)).map fun x => c1.get n x).sum +
      ((C.map (applyD2 n 3)).map fun x => c1.get n x).sum := by
    have hm : C.map (fun x => s4.get n x) =
        C.map (fun x =>
          (c1.get n (applyD2 n 0 x) + c1.get n (applyD2 n 1 x)) +
          (c1.get n (applyD2 n 2 x) + c1.get n (applyD2 n 3 x))) := by
      apply List.map_congr_left
      intro x hx
      have hxl : x < 2 ^ n := hC.1 x hx
      have hrl : bitRev n x < 2 ^ n := by
        simpa [applyD2] using applyD2_lt (n := n) (g := 2) hxl
      rw [hs4_eq x hxl, hs2_eq x hxl, hs2_eq (bitRev n x) hrl]
      simp [applyD2]
    rw [hm,
        sum_map_add_rec (fun x => c1.get n (applyD2 n 0 x) + c1.get n (applyD2 n 1 x))
                        (fun x => c1.get n (applyD2 n 2 x) + c1.get n (applyD2 n 3 x)) C,
        sum_map_add_rec (fun x => c1.get n (applyD2 n 0 x)) (fun x => c1.get n (applyD2 n 1 x)) C,
        sum_map_add_rec (fun x => c1.get n (applyD2 n 2 x)) (fun x => c1.get n (applyD2 n 3 x)) C]
    simp only [List.map_map, Function.comp_def]
    omega
  have hg0 := hsum_c1 (isValidDeletionCode_map_applyD2 hs (g := 0) hC)
  have hg1 := hsum_c1 (isValidDeletionCode_map_applyD2 hs (g := 1) hC)
  have hg2 := hsum_c1 (isValidDeletionCode_map_applyD2 hs (g := 2) hC)
  have hg3 := hsum_c1 (isValidDeletionCode_map_applyD2 hs (g := 3) hC)
  have h_tot : Lmin * C.length < Lmin * (M + 1) := by omega
  rcases Nat.lt_or_ge C.length (M + 1) with hlt | hge
  · omega
  · have : Lmin * (M + 1) ≤ Lmin * C.length := Nat.mul_le_mul_left Lmin hge
    omega

end DeletionCode.RecDual
