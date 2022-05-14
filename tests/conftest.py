from fastapi.testclient import TestClient
from app.main import app
from app import models, schemas
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from app.config import settings
from app.database import get_db, Base
import pytest
from app.OAuth2 import create_access_token
from app import models


SQLALCHEMY_DATABASE_URL = f"postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}_test"
engine = create_engine(SQLALCHEMY_DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(scope="function")
def session():
    print(SQLALCHEMY_DATABASE_URL)
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

@pytest.fixture(scope="function")
def client(session):
    def override_get_db():
        try:
            yield session
        finally:
            session.close()
    app.dependency_overrides[get_db] = override_get_db   
    yield TestClient(app)

@pytest.fixture
def test_user2(client):
    user_data = {"email": "test2@gmail.com", "password":"password2"}
    res = client.post("/users/", json=user_data)
    assert res.status_code == 201
    new_user = res.json()
    new_user["password"] = user_data["password"]
    return new_user

@pytest.fixture
def test_user(client):
    user_data = {"email": "test1@gmail.com", "password":"password1"}
    res = client.post("/users/", json=user_data)
    assert res.status_code == 201
    new_user = res.json()
    new_user["password"] = user_data["password"]
    return new_user

@pytest.fixture
def token(test_user):
    return create_access_token({"user_id": test_user["id"]})

@pytest.fixture
def authorized_client(client, token):
    client.headers = {
        **client.headers,
        "Authorization": f"Bearer {token}"
    }
    return client

@pytest.fixture
def test_posts(test_user, session, test_user2):
    posts_data = [
        {
            "title": "title 1",
            "content": "some content 1",
            "user_id": test_user['id']
        },
        {
            "title": "title 2",
            "content": "some content 2",
            "user_id": test_user['id']
        },
        {
            "title": "title 3",
            "content": "some content 3",
            "user_id": test_user['id']
        },
        {
            "title": "title 4",
            "content": "some content 4",
            "user_id": test_user['id']
        },
        {
            "title": "title 5",
            "content": "some content 5",
            "user_id": test_user2['id']
        }
    ]
    def create_post_map(post):
        return models.Post(**post)
    posts_map = map(create_post_map, posts_data)
    posts = list(posts_map)
    session.add_all(posts)
    session.commit()

    posts = session.query(models.Post).all()
    return posts