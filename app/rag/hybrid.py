from typing import Any

from app.rag.bm25 import BM25Retriever
from app.rag.embeddings import EmbeddingModel
from app.rag.qdrant_store import QdrantStore
from app.rag.rrf import reciprocal_rank_fusion


class HybridRetriever:

    def __init__(
        self,
        documents: list[dict[str, Any]],
        embedding_model: EmbeddingModel,
        qdrant_store: QdrantStore,
    ):

        self.documents = documents

        self.embedding_model = (
            embedding_model
        )

        self.qdrant_store = qdrant_store

        self.bm25 = BM25Retriever(
            documents
        )

    def search(
        self,
        query: str,
        limit: int = 5,
        candidate_limit: int = 5,
    ) -> list[dict[str, Any]]:

        if not query or not query.strip():
            return []

        # =====================================================
        # DENSE RETRIEVAL
        # =====================================================

        query_vector = (
            self.embedding_model.encode_one(
                query
            )
        )

        dense_results = (
            self.qdrant_store.search(
                query_vector=query_vector,
                limit=candidate_limit,
            )
        )

        # Mark the retrieval source.
        for result in dense_results:
            result[
                "retrieval_source"
            ] = "dense"

        # =====================================================
        # SPARSE RETRIEVAL
        # =====================================================

        sparse_results = (
            self.bm25.search(
                query=query,
                limit=candidate_limit,
            )
        )

        # Mark the retrieval source.
        for result in sparse_results:
            result[
                "retrieval_source"
            ] = "sparse"

        # =====================================================
        # RRF FUSION
        # =====================================================

        fused_results = reciprocal_rank_fusion(
            result_lists=[
                dense_results,
                sparse_results,
            ],
            k=60,
            limit=limit,
        )

        return fused_results