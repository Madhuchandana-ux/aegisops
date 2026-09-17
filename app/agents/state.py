from typing import Any, TypedDict


class AgentState(TypedDict, total=False):
    """
    Shared state passed between AegisOps agent nodes.
    """

    # -------------------------
    # Incident information
    # -------------------------

    incident_id: str
    incident_text: str
    caller: str

    # -------------------------
    # Classification
    # -------------------------

    category: str
    subcategory: str
    priority: str

    # -------------------------
    # Retrieval
    # -------------------------

    retrieved_documents: list[dict[str, Any]]
    retrieval_scores: list[float]

    # -------------------------
    # LLM analysis
    # -------------------------

    analysis: str
    proposed_resolution: str
    reasoning_summary: str

    # -------------------------
    # Confidence and risk
    # -------------------------

    confidence: float
    risk_level: str
    requires_human: bool

    # -------------------------
    # Action
    # -------------------------

    selected_action: str
    action_result: dict[str, Any]

    # -------------------------
    # Verification
    # -------------------------

    verification_result: dict[str, Any]

    # -------------------------
    # Final response
    # -------------------------

    final_response: str

    # -------------------------
    # Operational metadata
    # -------------------------

    run_id: str
    step_count: int
    errors: list[str]