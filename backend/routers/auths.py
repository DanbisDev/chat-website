import datetime
import os
import select
from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlmodel import SQLModel, Session
from backend import database as db
from backend.auth import AccessToken, Claims, InvalidCredentials, UserRegistration
from backend.entities import User, UserResponse
from passlib.context import CryptContext
from backend.schema import UserInDB
import jwt

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")
auth_router = APIRouter(prefix="/auth", tags=["Authentication"])
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
access_token_duration = 3600  # seconds
jwt_key = os.environ.get("JWT_KEY")
jwt_alg = "HS256"

class UserRegistration(SQLModel):
    """Request model to register new user."""

    username: str
    email: str
    password: str

@auth_router.post("/registration", response_model=UserResponse)
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


def verify_token(token: str, session: Session) -> UserInDB:   
    try:
        payload = jwt.decode(token, jwt_key, algorithms=[jwt_alg])
        user_id = payload.get("sub")
        user = session.get(UserInDB, user_id)
        if user_id is None:
            raise HTTPException(status_code=401, detail="Invalid token: User ID missing")
        
        user = session.get(UserInDB, user_id)
        if user is None:
            raise HTTPException(status_code=401, detail="User not found")
        
        return user
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token has expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")
    except Exception as e:
        # Catch any unexpected errors during token verification
        raise HTTPException(status_code=500, detail="Internal server error") from e


def get_current_user(session: Session = Depends(db.get_session), token: str = Depends(oauth2_scheme)) -> UserInDB:
    """
    Dependency to get the current user from the provided token.
    """
    # Verify token and get user from token
    user = verify_token(token, session)
    if user is None:
        raise HTTPException(
            status_code=401,
            detail="Invalid or expired token",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return UserInDB()












def _get_authenticated_user(
    session: Session,
    form: OAuth2PasswordRequestForm,
) -> UserInDB:
    user = session.exec(
        select(UserInDB).where(UserInDB.username == form.username)
    ).first()

    if user is None or not pwd_context.verify(form.password, user.hashed_password):
        raise InvalidCredentials()

    return user

def _build_access_token(user: UserInDB) -> AccessToken:
    expiration = int(datetime.now(datetime.timezone.utc).timestamp()) + access_token_duration
    claims = Claims(sub=str(user.id), exp=expiration)
    access_token = jwt.encode(claims.model_dump(), key=jwt_key, algorithm=jwt_alg)

    return AccessToken(
        access_token=access_token,
        token_type="Bearer",
        expires_in=access_token_duration,
    )