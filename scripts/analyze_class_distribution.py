from pathlib import Path

import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[1]

TRAIN_PATH = (
    PROJECT_ROOT
    / "data"
    / "processed"
    / "external"
    / "aegisops_train_final.csv"
)

TEST_PATH = (
    PROJECT_ROOT
    / "data"
    / "processed"
    / "external"
    / "aegisops_test_final.csv"
)


def main():

    print("=" * 70)
    print("AegisOps Class Distribution Analysis")
    print("=" * 70)

    train_df = pd.read_csv(
        TRAIN_PATH
    )

    test_df = pd.read_csv(
        TEST_PATH
    )

    train_counts = (
        train_df["category"]
        .value_counts()
    )

    test_counts = (
        test_df["category"]
        .value_counts()
    )

    all_categories = sorted(
        set(train_counts.index)
        | set(test_counts.index)
    )

    distribution = pd.DataFrame(
        {
            "training": [
                train_counts.get(
                    category,
                    0,
                )
                for category in all_categories
            ],
            "test": [
                test_counts.get(
                    category,
                    0,
                )
                for category in all_categories
            ],
        },
        index=all_categories,
    )

    distribution["training_percentage"] = (
        distribution["training"]
        / len(train_df)
        * 100
    )

    distribution["test_percentage"] = (
        distribution["test"]
        / len(test_df)
        * 100
    )

    print("\nClass distribution:")
    print(
        distribution.to_string(
            float_format=lambda x: f"{x:.2f}"
        )
    )

    print("\n" + "-" * 70)
    print("CLASSES MISSING FROM TEST SET")
    print("-" * 70)

    missing_test_classes = [
        category
        for category in all_categories
        if test_counts.get(category, 0) == 0
    ]

    if missing_test_classes:

        for category in missing_test_classes:
            print(
                f"  {category}"
            )

    else:

        print(
            "No training classes are missing "
            "from the test set."
        )

    print("\n" + "-" * 70)
    print("CLASSES MISSING FROM TRAINING SET")
    print("-" * 70)

    missing_train_classes = [
        category
        for category in all_categories
        if train_counts.get(category, 0) == 0
    ]

    if missing_train_classes:

        for category in missing_train_classes:
            print(
                f"  {category}"
            )

    else:

        print(
            "No test classes are missing "
            "from the training set."
        )

    print("\n" + "=" * 70)
    print("CLASS DISTRIBUTION ANALYSIS COMPLETE")
    print("=" * 70)


if __name__ == "__main__":
    main()