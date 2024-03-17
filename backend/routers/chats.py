from fastapi import APIRouter, Depends, Query
from fastapi.responses import JSONResponse
from sqlmodel import Session
from backend import database as db
from backend.routers.auths import get_current_user

chats_router = APIRouter(prefix="/chats", tags=["Chats"])

from backend.entities import *


@chats_router.get("")
def get_chats(session: Session = Depends(db.get_session)):
    """
    Get All Chats
    """
    return db.get_chats(session)

@chats_router.post("/{chat_id}/messages", status_code = 201)
def new_message_handler(
    chat_id: int,
    message: NewMessage,
    session: Session = Depends(db.get_session),
    current_user: UserInDB = Depends(get_current_user)
) -> MessageResponse:
    return db.new_message(session, chat_id, message.text, current_user.id)

@chats_router.get("/{chat_id}")
def get_chat_by_id(
    chat_id: int,
    include: list[str] = Query([]),
    session: Session = Depends(db.get_session)
):
    data = db.get_chat_by_id(session, chat_id, "messages" in include, "users" in include)

    response_data = {
        "meta": data.meta,
        "chat": data.chat
    }

    if "messages" in include and data.messages is not None:
        response_data["messages"] = data.messages

    if "users" in include and data.users is not None:
        response_data["users"] = data.users

    return response_data

@chats_router.put("/{chat_id}", response_model=ChatResponse)
def update_chat_name(chat_id:int, new_name:ChatNameUpdate, session: Session = Depends(db.get_session)):
    """
    Update Chat Name by ID
    """
    return db.update_chat_name(session, chat_id, new_name.name)


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