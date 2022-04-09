from email.quoprimime import body_length
import json
from typing import Optional
from fastapi import FastAPI, Response, status, HTTPException
from fastapi.params import Body
from pydantic import BaseModel
import itertools

# to start fastapi server at command enter the below
# uvicorn <name_of_file_server_is_in>:<name_of_server_variable> --reload
# eg: uvicorn main:app --reload
# --reload restarts server when code is changed and saved.
# DO NOT USE IT IN PRODUCTION.
app = FastAPI()


class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: Optional[int] = None


my_posts_id = itertools.count(start=1, step=1)
my_posts = [
    {
        "id": next(my_posts_id),
        "title": "Title of post 1",
        "content": "Content for post 1",
    },
    {
        "id": next(my_posts_id),
        "title": "Title of post 2",
        "content": "Content for post 2",
    },
]


@app.get("/posts/latest")
def get_latest_post():
    post = my_posts[len(my_posts) - 1]
    return {"data": post}


@app.get("/posts/{id}")
def get_post(id: int, response: Response):
    found_post = list(filter(lambda post: post["id"] == id, my_posts))
    post = found_post[0] if len(found_post) > 0 else ""
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Resource with id {id} does not exist",
        )
    return {"data": post}


@app.put("/posts/{id}")
def update_post(id: int, post: Post, response: Response):
    global my_posts
    update_index = next(
        (index for index in range(len(my_posts)) if my_posts[index]["id"] == id), None
    )
    if update_index is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Resource with id {id} does not exist",
        )
    post_dict = post.dict()
    post_dict["id"] = id
    my_posts[update_index] = post_dict
    return {"data": post_dict}


@app.delete("/posts/{id}")
def delete_post(id: int):
    global my_posts
    delete_post = list(filter(lambda post: post["id"] == id, my_posts))
    post = delete_post[0] if len(delete_post) > 0 else ""
    if post:
        my_posts = list(filter(lambda post: post["id"] != id, my_posts))
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Resource with id {id} does not exist",
        )
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.get("/posts")
def get_posts():
    return {"data": my_posts}


@app.post("/posts")
def create_post(post: Post, response: Response):
    post_dict = post.dict()
    post_dict["id"] = next(my_posts_id)
    my_posts.append(post_dict)
    response.status_code = status.HTTP_201_CREATED
    return {"data": post_dict}


@app.get("/")
def root():
    return {"message": "Demo Social API!"}
