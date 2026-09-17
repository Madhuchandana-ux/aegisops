from app.agents.graph import (
    build_initial_state,
    validate_incident,
)


def test_initial_state():
    state = build_initial_state(
        incident_id="INC0010001",
        incident_text="VPN is not working",
        caller="employee01",
    )

    assert state["incident_id"] == "INC0010001"
    assert state["incident_text"] == "VPN is not working"
    assert state["caller"] == "employee01"

    assert state["confidence"] == 0.0
    assert state["risk_level"] == "UNKNOWN"


def test_valid_incident():
    state = build_initial_state(
        incident_id="INC0010001",
        incident_text="VPN is not working",
    )

    result = validate_incident(state)

    assert result["errors"] == []


def test_empty_incident():
    state = build_initial_state(
        incident_id="INC0010001",
        incident_text="",
    )

    result = validate_incident(state)

    assert len(result["errors"]) > 0