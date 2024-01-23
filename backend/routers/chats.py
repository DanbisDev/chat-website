from fastapi import APIRouter
from fastapi.responses import JSONResponse
from backend import database as db

chats_router = APIRouter(prefix="/chats", tags=["Chats"])

from backend.entities import (
    ChatNameUpdate,
    Chat,
    MessageCollection,
    UserCollection
)

@chats_router.get("")
def get_chats():
    return db.get_chats()

@chats_router.get("/{chat_id}", response_model=Chat)
def get_chat_by_id(chat_id: str):
    return db.get_chat_by_id(chat_id)

@chats_router.put("/{chat_id}", response_model=Chat)
def update_chat_name(chat_id:str, new_name:ChatNameUpdate):
    return db.update_chat_name(chat_id, new_name)

@chats_router.delete("/{chat_id}", status_code = 204)
def delete_chat_by_id(chat_id:str):
    db.delete_chat_by_id(chat_id)


@chats_router.get("/{chat_id}/messages", response_model=MessageCollection)
def get_message_col_by_chat_id(chat_id:str):
    return db.get_message_col_by_chat_id(chat_id)

@chats_router.get("/{chat_id}/users", response_model=UserCollection)
def get_users_in_chat_by_chat_id(chat_id:str):
    return db.get_users_in_chat_by_chat_id(chat_id)