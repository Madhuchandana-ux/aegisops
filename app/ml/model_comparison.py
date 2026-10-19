from dataclasses import dataclass

import pandas as pd

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.svm import LinearSVC
from sklearn.metrics import (
    accuracy_score,
    classification_report,
)


@dataclass
class ModelResult:
    name: str
    accuracy: float
    macro_f1: float
    weighted_f1: float
    report: dict


def build_logistic_regression():

    return Pipeline(
        [
            (
                "tfidf",
                TfidfVectorizer(
                    lowercase=True,
                    strip_accents="unicode",
                    ngram_range=(1, 2),
                    min_df=2,
                    sublinear_tf=True,
                ),
            ),
            (
                "classifier",
                LogisticRegression(
                    max_iter=2000,
                    class_weight="balanced",
                    random_state=42,
                ),
            ),
        ]
    )


def build_linear_svm():

    return Pipeline(
        [
            (
                "tfidf",
                TfidfVectorizer(
                    lowercase=True,
                    strip_accents="unicode",
                    ngram_range=(1, 2),
                    min_df=2,
                    sublinear_tf=True,
                ),
            ),
            (
                "classifier",
                LinearSVC(
                    class_weight="balanced",
                    random_state=42,
                ),
            ),
        ]
    )


def evaluate_model(
    model,
    model_name: str,
    train_df: pd.DataFrame,
    test_df: pd.DataFrame,
) -> ModelResult:

    X_train = (
        train_df["description"]
        .fillna("")
        .astype(str)
        .str.strip()
    )

    y_train = (
        train_df["category"]
        .fillna("")
        .astype(str)
        .str.strip()
    )

    X_test = (
        test_df["description"]
        .fillna("")
        .astype(str)
        .str.strip()
    )

    y_test = (
        test_df["category"]
        .fillna("")
        .astype(str)
        .str.strip()
    )

    model.fit(
        X_train,
        y_train,
    )

    predictions = model.predict(
        X_test
    )

    report = classification_report(
        y_test,
        predictions,
        output_dict=True,
        zero_division=0,
    )

    accuracy = accuracy_score(
        y_test,
        predictions,
    )

    macro_f1 = report["macro avg"]["f1-score"]

    weighted_f1 = report["weighted avg"]["f1-score"]

    return ModelResult(
        name=model_name,
        accuracy=float(accuracy),
        macro_f1=float(macro_f1),
        weighted_f1=float(weighted_f1),
        report=report,
    )