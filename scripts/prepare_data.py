from pathlib import Path

from app.ml.data_loader import load_incidents
from app.ml.data_quality import (
    generate_quality_report,
)
from app.ml.dataset_split import (
    split_dataset,
)
from app.ml.validation import (
    validate_incident_ids,
    validate_schema,
    validate_text_fields,
)


PROJECT_ROOT = Path(__file__).resolve().parents[1]

OUTPUT_DIR = (
    PROJECT_ROOT
    / "data"
    / "processed"
)


def main():
    print("=" * 60)
    print("AegisOps Data Preparation")
    print("=" * 60)

    df = load_incidents()

    print(
        f"\nLoaded {len(df)} incident records."
    )

    print("\n1. Validating schema...")

    validate_schema(df)

    print("Schema validation: PASSED")

    print("\n2. Validating text fields...")

    validate_text_fields(df)

    print("Text validation: PASSED")

    print("\n3. Validating incident IDs...")

    validate_incident_ids(df)

    print("Incident ID validation: PASSED")

    print("\n4. Generating quality report...")

    report = generate_quality_report(df)

    print(
        f"Rows: {report.row_count}"
    )

    print(
        f"Columns: {report.column_count}"
    )

    print(
        f"Duplicate rows: "
        f"{report.duplicate_rows}"
    )

    print("\nMissing values:")

    for column, count in (
        report.missing_values.items()
    ):
        print(
            f"  {column}: {count}"
        )

    print("\nCategory distribution:")

    for category, count in (
        report.category_distribution.items()
    ):
        print(
            f"  {category}: {count}"
        )

    print("\nPriority distribution:")

    for priority, count in (
        report.priority_distribution.items()
    ):
        print(
            f"  {priority}: {count}"
        )

    print("\n5. Splitting dataset...")

    train_df, validation_df, test_df = (
        split_dataset(
            df,
            OUTPUT_DIR,
        )
    )

    print(
        f"Train records: {len(train_df)}"
    )

    print(
        f"Validation records: "
        f"{len(validation_df)}"
    )

    print(
        f"Test records: {len(test_df)}"
    )

    print("\nData preparation complete.")


if __name__ == "__main__":
    main()