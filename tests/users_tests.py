from fastapi.testclient import TestClient

from backend.main import app

client = TestClient(app)


# User Endpoint Tests
def test_get_all_users():
    response = client.get("/users")
    assert response.status_code == 200

def test_create_user():
    create_params = {
        "id" : "Danny"
    } 

    response = client.post("/users", json=create_params)
    assert response.status_code == 200

def test_create_user_v():
    create_params = {
        "id" : "Danny2"
    } 

    response = client.post("/users", json=create_params)
    assert response.status_code == 200
    assert response.json()["user"]["id"] == "Danny2"

def test_create_duplicate_user():
    response = client.post("/users", json={"id":"danny"})
    response = client.post("/users", json={"id":"danny"})
    expected_response = {
        "detail": {
            "type": "duplicate_entity",
            "entity_name": "User",
            "entity_id": "danny"
        }
    }
    assert response.status_code == 422
    assert response.json() == expected_response


def test_get_user():
    response = client.get("/users/bishop")
    assert response.status_code == 200

def test_get_user_response_v():
    response = client.get("/users/bishop")
    expected_response = {
        "user": {
            "id":"bishop",
            "created_at":"2014-04-14T10:49:07"
        }
    }
    assert response.status_code == 200
    assert response.json() == expected_response

def test_get_not_found_user():
    response = client.get("/users/doesntexist")
    expected_response = {
        "detail": 
        {
            "type": "entity_not_found",
            "entity_name": "User",
            "entity_id": "doesntexist"
        }
    }

    assert response.status_code == 404
    assert response.json() == expected_response

def test_get_user_chats():
    response = client.get("/users/bishop/chats")
    expected_response = {
        "meta": {
            "count": 1
        },
        "chats": [
            {
                "id": "734eeb9ddaec43b2ab6e289a0d472376",
                "name": "nostromo",
                "user_ids": ["bishop", "burke", "ripley"],
                "owner_id": "ripley",
                "created_at": "2023-09-18T14:18:46"
            }
        ]
    }
    assert response.status_code == 200
    assert response.json() == expected_response

