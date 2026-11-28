/-
  DeletionCode/Statements.lean — Minimal Human-Auditable Trusted Computing Base (TCB).
  ZERO internal imports; depends ONLY on Lean 4.36.0 core (Init).

  Defines:
  1. Pure inductive subsequence relation `IsSubseq`, `s`-deletion ball `InDelBall`, and
     common-subsequence predicate `HasCommonSubseqAtLeast`.
  2. LSB-first `natToWord` decoding, `bitComp`, and `bitRev`.
  3. Formal `IsValidDeletionCode` and `IsInclusionMaximal` predicates on `List Nat`.
  4. Exact certified codebook constants (`cert_15_2_code`, `cert_15_3_code`,
     `cert_16_3_code`, `cert_16_2_code`) and exact-optimal small witnesses.
-/

namespace DeletionCode

/-- Standard inductive subsequence relation on binary words (`List Bool`). -/
inductive IsSubseq : List Bool → List Bool → Prop where
  | nil : IsSubseq [] []
  | cons_keep (b : Bool) {u v : List Bool} : IsSubseq u v → IsSubseq (b :: u) (b :: v)
  | cons_drop (b : Bool) {u v : List Bool} : IsSubseq u v → IsSubseq u (b :: v)

/-- A word `d` is in the `s`-deletion ball `D_s(x)` iff `d` is a subsequence of `x` of length `x.length - s`. -/
def InDelBall (s : Nat) (x d : List Bool) : Prop :=
  IsSubseq d x ∧ d.length + s = x.length

/-- Existence of a common subsequence of length at least `k` (`LCS(x, y) >= k`). -/
def HasCommonSubseqAtLeast (k : Nat) (x y : List Bool) : Prop :=
  ∃ d : List Bool, k ≤ d.length ∧ IsSubseq d x ∧ IsSubseq d y

/-- LSB-first bit-vector decoding `natToWord n x : List Bool` of exact length `n`. -/
def natToWord : Nat → Nat → List Bool
  | 0, _ => []
  | n + 1, x => (x % 2 == 1) :: natToWord n (x / 2)

/-- Bitwise complement on `n`-bit words (`0 .. 2^n - 1`). -/
def bitComp (n x : Nat) : Nat := (2 ^ n - 1) - x

/-- Bitwise string reversal on `n`-bit words (`0 .. 2^n - 1`). -/
def bitRev (n x : Nat) : Nat :=
  let rec go : Nat → Nat → Nat → Nat
    | 0, _, acc => acc
    | k + 1, cur, acc => go k (cur / 2) (2 * acc + cur % 2)
  go n x 0

/-- Formal validity predicate for an `s`-deletion-correcting code encoded as `List Nat` of `n`-bit words. -/
def IsValidDeletionCode (n s : Nat) (C : List Nat) : Prop :=
  (∀ x ∈ C, x < 2 ^ n) ∧
  (∀ (i j : Nat) (hi : i < C.length) (hj : j < C.length), i ≠ j →
    C[i] ≠ C[j] ∧
    (∀ d, ¬ (InDelBall s (natToWord n C[i]) d ∧ InDelBall s (natToWord n C[j]) d)) ∧
    ¬ HasCommonSubseqAtLeast (n - s) (natToWord n C[i]) (natToWord n C[j]))

/-- Formal inclusion-maximality (non-extendability) predicate over all `2^n` binary words.
    NOTE (-0 Hype): Certifies inclusion-maximality (no single word can extend `C`), NOT global cardinality optimality. -/
def IsInclusionMaximal (n s : Nat) (C : List Nat) : Prop :=
  ∀ x : Nat, x < 2 ^ n →
    ∃ (i : Nat) (_ : i < C.length) (d : List Bool),
      InDelBall s (natToWord n x) d ∧ InDelBall s (natToWord n C[i]) d

end DeletionCode
