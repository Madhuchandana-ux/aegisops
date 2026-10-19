from app.agents.nodes.servicenow_target import (
    servicenow_target_node,
)


def test_mock_service_now_target_is_generated(
    monkeypatch,
):
    monkeypatch.setenv(
        "SERVICENOW_MODE",
        "mock",
    )

    state = {
        "incident_id": "INC0010001",
        "servicenow_sys_id": "",
        "step_count": 0,
    }

    result = servicenow_target_node(state)

    assert (
        result["servicenow_sys_id"]
        == "MOCK-INC0010001"
    )

    assert (
        result["step_count"]
        == 1
    )


def test_existing_service_now_id_is_preserved(
    monkeypatch,
):
    monkeypatch.setenv(
        "SERVICENOW_MODE",
        "mock",
    )

    state = {
        "incident_id": "INC0010001",
        "servicenow_sys_id": "existing123",
        "step_count": 0,
    }

    result = servicenow_target_node(state)

    assert (
        result["servicenow_sys_id"]
        == "existing123"
    )