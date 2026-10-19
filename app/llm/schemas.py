from pydantic import BaseModel, Field


class ResolutionAnalysis(BaseModel):

    problem_summary: str = Field(
        description=(
            "A concise summary of the IT incident."
        )
    )

    likely_root_cause: str = Field(
        description=(
            "The likely cause based only on "
            "the incident and retrieved evidence."
        )
    )

    resolution_steps: list[str] = Field(
        description=(
            "Ordered troubleshooting or resolution "
            "steps supported by the retrieved evidence."
        )
    )

    recommended_action: str = Field(
        description=(
            "The recommended next action. "
            "Do not claim that an external action "
            "was executed."
        )
    )

    confidence: float = Field(
        ge=0.0,
        le=1.0,
        description=(
            "Confidence in the proposed resolution."
        )
    )

    risk_level: str = Field(
        description=(
            "Risk classification: LOW, MEDIUM, or HIGH."
        )
    )

    requires_human_approval: bool = Field(
        description=(
            "Whether human approval should be required "
            "before any external action."
        )
    )