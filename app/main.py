from random import randrange
from typing import Optional

from fastapi import Body, FastAPI, HTTPException, Response, status
from pkg_resources import require
from pydantic import BaseModel

app = FastAPI()


class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: Optional[int] = None  # or use 'rating: int | None'


my_posts = [
    {
        "title": "post title 1",
        "content": "post content 1",
        "published": True,
        "rating": 5,
        "id": 1,
    },
    {
        "title": "post title 2",
        "content": "post content 2",
        "published": False,
        "rating": 4,
        "id": 2,
    },
]


def find_post(id):
    for p in my_posts:
        if p["id"] == id:
            return p


def find_index(id):
    for i, p in enumerate(my_posts):
        if p["id"] == id:
            return i


# order of path operations matters. Be careful while defining paths
@app.get("/")
def root():
    return {"message": "Hello World!"}


@app.get("/posts")  # getting all posts
def get_all_posts():
    return {"data": my_posts}  # list will be serialized into a JSON object


@app.post(
    "/posts", status_code=status.HTTP_201_CREATED
)  # creating a new post, deafult status code
def create_posts(post: Post):
    # print(post)  # post is a pydantic model
    # print(post.dict())  # this is a python dict
    post_dict = post.dict()
    post_dict["id"] = randrange(0, 1000000)
    my_posts.append(post_dict)
    return {"data": post_dict}


@app.get("/posts/{id}")  # get a specific post
def get_post(id: int, response: Response):  # tweak the response
    required_post = find_post(id)
    if not required_post:
        # response.status_code = 404    #hardcoded
        # OR USE
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {"message": f"Post with id: {id} not found"}
        # OR USE BEST ONE
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with id: {id} not found",
        )

    return {"data": required_post}


@app.delete(
    "/posts/{id}", status_code=status.HTTP_204_NO_CONTENT
)  # delete a specific post
def delete_post(id: int):
    required_index = find_index(id)
    if not required_index:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with id: {id} not found",
        )
    del my_posts[required_index]
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.put("/posts/{id}")  # update a specific post using PUT
def update_post(id: int, post: Post):
    required_index = find_index(id)
    if not required_index:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with id: {id} not found",
        )
    print(post)
    post_dict = post.dict()
    post_dict["id"] = id
    my_posts[required_index] = post_dict
    return {"message": f"Post with id: {id} updated successfully"}
