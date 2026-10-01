"""
BM25 Lexical Engine Interface
"""
from backend.app.services.bm25_index import BM25IndexService, get_bm25_service

__all__ = ["BM25IndexService", "get_bm25_service"]
