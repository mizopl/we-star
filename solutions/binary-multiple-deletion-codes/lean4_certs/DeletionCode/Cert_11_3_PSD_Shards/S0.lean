/-
  DeletionCode/Cert_11_3_PSD_Shards/S0.lean — Pair-Check Shard 0/8 for `(11, 3)`
  Rows 0..20 (6531 unordered `D_2` orbit pairs across 11 chunks)
-/
import DeletionCode.SchrijverPSD
import DeletionCode.Cert_11_3_PSD_Shards.Data

set_option maxRecDepth 65536
set_option maxHeartbeats 4000000

namespace DeletionCode.PeelReduce

open DeletionCode.SchrijverPSD

-- Chunk 0: rows 0..1 (641 orbit pairs)
private theorem h_11_3_psd_s0_c0 :
    checkOrbRows 11 3 (- Int.ofNat 6241589) 2 (orbs_11_3_psd.drop 0) = true := by rfl
-- Chunk 1: rows 2..3 (637 orbit pairs)
private theorem h_11_3_psd_s0_c1 :
    checkOrbRows 11 3 (- Int.ofNat 6241589) 2 (orbs_11_3_psd.drop 2) = true := by rfl
-- Chunk 2: rows 4..5 (633 orbit pairs)
private theorem h_11_3_psd_s0_c2 :
    checkOrbRows 11 3 (- Int.ofNat 6241589) 2 (orbs_11_3_psd.drop 4) = true := by rfl
-- Chunk 3: rows 6..7 (629 orbit pairs)
private theorem h_11_3_psd_s0_c3 :
    checkOrbRows 11 3 (- Int.ofNat 6241589) 2 (orbs_11_3_psd.drop 6) = true := by rfl
-- Chunk 4: rows 8..9 (625 orbit pairs)
private theorem h_11_3_psd_s0_c4 :
    checkOrbRows 11 3 (- Int.ofNat 6241589) 2 (orbs_11_3_psd.drop 8) = true := by rfl
-- Chunk 5: rows 10..11 (621 orbit pairs)
private theorem h_11_3_psd_s0_c5 :
    checkOrbRows 11 3 (- Int.ofNat 6241589) 2 (orbs_11_3_psd.drop 10) = true := by rfl
-- Chunk 6: rows 12..13 (617 orbit pairs)
private theorem h_11_3_psd_s0_c6 :
    checkOrbRows 11 3 (- Int.ofNat 6241589) 2 (orbs_11_3_psd.drop 12) = true := by rfl
-- Chunk 7: rows 14..15 (613 orbit pairs)
private theorem h_11_3_psd_s0_c7 :
    checkOrbRows 11 3 (- Int.ofNat 6241589) 2 (orbs_11_3_psd.drop 14) = true := by rfl
-- Chunk 8: rows 16..17 (609 orbit pairs)
private theorem h_11_3_psd_s0_c8 :
    checkOrbRows 11 3 (- Int.ofNat 6241589) 2 (orbs_11_3_psd.drop 16) = true := by rfl
-- Chunk 9: rows 18..19 (605 orbit pairs)
private theorem h_11_3_psd_s0_c9 :
    checkOrbRows 11 3 (- Int.ofNat 6241589) 2 (orbs_11_3_psd.drop 18) = true := by rfl
-- Chunk 10: rows 20..20 (301 orbit pairs)
private theorem h_11_3_psd_s0_c10 :
    checkOrbRows 11 3 (- Int.ofNat 6241589) 1 (orbs_11_3_psd.drop 20) = true := by rfl

theorem hshard_11_3_psd_s0 :
    checkOrbRows 11 3 (- Int.ofNat 6241589) 21 (orbs_11_3_psd.drop 0) = true := by
  have h10 := h_11_3_psd_s0_c10
  have h9 : checkOrbRows 11 3 (- Int.ofNat 6241589) 3 (orbs_11_3_psd.drop 18) = true :=
    checkOrbRows_add 11 3 (- Int.ofNat 6241589) 2 1 (orbs_11_3_psd.drop 18) h_11_3_psd_s0_c9
      (by simpa [List.drop_drop, Nat.add_comm] using h10)
  have h8 : checkOrbRows 11 3 (- Int.ofNat 6241589) 5 (orbs_11_3_psd.drop 16) = true :=
    checkOrbRows_add 11 3 (- Int.ofNat 6241589) 2 3 (orbs_11_3_psd.drop 16) h_11_3_psd_s0_c8
      (by simpa [List.drop_drop, Nat.add_comm] using h9)
  have h7 : checkOrbRows 11 3 (- Int.ofNat 6241589) 7 (orbs_11_3_psd.drop 14) = true :=
    checkOrbRows_add 11 3 (- Int.ofNat 6241589) 2 5 (orbs_11_3_psd.drop 14) h_11_3_psd_s0_c7
      (by simpa [List.drop_drop, Nat.add_comm] using h8)
  have h6 : checkOrbRows 11 3 (- Int.ofNat 6241589) 9 (orbs_11_3_psd.drop 12) = true :=
    checkOrbRows_add 11 3 (- Int.ofNat 6241589) 2 7 (orbs_11_3_psd.drop 12) h_11_3_psd_s0_c6
      (by simpa [List.drop_drop, Nat.add_comm] using h7)
  have h5 : checkOrbRows 11 3 (- Int.ofNat 6241589) 11 (orbs_11_3_psd.drop 10) = true :=
    checkOrbRows_add 11 3 (- Int.ofNat 6241589) 2 9 (orbs_11_3_psd.drop 10) h_11_3_psd_s0_c5
      (by simpa [List.drop_drop, Nat.add_comm] using h6)
  have h4 : checkOrbRows 11 3 (- Int.ofNat 6241589) 13 (orbs_11_3_psd.drop 8) = true :=
    checkOrbRows_add 11 3 (- Int.ofNat 6241589) 2 11 (orbs_11_3_psd.drop 8) h_11_3_psd_s0_c4
      (by simpa [List.drop_drop, Nat.add_comm] using h5)
  have h3 : checkOrbRows 11 3 (- Int.ofNat 6241589) 15 (orbs_11_3_psd.drop 6) = true :=
    checkOrbRows_add 11 3 (- Int.ofNat 6241589) 2 13 (orbs_11_3_psd.drop 6) h_11_3_psd_s0_c3
      (by simpa [List.drop_drop, Nat.add_comm] using h4)
  have h2 : checkOrbRows 11 3 (- Int.ofNat 6241589) 17 (orbs_11_3_psd.drop 4) = true :=
    checkOrbRows_add 11 3 (- Int.ofNat 6241589) 2 15 (orbs_11_3_psd.drop 4) h_11_3_psd_s0_c2
      (by simpa [List.drop_drop, Nat.add_comm] using h3)
  have h1 : checkOrbRows 11 3 (- Int.ofNat 6241589) 19 (orbs_11_3_psd.drop 2) = true :=
    checkOrbRows_add 11 3 (- Int.ofNat 6241589) 2 17 (orbs_11_3_psd.drop 2) h_11_3_psd_s0_c1
      (by simpa [List.drop_drop, Nat.add_comm] using h2)
  have h0 : checkOrbRows 11 3 (- Int.ofNat 6241589) 21 (orbs_11_3_psd.drop 0) = true :=
    checkOrbRows_add 11 3 (- Int.ofNat 6241589) 2 19 (orbs_11_3_psd.drop 0) h_11_3_psd_s0_c0
      (by simpa [List.drop_drop, Nat.add_comm] using h1)
  exact h0

end DeletionCode.PeelReduce
