from fastapi.testclient import TestClient

from backend.main import app

client = TestClient(app)

# User Endpoint Tests
def test_get_all_users():
    response = client.get("/chats")
    assert response.status_code == 200
    assert response.json()["meta"]["count"] == 6
    curr_name = ""
    # Verify alphabetical order
    for chat in response.json()["chats"]:
        assert chat["name"] > curr_name
        curr_name = chat["name"]

def test_get_chat_id():
    response = client.get("/chats/6215e6864e884132baa01f7f972400e2")
    expected_response = {"chat": {
        "id": "6215e6864e884132baa01f7f972400e2",
        "name": "skynet",
        "user_ids": ["sarah", "terminator"],
        "owner_id":"sarah",
        "created_at":"2023-07-08T18:46:47"
    }}

    assert response.status_code == 200
    assert response.json() == expected_response

def test_get_fake_chat_id():
    response = client.get("/chats/12")
    expected_response = {
    "detail": {
        "type": "entity_not_found",
        "entity_name": "Chat",
        "entity_id": "12"
    }
}

def test_update_name():
    response = client.put("chats/6215e6864e884132baa01f7f972400e2", json={"name":"new chat name"})
    expected_response = {"chat": {
        "id": "6215e6864e884132baa01f7f972400e2",
        "name": "new chat name",
        "user_ids": ["sarah", "terminator"],
        "owner_id":"sarah",
        "created_at":"2023-07-08T18:46:47"
    }}

    assert response.json() == expected_response
    assert response.status_code == 200

def test_update_name_fake_chat():
    response = client.put("chats/12", json={"name":"new chat name"})
    expected_response = {
    "detail": {
        "type": "entity_not_found",
        "entity_name": "Chat",
        "entity_id": "12"
    }
}

    assert response.status_code == 404
    assert response.json() == expected_response


def test_list_of_messages_given_id():
    response = client.get("chats/6215e6864e884132baa01f7f972400e2/messages")

    assert response.status_code == 200
    assert response.json()["meta"]["count"] == 35



def test_delete_chat():
    response = client.delete("chats/6215e6864e884132baa01f7f972400e2")

    assert response.status_code == 204
    assert response.json() == None

def test_delete_fake_chat():
    response = client.delete("chats/12")
    expected_response = {
        "detail": {
            "type": "entity_not_found",
            "entity_name": "Chat",
            "entity_id": "12"
        }
    }


    assert response.status_code == 404
    assert response.json() == expected_response


def test_list_of_messages_given_id_on_deleted_chat():
    response = client.get("chats/6215e6864e884132baa01f7f972400e2/messages")
    expected_response = {
        "detail": {
            "type": "entity_not_found",
            "entity_name": "Chat",
            "entity_id": "6215e6864e884132baa01f7f972400e2"
        }
    }

    assert response.status_code == 404
    assert response.json() == expected_response

def test_get_users_in_chat_by_chat_id():
    response = client.get("chats/660c7a6bc1324e4488cafabc59529c93/users")
    expected_response = {
    "meta": {
        "count": 2,
    },
    "users": [
        {
            "id": "reese",
            "created_at": "2016-02-16T08:15:30"
        },
        {
            "id": "sarah",
            "created_at": "2006-03-02T22:30:11"
        }
    ]
}

    assert response.status_code == 200
    assert response.json() == expected_response

def test_get_users_in_chat_by_chat_id_fake_id():
    response = client.get("chats/12/users")
    expected_response = {
        "detail": {
            "type": "entity_not_found",
            "entity_name": "Chat",
            "entity_id": "12"
        }
    }

    assert response.status_code == 404
    assert response.json() == expected_response
