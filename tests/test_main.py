import json
from unittest.mock import patch
from app.main import app

def test_root_route():
    client = app.test_client()
    response = client.get("/")
    assert response.status_code == 200
    assert response.json == {"message": "API funcionando!"}

def test_get_users():
    # mocka a função fetch_users que está em app.main
    fake_users = [{"id": 1, "name": "Teste Usuário", "email": "teste@example.com"}]
    with patch("app.main.fetch_users", return_value=fake_users):
        client = app.test_client()
        response = client.get("/users")
        assert response.status_code == 200
        assert isinstance(response.json, list)
        assert response.json == fake_users

def test_create_user():
    # mocka insert_user para não usar o DB real
    with patch("app.main.insert_user", return_value=42) as mock_insert:
        client = app.test_client()
        payload = {"name": "Teste Usuário", "email": "teste@example.com"}
        response = client.post("/users", json=payload)
        assert response.status_code == 201
        assert response.json["name"] == "Teste Usuário"
        assert response.json["email"] == "teste@example.com"
        assert response.json["id"] == 42
        mock_insert.assert_called_once_with("Teste Usuário", "teste@example.com")
