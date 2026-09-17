import pandas as pd


REQUIRED_COLUMNS = {
    "incident_id",
    "short_description",
    "description",
    "category",
    "subcategory",
    "priority",
    "impact",
    "urgency",
    "resolution",
}


def validate_schema(
    df: pd.DataFrame,
) -> None:
    """
    Verify that the incident dataset contains
    all required columns.
    """

    missing_columns = (
        REQUIRED_COLUMNS
        - set(df.columns)
    )

    if missing_columns:
        raise ValueError(
            "Missing required columns: "
            + ", ".join(
                sorted(missing_columns)
            )
        )


def validate_text_fields(
    df: pd.DataFrame,
) -> None:
    """
    Verify that important text fields contain
    usable values.
    """

    text_columns = [
        "short_description",
        "description",
        "category",
        "subcategory",
        "priority",
    ]

    for column in text_columns:
        if column not in df.columns:
            continue

        empty_count = (
            df[column]
            .fillna("")
            .astype(str)
            .str.strip()
            .eq("")
            .sum()
        )

        if empty_count > 0:
            raise ValueError(
                f"Column '{column}' contains "
                f"{empty_count} empty values."
            )


def validate_incident_ids(
    df: pd.DataFrame,
) -> None:
    """
    Ensure incident IDs are unique.
    """

    duplicate_ids = (
        df["incident_id"]
        .duplicated()
        .sum()
    )

    if duplicate_ids > 0:
        raise ValueError(
            f"Found {duplicate_ids} "
            "duplicate incident IDs."
        )