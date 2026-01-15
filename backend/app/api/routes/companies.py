"""
Companies API routes.
"""

from fastapi import APIRouter

from app.models.company import CompaniesResponse
from app.services.company_service import CompanyService

router = APIRouter()
company_service = CompanyService()


@router.get("/companies", response_model=CompaniesResponse)
async def get_companies() -> CompaniesResponse:
    """
    Get list of available companies for resume evaluation.

    Returns:
        CompaniesResponse containing list of companies with metadata
    """
    companies = company_service.get_all_companies()
    return CompaniesResponse(companies=companies)
