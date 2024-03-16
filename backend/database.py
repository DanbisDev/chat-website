from datetime import datetime
from uuid import uuid4
from sqlmodel import Session, SQLModel, create_engine, select
from backend.schema import UserInDB, ChatInDB, MessageInDB, UserChatLinkInDB

from backend.entities import *


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

def get_all_users(session: Session) -> UserCollection:
    """
    Retrieve all users from the database

    :return: ordered list of all users
    """
    users_in_db = session.exec(select(UserInDB)).all()

    users = []
    for user_ndb in users_in_db:
        users.append(User(
            id = user_ndb.id,
            username = user_ndb.username,
            email = user_ndb.email,
            created_at = user_ndb.created_at
        ))

    return UserCollection(
        meta = Metadata(count = len(users)),
        users = users
    )

def create_user(session: Session, user_to_add: UserCreate) -> UserInDB:
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
        user = UserInDB(**user_to_add.model_dump())
        
        session.add(user)
        session.commit()
        session.refresh(user)
        return User(id=user.id, username=user.username, email=user.email, created_at=user.created_at)

def get_user(session: Session, user_id) -> UserResponse:
    """
    Grabs a user in the database.
    
    :param user_id: user id to grab
    :return: the user specified
    :raises EntityNotFoundException: if the user doesn't exist in the DB
    """
    user = session.get(UserInDB, user_id)
    if user:
        return UserResponse(user=User(**user.model_dump()))
    else:
        raise EntityNotFoundException(entity_name="User", entity_id=user_id)

    
def get_user_chats(session: Session, user_id) -> UserChatCollection:
    """
    Grabs a list of all chats a user is in
    
    :param user_id: user id to grab
    :return: A ChatCollection of chats the user is in
    :raises EntityNotFoundException: if the user doesn't exist in the DB
    """


    user = session.get(UserInDB, user_id)
    if user:
        chats = []
        for chat in user.chats:
            owner_userindb = session.get(UserInDB, chat.owner.id)
            chats.append(Chat(id=chat.id,
                              name=chat.name, 
                              owner = User(
                                  id=owner_userindb.id,
                                  username=owner_userindb.username,
                                  email=owner_userindb.email,
                                  created_at=owner_userindb.created_at
                              ), 
                              created_at=str(chat.created_at)))

        return UserChatCollection(
            meta=Metadata(count = len (user.chats)),
            chats=chats
        )
        
    else:
        raise EntityNotFoundException(entity_name="UserInDB", entity_id=user_id)

def get_user_by_username(session: Session, username) -> UserInDB:
    """
    Grabs a userindb based on the username passed in
    """
    statement = select(UserInDB).where(
        UserInDB.username == username
    )

    return session.exec(statement).first()

def get_user_by_email(session: Session, email) -> UserInDB:
    """
    Grabs a userindb based on the email passed in
    """
    statement = select(UserInDB).where(
        UserInDB.email == email
    )

    return session.exec(statement).first()

def get_chats(session: Session) -> ChatCollection:
    """
    Grabs all chats in the database
    
    :return: A ChatCollection of all chats in teh DB
    """
    chatsindb = session.exec(select(ChatInDB)).all()
    chats = []
    for chat in chatsindb:
        owner_userindb = session.get(UserInDB, chat.owner.id)
        chats.append(Chat(
            id=chat.id,
            name=chat.name,
            owner = User(
                id=owner_userindb.id,
                username=owner_userindb.username,
                email=owner_userindb.email,
                created_at=owner_userindb.created_at
            ), 
            created_at=chat.created_at
        ))


    return ChatCollection(
        meta=Metadata(
            count = len(chats)
        ),
        chats=chats
    )

def get_chat_by_id(session: Session, chat_id) -> ChatCollection:
    """
    Grabs a chat from the DB with the given chat_id
    
    :param chat_id: chat id to grab
    :return: A Chat with the given id
    :raises EntityNotFoundException: if the chat doesn't exist in the DB
    """
    chat = session.get(ChatInDB, chat_id)
    if chat:
        chat_meta = ChatMeta(
            message_count = len(chat.messages),
            user_count = len(chat.users)
        )
        chat_response = ChatResponse(
            id = chat.id,
            name = chat.name,
            owner = User(**chat.owner.model_dump()),
            created_at = chat.created_at
        )
        message_list = []
        for message in chat.messages:
            message_list.append(Message(
                user = User(**message.user.model_dump()),
                **message.model_dump()
                ))
            
        user_list = []
        for user in chat.users:
            user_list.append(User(**user.model_dump()))
        
        return ChatCollection(
            meta=chat_meta,
            chat = chat_response,
            messages = message_list,
            users = user_list
        )
    else:
        raise EntityNotFoundException(entity_name="Chat", entity_id=chat_id)


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

def  get_message_col_by_chat_id(session: Session, chat_id:str) -> MessageCollection:
    """
    Gets a collection of messages given from a single chat with the provided
    chat id
    
    :param chat_id: the chat id to grab messages from
    :returns: a MessageCollection of all messages in the given chat
    """
    messages = session.exec(select(MessageInDB).where(MessageInDB.chat_id == chat_id)).all()
    m_list = []
    for message in messages:
        m_list.append(Message(
            id = message.id,
            text = message.text,
            chat_id = message.chat_id,
            user = get_user(session, message.user.id).user,
            created_at = message.created_at
        ))
    
    return MessageCollection(
        meta = Metadata(count = len(m_list)),
        messages = m_list
    )

def get_users_in_chat_by_chat_id(session: Session,chat_id:str) -> UserCollection:
    """
    Gets a collection of users who are participating in a given chat
    found by the provided chat id
    
    :param chat_id: the chat id to grab users from
    :returns: a UserCollection of all users in the given chat
    """
    chat = session.get(ChatInDB, chat_id)

    users = []
    for user in chat.users:
        users.append(User(
            id = user.id,
            username = user.username,
            email = user.email,
            created_at = user.created_at
        ))
    
    return UserCollection(
        meta = Metadata(
            count = len(users)
        ),
        users = users
    )


class EntityNotFoundException(Exception):
    def __init__(self, *, entity_name: str, entity_id: str):
        self.entity_name = entity_name
        self.entity_id = entity_id

class EntityAlreadyExistsException(Exception):
    def __init__(self, *, entity_name: str, entity_id: str):
        self.entity_name = entity_name
        self.entity_id = entity_id
