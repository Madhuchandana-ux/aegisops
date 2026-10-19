from app.security.policy import evaluate_policy


def test_low_confidence_requires_human():

    result = evaluate_policy(
        classification_confidence=0.60,
        reasoning_confidence=0.90,
        priority="P3",
        risk_level="LOW",
        proposed_action="Troubleshoot VPN",
        has_retrieved_evidence=True,
    )

    assert result.allowed is False
    assert result.requires_human is True
    assert result.risk_level == "HIGH"


def test_high_priority_requires_human():

    result = evaluate_policy(
        classification_confidence=0.95,
        reasoning_confidence=0.95,
        priority="P1",
        risk_level="LOW",
        proposed_action="Troubleshoot VPN",
        has_retrieved_evidence=True,
    )

    assert result.allowed is False
    assert result.requires_human is True


def test_no_evidence_requires_human():

    result = evaluate_policy(
        classification_confidence=0.95,
        reasoning_confidence=0.95,
        priority="P3",
        risk_level="LOW",
        proposed_action="Troubleshoot VPN",
        has_retrieved_evidence=False,
    )

    assert result.allowed is False
    assert result.requires_human is True


def test_dangerous_action_requires_human():

    result = evaluate_policy(
        classification_confidence=0.95,
        reasoning_confidence=0.95,
        priority="P3",
        risk_level="LOW",
        proposed_action="Reset password",
        has_retrieved_evidence=True,
    )

    assert result.allowed is False
    assert result.requires_human is True


def test_safe_action_can_be_automated():

    result = evaluate_policy(
        classification_confidence=0.95,
        reasoning_confidence=0.95,
        priority="P3",
        risk_level="LOW",
        proposed_action="Provide troubleshooting instructions",
        has_retrieved_evidence=True,
    )

    assert result.allowed is True
    assert result.requires_human is False
    assert result.risk_level == "LOW"
def test_prompt_injection_requires_human_approval():
    decision = evaluate_policy(
        classification_confidence=0.95,
        reasoning_confidence=0.95,
        priority="P3",
        risk_level="LOW",
        proposed_action="Add a troubleshooting work note",
        has_retrieved_evidence=True,
        prompt_injection_detected=True,
    )

    assert decision.allowed is False
    assert decision.requires_human is True
    assert decision.risk_level == "HIGH"
    assert "prompt injection" in decision.reason.lower()