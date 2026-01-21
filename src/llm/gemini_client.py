"""Google Gemini client implementation."""
import os
from typing import AsyncIterator, Optional

from src.llm.base_client import BaseLLMClient, GenerationConfig, GenerationResult


class GeminiClient(BaseLLMClient):
    """Client for Google Gemini API.
    
    Supports Gemini Pro and Gemini Ultra models.
    
    Example:
        >>> client = GeminiClient(api_key="...", model="gemini-pro")
        >>> result = await client.generate("Create a Python web scraper")
        >>> print(result.content)
    """
    
    DEFAULT_MODEL = "gemini-pro"
    
    def __init__(
        self,
        api_key: Optional[str] = None,
        model: str = DEFAULT_MODEL,
        base_url: Optional[str] = None
    ) -> None:
        """Initialize Gemini client.
        
        Args:
            api_key: Google API key. Defaults to GOOGLE_API_KEY env var.
            model: Model to use (e.g., "gemini-pro", "gemini-ultra").
            base_url: Custom API base URL (not typically used).
        """
        api_key = api_key or os.getenv("GOOGLE_API_KEY", "")
        super().__init__(api_key, model, base_url)
        self._client = None
    
    @property
    def provider_name(self) -> str:
        """Return the provider name."""
        return "google"
    
    def _get_client(self):
        """Get or create the Gemini client."""
        if self._client is None:
            try:
                import google.generativeai as genai
                genai.configure(api_key=self.api_key)
                self._client = genai.GenerativeModel(self.model)
            except ImportError:
                raise ImportError(
                    "google-generativeai package is required. "
                    "Install with: pip install google-generativeai"
                )
        return self._client
    
    async def generate(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        config: Optional[GenerationConfig] = None
    ) -> GenerationResult:
        """Generate code using Gemini API.
        
        Args:
            prompt: The user prompt for code generation.
            system_prompt: Optional system prompt (prepended to user prompt).
            config: Generation configuration.
            
        Returns:
            GenerationResult with generated content.
        """
        config = config or GenerationConfig()
        system_prompt = system_prompt or self._get_default_system_prompt()
        
        # Gemini doesn't have separate system prompt, so prepend it
        full_prompt = f"{system_prompt}\n\nUser request: {prompt}"
        
        client = self._get_client()
        
        generation_config = {
            "temperature": config.temperature,
            "max_output_tokens": config.max_tokens,
            "top_p": config.top_p,
        }
        if config.stop_sequences:
            generation_config["stop_sequences"] = config.stop_sequences
        
        response = await client.generate_content_async(
            full_prompt,
            generation_config=generation_config
        )
        
        # Get token count if available
        tokens_used = 0
        try:
            if hasattr(response, 'usage_metadata'):
                tokens_used = (
                    response.usage_metadata.prompt_token_count +
                    response.usage_metadata.candidates_token_count
                )
        except Exception:
            pass
        
        return GenerationResult(
            content=response.text if response.text else "",
            model=self.model,
            provider=self.provider_name,
            tokens_used=tokens_used,
            finish_reason="stop",
            metadata={}
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
        
        full_prompt = f"{system_prompt}\n\nUser request: {prompt}"
        
        client = self._get_client()
        
        generation_config = {
            "temperature": config.temperature,
            "max_output_tokens": config.max_tokens,
            "top_p": config.top_p,
        }
        
        response = await client.generate_content_async(
            full_prompt,
            generation_config=generation_config,
            stream=True
        )
        
        async for chunk in response:
            if chunk.text:
                yield chunk.text
    
    async def validate_connection(self) -> bool:
        """Validate API connection.
        
        Returns:
            True if connection is valid.
        """
        try:
            client = self._get_client()
            await client.generate_content_async("Hi")
            return True
        except Exception:
            return False
