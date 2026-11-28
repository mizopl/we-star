/-
  DeletionCode/Cert_11_3_PSD_Shards/P2.lean — Flat-Wave Domination Shard (2 slow `D_2`-orbit step(s), wave 0)
-/
import DeletionCode.PeelReduce
import DeletionCode.Cert_11_3_PSD_Shards.Trees

set_option maxRecDepth 65536
set_option maxHeartbeats 1500000

namespace DeletionCode.PeelReduce

private def wave_11_3_psd_w0_p2_c0 : List (Nat × Nat) := [(286, 62)]
private theorem hwave_11_3_psd_w0_p2_c0 :
    wave_11_3_psd_w0_p2_c0.all (checkDomWaveStep 11 3 initTree_11_3_psd midTree_11_3_psd_0) = true := by rfl
private def wave_11_3_psd_w0_p2_c1 : List (Nat × Nat) := [(302, 62)]
private theorem hwave_11_3_psd_w0_p2_c1 :
    wave_11_3_psd_w0_p2_c1.all (checkDomWaveStep 11 3 initTree_11_3_psd midTree_11_3_psd_0) = true := by rfl

def wave_11_3_psd_w0_p2 : List (Nat × Nat) := wave_11_3_psd_w0_p2_c0 ++ wave_11_3_psd_w0_p2_c1

theorem hwave_11_3_psd_w0_p2 : ∀ st ∈ wave_11_3_psd_w0_p2, checkDomWaveStep 11 3 initTree_11_3_psd midTree_11_3_psd_0 st = true := by
  intro st hst
  simp only [wave_11_3_psd_w0_p2, List.mem_append] at hst
  rcases hst with hst | hcur
  case inr => exact List.all_eq_true.mp hwave_11_3_psd_w0_p2_c1 st hcur
  exact List.all_eq_true.mp hwave_11_3_psd_w0_p2_c0 st hst

end DeletionCode.PeelReduce
