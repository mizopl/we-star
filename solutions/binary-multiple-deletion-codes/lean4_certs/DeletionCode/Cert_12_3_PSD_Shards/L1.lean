/-
  DeletionCode/Cert_12_3_PSD_Shards/L1.lean — FastOrb Link Shard 1/4 (orbits 200..399, chunked 25/thm)
-/
import DeletionCode.FastSchrijver
import DeletionCode.Cert_12_3_PSD_Shards.Data
import DeletionCode.Cert_12_3_PSD_Shards.KData

set_option maxRecDepth 65536
set_option maxHeartbeats 4000000

namespace DeletionCode.FastSchrijver

open DeletionCode.PeelReduce

private theorem hl_12_3_psd_l1_c0 :
    checkFastLinkRows 12 3 512 16777216 512 25 (orbs_12_3_psd.drop 200) (korbs_12_3_psd.drop 200) = true := by rfl
private theorem hl_12_3_psd_l1_c1 :
    checkFastLinkRows 12 3 512 16777216 512 25 (orbs_12_3_psd.drop 225) (korbs_12_3_psd.drop 225) = true := by rfl
private theorem hl_12_3_psd_l1_c2 :
    checkFastLinkRows 12 3 512 16777216 512 25 (orbs_12_3_psd.drop 250) (korbs_12_3_psd.drop 250) = true := by rfl
private theorem hl_12_3_psd_l1_c3 :
    checkFastLinkRows 12 3 512 16777216 512 25 (orbs_12_3_psd.drop 275) (korbs_12_3_psd.drop 275) = true := by rfl
private theorem hl_12_3_psd_l1_c4 :
    checkFastLinkRows 12 3 512 16777216 512 25 (orbs_12_3_psd.drop 300) (korbs_12_3_psd.drop 300) = true := by rfl
private theorem hl_12_3_psd_l1_c5 :
    checkFastLinkRows 12 3 512 16777216 512 25 (orbs_12_3_psd.drop 325) (korbs_12_3_psd.drop 325) = true := by rfl
private theorem hl_12_3_psd_l1_c6 :
    checkFastLinkRows 12 3 512 16777216 512 25 (orbs_12_3_psd.drop 350) (korbs_12_3_psd.drop 350) = true := by rfl
private theorem hl_12_3_psd_l1_c7 :
    checkFastLinkRows 12 3 512 16777216 512 25 (orbs_12_3_psd.drop 375) (korbs_12_3_psd.drop 375) = true := by rfl

theorem hlink_12_3_psd_l1 :
    checkFastLinkRows 12 3 512 16777216 512 200 (orbs_12_3_psd.drop 200) (korbs_12_3_psd.drop 200) = true := by
  have h7 := hl_12_3_psd_l1_c7
  have h6 : checkFastLinkRows 12 3 512 16777216 512 50 (orbs_12_3_psd.drop 350) (korbs_12_3_psd.drop 350) = true :=
    checkFastLinkRows_add 12 3 512 16777216 512 25 25 (orbs_12_3_psd.drop 350) (korbs_12_3_psd.drop 350) hl_12_3_psd_l1_c6
      (by simpa [List.drop_drop, Nat.add_comm] using h7)
  have h5 : checkFastLinkRows 12 3 512 16777216 512 75 (orbs_12_3_psd.drop 325) (korbs_12_3_psd.drop 325) = true :=
    checkFastLinkRows_add 12 3 512 16777216 512 25 50 (orbs_12_3_psd.drop 325) (korbs_12_3_psd.drop 325) hl_12_3_psd_l1_c5
      (by simpa [List.drop_drop, Nat.add_comm] using h6)
  have h4 : checkFastLinkRows 12 3 512 16777216 512 100 (orbs_12_3_psd.drop 300) (korbs_12_3_psd.drop 300) = true :=
    checkFastLinkRows_add 12 3 512 16777216 512 25 75 (orbs_12_3_psd.drop 300) (korbs_12_3_psd.drop 300) hl_12_3_psd_l1_c4
      (by simpa [List.drop_drop, Nat.add_comm] using h5)
  have h3 : checkFastLinkRows 12 3 512 16777216 512 125 (orbs_12_3_psd.drop 275) (korbs_12_3_psd.drop 275) = true :=
    checkFastLinkRows_add 12 3 512 16777216 512 25 100 (orbs_12_3_psd.drop 275) (korbs_12_3_psd.drop 275) hl_12_3_psd_l1_c3
      (by simpa [List.drop_drop, Nat.add_comm] using h4)
  have h2 : checkFastLinkRows 12 3 512 16777216 512 150 (orbs_12_3_psd.drop 250) (korbs_12_3_psd.drop 250) = true :=
    checkFastLinkRows_add 12 3 512 16777216 512 25 125 (orbs_12_3_psd.drop 250) (korbs_12_3_psd.drop 250) hl_12_3_psd_l1_c2
      (by simpa [List.drop_drop, Nat.add_comm] using h3)
  have h1 : checkFastLinkRows 12 3 512 16777216 512 175 (orbs_12_3_psd.drop 225) (korbs_12_3_psd.drop 225) = true :=
    checkFastLinkRows_add 12 3 512 16777216 512 25 150 (orbs_12_3_psd.drop 225) (korbs_12_3_psd.drop 225) hl_12_3_psd_l1_c1
      (by simpa [List.drop_drop, Nat.add_comm] using h2)
  have h0 : checkFastLinkRows 12 3 512 16777216 512 200 (orbs_12_3_psd.drop 200) (korbs_12_3_psd.drop 200) = true :=
    checkFastLinkRows_add 12 3 512 16777216 512 25 175 (orbs_12_3_psd.drop 200) (korbs_12_3_psd.drop 200) hl_12_3_psd_l1_c0
      (by simpa [List.drop_drop, Nat.add_comm] using h1)
  exact h0

end DeletionCode.FastSchrijver
