import re
from dataclasses import dataclass

import pandas as pd


@dataclass
class IntegrityReport:
    row_count: int
    duplicate_rows: int
    duplicate_ids: int
    empty_descriptions: int
    empty_categories: int
    train_test_exact_text_overlap: int
    suspicious_email_count: int
    suspicious_phone_count: int
    suspicious_ip_count: int
    category_distribution: dict[str, int]


EMAIL_PATTERN = re.compile(
    r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b"
)

PHONE_PATTERN = re.compile(
    r"(?<!\d)(?:\+?\d[\d\s().-]{7,}\d)(?!\d)"
)

IP_PATTERN = re.compile(
    r"\b(?:\d{1,3}\.){3}\d{1,3}\b"
)


def _count_pattern_matches(
    series: pd.Series,
    pattern: re.Pattern,
) -> int:
    """
    Count rows containing at least one match.
    """

    return int(
        series
        .fillna("")
        .astype(str)
        .str.contains(
            pattern,
            regex=True,
            na=False,
        )
        .sum()
    )


def generate_integrity_report(
    df: pd.DataFrame,
) -> IntegrityReport:
    """
    Generate integrity and privacy indicators
    for an AegisOps canonical dataset.
    """

    descriptions = (
        df["description"]
        .fillna("")
        .astype(str)
        .str.strip()
    )

    categories = (
        df["category"]
        .fillna("")
        .astype(str)
        .str.strip()
    )

    duplicate_rows = int(
        df.duplicated().sum()
    )

    duplicate_ids = int(
        df["incident_id"].duplicated().sum()
    )

    empty_descriptions = int(
        descriptions.eq("").sum()
    )

    empty_categories = int(
        categories.eq("").sum()
    )

    suspicious_email_count = _count_pattern_matches(
        descriptions,
        EMAIL_PATTERN,
    )

    suspicious_phone_count = _count_pattern_matches(
        descriptions,
        PHONE_PATTERN,
    )

    suspicious_ip_count = _count_pattern_matches(
        descriptions,
        IP_PATTERN,
    )

    category_distribution = (
        categories
        .value_counts()
        .to_dict()
    )

    return IntegrityReport(
        row_count=len(df),
        duplicate_rows=duplicate_rows,
        duplicate_ids=duplicate_ids,
        empty_descriptions=empty_descriptions,
        empty_categories=empty_categories,
        train_test_exact_text_overlap=0,
        suspicious_email_count=suspicious_email_count,
        suspicious_phone_count=suspicious_phone_count,
        suspicious_ip_count=suspicious_ip_count,
        category_distribution={
            str(key): int(value)
            for key, value in category_distribution.items()
        },
    )


def find_exact_text_overlap(
    train_df: pd.DataFrame,
    test_df: pd.DataFrame,
) -> set[str]:
    """
    Find identical descriptions appearing in both
    training and test datasets.
    """

    train_text = set(
        train_df["description"]
        .fillna("")
        .astype(str)
        .str.strip()
    )

    test_text = set(
        test_df["description"]
        .fillna("")
        .astype(str)
        .str.strip()
    )

    train_text.discard("")
    test_text.discard("")

    return train_text.intersection(test_text)