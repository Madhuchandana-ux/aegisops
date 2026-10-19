from typing import Any

from sentence_transformers import CrossEncoder


class CrossEncoderReranker:

    def __init__(
        self,
        model_name: str = (
            "cross-encoder/ms-marco-MiniLM-L-6-v2"
        ),
    ):

        self.model_name = model_name

        self.model = CrossEncoder(
            model_name
        )

    def rerank(
        self,
        query: str,
        documents: list[dict[str, Any]],
        limit: int = 5,
    ) -> list[dict[str, Any]]:

        if not query or not query.strip():
            return []

        if not documents:
            return []

        # -----------------------------------------------------
        # Create query-document pairs
        # -----------------------------------------------------

        pairs = [
            (
                query,
                document["text"],
            )
            for document in documents
        ]

        # -----------------------------------------------------
        # Generate cross-encoder relevance scores
        # -----------------------------------------------------

        scores = self.model.predict(
            pairs
        )

        # -----------------------------------------------------
        # Attach reranking scores
        # -----------------------------------------------------

        reranked_documents = []

        for document, score in zip(
            documents,
            scores,
        ):

            result = dict(document)

            result[
                "reranker_score"
            ] = float(score)

            result[
                "reranker_model"
            ] = self.model_name

            reranked_documents.append(
                result
            )

        # -----------------------------------------------------
        # Sort by cross-encoder score
        # -----------------------------------------------------

        reranked_documents.sort(
            key=lambda document: document[
                "reranker_score"
            ],
            reverse=True,
        )

        return reranked_documents[:limit]