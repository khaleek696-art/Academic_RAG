from typing import List, Dict, Any, Optional
from backend.app.services.bm25_index import bm25_service
from backend.app.services.vector_index import qdrant_service
from backend.app.config import settings

class HybridRetriever:
    """Merges BM25 lexical search and Qdrant dense vector search using Reciprocal Rank Fusion (RRF)."""

    def __init__(self, k_rrf: int = 60):
        self.k_rrf = k_rrf

    def retrieve(self, query: str, subject_id: Optional[int] = None, top_k: int = 20) -> List[Dict[str, Any]]:
        # 1. Lexical BM25 Search
        bm25_results = bm25_service.search(query, top_k=top_k, subject_id=subject_id)

        # 2. Dense Vector Qdrant Search
        qdrant_results = qdrant_service.search(query, top_k=top_k, subject_id=subject_id)

        # 3. Reciprocal Rank Fusion (RRF)
        rrf_scores = {}
        chunk_metadata = {}

        for rank, item in enumerate(bm25_results, start=1):
            key = (item["filename"], item["page"], item["text"][:50])
            score = 1.0 / (self.k_rrf + rank)
            rrf_scores[key] = rrf_scores.get(key, 0.0) + score
            chunk_metadata[key] = item

        for rank, item in enumerate(qdrant_results, start=1):
            key = (item["filename"], item["page"], item["text"][:50])
            score = 1.0 / (self.k_rrf + rank)
            rrf_scores[key] = rrf_scores.get(key, 0.0) + score
            chunk_metadata[key] = item

        # Sort combined results by RRF score
        sorted_keys = sorted(rrf_scores.keys(), key=lambda k: rrf_scores[k], reverse=True)

        final_candidates = []
        for key in sorted_keys[:top_k]:
            item = dict(chunk_metadata[key])
            item["rrf_score"] = rrf_scores[key]
            final_candidates.append(item)

        return final_candidates

hybrid_retriever = HybridRetriever()
