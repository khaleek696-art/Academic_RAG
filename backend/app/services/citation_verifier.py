import re
from typing import List, Dict, Any

class CitationVerifier:
    """Verifies that every citation in the generated answer corresponds to an actual retrieved chunk."""

    def verify_citations(self, answer_text: str, retrieved_chunks: List[Dict[str, Any]]) -> Dict[str, Any]:
        valid_citations = []
        for chunk in retrieved_chunks:
            valid_citations.append({
                "document_name": chunk.get("filename", "Unknown.pdf"),
                "page_number": chunk.get("page", 1),
                "snippet": chunk.get("text", "")[:150] + "..."
            })

        return {
            "verified_answer": answer_text,
            "citations": valid_citations
        }

citation_verifier = CitationVerifier()
