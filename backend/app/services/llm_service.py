"""
LLM service for interacting with Anthropic Claude API.
"""

import os
import logging
import time
from typing import Any, Optional
from anthropic import Anthropic, APIError, APITimeoutError, RateLimitError

logger = logging.getLogger(__name__)


class LLMService:
    """Service for interacting with Anthropic Claude API with retry logic."""
    
    def __init__(self):
        """Initialize LLM service with API key from environment."""
        api_key = os.getenv("ANTHROPIC_API_KEY")
        if not api_key:
            raise ValueError("ANTHROPIC_API_KEY environment variable not set")
        
        self.client = Anthropic(api_key=api_key)
        # Allow model to be configured via environment variable
        self.model = os.getenv("ANTHROPIC_MODEL", "claude-3-5-sonnet-20241022")
        self.max_retries = int(os.getenv("LLM_MAX_RETRIES", "3"))
        self.base_delay = int(os.getenv("LLM_RETRY_DELAY", "1"))  # seconds
        
        logger.info(f"LLMService initialized with model: {self.model}")
    
    async def generate_completion(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        max_tokens: int = 4096,
        temperature: float = 0.7,
    ) -> str:
        """
        Generate completion from Claude API with retry logic.
        
        Args:
            prompt: User prompt to send to Claude
            system_prompt: Optional system prompt for context
            max_tokens: Maximum tokens in response
            temperature: Sampling temperature (0-1)
            
        Returns:
            Generated text response
            
        Raises:
            Exception: If all retries fail
        """
        for attempt in range(self.max_retries):
            try:
                logger.info(f"Calling Claude API (attempt {attempt + 1}/{self.max_retries})")
                
                # Prepare messages
                messages = [{"role": "user", "content": prompt}]
                
                # Call Claude API
                response = self.client.messages.create(
                    model=self.model,
                    max_tokens=max_tokens,
                    temperature=temperature,
                    system=system_prompt if system_prompt else "",
                    messages=messages,
                )
                
                # Extract text from response
                if response.content and len(response.content) > 0:
                    result = response.content[0].text
                    logger.info(f"Claude API call successful (tokens: {response.usage.input_tokens} in, {response.usage.output_tokens} out)")
                    return result
                else:
                    raise ValueError("Empty response from Claude API")
                
            except RateLimitError as e:
                logger.warning(f"Rate limit hit on attempt {attempt + 1}: {e}")
                if attempt < self.max_retries - 1:
                    delay = self.base_delay * (2 ** attempt)  # Exponential backoff
                    logger.info(f"Retrying in {delay} seconds...")
                    time.sleep(delay)
                else:
                    logger.error("Max retries reached for rate limit")
                    raise Exception(f"Rate limit exceeded after {self.max_retries} attempts") from e
                    
            except APITimeoutError as e:
                logger.warning(f"API timeout on attempt {attempt + 1}: {e}")
                if attempt < self.max_retries - 1:
                    delay = self.base_delay * (2 ** attempt)
                    logger.info(f"Retrying in {delay} seconds...")
                    time.sleep(delay)
                else:
                    logger.error("Max retries reached for timeout")
                    raise Exception(f"API timeout after {self.max_retries} attempts") from e
                    
            except APIError as e:
                logger.error(f"API error on attempt {attempt + 1}: {e}")
                if attempt < self.max_retries - 1:
                    delay = self.base_delay * (2 ** attempt)
                    logger.info(f"Retrying in {delay} seconds...")
                    time.sleep(delay)
                else:
                    logger.error("Max retries reached for API error")
                    raise Exception(f"API error after {self.max_retries} attempts") from e
                    
            except Exception as e:
                logger.error(f"Unexpected error on attempt {attempt + 1}: {e}")
                raise Exception(f"Unexpected error calling Claude API: {str(e)}") from e
        
        raise Exception("Failed to generate completion after all retries")
