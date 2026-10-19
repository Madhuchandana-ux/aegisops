import os

from dotenv import load_dotenv

from app.agents.state import AgentState


load_dotenv()


def servicenow_target_node(
    state: AgentState,
) -> AgentState:
    """
    Prepare the ServiceNow target.

    In mock mode, a deterministic local sys_id is generated.

    In real mode, an externally supplied ServiceNow sys_id
    must be provided.
    """

    mode = os.getenv(
        "SERVICENOW_MODE",
        "real",
    ).strip().lower()

    current_sys_id = (
        state.get(
            "servicenow_sys_id",
            "",
        )
        .strip()
    )

    if current_sys_id:
        state["step_count"] = (
            state.get("step_count", 0) + 1
        )
        return state

    if mode == "mock":

        incident_id = (
            state.get(
                "incident_id",
                "",
            )
            .strip()
        )

        run_id = (
            state.get(
                "run_id",
                "",
            )
            .strip()
        )

        if incident_id:
            sys_id = (
                f"MOCK-{incident_id}"
            )
        elif run_id:
            sys_id = (
                f"MOCK-{run_id}"
            )
        else:
            sys_id = "MOCK-INCIDENT"

        state["servicenow_sys_id"] = sys_id

    state["step_count"] = (
        state.get("step_count", 0) + 1
    )

    return state