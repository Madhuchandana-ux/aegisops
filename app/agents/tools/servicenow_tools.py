
from typing import Any

from app.security.rbac import can_execute_action
from app.servicenow.factory import create_servicenow_client
from app.servicenow.incidents import IncidentService


# ============================================================
# INTERNAL AUTHORIZATION HELPER
# ============================================================

def _require_action_permission(
    role: str,
    action_name: str,
) -> None:
    """
    Verify that the supplied role can execute the requested
    controlled ServiceNow action.

    Unknown actions are denied by the RBAC layer.
    """

    if not can_execute_action(
        role,
        action_name,
    ):
        raise PermissionError(
            f"Role '{role}' is not authorized "
            f"to execute action '{action_name}'."
        )


# ============================================================
# GET INCIDENT
# ============================================================

def get_incident_tool(
    sys_id: str,
    role: str = "viewer",
) -> dict[str, Any]:
    """
    Retrieve a ServiceNow incident.

    Requires:
        incident:view
    """

    _require_action_permission(
        role,
        "get_incident",
    )
    client = create_servicenow_client()

    service = IncidentService(
        client
    )

    return service.get_incident(
        sys_id
    )


# ============================================================
# ADD WORK NOTE
# ============================================================

def add_work_note_tool(
    sys_id: str,
    work_note: str,
    role: str = "analyst",
) -> dict[str, Any]:
    """
    Add a work note to a ServiceNow incident.

    Requires:
        incident:add_work_note
    """

    _require_action_permission(
        role,
        "add_work_note",
    )

    client = create_servicenow_client()

    service = IncidentService(
        client
    )

    return service.add_work_note(
        sys_id=sys_id,
        work_note=work_note,
    )


# ============================================================
# UPDATE INCIDENT
# ============================================================

def update_incident_tool(
    sys_id: str,
    fields: dict[str, Any],
    role: str = "operator",
) -> dict[str, Any]:
    """
    Update a ServiceNow incident.

    Requires:
        incident:update
    """

    _require_action_permission(
        role,
        "update_incident",
    )

    client = create_servicenow_client()

    service = IncidentService(
        client
    )

    return service.update_incident(
        sys_id=sys_id,
        fields=fields,
    )


# ============================================================
# RESOLVE INCIDENT
# ============================================================

def resolve_incident_tool(
    sys_id: str,
    resolution_notes: str,
    role: str = "operator",
) -> dict[str, Any]:
    """
    Resolve a ServiceNow incident.

    Requires:
        incident:resolve
    """

    _require_action_permission(
        role,
        "resolve_incident",
    )

    client = create_servicenow_client()

    service = IncidentService(
        client
    )

    return service.resolve_incident(
        sys_id=sys_id,
        resolution_notes=resolution_notes,
    )
