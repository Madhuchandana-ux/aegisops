from dataclasses import dataclass
from pathlib import Path
from typing import Any

import joblib
import pandas as pd

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.pipeline import FeatureUnion, Pipeline
from sklearn.svm import LinearSVC
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix,
    f1_score,
)


@dataclass
class ClassificationResult:
    """
    Result returned by the incident classifier.
    """

    category: str
    confidence: float

    @property
    def predicted_category(self) -> str:
        """
        Backward-compatible name used by the unit tests.
        """
        return self.category


class IncidentClassifier:
    """
    Production-oriented incident classification model.

    Architecture:
        Word TF-IDF
              +
        Character TF-IDF
              ↓
        FeatureUnion
              ↓
        LinearSVC
    """

    def __init__(self) -> None:
        self.model = self._build_model()
        self.is_fitted = False

    @staticmethod
    def _build_model() -> Pipeline:
        """
        Build the Word + Character TF-IDF + Linear SVM pipeline.
        """

        word_features = TfidfVectorizer(
            analyzer="word",
            lowercase=True,
            strip_accents="unicode",
            ngram_range=(1, 2),
            min_df=2,
            sublinear_tf=True,
        )

        character_features = TfidfVectorizer(
            analyzer="char_wb",
            lowercase=True,
            strip_accents="unicode",
            ngram_range=(3, 5),
            min_df=2,
            sublinear_tf=True,
        )

        combined_features = FeatureUnion(
            [
                ("word", word_features),
                ("character", character_features),
            ]
        )

        classifier = LinearSVC(
            class_weight="balanced",
            random_state=42,
        )

        return Pipeline(
            [
                ("features", combined_features),
                ("classifier", classifier),
            ]
        )

    @staticmethod
    def _validate_training_dataframe(df: pd.DataFrame) -> None:
        """
        Validate the dataframe before training.
        """

        required_columns = {
            "description",
            "category",
        }

        missing_columns = required_columns - set(df.columns)

        if missing_columns:
            raise ValueError(
                f"Missing required columns: {sorted(missing_columns)}"
            )

        if df.empty:
            raise ValueError(
                "Training dataframe cannot be empty."
            )

        descriptions = (
            df["description"]
            .fillna("")
            .astype(str)
            .str.strip()
        )

        if descriptions.eq("").any():
            raise ValueError(
                "Training data contains empty incident descriptions."
            )

        categories = (
            df["category"]
            .fillna("")
            .astype(str)
            .str.strip()
        )

        if categories.eq("").any():
            raise ValueError(
                "Training data contains empty categories."
            )

    def train(self, df: pd.DataFrame) -> None:
        """
        Train the classifier.
        """

        self._validate_training_dataframe(df)

        X = (
            df["description"]
            .fillna("")
            .astype(str)
            .str.strip()
            .tolist()
        )

        y = (
            df["category"]
            .fillna("")
            .astype(str)
            .str.strip()
            .tolist()
        )

        self.model.fit(X, y)
        self.is_fitted = True

    @staticmethod
    def _normalize_confidence(
        decision_scores: Any,
    ) -> float:
        """
        Convert the SVM decision margin into a bounded confidence-like
        score in [0, 1].

        IMPORTANT:
        This is NOT a calibrated probability.
        """

        import numpy as np

        scores = np.asarray(decision_scores)

        if scores.ndim == 1:
            margin = float(np.max(np.abs(scores)))
        else:
            sorted_scores = np.sort(scores[0])
            margin = float(
                sorted_scores[-1] - sorted_scores[-2]
            )

        confidence = 1.0 / (1.0 + np.exp(-margin))

        return float(
            max(
                0.0,
                min(1.0, confidence),
            )
        )

    def predict(self, text: str) -> ClassificationResult:
        """
        Predict the incident category.
        """

        if not self.is_fitted:
            raise RuntimeError(
                "IncidentClassifier must be trained before prediction."
            )

        if not isinstance(text, str) or not text.strip():
            raise ValueError(
                "Incident description cannot be empty."
            )

        cleaned_text = text.strip()

        prediction = self.model.predict(
            [cleaned_text]
        )[0]

        decision_scores = self.model.decision_function(
            [cleaned_text]
        )

        confidence = self._normalize_confidence(
            decision_scores
        )

        return ClassificationResult(
            category=str(prediction),
            confidence=confidence,
        )

    def evaluate(
        self,
        df: pd.DataFrame,
    ) -> dict[str, Any]:
        """
        Evaluate the classifier and return standard classification metrics.
        """

        if not self.is_fitted:
            raise RuntimeError(
                "IncidentClassifier must be trained before evaluation."
            )

        self._validate_training_dataframe(df)

        X = (
            df["description"]
            .fillna("")
            .astype(str)
            .str.strip()
            .tolist()
        )

        y_true = (
            df["category"]
            .fillna("")
            .astype(str)
            .str.strip()
            .tolist()
        )

        y_pred = self.model.predict(X)

        labels = sorted(
            set(y_true) | set(y_pred)
        )

        report = classification_report(
            y_true,
            y_pred,
            labels=labels,
            output_dict=True,
            zero_division=0,
        )

        matrix = confusion_matrix(
            y_true,
            y_pred,
            labels=labels,
        )

        return {
            "accuracy": float(
                accuracy_score(y_true, y_pred)
            ),
            "macro_f1": float(
                f1_score(
                    y_true,
                    y_pred,
                    average="macro",
                    zero_division=0,
                )
            ),
            "weighted_f1": float(
                f1_score(
                    y_true,
                    y_pred,
                    average="weighted",
                    zero_division=0,
                )
            ),
            "classification_report": report,
            "confusion_matrix": matrix.tolist(),
            "confusion_matrix_labels": labels,
        }

    def save(self, path: str | Path) -> None:
        """
        Save the trained classifier.
        """

        if not self.is_fitted:
            raise RuntimeError(
                "Cannot save an untrained classifier."
            )

        path = Path(path)
        path.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        joblib.dump(
            self.model,
            path,
        )

    def load(self, path: str | Path) -> None:
        """
        Load a previously trained classifier.
        """

        path = Path(path)

        if not path.exists():
            raise FileNotFoundError(
                f"Model file not found: {path}"
            )

        self.model = joblib.load(path)
        self.is_fitted = True