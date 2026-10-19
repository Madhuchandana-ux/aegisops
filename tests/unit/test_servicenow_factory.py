import pytest

from app.config import get_settings
from app.servicenow.factory import (
    create_servicenow_client,
)
from app.servicenow.client import (
    ServiceNowClient,
)
from app.servicenow.mock_client import (
    MockServiceNowClient,
)


def test_servicenow_factory_requires_url(
    monkeypatch,
):
    monkeypatch.setenv(
        "SERVICENOW_MODE",
        "real",
    )

    monkeypatch.setenv(
        "SERVICENOW_URL",
        "",
    )

    monkeypatch.setenv(
        "SERVICENOW_USERNAME",
        "test_user",
    )

    monkeypatch.setenv(
        "SERVICENOW_PASSWORD",
        "test_password",
    )

    get_settings.cache_clear()

    with pytest.raises(
        RuntimeError,
        match="SERVICENOW_URL",
    ):
        create_servicenow_client()


def test_servicenow_factory_requires_username(
    monkeypatch,
):
    monkeypatch.setenv(
        "SERVICENOW_MODE",
        "real",
    )

    monkeypatch.setenv(
        "SERVICENOW_URL",
        "https://example.service-now.com",
    )

    monkeypatch.setenv(
        "SERVICENOW_USERNAME",
        "",
    )

    monkeypatch.setenv(
        "SERVICENOW_PASSWORD",
        "test_password",
    )

    get_settings.cache_clear()

    with pytest.raises(
        RuntimeError,
        match="SERVICENOW_USERNAME",
    ):
        create_servicenow_client()


def test_servicenow_factory_requires_password(
    monkeypatch,
):
    monkeypatch.setenv(
        "SERVICENOW_MODE",
        "real",
    )

    monkeypatch.setenv(
        "SERVICENOW_URL",
        "https://example.service-now.com",
    )

    monkeypatch.setenv(
        "SERVICENOW_USERNAME",
        "test_user",
    )

    monkeypatch.setenv(
        "SERVICENOW_PASSWORD",
        "",
    )

    get_settings.cache_clear()

    with pytest.raises(
        RuntimeError,
        match="SERVICENOW_PASSWORD",
    ):
        create_servicenow_client()


def test_servicenow_factory_creates_real_client(
    monkeypatch,
):
    monkeypatch.setenv(
        "SERVICENOW_MODE",
        "real",
    )

    monkeypatch.setenv(
        "SERVICENOW_URL",
        "https://example.service-now.com",
    )

    monkeypatch.setenv(
        "SERVICENOW_USERNAME",
        "test_user",
    )

    monkeypatch.setenv(
        "SERVICENOW_PASSWORD",
        "test_password",
    )

    get_settings.cache_clear()

    client = create_servicenow_client()

    assert isinstance(
        client,
        ServiceNowClient,
    )

    assert (
        client.base_url
        == "https://example.service-now.com"
    )

    assert (
        client.username
        == "test_user"
    )

    assert (
        client.password
        == "test_password"
    )


def test_servicenow_factory_creates_mock_client(
    monkeypatch,
):
    monkeypatch.setenv(
        "SERVICENOW_MODE",
        "mock",
    )

    monkeypatch.setenv(
        "SERVICENOW_URL",
        "",
    )

    monkeypatch.setenv(
        "SERVICENOW_USERNAME",
        "",
    )

    monkeypatch.setenv(
        "SERVICENOW_PASSWORD",
        "",
    )

    get_settings.cache_clear()

    client = create_servicenow_client()

    assert isinstance(
        client,
        MockServiceNowClient,
    )