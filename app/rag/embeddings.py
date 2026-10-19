from sentence_transformers import SentenceTransformer


class EmbeddingModel:
    """
    Wrapper around the Sentence Transformers embedding model.

    This class converts text into dense numerical vectors
    that can be stored and searched in Qdrant.
    """

    def __init__(
        self,
        model_name: str = "sentence-transformers/all-MiniLM-L6-v2",
    ):
        self.model_name = model_name

        self.model = SentenceTransformer(
            model_name
        )

        self.dimension = (
            self.model.get_embedding_dimension()
        )

    def encode(
        self,
        texts: list[str],
    ) -> list[list[float]]:

        if not texts:
            return []

        embeddings = self.model.encode(
            texts,
            normalize_embeddings=True,
        )

        return embeddings.tolist()

    def encode_one(
        self,
        text: str,
    ) -> list[float]:

        if not text or not text.strip():
            raise ValueError(
                "Text cannot be empty."
            )

        return self.encode([text])[0]