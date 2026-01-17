"""
Tests for results API endpoint.
"""

import json
import pytest
from pathlib import Path
from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


@pytest.fixture
def test_session_dir(tmp_path):
    """Create a test session directory with sample results."""
    session_id = "test-session-123"
    session_dir = tmp_path / "data" / "sessions" / session_id
    session_dir.mkdir(parents=True)
    
    # Create sample resume analysis
    resume_analysis = {
        "personal_info": {"name": "John Doe", "email": "john@example.com"},
        "skills": {"programming_languages": ["Python", "Java"]},
        "experience": [],
        "projects": [],
    }
    with open(session_dir / "resume_analysis.json", "w") as f:
        json.dump(resume_analysis, f)
    
    # Create sample match analysis
    match_analysis = {
        "ats_score": {"score": 85, "explanation": "Good ATS score"},
        "role_match_score": {"score": 78, "explanation": "Strong role match"},
        "company_fit_score": {"score": 82, "explanation": "Good company fit"},
        "overall_score": {"score": 80, "explanation": "Overall strong match"},
    }
    with open(session_dir / "match_analysis.json", "w") as f:
        json.dump(match_analysis, f)
    
    # Create sample gap analysis
    gap_analysis = {
        "technical_gaps": [],
        "experience_gaps": [],
        "summary": {"total_gaps": 5},
    }
    with open(session_dir / "gap_analysis.json", "w") as f:
        json.dump(gap_analysis, f)
    
    # Create sample timeline
    timeline = {
        "phases": [],
        "metadata": {"total_weeks": 12},
    }
    with open(session_dir / "timeline.json", "w") as f:
        json.dump(timeline, f)
    
    return session_id, session_dir


def test_get_results_success(test_session_dir, monkeypatch):
    """Test successful retrieval of complete results."""
    session_id, session_dir = test_session_dir
    
    # Monkeypatch the data directory path
    monkeypatch.setattr("app.api.routes.results.Path", lambda x: Path(str(session_dir.parent.parent.parent / x)))
    
    response = client.get(f"/api/results/{session_id}")
    
    assert response.status_code == 200
    data = response.json()
    
    assert data["session_id"] == session_id
    assert data["status"] == "completed"
    assert data["overall_score"] == 80
    assert data["resume_analysis"] is not None
    assert data["match_analysis"] is not None
    assert data["gap_analysis"] is not None
    assert data["timeline"] is not None
    assert "Complete analysis results available" in data["message"]


def test_get_results_partial(test_session_dir, monkeypatch):
    """Test retrieval of partial results when some files are missing."""
    session_id, session_dir = test_session_dir
    
    # Remove timeline file to simulate partial results
    (session_dir / "timeline.json").unlink()
    
    # Monkeypatch the data directory path
    monkeypatch.setattr("app.api.routes.results.Path", lambda x: Path(str(session_dir.parent.parent.parent / x)))
    
    response = client.get(f"/api/results/{session_id}")
    
    assert response.status_code == 200
    data = response.json()
    
    assert data["session_id"] == session_id
    assert data["status"] == "partial"
    assert data["overall_score"] == 80
    assert data["resume_analysis"] is not None
    assert data["match_analysis"] is not None
    assert data["gap_analysis"] is not None
    assert data["timeline"] is None
    assert "Partial results available" in data["message"]
    assert "timeline" in data["message"]


def test_get_results_session_not_found(tmp_path, monkeypatch):
    """Test error when session directory doesn't exist."""
    # Monkeypatch to use tmp_path
    monkeypatch.setattr("app.api.routes.results.Path", lambda x: tmp_path / x)
    
    response = client.get("/api/results/nonexistent-session")
    
    assert response.status_code == 404
    assert "Session not found" in response.json()["detail"]


def test_get_results_no_results(tmp_path, monkeypatch):
    """Test error when session exists but has no result files."""
    session_id = "empty-session"
    session_dir = tmp_path / "data" / "sessions" / session_id
    session_dir.mkdir(parents=True)
    
    # Monkeypatch the data directory path
    monkeypatch.setattr("app.api.routes.results.Path", lambda x: Path(str(session_dir.parent.parent.parent / x)))
    
    response = client.get(f"/api/results/{session_id}")
    
    assert response.status_code == 404
    assert "No analysis results found" in response.json()["detail"]


def test_get_results_invalid_json(test_session_dir, monkeypatch):
    """Test handling of corrupted JSON files."""
    session_id, session_dir = test_session_dir
    
    # Corrupt the timeline file
    with open(session_dir / "timeline.json", "w") as f:
        f.write("invalid json {")
    
    # Monkeypatch the data directory path
    monkeypatch.setattr("app.api.routes.results.Path", lambda x: Path(str(session_dir.parent.parent.parent / x)))
    
    response = client.get(f"/api/results/{session_id}")
    
    assert response.status_code == 200
    data = response.json()
    
    # Should still return partial results
    assert data["status"] == "partial"
    assert data["timeline"] is None
    assert data["resume_analysis"] is not None


def test_get_results_missing_overall_score(test_session_dir, monkeypatch):
    """Test handling when match analysis exists but overall score is missing."""
    session_id, session_dir = test_session_dir
    
    # Update match analysis to remove overall score
    match_analysis = {
        "ats_score": {"score": 85},
        "role_match_score": {"score": 78},
        "company_fit_score": {"score": 82},
    }
    with open(session_dir / "match_analysis.json", "w") as f:
        json.dump(match_analysis, f)
    
    # Monkeypatch the data directory path
    monkeypatch.setattr("app.api.routes.results.Path", lambda x: Path(str(session_dir.parent.parent.parent / x)))
    
    response = client.get(f"/api/results/{session_id}")
    
    assert response.status_code == 200
    data = response.json()
    
    assert data["overall_score"] is None
    assert data["match_analysis"] is not None


def test_get_results_only_resume_analysis(test_session_dir, monkeypatch):
    """Test status when only resume analysis is available."""
    session_id, session_dir = test_session_dir
    
    # Remove all files except resume analysis
    (session_dir / "match_analysis.json").unlink()
    (session_dir / "gap_analysis.json").unlink()
    (session_dir / "timeline.json").unlink()
    
    # Monkeypatch the data directory path
    monkeypatch.setattr("app.api.routes.results.Path", lambda x: Path(str(session_dir.parent.parent.parent / x)))
    
    response = client.get(f"/api/results/{session_id}")
    
    assert response.status_code == 200
    data = response.json()
    
    assert data["status"] == "partial"
    assert data["overall_score"] is None
    assert data["resume_analysis"] is not None
    assert data["match_analysis"] is None
