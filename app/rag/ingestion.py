from app.ml.data_loader import load_knowledge_base
from app.rag.embeddings import EmbeddingModel
from app.rag.qdrant_store import QdrantStore


def build_documents() -> list[dict]:
    """
    Load the knowledge base, generate embeddings,
    and prepare documents for Qdrant.
    """

    df = load_knowledge_base()

    embedding_model = EmbeddingModel()

    documents = []
    texts = []

    # ---------------------------------------------------------
    # Step 1: Create the text that will be embedded
    # ---------------------------------------------------------
    for _, row in df.iterrows():

        text = (
            f"Title: {row['title']}\n"
            f"Category: {row['category']}\n"
            f"Content: {row['content']}"
        )

        texts.append(text)

    # ---------------------------------------------------------
    # Step 2: Generate dense embeddings
    # ---------------------------------------------------------
    embeddings = embedding_model.encode(texts)

    # ---------------------------------------------------------
    # Step 3: Build Qdrant documents
    # ---------------------------------------------------------
    for index, (_, row) in enumerate(df.iterrows()):

        documents.append(
            {
                "kb_id": str(row["document_id"]),
                "title": str(row["title"]),
                "content": str(row["content"]),
                "category": str(row["category"]),
                "source": str(row["source"]),
                "text": texts[index],
                "embedding": embeddings[index],
            }
        )

    return documents


def ingest_knowledge_base(
    recreate: bool = True,
) -> int:
    """
    Generate embeddings for the knowledge base
    and store them in Qdrant.
    """

    documents = build_documents()

    embedding_model = EmbeddingModel()

    store = QdrantStore(
        vector_size=embedding_model.dimension
    )

    store.create_collection(
        recreate=recreate
    )

    store.upsert_documents(
        documents
    )

    return len(documents)