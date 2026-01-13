"""Health check endpoint"""
from fastapi import APIRouter
from datetime import datetime
from typing import Dict

router = APIRouter()

@router.get("/health")
async def health_check() -> Dict[str, str]:
    """
    Health check endpoint to verify API is running
    
    Returns:
        Dict with status and timestamp
    """
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "service": "Ready2Intern API"
    }
