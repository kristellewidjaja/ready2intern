"""
Company data models for API responses.
"""

from pydantic import BaseModel


class Company(BaseModel):
    """Company information model."""

    id: str
    name: str
    display_name: str
    color: str  # Hex color for UI theming
    logo_url: str  # URL path to company logo
    tenets_file: str  # Filename of company tenets document
    description: str  # Brief description of company evaluation criteria


class CompaniesResponse(BaseModel):
    """Response model for GET /api/companies endpoint."""

    companies: list[Company]
