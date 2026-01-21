"""Anthropic Claude client implementation."""
import os
from typing import AsyncIterator, Optional

from src.llm.base_client import BaseLLMClient, GenerationConfig, GenerationResult


class AnthropicClient(BaseLLMClient):
    """Client for Anthropic Claude API.
    
    Supports Claude 3 models (Opus, Sonnet, Haiku) and Claude Code.
    
    Example:
        >>> client = AnthropicClient(api_key="sk-ant-...", model="claude-3-sonnet-20240229")
        >>> result = await client.generate("Create a Python REST API")
        >>> print(result.content)
    """
    
    DEFAULT_MODEL = "claude-3-sonnet-20240229"
    DEFAULT_BASE_URL = "https://api.anthropic.com"
    
    def __init__(
        self,
        api_key: Optional[str] = None,
        model: str = DEFAULT_MODEL,
        base_url: Optional[str] = None
    ) -> None:
        """Initialize Anthropic client.
        
        Args:
            api_key: Anthropic API key. Defaults to ANTHROPIC_API_KEY env var.
            model: Model to use (e.g., "claude-3-opus-20240229").
            base_url: Custom API base URL.
        """
        api_key = api_key or os.getenv("ANTHROPIC_API_KEY", "")
        base_url = base_url or self.DEFAULT_BASE_URL
        super().__init__(api_key, model, base_url)
        self._client = None
    
    @property
    def provider_name(self) -> str:
        """Return the provider name."""
        return "anthropic"
    
    def _get_client(self):
        """Get or create the Anthropic client."""
        if self._client is None:
            try:
                from anthropic import AsyncAnthropic
                self._client = AsyncAnthropic(
                    api_key=self.api_key,
                    base_url=self.base_url
                )
            except ImportError:
                raise ImportError(
                    "anthropic package is required. Install with: pip install anthropic"
                )
        return self._client
    
    async def generate(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        config: Optional[GenerationConfig] = None
    ) -> GenerationResult:
        """Generate code using Claude API.
        
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
        
        response = await client.messages.create(
            model=self.model,
            max_tokens=config.max_tokens,
            system=system_prompt,
            messages=[
                {"role": "user", "content": prompt}
            ],
            temperature=config.temperature,
            top_p=config.top_p,
            stop_sequences=config.stop_sequences or []
        )
        
        content = ""
        if response.content:
            content = response.content[0].text if hasattr(response.content[0], 'text') else str(response.content[0])
        
        return GenerationResult(
            content=content,
            model=self.model,
            provider=self.provider_name,
            tokens_used=response.usage.input_tokens + response.usage.output_tokens,
            finish_reason=response.stop_reason or "unknown",
            metadata={
                "input_tokens": response.usage.input_tokens,
                "output_tokens": response.usage.output_tokens,
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
        
        async with client.messages.stream(
            model=self.model,
            max_tokens=config.max_tokens,
            system=system_prompt,
            messages=[
                {"role": "user", "content": prompt}
            ],
            temperature=config.temperature,
            top_p=config.top_p
        ) as stream:
            async for text in stream.text_stream:
                yield text
    
    async def validate_connection(self) -> bool:
        """Validate API connection.
        
        Returns:
            True if connection is valid.
        """
        try:
            client = self._get_client()
            # Simple test message
            await client.messages.create(
                model=self.model,
                max_tokens=10,
                messages=[{"role": "user", "content": "Hi"}]
            )
            return True
        except Exception:
            return False
