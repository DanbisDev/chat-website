from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from sqlmodel import Session
from backend import database as db

chats_router = APIRouter(prefix="/chats", tags=["Chats"])

from backend.entities import *


@chats_router.get("")
def get_chats(session: Session = Depends(db.get_session)):
    """
    Get All Chats
    """
    return db.get_chats(session)

@chats_router.get("/{chat_id}", response_model=ChatCollection)
def get_chat_by_id(chat_id: int, session: Session = Depends(db.get_session)):
    """
    Get Chat by ID
    """
    return db.get_chat_by_id(session, chat_id)

@chats_router.put("/{chat_id}", response_model=Chat)
def update_chat_name(chat_id:int, new_name:ChatNameUpdate, session: Session = Depends(db.get_session)):
    """
    Update Chat Name by ID
    """
    return db.update_chat_name(session, chat_id, new_name)


@chats_router.get("/{chat_id}/messages", response_model=MessageCollection)
def get_message_col_by_chat_id(chat_id:int, session: Session = Depends(db.get_session)):
    """
    Get Message Collection by Chat ID
    """
    return db.get_message_col_by_chat_id(session, chat_id)

@chats_router.get("/{chat_id}/users", response_model=UserCollection)
def get_users_in_chat_by_chat_id(chat_id:int, session: Session = Depends(db.get_session)):
    """
    Get Users in Chat by Chat ID
    """
    return db.get_users_in_chat_by_chat_id(session, chat_id,)