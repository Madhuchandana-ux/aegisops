from app.rag.reranker import CrossEncoderReranker


def test_reranker_returns_empty_for_empty_documents():

    reranker = CrossEncoderReranker()

    results = reranker.rerank(
        query="VPN problem",
        documents=[],
        limit=3,
    )

    assert results == []


def test_reranker_rejects_empty_query():

    reranker = CrossEncoderReranker()

    documents = [
        {
            "kb_id": "KB001",
            "title": "VPN Troubleshooting",
            "text": (
                "Troubleshoot corporate VPN "
                "connection problems."
            ),
        }
    ]

    results = reranker.rerank(
        query="",
        documents=documents,
        limit=3,
    )

    assert results == []