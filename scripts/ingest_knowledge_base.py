from app.rag.ingestion import (
    ingest_knowledge_base,
)


def main():

    print("=" * 70)
    print("AegisOps Knowledge Base Ingestion")
    print("=" * 70)

    count = ingest_knowledge_base(
        recreate=True
    )

    print()
    print(
        f"Successfully indexed {count} "
        "knowledge-base documents."
    )

    print()
    print("Vector store:")
    print("Qdrant")

    print()
    print("Ingestion complete.")


if __name__ == "__main__":
    main()