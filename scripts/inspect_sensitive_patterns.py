from pathlib import Path
import re

import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[1]

DATASETS = [
    (
        "training",
        PROJECT_ROOT
        / "data"
        / "processed"
        / "external"
        / "aegisops_train.csv",
    ),
    (
        "test",
        PROJECT_ROOT
        / "data"
        / "processed"
        / "external"
        / "aegisops_test_clean.csv",
    ),
]


PHONE_PATTERN = re.compile(
    r"(?<!\d)(?:\+?\d[\d\s().-]{7,}\d)(?!\d)"
)

EMAIL_PATTERN = re.compile(
    r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b"
)

IP_PATTERN = re.compile(
    r"\b(?:\d{1,3}\.){3}\d{1,3}\b"
)


def inspect_pattern(
    name: str,
    df: pd.DataFrame,
    pattern: re.Pattern,
):
    matches = []

    for text in (
        df["description"]
        .fillna("")
        .astype(str)
    ):
        if pattern.search(text):
            matches.append(text)

    print(
        f"\n{name}: {len(matches)} matching records"
    )

    for text in matches[:10]:
        print("-" * 60)
        print(text[:500])


def main():
    print("=" * 70)
    print("AegisOps Sensitive Pattern Inspection")
    print("=" * 70)

    for name, path in DATASETS:

        if not path.exists():
            print(
                f"\nSkipping {name}: "
                f"{path} does not exist."
            )
            continue

        df = pd.read_csv(path)

        print(
            f"\nDataset: {name}"
        )

        inspect_pattern(
            "Possible phone numbers",
            df,
            PHONE_PATTERN,
        )

        inspect_pattern(
            "Possible email addresses",
            df,
            EMAIL_PATTERN,
        )

        inspect_pattern(
            "Possible IP addresses",
            df,
            IP_PATTERN,
        )


if __name__ == "__main__":
    main()