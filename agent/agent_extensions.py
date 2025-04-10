from typing import List, Dict, Any, Optional, Union
from openai_agents import Agent
from openai_agents.schema import MessageContent, Message
from openai_agents.providers import BaseProvider, OpenAIProvider
from .anthropic_provider import AnthropicProvider, AnthropicProviderConfig
from .provider_factory import ProviderFactory
from .citation_parser import parse_citations, Citation
from .citation_helpers import format_message_with_citations


class EnhancedAgent(Agent):
    """An agent that supports both OpenAI and Anthropic models with citation handling."""
    
    def __init__(
        self,
        name: str,
        instructions: str,
        provider_type: str = "anthropic", 
        provider_config: Optional[Dict[str, Any]] = None,
        tools: Optional[List[Dict[str, Any]]] = None,
    ):

        self.provider_type = provider_type.lower()
        provider = ProviderFactory.create_provider(provider_type, provider_config)
        

        super().__init__(
            name=name,
            instructions=instructions,
            tools=tools,
            provider=provider
        )
        

        self.supports_citations = isinstance(provider, AnthropicProvider)
    
    async def run(self, message: Union[str, MessageContent]) -> Message:
        """Run the agent and return a message with citation information if available."""
        response = await super().run(message)
        

        if self.supports_citations:
            citations = parse_citations(response.raw)
            response.custom_data = {"citations": [c.model_dump() for c in citations]}
        
        return response
    
    def get_formatted_response(self, message: Message) -> str:
        """Get the response with citations highlighted for display (if available)."""
        if self.supports_citations:
            return format_message_with_citations(message.raw)
        return message.content
    
    def switch_provider(self, provider_type: str, provider_config: Optional[Dict[str, Any]] = None):
        """Switch between OpenAI and Anthropic providers."""
        self.provider_type = provider_type.lower()
        new_provider = ProviderFactory.create_provider(provider_type, provider_config)
        self._provider = new_provider
        self.supports_citations = isinstance(new_provider, AnthropicProvider)
        return self