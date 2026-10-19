from dataclasses import dataclass


@dataclass
class PolicyDecision:
    """
    Result produced by the AegisOps policy engine.

    The policy engine is deterministic.
    It does not rely on the LLM to authorize actions.
    """

    allowed: bool
    requires_human: bool
    risk_level: str
    reason: str


# ============================================================
# RISKY ACTION KEYWORDS
# ============================================================

HIGH_RISK_ACTION_KEYWORDS = {
    "delete",
    "remove",
    "disable",
    "unlock",
    "reset password",
    "change password",
    "modify permissions",
    "grant access",
    "revoke access",
    "restart server",
    "shutdown",
    "stop service",
}


def evaluate_policy(
    *,
    classification_confidence: float,
    reasoning_confidence: float,
    priority: str,
    risk_level: str,
    proposed_action: str,
    has_retrieved_evidence: bool,
    prompt_injection_detected: bool = False,
) -> PolicyDecision:

    priority = priority.upper().strip()
    risk_level = risk_level.upper().strip()
    proposed_action = proposed_action.lower().strip()

    if prompt_injection_detected:
        return PolicyDecision(
            False,
            True,
            "HIGH",
            "Potential prompt injection was detected. External automation requires human approval.",
        )

    if not has_retrieved_evidence:
        return PolicyDecision(
            False,
            True,
            "HIGH",
            "No relevant knowledge-base evidence was retrieved.",
        )

    if classification_confidence < 0.70:
        return PolicyDecision(
            False,
            True,
            "HIGH",
            "Classification confidence is below the minimum automation threshold.",
        )

    if reasoning_confidence < 0.70:
        return PolicyDecision(
            False,
            True,
            "HIGH",
            "Reasoning confidence is below the minimum automation threshold.",
        )

    if priority in {"P1", "P2"}:
        return PolicyDecision(
            False,
            True,
            "HIGH",
            f"{priority} incidents require human approval.",
        )

    if risk_level == "HIGH":
        return PolicyDecision(
            False,
            True,
            "HIGH",
            "The reasoning component identified the proposed resolution as high risk.",
        )

    for keyword in HIGH_RISK_ACTION_KEYWORDS:
        if keyword in proposed_action:
            return PolicyDecision(
                False,
                True,
                "HIGH",
                f"The proposed action contains a restricted operation: '{keyword}'.",
            )

    if risk_level == "MEDIUM":
        return PolicyDecision(
            False,
            True,
            "MEDIUM",
            "Medium-risk actions require human approval.",
        )

    return PolicyDecision(
        True,
        False,
        "LOW",
        "The proposed action passed all automation policy checks.",
    )