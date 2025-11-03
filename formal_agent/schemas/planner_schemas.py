"""Input schemas for Planner Agent tools."""

from pydantic import BaseModel, Field


class PlannerToolExampleInput(BaseModel):
    """Example input schema for planner tools."""
    input_data: str = Field(
        description="Example input parameter - replace with actual parameters when implementing real tools"
    )
