from pathlib import Path

import pandas as pd

from app.ml.model_comparison import (
    build_linear_svm,
    build_logistic_regression,
    evaluate_model,
)


PROJECT_ROOT = Path(__file__).resolve().parents[1]

TRAIN_PATH = (
    PROJECT_ROOT
    / "data"
    / "processed"
    / "external"
    / "aegisops_train_final.csv"
)

TEST_PATH = (
    PROJECT_ROOT
    / "data"
    / "processed"
    / "external"
    / "aegisops_test_final.csv"
)


def main():

    print("=" * 70)
    print("AegisOps Classification Model Comparison")
    print("=" * 70)

    train_df = pd.read_csv(
        TRAIN_PATH
    )

    test_df = pd.read_csv(
        TEST_PATH
    )

    print(
        f"\nTraining records: {len(train_df)}"
    )

    print(
        f"Test records: {len(test_df)}"
    )

    models = [
        (
            "Logistic Regression",
            build_logistic_regression(),
        ),
        (
            "Linear SVM",
            build_linear_svm(),
        ),
    ]

    results = []

    for model_name, model in models:

        print("\n" + "-" * 70)

        print(
            f"Training: {model_name}"
        )

        print("-" * 70)

        result = evaluate_model(
            model=model,
            model_name=model_name,
            train_df=train_df,
            test_df=test_df,
        )

        results.append(result)

        print(
            f"Accuracy: "
            f"{result.accuracy:.4f}"
        )

        print(
            f"Macro F1: "
            f"{result.macro_f1:.4f}"
        )

        print(
            f"Weighted F1: "
            f"{result.weighted_f1:.4f}"
        )

        print("\nClassification report:")

        report_df = (
            pd.DataFrame(
                result.report
            )
            .transpose()
        )

        print(
            report_df.to_string()
        )

    # ------------------------------------------------------------
    # Comparison table
    # ------------------------------------------------------------

    print("\n" + "=" * 70)
    print("MODEL COMPARISON")
    print("=" * 70)

    comparison = pd.DataFrame(
        [
            {
                "model": result.name,
                "accuracy": result.accuracy,
                "macro_f1": result.macro_f1,
                "weighted_f1": result.weighted_f1,
            }
            for result in results
        ]
    )

    print(
        comparison.to_string(
            index=False,
            float_format=lambda x: f"{x:.4f}",
        )
    )

    print("\n" + "=" * 70)
    print("MODEL COMPARISON COMPLETE")
    print("=" * 70)


if __name__ == "__main__":
    main()