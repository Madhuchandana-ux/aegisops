
from typing import Any

from fastapi import Depends, HTTPException, status

from app.security.auth import get_current_user
from app.security.rbac import can_execute_action


# ============================================================
# ACTION AUTHORIZATION
# ============================================================

def require_action_permission(
    action_name: str,
    current_user: dict[str, Any],
) -> None:
    """
    Verify that the authenticated user is allowed to execute
    the requested controlled action.

    This function performs RBAC authorization.

    It does NOT decide whether the action is safe to automate.
    That decision belongs to the policy engine.
    """

    role = current_user.get("role")

    if not role:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Authenticated user has no valid role.",
        )

    allowed = can_execute_action(
        role,
        action_name,
    )

    if not allowed:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=(
                f"Role '{role}' is not authorized "
                f"to execute action '{action_name}'."
            ),
        )


# ============================================================
# FASTAPI DEPENDENCY FACTORY
# ============================================================

def action_permission_dependency(
    action_name: str,
):
    """
    Create a FastAPI dependency that requires a specific
    controlled ServiceNow action.
    """

    def dependency(
        current_user: dict[str, Any] = Depends(
            get_current_user
        ),
    ) -> dict[str, Any]:

        require_action_permission(
            action_name,
            current_user,
        )

        return current_user

    return dependency
