from app.agents.graph import build_initial_state
from app.llm.reasoning import run_reasoning


def main():

    print("=" * 70)
    print("AegisOps LLM Reasoning Test")
    print("=" * 70)

    state = build_initial_state(
        incident_id="LLMTEST001",
        incident_text=(
            "User cannot connect to the "
            "corporate VPN from home."
        ),
        caller="test_user",
    )

    state["category"] = "network"

    state["classification_confidence"] = 0.92

    state["retrieved_documents"] = [
        {
            "kb_id": "KB001",
            "title": (
                "VPN Connection Troubleshooting"
            ),
            "category": "network",
            "content": (
                "If a user cannot connect to "
                "the corporate VPN, verify "
                "network connectivity, confirm "
                "the VPN client configuration, "
                "clear cached credentials, and "
                "authenticate again."
            ),
        }
    ]

    result = run_reasoning(
        state
    )

    print()
    print("Problem summary:")
    print(result["analysis"])

    print()
    print("Likely root cause:")
    print(result["reasoning_summary"])

    print()
    print("Proposed resolution:")
    print(result["proposed_resolution"])

    print()
    print(
        "Confidence:",
        result["confidence"],
    )

    print()
    print(
        "Risk level:",
        result["risk_level"],
    )

    print()
    print(
        "Human approval required:",
        result["requires_human"],
    )

    print()
    print("=" * 70)


if __name__ == "__main__":
    main()