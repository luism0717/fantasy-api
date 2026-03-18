def test_register_user(client):
    # Resiter User
    response = client.post("/auth/register", json={"username": "luis", "email": "luis@test.com", "password": "test123"})
    assert response.status_code == 201

def test_register_duplicate_email(client):
    client.post("/auth/register", json={"username": "luis", "email": "luis@test.com", "password": "test123"})
    second_response = client.post("/auth/register", json={"username": "luis", "email": "luis@test.com", "password": "test123"})
    assert second_response.status_code == 400

def test_login_success(client):
    client.post("/auth/register", json={"username": "luis", "email": "luis@test.com", "password": "test123"})
    # Login to get a token
    login = client.post("/auth/login", data={"username": "luis", "password": "test123"})
    assert login.status_code == 200

def test_login_wrong_password(client):
    client.post("/auth/register", json={"username": "luis", "email": "luis@test.com", "password": "test123"})
    login = client.post("/auth/login", data={"username": "luis", "password": "test1234"})
    assert login.status_code == 401