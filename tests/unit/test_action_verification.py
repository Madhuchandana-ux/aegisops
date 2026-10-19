from unittest.mock import patch

from app.agents.nodes.action import action_node
from app.agents.nodes.verification import verification_node


# ============================================================
# ACTION NODE TESTS
# ============================================================


@patch(
    "app.agents.nodes.action.add_work_note_tool"
)
@patch(
    "app.agents.nodes.action.resolve_incident_tool"
)
def test_action_requires_human_approval(
    mock_resolve_incident,
    mock_add_work_note,
):
    state = {
        "selected_action": "request_human_approval",
        "policy_allowed": False,
        "action_executed": False,
        "user_role": "operator",
        "servicenow_sys_id": "abc123",
        "action_name": "resolve_incident",
    }

    result = action_node(state)

    assert (
        result["action_result"]["status"]
        == "pending"
    )

    assert (
        result["action_executed"]
        is False
    )

    # Critical security checks:
    # No external ServiceNow action should execute
    # while human approval is pending.
    mock_resolve_incident.assert_not_called()
    mock_add_work_note.assert_not_called()


def test_action_blocked_by_policy():
    state = {
        "selected_action": "automated_resolution",
        "policy_allowed": False,
        "action_executed": False,
        "user_role": "operator",
    }

    result = action_node(state)

    assert (
        result["action_result"]["status"]
        == "blocked"
    )

    assert (
        result["action_executed"]
        is False
    )


def test_action_requires_servicenow_id():
    state = {
        "selected_action": "automated_resolution",
        "policy_allowed": True,
        "servicenow_sys_id": "",
        "action_name": "resolve_incident",
        "action_executed": False,
        "user_role": "operator",
    }

    result = action_node(state)

    assert (
        result["action_result"]["status"]
        == "failed"
    )

    assert (
        result["action_executed"]
        is False
    )


def test_action_blocks_unknown_action():
    state = {
        "selected_action": "automated_resolution",
        "policy_allowed": True,
        "servicenow_sys_id": "abc123",
        "action_name": "delete_everything",
        "action_executed": False,
        "user_role": "admin",
    }

    result = action_node(state)

    assert (
        result["action_result"]["status"]
        == "blocked"
    )

    assert (
        result["action_executed"]
        is False
    )

    assert (
        "Unsupported action"
        in result["action_result"]["message"]
    )


# ============================================================
# SERVICE NOW ACTION TEST
# ============================================================


@patch(
    "app.agents.nodes.action.resolve_incident_tool"
)
def test_resolve_incident_action(
    mock_resolve_incident,
):
    mock_resolve_incident.return_value = {
        "result": {
            "sys_id": "abc123",
            "state": "6",
        }
    }

    state = {
        "selected_action": "automated_resolution",
        "policy_allowed": True,
        "servicenow_sys_id": "abc123",
        "action_name": "resolve_incident",
        "proposed_resolution": (
            "The password issue was resolved."
        ),
        "user_role": "operator",
        "action_executed": False,
    }

    result = action_node(state)

    assert (
        result["action_result"]["status"]
        == "executed"
    )

    assert (
        result["action_executed"]
        is True
    )

    mock_resolve_incident.assert_called_once_with(
        sys_id="abc123",
        resolution_notes=(
            "The password issue was resolved."
        ),
        role="operator",
    )


@patch(
    "app.agents.nodes.action.add_work_note_tool"
)
def test_add_work_note_action(
    mock_add_work_note,
):
    mock_add_work_note.return_value = {
        "result": {
            "sys_id": "abc123",
        }
    }

    state = {
        "selected_action": "automated_resolution",
        "policy_allowed": True,
        "servicenow_sys_id": "abc123",
        "action_name": "add_work_note",
        "proposed_resolution": (
            "Troubleshooting instructions were provided."
        ),
        "user_role": "analyst",
        "action_executed": False,
    }

    result = action_node(state)

    assert (
        result["action_result"]["status"]
        == "executed"
    )

    assert (
        result["action_executed"]
        is True
    )

    mock_add_work_note.assert_called_once_with(
        sys_id="abc123",
        work_note=(
            "Troubleshooting instructions were provided."
        ),
        role="analyst",
    )


# ============================================================
# VERIFICATION TESTS
# ============================================================


def test_verification_when_action_not_executed():
    state = {
        "action_result": {
            "status": "pending"
        },
        "servicenow_sys_id": "",
        "user_role": "viewer",
    }

    result = verification_node(state)

    assert (
        result["verification_result"]["status"]
        == "not_executed"
    )

    assert (
        result["verification_result"]["verified"]
        is False
    )


@patch(
    "app.agents.nodes.verification.get_incident_tool"
)
def test_resolve_verification(
    mock_get_incident,
):
    mock_get_incident.return_value = {
        "result": {
            "sys_id": "abc123",
            "state": "6",
        }
    }

    state = {
        "action_result": {
            "status": "executed"
        },
        "servicenow_sys_id": "abc123",
        "action_name": "resolve_incident",
        "user_role": "operator",
    }

    result = verification_node(state)

    assert (
        result["verification_result"]["status"]
        == "verified"
    )

    assert (
        result["verification_result"]["verified"]
        is True
    )

    mock_get_incident.assert_called_once_with(
        "abc123",
        role="operator",
    )


@patch(
    "app.agents.nodes.verification.get_incident_tool"
)
def test_resolve_verification_fails_when_state_not_resolved(
    mock_get_incident,
):
    mock_get_incident.return_value = {
        "result": {
            "sys_id": "abc123",
            "state": "2",
        }
    }

    state = {
        "action_result": {
            "status": "executed"
        },
        "servicenow_sys_id": "abc123",
        "action_name": "resolve_incident",
        "user_role": "operator",
    }

    result = verification_node(state)

    assert (
        result["verification_result"]["status"]
        == "verification_failed"
    )

    assert (
        result["verification_result"]["verified"]
        is False
    )


@patch(
    "app.agents.nodes.verification.get_incident_tool"
)
def test_verification_failure_is_handled(
    mock_get_incident,
):
    mock_get_incident.side_effect = Exception(
        "ServiceNow unavailable"
    )

    state = {
        "action_result": {
            "status": "executed"
        },
        "servicenow_sys_id": "abc123",
        "action_name": "resolve_incident",
        "user_role": "operator",
    }

    result = verification_node(state)

    assert (
        result["verification_result"]["status"]
        == "failed"
    )

    assert (
        result["verification_result"]["verified"]
        is False
    )

    assert (
        "ServiceNow unavailable"
        in result["verification_result"]["message"]
    )
@patch(
    "app.agents.nodes.action.add_work_note_tool"
)
@patch(
    "app.agents.nodes.action.resolve_incident_tool"
)
def test_action_blocks_inconsistent_authorization_state(
    mock_resolve_incident,
    mock_add_work_note,
):
    state = {
        "selected_action": "blocked",
        "policy_allowed": True,
        "servicenow_sys_id": "abc123",
        "action_name": "resolve_incident",
        "user_role": "operator",
        "action_executed": False,
    }

    result = action_node(state)

    assert result["action_result"]["status"] == "blocked"
    assert result["action_executed"] is False

    mock_resolve_incident.assert_not_called()
    mock_add_work_note.assert_not_called()

@patch(
    "app.agents.nodes.action.resolve_incident_tool"
)
def test_action_rejects_response_for_different_incident(
    mock_resolve_incident,
):
    mock_resolve_incident.return_value = {
        "result": {
            "sys_id": "different-id",
            "state": "6",
        }
    }

    state = {
        "selected_action": "automated_resolution",
        "policy_allowed": True,
        "servicenow_sys_id": "abc123",
        "action_name": "resolve_incident",
        "proposed_resolution": "Fix applied.",
        "user_role": "operator",
        "action_executed": False,
    }

    result = action_node(state)

    assert result["action_result"]["status"] == "failed"
    assert result["action_executed"] is False


@patch(
    "app.agents.nodes.action.resolve_incident_tool"
)
def test_action_rejects_malformed_response(
    mock_resolve_incident,
):
    mock_resolve_incident.return_value = {}

    state = {
        "selected_action": "automated_resolution",
        "policy_allowed": True,
        "servicenow_sys_id": "abc123",
        "action_name": "resolve_incident",
        "proposed_resolution": "Fix applied.",
        "user_role": "operator",
        "action_executed": False,
    }

    result = action_node(state)

    assert result["action_result"]["status"] == "failed"
    assert result["action_executed"] is False


@patch(
    "app.agents.nodes.action.resolve_incident_tool"
)
def test_action_rejects_response_without_resolved_state(
    mock_resolve_incident,
):
    mock_resolve_incident.return_value = {
        "result": {
            "sys_id": "abc123",
            "state": "2",
        }
    }

    state = {
        "selected_action": "automated_resolution",
        "policy_allowed": True,
        "servicenow_sys_id": "abc123",
        "action_name": "resolve_incident",
        "proposed_resolution": "Fix applied.",
        "user_role": "operator",
        "action_executed": False,
    }

    result = action_node(state)

    assert result["action_result"]["status"] == "failed"
    assert result["action_executed"] is False
