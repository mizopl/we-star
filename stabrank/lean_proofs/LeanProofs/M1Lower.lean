/-
χ(|H⟩) ≥ 2, χ(|T⟩) ≥ 2 against `stabRankP 2`, and χ(|H₃⟩) ≥ 2, χ(|N⟩) ≥ 2
against `stabRankP 3` and `Stabilizer.stabRank`: none of the four one-qudit
magic states is a stabilizer state.

The argument is the algebraic one-modulus test `IsStabP.pow_period_eq` of
`Stabilizer/RankOne.lean` (as in `QubitM2Lower.lean`): every nonzero entry of an
`IsStabP p` vector is `c ζ_D^e`, so its `D`-th power is `c^D` across the support.
Combined with `QubitHM1StabRank`, `QubitTM1StabRank`, `H3M1StabRank`, and
`NorrellM1StabRank`, all four one-copy cells are settled at `2` with both
directions machine-checked in Lean.
-/
import LeanProofs.QubitM2Lower
import LeanProofs.QubitHM1StabRank
import LeanProofs.QubitTM1StabRank
import LeanProofs.H3M1StabRank
import LeanProofs.NorrellM1StabRank
import LeanProofs.Stabilizer.RankOne

namespace StabRank

open Stabilizer

/-! ### One-qubit probe indices `0` and `1` -/

def idx2_0 : Fin (2 ^ 1) := (digitsP 2 1).symm ![0]
def idx2_1 : Fin (2 ^ 1) := (digitsP 2 1).symm ![1]

/-! ### `|H⟩` (`m = 1`) -/

set_option linter.flexible false in
theorem hVec1_idx0 : hVec 1 idx2_0 = (cH : ℂ) := by
  simp (config := { decide := true }) [hVec, hAmp1, idx2_0]

set_option linter.flexible false in
theorem hVec1_idx1 : hVec 1 idx2_1 = (sH : ℂ) := by
  simp (config := { decide := true }) [hVec, hAmp1, idx2_1]

theorem hVec1_not_isStabP : ¬ IsStabP 2 (hVec 1) := by
  intro hstab
  have hx : hVec 1 idx2_0 ≠ 0 := by rw [hVec1_idx0]; exact cH_ne_zero
  have hy : hVec 1 idx2_1 ≠ 0 := by rw [hVec1_idx1]; exact sH_ne_zero
  have h := hstab.pow_period_eq hx hy
  rw [hVec1_idx0, hVec1_idx1, stabPeriod_two] at h
  have hc := cH_sq
  have hs := sH_sq
  have h2 := sqrt2_sq_c
  have h' : ((cH : ℂ) ^ 2) ^ 2 = ((sH : ℂ) ^ 2) ^ 2 := by linear_combination h
  rw [hc, hs] at h'
  have hs2 : (Real.sqrt 2 : ℂ) = 0 := by linear_combination 2 * h'
  rw [hs2] at h2
  norm_num at h2

theorem hVec1_ne_zero : hVec 1 ≠ 0 := by
  intro h
  have h0 := hVec1_idx0
  rw [h, Pi.zero_apply] at h0
  exact cH_ne_zero h0.symm

/-- **χ(|H⟩) ≥ 2 against `IsStabP 2`.** -/
theorem qubit_h_m1_stabRankP_gt_one : stabRankP 2 (hVec 1) > 1 :=
  stabRank_gt_one_of_not_stab _ _ (decompCardsP_nonempty 2 1 _)
    (fun _ _ hσ ha => hσ.smul ha) hVec1_ne_zero hVec1_not_isStabP

/-- **χ(|H⟩) = 2**, both directions machine-checked against `IsStabP 2`. -/
theorem qubit_h_m1_stabRankP_eq_two : stabRankP 2 (hVec 1) = 2 :=
  le_antisymm qubit_h_m1_stabRankP_le_two qubit_h_m1_stabRankP_gt_one

/-! ### `|T⟩` (`m = 1`) -/

set_option linter.flexible false in
theorem tVec1_idx0 : tVec 1 idx2_0 = (cT : ℂ) := by
  simp (config := { decide := true }) [tVec, tAmp1, idx2_0]

set_option linter.flexible false in
theorem tVec1_idx1 : tVec 1 idx2_1 = Complex.exp (Real.pi / 4 * Complex.I) * sT := by
  simp (config := { decide := true }) [tVec, tAmp1, idx2_1]

theorem tVec1_not_isStabP : ¬ IsStabP 2 (tVec 1) := by
  intro hstab
  have he : Complex.exp (Real.pi / 4 * Complex.I) ≠ 0 := Complex.exp_ne_zero _
  have hx : tVec 1 idx2_0 ≠ 0 := by rw [tVec1_idx0]; exact cT_ne_zero
  have hy : tVec 1 idx2_1 ≠ 0 := by rw [tVec1_idx1]; exact mul_ne_zero he sT_ne_zero
  have h := hstab.pow_period_eq hx hy
  rw [tVec1_idx0, tVec1_idx1, stabPeriod_two, exp_pi_div_four_mul_I] at h
  have hc := cT_sq
  have hs := sT_sq
  have h2 := sqrt2_sq_c
  have h3 := sqrt3_sq_c
  have hI := Complex.I_sq
  have h' : ((cT : ℂ) ^ 2) ^ 2 = -((sT : ℂ) ^ 2) ^ 2 := by
    linear_combination h
      + ((sT : ℂ) ^ 4 * (Complex.I + 1) ^ 4 * ((Real.sqrt 2 : ℂ) ^ 2 + 2) / 16) * h2
      + ((sT : ℂ) ^ 4 * (Complex.I ^ 2 + 4 * Complex.I + 5) / 4) * hI
  rw [hc, hs] at h'
  have hfalse : (24 : ℂ) = 0 := by
    linear_combination 36 * h' - 2 * h3
  norm_num at hfalse

theorem tVec1_ne_zero : tVec 1 ≠ 0 := by
  intro h
  have h0 := tVec1_idx0
  rw [h, Pi.zero_apply] at h0
  exact cT_ne_zero h0.symm

/-- **χ(|T⟩) ≥ 2 against `IsStabP 2`.** -/
theorem qubit_t_m1_stabRankP_gt_one : stabRankP 2 (tVec 1) > 1 :=
  stabRank_gt_one_of_not_stab _ _ (decompCardsP_nonempty 2 1 _)
    (fun _ _ hσ ha => hσ.smul ha) tVec1_ne_zero tVec1_not_isStabP

/-- **χ(|T⟩) = 2**, both directions machine-checked against `IsStabP 2`. -/
theorem qubit_t_m1_stabRankP_eq_two : stabRankP 2 (tVec 1) = 2 :=
  le_antisymm qubit_t_m1_stabRankP_le_two qubit_t_m1_stabRankP_gt_one

/-! ### One-qutrit probe indices `0`, `1`, `2` -/

def idx3_0 : Fin (3 ^ 1) := (digitsP 3 1).symm ![0]
def idx3_1 : Fin (3 ^ 1) := (digitsP 3 1).symm ![1]
def idx3_2 : Fin (3 ^ 1) := (digitsP 3 1).symm ![2]

/-! ### `|H₃⟩` (`m = 1`) -/

set_option linter.flexible false in
theorem h3Vec1_idx0 : h3Vec 1 idx3_0 = NH3C * (3 + (Real.sqrt 3 : ℂ)) / 6 := by
  have h : digitsP 3 1 idx3_0 0 = 0 := by decide
  simp [h3Vec, h, h3Amp1_eq]

set_option linter.flexible false in
theorem h3Vec1_idx1 : h3Vec 1 idx3_1 = NH3C * (Real.sqrt 3 : ℂ) / 6 := by
  have h : digitsP 3 1 idx3_1 0 = 1 := by decide
  simp [h3Vec, h, h3Amp1_eq]

theorem three_add_sqrt3_ne_zero : (3 : ℂ) + (Real.sqrt 3 : ℂ) ≠ 0 := by
  intro h
  have h3 := sqrt3_sq_cH
  have hs : (Real.sqrt 3 : ℂ) = -3 := by linear_combination h
  rw [hs] at h3
  norm_num at h3

theorem h3Vec1_idx0_ne_zero : h3Vec 1 idx3_0 ≠ 0 := by
  rw [h3Vec1_idx0]
  exact div_ne_zero (mul_ne_zero NH3C_ne_zero three_add_sqrt3_ne_zero) (by norm_num)

theorem h3Vec1_idx1_ne_zero : h3Vec 1 idx3_1 ≠ 0 := by
  rw [h3Vec1_idx1]
  exact div_ne_zero (mul_ne_zero NH3C_ne_zero sqrt3_ne_zero) (by norm_num)

theorem h3Vec1_not_isStabP : ¬ IsStabP 3 (h3Vec 1) := by
  intro hstab
  have h := hstab.pow_period_eq h3Vec1_idx0_ne_zero h3Vec1_idx1_ne_zero
  rw [h3Vec1_idx0, h3Vec1_idx1, stabPeriod_three] at h
  have hmul : NH3C ^ 3 * (((3 + (Real.sqrt 3 : ℂ)) / 6) ^ 3 - ((Real.sqrt 3 : ℂ) / 6) ^ 3) = 0 := by
    linear_combination h
  have hdiff := (mul_eq_zero.mp hmul).resolve_left (pow_ne_zero 3 NH3C_ne_zero)
  have h3 := sqrt3_sq_cH
  have hfalse : (27 : ℂ) = 0 := by
    linear_combination 216 * (2 - (Real.sqrt 3 : ℂ)) * hdiff
      + (9 + 9 * (Real.sqrt 3 : ℂ)) * h3
  norm_num at hfalse

theorem h3Vec1_ne_zero : h3Vec 1 ≠ 0 := by
  intro h
  have h0 := h3Vec1_idx0_ne_zero
  rw [h] at h0
  exact h0 rfl

/-- **χ(|H₃⟩) ≥ 2 against `IsStabP 3`.** -/
theorem h3_m1_stabRankP_gt_one : stabRankP 3 (h3Vec 1) > 1 :=
  stabRank_gt_one_of_not_stab _ _ (decompCardsP_nonempty 3 1 _)
    (fun _ _ hσ ha => hσ.smul ha) h3Vec1_ne_zero h3Vec1_not_isStabP

/-- **χ(|H₃⟩) ≥ 2 against `IsStab`.** -/
theorem h3_m1_stabRank_gt_one : Stabilizer.stabRank (IsStab (n := 1)) (h3Vec 1) > 1 := by
  rw [stabRank_eq_stabRankP]
  exact h3_m1_stabRankP_gt_one

/-- **χ(|H₃⟩) = 2**, both directions machine-checked against `IsStab`. -/
theorem h3_m1_stabRank_eq_two : Stabilizer.stabRank (IsStab (n := 1)) (h3Vec 1) = 2 :=
  le_antisymm h3_m1_stabRank_le_two h3_m1_stabRank_gt_one

/-! ### `|N⟩` (`m = 1`) -/

set_option linter.flexible false in
theorem norrellVec1_idx0 :
    norrellVec 1 idx3_0 = (Real.sqrt 2 : ℂ) * (Real.sqrt 3 : ℂ) / 6 := by
  have h : digitsP 3 1 idx3_0 0 = 0 := by decide
  simp [norrellVec, h, norrellAmp1_zero]

set_option linter.flexible false in
theorem norrellVec1_idx2 :
    norrellVec 1 idx3_2 = -((Real.sqrt 2 : ℂ) * (Real.sqrt 3 : ℂ)) / 3 := by
  have h : digitsP 3 1 idx3_2 0 = 2 := by decide
  simp [norrellVec, h, norrellAmp1_two]

theorem sqrt2_ne_zero_c : (Real.sqrt 2 : ℂ) ≠ 0 := by
  intro hz
  have hp : (Real.sqrt 2 : ℂ) * (Real.sqrt 2 : ℂ) = 0 := by rw [hz]; ring
  rw [sqrt2_sq_cN] at hp
  norm_num at hp

theorem norrellVec1_idx0_ne_zero : norrellVec 1 idx3_0 ≠ 0 := by
  rw [norrellVec1_idx0]
  exact div_ne_zero (mul_ne_zero sqrt2_ne_zero_c sqrt3_ne_zero) (by norm_num)

theorem norrellVec1_idx2_ne_zero : norrellVec 1 idx3_2 ≠ 0 := by
  rw [norrellVec1_idx2]
  exact div_ne_zero (neg_ne_zero.mpr (mul_ne_zero sqrt2_ne_zero_c sqrt3_ne_zero)) (by norm_num)

theorem norrellVec1_not_isStabP : ¬ IsStabP 3 (norrellVec 1) := by
  intro hstab
  have h := hstab.pow_period_eq norrellVec1_idx0_ne_zero norrellVec1_idx2_ne_zero
  rw [norrellVec1_idx0, norrellVec1_idx2, stabPeriod_three] at h
  have hpow : ((Real.sqrt 2 : ℂ) * (Real.sqrt 3 : ℂ)) ^ 3 = 0 := by
    linear_combination 24 * h
  exact mul_ne_zero sqrt2_ne_zero_c sqrt3_ne_zero (eq_zero_of_pow_eq_zero hpow)

theorem norrellVec1_ne_zero : norrellVec 1 ≠ 0 := by
  intro h
  have h0 := norrellVec1_idx0_ne_zero
  rw [h] at h0
  exact h0 rfl

/-- **χ(|N⟩) ≥ 2 against `IsStabP 3`.** -/
theorem norrell_m1_stabRankP_gt_one : stabRankP 3 (norrellVec 1) > 1 :=
  stabRank_gt_one_of_not_stab _ _ (decompCardsP_nonempty 3 1 _)
    (fun _ _ hσ ha => hσ.smul ha) norrellVec1_ne_zero norrellVec1_not_isStabP

/-- **χ(|N⟩) ≥ 2 against `IsStab`.** -/
theorem norrell_m1_stabRank_gt_one : Stabilizer.stabRank (IsStab (n := 1)) (norrellVec 1) > 1 := by
  rw [stabRank_eq_stabRankP]
  exact norrell_m1_stabRankP_gt_one

/-- **χ(|N⟩) = 2**, both directions machine-checked against `IsStab`. -/
theorem norrell_m1_stabRank_eq_two : Stabilizer.stabRank (IsStab (n := 1)) (norrellVec 1) = 2 :=
  le_antisymm norrell_m1_stabRank_le_two norrell_m1_stabRank_gt_one

end StabRank
