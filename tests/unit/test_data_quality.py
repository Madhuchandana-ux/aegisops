import pandas as pd
import pytest

from app.ml.data_quality import (
    generate_quality_report,
)
from app.ml.validation import (
    validate_incident_ids,
    validate_schema,
    validate_text_fields,
)


def create_test_dataframe():
    return pd.DataFrame(
        {
            "incident_id": [
                "INC001",
                "INC002",
            ],
            "short_description": [
                "VPN failure",
                "Password reset",
            ],
            "description": [
                "VPN is not working.",
                "Password needs reset.",
            ],
            "category": [
                "network",
                "access",
            ],
            "subcategory": [
                "vpn",
                "authentication",
            ],
            "priority": [
                "P2",
                "P3",
            ],
            "impact": [
                2,
                3,
            ],
            "urgency": [
                2,
                2,
            ],
            "resolution": [
                "Reset VPN.",
                "Reset password.",
            ],
        }
    )


def test_quality_report():
    df = create_test_dataframe()

    report = generate_quality_report(df)

    assert report.row_count == 2
    assert report.column_count == 9
    assert report.duplicate_rows == 0


def test_schema_validation():
    df = create_test_dataframe()

    validate_schema(df)


def test_text_validation():
    df = create_test_dataframe()

    validate_text_fields(df)


def test_duplicate_id_validation():
    df = create_test_dataframe()

    df.loc[1, "incident_id"] = "INC001"

    with pytest.raises(ValueError):
        validate_incident_ids(df)


def test_missing_column_validation():
    df = create_test_dataframe()

    df = df.drop(
        columns=["priority"]
    )

    with pytest.raises(ValueError):
        validate_schema(df)