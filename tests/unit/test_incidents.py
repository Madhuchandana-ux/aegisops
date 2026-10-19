from fastapi.testclient import TestClient

from app.main import app
from app.security.auth import create_access_token


client = TestClient(app)


def get_auth_headers(
    username: str,
    role: str,
) -> dict[str, str]:
    """Create Authorization headers for an authenticated test user."""

    token = create_access_token(
        username=username,
        role=role,
    )

    return {
        "Authorization": f"Bearer {token}",
    }


def test_create_incident():
    response = client.post(
        "/api/v1/incidents",
        headers=get_auth_headers(
            "viewer",
            "viewer",
        ),
        json={
            "incident_id": "INC0010001",
            "description": "VPN connection is not working.",
            "caller": "employee01",
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["status"] == "received"
    assert data["incident_id"] == "INC0010001"
    assert data["validated"] is True
    assert data["request_id"]


def test_create_incident_without_id():
    response = client.post(
        "/api/v1/incidents",
        headers=get_auth_headers(
            "viewer",
            "viewer",
        ),
        json={
            "description": "Laptop is running very slowly.",
            "caller": "employee02",
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["incident_id"] == "LOCAL-INCIDENT"
    assert data["validated"] is True
    assert data["request_id"]


def test_create_incident_requires_authentication():
    response = client.post(
        "/api/v1/incidents",
        json={
            "description": "VPN connection is not working.",
        },
    )

    assert response.status_code == 401


def test_viewer_can_create_incident():
    response = client.post(
        "/api/v1/incidents",
        headers=get_auth_headers(
            "viewer",
            "viewer",
        ),
        json={
            "description": "VPN connection is not working.",
        },
    )

    assert response.status_code == 200


def test_analyst_can_create_incident():
    response = client.post(
        "/api/v1/incidents",
        headers=get_auth_headers(
            "analyst",
            "analyst",
        ),
        json={
            "description": "Outlook is not opening.",
        },
    )

    assert response.status_code == 200


def test_operator_can_create_incident():
    response = client.post(
        "/api/v1/incidents",
        headers=get_auth_headers(
            "operator",
            "operator",
        ),
        json={
            "description": "Laptop is overheating.",
        },
    )

    assert response.status_code == 200


def test_admin_can_create_incident():
    response = client.post(
        "/api/v1/incidents",
        headers=get_auth_headers(
            "admin",
            "admin",
        ),
        json={
            "description": "Printer is not connecting.",
        },
    )

    assert response.status_code == 200


def test_invalid_token_is_rejected():
    response = client.post(
        "/api/v1/incidents",
        headers={
            "Authorization": "Bearer invalid-token",
        },
        json={
            "description": "VPN connection is not working.",
        },
    )

    assert response.status_code == 401


def test_reject_short_description():
    response = client.post(
        "/api/v1/incidents",
        headers=get_auth_headers(
            "viewer",
            "viewer",
        ),
        json={
            "description": "VPN",
        },
    )

    assert response.status_code == 422


def test_reject_missing_description():
    response = client.post(
        "/api/v1/incidents",
        headers=get_auth_headers(
            "viewer",
            "viewer",
        ),
        json={
            "incident_id": "INC0010002",
        },
    )

    assert response.status_code == 422


def test_custom_request_id():
    custom_request_id = "test-request-123"

    response = client.post(
        "/api/v1/incidents",
        headers={
            **get_auth_headers(
                "viewer",
                "viewer",
            ),
            "X-Request-ID": custom_request_id,
        },
        json={
            "description": "Cannot connect to company VPN.",
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["request_id"] == custom_request_id
    assert (
        response.headers["X-Request-ID"]
        == custom_request_id
    )