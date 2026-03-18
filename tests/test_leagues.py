def test_create_league_unauthenticated(client):
    response = client.post("/leagues/", json={"name": "Test", "sport": "test", "max_teams": 8})
    assert response.status_code == 401

def test_create_league(client):
    # Resiter User
    client.post("/auth/register", json={"username": "luis", "email": "luis@test.com", "password": "test123"})
    # Login to get a token
    login = client.post("/auth/login", data={"username": "luis", "password": "test123"})
    token = login.json()["access_token"]
    # Use the token
    headers = {"Authorization": f"Bearer {token}"}
    response = client.post("/leagues/", json={"name": "Test", "sport": "test", "max_teams": 8}, headers=headers)
    assert response.status_code == 201

def test_get_leagues(client):
    response = client.get("/leagues/")
    assert response.status_code == 200

def test_get_league_not_found(client):
    response = client.get("/leagues/999")
    assert response.status_code == 404

def test_join_league(client):
    # Resiter User
    client.post("/auth/register", json={"username": "luis", "email": "luis@test.com", "password": "test123"})
    # Login to get a token
    login = client.post("/auth/login", data={"username": "luis", "password": "test123"})
    token = login.json()["access_token"]
    # Use the token
    headers = {"Authorization": f"Bearer {token}"}
    league = client.post("/leagues/", json={"name": "Test", "sport": "test", "max_teams": 8}, headers=headers)
    invite_code = league.json()["invite_code"]
    response = client.post("/leagues/1/join", json={"name": "My Team", "invite_code": invite_code}, headers=headers)
    assert response.status_code == 201
