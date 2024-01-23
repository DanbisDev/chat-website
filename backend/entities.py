from pydantic import BaseModel, Field
from datetime import date, datetime

class Metadata(BaseModel):
    """Represents metadata for a collection"""
    count: int

class UserInDB(BaseModel):
    """Represents a user in the database"""

    id: str
    created_at: datetime

class UserCreate(BaseModel):
    """Represents parameters for adding a new user to the database"""
    id: str

class User(BaseModel):
    """Represents an API response for a user"""
    user: UserInDB

class UserCollection(BaseModel):
    """Represents an API response for a collection of users"""

    meta: Metadata
    users: list[UserInDB]


class ChatInDB(BaseModel):
    """Represents a single chat channel in the database"""
    id: str
    name: str
    user_ids: list[str]
    owner_id: str
    created_at: datetime

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

