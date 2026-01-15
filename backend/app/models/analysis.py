"""
Analysis request and response models.
"""

from pydantic import BaseModel, Field, field_validator


class AnalysisRequest(BaseModel):
    """Request model for POST /api/analyze endpoint."""

    session_id: str = Field(..., description="Session ID from resume upload")
    company: str = Field(..., description="Selected company ID (amazon, meta, google)")
    role_description: str = Field(
        ...,
        min_length=50,
        max_length=10000,
        description="Job role description (50-10,000 characters)",
    )
    target_deadline: str | None = Field(
        None, description="Optional target application deadline (ISO date)"
    )

    @field_validator("role_description")
    @classmethod
    def validate_role_description(cls, v: str) -> str:
        """Validate role description length and content."""
        v = v.strip()
        if len(v) < 50:
            raise ValueError(
                f"Role description must be at least 50 characters (currently {len(v)})"
            )
        if len(v) > 10000:
            raise ValueError(
                f"Role description must not exceed 10,000 characters (currently {len(v)})"
            )
        return v

    @field_validator("company")
    @classmethod
    def validate_company(cls, v: str) -> str:
        """Validate company ID."""
        valid_companies = ["amazon", "meta", "google"]
        if v.lower() not in valid_companies:
            raise ValueError(
                f"Invalid company. Must be one of: {', '.join(valid_companies)}"
            )
        return v.lower()


class AnalysisResponse(BaseModel):
    """Response model for POST /api/analyze endpoint."""

    analysis_id: str
    session_id: str
    status: str
    message: str
