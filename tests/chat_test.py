import datetime
from fastapi.testclient import TestClient

import pytest

from datetime import date
from backend.main import app
from backend.schema import ChatInDB, UserInDB

client = TestClient(app)


def test_get_skynet_chat(client, default_data):
    """GET /chats/1"""
    response = client.get("/chats/1?include=users&include=messages")

    assert response.status_code == 200
    assert "messages" in response.json() 
    assert "chat" in response.json() 
    assert "users" in response.json() 
    assert "meta" in response.json()

    expected_response = {
    "meta": {
        "message_count": 2,
        "user_count": 2
    },
    "chat": {
        "id": 1,
        "name": "Chat 1",
        "owner": {
            "id": 1,
            "username": "danbis",
            "email": "danbis@gmail.com",
            "created_at": "2021-05-05T00:00:00"
        },
        "created_at": "2021-05-07T00:00:00"
    },
    "messages": [
        {
        "chat_id": 1,
        "created_at": "2021-05-06T00:00:00",
        "id": 1,
        "text": "hello world!",
        "user": {
            "id": 1,
            "username": "danbis",
            "email": "danbis@gmail.com",
            "created_at": "2021-05-05T00:00:00"
        },
        },
        {
        "chat_id": 1,
        "created_at": "2021-05-06T00:00:00",
        "id": 2,
        "text": "Lame",
        "user": {
            "id": 2,
            "username": "sarah",
            "email": "dannith@gmail.com",
            "created_at": "2021-05-05T00:00:00"
        },
        }
    ],
    "users": [
        {
            "id": 1,
            "username": "danbis",
            "email": "danbis@gmail.com",
            "created_at": "2021-05-05T00:00:00"
        },
        {
            "id": 2,
            "username": "sarah",
            "email": "dannith@gmail.com",
            "created_at": "2021-05-05T00:00:00"
        }
    ]
    }

    assert response.json() == expected_response