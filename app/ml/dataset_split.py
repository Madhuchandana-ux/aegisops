from pathlib import Path

import pandas as pd
from sklearn.model_selection import train_test_split


def split_dataset(
    df: pd.DataFrame,
    output_dir: Path,
    random_state: int = 42,
) -> tuple[
    pd.DataFrame,
    pd.DataFrame,
    pd.DataFrame,
]:
    """
    Split data into train, validation, and test sets.

    Proportions:
        70% train
        15% validation
        15% test
    """

    output_dir.mkdir(
        parents=True,
        exist_ok=True,
    )

    train_df, temporary_df = train_test_split(
        df,
        test_size=0.30,
        random_state=random_state,
    )

    validation_df, test_df = train_test_split(
        temporary_df,
        test_size=0.50,
        random_state=random_state,
    )

    train_df = train_df.reset_index(drop=True)
    validation_df = validation_df.reset_index(drop=True)
    test_df = test_df.reset_index(drop=True)

    train_df.to_csv(
        output_dir / "train.csv",
        index=False,
    )

    validation_df.to_csv(
        output_dir / "validation.csv",
        index=False,
    )

    test_df.to_csv(
        output_dir / "test.csv",
        index=False,
    )

    return (
        train_df,
        validation_df,
        test_df,
    )