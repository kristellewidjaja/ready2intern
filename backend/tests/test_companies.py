"""
Tests for companies API endpoint.
"""

import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_get_companies_success():
    """Test GET /api/companies returns list of companies."""
    response = client.get("/api/companies")
    
    assert response.status_code == 200
    data = response.json()
    
    assert "companies" in data
    assert isinstance(data["companies"], list)
    assert len(data["companies"]) == 3  # Amazon, Meta, Google
    
    # Verify structure of first company
    company = data["companies"][0]
    assert "id" in company
    assert "name" in company
    assert "display_name" in company
    assert "color" in company
    assert "logo_url" in company
    assert "tenets_file" in company
    assert "description" in company


def test_companies_have_required_fields():
    """Test that all companies have required fields."""
    response = client.get("/api/companies")
    data = response.json()
    
    required_fields = ["id", "name", "display_name", "color", "logo_url", "tenets_file", "description"]
    
    for company in data["companies"]:
        for field in required_fields:
            assert field in company
            assert company[field] is not None
            assert company[field] != ""


def test_companies_have_unique_ids():
    """Test that all companies have unique IDs."""
    response = client.get("/api/companies")
    data = response.json()
    
    company_ids = [company["id"] for company in data["companies"]]
    assert len(company_ids) == len(set(company_ids))  # All IDs are unique


def test_companies_include_expected_companies():
    """Test that response includes Amazon, Meta, and Google."""
    response = client.get("/api/companies")
    data = response.json()
    
    company_ids = [company["id"] for company in data["companies"]]
    assert "amazon" in company_ids
    assert "meta" in company_ids
    assert "google" in company_ids


def test_company_colors_are_valid_hex():
    """Test that company colors are valid hex codes."""
    response = client.get("/api/companies")
    data = response.json()
    
    import re
    hex_pattern = re.compile(r'^#[0-9A-Fa-f]{6}$')
    
    for company in data["companies"]:
        assert hex_pattern.match(company["color"]), f"Invalid color: {company['color']}"


def test_company_logo_urls_are_valid():
    """Test that company logo URLs are valid paths."""
    response = client.get("/api/companies")
    data = response.json()
    
    for company in data["companies"]:
        logo_url = company["logo_url"]
        assert logo_url.startswith("/logos/")
        assert logo_url.endswith(".svg")
