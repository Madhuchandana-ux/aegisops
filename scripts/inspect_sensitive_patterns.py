from pathlib import Path
import re
import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parents[1]

DATASETS = [
    ("training", PROJECT_ROOT / "data/processed/external/aegisops_train.csv"),
    ("test", PROJECT_ROOT / "data/processed/external/aegisops_test_clean.csv"),
]

TEXT_COLUMNS = ["short_description", "description", "resolution"]

PATTERNS = {
    "possible phone numbers": re.compile(
        r"(?<!\d)(?:\+?\d[\d\s().-]{7,}\d)(?!\d)"
    ),
    "possible email addresses": re.compile(
        r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b"
    ),
    "possible IPv4 addresses": re.compile(
        r"\b(?:\d{1,3}\.){3}\d{1,3}\b"
    ),
}


def main():
    print("=" * 70)
    print("AegisOps Privacy Pattern Scan")
    print("Matching text is never printed.")
    print("=" * 70)

    for dataset_name, path in DATASETS:
        if not path.exists():
            print(f"\n{dataset_name}: file not found; skipped.")
            continue

        df = pd.read_csv(path)
        columns = [c for c in TEXT_COLUMNS if c in df.columns]

        print(f"\n{dataset_name}: {len(df)} records")

        if not columns:
            print("No expected text columns found.")
            continue

        for column in columns:
            descriptions = df[column].fillna("").astype(str)
            print(f"\n  Column: {column}")

            for pattern_name, pattern in PATTERNS.items():
                matching_rows = [
                    row_number
                    for row_number, value in enumerate(descriptions, start=2)
                    if pattern.search(value)
                ]

                print(f"    {pattern_name}: {len(matching_rows)} records")

                if matching_rows:
                    print(
                        f"    CSV row numbers (first 20): "
                        f"{matching_rows[:20]}"
                    )


if __name__ == "__main__":
    main()
