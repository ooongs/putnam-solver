"""Prover node for the workflow graph."""

from formal_agent.agents.prover_agent import ProverAgent
from typing import Dict, Any


def prover_node(state: Dict[str, Any]) -> Dict[str, Any]:
    """
    Node that generates a Lean 4 proof.
    
    Args:
        state: Current agent state
        
    Returns:
        Partial state update with lean_candidate populated
    """
    prover = ProverAgent()
    
    lean_code = prover.prove(
        lean4_statement=state["lean4_statement"],
        plan_hint=state.get("plan_hint", ""),
        critic_hint=state.get("critic_hint", "")
    )
    
    # Return only the updated fields - LangGraph will merge with existing state
    return {"lean_candidate": lean_code}
