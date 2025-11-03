"""Output schemas for agent responses."""

from pydantic import BaseModel, Field


class PlannerOutput(BaseModel):
    """Structured output from the Planner Agent."""
    plan: str = Field(description="Step-by-step proof plan with strategies and tactics")


class ProverOutput(BaseModel):
    """Structured output from the Prover Agent."""
    lean_code: str = Field(description="Complete Lean 4 proof code with imports")


class CriticOutput(BaseModel):
    """Structured output from the Critic Agent."""
    critique: str = Field(description="Detailed analysis of the error and suggested fixes")

