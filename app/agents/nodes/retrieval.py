from pathlib import Path

from app.agents.state import AgentState
from app.rag.embeddings import EmbeddingModel
from app.rag.ingestion import build_documents
from app.rag.qdrant_store import QdrantStore
from app.rag.retrieval_pipeline import RetrievalPipeline


# ============================================================
# PROJECT PATH
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parents[3]


# ============================================================
# LAZY INITIALIZATION
# ============================================================
#
# We do NOT initialize the RAG models when this module is
# imported.
#
# They are loaded only when retrieval is actually needed.
#
# This makes application startup faster and makes testing
# easier.
# ============================================================

_retrieval_pipeline = None


def get_retrieval_pipeline() -> RetrievalPipeline:

    global _retrieval_pipeline

    if _retrieval_pipeline is not None:
        return _retrieval_pipeline

    print("Initializing AegisOps RAG retrieval pipeline...")

    # --------------------------------------------------------
    # Load embedding model
    # --------------------------------------------------------

    embedding_model = EmbeddingModel()

    # --------------------------------------------------------
    # Connect to existing Qdrant collection
    # --------------------------------------------------------

    qdrant_store = QdrantStore(
        vector_size=embedding_model.dimension
    )

    # --------------------------------------------------------
    # Load knowledge-base documents
    #
    # These documents are used by BM25.
    # Qdrant already contains their embeddings.
    # --------------------------------------------------------

    documents = build_documents()

    # --------------------------------------------------------
    # Create hybrid retrieval pipeline
    # --------------------------------------------------------

    _retrieval_pipeline = RetrievalPipeline(
        documents=documents,
        embedding_model=embedding_model,
        qdrant_store=qdrant_store,
    )

    print("RAG retrieval pipeline initialized.")

    return _retrieval_pipeline


# ============================================================
# LANGGRAPH RETRIEVAL NODE
# ============================================================

def retrieval_node(state: AgentState) -> AgentState:

    incident_text = state.get(
        "incident_text",
        "",
    ).strip()

    if not incident_text:

        state["retrieved_documents"] = []
        state["retrieval_scores"] = []

        state["errors"] = [
            "Incident description is empty."
        ]

        return state

    try:

        pipeline = get_retrieval_pipeline()

        # ----------------------------------------------------
        # Retrieve candidates
        # ----------------------------------------------------

        results = pipeline.search(
            query=incident_text,
            final_limit=3,
            candidate_limit=5,
        )

        # ----------------------------------------------------
        # Store retrieved documents in AgentState
        # ----------------------------------------------------

        state["retrieved_documents"] = results

        # ----------------------------------------------------
        # Store reranker scores separately
        # ----------------------------------------------------

        state["retrieval_scores"] = [
            float(
                result.get(
                    "reranker_score",
                    0.0,
                )
            )
            for result in results
        ]

        # ----------------------------------------------------
        # Increment graph step counter
        # ----------------------------------------------------

        state["step_count"] = (
            state.get("step_count", 0) + 1
        )

        return state

    except Exception as exc:

        state["retrieved_documents"] = []
        state["retrieval_scores"] = []

        state["errors"] = [
            f"Retrieval failed: {str(exc)}"
        ]

        return state