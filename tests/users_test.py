from datetime import datetime
from fastapi.testclient import TestClient
import jwt

from backend.main import app

client = TestClient(app)


# User Endpoint Tests
def test_get_all_users(client, default_data):
    response = client.get("/users")
    assert response.status_code == 200

def test_create_user(client):
    create_params = {
        "username": "Danbis",
        "email": "danbis@gmail.com",
        "password": "123"
    } 

    response = client.post("/auth/registration", json=create_params)
    expected_response = {
        "user": {
            "id": 1,
            "username": "Danbis",
            "email": "danbis@gmail.com",
            "created_at": response.json()['user']['created_at']
        }
    }
    assert response.json() == expected_response
    assert response.status_code == 201


def test_create_duplicate_username(client):
    create_params = {
        "username": "Danbis",
        "email": "danbis@gmail.com",
        "password": "123"
    } 

    response_safe = client.post("/auth/registration", json=create_params)

    create_params = {
        "username": "Danbis",
        "email": "danbis2@gmail.com",
        "password": "123"
    } 

    response_dupe = client.post("/auth/registration", json=create_params)

    assert response_safe.status_code == 201
    expected_response = {
        "detail": {
            "type": "duplicate_value",
            "entity_name": "User",
            "entity_field": "username",
            "entity_value": "Danbis"
        }
    }
    assert response_dupe.status_code == 422
    assert response_dupe.json() == expected_response

def test_create_duplicate_email(client):
    create_params = {
        "username": "Danbis",
        "email": "danbis@gmail.com",
        "password": "123"
    } 

    response_safe = client.post("/auth/registration", json=create_params)

    create_params = {
        "username": "Danbis2",
        "email": "danbis@gmail.com",
        "password": "123"
    } 

    response_dupe = client.post("/auth/registration", json=create_params)

    assert response_safe.status_code == 201
    expected_response = {
        "detail": {
            "type": "duplicate_value",
            "entity_name": "User",
            "entity_field": "email",
            "entity_value": "danbis@gmail.com"
        }
    }
    assert response_dupe.status_code == 422
    assert response_dupe.json() == expected_response


def test_get_user(client):
    create_params = {
        "username": "Danbis",
        "email": "danbis@gmail.com",
        "password": "123"
    } 

    response = client.post("/auth/registration", json=create_params)

    response = client.get("/users/1")
    assert response.status_code == 200

def test_get_user_response_v(client):
    create_params = {
        "username": "Danbis",
        "email": "danbis@gmail.com",
        "password": "123"
    } 

    response = client.post("/auth/registration", json=create_params)

    response = client.get("/users/1")
    expected_response = {
        "user": {
            "id": 1,
            "username": "Danbis",
            "email": "danbis@gmail.com",
            "created_at": response.json()['user']['created_at']
        }
    }
    assert response.status_code == 200
    assert response.json() == expected_response

def test_get_user_chats(client, default_data):
    
    
    response = client.get("/users/1/chats")

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

def test_get_token_invalid_user(client, default_data):
    """POST /auth/token"""
    auth_data = {
        "username": "danbis",
        "password": "1234",
    }

    expected_response = {
        "detail": {
            "error": "invalid_client",
            "error_description": "invalid username or password"
        }
    }

    response = client.post("/auth/token", data=auth_data)
    assert response.json() == expected_response
    assert response.status_code == 422

def test_get_token_user(client, default_data):
    auth_data = {
        "username": "danbis",
        "password": "123",
    }
    response = client.post("/auth/token", data=auth_data)

    assert response.status_code == 200
    assert "access_token" in response.json()
    assert response.json()["token_type"] == "Bearer"
    assert response.json()["expires_in"] == 3600


def test_get_user_self(client, default_data):
    """GET /users/me"""
    auth_data = {
        "username": "danbis",
        "password": "123",
    }
    response = client.post("/auth/token", data=auth_data)
    assert response.status_code == 200
    token = response.json()["access_token"]

    response = client.get("/users/me", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200

def test_update_own_username(client, default_data):
    """PUT /users/me"""
    auth_data = {
        "username": "sarah",
        "password": "sarahpassword",
    }
    response = client.post("/auth/token", data=auth_data)
    assert response.status_code == 200
    token = response.json()["access_token"]

    response = client.put(
        "/users/me",
        headers={"Authorization": f"Bearer {token}"},
        json={"username": "sarah_updated"},
    )
    assert response.status_code == 200

def test_update_own_username_bad_token(client, default_data):
    """PUT /users/me"""
    auth_data = {
        "username": "sarah",
        "password": "sarahpassword",
    }

    response = client.put(
        "/users/me",
        headers={"Authorization": f"Bearer token"},
        json={"username": "sarah_updated"},
    )
    assert response.status_code == 401
