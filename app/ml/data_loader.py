from pathlib import Path

import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[2]

INCIDENT_DATA_PATH = (
    PROJECT_ROOT
    / "data"
    / "raw"
    / "incidents.csv"
)

KNOWLEDGE_BASE_PATH = (
    PROJECT_ROOT
    / "data"
    / "knowledge_base"
    / "knowledge_base.csv"
)


def load_incidents() -> pd.DataFrame:
    """
    Load the incident dataset.
    """

    if not INCIDENT_DATA_PATH.exists():
        raise FileNotFoundError(
            f"Incident dataset not found: "
            f"{INCIDENT_DATA_PATH}"
        )

    return pd.read_csv(INCIDENT_DATA_PATH)


def load_knowledge_base() -> pd.DataFrame:
    """
    Load the knowledge-base dataset.
    """

    if not KNOWLEDGE_BASE_PATH.exists():
        raise FileNotFoundError(
            f"Knowledge base not found: "
            f"{KNOWLEDGE_BASE_PATH}"
        )

    return pd.read_csv(KNOWLEDGE_BASE_PATH)