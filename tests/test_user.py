from app.models.user import UserCreate
from app.utils.user import create_user_in_db

def test_signup(client):
    """
    Tests user registration is sucessful
    """
    response = client.post(
        "/register", 
        json = {
            "name": "test user", 
            "email": "testuser@example.com", 
            "password": "password123"
            }
    )
    assert response.status_code == 200
    body = response.json()

    assert "access_token" in body
    assert body["token_type"] == "bearer"

def test_signup_existing_user(client,test_user):
    """
    Tests user registration of already existing user
    is not sucessful
    """
    response = client.post(
        "/register", 
        json = {
            "name": test_user.name, 
            "email": test_user.email, 
            "password": "password123"
            }
    )

    assert response.status_code == 400
    assert response.json() == {"detail": "Email already registered"}

def test_login_sucess(client, test_user):
    """
    Tests user login is sucessful with valid
    user credentials
    """

    response = client.post(
        "/login",
        data={
            "username": test_user.email,
            "password": "password123"
        }
    )

    assert response.status_code == 200

    body = response.json()

    assert "access_token" in body
    assert body["token_type"] == "bearer"

def test_login_failure(client, test_user):
    """
    Tests login fails with wrong password
    """

    response = client.post(
        "/login",
        data ={
            "username": test_user.email,
            "password": "wrongpassword"
        }
    )

    assert response.status_code == 401