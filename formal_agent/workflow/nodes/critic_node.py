"""Critic node for the workflow graph."""

from formal_agent.agents.critic_agent import CriticAgent
from typing import Dict, Any


def critic_node(state: Dict[str, Any]) -> Dict[str, Any]:
    """
    Node that provides critique on a failed proof.
    
    Args:
        state: Current agent state
        
    Returns:
        Partial state update with critic_hint and iteration_count populated
    """
    critic = CriticAgent()
    
    feedback = critic.critique(
        lean_candidate=state["lean_candidate"],
        verify_log=state["verify_log"],
        plan_hint=state["plan_hint"]
    )
    
    # Increment iteration count
    current_iteration = state.get("iteration_count", 0)
    
    # Return only the updated fields - LangGraph will merge with existing state
    return {
        "critic_hint": feedback,
        "iteration_count": current_iteration + 1
    }
