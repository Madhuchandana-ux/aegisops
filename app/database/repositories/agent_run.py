from datetime import datetime

from sqlalchemy.orm import Session

from app.database.models.agent_run import AgentRun


def create_agent_run(
    db: Session,
    *,
    run_id: str,
    incident_id: str,
    username: str,
    incident_text: str,
) -> AgentRun:

    agent_run = AgentRun(
        run_id=run_id,
        incident_id=incident_id,
        username=username,
        incident_text=incident_text,
        status="started",
    )

    db.add(agent_run)
    db.commit()
    db.refresh(agent_run)

    return agent_run


def get_agent_run(
    db: Session,
    run_id: str,
) -> AgentRun | None:

    return (
        db.query(AgentRun)
        .filter(AgentRun.run_id == run_id)
        .first()
    )


def complete_agent_run(
    db: Session,
    run_id: str,
    *,
    category: str,
    priority: str,
    confidence: float,
    status: str,
    final_response: str,
) -> AgentRun | None:

    agent_run = get_agent_run(db, run_id)

    if agent_run is None:
        return None

    agent_run.category = category
    agent_run.priority = priority
    agent_run.confidence = confidence
    agent_run.status = status
    agent_run.final_response = final_response
    agent_run.completed_at = datetime.utcnow()

    db.commit()
    db.refresh(agent_run)

    return agent_run