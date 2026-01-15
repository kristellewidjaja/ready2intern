"""
Analysis API routes.
"""

import uuid
import logging
from pathlib import Path
from fastapi import APIRouter, HTTPException

from app.models.analysis import AnalysisRequest, AnalysisResponse
from app.services.company_service import CompanyService
from app.services.resume_analysis_service import ResumeAnalysisService

router = APIRouter()
logger = logging.getLogger(__name__)
company_service = CompanyService()

# Lazy initialization to avoid requiring API key at import time
_resume_analysis_service = None


def get_resume_analysis_service():
    """Get or create resume analysis service instance."""
    global _resume_analysis_service
    if _resume_analysis_service is None:
        _resume_analysis_service = ResumeAnalysisService()
    return _resume_analysis_service


@router.post("/analyze", response_model=AnalysisResponse)
async def analyze_resume(request: AnalysisRequest) -> AnalysisResponse:
    """
    Start resume analysis process using LLM.
    
    This endpoint:
    1. Validates the request
    2. Extracts text from the uploaded resume (PDF/DOCX)
    3. Sends resume to Claude API for analysis
    4. Extracts structured data (skills, experience, education, projects)
    5. Saves results to data/sessions/{session_id}/resume_analysis.json
    
    Args:
        request: Analysis request with session_id, company, role_description
        
    Returns:
        AnalysisResponse with analysis_id and status
        
    Raises:
        HTTPException: If validation fails, session not found, or analysis fails
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
    
    # Get the resume file path
    resume_file_path = str(session_files[0])
    logger.info(f"Found resume file: {resume_file_path}")
    
    # Generate unique analysis ID
    analysis_id = str(uuid.uuid4())
    
    try:
        # Perform resume analysis using LLM
        logger.info(f"Starting LLM-based resume analysis for session: {request.session_id}")
        resume_analysis_service = get_resume_analysis_service()
        analysis_result = await resume_analysis_service.analyze_resume(
            resume_file_path=resume_file_path,
            session_id=request.session_id,
        )
        
        logger.info(f"Resume analysis completed successfully for session: {request.session_id}")
        logger.info(f"Extracted {len(analysis_result.get('skills', {}).get('programming_languages', []))} programming languages")
        logger.info(f"Found {len(analysis_result.get('experience', []))} work experiences")
        logger.info(f"Found {len(analysis_result.get('projects', []))} projects")
        
        return AnalysisResponse(
            analysis_id=analysis_id,
            session_id=request.session_id,
            status="completed",
            message="Resume analysis completed successfully. Results saved."
        )
        
    except Exception as e:
        logger.error(f"Resume analysis failed for session {request.session_id}: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Resume analysis failed: {str(e)}"
        )
