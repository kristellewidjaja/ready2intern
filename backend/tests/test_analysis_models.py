"""
Tests for analysis models and validation.
"""

import pytest
from pydantic import ValidationError
from app.models.analysis import AnalysisRequest


def test_analysis_request_valid():
    """Test valid analysis request."""
    request = AnalysisRequest(
        session_id="test-session-123",
        company="amazon",
        role_description="A" * 100,  # Valid length
    )
    assert request.session_id == "test-session-123"
    assert request.company == "amazon"
    assert len(request.role_description) == 100


def test_analysis_request_role_description_too_short():
    """Test role description validation - too short."""
    with pytest.raises(ValidationError) as exc_info:
        AnalysisRequest(
            session_id="test-session-123",
            company="amazon",
            role_description="Short",  # Only 5 characters
        )
    
    errors = exc_info.value.errors()
    assert any("at least 50 characters" in str(error) for error in errors)


def test_analysis_request_role_description_too_long():
    """Test role description validation - too long."""
    with pytest.raises(ValidationError) as exc_info:
        AnalysisRequest(
            session_id="test-session-123",
            company="amazon",
            role_description="A" * 10001,  # 10,001 characters
        )
    
    errors = exc_info.value.errors()
    # Check for Pydantic's max_length error or custom validator error
    assert any("10000" in str(error) or "10,000" in str(error) for error in errors)


def test_analysis_request_role_description_min_length():
    """Test role description validation - exactly minimum length."""
    request = AnalysisRequest(
        session_id="test-session-123",
        company="amazon",
        role_description="A" * 50,  # Exactly 50 characters
    )
    assert len(request.role_description) == 50


def test_analysis_request_role_description_max_length():
    """Test role description validation - exactly maximum length."""
    request = AnalysisRequest(
        session_id="test-session-123",
        company="amazon",
        role_description="A" * 10000,  # Exactly 10,000 characters
    )
    assert len(request.role_description) == 10000


def test_analysis_request_role_description_strips_whitespace():
    """Test role description validation - strips whitespace."""
    request = AnalysisRequest(
        session_id="test-session-123",
        company="amazon",
        role_description="  " + ("A" * 50) + "  ",  # Whitespace around valid content
    )
    assert len(request.role_description) == 50
    assert request.role_description == "A" * 50


def test_analysis_request_invalid_company():
    """Test company validation - invalid company."""
    with pytest.raises(ValidationError) as exc_info:
        AnalysisRequest(
            session_id="test-session-123",
            company="invalid-company",
            role_description="A" * 100,
        )
    
    errors = exc_info.value.errors()
    assert any("Invalid company" in str(error) for error in errors)


def test_analysis_request_company_case_insensitive():
    """Test company validation - case insensitive."""
    request = AnalysisRequest(
        session_id="test-session-123",
        company="AMAZON",  # Uppercase
        role_description="A" * 100,
    )
    assert request.company == "amazon"  # Should be lowercased


def test_analysis_request_all_companies():
    """Test all valid company IDs."""
    for company in ["amazon", "meta", "google"]:
        request = AnalysisRequest(
            session_id="test-session-123",
            company=company,
            role_description="A" * 100,
        )
        assert request.company == company


def test_analysis_request_with_optional_deadline():
    """Test analysis request with optional target deadline."""
    request = AnalysisRequest(
        session_id="test-session-123",
        company="amazon",
        role_description="A" * 100,
        target_deadline="2026-03-01",
    )
    assert request.target_deadline == "2026-03-01"


def test_analysis_request_without_optional_deadline():
    """Test analysis request without optional target deadline."""
    request = AnalysisRequest(
        session_id="test-session-123",
        company="amazon",
        role_description="A" * 100,
    )
    assert request.target_deadline is None
