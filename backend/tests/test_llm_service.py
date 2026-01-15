"""
Tests for LLM service.
"""

import pytest
import os
from unittest.mock import Mock, patch, AsyncMock
from anthropic import APIError, APITimeoutError, RateLimitError
from app.services.llm_service import LLMService


@pytest.fixture
def mock_env_vars(monkeypatch):
    """Set up mock environment variables."""
    monkeypatch.setenv("ANTHROPIC_API_KEY", "test-api-key-12345")


@pytest.fixture
def llm_service(mock_env_vars):
    """Create an LLMService instance with mocked API key."""
    return LLMService()


@pytest.fixture
def mock_anthropic_response():
    """Create a mock Anthropic API response."""
    mock_response = Mock()
    mock_response.content = [Mock(text="This is a test response from Claude")]
    mock_response.usage = Mock(input_tokens=100, output_tokens=50)
    return mock_response


class TestLLMService:
    """Test suite for LLMService."""
    
    def test_init_success(self, mock_env_vars, monkeypatch):
        """Test LLMService initialization with valid API key."""
        # Ensure no model override from environment
        monkeypatch.delenv("ANTHROPIC_MODEL", raising=False)
        
        service = LLMService()
        assert service is not None
        assert service.model == "claude-3-5-sonnet-20241022"  # Default value
        assert service.max_retries == 3  # Default value
        assert service.base_delay == 1  # Default value
    
    def test_init_no_api_key(self, monkeypatch):
        """Test LLMService initialization without API key."""
        monkeypatch.delenv("ANTHROPIC_API_KEY", raising=False)
        
        with pytest.raises(ValueError, match="ANTHROPIC_API_KEY"):
            LLMService()
    
    @pytest.mark.asyncio
    @patch("app.services.llm_service.Anthropic")
    async def test_generate_completion_success(
        self, mock_anthropic_class, llm_service, mock_anthropic_response
    ):
        """Test successful completion generation."""
        # Mock the client
        mock_client = Mock()
        mock_client.messages.create.return_value = mock_anthropic_response
        mock_anthropic_class.return_value = mock_client
        llm_service.client = mock_client
        
        # Generate completion
        result = await llm_service.generate_completion(
            prompt="Test prompt",
            system_prompt="Test system prompt",
        )
        
        assert result == "This is a test response from Claude"
        mock_client.messages.create.assert_called_once()
    
    @pytest.mark.asyncio
    @patch("app.services.llm_service.Anthropic")
    async def test_generate_completion_with_custom_params(
        self, mock_anthropic_class, llm_service, mock_anthropic_response
    ):
        """Test completion generation with custom parameters."""
        mock_client = Mock()
        mock_client.messages.create.return_value = mock_anthropic_response
        mock_anthropic_class.return_value = mock_client
        llm_service.client = mock_client
        
        result = await llm_service.generate_completion(
            prompt="Custom prompt",
            system_prompt="Custom system",
            max_tokens=2048,
            temperature=0.5,
        )
        
        assert result == "This is a test response from Claude"
        
        # Verify parameters
        call_args = mock_client.messages.create.call_args
        assert call_args.kwargs["max_tokens"] == 2048
        assert call_args.kwargs["temperature"] == 0.5
    
    @pytest.mark.asyncio
    @patch("app.services.llm_service.Anthropic")
    @patch("time.sleep", return_value=None)  # Mock sleep to speed up tests
    async def test_generate_completion_retry_on_rate_limit(
        self, mock_sleep, mock_anthropic_class, llm_service, mock_anthropic_response
    ):
        """Test retry logic on rate limit error."""
        mock_client = Mock()
        
        # Create proper RateLimitError with required arguments
        mock_response = Mock()
        mock_response.status_code = 429
        rate_limit_error = RateLimitError(
            "Rate limit exceeded",
            response=mock_response,
            body={"error": "rate_limit"}
        )
        
        # First call raises RateLimitError, second succeeds
        mock_client.messages.create.side_effect = [
            rate_limit_error,
            mock_anthropic_response,
        ]
        
        mock_anthropic_class.return_value = mock_client
        llm_service.client = mock_client
        
        result = await llm_service.generate_completion(prompt="Test")
        
        assert result == "This is a test response from Claude"
        assert mock_client.messages.create.call_count == 2
        mock_sleep.assert_called_once()  # Verify exponential backoff was used
    
    @pytest.mark.asyncio
    @patch("app.services.llm_service.Anthropic")
    @patch("time.sleep", return_value=None)
    async def test_generate_completion_retry_on_timeout(
        self, mock_sleep, mock_anthropic_class, llm_service, mock_anthropic_response
    ):
        """Test retry logic on timeout error."""
        mock_client = Mock()
        
        # First call times out, second succeeds
        mock_client.messages.create.side_effect = [
            APITimeoutError("Request timeout"),
            mock_anthropic_response,
        ]
        
        mock_anthropic_class.return_value = mock_client
        llm_service.client = mock_client
        
        result = await llm_service.generate_completion(prompt="Test")
        
        assert result == "This is a test response from Claude"
        assert mock_client.messages.create.call_count == 2
    
    @pytest.mark.asyncio
    @patch("app.services.llm_service.Anthropic")
    @patch("time.sleep", return_value=None)
    async def test_generate_completion_max_retries_exceeded(
        self, mock_sleep, mock_anthropic_class, llm_service
    ):
        """Test that exception is raised after max retries."""
        mock_client = Mock()
        
        # Create proper RateLimitError
        mock_response = Mock()
        mock_response.status_code = 429
        rate_limit_error = RateLimitError(
            "Rate limit exceeded",
            response=mock_response,
            body={"error": "rate_limit"}
        )
        
        # All calls raise RateLimitError
        mock_client.messages.create.side_effect = rate_limit_error
        
        mock_anthropic_class.return_value = mock_client
        llm_service.client = mock_client
        
        with pytest.raises(Exception, match="Rate limit exceeded after"):
            await llm_service.generate_completion(prompt="Test")
        
        assert mock_client.messages.create.call_count == 3  # max_retries
    
    @pytest.mark.asyncio
    @patch("app.services.llm_service.Anthropic")
    async def test_generate_completion_empty_response(
        self, mock_anthropic_class, llm_service
    ):
        """Test handling of empty response from API."""
        mock_client = Mock()
        
        # Mock empty response
        mock_response = Mock()
        mock_response.content = []
        mock_client.messages.create.return_value = mock_response
        
        mock_anthropic_class.return_value = mock_client
        llm_service.client = mock_client
        
        with pytest.raises(Exception, match="Empty response"):
            await llm_service.generate_completion(prompt="Test")
    
    @pytest.mark.asyncio
    @patch("app.services.llm_service.Anthropic")
    async def test_generate_completion_api_error(
        self, mock_anthropic_class, llm_service
    ):
        """Test handling of generic API error."""
        mock_client = Mock()
        
        # Create proper APIError with required arguments
        mock_request = Mock()
        api_error = APIError("API Error", request=mock_request, body={"error": "api_error"})
        mock_client.messages.create.side_effect = api_error
        
        mock_anthropic_class.return_value = mock_client
        llm_service.client = mock_client
        
        with pytest.raises(Exception, match="API error after"):
            await llm_service.generate_completion(prompt="Test")
    
    @pytest.mark.asyncio
    @patch("app.services.llm_service.Anthropic")
    async def test_generate_completion_unexpected_error(
        self, mock_anthropic_class, llm_service
    ):
        """Test handling of unexpected error."""
        mock_client = Mock()
        mock_client.messages.create.side_effect = ValueError("Unexpected error")
        
        mock_anthropic_class.return_value = mock_client
        llm_service.client = mock_client
        
        with pytest.raises(Exception, match="Unexpected error"):
            await llm_service.generate_completion(prompt="Test")
