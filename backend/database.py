import json
from datetime import date
from uuid import uuid4


from backend.entities import (
    UserInDB,
    UserCreate,
    User,
    UserCollection,
    ChatCollection,
    ChatInDB,
    Chat,
    ChatNameUpdate,
    Message,
    MessageCollection,
    Metadata
)

with open("backend/fake_db.json", "r") as f:
    DB = json.load(f)

def get_all_users() -> list[UserInDB]:
    """
    Retrieve all users from the database

    :return: ordered list of all users
    """
    return [UserInDB(**user_data) for user_data in DB["users"].values()]

def create_user(user_create: UserCreate) -> User:
    """
    Create a new user in the database.
    
    :param user_create: attributes of the user to be created
    :return: the newly created user
    :raises EntityAlreadyExistsException: if the user id already exists in the DB
    """
    user = UserInDB(
        created_at = date.today(),
        **user_create.model_dump()
    )

    if user.id in DB["users"]:
        raise EntityAlreadyExistsException(entity_name="User", entity_id=user.id)
    else:     
        DB["users"][user.id] = user.model_dump()
        return User(user=user)

def get_user(user_id) -> User:
    """
    Grabs a user in the database.
    
    :param user_id: user id to grab
    :return: the user specified
    :raises EntityNotFoundException: if the user doesn't exist in the DB
    """
    if user_id in DB["users"]:
        return User(user = UserInDB(**DB["users"][user_id]))
    else:
        raise EntityNotFoundException(entity_name="User", entity_id=user_id)
    
def get_user_chats(user_id) -> ChatCollection:
    """
    Grabs a list of all chats a user is in
    
    :param user_id: user id to grab
    :return: A ChatCollection of chats the user is in
    :raises EntityNotFoundException: if the user doesn't exist in the DB
    """
    if user_id not in DB["users"]:
        raise EntityNotFoundException(entity_name="User", entity_id=user_id)
    
    chats = []
    for chat in DB["chats"]:
        if user_id in DB["chats"][chat]["user_ids"] and chat not in chats:
            chats.append(DB["chats"][chat])

    return ChatCollection(meta=Metadata(count=len(chats)), chats=sorted(chats, key=lambda x: x['name']))

def get_chats() -> ChatCollection:
    """
    Grabs all chats in the database
    
    :return: A ChatCollection of all chats in teh DB
    """
    chats = []
    for chat in DB["chats"]:
        chats.append(DB["chats"][chat])
    
    return ChatCollection(meta=Metadata(count=len(chats)), chats=sorted(chats, key=lambda x: x['name']))

def get_chat_by_id(chat_id) -> Chat:
    """
    Grabs a chat from the DB with the given chat_id
    
    :param chat_id: chat id to grab
    :return: A Chat with the given id
    :raises EntityNotFoundException: if the chat doesn't exist in the DB
    """
    if chat_id in DB["chats"]:
        chat = DB["chats"][chat_id]
        return Chat(chat=ChatInDB(
            id=chat_id,
            name=chat["name"],
            user_ids=chat["user_ids"],
            owner_id=chat["owner_id"],
            created_at=chat["created_at"]
        ))
    else:
        raise EntityNotFoundException(entity_name="Chat", entity_id=chat_id)

def update_chat_name(chat_id:str, new_name:ChatNameUpdate) -> Chat:
    """
    Updates the given chat id with the given new name
    
    :param chat_id: the chat id to grab
    :param new_name: the new name the chat should have
    :returns: A chat object with the updated name
    :raises EntityNotFoundException: if the chat doesn't exist in the DataBase
    """
    chat = get_chat_by_id(chat_id)
    chat.chat.name = new_name.name
    DB["chats"][chat_id]["name"] = new_name.name
    return chat
    
def delete_chat_by_id(chat_id:str):
    """
    Deletes a chat from the database with the given chat id
    
    :param chat_id: the chat id to delete
    :returns: default empty json response with status code 204
    """
    if chat_id in DB["chats"]:
        del DB["chats"][chat_id]
    else:
        raise EntityNotFoundException(entity_name="Chat", entity_id=chat_id)

def get_message_col_by_chat_id(chat_id:str) -> MessageCollection:
    """
    Gets a collection of messages given from a single chat with the provided
    chat id
    
    :param chat_id: the chat id to grab messages from
    :returns: a MessageCollection of all messages in the given chat
    """
    messages = []
    if chat_id in DB["chats"]:
        for message in DB["chats"][chat_id]["messages"]:
            messages.append(Message(
                id = message["id"],
                user_id = message["user_id"],
                text = message["text"],
                created_at= message["created_at"]
            ))
        return MessageCollection(meta = Metadata(count=len(messages)), messages=messages)
    else:
        raise EntityNotFoundException(entity_name="Chat", entity_id=chat_id)

def get_users_in_chat_by_chat_id(chat_id:str) -> UserCollection:
    """
    Gets a collection of users who are participating in a given chat
    found by the provided chat id
    
    :param chat_id: the chat id to grab users from
    :returns: a UserCollection of all users in the given chat
    """
    users = []
    if chat_id in DB["chats"]:
        for user in DB["chats"][chat_id]["user_ids"]:
            users.append(UserInDB(
                id=user,
                created_at = DB["users"][user]["created_at"]
            ))
        sorted_users = chats=sorted(users, key=lambda x: x.id)
        return UserCollection(meta=Metadata(count=len(sorted_users)), users=sorted_users)
    else:
        raise EntityNotFoundException(entity_name="Chat", entity_id=chat_id) 

class EntityNotFoundException(Exception):
    def __init__(self, *, entity_name: str, entity_id: str):
        self.entity_name = entity_name
        self.entity_id = entity_id

class EntityAlreadyExistsException(Exception):
    def __init__(self, *, entity_name: str, entity_id: str):
        self.entity_name = entity_name
        self.entity_id = entity_id
