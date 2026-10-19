import os

from app.config import get_settings
from app.servicenow.client import ServiceNowClient
from app.servicenow.mock_client import MockServiceNowClient


def create_servicenow_client():
    """
    Create the configured ServiceNow client.

    Supported modes:

        mock
            Uses the local in-memory ServiceNow simulator.

        real
            Uses the actual ServiceNow REST API.
    """

    settings = get_settings()

    mode = os.getenv(
        "SERVICENOW_MODE",
        "real",
    ).strip().lower()

    # ========================================================
    # MOCK MODE
    # ========================================================

    if mode == "mock":
        return MockServiceNowClient()

    # ========================================================
    # INVALID MODE
    # ========================================================

    if mode != "real":
        raise RuntimeError(
            f"Unsupported SERVICENOW_MODE: '{mode}'. "
            "Expected 'mock' or 'real'."
        )

    # ========================================================
    # REAL MODE VALIDATION
    # ========================================================

    if not settings.servicenow_url:
        raise RuntimeError(
            "SERVICENOW_URL is not configured."
        )

    if not settings.servicenow_username:
        raise RuntimeError(
            "SERVICENOW_USERNAME is not configured."
        )

    if not settings.servicenow_password:
        raise RuntimeError(
            "SERVICENOW_PASSWORD is not configured."
        )

    return ServiceNowClient(
        base_url=settings.servicenow_url,
        username=settings.servicenow_username,
        password=settings.servicenow_password,
        timeout=settings.servicenow_timeout,
    )