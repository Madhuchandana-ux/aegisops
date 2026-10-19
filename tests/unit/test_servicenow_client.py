import httpx
import pytest

from app.servicenow.client import (
    ServiceNowClient,
    ServiceNowError,
)


def test_build_url():
    client = ServiceNowClient(
        base_url="https://example.service-now.com",
        username="test_user",
        password="test_password",
    )

    url = client._build_url(
        "/api/now/table/incident"
    )

    assert (
        url
        == "https://example.service-now.com/api/now/table/incident"
    )


def test_get_success(monkeypatch):
    client = ServiceNowClient(
        base_url="https://example.service-now.com",
        username="test_user",
        password="test_password",
    )

    def mock_get(*args, **kwargs):
        return httpx.Response(
            status_code=200,
            json={
                "result": {
                    "number": "INC0010001"
                }
            },
            request=httpx.Request(
                "GET",
                args[0],
            ),
        )

    monkeypatch.setattr(
        httpx,
        "get",
        mock_get,
    )

    result = client.get(
        "/api/now/table/incident/123"
    )

    assert result["result"]["number"] == "INC0010001"


def test_get_failure(monkeypatch):
    client = ServiceNowClient(
        base_url="https://example.service-now.com",
        username="test_user",
        password="test_password",
    )

    def mock_get(*args, **kwargs):
        request = httpx.Request(
            "GET",
            args[0],
        )

        return httpx.Response(
            status_code=500,
            request=request,
        )

    monkeypatch.setattr(
        httpx,
        "get",
        mock_get,
    )

    with pytest.raises(ServiceNowError):
        client.get(
            "/api/now/table/incident/123"
        )


def test_post_success(monkeypatch):
    client = ServiceNowClient(
        base_url="https://example.service-now.com",
        username="test_user",
        password="test_password",
    )

    def mock_post(*args, **kwargs):
        return httpx.Response(
            status_code=201,
            json={
                "result": {
                    "number": "INC0010002"
                }
            },
            request=httpx.Request(
                "POST",
                args[0],
            ),
        )

    monkeypatch.setattr(
        httpx,
        "post",
        mock_post,
    )

    result = client.post(
        "/api/now/table/incident",
        {
            "short_description": "VPN issue",
        },
    )

    assert result["result"]["number"] == "INC0010002"


def test_patch_success(monkeypatch):
    client = ServiceNowClient(
        base_url="https://example.service-now.com",
        username="test_user",
        password="test_password",
    )

    def mock_patch(*args, **kwargs):
        return httpx.Response(
            status_code=200,
            json={
                "result": {
                    "number": "INC0010001",
                    "state": "Resolved",
                }
            },
            request=httpx.Request(
                "PATCH",
                args[0],
            ),
        )

    monkeypatch.setattr(
        httpx,
        "patch",
        mock_patch,
    )

    result = client.patch(
        "/api/now/table/incident/123",
        {
            "state": "6",
        },
    )

    assert result["result"]["state"] == "Resolved"