
from pydantic import BaseModel


# ============================================================
# LOGIN REQUEST
# ============================================================

class LoginRequest(BaseModel):
    username: str
    password: str


# ============================================================
# LOGIN RESPONSE
# ============================================================

class LoginResponse(BaseModel):
    access_token: str
    token_type: str
    expires_in: int


# ============================================================
# CURRENT USER RESPONSE
# ============================================================

class CurrentUserResponse(BaseModel):
    username: str
    role: str
