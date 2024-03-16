import datetime
from fastapi.testclient import TestClient

import pytest

from datetime import date
from backend.main import app
from backend.schema import ChatInDB, UserInDB

client = TestClient(app)


def test_get_skynet_chat(client, default_data):
    """GET /chats/1"""
    response = client.get("/chats/1")

    assert response.status_code == 200
    assert "messages" in response.json() 
    assert "chat" in response.json() 
    assert "users" in response.json() 
    assert "meta" in response.json()