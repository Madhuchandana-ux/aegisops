import re
from typing import Any


class BM25Retriever:

    def __init__(
        self,
        documents: list[dict[str, Any]],
    ):
        self.documents = documents

        self.tokenized_documents = [
            self._tokenize(
                document["text"]
            )
            for document in documents
        ]

        from rank_bm25 import BM25Okapi

        self.bm25 = BM25Okapi(
            self.tokenized_documents
        )

    @staticmethod
    def _tokenize(
        text: str,
    ) -> list[str]:

        text = text.lower()

        tokens = re.findall(
            r"\b[a-zA-Z0-9]+\b",
            text,
        )

        return tokens

    def search(
        self,
        query: str,
        limit: int = 5,
    ) -> list[dict[str, Any]]:

        if not query or not query.strip():
            return []

        query_tokens = self._tokenize(
            query
        )

        if not query_tokens:
            return []

        scores = self.bm25.get_scores(
            query_tokens
        )

        ranked_indices = sorted(
            range(len(scores)),
            key=lambda index: scores[index],
            reverse=True,
        )

        results = []

        for index in ranked_indices[:limit]:

            document = self.documents[index]

            results.append(
                {
                    "kb_id": document["kb_id"],
                    "title": document["title"],
                    "content": document["content"],
                    "category": document["category"],
                    "source": document["source"],
                    "text": document["text"],
                    "score": float(
                        scores[index]
                    ),
                }
            )

        return results