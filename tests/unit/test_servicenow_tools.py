import pytest
from unittest.mock import Mock

from app.agents.tools import servicenow_tools


def test_get_incident_tool(monkeypatch):
    mock_service = Mock()

    mock_service.get_incident.return_value = {
        "result": {
            "number": "INC0010001",
        }
    }

    monkeypatch.setattr(
        servicenow_tools,
        "IncidentService",
        lambda client: mock_service,
    )

    monkeypatch.setattr(
        servicenow_tools,
        "create_servicenow_client",
        lambda: Mock(),
    )

    result = servicenow_tools.get_incident_tool(
        "abc123"
    )

    mock_service.get_incident.assert_called_once_with(
        "abc123"
    )

    assert (
        result["result"]["number"]
        == "INC0010001"
    )


def test_add_work_note_tool(monkeypatch):
    mock_service = Mock()

    mock_service.add_work_note.return_value = {
        "result": {
            "sys_id": "abc123",
        }
    }

    monkeypatch.setattr(
        servicenow_tools,
        "IncidentService",
        lambda client: mock_service,
    )

    monkeypatch.setattr(
        servicenow_tools,
        "create_servicenow_client",
        lambda: Mock(),
    )

    result = servicenow_tools.add_work_note_tool(
        "abc123",
        "Investigating VPN connectivity.",
    )

    mock_service.add_work_note.assert_called_once_with(
        sys_id="abc123",
        work_note="Investigating VPN connectivity.",
    )

    assert (
        result["result"]["sys_id"]
        == "abc123"
    )


def test_update_incident_tool(monkeypatch):
    mock_service = Mock()

    mock_service.update_incident.return_value = {
        "result": {
            "sys_id": "abc123",
        }
    }

    monkeypatch.setattr(
        servicenow_tools,
        "IncidentService",
        lambda client: mock_service,
    )

    monkeypatch.setattr(
        servicenow_tools,
        "create_servicenow_client",
        lambda: Mock(),
    )

    fields = {
        "work_notes": "Troubleshooting started."
    }

    servicenow_tools.update_incident_tool(
        "abc123",
        fields,
        role="operator",
    )

    mock_service.update_incident.assert_called_once_with(
        sys_id="abc123",
        fields=fields,
    )


def test_resolve_incident_tool(monkeypatch):
    mock_service = Mock()

    mock_service.resolve_incident.return_value = {
        "result": {
            "sys_id": "abc123",
            "state": "6",
        }
    }

    monkeypatch.setattr(
        servicenow_tools,
        "IncidentService",
        lambda client: mock_service,
    )

    monkeypatch.setattr(
        servicenow_tools,
        "create_servicenow_client",
        lambda: Mock(),
    )

    result = servicenow_tools.resolve_incident_tool(
        "abc123",
        "VPN issue resolved.",
        role="operator",
    )

    mock_service.resolve_incident.assert_called_once_with(
        sys_id="abc123",
        resolution_notes="VPN issue resolved.",
    )

    assert (
        result["result"]["state"]
        == "6"
    )


# ============================================================
# RBAC TESTS
# ============================================================


def test_viewer_can_get_incident(monkeypatch):
    mock_service = Mock()

    mock_service.get_incident.return_value = {
        "result": {
            "number": "INC0010001",
        }
    }

    monkeypatch.setattr(
        servicenow_tools,
        "IncidentService",
        lambda client: mock_service,
    )

    monkeypatch.setattr(
        servicenow_tools,
        "create_servicenow_client",
        lambda: Mock(),
    )

    result = servicenow_tools.get_incident_tool(
        "abc123",
        role="viewer",
    )

    assert result["result"]["number"] == "INC0010001"


def test_viewer_cannot_add_work_note(monkeypatch):
    create_client = Mock()

    monkeypatch.setattr(
        servicenow_tools,
        "create_servicenow_client",
        create_client,
    )

    with pytest.raises(PermissionError):
        servicenow_tools.add_work_note_tool(
            "abc123",
            "Unauthorized note.",
            role="viewer",
        )

    create_client.assert_not_called()


def test_viewer_cannot_update_incident(monkeypatch):
    create_client = Mock()

    monkeypatch.setattr(
        servicenow_tools,
        "create_servicenow_client",
        create_client,
    )

    with pytest.raises(PermissionError):
        servicenow_tools.update_incident_tool(
            "abc123",
            {"priority": "1"},
            role="viewer",
        )

    create_client.assert_not_called()


def test_analyst_can_add_work_note(monkeypatch):
    mock_service = Mock()

    mock_service.add_work_note.return_value = {
        "result": {
            "sys_id": "abc123",
        }
    }

    monkeypatch.setattr(
        servicenow_tools,
        "IncidentService",
        lambda client: mock_service,
    )

    monkeypatch.setattr(
        servicenow_tools,
        "create_servicenow_client",
        lambda: Mock(),
    )

    result = servicenow_tools.add_work_note_tool(
        "abc123",
        "Investigating incident.",
        role="analyst",
    )

    assert result["result"]["sys_id"] == "abc123"


def test_analyst_cannot_update_incident(monkeypatch):
    create_client = Mock()

    monkeypatch.setattr(
        servicenow_tools,
        "create_servicenow_client",
        create_client,
    )

    with pytest.raises(PermissionError):
        servicenow_tools.update_incident_tool(
            "abc123",
            {"priority": "1"},
            role="analyst",
        )

    create_client.assert_not_called()


def test_operator_can_update_incident(monkeypatch):
    mock_service = Mock()

    mock_service.update_incident.return_value = {
        "result": {
            "sys_id": "abc123",
        }
    }

    monkeypatch.setattr(
        servicenow_tools,
        "IncidentService",
        lambda client: mock_service,
    )

    monkeypatch.setattr(
        servicenow_tools,
        "create_servicenow_client",
        lambda: Mock(),
    )

    result = servicenow_tools.update_incident_tool(
        "abc123",
        {"priority": "2"},
        role="operator",
    )

    assert result["result"]["sys_id"] == "abc123"

    mock_service.update_incident.assert_called_once_with(
        sys_id="abc123",
        fields={"priority": "2"},
    )


def test_viewer_cannot_resolve_incident(monkeypatch):
    create_client = Mock()

    monkeypatch.setattr(
        servicenow_tools,
        "create_servicenow_client",
        create_client,
    )

    with pytest.raises(PermissionError):
        servicenow_tools.resolve_incident_tool(
            "abc123",
            "Unauthorized resolution.",
            role="viewer",
        )

    create_client.assert_not_called()


def test_analyst_cannot_resolve_incident(monkeypatch):
    create_client = Mock()

    monkeypatch.setattr(
        servicenow_tools,
        "create_servicenow_client",
        create_client,
    )

    with pytest.raises(PermissionError):
        servicenow_tools.resolve_incident_tool(
            "abc123",
            "Unauthorized resolution.",
            role="analyst",
        )

    create_client.assert_not_called()


def test_unknown_action_is_denied():
    with pytest.raises(PermissionError):
        servicenow_tools._require_action_permission(
            "admin",
            "delete_everything",
        )