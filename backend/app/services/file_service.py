"""File handling service for resume uploads"""
import os
import uuid
from pathlib import Path
from typing import Tuple
from fastapi import UploadFile, HTTPException
import logging

logger = logging.getLogger(__name__)

# Constants
MAX_FILE_SIZE = 5 * 1024 * 1024  # 5MB in bytes
ALLOWED_EXTENSIONS = {'.pdf', '.docx'}
UPLOAD_DIR = Path("data/resumes")


class FileService:
    """Service for handling file uploads and validation"""
    
    def __init__(self):
        """Initialize file service and ensure upload directory exists"""
        self.upload_dir = UPLOAD_DIR
        self.upload_dir.mkdir(parents=True, exist_ok=True)
        logger.info(f"FileService initialized with upload directory: {self.upload_dir}")
    
    async def validate_file(self, file: UploadFile) -> Tuple[bool, str]:
        """
        Validate uploaded file for type and size
        
        Args:
            file: The uploaded file object
            
        Returns:
            Tuple of (is_valid, error_message)
        """
        # Check if file has a filename
        if not file.filename:
            return False, "No file provided"
        
        # Check file extension
        file_ext = Path(file.filename).suffix.lower()
        if file_ext not in ALLOWED_EXTENSIONS:
            return False, f"Invalid file type. Allowed types: {', '.join(ALLOWED_EXTENSIONS)}"
        
        # Read file content to check size
        content = await file.read()
        file_size = len(content)
        
        # Reset file pointer for later use
        await file.seek(0)
        
        # Check file size
        if file_size == 0:
            return False, "File is empty"
        
        if file_size > MAX_FILE_SIZE:
            size_mb = file_size / (1024 * 1024)
            max_mb = MAX_FILE_SIZE / (1024 * 1024)
            return False, f"File size ({size_mb:.2f}MB) exceeds maximum allowed size ({max_mb}MB)"
        
        return True, ""
    
    async def save_file(self, file: UploadFile, session_id: str) -> Tuple[str, int]:
        """
        Save uploaded file to disk
        
        Args:
            file: The uploaded file object
            session_id: Unique session identifier
            
        Returns:
            Tuple of (file_path, file_size)
        """
        # Generate unique filename
        file_ext = Path(file.filename).suffix.lower()
        timestamp = uuid.uuid4().hex[:8]
        filename = f"{session_id}_{timestamp}{file_ext}"
        file_path = self.upload_dir / filename
        
        # Read file content
        content = await file.read()
        file_size = len(content)
        
        # Save file
        try:
            with open(file_path, "wb") as f:
                f.write(content)
            logger.info(f"File saved: {file_path} ({file_size} bytes)")
            return str(file_path), file_size
        except Exception as e:
            logger.error(f"Failed to save file: {e}")
            raise HTTPException(status_code=500, detail=f"Failed to save file: {str(e)}")
    
    def delete_file(self, file_path: str) -> bool:
        """
        Delete a file from disk
        
        Args:
            file_path: Path to the file to delete
            
        Returns:
            True if deletion successful, False otherwise
        """
        try:
            path = Path(file_path)
            if path.exists():
                path.unlink()
                logger.info(f"File deleted: {file_path}")
                return True
            return False
        except Exception as e:
            logger.error(f"Failed to delete file {file_path}: {e}")
            return False
    
    def generate_session_id(self) -> str:
        """
        Generate a unique session ID
        
        Returns:
            UUID string
        """
        return str(uuid.uuid4())
