from app.agents.state import AgentState
from app.config import get_settings
from app.llm.client import create_llm
from app.llm.mock import generate_mock_reasoning
from app.llm.prompts import (
    SYSTEM_PROMPT,
    USER_PROMPT_TEMPLATE,
)
from app.llm.schemas import ResolutionAnalysis


def build_retrieved_context(
    documents: list[dict],
) -> str:

    if not documents:
        return (
            "No relevant knowledge-base documents "
            "were retrieved."
        )

    context_parts = []

    for index, document in enumerate(
        documents,
        start=1,
    ):

        context_parts.append(
            f"""
DOCUMENT {index}

ID:
{document.get("kb_id", "unknown")}

TITLE:
{document.get("title", "unknown")}

CATEGORY:
{document.get("category", "unknown")}

CONTENT:
{document.get("content", "")}
""".strip()
        )

    return "\n\n".join(context_parts)


def run_reasoning(
    state: AgentState,
) -> AgentState:

    settings = get_settings()

    incident_text = state.get(
        "incident_text",
        "",
    )

    category = state.get(
        "category",
        "unknown",
    )

    classification_confidence = state.get(
        "classification_confidence",
        0.0,
    )

    retrieved_documents = state.get(
        "retrieved_documents",
        [],
    )

    # ============================================================
    # MOCK PROVIDER
    # ============================================================

    if settings.llm_provider.lower() == "mock":

        result = generate_mock_reasoning(
            incident_text=incident_text,
            category=category,
            classification_confidence=(
                classification_confidence
            ),
            retrieved_documents=retrieved_documents,
        )

    # ============================================================
    # REAL LLM PROVIDERS
    # ============================================================

    else:

        retrieved_context = build_retrieved_context(
            retrieved_documents
        )

        user_prompt = USER_PROMPT_TEMPLATE.format(
            incident_text=incident_text,
            category=category,
            classification_confidence=(
                classification_confidence
            ),
            retrieved_context=retrieved_context,
        )

        llm = create_llm()

        structured_llm = llm.with_structured_output(
            ResolutionAnalysis
        )

        result = structured_llm.invoke(
            [
                (
                    "system",
                    SYSTEM_PROMPT,
                ),
                (
                    "human",
                    user_prompt,
                ),
            ]
        )

    # ============================================================
    # MAP STRUCTURED OUTPUT INTO AGENT STATE
    # ============================================================

    state["analysis"] = result.problem_summary

    state["proposed_resolution"] = (
        "\n".join(
            result.resolution_steps
        )
    )

    state["reasoning_summary"] = (
        result.likely_root_cause
    )

    state["confidence"] = (
        result.confidence
    )

    state["risk_level"] = (
        result.risk_level.upper()
    )

    state["requires_human"] = (
        result.requires_human_approval
    )

    state["selected_action"] = (
        result.recommended_action
    )

    state["step_count"] = (
        state.get("step_count", 0) + 1
    )

    return state