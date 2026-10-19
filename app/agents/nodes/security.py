
from app.agents.state import AgentState
from app.security.prompt_injection import (
    detect_prompt_injection,
)


def prompt_injection_node(
    state: AgentState,
) -> AgentState:
    """
    Inspect incident text for prompt-injection patterns.

    Important:
    This node does not attempt to determine the user's
    intent. It only identifies suspicious instruction-like
    patterns.

    Detected content remains untrusted.
    """

    incident_text = state.get(
        "incident_text",
        "",
    )

    result = detect_prompt_injection(
        incident_text
    )

    state["prompt_injection_detected"] = (
        result.detected
    )

    state["prompt_injection_risk"] = (
        result.risk_level
    )

    state["prompt_injection_patterns"] = (
        result.matched_patterns
    )

    state["step_count"] = (
        state.get("step_count", 0) + 1
    )

    return state
