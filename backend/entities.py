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

class UpdateUserData(BaseModel):
    username: str = None
    email: str = None

class UserResponse(BaseModel):
    user: User

class UserCollection(BaseModel):
    """Represents an API response for a collection of users"""

    meta: Metadata
    users: list[User]

class Chat(BaseModel):
    """Represetns a chatindb object"""
    id: int
    name: str
    owner: User
    created_at: datetime

class UserChatCollection(BaseModel):
    meta: Metadata
    chats: list[Chat]


class ChatMeta(BaseModel):
    message_count: int
    user_count: int

class ChatResponse(BaseModel):
    id: int
    name: str
    owner: User
    created_at: datetime

class Message(BaseModel):
    id: int
    chat_id: int
    created_at: datetime
    text: str
    user: User


class ChatCollection(BaseModel):
    """Represents a collection of chat in db objects"""
    meta: ChatMeta
    chat: ChatResponse
    messages: Optional[list[Message]] = None
    users: Optional[list[User]] = None

class ChatNameUpdate(BaseModel):
    """Represents a chat name update"""
    name: str



class MessageCollection(BaseModel):
    """Represents a collection of messages"""
    meta: Metadata
    messages: list[Message]

