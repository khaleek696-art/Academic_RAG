import pickle
from pathlib import Path
from typing import List, Dict, Any
from backend.app.config import settings

class BM25Service:
    """Lexical keyword retrieval using rank_bm25."""

    def __init__(self):
        self.index_dir = Path(settings.BM25_INDEX_PATH)
        self.index_dir.mkdir(parents=True, exist_ok=True)
        self.index_file = self.index_dir / "bm25.pkl"
        self.bm25 = None
        self.corpus_chunks = []
        self._load_index()

    def _tokenize(self, text: str) -> List[str]:
        return text.lower().split()

    def _load_index(self):
        if self.index_file.exists():
            try:
                with open(self.index_file, "rb") as f:
                    data = pickle.load(f)
                    self.bm25 = data.get("bm25")
                    self.corpus_chunks = data.get("chunks", [])
            except Exception as e:
                print(f"Warning loading BM25 index: {str(e)}")

    def build_index(self, chunks: List[Dict[str, Any]]):
        if not chunks:
            return

        self.corpus_chunks = chunks
        tokenized_corpus = [self._tokenize(c["text"]) for c in chunks]

        try:
            from rank_bm25 import BM25Okapi
            self.bm25 = BM25Okapi(tokenized_corpus)
            with open(self.index_file, "wb") as f:
                pickle.dump({"bm25": self.bm25, "chunks": self.corpus_chunks}, f)
            print(f"✅ Indexed {len(chunks)} chunks in BM25 index.")
        except Exception as e:
            print(f"Error building BM25 index: {str(e)}")

    def search(self, query: str, top_k: int = None, subject_id: int = None) -> List[Dict[str, Any]]:
        k = top_k or settings.BM25_TOP_K
        if not self.bm25 or not self.corpus_chunks:
            return []

        tokenized_query = self._tokenize(query)
        scores = self.bm25.get_scores(tokenized_query)

        scored_chunks = []
        for idx, score in enumerate(scores):
            chunk = self.corpus_chunks[idx]
            if subject_id is not None and chunk.get("subject_id") != subject_id:
                continue
            scored_chunks.append({
                "score": float(score),
                "document_id": chunk.get("document_id"),
                "subject_id": chunk.get("subject_id"),
                "filename": chunk.get("filename"),
                "page": chunk.get("page"),
                "text": chunk.get("text", "")
            })

        scored_chunks.sort(key=lambda x: x["score"], reverse=True)
        return scored_chunks[:k]

bm25_service = BM25Service()
