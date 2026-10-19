
import pytest

from app.security.rbac import (
    Permission,
    Role,
    can_execute_action,
    has_permission,
    permission_for_action,
    require_permission,
)


# ============================================================
# ROLE PERMISSION TESTS
# ============================================================


def test_viewer_can_view_incident():
    assert has_permission(
        Role.VIEWER,
        Permission.VIEW_INCIDENT,
    ) is True


def test_viewer_cannot_add_work_note():
    assert has_permission(
        Role.VIEWER,
        Permission.ADD_WORK_NOTE,
    ) is False


def test_analyst_can_add_work_note():
    assert has_permission(
        Role.ANALYST,
        Permission.ADD_WORK_NOTE,
    ) is True


def test_analyst_cannot_resolve_incident():
    assert has_permission(
        Role.ANALYST,
        Permission.RESOLVE_INCIDENT,
    ) is False


def test_operator_can_resolve_incident():
    assert has_permission(
        Role.OPERATOR,
        Permission.RESOLVE_INCIDENT,
    ) is True


def test_admin_has_admin_permission():
    assert has_permission(
        Role.ADMIN,
        Permission.ADMIN,
    ) is True


# ============================================================
# ACTION AUTHORIZATION TESTS
# ============================================================


def test_analyst_can_add_work_note_action():
    assert can_execute_action(
        "analyst",
        "add_work_note",
    ) is True


def test_analyst_cannot_resolve_incident_action():
    assert can_execute_action(
        "analyst",
        "resolve_incident",
    ) is False


def test_operator_can_resolve_incident_action():
    assert can_execute_action(
        "operator",
        "resolve_incident",
    ) is True


def test_unknown_action_is_denied():
    assert can_execute_action(
        "admin",
        "delete_database",
    ) is False


# ============================================================
# ACTION → PERMISSION TESTS
# ============================================================


def test_resolve_action_requires_resolve_permission():
    assert permission_for_action(
        "resolve_incident"
    ) == Permission.RESOLVE_INCIDENT


def test_unknown_action_has_no_permission():
    assert permission_for_action(
        "delete_database"
    ) is None


# ============================================================
# REQUIRE PERMISSION TESTS
# ============================================================


def test_require_permission_allows_valid_permission():
    require_permission(
        "operator",
        "resolve_incident",
    )


def test_require_permission_rejects_invalid_permission():
    with pytest.raises(PermissionError):
        require_permission(
            "analyst",
            "resolve_incident",
        )
