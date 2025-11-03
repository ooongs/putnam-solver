"""Verifier node for the workflow graph."""

from formal_agent.agents.verifier import Verifier
from typing import Dict, Any


def verifier_node(state: Dict[str, Any]) -> Dict[str, Any]:
    """
    Node that verifies a Lean 4 proof candidate.
    
    Args:
        state: Current agent state
        
    Returns:
        Partial state update with verify_success and verify_log populated
    """
    verifier = Verifier()
    
    success, log = verifier.verify(state["lean_candidate"])
    
    # Return only the updated fields - LangGraph will merge with existing state
    return {
        "verify_success": success,
        "verify_log": log
    }
