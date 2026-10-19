from sqlalchemy.orm import Session

from app.database.models.audit_log import AuditLog


def create_audit_log(
    db: Session,
    *,
    run_id: str,
    username: str,
    action: str,
    risk_level: str,
    allowed: bool,
    reason: str,
) -> AuditLog:

    audit_log = AuditLog(
        run_id=run_id,
        username=username,
        action=action,
        risk_level=risk_level,
        allowed=allowed,
        reason=reason,
    )

    db.add(audit_log)
    db.commit()
    db.refresh(audit_log)

    return audit_log