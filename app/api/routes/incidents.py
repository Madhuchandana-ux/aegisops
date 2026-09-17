from fastapi import APIRouter
from pydantic import BaseModel, Field


router = APIRouter(
    prefix="/api/v1/incidents",
    tags=["Incidents"],
)


class IncidentRequest(BaseModel):
    """
    Data submitted by a user or external system
    when creating an incident-analysis request.
    """

    incident_id: str | None = Field(
        default=None,
        description="ServiceNow incident number.",
    )

    description: str = Field(
        min_length=5,
        description="Description of the IT incident.",
    )

    caller: str | None = Field(
        default=None,
        description="Person reporting the incident.",
    )


class IncidentResponse(BaseModel):
    """
    Temporary response.

    The response will become much richer once
    the agentic workflow is implemented.
    """

    status: str
    message: str
    incident_id: str | None = None


@router.post(
    "/analyze",
    response_model=IncidentResponse,
)
async def analyze_incident(
    request: IncidentRequest,
):
    """
    Receive an incident-analysis request.

    Agent processing will be connected later.
    """

    return IncidentResponse(
        status="received",
        message=(
            "Incident received. "
            "Agent analysis will be connected "
            "in a later phase."
        ),
        incident_id=request.incident_id,
    )