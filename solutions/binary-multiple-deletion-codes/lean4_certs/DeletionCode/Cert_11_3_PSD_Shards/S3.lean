/-
  DeletionCode/Cert_11_3_PSD_Shards/S3.lean — Pair-Check Shard 3/8 for `(11, 3)`
  Rows 67..93 (6507 unordered `D_2` orbit pairs across 9 chunks)
-/
import DeletionCode.SchrijverPSD
import DeletionCode.Cert_11_3_PSD_Shards.Data

set_option maxRecDepth 65536
set_option maxHeartbeats 4000000

namespace DeletionCode.PeelReduce

open DeletionCode.SchrijverPSD

-- Chunk 0: rows 67..69 (759 orbit pairs)
private theorem h_11_3_psd_s3_c0 :
    checkOrbRows 11 3 (- Int.ofNat 6241589) 3 (orbs_11_3_psd.drop 67) = true := by rfl
-- Chunk 1: rows 70..72 (750 orbit pairs)
private theorem h_11_3_psd_s3_c1 :
    checkOrbRows 11 3 (- Int.ofNat 6241589) 3 (orbs_11_3_psd.drop 70) = true := by rfl
-- Chunk 2: rows 73..75 (741 orbit pairs)
private theorem h_11_3_psd_s3_c2 :
    checkOrbRows 11 3 (- Int.ofNat 6241589) 3 (orbs_11_3_psd.drop 73) = true := by rfl
-- Chunk 3: rows 76..78 (732 orbit pairs)
private theorem h_11_3_psd_s3_c3 :
    checkOrbRows 11 3 (- Int.ofNat 6241589) 3 (orbs_11_3_psd.drop 76) = true := by rfl
-- Chunk 4: rows 79..81 (723 orbit pairs)
private theorem h_11_3_psd_s3_c4 :
    checkOrbRows 11 3 (- Int.ofNat 6241589) 3 (orbs_11_3_psd.drop 79) = true := by rfl
-- Chunk 5: rows 82..84 (714 orbit pairs)
private theorem h_11_3_psd_s3_c5 :
    checkOrbRows 11 3 (- Int.ofNat 6241589) 3 (orbs_11_3_psd.drop 82) = true := by rfl
-- Chunk 6: rows 85..87 (705 orbit pairs)
private theorem h_11_3_psd_s3_c6 :
    checkOrbRows 11 3 (- Int.ofNat 6241589) 3 (orbs_11_3_psd.drop 85) = true := by rfl
-- Chunk 7: rows 88..90 (696 orbit pairs)
private theorem h_11_3_psd_s3_c7 :
    checkOrbRows 11 3 (- Int.ofNat 6241589) 3 (orbs_11_3_psd.drop 88) = true := by rfl
-- Chunk 8: rows 91..93 (687 orbit pairs)
private theorem h_11_3_psd_s3_c8 :
    checkOrbRows 11 3 (- Int.ofNat 6241589) 3 (orbs_11_3_psd.drop 91) = true := by rfl

theorem hshard_11_3_psd_s3 :
    checkOrbRows 11 3 (- Int.ofNat 6241589) 27 (orbs_11_3_psd.drop 67) = true := by
  have h8 := h_11_3_psd_s3_c8
  have h7 : checkOrbRows 11 3 (- Int.ofNat 6241589) 6 (orbs_11_3_psd.drop 88) = true :=
    checkOrbRows_add 11 3 (- Int.ofNat 6241589) 3 3 (orbs_11_3_psd.drop 88) h_11_3_psd_s3_c7
      (by simpa [List.drop_drop, Nat.add_comm] using h8)
  have h6 : checkOrbRows 11 3 (- Int.ofNat 6241589) 9 (orbs_11_3_psd.drop 85) = true :=
    checkOrbRows_add 11 3 (- Int.ofNat 6241589) 3 6 (orbs_11_3_psd.drop 85) h_11_3_psd_s3_c6
      (by simpa [List.drop_drop, Nat.add_comm] using h7)
  have h5 : checkOrbRows 11 3 (- Int.ofNat 6241589) 12 (orbs_11_3_psd.drop 82) = true :=
    checkOrbRows_add 11 3 (- Int.ofNat 6241589) 3 9 (orbs_11_3_psd.drop 82) h_11_3_psd_s3_c5
      (by simpa [List.drop_drop, Nat.add_comm] using h6)
  have h4 : checkOrbRows 11 3 (- Int.ofNat 6241589) 15 (orbs_11_3_psd.drop 79) = true :=
    checkOrbRows_add 11 3 (- Int.ofNat 6241589) 3 12 (orbs_11_3_psd.drop 79) h_11_3_psd_s3_c4
      (by simpa [List.drop_drop, Nat.add_comm] using h5)
  have h3 : checkOrbRows 11 3 (- Int.ofNat 6241589) 18 (orbs_11_3_psd.drop 76) = true :=
    checkOrbRows_add 11 3 (- Int.ofNat 6241589) 3 15 (orbs_11_3_psd.drop 76) h_11_3_psd_s3_c3
      (by simpa [List.drop_drop, Nat.add_comm] using h4)
  have h2 : checkOrbRows 11 3 (- Int.ofNat 6241589) 21 (orbs_11_3_psd.drop 73) = true :=
    checkOrbRows_add 11 3 (- Int.ofNat 6241589) 3 18 (orbs_11_3_psd.drop 73) h_11_3_psd_s3_c2
      (by simpa [List.drop_drop, Nat.add_comm] using h3)
  have h1 : checkOrbRows 11 3 (- Int.ofNat 6241589) 24 (orbs_11_3_psd.drop 70) = true :=
    checkOrbRows_add 11 3 (- Int.ofNat 6241589) 3 21 (orbs_11_3_psd.drop 70) h_11_3_psd_s3_c1
      (by simpa [List.drop_drop, Nat.add_comm] using h2)
  have h0 : checkOrbRows 11 3 (- Int.ofNat 6241589) 27 (orbs_11_3_psd.drop 67) = true :=
    checkOrbRows_add 11 3 (- Int.ofNat 6241589) 3 24 (orbs_11_3_psd.drop 67) h_11_3_psd_s3_c0
      (by simpa [List.drop_drop, Nat.add_comm] using h1)
  exact h0

end DeletionCode.PeelReduce
