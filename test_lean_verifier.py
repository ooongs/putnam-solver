from pathlib import Path
import textwrap
import os
from dotenv import load_dotenv
from formal_agent.agents.verifier import Verifier





def main():
    # (A) Valid proof example
    good_code = """
    theorem add_comm_test (a b : Nat) : a + b = b + a := by
      exact Nat.add_comm a b
    """

    # (B) Example designed to fail
    bad_code = """
    theorem bad_claim : 2 + 2 = 5 := by
      rfl
    """

    # (C) Test proof
    test_code = """
    import Mathlib.Data.Real.Basic
    import Mathlib.Data.Real.Sqrt
    import Mathlib.Data.Set.Basic
    import Mathlib.Analysis.SpecialFunctions.Pow.Real
    import Mathlib.Analysis.SpecialFunctions.Sqrt

    open Set Real

    open Real

    theorem putnam_1981_a1 : ∃ m : ℝ, m = Inf {((u - v)^2 + (Real.sqrt (2 - u^2) - 9 / v)^2) | (u v : ℝ) (_ : 0 < u ∧ u < Real.sqrt 2 ∧ v > 0)} := by
    refine ⟨Inf {((u - v)^2 + (Real.sqrt (2 - u^2) - 9 / v)^2) | (u v : ℝ) (_ : 0 < u ∧ u < Real.sqrt 2 ∧ v > 0)}, rfl⟩
    """
    verifier = Verifier()


    print("=== [TEST 1] good_code ===")
    success, log = verifier.verify(good_code)
    print("success:", success)
    print("log:")
    print(log)

    print("\n=== [TEST 2] bad_code ===")
    success, log = verifier.verify(bad_code)
    print("success:", success)
    print("log:")
    print(log)

    print("\n=== [TEST 3] test_code ===")
    success, log = verifier.verify(test_code)
    print("success:", success)
    print("log:")
    print(log)


if __name__ == "__main__":
    main()