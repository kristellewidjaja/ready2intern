"""Upload-related Pydantic models"""
from pydantic import BaseModel, Field
from typing import Literal


class UploadResponse(BaseModel):
    """Response model for file upload"""
    session_id: str = Field(..., description="Unique session identifier (UUID)")
    status: Literal["uploaded"] = Field(default="uploaded", description="Upload status")
    message: str = Field(default="Resume uploaded successfully", description="Status message")
    filename: str = Field(..., description="Original filename")
    file_size: int = Field(..., description="File size in bytes")


class ErrorResponse(BaseModel):
    """Error response model"""
    error: str = Field(..., description="Error type")
    message: str = Field(..., description="Human-readable error message")
    details: dict = Field(default_factory=dict, description="Additional error details")
