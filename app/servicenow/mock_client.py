from typing import Any

from app.servicenow.client import ServiceNowError


class MockServiceNowClient:
    """
    Local in-memory ServiceNow simulator.

    This class implements the same basic interface used by
    IncidentService:

        get()
        post()
        patch()

    It is intended for local development and demonstrations.

    It does NOT make network requests.
    """

    _records: dict[str, dict[str, Any]] = {}

    def __init__(
        self,
        base_url: str = "mock://servicenow",
        username: str = "mock-user",
        password: str = "",
        timeout: float = 10.0,
    ):
        self.base_url = base_url
        self.username = username
        self.password = password
        self.timeout = timeout

    def _extract_sys_id(
        self,
        endpoint: str,
    ) -> str:
        endpoint = endpoint.rstrip("/")

        if "/" not in endpoint:
            raise ServiceNowError(
                "Invalid mock ServiceNow endpoint."
            )

        return endpoint.rsplit("/", 1)[-1]

    @classmethod
    def _create_default_record(
        cls,
        sys_id: str,
    ) -> dict[str, Any]:
        record = {
            "sys_id": sys_id,
            "number": sys_id,
            "short_description": (
                "Mock AegisOps incident"
            ),
            "description": "",
            "state": "2",
            "priority": "3",
            "category": "inquiry",
            "work_notes": "",
            "close_notes": "",
        }

        cls._records[sys_id] = record

        return record

    def get(
        self,
        endpoint: str,
        params: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        """
        Simulate GET /incident/{sys_id}.
        """

        sys_id = self._extract_sys_id(
            endpoint
        )

        record = self._records.get(sys_id)

        if record is None:
            raise ServiceNowError(
                f"Mock ServiceNow incident '{sys_id}' "
                "does not exist."
            )

        return {
            "result": dict(record)
        }

    def post(
        self,
        endpoint: str,
        payload: dict[str, Any],
    ) -> dict[str, Any]:
        """
        Simulate creating an incident.
        """

        sys_id = (
            f"MOCK-{len(self._records) + 1:04d}"
        )

        record = {
            "sys_id": sys_id,
            "number": sys_id,
            "short_description": payload.get(
                "short_description",
                "Mock incident",
            ),
            "description": payload.get(
                "description",
                "",
            ),
            "state": "1",
            "priority": payload.get(
                "priority",
                "3",
            ),
            "category": payload.get(
                "category",
                "inquiry",
            ),
            "work_notes": "",
            "close_notes": "",
        }

        self._records[sys_id] = record

        return {
            "result": dict(record)
        }

    def patch(
        self,
        endpoint: str,
        payload: dict[str, Any],
    ) -> dict[str, Any]:
        """
        Simulate updating an incident.

        For demo purposes, PATCH automatically creates the
        mock record if the target does not already exist.
        """

        sys_id = self._extract_sys_id(
            endpoint
        )

        record = self._records.get(sys_id)

        if record is None:
            record = self._create_default_record(
                sys_id
            )

        for field, value in payload.items():

            if field == "work_notes":
                existing_notes = record.get(
                    "work_notes",
                    "",
                )

                if existing_notes:
                    record["work_notes"] = (
                        f"{existing_notes}\n{value}"
                    )
                else:
                    record["work_notes"] = str(value)

            else:
                record[field] = value

        self._records[sys_id] = record

        return {
            "result": dict(record)
        }