from pydantic import BaseModel, Field
from datetime import date, datetime
from backend.schema import *

class Metadata(BaseModel):
    """Represents metadata for a collection"""
    count: int

class UserCreate(BaseModel):
    """Represents parameters for adding a new user to the database"""
    id: int
    username: str
    email: str
    hashed_password: str

class User(BaseModel):
    """Represents an API response for a user"""
    id: int
    username: str
    email: str
    created_at: datetime

class UserResponse(BaseModel):
    user: User

class UserCollection(BaseModel):
    """Represents an API response for a collection of users"""

    meta: Metadata
    users: list[UserInDB]

class Chat(BaseModel):
    """Represetns a chatindb object"""
    chat: ChatInDB


class ChatCollection(BaseModel):
    """Represents a collection of chat in db objects"""
    meta: Metadata
    chats: list[ChatInDB]

class ChatNameUpdate(BaseModel):
    """Represents a chat name update"""
    name: str

class Message(BaseModel):
    id: str
    user_id: str
    text: str
    created_at: datetime

class MessageCollection(BaseModel):
    """Represents a collection of messages"""
    meta: Metadata
    messages: list[Message]

