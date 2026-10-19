from typing import Any


def reciprocal_rank_fusion(
    result_lists: list[list[dict[str, Any]]],
    k: int = 60,
    limit: int = 10,
) -> list[dict[str, Any]]:
    """
    Combine multiple ranked retrieval result lists
    using Reciprocal Rank Fusion (RRF).

    RRF formula:

        RRF(d) = Σ 1 / (k + rank)

    where:
        d    = document
        rank = document's rank in a retrieval list
        k    = smoothing constant
    """

    fused_documents: dict[str, dict[str, Any]] = {}

    # ---------------------------------------------------------
    # Process every retrieval system
    # ---------------------------------------------------------
    for result_list in result_lists:

        # Ranks start at 1, not 0.
        for rank, document in enumerate(
            result_list,
            start=1,
        ):

            document_id = str(
                document["kb_id"]
            )

            # Create the document entry
            # the first time we encounter it.
            if document_id not in fused_documents:

                fused_documents[document_id] = {
                    **document,
                    "rrf_score": 0.0,
                    "retrieval_sources": [],
                }

            # -------------------------------------------------
            # Add the RRF contribution
            # -------------------------------------------------
            fused_documents[
                document_id
            ]["rrf_score"] += (
                1.0 / (k + rank)
            )

            # Track which retrieval systems found it.
            source = document.get(
                "retrieval_source"
            )

            if (
                source
                and source
                not in fused_documents[
                    document_id
                ]["retrieval_sources"]
            ):

                fused_documents[
                    document_id
                ]["retrieval_sources"].append(
                    source
                )

    # ---------------------------------------------------------
    # Sort by fused RRF score
    # ---------------------------------------------------------
    ranked_documents = sorted(
        fused_documents.values(),
        key=lambda document: document[
            "rrf_score"
        ],
        reverse=True,
    )

    return ranked_documents[:limit]