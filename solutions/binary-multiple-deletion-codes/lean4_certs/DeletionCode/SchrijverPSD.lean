/-
  DeletionCode/SchrijverPSD.lean — Universal Zero-Mathlib Pure-Kernel Schrijver θ' PSD
  Sum-of-Squares Upper-Bound Engine for ALL Binary `s`-Deletion-Correcting Codes (`s ≤ n`).

  Certifies `M_s(n) ≤ M` beyond flat LP and clique/CG-1 hierarchies via an exact integer
  `D_2 = <c, r>`-equivariant Gram factorization `Q = L^T L` with:
    1. Diagonal bound:   `∀ x < 2^n, ‖v(x)‖^2 ≤ T - S`
    2. Non-edge bound:   `∀ x ≠ y` with `D_s(x) ∩ D_s(y) = ∅`, `⟨v(x), v(y)⟩ ≤ -S`
    3. Exact arithmetic: `S > 0` and `T < (M + 1) * S`
  Then for ANY valid `(n, s)` deletion code `C`:
    `0 ≤ ‖∑_{x ∈ C} v(x)‖^2 = ∑_{x ∈ C} ‖v(x)‖^2 + 2 ∑_{i < j} ⟨v(C[i]), v(C[j])⟩`
    `  ≤ |C| (T - S) - |C| (|C| - 1) S = |C| (T - |C| S)`,
  forcing `|C| ≤ M` with ZERO square roots, ZERO floats, ZERO Mathlib, ZERO `sorryAx`,
  and ZERO `native_decide` / `Lean.ofReduceBool`.

  Uses a 4-point Walsh-Hadamard transform over the 4 irreps of `D_2 = Z_2 × Z_2` so every
  unordered orbit pair `(i, j)` (`i ≤ j`) computes its inner product ONCE and checks all
  4 group shifts `h ∈ {0, 1, 2, 3}` via additions/subtractions + `canMatchNat`.
-/
import DeletionCode.Basic
import DeletionCode.DualLP
import DeletionCode.CutDual
import DeletionCode.RecDual

set_option maxRecDepth 65536

namespace DeletionCode.SchrijverPSD

open DeletionCode
open DeletionCode.DualLP
open DeletionCode.CutDual
open DeletionCode.RecDual

/-! ## 1. `D_2 = Z_2 × Z_2` Group Law, Canonical Representatives & 4 Irrep Characters -/

/-- Group multiplication in `D_2 = {0=id, 1=c, 2=r, 3=cr}` (bitwise XOR on `0..3`). -/
def xorD2 (a b : Nat) : Nat :=
  match a, b with
  | 0, b => b
  | a, 0 => a
  | 1, 1 => 0
  | 1, 2 => 3
  | 1, 3 => 2
  | 2, 1 => 3
  | 2, 2 => 0
  | 2, 3 => 1
  | 3, 1 => 2
  | 3, 2 => 1
  | 3, 3 => 0
  | _, _ => 0

theorem xorD2_lt {a b : Nat} (ha : a < 4) (hb : b < 4) : xorD2 a b < 4 := by
  match a, b with
  | 0, 0 | 0, 1 | 0, 2 | 0, 3
  | 1, 0 | 1, 1 | 1, 2 | 1, 3
  | 2, 0 | 2, 1 | 2, 2 | 2, 3
  | 3, 0 | 3, 1 | 3, 2 | 3, 3 => decide
  | a + 4, _ => omega
  | _, b + 4 => omega

theorem xorD2_comm {a b : Nat} (ha : a < 4) (hb : b < 4) : xorD2 a b = xorD2 b a := by
  match a, b with
  | 0, 0 | 0, 1 | 0, 2 | 0, 3
  | 1, 0 | 1, 1 | 1, 2 | 1, 3
  | 2, 0 | 2, 1 | 2, 2 | 2, 3
  | 3, 0 | 3, 1 | 3, 2 | 3, 3 => rfl
  | a + 4, _ => omega
  | _, b + 4 => omega

theorem xorD2_self {a : Nat} (ha : a < 4) : xorD2 a a = 0 := by
  match a with
  | 0 | 1 | 2 | 3 => rfl
  | a + 4 => omega

private theorem bitRev_lt_of_apply {n x : Nat} (hx : x < 2 ^ n) : bitRev n x < 2 ^ n := by
  simpa [applyD2] using applyD2_lt (n := n) (g := 2) hx

private theorem bitRev_involutive_pub {n x : Nat} (hx : x < 2 ^ n) : bitRev n (bitRev n x) = x := by
  simpa [applyD2] using applyD2_involutive (n := n) (g := 2) hx

private theorem bitRev_bitComp_comm {n y : Nat} (hy : y < 2 ^ n) :
    bitRev n (bitComp n y) = bitComp n (bitRev n y) := by
  have hx : bitRev n y < 2 ^ n := bitRev_lt_of_apply hy
  have h3 : bitComp n (bitRev n (bitComp n (bitRev n (bitRev n y)))) = bitRev n y := by
    simpa [applyD2] using applyD2_involutive (n := n) (g := 3) hx
  rw [bitRev_involutive_pub hy] at h3
  have hlt : bitRev n (bitComp n y) < 2 ^ n := bitRev_lt_of_apply (by simpa [applyD2] using applyD2_lt (n := n) (g := 1) hy)
  have hc := congrArg (bitComp n) h3
  rw [bitComp_involutive hlt] at hc
  exact hc

/-- Group homomorphism law for `applyD2`: `g1 (g2 x) = (g1 ⊕ g2) x` for `g1, g2 < 4`. -/
theorem applyD2_comp {n g1 g2 x : Nat} (hg1 : g1 < 4) (hg2 : g2 < 4) (hx : x < 2 ^ n) :
    applyD2 n g1 (applyD2 n g2 x) = applyD2 n (xorD2 g1 g2) x := by
  have hc_lt : bitComp n x < 2 ^ n := by simpa [applyD2] using applyD2_lt (n := n) (g := 1) hx
  have hr_lt : bitRev n x < 2 ^ n := bitRev_lt_of_apply hx
  match g1, g2 with
  | 0, 0 | 0, 1 | 0, 2 | 0, 3 => simp [applyD2, xorD2]
  | 1, 0 | 2, 0 | 3, 0 => simp [applyD2, xorD2]
  | 1, 1 => simp [applyD2, xorD2, bitComp_involutive hx]
  | 1, 2 => simp [applyD2, xorD2]
  | 1, 3 => simp [applyD2, xorD2, bitComp_involutive hr_lt]
  | 2, 1 => simp [applyD2, xorD2, bitRev_bitComp_comm hx]
  | 2, 2 => simp [applyD2, xorD2, bitRev_involutive_pub hx]
  | 2, 3 =>
    simp only [applyD2, xorD2, show (2 : Nat) ≠ 0 by omega, show (2 : Nat) ≠ 1 by omega,
      show (3 : Nat) ≠ 0 by omega, show (3 : Nat) ≠ 1 by omega, show (3 : Nat) ≠ 2 by omega,
      show (1 : Nat) ≠ 0 by omega, ↓reduceIte]
    rw [bitRev_bitComp_comm hr_lt, bitRev_involutive_pub hx]
  | 3, 1 =>
    simp only [applyD2, xorD2, show (3 : Nat) ≠ 0 by omega, show (3 : Nat) ≠ 1 by omega,
      show (3 : Nat) ≠ 2 by omega, show (1 : Nat) ≠ 0 by omega, show (2 : Nat) ≠ 0 by omega,
      show (2 : Nat) ≠ 1 by omega, ↓reduceIte]
    rw [bitRev_bitComp_comm hx, bitComp_involutive hr_lt]
  | 3, 2 =>
    simp only [applyD2, xorD2, show (3 : Nat) ≠ 0 by omega, show (3 : Nat) ≠ 1 by omega,
      show (3 : Nat) ≠ 2 by omega, show (2 : Nat) ≠ 0 by omega, show (2 : Nat) ≠ 1 by omega,
      show (1 : Nat) ≠ 0 by omega, ↓reduceIte]
    rw [bitRev_involutive_pub hx]
  | 3, 3 =>
    simpa [applyD2, xorD2] using applyD2_involutive (n := n) (g := 3) hx
  | g1 + 4, _ => omega
  | _, g2 + 4 => omega

/-- Canonical `D_2` orbit element `(g, r)` where `r = applyD2 n g x` is minimal in the orbit of `x`. -/
def canonD2 (n x : Nat) : Nat × Nat :=
  let x0 := x
  let x1 := bitComp n x
  let x2 := bitRev n x
  let x3 := bitComp n (bitRev n x)
  let p01 := if Nat.ble x0 x1 then (0, x0) else (1, x1)
  let p23 := if Nat.ble x2 x3 then (2, x2) else (3, x3)
  if Nat.ble p01.2 p23.2 then p01 else p23

theorem canonD2_spec (n x : Nat) (hx : x < 2 ^ n) :
    (canonD2 n x).1 < 4 ∧
    (canonD2 n x).2 = applyD2 n (canonD2 n x).1 x ∧
    (canonD2 n x).2 < 2 ^ n ∧
    applyD2 n (canonD2 n x).1 (canonD2 n x).2 = x := by
  unfold canonD2
  dsimp only
  split <;> split <;> split
  all_goals
    simp only [applyD2]
    refine ⟨by omega, by simp, ?_, ?_⟩
    · first | exact hx | exact applyD2_lt (n := n) (g := 1) hx | exact applyD2_lt (n := n) (g := 2) hx | exact applyD2_lt (n := n) (g := 3) hx
    · first | rfl | exact applyD2_involutive (n := n) (g := 1) hx | exact applyD2_involutive (n := n) (g := 2) hx | exact applyD2_involutive (n := n) (g := 3) hx

/-- The 4 1D characters `χ_c : D_2 → {+1, -1}` (`0: ++, 1: -+, 2: +-, 3: --`). -/
def chi (c g : Nat) : Int :=
  match c, g with
  | 0, _ => 1
  | 1, 0 => 1
  | 1, 1 => -1
  | 1, 2 => 1
  | 1, 3 => -1
  | 2, 0 => 1
  | 2, 1 => 1
  | 2, 2 => -1
  | 2, 3 => -1
  | 3, 0 => 1
  | 3, 1 => -1
  | 3, 2 => -1
  | 3, 3 => 1
  | _, _ => 1

theorem chi_mul {c g1 g2 : Nat} (hc : c < 4) (hg1 : g1 < 4) (hg2 : g2 < 4) :
    chi c g1 * chi c g2 = chi c (xorD2 g1 g2) := by
  match c, g1, g2 with
  | 0, 0, 0 | 0, 0, 1 | 0, 0, 2 | 0, 0, 3
  | 0, 1, 0 | 0, 1, 1 | 0, 1, 2 | 0, 1, 3
  | 0, 2, 0 | 0, 2, 1 | 0, 2, 2 | 0, 2, 3
  | 0, 3, 0 | 0, 3, 1 | 0, 3, 2 | 0, 3, 3
  | 1, 0, 0 | 1, 0, 1 | 1, 0, 2 | 1, 0, 3
  | 1, 1, 0 | 1, 1, 1 | 1, 1, 2 | 1, 1, 3
  | 1, 2, 0 | 1, 2, 1 | 1, 2, 2 | 1, 2, 3
  | 1, 3, 0 | 1, 3, 1 | 1, 3, 2 | 1, 3, 3
  | 2, 0, 0 | 2, 0, 1 | 2, 0, 2 | 2, 0, 3
  | 2, 1, 0 | 2, 1, 1 | 2, 1, 2 | 2, 1, 3
  | 2, 2, 0 | 2, 2, 1 | 2, 2, 2 | 2, 2, 3
  | 2, 3, 0 | 2, 3, 1 | 2, 3, 2 | 2, 3, 3
  | 3, 0, 0 | 3, 0, 1 | 3, 0, 2 | 3, 0, 3
  | 3, 1, 0 | 3, 1, 1 | 3, 1, 2 | 3, 1, 3
  | 3, 2, 0 | 3, 2, 1 | 3, 2, 2 | 3, 2, 3
  | 3, 3, 0 | 3, 3, 1 | 3, 3, 2 | 3, 3, 3 => rfl
  | c + 4, _, _ => omega
  | _, g1 + 4, _ => omega
  | _, _, g2 + 4 => omega

/-! ## 2. Exact Integer Inner Products and Sum-of-Squares Algebra (Zero Mathlib) -/

/-- Tail-recursive integer dot product for fast pure-kernel evaluation. -/
def dotIntGo : List Int → List Int → Int → Int
  | [], _, acc => acc
  | _, [], acc => acc
  | a :: as, b :: bs, acc => dotIntGo as bs (acc + a * b)

/-- Spec integer dot product. -/
def dotInt : List Int → List Int → Int
  | [], _ => 0
  | _, [] => 0
  | a :: as, b :: bs => a * b + dotInt as bs

theorem dotIntGo_eq : ∀ (u v : List Int) (acc : Int), dotIntGo u v acc = acc + dotInt u v
  | [], _, acc => by simp [dotIntGo, dotInt]
  | _ :: _, [], acc => by simp [dotIntGo, dotInt]
  | a :: as, b :: bs, acc => by
    simp only [dotIntGo, dotInt, dotIntGo_eq as bs (acc + a * b)]
    omega

theorem dotInt_comm : ∀ (u v : List Int), dotInt u v = dotInt v u
  | [], [] => rfl
  | [], _ :: _ => rfl
  | _ :: _, [] => rfl
  | a :: as, b :: bs => by
    simp only [dotInt, dotInt_comm as bs, Int.mul_comm a b]

private theorem int_mul_self_nonneg (a : Int) : 0 ≤ a * a := by
  cases a with
  | ofNat m => exact Int.natCast_nonneg (m * m)
  | negSucc m => exact Int.natCast_nonneg ((m + 1) * (m + 1))

theorem dotInt_self_nonneg : ∀ (u : List Int), 0 ≤ dotInt u u
  | [] => by simp [dotInt]
  | a :: as => by
    simp only [dotInt]
    have h1 : 0 ≤ a * a := int_mul_self_nonneg a
    have h2 : 0 ≤ dotInt as as := dotInt_self_nonneg as
    omega

theorem dotInt_append : ∀ {u1 u2 v1 v2 : List Int},
    u1.length = v1.length →
    dotInt (u1 ++ u2) (v1 ++ v2) = dotInt u1 v1 + dotInt u2 v2
  | [], u2, [], v2, _ => by simp [dotInt]
  | a :: as, u2, b :: bs, v2, hlen => by
    simp only [List.cons_append, dotInt]
    have htail : as.length = bs.length := by simpa using hlen
    rw [dotInt_append htail]
    omega
  | [], _, _ :: _, _, h => by simp at h
  | _ :: _, _, [], _, h => by simp at h

def scaleVec (s : Int) (v : List Int) : List Int :=
  v.map (s * ·)

theorem scaleVec_length (s : Int) (v : List Int) : (scaleVec s v).length = v.length :=
  List.length_map ..

theorem dotInt_scale (s1 s2 : Int) : ∀ (u v : List Int),
    dotInt (scaleVec s1 u) (scaleVec s2 v) = (s1 * s2) * dotInt u v
  | [], [] => by simp [scaleVec, dotInt]
  | [], _ :: _ => by simp [scaleVec, dotInt]
  | _ :: _, [] => by simp [scaleVec, dotInt]
  | a :: as, b :: bs => by
    simp only [scaleVec, List.map_cons, dotInt]
    change (s1 * a) * (s2 * b) + dotInt (scaleVec s1 as) (scaleVec s2 bs) =
      (s1 * s2) * (a * b + dotInt as bs)
    rw [dotInt_scale s1 s2 as bs, Int.mul_add]
    have hterm : (s1 * a) * (s2 * b) = (s1 * s2) * (a * b) := by
      rw [Int.mul_assoc s1 a (s2 * b), ← Int.mul_assoc a s2 b, Int.mul_comm a s2,
          Int.mul_assoc s2 a b, ← Int.mul_assoc s1 s2 (a * b)]
    rw [hterm]

def vecAdd : List Int → List Int → List Int
  | [], _ => []
  | _, [] => []
  | a :: as, b :: bs => (a + b) :: vecAdd as bs

theorem vecAdd_length : ∀ {u v : List Int}, u.length = v.length → (vecAdd u v).length = u.length
  | [], [], _ => rfl
  | _ :: as, _ :: bs, h => by
    simp only [vecAdd, List.length_cons]
    exact congrArg (· + 1) (vecAdd_length (by simpa using h))
  | [], _ :: _, h => by simp at h
  | _ :: _, [], h => by simp at h

theorem dotInt_vecAdd_left : ∀ {u v w : List Int},
    u.length = v.length → v.length = w.length →
    dotInt (vecAdd u v) w = dotInt u w + dotInt v w
  | [], [], [], _, _ => by simp [vecAdd, dotInt]
  | a :: as, b :: bs, c :: cs, h1, h2 => by
    simp only [vecAdd, dotInt]
    rw [dotInt_vecAdd_left (by simpa using h1) (by simpa using h2), Int.add_mul]
    omega
  | [], _ :: _, _, h, _ => by simp at h
  | _ :: _, [], _, h, _ => by simp at h
  | _, [], _ :: _, _, h => by simp at h
  | _, _ :: _, [], _, h => by simp at h

theorem dotInt_vecAdd_right {u v w : List Int} (h1 : v.length = w.length) (h2 : u.length = v.length) :
    dotInt u (vecAdd v w) = dotInt u v + dotInt u w := by
  rw [dotInt_comm, dotInt_vecAdd_left h1 (by omega), dotInt_comm v u, dotInt_comm w u]

theorem dotInt_zero_right : ∀ (R : Nat) (u : List Int), dotInt u (List.replicate R 0) = 0
  | 0, [] => rfl
  | 0, _ :: _ => rfl
  | _ + 1, [] => rfl
  | R + 1, a :: as => by
    simp only [List.replicate_succ, dotInt, Int.mul_zero, Int.zero_add]
    exact dotInt_zero_right R as

def vecSum (R : Nat) : List (List Int) → List Int
  | [] => List.replicate R 0
  | v :: vs => vecAdd v (vecSum R vs)

theorem vecSum_length (R : Nat) : ∀ (vs : List (List Int)),
    (∀ v ∈ vs, v.length = R) → (vecSum R vs).length = R
  | [], _ => List.length_replicate ..
  | v :: vs, hall => by
    have hv : v.length = R := hall v (List.mem_cons_self ..)
    have hvs : (vecSum R vs).length = R :=
      vecSum_length R vs (fun w hw => hall w (List.mem_cons_of_mem v hw))
    simp only [vecSum]
    rw [vecAdd_length (by omega), hv]

def dotSumWith (u : List Int) : List (List Int) → Int
  | [] => 0
  | v :: vs => dotInt u v + dotSumWith u vs

theorem dotInt_vecSum_right (R : Nat) (u : List Int) (hu : u.length = R) :
    ∀ (vs : List (List Int)), (∀ v ∈ vs, v.length = R) →
      dotInt u (vecSum R vs) = dotSumWith u vs
  | [], _ => by simp [vecSum, dotSumWith, dotInt_zero_right]
  | v :: vs, hall => by
    have hv : v.length = R := hall v (List.mem_cons_self ..)
    have hvs : (vecSum R vs).length = R :=
      vecSum_length R vs (fun w hw => hall w (List.mem_cons_of_mem v hw))
    simp only [vecSum, dotSumWith]
    rw [dotInt_vecAdd_right (by omega) (by omega),
        dotInt_vecSum_right R u hu vs (fun w hw => hall w (List.mem_cons_of_mem v hw))]

/-- Master Sum-of-Squares Upper Bound on any list of `R`-dimensional integer vectors! -/
theorem sos_gram_bound (R : Nat) (diagMax offMax : Int) :
    ∀ (vs : List (List Int)),
      (∀ v ∈ vs, v.length = R) →
      (∀ v ∈ vs, dotInt v v ≤ diagMax) →
      (∀ i j (hi : i < vs.length) (hj : j < vs.length), i < j → dotInt vs[i] vs[j] ≤ offMax) →
      0 ≤ Int.ofNat vs.length * diagMax + Int.ofNat (vs.length * (vs.length - 1)) * offMax := by
  intro vs hlen hdiag hoff
  have hsq : 0 ≤ dotInt (vecSum R vs) (vecSum R vs) := dotInt_self_nonneg _
  suffices hle : dotInt (vecSum R vs) (vecSum R vs) ≤
      Int.ofNat vs.length * diagMax + Int.ofNat (vs.length * (vs.length - 1)) * offMax by omega
  clear hsq
  induction vs with
  | nil =>
    simp [vecSum, dotInt_zero_right]
  | cons v rest ih =>
    have hv : v.length = R := hlen v (List.mem_cons_self ..)
    have hrest_len : ∀ w ∈ rest, w.length = R := fun w hw => hlen w (List.mem_cons_of_mem v hw)
    have hrest_sum_len : (vecSum R rest).length = R := vecSum_length R rest hrest_len
    have hrest_diag : ∀ w ∈ rest, dotInt w w ≤ diagMax := fun w hw => hdiag w (List.mem_cons_of_mem v hw)
    have hrest_off : ∀ i j (hi : i < rest.length) (hj : j < rest.length), i < j →
        dotInt rest[i] rest[j] ≤ offMax := by
      intro i j hi hj hij
      exact hoff (i + 1) (j + 1) (Nat.succ_lt_succ hi) (Nat.succ_lt_succ hj) (Nat.succ_lt_succ hij)
    have hih := ih hrest_len hrest_diag hrest_off
    have hv_diag : dotInt v v ≤ diagMax := hdiag v (List.mem_cons_self ..)
    have hcross : dotSumWith v rest ≤ Int.ofNat rest.length * offMax := by
      have hall_v : ∀ j (hj : j < rest.length), dotInt v rest[j] ≤ offMax := by
        intro j hj
        exact hoff 0 (j + 1) (Nat.zero_lt_succ _) (Nat.succ_lt_succ hj) (Nat.zero_lt_succ j)
      clear ih hih hlen hdiag hoff hrest_len hrest_sum_len hrest_diag hrest_off hv hv_diag
      induction rest with
      | nil => simp [dotSumWith]
      | cons w ws ihw =>
        simp only [dotSumWith, List.length_cons]
        have hw0 : dotInt v w ≤ offMax := hall_v 0 (Nat.zero_lt_succ _)
        have hws : dotSumWith v ws ≤ Int.ofNat ws.length * offMax :=
          ihw (fun j hj => hall_v (j + 1) (Nat.succ_lt_succ hj))
        have hcast : Int.ofNat (ws.length + 1) * offMax = Int.ofNat ws.length * offMax + offMax := by
          have : Int.ofNat (ws.length + 1) = Int.ofNat ws.length + 1 := rfl
          rw [this, Int.add_mul, Int.one_mul]
        omega
    -- Expand `dotInt (vecAdd v S) (vecAdd v S) = dotInt v v + 2 * dotInt v S + dotInt S S`
    have hadd_len : (vecAdd v (vecSum R rest)).length = R := by
      rw [vecAdd_length (by omega), hv]
    have hexp : dotInt (vecSum R (v :: rest)) (vecSum R (v :: rest)) =
        dotInt v v + 2 * dotSumWith v rest + dotInt (vecSum R rest) (vecSum R rest) := by
      simp only [vecSum]
      rw [dotInt_vecAdd_left (by omega) (by omega),
          dotInt_vecAdd_right (by omega) (by omega),
          dotInt_vecAdd_right (by omega) (by omega),
          dotInt_comm (vecSum R rest) v,
          dotInt_vecSum_right R v hv rest hrest_len]
      omega
    rw [hexp]
    -- Algebraic identity on lengths: `(k+1)*k = k*(k-1) + 2*k`
    have hlen_nat : (rest.length + 1) * rest.length = rest.length * (rest.length - 1) + 2 * rest.length := by
      cases hk : rest.length with
      | zero => simp
      | succ k =>
        simp only [Nat.add_sub_cancel]
        have h1 : (k + 1 + 1) * (k + 1) = (k + 1) * k + 2 * (k + 1) := by
          rw [Nat.add_mul, Nat.mul_add, Nat.mul_one, Nat.one_mul]
          omega
        exact h1
    have hlen_eq : ((v :: rest).length * ((v :: rest).length - 1)) =
        rest.length * (rest.length - 1) + 2 * rest.length := by
      simpa using hlen_nat
    have h1 : Int.ofNat (v :: rest).length * diagMax =
        Int.ofNat rest.length * diagMax + diagMax := by
      have : Int.ofNat (v :: rest).length = Int.ofNat rest.length + 1 := rfl
      rw [this, Int.add_mul, Int.one_mul]
    have h2 : Int.ofNat ((v :: rest).length * ((v :: rest).length - 1)) * offMax =
        Int.ofNat (rest.length * (rest.length - 1)) * offMax + 2 * (Int.ofNat rest.length * offMax) := by
      rw [hlen_eq]
      have hcast : Int.ofNat (rest.length * (rest.length - 1) + 2 * rest.length) =
          Int.ofNat (rest.length * (rest.length - 1)) + 2 * Int.ofNat rest.length := rfl
      rw [hcast, Int.add_mul, Int.mul_assoc]
    rw [h1, h2]
    omega

/-! ## 3. `D_2`-Orbit Entries, Sparse Lookup Tree & Walsh-Hadamard Pair Verification -/

/-- One `D_2`-orbit representative and its 4 irrep coordinate blocks `(++, -+, +-, --)`. -/
structure OrbEntry where
  rep : Nat
  v0 : List Int
  v1 : List Int
  v2 : List Int
  v3 : List Int

/-- Signed full vector `v(x) ∈ Z^{r0+r1+r2+r3}` for orbit entry `e` at group element `g < 4`. -/
def vecOfOrb (g : Nat) (e : OrbEntry) : List Int :=
  scaleVec (chi 0 g) e.v0 ++
  scaleVec (chi 1 g) e.v1 ++
  scaleVec (chi 2 g) e.v2 ++
  scaleVec (chi 3 g) e.v3

theorem vecOfOrb_length {r0 r1 r2 r3 : Nat} {g : Nat} {e : OrbEntry}
    (h0 : e.v0.length = r0) (h1 : e.v1.length = r1) (h2 : e.v2.length = r2) (h3 : e.v3.length = r3) :
    (vecOfOrb g e).length = r0 + r1 + r2 + r3 := by
  simp only [vecOfOrb, List.length_append, scaleVec_length, h0, h1, h2, h3]

/-- Exact 4-irrep Walsh-Hadamard identity: `⟨v(gx, ex), v(gy, ey)⟩` depends ONLY on `h = gx ⊕ gy`! -/
theorem dotInt_vecOfOrb {r0 r1 r2 r3 gx gy : Nat} {ex ey : OrbEntry}
    (hgx : gx < 4) (hgy : gy < 4)
    (hx0 : ex.v0.length = r0) (hx1 : ex.v1.length = r1) (hx2 : ex.v2.length = r2) (_hx3 : ex.v3.length = r3)
    (hy0 : ey.v0.length = r0) (hy1 : ey.v1.length = r1) (hy2 : ey.v2.length = r2) (_hy3 : ey.v3.length = r3) :
    dotInt (vecOfOrb gx ex) (vecOfOrb gy ey) =
      chi 0 (xorD2 gx gy) * dotInt ex.v0 ey.v0 +
      chi 1 (xorD2 gx gy) * dotInt ex.v1 ey.v1 +
      chi 2 (xorD2 gx gy) * dotInt ex.v2 ey.v2 +
      chi 3 (xorD2 gx gy) * dotInt ex.v3 ey.v3 := by
  unfold vecOfOrb
  rw [dotInt_append (by simp [scaleVec_length, hx0, hx1, hx2, hy0, hy1, hy2]),
      dotInt_append (by simp [scaleVec_length, hx0, hx1, hy0, hy1]),
      dotInt_append (by simp [scaleVec_length, hx0, hy0]),
      dotInt_scale, dotInt_scale, dotInt_scale, dotInt_scale,
      chi_mul (by omega) hgx hgy,
      chi_mul (by omega) hgx hgy,
      chi_mul (by omega) hgx hgy,
      chi_mul (by omega) hgx hgy]

/-- Sparse depth-`n` LSB-first tree mapping canonical orbit representative `r ↦ some (idx, e)`. -/
inductive OrbTree where
  | empty : OrbTree
  | leaf (idx : Nat) (e : OrbEntry) : OrbTree
  | node (l r : OrbTree) : OrbTree

def OrbTree.insert (k x idx : Nat) (e : OrbEntry) (t : OrbTree) : OrbTree :=
  match k, t with
  | 0, _ => .leaf idx e
  | k' + 1, .empty =>
    if x % 2 == 0 then .node (OrbTree.insert k' (x / 2) idx e .empty) .empty
    else .node .empty (OrbTree.insert k' (x / 2) idx e .empty)
  | k' + 1, .node l r =>
    if x % 2 == 0 then .node (OrbTree.insert k' (x / 2) idx e l) r
    else .node l (OrbTree.insert k' (x / 2) idx e r)
  | _ + 1, .leaf _ _ => t

def OrbTree.get (k : Nat) (t : OrbTree) (x : Nat) : Option (Nat × OrbEntry) :=
  match t with
  | .empty => none
  | .leaf idx e => match k with | 0 => some (idx, e) | _ => none
  | .node l r => match k with
    | 0 => none
    | k' + 1 => if x % 2 == 0 then l.get k' (x / 2) else r.get k' (x / 2)
termination_by structural t

private theorem OrbTree.get_insert_sound (k x idx : Nat) (e : OrbEntry) (t : OrbTree)
    (P : Nat → Nat → OrbEntry → Prop)
    (ht : ∀ y i a, y < 2 ^ k → t.get k y = some (i, a) → P y i a)
    (hx : x < 2 ^ k) (hnew : P x idx e) :
    ∀ y i a, y < 2 ^ k → (t.insert k x idx e).get k y = some (i, a) → P y i a := by
  induction k generalizing x t P with
  | zero =>
    intro y i a hy hget
    have hx0 : x = 0 := by simpa using hx
    have hy0 : y = 0 := by simpa using hy
    subst hx0; subst hy0
    simp only [OrbTree.insert, OrbTree.get, Option.some.injEq, Prod.mk.injEq] at hget
    rcases hget with ⟨rfl, rfl⟩
    exact hnew
  | succ k' ih =>
    have hpow : 2 ^ (k' + 1) = 2 * 2 ^ k' := by rw [Nat.pow_succ, Nat.mul_comm]
    have hx' : x / 2 < 2 ^ k' := by rw [hpow] at hx; omega
    intro y i a hy hget
    have hy' : y / 2 < 2 ^ k' := by rw [hpow] at hy; omega
    cases t with
    | empty =>
      simp only [OrbTree.insert] at hget
      by_cases hxm : x % 2 = 0
      · simp only [hxm, beq_self_eq_true, ↓reduceIte, OrbTree.get] at hget
        by_cases hym : y % 2 = 0
        · simp only [hym, beq_self_eq_true, ↓reduceIte] at hget
          have hP' : P (2 * (y / 2)) i a :=
            ih (x / 2) .empty (fun z j b => P (2 * z) j b)
              (fun _ _ _ _ h => by simp [OrbTree.get] at h) hx'
              (by have hxx : 2 * (x / 2) = x := by omega
                  rw [hxx]; exact hnew)
              (y / 2) i a hy' hget
          have : 2 * (y / 2) = y := by omega
          rwa [this] at hP'
        · have hy1 : y % 2 = 1 := by omega
          have h10 : (1 == 0) = false := rfl
          simp [hy1, h10] at hget
      · have hx1 : x % 2 = 1 := by omega
        have h10 : (1 == 0) = false := rfl
        simp only [hx1, h10, Bool.false_eq_true, ↓reduceIte, OrbTree.get] at hget
        by_cases hym : y % 2 = 0
        · simp [hym] at hget
        · have hy1 : y % 2 = 1 := by omega
          simp only [hy1, h10, Bool.false_eq_true, ↓reduceIte] at hget
          have hP' : P (2 * (y / 2) + 1) i a :=
            ih (x / 2) .empty (fun z j b => P (2 * z + 1) j b)
              (fun _ _ _ _ h => by simp [OrbTree.get] at h) hx'
              (by have hxx : 2 * (x / 2) + 1 = x := by omega
                  rw [hxx]; exact hnew)
              (y / 2) i a hy' hget
          have : 2 * (y / 2) + 1 = y := by omega
          rwa [this] at hP'
    | leaf _ _ =>
      simp [OrbTree.insert, OrbTree.get] at hget
    | node l r =>
      simp only [OrbTree.insert] at hget
      have htl : ∀ z j b, z < 2 ^ k' → l.get k' z = some (j, b) → P (2 * z) j b := by
        intro z j b hz hgl
        apply ht (2 * z) j b (by rw [hpow]; omega)
        simp [OrbTree.get, hgl]
      have htr : ∀ z j b, z < 2 ^ k' → r.get k' z = some (j, b) → P (2 * z + 1) j b := by
        intro z j b hz hgr
        apply ht (2 * z + 1) j b (by rw [hpow]; omega)
        have hm : (2 * z + 1) % 2 = 1 := by omega
        have hd : (2 * z + 1) / 2 = z := by omega
        have h10 : (1 == 0) = false := rfl
        simp [OrbTree.get, hm, hd, h10, hgr]
      by_cases hxm : x % 2 = 0
      · simp only [hxm, beq_self_eq_true, ↓reduceIte, OrbTree.get] at hget
        by_cases hym : y % 2 = 0
        · simp only [hym, beq_self_eq_true, ↓reduceIte] at hget
          have hP' : P (2 * (y / 2)) i a :=
            ih (x / 2) l (fun z j b => P (2 * z) j b) htl hx'
              (by have hxx : 2 * (x / 2) = x := by omega
                  rw [hxx]; exact hnew)
              (y / 2) i a hy' hget
          have : 2 * (y / 2) = y := by omega
          rwa [this] at hP'
        · have hy1 : y % 2 = 1 := by omega
          have h10 : (1 == 0) = false := rfl
          simp only [hy1, h10, Bool.false_eq_true, ↓reduceIte] at hget
          have hP' := htr (y / 2) i a hy' hget
          have : 2 * (y / 2) + 1 = y := by omega
          rwa [this] at hP'
      · have hx1 : x % 2 = 1 := by omega
        have h10 : (1 == 0) = false := rfl
        simp only [hx1, h10, Bool.false_eq_true, ↓reduceIte, OrbTree.get] at hget
        by_cases hym : y % 2 = 0
        · simp only [hym, beq_self_eq_true, ↓reduceIte] at hget
          have hP' := htl (y / 2) i a hy' hget
          have : 2 * (y / 2) = y := by omega
          rwa [this] at hP'
        · have hy1 : y % 2 = 1 := by omega
          simp only [hy1, h10, Bool.false_eq_true, ↓reduceIte] at hget
          have hP' : P (2 * (y / 2) + 1) i a :=
            ih (x / 2) r (fun z j b => P (2 * z + 1) j b) htr hx'
              (by have hxx : 2 * (x / 2) + 1 = x := by omega
                  rw [hxx]; exact hnew)
              (y / 2) i a hy' hget
          have : 2 * (y / 2) + 1 = y := by omega
          rwa [this] at hP'

def buildOrbTreeGo (n : Nat) : Nat → List OrbEntry → OrbTree → OrbTree
  | _, [], t => t
  | idx, e :: es, t => buildOrbTreeGo n (idx + 1) es (t.insert n e.rep idx e)

def buildOrbTree (n : Nat) (orbs : List OrbEntry) : OrbTree :=
  buildOrbTreeGo n 0 orbs .empty

private theorem buildOrbTreeGo_sound (n : Nat) (full : List OrbEntry)
    (P : Nat → Nat → OrbEntry → Prop)
    (hP : ∀ i (hi : i < full.length), P full[i].rep i full[i]) :
    ∀ (idx : Nat) (es : List OrbEntry) (t : OrbTree),
      (∀ k (hk : k < es.length), idx + k < full.length ∧ full[idx + k]? = some es[k] ∧ es[k].rep < 2 ^ n) →
      (∀ y i a, y < 2 ^ n → t.get n y = some (i, a) → P y i a) →
      ∀ y i a, y < 2 ^ n → (buildOrbTreeGo n idx es t).get n y = some (i, a) → P y i a
  | _, [], t, _, ht, y, i, a, hy, hget => ht y i a hy hget
  | idx, e :: es, t, hsub, ht, y, i, a, hy, hget => by
    have h0 := hsub 0 (Nat.zero_lt_succ _)
    simp only [Nat.add_zero, List.getElem_cons_zero] at h0
    have he_eq : full[idx] = e := by
      have hsome := List.getElem?_eq_getElem h0.1
      rw [hsome, Option.some.injEq] at h0
      exact h0.2.1
    have hnew : P e.rep idx e := by
      have := hP idx h0.1
      rwa [he_eq] at this
    have ht' := OrbTree.get_insert_sound n e.rep idx e t P ht h0.2.2 hnew
    have hsub' : ∀ k (hk : k < es.length), idx + 1 + k < full.length ∧ full[idx + 1 + k]? = some es[k] ∧ es[k].rep < 2 ^ n := by
      intro k hk
      have hk1 := hsub (k + 1) (Nat.succ_lt_succ hk)
      have hidx : idx + (k + 1) = idx + 1 + k := by omega
      rw [hidx] at hk1
      simpa using hk1
    exact buildOrbTreeGo_sound n full P hP (idx + 1) es (t.insert n e.rep idx e) hsub' ht' y i a hy hget

theorem buildOrbTree_sound {n : Nat} {orbs : List OrbEntry}
    (hlt : ∀ e ∈ orbs, e.rep < 2 ^ n)
    {y idx : Nat} {e : OrbEntry} (hy : y < 2 ^ n)
    (hget : (buildOrbTree n orbs).get n y = some (idx, e)) :
    ∃ (hi : idx < orbs.length), orbs[idx] = e ∧ e.rep = y := by
  let P : Nat → Nat → OrbEntry → Prop := fun r i a => ∃ (hi : i < orbs.length), orbs[i] = a ∧ a.rep = r
  have hP : ∀ i (hi : i < orbs.length), P orbs[i].rep i orbs[i] := fun i hi => ⟨hi, rfl, rfl⟩
  have hsub : ∀ k (hk : k < orbs.length), 0 + k < orbs.length ∧ orbs[0 + k]? = some orbs[k] ∧ orbs[k].rep < 2 ^ n := by
    intro k hk
    refine ⟨by omega, by simp [List.getElem?_eq_getElem hk], hlt orbs[k] (List.getElem_mem hk)⟩
  exact buildOrbTreeGo_sound n orbs P hP 0 orbs .empty hsub
    (fun _ _ _ _ h => by simp [OrbTree.get] at h) y idx e hy hget

/-- Depth-`k` binary tree sweep verifying `(t.get n (canonD2 n x).2).isSome = true` for all `x < 2^n`. -/
def checkCoverRec (n : Nat) (t : OrbTree) : Nat → Nat → Bool
  | 0, x => (t.get n (canonD2 n x).2).isSome
  | k + 1, x =>
    match checkCoverRec n t k (2 * x) with
    | true => checkCoverRec n t k (2 * x + 1)
    | false => false

private theorem checkCoverRec_spec (n : Nat) (t : OrbTree) :
    ∀ (k base : Nat), checkCoverRec n t k base = true →
      ∀ rem < 2 ^ k, (t.get n (canonD2 n (base * 2 ^ k + rem)).2).isSome = true
  | 0, base, h, rem, hrem => by
    have h0 : rem = 0 := by simpa using hrem
    subst h0
    simpa [checkCoverRec] using h
  | k + 1, base, h, rem, hrem => by
    simp only [checkCoverRec] at h
    cases hl : checkCoverRec n t k (2 * base)
    · simp [hl] at h
    · simp only [hl] at h
      have hpow : 2 ^ (k + 1) = 2 * 2 ^ k := by rw [Nat.pow_succ, Nat.mul_comm]
      have hlt2 : rem < 2 * 2 ^ k := hpow ▸ hrem
      by_cases hside : rem < 2 ^ k
      · have ih := checkCoverRec_spec n t k (2 * base) hl rem hside
        have heq : 2 * base * 2 ^ k + rem = base * 2 ^ (k + 1) + rem := by
          rw [hpow, Nat.mul_comm 2 base, Nat.mul_assoc]
        rwa [heq] at ih
      · have hrem' : rem - 2 ^ k < 2 ^ k := by omega
        have ih := checkCoverRec_spec n t k (2 * base + 1) h (rem - 2 ^ k) hrem'
        have heq : (2 * base + 1) * 2 ^ k + (rem - 2 ^ k) = base * 2 ^ (k + 1) + rem := by
          rw [Nat.add_mul, Nat.one_mul, hpow, Nat.mul_comm 2 base, Nat.mul_assoc]
          omega
        rwa [heq] at ih

theorem checkCoverRec_all {n : Nat} {t : OrbTree} (h : checkCoverRec n t n 0 = true) :
    ∀ x < 2 ^ n, (t.get n (canonD2 n x).2).isSome = true := by
  intro x hx
  simpa using checkCoverRec_spec n t n 0 h x hx

/-! ## 4. Diagonal Check and Walsh-Hadamard Pair Checkers (Chunk-Splittable!) -/

def checkOrbDiag (n r0 r1 r2 r3 : Nat) (diagMax : Int) (e : OrbEntry) : Bool :=
  decide (e.rep < 2 ^ n) &&
  Nat.beq e.v0.length r0 &&
  Nat.beq e.v1.length r1 &&
  Nat.beq e.v2.length r2 &&
  Nat.beq e.v3.length r3 &&
  decide (dotIntGo e.v0 e.v0 0 + dotIntGo e.v1 e.v1 0 + dotIntGo e.v2 e.v2 0 + dotIntGo e.v3 e.v3 0 ≤ diagMax)

theorem checkOrbDiag_sound {n r0 r1 r2 r3 : Nat} {diagMax : Int} {e : OrbEntry}
    (h : checkOrbDiag n r0 r1 r2 r3 diagMax e = true) :
    e.rep < 2 ^ n ∧ e.v0.length = r0 ∧ e.v1.length = r1 ∧ e.v2.length = r2 ∧ e.v3.length = r3 ∧
    dotInt e.v0 e.v0 + dotInt e.v1 e.v1 + dotInt e.v2 e.v2 + dotInt e.v3 e.v3 ≤ diagMax := by
  simp only [checkOrbDiag, Bool.and_eq_true, decide_eq_true_eq] at h
  rcases h with ⟨⟨⟨⟨⟨hlt, h0⟩, h1⟩, h2⟩, h3⟩, hle⟩
  rw [dotIntGo_eq, dotIntGo_eq, dotIntGo_eq, dotIntGo_eq] at hle
  refine ⟨hlt, Nat.eq_of_beq_eq_true h0, Nat.eq_of_beq_eq_true h1,
          Nat.eq_of_beq_eq_true h2, Nat.eq_of_beq_eq_true h3, by omega⟩

/-- Check one Walsh-Hadamard shift `h ∈ {0,1,2,3}` of orbit pair `(a, b)`. -/
def checkShift (n s : Nat) (negS : Int) (ra rb : Nat) (h : Nat) (d : Int) : Bool :=
  let y := applyD2 n h rb
  if Nat.beq ra y then true
  else if decide (d ≤ negS) then true
  else canMatchNat (n + s) (n - s) s s ra y

theorem checkShift_sound {n s : Nat} (hs : s ≤ n) {negS : Int} {ra rb h : Nat} {d : Int}
    (hc : checkShift n s negS ra rb h d = true)
    (hne : ra ≠ applyD2 n h rb)
    (hdisj : ∀ u : List Bool, ¬ (InDelBall s (natToWord n ra) u ∧ InDelBall s (natToWord n (applyD2 n h rb)) u)) :
    d ≤ negS := by
  unfold checkShift at hc
  dsimp only at hc
  cases hbeq : Nat.beq ra (applyD2 n h rb)
  · simp only [hbeq, Bool.false_eq_true, ↓reduceIte] at hc
    cases hle : decide (d ≤ negS)
    · simp only [hle, Bool.false_eq_true, ↓reduceIte] at hc
      obtain ⟨u, hlen, hu1, hu2⟩ := canMatchNat_sound (n + s) (n - s) s s ra (applyD2 n h rb) hc
      have hns : n - s + s = n := Nat.sub_add_cancel hs
      rw [hns] at hu1 hu2
      exact False.elim (hdisj u ⟨⟨hu1, by rw [natToWord_length, hlen]; omega⟩,
                                 ⟨hu2, by rw [natToWord_length, hlen]; omega⟩⟩)
    · exact decide_eq_true_eq.mp hle
  · exact absurd (Nat.eq_of_beq_eq_true hbeq) hne

/-- Check ALL 4 `D_2` shifts of unordered orbit pair `(a, b)` with ONE length-`r` dot product! -/
def checkOrbPair (n s : Nat) (negS : Int) (a b : OrbEntry) : Bool :=
  let p0 := dotIntGo a.v0 b.v0 0
  let p1 := dotIntGo a.v1 b.v1 0
  let p2 := dotIntGo a.v2 b.v2 0
  let p3 := dotIntGo a.v3 b.v3 0
  match checkShift n s negS a.rep b.rep 0 (p0 + p1 + p2 + p3) with
  | false => false
  | true =>
    match checkShift n s negS a.rep b.rep 1 (p0 - p1 + p2 - p3) with
    | false => false
    | true =>
      match checkShift n s negS a.rep b.rep 2 (p0 + p1 - p2 - p3) with
      | false => false
      | true => checkShift n s negS a.rep b.rep 3 (p0 - p1 - p2 + p3)

theorem checkOrbPair_sound {n s : Nat} (hs : s ≤ n) {negS : Int} {a b : OrbEntry}
    (hp : checkOrbPair n s negS a b = true)
    {h : Nat} (hh : h < 4)
    (hne : a.rep ≠ applyD2 n h b.rep)
    (hdisj : ∀ u : List Bool, ¬ (InDelBall s (natToWord n a.rep) u ∧ InDelBall s (natToWord n (applyD2 n h b.rep)) u)) :
    chi 0 h * dotInt a.v0 b.v0 + chi 1 h * dotInt a.v1 b.v1 +
    chi 2 h * dotInt a.v2 b.v2 + chi 3 h * dotInt a.v3 b.v3 ≤ negS := by
  unfold checkOrbPair at hp
  dsimp only at hp
  rw [dotIntGo_eq, dotIntGo_eq, dotIntGo_eq, dotIntGo_eq] at hp
  simp only [Int.zero_add] at hp
  cases hc0 : checkShift n s negS a.rep b.rep 0 (dotInt a.v0 b.v0 + dotInt a.v1 b.v1 + dotInt a.v2 b.v2 + dotInt a.v3 b.v3)
  · simp [hc0] at hp
  · simp only [hc0] at hp
    cases hc1 : checkShift n s negS a.rep b.rep 1 (dotInt a.v0 b.v0 - dotInt a.v1 b.v1 + dotInt a.v2 b.v2 - dotInt a.v3 b.v3)
    · simp [hc1] at hp
    · simp only [hc1] at hp
      cases hc2 : checkShift n s negS a.rep b.rep 2 (dotInt a.v0 b.v0 + dotInt a.v1 b.v1 - dotInt a.v2 b.v2 - dotInt a.v3 b.v3)
      · simp [hc2] at hp
      · simp only [hc2] at hp
        match h with
        | 0 =>
          have h0 := checkShift_sound hs hc0 hne hdisj
          simp only [chi]; omega
        | 1 =>
          have h1 := checkShift_sound hs hc1 hne hdisj
          simp only [chi]; omega
        | 2 =>
          have h2 := checkShift_sound hs hc2 hne hdisj
          simp only [chi]; omega
        | 3 =>
          have h3 := checkShift_sound hs hp hne hdisj
          simp only [chi]; omega
        | h + 4 => omega

def checkOrbVsList (n s : Nat) (negS : Int) (a : OrbEntry) : List OrbEntry → Bool
  | [] => true
  | b :: bs => match checkOrbPair n s negS a b with
    | true => checkOrbVsList n s negS a bs
    | false => false

private theorem checkOrbVsList_sound {n s : Nat} {negS : Int} {a : OrbEntry} :
    ∀ {bs : List OrbEntry}, checkOrbVsList n s negS a bs = true →
      ∀ b ∈ bs, checkOrbPair n s negS a b = true
  | [], _, _, hm => by cases hm
  | b :: bs, h, z, hz => by
    simp only [checkOrbVsList] at h
    cases hp : checkOrbPair n s negS a b
    · simp [hp] at h
    · simp only [hp] at h
      rcases List.mem_cons.mp hz with rfl | hmem
      · exact hp
      · exact checkOrbVsList_sound h z hmem

/-- Upper-triangular orbit-pair checker covering all `0 ≤ i ≤ j < L.length`. -/
def checkOrbTri (n s : Nat) (negS : Int) : List OrbEntry → Bool
  | [] => true
  | a :: rest => match checkOrbVsList n s negS a (a :: rest) with
    | true => checkOrbTri n s negS rest
    | false => false

/-- Chunk-sized prefix of `checkOrbTri` (processes `k` outer rows so large proofs split into fast chunks!). -/
def checkOrbRows (n s : Nat) (negS : Int) : Nat → List OrbEntry → Bool
  | 0, _ => true
  | _ + 1, [] => true
  | k + 1, a :: rest => match checkOrbVsList n s negS a (a :: rest) with
    | true => checkOrbRows n s negS k rest
    | false => false

theorem checkOrbRows_add (n s : Nat) (negS : Int) :
    ∀ (a b : Nat) (L : List OrbEntry),
      checkOrbRows n s negS a L = true →
      checkOrbRows n s negS b (L.drop a) = true →
      checkOrbRows n s negS (a + b) L = true
  | 0, _, _, _, h2 => by simpa using h2
  | a + 1, b, [], _, _ => by
    have : a + 1 + b = (a + b) + 1 := by omega
    rw [this]; rfl
  | a + 1, b, x :: rest, h1, h2 => by
    have hadd : a + 1 + b = (a + b) + 1 := by omega
    rw [hadd]
    simp only [checkOrbRows] at h1 ⊢
    simp only [List.drop_succ_cons] at h2
    cases hv : checkOrbVsList n s negS x (x :: rest)
    · simp [hv] at h1
    · simp only [hv] at h1 ⊢
      exact checkOrbRows_add n s negS a b rest h1 h2

theorem checkOrbTri_of_rows (n s : Nat) (negS : Int) :
    ∀ (k : Nat) (L : List OrbEntry),
      checkOrbRows n s negS k L = true →
      checkOrbTri n s negS (L.drop k) = true →
      checkOrbTri n s negS L = true
  | 0, _, _, h2 => h2
  | _ + 1, [], _, _ => rfl
  | k + 1, a :: rest, h1, h2 => by
    simp only [checkOrbRows] at h1
    simp only [List.drop_succ_cons] at h2
    simp only [checkOrbTri]
    cases hv : checkOrbVsList n s negS a (a :: rest)
    · simp [hv] at h1
    · simp only [hv] at h1 ⊢
      exact checkOrbTri_of_rows n s negS k rest h1 h2

theorem checkOrbTri_sound {n s : Nat} {negS : Int} :
    ∀ {L : List OrbEntry}, checkOrbTri n s negS L = true →
      ∀ i j (hi : i < L.length) (hj : j < L.length), i ≤ j →
        checkOrbPair n s negS L[i] L[j] = true
  | [], _, i, _, hi, _, _ => absurd hi (Nat.not_lt_zero _)
  | a :: rest, h, i, j, hi, hj, hij => by
    simp only [checkOrbTri] at h
    cases hv : checkOrbVsList n s negS a (a :: rest)
    · simp [hv] at h
    · simp only [hv] at h
      cases i with
      | zero =>
        exact checkOrbVsList_sound hv (a :: rest)[j] (List.getElem_mem hj)
      | succ i' =>
        cases j with
        | zero => omega
        | succ j' =>
          exact checkOrbTri_sound h i' j' (Nat.lt_of_succ_lt_succ hi) (Nat.lt_of_succ_lt_succ hj) (Nat.le_of_succ_le_succ hij)

/-! ## 5. Universal Pure-Kernel Schrijver θ' PSD Weak Duality Master Theorem -/

/--
  Subgraph-Restricted Pure-Kernel Schrijver θ' PSD Upper Bound Theorem for ALL `(n, s)` (`s ≤ n`).
  Same exact Gram proof as `weak_duality_schrijver_psd`, requiring orbit coverage ONLY for words
  actually in `C` — enabling seamless composition with `DeletionCode.PeelReduce` (Onion Peeling)!
-/
theorem weak_duality_schrijver_psd_on {n s r0 r1 r2 r3 S T M : Nat}
    (hs : s ≤ n) (_hS : 0 < S) (hbound : T < (M + 1) * S)
    (orbs : List OrbEntry)
    (hdiag : orbs.all (checkOrbDiag n r0 r1 r2 r3 (Int.ofNat T - Int.ofNat S)) = true)
    (hpairs : checkOrbTri n s (- Int.ofNat S) orbs = true)
    {C : List Nat} (hC : IsValidDeletionCode n s C)
    (hmem : ∀ x ∈ C, ((buildOrbTree n orbs).get n (canonD2 n x).2).isSome = true) :
    C.length ≤ M := by
  have hall_diag : ∀ e ∈ orbs,
      e.rep < 2 ^ n ∧ e.v0.length = r0 ∧ e.v1.length = r1 ∧ e.v2.length = r2 ∧ e.v3.length = r3 ∧
      dotInt e.v0 e.v0 + dotInt e.v1 e.v1 + dotInt e.v2 e.v2 + dotInt e.v3 e.v3 ≤ Int.ofNat T - Int.ofNat S :=
    fun e he => checkOrbDiag_sound (List.all_eq_true.mp hdiag e he)
  have hlt_orbs : ∀ e ∈ orbs, e.rep < 2 ^ n := fun e he => (hall_diag e he).1
  let tree := buildOrbTree n orbs
  let R := r0 + r1 + r2 + r3
  -- Map each codeword `x ∈ C` to its `D_2`-signed vector `vec(x) ∈ Z^R`
  let getEntry (x : Nat) : OrbEntry :=
    match tree.get n (canonD2 n x).2 with
    | some (_, e) => e
    | none => ⟨0, List.replicate r0 0, List.replicate r1 0, List.replicate r2 0, List.replicate r3 0⟩
  let vecOf (x : Nat) : List Int :=
    vecOfOrb (canonD2 n x).1 (getEntry x)
  have hlookup : ∀ x ∈ C,
      ∃ (idx : Nat) (hi : idx < orbs.length),
        getEntry x = orbs[idx] ∧ orbs[idx].rep = (canonD2 n x).2 := by
    intro x hx
    have hcs := canonD2_spec n x (hC.1 x hx)
    have his := hmem x hx
    cases hget : tree.get n (canonD2 n x).2 with
    | none => simp [tree, hget] at his
    | some p =>
      rcases p with ⟨idx, e⟩
      obtain ⟨hi, heq, hrep⟩ := buildOrbTree_sound hlt_orbs hcs.2.2.1 hget
      refine ⟨idx, hi, ?_, by rw [heq, hrep]⟩
      simp [getEntry, hget, heq]
  let vs := C.map vecOf
  have hvs_len : ∀ v ∈ vs, v.length = R := by
    intro v hv
    rw [List.mem_map] at hv
    rcases hv with ⟨x, hx, rfl⟩
    obtain ⟨idx, hi, heq, _⟩ := hlookup x hx
    have hd := hall_diag orbs[idx] (List.getElem_mem hi)
    simp only [vecOf, heq]
    exact vecOfOrb_length hd.2.1 hd.2.2.1 hd.2.2.2.1 hd.2.2.2.2.1
  have hvs_diag : ∀ v ∈ vs, dotInt v v ≤ Int.ofNat T - Int.ofNat S := by
    intro v hv
    rw [List.mem_map] at hv
    rcases hv with ⟨x, hx, rfl⟩
    have hcs := canonD2_spec n x (hC.1 x hx)
    obtain ⟨idx, hi, heq, _⟩ := hlookup x hx
    have hd := hall_diag orbs[idx] (List.getElem_mem hi)
    simp only [vecOf, heq]
    rw [dotInt_vecOfOrb hcs.1 hcs.1 hd.2.1 hd.2.2.1 hd.2.2.2.1 hd.2.2.2.2.1
          hd.2.1 hd.2.2.1 hd.2.2.2.1 hd.2.2.2.2.1, xorD2_self hcs.1]
    simp only [chi, Int.one_mul]
    exact hd.2.2.2.2.2
  have hvs_off : ∀ i j (hi : i < vs.length) (hj : j < vs.length), i < j →
      dotInt vs[i] vs[j] ≤ - Int.ofNat S := by
    intro i j hi hj hij
    have hiC : i < C.length := by simpa [vs] using hi
    have hjC : j < C.length := by simpa [vs] using hj
    have hne_ij : i ≠ j := Nat.ne_of_lt hij
    have hxi : C[i] < 2 ^ n := hC.1 C[i] (List.getElem_mem hiC)
    have hxj : C[j] < 2 ^ n := hC.1 C[j] (List.getElem_mem hjC)
    have hcsi := canonD2_spec n C[i] hxi
    have hcsj := canonD2_spec n C[j] hxj
    obtain ⟨oi, hoi, heqi, hrepi⟩ := hlookup C[i] (List.getElem_mem hiC)
    obtain ⟨oj, hoj, heqj, hrepj⟩ := hlookup C[j] (List.getElem_mem hjC)
    have hdi := hall_diag orbs[oi] (List.getElem_mem hoi)
    have hdj := hall_diag orbs[oj] (List.getElem_mem hoj)
    -- Helper proving `dotInt (vecOf C[a]) (vecOf C[b]) ≤ -S` whenever `oa ≤ ob`
    have hord : ∀ (a b : Nat) (ha : a < C.length) (hb : b < C.length) (hab : a ≠ b)
        (oa ob : Nat) (hoa : oa < orbs.length) (hob : ob < orbs.length),
        oa ≤ ob →
        getEntry C[a] = orbs[oa] → orbs[oa].rep = (canonD2 n C[a]).2 →
        getEntry C[b] = orbs[ob] → orbs[ob].rep = (canonD2 n C[b]).2 →
        dotInt (vecOf C[a]) (vecOf C[b]) ≤ - Int.ofNat S := by
      intro a b ha hb hab oa ob hoa hob hle hea hrepa heb hrepb
      have hxa : C[a] < 2 ^ n := hC.1 C[a] (List.getElem_mem ha)
      have hxb : C[b] < 2 ^ n := hC.1 C[b] (List.getElem_mem hb)
      have hcsa := canonD2_spec n C[a] hxa
      have hcsb := canonD2_spec n C[b] hxb
      have hda := hall_diag orbs[oa] (List.getElem_mem hoa)
      have hdb := hall_diag orbs[ob] (List.getElem_mem hob)
      let h := xorD2 (canonD2 n C[a]).1 (canonD2 n C[b]).1
      have hh : h < 4 := xorD2_lt hcsa.1 hcsb.1
      -- Apply `D_2` automorphism `g_a` to valid code `C`!
      have hCg : IsValidDeletionCode n s (C.map (applyD2 n (canonD2 n C[a]).1)) :=
        isValidDeletionCode_map_applyD2 hs hC
      have hpair_g := hCg.2 a b (by simp [ha]) (by simp [hb]) hab
      simp only [List.getElem_map] at hpair_g
      have ha_img : applyD2 n (canonD2 n C[a]).1 C[a] = orbs[oa].rep := by
        rw [hrepa, hcsa.2.1]
      have hb_img : applyD2 n (canonD2 n C[a]).1 C[b] = applyD2 n h orbs[ob].rep := by
        have hcb : C[b] = applyD2 n (canonD2 n C[b]).1 orbs[ob].rep := by
          rw [hrepb]; exact hcsb.2.2.2.symm
        have hstep := congrArg (applyD2 n (canonD2 n C[a]).1) hcb
        rw [hstep]
        exact applyD2_comp hcsa.1 hcsb.1 (by rw [hrepb]; exact hcsb.2.2.1)
      rw [ha_img, hb_img] at hpair_g
      have hchk := checkOrbTri_sound hpairs oa ob hoa hob hle
      have hdot := checkOrbPair_sound hs hchk hh hpair_g.1 hpair_g.2.1
      simp only [vecOf, hea, heb]
      rw [dotInt_vecOfOrb hcsa.1 hcsb.1 hda.2.1 hda.2.2.1 hda.2.2.2.1 hda.2.2.2.2.1
            hdb.2.1 hdb.2.2.1 hdb.2.2.2.1 hdb.2.2.2.2.1]
      exact hdot
    simp only [vs, List.getElem_map]
    rcases Nat.le_or_ge oi oj with hle | hge
    · exact hord i j hiC hjC hne_ij oi oj hoi hoj hle heqi hrepi heqj hrepj
    · rw [dotInt_comm]
      exact hord j i hjC hiC hne_ij.symm oj oi hoj hoi hge heqj hrepj heqi hrepi
  -- Apply the Sum-of-Squares Gram bound!
  have hsos := sos_gram_bound R (Int.ofNat T - Int.ofNat S) (- Int.ofNat S) vs hvs_len hvs_diag hvs_off
  have hvslen : vs.length = C.length := List.length_map ..
  rw [hvslen] at hsos
  -- Rewrite `|C| * (T - S) + |C|*(|C|-1) * (-S) = |C| * (T - |C| * S)`
  rcases Nat.eq_zero_or_pos C.length with h0 | hpos
  · omega
  · have hmul_sub : C.length * (C.length - 1) + C.length = C.length * C.length := by
      cases hk : C.length with
      | zero => omega
      | succ k =>
        simp only [Nat.add_sub_cancel]
        rw [Nat.mul_add, Nat.mul_one]
    have halg : Int.ofNat C.length * (Int.ofNat T - Int.ofNat S) +
        Int.ofNat (C.length * (C.length - 1)) * (- Int.ofNat S) =
        Int.ofNat C.length * Int.ofNat T - Int.ofNat (C.length * C.length) * Int.ofNat S := by
      rw [Int.mul_sub, Int.mul_neg]
      have hsum : Int.ofNat (C.length * (C.length - 1)) * Int.ofNat S + Int.ofNat C.length * Int.ofNat S =
          Int.ofNat (C.length * C.length) * Int.ofNat S := by
        rw [← Int.add_mul]
        have : Int.ofNat (C.length * (C.length - 1)) + Int.ofNat C.length = Int.ofNat (C.length * C.length) := by
          rw [← hmul_sub]; rfl
        rw [this]
      omega
    rw [halg] at hsos
    have hnat_le : C.length * C.length * S ≤ C.length * T := by
      have h1 : Int.ofNat (C.length * C.length * S) ≤ Int.ofNat (C.length * T) := by
        have hcc : Int.ofNat (C.length * C.length * S) = Int.ofNat (C.length * C.length) * Int.ofNat S := rfl
        have hct : Int.ofNat (C.length * T) = Int.ofNat C.length * Int.ofNat T := rfl
        omega
      exact Int.ofNat_le.mp h1
    have hcancel : C.length * S ≤ T := by
      have h1 : C.length * (C.length * S) ≤ C.length * T := by
        simpa [Nat.mul_assoc] using hnat_le
      exact Nat.le_of_mul_le_mul_left h1 hpos
    rcases Nat.lt_or_ge C.length (M + 1) with hlt | hge
    · omega
    · have hmul : (M + 1) * S ≤ C.length * S := Nat.mul_le_mul_right S hge
      omega

/--
  Universal Pure-Kernel Schrijver θ' PSD Upper Bound Theorem for ALL `(n, s)` (`s ≤ n`).
  Given `D_2`-equivariant integer coordinate blocks `orbs` of dimensions `(r0, r1, r2, r3)`
  and exact positive integers `S, T` with `T < (M + 1) * S`, certifies `|C| ≤ M` for EVERY
  valid `(n, s)` binary deletion-correcting code `C`.
-/
theorem weak_duality_schrijver_psd {n s r0 r1 r2 r3 S T M : Nat}
    (hs : s ≤ n) (hS : 0 < S) (hbound : T < (M + 1) * S)
    (orbs : List OrbEntry)
    (hdiag : orbs.all (checkOrbDiag n r0 r1 r2 r3 (Int.ofNat T - Int.ofNat S)) = true)
    (hcover : checkCoverRec n (buildOrbTree n orbs) n 0 = true)
    (hpairs : checkOrbTri n s (- Int.ofNat S) orbs = true)
    {C : List Nat} (hC : IsValidDeletionCode n s C) :
    C.length ≤ M :=
  weak_duality_schrijver_psd_on hs hS hbound orbs hdiag hpairs hC
    (fun x hx => checkCoverRec_all hcover x (hC.1 x hx))

end DeletionCode.SchrijverPSD
