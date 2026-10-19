
import pytest

from fastapi import HTTPException

from app.security.auth import (
    authenticate_user,
    create_access_token,
    decode_access_token,
)


# ============================================================
# AUTHENTICATION
# ============================================================

def test_valid_user_authentication():
    user = authenticate_user(
        "operator",
        "Operator@123",
    )

    assert user is not None
    assert user["username"] == "operator"
    assert user["role"] == "operator"


def test_invalid_password_rejected():
    user = authenticate_user(
        "operator",
        "WrongPassword",
    )

    assert user is None


def test_unknown_user_rejected():
    user = authenticate_user(
        "does_not_exist",
        "Password123",
    )

    assert user is None


# ============================================================
# JWT CREATION
# ============================================================

def test_create_access_token():
    token = create_access_token(
        username="operator",
        role="operator",
    )

    assert isinstance(token, str)
    assert len(token) > 0


# ============================================================
# JWT DECODING
# ============================================================

def test_decode_access_token():
    token = create_access_token(
        username="operator",
        role="operator",
    )

    payload = decode_access_token(token)

    assert payload["sub"] == "operator"
    assert payload["role"] == "operator"


def test_invalid_token_rejected():
    with pytest.raises(HTTPException) as exc_info:
        decode_access_token(
            "this-is-not-a-valid-jwt"
        )

    assert exc_info.value.status_code == 401
