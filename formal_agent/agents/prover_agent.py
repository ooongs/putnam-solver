"""Prover agent that generates Lean 4 proofs."""

from langchain_openai import ChatOpenAI
from langchain.agents import create_agent
from langchain.agents.structured_output import ToolStrategy
import yaml
from pathlib import Path
from dotenv import load_dotenv
import os

from formal_agent.utils.prompt_templates import PROVER_SYSTEM_PROMPT
from formal_agent.tools.prover_tools import prover_tool_example
from formal_agent.schemas.agent_outputs import ProverOutput

# Load environment variables from .env file
load_dotenv()


class ProverAgent:
    """Agent that writes Lean 4 proofs with tool support."""
    
    def __init__(self, config_path: str = "config/model_config.yaml"):
        """Initialize the prover agent with configuration and tools."""
        config_file = Path(__file__).parent.parent / config_path
        with open(config_file, 'r') as f:
            config = yaml.safe_load(f)
        
        prover_config = config['prover']
        
        # Create the model
        model = ChatOpenAI(
            model=prover_config['model_name'],
            temperature=prover_config['temperature'],
            max_tokens=prover_config['max_tokens']
        )
        
        # Tools available to the prover
        tools = [prover_tool_example]
        
        # Create agent with structured output
        self.agent = create_agent(
            model=model,
            tools=tools,
            response_format=ToolStrategy(ProverOutput)
        )
    
    def prove(self, lean4_statement: str, plan_hint: str, critic_hint: str = "") -> str:
        """
        Generate a Lean 4 proof.
        
        Args:
            lean4_statement: The Lean 4 theorem statement
            plan_hint: The proof plan from planner
            critic_hint: Feedback from critic (if any)
            
        Returns:
            Lean 4 code as a string
        """
        # Prepare critic hint section
        critic_hint_section = ""
        if critic_hint:
            critic_hint_section = f"\nCritic Feedback:\n{critic_hint}\n\nPlease address the feedback above."
        
        # Format the system prompt with the inputs
        system_prompt = PROVER_SYSTEM_PROMPT.format(
            lean4_statement=lean4_statement,
            plan_hint=plan_hint,
            critic_hint_section=critic_hint_section
        )
        
        # Invoke the agent with the system prompt
        result = self.agent.invoke({
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": "Please generate the Lean 4 proof."}
            ]
        })
        
        # Extract structured response
        structured_output = result.get("structured_response")
        if structured_output:
            return structured_output.lean_code
        else:
            # Fallback to last message content
            return result["messages"][-1].content
