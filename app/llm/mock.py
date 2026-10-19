from app.llm.schemas import ResolutionAnalysis


def generate_mock_reasoning(
    incident_text: str,
    category: str,
    classification_confidence: float,
    retrieved_documents: list[dict],
) -> ResolutionAnalysis:

    if retrieved_documents:

        first_document = retrieved_documents[0]

        title = first_document.get(
            "title",
            "Relevant knowledge-base article",
        )

        content = first_document.get(
            "content",
            "",
        )

        resolution_steps = [
            step.strip()
            for step in content.split(",")
            if step.strip()
        ]

        if not resolution_steps:
            resolution_steps = [
                "Review the relevant internal IT procedure.",
                "Follow the approved troubleshooting workflow.",
                "Escalate if the issue persists.",
            ]

        return ResolutionAnalysis(
            problem_summary=(
                f"The incident concerns an IT issue in the "
                f"{category} category."
            ),
            likely_root_cause=(
                f"The available knowledge-base evidence suggests "
                f"that the incident may be related to the procedure "
                f"described in '{title}'."
            ),
            resolution_steps=resolution_steps,
            recommended_action=(
                "Follow the approved troubleshooting procedure "
                "described in the retrieved knowledge."
            ),
            confidence=min(
                max(classification_confidence, 0.0),
                1.0,
            ),
            risk_level="LOW",
            requires_human_approval=False,
        )

    return ResolutionAnalysis(
        problem_summary=(
            "The incident was classified, but no relevant "
            "knowledge-base evidence was retrieved."
        ),
        likely_root_cause=(
            "The available evidence is insufficient to determine "
            "a reliable root cause."
        ),
        resolution_steps=[
            "Collect additional diagnostic information.",
            "Retrieve relevant internal documentation.",
            "Escalate for human investigation if necessary.",
        ],
        recommended_action=(
            "Perform additional investigation before taking "
            "any external action."
        ),
        confidence=0.30,
        risk_level="HIGH",
        requires_human_approval=True,
    )