"""Planner agent that generates proof plans."""

from langchain_openai import ChatOpenAI
from langchain.agents import create_agent
from langchain.agents.structured_output import ToolStrategy
import yaml
from pathlib import Path
from dotenv import load_dotenv
import os

from formal_agent.utils.prompt_templates import PLANNER_SYSTEM_PROMPT
from formal_agent.tools.planner_tools import planner_tool_example
from formal_agent.schemas.agent_outputs import PlannerOutput

# Load environment variables from .env file
load_dotenv()


class PlannerAgent:
    """Agent that creates high-level proof plans with tool support."""
    
    def __init__(self, config_path: str = "config/model_config.yaml"):
        """Initialize the planner agent with configuration and tools."""
        config_file = Path(__file__).parent.parent / config_path
        with open(config_file, 'r') as f:
            config = yaml.safe_load(f)
        
        planner_config = config['planner']
        
        # Create the model
        model = ChatOpenAI(
            model=planner_config['model_name'],
            temperature=planner_config['temperature'],
            max_tokens=planner_config['max_tokens']
        )
        
        # Tools available to the planner
        tools = [planner_tool_example]
        
        # Create agent with structured output
        self.agent = create_agent(
            model=model,
            # tools=tools,
            response_format=ToolStrategy(PlannerOutput)
        )
    
    def plan(self, informal_statement: str, lean4_statement: str) -> str:
        """
        Generate a proof plan.
        
        Args:
            informal_statement: The informal mathematical statement
            lean4_statement: The Lean 4 formalization
            
        Returns:
            String containing the proof plan
        """
        # Format the system prompt with the inputs
        system_prompt = PLANNER_SYSTEM_PROMPT.format(
            informal_statement=informal_statement,
            lean4_statement=lean4_statement
        )
        
        # Invoke the agent with the system prompt
        result = self.agent.invoke({
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": "Please generate the proof plan."}
            ]
        })
        
        # Extract structured response
        structured_output = result.get("structured_response")
        if structured_output:
            return structured_output.plan
        else:
            # Fallback to last message content
            return result["messages"][-1].content
