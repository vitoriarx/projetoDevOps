import json
from main import app

def test_root_route():
    client = app.test_client()
    response = client.get("/")
    assert response.status_code == 200
    assert response.json == {"message": "API funcionando!"}

def test_get_users():
    client = app.test_client()
    response = client.get("/users")
    assert response.status_code == 200
    assert isinstance(response.json, list)

def test_create_user():
    client = app.test_client()
    payload = {
        "name": "Teste Usuário",
        "email": "teste@example.com"
    }

    response = client.post("/users", json=payload)
    assert response.status_code == 201
    assert response.json["name"] == "Teste Usuário"
