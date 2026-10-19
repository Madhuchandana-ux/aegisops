
from app.agents.nodes.decision import (
    decision_node,
    select_controlled_action,
)


def test_select_controlled_action_resolve():
    action = select_controlled_action(
        "Resolve the incident after applying the fix."
    )

    assert action == "resolve_incident"


def test_select_controlled_action_close():
    action = select_controlled_action(
        "Close the incident after verification."
    )

    assert action == "resolve_incident"


def test_unknown_proposal_does_not_default_to_work_note():
    action = select_controlled_action(
        "Provide troubleshooting instructions to the user."
    )

    assert action is None


def test_decision_requires_human_for_low_classification_confidence():
    state = {
        "classification_confidence": 0.60,
        "confidence": 0.90,
        "priority": "P3",
        "risk_level": "LOW",
        "proposed_resolution": "Add troubleshooting instructions.",
        "retrieved_documents": [
            {
                "document_id": "KB001",
                "title": "VPN Troubleshooting",
            }
        ],
        "reasoning_summary": "",
        "step_count": 0,
    }

    result = decision_node(state)

    assert result["policy_allowed"] is False
    assert result["requires_human"] is True
    assert result["selected_action"] == "request_human_approval"
    assert result["action_name"] == ""


def test_decision_requires_human_for_unknown_action():
    state = {
        "classification_confidence": 0.95,
        "confidence": 0.90,
        "priority": "P3",
        "risk_level": "LOW",
        "proposed_resolution": "Provide troubleshooting instructions.",
        "retrieved_documents": [
            {
                "document_id": "KB001",
                "title": "VPN Troubleshooting",
            }
        ],
        "reasoning_summary": "",
        "step_count": 0,
    }

    result = decision_node(state)

    assert result["policy_allowed"] is True
    assert result["requires_human"] is True
    assert result["selected_action"] == "request_human_approval"
    assert result["action_name"] == ""


def test_decision_blocks_high_priority_incident():
    state = {
        "classification_confidence": 0.95,
        "confidence": 0.90,
        "priority": "P1",
        "risk_level": "LOW",
        "proposed_resolution": "Add a work note.",
        "retrieved_documents": [
            {
                "document_id": "KB001",
                "title": "VPN Troubleshooting",
            }
        ],
        "reasoning_summary": "",
        "step_count": 0,
    }

    result = decision_node(state)

    assert result["policy_allowed"] is False
    assert result["requires_human"] is True
    assert result["selected_action"] == "request_human_approval"
    assert result["action_name"] == ""
