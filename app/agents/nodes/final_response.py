from app.agents.state import AgentState


def final_response_node(
    state: AgentState,
) -> AgentState:
    """
    Build the user-facing final response from the
    complete agent execution state.

    This node does not perform external actions.
    """

    category = state.get(
        "category",
        "Unknown",
    )

    priority = state.get(
        "priority",
        "P3",
    )

    confidence = state.get(
        "classification_confidence",
        0.0,
    )

    proposed_resolution = (
        state.get(
            "proposed_resolution",
            "",
        )
        .strip()
    )

    selected_action = state.get(
        "selected_action",
        "",
    )

    action_result = state.get(
        "action_result",
        {},
    )

    verification_result = state.get(
        "verification_result",
        {},
    )

    risk_level = state.get(
        "risk_level",
        "UNKNOWN",
    )

    requires_human = state.get(
        "requires_human",
        False,
    )

    policy_reason = state.get(
        "policy_reason",
        "",
    )

    incident_id = state.get(
        "incident_id",
        "",
    )

    verification_status = (
        verification_result.get(
            "status",
            "unknown",
        )
    )

    action_status = action_result.get(
        "status",
        "unknown",
    )

    lines: list[str] = []
        # Handle invalid incidents before building a normal summary.
    errors = state.get("errors", [])

    if errors:
        lines.append("AegisOps Incident Resolution Summary")
        lines.append("Status: INVALID INCIDENT")

        for error in errors:
            lines.append(f"Reason: {error}")

        lines.append(
            "No external ServiceNow action was executed."
        )

        state["final_response"] = "\n".join(lines)
        state["step_count"] = state.get("step_count", 0) + 1

        return state

    lines.append(
        "AegisOps Incident Resolution Summary"
    )

    if incident_id:
        lines.append(
            f"Incident: {incident_id}"
        )

    lines.append(
        f"Category: {category}"
    )

    lines.append(
        f"Priority: {priority}"
    )

    lines.append(
        "Classification confidence: "
        f"{confidence:.2%}"
    )

    lines.append(
        f"Risk level: {risk_level}"
    )

    if proposed_resolution:
        lines.append(
            "\nRecommended resolution:\n"
            f"{proposed_resolution}"
        )

    if requires_human:
        lines.append(
            "\nStatus: HUMAN APPROVAL REQUIRED"
        )

        if policy_reason:
            lines.append(
                f"Reason: {policy_reason}"
            )

        lines.append(
            "No external ServiceNow action "
            "was executed."
        )

    elif action_status == "executed":

        lines.append(
            "\nAction: "
            f"{selected_action}"
        )

        lines.append(
            "Action status: EXECUTED"
        )

        if verification_status == "verified":

            lines.append(
                "Verification: VERIFIED"
            )

            lines.append(
                "The external incident state was "
                "successfully verified after the action."
            )

        elif verification_status == "not_executed":

            lines.append(
                "Verification: NOT EXECUTED"
            )

        else:

            lines.append(
                "Verification: "
                f"{verification_status.upper()}"
            )

    elif action_status == "blocked":

        lines.append(
            "\nAction status: BLOCKED"
        )

        message = action_result.get(
            "message",
            "",
        )

        if message:
            lines.append(
                f"Reason: {message}"
            )

    elif action_status == "failed":

        lines.append(
            "\nAction status: FAILED"
        )

        message = action_result.get(
            "message",
            "",
        )

        if message:
            lines.append(
                f"Reason: {message}"
            )

    else:

        lines.append(
            "\nAction status: "
            f"{action_status.upper()}"
        )

    state["final_response"] = (
        "\n".join(lines)
    )

    state["step_count"] = (
        state.get("step_count", 0) + 1
    )

    return state