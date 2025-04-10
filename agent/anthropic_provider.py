from typing import List, Optional, Dict, Any
import json
import anthropic
from openai.types.chat import ChatCompletionMessage
from openai_agents.providers import BaseProvider
from pydantic import BaseModel, Field


class AnthropicProviderConfig(BaseModel):
    model: str = Field(default="claude-3-5-sonnet-20240620")
    api_key: Optional[str] = None
    max_tokens: int = 4096
    temperature: float = 0.7
    enable_citations: bool = True
    citation_url_format: Optional[str] = None


class AnthropicProvider(BaseProvider):
    """Provider for Anthropic's Claude models with citation support."""
    
    def __init__(self, config: Optional[AnthropicProviderConfig] = None):
        self.config = config or AnthropicProviderConfig()
        self.client = anthropic.Anthropic(api_key=self.config.api_key)
        
    async def generate(
        self, 
        messages: List[Dict[str, Any]], 
        tools: Optional[List[Dict[str, Any]]] = None,
        **kwargs
    ) -> ChatCompletionMessage:
        """Generate a response from Anthropic with citation support."""
        anthropic_messages = self._convert_to_anthropic_messages(messages)
        
        params = {
            "model": self.config.model,
            "max_tokens": self.config.max_tokens,
            "temperature": self.config.temperature,
            "messages": anthropic_messages,
        }
        
        if self.config.enable_citations:
            params["citation_url_format"] = self.config.citation_url_format
        
        if tools:
            params["tools"] = tools
        
        params.update(kwargs)
        
        response = self.client.messages.create(**params)
        
        openai_message = self._convert_to_openai_message(response)
        
        return openai_message
    
    def _convert_to_anthropic_messages(self, messages: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Convert OpenAI message format to Anthropic format."""
        anthropic_messages = []
        
        for msg in messages:
            role = msg["role"]
            content = msg["content"]
            
            if role == "system":
                anthropic_messages.append({"role": "system", "content": content})
            elif role == "user":
                anthropic_messages.append({"role": "user", "content": content})
            elif role == "assistant":
                anthropic_messages.append({"role": "assistant", "content": content})
            elif role == "tool":
                pass
        
        return anthropic_messages
    
    def _convert_to_openai_message(self, anthropic_response: anthropic.types.Message) -> ChatCompletionMessage:
        """Convert Anthropic response to OpenAI ChatCompletionMessage format."""
        content = anthropic_response.content[0].text
        return ChatCompletionMessage(
            role="assistant",
            content=content,
            custom_data={"anthropic_response": anthropic_response.model_dump()}
        )