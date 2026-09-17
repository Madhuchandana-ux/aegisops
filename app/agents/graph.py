from app.agents.state import AgentState


def build_initial_state(
    incident_id: str,
    incident_text: str,
    caller: str = "",
) -> AgentState:
    """
    Create the initial state for an agent run.
    """

    return AgentState(
        incident_id=incident_id,
        incident_text=incident_text,
        caller=caller,

        retrieved_documents=[],
        retrieval_scores=[],

        confidence=0.0,
        risk_level="UNKNOWN",
        requires_human=False,

        action_result={},
        verification_result={},

        run_id="",
        step_count=0,

        errors=[],
    )


def validate_incident(
    state: AgentState,
) -> AgentState:
    """
    Validate the incident before downstream processing.
    """

    incident_text = state.get(
        "incident_text",
        "",
    ).strip()

    if not incident_text:
        state["errors"] = [
            "Incident description is empty."
        ]

        return state

    state["errors"] = []

    return state