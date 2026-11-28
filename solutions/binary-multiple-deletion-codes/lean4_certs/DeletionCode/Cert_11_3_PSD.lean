/-
  DeletionCode/Cert_11_3_PSD.lean — Pure-Kernel Flat-Wave Onion-Peeling + Schrijver θ' PSD Proof for `(11, 3)`
  Source certificate: `cert_psd_11_3_peeled.json`
  Reduction: 2 symbolic insertion balls + 85 `D_2`-orbit domination steps (2 flat wave(s)) -> 1246 core vertices (321 orbits)
  Core Gram bound: `T / S = 43683368 / 6241589 = 6.998758 < 7` => `M_3(11) ≤ 2 + 6 = 8`!
  Zero Mathlib, zero sorryAx, zero native_decide / Lean.ofReduceBool.
-/
import DeletionCode.Basic
import DeletionCode.DualLP
import DeletionCode.CutDual
import DeletionCode.RecDual
import DeletionCode.SchrijverPSD
import DeletionCode.PeelReduce
import DeletionCode.Cert_11_3_PSD_Shards.Data
import DeletionCode.Cert_11_3_PSD_Shards.Trees
import DeletionCode.Cert_11_3_PSD_Shards.P0
import DeletionCode.Cert_11_3_PSD_Shards.P1
import DeletionCode.Cert_11_3_PSD_Shards.P2
import DeletionCode.Cert_11_3_PSD_Shards.P3
import DeletionCode.Cert_11_3_PSD_Shards.P4
import DeletionCode.Cert_11_3_PSD_Shards.P5
import DeletionCode.Cert_11_3_PSD_Shards.S0
import DeletionCode.Cert_11_3_PSD_Shards.S1
import DeletionCode.Cert_11_3_PSD_Shards.S2
import DeletionCode.Cert_11_3_PSD_Shards.S3
import DeletionCode.Cert_11_3_PSD_Shards.S4
import DeletionCode.Cert_11_3_PSD_Shards.S5
import DeletionCode.Cert_11_3_PSD_Shards.S6
import DeletionCode.Cert_11_3_PSD_Shards.S7

set_option maxRecDepth 65536
set_option maxHeartbeats 4000000

namespace DeletionCode.PeelReduce

open DeletionCode
open DeletionCode.DualLP
open DeletionCode.CutDual
open DeletionCode.RecDual
open DeletionCode.SchrijverPSD

private def wave_11_3_psd_w0 : List (Nat × Nat) := wave_11_3_psd_w0_p0 ++ wave_11_3_psd_w0_p1 ++ wave_11_3_psd_w0_p2 ++ wave_11_3_psd_w0_p3
private theorem happly_11_3_psd_w0 :
    applyDomSteps 11 initTree_11_3_psd wave_11_3_psd_w0 = midTree_11_3_psd_0 := by rfl
private theorem hwave_11_3_psd_w0 : ∀ st ∈ wave_11_3_psd_w0, checkDomWaveStep 11 3 initTree_11_3_psd midTree_11_3_psd_0 st = true := by
  intro st hst
  simp only [wave_11_3_psd_w0, List.mem_append] at hst
  rcases hst with hst | hcur
  case inr => exact hwave_11_3_psd_w0_p3 st hcur
  rcases hst with hst | hcur
  case inr => exact hwave_11_3_psd_w0_p2 st hcur
  rcases hst with hst | hcur
  case inr => exact hwave_11_3_psd_w0_p1 st hcur
  exact hwave_11_3_psd_w0_p0 st hst
private def wave_11_3_psd_w1 : List (Nat × Nat) := wave_11_3_psd_w1_p0 ++ wave_11_3_psd_w1_p1
private theorem happly_11_3_psd_w1 :
    applyDomSteps 11 midTree_11_3_psd_0 wave_11_3_psd_w1 = coreTree_11_3_psd := by rfl
private theorem hwave_11_3_psd_w1 : ∀ st ∈ wave_11_3_psd_w1, checkDomWaveStep 11 3 midTree_11_3_psd_0 coreTree_11_3_psd st = true := by
  intro st hst
  simp only [wave_11_3_psd_w1, List.mem_append] at hst
  rcases hst with hst | hcur
  case inr => exact hwave_11_3_psd_w1_p1 st hcur
  exact hwave_11_3_psd_w1_p0 st hst

private theorem hdiag_11_3_psd :
    orbs_11_3_psd.all (checkOrbDiag 11 10 8 6 8 (Int.ofNat 43683368 - Int.ofNat 6241589)) = true := by
  rfl

private theorem hcover_11_3_psd :
    checkTreeCoveredByOrbs 11 coreTree_11_3_psd (buildOrbTree 11 orbs_11_3_psd) = true := by
  rfl

private theorem hpairs_11_3_psd : checkOrbTri 11 3 (- Int.ofNat 6241589) orbs_11_3_psd = true := by
  have h7 := hshard_11_3_psd_s7
  have h6 : checkOrbTri 11 3 (- Int.ofNat 6241589) (orbs_11_3_psd.drop 162) = true :=
    checkOrbTri_of_rows 11 3 (- Int.ofNat 6241589) 48 (orbs_11_3_psd.drop 162) hshard_11_3_psd_s6
      (by simpa [List.drop_drop, Nat.add_comm] using h7)
  have h5 : checkOrbTri 11 3 (- Int.ofNat 6241589) (orbs_11_3_psd.drop 125) = true :=
    checkOrbTri_of_rows 11 3 (- Int.ofNat 6241589) 37 (orbs_11_3_psd.drop 125) hshard_11_3_psd_s5
      (by simpa [List.drop_drop, Nat.add_comm] using h6)
  have h4 : checkOrbTri 11 3 (- Int.ofNat 6241589) (orbs_11_3_psd.drop 94) = true :=
    checkOrbTri_of_rows 11 3 (- Int.ofNat 6241589) 31 (orbs_11_3_psd.drop 94) hshard_11_3_psd_s4
      (by simpa [List.drop_drop, Nat.add_comm] using h5)
  have h3 : checkOrbTri 11 3 (- Int.ofNat 6241589) (orbs_11_3_psd.drop 67) = true :=
    checkOrbTri_of_rows 11 3 (- Int.ofNat 6241589) 27 (orbs_11_3_psd.drop 67) hshard_11_3_psd_s3
      (by simpa [List.drop_drop, Nat.add_comm] using h4)
  have h2 : checkOrbTri 11 3 (- Int.ofNat 6241589) (orbs_11_3_psd.drop 43) = true :=
    checkOrbTri_of_rows 11 3 (- Int.ofNat 6241589) 24 (orbs_11_3_psd.drop 43) hshard_11_3_psd_s2
      (by simpa [List.drop_drop, Nat.add_comm] using h3)
  have h1 : checkOrbTri 11 3 (- Int.ofNat 6241589) (orbs_11_3_psd.drop 21) = true :=
    checkOrbTri_of_rows 11 3 (- Int.ofNat 6241589) 22 (orbs_11_3_psd.drop 21) hshard_11_3_psd_s1
      (by simpa [List.drop_drop, Nat.add_comm] using h2)
  have h0 : checkOrbTri 11 3 (- Int.ofNat 6241589) (orbs_11_3_psd.drop 0) = true :=
    checkOrbTri_of_rows 11 3 (- Int.ofNat 6241589) 21 (orbs_11_3_psd.drop 0) hshard_11_3_psd_s0
      (by simpa [List.drop_drop, Nat.add_comm] using h1)
  simpa using h0

theorem cert_11_3_psd_upper_bound {C : List Nat} (hC : IsValidDeletionCode 11 3 C) :
    C.length ≤ 8 :=
  weak_duality_peel_wave2_psd
    (n := 11) (s := 3) (r0 := 10) (r1 := 8) (r2 := 6) (r3 := 8)
    (S := 6241589) (T := 43683368) (M_core := 6)
    (by omega) (by omega) (by omega)
    balls_11_3_psd initTree_11_3_psd midTree_11_3_psd_0 coreTree_11_3_psd wave_11_3_psd_w0 wave_11_3_psd_w1 orbs_11_3_psd
    hinit_11_3_psd hinv0_11_3_psd happly_11_3_psd_w0 hwave_11_3_psd_w0 happly_11_3_psd_w1 hwave_11_3_psd_w1 hdiag_11_3_psd hcover_11_3_psd hpairs_11_3_psd hC

def cert_11_3_psd_code : List Nat := [0, 15, 254, 312, 907, 1753, 1984, 2047]

theorem cert_11_3_psd_code_valid : IsValidDeletionCode 11 3 cert_11_3_psd_code :=
  checkCode3_sound 11 (by decide) (buildOwner3 11 cert_11_3_psd_code) cert_11_3_psd_code (by rfl)

theorem exact_opt_11_3_psd :
    (IsValidDeletionCode 11 3 cert_11_3_psd_code ∧ cert_11_3_psd_code.length = 8) ∧
    (∀ C : List Nat, IsValidDeletionCode 11 3 C → C.length ≤ 8) :=
  ⟨⟨cert_11_3_psd_code_valid, rfl⟩, fun _ hC => cert_11_3_psd_upper_bound hC⟩

end DeletionCode.PeelReduce
