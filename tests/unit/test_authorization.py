
import pytest

from fastapi import HTTPException

from app.security.authorization import (
    require_action_permission,
)
from app.security.rbac import (
    can_execute_action,
)


# ============================================================
# RBAC ACTION TESTS
# ============================================================

def test_viewer_can_get_incident():
    assert can_execute_action(
        "viewer",
        "get_incident",
    ) is True


def test_viewer_cannot_add_work_note():
    assert can_execute_action(
        "viewer",
        "add_work_note",
    ) is False


def test_analyst_can_add_work_note():
    assert can_execute_action(
        "analyst",
        "add_work_note",
    ) is True


def test_analyst_cannot_resolve_incident():
    assert can_execute_action(
        "analyst",
        "resolve_incident",
    ) is False


def test_operator_can_resolve_incident():
    assert can_execute_action(
        "operator",
        "resolve_incident",
    ) is True


# ============================================================
# AUTHORIZATION DEPENDENCY TESTS
# ============================================================

def test_operator_can_execute_resolve():
    user = {
        "username": "operator",
        "role": "operator",
    }

    require_action_permission(
        "resolve_incident",
        user,
    )


def test_analyst_cannot_execute_resolve():
    user = {
        "username": "analyst",
        "role": "analyst",
    }

    with pytest.raises(HTTPException) as exc_info:

        require_action_permission(
            "resolve_incident",
            user,
        )

    assert exc_info.value.status_code == 403


def test_viewer_cannot_execute_work_note():
    user = {
        "username": "viewer",
        "role": "viewer",
    }

    with pytest.raises(HTTPException) as exc_info:

        require_action_permission(
            "add_work_note",
            user,
        )

    assert exc_info.value.status_code == 403


def test_missing_role_is_rejected():
    user = {
        "username": "viewer",
    }

    with pytest.raises(HTTPException) as exc_info:

        require_action_permission(
            "get_incident",
            user,
        )

    assert exc_info.value.status_code == 403
