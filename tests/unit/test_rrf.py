from app.rag.rrf import reciprocal_rank_fusion


def test_rrf_combines_results():

    dense_results = [
        {
            "kb_id": "KB001",
            "title": "VPN",
            "score": 0.9,
        },
        {
            "kb_id": "KB002",
            "title": "Password",
            "score": 0.8,
        },
    ]

    sparse_results = [
        {
            "kb_id": "KB002",
            "title": "Password",
            "score": 5.0,
        },
        {
            "kb_id": "KB001",
            "title": "VPN",
            "score": 4.0,
        },
    ]

    results = reciprocal_rank_fusion(
        result_lists=[
            dense_results,
            sparse_results,
        ],
        k=60,
        limit=2,
    )

    assert len(results) == 2

    ids = {
        result["kb_id"]
        for result in results
    }

    assert ids == {
        "KB001",
        "KB002",
    }


def test_rrf_document_found_by_both_systems():

    dense_results = [
        {
            "kb_id": "KB001",
            "title": "VPN",
        }
    ]

    sparse_results = [
        {
            "kb_id": "KB001",
            "title": "VPN",
        }
    ]

    results = reciprocal_rank_fusion(
        result_lists=[
            dense_results,
            sparse_results,
        ]
    )

    assert len(results) == 1

    assert (
        results[0]["retrieval_sources"]
        == []
    )


def test_rrf_empty_results():

    results = reciprocal_rank_fusion(
        result_lists=[
            [],
            [],
        ]
    )

    assert results == []