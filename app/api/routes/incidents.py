import logging

from fastapi import APIRouter, Depends, HTTPException, Request
from pydantic import BaseModel, Field

from app.agents.graph import (
    build_initial_state,
    validate_incident,
)
from app.api.dependencies import require_action


logger = logging.getLogger(__name__)


router = APIRouter(
    prefix="/api/v1/incidents",
    tags=["Incidents"],
)


class IncidentRequest(BaseModel):
    """
    Request model used when an IT incident is submitted.
    """

    incident_id: str | None = Field(
        default=None,
        description="ServiceNow incident number.",
        examples=["INC0010001"],
    )

    description: str = Field(
        min_length=5,
        max_length=5000,
        description="Description of the IT incident.",
        examples=[
            "VPN connection fails when connecting from home."
        ],
    )

    caller: str | None = Field(
        default=None,
        max_length=255,
        description="Person reporting the incident.",
        examples=["employee01"],
    )


class IncidentResponse(BaseModel):
    """
    Standard response returned by the incident API.
    """

    status: str
    message: str
    incident_id: str | None = None
    validated: bool
    request_id: str


@router.post(
    "",
    response_model=IncidentResponse,
)
async def create_incident(
    request: Request,
    incident: IncidentRequest,
    current_user: dict = Depends(
        require_action("create_incident")
    ),
):
    """
    Receive and validate a new IT incident.

    The endpoint requires an authenticated user with
    the 'create_incident' permission.
    """

    request_id = getattr(
        request.state,
        "request_id",
        "unknown",
    )

    incident_id = (
        incident.incident_id
        or "LOCAL-INCIDENT"
    )

    logger.info(
        "Incident received | request_id=%s | "
        "incident_id=%s | username=%s | role=%s",
        request_id,
        incident_id,
        current_user["username"],
        current_user["role"],
    )

    state = build_initial_state(
    incident_id=incident_id,
    incident_text=incident.description,
    caller=incident.caller or "",
    username=current_user["username"],
    user_role=current_user["role"],
)

    state = validate_incident(state)

    if state.get("errors"):
        logger.warning(
            "Incident validation failed | "
            "request_id=%s | incident_id=%s",
            request_id,
            incident_id,
        )

        raise HTTPException(
            status_code=400,
            detail=state["errors"],
        )

    logger.info(
    "Incident received | request_id=%s | "
    "incident_id=%s | username=%s | role=%s",
    request_id,
    incident_id,
    current_user["username"],
    current_user["role"],
)

    return IncidentResponse(
        status="received",
        message=(
            "Incident successfully received "
            "and validated."
        ),
        incident_id=incident_id,
        validated=True,
        request_id=request_id,
    )