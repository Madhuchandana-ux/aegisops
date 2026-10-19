from typing import Any, TypedDict

class AgentState(TypedDict, total=False):
    incident_id: str
    incident_text: str
    caller: str

    username: str
    user_role: str

    prompt_injection_detected: bool
    prompt_injection_risk: str
    prompt_injection_patterns: list[str]

    category: str
    subcategory: str
    servicenow_sys_id: str
    action_name: str
    action_executed: bool
    username: str
    user_role: str

    # ML classification information
    classification_confidence: float
    classification_model: str

    priority: str

    retrieved_documents: list[dict[str, Any]]
    retrieval_scores: list[float]

    analysis: str
    proposed_resolution: str
    reasoning_summary: str

    confidence: float
    risk_level: str
    requires_human: bool

    policy_allowed: bool
    policy_reason: str

    selected_action: str

    action_result: dict[str, Any]
    verification_result: dict[str, Any]

    final_response: str

    run_id: str
    step_count: int
    errors: list[str]