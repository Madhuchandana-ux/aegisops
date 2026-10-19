import pandas as pd
import pytest

from app.ml.classifier import IncidentClassifier


def create_training_dataframe():
    return pd.DataFrame(
        {
            "description": [
                "Cannot access shared file folder.",
                "File server access is unavailable.",
                "Need access to company files.",
                "Microsoft Office application crashes.",
                "Outlook is not opening.",
                "Excel application is failing.",
                "User cannot log into account.",
                "Password authentication failed.",
                "Corporate account login does not work.",
            ],
            "category": [
                "Fileservice",
                "Fileservice",
                "Fileservice",
                "Software",
                "Software",
                "Software",
                "Active Directory",
                "Active Directory",
                "Active Directory",
            ],
        }
    )


def test_classifier_training():

    df = create_training_dataframe()

    classifier = IncidentClassifier()

    classifier.train(df)

    assert classifier.is_fitted is True


def test_classifier_prediction():

    df = create_training_dataframe()

    classifier = IncidentClassifier()

    classifier.train(df)

    result = classifier.predict(
        "I cannot access the file server."
    )

    assert result.predicted_category in {
        "Fileservice",
        "Software",
        "Active Directory",
    }

    assert 0.0 <= result.confidence <= 1.0


def test_prediction_requires_training():

    classifier = IncidentClassifier()

    with pytest.raises(RuntimeError):

        classifier.predict(
            "VPN connection is failing."
        )


def test_empty_description_is_rejected():

    df = create_training_dataframe()

    classifier = IncidentClassifier()

    classifier.train(df)

    with pytest.raises(ValueError):

        classifier.predict("")


def test_classifier_evaluation():

    train_df = create_training_dataframe()

    test_df = pd.DataFrame(
        {
            "description": [
                "Cannot access shared files.",
                "Outlook application crashes.",
                "Password login failed.",
            ],
            "category": [
                "Fileservice",
                "Software",
                "Active Directory",
            ],
        }
    )

    classifier = IncidentClassifier()

    classifier.train(train_df)

    results = classifier.evaluate(
        test_df
    )

    assert "accuracy" in results

    assert (
        0.0
        <= results["accuracy"]
        <= 1.0
    )

    assert "classification_report" in results

    assert "confusion_matrix" in results