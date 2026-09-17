from app.ml.data_loader import (
    load_incidents,
    load_knowledge_base,
)


def test_load_incidents():
    df = load_incidents()

    assert len(df) == 10

    assert "incident_id" in df.columns
    assert "description" in df.columns
    assert "category" in df.columns
    assert "priority" in df.columns


def test_load_knowledge_base():
    df = load_knowledge_base()

    assert len(df) == 8

    assert "document_id" in df.columns
    assert "title" in df.columns
    assert "content" in df.columns
    assert "category" in df.columns