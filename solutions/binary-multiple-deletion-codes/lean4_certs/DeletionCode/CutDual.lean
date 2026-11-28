/-
  DeletionCode/CutDual.lean — Pure-Kernel Weak LP + Cutting-Plane Duality Upper Bounds
  Supporting:
    1. Ball inequalities (`D_s` descendant weights `y_d`)
    2. Non-ball maximal cliques (`CLQ`: pairwise intersecting `D_s` balls)
    3. `2-of-m` Chvátal-Gomory rank-1 cuts (`M23`, `CG25`, etc.)
    4. Exact `D_2 = <c, r>` automorphism reduction (`bitComp`, `bitRev`)
  Zero Mathlib, zero sorryAx, zero native_decide / Lean.ofReduceBool.
-/
import DeletionCode.Basic
import DeletionCode.DualLP

set_option maxRecDepth 32768

namespace DeletionCode.CutDual

open DeletionCode
open DeletionCode.DualLP

/-! ## 1. `D_2 = <c, r>` Automorphism Invariance of `IsSubseq` and `InDelBall` -/

theorem isSubseq_map (f : Bool → Bool) :
    ∀ {u v : List Bool}, IsSubseq u v → IsSubseq (u.map f) (v.map f)
  | _, _, .nil => .nil
  | _, _, .cons_keep b h => .cons_keep (f b) (isSubseq_map f h)
  | _, _, .cons_drop b h => .cons_drop (f b) (isSubseq_map f h)

theorem isSubseq_append {u₁ v₁ u₂ v₂ : List Bool}
    (h₁ : IsSubseq u₁ v₁) (h₂ : IsSubseq u₂ v₂) : IsSubseq (u₁ ++ u₂) (v₁ ++ v₂) := by
  induction h₁ with
  | nil => simpa using h₂
  | cons_keep b _ ih => simpa using IsSubseq.cons_keep b ih
  | cons_drop b _ ih => simpa using IsSubseq.cons_drop b ih

theorem isSubseq_reverse :
    ∀ {u v : List Bool}, IsSubseq u v → IsSubseq u.reverse v.reverse
  | _, _, .nil => .nil
  | _, _, .cons_keep b h => by
    simp only [List.reverse_cons]
    exact isSubseq_append (isSubseq_reverse h) (.cons_keep b .nil)
  | _, _, .cons_drop b h => by
    simp only [List.reverse_cons]
    simpa using isSubseq_append (isSubseq_reverse h) (.cons_drop b .nil)

private theorem natToWord_bitComp :
    ∀ (n x : Nat), x < 2 ^ n → natToWord n (bitComp n x) = (natToWord n x).map Bool.not
  | 0, _, _ => rfl
  | n + 1, x, hx => by
    have hpow : 2 ^ (n + 1) = 2 * 2 ^ n := by rw [Nat.pow_succ, Nat.mul_comm]
    have hpos : 0 < 2 ^ n := Nat.two_pow_pos n
    have hlt_pow : x < 2 * 2 ^ n := hpow ▸ hx
    have hdiv_lt : x / 2 < 2 ^ n := by omega
    have hbc_succ : bitComp (n + 1) x = 2 * bitComp n (x / 2) + (1 - x % 2) := by
      unfold bitComp
      rw [hpow]
      omega
    have hmod_bc : bitComp (n + 1) x % 2 = 1 - x % 2 := by
      rw [hbc_succ]
      omega
    have hdiv_bc : bitComp (n + 1) x / 2 = bitComp n (x / 2) := by
      rw [hbc_succ]
      omega
    have hhead : ((bitComp (n + 1) x % 2 == 1) : Bool) = !(x % 2 == 1) := by
      rw [hmod_bc]
      have hx2 : x % 2 < 2 := Nat.mod_lt x (by omega)
      rcases Nat.lt_succ_iff_lt_or_eq.mp hx2 with h0 | h1
      · have : x % 2 = 0 := by omega
        simp [this]
      · simp [h1]
    simp only [natToWord, List.map_cons, hdiv_bc, hhead]
    congr 1
    exact natToWord_bitComp n (x / 2) hdiv_lt

private theorem natToWord_add_mul_pow2 :
    ∀ (k a b : Nat), a < 2 ^ k →
      natToWord (k + 1) (a + b % 2 * 2 ^ k) = natToWord k a ++ [(b % 2 == 1)]
  | 0, a, b, ha => by
    have ha0 : a = 0 := by simpa using ha
    subst ha0
    simp [natToWord]
  | k + 1, a, b, ha => by
    have hpow : 2 ^ (k + 1) = 2 * 2 ^ k := by rw [Nat.pow_succ, Nat.mul_comm]
    have ha2 : a < 2 * 2 ^ k := hpow ▸ ha
    have hlin : a + b % 2 * 2 ^ (k + 1) = a + 2 * (b % 2 * 2 ^ k) := by
      rw [hpow, Nat.mul_left_comm (b % 2) 2 (2 ^ k)]
    have hmod : (a + b % 2 * 2 ^ (k + 1)) % 2 = a % 2 := by
      rw [hlin]; omega
    have hdiv : (a + b % 2 * 2 ^ (k + 1)) / 2 = a / 2 + b % 2 * 2 ^ k := by
      rw [hlin]; omega
    change ((a + b % 2 * 2 ^ (k + 1)) % 2 == 1) :: natToWord (k + 1) ((a + b % 2 * 2 ^ (k + 1)) / 2) =
           (a % 2 == 1) :: (natToWord k (a / 2) ++ [(b % 2 == 1)])
    rw [hmod, hdiv, natToWord_add_mul_pow2 k (a / 2) b (by omega)]

private theorem bitRev_go_eq (k cur acc : Nat) :
    bitRev.go k cur acc = bitRev.go k cur 0 + acc * 2 ^ k := by
  induction k generalizing cur acc with
  | zero => simp [bitRev.go]
  | succ k' ih =>
    simp only [bitRev.go, Nat.mul_zero, Nat.zero_add]
    rw [ih (cur / 2) (2 * acc + cur % 2), ih (cur / 2) (cur % 2)]
    have hpow : 2 ^ (k' + 1) = 2 * 2 ^ k' := by rw [Nat.pow_succ, Nat.mul_comm]
    have hmul : (2 * acc + cur % 2) * 2 ^ k' = acc * (2 * 2 ^ k') + cur % 2 * 2 ^ k' := by
      rw [Nat.add_mul, Nat.mul_comm 2 acc, Nat.mul_assoc]
    rw [hpow, hmul]
    omega

private theorem bitRev_lt (k cur : Nat) : bitRev k cur < 2 ^ k := by
  unfold bitRev
  induction k generalizing cur with
  | zero => simp [bitRev.go]
  | succ k' ih =>
    simp only [bitRev.go, Nat.mul_zero, Nat.zero_add]
    rw [bitRev_go_eq k' (cur / 2) (cur % 2)]
    have h1 := ih (cur / 2)
    have h2 : cur % 2 ≤ 1 := by omega
    have h3 : cur % 2 * 2 ^ k' ≤ 2 ^ k' := by
      simpa using Nat.mul_le_mul_right (2 ^ k') h2
    have hpow : 2 ^ (k' + 1) = 2 * 2 ^ k' := by rw [Nat.pow_succ, Nat.mul_comm]
    rw [hpow]
    omega

private theorem natToWord_bitRev :
    ∀ (n x : Nat), natToWord n (bitRev n x) = (natToWord n x).reverse
  | 0, _ => rfl
  | n + 1, x => by
    have hstep : bitRev (n + 1) x = bitRev n (x / 2) + (x % 2) * 2 ^ n := by
      unfold bitRev
      simp only [bitRev.go, Nat.mul_zero, Nat.zero_add]
      exact bitRev_go_eq n (x / 2) (x % 2)
    rw [hstep, natToWord_add_mul_pow2 n (bitRev n (x / 2)) x (bitRev_lt n (x / 2))]
    simp only [natToWord, List.reverse_cons]
    congr 1
    exact natToWord_bitRev n (x / 2)

/-- `D_2 = <c, r>` group action on `n`-bit words (`0 = id`, `1 = c`, `2 = r`, `3 = c ∘ r`). -/
def applyD2 (n g x : Nat) : Nat :=
  if g = 0 then x
  else if g = 1 then bitComp n x
  else if g = 2 then bitRev n x
  else bitComp n (bitRev n x)

theorem applyD2_lt {n g x : Nat} (hx : x < 2 ^ n) : applyD2 n g x < 2 ^ n := by
  by_cases h0 : g = 0
  · simp [applyD2, h0, hx]
  · by_cases h1 : g = 1
    · simp [applyD2, h1]
      unfold bitComp; omega
    · by_cases h2 : g = 2
      · simp [applyD2, h2]
        exact bitRev_lt n x
      · simp [applyD2, h0, h1, h2]
        unfold bitComp
        have h := bitRev_lt n x
        omega

theorem bitComp_involutive {n x : Nat} (hx : x < 2 ^ n) : bitComp n (bitComp n x) = x := by
  unfold bitComp; omega

private theorem bitRev_go_inv_aux :
    ∀ (n x : Nat), x < 2 ^ n → bitRev n (bitRev n x) = x := by
  intro n x hx
  have h1 : natToWord n (bitRev n (bitRev n x)) = natToWord n x := by
    rw [natToWord_bitRev, natToWord_bitRev, List.reverse_reverse]
  have hm := natToWord_eq_mod n _ _ h1
  have hlt := bitRev_lt n (bitRev n x)
  rw [Nat.mod_eq_of_lt hlt, Nat.mod_eq_of_lt hx] at hm
  exact hm

/-- Every element of `D_2 = Z_2 × Z_2` is an involution (`g (g x) = x`). -/
theorem applyD2_involutive {n g x : Nat} (hx : x < 2 ^ n) : applyD2 n g (applyD2 n g x) = x := by
  by_cases h0 : g = 0
  · simp [applyD2, h0]
  · by_cases h1 : g = 1
    · simp [applyD2, h1]
      exact bitComp_involutive hx
    · by_cases h2 : g = 2
      · simp [applyD2, h2]
        exact bitRev_go_inv_aux n x hx
      · simp [applyD2, h0, h1, h2]
        have hcomp_rev : ∀ y, y < 2 ^ n → bitRev n (bitComp n y) = bitComp n (bitRev n y) := by
          intro y hy
          have h1 : natToWord n (bitRev n (bitComp n y)) = natToWord n (bitComp n (bitRev n y)) := by
            rw [natToWord_bitRev, natToWord_bitComp n y hy,
                natToWord_bitComp n (bitRev n y) (bitRev_lt n y), natToWord_bitRev, List.map_reverse]
          have hm := natToWord_eq_mod n _ _ h1
          have hlt1 := bitRev_lt n (bitComp n y)
          have hlt2 : bitComp n (bitRev n y) < 2 ^ n := by
            unfold bitComp; have := bitRev_lt n y; omega
          rw [Nat.mod_eq_of_lt hlt1, Nat.mod_eq_of_lt hlt2] at hm
          exact hm
        have hbr := bitRev_lt n x
        rw [hcomp_rev (bitRev n x) hbr, bitRev_go_inv_aux n x hx, bitComp_involutive hx]

theorem inDelBall_applyD2 {n s g x d : Nat} (hs : s ≤ n) (hx : x < 2 ^ n) (hd : d < 2 ^ (n - s))
    (h : InDelBall s (natToWord n x) (natToWord (n - s) d)) :
    InDelBall s (natToWord n (applyD2 n g x)) (natToWord (n - s) (applyD2 (n - s) g d)) := by
  by_cases h0 : g = 0
  · simp [applyD2, h0, h]
  · by_cases h1 : g = 1
    · simp [applyD2, h1]
      refine ⟨?_, ?_⟩
      · rw [natToWord_bitComp n x hx, natToWord_bitComp (n - s) d hd]
        exact isSubseq_map Bool.not h.1
      · rw [natToWord_length, natToWord_length]
        omega
    · by_cases h2 : g = 2
      · simp [applyD2, h2]
        refine ⟨?_, ?_⟩
        · rw [natToWord_bitRev n x, natToWord_bitRev (n - s) d]
          exact isSubseq_reverse h.1
        · rw [natToWord_length, natToWord_length]
          omega
      · simp [applyD2, h0, h1, h2]
        refine ⟨?_, ?_⟩
        · rw [natToWord_bitComp n _ (bitRev_lt n x), natToWord_bitRev n x,
              natToWord_bitComp (n - s) _ (bitRev_lt (n - s) d), natToWord_bitRev (n - s) d]
          exact isSubseq_map Bool.not (isSubseq_reverse h.1)
        · rw [natToWord_length, natToWord_length]
          omega

/-! ## 2. Exact `s = 2` Ball Descriptors, `CLQ` Word Cliques, General `CG` Cuts & `D_2` Weak Duality -/

theorem del2Nat_lt {n i j x : Nat} (hx : x < 2 ^ n) (hi : i < j) (hj : j < n) :
    del2Nat x i j < 2 ^ (n - 2) := by
  unfold del2Nat
  have h1 : delBit x j < 2 ^ (n - 1) := delBit_lt_pub n j x hx hj
  have h2 : delBit (delBit x j) i < 2 ^ (n - 1 - 1) :=
    delBit_lt_pub (n - 1) i (delBit x j) h1 (by omega)
  simpa [Nat.sub_sub] using h2

def allPairs2 (n : Nat) : List (Nat × Nat) :=
  (List.range n).flatMap fun i =>
    ((List.range n).filter (i < ·)).map fun j => (i, j)

theorem mem_allPairs2 {n i j : Nat} : (i, j) ∈ allPairs2 n ↔ i < j ∧ j < n := by
  simp only [allPairs2, List.mem_flatMap, List.mem_map, List.mem_filter, List.mem_range,
    decide_eq_true_eq]
  constructor
  · rintro ⟨a, ha, b, ⟨hb, hab⟩, hpair⟩
    have : a = i := congrArg Prod.fst hpair
    have : b = j := congrArg Prod.snd hpair
    omega
  · rintro ⟨hij, hj⟩
    exact ⟨i, by omega, j, ⟨hj, hij⟩, rfl⟩

def dedupNat : List Nat → List Nat
  | [] => []
  | x :: xs => let r := dedupNat xs; if r.contains x then r else x :: r

theorem mem_dedupNat {x : Nat} : ∀ {L : List Nat}, x ∈ dedupNat L ↔ x ∈ L
  | [] => by simp [dedupNat]
  | y :: ys => by
    simp only [dedupNat]
    split
    · rename_i h
      simp only [List.contains_eq_mem, decide_eq_true_eq] at h
      rw [mem_dedupNat]
      constructor
      · intro hx; exact List.mem_cons_of_mem y hx
      · intro hx
        rcases List.mem_cons.mp hx with rfl | hys
        · exact mem_dedupNat.mp h
        · exact hys
    · rename_i h
      simp only [List.contains_eq_mem, decide_eq_true_eq] at h
      simp [List.mem_cons, mem_dedupNat]

theorem nodup_dedupNat : ∀ (L : List Nat), (dedupNat L).Nodup
  | [] => List.nodup_nil
  | y :: ys => by
    simp only [dedupNat]
    split
    · exact nodup_dedupNat ys
    · rename_i h
      simp only [List.contains_eq_mem, decide_eq_true_eq] at h
      exact List.nodup_cons.mpr ⟨h, nodup_dedupNat ys⟩

def del2List (n x : Nat) : List Nat :=
  dedupNat ((allPairs2 n).map fun p => del2Nat x p.1 p.2)

theorem del2List_nodup (n x : Nat) : (del2List n x).Nodup :=
  nodup_dedupNat _

theorem del2List_lt {n x d : Nat} (hx : x < 2 ^ n) (hd : d ∈ del2List n x) :
    d < 2 ^ (n - 2) := by
  rw [del2List, mem_dedupNat, List.mem_map] at hd
  rcases hd with ⟨⟨i, j⟩, hp, rfl⟩
  rcases mem_allPairs2.mp hp with ⟨hi, hj⟩
  exact del2Nat_lt hx hi hj

theorem mem_del2List_inDelBall {n x d : Nat} (hn : 2 ≤ n) (hd : d ∈ del2List n x) :
    InDelBall 2 (natToWord n x) (natToWord (n - 2) d) := by
  rw [del2List, mem_dedupNat, List.mem_map] at hd
  rcases hd with ⟨⟨i, j⟩, hp, rfl⟩
  rcases mem_allPairs2.mp hp with ⟨hi, hj⟩
  refine ⟨del2Nat_isSubseq hi hj, ?_⟩
  rw [natToWord_length, natToWord_length]
  omega

private def invWordD2 (g : Nat) (d : List Bool) : List Bool :=
  if g = 0 then d
  else if g = 1 then d.map Bool.not
  else if g = 2 then d.reverse
  else d.reverse.map Bool.not

theorem isValidDeletionCode_map_applyD2 {n s g : Nat} (hs : s ≤ n) {C : List Nat}
    (hC : IsValidDeletionCode n s C) : IsValidDeletionCode n s (C.map (applyD2 n g)) := by
  have hword_map : ∀ {k x : Nat} {d : List Bool}, x < 2 ^ k →
      (invWordD2 g d).length = d.length ∧
      (InDelBall s (natToWord k (applyD2 k g x)) d →
        InDelBall s (natToWord k x) (invWordD2 g d)) := by
    intro k x d hx
    by_cases h0 : g = 0
    · simp [applyD2, invWordD2, h0]
    · by_cases h1 : g = 1
      · simp [applyD2, invWordD2, h1]
        intro ⟨hsub, hlen⟩
        refine ⟨?_, ?_⟩
        · have hcomp := isSubseq_map Bool.not hsub
          rw [natToWord_bitComp k x hx, List.map_map] at hcomp
          have hnot : (Bool.not ∘ Bool.not) = id := by funext b; cases b <;> rfl
          simpa [hnot] using hcomp
        · rw [natToWord_length] at hlen ⊢; simp [hlen]
      · by_cases h2 : g = 2
        · simp [applyD2, invWordD2, h2]
          intro ⟨hsub, hlen⟩
          refine ⟨?_, ?_⟩
          · have hrev := isSubseq_reverse hsub
            rw [natToWord_bitRev k x, List.reverse_reverse] at hrev
            exact hrev
          · rw [natToWord_length] at hlen ⊢; simp [hlen]
        · simp [applyD2, invWordD2, h0, h1, h2]
          intro ⟨hsub, hlen⟩
          refine ⟨?_, ?_⟩
          · have hcomp := isSubseq_map Bool.not hsub
            rw [natToWord_bitComp k (bitRev k x) (bitRev_lt k x), List.map_map] at hcomp
            have hnot : (Bool.not ∘ Bool.not) = id := by funext b; cases b <;> rfl
            rw [hnot, List.map_id, natToWord_bitRev k x] at hcomp
            have hrev := isSubseq_reverse hcomp
            rw [List.reverse_reverse] at hrev
            simpa [List.map_reverse] using hrev
          · rw [natToWord_length] at hlen ⊢; simp [hlen]
  refine ⟨?_, ?_⟩
  · intro y hy
    rw [List.mem_map] at hy
    rcases hy with ⟨x, hx, rfl⟩
    exact applyD2_lt (hC.1 x hx)
  · intro i j hi hj hij
    rw [List.length_map] at hi hj
    have hCi_lt : C[i] < 2 ^ n := hC.1 C[i] (List.getElem_mem hi)
    have hCj_lt : C[j] < 2 ^ n := hC.1 C[j] (List.getElem_mem hj)
    have hpair := hC.2 i j hi hj hij
    rw [List.getElem_map, List.getElem_map]
    have hdisj : ∀ d : List Bool, ¬ (InDelBall s (natToWord n (applyD2 n g C[i])) d ∧
                                     InDelBall s (natToWord n (applyD2 n g C[j])) d) := by
      intro d ⟨hd1, hd2⟩
      exact hpair.2.1 _ ⟨(hword_map hCi_lt).2 hd1, (hword_map hCj_lt).2 hd2⟩
    refine ⟨?_, hdisj, ?_⟩
    · intro heq
      apply hpair.1
      have h1 := congrArg (applyD2 n g) heq
      rw [applyD2_involutive hCi_lt, applyD2_involutive hCj_lt] at h1
      exact h1
    · rw [← disjoint_delBall_iff_no_common_subseq hs (by rw [natToWord_length]) (by rw [natToWord_length])]
      exact hdisj

/-- Pairwise deletion-ball conflict check on strictly ascending word list `Q ⊂ [0, 2^n)`. -/
def clqEdge2 (n u v : Nat) : Bool :=
  (del2List n u).any fun d => (del2List n v).contains d

def checkClq2 (n : Nat) : List Nat → Bool
  | [] => true
  | u :: us => (u < 2 ^ n) && (us.all fun v => u < v && clqEdge2 n u v) && checkClq2 n us

theorem checkClq2_sound {n : Nat} (hn : 2 ≤ n) :
    ∀ {Q : List Nat}, checkClq2 n Q = true →
      (∀ u ∈ Q, u < 2 ^ n) ∧ Q.Nodup ∧
      (∀ u ∈ Q, ∀ v ∈ Q, u ≠ v →
        ∃ d : List Bool, InDelBall 2 (natToWord n u) d ∧ InDelBall 2 (natToWord n v) d)
  | [], _ => ⟨by simp, List.nodup_nil, by simp⟩
  | u :: us, h => by
    simp only [checkClq2, Bool.and_eq_true, decide_eq_true_eq] at h
    rcases h with ⟨⟨hu_lt, hall⟩, hrest⟩
    have ih := checkClq2_sound hn hrest
    rw [List.all_eq_true] at hall
    have hu_not_mem : u ∉ us := by
      intro hum
      have := hall u hum
      simp only [Bool.and_eq_true, decide_eq_true_eq] at this
      omega
    refine ⟨?_, List.nodup_cons.mpr ⟨hu_not_mem, ih.2.1⟩, ?_⟩
    · intro z hz
      rcases List.mem_cons.mp hz with rfl | hzs
      · exact hu_lt
      · exact ih.1 z hzs
    · intro a ha b hb hab
      rcases List.mem_cons.mp ha with rfl | has <;> rcases List.mem_cons.mp hb with rfl | hbs
      · exact False.elim (hab rfl)
      · have hvb := hall b hbs
        simp only [Bool.and_eq_true, decide_eq_true_eq, clqEdge2, List.any_eq_true, List.contains_eq_mem] at hvb
        rcases hvb.2 with ⟨d, hd1, hd2⟩
        exact ⟨natToWord (n - 2) d, mem_del2List_inDelBall hn hd1, mem_del2List_inDelBall hn hd2⟩
      · have hva := hall a has
        simp only [Bool.and_eq_true, decide_eq_true_eq, clqEdge2, List.any_eq_true, List.contains_eq_mem] at hva
        rcases hva.2 with ⟨d, hd1, hd2⟩
        exact ⟨natToWord (n - 2) d, mem_del2List_inDelBall hn hd2, mem_del2List_inDelBall hn hd1⟩
      · exact ih.2.2 a has b hbs hab

theorem filter_len_le_one_of_pairwise {α : Type} (p : α → Bool) :
    ∀ (L : List α), (∀ i j (hi : i < L.length) (hj : j < L.length), i ≠ j → p L[i] = true → p L[j] = true → False) →
      (L.filter (fun x => p x)).length ≤ 1
  | [], _ => by simp
  | x :: xs, h => by
    have hxs : ∀ i j (hi : i < xs.length) (hj : j < xs.length), i ≠ j → p xs[i] = true → p xs[j] = true → False := by
      intro i j hi hj hij hpi hpj
      exact h (i + 1) (j + 1) (Nat.succ_lt_succ hi) (Nat.succ_lt_succ hj) (by omega) hpi hpj
    have ih := filter_len_le_one_of_pairwise p xs hxs
    by_cases hpx : p x = true
    · have hnone : ∀ y ∈ xs, p y = false := by
        intro y hy
        rcases List.mem_iff_getElem.mp hy with ⟨j, hj, rfl⟩
        cases hpy : p xs[j]
        · rfl
        · exact False.elim (h 0 (j + 1) (Nat.zero_lt_succ _) (Nat.succ_lt_succ hj) (by omega) hpx hpy)
      have hfil : xs.filter (fun z => p z) = [] := by
        rw [List.filter_eq_nil_iff]
        intro y hy
        simp [hnone y hy]
      rw [List.filter_cons]
      simp [hpx, hfil]
    · simp [hpx, ih]

private theorem sum_ite_eq_mul_filter {α : Type} (p : α → Bool) (w : Nat) :
    ∀ (L : List α), (L.map fun x => if p x = true then w else 0).sum = w * (L.filter p).length
  | [] => by simp
  | x :: xs => by
    by_cases hx : p x = true
    · simp [hx, sum_ite_eq_mul_filter p w xs, Nat.mul_add, Nat.add_comm]
    · have hfx : p x = false := Bool.eq_false_iff.mpr hx
      simp [hfx, sum_ite_eq_mul_filter p w xs]

theorem clq_sum_le_weight {n w : Nat} (hn : 2 ≤ n) {Q C : List Nat}
    (hQ : checkClq2 n Q = true) (hC : IsValidDeletionCode n 2 C) :
    (C.map fun x => if Q.contains x then w else 0).sum ≤ w := by
  have hQ_snd := checkClq2_sound hn hQ
  have h_le1 : (C.filter fun x => Q.contains x).length ≤ 1 := by
    apply filter_len_le_one_of_pairwise (fun x => Q.contains x) C
    intro i j hi hj hij hpi hpj
    simp only [List.contains_eq_mem, decide_eq_true_eq] at hpi hpj
    have hpair := hC.2 i j hi hj hij
    rcases hQ_snd.2.2 C[i] hpi C[j] hpj hpair.1 with ⟨d, hd1, hd2⟩
    exact hpair.2.1 d ⟨hd1, hd2⟩
  rw [sum_ite_eq_mul_filter (fun x => Q.contains x) w C]
  calc w * (C.filter fun x => Q.contains x).length ≤ w * 1 := Nat.mul_le_mul_left w h_le1
    _ = w := Nat.mul_one w

/-- General Rank-1 Chvátal-Gomory inequality on a strictly ascending list `S` of `(n-2)`-descendants with divisor `q ≥ 1`. -/
def checkCg2 (nd : Nat) (q rhs : Nat) (S : List Nat) : Bool :=
  (0 < q) && isStrictAsc S && S.all (· < nd) && decide (S.length / q ≤ rhs)

private theorem sum_map_add {α : Type} (f g : α → Nat) :
    ∀ (L : List α), (L.map fun x => f x + g x).sum = (L.map f).sum + (L.map g).sum
  | [] => by simp
  | x :: xs => by
    simp only [List.map_cons, List.sum_cons, sum_map_add f g xs]
    omega

private theorem sum_map_zero {α : Type} :
    ∀ (L : List α), (L.map (fun _ => 0)).sum = 0
  | [] => rfl
  | _ :: xs => by simp [sum_map_zero xs]

private theorem sum_map_swap {α β : Type} (f : α → β → Nat) :
    ∀ (A : List α) (B : List β),
      (A.map fun a => (B.map fun b => f a b).sum).sum =
      (B.map fun b => (A.map fun a => f a b).sum).sum
  | [], B => by
    simp only [List.map_nil, List.sum_nil]
    exact (sum_map_zero B).symm
  | a :: as, B => by
    simp only [List.map_cons, List.sum_cons, sum_map_swap f as B, ← sum_map_add]

private theorem sum_map_mul_right {α : Type} (f : α → Nat) (c : Nat) :
    ∀ (L : List α), (L.map fun x => f x * c).sum = (L.map f).sum * c
  | [] => by simp
  | x :: xs => by
    simp only [List.map_cons, List.sum_cons, sum_map_mul_right f c xs, Nat.add_mul]

private theorem sum_map_le_of_le {α : Type} (f g : α → Nat) (hfg : ∀ x, f x ≤ g x) :
    ∀ (L : List α), (L.map f).sum ≤ (L.map g).sum
  | [] => by simp
  | x :: xs => by
    simp only [List.map_cons, List.sum_cons]
    have h1 := hfg x
    have h2 := sum_map_le_of_le f g hfg xs
    omega

theorem cg_sum_le_weight {n w q rhs : Nat} (hn : 2 ≤ n) {S C : List Nat}
    (hcg : checkCg2 (2 ^ (n - 2)) q rhs S = true) (hC : IsValidDeletionCode n 2 C) :
    (C.map fun x => ((S.filter fun d => (del2List n x).contains d).length / q) * w).sum ≤ rhs * w := by
  simp only [checkCg2, Bool.and_eq_true, decide_eq_true_eq, List.all_eq_true] at hcg
  rcases hcg with ⟨⟨⟨hq, hS_asc⟩, hS_lt⟩, hdiv_le⟩
  have hS_nd : S.Nodup := strictAsc_nodup hS_asc
  let f : Nat → List Nat := fun x => S.filter fun d => (del2List n x).contains d
  have hfnodup : ∀ x ∈ C, (f x).Nodup := fun _ _ => hS_nd.filter _
  have hfdisj : ∀ i j (hi : i < C.length) (hj : j < C.length), i ≠ j →
      ∀ d, ¬ (d ∈ f C[i] ∧ d ∈ f C[j]) := by
    intro i j hi hj hij d ⟨h1, h2⟩
    simp only [f, List.mem_filter, List.contains_eq_mem, decide_eq_true_eq] at h1 h2
    have hpair := hC.2 i j hi hj hij
    exact hpair.2.1 (natToWord (n - 2) d) ⟨mem_del2List_inDelBall hn h1.2, mem_del2List_inDelBall hn h2.2⟩
  have hflat := flatMap_nodup_and_sum (fun _ => 1) f C hfnodup hfdisj
  have hsub : ∀ d ∈ C.flatMap f, d ∈ S := by
    intro d hd
    rw [List.mem_flatMap] at hd
    rcases hd with ⟨x, _, hdx⟩
    exact (List.mem_filter.mp hdx).1
  have hsum_le_S := sum_map_le_of_nodup_subset (fun _ => 1) (C.flatMap f) S hflat.1 hsub
  have h_len1 : ∀ (L : List Nat), (L.map (fun _ => 1)).sum = L.length := by
    intro L; induction L with
    | nil => simp
    | cons _ _ ih => simp [ih, Nat.add_comm]
  have h_sum_fx : (C.map fun x => (f x).length).sum ≤ S.length := by
    have h1 : (C.map fun x => (List.map (fun _ => 1) (f x)).sum).sum = (C.map fun x => (f x).length).sum := by
      congr 1; apply List.map_congr_left; intro x _; exact h_len1 (f x)
    rw [← h1, ← hflat.2, h_len1, h_len1] at *
    omega
  have hq_mul : (C.map fun x => ((f x).length / q)).sum * q ≤ S.length := by
    rw [← sum_map_mul_right (fun x => (f x).length / q) q C]
    have hterm : (C.map fun x => ((f x).length / q) * q).sum ≤ (C.map fun x => (f x).length).sum :=
      sum_map_le_of_le (fun x => ((f x).length / q) * q) (fun x => (f x).length)
        (fun x => Nat.div_mul_le_self (f x).length q) C
    omega
  have hdiv_sum : (C.map fun x => ((f x).length / q)).sum ≤ rhs := by
    have : (C.map fun x => ((f x).length / q)).sum ≤ S.length / q :=
      (Nat.le_div_iff_mul_le hq).mpr hq_mul
    omega
  rw [sum_map_mul_right (fun x => (f x).length / q) w C]
  exact Nat.mul_le_mul_right w hdiv_sum

def wordCov1 (n : Nat) (y : Nat → Nat)
    (clqs : List (Nat × List Nat))
    (cgs : List (Nat × Nat × Nat × List Nat)) (x : Nat) : Nat :=
  let ds := del2List n x
  (ds.map y).sum +
  (clqs.map fun c => if c.2.contains x then c.1 else 0).sum +
  (cgs.map fun cg => ((cg.2.2.2.filter fun d => ds.contains d).length / cg.2.1) * cg.1).sum

theorem sum_wordCov1_le {n : Nat} (hn : 2 ≤ n) (y : Nat → Nat)
    (clqs : List (Nat × List Nat)) (hclqs : clqs.all fun c => checkClq2 n c.2)
    (cgs : List (Nat × Nat × Nat × List Nat)) (hcgs : cgs.all fun cg => checkCg2 (2 ^ (n - 2)) cg.2.1 cg.2.2.1 cg.2.2.2)
    {C : List Nat} (hC : IsValidDeletionCode n 2 C) :
    (C.map (wordCov1 n y clqs cgs)).sum ≤
      ((List.range (2 ^ (n - 2))).map y).sum +
      (clqs.map (·.1)).sum +
      (cgs.map fun cg => cg.2.2.1 * cg.1).sum := by
  have hsplit : (C.map (wordCov1 n y clqs cgs)).sum =
      (C.map fun x => ((del2List n x).map y).sum).sum +
      (C.map fun x => (clqs.map fun c => if c.2.contains x then c.1 else 0).sum).sum +
      (C.map fun x => (cgs.map fun cg => ((cg.2.2.2.filter fun d => (del2List n x).contains d).length / cg.2.1) * cg.1).sum).sum := by
    unfold wordCov1
    rw [sum_map_add (fun x => ((del2List n x).map y).sum + (clqs.map fun c => if c.2.contains x then c.1 else 0).sum)
          (fun x => (cgs.map fun cg => ((cg.2.2.2.filter fun d => (del2List n x).contains d).length / cg.2.1) * cg.1).sum)]
    congr 1
    exact sum_map_add (fun x => ((del2List n x).map y).sum)
      (fun x => (clqs.map fun c => if c.2.contains x then c.1 else 0).sum) C
  rw [hsplit]
  have h1 : (C.map fun x => ((del2List n x).map y).sum).sum ≤ ((List.range (2 ^ (n - 2))).map y).sum := by
    have hdisj : ∀ i j (hi : i < C.length) (hj : j < C.length), i ≠ j →
        ∀ d, ¬ (d ∈ del2List n C[i] ∧ d ∈ del2List n C[j]) := by
      intro i j hi hj hij d ⟨hd1, hd2⟩
      exact (hC.2 i j hi hj hij).2.1 (natToWord (n - 2) d)
        ⟨mem_del2List_inDelBall hn hd1, mem_del2List_inDelBall hn hd2⟩
    have hflat := flatMap_nodup_and_sum y (del2List n) C (fun x _ => del2List_nodup n x) hdisj
    have hsub : ∀ d ∈ C.flatMap (del2List n), d ∈ List.range (2 ^ (n - 2)) := by
      intro d hd
      rw [List.mem_flatMap] at hd
      rcases hd with ⟨x, hx, hdx⟩
      rw [List.mem_range]
      exact del2List_lt (hC.1 x hx) hdx
    rw [← hflat.2]
    exact sum_map_le_of_nodup_subset y (C.flatMap (del2List n)) (List.range (2 ^ (n - 2))) hflat.1 hsub
  have h2 : (C.map fun x => (clqs.map fun c => if c.2.contains x then c.1 else 0).sum).sum ≤ (clqs.map (·.1)).sum := by
    rw [sum_map_swap (fun x c => if c.2.contains x then c.1 else 0) C clqs]
    rw [List.all_eq_true] at hclqs
    clear h1 hsplit hcgs
    induction clqs with
    | nil => simp
    | cons c cs ih =>
      simp only [List.map_cons, List.sum_cons]
      have hc := @clq_sum_le_weight n c.1 hn c.2 C (hclqs c (by simp)) hC
      have hcs := ih (fun z hz => hclqs z (by simp [hz]))
      omega
  have h3 : (C.map fun x => (cgs.map fun cg => ((cg.2.2.2.filter fun d => (del2List n x).contains d).length / cg.2.1) * cg.1).sum).sum ≤
      (cgs.map fun cg => cg.2.2.1 * cg.1).sum := by
    rw [sum_map_swap (fun x cg => ((cg.2.2.2.filter fun d => (del2List n x).contains d).length / cg.2.1) * cg.1) C cgs]
    rw [List.all_eq_true] at hcgs
    clear h1 h2 hsplit hclqs
    induction cgs with
    | nil => simp
    | cons cg cgs' ih =>
      simp only [List.map_cons, List.sum_cons]
      have hcg := @cg_sum_le_weight n cg.1 cg.2.1 cg.2.2.1 hn cg.2.2.2 C (hcgs cg (by simp)) hC
      have hcgs' := ih (fun z hz => hcgs z (by simp [hz]))
      omega
  omega

def wordCovD2 (n : Nat) (y : Nat → Nat)
    (clqs : List (Nat × List Nat))
    (cgs : List (Nat × Nat × Nat × List Nat)) (x : Nat) : Nat :=
  wordCov1 n y clqs cgs (applyD2 n 0 x) +
  wordCov1 n y clqs cgs (applyD2 n 1 x) +
  wordCov1 n y clqs cgs (applyD2 n 2 x) +
  wordCov1 n y clqs cgs (applyD2 n 3 x)

def checkWordsD2 (n Lmin : Nat) (y : Nat → Nat)
    (clqs : List (Nat × List Nat))
    (cgs : List (Nat × Nat × Nat × List Nat)) : Bool :=
  (List.range (2 ^ n)).all fun x => decide (Lmin ≤ wordCovD2 n y clqs cgs x)

theorem weak_duality_cut2_d2 {n Lmin M : Nat} (hn : 2 ≤ n)
    (y : Nat → Nat)
    (clqs : List (Nat × List Nat)) (hclqs : clqs.all fun c => checkClq2 n c.2 = true)
    (cgs : List (Nat × Nat × Nat × List Nat))
    (hcgs : cgs.all fun cg => checkCg2 (2 ^ (n - 2)) cg.2.1 cg.2.2.1 cg.2.2.2 = true)
    (hwords : checkWordsD2 n Lmin y clqs cgs = true)
    (hbound : 4 * (((List.range (2 ^ (n - 2))).map y).sum + (clqs.map (·.1)).sum +
        (cgs.map fun cg => cg.2.2.1 * cg.1).sum) < Lmin * (M + 1))
    {C : List Nat} (hC : IsValidDeletionCode n 2 C) :
    C.length ≤ M := by
  have hcov : ∀ x ∈ C, Lmin ≤ wordCovD2 n y clqs cgs x := by
    intro x hx
    rw [checkWordsD2, List.all_eq_true] at hwords
    simpa [decide_eq_true_eq] using hwords x (List.mem_range.mpr (hC.1 x hx))
  have h_lhs : Lmin * C.length ≤ (C.map (wordCovD2 n y clqs cgs)).sum :=
    mul_length_le_sum Lmin (wordCovD2 n y clqs cgs) C hcov
  have h_d2_sum : (C.map (wordCovD2 n y clqs cgs)).sum =
      ((C.map (applyD2 n 0)).map (wordCov1 n y clqs cgs)).sum +
      ((C.map (applyD2 n 1)).map (wordCov1 n y clqs cgs)).sum +
      ((C.map (applyD2 n 2)).map (wordCov1 n y clqs cgs)).sum +
      ((C.map (applyD2 n 3)).map (wordCov1 n y clqs cgs)).sum := by
    unfold wordCovD2
    simp only [List.map_map]
    rw [sum_map_add (fun x => wordCov1 n y clqs cgs (applyD2 n 0 x) + wordCov1 n y clqs cgs (applyD2 n 1 x) + wordCov1 n y clqs cgs (applyD2 n 2 x))
          (fun x => wordCov1 n y clqs cgs (applyD2 n 3 x)) C]
    congr 1
    rw [sum_map_add (fun x => wordCov1 n y clqs cgs (applyD2 n 0 x) + wordCov1 n y clqs cgs (applyD2 n 1 x))
          (fun x => wordCov1 n y clqs cgs (applyD2 n 2 x)) C]
    congr 1
    exact sum_map_add (fun x => wordCov1 n y clqs cgs (applyD2 n 0 x))
      (fun x => wordCov1 n y clqs cgs (applyD2 n 1 x)) C
  have hg0 := sum_wordCov1_le hn y clqs hclqs cgs hcgs (isValidDeletionCode_map_applyD2 hn (g := 0) hC)
  have hg1 := sum_wordCov1_le hn y clqs hclqs cgs hcgs (isValidDeletionCode_map_applyD2 hn (g := 1) hC)
  have hg2 := sum_wordCov1_le hn y clqs hclqs cgs hcgs (isValidDeletionCode_map_applyD2 hn (g := 2) hC)
  have hg3 := sum_wordCov1_le hn y clqs hclqs cgs hcgs (isValidDeletionCode_map_applyD2 hn (g := 3) hC)
  have h_tot : Lmin * C.length < Lmin * (M + 1) := by omega
  rcases Nat.lt_or_ge C.length (M + 1) with hlt | hge
  · omega
  · have : Lmin * (M + 1) ≤ Lmin * C.length := Nat.mul_le_mul_left Lmin hge
    omega

/-! ## 3. Fast Witnessed Certificates (`BTree` Ball Table + Explicit `(i₁,j₁,i₂,j₂)` Clique Edge Witnesses) -/

inductive BTree (α : Type) where
  | leaf (v : α) : BTree α
  | node (l r : BTree α) : BTree α

def BTree.get {α : Type} : BTree α → Nat → Nat → α
  | .leaf v, _, _ => v
  | .node l r, k + 1, x => if x % 2 == 0 then l.get k (x / 2) else r.get k (x / 2)
  | .node l _, 0, _ => l.get 0 0

def ballWitOk (n x : Nat) (L : List (Nat × Nat × Nat)) : Bool :=
  isStrictAsc (L.map Prod.fst) &&
  L.all fun (d, i, j) => (i < j) && (j < n) && (del2Nat x i j == d)

theorem ballWitOk_sound {n x : Nat} (hn : 2 ≤ n) (hx : x < 2 ^ n) {L : List (Nat × Nat × Nat)}
    (hb : ballWitOk n x L = true) :
    (L.map Prod.fst).Nodup ∧
    (∀ d ∈ L.map Prod.fst, d < 2 ^ (n - 2)) ∧
    (∀ d ∈ L.map Prod.fst, InDelBall 2 (natToWord n x) (natToWord (n - 2) d)) := by
  simp only [ballWitOk, Bool.and_eq_true, List.all_eq_true, decide_eq_true_eq, beq_iff_eq] at hb
  rcases hb with ⟨hasc, hall⟩
  refine ⟨strictAsc_nodup hasc, ?_, ?_⟩
  · intro d hd
    rw [List.mem_map] at hd
    rcases hd with ⟨⟨d', i, j⟩, hm, rfl⟩
    rcases hall (d', i, j) hm with ⟨⟨hij, hjn⟩, heq⟩
    rw [← heq]
    exact del2Nat_lt hx hij hjn
  · intro d hd
    rw [List.mem_map] at hd
    rcases hd with ⟨⟨d', i, j⟩, hm, rfl⟩
    rcases hall (d', i, j) hm with ⟨⟨hij, hjn⟩, heq⟩
    rw [← heq]
    refine ⟨del2Nat_isSubseq hij hjn, ?_⟩
    rw [natToWord_length, natToWord_length]
    omega

def checkEdgeRow (n u : Nat) : List Nat → List (Nat × Nat × Nat × Nat) → Bool
  | [], [] => true
  | v :: vs, (i1, j1, i2, j2) :: rs =>
    (u < v) && (i1 < j1) && (j1 < n) && (i2 < j2) && (j2 < n) &&
      (del2Nat u i1 j1 == del2Nat v i2 j2) && checkEdgeRow n u vs rs
  | _, _ => false

theorem checkEdgeRow_sound {n u : Nat} (hn : 2 ≤ n) :
    ∀ {vs : List Nat} {rs : List (Nat × Nat × Nat × Nat)},
      checkEdgeRow n u vs rs = true →
      ∀ v ∈ vs, u < v ∧
        ∃ d : List Bool, InDelBall 2 (natToWord n u) d ∧ InDelBall 2 (natToWord n v) d
  | [], [], _ => by simp
  | [], _ :: _, h => by simp [checkEdgeRow] at h
  | _ :: _, [], h => by simp [checkEdgeRow] at h
  | v :: vs, (i1, j1, i2, j2) :: rs, h => by
    simp only [checkEdgeRow, Bool.and_eq_true, decide_eq_true_eq, beq_iff_eq] at h
    rcases h with ⟨⟨⟨⟨⟨⟨huv, hi1⟩, hj1⟩, hi2⟩, hj2⟩, heq⟩, hrest⟩
    intro z hz
    rcases List.mem_cons.mp hz with rfl | hzs
    · refine ⟨huv, natToWord (n - 2) (del2Nat u i1 j1), ?_, ?_⟩
      · refine ⟨del2Nat_isSubseq hi1 hj1, ?_⟩
        rw [natToWord_length, natToWord_length]; omega
      · rw [heq]
        refine ⟨del2Nat_isSubseq hi2 hj2, ?_⟩
        rw [natToWord_length, natToWord_length]; omega
    · exact checkEdgeRow_sound hn hrest z hzs

def checkClqWit (n : Nat) : List Nat → List (List (Nat × Nat × Nat × Nat)) → Bool
  | [], [] => true
  | u :: us, ws :: wss => (u < 2 ^ n) && checkEdgeRow n u us ws && checkClqWit n us wss
  | _, _ => false

theorem checkClqWit_sound {n : Nat} (hn : 2 ≤ n) :
    ∀ {Q : List Nat} {W : List (List (Nat × Nat × Nat × Nat))},
      checkClqWit n Q W = true →
      (∀ u ∈ Q, u < 2 ^ n) ∧
      (∀ u ∈ Q, ∀ v ∈ Q, u ≠ v →
        ∃ d : List Bool, InDelBall 2 (natToWord n u) d ∧ InDelBall 2 (natToWord n v) d)
  | [], [], _ => ⟨by simp, by simp⟩
  | [], _ :: _, h => by simp [checkClqWit] at h
  | _ :: _, [], h => by simp [checkClqWit] at h
  | u :: us, ws :: wss, h => by
    simp only [checkClqWit, Bool.and_eq_true, decide_eq_true_eq] at h
    rcases h with ⟨⟨hu, hrow⟩, hrest⟩
    have ih := checkClqWit_sound hn hrest
    refine ⟨?_, ?_⟩
    · intro z hz
      rcases List.mem_cons.mp hz with rfl | hzs
      · exact hu
      · exact ih.1 z hzs
    · intro a ha b hb hab
      rcases List.mem_cons.mp ha with rfl | has <;> rcases List.mem_cons.mp hb with rfl | hbs
      · exact False.elim (hab rfl)
      · exact (checkEdgeRow_sound hn hrow b hbs).2
      · rcases (checkEdgeRow_sound hn hrow a has).2 with ⟨d, hd1, hd2⟩
        exact ⟨d, hd2, hd1⟩
      · exact ih.2 a has b hbs hab

theorem clqWit_sum_le_weight {n w : Nat} (hn : 2 ≤ n) {Q : List Nat}
    {W : List (List (Nat × Nat × Nat × Nat))} {C : List Nat}
    (hQ : checkClqWit n Q W = true) (hC : IsValidDeletionCode n 2 C) :
    (C.map fun x => if Q.contains x then w else 0).sum ≤ w := by
  have hQ_snd := checkClqWit_sound hn hQ
  have h_le1 : (C.filter fun x => Q.contains x).length ≤ 1 := by
    apply filter_len_le_one_of_pairwise (fun x => Q.contains x) C
    intro i j hi hj hij hpi hpj
    simp only [List.contains_eq_mem, decide_eq_true_eq] at hpi hpj
    have hpair := hC.2 i j hi hj hij
    rcases hQ_snd.2 C[i] hpi C[j] hpj hpair.1 with ⟨d, hd1, hd2⟩
    exact hpair.2.1 d ⟨hd1, hd2⟩
  rw [sum_ite_eq_mul_filter (fun x => Q.contains x) w C]
  calc w * (C.filter fun x => Q.contains x).length ≤ w * 1 := Nat.mul_le_mul_left w h_le1
    _ = w := Nat.mul_one w

theorem cgWit_sum_le_weight {n w q rhs : Nat} (hn : 2 ≤ n)
    (bTree : BTree (List (Nat × Nat × Nat)))
    (hb : ∀ x < 2 ^ n, ballWitOk n x (bTree.get n x) = true)
    {S C : List Nat} (hcg : checkCg2 (2 ^ (n - 2)) q rhs S = true)
    (hC : IsValidDeletionCode n 2 C) :
    (C.map fun x => ((S.filter fun d => ((bTree.get n x).map Prod.fst).contains d).length / q) * w).sum ≤ rhs * w := by
  simp only [checkCg2, Bool.and_eq_true, decide_eq_true_eq, List.all_eq_true] at hcg
  rcases hcg with ⟨⟨⟨hq, hS_asc⟩, hS_lt⟩, hdiv_le⟩
  have hS_nd : S.Nodup := strictAsc_nodup hS_asc
  let f : Nat → List Nat := fun x => S.filter fun d => ((bTree.get n x).map Prod.fst).contains d
  have hfnodup : ∀ x ∈ C, (f x).Nodup := fun _ _ => hS_nd.filter _
  have hfdisj : ∀ i j (hi : i < C.length) (hj : j < C.length), i ≠ j →
      ∀ d, ¬ (d ∈ f C[i] ∧ d ∈ f C[j]) := by
    intro i j hi hj hij d ⟨h1, h2⟩
    simp only [f, List.mem_filter, List.contains_eq_mem, decide_eq_true_eq] at h1 h2
    have hi_snd := ballWitOk_sound hn (hC.1 C[i] (List.getElem_mem hi)) (hb C[i] (hC.1 C[i] (List.getElem_mem hi)))
    have hj_snd := ballWitOk_sound hn (hC.1 C[j] (List.getElem_mem hj)) (hb C[j] (hC.1 C[j] (List.getElem_mem hj)))
    exact (hC.2 i j hi hj hij).2.1 (natToWord (n - 2) d) ⟨hi_snd.2.2 d h1.2, hj_snd.2.2 d h2.2⟩
  have hflat := flatMap_nodup_and_sum (fun _ => 1) f C hfnodup hfdisj
  have hsub : ∀ d ∈ C.flatMap f, d ∈ S := by
    intro d hd; rw [List.mem_flatMap] at hd; rcases hd with ⟨x, _, hdx⟩; exact (List.mem_filter.mp hdx).1
  have hsum_le_S := sum_map_le_of_nodup_subset (fun _ => 1) (C.flatMap f) S hflat.1 hsub
  have h_len1 : ∀ (L : List Nat), (L.map (fun _ => 1)).sum = L.length := by
    intro L; induction L with
    | nil => simp
    | cons _ _ ih => simp [ih, Nat.add_comm]
  have h_sum_fx : (C.map fun x => (f x).length).sum ≤ S.length := by
    have h1 : (C.map fun x => (List.map (fun _ => 1) (f x)).sum).sum = (C.map fun x => (f x).length).sum := by
      congr 1; apply List.map_congr_left; intro x _; exact h_len1 (f x)
    rw [← h1, ← hflat.2, h_len1, h_len1] at *
    omega
  have hq_mul : (C.map fun x => ((f x).length / q)).sum * q ≤ S.length := by
    rw [← sum_map_mul_right (fun x => (f x).length / q) q C]
    have hterm : (C.map fun x => ((f x).length / q) * q).sum ≤ (C.map fun x => (f x).length).sum :=
      sum_map_le_of_le (fun x => ((f x).length / q) * q) (fun x => (f x).length)
        (fun x => Nat.div_mul_le_self (f x).length q) C
    omega
  have hdiv_sum : (C.map fun x => ((f x).length / q)).sum ≤ rhs := by
    have : (C.map fun x => ((f x).length / q)).sum ≤ S.length / q :=
      (Nat.le_div_iff_mul_le hq).mpr hq_mul
    omega
  rw [sum_map_mul_right (fun x => (f x).length / q) w C]
  exact Nat.mul_le_mul_right w hdiv_sum

def wordCovWit1 (n : Nat) (bTree : BTree (List (Nat × Nat × Nat))) (y : Nat → Nat)
    (clqs : List (Nat × List Nat × List (List (Nat × Nat × Nat × Nat))))
    (cgs : List (Nat × Nat × Nat × List Nat)) (x : Nat) : Nat :=
  let ds := (bTree.get n x).map Prod.fst
  (ds.map y).sum +
  (clqs.map fun c => if c.2.1.contains x then c.1 else 0).sum +
  (cgs.map fun cg => ((cg.2.2.2.filter fun d => ds.contains d).length / cg.2.1) * cg.1).sum

theorem sum_wordCovWit1_le {n : Nat} (hn : 2 ≤ n)
    (bTree : BTree (List (Nat × Nat × Nat)))
    (hb : ∀ x < 2 ^ n, ballWitOk n x (bTree.get n x) = true)
    (y : Nat → Nat)
    (clqs : List (Nat × List Nat × List (List (Nat × Nat × Nat × Nat))))
    (hclqs : clqs.all fun c => checkClqWit n c.2.1 c.2.2)
    (cgs : List (Nat × Nat × Nat × List Nat))
    (hcgs : cgs.all fun cg => checkCg2 (2 ^ (n - 2)) cg.2.1 cg.2.2.1 cg.2.2.2)
    {C : List Nat} (hC : IsValidDeletionCode n 2 C) :
    (C.map (wordCovWit1 n bTree y clqs cgs)).sum ≤
      ((List.range (2 ^ (n - 2))).map y).sum +
      (clqs.map (·.1)).sum +
      (cgs.map fun cg => cg.2.2.1 * cg.1).sum := by
  have hsplit : (C.map (wordCovWit1 n bTree y clqs cgs)).sum =
      (C.map fun x => (((bTree.get n x).map Prod.fst).map y).sum).sum +
      (C.map fun x => (clqs.map fun c => if c.2.1.contains x then c.1 else 0).sum).sum +
      (C.map fun x => (cgs.map fun cg => ((cg.2.2.2.filter fun d => ((bTree.get n x).map Prod.fst).contains d).length / cg.2.1) * cg.1).sum).sum := by
    unfold wordCovWit1
    rw [sum_map_add (fun x => (((bTree.get n x).map Prod.fst).map y).sum + (clqs.map fun c => if c.2.1.contains x then c.1 else 0).sum)
          (fun x => (cgs.map fun cg => ((cg.2.2.2.filter fun d => ((bTree.get n x).map Prod.fst).contains d).length / cg.2.1) * cg.1).sum)]
    congr 1
    exact sum_map_add (fun x => (((bTree.get n x).map Prod.fst).map y).sum)
      (fun x => (clqs.map fun c => if c.2.1.contains x then c.1 else 0).sum) C
  rw [hsplit]
  have h1 : (C.map fun x => (((bTree.get n x).map Prod.fst).map y).sum).sum ≤ ((List.range (2 ^ (n - 2))).map y).sum := by
    let f : Nat → List Nat := fun x => (bTree.get n x).map Prod.fst
    have hfnd : ∀ x ∈ C, (f x).Nodup := fun x hx =>
      (ballWitOk_sound hn (hC.1 x hx) (hb x (hC.1 x hx))).1
    have hdisj : ∀ i j (hi : i < C.length) (hj : j < C.length), i ≠ j →
        ∀ d, ¬ (d ∈ f C[i] ∧ d ∈ f C[j]) := by
      intro i j hi hj hij d ⟨hd1, hd2⟩
      have hi_s := ballWitOk_sound hn (hC.1 C[i] (List.getElem_mem hi)) (hb C[i] (hC.1 C[i] (List.getElem_mem hi)))
      have hj_s := ballWitOk_sound hn (hC.1 C[j] (List.getElem_mem hj)) (hb C[j] (hC.1 C[j] (List.getElem_mem hj)))
      exact (hC.2 i j hi hj hij).2.1 (natToWord (n - 2) d) ⟨hi_s.2.2 d hd1, hj_s.2.2 d hd2⟩
    have hflat := flatMap_nodup_and_sum y f C hfnd hdisj
    have hsub : ∀ d ∈ C.flatMap f, d ∈ List.range (2 ^ (n - 2)) := by
      intro d hd; rw [List.mem_flatMap] at hd; rcases hd with ⟨x, hx, hdx⟩; rw [List.mem_range]
      exact (ballWitOk_sound hn (hC.1 x hx) (hb x (hC.1 x hx))).2.1 d hdx
    rw [← hflat.2]
    exact sum_map_le_of_nodup_subset y (C.flatMap f) (List.range (2 ^ (n - 2))) hflat.1 hsub
  have h2 : (C.map fun x => (clqs.map fun c => if c.2.1.contains x then c.1 else 0).sum).sum ≤ (clqs.map (·.1)).sum := by
    rw [sum_map_swap (fun x c => if c.2.1.contains x then c.1 else 0) C clqs]
    rw [List.all_eq_true] at hclqs
    clear h1 hsplit hcgs
    induction clqs with
    | nil => simp
    | cons c cs ih =>
      simp only [List.map_cons, List.sum_cons]
      have hc := @clqWit_sum_le_weight n c.1 hn c.2.1 c.2.2 C (hclqs c (by simp)) hC
      have hcs := ih (fun z hz => hclqs z (by simp [hz]))
      omega
  have h3 : (C.map fun x => (cgs.map fun cg => ((cg.2.2.2.filter fun d => ((bTree.get n x).map Prod.fst).contains d).length / cg.2.1) * cg.1).sum).sum ≤
      (cgs.map fun cg => cg.2.2.1 * cg.1).sum := by
    rw [sum_map_swap (fun x cg => ((cg.2.2.2.filter fun d => ((bTree.get n x).map Prod.fst).contains d).length / cg.2.1) * cg.1) C cgs]
    rw [List.all_eq_true] at hcgs
    clear h1 h2 hsplit hclqs
    induction cgs with
    | nil => simp
    | cons cg cgs' ih =>
      simp only [List.map_cons, List.sum_cons]
      have hcg := @cgWit_sum_le_weight n cg.1 cg.2.1 cg.2.2.1 hn bTree hb cg.2.2.2 C (hcgs cg (by simp)) hC
      have hcgs' := ih (fun z hz => hcgs z (by simp [hz]))
      omega
  omega

def wordCovWitD2 (n : Nat) (bTree : BTree (List (Nat × Nat × Nat))) (y : Nat → Nat)
    (clqs : List (Nat × List Nat × List (List (Nat × Nat × Nat × Nat))))
    (cgs : List (Nat × Nat × Nat × List Nat)) (x : Nat) : Nat :=
  wordCovWit1 n bTree y clqs cgs (applyD2 n 0 x) +
  wordCovWit1 n bTree y clqs cgs (applyD2 n 1 x) +
  wordCovWit1 n bTree y clqs cgs (applyD2 n 2 x) +
  wordCovWit1 n bTree y clqs cgs (applyD2 n 3 x)

theorem weak_duality_cut2_fast {n Lmin M : Nat} (hn : 2 ≤ n)
    (bTree : BTree (List (Nat × Nat × Nat)))
    (hb : (List.range (2 ^ n)).all (fun x => ballWitOk n x (bTree.get n x)) = true)
    (y : Nat → Nat)
    (clqs : List (Nat × List Nat × List (List (Nat × Nat × Nat × Nat))))
    (hclqs : clqs.all fun c => checkClqWit n c.2.1 c.2.2 = true)
    (cgs : List (Nat × Nat × Nat × List Nat))
    (hcgs : cgs.all fun cg => checkCg2 (2 ^ (n - 2)) cg.2.1 cg.2.2.1 cg.2.2.2 = true)
    (hwords : ∀ x < 2 ^ n, Lmin ≤ wordCovWitD2 n bTree y clqs cgs x)
    (hbound : 4 * (((List.range (2 ^ (n - 2))).map y).sum + (clqs.map (·.1)).sum +
        (cgs.map fun cg => cg.2.2.1 * cg.1).sum) < Lmin * (M + 1))
    {C : List Nat} (hC : IsValidDeletionCode n 2 C) :
    C.length ≤ M := by
  have hb' : ∀ x < 2 ^ n, ballWitOk n x (bTree.get n x) = true := by
    intro x hx
    rw [List.all_eq_true] at hb
    exact hb x (List.mem_range.mpr hx)
  have hcov : ∀ x ∈ C, Lmin ≤ wordCovWitD2 n bTree y clqs cgs x :=
    fun x hx => hwords x (hC.1 x hx)
  have h_lhs : Lmin * C.length ≤ (C.map (wordCovWitD2 n bTree y clqs cgs)).sum :=
    mul_length_le_sum Lmin (wordCovWitD2 n bTree y clqs cgs) C hcov
  have h_d2_sum : (C.map (wordCovWitD2 n bTree y clqs cgs)).sum =
      ((C.map (applyD2 n 0)).map (wordCovWit1 n bTree y clqs cgs)).sum +
      ((C.map (applyD2 n 1)).map (wordCovWit1 n bTree y clqs cgs)).sum +
      ((C.map (applyD2 n 2)).map (wordCovWit1 n bTree y clqs cgs)).sum +
      ((C.map (applyD2 n 3)).map (wordCovWit1 n bTree y clqs cgs)).sum := by
    unfold wordCovWitD2
    simp only [List.map_map]
    rw [sum_map_add (fun x => wordCovWit1 n bTree y clqs cgs (applyD2 n 0 x) + wordCovWit1 n bTree y clqs cgs (applyD2 n 1 x) + wordCovWit1 n bTree y clqs cgs (applyD2 n 2 x))
          (fun x => wordCovWit1 n bTree y clqs cgs (applyD2 n 3 x)) C]
    congr 1
    rw [sum_map_add (fun x => wordCovWit1 n bTree y clqs cgs (applyD2 n 0 x) + wordCovWit1 n bTree y clqs cgs (applyD2 n 1 x))
          (fun x => wordCovWit1 n bTree y clqs cgs (applyD2 n 2 x)) C]
    congr 1
    exact sum_map_add (fun x => wordCovWit1 n bTree y clqs cgs (applyD2 n 0 x))
      (fun x => wordCovWit1 n bTree y clqs cgs (applyD2 n 1 x)) C
  have hg0 := sum_wordCovWit1_le hn bTree hb' y clqs hclqs cgs hcgs (isValidDeletionCode_map_applyD2 hn (g := 0) hC)
  have hg1 := sum_wordCovWit1_le hn bTree hb' y clqs hclqs cgs hcgs (isValidDeletionCode_map_applyD2 hn (g := 1) hC)
  have hg2 := sum_wordCovWit1_le hn bTree hb' y clqs hclqs cgs hcgs (isValidDeletionCode_map_applyD2 hn (g := 2) hC)
  have hg3 := sum_wordCovWit1_le hn bTree hb' y clqs hclqs cgs hcgs (isValidDeletionCode_map_applyD2 hn (g := 3) hC)
  have h_tot : Lmin * C.length < Lmin * (M + 1) := by omega
  rcases Nat.lt_or_ge C.length (M + 1) with hlt | hge
  · omega
  · have : Lmin * (M + 1) ≤ Lmin * C.length := Nat.mul_le_mul_left Lmin hge
    omega

end DeletionCode.CutDual

