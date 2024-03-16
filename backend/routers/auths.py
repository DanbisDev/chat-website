import datetime
import os
import select
from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import ValidationError
from sqlmodel import SQLModel, Session
from backend import database as db
from backend.auth import AccessToken, Claims, ExpiredToken, InvalidCredentials, InvalidToken, UserRegistration
from backend.entities import User, UserResponse
from passlib.context import CryptContext
from backend.schema import UserInDB
from jose import jwt, ExpiredSignatureError, JWTError

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")
auth_router = APIRouter(prefix="/auth", tags=["Authentication"])
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
access_token_duration = 3600  # seconds
jwt_key = os.environ.get(
    "JWT_KEY", 
    default="any string you want for a dev JWT key",
)
jwt_alg = "HS256"

class UserRegistration(SQLModel):
    """Request model to register new user."""

    username: str
    email: str
    password: str

@auth_router.post("/registration", response_model=UserResponse, status_code=201)
def register_new_user(
    registration: UserRegistration,
    # session: Session = Depends(db.get_session),
    session: Session = Depends(db.get_session),
):
    """Register new user."""

    hashed_password = pwd_context.hash(registration.password)
    user = UserInDB(
        **registration.model_dump(),
        hashed_password=hashed_password,
    )

    # if username already exists
    if db.get_user_by_username(session, registration.username):
        raise HTTPException(
            status_code=422,
            detail = {
                "type": "duplicate_value",
                "entity_name": "User",
                "entity_field": "username",
                "entity_value": registration.username,
            }
        )

    # if email aready exists
    if db.get_user_by_email(session, registration.email):
                raise HTTPException(
            status_code=422,
            detail = {
                "type": "duplicate_value",
                "entity_name": "User",
                "entity_field": "email",
                "entity_value": registration.email,
            }
        )

    session.add(user)
    session.commit()
    session.refresh(user)
    return UserResponse(user=User(id=user.id, username=user.username, email=user.email, created_at=user.created_at))

@auth_router.post("/token", response_model=AccessToken)
def get_access_token(
    form: OAuth2PasswordRequestForm = Depends(),
    session: Session = Depends(db.get_session),
):
    """Get access token for user."""

    user = _get_authenticated_user(session, form)
    return _build_access_token(user)


def _decode_access_token(session: Session, token: str) -> UserInDB:
    try:
        claims_dict = jwt.decode(token, key=jwt_key, algorithms=[jwt_alg])
        claims = Claims(**claims_dict)
        user_id = claims.sub
        user = session.get(UserInDB, user_id)

        if user is None:
            raise InvalidToken()

        return user
    except jwt.ExpiredSignatureError:
        raise ExpiredToken()
    except JWTError():
        raise InvalidToken()
    except ValidationError():
        raise InvalidToken()



def get_current_user(session: Session = Depends(db.get_session), token: str = Depends(oauth2_scheme)) -> UserInDB:
    """
    Dependency to get the current user from the provided token.
    """
    # Verify token and get user from token
    try:
        user = _decode_access_token(session, token)
        if user is None:
            raise HTTPException(
                status_code=401,
                detail={
                    "error": "invalid_token",
                    "error_description": "Invalid or expired token"
                },
            )
        return user
    except InvalidCredentials:
        raise InvalidCredentials
        

def _get_authenticated_user(
    session: Session,
    form: OAuth2PasswordRequestForm,
) -> UserInDB:
    user = db.get_user_by_username(session, form.username)

    print(type(user))

    if user is None or not pwd_context.verify(form.password, user.hashed_password):
        raise InvalidCredentials()

    return user

def _build_access_token(user: UserInDB) -> AccessToken:
    expiration = int(datetime.datetime.now(datetime.timezone.utc).timestamp()) + access_token_duration
    claims = Claims(sub=str(user.id), exp=expiration)
    access_token = jwt.encode(claims.model_dump(), key=jwt_key, algorithm=jwt_alg)

    return AccessToken(
        access_token=access_token,
        token_type="Bearer",
        expires_in=access_token_duration,
    )