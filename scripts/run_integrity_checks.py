from pathlib import Path

from app.ml.data_loader import load_incidents
from app.ml.integrity_checks import (
    find_exact_text_overlap,
    generate_integrity_report,
)


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


def main():
    print("=" * 70)
    print("AegisOps Dataset Integrity Check")
    print("=" * 70)

    print("\nLoading canonical training dataset...")

    train_df = load_csv(TRAIN_PATH)

    print(
        f"Training records: {len(train_df)}"
    )

    print("\nLoading canonical test dataset...")

    test_df = load_csv(TEST_PATH)

    print(
        f"Test records: {len(test_df)}"
    )

    # ---------------------------------------------------------
    # TRAINING DATA
    # ---------------------------------------------------------

    print("\n" + "-" * 70)
    print("TRAINING DATA")
    print("-" * 70)

    train_report = generate_integrity_report(
        train_df
    )

    print(
        f"Rows: {train_report.row_count}"
    )

    print(
        f"Duplicate rows: "
        f"{train_report.duplicate_rows}"
    )

    print(
        f"Duplicate IDs: "
        f"{train_report.duplicate_ids}"
    )

    print(
        f"Empty descriptions: "
        f"{train_report.empty_descriptions}"
    )

    print(
        f"Empty categories: "
        f"{train_report.empty_categories}"
    )

    print(
        f"Possible emails: "
        f"{train_report.suspicious_email_count}"
    )

    print(
        f"Possible phone numbers: "
        f"{train_report.suspicious_phone_count}"
    )

    print(
        f"Possible IP addresses: "
        f"{train_report.suspicious_ip_count}"
    )

    print("\nCategory distribution:")

    for category, count in (
        train_report.category_distribution.items()
    ):
        print(
            f"  {category}: {count}"
        )

    # ---------------------------------------------------------
    # TEST DATA
    # ---------------------------------------------------------

    print("\n" + "-" * 70)
    print("TEST DATA")
    print("-" * 70)

    test_report = generate_integrity_report(
        test_df
    )

    print(
        f"Rows: {test_report.row_count}"
    )

    print(
        f"Duplicate rows: "
        f"{test_report.duplicate_rows}"
    )

    print(
        f"Duplicate IDs: "
        f"{test_report.duplicate_ids}"
    )

    print(
        f"Empty descriptions: "
        f"{test_report.empty_descriptions}"
    )

    print(
        f"Empty categories: "
        f"{test_report.empty_categories}"
    )

    print(
        f"Possible emails: "
        f"{test_report.suspicious_email_count}"
    )

    print(
        f"Possible phone numbers: "
        f"{test_report.suspicious_phone_count}"
    )

    print(
        f"Possible IP addresses: "
        f"{test_report.suspicious_ip_count}"
    )

    print("\nCategory distribution:")

    for category, count in (
        test_report.category_distribution.items()
    ):
        print(
            f"  {category}: {count}"
        )

    # ---------------------------------------------------------
    # TRAIN / TEST OVERLAP
    # ---------------------------------------------------------

    print("\n" + "-" * 70)
    print("TRAIN / TEST LEAKAGE CHECK")
    print("-" * 70)

    overlap = find_exact_text_overlap(
        train_df,
        test_df,
    )

    print(
        f"Exact text overlap: {len(overlap)}"
    )

    if overlap:
        print(
            "\nWARNING: Identical ticket descriptions "
            "appear in both train and test."
        )

        for text in list(overlap)[:10]:
            print(
                f"  {text[:200]}"
            )
    else:
        print(
            "No exact ticket-text overlap detected."
        )

    # ---------------------------------------------------------
    # FINAL STATUS
    # ---------------------------------------------------------

    print("\n" + "=" * 70)

    problems = []

    if train_report.duplicate_rows:
        problems.append(
            "duplicate training rows"
        )

    if test_report.duplicate_rows:
        problems.append(
            "duplicate test rows"
        )

    if train_report.duplicate_ids:
        problems.append(
            "duplicate training IDs"
        )

    if test_report.duplicate_ids:
        problems.append(
            "duplicate test IDs"
        )

    if train_report.empty_descriptions:
        problems.append(
            "empty training descriptions"
        )

    if test_report.empty_descriptions:
        problems.append(
            "empty test descriptions"
        )

    if train_report.empty_categories:
        problems.append(
            "empty training categories"
        )

    if test_report.empty_categories:
        problems.append(
            "empty test categories"
        )

    if overlap:
        problems.append(
            "train/test text overlap"
        )

    if problems:
        print("DATASET STATUS: REVIEW REQUIRED")

        print("\nProblems detected:")

        for problem in problems:
            print(
                f"  - {problem}"
            )
    else:
        print(
            "DATASET STATUS: BASIC INTEGRITY CHECK PASSED"
        )

    print("=" * 70)


def load_csv(path: Path):
    if not path.exists():
        raise FileNotFoundError(
            f"Dataset not found: {path}"
        )

    import pandas as pd

    return pd.read_csv(path)


if __name__ == "__main__":
    main()