from collections.abc import Callable
from typing import Any

from fastapi import Depends, HTTPException, status

from app.security.auth import get_current_user
from app.security.rbac import can_execute_action


def require_action(action_name: str) -> Callable:
    """
    FastAPI dependency factory for action-level authorization.

    The current user's JWT is validated first.
    Their database-backed role is then checked against
    the requested controlled action.
    """

    def dependency(
        current_user: dict[str, Any] = Depends(get_current_user),
    ) -> dict[str, Any]:

        role = current_user["role"]

        if not can_execute_action(role, action_name):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=(
                    f"Role '{role}' is not authorized "
                    f"to execute '{action_name}'."
                ),
            )

        return current_user

    return dependency