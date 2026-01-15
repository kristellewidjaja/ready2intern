"""
Tests for analyze API endpoint.
"""

import pytest
from unittest.mock import patch, AsyncMock
from fastapi.testclient import TestClient
from pathlib import Path
from app.main import app

client = TestClient(app)


@patch("app.api.routes.analyze.get_role_matching_service")
@patch("app.api.routes.analyze.get_resume_analysis_service")
def test_analyze_endpoint_success(mock_get_resume_service, mock_get_role_service, tmp_path):
    """Test successful analysis request with LLM integration."""
    # Create a test resume file
    resume_dir = Path("data/resumes")
    resume_dir.mkdir(parents=True, exist_ok=True)
    
    test_session_id = "test-session-123"
    test_file = resume_dir / f"{test_session_id}_test.pdf"
    test_file.write_text("test resume content")
    
    # Mock the resume analysis service
    mock_resume_service = AsyncMock()
    mock_resume_service.analyze_resume = AsyncMock(return_value={
        "personal_info": {"name": "Test User"},
        "skills": {"programming_languages": ["Python"]},
        "experience": [],
        "projects": [],
        "education": [],
        "summary": "Test summary"
    })
    mock_get_resume_service.return_value = mock_resume_service
    
    # Mock the role matching service
    mock_role_service = AsyncMock()
    mock_role_service.analyze_match = AsyncMock(return_value={
        "ats_score": {"score": 85},
        "role_match_score": {"score": 80},
        "company_fit_score": {"score": 75},
        "overall_score": {"score": 79}
    })
    mock_get_role_service.return_value = mock_role_service
    
    try:
        response = client.post(
            "/api/analyze",
            json={
                "session_id": test_session_id,
                "company": "amazon",
                "role_description": "A" * 100,  # Valid length
            },
        )
        
        assert response.status_code == 200
        data = response.json()
        
        assert "analysis_id" in data
        assert data["session_id"] == test_session_id
        assert data["status"] == "completed"
        assert "successfully" in data["message"].lower()
        
        # Verify both services were called
        mock_resume_service.analyze_resume.assert_called_once()
        mock_role_service.analyze_match.assert_called_once()
        
    finally:
        # Cleanup
        if test_file.exists():
            test_file.unlink()


def test_analyze_endpoint_invalid_company():
    """Test analysis with invalid company."""
    response = client.post(
        "/api/analyze",
        json={
            "session_id": "test-session-123",
            "company": "invalid-company",
            "role_description": "A" * 100,
        },
    )
    
    assert response.status_code == 422  # Validation error


def test_analyze_endpoint_role_description_too_short():
    """Test analysis with role description too short."""
    response = client.post(
        "/api/analyze",
        json={
            "session_id": "test-session-123",
            "company": "amazon",
            "role_description": "Short",  # Too short
        },
    )
    
    assert response.status_code == 422  # Validation error


def test_analyze_endpoint_role_description_too_long():
    """Test analysis with role description too long."""
    response = client.post(
        "/api/analyze",
        json={
            "session_id": "test-session-123",
            "company": "amazon",
            "role_description": "A" * 10001,  # Too long
        },
    )
    
    assert response.status_code == 422  # Validation error


def test_analyze_endpoint_missing_session():
    """Test analysis with non-existent session."""
    response = client.post(
        "/api/analyze",
        json={
            "session_id": "non-existent-session",
            "company": "amazon",
            "role_description": "A" * 100,
        },
    )
    
    assert response.status_code == 404
    assert "No resume found" in response.json()["detail"]


def test_analyze_endpoint_missing_fields():
    """Test analysis with missing required fields."""
    response = client.post(
        "/api/analyze",
        json={
            "company": "amazon",
            # Missing session_id and role_description
        },
    )
    
    assert response.status_code == 422  # Validation error


@patch("app.api.routes.analyze.get_role_matching_service")
@patch("app.api.routes.analyze.get_resume_analysis_service")
def test_analyze_endpoint_with_optional_deadline(mock_get_resume_service, mock_get_role_service, tmp_path):
    """Test analysis with optional target deadline."""
    # Create a test resume file
    resume_dir = Path("data/resumes")
    resume_dir.mkdir(parents=True, exist_ok=True)
    
    test_session_id = "test-session-456"
    test_file = resume_dir / f"{test_session_id}_test.pdf"
    test_file.write_text("test resume content")
    
    # Mock the resume analysis service
    mock_resume_service = AsyncMock()
    mock_resume_service.analyze_resume = AsyncMock(return_value={
        "personal_info": {"name": "Test User"},
        "skills": {"programming_languages": ["Python"]},
        "experience": [],
        "projects": [],
        "education": [],
        "summary": "Test summary"
    })
    mock_get_resume_service.return_value = mock_resume_service
    
    # Mock the role matching service
    mock_role_service = AsyncMock()
    mock_role_service.analyze_match = AsyncMock(return_value={
        "ats_score": {"score": 85},
        "role_match_score": {"score": 80},
        "company_fit_score": {"score": 75},
        "overall_score": {"score": 79}
    })
    mock_get_role_service.return_value = mock_role_service
    
    try:
        response = client.post(
            "/api/analyze",
            json={
                "session_id": test_session_id,
                "company": "meta",
                "role_description": "A" * 100,
                "target_deadline": "2026-03-01",
            },
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "completed"
        
    finally:
        # Cleanup
        if test_file.exists():
            test_file.unlink()


@patch("app.api.routes.analyze.get_role_matching_service")
@patch("app.api.routes.analyze.get_resume_analysis_service")
def test_analyze_endpoint_all_companies(mock_get_resume_service, mock_get_role_service, tmp_path):
    """Test analysis with all valid companies."""
    resume_dir = Path("data/resumes")
    resume_dir.mkdir(parents=True, exist_ok=True)
    
    # Mock the resume analysis service
    mock_resume_service = AsyncMock()
    mock_resume_service.analyze_resume = AsyncMock(return_value={
        "personal_info": {"name": "Test User"},
        "skills": {"programming_languages": ["Python"]},
        "experience": [],
        "projects": [],
        "education": [],
        "summary": "Test summary"
    })
    mock_get_resume_service.return_value = mock_resume_service
    
    # Mock the role matching service
    mock_role_service = AsyncMock()
    mock_role_service.analyze_match = AsyncMock(return_value={
        "ats_score": {"score": 85},
        "role_match_score": {"score": 80},
        "company_fit_score": {"score": 75},
        "overall_score": {"score": 79}
    })
    mock_get_role_service.return_value = mock_role_service
    
    for company in ["amazon", "meta", "google"]:
        test_session_id = f"test-session-{company}"
        test_file = resume_dir / f"{test_session_id}_test.pdf"
        test_file.write_text("test resume content")
        
        try:
            response = client.post(
                "/api/analyze",
                json={
                    "session_id": test_session_id,
                    "company": company,
                    "role_description": "A" * 100,
                },
            )
            
            assert response.status_code == 200
            data = response.json()
            assert data["session_id"] == test_session_id
            assert data["status"] == "completed"
            
        finally:
            # Cleanup
            if test_file.exists():
                test_file.unlink()


@patch("app.api.routes.analyze.get_role_matching_service")
@patch("app.api.routes.analyze.get_resume_analysis_service")
def test_analyze_endpoint_llm_failure(mock_get_resume_service, mock_get_role_service, tmp_path):
    """Test analysis when LLM service fails."""
    # Create a test resume file
    resume_dir = Path("data/resumes")
    resume_dir.mkdir(parents=True, exist_ok=True)
    
    test_session_id = "test-session-fail"
    test_file = resume_dir / f"{test_session_id}_test.pdf"
    test_file.write_text("test resume content")
    
    # Mock the resume analysis service to raise exception
    mock_resume_service = AsyncMock()
    mock_resume_service.analyze_resume = AsyncMock(
        side_effect=Exception("LLM API failed")
    )
    mock_get_resume_service.return_value = mock_resume_service
    
    # Mock role service (won't be called due to resume failure)
    mock_role_service = AsyncMock()
    mock_get_role_service.return_value = mock_role_service
    
    try:
        response = client.post(
            "/api/analyze",
            json={
                "session_id": test_session_id,
                "company": "amazon",
                "role_description": "A" * 100,
            },
        )
        
        assert response.status_code == 500
        assert "failed" in response.json()["detail"].lower()
        
    finally:
        # Cleanup
        if test_file.exists():
            test_file.unlink()
