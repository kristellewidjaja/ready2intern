"""
Tests for gap analysis service.
"""

import json
import pytest
from pathlib import Path
from unittest.mock import AsyncMock, MagicMock, patch, mock_open

from app.services.gap_analysis_service import GapAnalysisService


@pytest.fixture
def gap_analysis_service():
    """Create gap analysis service instance."""
    with patch("app.services.gap_analysis_service.LLMService"):
        service = GapAnalysisService()
        # Mock the LLM service to avoid API key requirement
        service.llm_service = MagicMock()
        return service


@pytest.fixture
def sample_match_analysis():
    """Sample match analysis data."""
    return {
        "ats_score": {
            "score": 88,
            "explanation": "Strong ATS optimization",
            "keyword_matches": {
                "matched_keywords": ["Python", "Java", "AWS", "Docker"],
                "missing_keywords": ["Kubernetes", "microservices"],
            },
        },
        "role_match_score": {
            "score": 82,
            "explanation": "Strong match for the role",
            "technical_skills_match": {
                "matched_skills": ["Python", "React", "PostgreSQL"],
                "missing_skills": ["GraphQL", "Redis"],
            },
            "experience_match": {
                "experience_gaps": ["Distributed systems", "Production debugging"],
            },
        },
        "company_fit_score": {
            "score": 75,
            "explanation": "Good cultural fit",
            "value_alignments": [
                {"company_value": "Customer Obsession", "strength": "strong"},
                {"company_value": "Ownership", "strength": "moderate"},
            ],
            "potential_concerns": ["Limited leadership examples"],
        },
        "overall_score": {
            "score": 81,
            "recommendation": "good_match",
            "key_concerns": ["Missing distributed systems experience"],
        },
    }


@pytest.fixture
def sample_gap_analysis():
    """Sample gap analysis result."""
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
                "priority_reasoning": "Critical for cloud-native development",
                "current_level": "none",
                "target_level": "intermediate",
                "impact_on_application": "Significant gap for role requirements",
                "recommendations": [
                    {
                        "action": "Complete Kubernetes tutorial",
                        "resources": [
                            {
                                "type": "course",
                                "name": "Kubernetes Basics",
                                "url": "https://kubernetes.io/docs/tutorials/",
                                "estimated_time": "10 hours",
                                "notes": "Official documentation",
                            }
                        ],
                        "success_criteria": "Deploy a multi-container app",
                        "estimated_time": "2 weeks",
                    }
                ],
            }
        ],
        "experience_gaps": [],
        "company_fit_gaps": [],
        "resume_optimization_gaps": [],
        "quick_wins": [],
        "long_term_development": [],
    }


class TestGapAnalysisService:
    """Test gap analysis service."""

    def test_initialization(self, gap_analysis_service):
        """Test service initialization."""
        assert gap_analysis_service is not None
        assert gap_analysis_service.llm_service is not None
        assert gap_analysis_service.company_service is not None

    @pytest.mark.asyncio
    async def test_analyze_gaps_success(
        self, gap_analysis_service, sample_match_analysis, sample_gap_analysis
    ):
        """Test successful gap analysis."""
        session_id = "test-session-123"
        company_id = "amazon"
        role_description = "Software Development Engineer Intern"

        # Mock dependencies
        gap_analysis_service._load_match_analysis = MagicMock(
            return_value=sample_match_analysis
        )
        gap_analysis_service.company_service.get_company_tenets = MagicMock(
            return_value="Customer Obsession\nOwnership\nInvent and Simplify"
        )
        gap_analysis_service.llm_service.generate_completion = AsyncMock(
            return_value=json.dumps(sample_gap_analysis)
        )
        gap_analysis_service._save_gap_results = MagicMock()

        # Execute
        result = await gap_analysis_service.analyze_gaps(
            session_id=session_id,
            company_id=company_id,
            role_description=role_description,
        )

        # Verify
        assert result is not None
        # Total gaps recalculated by validation (1 technical gap in sample)
        assert result["summary"]["total_gaps"] == 1
        assert result["summary"]["high_priority_count"] == 1
        assert len(result["technical_gaps"]) == 1
        gap_analysis_service._save_gap_results.assert_called_once()

    @pytest.mark.asyncio
    async def test_analyze_gaps_missing_match_analysis(self, gap_analysis_service):
        """Test gap analysis with missing match analysis."""
        session_id = "test-session-123"
        company_id = "amazon"
        role_description = "Software Development Engineer Intern"

        # Mock missing match analysis
        gap_analysis_service._load_match_analysis = MagicMock(return_value=None)

        # Execute and verify exception
        with pytest.raises(Exception) as exc_info:
            await gap_analysis_service.analyze_gaps(
                session_id=session_id,
                company_id=company_id,
                role_description=role_description,
            )

        assert "Match analysis not found" in str(exc_info.value)

    @pytest.mark.asyncio
    async def test_analyze_gaps_missing_company_tenets(
        self, gap_analysis_service, sample_match_analysis
    ):
        """Test gap analysis with missing company tenets."""
        session_id = "test-session-123"
        company_id = "invalid-company"
        role_description = "Software Development Engineer Intern"

        # Mock dependencies
        gap_analysis_service._load_match_analysis = MagicMock(
            return_value=sample_match_analysis
        )
        gap_analysis_service.company_service.get_company_tenets = MagicMock(
            return_value=None
        )

        # Execute and verify exception
        with pytest.raises(Exception) as exc_info:
            await gap_analysis_service.analyze_gaps(
                session_id=session_id,
                company_id=company_id,
                role_description=role_description,
            )

        assert "Company tenets not found" in str(exc_info.value)

    def test_load_match_analysis_success(self, gap_analysis_service, tmp_path):
        """Test loading match analysis from file system."""
        session_id = "test-session-123"
        match_data = {"ats_score": {"score": 85}}

        # Create test file
        session_dir = tmp_path / "data" / "sessions" / session_id
        session_dir.mkdir(parents=True)
        match_file = session_dir / "match_analysis.json"
        match_file.write_text(json.dumps(match_data))

        # Mock Path to use tmp_path
        with patch("app.services.gap_analysis_service.Path") as mock_path:
            mock_path.return_value = match_file
            result = gap_analysis_service._load_match_analysis(session_id)

        assert result is not None
        assert result["ats_score"]["score"] == 85

    def test_load_match_analysis_not_found(self, gap_analysis_service):
        """Test loading match analysis when file doesn't exist."""
        session_id = "nonexistent-session"

        result = gap_analysis_service._load_match_analysis(session_id)

        assert result is None

    def test_parse_llm_response_valid_json(self, gap_analysis_service):
        """Test parsing valid JSON response."""
        response = json.dumps(
            {
                "summary": {"total_gaps": 5},
                "technical_gaps": [],
                "experience_gaps": [],
                "company_fit_gaps": [],
                "resume_optimization_gaps": [],
            }
        )

        result = gap_analysis_service._parse_llm_response(response)

        assert result is not None
        assert result["summary"]["total_gaps"] == 5

    def test_parse_llm_response_with_markdown(self, gap_analysis_service):
        """Test parsing JSON wrapped in markdown code blocks."""
        response = (
            "```json\n"
            + json.dumps(
                {
                    "summary": {"total_gaps": 5},
                    "technical_gaps": [],
                    "experience_gaps": [],
                    "company_fit_gaps": [],
                    "resume_optimization_gaps": [],
                }
            )
            + "\n```"
        )

        result = gap_analysis_service._parse_llm_response(response)

        assert result is not None
        assert result["summary"]["total_gaps"] == 5

    def test_parse_llm_response_missing_fields(self, gap_analysis_service):
        """Test parsing response with missing required fields."""
        response = json.dumps({"summary": {"total_gaps": 5}})

        result = gap_analysis_service._parse_llm_response(response)

        assert result is not None
        assert "technical_gaps" in result
        assert "experience_gaps" in result
        assert result["technical_gaps"] == []

    def test_parse_llm_response_invalid_json(self, gap_analysis_service):
        """Test parsing invalid JSON response."""
        response = "This is not valid JSON {incomplete"

        with pytest.raises(ValueError) as exc_info:
            gap_analysis_service._parse_llm_response(response)

        assert "Invalid JSON response" in str(exc_info.value)

    def test_validate_gap_data(self, gap_analysis_service):
        """Test gap data validation and counting."""
        gap_data = {
            "summary": {},
            "technical_gaps": [
                {"gap_id": "tech_1", "priority": "high"},
                {"gap_id": "tech_2", "priority": "medium"},
            ],
            "experience_gaps": [{"gap_id": "exp_1", "priority": "high"}],
            "company_fit_gaps": [{"gap_id": "fit_1", "priority": "low"}],
            "resume_optimization_gaps": [],
        }

        result = gap_analysis_service._validate_gap_data(gap_data)

        assert result["summary"]["total_gaps"] == 4
        assert result["summary"]["high_priority_count"] == 2
        assert result["summary"]["medium_priority_count"] == 1
        assert result["summary"]["low_priority_count"] == 1

    def test_validate_gap_data_empty(self, gap_analysis_service):
        """Test validation with no gaps."""
        gap_data = {
            "technical_gaps": [],
            "experience_gaps": [],
            "company_fit_gaps": [],
            "resume_optimization_gaps": [],
        }

        result = gap_analysis_service._validate_gap_data(gap_data)

        assert result["summary"]["total_gaps"] == 0
        assert result["summary"]["high_priority_count"] == 0

    def test_save_gap_results(self, gap_analysis_service, tmp_path, sample_gap_analysis):
        """Test saving gap results to file system."""
        session_id = "test-session-123"

        # Mock Path to use tmp_path
        with patch("app.services.gap_analysis_service.Path") as mock_path:
            session_dir = tmp_path / "data" / "sessions" / session_id
            session_dir.mkdir(parents=True)
            mock_path.return_value = session_dir

            gap_analysis_service._save_gap_results(session_id, sample_gap_analysis)

            # Verify file was created
            output_file = session_dir / "gap_analysis.json"
            assert output_file.exists()

            # Verify content
            with open(output_file) as f:
                saved_data = json.load(f)
            assert saved_data["summary"]["total_gaps"] == 8

    def test_load_gap_results_success(self, gap_analysis_service, tmp_path):
        """Test loading gap results from file system."""
        session_id = "test-session-123"
        gap_data = {"summary": {"total_gaps": 5}}

        # Create test file
        session_dir = tmp_path / "data" / "sessions" / session_id
        session_dir.mkdir(parents=True)
        gap_file = session_dir / "gap_analysis.json"
        gap_file.write_text(json.dumps(gap_data))

        # Mock Path to use tmp_path
        with patch("app.services.gap_analysis_service.Path") as mock_path:
            mock_path.return_value = gap_file
            result = gap_analysis_service.load_gap_results(session_id)

        assert result is not None
        assert result["summary"]["total_gaps"] == 5

    def test_load_gap_results_not_found(self, gap_analysis_service):
        """Test loading gap results when file doesn't exist."""
        session_id = "nonexistent-session"

        result = gap_analysis_service.load_gap_results(session_id)

        assert result is None
