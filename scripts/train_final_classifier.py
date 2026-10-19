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

MODEL_DIR = PROJECT_ROOT / "models"

MODEL_PATH = MODEL_DIR / "incident_classifier_final.joblib"


def main():
    print("=" * 70)
    print("AegisOps Final Incident Classifier Training")
    print("=" * 70)

    train_df = pd.read_csv(TRAIN_PATH)
    test_df = pd.read_csv(TEST_PATH)

    print(f"\nTraining records: {len(train_df)}")
    print(f"Final test records: {len(test_df)}")

    print("\nTraining final model...")

    classifier = IncidentClassifier()

    classifier.train(train_df)

    print("Training complete.")

    print("\nEvaluating on final test set...")

    metrics = classifier.evaluate(test_df)

    print("\n" + "-" * 70)
    print("FINAL TEST RESULTS")
    print("-" * 70)

    print(
        f"Accuracy:    {metrics['accuracy']:.4f}"
    )

    print(
        f"Macro F1:    {metrics['macro_f1']:.4f}"
    )

    print(
        f"Weighted F1: {metrics['weighted_f1']:.4f}"
    )

    print("\nClassification report:")

    report_df = pd.DataFrame(
        metrics["classification_report"]
    ).transpose()

    print(
        report_df.to_string()
    )

    MODEL_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )

    classifier.save(
        MODEL_PATH
    )

    print("\nModel saved to:")
    print(MODEL_PATH)

    print("\n" + "=" * 70)
    print("FINAL CLASSIFIER TRAINING COMPLETE")
    print("=" * 70)


if __name__ == "__main__":
    main()
