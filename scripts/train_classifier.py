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

MODEL_DIR = (
    PROJECT_ROOT
    / "models"
)

MODEL_PATH = (
    MODEL_DIR
    / "incident_classifier.joblib"
)


def main():

    print("=" * 70)
    print("AegisOps Incident Classification Training")
    print("=" * 70)

    # ------------------------------------------------------------
    # 1. Check datasets
    # ------------------------------------------------------------

    if not TRAIN_PATH.exists():
        raise FileNotFoundError(
            f"Training dataset not found: {TRAIN_PATH}"
        )

    if not TEST_PATH.exists():
        raise FileNotFoundError(
            f"Test dataset not found: {TEST_PATH}"
        )

    # ------------------------------------------------------------
    # 2. Load datasets
    # ------------------------------------------------------------

    print("\nLoading training dataset...")

    train_df = pd.read_csv(
        TRAIN_PATH
    )

    print(
        f"Training records: {len(train_df)}"
    )

    print("\nLoading test dataset...")

    test_df = pd.read_csv(
        TEST_PATH
    )

    print(
        f"Test records: {len(test_df)}"
    )

    # ------------------------------------------------------------
    # 3. Show categories
    # ------------------------------------------------------------

    print("\nTraining categories:")

    print(
        train_df["category"]
        .value_counts()
        .to_string()
    )

    # ------------------------------------------------------------
    # 4. Create classifier
    # ------------------------------------------------------------

    print("\nCreating TF-IDF + Logistic Regression model...")

    classifier = IncidentClassifier()

    # ------------------------------------------------------------
    # 5. Train
    # ------------------------------------------------------------

    print("\nTraining model...")

    classifier.train(
        train_df
    )

    print("Training completed.")

    # ------------------------------------------------------------
    # 6. Evaluate
    # ------------------------------------------------------------

    print("\nEvaluating model...")

    results = classifier.evaluate(
        test_df
    )

    print(
        f"\nAccuracy: "
        f"{results['accuracy']:.4f}"
    )

    print("\nClassification report:")

    report_df = pd.DataFrame(
        results["classification_report"]
    ).transpose()

    print(
        report_df.to_string()
    )

    print("\nConfusion matrix:")

    print(
        pd.DataFrame(
            results["confusion_matrix"],
            index=results["labels"],
            columns=results["labels"],
        )
    )

    # ------------------------------------------------------------
    # 7. Save model
    # ------------------------------------------------------------

    print("\nSaving trained model...")

    classifier.save(
        MODEL_PATH
    )

    print(
        f"Model saved to:\n{MODEL_PATH}"
    )

    # ------------------------------------------------------------
    # 8. Test individual predictions
    # ------------------------------------------------------------

    print("\nTesting sample incidents...")

    examples = [
        "User cannot access a shared network folder.",
        "The user's Microsoft Office application is not working.",
        "User cannot log into the corporate account.",
        "The computer has stopped working.",
    ]

    for description in examples:

        result = classifier.predict(
            description
        )

        print("\nIncident:")
        print(description)

        print(
            f"Predicted category: "
            f"{result.predicted_category}"
        )

        print(
            f"Confidence: "
            f"{result.confidence:.4f}"
        )

    print("\n" + "=" * 70)
    print("CLASSIFIER TRAINING COMPLETE")
    print("=" * 70)


if __name__ == "__main__":
    main()