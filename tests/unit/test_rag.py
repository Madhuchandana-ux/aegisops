from app.rag.embeddings import EmbeddingModel
from app.rag.qdrant_store import QdrantStore


def test_embedding_dimension():

    model = EmbeddingModel()

    assert model.dimension == 384


def test_single_embedding():

    model = EmbeddingModel()

    vector = model.encode_one(
        "VPN connection is failing."
    )

    assert len(vector) == 384


def test_empty_embedding_rejected():

    model = EmbeddingModel()

    try:
        model.encode_one("")

    except ValueError:
        return

    assert False, (
        "Expected ValueError for empty text."
    )

def test_qdrant_store_creation(tmp_path):
    store = QdrantStore(
        path=tmp_path / "qdrant_test_storage",
        collection_name="test_collection",
    )

    assert store.client is not None
    assert store.collection_name == "test_collection"
    assert store.vector_size == 384