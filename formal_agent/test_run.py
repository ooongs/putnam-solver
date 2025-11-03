"""Test script to run the formal agent workflow on a sample problem."""

import sys
import os
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from formal_agent.utils.io_utils import load_json
from formal_agent.workflow.orchestrator_graph import run_workflow


def main():
    """Run the workflow on a test problem."""
    # Load the test problem
    data_file = Path(__file__).parent / "data" / "putnam_1981_a1.json"
    problem = load_json(str(data_file))
    
    print("=" * 80)
    print("Starting Formal Agent Workflow")
    print("=" * 80)
    print(f"\nProblem ID: {problem['problem_id']}")
    print(f"\nInformal Statement:\n{problem['informal_statement']}")
    print(f"\nLean 4 Statement:\n{problem['lean4_statement']}")
    print("\n" + "=" * 80)
    print("Running workflow...")
    print("=" * 80 + "\n")
    
    # Run the workflow
    try:
        result = run_workflow(
            informal_statement=problem['informal_statement'],
            lean4_statement=problem['lean4_statement'],
            max_iterations=3
        )
        
        print("\n" + "=" * 80)
        print("Workflow Complete")
        print("=" * 80)
        print(f"\nVerification Success: {result['verify_success']}")
        
        if result['verify_success']:
            print("\n✓ Proof verified successfully!")
            print(f"\nFinal Lean Code:\n{result['lean_candidate']}")
        else:
            print("\n✗ Proof verification failed after maximum iterations")
            print(f"\nLast Verification Log:\n{result['verify_log']}")
            print(f"\nLast Lean Candidate:\n{result['lean_candidate']}")
        
        print("\n" + "=" * 80)
        
    except Exception as e:
        print(f"\n✗ Error running workflow: {str(e)}")
        import traceback
        traceback.print_exc()
        return 1
    
    return 0


if __name__ == "__main__":
    sys.exit(main())

