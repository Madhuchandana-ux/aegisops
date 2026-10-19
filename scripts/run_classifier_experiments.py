from pathlib import Path

import pandas as pd

from app.ml.model_experiments import (
    build_word_char_svm,
    build_word_svm,
    build_word_svm_c05,
    build_word_svm_c1,
    build_word_svm_c2,
    evaluate_model,
)


PROJECT_ROOT = Path(__file__).resolve().parents[1]

TRAIN_PATH = (
    PROJECT_ROOT
    / "data"
    / "processed"
    / "external"
    / "aegisops_train_split.csv"
)

VALIDATION_PATH = (
    PROJECT_ROOT
    / "data"
    / "processed"
    / "external"
    / "aegisops_validation.csv"
)


def main():
    print("=" * 70)
    print("AegisOps Classifier Experiments")
    print("=" * 70)

    train_df = pd.read_csv(TRAIN_PATH)
    validation_df = pd.read_csv(VALIDATION_PATH)

    print(f"\nTraining records: {len(train_df)}")
    print(f"Validation records: {len(validation_df)}")

    experiments = [
        (
            "Word TF-IDF + Linear SVM",
            build_word_svm(),
        ),
        (
            "Word + Character TF-IDF + Linear SVM",
            build_word_char_svm(),
        ),
        (
            "Linear SVM C=0.5",
            build_word_svm_c05(),
        ),
        (
            "Linear SVM C=1.0",
            build_word_svm_c1(),
        ),
        (
            "Linear SVM C=2.0",
            build_word_svm_c2(),
        ),
    ]

    results = []

    for name, model in experiments:
        print("\n" + "-" * 70)
        print(f"Experiment: {name}")
        print("-" * 70)

        result = evaluate_model(
            model=model,
            model_name=name,
            train_df=train_df,
            validation_df=validation_df,
        )

        results.append(result)

        print(f"Accuracy:    {result.accuracy:.4f}")
        print(f"Macro F1:    {result.macro_f1:.4f}")
        print(f"Weighted F1: {result.weighted_f1:.4f}")

    comparison = pd.DataFrame(
        [
            {
                "experiment": result.name,
                "accuracy": result.accuracy,
                "macro_f1": result.macro_f1,
                "weighted_f1": result.weighted_f1,
            }
            for result in results
        ]
    )

    print("\n" + "=" * 70)
    print("EXPERIMENT COMPARISON")
    print("=" * 70)

    print(
        comparison.to_string(
            index=False,
            float_format=lambda x: f"{x:.4f}",
        )
    )

    print("\n" + "=" * 70)
    print("EXPERIMENTS COMPLETE")
    print("=" * 70)


if __name__ == "__main__":
    main()