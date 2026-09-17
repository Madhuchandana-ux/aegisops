from pathlib import Path

import pandas as pd


def _find_column(
    df: pd.DataFrame,
    candidates: list[str],
) -> str:
    """
    Find a column using case-insensitive matching.
    """

    normalized_columns = {
        str(column).strip().lower(): column
        for column in df.columns
    }

    for candidate in candidates:
        if candidate.lower() in normalized_columns:
            return normalized_columns[candidate.lower()]

    raise ValueError(
        f"Could not find any of these columns: {candidates}. "
        f"Available columns: {list(df.columns)}"
    )


def load_source_pair(
    feature_path: Path,
    label_path: Path,
) -> pd.DataFrame:
    """
    Load the source feature and label files.

    The Zenodo dataset contains an ID column in both files,
    so the feature and label data are joined using that ID.
    """

    X = pd.read_csv(feature_path)
    y = pd.read_csv(label_path)

    print(f"Feature columns: {list(X.columns)}")
    print(f"Label columns: {list(y.columns)}")

    # ---------------------------------------------------------
    # 1. Find the common ID column
    # ---------------------------------------------------------

    feature_id_column = _find_column(
        X,
        [
            "id",
            "ticket_id",
            "incident_id",
        ],
    )

    label_id_column = _find_column(
        y,
        [
            "id",
            "ticket_id",
            "incident_id",
        ],
    )

    # ---------------------------------------------------------
    # 2. Find the ticket-text column
    # ---------------------------------------------------------

    text_column = _find_column(
        X,
        [
            "text",
            "description",
            "ticket",
            "incident",
            "content",
        ],
    )

    # ---------------------------------------------------------
    # 3. Find the classification label
    # ---------------------------------------------------------

    label_column = _find_column(
        y,
        [
            "category_truth",
            "label",
            "category",
            "class",
            "target",
        ],
    )

    # ---------------------------------------------------------
    # 4. Rename IDs temporarily for a clean merge
    # ---------------------------------------------------------

    X_temp = X[
        [
            feature_id_column,
            text_column,
        ]
    ].copy()

    y_temp = y[
        [
            label_id_column,
            label_column,
        ]
    ].copy()

    X_temp = X_temp.rename(
        columns={
            feature_id_column: "source_id",
            text_column: "source_text",
        }
    )

    y_temp = y_temp.rename(
        columns={
            label_id_column: "source_id",
            label_column: "source_label",
        }
    )

    # ---------------------------------------------------------
    # 5. Check duplicate IDs before merging
    # ---------------------------------------------------------

    if X_temp["source_id"].duplicated().any():
        raise ValueError(
            "Duplicate IDs found in the feature dataset."
        )

    if y_temp["source_id"].duplicated().any():
        raise ValueError(
            "Duplicate IDs found in the label dataset."
        )

    # ---------------------------------------------------------
    # 6. Merge using the source ID
    # ---------------------------------------------------------

    result = X_temp.merge(
        y_temp,
        on="source_id",
        how="inner",
        validate="one_to_one",
    )

    # ---------------------------------------------------------
    # 7. Verify that no records were lost
    # ---------------------------------------------------------

    if len(result) != len(X_temp):
        raise ValueError(
            "Feature/label merge lost records. "
            f"Features: {len(X_temp)}, "
            f"Merged: {len(result)}"
        )

    if len(result) != len(y_temp):
        raise ValueError(
            "Feature/label merge lost records. "
            f"Labels: {len(y_temp)}, "
            f"Merged: {len(result)}"
        )

    # ---------------------------------------------------------
    # 8. Clean text and labels
    # ---------------------------------------------------------

    result["source_text"] = (
        result["source_text"]
        .fillna("")
        .astype(str)
        .str.strip()
    )

    result["source_label"] = (
        result["source_label"]
        .fillna("")
        .astype(str)
        .str.strip()
    )

    if result["source_text"].eq("").any():
        raise ValueError(
            "Empty ticket text found after loading the dataset."
        )

    if result["source_label"].eq("").any():
        raise ValueError(
            "Empty classification label found after loading the dataset."
        )

    return result


def create_canonical_dataset(
    df: pd.DataFrame,
    source_prefix: str,
) -> pd.DataFrame:
    """
    Convert external IT support tickets into the
    AegisOps canonical incident representation.

    Fields unavailable in the source are explicitly marked
    as unknown rather than artificially generated.
    """

    canonical = pd.DataFrame()

    # Preserve the original source ID for traceability.
    canonical["source_id"] = df["source_id"]

    canonical["incident_id"] = [
        f"{source_prefix}_{index:05d}"
        for index in range(1, len(df) + 1)
    ]

    canonical["short_description"] = (
        df["source_text"]
        .fillna("")
        .astype(str)
        .str.strip()
        .str.slice(0, 200)
    )

    canonical["description"] = (
        df["source_text"]
        .fillna("")
        .astype(str)
        .str.strip()
    )

    # category_truth is the actual human-assigned
    # classification label from the source dataset.
    canonical["category"] = (
        df["source_label"]
        .fillna("")
        .astype(str)
        .str.strip()
    )

    # These fields are not available in this source.
    canonical["subcategory"] = "unknown"
    canonical["priority"] = "unknown"
    canonical["impact"] = pd.NA
    canonical["urgency"] = pd.NA
    canonical["resolution"] = ""

    canonical["data_source"] = (
        "zenodo_it_support_tickets"
    )

    return canonical