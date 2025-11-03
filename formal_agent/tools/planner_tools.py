"""Example tools for the Planner Agent."""

from langchain.tools import tool


@tool
def planner_tool_example(input_data: str) -> str:
    """Example tool for planner agent. Replace this with actual tool implementations when ready.
    
    Args:
        input_data: Example input parameter
        
    Returns:
        Example output string
    """
    # Example output - replace with actual implementation later
    return f"Example planner tool output for input: {input_data}"
