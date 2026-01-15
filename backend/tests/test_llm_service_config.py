"""
Tests for LLM service configuration options.
"""

import pytest
import os
from app.services.llm_service import LLMService


class TestLLMServiceConfiguration:
    """Test suite for LLM service configuration."""
    
    def test_default_model(self, monkeypatch):
        """Test that default model is used when not configured."""
        monkeypatch.setenv("ANTHROPIC_API_KEY", "test-key-123")
        
        service = LLMService()
        
        assert service.model == "claude-3-5-sonnet-20241022"
    
    def test_custom_model(self, monkeypatch):
        """Test that custom model can be configured."""
        monkeypatch.setenv("ANTHROPIC_API_KEY", "test-key-123")
        monkeypatch.setenv("ANTHROPIC_MODEL", "claude-3-5-haiku-20241022")
        
        service = LLMService()
        
        assert service.model == "claude-3-5-haiku-20241022"
    
    def test_default_max_retries(self, monkeypatch):
        """Test that default max retries is used when not configured."""
        monkeypatch.setenv("ANTHROPIC_API_KEY", "test-key-123")
        
        service = LLMService()
        
        assert service.max_retries == 3
    
    def test_custom_max_retries(self, monkeypatch):
        """Test that custom max retries can be configured."""
        monkeypatch.setenv("ANTHROPIC_API_KEY", "test-key-123")
        monkeypatch.setenv("LLM_MAX_RETRIES", "5")
        
        service = LLMService()
        
        assert service.max_retries == 5
    
    def test_default_retry_delay(self, monkeypatch):
        """Test that default retry delay is used when not configured."""
        monkeypatch.setenv("ANTHROPIC_API_KEY", "test-key-123")
        
        service = LLMService()
        
        assert service.base_delay == 1
    
    def test_custom_retry_delay(self, monkeypatch):
        """Test that custom retry delay can be configured."""
        monkeypatch.setenv("ANTHROPIC_API_KEY", "test-key-123")
        monkeypatch.setenv("LLM_RETRY_DELAY", "2")
        
        service = LLMService()
        
        assert service.base_delay == 2
    
    def test_all_custom_config(self, monkeypatch):
        """Test that all configuration options can be set together."""
        monkeypatch.setenv("ANTHROPIC_API_KEY", "test-key-123")
        monkeypatch.setenv("ANTHROPIC_MODEL", "claude-3-opus-20240229")
        monkeypatch.setenv("LLM_MAX_RETRIES", "10")
        monkeypatch.setenv("LLM_RETRY_DELAY", "3")
        
        service = LLMService()
        
        assert service.model == "claude-3-opus-20240229"
        assert service.max_retries == 10
        assert service.base_delay == 3
