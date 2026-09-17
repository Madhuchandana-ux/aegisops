from dataclasses import dataclass


@dataclass
class IncidentRecord:
    """
    Standard representation of an IT incident.

    This schema is shared by the ML and agent layers.
    """

    incident_id: str
    short_description: str
    description: str

    category: str
    subcategory: str

    priority: str
    impact: int
    urgency: int

    resolution: str = ""