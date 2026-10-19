from app.ml.data_loader import load_knowledge_base
from app.rag.bm25 import BM25Retriever


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
    print("AegisOps BM25 Sparse Retrieval Test")
    print("=" * 70)

    documents = build_documents()

    retriever = BM25Retriever(
        documents
    )

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
    )

    print("Top BM25 results:")
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