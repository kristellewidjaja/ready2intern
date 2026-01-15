"""
Analysis API routes.
"""

import uuid
import logging
from pathlib import Path
from fastapi import APIRouter, HTTPException

from app.models.analysis import AnalysisRequest, AnalysisResponse
from app.services.company_service import CompanyService

router = APIRouter()
logger = logging.getLogger(__name__)
company_service = CompanyService()


@router.post("/analyze", response_model=AnalysisResponse)
async def analyze_resume(request: AnalysisRequest) -> AnalysisResponse:
    """
    Start resume analysis process.
    
    This is a stub endpoint that validates input and returns an analysis ID.
    Actual LLM analysis will be implemented in Feature Slice 6.
    
    Args:
        request: Analysis request with session_id, company, role_description
        
    Returns:
        AnalysisResponse with analysis_id and status
        
    Raises:
        HTTPException: If validation fails or session not found
    """
    logger.info(f"Received analysis request for session: {request.session_id}")
    
    # Validate company ID
    if not company_service.validate_company_id(request.company):
        raise HTTPException(
            status_code=400,
            detail=f"Invalid company ID: {request.company}"
        )
    
    # Check if resume file exists for this session
    resume_dir = Path("data/resumes")
    session_files = list(resume_dir.glob(f"{request.session_id}_*"))
    
    if not session_files:
        raise HTTPException(
            status_code=404,
            detail=f"No resume found for session: {request.session_id}"
        )
    
    # Generate unique analysis ID
    analysis_id = str(uuid.uuid4())
    
    # Create session directory for analysis results (for future use)
    session_dir = Path(f"data/sessions/{request.session_id}")
    session_dir.mkdir(parents=True, exist_ok=True)
    
    logger.info(f"Created analysis {analysis_id} for session {request.session_id}")
    logger.info(f"Company: {request.company}, Role description length: {len(request.role_description)}")
    
    # Return immediate response
    # Actual analysis will be implemented in Feature Slice 6
    return AnalysisResponse(
        analysis_id=analysis_id,
        session_id=request.session_id,
        status="queued",
        message="Analysis request received. Processing will begin shortly."
    )
