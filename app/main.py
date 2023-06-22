import time
from random import randrange
from typing import Optional

import psycopg2
from fastapi import Body, FastAPI, HTTPException, Response, status
from psycopg2.extras import RealDictCursor  # to get column names for values retrived
from pydantic import BaseModel

app = FastAPI()


class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: Optional[int] = None  # or use 'rating: int | None'


while (
    True
):  # try to connect regularly till connection is established, if failed to connect wait for some time and try again
    try:
        conn = psycopg2.connect(
            host="localhost",
            database="fcc-fastapi",
            user="vpk",
            password="vpk123#",
            cursor_factory=RealDictCursor,
        )  # bad practice to hardcode values, security issue + values can vary
        cursor = conn.cursor()
        print(f"Database connection was successful")
        break
    except Exception as error:
        print(f"Connection to database failed")
        print(f"Error: {error}")
        time.sleep(2)  # wait for 2 secs before trying again

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
    cursor.execute("""SELECT * FROM posts;""")
    all_posts = cursor.fetchall()  # fetch all posts from the query
    print(all_posts)
    return {"data": all_posts}


@app.post(
    "/posts", status_code=status.HTTP_201_CREATED
)  # creating a new post, deafult status code
def create_posts(post: Post):
    cursor.execute(
        """INSERT INTO posts (p_title, p_content, published) VALUES (%s, %s, %s) RETURNING *""",
        (post.title, post.content, post.published),
    )  # while inserting we parameterise and put values taken from request body into it. Even f-string can work but it is vulnerable to sql injection attacks.
    new_post = cursor.fetchone()
    conn.commit()  # commit the staged changes to finalise, very important
    return {"data": new_post}


@app.get("/posts/{id}")  # get a specific post
def get_post(id: int):  # tweak the response
    cursor.execute(
        """SELECT * FROM posts WHERE p_id = %s""", (str(id),)
    )  # extra comma means its a tuple
    specific_post = cursor.fetchone()
    if not specific_post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"post with id: {id} not found",
        )
    return {"data": specific_post}


@app.delete(
    "/posts/{id}", status_code=status.HTTP_204_NO_CONTENT
)  # delete a specific post
def delete_post(id: int):
    cursor.execute("""DELETE FROM posts WHERE p_id = %s RETURNING *""", (str(id),))
    deleted_post = cursor.fetchone()
    if not deleted_post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with id: {id} doesn't exist",
        )
    conn.commit()  # commit the changes
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.put("/posts/{id}")  # update a specific post using PUT
def update_post(id: int, post: Post):
    cursor.execute(
        """UPDATE posts SET p_title = %s, p_content = %s WHERE p_id = %s RETURNING *""",
        (post.title, post.content, str(id)),
    )
    updated_post = cursor.fetchone()
    if not updated_post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with id: {id} not found",
        )
    conn.commit()  # commit changes
    return {"message": f"Post with id: {id} updated successfully", "data": updated_post}
