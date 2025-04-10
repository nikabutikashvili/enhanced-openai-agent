from typing import List, Dict, Any
from .citation_parser import Citation, parse_citations


def highlight_citations(text: str, citations: List[Citation]) -> str:
    sorted_citations = sorted(citations, key=lambda c: c.start_index, reverse=True)
    
    for citation in sorted_citations:
        if citation.url:
            citation_marker = f" [{citation.url}]"
        elif citation.title:
            citation_marker = f" [{citation.title}]"
        else:
            citation_marker = f" [Citation: {citation.document_id}]"
            
        text = (
            text[:citation.end_index] + 
            citation_marker +
            text[citation.end_index:]
        )
    
    return text


def format_message_with_citations(message: Dict[str, Any]) -> str:
    if not message.get("content"):
        return ""
        
    text = message["content"]
    citations = parse_citations(message)
    
    if not citations:
        return text
        
    return highlight_citations(text, citations)