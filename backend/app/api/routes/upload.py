"""Resume upload endpoint"""
from fastapi import APIRouter, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
import logging

from app.models.upload import UploadResponse, ErrorResponse
from app.services.file_service import FileService

logger = logging.getLogger(__name__)

router = APIRouter()
file_service = FileService()


@router.post("/upload", response_model=UploadResponse, responses={
    400: {"model": ErrorResponse},
    500: {"model": ErrorResponse}
})
async def upload_resume(file: UploadFile = File(...)):
    """
    Upload resume file
    
    - **file**: Resume file (PDF or DOCX, max 5MB)
    
    Returns session_id for tracking the analysis
    """
    logger.info(f"Received upload request: {file.filename}")
    
    # Validate file
    is_valid, error_message = await file_service.validate_file(file)
    if not is_valid:
        logger.warning(f"File validation failed: {error_message}")
        return JSONResponse(
            status_code=400,
            content={
                "error": "Validation error",
                "message": error_message,
                "details": {
                    "filename": file.filename,
                    "max_size_mb": 5,
                    "allowed_types": [".pdf", ".docx"]
                }
            }
        )
    
    # Generate session ID
    session_id = file_service.generate_session_id()
    logger.info(f"Generated session_id: {session_id}")
    
    # Save file
    try:
        file_path, file_size = await file_service.save_file(file, session_id)
        logger.info(f"File saved successfully: {file_path}")
        
        return UploadResponse(
            session_id=session_id,
            status="uploaded",
            message="Resume uploaded successfully",
            filename=file.filename,
            file_size=file_size
        )
    except HTTPException as e:
        logger.error(f"Upload failed: {e.detail}")
        return JSONResponse(
            status_code=500,
            content={
                "error": "Upload failed",
                "message": str(e.detail),
                "details": {"session_id": session_id}
            }
        )
    except Exception as e:
        logger.error(f"Unexpected error during upload: {e}")
        return JSONResponse(
            status_code=500,
            content={
                "error": "Internal server error",
                "message": "An unexpected error occurred during file upload",
                "details": {}
            }
        )
