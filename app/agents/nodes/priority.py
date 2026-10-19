from app.agents.state import AgentState


HIGH_PRIORITY_KEYWORDS = {
    "production down",
    "production outage",
    "entire system down",
    "all users affected",
    "critical outage",
    "database down",
    "server down",
    "security breach",
    "data breach",
}

MEDIUM_PRIORITY_KEYWORDS = {
    "multiple users",
    "cannot access",
    "unable to access",
    "service unavailable",
    "application unavailable",
    "repeatedly failing",
}


def priority_node(state: AgentState) -> AgentState:
    """
    Determine incident priority using deterministic rules.

    This is intentionally kept separate from the LLM so that
    priority assignment remains auditable and predictable.
    """

    incident_text = state.get("incident_text", "").strip().lower()

    if not incident_text:
        state["priority"] = "P3"
        state["step_count"] = state.get("step_count", 0) + 1
        return state

    for keyword in HIGH_PRIORITY_KEYWORDS:
        if keyword in incident_text:
            state["priority"] = "P1"
            state["step_count"] = state.get("step_count", 0) + 1
            return state

    for keyword in MEDIUM_PRIORITY_KEYWORDS:
        if keyword in incident_text:
            state["priority"] = "P2"
            state["step_count"] = state.get("step_count", 0) + 1
            return state

    state["priority"] = "P3"
    state["step_count"] = state.get("step_count", 0) + 1

    return state