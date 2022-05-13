from fastapi import status
from typing import List
import pytest
from app import schemas
from tests.conftest import test_user

def test_get_all_posts(authorized_client, test_posts):
    res = authorized_client.get("/posts/")

    def validate(post):
        return schemas.PostResponse(**post)
    
    posts_map = map(validate, res.json())
    posts_list = list(posts_map)
    
    assert len(res.json()) == len(test_posts)
    assert res.status_code == status.HTTP_200_OK

def test_unauthorized_user_get_all_posts(client, test_posts):
    res = client.get(f"/posts/{test_posts[0].id}")
    assert res.status_code == status.HTTP_401_UNAUTHORIZED

def test_unauthorized_user_get_one_all_posts(client, test_posts):
    res = client.get("/posts/")
    assert res.status_code == status.HTTP_401_UNAUTHORIZED

def test_get_one_post_not_exist(authorized_client, test_posts):
    res = authorized_client.get("/posts/283344")
    assert res.status_code == status.HTTP_404_NOT_FOUND

def test_get_one_post(authorized_client, test_posts):
    res = authorized_client.get(f"/posts/{test_posts[0].id}")
    post = schemas.PostResponse(**res.json())
    assert res.status_code == status.HTTP_200_OK
    assert post.Post.id == test_posts[0].id
    assert post.Post.content == test_posts[0].content
    assert post.Post.creation_date == test_posts[0].creation_date

@pytest.mark.parametrize("title, content, published", [
    ("awesome new title", "awesome new content", True),
    ("favorite pizza", "I love pepperoni", False),
    ("Blockchain", "A decentralized technology", True)
])
def test_create_post(authorized_client, test_user, test_posts, title, content, published):
    res = authorized_client.post("/posts/", json={"title": title, "content": content, "published": published})
    post = schemas.Post(**res.json())
    assert res.status_code == status.HTTP_201_CREATED
    assert post.title == title
    assert post.content == content
    assert post.published == published
    assert post.user_id == test_user["id"]

def test_create_post_default_published_true(authorized_client, test_user, test_posts):
    res = authorized_client.post("/posts/", json={"title": "some title", "content": "some content"})
    post = schemas.Post(**res.json())
    assert res.status_code == status.HTTP_201_CREATED
    assert post.title == "some title"
    assert post.content == "some content"
    assert post.published == True
    assert post.user_id == test_user["id"]

def test_unauthorized_user_create_post(client, test_posts):
    res = client.post("/posts/", json={"title": "some title", "content": "some content"})
    assert res.status_code == status.HTTP_401_UNAUTHORIZED

def test_unauthorized_user_delete_post(client, test_posts):
    res = client.delete(f"/posts/{test_posts[0].id}")
    assert res.status_code == status.HTTP_401_UNAUTHORIZED

def test_delete_post_success(authorized_client, test_user, test_posts):
    res = authorized_client.delete(f"/posts/{test_posts[0].id}")
    assert res.status_code == status.HTTP_204_NO_CONTENT

def test_delete_post_not_exist(authorized_client, test_user, test_posts):
    res = authorized_client.delete(f"/posts/293039")
    assert res.status_code == status.HTTP_404_NOT_FOUND

def test_delete_other_user_post(authorized_client, test_user, test_posts):
    res = authorized_client.delete(f"/posts/{test_posts[4].id}")
    assert res.status_code == status.HTTP_401_UNAUTHORIZED

def test_update_post(authorized_client, test_user, test_posts):
    data = {
        "title": "updated title",
        "content": "updated content",
        "id": test_posts[0].id
    }
    res = authorized_client.put(f"/posts/{test_posts[0].id}", json = data)
    updated_post = schemas.Post(**res.json())
    assert updated_post.title == data["title"]
    assert updated_post.content == data["content"]
    assert res.status_code == status.HTTP_200_OK

def test_update_other_user_post(authorized_client, test_user, test_user2, test_posts):
    data = {
        "title": "updated title",
        "content": "updated content",
        "id": test_posts[0].id
    }
    res = authorized_client.put(f"/posts/{test_posts[4].id}", json = data)
    assert res.status_code == status.HTTP_401_UNAUTHORIZED

def test_nonauthorized_user_update_post(client, test_user, test_posts):
    res = client.put(f"/posts/{test_posts[0].id}")
    assert res.status_code == status.HTTP_401_UNAUTHORIZED

def test_delete_post_not_exist(authorized_client, test_user, test_posts):
    data = {
        "title": "updated title",
        "content": "updated content",
        "id": test_posts[0].id
    }
    res = authorized_client.put(f"/posts/293039", json = data)
    assert res.status_code == status.HTTP_404_NOT_FOUND