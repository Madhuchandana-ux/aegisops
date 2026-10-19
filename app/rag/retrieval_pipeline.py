from typing import Any

from app.rag.embeddings import EmbeddingModel
from app.rag.hybrid import HybridRetriever
from app.rag.qdrant_store import QdrantStore
from app.rag.reranker import CrossEncoderReranker


class RetrievalPipeline:

    def __init__(
        self,
        documents: list[dict[str, Any]],
        embedding_model: EmbeddingModel,
        qdrant_store: QdrantStore,
    ):

        self.hybrid_retriever = (
            HybridRetriever(
                documents=documents,
                embedding_model=embedding_model,
                qdrant_store=qdrant_store,
            )
        )

        self.reranker = (
            CrossEncoderReranker()
        )

    def search(
        self,
        query: str,
        final_limit: int = 3,
        candidate_limit: int = 5,
    ) -> list[dict[str, Any]]:

        if not query or not query.strip():
            return []

        # =====================================================
        # STEP 1 — Hybrid retrieval
        # =====================================================

        candidates = (
            self.hybrid_retriever.search(
                query=query,
                limit=candidate_limit,
                candidate_limit=candidate_limit,
            )
        )

        if not candidates:
            return []

        # =====================================================
        # STEP 2 — Cross-encoder re-ranking
        # =====================================================

        final_results = (
            self.reranker.rerank(
                query=query,
                documents=candidates,
                limit=final_limit,
            )
        )

        return final_results
