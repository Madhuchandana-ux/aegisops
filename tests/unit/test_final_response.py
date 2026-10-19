from app.agents.nodes.final_response import (
    final_response_node,
)


def test_final_response_for_verified_execution():
    state = {
        "incident_id": "INC0010001",
        "category": "Support general",
        "priority": "P3",
        "classification_confidence": 0.767,
        "risk_level": "LOW",
        "proposed_resolution": (
            "Verify network connectivity."
        ),
        "selected_action": "automated_resolution",
        "requires_human": False,
        "policy_reason": "",
        "action_result": {
            "status": "executed",
        },
        "verification_result": {
            "status": "verified",
            "verified": True,
        },
    }

    result = final_response_node(state)

    assert result["final_response"]

    assert (
        "INC0010001"
        in result["final_response"]
    )

    assert (
        "VERIFIED"
        in result["final_response"]
    )

    assert (
        result["step_count"]
        == 1
    )


def test_final_response_for_human_approval():
    state = {
        "incident_id": "INC0010002",
        "category": "Support general",
        "priority": "P2",
        "classification_confidence": 0.80,
        "risk_level": "HIGH",
        "proposed_resolution": (
            "Reset the user's password."
        ),
        "selected_action": (
            "request_human_approval"
        ),
        "requires_human": True,
        "policy_reason": (
            "High-risk actions require human approval."
        ),
        "action_result": {
            "status": "pending",
        },
        "verification_result": {
            "status": "not_executed",
            "verified": False,
        },
    }

    result = final_response_node(state)

    assert (
        "HUMAN APPROVAL REQUIRED"
        in result["final_response"]
    )

    assert (
        "No external ServiceNow action"
        in result["final_response"]
    )


def test_final_response_for_blocked_action():
    state = {
        "incident_id": "INC0010003",
        "category": "Software",
        "priority": "P3",
        "classification_confidence": 0.90,
        "risk_level": "HIGH",
        "proposed_resolution": "Restricted action.",
        "selected_action": "blocked",
        "requires_human": False,
        "policy_reason": "",
        "action_result": {
            "status": "blocked",
            "message": "Policy blocked the action.",
        },
        "verification_result": {
            "status": "not_executed",
            "verified": False,
        },
    }

    result = final_response_node(state)

    assert (
        "BLOCKED"
        in result["final_response"]
    )

    assert (
        "Policy blocked the action."
        in result["final_response"]
    )