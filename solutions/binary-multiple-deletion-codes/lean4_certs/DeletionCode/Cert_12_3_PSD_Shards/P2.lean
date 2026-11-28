/-
  DeletionCode/Cert_12_3_PSD_Shards/P2.lean — Flat-Wave Domination Shard (26 fast `D_2`-orbit step(s), wave 0)
-/
import DeletionCode.PeelReduce
import DeletionCode.Cert_12_3_PSD_Shards.Trees

set_option maxRecDepth 65536
set_option maxHeartbeats 1500000

namespace DeletionCode.PeelReduce

private def wave_12_3_psd_w0_p2_c0 : List (Nat × Nat) := [(758, 502), (761, 505), (762, 506), (764, 508), (765, 509), (766, 510), (893, 509), (894, 510), (1018, 1020), (1037, 1031), (1045, 1031), (1046, 1038), (1069, 1053), (1070, 1054), (1117, 1085), (1118, 1086), (1214, 1150), (1278, 510), (1285, 1283), (1406, 510)]
private theorem hwave_12_3_psd_w0_p2_c0 :
    wave_12_3_psd_w0_p2_c0.all (checkDomWaveStep 12 3 initTree_12_3_psd coreTree_12_3_psd) = true := by rfl
private def wave_12_3_psd_w0_p2_c1 : List (Nat × Nat) := [(1526, 1014), (1529, 1017), (1665, 1793), (1857, 1921), (1953, 1985), (1530, 1020)]
private theorem hwave_12_3_psd_w0_p2_c1 :
    wave_12_3_psd_w0_p2_c1.all (checkDomWaveStep 12 3 initTree_12_3_psd coreTree_12_3_psd) = true := by rfl

def wave_12_3_psd_w0_p2 : List (Nat × Nat) := wave_12_3_psd_w0_p2_c0 ++ wave_12_3_psd_w0_p2_c1

theorem hwave_12_3_psd_w0_p2 : ∀ st ∈ wave_12_3_psd_w0_p2, checkDomWaveStep 12 3 initTree_12_3_psd coreTree_12_3_psd st = true := by
  intro st hst
  simp only [wave_12_3_psd_w0_p2, List.mem_append] at hst
  rcases hst with hst | hcur
  case inr => exact List.all_eq_true.mp hwave_12_3_psd_w0_p2_c1 st hcur
  exact List.all_eq_true.mp hwave_12_3_psd_w0_p2_c0 st hst

end DeletionCode.PeelReduce
