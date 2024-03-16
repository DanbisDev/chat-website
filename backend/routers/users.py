from fastapi import APIRouter, Depends
from sqlmodel import Session
from backend import database as db

users_router = APIRouter(prefix="/users", tags=["Users"])

from backend.routers.auths import get_current_user
from backend.schema import *

from backend.entities import *




@users_router.get("")
def get_users(session: Session = Depends(db.get_session)):
    """
    Gets all users in the database
    """
    return db.get_all_users(session)

@users_router.get("/me", response_model=UserResponse)
def get_self(user: UserInDB = Depends(get_current_user)):
    """Get current user."""
    return UserResponse(user=User(**user.model_dump()))

@users_router.put("/me", response_model=UserResponse)
def update_current_user_data(
    update_data: UpdateUserData,
    current_user: UserInDB = Depends(get_current_user),
    session: Session = Depends(db.get_session),
):
    """Update the username or email of the current user."""
    if update_data.username:
        current_user.username = update_data.username
    if update_data.email:
        current_user.email = update_data.email
    
    session.commit()
    session.refresh(current_user)
    
    return UserResponse(user = User(
        id = current_user.id,
        username = current_user.username,
        email = current_user.email,
        created_at = current_user.created_at
    ))

@users_router.get("/{user_id}", response_model=UserResponse)
def get_user(user_id: int, session: Session = Depends(db.get_session)):
    """Get new user data from the database"""
    return db.get_user(session, user_id)

@users_router.get("/{user_id}/chats", response_model=UserChatCollection)
def get_user_chats(user_id: int, session: Session = Depends(db.get_session)):
    """Get a list of all chats a given user has participated in"""
    return db.get_user_chats(session, user_id)


