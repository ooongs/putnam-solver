"""Planner node for the workflow graph."""

from formal_agent.agents.planner_agent import PlannerAgent
from typing import Dict, Any


def planner_node(state: Dict[str, Any]) -> Dict[str, Any]:
    """
    Node that generates a proof plan.
    
    Args:
        state: Current agent state
        
    Returns:
        Partial state update with plan_hint populated
    """
    planner = PlannerAgent()
    
    plan_result = planner.plan(
        informal_statement=state["informal_statement"],
        lean4_statement=state["lean4_statement"]
    )
    
    # Return only the updated fields - LangGraph will merge with existing state
    return {"plan_hint": plan_result}
