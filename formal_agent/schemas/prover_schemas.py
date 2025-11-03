"""Input schemas for Prover Agent tools."""

from pydantic import BaseModel, Field


class ProverToolExampleInput(BaseModel):
    """Example input schema for prover tools."""
    input_data: str = Field(
        description="Example input parameter - replace with actual parameters when implementing real tools"
    )
