import os
from typing import List, Dict, Any, Optional
from pathlib import Path
from backend.app.config import settings

class QdrantVectorService:
    """Qdrant Vector Database service handling local embedding storage and metadata filtering."""

    def __init__(self):
        self.qdrant_path = settings.QDRANT_PATH
        self.collection_name = settings.QDRANT_COLLECTION
        self.embedding_model_name = settings.EMBEDDING_MODEL
        self._client = None
        self._embedder = None
        self.vector_dim = 384 # Default dimension for all-MiniLM-L6-v2

    @property
    def client(self):
        if self._client is None:
            try:
                from qdrant_client import QdrantClient
                Path(self.qdrant_path).mkdir(parents=True, exist_ok=True)
                self._client = QdrantClient(path=self.qdrant_path)
                self._ensure_collection()
            except Exception as e:
                print(f"Warning: Qdrant client initialization: {str(e)}")
                self._client = None
        return self._client

    @property
    def embedder(self):
        if self._embedder is None:
            try:
                from sentence_transformers import SentenceTransformer
                self._embedder = SentenceTransformer(self.embedding_model_name)
            except Exception as e:
                print(f"Warning: Loading SentenceTransformer: {str(e)}")
                self._embedder = None
        return self._embedder

    def _ensure_collection(self):
        if not self.client:
            return
        try:
            from qdrant_client.http import models
            collections = [c.name for c in self.client.get_collections().collections]
            if self.collection_name not in collections:
                self.client.create_collection(
                    collection_name=self.collection_name,
                    vectors_config=models.VectorParams(
                        size=self.vector_dim,
                        distance=models.Distance.COSINE
                    )
                )
                print(f"✅ Qdrant Collection '{self.collection_name}' created successfully!")
        except Exception as e:
            print(f"Error ensuring collection: {str(e)}")

    def _get_embedding(self, text: str) -> List[float]:
        if self.embedder:
            return self.embedder.encode(text).tolist()
        else:
            # Deterministic mock fallback vector of dim 384 if sentence-transformers model downloading/offline
            import hashlib
            val = int(hashlib.md5(text.encode()).hexdigest(), 16)
            return [((val >> (i % 32)) & 1) * 0.1 for i in range(384)]

    def add_chunks(self, chunks: List[Dict[str, Any]]) -> List[int]:
        if not chunks:
            return []

        if not self.client:
            return [c.get("chunk_index", idx) for idx, c in enumerate(chunks)]

        try:
            from qdrant_client.http import models
            points = []
            for idx, c in enumerate(chunks):
                point_id = c.get("id") or (c["document_id"] * 10000 + c["chunk_index"])
                vec = self._get_embedding(c["text"])

                payload = {
                    "document_id": c["document_id"],
                    "subject_id": c["subject_id"],
                    "filename": c["filename"],
                    "page": c["page"],
                    "text": c["text"]
                }

                points.append(
                    models.PointStruct(
                        id=point_id,
                        vector=vec,
                        payload=payload
                    )
                )

            self.client.upsert(
                collection_name=self.collection_name,
                points=points
            )
            print(f"✅ Indexed {len(points)} chunks into Qdrant Vector Store.")
            return [p.id for p in points]
        except Exception as e:
            print(f"Error indexing to Qdrant: {str(e)}")
            return []

    def search(self, query: str, top_k: int = None, subject_id: Optional[int] = None) -> List[Dict[str, Any]]:
        k = top_k or settings.DENSE_TOP_K
        query_vector = self._get_embedding(query)

        if not self.client:
            return []

        try:
            from qdrant_client.http import models
            query_filter = None
            if subject_id is not None:
                query_filter = models.Filter(
                    must=[
                        models.FieldCondition(
                            key="subject_id",
                            match=models.MatchValue(value=subject_id)
                        )
                    ]
                )

            results = []
            if hasattr(self.client, "query_points"):
                res = self.client.query_points(
                    collection_name=self.collection_name,
                    query=query_vector,
                    query_filter=query_filter,
                    limit=k
                )
                results = res.points
            elif hasattr(self.client, "search"):
                results = self.client.search(
                    collection_name=self.collection_name,
                    query_vector=query_vector,
                    query_filter=query_filter,
                    limit=k
                )

            hits = []
            for r in results:
                payload = r.payload or {}
                hits.append({
                    "score": getattr(r, "score", 0.0),
                    "document_id": payload.get("document_id"),
                    "subject_id": payload.get("subject_id"),
                    "filename": payload.get("filename"),
                    "page": payload.get("page"),
                    "text": payload.get("text", "")
                })
            return hits
        except Exception as e:
            print(f"Error searching Qdrant: {str(e)}")
            return []

qdrant_service = QdrantVectorService()
