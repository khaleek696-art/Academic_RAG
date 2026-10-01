# Academic RAG Architecture Documentation

## System Layers
1. **Document Parsing & Page-Aware Chunking**: PyMuPDF page-aware text splitter.
2. **Dual Indexing**: Qdrant Vector Engine + BM25 Sparse Search.
3. **Hybrid Retrieval**: Reciprocal Rank Fusion (RRF).
4. **Cross-Encoder Reranking**: `ms-marco-MiniLM-L-6-v2`.
5. **Refusal Gate**: Confidence threshold safeguard.
6. **LLM Generation**: Google Gemini 2.5 Flash API + Citation Verification.
