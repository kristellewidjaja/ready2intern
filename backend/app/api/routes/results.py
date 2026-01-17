"""
Results API routes.
"""

import json
import logging
from pathlib import Path
from fastapi import APIRouter, HTTPException

from app.models.results import ResultsResponse

router = APIRouter()
logger = logging.getLogger(__name__)


@router.get("/results/{session_id}", response_model=ResultsResponse)
async def get_results(session_id: str) -> ResultsResponse:
    """
    Retrieve complete analysis results for a session.
    
    Loads all analysis JSON files from the session directory and combines
    them into a single response object. Returns partial results if some
    files are missing.
    
    Args:
        session_id: Session ID from resume upload
        
    Returns:
        ResultsResponse with all available analysis data
        
    Raises:
        HTTPException: If session directory doesn't exist or no results found
    """
    logger.info(f"Fetching results for session: {session_id}")
    
    # Check if session directory exists
    session_dir = Path(f"data/sessions/{session_id}")
    if not session_dir.exists():
        raise HTTPException(
            status_code=404,
            detail=f"Session not found: {session_id}"
        )
    
    # Define expected result files
    result_files = {
        "resume_analysis": session_dir / "resume_analysis.json",
        "match_analysis": session_dir / "match_analysis.json",
        "gap_analysis": session_dir / "gap_analysis.json",
        "timeline": session_dir / "timeline.json",
    }
    
    # Load available results
    results = {}
    missing_files = []
    
    for key, file_path in result_files.items():
        if file_path.exists():
            try:
                with open(file_path, "r") as f:
                    results[key] = json.load(f)
                logger.info(f"Loaded {key} for session {session_id}")
            except Exception as e:
                logger.error(f"Failed to load {key}: {e}")
                results[key] = None
                missing_files.append(key)
        else:
            logger.warning(f"Missing {key} for session {session_id}")
            results[key] = None
            missing_files.append(key)
    
    # Check if we have at least some results
    if all(v is None for v in results.values()):
        raise HTTPException(
            status_code=404,
            detail=f"No analysis results found for session: {session_id}"
        )
    
    # Extract overall score from match analysis if available
    overall_score = None
    if results.get("match_analysis"):
        overall_score_data = results["match_analysis"].get("overall_score", {})
        overall_score = overall_score_data.get("score")
    
    # Determine status
    if not missing_files:
        status = "completed"
        message = "Complete analysis results available"
    elif results.get("resume_analysis"):
        status = "partial"
        message = f"Partial results available. Missing: {', '.join(missing_files)}"
    else:
        status = "failed"
        message = "Analysis incomplete or failed"
    
    return ResultsResponse(
        session_id=session_id,
        status=status,
        resume_analysis=results.get("resume_analysis"),
        match_analysis=results.get("match_analysis"),
        gap_analysis=results.get("gap_analysis"),
        timeline=results.get("timeline"),
        overall_score=overall_score,
        message=message,
    )
