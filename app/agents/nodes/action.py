
from app.agents.state import AgentState
from app.agents.tools.servicenow_tools import (
    add_work_note_tool,
    resolve_incident_tool,
)


def action_node(state: AgentState) -> AgentState:
    selected_action = state.get("selected_action", "")
    policy_allowed = state.get("policy_allowed", False)
    sys_id = state.get("servicenow_sys_id", "")
    user_role = state.get("user_role", "viewer")

    # Never assume that an action succeeded.
    state["action_executed"] = False

    if selected_action == "request_human_approval":
        state["action_result"] = {
            "status": "pending",
            "message": (
                "Human approval required before "
                "any external action."
            ),
        }
        return state

    # Fail closed unless automation is explicitly authorized.
    if (
        selected_action != "automated_resolution"
        or not policy_allowed
    ):
        state["action_result"] = {
            "status": "blocked",
            "message": (
                "Action blocked because explicit "
                "automation authorization is missing."
            ),
        }
        return state

    if not sys_id:
        state["action_result"] = {
            "status": "failed",
            "message": "ServiceNow incident sys_id is missing.",
        }
        return state

    action_name = state.get("action_name", "")

    try:
        if action_name == "add_work_note":
            response = add_work_note_tool(
                sys_id=sys_id,
                work_note=state.get(
                    "proposed_resolution",
                    "AegisOps troubleshooting performed.",
                ),
                role=user_role,
            )

        elif action_name == "resolve_incident":
            response = resolve_incident_tool(
                sys_id=sys_id,
                resolution_notes=state.get(
                    "proposed_resolution",
                    "Incident resolved by AegisOps.",
                ),
                role=user_role,
            )

        else:
            state["action_result"] = {
                "status": "blocked",
                "message": f"Unsupported action: {action_name}",
            }
            return state

        # Validate the tool response before claiming success.
        if not isinstance(response, dict):
            state["action_result"] = {
                "status": "failed",
                "message": (
                    "ServiceNow returned an invalid response."
                ),
            }
            return state

        incident = response.get("result")

        if not isinstance(incident, dict):
            state["action_result"] = {
                "status": "failed",
                "message": (
                    "ServiceNow response is missing a valid "
                    "incident result."
                ),
            }
            return state

        # The response must identify the incident we requested.
        response_sys_id = incident.get("sys_id")

        if (
            not isinstance(response_sys_id, str)
            or response_sys_id != sys_id
        ):
            state["action_result"] = {
                "status": "failed",
                "message": (
                    "ServiceNow response does not match "
                    "the requested incident."
                ),
            }
            return state

        # A resolution response must explicitly confirm state 6.
        if action_name == "resolve_incident":
            if str(incident.get("state", "")) != "6":
                state["action_result"] = {
                    "status": "failed",
                    "message": (
                        "ServiceNow did not confirm that "
                        "the incident was resolved."
                    ),
                }
                return state

        # For a work note, a matching incident response confirms
        # the update response, but not independent verification
        # that the journal entry is present.
        state["action_executed"] = True
        state["action_result"] = {
            "status": "executed",
            "result": response,
        }

    except PermissionError as exc:
        state["action_result"] = {
            "status": "blocked",
            "message": str(exc),
        }

    except Exception as exc:
        state["action_result"] = {
            "status": "failed",
            "message": str(exc),
        }

    state["step_count"] = state.get("step_count", 0) + 1
    return state
