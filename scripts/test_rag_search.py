from app.rag.embeddings import EmbeddingModel
from app.rag.qdrant_store import QdrantStore


def main():

    print("=" * 70)
    print("AegisOps Dense RAG Search Test")
    print("=" * 70)

    query = (
        "User cannot connect to the corporate VPN "
        "from home."
    )

    print()
    print(f"Query: {query}")

    embedding_model = EmbeddingModel()

    store = QdrantStore(
        vector_size=embedding_model.dimension
    )

    query_vector = (
        embedding_model.encode_one(
            query
        )
    )

    results = store.search(
        query_vector=query_vector,
        limit=3,
    )

    print()
    print("Top results:")
    print("-" * 70)

    for rank, result in enumerate(
        results,
        start=1,
    ):

        print(
            f"{rank}. "
            f"{result['kb_id']} | "
            f"{result['title']}"
        )

        print(
            f"   Score: "
            f"{result['score']:.4f}"
        )

        print(
            f"   Category: "
            f"{result['category']}"
        )

        print()

    print("=" * 70)


if __name__ == "__main__":
    main()