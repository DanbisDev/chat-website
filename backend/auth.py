import os
from fastapi import HTTPException
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext
from pydantic import BaseModel
from sqlmodel import SQLModel

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
jwt_key = os.environ.get("JWT_KEY")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")

class UserRegistration(SQLModel):
    """Request model to register new user."""

    username: str
    email: str
    password: str

class Claims(BaseModel):
    """Access token claims (aka payload)."""

    sub: str  # id of user
    exp: int  # unix timestamp

class AccessToken(BaseModel):
    """Response model for access token."""

    access_token: str
    token_type: str
    expires_in: int

class AuthException(HTTPException):
    def __init__(self, error: str, description: str):
        super().__init__(
            status_code=401,
            detail={
                "error": error,
                "error_description": description,
            },
        )

class InvalidCredentials(AuthException):
    def __init__(self):
        super().__init__(
            error="invalid_client",
            description="invalid username or password",
        )


class InvalidToken(AuthException):
    def __init__(self):
        super().__init__(
            error="invalid_client",
            description="invalid bearer token",
        )


class ExpiredToken(AuthException):
    def __init__(self):
        super().__init__(
            error="invalid_client",
            description="expired bearer token",
        )