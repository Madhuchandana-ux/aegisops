from app.agents.state import AgentState
from app.database.repositories.agent_run import (
    complete_agent_run,
    create_agent_run,
)
from app.database.repositories.audit_log import create_audit_log
from app.database.session import SessionLocal


def start_agent_run(state: AgentState) -> None:
    run_id = state.get("run_id", "")

    if not run_id:
        return

    db = SessionLocal()

    try:
        create_agent_run(
            db,
            run_id=run_id,
            incident_id=state.get("incident_id", ""),
            username=state.get("username", ""),
            incident_text=state.get("incident_text", ""),
        )
    finally:
        db.close()


def finish_agent_run(state: AgentState) -> None:
    run_id = state.get("run_id", "")

    if not run_id:
        return

    db = SessionLocal()

    try:
        complete_agent_run(
            db,
            run_id,
            category=state.get("category", ""),
            priority=state.get("priority", ""),
            confidence=state.get("confidence", 0.0),
            status="completed",
            final_response=state.get("final_response", ""),
        )
    finally:
        db.close()


def record_policy_decision(state: AgentState) -> None:
    run_id = state.get("run_id", "")

    if not run_id:
        return

    db = SessionLocal()

    try:
        create_audit_log(
            db,
            run_id=run_id,
            username=state.get("username", ""),
            action=state.get("action_name", ""),
            risk_level=state.get("risk_level", "UNKNOWN"),
            allowed=state.get("policy_allowed", False),
            reason=state.get("policy_reason", ""),
        )
    finally:
        db.close()