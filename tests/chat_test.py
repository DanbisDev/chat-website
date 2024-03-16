import datetime
from fastapi.testclient import TestClient

import pytest

from datetime import date
from backend.main import app
from backend.schema import ChatInDB, UserInDB

client = TestClient(app)

def test_get_chats(client, default_data):
    
    
    response = client.get("/chats")

    expected_response = {
        "meta": {
            "count": 1
        },
        "chats": [
            {
                "id": 1,
                "name": "Chat 1",
                "owner": {
                    "id": 1,
                    "username": "danbis",
                    "email": "danbis@gmail.com",
                    "created_at": "2021-05-05T00:00:00"
                },
                "created_at": "2021-05-07T00:00:00"
            }
        ]
    }


    assert response.status_code == 200
    assert response.json() == expected_response

def test_get_messages(client, default_data):
    response = client.get("/chats/1/messages")

    expected_response = {
        "meta": {
            "count": 1
        },
        "messages": [
            {
            "id": 1,
            "text": "hello world!",
            "chat_id": 1,
            "user": {
                "id": 1,
                "username": "danbis",
                "email": "danbis@gmail.com",
                "created_at": "2021-05-05T00:00:00"
            },
            "created_at": "2021-05-06T00:00:00"
            }
        ]
    }

    assert response.status_code == 200
    assert response.json() == expected_response


def test_get_chat_users(client, default_data):
    response = client.get("/chats/1/users")

    expected_response = {
        "meta": {
            "count": 2
        },
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

    assert response.status_code == 200
    assert response.json() == expected_response

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
    