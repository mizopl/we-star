/-
  DeletionCode/Cert_10_2_PSD.lean — Pure-Kernel Flat-Wave Onion-Peeling + Schrijver θ' PSD Proof for `(10, 2)`
  Source certificate: `cert_psd_10_2_peeled.json`
  Reduction: 2 symbolic insertion balls + 20 `D_2`-orbit domination steps (1 flat wave(s)) -> 836 core vertices (221 orbits)
  Core Gram bound: `T / S = 63775738 / 3989359 = 15.986462 < 16` => `M_2(10) ≤ 2 + 15 = 17`!
  Zero Mathlib, zero sorryAx, zero native_decide / Lean.ofReduceBool.
-/
import DeletionCode.Basic
import DeletionCode.DualLP
import DeletionCode.CutDual
import DeletionCode.RecDual
import DeletionCode.SchrijverPSD
import DeletionCode.PeelReduce
import DeletionCode.Cert_10_2_PSD.Data
import DeletionCode.Cert_10_2_PSD.S0
import DeletionCode.Cert_10_2_PSD.S1
import DeletionCode.Cert_10_2_PSD.S2
import DeletionCode.Cert_10_2_PSD.S3
import DeletionCode.Cert_10_2_PSD.S4
import DeletionCode.Cert_10_2_PSD.S5

set_option maxRecDepth 65536
set_option maxHeartbeats 4000000

namespace DeletionCode.PeelReduce

open DeletionCode
open DeletionCode.DualLP
open DeletionCode.CutDual
open DeletionCode.RecDual
open DeletionCode.SchrijverPSD

private abbrev Z := BTree.zero
private abbrev O := BTree.one
private abbrev N := BTree.node

private def initTree_10_2_psd : BTree :=
  (N (N (N (N (N (N (N (N Z (N Z (N Z O))) (N (N Z (N Z O)) (N (N Z O) O))) (N (N (N Z (N Z O)) (N (N Z O) O)) (N (N (N Z O) O) O))) (N (N (N (N Z (N Z O)) (N (N Z O) O)) (N (N (N Z O) O) O)) (N (N (N (N Z O) O) O) O))) (N (N (N (N (N Z (N Z O)) (N (N Z O) O)) (N (N (N Z O) O) O)) (N (N (N (N Z O) O) O) O)) (N (N (N (N (N Z O) O) O) O) O))) (N (N (N (N (N (N Z (N Z O)) (N (N Z O) O)) (N (N (N Z O) O) O)) (N (N (N (N Z O) O) O) O)) (N (N (N (N (N Z O) O) O) O) O)) (N (N (N (N (N (N Z O) O) O) O) O) (N O (N O (N O (N O (N O Z)))))))) (N (N (N (N (N (N (N Z (N Z O)) (N (N Z O) O)) (N (N (N Z O) O) O)) (N (N (N (N Z O) O) O) O)) (N (N (N (N (N Z O) O) O) O) O)) (N (N (N (N (N (N Z O) O) O) O) O) (N O (N O (N O (N O (N O Z))))))) (N (N (N (N (N (N (N Z O) O) O) O) O) (N O (N O (N O (N O (N O Z)))))) (N (N O (N O (N O (N O (N O Z))))) (N (N O (N O (N O (N O Z)))) (N (N O (N O (N O Z))) (N (N O (N O Z)) (N (N O Z) Z)))))))) (N (N (N (N (N (N (N (N Z (N Z O)) (N (N Z O) O)) (N (N (N Z O) O) O)) (N (N (N (N Z O) O) O) O)) (N (N (N (N (N Z O) O) O) O) O)) (N (N (N (N (N (N Z O) O) O) O) O) (N O (N O (N O (N O (N O Z))))))) (N (N (N (N (N (N (N Z O) O) O) O) O) (N O (N O (N O (N O (N O Z)))))) (N (N O (N O (N O (N O (N O Z))))) (N (N O (N O (N O (N O Z)))) (N (N O (N O (N O Z))) (N (N O (N O Z)) (N (N O Z) Z))))))) (N (N (N (N (N (N (N (N Z O) O) O) O) O) (N O (N O (N O (N O (N O Z)))))) (N (N O (N O (N O (N O (N O Z))))) (N (N O (N O (N O (N O Z)))) (N (N O (N O (N O Z))) (N (N O (N O Z)) (N (N O Z) Z)))))) (N (N (N O (N O (N O (N O (N O Z))))) (N (N O (N O (N O (N O Z)))) (N (N O (N O (N O Z))) (N (N O (N O Z)) (N (N O Z) Z))))) (N (N (N O (N O (N O (N O Z)))) (N (N O (N O (N O Z))) (N (N O (N O Z)) (N (N O Z) Z)))) (N (N (N O (N O (N O Z))) (N (N O (N O Z)) (N (N O Z) Z))) (N (N (N O (N O Z)) (N (N O Z) Z)) (N (N (N O Z) Z) Z))))))))

private theorem hinit_10_2_psd : buildBallsComplTree 10 2 balls_10_2_psd = initTree_10_2_psd := by rfl

private theorem hinv0_10_2_psd : checkD2InvRec 10 initTree_10_2_psd 10 0 = true := by rfl

private def coreTree_10_2_psd : BTree :=
  (N (N (N (N (N (N (N (N Z (N Z (N Z O))) (N Z (N Z O))) (N Z (N (N (N Z O) (N O Z)) O))) (N (N (N (N Z (N Z O)) (N (N Z O) (N O Z))) (N (N (N Z O) (N O Z)) (N (N O Z) Z))) (N (N (N (N Z O) O) (N O (N O Z))) O))) (N (N (N (N (N Z (N Z O)) (N (N Z O) O)) (N (N (N Z O) O) (N O (N O Z)))) (N (N (N (N Z O) O) (N O (N O Z))) (N O (N (N O Z) Z)))) (N (N (N (N (N Z O) O) O) (N O (N O (N O Z)))) O))) (N (N (N (N (N (N Z (N Z O)) (N (N Z O) O)) (N (N (N Z O) O) O)) (N (N (N (N Z O) O) O) (N O (N O (N O Z))))) (N (N (N (N (N Z O) O) O) (N O (N O (N O Z)))) (N O (N O (N (N O Z) Z))))) (N (N (N (N (N (N Z O) O) O) O) (N O (N O (N O (N O Z))))) (N O (N O (N O (N O (N O Z)))))))) (N (N (N (N (N (N (N Z (N Z O)) (N Z O)) (N (N (N Z O) (N O Z)) O)) (N (N (N (N Z O) O) (N O (N O Z))) O)) (N (N (N (N (N Z O) O) O) (N O (N O (N O Z)))) (N O (N O (N O (N O Z)))))) (N (N (N (N (N (N Z O) O) O) O) (N O (N O (N O (N O Z))))) (N O (N O (N O (N (N O Z) Z)))))) (N (N (N (N (N (N (N Z O) O) O) O) O) (N (N (N (N (N Z O) O) O) O) (N O (N O (N O (N O Z)))))) (N (N O (N (N (N (N Z O) O) O) (N O (N O (N O Z))))) (N (N O (N (N (N Z O) O) (N O (N O Z)))) (N (N O (N (N Z O) (N O Z))) (N (N O Z) (N (N O Z) Z)))))))) (N (N (N (N (N (N (N (N Z (N Z O)) (N Z O)) (N (N (N Z O) (N O Z)) O)) (N (N (N (N Z O) O) (N O (N O Z))) O)) (N (N (N (N (N Z O) O) O) (N O (N O (N O Z)))) O)) (N (N (N (N (N (N Z O) O) O) O) (N O (N O (N O (N O Z))))) (N O (N O (N O (N O (N O Z))))))) (N (N (N (N (N (N Z (N Z O)) O) O) O) (N (N (N (N (N Z O) O) O) O) (N O (N O (N O (N O Z)))))) (N (N (N (N (N (N Z O) O) O) O) (N (N (N (N Z O) O) O) (N O (N O (N O Z))))) (N (N O (N (N (N Z O) O) (N O (N O Z)))) (N (N O (N (N Z O) (N O Z))) (N (N O Z) (N (N O Z) Z))))))) (N (N (N (N (N (N (N (N Z O) O) O) O) O) (N (N (N (N (N Z O) O) O) O) (N O (N O (N O (N O Z)))))) (N (N (N (N (N Z (N Z O)) O) O) (N (N (N (N Z O) O) O) (N O (N O (N O Z))))) (N (N (N (N (N Z O) O) O) (N O (N O (N O Z)))) (N (N O (N O (N O Z))) (N (N O (N O Z)) (N (N O Z) Z)))))) (N (N (N O (N (N (N (N Z O) O) O) (N O (N O (N O Z))))) (N (N (N (N Z (N Z O)) O) (N (N (N Z O) O) (N O (N O Z)))) (N (N (N (N Z O) O) (N O (N O Z))) (N (N O (N O Z)) (N (N O Z) Z))))) (N (N (N O (N (N (N Z O) O) (N O (N O Z)))) (N (N (N Z (N Z O)) (N (N Z O) (N O Z))) (N (N (N Z O) (N O Z)) (N (N O Z) Z)))) (N (N (N O (N (N Z O) (N O Z))) Z) (N (N (N O Z) Z) (N (N (N O Z) Z) Z))))))))
private def wave_10_2_psd_w0_c0 : List (Nat × Nat) := [(11, 7), (13, 7), (19, 7), (21, 7), (22, 14), (23, 15), (27, 15), (39, 15), (43, 15), (45, 29)]
private theorem hwave_10_2_psd_w0_c0 :
    wave_10_2_psd_w0_c0.all (checkDomWaveStep 10 2 initTree_10_2_psd coreTree_10_2_psd) = true := by rfl
private def wave_10_2_psd_w0_c1 : List (Nat × Nat) := [(46, 30), (47, 31), (55, 31), (87, 31), (93, 61), (94, 62), (189, 125), (190, 126), (261, 259), (382, 254)]
private theorem hwave_10_2_psd_w0_c1 :
    wave_10_2_psd_w0_c1.all (checkDomWaveStep 10 2 initTree_10_2_psd coreTree_10_2_psd) = true := by rfl
private def wave_10_2_psd_w0 : List (Nat × Nat) := wave_10_2_psd_w0_c0 ++ wave_10_2_psd_w0_c1
private theorem happly_10_2_psd_w0 :
    applyDomSteps 10 initTree_10_2_psd wave_10_2_psd_w0 = coreTree_10_2_psd := by rfl
private theorem hwave_10_2_psd_w0 : ∀ st ∈ wave_10_2_psd_w0, checkDomWaveStep 10 2 initTree_10_2_psd coreTree_10_2_psd st = true := by
  intro st hst
  simp only [wave_10_2_psd_w0, List.mem_append] at hst
  rcases hst with hst | hcur
  case inr => exact List.all_eq_true.mp hwave_10_2_psd_w0_c1 st hcur
  exact List.all_eq_true.mp hwave_10_2_psd_w0_c0 st hst

private theorem hdiag_10_2_psd :
    orbs_10_2_psd.all (checkOrbDiag 10 26 25 19 26 (Int.ofNat 63775738 - Int.ofNat 3989359)) = true := by
  rfl

private theorem hcover_10_2_psd :
    checkTreeCoveredByOrbs 10 coreTree_10_2_psd (buildOrbTree 10 orbs_10_2_psd) = true := by
  rfl

private theorem hpairs_10_2_psd : checkOrbTri 10 2 (- Int.ofNat 3989359) orbs_10_2_psd = true := by
  have h5 := hshard_10_2_psd_s5
  have h4 : checkOrbTri 10 2 (- Int.ofNat 3989359) (orbs_10_2_psd.drop 93) = true :=
    checkOrbTri_of_rows 10 2 (- Int.ofNat 3989359) 38 (orbs_10_2_psd.drop 93) hshard_10_2_psd_s4
      (by simpa [List.drop_drop, Nat.add_comm] using h5)
  have h3 : checkOrbTri 10 2 (- Int.ofNat 3989359) (orbs_10_2_psd.drop 64) = true :=
    checkOrbTri_of_rows 10 2 (- Int.ofNat 3989359) 29 (orbs_10_2_psd.drop 64) hshard_10_2_psd_s3
      (by simpa [List.drop_drop, Nat.add_comm] using h4)
  have h2 : checkOrbTri 10 2 (- Int.ofNat 3989359) (orbs_10_2_psd.drop 40) = true :=
    checkOrbTri_of_rows 10 2 (- Int.ofNat 3989359) 24 (orbs_10_2_psd.drop 40) hshard_10_2_psd_s2
      (by simpa [List.drop_drop, Nat.add_comm] using h3)
  have h1 : checkOrbTri 10 2 (- Int.ofNat 3989359) (orbs_10_2_psd.drop 19) = true :=
    checkOrbTri_of_rows 10 2 (- Int.ofNat 3989359) 21 (orbs_10_2_psd.drop 19) hshard_10_2_psd_s1
      (by simpa [List.drop_drop, Nat.add_comm] using h2)
  have h0 : checkOrbTri 10 2 (- Int.ofNat 3989359) (orbs_10_2_psd.drop 0) = true :=
    checkOrbTri_of_rows 10 2 (- Int.ofNat 3989359) 19 (orbs_10_2_psd.drop 0) hshard_10_2_psd_s0
      (by simpa [List.drop_drop, Nat.add_comm] using h1)
  simpa using h0

theorem cert_10_2_psd_upper_bound {C : List Nat} (hC : IsValidDeletionCode 10 2 C) :
    C.length ≤ 17 :=
  weak_duality_peel_wave1_psd
    (n := 10) (s := 2) (r0 := 26) (r1 := 25) (r2 := 19) (r3 := 26)
    (S := 3989359) (T := 63775738) (M_core := 15)
    (by omega) (by omega) (by omega)
    balls_10_2_psd initTree_10_2_psd coreTree_10_2_psd wave_10_2_psd_w0 orbs_10_2_psd
    hinit_10_2_psd hinv0_10_2_psd happly_10_2_psd_w0 hwave_10_2_psd_w0 hdiag_10_2_psd hcover_10_2_psd hpairs_10_2_psd hC

def cert_10_2_psd_code : List Nat := [0, 15, 42, 120, 127, 193, 343, 460, 563, 674, 830, 896, 903, 981, 1008, 1023]

theorem cert_10_2_psd_code_valid : IsValidDeletionCode 10 2 cert_10_2_psd_code :=
  checkCode2_sound 10 (by decide) (buildOwner2 10 cert_10_2_psd_code) cert_10_2_psd_code (by rfl)

end DeletionCode.PeelReduce
