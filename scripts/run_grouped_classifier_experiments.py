import json
from pathlib import Path

import joblib
import pandas as pd
import sklearn
from sklearn.dummy import DummyClassifier
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix,
)
from sklearn.pipeline import Pipeline
from sklearn.svm import LinearSVC
from sklearn.feature_extraction.text import TfidfVectorizer

from app.ml.model_experiments import (
    build_word_svm,
    build_word_char_svm,
)

PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = PROJECT_ROOT / "data" / "processed" / "external"
RESULTS_DIR = PROJECT_ROOT / "reports" / "classifier_experiments"

TRAIN_PATH = DATA_DIR / "aegisops_train_grouped.csv"
VAL_PATH = DATA_DIR / "aegisops_validation_grouped.csv"

TEXT_COL = "description"
TARGET_COL = "category"
RANDOM_SEED = 42


def main():
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)

    train = pd.read_csv(TRAIN_PATH)
    val = pd.read_csv(VAL_PATH)

    X_train = train[TEXT_COL].fillna("").astype(str).str.strip()
    y_train = train[TARGET_COL].astype(str).str.strip()
    X_val = val[TEXT_COL].fillna("").astype(str).str.strip()
    y_val = val[TARGET_COL].astype(str).str.strip()

    if X_train.eq("").any() or X_val.eq("").any():
        raise ValueError("Empty incident descriptions detected.")

    if y_train.eq("").any() or y_val.eq("").any():
        raise ValueError("Empty category labels detected.")

    train_text = set(X_train.str.lower())
    val_text = set(X_val.str.lower())
    if train_text & val_text:
        raise ValueError("Training and validation descriptions overlap.")

    labels = sorted(set(y_train) | set(y_val))

    experiments = [
        (
            "Majority-class Dummy baseline",
            DummyClassifier(strategy="most_frequent"),
        ),
        (
            "Word TF-IDF + Linear SVM",
            build_word_svm(),
        ),
        (
            "Word + Character TF-IDF + Linear SVM",
            build_word_char_svm(),
        ),
    ]

    summary_rows = []
    detailed_results = {}

    print("=" * 72)
    print("AEGISOPS GROUPED VALIDATION EXPERIMENTS")
    print("=" * 72)
    print("Training rows:", len(train))
    print("Validation rows:", len(val))
    print("Training categories:", y_train.nunique())
    print("Validation categories:", y_val.nunique())
    print("Shared normalized descriptions:", len(train_text & val_text))
    print("Final test file will NOT be used.")

    for name, model in experiments:
        print("\n" + "-" * 72)
        print("Model:", name)

        model.fit(X_train, y_train)
        predictions = model.predict(X_val)

        accuracy = accuracy_score(y_val, predictions)
        report = classification_report(
            y_val,
            predictions,
            labels=labels,
            output_dict=True,
            zero_division=0,
        )
        macro_f1 = report["macro avg"]["f1-score"]
        weighted_f1 = report["weighted avg"]["f1-score"]

        summary_rows.append({
            "model": name,
            "accuracy": accuracy,
            "macro_f1": macro_f1,
            "weighted_f1": weighted_f1,
        })

        detailed_results[name] = {
            "accuracy": float(accuracy),
            "macro_f1": float(macro_f1),
            "weighted_f1": float(weighted_f1),
            "classification_report": report,
            "confusion_matrix": confusion_matrix(
                y_val, predictions, labels=labels
            ).tolist(),
            "confusion_matrix_labels": labels,
        }

        print(f"Accuracy:    {accuracy:.4f}")
        print(f"Macro F1:    {macro_f1:.4f}")
        print(f"Weighted F1: {weighted_f1:.4f}")

    comparison = pd.DataFrame(summary_rows).sort_values(
        "macro_f1", ascending=False
    )

    summary_path = RESULTS_DIR / "validation_model_comparison.csv"
    details_path = RESULTS_DIR / "validation_detailed_metrics.json"

    comparison.to_csv(summary_path, index=False)

    with open(details_path, "w", encoding="utf-8") as file:
        json.dump({
            "random_seed": RANDOM_SEED,
            "training_file": TRAIN_PATH.name,
            "validation_file": VAL_PATH.name,
            "training_rows": len(train),
            "validation_rows": len(val),
            "sklearn_version": sklearn.__version__,
            "selection_metric": "macro_f1",
            "category_labels": labels,
            "results": detailed_results,
        }, file, indent=2)

    print("\n" + "=" * 72)
    print("MODEL COMPARISON — RANKED BY MACRO F1")
    print("=" * 72)
    print(comparison.to_string(
        index=False,
        float_format=lambda value: f"{value:.4f}",
    ))

    print("\nSaved summary:", summary_path)
    print("Saved detailed metrics:", details_path)
    print("\nExperiments complete. No final test data was used.")


if __name__ == "__main__":
    main()
