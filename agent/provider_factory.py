from typing import Optional, Union, Dict, Any
from openai_agents.providers import OpenAIProvider
from .anthropic_provider import AnthropicProvider, AnthropicProviderConfig

class ProviderFactory:
    """Factory for creating LLM providers with unified configuration."""
    
    @staticmethod
    def create_provider(
        provider_type: str,
        config: Optional[Union[Dict[str, Any], AnthropicProviderConfig]] = None
    ):

        if provider_type.lower() == "anthropic":
            if isinstance(config, dict):
                config = AnthropicProviderConfig(**config)
            return AnthropicProvider(config=config)
        
        elif provider_type.lower() == "openai":
            return OpenAIProvider(**config if config else {})
        
        else:
            raise ValueError(f"Unsupported provider type: {provider_type}")