from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_get_players(client):
    response = client.get("/players/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_get_player_not_found(client):
    # GET /players/999 should return 404
    response = client.get("/players/999")
    assert response.status_code == 404

def test_create_player_unauthenticated(client):
    # POST /players without a token should return 401
    response = client.post("/players/", json={"name": "Test", "position": "QB", "nfl_team": "Test Team"})
    assert response.status_code == 401

def test_create_player(client):
    # POST /players with valid data should return 201
    # Resiter User
    client.post("/auth/register", json={"username": "luis", "email": "luis@test.com", "password": "test123"})
    # Login to get a token
    login = client.post("/auth/login", data={"username": "luis", "password": "test123"})
    token = login.json()["access_token"]
    # Use the token
    headers = {"Authorization": f"Bearer {token}"}
    response = client.post("/players/", json={"name": "Test", "position": "QB", "nfl_team": "Test Team"}, headers=headers)
    assert response.status_code == 201

