from pathlib import Path

import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[1]

TRAIN_PATH = (
    PROJECT_ROOT
    / "data"
    / "processed"
    / "external"
    / "aegisops_train.csv"
)

TEST_PATH = (
    PROJECT_ROOT
    / "data"
    / "processed"
    / "external"
    / "aegisops_test.csv"
)

OUTPUT_DIR = (
    PROJECT_ROOT
    / "data"
    / "processed"
    / "external"
)


def normalize_text(series: pd.Series) -> pd.Series:
    """
    Normalize text only for duplicate comparison.

    The actual description stored in the dataset is not modified.
    """

    return (
        series
        .fillna("")
        .astype(str)
        .str.strip()
        .str.lower()
        .str.replace(r"\s+", " ", regex=True)
    )


def main():
    print("=" * 70)
    print("AegisOps Train/Test Leakage Cleaning")
    print("=" * 70)

    train_df = pd.read_csv(TRAIN_PATH)
    test_df = pd.read_csv(TEST_PATH)

    print(f"\nOriginal training records: {len(train_df)}")
    print(f"Original test records: {len(test_df)}")

    train_text = normalize_text(
        train_df["description"]
    )

    test_text = normalize_text(
        test_df["description"]
    )

    train_text_set = set(train_text)

    overlap_mask = test_text.isin(
        train_text_set
    )

    overlap_count = int(
        overlap_mask.sum()
    )

    print(
        f"\nExact normalized text overlap: "
        f"{overlap_count}"
    )

    if overlap_count > 0:
        print(
            "\nRemoving overlapping records "
            "from TEST only..."
        )

    cleaned_test_df = test_df.loc[
        ~overlap_mask
    ].copy()

    cleaned_test_df = (
        cleaned_test_df
        .reset_index(drop=True)
    )

    output_path = (
        OUTPUT_DIR
        / "aegisops_test_clean.csv"
    )

    cleaned_test_df.to_csv(
        output_path,
        index=False,
    )

    print(
        f"\nCleaned test records: "
        f"{len(cleaned_test_df)}"
    )

    print(
        f"Records removed: "
        f"{len(test_df) - len(cleaned_test_df)}"
    )

    print(
        f"\nOutput:"
        f"\n{output_path}"
    )

    print("\nLeakage cleaning complete.")


if __name__ == "__main__":
    main()