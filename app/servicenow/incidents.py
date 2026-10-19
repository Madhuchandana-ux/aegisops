from typing import Any

from app.servicenow.client import ServiceNowClient


class IncidentService:
    """
    Controlled ServiceNow incident operations.

    This class exposes only the incident operations that
    AegisOps is allowed to perform.
    """

    INCIDENT_ENDPOINT = "/api/now/table/incident"

    def __init__(self, client: ServiceNowClient):
        self.client = client

    def get_incident(
        self,
        sys_id: str,
    ) -> dict[str, Any]:
        """
        Retrieve one ServiceNow incident by sys_id.
        """

        if not sys_id or not sys_id.strip():
            raise ValueError("sys_id cannot be empty.")

        return self.client.get(
            f"{self.INCIDENT_ENDPOINT}/{sys_id}"
        )

    def create_incident(
        self,
        short_description: str,
        description: str = "",
        category: str | None = None,
        priority: str | None = None,
    ) -> dict[str, Any]:
        """
        Create a new ServiceNow incident.
        """

        if not short_description.strip():
            raise ValueError(
                "short_description cannot be empty."
            )

        payload: dict[str, Any] = {
            "short_description": short_description,
            "description": description,
        }

        if category:
            payload["category"] = category

        if priority:
            payload["priority"] = priority

        return self.client.post(
            self.INCIDENT_ENDPOINT,
            payload,
        )

    def update_incident(
        self,
        sys_id: str,
        fields: dict[str, Any],
    ) -> dict[str, Any]:
        """
        Update approved incident fields.
        """

        if not sys_id or not sys_id.strip():
            raise ValueError("sys_id cannot be empty.")

        if not fields:
            raise ValueError(
                "At least one field is required."
            )

        return self.client.patch(
            f"{self.INCIDENT_ENDPOINT}/{sys_id}",
            fields,
        )

    def add_work_note(
        self,
        sys_id: str,
        work_note: str,
    ) -> dict[str, Any]:
        """
        Add a work note to an incident.
        """

        if not sys_id or not sys_id.strip():
            raise ValueError("sys_id cannot be empty.")

        if not work_note.strip():
            raise ValueError(
                "work_note cannot be empty."
            )

        return self.client.patch(
            f"{self.INCIDENT_ENDPOINT}/{sys_id}",
            {
                "work_notes": work_note,
            },
        )

    def resolve_incident(
        self,
        sys_id: str,
        resolution_notes: str,
    ) -> dict[str, Any]:
        """
        Resolve an incident using the approved
        ServiceNow incident state.
        """

        if not sys_id or not sys_id.strip():
            raise ValueError("sys_id cannot be empty.")

        if not resolution_notes.strip():
            raise ValueError(
                "resolution_notes cannot be empty."
            )

        payload = {
            "state": "6",
            "close_notes": resolution_notes,
        }

        return self.client.patch(
            f"{self.INCIDENT_ENDPOINT}/{sys_id}",
            payload,
        )