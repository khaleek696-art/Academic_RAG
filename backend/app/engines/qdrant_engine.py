"""
Qdrant Vector Engine Interface
"""
from backend.app.services.vector_index import VectorIndexService, get_vector_service

__all__ = ["VectorIndexService", "get_vector_service"]
