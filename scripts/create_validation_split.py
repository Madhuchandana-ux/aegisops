from pathlib import Path

import pandas as pd
from sklearn.model_selection import train_test_split


PROJECT_ROOT = Path(__file__).resolve().parents[1]

TRAIN_PATH = (
    PROJECT_ROOT
    / "data"
    / "processed"
    / "external"
    / "aegisops_train_final.csv"
)

OUTPUT_DIR = (
    PROJECT_ROOT
    / "data"
    / "processed"
    / "external"
)


def main():
    print("=" * 70)
    print("AegisOps Validation Split Creation")
    print("=" * 70)

    df = pd.read_csv(TRAIN_PATH)

    print(f"\nOriginal training records: {len(df)}")

    train_df, validation_df = train_test_split(
        df,
        test_size=0.20,
        random_state=42,
        stratify=df["category"],
    )

    train_output = OUTPUT_DIR / "aegisops_train_split.csv"
    validation_output = OUTPUT_DIR / "aegisops_validation.csv"

    train_df.to_csv(train_output, index=False)
    validation_df.to_csv(validation_output, index=False)

    print(f"\nNew training records: {len(train_df)}")
    print(f"Validation records: {len(validation_df)}")

    print("\nTraining class distribution:")
    print(train_df["category"].value_counts().sort_index())

    print("\nValidation class distribution:")
    print(validation_df["category"].value_counts().sort_index())

    print("\nSaved:")
    print(train_output)
    print(validation_output)

    print("\n" + "=" * 70)
    print("VALIDATION SPLIT COMPLETE")
    print("=" * 70)


if __name__ == "__main__":
    main()