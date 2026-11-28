/-
  DeletionCode/Cert_11_3_PSD_Shards/P5.lean — Flat-Wave Domination Shard (1 slow `D_2`-orbit step(s), wave 1)
-/
import DeletionCode.PeelReduce
import DeletionCode.Cert_11_3_PSD_Shards.Trees

set_option maxRecDepth 65536
set_option maxHeartbeats 1500000

namespace DeletionCode.PeelReduce

private def wave_11_3_psd_w1_p1_c0 : List (Nat × Nat) := [(666, 682)]
private theorem hwave_11_3_psd_w1_p1_c0 :
    wave_11_3_psd_w1_p1_c0.all (checkDomWaveStep 11 3 midTree_11_3_psd_0 coreTree_11_3_psd) = true := by rfl

def wave_11_3_psd_w1_p1 : List (Nat × Nat) := wave_11_3_psd_w1_p1_c0

theorem hwave_11_3_psd_w1_p1 : ∀ st ∈ wave_11_3_psd_w1_p1, checkDomWaveStep 11 3 midTree_11_3_psd_0 coreTree_11_3_psd st = true :=
  fun st hst => List.all_eq_true.mp hwave_11_3_psd_w1_p1_c0 st hst

end DeletionCode.PeelReduce
