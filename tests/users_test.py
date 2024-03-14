from datetime import datetime
from fastapi.testclient import TestClient

from backend.main import app

client = TestClient(app)


# User Endpoint Tests
def test_get_all_users(client):
    response = client.get("/users")
    assert response.status_code == 200

def test_create_user(client):
    create_params = {
        "id" : 11,
        "username": "Danny",
        "email": "deckergame.danny@gmail.com",
        "hashed_password": "fjdklsajtgeklsafdsa"
    } 

    response = client.post("/users", json=create_params)
    expected_response = {
        "id": 11,
        "username": "Danny",
        "email": "deckergame.danny@gmail.com",
        "created_at": response.json()['created_at']
    }
    assert response.json() == expected_response
    assert response.status_code == 200


def test_create_duplicate_user(client):
    create_params = {
        "id" : 123,
        "username": "Danny",
        "email": "deckergame.danny@gmail.com",
        "hashed_password": "fjdklsajtgeklsafdsa"
    } 
    response1 = client.post("/users", json=create_params)
    response2 = client.post("/users", json=create_params)

    assert response1.status_code == 200
    expected_response = {
        'detail': 
        {
            'entity_id': 123,
            'entity_name': 'UserInDB',
            'type': 'duplicate_entity'
        }
    }
    assert response2.status_code == 422
    assert response2.json() == expected_response


def test_get_user(client):
    create_params = {
        "id" : 1,
        "username": "Danny",
        "email": "deckergame.danny@gmail.com",
        "hashed_password": "fjdklsajtgeklsafdsa"
    } 

    client.post("/users", json=create_params)
    response = client.get("/users/1")
    assert response.status_code == 200

def test_get_user_response_v(client):
    create_params = {
        "id" : 1,
        "username": "Danny",
        "email": "deckergame.danny@gmail.com",
        "hashed_password": "fjdklsajtgeklsafdsa"
    } 

    client.post("/users", json=create_params)
    response = client.get("/users/1")
    expected_response = {
        "user": {
            "id": 1,
            "username": "Danny",
            "email": "deckergame.danny@gmail.com",
            "created_at": response.json()['user']['created_at']
        }
    }
    assert response.status_code == 200
    assert response.json() == expected_response

def test_get_not_found_user(client):
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


