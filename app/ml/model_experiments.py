from dataclasses import dataclass

import pandas as pd

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report
from sklearn.pipeline import FeatureUnion, Pipeline
from sklearn.svm import LinearSVC


@dataclass
class ExperimentResult:
    name: str
    accuracy: float
    macro_f1: float
    weighted_f1: float


def build_word_svm():
    """
    Baseline word-level TF-IDF + Linear SVM.
    """

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


def build_word_char_svm():
    """
    Combines word-level and character-level TF-IDF.

    Word features capture semantic terms such as:
        password
        outlook
        server
        printer

    Character features can capture:
        spelling variations
        abbreviations
        technical identifiers
        partial words
    """

    word_features = TfidfVectorizer(
        analyzer="word",
        lowercase=True,
        strip_accents="unicode",
        ngram_range=(1, 2),
        min_df=2,
        sublinear_tf=True,
    )

    char_features = TfidfVectorizer(
        analyzer="char_wb",
        lowercase=True,
        strip_accents="unicode",
        ngram_range=(3, 5),
        min_df=2,
        sublinear_tf=True,
    )

    return Pipeline(
        [
            (
                "features",
                FeatureUnion(
                    [
                        ("word", word_features),
                        ("char", char_features),
                    ]
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


def build_word_svm_c1():
    """
    Linear SVM with C=1.
    """

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
                    C=1.0,
                    class_weight="balanced",
                    random_state=42,
                ),
            ),
        ]
    )


def build_word_svm_c2():
    """
    Linear SVM with stronger regularization setting.
    """

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
                    C=2.0,
                    class_weight="balanced",
                    random_state=42,
                ),
            ),
        ]
    )


def build_word_svm_c05():
    """
    Linear SVM with C=0.5.
    """

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
                    C=0.5,
                    class_weight="balanced",
                    random_state=42,
                ),
            ),
        ]
    )


def evaluate_model(
    model,
    model_name,
    train_df,
    validation_df,
):
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

    X_validation = (
        validation_df["description"]
        .fillna("")
        .astype(str)
        .str.strip()
    )

    y_validation = (
        validation_df["category"]
        .fillna("")
        .astype(str)
        .str.strip()
    )

    model.fit(X_train, y_train)

    predictions = model.predict(X_validation)

    report = classification_report(
        y_validation,
        predictions,
        output_dict=True,
        zero_division=0,
    )

    return ExperimentResult(
        name=model_name,
        accuracy=float(
            accuracy_score(
                y_validation,
                predictions,
            )
        ),
        macro_f1=float(
            report["macro avg"]["f1-score"]
        ),
        weighted_f1=float(
            report["weighted avg"]["f1-score"]
        ),
    )