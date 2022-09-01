from typing import List
from app import schemas
import pytest


def test_get_all_posts(authorized_client, test_posts):
    res = authorized_client.get("/posts/")

    def validate(post):
        return schemas.PostCreate(**post)
    post_map = map(validate, res.json())
    assert len(res.json()) == len(test_posts)
    assert res.status_code == 200


# def test_unauthorized_get_all_posts(client, test_posts):
#     res = client.get("/posts/")
#     assert res.status_code == 401


# def test_unauthorized_get_one_post(client, test_posts):
#     res = client.get(f"/posts/{test_posts[0].id}")
#     assert res.status_code == 401
                          

# def test_get_unavailable_post(authorized_client, test_posts):
#     res = authorized_client.get("/posts/8888")
#     assert res.status_code == 404


# def test_get_one_post(authorized_client, test_posts):
#     res = authorized_client.get(f"/posts/{test_posts[0].id}")
#     print(res.json())
#     post = schemas.PostOut(**res.json())
#     assert post.Post.id ==test_posts[0].id
#     assert post.Post.title ==test_posts[0].title

#     assert res.status_code == 200

# @pytest.mark.parametrize("title, content, published", [ 
#     ("Dope title", "awesome new content", True),
#     ("Favorite Pizza", "I love pepporoni", False),
#     ("tallest skyscrapper", "I just want the money", True)
# ])


# def test_create_post(authorized_client, test_user, test_posts, title, content, published):
#     res = authorized_client.post("/posts/", 
#             json={"title": title, "content": content, "published": published})
    
#     created_post = schemas.PostResponse(**res.json())
#     assert res.status_code == 201
#     assert created_post.title ==  title
#     assert created_post.content ==  content
#     assert created_post.published ==  published
#     assert created_post.owner_id ==  test_user['id']

# def test_create_post_default_published_true(authorized_client, test_user, test_posts):
#     res = authorized_client.post(
#         "/posts/", json={"title": "arbitrary title", 
#                             "content": "aasdfjasdf"})
    
#     created_post = schemas.PostResponse(**res.json())
#     assert res.status_code == 201
#     assert created_post.title == "arbitrary title"
#     assert created_post.content ==  "aasdfjasdf"
#     assert created_post.published == True
#     assert created_post.owner_id ==  test_user['id']

# def test_unauthorized_user_create_post(client, test_user, test_posts):
#     res = client.post(
#         "/posts/", json={"title": "arbitrary title", "content": "aasdfjasdf"})
#     assert res.status_code == 401  

# def test_unauthorized_user_delete_post(client, test_user, test_posts):
#     res = client.delete(
#         f"/posts/{test_posts[0].id}")
#     assert res.status_code == 401

# def test_delete_post(authorized_client, test_user, test_posts):
#     res = authorized_client.delete(
#         f"/posts/{test_posts[0].id}")
#     assert res.status_code == 204

# def test_delete_post_non_exist(authorized_client, test_user, test_posts):
#     res = authorized_client.delete(
#         "/posts/80000")
#     assert res.status_code == 404

def test_delete_other_users_posts(authorized_client_2, test_user_2, test_posts):
    res = authorized_client_2.delete(
        f"/posts/{test_posts[0].id}")
    assert res.status_code == 403

# def test_update_post(authorized_client, test_user, test_posts):
#     data = {
#         "title": "Updated Title",
#         "content": "Upload Content",
#         "id": test_posts[0].id
#     }
#     res = authorized_client.put(f"/posts/{test_posts[0].id}", json=data)
#     updated_posts = schemas.PostResponse(**res.json())
#     assert res.status_code == 200
#     assert updated_posts.title == data["title"]
#     assert updated_posts.content == data["content"]

# def test_update_other_user_post(authorized_client, test_user, test_posts, test_user_2):
#     data = {
#         "title": "Updated Title",
#         "content": "Upload Content",
#         "id": test_posts[3].id
#     }
#     res = authorized_client.put(f"/posts/{test_posts[3].id}", json=data)
#     assert res.status_code == 403

# def test_unauthorized_user_update_post(client, test_user, test_posts):
#     res = client.put(
#         f"/posts/{test_posts[0].id}")
#     assert res.status_code == 401

# def test_update_post_non_exist(authorized_client, test_user, test_posts):
#     data = {
#         "title": "Updated Title",
#         "content": "Upload Content",
#         "id": test_posts[3].id
#     }
    
#     res = authorized_client.put(
#         "/posts/80000", json=data)

#     assert res.status_code == 404