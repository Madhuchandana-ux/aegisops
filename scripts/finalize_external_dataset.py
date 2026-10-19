from pathlib import Path

import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[1]

INPUT_TRAIN = (
    PROJECT_ROOT
    / "data"
    / "processed"
    / "external"
    / "aegisops_train.csv"
)

INPUT_TEST = (
    PROJECT_ROOT
    / "data"
    / "processed"
    / "external"
    / "aegisops_test_clean.csv"
)

OUTPUT_DIR = (
    PROJECT_ROOT
    / "data"
    / "processed"
    / "external"
)


REQUIRED_COLUMNS = {
    "source_id",
    "incident_id",
    "short_description",
    "description",
    "category",
    "subcategory",
    "priority",
    "impact",
    "urgency",
    "resolution",
    "data_source",
}


def normalize_text(series: pd.Series) -> pd.Series:
    """
    Normalize text only for validation.

    The original ticket text is not changed.
    """
    return (
        series
        .fillna("")
        .astype(str)
        .str.strip()
        .str.lower()
        .str.replace(r"\s+", " ", regex=True)
    )


def validate_dataset(
    df: pd.DataFrame,
    dataset_name: str,
) -> None:

    print(f"\nValidating {dataset_name} dataset...")

    missing_columns = REQUIRED_COLUMNS - set(df.columns)

    if missing_columns:
        raise ValueError(
            f"{dataset_name} is missing columns: "
            f"{sorted(missing_columns)}"
        )

    if df["incident_id"].duplicated().any():
        raise ValueError(
            f"{dataset_name} contains duplicate incident IDs."
        )

    if df["source_id"].duplicated().any():
        raise ValueError(
            f"{dataset_name} contains duplicate source IDs."
        )

    empty_descriptions = (
        df["description"]
        .fillna("")
        .astype(str)
        .str.strip()
        .eq("")
        .sum()
    )

    if empty_descriptions > 0:
        raise ValueError(
            f"{dataset_name} contains "
            f"{empty_descriptions} empty descriptions."
        )

    empty_categories = (
        df["category"]
        .fillna("")
        .astype(str)
        .str.strip()
        .eq("")
        .sum()
    )

    if empty_categories > 0:
        raise ValueError(
            f"{dataset_name} contains "
            f"{empty_categories} empty categories."
        )

    print("  Required columns: PASSED")
    print("  Unique incident IDs: PASSED")
    print("  Unique source IDs: PASSED")
    print("  Non-empty descriptions: PASSED")
    print("  Non-empty categories: PASSED")


def check_internal_duplicate_text(
    df: pd.DataFrame,
    dataset_name: str,
) -> int:

    normalized = normalize_text(df["description"])

    duplicate_count = int(
        normalized.duplicated(keep=False).sum()
    )

    print(
        f"  Duplicate normalized descriptions "
        f"in {dataset_name}: {duplicate_count}"
    )

    return duplicate_count


def check_train_test_overlap(
    train_df: pd.DataFrame,
    test_df: pd.DataFrame,
) -> int:

    train_text = set(
        normalize_text(train_df["description"])
    )

    test_text = set(
        normalize_text(test_df["description"])
    )

    train_text.discard("")
    test_text.discard("")

    overlap = train_text.intersection(test_text)

    return len(overlap)


def main():

    print("=" * 70)
    print("AegisOps Final External Dataset Validation")
    print("=" * 70)

    if not INPUT_TRAIN.exists():
        raise FileNotFoundError(
            f"Training dataset not found: {INPUT_TRAIN}"
        )

    if not INPUT_TEST.exists():
        raise FileNotFoundError(
            f"Clean test dataset not found: {INPUT_TEST}"
        )

    train_df = pd.read_csv(INPUT_TRAIN)
    test_df = pd.read_csv(INPUT_TEST)

    print(f"\nTraining records: {len(train_df)}")
    print(f"Test records: {len(test_df)}")
    print(f"Total records: {len(train_df) + len(test_df)}")

    # ------------------------------------------------------------
    # 1. Validate structure
    # ------------------------------------------------------------

    validate_dataset(
        train_df,
        "training",
    )

    validate_dataset(
        test_df,
        "test",
    )

    # ------------------------------------------------------------
    # 2. Check duplicate descriptions
    # ------------------------------------------------------------

    print("\nChecking duplicate ticket descriptions...")

    train_duplicate_text = check_internal_duplicate_text(
        train_df,
        "training",
    )

    test_duplicate_text = check_internal_duplicate_text(
        test_df,
        "test",
    )

    # ------------------------------------------------------------
    # 3. Check train/test leakage
    # ------------------------------------------------------------

    print("\nChecking train/test text leakage...")

    overlap_count = check_train_test_overlap(
        train_df,
        test_df,
    )

    print(
        f"  Remaining normalized train/test overlap: "
        f"{overlap_count}"
    )

    if overlap_count != 0:
        raise ValueError(
            "Train/test leakage still exists."
        )

    print("  Train/test leakage check: PASSED")

    # ------------------------------------------------------------
    # 4. Category distributions
    # ------------------------------------------------------------

    print("\nTraining category distribution:")

    print(
        train_df["category"]
        .value_counts()
        .to_string()
    )

    print("\nTest category distribution:")

    print(
        test_df["category"]
        .value_counts()
        .to_string()
    )

    # ------------------------------------------------------------
    # 5. Save final datasets
    # ------------------------------------------------------------

    OUTPUT_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )

    final_train_path = (
        OUTPUT_DIR / "aegisops_train_final.csv"
    )

    final_test_path = (
        OUTPUT_DIR / "aegisops_test_final.csv"
    )

    train_df.to_csv(
        final_train_path,
        index=False,
    )

    test_df.to_csv(
        final_test_path,
        index=False,
    )

    # ------------------------------------------------------------
    # 6. Final summary
    # ------------------------------------------------------------

    print("\n" + "=" * 70)
    print("FINAL DATASET STATUS")
    print("=" * 70)

    print("\nTraining:")
    print(f"  Records: {len(train_df)}")
    print(f"  Duplicate rows: {train_df.duplicated().sum()}")
    print(
        f"  Duplicate IDs: "
        f"{train_df['incident_id'].duplicated().sum()}"
    )

    print("\nTest:")
    print(f"  Records: {len(test_df)}")
    print(f"  Duplicate rows: {test_df.duplicated().sum()}")
    print(
        f"  Duplicate IDs: "
        f"{test_df['incident_id'].duplicated().sum()}"
    )

    print("\nFinal files:")

    print(final_train_path)
    print(final_test_path)

    print("\n" + "=" * 70)
    print("DATASET FINALIZATION PASSED")
    print("=" * 70)


if __name__ == "__main__":
    main()