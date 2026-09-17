from pathlib import Path
import sys

import pandas as pd


def inspect_dataset(file_path: str) -> None:
    path = Path(file_path)

    if not path.exists():
        print(f"ERROR: Dataset not found: {path}")
        sys.exit(1)

    print("=" * 70)
    print("AegisOps Dataset Inspector")
    print("=" * 70)

    print(f"\nFile: {path}")
    print(f"Size: {path.stat().st_size / 1024:.2f} KB")

    if path.suffix.lower() == ".csv":
        df = pd.read_csv(path)
    elif path.suffix.lower() in {".xlsx", ".xls"}:
        df = pd.read_excel(path)
    elif path.suffix.lower() == ".json":
        df = pd.read_json(path)
    else:
        print(f"Unsupported file type: {path.suffix}")
        sys.exit(1)

    print("\n--- Dataset Shape ---")
    print(f"Rows: {len(df)}")
    print(f"Columns: {len(df.columns)}")

    print("\n--- Columns ---")
    for column in df.columns:
        print(f"  - {column}")

    print("\n--- Data Types ---")
    print(df.dtypes.to_string())

    print("\n--- Missing Values ---")
    missing = df.isna().sum()

    for column, count in missing.items():
        print(f"  {column}: {count}")

    print("\n--- Duplicate Rows ---")
    print(df.duplicated().sum())

    print("\n--- First 5 Records ---")
    print(df.head().to_string())

    print("\n--- Basic Statistics ---")
    print(df.describe(include="all").transpose().to_string())

    print("\nInspection complete.")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print(
            "Usage:\n"
            "python scripts\\inspect_dataset.py <path-to-dataset>"
        )
        sys.exit(1)

    inspect_dataset(sys.argv[1])