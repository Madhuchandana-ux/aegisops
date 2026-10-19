
from app.agents.state import AgentState
from app.security.policy import evaluate_policy


# ============================================================
# CONTROLLED SERVICE NOW ACTIONS
# ============================================================

ALLOWED_ACTIONS = {
    "add_work_note",
    "resolve_incident",
}


def select_controlled_action(proposed_action):
    """
    Return only explicitly recognized ServiceNow actions.
    Unknown proposals return None.
    """
    if not isinstance(proposed_action, str):
        return None

    normalized_action = proposed_action.strip().lower()

    if not normalized_action:
        return None

    if any(
        phrase in normalized_action
        for phrase in (
            "resolve incident",
            "resolve the incident",
            "close incident",
            "close the incident",
        )
    ):
        return "resolve_incident"

    if any(
        phrase in normalized_action
        for phrase in (
            "add work note",
            "add a work note",
            "record a work note",
            "document troubleshooting",
        )
    ):
        return "add_work_note"

    return None


# ============================================================
# DECISION NODE
# ============================================================

def decision_node(state: AgentState) -> AgentState:
    classification_confidence = state.get(
        "classification_confidence",
        0.0,
    )
    reasoning_confidence = state.get("confidence", 0.0)
    priority = state.get("priority", "P3")
    risk_level = state.get("risk_level", "LOW")
    proposed_action = state.get("proposed_resolution", "")
    retrieved_documents = state.get("retrieved_documents", [])

    # Evaluate policy.
    policy_decision = evaluate_policy(
        classification_confidence=classification_confidence,
        reasoning_confidence=reasoning_confidence,
        priority=priority,
        risk_level=risk_level,
        proposed_action=proposed_action,
        has_retrieved_evidence=bool(retrieved_documents),
        prompt_injection_detected=state.get(
            "prompt_injection_detected",
            False,
        ),
    )

    # Save the original policy result.
    state["policy_allowed"] = policy_decision.allowed
    state["policy_reason"] = policy_decision.reason
    state["risk_level"] = policy_decision.risk_level
    state["requires_human"] = policy_decision.requires_human

    # Choose the next action safely.
    if policy_decision.requires_human:
        state["selected_action"] = "request_human_approval"
        state["action_name"] = ""

    elif not policy_decision.allowed:
        state["selected_action"] = "blocked"
        state["action_name"] = ""

    else:
        action_name = select_controlled_action(proposed_action)

        if action_name not in ALLOWED_ACTIONS:
            # Policy passed, but the proposed action is unknown.
            # Preserve policy_allowed and require human review.
            state["requires_human"] = True
            state["selected_action"] = "request_human_approval"
            state["action_name"] = ""
            state["policy_reason"] = (
                "The proposed action is not explicitly recognized. "
                "Human review is required."
            )
        else:
            state["selected_action"] = "automated_resolution"
            state["action_name"] = action_name

    # Add the decision explanation to the summary.
    state["reasoning_summary"] = (
        state.get("reasoning_summary", "")
        + "\n\nPolicy decision: "
        + state["policy_reason"]
    )

    state["step_count"] = state.get("step_count", 0) + 1

    return state
