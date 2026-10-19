from app.agents.graph import (
    agent_graph,
    build_initial_state,
)


def test_agent_graph_uses_trained_classifier():

    state = build_initial_state(
        incident_id="TEST001",
        incident_text=(
            "User cannot access the file server."
        ),
        caller="test_user",
    )

    result = agent_graph.invoke(state)

    assert result["category"] != ""

    assert (
        "classification_confidence"
        in result
    )

    assert (
        result["classification_model"]
        == "word_char_tfidf_linear_svm"
    )

    assert (
        0.0
        <= result["classification_confidence"]
        <= 1.0
    )