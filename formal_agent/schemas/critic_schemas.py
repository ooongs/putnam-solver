"""Input schemas for Critic Agent tools."""

from pydantic import BaseModel, Field


class CriticToolExampleInput(BaseModel):
    """Example input schema for critic tools."""
    input_data: str = Field(
        description="Example input parameter - replace with actual parameters when implementing real tools"
    )
