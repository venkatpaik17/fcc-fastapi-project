from typing import List

from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy import func
from sqlalchemy.orm import Session

from .. import models, oauth2, schemas
from ..database import get_db

# create a router instance
router = APIRouter(prefix="/posts", tags=["Posts"])


# getting all posts, since we are getting list of posts, we type it as List[schemas.Post] for the pydantic to parse and shape it properly
# just using schemas.Post will make the pydantic to shape the list of posts as a single post and hence error
@router.get(
    "/", response_model=List[schemas.PostOut]
)  # schemas.Post as response_model if posts without votes
def get_all_posts(
    db: Session = Depends(get_db),
    user_id: schemas.TokenData = Depends(oauth2.get_current_user),
    limit: int = 3,
    skip: int = 0,
    search: str = "",
):
    # getting all posts without votes
    # all_posts = (
    #     db.query(models.Post)
    #     .filter(
    #         models.Post.p_title.contains(search)
    #     )  # can use any str function here to get desired the response
    #     .limit(limit)
    #     .offset(skip)
    #     .all()
    # )

    # get all posts with votes
    # join posts and votes table, group by post id and get number of votes for each post using count function
    # by default sqlalchemy performs inner join
    # SELECT posts.*, COUNT(votes.post_id) as No_of_votes FROM posts LEFT JOIN votes ON posts.p_id = votes.post_id GROUP BY posts.p_id;
    all_posts = (
        (
            db.query(models.Post, func.count(models.Vote.post_id).label("votes"))
            .join(models.Vote, models.Post.p_id == models.Vote.post_id, isouter=True)
            .group_by(models.Post.p_id)
        )
        .filter(models.Post.p_title.contains(search))
        .limit(limit)
        .offset(skip)
        .all()
    )
    return all_posts  # response format is slightly different so we need to change the response model in schemas.py and update response_model parameter


# creating a new post, deafult status code
# we check whether user is logged in or not using the get_current_user dependency
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
def create_posts(
    post: schemas.PostCreate,
    db: Session = Depends(get_db),
    user_id: schemas.TokenData = Depends(oauth2.get_current_user),
):
    # if we have very large number of columns, it is tiresome to extract fields like this so convert the request to dict and unpack it.
    # new_post = models.Post(
    #     p_title=post.title, p_content=post.content, published=post.published
    # )

    # from token data get id of the logged in user and add it as owner_id in posts table for this new post
    # creating an instance of Post class in models module
    new_post = models.Post(owner_id=user_id.u_id, **post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)  # retrieve the created post
    return new_post


# get a specific post, tweak the response
@router.get(
    "/{id}", response_model=schemas.PostOut
)  # schemas.Post as response_model if posts without votes
def get_post(
    id: int,
    db: Session = Depends(get_db),
    user_id: schemas.TokenData = Depends(oauth2.get_current_user),
):
    # get specific post without votes
    # specific_post = db.query(models.Post).filter(models.Post.p_id == id).first()

    # get specific post with votes (join, groupby, count)
    specific_post = (
        (
            db.query(models.Post, func.count(models.Vote.post_id).label("votes"))
            .join(models.Vote, models.Post.p_id == models.Vote.post_id, isouter=True)
            .group_by(models.Post.p_id)
        )
        .filter(models.Post.p_id == id)
        .first()
    )
    if not specific_post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"post with id: {id} not found",
        )
    return specific_post


# delete a specific post
@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(
    id: int,
    db: Session = Depends(get_db),
    user_id: schemas.TokenData = Depends(oauth2.get_current_user),
):
    # this is the query to get the post wrt to id
    deleted_post_query = db.query(models.Post).filter(models.Post.p_id == id)
    post_to_be_deleted = deleted_post_query.first()
    if not post_to_be_deleted:  # here we check if the post is found or not
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with id: {id} doesn't exist",
        )
    # check to make sure the post is deleted by its owner only.
    if post_to_be_deleted.owner_id != user_id.u_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"Not authorized to perform the requested action",
        )
    # here we call delete function on the post query to delete the post with id
    deleted_post_query.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)


# update a specific post using PUT
@router.put("/{id}", response_model=schemas.Post)
def update_post(
    id: int,
    post: schemas.PostCreate,
    db: Session = Depends(get_db),
    user_id: schemas.TokenData = Depends(oauth2.get_current_user),
):
    # this is the query to get the post wrt to id
    updated_post_query = db.query(models.Post).filter(models.Post.p_id == id)
    post_to_be_updated = updated_post_query.first()
    if not post_to_be_updated:  # here we check if the post is found or not
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with id: {id} not found",
        )
    # check to make sure the post is updated by owner only.
    if post_to_be_updated.owner_id != user_id.u_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"Not authorized to perform the requested action",
        )

    # call update function on query and pass request body to update the fields
    updated_post_query.update(post.dict(), synchronize_session=False)
    db.commit()

    # query to get the updated post
    return updated_post_query.first()
