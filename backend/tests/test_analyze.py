"""
Tests for analyze API endpoint.
"""

import pytest
from fastapi.testclient import TestClient
from pathlib import Path
from app.main import app

client = TestClient(app)


def test_analyze_endpoint_success(tmp_path):
    """Test successful analysis request."""
    # Create a test resume file
    resume_dir = Path("data/resumes")
    resume_dir.mkdir(parents=True, exist_ok=True)
    
    test_session_id = "test-session-123"
    test_file = resume_dir / f"{test_session_id}_test.pdf"
    test_file.write_text("test resume content")
    
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
        assert data["status"] == "queued"
        assert "message" in data
        
        # Check that session directory was created
        session_dir = Path(f"data/sessions/{test_session_id}")
        assert session_dir.exists()
        
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


def test_analyze_endpoint_with_optional_deadline(tmp_path):
    """Test analysis with optional target deadline."""
    # Create a test resume file
    resume_dir = Path("data/resumes")
    resume_dir.mkdir(parents=True, exist_ok=True)
    
    test_session_id = "test-session-456"
    test_file = resume_dir / f"{test_session_id}_test.pdf"
    test_file.write_text("test resume content")
    
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
        assert data["status"] == "queued"
        
    finally:
        # Cleanup
        if test_file.exists():
            test_file.unlink()


def test_analyze_endpoint_all_companies(tmp_path):
    """Test analysis with all valid companies."""
    resume_dir = Path("data/resumes")
    resume_dir.mkdir(parents=True, exist_ok=True)
    
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
            
        finally:
            # Cleanup
            if test_file.exists():
                test_file.unlink()
