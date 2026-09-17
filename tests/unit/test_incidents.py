from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_create_incident():
    response = client.post(
        "/api/v1/incidents",
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


def test_reject_short_description():
    response = client.post(
        "/api/v1/incidents",
        json={
            "description": "VPN",
        },
    )

    assert response.status_code == 422


def test_reject_missing_description():
    response = client.post(
        "/api/v1/incidents",
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