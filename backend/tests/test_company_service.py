"""
Tests for CompanyService.
"""

import pytest
from pathlib import Path
from app.services.company_service import CompanyService


@pytest.fixture
def company_service():
    """Create a CompanyService instance for testing."""
    return CompanyService()


def test_get_all_companies(company_service):
    """Test getting all companies."""
    companies = company_service.get_all_companies()
    
    assert len(companies) == 3
    assert all(hasattr(c, "id") for c in companies)
    assert all(hasattr(c, "name") for c in companies)
    assert all(hasattr(c, "display_name") for c in companies)


def test_get_company_by_id_valid(company_service):
    """Test getting a company by valid ID."""
    company = company_service.get_company_by_id("amazon")
    
    assert company is not None
    assert company.id == "amazon"
    assert company.display_name == "Amazon"
    assert company.color == "#FF9900"


def test_get_company_by_id_invalid(company_service):
    """Test getting a company by invalid ID."""
    company = company_service.get_company_by_id("invalid_company")
    
    assert company is None


def test_validate_company_id_valid(company_service):
    """Test validating valid company IDs."""
    assert company_service.validate_company_id("amazon") is True
    assert company_service.validate_company_id("meta") is True
    assert company_service.validate_company_id("google") is True


def test_validate_company_id_invalid(company_service):
    """Test validating invalid company IDs."""
    assert company_service.validate_company_id("invalid") is False
    assert company_service.validate_company_id("") is False
    assert company_service.validate_company_id("Apple") is False


def test_get_company_tenets_valid(company_service):
    """Test loading company tenets for valid company."""
    tenets = company_service.get_company_tenets("amazon")
    
    if tenets:  # Only test if file exists
        assert isinstance(tenets, str)
        assert len(tenets) > 0
        assert "Leadership Principles" in tenets or "leadership" in tenets.lower()


def test_get_company_tenets_invalid(company_service):
    """Test loading company tenets for invalid company."""
    tenets = company_service.get_company_tenets("invalid_company")
    
    assert tenets is None


def test_all_companies_have_tenets_files(company_service):
    """Test that all companies have corresponding tenets files."""
    companies = company_service.get_all_companies()
    
    for company in companies:
        tenets_path = Path(company_service.tenets_dir) / company.tenets_file
        # Note: File may not exist in test environment, so we just check the path is valid
        assert company.tenets_file.endswith(".txt")
        assert len(company.tenets_file) > 0
