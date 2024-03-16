import datetime
import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session, SQLModel, StaticPool, create_engine
from typing import Optional
from backend import auth
from backend.routers import auths
from backend.main import app
from backend import database as db
from backend.schema import ChatInDB, MessageInDB, UserChatLinkInDB, UserInDB
from passlib.context import CryptContext


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

@pytest.fixture
def session():
    engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        yield session


@pytest.fixture
def client(session):
    def _get_session_override():
        return session

    app.dependency_overrides[db.get_session] = _get_session_override

    yield TestClient(app)

    app.dependency_overrides.clear()

@pytest.fixture
def default_data(session):

    chat1 = ChatInDB(
            id = 1,
            name="Chat 1",
            owner_id = 1,
            created_at = datetime.date.fromisoformat("2021-05-07")
        )

    user1 = UserInDB(
        id=1,
        username= "danbis",
        email="danbis@gmail.com",
        hashed_password=pwd_context.hash('123'),
        created_at = datetime.date.fromisoformat("2021-05-05")
    )
    
    user2 = UserInDB(
        id=2,
        username= "sarah",
        email="dannith@gmail.com",
        hashed_password=pwd_context.hash('sarahpassword'),
        created_at = datetime.date.fromisoformat("2021-05-05")
    )

    message1 = MessageInDB(
        id=1,
        text="hello world!",
        user_id=1,
        chat_id=1,
        created_at = datetime.date.fromisoformat("2021-05-06")
    )

    user_chat_link1 = UserChatLinkInDB(user_id=1, chat_id=chat1.id)
    user_chat_link2 = UserChatLinkInDB(user_id=2, chat_id=chat1.id)
    user_chat_link3 = UserChatLinkInDB(user_id=3, chat_id=chat1.id)
    
    # Add created entities to session
    session.add_all([user1, user2, chat1, user_chat_link1, user_chat_link2, user_chat_link3, message1])
    session.commit()
    
    # Return created entities
    return {
        "users": [user1, user2],
        "chats": [chat1],
        "user_chat_links": [user_chat_link1, user_chat_link2, user_chat_link3],
        "messages": [message1]
    }

# @pytest.fixture
# def default_users(session, default_chats):
#     return [
#         UserInDB(
#             id=1,
#             username="Danny",
#             email="email1@gmail.com",
#             hashed_password="fjdkslafdas",
#             created_at=datetime.date.fromisoformat("2021-05-05"),
#             chats = default_chats.copy()
#         ),
#         UserInDB(
#             id=2,
#             username="Ian",
#             email="email2@gmail.com",
#             hashed_password="fjdkslafdas",
#             created_at=datetime.date.fromisoformat("2021-05-05"),
#             chats = default_chats.copy()
#         ),
#         UserInDB(
#             id=3,
#             username="Andy",
#             email="email3@gmail.com",
#             hashed_password="fjdkslafdas",
#             created_at=datetime.date.fromisoformat("2021-05-05"),
#             chats = default_chats.copy()
#         )
#     ]

# @pytest.fixture
# def default_chats(session):

#     chats =  [
#         ChatInDB(
#             id=1,
#             name="Dannys Chat",
#             owner_id = 1,
#             created_at = datetime.date.fromisoformat("2021-05-05"),
#         )
#     ]

#     return chats

# @pytest.fixture
# def default_link(session, default_users, default_chats):
#     chat_links = []
#     for user in default_users:
#         chat_links.append(UserChatLinkInDB(
#             user_id = user.id,
#             chat_id = default_chats[0].id
#         ))

#     session.add(chat_links)
#     session.commit()
#     session.refresh(chat_links)

#     return chat_links

