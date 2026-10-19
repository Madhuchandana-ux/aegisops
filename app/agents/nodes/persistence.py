from app.agents.state import AgentState
from app.database.services.agent_run_service import (
    finish_agent_run,
    record_policy_decision,
    start_agent_run,
)


def persistence_start_node(state: AgentState) -> AgentState:
    start_agent_run(state)

    state["step_count"] = state.get("step_count", 0) + 1

    return state


def persistence_policy_node(state: AgentState) -> AgentState:
    record_policy_decision(state)

    state["step_count"] = state.get("step_count", 0) + 1

    return state


def persistence_finish_node(state: AgentState) -> AgentState:
    finish_agent_run(state)

    state["step_count"] = state.get("step_count", 0) + 1

    return state