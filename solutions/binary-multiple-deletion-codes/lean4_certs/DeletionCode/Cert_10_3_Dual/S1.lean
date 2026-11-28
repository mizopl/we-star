/-
  DeletionCode/Cert_10_3_Dual/S1.lean — Parallel Clique Verification Shard 2/4 for `(10, 3)`
  Contains 4 cliques (21,732 edges, 4 chunks).
  Zero Mathlib, zero sorryAx, zero native_decide.
-/
import DeletionCode.RecDual

set_option maxRecDepth 65536
set_option maxHeartbeats 1200000

namespace DeletionCode.RecDual

open DeletionCode
open DeletionCode.RecDual

private def clqGrp_10_3_s1_0 : List (Nat × List Nat) :=
  [
    (979808, [141, 147, 149, 153, 163, 165, 166, 169, 170, 178, 198, 201, 209, 217, 233, 282, 293, 297, 298, 305, 308, 332, 337, 338, 340, 341, 354, 357, 390, 394, 396, 397, 398, 402, 403, 404, 410, 411, 419, 425, 427, 428, 429, 435, 437, 454, 460, 461, 467, 561, 563, 564, 569, 586, 588, 594, 595, 596, 597, 598, 601, 612, 613, 617, 619, 621, 625, 626, 627, 649, 657, 658, 660, 665, 666, 667, 669, 675, 676, 679, 681, 682, 683, 685, 691, 708, 710, 713, 715, 716, 717, 725, 729, 741, 785, 786, 788, 789, 793, 802, 804, 805, 806, 809, 817, 818, 819, 820, 821, 825, 843, 844, 845, 846, 851, 853, 854, 857, 869, 870, 917])
  ]
private def clqGrp_10_3_s1_1 : List (Nat × List Nat) :=
  [
    (1909724, [170, 178, 197, 198, 202, 209, 293, 294, 297, 298, 305, 306, 326, 329, 330, 337, 338, 390, 393, 394, 396, 401, 402, 405, 406, 409, 421, 422, 450, 452, 461, 537, 538, 549, 550, 553, 554, 561, 562, 564, 582, 585, 586, 588, 593, 594, 596, 601, 602, 612, 614, 617, 618, 650, 652, 654, 657, 658, 660, 661, 662, 676, 677, 678, 682, 708, 715, 716, 717, 738, 774, 777, 778, 780, 785, 786, 787, 788, 792, 794, 795, 801, 803, 804, 809, 810, 811, 818, 819, 821, 824, 825, 834, 836, 843, 845, 846, 851, 853, 854, 858, 869, 870, 874, 882, 898, 900, 901, 905, 906, 907, 909, 915, 917])
  ]
private def clqGrp_10_3_s1_2 : List (Nat × List Nat) :=
  [
    (630998, [106, 114, 150, 154, 170, 198, 201, 202, 229, 278, 281, 282, 298, 306, 326, 329, 330, 338, 354, 356, 357, 358, 362, 394, 396, 401, 403, 404, 405, 408, 410, 418, 420, 426, 450, 452, 460, 550, 554, 556, 561, 562, 564, 585, 586, 588, 596, 597, 610, 613, 618, 649, 658, 659, 660, 661, 664, 665, 666, 674, 677, 678, 681, 682, 690, 708, 714, 716, 717, 718, 725, 730, 741, 742, 746, 778, 786, 790, 792, 794, 804, 805, 806, 809, 810, 812, 814, 818, 819, 821, 822, 825, 834, 836, 837, 843, 846, 853, 854, 857, 858, 869, 898, 900, 902, 909, 917, 922, 924])
  ]
private def clqGrp_10_3_s1_3 : List (Nat × List Nat) :=
  [
    (762821, [126, 184, 190, 220, 228, 236, 238, 246, 252, 312, 364, 366, 428, 430, 438, 440, 441, 444, 462, 470, 474, 476, 500, 504, 604, 620, 622, 630, 632, 634, 636, 668, 686, 694, 698, 700, 718, 726, 730, 732, 754, 760, 796, 798, 814, 822, 826, 828, 846, 854, 858, 860, 870, 874, 876, 882, 884, 888, 910, 918, 924, 980, 984, 996, 1000, 1008])
  ]

def shard_10_3_s1 : List (Nat × List Nat) :=
  clqGrp_10_3_s1_0 ++ clqGrp_10_3_s1_1 ++ clqGrp_10_3_s1_2 ++ clqGrp_10_3_s1_3

private theorem hclq_10_3_s1_0 : clqGrp_10_3_s1_0.all (fun c => checkClqRec 10 3 c.2) = true := by rfl
private theorem hclq_10_3_s1_1 : clqGrp_10_3_s1_1.all (fun c => checkClqRec 10 3 c.2) = true := by rfl
private theorem hclq_10_3_s1_2 : clqGrp_10_3_s1_2.all (fun c => checkClqRec 10 3 c.2) = true := by rfl
private theorem hclq_10_3_s1_3 : clqGrp_10_3_s1_3.all (fun c => checkClqRec 10 3 c.2) = true := by rfl

theorem hshard_10_3_s1 : ∀ c ∈ shard_10_3_s1, checkClqRec 10 3 c.2 = true := by
  intro c hc
  simp only [shard_10_3_s1, List.mem_append] at hc
  rcases hc with hc | h3
  case inr => exact List.all_eq_true.mp hclq_10_3_s1_3 c h3
  rcases hc with hc | h2
  case inr => exact List.all_eq_true.mp hclq_10_3_s1_2 c h2
  rcases hc with hc | h1
  case inr => exact List.all_eq_true.mp hclq_10_3_s1_1 c h1
  exact List.all_eq_true.mp hclq_10_3_s1_0 c hc

end DeletionCode.RecDual
