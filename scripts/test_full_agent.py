from app.agents.graph import (
    agent_graph,
    build_initial_state,
)


def main():

    print("=" * 70)
    print("AegisOps Full Agent Test")
    print("=" * 70)

    # ========================================================
    # INPUT INCIDENT
    # ========================================================

    incident_text = (
        "User cannot connect to the corporate VPN "
        "from home."
    )

    print()
    print("Incident:")
    print(incident_text)

    # ========================================================
    # BUILD INITIAL STATE
    # ========================================================

    state = build_initial_state(
        incident_id="E2E001",
        incident_text=incident_text,
        caller="test_user",
    )

    # ========================================================
    # RUN COMPLETE LANGGRAPH
    # ========================================================

    result = agent_graph.invoke(state)

    # ========================================================
    # CLASSIFICATION
    # ========================================================

    print()
    print("-" * 70)
    print("CLASSIFICATION")
    print("-" * 70)

    print(
        "Category:",
        result.get("category"),
    )

    print(
        "Classification confidence:",
        result.get(
            "classification_confidence"
        ),
    )

    print(
        "Classification model:",
        result.get(
            "classification_model"
        ),
    )

    # ========================================================
    # RETRIEVAL
    # ========================================================

    print()
    print("-" * 70)
    print("RETRIEVED KNOWLEDGE")
    print("-" * 70)

    documents = result.get(
        "retrieved_documents",
        [],
    )

    if not documents:

        print("No documents retrieved.")

    else:

        for rank, document in enumerate(
            documents,
            start=1,
        ):

            print()
            print(
                f"{rank}. "
                f"{document.get('kb_id')}"
            )

            print(
                "Title:",
                document.get(
                    "title"
                ),
            )

            print(
                "Category:",
                document.get(
                    "category"
                ),
            )

            print(
                "Reranker score:",
                document.get(
                    "reranker_score"
                ),
            )

            print(
                "Retrieval sources:",
                document.get(
                    "retrieval_sources"
                ),
            )

    # ========================================================
    # LLM / REASONING
    # ========================================================

    print()
    print("-" * 70)
    print("REASONING")
    print("-" * 70)

    print()
    print("Analysis:")

    print(
        result.get(
            "analysis",
            "",
        )
    )

    print()
    print("Likely root cause:")

    print(
        result.get(
            "reasoning_summary",
            "",
        )
    )

    print()
    print("Proposed resolution:")

    print(
        result.get(
            "proposed_resolution",
            "",
        )
    )

    print()
    print(
        "Reasoning confidence:",
        result.get(
            "confidence"
        ),
    )

    # ========================================================
    # DECISION
    # ========================================================

    print()
    print("-" * 70)
    print("DECISION")
    print("-" * 70)

    print(
        "Risk level:",
        result.get(
            "risk_level"
        ),
    )

    print(
        "Human approval required:",
        result.get(
            "requires_human"
        ),
    )

    print(
        "Selected action:",
        result.get(
            "selected_action"
        ),
    )

    # ========================================================
    # ACTION
    # ========================================================

    print()
    print("-" * 70)
    print("ACTION")
    print("-" * 70)

    print(
        result.get(
            "action_result"
        )
    )

    # ========================================================
    # VERIFICATION
    # ========================================================

    print()
    print("-" * 70)
    print("VERIFICATION")
    print("-" * 70)

    print(
        result.get(
            "verification_result"
        )
    )

    # ========================================================
    # FINAL STATE
    # ========================================================

    print()
    print("-" * 70)
    print("GRAPH EXECUTION")
    print("-" * 70)

    print(
        "Steps executed:",
        result.get(
            "step_count"
        ),
    )

    print(
        "Errors:",
        result.get(
            "errors"
        ),
    )

    print()
    print("=" * 70)
    print("Full agent test completed.")
    print("=" * 70)


if __name__ == "__main__":
    main()