from unittest.mock import Mock

import pytest

from app.servicenow.client import ServiceNowClient
from app.servicenow.incidents import IncidentService


@pytest.fixture
def mock_client():
    return Mock(spec=ServiceNowClient)


@pytest.fixture
def incident_service(mock_client):
    return IncidentService(mock_client)


def test_get_incident(
    incident_service,
    mock_client,
):
    mock_client.get.return_value = {
        "result": {
            "sys_id": "abc123",
            "number": "INC0010001",
        }
    }

    result = incident_service.get_incident(
        "abc123"
    )

    mock_client.get.assert_called_once_with(
        "/api/now/table/incident/abc123"
    )

    assert (
        result["result"]["number"]
        == "INC0010001"
    )


def test_create_incident(
    incident_service,
    mock_client,
):
    mock_client.post.return_value = {
        "result": {
            "number": "INC0010002"
        }
    }

    result = incident_service.create_incident(
        short_description="VPN connection failure",
        description="User cannot connect to VPN.",
        category="network",
        priority="3",
    )

    mock_client.post.assert_called_once_with(
        "/api/now/table/incident",
        {
            "short_description":
                "VPN connection failure",
            "description":
                "User cannot connect to VPN.",
            "category":
                "network",
            "priority":
                "3",
        },
    )

    assert (
        result["result"]["number"]
        == "INC0010002"
    )


def test_update_incident(
    incident_service,
    mock_client,
):
    mock_client.patch.return_value = {
        "result": {
            "sys_id": "abc123"
        }
    }

    fields = {
        "work_notes": "Investigating VPN issue."
    }

    incident_service.update_incident(
        "abc123",
        fields,
    )

    mock_client.patch.assert_called_once_with(
        "/api/now/table/incident/abc123",
        fields,
    )


def test_add_work_note(
    incident_service,
    mock_client,
):
    mock_client.patch.return_value = {
        "result": {
            "sys_id": "abc123"
        }
    }

    incident_service.add_work_note(
        "abc123",
        "VPN troubleshooting started.",
    )

    mock_client.patch.assert_called_once_with(
        "/api/now/table/incident/abc123",
        {
            "work_notes":
                "VPN troubleshooting started."
        },
    )


def test_resolve_incident(
    incident_service,
    mock_client,
):
    mock_client.patch.return_value = {
        "result": {
            "sys_id": "abc123",
            "state": "6",
        }
    }

    incident_service.resolve_incident(
        "abc123",
        "VPN configuration corrected.",
    )

    mock_client.patch.assert_called_once_with(
        "/api/now/table/incident/abc123",
        {
            "state": "6",
            "close_notes":
                "VPN configuration corrected.",
        },
    )


def test_get_incident_rejects_empty_sys_id(
    incident_service,
):
    with pytest.raises(ValueError):
        incident_service.get_incident("")


def test_create_incident_rejects_empty_description(
    incident_service,
):
    with pytest.raises(ValueError):
        incident_service.create_incident("")


def test_update_incident_rejects_empty_fields(
    incident_service,
):
    with pytest.raises(ValueError):
        incident_service.update_incident(
            "abc123",
            {},
        )


def test_add_work_note_rejects_empty_note(
    incident_service,
):
    with pytest.raises(ValueError):
        incident_service.add_work_note(
            "abc123",
            "",
        )


def test_resolve_incident_rejects_empty_notes(
    incident_service,
):
    with pytest.raises(ValueError):
        incident_service.resolve_incident(
            "abc123",
            "",
        )