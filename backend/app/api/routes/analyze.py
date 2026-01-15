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
from app.services.role_matching_service import RoleMatchingService
from app.services.gap_analysis_service import GapAnalysisService
from app.services.timeline_service import TimelineService

router = APIRouter()
logger = logging.getLogger(__name__)
company_service = CompanyService()

# Lazy initialization to avoid requiring API key at import time
_resume_analysis_service = None
_role_matching_service = None
_gap_analysis_service = None
_timeline_service = None


def get_resume_analysis_service():
    """Get or create resume analysis service instance."""
    global _resume_analysis_service
    if _resume_analysis_service is None:
        _resume_analysis_service = ResumeAnalysisService()
    return _resume_analysis_service


def get_role_matching_service():
    """Get or create role matching service instance."""
    global _role_matching_service
    if _role_matching_service is None:
        _role_matching_service = RoleMatchingService()
    return _role_matching_service


def get_gap_analysis_service():
    """Get or create gap analysis service instance."""
    global _gap_analysis_service
    if _gap_analysis_service is None:
        _gap_analysis_service = GapAnalysisService()
    return _gap_analysis_service


def get_timeline_service():
    """Get or create timeline service instance."""
    global _timeline_service
    if _timeline_service is None:
        _timeline_service = TimelineService()
    return _timeline_service


@router.post("/analyze", response_model=AnalysisResponse)
async def analyze_resume(request: AnalysisRequest) -> AnalysisResponse:
    """
    Start complete resume analysis process using LLM.
    
    This endpoint performs four-phase analysis:
    
    Phase 1 - Resume Analysis:
    1. Validates the request
    2. Extracts text from the uploaded resume (PDF/DOCX)
    3. Sends resume to Claude API for analysis
    4. Extracts structured data (skills, experience, education, projects)
    5. Saves results to data/sessions/{session_id}/resume_analysis.json
    
    Phase 2 - Role Matching:
    6. Loads resume analysis results
    7. Loads company tenets
    8. Sends combined data to Claude API for matching analysis
    9. Calculates ATS, Role Match, and Company Fit scores
    10. Saves results to data/sessions/{session_id}/match_analysis.json
    
    Phase 3 - Gap Analysis:
    11. Loads match analysis results
    12. Sends data to Claude API for gap identification
    13. Identifies technical, experience, company fit, and resume gaps
    14. Generates prioritized recommendations with resources
    15. Saves results to data/sessions/{session_id}/gap_analysis.json
    
    Phase 4 - Timeline Generation:
    16. Loads gap analysis results
    17. Calculates timeline parameters (weeks available, hours per week)
    18. Sends data to Claude API for timeline generation
    19. Creates phases, tasks, milestones, and weekly breakdown
    20. Saves results to data/sessions/{session_id}/timeline.json
    
    Args:
        request: Analysis request with session_id, company, role_description, target_deadline
        
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
        # Phase 1: Perform resume analysis using LLM
        logger.info(f"Phase 1: Starting resume analysis for session: {request.session_id}")
        resume_analysis_service = get_resume_analysis_service()
        analysis_result = await resume_analysis_service.analyze_resume(
            resume_file_path=resume_file_path,
            session_id=request.session_id,
        )
        
        logger.info(f"Resume analysis completed successfully")
        logger.info(f"Extracted {len(analysis_result.get('skills', {}).get('programming_languages', []))} programming languages")
        logger.info(f"Found {len(analysis_result.get('experience', []))} work experiences")
        logger.info(f"Found {len(analysis_result.get('projects', []))} projects")
        
        # Phase 2: Perform role matching analysis
        logger.info(f"Phase 2: Starting role matching analysis for session: {request.session_id}")
        role_matching_service = get_role_matching_service()
        match_result = await role_matching_service.analyze_match(
            session_id=request.session_id,
            company_id=request.company,
            role_description=request.role_description,
        )
        
        logger.info(f"Role matching analysis completed successfully")
        logger.info(f"Scores - ATS: {match_result.get('ats_score', {}).get('score', 0)}, "
                   f"Role Match: {match_result.get('role_match_score', {}).get('score', 0)}, "
                   f"Company Fit: {match_result.get('company_fit_score', {}).get('score', 0)}, "
                   f"Overall: {match_result.get('overall_score', {}).get('score', 0)}")
        
        # Phase 3: Perform gap analysis
        logger.info(f"Phase 3: Starting gap analysis for session: {request.session_id}")
        gap_analysis_service = get_gap_analysis_service()
        gap_result = await gap_analysis_service.analyze_gaps(
            session_id=request.session_id,
            company_id=request.company,
            role_description=request.role_description,
        )
        
        logger.info(f"Gap analysis completed successfully")
        logger.info(f"Gaps identified - Total: {gap_result.get('summary', {}).get('total_gaps', 0)}, "
                   f"High: {gap_result.get('summary', {}).get('high_priority_count', 0)}, "
                   f"Medium: {gap_result.get('summary', {}).get('medium_priority_count', 0)}, "
                   f"Low: {gap_result.get('summary', {}).get('low_priority_count', 0)}")
        
        # Phase 4: Generate development timeline
        logger.info(f"Phase 4: Starting timeline generation for session: {request.session_id}")
        timeline_service = get_timeline_service()
        timeline_result = await timeline_service.generate_timeline(
            session_id=request.session_id,
            role_description=request.role_description,
            target_deadline=request.target_deadline,
        )
        
        logger.info(f"Timeline generation completed successfully")
        logger.info(f"Timeline - Phases: {len(timeline_result.get('phases', []))}, "
                   f"Weeks: {timeline_result.get('metadata', {}).get('total_weeks', 0)}, "
                   f"Total hours: {timeline_result.get('metadata', {}).get('total_hours', 0)}")
        
        return AnalysisResponse(
            analysis_id=analysis_id,
            session_id=request.session_id,
            status="completed",
            message="Complete analysis finished successfully. Resume parsed, role matching completed, gap analysis generated, and development timeline created."
        )
        
    except Exception as e:
        logger.error(f"Analysis failed for session {request.session_id}: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Analysis failed: {str(e)}"
        )
