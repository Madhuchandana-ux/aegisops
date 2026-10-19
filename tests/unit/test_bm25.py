from app.rag.bm25 import BM25Retriever


def create_test_documents():

    return [
        {
            "kb_id": "KB001",
            "title": "VPN Troubleshooting",
            "content": (
                "Troubleshoot corporate VPN "
                "connection problems."
            ),
            "category": "network",
            "source": "test",
            "text": (
                "Title: VPN Troubleshooting "
                "Category: network "
                "Troubleshoot corporate VPN "
                "connection problems."
            ),
        },
        {
            "kb_id": "KB002",
            "title": "Password Reset",
            "content": (
                "Reset a forgotten corporate password."
            ),
            "category": "access",
            "source": "test",
            "text": (
                "Title: Password Reset "
                "Category: access "
                "Reset a forgotten corporate password."
            ),
        },
    ]


def test_bm25_returns_results():

    documents = create_test_documents()

    retriever = BM25Retriever(
        documents
    )

    results = retriever.search(
        "VPN connection problem",
        limit=2,
    )

    assert len(results) > 0


def test_bm25_retrieves_relevant_document():

    documents = create_test_documents()

    retriever = BM25Retriever(
        documents
    )

    results = retriever.search(
        "VPN connection problem",
        limit=1,
    )

    assert results[0]["kb_id"] == "KB001"


def test_bm25_empty_query():

    documents = create_test_documents()

    retriever = BM25Retriever(
        documents
    )

    results = retriever.search(
        "",
        limit=5,
    )

    assert results == []