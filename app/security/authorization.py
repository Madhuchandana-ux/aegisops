from typing import Any

from fastapi import HTTPException, status

from app.security.rbac import can_execute_action


# ============================================================
# AUTHORIZATION HELPERS
# ============================================================


def require_action_permission(
    action_name: str,
    user: dict[str, Any],
) -> None:
    """Require a user to have permission to execute a controlled action.

    Raises an HTTP 403 when the user is missing a role or the role does not
    have permission for the requested action.
    """
    role = user.get("role") if isinstance(user, dict) else None

    if not role or not can_execute_action(role, action_name):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=(
                f"User '{user.get('username', 'unknown')}' is not authorized "
                f"to execute action '{action_name}'."
            ),
        )
