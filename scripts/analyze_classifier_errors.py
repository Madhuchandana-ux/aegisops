from pathlib import Path

import pandas as pd

from app.ml.classifier import IncidentClassifier


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

MODEL_PATH = (
    PROJECT_ROOT
    / "models"
    / "incident_classifier.joblib"
)

OUTPUT_DIR = (
    PROJECT_ROOT
    / "data"
    / "processed"
    / "external"
)


def main():

    print("=" * 70)
    print("AegisOps Classification Error Analysis")
    print("=" * 70)

    # ------------------------------------------------------------
    # 1. Load test dataset
    # ------------------------------------------------------------

    if not TEST_PATH.exists():
        raise FileNotFoundError(
            f"Test dataset not found: {TEST_PATH}"
        )

    test_df = pd.read_csv(
        TEST_PATH
    )

    print(
        f"\nTest records: {len(test_df)}"
    )

    # ------------------------------------------------------------
    # 2. Load trained model
    # ------------------------------------------------------------

    if not MODEL_PATH.exists():
        raise FileNotFoundError(
            f"Model not found: {MODEL_PATH}"
        )

    classifier = IncidentClassifier()

    classifier.load(
        MODEL_PATH
    )

    print("Trained classifier loaded.")

    # ------------------------------------------------------------
    # 3. Generate predictions
    # ------------------------------------------------------------

    predictions = []

    confidences = []

    for description in test_df["description"]:

        result = classifier.predict(
            description
        )

        predictions.append(
            result.predicted_category
        )

        confidences.append(
            result.confidence
        )

    analysis_df = test_df.copy()

    analysis_df["predicted_category"] = predictions

    analysis_df["confidence"] = confidences

    analysis_df["correct"] = (
        analysis_df["category"]
        == analysis_df["predicted_category"]
    )

    # ------------------------------------------------------------
    # 4. Overall statistics
    # ------------------------------------------------------------

    total = len(analysis_df)

    correct = int(
        analysis_df["correct"].sum()
    )

    incorrect = total - correct

    print("\n" + "-" * 70)
    print("OVERALL RESULTS")
    print("-" * 70)

    print(f"Total predictions: {total}")
    print(f"Correct predictions: {correct}")
    print(f"Incorrect predictions: {incorrect}")

    print(
        f"Accuracy: "
        f"{correct / total:.4f}"
    )

    # ------------------------------------------------------------
    # 5. Errors by actual category
    # ------------------------------------------------------------

    print("\n" + "-" * 70)
    print("ERRORS BY ACTUAL CATEGORY")
    print("-" * 70)

    errors_by_actual = (
        analysis_df[
            ~analysis_df["correct"]
        ]
        .groupby("category")
        .size()
        .sort_values(
            ascending=False
        )
    )

    print(
        errors_by_actual.to_string()
    )

    # ------------------------------------------------------------
    # 6. Errors by predicted category
    # ------------------------------------------------------------

    print("\n" + "-" * 70)
    print("ERRORS BY PREDICTED CATEGORY")
    print("-" * 70)

    errors_by_prediction = (
        analysis_df[
            ~analysis_df["correct"]
        ]
        .groupby("predicted_category")
        .size()
        .sort_values(
            ascending=False
        )
    )

    print(
        errors_by_prediction.to_string()
    )

    # ------------------------------------------------------------
    # 7. Confusion pairs
    # ------------------------------------------------------------

    print("\n" + "-" * 70)
    print("TOP CONFUSION PAIRS")
    print("-" * 70)

    confusion_pairs = (
        analysis_df[
            ~analysis_df["correct"]
        ]
        .groupby(
            [
                "category",
                "predicted_category",
            ]
        )
        .size()
        .sort_values(
            ascending=False
        )
    )

    for (
        (actual, predicted),
        count,
    ) in confusion_pairs.head(15).items():

        print(
            f"{actual} -> {predicted}: "
            f"{count}"
        )

    # ------------------------------------------------------------
    # 8. Low-confidence errors
    # ------------------------------------------------------------

    print("\n" + "-" * 70)
    print("LOW-CONFIDENCE ERRORS")
    print("-" * 70)

    low_confidence_errors = (
        analysis_df[
            ~analysis_df["correct"]
        ]
        .sort_values(
            "confidence"
        )
    )

    for _, row in low_confidence_errors.head(15).iterrows():

        print("\nActual:")
        print(row["category"])

        print("Predicted:")
        print(row["predicted_category"])

        print(
            f"Confidence: "
            f"{row['confidence']:.4f}"
        )

        print("Description:")
        print(
            str(row["description"])[:500]
        )

    # ------------------------------------------------------------
    # 9. High-confidence errors
    # ------------------------------------------------------------

    print("\n" + "-" * 70)
    print("HIGH-CONFIDENCE ERRORS")
    print("-" * 70)

    high_confidence_errors = (
        analysis_df[
            ~analysis_df["correct"]
        ]
        .sort_values(
            "confidence",
            ascending=False,
        )
    )

    for _, row in high_confidence_errors.head(15).iterrows():

        print("\nActual:")
        print(row["category"])

        print("Predicted:")
        print(row["predicted_category"])

        print(
            f"Confidence: "
            f"{row['confidence']:.4f}"
        )

        print("Description:")
        print(
            str(row["description"])[:500]
        )

    # ------------------------------------------------------------
    # 10. Save complete error analysis
    # ------------------------------------------------------------

    OUTPUT_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )

    output_path = (
        OUTPUT_DIR
        / "classifier_predictions.csv"
    )

    analysis_df.to_csv(
        output_path,
        index=False,
    )

    print("\n" + "-" * 70)
    print("OUTPUT")
    print("-" * 70)

    print(
        f"Prediction analysis saved to:\n"
        f"{output_path}"
    )

    print("\n" + "=" * 70)
    print("ERROR ANALYSIS COMPLETE")
    print("=" * 70)


if __name__ == "__main__":
    main()