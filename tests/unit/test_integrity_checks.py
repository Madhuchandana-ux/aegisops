import pandas as pd

from app.ml.integrity_checks import (
    find_exact_text_overlap,
    generate_integrity_report,
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
                "unknown",
                "unknown",
            ],
            "impact": [
                None,
                None,
            ],
            "urgency": [
                None,
                None,
            ],
            "resolution": [
                "",
                "",
            ],
        }
    )


def test_integrity_report():
    df = create_test_dataframe()

    report = generate_integrity_report(df)

    assert report.row_count == 2
    assert report.duplicate_rows == 0
    assert report.duplicate_ids == 0
    assert report.empty_descriptions == 0
    assert report.empty_categories == 0


def test_exact_text_overlap():
    train_df = create_test_dataframe()

    test_df = pd.DataFrame(
        {
            "incident_id": ["TEST001"],
            "short_description": ["VPN failure"],
            "description": ["VPN is not working."],
            "category": ["network"],
            "subcategory": ["unknown"],
            "priority": ["unknown"],
            "impact": [None],
            "urgency": [None],
            "resolution": [""],
        }
    )

    overlap = find_exact_text_overlap(
        train_df,
        test_df,
    )

    assert "VPN is not working." in overlap


def test_no_exact_text_overlap():
    train_df = create_test_dataframe()

    test_df = pd.DataFrame(
        {
            "incident_id": ["TEST001"],
            "short_description": ["Email failure"],
            "description": ["Email is not working."],
            "category": ["software"],
            "subcategory": ["unknown"],
            "priority": ["unknown"],
            "impact": [None],
            "urgency": [None],
            "resolution": [""],
        }
    )

    overlap = find_exact_text_overlap(
        train_df,
        test_df,
    )

    assert len(overlap) == 0