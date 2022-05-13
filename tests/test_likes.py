from fastapi import status
import pytest
from app import models


@pytest.fixture
def test_like(test_posts, session, test_user):
    new_like = models.Like(post_id=test_posts[4].id, user_id=test_user["id"])
    session.add(new_like)
    session.commit()


def test_like_on_post(authorized_client, test_posts):
    res = authorized_client.post("/likes/", json = {"post_id": test_posts[0].id, "dir":1})
    assert res.status_code == status.HTTP_201_CREATED

def test_like_twice_post(authorized_client, test_posts , test_like):
    res = authorized_client.post("/likes/", json={"post_id": test_posts[4].id, "dir":1})
    assert res.status_code == status.HTTP_409_CONFLICT

def test_delete_like(authorized_client, test_posts , test_like):
    res = authorized_client.post("/likes/", json={"post_id": test_posts[4].id, "dir":0})
    assert res.status_code == status.HTTP_201_CREATED

def test_delete_like_non_exist(authorized_client, test_posts , test_like):
    res = authorized_client.post("/likes/", json={"post_id": test_posts[0].id, "dir":0})
    assert res.status_code == status.HTTP_404_NOT_FOUND

def test_like_post_non_exit(authorized_client, test_like):
    res = authorized_client.post("/likes/", json = {"post_id": 1232, "dir":0})
    assert res.status_code == status.HTTP_404_NOT_FOUND

def test_nonauthorized_client_like_post(client, test_posts, test_like):
    res = client.post("/likes/", json={"post_id": test_posts[0].id, "dir":1})
    assert res.status_code == status.HTTP_401_UNAUTHORIZED