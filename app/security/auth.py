from datetime import datetime, timedelta, timezone
from typing import Any

import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from pwdlib import PasswordHash

from app.config import get_settings
from app.database.repositories.user import get_user_by_username
from app.database.session import SessionLocal
from app.security.rbac import Role


# ============================================================
# CONFIGURATION
# ============================================================

settings = get_settings()

# JWT algorithm used to sign tokens.
JWT_ALGORITHM = "HS256"

# Token lifetime.
ACCESS_TOKEN_EXPIRE_MINUTES = 30


# ============================================================
# PASSWORD HASHING
# ============================================================

password_hash = PasswordHash.recommended()


# ============================================================
# PASSWORD VERIFICATION
# ============================================================

def verify_password(
    plain_password: str,
    stored_password_hash: str,
) -> bool:
    """
    Verify a plain-text password against its stored password hash.

    The database stores only password hashes.
    """

    return password_hash.verify(
        plain_password,
        stored_password_hash,
    )


# ============================================================
# USER AUTHENTICATION
# ============================================================

def authenticate_user(
    username: str,
    password: str,
) -> dict[str, Any] | None:
    """
    Authenticate a user using the SQLite user database.

    Returns a user dictionary when credentials are valid.

    Returns None when:
        - the username does not exist
        - the password is incorrect
        - the user is inactive
    """

    db = SessionLocal()

    try:
        user = get_user_by_username(
            db,
            username,
        )

        if user is None:
            return None

        if not user.is_active:
            return None

        if not verify_password(
            password,
            user.password_hash,
        ):
            return None

        return {
            "username": user.username,
            "role": user.role,
        }

    finally:
        db.close()


# ============================================================
# JWT TOKEN CREATION
# ============================================================

def create_access_token(
    username: str,
    role: str,
    expires_delta: timedelta | None = None,
) -> str:
    """
    Create a signed JWT access token.

    The token contains:
        sub  -> username
        role -> user's role
        iat  -> issued-at time
        exp  -> expiration time
    """

    if expires_delta is None:
        expires_delta = timedelta(
            minutes=ACCESS_TOKEN_EXPIRE_MINUTES
        )

    now = datetime.now(timezone.utc)

    expire = now + expires_delta

    payload = {
        "sub": username,
        "role": role,
        "iat": now,
        "exp": expire,
    }

    # Temporary development secret.
    #
    # We will move this to a dedicated JWT_SECRET
    # environment variable later.

    secret = settings.jwt_secret

    if not secret:
     raise RuntimeError(
        "JWT_SECRET is not configured."
    )
    token = jwt.encode(
        payload,
        secret,
        algorithm=JWT_ALGORITHM,
    )

    return token


# ============================================================
# JWT TOKEN DECODING
# ============================================================

def decode_access_token(
    token: str,
) -> dict[str, Any]:
    """
    Decode and validate a JWT access token.

    Raises HTTP 401 when:
        - token is invalid
        - token is expired
        - required claims are missing
    """
    secret = settings.jwt_secret

    if not secret:
      raise RuntimeError(
         "JWT_SECRET is not configured."
    )
    try:
        payload = jwt.decode(
            token,
            secret,
            algorithms=[JWT_ALGORITHM],
        )

    except jwt.ExpiredSignatureError as exc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Access token has expired.",
            headers={
                "WWW-Authenticate": "Bearer"
            },
        ) from exc

    except jwt.InvalidTokenError as exc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid access token.",
            headers={
                "WWW-Authenticate": "Bearer"
            },
        ) from exc

    username = payload.get("sub")
    role = payload.get("role")

    if not username or not role:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Access token is missing required claims.",
            headers={
                "WWW-Authenticate": "Bearer"
            },
        )

    return payload


# ============================================================
# BEARER TOKEN SECURITY
# ============================================================

bearer_scheme = HTTPBearer(
    auto_error=True,
)


# ============================================================
# CURRENT USER
# ============================================================

def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(
        bearer_scheme
    ),
) -> dict[str, Any]:
    """
    FastAPI dependency that authenticates the current request.

    The JWT is checked first.

    Then the database is checked to make sure:
        1. The user still exists.
        2. The user is still active.
        3. The user's current role matches the JWT role.

    Returns:

    {
        "username": "...",
        "role": "..."
    }
    """

    token = credentials.credentials

    # --------------------------------------------------------
    # STEP 1: Decode and validate JWT
    # --------------------------------------------------------

    payload = decode_access_token(token)

    username = payload["sub"]
    token_role = payload["role"]

    # --------------------------------------------------------
    # STEP 2: Look up current user in SQLite
    # --------------------------------------------------------

    db = SessionLocal()

    try:
        user = get_user_by_username(
            db,
            username,
        )

        # ----------------------------------------------------
        # User no longer exists
        # ----------------------------------------------------

        if user is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="User no longer exists.",
                headers={
                    "WWW-Authenticate": "Bearer"
                },
            )

        # ----------------------------------------------------
        # User was disabled after token creation
        # ----------------------------------------------------

        if not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="User account is inactive.",
                headers={
                    "WWW-Authenticate": "Bearer"
                },
            )

        # ----------------------------------------------------
        # STEP 3: Prevent role tampering
        # ----------------------------------------------------

        if user.role != token_role:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="User role is invalid.",
                headers={
                    "WWW-Authenticate": "Bearer"
                },
            )

        # ----------------------------------------------------
        # STEP 4: Return authenticated user
        # ----------------------------------------------------

        return {
            "username": user.username,
            "role": user.role,
        }

    finally:
        db.close()