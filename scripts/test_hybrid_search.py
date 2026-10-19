from app.ml.data_loader import load_knowledge_base
from app.rag.embeddings import EmbeddingModel
from app.rag.hybrid import HybridRetriever
from app.rag.qdrant_store import QdrantStore


def build_documents() -> list[dict]:

    df = load_knowledge_base()

    documents = []

    for _, row in df.iterrows():

        text = (
            f"Title: {row['title']}\n"
            f"Category: {row['category']}\n"
            f"Content: {row['content']}"
        )

        documents.append(
            {
                "kb_id": str(
                    row["document_id"]
                ),
                "title": str(
                    row["title"]
                ),
                "content": str(
                    row["content"]
                ),
                "category": str(
                    row["category"]
                ),
                "source": str(
                    row["source"]
                ),
                "text": text,
            }
        )

    return documents


def main():

    print("=" * 70)
    print("AegisOps Hybrid RAG Test")
    print("=" * 70)

    # ---------------------------------------------------------
    # Load knowledge base
    # ---------------------------------------------------------

    documents = build_documents()

    print()
    print(
        f"Knowledge-base documents: "
        f"{len(documents)}"
    )

    # ---------------------------------------------------------
    # Initialize embedding model
    # ---------------------------------------------------------

    embedding_model = EmbeddingModel()

    # ---------------------------------------------------------
    # Initialize Qdrant
    # ---------------------------------------------------------

    qdrant_store = QdrantStore(
        vector_size=embedding_model.dimension
    )

    # ---------------------------------------------------------
    # Initialize hybrid retriever
    # ---------------------------------------------------------

    retriever = HybridRetriever(
        documents=documents,
        embedding_model=embedding_model,
        qdrant_store=qdrant_store,
    )

    # ---------------------------------------------------------
    # Test query
    # ---------------------------------------------------------

    query = (
        "User cannot connect to the "
        "corporate VPN from home."
    )

    print()
    print(f"Query: {query}")
    print()

    results = retriever.search(
        query=query,
        limit=5,
        candidate_limit=5,
    )

    print("Hybrid retrieval results:")
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
            f"   RRF Score: "
            f"{result['rrf_score']:.6f}"
        )

        print(
            f"   Retrieval sources: "
            f"{', '.join(result['retrieval_sources'])}"
        )

        print(
            f"   Category: "
            f"{result['category']}"
        )

        print()

    print("=" * 70)


if __name__ == "__main__":
    main()