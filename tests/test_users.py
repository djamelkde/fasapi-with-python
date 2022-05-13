import pytest
from app import schemas
from jose import jwt
from app.config import settings
from fastapi import status


def test_root(client):
    response = client.get("/")
    print(response.json().get("message"))
    assert response.json().get("message") == "Simple FastAPI with Python3"
    assert response.status_code == status.HTTP_200_OK

def test_create_user(client):
    response = client.post("/users/", json = {"email": "test1@gmail.com", "password": "password1"})
    new_user = schemas.UserResponse(**response.json())
    assert  new_user.email == "test1@gmail.com"
    assert response.status_code == status.HTTP_201_CREATED

def test_login_user(test_user, client):
    response = client.post("/login", data={"username": test_user["email"], "password": test_user["password"]})
    login_res = schemas.Token(**response.json())
    #verify that the token is valid
    payload = jwt.decode(login_res.access_token, settings.secret_key, algorithms=[settings.algorithm])
    id = payload.get("user_id")
    assert id == test_user["id"]
    assert login_res.token_type == "bearer"
    assert response.status_code == status.HTTP_200_OK

@pytest.mark.parametrize("attempted_email, attempted_password, status_code", [
    ("hello@gmail.com", "password1", 403),
    ("test@gmail.com", "password1234", 403),
    ("wrongemail@yahoo.com", "wrongpassword", 403),
    (None, "password123", 422),
    ("test1@gmail.com", None, 422)
])
def test_incorrect_login(attempted_email, attempted_password, status_code, test_user, client):
    res = client.post("/login", data={"username": attempted_email, "password": attempted_password})
    #login_res = 
    assert res.status_code == status_code