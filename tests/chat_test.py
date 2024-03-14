import datetime
from fastapi.testclient import TestClient

import pytest

from datetime import date
from backend.main import app
from backend.schema import ChatInDB, UserInDB

client = TestClient(app)

@pytest.fixture
def default_chats():
    return [
        ChatInDB(
            id=1,
            name="Dannys Chat",
            owner_id=1,
            created_at=datetime.date.fromisoformat("2021-05-07"),
            owner=UserInDB(
                id=1,
                username="Danny",
                email="email1@gmail.com",
                hashed_password="fjdkslafdas",
                created_at=datetime.date.fromisoformat("2021-05-05")
            ),
            users=[
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
            ],
            messages=[]
        )
    ]


def test_create_user(client):
    create_params = {
        "id" : 123,
        "username": "Danny",
        "email": "deckergame.danny@gmail.com",
        "hashed_password": "fjdklsajtgeklsafdsa"
    } 

    response = client.post("/users", json=create_params)
    expected_response = {
        "id": 123,
        "username": "Danny",
        "email": "deckergame.danny@gmail.com",
        "created_at": response.json()['created_at']
    }
    assert response.json() == expected_response
    assert response.status_code == 200

# User Endpoint Tests
def test_get_all_users(client):
    response = client.get("/users")
    assert response.status_code == 200

# def test_get_chat_id(client, default_chats):

#     default_chats()

#     response = client.get("/chats/1")
#     expected_response = {
#         "chat": {
#             "id": 1,
#             "name": "chat name",
#             "owner": {
#                 "id": 1,
#                 "username": "juniper",
#                 "email": "juniper@cool.email",
#                 "created_at": "2023-10-31T18:33:09"
#             },
#             "created_at": "2023-11-22T10:41:23"
#         },
#     }

#     assert response.status_code == 200
#     assert response.json() == expected_response

# def test_get_fake_chat_id(client):
#     response = client.get("/chats/12")
#     expected_response = {
#     "detail": {
#         "type": "entity_not_found",
#         "entity_name": "Chat",
#         "entity_id": "12"
#     }
# }

# def test_update_name(client):
#     response = client.put("chats/6215e6864e884132baa01f7f972400e2", json={"name":"new chat name"})
#     expected_response = {"chat": {
#         "id": "6215e6864e884132baa01f7f972400e2",
#         "name": "new chat name",
#         "user_ids": ["sarah", "terminator"],
#         "owner_id":"sarah",
#         "created_at":"2023-07-08T18:46:47"
#     }}

#     assert response.json() == expected_response
#     assert response.status_code == 200


# def test_check_name_updated(client):
#     client = TestClient(app)
#     response = client.get("/chats/6215e6864e884132baa01f7f972400e2")
#     expected_response = {"chat": {
#         "id": "6215e6864e884132baa01f7f972400e2",
#         "name": "new chat name",
#         "user_ids": ["sarah", "terminator"],
#         "owner_id":"sarah",
#         "created_at":"2023-07-08T18:46:47"
#     }}

#     assert response.status_code == 200
#     assert response.json() == expected_response

# def test_update_name_fake_chat(client):
#     response = client.put("chats/12", json={"name":"new chat name"})
#     expected_response = {
#     "detail": {
#         "type": "entity_not_found",
#         "entity_name": "Chat",
#         "entity_id": "12"
#     }
# }

#     assert response.status_code == 404
#     assert response.json() == expected_response


# def test_list_of_messages_given_id(client):
#     response = client.get("chats/6215e6864e884132baa01f7f972400e2/messages")

#     assert response.status_code == 200
#     assert response.json()["meta"]["count"] == 35



# def test_delete_chat(client):
#     response = client.delete("chats/6215e6864e884132baa01f7f972400e2")

#     assert response.status_code == 204
#     assert response.content == b""

#     response = client.get("chats/6215e6864e884132baa01f7f972400e2")

#     assert response.status_code == 404

# def test_delete_fake_chat(client):
#     response = client.delete("chats/12")
#     expected_response = {
#         "detail": {
#             "type": "entity_not_found",
#             "entity_name": "Chat",
#             "entity_id": "12"
#         }
#     }


#     assert response.status_code == 404
#     assert response.json() == expected_response


# def test_list_of_messages_given_id_on_deleted_chat(client):
#     response = client.get("chats/6215e6864e884132baa01f7f972400e2/messages")
#     expected_response = {
#         "detail": {
#             "type": "entity_not_found",
#             "entity_name": "Chat",
#             "entity_id": "6215e6864e884132baa01f7f972400e2"
#         }
#     }

#     assert response.status_code == 404
#     assert response.json() == expected_response

# def test_get_users_in_chat_by_chat_id(client):
#     response = client.get("chats/660c7a6bc1324e4488cafabc59529c93/users")
#     expected_response = {
#     "meta": {
#         "count": 2,
#     },
#     "users": [
#         {
#             "id": "reese",
#             "created_at": "2016-02-16T08:15:30"
#         },
#         {
#             "id": "sarah",
#             "created_at": "2006-03-02T22:30:11"
#         }
#     ]
# }

#     assert response.status_code == 200
#     assert response.json() == expected_response

# def test_get_users_in_chat_by_chat_id_fake_id(client):
#     response = client.get("chats/12/users")
#     expected_response = {
#         "detail": {
#             "type": "entity_not_found",
#             "entity_name": "Chat",
#             "entity_id": "12"
#         }
#     }

#     assert response.status_code == 404
#     assert response.json() == expected_response
    