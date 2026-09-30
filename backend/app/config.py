import os
from pathlib import Path
from pydantic_settings import BaseSettings

BASE_DIR = Path(__file__).resolve().parent.parent.parent

class Settings(BaseSettings):
    LLM_PROVIDER: str = "openai"
    LLM_API_KEY: str = ""
    LLM_MODEL: str = "gpt-4o-mini"

    EMBEDDING_MODEL: str = "sentence-transformers/all-MiniLM-L6-v2"
    RERANKER_MODEL: str = "cross-encoder/ms-marco-MiniLM-L-6-v2"

    CHUNK_SIZE: int = 600
    CHUNK_OVERLAP: int = 100
    BM25_TOP_K: int = 20
    DENSE_TOP_K: int = 20
    RERANK_TOP_K: int = 5
    CONFIDENCE_THRESHOLD: float = 0.35

    SQLITE_DB_PATH: str = "data/app.db"
    QDRANT_PATH: str = "data/qdrant_db"
    QDRANT_COLLECTION: str = "academic_chunks"
    BM25_INDEX_PATH: str = "data/bm25_index"
    UPLOAD_DIR: str = "data/raw"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        extra = "ignore"

settings = Settings()

def ensure_directories():
    for path_str in [settings.SQLITE_DB_PATH, settings.QDRANT_PATH, settings.BM25_INDEX_PATH, settings.UPLOAD_DIR]:
        p = Path(path_str)
        if p.suffix: # file path
            p.parent.mkdir(parents=True, exist_ok=True)
        else:
            p.mkdir(parents=True, exist_ok=True)
