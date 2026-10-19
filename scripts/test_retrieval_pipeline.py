from app.ml.data_loader import load_knowledge_base
from app.rag.embeddings import EmbeddingModel
from app.rag.qdrant_store import QdrantStore
from app.rag.retrieval_pipeline import RetrievalPipeline


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
    print("AegisOps End-to-End Retrieval Pipeline")
    print("=" * 70)

    # ---------------------------------------------------------
    # Load documents
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
    # Initialize complete retrieval pipeline
    # ---------------------------------------------------------

    pipeline = RetrievalPipeline(
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

    # ---------------------------------------------------------
    # Execute pipeline
    # ---------------------------------------------------------

    results = pipeline.search(
        query=query,
        final_limit=3,
        candidate_limit=5,
    )

    print()
    print("Final re-ranked results:")
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
            f"{result.get('rrf_score', 0):.6f}"
        )

        print(
            f"   Cross-Encoder Score: "
            f"{result['reranker_score']:.4f}"
        )

        print(
            f"   Sources: "
            f"{', '.join(result.get('retrieval_sources', []))}"
        )

        print(
            f"   Category: "
            f"{result['category']}"
        )

        print()

    print("=" * 70)


if __name__ == "__main__":
    main()