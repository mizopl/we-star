/-
  DeletionCode/Cert_10_3_Dual/S0.lean — Parallel Clique Verification Shard 1/4 for `(10, 3)`
  Contains 3 cliques (20,178 edges, 3 chunks).
  Zero Mathlib, zero sorryAx, zero native_decide.
-/
import DeletionCode.RecDual

set_option maxRecDepth 65536
set_option maxHeartbeats 1200000

namespace DeletionCode.RecDual

open DeletionCode
open DeletionCode.RecDual

private def clqGrp_10_3_s0_0 : List (Nat × List Nat) :=
  [
    (1122295, [101, 102, 141, 147, 154, 163, 165, 166, 169, 170, 172, 177, 179, 182, 198, 202, 203, 205, 212, 213, 230, 275, 281, 291, 294, 297, 298, 300, 305, 306, 307, 309, 326, 330, 332, 333, 338, 339, 340, 341, 342, 356, 357, 358, 394, 396, 402, 404, 406, 408, 409, 410, 412, 413, 422, 425, 426, 427, 429, 459, 461, 550, 554, 561, 562, 566, 585, 586, 587, 588, 590, 594, 596, 597, 598, 601, 602, 610, 611, 613, 614, 615, 617, 619, 621, 622, 627, 630, 660, 662, 664, 665, 666, 667, 675, 678, 681, 682, 683, 684, 685, 686, 690, 691, 693, 694, 708, 714, 716, 717, 718, 723, 725, 726, 729, 742, 786, 788, 789, 793, 802, 804, 810, 811, 813, 818, 819, 820, 821, 822, 825, 843, 844, 851, 853, 854, 857, 869, 921])
  ]
private def clqGrp_10_3_s0_1 : List (Nat × List Nat) :=
  [
    (601016, [116, 154, 156, 169, 170, 172, 177, 178, 180, 189, 201, 202, 204, 209, 211, 212, 214, 219, 228, 233, 234, 235, 237, 238, 245, 282, 298, 301, 306, 308, 310, 317, 330, 332, 338, 340, 341, 345, 346, 348, 354, 356, 357, 358, 361, 362, 363, 365, 366, 374, 405, 410, 411, 413, 421, 427, 428, 429, 430, 434, 435, 437, 438, 440, 442, 444, 459, 461, 462, 467, 469, 470, 474, 476, 486, 498, 500, 600, 602, 618, 621, 630, 666, 669, 682, 685, 693, 694, 717, 722, 725, 726, 729, 730, 732, 741, 742, 754, 756, 812, 821, 822, 845, 854, 858, 860, 873, 876, 884, 918, 921, 922])
  ]
private def clqGrp_10_3_s0_2 : List (Nat × List Nat) :=
  [
    (395356, [102, 108, 118, 150, 166, 170, 178, 180, 198, 204, 205, 210, 214, 281, 294, 300, 306, 307, 308, 330, 332, 334, 358, 396, 410, 412, 413, 427, 458, 462, 554, 556, 562, 564, 565, 570, 573, 588, 589, 595, 596, 603, 604, 610, 611, 613, 615, 619, 621, 627, 629, 654, 658, 660, 665, 666, 682, 683, 684, 686, 690, 691, 693, 697, 700, 714, 715, 716, 717, 718, 723, 730, 732, 742, 790, 792, 793, 796, 810, 811, 813, 814, 818, 821, 822, 825, 828, 845, 846, 854, 858, 910, 922, 924])
  ]

def shard_10_3_s0 : List (Nat × List Nat) :=
  clqGrp_10_3_s0_0 ++ clqGrp_10_3_s0_1 ++ clqGrp_10_3_s0_2

private theorem hclq_10_3_s0_0 : clqGrp_10_3_s0_0.all (fun c => checkClqRec 10 3 c.2) = true := by rfl
private theorem hclq_10_3_s0_1 : clqGrp_10_3_s0_1.all (fun c => checkClqRec 10 3 c.2) = true := by rfl
private theorem hclq_10_3_s0_2 : clqGrp_10_3_s0_2.all (fun c => checkClqRec 10 3 c.2) = true := by rfl

theorem hshard_10_3_s0 : ∀ c ∈ shard_10_3_s0, checkClqRec 10 3 c.2 = true := by
  intro c hc
  simp only [shard_10_3_s0, List.mem_append] at hc
  rcases hc with hc | h2
  case inr => exact List.all_eq_true.mp hclq_10_3_s0_2 c h2
  rcases hc with hc | h1
  case inr => exact List.all_eq_true.mp hclq_10_3_s0_1 c h1
  exact List.all_eq_true.mp hclq_10_3_s0_0 c hc

end DeletionCode.RecDual
