from typing import List, Dict, Any
from backend.app.config import settings

class CrossEncoderReranker:
    """Reranks candidate chunks using cross-encoder/ms-marco-MiniLM-L-6-v2."""

    def __init__(self):
        self.model_name = settings.RERANKER_MODEL
        self._reranker = None

    @property
    def reranker(self):
        if self._reranker is None:
            try:
                from sentence_transformers import CrossEncoder
                self._reranker = CrossEncoder(self.model_name)
            except Exception as e:
                print(f"Warning loading CrossEncoder: {str(e)}")
                self._reranker = None
        return self._reranker

    def rerank(self, query: str, candidates: List[Dict[str, Any]], top_k: int = None) -> List[Dict[str, Any]]:
        k = top_k or settings.RERANK_TOP_K
        if not candidates:
            return []

        if self.reranker:
            pairs = [[query, item["text"]] for item in candidates]
            scores = self.reranker.predict(pairs)
            for idx, score in enumerate(scores):
                candidates[idx]["confidence_score"] = float(score)
        else:
            # Fallback score if cross-encoder loading
            for item in candidates:
                item["confidence_score"] = item.get("rrf_score", 0.5) * 10

        candidates.sort(key=lambda x: x["confidence_score"], reverse=True)
        return candidates[:k]

reranker = CrossEncoderReranker()
