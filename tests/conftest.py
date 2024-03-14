import datetime
import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session, SQLModel, StaticPool, create_engine

from backend.main import app
from backend import database as db
from backend.schema import ChatInDB, UserInDB


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
def default_users():
    return [
        UserInDB(
            id=1,
            username="Danny",
            email="email1@gmail.com",
            hashed_password="fjdkslafdas",
            created_at=datetime.date.fromisoformat("2021-05-05")
        ),
        UserInDB(
            id=2,
            username="Ian",
            email="email2@gmail.com",
            hashed_password="fjdkslafdas",
            created_at=datetime.date.fromisoformat("2021-05-05")
        ),
        UserInDB(
            id=3,
            username="Andy",
            email="email3@gmail.com",
            hashed_password="fjdkslafdas",
            created_at=datetime.date.fromisoformat("2021-05-05")
        )
    ]

