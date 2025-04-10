from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field


class Citation(BaseModel):
    start_index: int
    end_index: int
    text: str
    document_id: Optional[str] = None
    url: Optional[str] = None
    title: Optional[str] = None
    
    def __str__(self):
        if self.url:
            return f"{self.text} [{self.url}]"
        elif self.title:
            return f"{self.text} [{self.title}]"
        else:
            return f"{self.text} [Document ID: {self.document_id}]"


def parse_citations(message: Dict[str, Any]) -> List[Citation]:
    if not message.get("custom_data") or not message["custom_data"].get("anthropic_response"):
        return []
        
    anthropic_data = message["custom_data"]["anthropic_response"]
    
    citations = []
    
    if not anthropic_data.get("citations"):
        return []
        
    for citation_data in anthropic_data["citations"]:
        citation = Citation(
            start_index=citation_data["start"],
            end_index=citation_data["end"],
            text=message["content"][citation_data["start"]:citation_data["end"]],
            document_id=citation_data.get("document_id"),
            url=citation_data.get("url"),
            title=citation_data.get("document_title")
        )
        citations.append(citation)
        
    return citations