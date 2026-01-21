"""Base client interface for LLM providers."""
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any, AsyncIterator, Optional


@dataclass
class GenerationConfig:
    """Configuration for code generation."""
    
    temperature: float = 0.7
    max_tokens: int = 4096
    top_p: float = 1.0
    stop_sequences: Optional[list[str]] = None
    
    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary."""
        return {
            "temperature": self.temperature,
            "max_tokens": self.max_tokens,
            "top_p": self.top_p,
            "stop_sequences": self.stop_sequences or [],
        }


@dataclass
class GenerationResult:
    """Result from code generation."""
    
    content: str
    model: str
    provider: str
    tokens_used: int
    finish_reason: str
    metadata: dict[str, Any]
    
    @property
    def success(self) -> bool:
        """Check if generation was successful."""
        return self.finish_reason in ("stop", "end_turn", "complete")


class BaseLLMClient(ABC):
    """Abstract base class for LLM clients.
    
    All AI provider clients should inherit from this class and implement
    the required methods for generating code.
    """
    
    def __init__(
        self,
        api_key: str,
        model: str,
        base_url: Optional[str] = None
    ) -> None:
        """Initialize the LLM client.
        
        Args:
            api_key: API key for the provider.
            model: Model identifier to use.
            base_url: Optional custom base URL for the API.
        """
        self.api_key = api_key
        self.model = model
        self.base_url = base_url
    
    @property
    @abstractmethod
    def provider_name(self) -> str:
        """Return the provider name."""
        pass
    
    @abstractmethod
    async def generate(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        config: Optional[GenerationConfig] = None
    ) -> GenerationResult:
        """Generate code from a prompt.
        
        Args:
            prompt: The user prompt for code generation.
            system_prompt: Optional system prompt for context.
            config: Generation configuration options.
            
        Returns:
            GenerationResult with the generated content.
        """
        pass
    
    @abstractmethod
    async def generate_stream(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        config: Optional[GenerationConfig] = None
    ) -> AsyncIterator[str]:
        """Generate code with streaming output.
        
        Args:
            prompt: The user prompt for code generation.
            system_prompt: Optional system prompt for context.
            config: Generation configuration options.
            
        Yields:
            Chunks of generated content.
        """
        pass
    
    @abstractmethod
    async def validate_connection(self) -> bool:
        """Validate that the API connection works.
        
        Returns:
            True if connection is valid, False otherwise.
        """
        pass
    
    def _get_default_system_prompt(self) -> str:
        """Get the default system prompt for code generation."""
        return """You are a senior software engineer. Generate clean, maintainable, 
production-quality code. Follow best practices, include proper error handling,
add type hints, and write clear documentation."""
