import time
from random import randrange
from typing import List, Optional

import psycopg2
from fastapi import Body, Depends, FastAPI, HTTPException, Response, status
from psycopg2.extras import RealDictCursor  # to get column names for values retrived
from sqlalchemy.orm import Session

from . import models, schemas
from .database import engine, get_db

# connection is established and tables are created
models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# this is direct connection using psycopg without ORM
# while (
#     True
# ):  # try to connect regularly till connection is established, if failed to connect wait for some time and try again
#     try:
#         conn = psycopg2.connect(
#             host="localhost",
#             database="fcc-fastapi",
#             user="vpk",
#             password="vpk123#",
#             cursor_factory=RealDictCursor,
#         )  # bad practice to hardcode values, security issue + values can vary
#         cursor = conn.cursor()
#         print(f"Database connection was successful")
#         break
#     except Exception as error:
#         print(f"Connection to database failed")
#         print(f"Error: {error}")
#         time.sleep(2)  # wait for 2 secs before trying again

# my_posts = [
#     {
#         "title": "post title 1",
#         "content": "post content 1",
#         "published": True,
#         "rating": 5,
#         "id": 1,
#     },
#     {
#         "title": "post title 2",
#         "content": "post content 2",
#         "published": False,
#         "rating": 4,
#         "id": 2,
#     },
# ]


# def find_post(id):
#     for p in my_posts:
#         if p["id"] == id:
#             return p


# def find_index(id):
#     for i, p in enumerate(my_posts):
#         if p["id"] == id:
#             return i


# order of path operations matters. Be careful while defining paths
@app.get("/")
def root():
    return {"message": "Hello World!"}


# getting all posts, since we are getting list of posts, we type it as List[schemas.Post] for the pydantic to parse and shape it properly
# just using schemas.Post will make the pydantic to shape the list of posts as a single post and hence error
@app.get("/posts", response_model=List[schemas.Post])
def get_all_posts(db: Session = Depends(get_db)):
    # cursor.execute("""SELECT * FROM posts;""")
    # all_posts = cursor.fetchall()  # fetch all posts from the query
    # print(all_posts)
    all_posts = db.query(models.Post).all()
    return all_posts


# creating a new post, deafult status code
@app.post("/posts", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
def create_posts(post: schemas.PostCreate, db: Session = Depends(get_db)):
    # cursor.execute(
    #     """INSERT INTO posts (p_title, p_content, published) VALUES (%s, %s, %s) RETURNING *""",
    #     (post.title, post.content, post.published),
    # )  # while inserting we parameterise and put values taken from request body into it. Even f-string can work but it is vulnerable to sql injection attacks.
    # new_post = cursor.fetchone()
    # conn.commit()  # commit the staged changes to finalise, very important

    # if we have very large number of columns, it is tiresome to extract fields like this so convert the request to dict and unpack it.
    # new_post = models.Post(
    #     p_title=post.title, p_content=post.content, published=post.published
    # )
    new_post = models.Post(
        **post.dict()
    )  # creating an instance of Post class in models module
    db.add(new_post)
    db.commit()
    db.refresh(new_post)  # retrieve the created post
    return new_post


@app.get("/posts/{id}", response_model=schemas.Post)  # get a specific post
def get_post(id: int, db: Session = Depends(get_db)):  # tweak the response
    # cursor.execute(
    #     """SELECT * FROM posts WHERE p_id = %s""", (str(id),)
    # )  # extra comma means its a tuple
    # specific_post = cursor.fetchone()

    specific_post = db.query(models.Post).filter(models.Post.p_id == id).first()
    if not specific_post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"post with id: {id} not found",
        )
    return specific_post


@app.delete(
    "/posts/{id}", status_code=status.HTTP_204_NO_CONTENT
)  # delete a specific post
def delete_post(id: int, db: Session = Depends(get_db)):
    # cursor.execute("""DELETE FROM posts WHERE p_id = %s RETURNING *""", (str(id),))
    # deleted_post = cursor.fetchone()
    # conn.commit()  # commit the changes

    # this is the query to get the post wrt to id
    deleted_post_query = db.query(models.Post).filter(models.Post.p_id == id)
    if not deleted_post_query.first():  # here we check if the post is found or not
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with id: {id} doesn't exist",
        )

    # here we call delete function on the post query to delete the post with id
    deleted_post_query.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.put("/posts/{id}", response_model=schemas.Post)  # update a specific post using PUT
def update_post(id: int, post: schemas.PostCreate, db: Session = Depends(get_db)):
    # cursor.execute(
    #     """UPDATE posts SET p_title = %s, p_content = %s WHERE p_id = %s RETURNING *""",
    #     (post.title, post.content, str(id)),
    # )
    # updated_post = cursor.fetchone()
    # conn.commit()  # commit changes

    # this is the query to get the post wrt to id
    updated_post_query = db.query(models.Post).filter(models.Post.p_id == id)
    if not updated_post_query.first():  # here we check if the post is found or not
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with id: {id} not found",
        )

    # call update function on query and pass request body to update the fields
    updated_post_query.update(post.dict(), synchronize_session=False)
    db.commit()

    # query to get the updated post
    return updated_post_query.first()
