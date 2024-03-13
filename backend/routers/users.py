from fastapi import APIRouter
from backend import database as db

users_router = APIRouter(prefix="/users", tags=["Users"])

from backend.entities import (
    UserCollection,
    UserInDB,
    UserCreate,
    User,
    ChatCollection
)

@users_router.get("")
def get_users():
    """
    Gets all users in the database
    """
    db_users = db.get_all_users()

    return UserCollection(
        meta={"count": len(db_users)},
        users = db_users,
    )


@users_router.post("", response_model=User)
def create_user(user_create: UserCreate):
    """Add a new user to the database"""
    return db.create_user(user_create)


@users_router.get("/{user_id}", response_model=User)
def get_user(user_id: int):
    """Get new user data from the database"""
    return db.get_user(user_id)

@users_router.get("/{user_id}/chats", response_model=ChatCollection)
def get_user_chats(user_id: int):
    """Get a list of all chats a given user has participated in"""
    return db.get_user_chats(user_id)
