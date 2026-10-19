from app.agents.state import AgentState


def validation_node(
    state: AgentState,
) -> AgentState:

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

    state["step_count"] = (
        state.get("step_count", 0) + 1
    )

    return state