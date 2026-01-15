"""
Tests for timeline service.
"""

import json
import pytest
from pathlib import Path
from unittest.mock import AsyncMock, MagicMock, patch, mock_open
from datetime import datetime, timedelta

from app.services.timeline_service import TimelineService


@pytest.fixture
def timeline_service():
    """Create timeline service instance."""
    with patch("app.services.timeline_service.LLMService"):
        service = TimelineService()
        # Mock the LLM service to avoid API key requirement
        service.llm_service = MagicMock()
        return service


@pytest.fixture
def sample_gap_analysis():
    """Sample gap analysis data."""
    return {
        "summary": {
            "total_gaps": 8,
            "high_priority_count": 2,
            "medium_priority_count": 4,
            "low_priority_count": 2,
            "estimated_preparation_time": "6-8 weeks",
            "overall_assessment": "Strong candidate with some skill gaps",
        },
        "technical_gaps": [
            {
                "gap_id": "tech_1",
                "category": "tools",
                "title": "Kubernetes Experience",
                "description": "Missing container orchestration experience",
                "priority": "high",
            }
        ],
        "experience_gaps": [
            {
                "gap_id": "exp_1",
                "category": "project_experience",
                "title": "Full-stack project",
                "description": "Need end-to-end project experience",
                "priority": "high",
            }
        ],
        "company_fit_gaps": [],
        "resume_optimization_gaps": [
            {
                "gap_id": "resume_1",
                "category": "keywords",
                "title": "Missing keywords",
                "description": "Add technical keywords",
                "priority": "medium",
            }
        ],
    }


@pytest.fixture
def sample_timeline():
    """Sample timeline result."""
    return {
        "metadata": {
            "total_weeks": 8,
            "total_hours": 96,
            "hours_per_week": 12,
            "start_date": "2026-01-15",
            "target_deadline": "2026-03-12",
            "intensity_level": "moderate",
            "feasibility_assessment": "Timeline is realistic with consistent effort",
        },
        "phases": [
            {
                "phase_id": "phase_1",
                "phase_number": 1,
                "title": "Foundation & Quick Wins",
                "description": "Focus on immediate improvements",
                "start_week": 1,
                "end_week": 2,
                "focus_areas": ["Resume optimization", "Environment setup"],
                "tasks": [
                    {
                        "task_id": "task_1",
                        "title": "Update resume with keywords",
                        "description": "Add missing technical keywords",
                        "gap_ids": ["resume_1"],
                        "estimated_hours": 4,
                        "priority": "high",
                        "dependencies": [],
                        "resources": ["ATS optimization guide"],
                        "success_criteria": "Resume passes ATS scan",
                    }
                ],
                "milestones": [
                    {
                        "milestone_id": "milestone_1",
                        "title": "Resume optimized",
                        "description": "Resume is ATS-friendly",
                        "target_date": "2026-01-22",
                        "completion_criteria": ["Keywords added", "Format validated"],
                        "deliverables": ["Updated resume PDF"],
                    }
                ],
                "estimated_hours_per_week": 12,
                "success_metrics": ["Resume score improved"],
            }
        ],
        "weekly_breakdown": [
            {
                "week_number": 1,
                "start_date": "2026-01-15",
                "end_date": "2026-01-21",
                "phase": "Phase 1: Foundation",
                "focus": "Resume optimization",
                "tasks": ["Update resume with keywords"],
                "estimated_hours": 12,
                "key_deliverable": "Optimized resume",
            }
        ],
        "critical_path": ["task_1"],
        "flexibility_notes": ["Can reduce project scope if time is tight"],
        "motivation_tips": ["Celebrate small wins", "Track progress weekly"],
    }


@pytest.mark.asyncio
async def test_generate_timeline_success(timeline_service, sample_gap_analysis, sample_timeline):
    """Test successful timeline generation."""
    session_id = "test-session-123"
    role_description = "Software Engineer Intern"
    target_deadline = "2026-03-12"
    
    # Mock _load_gap_analysis to return sample data
    timeline_service._load_gap_analysis = MagicMock(return_value=sample_gap_analysis)
    
    # Mock LLM response
    timeline_service.llm_service.generate_completion = AsyncMock(
        return_value=json.dumps(sample_timeline)
    )
    
    # Mock _save_timeline_results
    timeline_service._save_timeline_results = MagicMock()
    
    result = await timeline_service.generate_timeline(
        session_id=session_id,
        role_description=role_description,
        target_deadline=target_deadline,
    )
    
    # Verify result structure
    assert "metadata" in result
    assert "phases" in result
    assert "weekly_breakdown" in result
    assert result["metadata"]["total_weeks"] == 8
    assert len(result["phases"]) == 1
    assert len(result["weekly_breakdown"]) == 1


@pytest.mark.asyncio
async def test_generate_timeline_default_deadline(timeline_service, sample_gap_analysis, sample_timeline):
    """Test timeline generation with default deadline (12 weeks)."""
    session_id = "test-session-123"
    role_description = "Software Engineer Intern"
    
    # Mock _load_gap_analysis to return sample data
    timeline_service._load_gap_analysis = MagicMock(return_value=sample_gap_analysis)
    
    # Mock LLM response
    timeline_service.llm_service.generate_completion = AsyncMock(
        return_value=json.dumps(sample_timeline)
    )
    
    # Mock _save_timeline_results
    timeline_service._save_timeline_results = MagicMock()
    
    result = await timeline_service.generate_timeline(
        session_id=session_id,
        role_description=role_description,
        target_deadline=None,  # Should default to 12 weeks
    )
    
    # Verify metadata has dates
    assert "metadata" in result
    assert "start_date" in result["metadata"]
    assert "target_deadline" in result["metadata"]


@pytest.mark.asyncio
async def test_generate_timeline_short_deadline(timeline_service, sample_gap_analysis, sample_timeline):
    """Test timeline generation with short deadline (intensive mode)."""
    session_id = "test-session-123"
    role_description = "Software Engineer Intern"
    
    # Set deadline to 3 weeks from now (should trigger intensive mode)
    start_date = datetime.now().date()
    target_deadline = (start_date + timedelta(weeks=3)).isoformat()
    
    # Mock _load_gap_analysis to return sample data
    timeline_service._load_gap_analysis = MagicMock(return_value=sample_gap_analysis)
    
    # Mock LLM to verify it receives correct hours_per_week
    async def mock_generate(prompt, system_prompt, max_tokens, temperature):
        # Verify prompt contains intensive hours (20 hours/week)
        assert "20" in prompt or "hours_per_week" in prompt
        return json.dumps(sample_timeline)
    
    timeline_service.llm_service.generate_completion = AsyncMock(side_effect=mock_generate)
    
    # Mock _save_timeline_results
    timeline_service._save_timeline_results = MagicMock()
    
    result = await timeline_service.generate_timeline(
        session_id=session_id,
        role_description=role_description,
        target_deadline=target_deadline,
    )
    
    assert "metadata" in result


@pytest.mark.asyncio
async def test_generate_timeline_gap_analysis_not_found(timeline_service):
    """Test timeline generation when gap analysis is missing."""
    session_id = "test-session-123"
    role_description = "Software Engineer Intern"
    
    # Mock gap analysis file does not exist
    with patch("app.services.timeline_service.Path") as mock_path:
        mock_gap_file = MagicMock()
        mock_gap_file.exists.return_value = False
        mock_path.return_value = mock_gap_file
        
        with pytest.raises(Exception) as exc_info:
            await timeline_service.generate_timeline(
                session_id=session_id,
                role_description=role_description,
            )
        
        assert "Gap analysis not found" in str(exc_info.value)


@pytest.mark.asyncio
async def test_generate_timeline_llm_failure(timeline_service, sample_gap_analysis):
    """Test timeline generation when LLM call fails."""
    session_id = "test-session-123"
    role_description = "Software Engineer Intern"
    
    with patch("app.services.timeline_service.Path") as mock_path:
        mock_gap_file = MagicMock()
        mock_gap_file.exists.return_value = True
        mock_path.return_value = mock_gap_file
        
        with patch("builtins.open", mock_open(read_data=json.dumps(sample_gap_analysis))):
            # Mock LLM failure
            timeline_service.llm_service.generate_completion = AsyncMock(
                side_effect=Exception("LLM API error")
            )
            
            with pytest.raises(Exception) as exc_info:
                await timeline_service.generate_timeline(
                    session_id=session_id,
                    role_description=role_description,
                )
            
            assert "Failed to generate timeline" in str(exc_info.value)


def test_parse_llm_response_valid_json(timeline_service, sample_timeline):
    """Test parsing valid JSON response."""
    response = json.dumps(sample_timeline)
    result = timeline_service._parse_llm_response(response)
    
    assert result == sample_timeline
    assert "metadata" in result
    assert "phases" in result


def test_parse_llm_response_with_markdown(timeline_service, sample_timeline):
    """Test parsing JSON wrapped in markdown code blocks."""
    response = f"```json\n{json.dumps(sample_timeline)}\n```"
    result = timeline_service._parse_llm_response(response)
    
    assert result == sample_timeline


def test_parse_llm_response_missing_fields(timeline_service):
    """Test parsing response with missing required fields."""
    incomplete_response = {
        "phases": [],
        # Missing metadata and weekly_breakdown
    }
    response = json.dumps(incomplete_response)
    result = timeline_service._parse_llm_response(response)
    
    # Should add default metadata
    assert "metadata" in result
    assert "weekly_breakdown" in result


def test_parse_llm_response_invalid_json(timeline_service):
    """Test parsing invalid JSON response."""
    response = "This is not valid JSON"
    
    with pytest.raises(ValueError) as exc_info:
        timeline_service._parse_llm_response(response)
    
    assert "Invalid JSON response" in str(exc_info.value)


def test_validate_timeline_data(timeline_service, sample_timeline):
    """Test timeline data validation."""
    start_date = "2026-01-15"
    target_deadline = "2026-03-12"
    weeks_available = 8
    
    result = timeline_service._validate_timeline_data(
        sample_timeline,
        start_date,
        target_deadline,
        weeks_available,
    )
    
    # Verify metadata is updated
    assert result["metadata"]["start_date"] == start_date
    assert result["metadata"]["target_deadline"] == target_deadline
    assert result["metadata"]["total_weeks"] == weeks_available
    
    # Verify total hours is calculated
    assert result["metadata"]["total_hours"] == 4  # From sample task
    
    # Verify optional fields exist
    assert "critical_path" in result
    assert "flexibility_notes" in result
    assert "motivation_tips" in result


def test_validate_timeline_data_missing_metadata(timeline_service):
    """Test validation with missing metadata."""
    timeline_data = {
        "phases": [],
        "weekly_breakdown": [],
    }
    
    result = timeline_service._validate_timeline_data(
        timeline_data,
        "2026-01-15",
        "2026-03-12",
        8,
    )
    
    # Should create metadata
    assert "metadata" in result
    assert result["metadata"]["total_weeks"] == 8


def test_load_timeline_results_success(timeline_service, sample_timeline):
    """Test loading saved timeline results."""
    session_id = "test-session-123"
    
    with patch("app.services.timeline_service.Path") as mock_path:
        mock_file = MagicMock()
        mock_file.exists.return_value = True
        mock_path.return_value = mock_file
        
        with patch("builtins.open", mock_open(read_data=json.dumps(sample_timeline))):
            result = timeline_service.load_timeline_results(session_id)
    
    assert result == sample_timeline


def test_load_timeline_results_not_found(timeline_service):
    """Test loading timeline when file doesn't exist."""
    session_id = "test-session-123"
    
    with patch("app.services.timeline_service.Path") as mock_path:
        mock_file = MagicMock()
        mock_file.exists.return_value = False
        mock_path.return_value = mock_file
        
        result = timeline_service.load_timeline_results(session_id)
    
    assert result is None


def test_save_timeline_results(timeline_service, sample_timeline):
    """Test saving timeline results."""
    session_id = "test-session-123"
    
    with patch("app.services.timeline_service.Path") as mock_path:
        mock_dir = MagicMock()
        mock_path.return_value = mock_dir
        
        with patch("builtins.open", mock_open()) as mock_file:
            timeline_service._save_timeline_results(session_id, sample_timeline)
            
            # Verify directory creation
            mock_dir.mkdir.assert_called_once_with(parents=True, exist_ok=True)
            
            # Verify file write
            mock_file.assert_called_once()
