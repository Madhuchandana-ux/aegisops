from dataclasses import dataclass

import pandas as pd


@dataclass
class DataQualityReport:
    """
    Stores the main quality checks for an incident dataset.
    """

    row_count: int
    column_count: int

    duplicate_rows: int

    missing_values: dict[str, int]

    empty_strings: dict[str, int]

    category_distribution: dict[str, int]

    priority_distribution: dict[str, int]


def generate_quality_report(
    df: pd.DataFrame,
) -> DataQualityReport:
    """
    Generate a basic data-quality report.
    """

    duplicate_rows = int(
        df.duplicated().sum()
    )

    missing_values = {
        column: int(df[column].isna().sum())
        for column in df.columns
    }

    empty_strings = {}

    for column in df.select_dtypes(
        include=["object"]
    ).columns:
        empty_strings[column] = int(
            df[column]
            .fillna("")
            .astype(str)
            .str.strip()
            .eq("")
            .sum()
        )

    category_distribution = {}

    if "category" in df.columns:
        category_distribution = (
            df["category"]
            .value_counts(dropna=False)
            .to_dict()
        )

    priority_distribution = {}

    if "priority" in df.columns:
        priority_distribution = (
            df["priority"]
            .value_counts(dropna=False)
            .to_dict()
        )

    return DataQualityReport(
        row_count=len(df),
        column_count=len(df.columns),
        duplicate_rows=duplicate_rows,
        missing_values=missing_values,
        empty_strings=empty_strings,
        category_distribution={
            str(key): int(value)
            for key, value
            in category_distribution.items()
        },
        priority_distribution={
            str(key): int(value)
            for key, value
            in priority_distribution.items()
        },
    )