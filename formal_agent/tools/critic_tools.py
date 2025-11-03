"""Example tools for the Critic Agent."""

from langchain.tools import tool


@tool
def critic_tool_example(input_data: str) -> str:
    """Example tool for critic agent. Replace this with actual tool implementations when ready.
    
    Args:
        input_data: Example input parameter
        
    Returns:
        Example output string
    """
    # Example output - replace with actual implementation later
    return f"Example critic tool output for input: {input_data}"
