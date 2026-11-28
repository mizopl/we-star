/-
  DeletionCode/Cert_11_3_PSD_Shards/S1.lean — Pair-Check Shard 1/8 for `(11, 3)`
  Rows 21..42 (6369 unordered `D_2` orbit pairs across 10 chunks)
-/
import DeletionCode.SchrijverPSD
import DeletionCode.Cert_11_3_PSD_Shards.Data

set_option maxRecDepth 65536
set_option maxHeartbeats 4000000

namespace DeletionCode.PeelReduce

open DeletionCode.SchrijverPSD

-- Chunk 0: rows 21..22 (599 orbit pairs)
private theorem h_11_3_psd_s1_c0 :
    checkOrbRows 11 3 (- Int.ofNat 6241589) 2 (orbs_11_3_psd.drop 21) = true := by rfl
-- Chunk 1: rows 23..24 (595 orbit pairs)
private theorem h_11_3_psd_s1_c1 :
    checkOrbRows 11 3 (- Int.ofNat 6241589) 2 (orbs_11_3_psd.drop 23) = true := by rfl
-- Chunk 2: rows 25..26 (591 orbit pairs)
private theorem h_11_3_psd_s1_c2 :
    checkOrbRows 11 3 (- Int.ofNat 6241589) 2 (orbs_11_3_psd.drop 25) = true := by rfl
-- Chunk 3: rows 27..28 (587 orbit pairs)
private theorem h_11_3_psd_s1_c3 :
    checkOrbRows 11 3 (- Int.ofNat 6241589) 2 (orbs_11_3_psd.drop 27) = true := by rfl
-- Chunk 4: rows 29..30 (583 orbit pairs)
private theorem h_11_3_psd_s1_c4 :
    checkOrbRows 11 3 (- Int.ofNat 6241589) 2 (orbs_11_3_psd.drop 29) = true := by rfl
-- Chunk 5: rows 31..32 (579 orbit pairs)
private theorem h_11_3_psd_s1_c5 :
    checkOrbRows 11 3 (- Int.ofNat 6241589) 2 (orbs_11_3_psd.drop 31) = true := by rfl
-- Chunk 6: rows 33..34 (575 orbit pairs)
private theorem h_11_3_psd_s1_c6 :
    checkOrbRows 11 3 (- Int.ofNat 6241589) 2 (orbs_11_3_psd.drop 33) = true := by rfl
-- Chunk 7: rows 35..36 (571 orbit pairs)
private theorem h_11_3_psd_s1_c7 :
    checkOrbRows 11 3 (- Int.ofNat 6241589) 2 (orbs_11_3_psd.drop 35) = true := by rfl
-- Chunk 8: rows 37..39 (849 orbit pairs)
private theorem h_11_3_psd_s1_c8 :
    checkOrbRows 11 3 (- Int.ofNat 6241589) 3 (orbs_11_3_psd.drop 37) = true := by rfl
-- Chunk 9: rows 40..42 (840 orbit pairs)
private theorem h_11_3_psd_s1_c9 :
    checkOrbRows 11 3 (- Int.ofNat 6241589) 3 (orbs_11_3_psd.drop 40) = true := by rfl

theorem hshard_11_3_psd_s1 :
    checkOrbRows 11 3 (- Int.ofNat 6241589) 22 (orbs_11_3_psd.drop 21) = true := by
  have h9 := h_11_3_psd_s1_c9
  have h8 : checkOrbRows 11 3 (- Int.ofNat 6241589) 6 (orbs_11_3_psd.drop 37) = true :=
    checkOrbRows_add 11 3 (- Int.ofNat 6241589) 3 3 (orbs_11_3_psd.drop 37) h_11_3_psd_s1_c8
      (by simpa [List.drop_drop, Nat.add_comm] using h9)
  have h7 : checkOrbRows 11 3 (- Int.ofNat 6241589) 8 (orbs_11_3_psd.drop 35) = true :=
    checkOrbRows_add 11 3 (- Int.ofNat 6241589) 2 6 (orbs_11_3_psd.drop 35) h_11_3_psd_s1_c7
      (by simpa [List.drop_drop, Nat.add_comm] using h8)
  have h6 : checkOrbRows 11 3 (- Int.ofNat 6241589) 10 (orbs_11_3_psd.drop 33) = true :=
    checkOrbRows_add 11 3 (- Int.ofNat 6241589) 2 8 (orbs_11_3_psd.drop 33) h_11_3_psd_s1_c6
      (by simpa [List.drop_drop, Nat.add_comm] using h7)
  have h5 : checkOrbRows 11 3 (- Int.ofNat 6241589) 12 (orbs_11_3_psd.drop 31) = true :=
    checkOrbRows_add 11 3 (- Int.ofNat 6241589) 2 10 (orbs_11_3_psd.drop 31) h_11_3_psd_s1_c5
      (by simpa [List.drop_drop, Nat.add_comm] using h6)
  have h4 : checkOrbRows 11 3 (- Int.ofNat 6241589) 14 (orbs_11_3_psd.drop 29) = true :=
    checkOrbRows_add 11 3 (- Int.ofNat 6241589) 2 12 (orbs_11_3_psd.drop 29) h_11_3_psd_s1_c4
      (by simpa [List.drop_drop, Nat.add_comm] using h5)
  have h3 : checkOrbRows 11 3 (- Int.ofNat 6241589) 16 (orbs_11_3_psd.drop 27) = true :=
    checkOrbRows_add 11 3 (- Int.ofNat 6241589) 2 14 (orbs_11_3_psd.drop 27) h_11_3_psd_s1_c3
      (by simpa [List.drop_drop, Nat.add_comm] using h4)
  have h2 : checkOrbRows 11 3 (- Int.ofNat 6241589) 18 (orbs_11_3_psd.drop 25) = true :=
    checkOrbRows_add 11 3 (- Int.ofNat 6241589) 2 16 (orbs_11_3_psd.drop 25) h_11_3_psd_s1_c2
      (by simpa [List.drop_drop, Nat.add_comm] using h3)
  have h1 : checkOrbRows 11 3 (- Int.ofNat 6241589) 20 (orbs_11_3_psd.drop 23) = true :=
    checkOrbRows_add 11 3 (- Int.ofNat 6241589) 2 18 (orbs_11_3_psd.drop 23) h_11_3_psd_s1_c1
      (by simpa [List.drop_drop, Nat.add_comm] using h2)
  have h0 : checkOrbRows 11 3 (- Int.ofNat 6241589) 22 (orbs_11_3_psd.drop 21) = true :=
    checkOrbRows_add 11 3 (- Int.ofNat 6241589) 2 20 (orbs_11_3_psd.drop 21) h_11_3_psd_s1_c0
      (by simpa [List.drop_drop, Nat.add_comm] using h1)
  exact h0

end DeletionCode.PeelReduce
