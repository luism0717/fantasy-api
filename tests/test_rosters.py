def test_add_to_roster_unauthenticated(client):
    reponse = client.post("/rosters/", json={"team_id": 1, "player_id": 1})
    assert reponse.status_code == 401

def test_add_to_roster(client):
    # Resiter User
    client.post("/auth/register", json={"username": "luis", "email": "luis@test.com", "password": "test123"})
    # Login to get a token
    login = client.post("/auth/login", data={"username": "luis", "password": "test123"})
    token = login.json()["access_token"]
    # Use the token
    headers = {"Authorization": f"Bearer {token}"}
    # Create a player
    player = client.post("/players/", json={"name": "Test", "position": "QB", "nfl_team": "Test Team"}, headers=headers)
    # Create a league
    league = client.post("/leagues/", json={"name": "Test", "sport": "nfl", "max_teams": 8}, headers=headers)
    invite_code = league.json()["invite_code"]
    # Join the league to create a team
    team =  client.post("/leagues/1/join", json={"name": "My Team", "invite_code": invite_code}, headers=headers)
    # Now add player to roster using real ids
    response = client.post("/rosters/", json={"team_id": team.json()["id"], "player_id": player.json()["id"]}, headers=headers)
    assert response.status_code == 201

def test_add_duplicate_player_to_roster(client):
    # Resiter User
    client.post("/auth/register", json={"username": "luis", "email": "luis@test.com", "password": "test123"})
    # Login to get a token
    login = client.post("/auth/login", data={"username": "luis", "password": "test123"})
    token = login.json()["access_token"]
    # Use the token
    headers = {"Authorization": f"Bearer {token}"}
    # Create a player
    player = client.post("/players/", json={"name": "Test", "position": "QB", "nfl_team": "Test Team"}, headers=headers)
    # Create a league
    league = client.post("/leagues/", json={"name": "Test", "sport": "nfl", "max_teams": 8}, headers=headers)
    invite_code = league.json()["invite_code"]
    # Join the league to create a team
    team =  client.post("/leagues/1/join", json={"name": "My Team", "invite_code": invite_code}, headers=headers)
    # Now add player to roster using real ids
    client.post("/rosters/", json={"team_id": team.json()["id"], "player_id": player.json()["id"]}, headers=headers)
    response = client.post("/rosters/", json={"team_id": team.json()["id"], "player_id": player.json()["id"]}, headers=headers)
    assert response.status_code == 400

def test_get_roster(client):
    response = client.get("/rosters/1")
    assert response.status_code == 200