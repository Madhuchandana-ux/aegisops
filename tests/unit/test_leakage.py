import pandas as pd

from app.ml.integrity_checks import (
    find_exact_text_overlap,
)


def test_detects_exact_overlap():

    train_df = pd.DataFrame(
        {
            "description": [
                "VPN is not working.",
                "Password reset required.",
            ]
        }
    )

    test_df = pd.DataFrame(
        {
            "description": [
                "VPN is not working.",
                "Printer is unavailable.",
            ]
        }
    )

    overlap = find_exact_text_overlap(
        train_df,
        test_df,
    )

    assert overlap == {
        "VPN is not working."
    }


def test_detects_no_overlap():

    train_df = pd.DataFrame(
        {
            "description": [
                "VPN is not working.",
            ]
        }
    )

    test_df = pd.DataFrame(
        {
            "description": [
                "Outlook crashes.",
            ]
        }
    )

    overlap = find_exact_text_overlap(
        train_df,
        test_df,
    )

    assert len(overlap) == 0