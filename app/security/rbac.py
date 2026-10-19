from enum import Enum

# ============================================================
# ROLES
# ============================================================


class Role(str, Enum):
    """Roles supported by AegisOps."""

    VIEWER = "viewer"
    ANALYST = "analyst"
    OPERATOR = "operator"
    ADMIN = "admin"


# ============================================================
# PERMISSIONS
# ============================================================


class Permission(str, Enum):
    VIEW_INCIDENT = "incident:view"
    CREATE_INCIDENT = "incident:create"
    ADD_WORK_NOTE = "incident:add_work_note"
    UPDATE_INCIDENT = "incident:update"
    RESOLVE_INCIDENT = "incident:resolve"
    ADMIN = "admin"

# ============================================================
# ROLE → PERMISSION MAPPING
# ============================================================

ROLE_PERMISSIONS: dict[Role, set[Permission]] = {
    Role.VIEWER: {
        Permission.VIEW_INCIDENT,
        Permission.CREATE_INCIDENT,
    },
    Role.ANALYST: {
        Permission.VIEW_INCIDENT,
        Permission.CREATE_INCIDENT,
        Permission.ADD_WORK_NOTE,
    },
    Role.OPERATOR: {
        Permission.VIEW_INCIDENT,
        Permission.CREATE_INCIDENT,
        Permission.ADD_WORK_NOTE,
        Permission.UPDATE_INCIDENT,
        Permission.RESOLVE_INCIDENT,
    },
    Role.ADMIN: {
        Permission.VIEW_INCIDENT,
        Permission.CREATE_INCIDENT,
        Permission.ADD_WORK_NOTE,
        Permission.UPDATE_INCIDENT,
        Permission.RESOLVE_INCIDENT,
        Permission.ADMIN,
    },
}


# ============================================================
# BASIC PERMISSION CHECK
# ============================================================


def has_permission(
    role: Role | str,
    permission: Permission | str,
) -> bool:
    """Check whether a role has a specific permission."""

    try:
        role = Role(role)
        permission = Permission(permission)
    except ValueError:
        return False

    return permission in ROLE_PERMISSIONS.get(role, set())


# ============================================================
# SERVICE NOW ACTION → PERMISSION
# ============================================================


ACTION_PERMISSIONS: dict[str, Permission] = {
    "get_incident": Permission.VIEW_INCIDENT,
    "create_incident": Permission.CREATE_INCIDENT,
    "add_work_note": Permission.ADD_WORK_NOTE,
    "update_incident": Permission.UPDATE_INCIDENT,
    "resolve_incident": Permission.RESOLVE_INCIDENT,
}


def permission_for_action(
    action_name: str,
) -> Permission | None:
    """Return the permission required for a controlled ServiceNow action.

    Unknown actions return None instead of being automatically authorized.
    """

    return ACTION_PERMISSIONS.get(action_name)


# ============================================================
# ACTION AUTHORIZATION
# ============================================================


def can_execute_action(
    role: Role | str,
    action_name: str,
) -> bool:
    """Check whether the given role is allowed to execute
    the requested controlled ServiceNow action.

    Unknown actions are denied by default.
    """

    permission = permission_for_action(action_name)

    if permission is None:
        return False

    return has_permission(role, permission)


# ============================================================
# REQUIRE PERMISSION / ACTION
# ============================================================


def require_permission(
    role: Role | str,
    permission_or_action: Permission | str,
) -> None:
    """Require a role to have a permission or permission
    associated with a controlled ServiceNow action.

    Unknown permissions and unknown actions are denied.
    """

    # --------------------------------------------------------
    # First check whether the value is a controlled action.
    # --------------------------------------------------------
    if isinstance(permission_or_action, str):
        action_permission = permission_for_action(permission_or_action)

        if action_permission is not None:
            if not has_permission(role, action_permission):
                raise PermissionError(
                    f"Role '{role}' does not have permission "
                    f"to execute action '{permission_or_action}'."
                )
            return

    # --------------------------------------------------------
    # Otherwise treat it as a Permission.
    # --------------------------------------------------------
    if not has_permission(role, permission_or_action):
        raise PermissionError(
            f"Role '{role}' does not have permission "
            f"'{permission_or_action}'."
        )