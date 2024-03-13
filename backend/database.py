from datetime import datetime
from uuid import uuid4
from sqlmodel import Session, SQLModel, create_engine

from schema import *


engine = create_engine(
    "sqlite:///backend/pony_express.db",
    echo=True,
    connect_args={"check_same_thread": False}
)

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session

def get_all_users(session: Session) -> list[UserInDB]:
    """
    Retrieve all users from the database

    :return: ordered list of all users
    """
    return session.get(UserInDB)

def create_user(session: Session, user_to_add: UserInDB) -> UserInDB:
    """
    Create a new user in the database.
    
    :param user_create: attributes of the user to be created
    :return: the newly created user
    :raises EntityAlreadyExistsException: if the user id already exists in the DB
    """

    user = session.get(UserInDB, user_to_add.id)
    if user:
        raise EntityAlreadyExistsException(entity_name="UserInDB", entity_id=user_to_add.id)
    else:
        session.add(user_to_add)
        session.commit()
        return user_to_add

def get_user(session: Session, user_id) -> UserInDB:
    """
    Grabs a user in the database.
    
    :param user_id: user id to grab
    :return: the user specified
    :raises EntityNotFoundException: if the user doesn't exist in the DB
    """
    user = session.get(UserInDB, user_id)
    if user:
        return user
    else:
        raise EntityNotFoundException(entity_name="UserInDB", entity_id=user_id)

    
def get_user_chats(session: Session, user_id) -> list[ChatInDB]:
    """
    Grabs a list of all chats a user is in
    
    :param user_id: user id to grab
    :return: A ChatCollection of chats the user is in
    :raises EntityNotFoundException: if the user doesn't exist in the DB
    """


    user = session.get(UserInDB, user_id)
    if user:
        return user.chats
    else:
        raise EntityNotFoundException(entity_name="UserInDB", entity_id=user_id)

def get_chats(session: Session) -> list[ChatInDB]:
    """
    Grabs all chats in the database
    
    :return: A ChatCollection of all chats in teh DB
    """
    return session.get(ChatInDB)

def get_chat_by_id(session: Session, chat_id) -> ChatInDB:
    """
    Grabs a chat from the DB with the given chat_id
    
    :param chat_id: chat id to grab
    :return: A Chat with the given id
    :raises EntityNotFoundException: if the chat doesn't exist in the DB
    """
    chat = session.get(ChatInDB, chat_id)
    if chat:
        return chat
    else:
        raise EntityNotFoundException(entity_name="ChatInDB", entity_id=chat_id)

def update_chat_name(session: Session,chat_id:str, new_name:str) -> ChatInDB:
    """
    Updates the given chat id with the given new name
    
    :param chat_id: the chat id to grab
    :param new_name: the new name the chat should have
    :returns: A chat object with the updated name
    :raises EntityNotFoundException: if the chat doesn't exist in the DataBase
    """
    chat = session.get(ChatInDB, chat_id)

    if chat is None:
        raise EntityNotFoundException(entity_name="ChatInDB", entity_id=chat_id)

    chat.name = new_name

    session.commit()

    return chat
    
def delete_chat_by_id(session: Session, chat_id:str):
    """
    Deletes a chat from the database with the given chat id
    
    :param chat_id: the chat id to delete
    :returns: default empty json response with status code 204
    """
    chat = session.get(ChatInDB, chat_id)

    if chat is None:
        raise EntityNotFoundException(entity_name="Chat", entity_id=chat_id)
    
    session.delete(chat)
    session.commit()

def  get_message_col_by_chat_id(session: Session, chat_id:str) -> list[MessageInDB]:
    """
    Gets a collection of messages given from a single chat with the provided
    chat id
    
    :param chat_id: the chat id to grab messages from
    :returns: a MessageCollection of all messages in the given chat
    """
    messages = session.get(MessageInDB).filter(MessageInDB.chat_id == chat_id).all()

    if messages is None:
        raise EntityNotFoundException(entity_name="MessageInDB", entity_id=chat_id)
    else:
        return messages

def get_users_in_chat_by_chat_id(session: Session,chat_id:str) -> list[UserInDB]:
    """
    Gets a collection of users who are participating in a given chat
    found by the provided chat id
    
    :param chat_id: the chat id to grab users from
    :returns: a UserCollection of all users in the given chat
    """
    users_chat_links = session.get(UserChatLinkInDB).filter(UserChatLinkInDB.chat_id == chat_id).all()

    user_ids = [link.user_id for link in users_chat_links]

    users = session.query(UserInDB).filter(UserInDB.id.in_(user_ids)).all()

    return users

class EntityNotFoundException(Exception):
    def __init__(self, *, entity_name: str, entity_id: str):
        self.entity_name = entity_name
        self.entity_id = entity_id

class EntityAlreadyExistsException(Exception):
    def __init__(self, *, entity_name: str, entity_id: str):
        self.entity_name = entity_name
        self.entity_id = entity_id
