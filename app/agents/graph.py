from uuid import uuid4

from langgraph.graph import END, START, StateGraph

from app.agents.nodes.action import action_node
from app.agents.nodes.classification import (
    classification_node,
)
from app.agents.nodes.decision import decision_node
from app.agents.nodes.final_response import (
    final_response_node,
)
from app.agents.nodes.persistence import (
    persistence_finish_node,
    persistence_policy_node,
    persistence_start_node,
)
from app.agents.nodes.priority import priority_node
from app.agents.nodes.reasoning import reasoning_node
from app.agents.nodes.retrieval import retrieval_node
from app.agents.nodes.security import (
    prompt_injection_node,
)
from app.agents.nodes.servicenow_target import (
    servicenow_target_node,
)
from app.agents.nodes.validation import validation_node
from app.agents.nodes.verification import (
    verification_node,
)
from app.agents.state import AgentState


def build_initial_state(
    incident_text: str,
    incident_id: str = "",
    caller: str = "",
    username: str = "",
    user_role: str = "viewer",
) -> AgentState:
    """
    Build the initial state for an AegisOps agent run.
    """

    return AgentState(
        incident_id=incident_id,
        incident_text=incident_text,
        caller=caller,
        username=username,
        user_role=user_role,

        prompt_injection_detected=False,
        prompt_injection_risk="LOW",
        prompt_injection_patterns=[],

        category="",
        subcategory="",

        classification_confidence=0.0,
        classification_model="",

        priority="",

        retrieved_documents=[],
        retrieval_scores=[],

        analysis="",
        proposed_resolution="",
        reasoning_summary="",

        confidence=0.0,
        risk_level="UNKNOWN",

        requires_human=False,
        policy_allowed=False,
        policy_reason="",

        selected_action="",

        action_result={},
        verification_result={},

        final_response="",

        run_id=str(uuid4()),
        step_count=0,
        errors=[],

        servicenow_sys_id="",
        action_name="",
        action_executed=False,
    )


def validate_incident(
    state: AgentState,
) -> AgentState:
    """
    Validate that the incident contains usable text.
    """

    incident_text = (
        state.get(
            "incident_text",
            "",
        )
        .strip()
    )

    if not incident_text:
        state["errors"] = [
            "Incident description is empty."
        ]

        return state

    state["errors"] = []

    return state
def route_after_validation(state: AgentState) -> str:
    """
    Stop invalid incidents before downstream processing.
    """
    if state.get("errors"):
        return "invalid"

    return "valid"

def build_agent_graph():
    """
    Build and compile the complete AegisOps LangGraph workflow.
    """

    workflow = StateGraph(AgentState)

    # ========================================================
    # NODES
    # ========================================================

    workflow.add_node(
        "persistence_start",
        persistence_start_node,
    )

    workflow.add_node(
        "validation",
        validation_node,
    )

    workflow.add_node(
        "servicenow_target",
        servicenow_target_node,
    )

    workflow.add_node(
        "prompt_injection",
        prompt_injection_node,
    )

    workflow.add_node(
        "classification",
        classification_node,
    )

    workflow.add_node(
        "priority",
        priority_node,
    )

    workflow.add_node(
        "retrieval",
        retrieval_node,
    )

    workflow.add_node(
        "reasoning",
        reasoning_node,
    )

    workflow.add_node(
        "decision",
        decision_node,
    )

    workflow.add_node(
        "persistence_policy",
        persistence_policy_node,
    )

    workflow.add_node(
        "action",
        action_node,
    )

    workflow.add_node(
        "verification",
        verification_node,
    )

    workflow.add_node(
        "final_response",
        final_response_node,
    )

    workflow.add_node(
        "persistence_finish",
        persistence_finish_node,
    )

    # ========================================================
    # EDGES
    # ========================================================

    workflow.add_edge(
        START,
        "persistence_start",
    )

    workflow.add_edge(
        "persistence_start",
        "validation",
    )

    workflow.add_conditional_edges(
    "validation",
    route_after_validation,
    {
        "valid": "servicenow_target",
        "invalid": "final_response",
    },
)

    workflow.add_edge(
        "servicenow_target",
        "prompt_injection",
    )

    workflow.add_edge(
        "prompt_injection",
        "classification",
    )

    workflow.add_edge(
        "classification",
        "priority",
    )

    workflow.add_edge(
        "priority",
        "retrieval",
    )

    workflow.add_edge(
        "retrieval",
        "reasoning",
    )

    workflow.add_edge(
        "reasoning",
        "decision",
    )

    workflow.add_edge(
        "decision",
        "persistence_policy",
    )

    workflow.add_edge(
        "persistence_policy",
        "action",
    )

    workflow.add_edge(
        "action",
        "verification",
    )

    workflow.add_edge(
        "verification",
        "final_response",
    )

    workflow.add_edge(
        "final_response",
        "persistence_finish",
    )

    workflow.add_edge(
        "persistence_finish",
        END,
    )

    return workflow.compile()


# Compile once when this module is imported.
agent_graph = build_agent_graph()