from fastapi import APIRouter, Depends
from sqlmodel import Session
from backend import database as db

users_router = APIRouter(prefix="/users", tags=["Users"])

from backend.schema import *

from backend.entities import (
    UserCollection,
    UserCreate,
    User,
    ChatCollection,
    UserResponse
)




@users_router.get("")
def get_users(session: Session = Depends(db.get_session)):
    """
    Gets all users in the database
    """
    db_users = db.get_all_users(session)

    return UserCollection(
        meta={"count": len(db_users)},
        users = db_users,
    )



@users_router.get("/{user_id}", response_model=UserResponse)
def get_user(user_id: str, session: Session = Depends(db.get_session)):
    """Get new user data from the database"""
    return db.get_user(session, user_id)

@users_router.get("/{user_id}/chats", response_model=ChatCollection)
def get_user_chats(user_id: str, session: Session = Depends(db.get_session)):
    """Get a list of all chats a given user has participated in"""
    return db.get_user_chats(session, int(user_id))
