"""Type definitions for the formal agent workflow."""

from typing import TypedDict


class AgentState(TypedDict):
    """
    State schema passed between nodes in the LangGraph workflow.
    
    State Management in LangGraph:
    - Each node receives the full state as Dict[str, Any]
    - Each node returns a partial state (Dict with only updated fields)
    - LangGraph automatically merges the partial update into the full state
    
    Example:
        def my_node(state: Dict[str, Any]) -> Dict[str, Any]:
            # Process state
            result = process(state["input"])
            # Return only what changed
            return {"output": result}
    
    State Fields:
    """
    informal_statement: str   # The informal mathematical problem
    lean4_statement: str       # The Lean 4 theorem formalization
    plan_hint: str            # Strategic guidance from planner
    lean_candidate: str       # The generated Lean 4 proof code
    verify_success: bool      # Whether verification passed
    verify_log: str           # Output from Lean verifier
    critic_hint: str          # Feedback from critic on failed attempts
