"""Tests for health check endpoint"""
import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_health_check():
    """Test health check endpoint returns 200 and correct data"""
    response = client.get("/api/health")
    assert response.status_code == 200
    
    data = response.json()
    assert data["status"] == "healthy"
    assert "timestamp" in data
    assert data["service"] == "Ready2Intern API"

def test_health_check_response_format():
    """Test health check response has correct format"""
    response = client.get("/api/health")
    data = response.json()
    
    # Check all required fields are present
    required_fields = ["status", "timestamp", "service"]
    for field in required_fields:
        assert field in data, f"Missing required field: {field}"
