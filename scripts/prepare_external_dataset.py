from pathlib import Path

from app.ml.canonical_mapping import (
    create_canonical_dataset,
    load_source_pair,
)


PROJECT_ROOT = Path(__file__).resolve().parents[1]

RAW_DIR = PROJECT_ROOT / "data" / "raw" / "external"
OUTPUT_DIR = PROJECT_ROOT / "data" / "processed" / "external"


def main():
    print("=" * 70)
    print("AegisOps External Dataset Preparation")
    print("=" * 70)

    train_x_path = RAW_DIR / "X_train.csv"
    train_y_path = RAW_DIR / "y_train.csv"

    test_x_path = RAW_DIR / "X_test.csv"
    test_y_path = RAW_DIR / "y_test.csv"

    print("\nLoading training data...")

    train_source = load_source_pair(
        train_x_path,
        train_y_path,
    )

    print(f"Training records: {len(train_source)}")

    print("\nLoading test data...")

    test_source = load_source_pair(
        test_x_path,
        test_y_path,
    )

    print(f"Test records: {len(test_source)}")

    print("\nCreating canonical training dataset...")

    train_canonical = create_canonical_dataset(
        train_source,
        source_prefix="ZENODO_TRAIN",
    )

    print("\nCreating canonical test dataset...")

    test_canonical = create_canonical_dataset(
        test_source,
        source_prefix="ZENODO_TEST",
    )

    OUTPUT_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )

    train_output = OUTPUT_DIR / "aegisops_train.csv"
    test_output = OUTPUT_DIR / "aegisops_test.csv"

    train_canonical.to_csv(
        train_output,
        index=False,
    )

    test_canonical.to_csv(
        test_output,
        index=False,
    )

    print("\n" + "=" * 70)
    print("Preparation complete")
    print("=" * 70)

    print(f"\nTraining output:")
    print(train_output)

    print(f"\nTest output:")
    print(test_output)

    print("\nTraining categories:")

    print(
        train_canonical["category"]
        .value_counts()
        .to_string()
    )

    print("\nTest categories:")

    print(
        test_canonical["category"]
        .value_counts()
        .to_string()
    )


if __name__ == "__main__":
    main()