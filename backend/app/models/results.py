"""
Results response models for complete analysis data.
"""

from typing import Any, Dict
from pydantic import BaseModel, Field


class ResultsResponse(BaseModel):
    """Response model for GET /api/results/{session_id} endpoint."""

    session_id: str = Field(..., description="Session ID")
    status: str = Field(..., description="Analysis status (completed, partial, failed)")
    resume_analysis: Dict[str, Any] | None = Field(
        None, description="Resume analysis results"
    )
    match_analysis: Dict[str, Any] | None = Field(
        None, description="Role matching analysis with scores"
    )
    gap_analysis: Dict[str, Any] | None = Field(
        None, description="Gap analysis with recommendations"
    )
    timeline: Dict[str, Any] | None = Field(
        None, description="Development timeline with phases"
    )
    overall_score: int | None = Field(
        None, description="Overall match score (0-100)", ge=0, le=100
    )
    message: str = Field(..., description="Status message")
