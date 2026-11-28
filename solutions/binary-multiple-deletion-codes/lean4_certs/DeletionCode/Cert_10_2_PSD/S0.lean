/-
  DeletionCode/Cert_10_2_PSD/S0.lean — Pair-Check Shard 0/6 for `(10, 2)`
  Rows 0..18 (4028 unordered `D_2` orbit pairs across 10 chunks)
-/
import DeletionCode.SchrijverPSD
import DeletionCode.Cert_10_2_PSD.Data

set_option maxRecDepth 65536
set_option maxHeartbeats 4000000

namespace DeletionCode.PeelReduce

open DeletionCode.SchrijverPSD

-- Chunk 0: rows 0..1 (441 orbit pairs)
private theorem h_10_2_psd_s0_c0 :
    checkOrbRows 10 2 (- Int.ofNat 3989359) 2 (orbs_10_2_psd.drop 0) = true := by rfl
-- Chunk 1: rows 2..3 (437 orbit pairs)
private theorem h_10_2_psd_s0_c1 :
    checkOrbRows 10 2 (- Int.ofNat 3989359) 2 (orbs_10_2_psd.drop 2) = true := by rfl
-- Chunk 2: rows 4..5 (433 orbit pairs)
private theorem h_10_2_psd_s0_c2 :
    checkOrbRows 10 2 (- Int.ofNat 3989359) 2 (orbs_10_2_psd.drop 4) = true := by rfl
-- Chunk 3: rows 6..7 (429 orbit pairs)
private theorem h_10_2_psd_s0_c3 :
    checkOrbRows 10 2 (- Int.ofNat 3989359) 2 (orbs_10_2_psd.drop 6) = true := by rfl
-- Chunk 4: rows 8..9 (425 orbit pairs)
private theorem h_10_2_psd_s0_c4 :
    checkOrbRows 10 2 (- Int.ofNat 3989359) 2 (orbs_10_2_psd.drop 8) = true := by rfl
-- Chunk 5: rows 10..11 (421 orbit pairs)
private theorem h_10_2_psd_s0_c5 :
    checkOrbRows 10 2 (- Int.ofNat 3989359) 2 (orbs_10_2_psd.drop 10) = true := by rfl
-- Chunk 6: rows 12..13 (417 orbit pairs)
private theorem h_10_2_psd_s0_c6 :
    checkOrbRows 10 2 (- Int.ofNat 3989359) 2 (orbs_10_2_psd.drop 12) = true := by rfl
-- Chunk 7: rows 14..15 (413 orbit pairs)
private theorem h_10_2_psd_s0_c7 :
    checkOrbRows 10 2 (- Int.ofNat 3989359) 2 (orbs_10_2_psd.drop 14) = true := by rfl
-- Chunk 8: rows 16..17 (409 orbit pairs)
private theorem h_10_2_psd_s0_c8 :
    checkOrbRows 10 2 (- Int.ofNat 3989359) 2 (orbs_10_2_psd.drop 16) = true := by rfl
-- Chunk 9: rows 18..18 (203 orbit pairs)
private theorem h_10_2_psd_s0_c9 :
    checkOrbRows 10 2 (- Int.ofNat 3989359) 1 (orbs_10_2_psd.drop 18) = true := by rfl

theorem hshard_10_2_psd_s0 :
    checkOrbRows 10 2 (- Int.ofNat 3989359) 19 (orbs_10_2_psd.drop 0) = true := by
  have h9 := h_10_2_psd_s0_c9
  have h8 : checkOrbRows 10 2 (- Int.ofNat 3989359) 3 (orbs_10_2_psd.drop 16) = true :=
    checkOrbRows_add 10 2 (- Int.ofNat 3989359) 2 1 (orbs_10_2_psd.drop 16) h_10_2_psd_s0_c8
      (by simpa [List.drop_drop, Nat.add_comm] using h9)
  have h7 : checkOrbRows 10 2 (- Int.ofNat 3989359) 5 (orbs_10_2_psd.drop 14) = true :=
    checkOrbRows_add 10 2 (- Int.ofNat 3989359) 2 3 (orbs_10_2_psd.drop 14) h_10_2_psd_s0_c7
      (by simpa [List.drop_drop, Nat.add_comm] using h8)
  have h6 : checkOrbRows 10 2 (- Int.ofNat 3989359) 7 (orbs_10_2_psd.drop 12) = true :=
    checkOrbRows_add 10 2 (- Int.ofNat 3989359) 2 5 (orbs_10_2_psd.drop 12) h_10_2_psd_s0_c6
      (by simpa [List.drop_drop, Nat.add_comm] using h7)
  have h5 : checkOrbRows 10 2 (- Int.ofNat 3989359) 9 (orbs_10_2_psd.drop 10) = true :=
    checkOrbRows_add 10 2 (- Int.ofNat 3989359) 2 7 (orbs_10_2_psd.drop 10) h_10_2_psd_s0_c5
      (by simpa [List.drop_drop, Nat.add_comm] using h6)
  have h4 : checkOrbRows 10 2 (- Int.ofNat 3989359) 11 (orbs_10_2_psd.drop 8) = true :=
    checkOrbRows_add 10 2 (- Int.ofNat 3989359) 2 9 (orbs_10_2_psd.drop 8) h_10_2_psd_s0_c4
      (by simpa [List.drop_drop, Nat.add_comm] using h5)
  have h3 : checkOrbRows 10 2 (- Int.ofNat 3989359) 13 (orbs_10_2_psd.drop 6) = true :=
    checkOrbRows_add 10 2 (- Int.ofNat 3989359) 2 11 (orbs_10_2_psd.drop 6) h_10_2_psd_s0_c3
      (by simpa [List.drop_drop, Nat.add_comm] using h4)
  have h2 : checkOrbRows 10 2 (- Int.ofNat 3989359) 15 (orbs_10_2_psd.drop 4) = true :=
    checkOrbRows_add 10 2 (- Int.ofNat 3989359) 2 13 (orbs_10_2_psd.drop 4) h_10_2_psd_s0_c2
      (by simpa [List.drop_drop, Nat.add_comm] using h3)
  have h1 : checkOrbRows 10 2 (- Int.ofNat 3989359) 17 (orbs_10_2_psd.drop 2) = true :=
    checkOrbRows_add 10 2 (- Int.ofNat 3989359) 2 15 (orbs_10_2_psd.drop 2) h_10_2_psd_s0_c1
      (by simpa [List.drop_drop, Nat.add_comm] using h2)
  have h0 : checkOrbRows 10 2 (- Int.ofNat 3989359) 19 (orbs_10_2_psd.drop 0) = true :=
    checkOrbRows_add 10 2 (- Int.ofNat 3989359) 2 17 (orbs_10_2_psd.drop 0) h_10_2_psd_s0_c0
      (by simpa [List.drop_drop, Nat.add_comm] using h1)
  exact h0

end DeletionCode.PeelReduce
