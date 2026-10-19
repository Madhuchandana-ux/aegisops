from pathlib import Path

from app.agents.state import AgentState
from app.ml.classifier import IncidentClassifier


PROJECT_ROOT = Path(__file__).resolve().parents[3]

MODEL_PATH = (
    PROJECT_ROOT
    / "models"
    / "incident_classifier_final.joblib"
)


_classifier = IncidentClassifier()
_classifier.load(MODEL_PATH)


def classification_node(
    state: AgentState,
) -> AgentState:

    incident_text = state.get(
        "incident_text",
        "",
    ).strip()

    if not incident_text:
        state["errors"] = [
            "Incident description is empty."
        ]
        return state

    result = _classifier.predict(
        incident_text
    )

    state["category"] = result.category

    state["subcategory"] = "unknown"

    state["classification_confidence"] = (
        result.confidence
    )

    state["classification_model"] = (
        "word_char_tfidf_linear_svm"
    )

    # Preserve classifier confidence as the
    # current overall confidence until the
    # reasoning stage produces its own confidence.
    state["confidence"] = result.confidence

    state["step_count"] = (
        state.get("step_count", 0) + 1
    )

    return state