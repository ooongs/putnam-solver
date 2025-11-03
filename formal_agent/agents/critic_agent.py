"""Critic agent that provides feedback on failed proofs."""

from langchain_openai import ChatOpenAI
from langchain.agents import create_agent
from langchain.agents.structured_output import ToolStrategy
import yaml
from pathlib import Path
from dotenv import load_dotenv
import os

from formal_agent.utils.prompt_templates import CRITIC_SYSTEM_PROMPT
from formal_agent.tools.critic_tools import critic_tool_example
from formal_agent.schemas.agent_outputs import CriticOutput

# Load environment variables from .env file
load_dotenv()


class CriticAgent:
    """Agent that critiques failed proof attempts with tool support."""
    
    def __init__(self, config_path: str = "config/model_config.yaml"):
        """Initialize the critic agent with configuration and tools."""
        config_file = Path(__file__).parent.parent / config_path
        with open(config_file, 'r') as f:
            config = yaml.safe_load(f)
        
        critic_config = config['critic']
        
        # Create the model
        model = ChatOpenAI(
            model=critic_config['model_name'],
            temperature=critic_config['temperature'],
            max_tokens=critic_config['max_tokens']
        )
        
        # Tools available to the critic
        tools = [critic_tool_example]
        
        # Create agent with structured output
        self.agent = create_agent(
            model=model,
            tools=tools,
            response_format=ToolStrategy(CriticOutput)
        )
    
    def critique(self, lean_candidate: str, verify_log: str, 
                 plan_hint: str) -> str:
        """
        Provide critique and feedback on a failed proof.
        
        Args:
            lean_candidate: The Lean 4 code that failed
            verify_log: The verification error log
            plan_hint: The original proof plan
            
        Returns:
            Feedback text as a string
        """
        # Format the system prompt with the inputs
        system_prompt = CRITIC_SYSTEM_PROMPT.format(
            lean_candidate=lean_candidate,
            verify_log=verify_log,
            plan_hint=plan_hint
        )
        
        # Invoke the agent with the system prompt
        result = self.agent.invoke({
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": "Please analyze the error and provide feedback."}
            ]
        })
        
        # Extract structured response
        structured_output = result.get("structured_response")
        if structured_output:
            return structured_output.critique
        else:
            # Fallback to last message content
            return result["messages"][-1].content
