from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.database.base import Base
from app.database.models import AgentRun, AuditLog
from app.database.repositories.agent_run import (
    complete_agent_run,
    create_agent_run,
    get_agent_run,
)
from app.database.repositories.audit_log import create_audit_log


def create_test_session():
    """
    Create a completely isolated in-memory SQLite database
    for each test.
    """

    engine = create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False},
    )

    Base.metadata.create_all(bind=engine)

    TestSessionLocal = sessionmaker(
        bind=engine,
        autoflush=False,
        autocommit=False,
    )

    return engine, TestSessionLocal()


def test_create_and_get_agent_run():
    engine, db = create_test_session()

    try:
        run_id = "test-run-repository-001"

        created = create_agent_run(
            db,
            run_id=run_id,
            incident_id="INC001",
            username="testuser",
            incident_text="VPN is not working.",
        )

        assert created.run_id == run_id
        assert created.status == "started"

        fetched = get_agent_run(
            db,
            run_id,
        )

        assert fetched is not None
        assert fetched.run_id == run_id
        assert fetched.incident_id == "INC001"
        assert fetched.username == "testuser"

    finally:
        db.close()
        engine.dispose()


def test_complete_agent_run():
    engine, db = create_test_session()

    try:
        run_id = "test-run-repository-002"

        create_agent_run(
            db,
            run_id=run_id,
            incident_id="INC002",
            username="testuser",
            incident_text="Outlook is not opening.",
        )

        updated = complete_agent_run(
            db,
            run_id,
            category="O365",
            priority="P2",
            confidence=0.91,
            status="completed",
            final_response="Restart Outlook and recreate the profile.",
        )

        assert updated is not None
        assert updated.category == "O365"
        assert updated.priority == "P2"
        assert updated.confidence == 0.91
        assert updated.status == "completed"
        assert updated.final_response == (
            "Restart Outlook and recreate the profile."
        )
        assert updated.completed_at is not None

    finally:
        db.close()
        engine.dispose()


def test_create_audit_log():
    engine, db = create_test_session()

    try:
        audit_log = create_audit_log(
            db,
            run_id="test-run-repository-003",
            username="testuser",
            action="add_work_note",
            risk_level="LOW",
            allowed=True,
            reason="Policy checks passed.",
        )

        assert audit_log.id is not None
        assert audit_log.run_id == "test-run-repository-003"
        assert audit_log.username == "testuser"
        assert audit_log.action == "add_work_note"
        assert audit_log.risk_level == "LOW"
        assert audit_log.allowed is True
        assert audit_log.reason == "Policy checks passed."

    finally:
        db.close()
        engine.dispose()