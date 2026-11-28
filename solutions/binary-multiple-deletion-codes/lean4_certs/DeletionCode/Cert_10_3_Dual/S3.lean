/-
  DeletionCode/Cert_10_3_Dual/S3.lean — Parallel Clique Verification Shard 4/4 for `(10, 3)`
  Contains 4 cliques (21,616 edges, 4 chunks).
  Zero Mathlib, zero sorryAx, zero native_decide.
-/
import DeletionCode.RecDual

set_option maxRecDepth 65536
set_option maxHeartbeats 1200000

namespace DeletionCode.RecDual

open DeletionCode
open DeletionCode.RecDual

private def clqGrp_10_3_s3_0 : List (Nat × List Nat) :=
  [
    (1363922, [106, 170, 177, 201, 210, 282, 294, 297, 298, 305, 326, 329, 330, 338, 354, 357, 358, 361, 362, 393, 394, 401, 402, 403, 404, 406, 408, 409, 410, 420, 421, 422, 425, 426, 450, 452, 461, 550, 553, 554, 561, 562, 564, 582, 585, 586, 588, 593, 594, 596, 597, 598, 601, 602, 612, 613, 614, 617, 650, 652, 657, 658, 659, 660, 661, 662, 664, 665, 666, 676, 677, 681, 682, 690, 706, 708, 714, 718, 723, 725, 726, 729, 730, 738, 741, 786, 788, 792, 794, 795, 797, 804, 805, 806, 809, 811, 813, 822, 826, 836, 837, 843, 851, 853, 854, 857, 858, 870, 873, 874, 882, 898, 900, 905, 906, 917, 921, 922, 924])
  ]
private def clqGrp_10_3_s3_1 : List (Nat × List Nat) :=
  [
    (400571, [102, 108, 156, 166, 170, 172, 178, 180, 184, 187, 198, 202, 205, 206, 210, 211, 212, 213, 216, 218, 228, 229, 237, 238, 294, 298, 300, 307, 308, 309, 330, 332, 333, 338, 339, 340, 341, 344, 345, 346, 347, 354, 355, 357, 358, 359, 362, 363, 364, 365, 366, 374, 410, 414, 419, 427, 429, 430, 435, 437, 438, 442, 459, 460, 461, 462, 467, 469, 470, 473, 474, 476, 486, 601, 615, 617, 618, 619, 621, 622, 627, 666, 668, 682, 684, 685, 686, 690, 691, 693, 694, 696, 714, 715, 716, 718, 723, 725, 726, 729, 730, 732, 790, 794, 810, 811, 812, 813, 814, 822, 825, 846, 854, 857, 858, 860, 874])
  ]
private def clqGrp_10_3_s3_2 : List (Nat × List Nat) :=
  [
    (328649, [149, 153, 165, 201, 210, 211, 213, 267, 277, 281, 291, 293, 294, 297, 298, 300, 306, 307, 308, 309, 323, 326, 329, 330, 332, 333, 337, 338, 339, 340, 341, 357, 394, 402, 405, 459, 547, 553, 554, 561, 562, 563, 565, 583, 585, 586, 588, 593, 594, 595, 597, 610, 613, 649, 658, 659, 660, 661, 664, 665, 666, 668, 674, 676, 677, 678, 681, 682, 683, 684, 685, 689, 690, 691, 693, 709, 714, 715, 717, 723, 725, 739, 778, 785, 786, 789, 794, 802, 805, 809, 810, 812, 813, 817, 818, 821, 834, 843, 845, 846, 853, 869, 905])
  ]
private def clqGrp_10_3_s3_3 : List (Nat × List Nat) :=
  [
    (547492, [126, 184, 190, 220, 228, 236, 238, 246, 252, 312, 318, 348, 364, 366, 370, 374, 380, 428, 438, 440, 441, 442, 444, 460, 462, 474, 476, 498, 500, 504, 574, 604, 622, 630, 632, 636, 670, 686, 694, 700, 718, 726, 730, 732, 742, 746, 748, 754, 756, 760, 796, 814, 822, 826, 828, 846, 854, 858, 870, 874, 876, 882, 884, 888, 910, 924, 952, 980, 984, 996, 1000, 1008])
  ]

def shard_10_3_s3 : List (Nat × List Nat) :=
  clqGrp_10_3_s3_0 ++ clqGrp_10_3_s3_1 ++ clqGrp_10_3_s3_2 ++ clqGrp_10_3_s3_3

private theorem hclq_10_3_s3_0 : clqGrp_10_3_s3_0.all (fun c => checkClqRec 10 3 c.2) = true := by rfl
private theorem hclq_10_3_s3_1 : clqGrp_10_3_s3_1.all (fun c => checkClqRec 10 3 c.2) = true := by rfl
private theorem hclq_10_3_s3_2 : clqGrp_10_3_s3_2.all (fun c => checkClqRec 10 3 c.2) = true := by rfl
private theorem hclq_10_3_s3_3 : clqGrp_10_3_s3_3.all (fun c => checkClqRec 10 3 c.2) = true := by rfl

theorem hshard_10_3_s3 : ∀ c ∈ shard_10_3_s3, checkClqRec 10 3 c.2 = true := by
  intro c hc
  simp only [shard_10_3_s3, List.mem_append] at hc
  rcases hc with hc | h3
  case inr => exact List.all_eq_true.mp hclq_10_3_s3_3 c h3
  rcases hc with hc | h2
  case inr => exact List.all_eq_true.mp hclq_10_3_s3_2 c h2
  rcases hc with hc | h1
  case inr => exact List.all_eq_true.mp hclq_10_3_s3_1 c h1
  exact List.all_eq_true.mp hclq_10_3_s3_0 c hc

end DeletionCode.RecDual
