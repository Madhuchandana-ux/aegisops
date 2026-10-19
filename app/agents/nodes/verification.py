from app.agents.state import AgentState
from app.agents.tools.servicenow_tools import get_incident_tool


def verification_node(state: AgentState) -> AgentState:
    """
    Verify the expected ServiceNow state after an action.
    """

    action_result = state.get(
        "action_result",
        {},
    )

    status = action_result.get(
        "status",
        "unknown",
    )

    sys_id = state.get(
        "servicenow_sys_id",
        "",
    )

    # Nothing was executed.
    if status in {
        "pending",
        "blocked",
        "failed",
    }:
        state["verification_result"] = {
            "status": "not_executed",
            "verified": False,
            "message": (
                "No external action was successfully executed."
            ),
        }

        state["step_count"] = state.get(
            "step_count",
            0,
        ) + 1

        return state

    if status != "executed":
        state["verification_result"] = {
            "status": "unknown",
            "verified": False,
            "message": "Action status is unknown.",
        }

        return state

    if not sys_id:
        state["verification_result"] = {
            "status": "failed",
            "verified": False,
            "message": (
                "Cannot verify without a ServiceNow sys_id."
            ),
        }

        return state

    try:
        observed = get_incident_tool(
    sys_id,
    role=state.get("user_role", "viewer"),
     )

        incident = observed.get(
            "result",
            {},
        )

        action_name = state.get(
            "action_name",
            "",
        )

        if action_name == "resolve_incident":
            verified = (
                str(
                    incident.get(
                        "state",
                        "",
                    )
                )
                == "6"
            )

        elif action_name == "add_work_note":
            verified = "work_notes" in incident

        else:
            verified = False

        state["verification_result"] = {
            "status": (
                "verified"
                if verified
                else "verification_failed"
            ),
            "verified": verified,
            "observed_state": incident,
        }

    except Exception as exc:
        state["verification_result"] = {
            "status": "failed",
            "verified": False,
            "message": str(exc),
        }

    state["step_count"] = state.get(
        "step_count",
        0,
    ) + 1

    return state