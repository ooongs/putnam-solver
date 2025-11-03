"""Orchestrator graph that coordinates the multi-agent workflow using LangGraph."""

from langgraph.graph import StateGraph, END
from typing import Dict, Any, TypedDict
from formal_agent.workflow.nodes import planner_node, prover_node, verifier_node, critic_node


class AgentState(TypedDict):
    """State schema for the agent workflow."""
    informal_statement: str
    lean4_statement: str
    plan_hint: str
    lean_candidate: str
    verify_success: bool
    verify_log: str
    critic_hint: str
    iteration_count: int
    max_iterations: int


def should_continue(state: Dict[str, Any]) -> str:
    """
    Conditional edge function that determines the next node after verification.
    
    Args:
        state: Current agent state
        
    Returns:
        "end" if verification succeeded or max iterations reached, "critic" otherwise
    """
    # End if verification succeeded
    if state.get("verify_success", False):
        return "end"
    
    # End if max iterations reached
    if state.get("iteration_count", 0) >= state.get("max_iterations", 5):
        return "end"
    
    # Otherwise continue to critic
    return "critic"


def create_workflow() -> StateGraph:
    """
    Create the LangGraph workflow for the formal proof agent.
    
    The workflow follows this pattern:
    1. planner_node: Generate a proof plan
    2. prover_node: Write a Lean 4 proof
    3. verifier_node: Verify the proof
    4. If verification succeeds → END
       If verification fails → critic_node → back to prover_node
    
    State Management:
    - Each node receives the full state as input
    - Each node returns a partial state (only updated fields)
    - LangGraph automatically merges partial updates into the full state
    
    Returns:
        Compiled StateGraph workflow
    """
    # Create the state graph with state schema
    workflow = StateGraph(AgentState)
    
    # Add nodes
    workflow.add_node("planner", planner_node)
    workflow.add_node("prover", prover_node)
    workflow.add_node("verifier", verifier_node)
    workflow.add_node("critic", critic_node)
    
    # Set entry point
    workflow.set_entry_point("planner")
    
    # Add edges
    workflow.add_edge("planner", "prover")
    workflow.add_edge("prover", "verifier")
    
    # Add conditional edge from verifier
    workflow.add_conditional_edges(
        "verifier",
        should_continue,
        {
            "end": END,
            "critic": "critic"
        }
    )
    
    # Add edge from critic back to prover
    workflow.add_edge("critic", "prover")
    
    # Compile and return
    return workflow.compile()


def run_workflow(informal_statement: str, lean4_statement: str, 
                 max_iterations: int = 5) -> AgentState:
    """
    Run the workflow on a given problem.
    
    Args:
        informal_statement: The informal mathematical statement
        lean4_statement: The Lean 4 formalization
        max_iterations: Maximum number of prover-critic iterations
        
    Returns:
        Final agent state containing all fields
    """
    # Initialize state with all required fields
    initial_state: AgentState = {
        "informal_statement": informal_statement,
        "lean4_statement": lean4_statement,
        "plan_hint": "",
        "lean_candidate": "",
        "verify_success": False,
        "verify_log": "",
        "critic_hint": "",
        "iteration_count": 0,
        "max_iterations": max_iterations
    }
    
    # Create and run workflow
    app = create_workflow()
    
    # Run with iteration limit
    # Each node will return partial state updates that get merged automatically
    # Formula: 1 (planner) + max_iterations * 3 (prover->verifier->critic) + 2 (final prover->verifier) + buffer
    recursion_limit = 1 + (max_iterations * 3) + 2 + 10
    result = app.invoke(initial_state, {"recursion_limit": recursion_limit})
    
    return result
