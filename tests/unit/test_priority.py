from app.agents.nodes.priority import priority_node
from app.agents.state import AgentState


def test_high_priority_incident():
    state = AgentState(
        incident_text="Production outage affecting all users."
    )

    result = priority_node(state)

    assert result["priority"] == "P1"


def test_medium_priority_incident():
    state = AgentState(
        incident_text="Multiple users cannot access the application."
    )

    result = priority_node(state)

    assert result["priority"] == "P2"


def test_normal_priority_incident():
    state = AgentState(
        incident_text="User cannot connect to the corporate VPN."
    )

    result = priority_node(state)

    assert result["priority"] == "P3"


def test_empty_incident_defaults_to_p3():
    state = AgentState(
        incident_text=""
    )

    result = priority_node(state)

    assert result["priority"] == "P3"