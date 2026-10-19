from pathlib import Path
from typing import Any

from qdrant_client import QdrantClient
from qdrant_client.models import (
    Distance,
    PointStruct,
    VectorParams,
)


PROJECT_ROOT = Path(__file__).resolve().parents[2]

QDRANT_PATH = (
    PROJECT_ROOT
    / "qdrant_storage"
)

COLLECTION_NAME = "aegisops_knowledge_base"


class QdrantStore:
    """
    Local Qdrant vector store for AegisOps knowledge documents.
    """

    def __init__(
        self,
        path: Path = QDRANT_PATH,
        collection_name: str = COLLECTION_NAME,
        vector_size: int = 384,
    ):

        self.path = Path(path)

        self.collection_name = (
            collection_name
        )

        self.vector_size = vector_size

        self.path.mkdir(
            parents=True,
            exist_ok=True,
        )

        self.client = QdrantClient(
            path=str(self.path)
        )

    def create_collection(
        self,
        recreate: bool = False,
    ) -> None:

        collections = (
            self.client.get_collections()
            .collections
        )

        existing_names = {
            collection.name
            for collection in collections
        }

        if (
            self.collection_name
            in existing_names
        ):

            if recreate:

                self.client.delete_collection(
                    self.collection_name
                )

            else:

                return

        self.client.create_collection(
            collection_name=(
                self.collection_name
            ),
            vectors_config=VectorParams(
                size=self.vector_size,
                distance=Distance.COSINE,
            ),
        )

    def upsert_documents(
        self,
        documents: list[dict[str, Any]],
    ) -> None:

        points = []

        for index, document in enumerate(
            documents
        ):

            points.append(
                PointStruct(
                    id=index + 1,
                    vector=document["embedding"],
                    payload={
                        key: value
                        for key, value
                        in document.items()
                        if key != "embedding"
                    },
                )
            )

        if not points:
            return

        self.client.upsert(
            collection_name=(
                self.collection_name
            ),
            points=points,
        )

    def search(
        self,
        query_vector: list[float],
        limit: int = 5,
    ) -> list[dict[str, Any]]:

        results = self.client.query_points(
            collection_name=(
                self.collection_name
            ),
            query=query_vector,
            limit=limit,
        ).points

        return [
            {
                "id": result.id,
                "score": result.score,
                **result.payload,
            }
            for result in results
        ]