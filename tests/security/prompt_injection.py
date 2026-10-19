
import re
from dataclasses import dataclass


# ============================================================
# DETECTION RESULT
# ============================================================


@dataclass
class InjectionDetectionResult:
    detected: bool
    risk_level: str
    matched_patterns: list[str]
    message: str


# ============================================================
# SUSPICIOUS PATTERNS
# ============================================================

INJECTION_PATTERNS = {
    "ignore_previous_instructions": [
        r"ignore\s+(all\s+)?previous\s+instructions",
        r"ignore\s+(all\s+)?prior\s+instructions",
        r"disregard\s+(all\s+)?previous\s+instructions",
        r"forget\s+(all\s+)?previous\s+instructions",
    ],

    "system_prompt_extraction": [
        r"reveal\s+(the\s+)?system\s+prompt",
        r"show\s+(me\s+)?(the\s+)?system\s+prompt",
        r"print\s+(the\s+)?system\s+prompt",
        r"tell\s+me\s+(the\s+)?system\s+prompt",
    ],

    "instruction_override": [
        r"you\s+are\s+now\s+",
        r"from\s+now\s+on\s+you\s+must",
        r"your\s+new\s+instructions\s+are",
        r"override\s+your\s+instructions",
    ],

    "privilege_escalation": [
        r"grant\s+me\s+admin",
        r"give\s+me\s+admin\s+access",
        r"bypass\s+(the\s+)?security",
        r"bypass\s+(the\s+)?authorization",
        r"disable\s+(the\s+)?security",
    ],

    "tool_manipulation": [
        r"call\s+the\s+service\s*now\s+api",
        r"execute\s+the\s+tool",
        r"run\s+the\s+tool",
        r"resolve\s+this\s+incident\s+immediately",
    ],
}


# ============================================================
# DETECTOR
# ============================================================


def detect_prompt_injection(
    text: str,
) -> InjectionDetectionResult:
    """
    Detect common prompt-injection patterns.

    This is a defensive heuristic layer.

    Detection does NOT mean that the text is definitely
    malicious. It means the text contains patterns that
    should not be treated as trusted instructions.
    """

    if not text or not text.strip():
        return InjectionDetectionResult(
            detected=False,
            risk_level="LOW",
            matched_patterns=[],
            message="No text was provided.",
        )

    normalized_text = text.lower()

    matched_patterns: list[str] = []

    for category, patterns in INJECTION_PATTERNS.items():

        for pattern in patterns:

            if re.search(
                pattern,
                normalized_text,
            ):
                matched_patterns.append(
                    category
                )

                # One match per category is enough.
                break

    if not matched_patterns:

        return InjectionDetectionResult(
            detected=False,
            risk_level="LOW",
            matched_patterns=[],
            message=(
                "No known prompt-injection "
                "pattern was detected."
            ),
        )

    return InjectionDetectionResult(
        detected=True,
        risk_level="HIGH",
        matched_patterns=matched_patterns,
        message=(
            "Potential prompt injection detected. "
            "The content must be treated as untrusted data."
        ),
    )
