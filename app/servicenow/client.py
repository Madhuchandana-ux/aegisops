from typing import Any

import httpx


class ServiceNowError(Exception):
    """Base exception for ServiceNow-related errors."""


class ServiceNowClient:
    """
    Client for communicating with the ServiceNow REST API.

    The client is responsible only for HTTP communication.
    Business rules and authorization belong elsewhere.
    """

    def __init__(
        self,
        base_url: str,
        username: str,
        password: str,
        timeout: float = 10.0,
    ):
        self.base_url = base_url.rstrip("/")
        self.username = username
        self.password = password
        self.timeout = timeout

    def _build_url(self, endpoint: str) -> str:
        """
        Build a complete ServiceNow API URL.
        """

        endpoint = endpoint.lstrip("/")

        return f"{self.base_url}/{endpoint}"

    def _headers(self) -> dict[str, str]:
        """
        Return standard HTTP headers.
        """

        return {
            "Accept": "application/json",
            "Content-Type": "application/json",
        }

    def get(
        self,
        endpoint: str,
        params: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        """
        Send a GET request to ServiceNow.
        """

        url = self._build_url(endpoint)

        try:
            response = httpx.get(
                url,
                auth=(self.username, self.password),
                headers=self._headers(),
                params=params,
                timeout=self.timeout,
            )

            response.raise_for_status()

        except httpx.HTTPError as exc:
            raise ServiceNowError(
                f"ServiceNow GET request failed: {exc}"
            ) from exc

        return response.json()

    def post(
        self,
        endpoint: str,
        payload: dict[str, Any],
    ) -> dict[str, Any]:
        """
        Send a POST request to ServiceNow.
        """

        url = self._build_url(endpoint)

        try:
            response = httpx.post(
                url,
                auth=(self.username, self.password),
                headers=self._headers(),
                json=payload,
                timeout=self.timeout,
            )

            response.raise_for_status()

        except httpx.HTTPError as exc:
            raise ServiceNowError(
                f"ServiceNow POST request failed: {exc}"
            ) from exc

        return response.json()

    def patch(
        self,
        endpoint: str,
        payload: dict[str, Any],
    ) -> dict[str, Any]:
        """
        Send a PATCH request to ServiceNow.
        """

        url = self._build_url(endpoint)

        try:
            response = httpx.patch(
                url,
                auth=(self.username, self.password),
                headers=self._headers(),
                json=payload,
                timeout=self.timeout,
            )

            response.raise_for_status()

        except httpx.HTTPError as exc:
            raise ServiceNowError(
                f"ServiceNow PATCH request failed: {exc}"
            ) from exc

        return response.json()