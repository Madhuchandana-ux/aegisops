
from fastapi import APIRouter, HTTPException, status

from app.api.schemas.auth import (
    CurrentUserResponse,
    LoginRequest,
    LoginResponse,
)
from app.security.auth import (
    ACCESS_TOKEN_EXPIRE_MINUTES,
    authenticate_user,
    create_access_token,
    get_current_user,
)


router = APIRouter(
    prefix="/auth",
    tags=["Authentication"],
)


# ============================================================
# LOGIN
# ============================================================

@router.post(
    "/login",
    response_model=LoginResponse,
)
async def login(
    request: LoginRequest,
):
    """
    Authenticate a user and return a JWT access token.
    """

    user = authenticate_user(
        username=request.username,
        password=request.password,
    )

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password.",
            headers={
                "WWW-Authenticate": "Bearer"
            },
        )

    access_token = create_access_token(
        username=user["username"],
        role=user["role"],
    )

    return LoginResponse(
        access_token=access_token,
        token_type="bearer",
        expires_in=ACCESS_TOKEN_EXPIRE_MINUTES * 60,
    )


# ============================================================
# CURRENT USER
# ============================================================

@router.get(
    "/me",
    response_model=CurrentUserResponse,
)
async def get_me(
    current_user: dict = __import__(
        "fastapi"
    ).Depends(get_current_user),
):
    """
    Return the identity represented by the JWT.
    """

    return CurrentUserResponse(
        username=current_user["username"],
        role=current_user["role"],
    )
