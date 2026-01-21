"""OpenAI/GitHub Copilot client implementation."""
import os
from typing import Any, AsyncIterator, Optional

from src.llm.base_client import BaseLLMClient, GenerationConfig, GenerationResult


class OpenAIClient(BaseLLMClient):
    """Client for OpenAI API (GPT-4, GPT-3.5) and GitHub Copilot.
    
    This client supports both OpenAI's API and GitHub Copilot through
    the OpenAI-compatible API.
    
    Example:
        >>> client = OpenAIClient(api_key="sk-...", model="gpt-4")
        >>> result = await client.generate("Create a Python function to sort a list")
        >>> print(result.content)
    """
    
    DEFAULT_MODEL = "gpt-4"
    DEFAULT_BASE_URL = "https://api.openai.com/v1"
    
    def __init__(
        self,
        api_key: Optional[str] = None,
        model: str = DEFAULT_MODEL,
        base_url: Optional[str] = None,
        organization: Optional[str] = None
    ) -> None:
        """Initialize OpenAI client.
        
        Args:
            api_key: OpenAI API key. Defaults to OPENAI_API_KEY env var.
            model: Model to use (e.g., "gpt-4", "gpt-3.5-turbo").
            base_url: Custom API base URL.
            organization: Optional organization ID.
        """
        api_key = api_key or os.getenv("OPENAI_API_KEY", "")
        base_url = base_url or self.DEFAULT_BASE_URL
        super().__init__(api_key, model, base_url)
        self.organization = organization
        self._client = None
    
    @property
    def provider_name(self) -> str:
        """Return the provider name."""
        return "openai"
    
    def _get_client(self):
        """Get or create the OpenAI client."""
        if self._client is None:
            try:
                from openai import AsyncOpenAI
                self._client = AsyncOpenAI(
                    api_key=self.api_key,
                    base_url=self.base_url,
                    organization=self.organization
                )
            except ImportError:
                raise ImportError(
                    "openai package is required. Install with: pip install openai"
                )
        return self._client
    
    async def generate(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        config: Optional[GenerationConfig] = None
    ) -> GenerationResult:
        """Generate code using OpenAI API.
        
        Args:
            prompt: The user prompt for code generation.
            system_prompt: Optional system prompt.
            config: Generation configuration.
            
        Returns:
            GenerationResult with generated content.
        """
        config = config or GenerationConfig()
        system_prompt = system_prompt or self._get_default_system_prompt()
        
        client = self._get_client()
        
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": prompt}
        ]
        
        response = await client.chat.completions.create(
            model=self.model,
            messages=messages,
            temperature=config.temperature,
            max_tokens=config.max_tokens,
            top_p=config.top_p,
            stop=config.stop_sequences
        )
        
        choice = response.choices[0]
        
        return GenerationResult(
            content=choice.message.content or "",
            model=self.model,
            provider=self.provider_name,
            tokens_used=response.usage.total_tokens if response.usage else 0,
            finish_reason=choice.finish_reason or "unknown",
            metadata={
                "prompt_tokens": response.usage.prompt_tokens if response.usage else 0,
                "completion_tokens": response.usage.completion_tokens if response.usage else 0,
            }
        )
    
    async def generate_stream(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        config: Optional[GenerationConfig] = None
    ) -> AsyncIterator[str]:
        """Generate code with streaming output.
        
        Args:
            prompt: The user prompt.
            system_prompt: Optional system prompt.
            config: Generation configuration.
            
        Yields:
            Chunks of generated content.
        """
        config = config or GenerationConfig()
        system_prompt = system_prompt or self._get_default_system_prompt()
        
        client = self._get_client()
        
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": prompt}
        ]
        
        stream = await client.chat.completions.create(
            model=self.model,
            messages=messages,
            temperature=config.temperature,
            max_tokens=config.max_tokens,
            top_p=config.top_p,
            stop=config.stop_sequences,
            stream=True
        )
        
        async for chunk in stream:
            if chunk.choices and chunk.choices[0].delta.content:
                yield chunk.choices[0].delta.content
    
    async def validate_connection(self) -> bool:
        """Validate API connection.
        
        Returns:
            True if connection is valid.
        """
        import logging
        logger = logging.getLogger(__name__)
        
        try:
            client = self._get_client()
            await client.models.list()
            return True
        except ImportError as e:
            logger.warning(f"OpenAI package not installed: {e}")
            return False
        except Exception as e:
            logger.warning(f"OpenAI connection validation failed: {e}")
            return False
